"""PostGIS boot check: version, six tables, row counts.

Exit code 1 on any connection or check failure so CI/scripts can gate on it.
Run from the repo root:  PYTHONPATH=backend python backend/scripts/check_db.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg
from psycopg import sql

from app.core.config import get_settings

EXPECTED_TABLES = (
    "parcels",
    "alus",
    "parcel_alus",
    "evidence_sheets",
    "listings",
    "orders",
)


def main() -> int:
    settings = get_settings()
    try:
        with psycopg.connect(
            settings.database_url, connect_timeout=5
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT postgis_version()")
                row = cursor.fetchone()
                version = row[0] if row else None
                print(f"postgis_version={version}")
                for table in EXPECTED_TABLES:
                    query = sql.SQL("SELECT to_regclass({})").format(
                        sql.Identifier(table)
                    )
                    cursor.execute(query)
                    exists = cursor.fetchone()[0] is not None
                    if not exists:
                        print(f"table={table} missing")
                        return 1
                    count_query = sql.SQL("SELECT count(*) FROM {}").format(
                        sql.Identifier(table)
                    )
                    cursor.execute(count_query)
                    count = cursor.fetchone()[0]
                    print(f"table={table} rows={count}")
    except Exception as error:  # noqa: BLE001 - a check reports, never crashes
        print(f"error: {error}")
        return 1
    print("db_check=ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
