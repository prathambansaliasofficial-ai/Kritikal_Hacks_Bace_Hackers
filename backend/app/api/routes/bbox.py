from __future__ import annotations

from fastapi import HTTPException


def parse_bbox(value: str | None) -> tuple[float, float, float, float]:
    """Parse and validate a ``minLon,minLat,maxLon,maxLat`` bbox query value.

    Raises ``HTTPException(422)`` on any invalid input.
    """
    if value is None:
        raise HTTPException(
            status_code=422,
            detail="bbox=minLon,minLat,maxLon,maxLat is required",
        )
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 4:
        raise HTTPException(
            status_code=422,
            detail="bbox must be minLon,minLat,maxLon,maxLat",
        )
    try:
        min_lon, min_lat, max_lon, max_lat = (float(part) for part in parts)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail="bbox values must be numbers",
        ) from error
    for name, num in (("minLon", min_lon), ("maxLon", max_lon)):
        if not -180.0 <= num <= 180.0:
            raise HTTPException(
                status_code=422, detail=f"{name} out of range [-180, 180]"
            )
    for name, num in (("minLat", min_lat), ("maxLat", max_lat)):
        if not -90.0 <= num <= 90.0:
            raise HTTPException(
                status_code=422, detail=f"{name} out of range [-90, 90]"
            )
    if min_lon > max_lon or min_lat > max_lat:
        raise HTTPException(
            status_code=422,
            detail="invalid bbox: min must be <= max",
        )
    return (min_lon, min_lat, max_lon, max_lat)
