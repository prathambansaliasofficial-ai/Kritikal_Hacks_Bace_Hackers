from __future__ import annotations

import re
from typing import Any

from app.core.db import db_connection
from app.repositories.base import fetch_one

WALLET_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")


def is_valid_wallet(wallet: str) -> bool:
    return bool(WALLET_RE.fullmatch(wallet))


def _row_dict(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "id": row["id"],
        "wallet_address": row["wallet_address"],
        "role": row["role"],
        "kyc_status": row["kyc_status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def upsert_user(wallet_address: str, role: str = "CITIZEN") -> dict[str, Any]:
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (wallet_address, role)
                VALUES (%s, %s)
                ON CONFLICT (wallet_address)
                DO UPDATE SET role = EXCLUDED.role, updated_at = now()
                RETURNING id, wallet_address, role, kyc_status, created_at, updated_at
                """,
                (wallet_address, role),
            )
            return _row_dict(cursor.fetchone())


def get_user(wallet_address: str) -> dict[str, Any] | None:
    row = fetch_one(
        """
        SELECT id, wallet_address, role, kyc_status, created_at, updated_at
        FROM users
        WHERE wallet_address = %s
        """,
        (wallet_address,),
    )
    return _row_dict(row)


def update_kyc(
    wallet_address: str, status: str, reason: str | None = None
) -> dict[str, Any] | None:
    row = fetch_one(
        """
        UPDATE users
        SET kyc_status = %s, updated_at = now()
        WHERE wallet_address = %s
        RETURNING id, wallet_address, role, kyc_status, created_at, updated_at
        """,
        (status, wallet_address),
    )
    return _row_dict(row)
