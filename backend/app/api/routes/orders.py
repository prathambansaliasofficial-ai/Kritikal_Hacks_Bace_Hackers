from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from app.repositories import (
    alus as alus_repo,
)
from app.repositories import (
    bundles as bundles_repo,
)
from app.repositories import (
    evidence as evidence_repo,
)
from app.repositories import (
    listings as listings_repo,
)
from app.repositories import (
    orders as orders_repo,
)
from app.repositories import (
    users as users_repo,
)
from app.repositories.orders import OrderError
from app.services.chain_client import ChainClientError, get_chain_state
from app.services.checks import (
    check_results_to_api,
    decide,
    run_checks,
)
from app.services.settlement import SettlementError, apply_decision

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
        "checks": row.get("checks") or [],
        "decision": row.get("decision"),
        "decided_at": row.get("decided_at"),
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
        raise HTTPException(
            status_code=422, detail="chain_order_id and tx_hash required"
        )
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


@router.post("/orders/{order_id}/evaluate")
async def evaluate_order(order_id: int = Path(...)) -> dict[str, Any]:
    """Run the six checks, persist the decision, and trigger settlement."""
    order = orders_repo.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if order["state"] != "FUNDED":
        raise HTTPException(status_code=409, detail="Order is not FUNDED")

    listing = listings_repo.get_listing(order["listing_id"])
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")

    bundle = bundles_repo.get_bundle(listing["bundle_id"])
    if bundle is None:
        raise HTTPException(status_code=404, detail="Bundle not found")

    alu_ids = bundles_repo.get_bundle_alu_ids(bundle["id"])
    alus_present = alus_repo.alus_present_in_parcel(listing["ulpin"], alu_ids)
    alu_conflict = orders_repo.alu_in_other_active_order(alu_ids, order_id)

    buyer = users_repo.get_user(order["buyer_wallet"])
    seller = users_repo.get_user(listing["seller_wallet"])
    if buyer is None or seller is None:
        raise HTTPException(status_code=404, detail="Buyer or seller not found")

    evidence = evidence_repo.get_latest_evidence_for_ulpin(listing["ulpin"])
    land_use_zoning = None
    evidence_ulpin = None
    if evidence is not None:
        payload = evidence["payload"] or {}
        fields = payload.get("fields") or {}
        zoning = fields.get("land_use_zoning")
        if isinstance(zoning, dict):
            land_use_zoning = zoning.get("value")
        evidence_ulpin = evidence["ulpin"]

    # Chain state for FUNDS_IN_ESCROW; failure => 502, persist nothing.
    try:
        chain_state = await get_chain_state(order["chain_order"])
    except ChainClientError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    context = {
        "listing_status": listing["status"],
        "order_listing_id": order["listing_id"],
        "listing_id": order["listing_id"],
        "bundle_status": bundle["status"],
        "alus_present": alus_present,
        "alu_in_other_active_order": alu_conflict,
        "buyer_kyc": buyer["kyc_status"],
        "seller_kyc": seller["kyc_status"],
        "land_use_zoning": land_use_zoning,
        "order_state": order["state"],
        "chain_state": chain_state,
        "listing_ulpin": listing["ulpin"],
        "bundle_ulpin": bundle["ulpin"],
        "parcel_ulpin": listing["ulpin"],
        "evidence_ulpin": evidence_ulpin,
        "buyer_wallet": order["buyer_wallet"],
        "seller_wallet": listing["seller_wallet"],
    }

    results = run_checks(context)
    decision = decide(results)

    orders_repo.save_evaluate(
        order_id, check_results_to_api(results), decision
    )

    # Settlement: APPROVED -> settle, REJECTED -> refund, NEEDS_REVIEW -> no-op.
    try:
        await apply_decision(order, decision)
    except SettlementError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error

    row = orders_repo.get_order(order_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_shape(row)
