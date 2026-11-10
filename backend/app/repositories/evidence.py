from __future__ import annotations

import json
from typing import Any

from app.core.db import db_connection
from app.repositories.base import fetch_all, fetch_one


def create_evidence_sheet(
    ulpin: str,
    payload: dict[str, Any],
    source_refs: list[str],
    tinyfish_run_id: str | None,
    evidence_hash: str,
) -> int:
    row = fetch_one(
        """
        INSERT INTO evidence_sheets (ulpin, status, payload, source_refs,
                                     tinyfish_run_id)
        VALUES (%s, 'PENDING', %s::jsonb, %s::jsonb, %s)
        RETURNING id
        """,
        (
            ulpin,
            json.dumps(payload),
            json.dumps(source_refs),
            tinyfish_run_id,
        ),
    )
    return int(row["id"])


def get_evidence_sheet(evidence_id: int) -> dict[str, Any] | None:
    row = fetch_one(
        """
        SELECT id, ulpin, status, payload, source_refs, tinyfish_run_id,
               reviewed_by, review_reason, reviewed_at, created_at, updated_at
        FROM evidence_sheets
        WHERE id = %s
        """,
        (evidence_id,),
    )
    return row


def list_evidence_sheets(ulpin: str) -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT id, ulpin, status, payload, source_refs, tinyfish_run_id,
               created_at
        FROM evidence_sheets
        WHERE ulpin = %s
        ORDER BY created_at DESC, id DESC
        """,
        (ulpin,),
    )


def list_reviews(status: str) -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT id AS evidence_id, ulpin, status, payload, created_at
        FROM evidence_sheets
        WHERE status = %s
        ORDER BY created_at ASC, id ASC
        """,
        (status,),
    )


def decide_review(
    evidence_id: int,
    decision: str,
    reason: str | None,
    officer: str | None,
) -> dict[str, Any] | None:
    """APPROVE -> CLEAN, REJECT -> REJECTED. Returns updated row or None."""
    row = fetch_one(
        "SELECT status FROM evidence_sheets WHERE id = %s", (evidence_id,)
    )
    if row is None:
        return None
    current = row["status"]
    if current not in ("PENDING", "NEEDS_REVIEW"):
        raise ValueError("already_decided")
    if decision == "REJECT" and not reason:
        raise ValueError("reason_required")
    new_status = "CLEAN" if decision == "APPROVE" else "REJECTED"
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE evidence_sheets
                SET status = %s, reviewed_by = %s, review_reason = %s,
                    reviewed_at = now(), updated_at = now()
                WHERE id = %s
                RETURNING id, ulpin, status, payload, created_at
                """,
                (new_status, officer, reason, evidence_id),
            )
            return cursor.fetchone()
