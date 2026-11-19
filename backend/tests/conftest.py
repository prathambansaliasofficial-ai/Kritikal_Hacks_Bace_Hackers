from __future__ import annotations

import os
from pathlib import Path

import psycopg
import pytest

os.environ.setdefault("TEST_DATABASE_URL", "")
from app.core.config import get_settings  # noqa: E402

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL") or get_settings().database_url


@pytest.fixture(scope="session")
def apply_schema():
    """Apply every 0*.sql migration to the test database (integration tests opt in)."""
    sql_dir = Path(__file__).resolve().parent.parent / "db"
    files = sorted(sql_dir.glob("0*.sql"))
    with psycopg.connect(TEST_DATABASE_URL, autocommit=True) as conn:
        with conn.cursor() as cur:
            for sql_file in files:
                cur.execute(sql_file.read_text())


@pytest.fixture
def db(apply_schema):
    """Per-test connection rolled back after the test.

    Repository calls use db_connection() -> TEST_DATABASE_URL, so each test
    cleans up the rows it inserts.
    """
    conn = psycopg.connect(TEST_DATABASE_URL)
    conn.autocommit = False
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()
