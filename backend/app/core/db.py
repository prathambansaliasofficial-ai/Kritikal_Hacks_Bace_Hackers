from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.core.config import get_settings


@contextmanager
def db_connection() -> Iterator[psycopg.Connection]:
    """Postgres connection: dict rows, 5s connect timeout, commit/rollback/close."""
    settings = get_settings()
    connection = psycopg.connect(
        settings.database_url,
        row_factory=dict_row,
        connect_timeout=5,
    )
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def check_database() -> dict[str, Any]:
    """Best-effort PostGIS health probe via db_connection. Never raises."""
    try:
        with db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT postgis_version()")
                row = cursor.fetchone()
        return {
            "status": "ok",
            "postgis_version": row[0] if row else None,
            "error": None,
        }
    except Exception as error:  # noqa: BLE001 - health probe must not crash the app
        return {
            "status": "unavailable",
            "postgis_version": None,
            "error": str(error),
        }
