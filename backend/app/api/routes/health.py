from fastapi import APIRouter

from app.core.config import get_settings
from app.core.db import check_database

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    database = check_database()
    return {
        "status": "ok" if database["status"] == "ok" else "degraded",
        "service": settings.app_name,
        "environment": settings.environment,
        "database": database,
    }
