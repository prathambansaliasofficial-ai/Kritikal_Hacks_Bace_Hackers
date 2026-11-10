from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from app.repositories import bundles as bundles_repo
from app.repositories.bundles import BundleError

router = APIRouter(tags=["bundles"])


class BundleCreate(BaseModel):
    ulpin: str
    name: str
    alu_ids: list[str]
    created_by: str


class BundleStatus(BaseModel):
    status: str


@router.post("/bundles", status_code=201)
def create_bundle(payload: BundleCreate) -> dict[str, Any]:
    try:
        return bundles_repo.create_bundle(
            payload.ulpin, payload.name, payload.alu_ids, payload.created_by
        )
    except BundleError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get("/bundles/{bundle_id}")
def get_bundle(bundle_id: int = Path(...)) -> dict[str, Any]:
    bundle = bundles_repo.get_bundle(bundle_id)
    if bundle is None:
        raise HTTPException(status_code=404, detail="Bundle not found")
    return bundle


@router.patch("/bundles/{bundle_id}")
def patch_bundle_status(
    bundle_id: int = Path(...), payload: BundleStatus | None = None
) -> dict[str, Any]:
    status = payload.status if payload else None
    try:
        bundle = bundles_repo.set_bundle_status(bundle_id, status)
    except BundleError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
    if bundle is None:
        raise HTTPException(status_code=404, detail="Bundle not found")
    return bundle
