import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.config import get_settings

router = APIRouter(prefix="/verifications", tags=["verifications"])


class VerificationRequest(BaseModel):
    ulpin: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9/_.-]+$")
    source_url: str | None = None
    goal: str | None = None


@router.post("")
async def create_verification(payload: VerificationRequest) -> dict:
    """Forward a ULPIN check to the TinyFish middleware.

    The backend owns the verify/clean-result policy. The middleware only gathers
    evidence, so this route currently returns the middleware response verbatim.
    """
    settings = get_settings()
    body = payload.model_dump(exclude_none=True)

    try:
        async with httpx.AsyncClient(timeout=settings.middleware_timeout_seconds) as client:
            response = await client.post(
                f"{settings.middleware_url.rstrip('/')}/verify/evidence",
                json=body,
            )
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail=f"Middleware unavailable: {error}",
        ) from error

    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail=f"Middleware error ({response.status_code}): {response.text}",
        )

    return response.json()
