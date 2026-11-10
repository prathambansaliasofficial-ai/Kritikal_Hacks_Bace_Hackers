from __future__ import annotations

import re
from typing import Any

from app.core.db import db_connection
from app.repositories.base import fetch_one
from app.services.chain import keccak256

BYTES32_RE = re.compile(r"^0x[a-fA-F0-9]{64}$")
CHAIN_ORDER_PREFIX = "landmarket-order:"


class OrderError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def _row_dict(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return dict(row)


def is_valid_bytes32(value: str) -> bool:
    return bool(BYTES32_RE.fullmatch(value))


def get_listing(listing_id: int) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT id, bundle_id, ulpin, seller_wallet, price_wei, status, created_at
        FROM listings
        WHERE id = %s
        """,
        (listing_id,),
    )


def get_user(wallet_address: str) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT id, wallet_address, role, kyc_status, created_at, updated_at
        FROM users
        WHERE wallet_address = %s
        """,
        (wallet_address,),
    )


def get_order(order_id: int) -> dict[str, Any] | None:
    return _row_dict(
        fetch_one(
            """
            SELECT id, listing_id, buyer_wallet, seller_wallet, amount_wei, state,
                   chain_order, tx_hash, evidence_hash, created_at, updated_at
            FROM orders
            WHERE id = %s
            """,
            (order_id,),
        )
    )


def create_order(listing_id: int, buyer_wallet: str) -> dict[str, Any]:
    listing = get_listing(listing_id)
    if listing is None:
        raise OrderError(404, "Listing not found")
    if listing["status"] != "LISTED":
        raise OrderError(409, "Listing is not LISTED")

    buyer = get_user(buyer_wallet)
    if buyer is None:
        raise OrderError(404, "Buyer not found")
    if buyer["kyc_status"] != "VERIFIED":
        raise OrderError(409, "Buyer KYC not VERIFIED")

    if buyer_wallet == listing["seller_wallet"]:
        raise OrderError(409, "Buyer cannot be the seller")

    try:
        amount = int(listing["price_wei"])
    except (TypeError, ValueError) as error:
        raise OrderError(422, "Invalid listing price") from error

    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO orders (listing_id, buyer_wallet, seller_wallet,
                                    amount_wei, state)
                VALUES (%s, %s, %s, %s, 'CREATED')
                RETURNING id, listing_id, buyer_wallet, seller_wallet, amount_wei,
                          state, chain_order, tx_hash, evidence_hash, created_at,
                          updated_at
                """,
                (listing_id, buyer_wallet, listing["seller_wallet"], amount),
            )
            return _row_dict(cursor.fetchone())


def fund_order(
    order_id: int, chain_order_id: str, tx_hash: str
) -> dict[str, Any] | None:
    order = get_order(order_id)
    if order is None:
        return None
    if order["state"] != "CREATED":
        raise OrderError(409, "Order is not CREATED")

    if not is_valid_bytes32(chain_order_id):
        raise OrderError(422, "chain_order_id must be 0x + 64 hex chars")
    if not is_valid_bytes32(tx_hash):
        raise OrderError(422, "tx_hash must be 0x + 64 hex chars")

    expected = keccak256(
        f"{CHAIN_ORDER_PREFIX}{order_id}".encode()
    )
    if chain_order_id.lower() != expected.lower():
        raise OrderError(422, "chain_order_id does not match the order")

    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE orders
                SET state = 'FUNDED', chain_order = %s, tx_hash = %s,
                    updated_at = now()
                WHERE id = %s AND state = 'CREATED'
                RETURNING id, listing_id, buyer_wallet, seller_wallet, amount_wei,
                          state, chain_order, tx_hash, evidence_hash, created_at,
                          updated_at
                """,
                (chain_order_id, tx_hash, order_id),
            )
            row = cursor.fetchone()
            return _row_dict(row)
