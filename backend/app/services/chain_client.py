from __future__ import annotations

import httpx

from app.core.config import get_settings


class ChainClientError(Exception):
    """Raised when the escrow chain cannot be reached or returns an error."""


async def get_chain_state(chain_order_id: str) -> int:
    """Call middleware GET /escrow/status/{orderId}; return the chain state int.

    Raises ChainClientError on middleware/chain failure (route maps to 502).
    """
    settings = get_settings()
    url = (
        f"{settings.middleware_url.rstrip('/')}/escrow/status/{chain_order_id}"
    )
    try:
        async with httpx.AsyncClient(
            timeout=settings.middleware_timeout_seconds
        ) as client:
            response = await client.get(url)
    except httpx.RequestError as error:
        raise ChainClientError(str(error)) from error

    if response.status_code >= 400:
        raise ChainClientError(
            f"Chain status error ({response.status_code}): {response.text}"
        )

    body = response.json()
    state = body.get("state")
    if not isinstance(state, int):
        raise ChainClientError("Chain status response missing state")
    return state
