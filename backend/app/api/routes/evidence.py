from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.repositories import evidence as evidence_repo

router = APIRouter(tags=["evidence"])


def _sheet_from_row(row: dict[str, Any]) -> dict[str, Any]:
    payload = row["payload"] or {}
    return {
        "id": row["id"],
        "ulpin": row["ulpin"],
        "status": row["status"],
        "evidence_hash": payload.get("evidence_hash"),
        "tinyfish_run_id": row["tinyfish_run_id"],
        "fields": payload.get("fields", {}),
        "sources": payload.get("sources", []),
        "created_at": row["created_at"],
    }


@router.get("/evidence/{evidence_id}")
def get_evidence(evidence_id: int) -> dict[str, Any]:
    row = evidence_repo.get_evidence_sheet(evidence_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return _sheet_from_row(row)


@router.get("/evidence")
def list_evidence(ulpin: str = Query(..., min_length=3, max_length=64)) -> dict[str, Any]:
    rows = evidence_repo.list_evidence_sheets(ulpin)
    return {"items": [_sheet_from_row(row) for row in rows]}
