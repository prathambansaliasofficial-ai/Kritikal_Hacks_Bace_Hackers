from __future__ import annotations

import httpx

from app.core.config import get_settings
from app.core.db import db_connection

TERMINAL_STATES = ("SETTLED", "REFUNDED")


class SettlementError(Exception):
    def __init__(self, detail: str, status_code: int = 502):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


async def apply_decision(order: dict, decision: str) -> dict:
    """Apply a trade decision to the escrow chain.

    APPROVED -> settle, REJECTED -> refund, NEEDS_REVIEW -> no-op.
    Returns the updated order dict. Idempotent on terminal states.
    Raises SettlementError (502) on middleware/chain failure; state unchanged.
    """
    if order["state"] in TERMINAL_STATES:
        return order

    if decision == "NEEDS_REVIEW":
        return order

    if decision == "APPROVED":
        endpoint = "/escrow/settle"
        new_state = "SETTLED"
    elif decision == "REJECTED":
        endpoint = "/escrow/refund"
        new_state = "REFUNDED"
    else:
        return order

    settings = get_settings()
    url = f"{settings.middleware_url.rstrip('/')}{endpoint}"
    body = {"orderId": order["chain_order"]}

    try:
        async with httpx.AsyncClient(
            timeout=settings.middleware_timeout_seconds
        ) as client:
            response = await client.post(url, json=body)
    except httpx.RequestError as error:
        raise SettlementError(str(error)) from error

    if response.status_code >= 400:
        raise SettlementError(
            f"Chain error ({response.status_code}): {response.text}"
        )

    result = response.json()
    tx_hash = result.get("txHash") or result.get("tx_hash")

    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE orders
                SET state = %s, tx_hash = %s, updated_at = now()
                WHERE id = %s
                RETURNING id, listing_id, buyer_wallet, seller_wallet, amount_wei,
                          state, chain_order, tx_hash, evidence_hash, created_at,
                          updated_at
                """,
                (new_state, tx_hash, order["id"]),
            )
            return cursor.fetchone()
