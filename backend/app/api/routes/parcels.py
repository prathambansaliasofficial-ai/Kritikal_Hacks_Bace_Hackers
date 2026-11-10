from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Path, Query

from app.api.routes.bbox import parse_bbox
from app.repositories import parcels as parcels_repo

router = APIRouter(tags=["parcels"])


@router.get("/parcels/{ulpin}")
def get_parcel(ulpin: str = Path(..., min_length=3, max_length=64)) -> dict[str, Any]:
    feature = parcels_repo.get_parcel(ulpin)
    if feature is None:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return feature


@router.get("/parcels")
def list_parcels(
    bbox: str | None = Query(None),
    limit: int = Query(100, ge=1, le=100),
) -> dict[str, Any]:
    parsed = parse_bbox(bbox)
    features = parcels_repo.list_parcels(parsed, limit)
    return {"type": "FeatureCollection", "features": features}
