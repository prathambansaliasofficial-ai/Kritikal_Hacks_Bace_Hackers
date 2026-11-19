from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Header, HTTPException, Path
from pydantic import BaseModel

from app.core.config import get_settings
from app.repositories import users as users_repo

router = APIRouter(tags=["users"])


class UserCreate(BaseModel):
    wallet_address: str
    role: str = "CITIZEN"


class KycUpdate(BaseModel):
    status: str
    reason: str | None = None


def _require_officer_token(x_officer_token: str | None) -> None:
    settings = get_settings()
    if not settings.dev_officer_token or x_officer_token != settings.dev_officer_token:
        raise HTTPException(status_code=401, detail="Missing or invalid officer token")


@router.post("/users", status_code=200)
def upsert_user(payload: UserCreate) -> dict[str, Any]:
    if not users_repo.is_valid_wallet(payload.wallet_address):
        raise HTTPException(status_code=422, detail="Invalid wallet address")
    if payload.role not in ("CITIZEN", "OFFICER"):
        raise HTTPException(status_code=422, detail="Invalid role")
    return users_repo.upsert_user(payload.wallet_address, payload.role)


@router.get("/users/{wallet_address}")
def get_user(
    wallet_address: str = Path(...),
) -> dict[str, Any]:
    if not users_repo.is_valid_wallet(wallet_address):
        raise HTTPException(status_code=422, detail="Invalid wallet address")
    user = users_repo.get_user(wallet_address)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/{wallet_address}/kyc")
def update_kyc(
    wallet_address: str = Path(...),
    payload: KycUpdate | None = None,
    x_officer_token: str | None = Header(default=None, alias="X-Officer-Token"),
) -> dict[str, Any]:
    _require_officer_token(x_officer_token)
    if not users_repo.is_valid_wallet(wallet_address):
        raise HTTPException(status_code=422, detail="Invalid wallet address")
    if payload is None or payload.status not in ("PENDING", "VERIFIED", "REJECTED"):
        raise HTTPException(status_code=422, detail="Invalid KYC status")
    user = users_repo.update_kyc(wallet_address, payload.status, payload.reason)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
