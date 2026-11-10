from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from app.repositories import orders as orders_repo
from app.repositories.orders import OrderError

router = APIRouter(tags=["orders"])


class OrderCreate(BaseModel):
    listing_id: int
    buyer_wallet: str


class OrderFunded(BaseModel):
    chain_order_id: str
    tx_hash: str


def _order_shape(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "listing_id": row["listing_id"],
        "buyer_wallet": row["buyer_wallet"],
        "seller_wallet": row["seller_wallet"],
        "amount_wei": row["amount_wei"],
        "state": row["state"],
        "chain_order_id": row["chain_order"],
        "tx_hash": row["tx_hash"],
        "evidence_hash": row["evidence_hash"],
        "checks": [],
        "decision": None,
        "decided_at": None,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


@router.post("/orders", status_code=201)
def create_order(payload: OrderCreate) -> dict[str, Any]:
    try:
        row = orders_repo.create_order(payload.listing_id, payload.buyer_wallet)
    except OrderError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    return _order_shape(row)


@router.post("/orders/{order_id}/funded")
def fund_order(
    order_id: int = Path(...), payload: OrderFunded | None = None
) -> dict[str, Any]:
    if payload is None:
        raise HTTPException(status_code=422, detail="chain_order_id and tx_hash required")
    try:
        row = orders_repo.fund_order(
            order_id, payload.chain_order_id, payload.tx_hash
        )
    except OrderError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    if row is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_shape(row)


@router.get("/orders/{order_id}")
def get_order(order_id: int = Path(...)) -> dict[str, Any]:
    row = orders_repo.get_order(order_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_shape(row)
