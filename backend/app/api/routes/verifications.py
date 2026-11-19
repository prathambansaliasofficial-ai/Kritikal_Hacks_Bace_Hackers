from __future__ import annotations

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.repositories import evidence as evidence_repo
from app.services.evidence import canonical_hash, normalize_sheet

router = APIRouter(prefix="/verifications", tags=["verifications"])


class VerificationRequest(BaseModel):
    ulpin: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9/_.-]+$")
    source_url: str | None = None
    goal: str | None = None


@router.post("")
async def create_verification(payload: VerificationRequest) -> dict:
    """Forward a ULPIN check to TinyFish, validate, hash and persist the sheet.

    The backend owns the evidence policy: exactly 21 fields, canonical SHA-256
    hash, never invent values.
    """
    settings = get_settings()
    body = {"ulpin": payload.ulpin}
    if payload.source_url is not None:
        body["sourceUrl"] = payload.source_url
    if payload.goal is not None:
        body["goal"] = payload.goal

    try:
        async with httpx.AsyncClient(
            timeout=settings.middleware_timeout_seconds
        ) as client:
            response = await client.post(
                f"{settings.middleware_url.rstrip('/')}/verify/evidence",
                json=body,
            )
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail=f"Middleware unavailable: {error}",
        ) from error

    if response.status_code == 422:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid evidence sheet: {response.text}",
        )
    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail=f"Middleware error ({response.status_code}): {response.text}",
        )

    sheet = response.json()
    fields = sheet.get("fields")
    if not isinstance(fields, dict):
        raise HTTPException(
            status_code=422,
            detail="Invalid evidence sheet: missing fields",
        )

    normalized = normalize_sheet(fields)
    sources = sheet.get("sources") or []
    if not isinstance(sources, list):
        sources = []
    sources = [str(s) for s in sources]
    tinyfish_run_id = sheet.get("runId") or sheet.get("tinyfish_run_id")

    evidence_hash = canonical_hash(payload.ulpin, normalized, sources)
    db_payload = {
        "ulpin": payload.ulpin,
        "fields": normalized,
        "sources": sorted(set(sources)),
        "evidence_hash": evidence_hash,
    }

    evidence_id = evidence_repo.create_evidence_sheet(
        ulpin=payload.ulpin,
        payload=db_payload,
        source_refs=sources,
        tinyfish_run_id=tinyfish_run_id,
        evidence_hash=evidence_hash,
    )

    return {
        "ulpin": payload.ulpin,
        "status": "PENDING",
        "evidence_id": evidence_id,
        "evidence_hash": evidence_hash,
        "tinyfish_run_id": tinyfish_run_id,
        "fields": normalized,
        "sources": sorted(set(sources)),
    }
