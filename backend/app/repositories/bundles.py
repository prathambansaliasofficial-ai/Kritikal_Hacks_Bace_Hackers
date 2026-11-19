from __future__ import annotations

from datetime import datetime
from typing import Any

from app.core.db import db_connection
from app.repositories.base import fetch_all, fetch_one


class BundleError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "DRAFT": {"ACTIVE", "ARCHIVED"},
    "ACTIVE": {"PAUSED", "ARCHIVED"},
    "PAUSED": {"ACTIVE", "ARCHIVED"},
    "ARCHIVED": set(),
}


def _iso(value: Any) -> Any:
    return value.isoformat() if isinstance(value, datetime) else value


def _row_dict(row: dict[str, Any]) -> dict[str, Any]:
    return {k: _iso(v) for k, v in row.items()}


def _parcel_exists(ulpin: str) -> bool:
    row = fetch_one("SELECT 1 FROM parcels WHERE ulpin = %s", (ulpin,))
    return row is not None


def _validate_alus(ulpin: str, alu_ids: list[str]) -> list[dict[str, Any]]:
    if len(set(alu_ids)) != len(alu_ids):
        dupes = sorted({a for a in alu_ids if alu_ids.count(a) > 1})
        raise BundleError(422, f"duplicate ALU in request: {dupes}")
    rows = fetch_all(
        """
        SELECT a.alu_id, a.level
        FROM alus a
        JOIN parcel_alus pa ON pa.alu_id = a.alu_id AND pa.ulpin = %s
        WHERE a.alu_id = ANY(%s)
        """,
        (ulpin, list(alu_ids)),
    )
    found = {row["alu_id"] for row in rows}
    missing = sorted(set(alu_ids) - found)
    if missing:
        raise BundleError(422, f"ALU not found or not in parcel {ulpin}: {missing}")
    return rows


def create_bundle(
    ulpin: str, name: str, alu_ids: list[str], created_by: str
) -> dict[str, Any]:
    if not _parcel_exists(ulpin):
        raise BundleError(404, "Parcel not found")
    alu_rows = _validate_alus(ulpin, alu_ids)

    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO bundles (ulpin, name, status, created_by)
                VALUES (%s, %s, 'DRAFT', %s)
                RETURNING id, ulpin, name, status, created_by, created_at, updated_at
                """,
                (ulpin, name, created_by),
            )
            bundle = _row_dict(cursor.fetchone())
            for alu in alu_rows:
                cursor.execute(
                    "INSERT INTO bundle_alus (bundle_id, alu_id) VALUES (%s, %s)",
                    (bundle["id"], alu["alu_id"]),
                )
    bundle["alus"] = [
        {"alu_id": alu["alu_id"], "level": alu["level"]} for alu in alu_rows
    ]
    return bundle


def get_bundle(bundle_id: int) -> dict[str, Any] | None:
    row = fetch_one(
        """
        SELECT id, ulpin, name, status, created_by, created_at, updated_at
        FROM bundles
        WHERE id = %s
        """,
        (bundle_id,),
    )
    if row is None:
        return None
    bundle = _row_dict(row)
    alus = fetch_all(
        """
        SELECT ba.alu_id, a.level
        FROM bundle_alus ba
        JOIN alus a ON a.alu_id = ba.alu_id
        WHERE ba.bundle_id = %s
        ORDER BY ba.alu_id
        """,
        (bundle_id,),
    )
    bundle["alus"] = [
        {"alu_id": a["alu_id"], "level": a["level"]} for a in alus
    ]
    return bundle


def get_bundle_alu_ids(bundle_id: int) -> list[str]:
    rows = fetch_all(
        "SELECT alu_id FROM bundle_alus WHERE bundle_id = %s ORDER BY alu_id",
        (bundle_id,),
    )
    return [row["alu_id"] for row in rows]


def set_bundle_status(bundle_id: int, status: str) -> dict[str, Any] | None:
    row = fetch_one(
        "SELECT status FROM bundles WHERE id = %s", (bundle_id,)
    )
    if row is None:
        return None
    current = row["status"]
    if status not in ALLOWED_TRANSITIONS.get(current, set()):
        raise BundleError(
            409, f"invalid transition {current} -> {status}"
        )
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE bundles
                SET status = %s, updated_at = now()
                WHERE id = %s
                RETURNING id, ulpin, name, status, created_by, created_at, updated_at
                """,
                (status, bundle_id),
            )
            return _row_dict(cursor.fetchone())
