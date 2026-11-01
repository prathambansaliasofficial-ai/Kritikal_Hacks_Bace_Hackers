from typing import Any

import psycopg

from app.core.config import get_settings


def check_database() -> dict[str, Any]:
    """Best-effort PostGIS health probe. Never raises: the API stays up without the DB."""
    settings = get_settings()
    try:
        with psycopg.connect(settings.database_url, connect_timeout=3) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT postgis_version()")
                version = cursor.fetchone()
        return {
            "status": "ok",
            "postgis_version": version[0] if version else None,
            "error": None,
        }
    except Exception as error:  # noqa: BLE001 - health probe must not crash the app
        return {
            "status": "unavailable",
            "postgis_version": None,
            "error": str(error),
        }
