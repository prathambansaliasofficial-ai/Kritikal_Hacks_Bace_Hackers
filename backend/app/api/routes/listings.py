from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel, Field

from app.repositories import listings as listings_repo
from app.repositories.listings import ListingError

router = APIRouter(tags=["listings"])


class ListingCreate(BaseModel):
    bundle_id: int = Field(gt=0)
    seller_wallet: str
    price_wei: str = Field(min_length=1)


class ListingStatus(BaseModel):
    status: str


@router.post("/listings", status_code=201)
def create_listing(payload: ListingCreate) -> dict[str, Any]:
    try:
        return listings_repo.create_listing(
            payload.bundle_id, payload.seller_wallet, payload.price_wei
        )
    except ListingError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get("/listings")
def list_listings(
    status: str | None = Query("LISTED"),
) -> dict[str, Any]:
    items = listings_repo.list_listings(status)
    return {"items": items}


@router.patch("/listings/{listing_id}")
def patch_listing_status(
    listing_id: int = Path(...), payload: ListingStatus | None = None
) -> dict[str, Any]:
    status = payload.status if payload else None
    try:
        listing = listings_repo.patch_listing_status(listing_id, status)
    except ListingError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
