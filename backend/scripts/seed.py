"""Idempotent demo seed runner: delete demo rows first, then insert.

Run from the repo root:  PYTHONPATH=backend python backend/scripts/seed.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg

from app.core.config import get_settings

DEMO_ULPIN = "DEMO-ULPIN-001"
DEMO_ALUS = (
    "ALU-100m-DEMO-000",
    "ALU-10m-DEMO-001",
    "ALU-10m-DEMO-002",
    "ALU-10m-DEMO-003",
    "ALU-10m-DEMO-004",
)
SQL_FILE = Path(__file__).resolve().parent.parent / "db" / "002_seed_demo.sql"


def main() -> int:
    settings = get_settings()
    sql = SQL_FILE.read_text()
    with psycopg.connect(settings.database_url, connect_timeout=5) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM parcel_alus WHERE ulpin = %s", (DEMO_ULPIN,)
            )
            cursor.execute(
                "DELETE FROM alus WHERE alu_id = ANY(%s)", (list(DEMO_ALUS),)
            )
            cursor.execute(
                "DELETE FROM parcels WHERE ulpin = %s", (DEMO_ULPIN,)
            )
            cursor.execute(sql)
        connection.commit()
    print("seed=ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
