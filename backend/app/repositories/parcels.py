from __future__ import annotations

from typing import Any

from app.repositories.base import fetch_all, fetch_one

DEMO_SOURCE = "DEMO_FIXTURE_NOT_OFFICIAL"


def _feature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "Feature",
        "id": row["ulpin"],
        "geometry": row["geometry"],
        "properties": {
            "ulpin": row["ulpin"],
            "geometry_status": row["geometry_status"],
            "attributes": row["attributes"],
            "demo": row.get("geometry_source") == DEMO_SOURCE,
        },
    }


def get_parcel(ulpin: str) -> dict | None:
    row = fetch_one(
        """
        SELECT ulpin,
               ST_AsGeoJSON(geometry)::json AS geometry,
               geometry_status,
               attributes,
               geometry_source
        FROM parcels
        WHERE ulpin = %s
        """,
        (ulpin,),
    )
    if row is None:
        return None
    return _feature(row)


def list_parcels(
    bbox: tuple[float, float, float, float], limit: int
) -> list[dict[str, Any]]:
    min_lon, min_lat, max_lon, max_lat = bbox
    rows = fetch_all(
        """
        SELECT ulpin,
               ST_AsGeoJSON(geometry)::json AS geometry,
               geometry_status,
               attributes,
               geometry_source
        FROM parcels
        WHERE ST_Intersects(
                  geometry,
                  ST_MakeEnvelope(%s, %s, %s, %s, 4326)
              )
        ORDER BY ulpin
        LIMIT %s
        """,
        (min_lon, min_lat, max_lon, max_lat, limit),
    )
    return [_feature(row) for row in rows]
