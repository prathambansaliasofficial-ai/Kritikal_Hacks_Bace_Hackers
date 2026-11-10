from __future__ import annotations

from typing import Any

from app.repositories.base import fetch_all, fetch_one


def get_alu(alu_id: str) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT alu_id, parent_id, level, geometry, created_at
        FROM alus
        WHERE alu_id = %s
        """,
        (alu_id,),
    )


def alus_present_in_parcel(ulpin: str, alu_ids: list[str]) -> bool:
    """True iff every alu_id exists and is linked to the parcel via parcel_alus."""
    if not alu_ids:
        return True
    rows = fetch_all(
        """
        SELECT pa.alu_id
        FROM parcel_alus pa
        JOIN alus a ON a.alu_id = pa.alu_id
        WHERE pa.ulpin = %s AND pa.alu_id = ANY(%s)
        """,
        (ulpin, list(alu_ids)),
    )
    found = {row["alu_id"] for row in rows}
    return all(alu_id in found for alu_id in alu_ids)
