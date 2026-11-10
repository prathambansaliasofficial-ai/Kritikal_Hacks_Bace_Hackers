from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel

from app.core.config import get_settings
from app.repositories import evidence as evidence_repo

router = APIRouter(tags=["reviews"])

ALLOWED_STATUSES = ("PENDING", "NEEDS_REVIEW")


def _require_officer_token(x_officer_token: str | None) -> None:
    settings = get_settings()
    if not settings.dev_officer_token or x_officer_token != settings.dev_officer_token:
        raise HTTPException(status_code=401, detail="Missing or invalid officer token")


class ReviewDecision(BaseModel):
    decision: str
    reason: str | None = None
    officer: str | None = None


@router.get("/reviews")
def list_reviews(
    status: str = Query("PENDING"),
    x_officer_token: str | None = Header(default=None, alias="X-Officer-Token"),
) -> dict[str, Any]:
    if status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=422, detail=f"status must be one of {list(ALLOWED_STATUSES)}"
        )
    rows = evidence_repo.list_reviews(status)
    items = []
    for row in rows:
        payload = row["payload"] or {}
        items.append(
            {
                "evidence_id": row["evidence_id"],
                "ulpin": row["ulpin"],
                "status": row["status"],
                "evidence_hash": payload.get("evidence_hash"),
                "created_at": row["created_at"],
            }
        )
    return {"items": items}


@router.post("/reviews/{evidence_id}/decision")
def decide_review(
    evidence_id: int,
    payload: ReviewDecision,
    x_officer_token: str | None = Header(default=None, alias="X-Officer-Token"),
) -> dict[str, Any]:
    _require_officer_token(x_officer_token)
    try:
        row = evidence_repo.decide_review(
            evidence_id, payload.decision, payload.reason, payload.officer
        )
    except ValueError as error:
        if str(error) == "already_decided":
            raise HTTPException(
                status_code=409, detail="Review already decided"
            ) from error
        if str(error) == "reason_required":
            raise HTTPException(
                status_code=422, detail="Reason required for reject"
            ) from error
        raise
    if row is None:
        raise HTTPException(status_code=404, detail="Evidence not found")
    sheet_payload = row["payload"] or {}
    return {
        "evidence_id": row["evidence_id"],
        "ulpin": row["ulpin"],
        "status": row["status"],
        "evidence_hash": sheet_payload.get("evidence_hash"),
        "reviewed_by": row["reviewed_by"],
        "review_reason": row["review_reason"],
        "reviewed_at": row["reviewed_at"],
        "created_at": row["created_at"],
    }
