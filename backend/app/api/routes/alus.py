from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.api.routes.bbox import parse_bbox
from app.services.alu_grid import ALU_LEVELS, GridError, cells_for_bbox

router = APIRouter(tags=["alus"])


@router.get("/alus")
def list_alus(
    bbox: str | None = Query(None),
    level: str = Query(..., description=f"One of {', '.join(ALU_LEVELS)}"),
) -> dict[str, Any]:
    if level not in ALU_LEVELS:
        raise HTTPException(status_code=422, detail=f"unknown level: {level}")
    parsed = parse_bbox(bbox)
    try:
        cells = cells_for_bbox(parsed, level)
    except GridError as error:
        raise HTTPException(status_code=422, detail=error.message) from error

    features: list[dict[str, Any]] = []
    for cell in cells:
        features.append(
            {
                "type": "Feature",
                "id": cell["alu_id"],
                "geometry": cell["geometry"],
                "properties": {
                    "alu_id": cell["alu_id"],
                    "parent_id": cell["parent_id"],
                    "level": cell["level"],
                    "area_sqm": cell["area_sqm"],
                    "demo": True,
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}
