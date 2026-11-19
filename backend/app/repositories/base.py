from __future__ import annotations

from app.core.db import db_connection


def fetch_one(sql: str, params: tuple | dict = ()) -> dict | None:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()


def fetch_all(sql: str, params: tuple | dict = ()) -> list[dict]:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()


def execute(sql: str, params: tuple | dict = ()) -> int:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount
