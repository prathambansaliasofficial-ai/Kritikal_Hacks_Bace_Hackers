from __future__ import annotations

import math
from typing import Any

R = 6378137.0
LAT_CLAMP = 85.05112878
CELL_CAP = 1500

ALU_LEVELS = ("1km", "100m", "10m", "1m", "0.1m2")

# level -> (width, height) in Web Mercator metres, fine -> coarse
LEVEL_SIZE: dict[str, tuple[float, float]] = {
    "1km": (1000.0, 1000.0),
    "100m": (100.0, 100.0),
    "10m": (10.0, 10.0),
    "1m": (1.0, 1.0),
    "0.1m2": (0.1, 1.0),
}

# next coarser level per level; 1km is the root
PARENT_LEVEL: dict[str, str | None] = {
    "0.1m2": "1m",
    "1m": "10m",
    "10m": "100m",
    "100m": "1km",
    "1km": None,
}


class GridError(Exception):
    """Raised by the grid service; the route maps it to an HTTP error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def _forward(lon: float, lat: float) -> tuple[float, float]:
    lat = max(-LAT_CLAMP, min(LAT_CLAMP, lat))
    x = R * math.radians(lon)
    y = R * math.log(math.tan(math.pi / 4.0 + math.radians(lat) / 2.0))
    return (x, y)


def _inverse(x: float, y: float) -> tuple[float, float]:
    lon = (x / R) * 180.0 / math.pi
    lat = (2.0 * math.atan(math.exp(y / R)) - math.pi / 2.0) * 180.0 / math.pi
    return (lon, lat)


def _slug(n: int) -> str:
    if n < 0:
        return "m" + str(abs(n))
    return str(n)


def cells_for_bbox(
    bbox: tuple[float, float, float, float], level: str
) -> list[dict[str, Any]]:
    """Return every ALU cell of `level` whose Web Mercator cell intersects `bbox`."""
    if level not in LEVEL_SIZE:
        raise GridError(f"unknown level: {level}")
    width, height = LEVEL_SIZE[level]
    min_lon, min_lat, max_lon, max_lat = bbox

    min_x, min_y = _forward(min_lon, min_lat)
    max_x, max_y = _forward(max_lon, max_lat)

    ix0 = math.floor(min_x / width)
    ix1 = math.floor(max_x / width)
    iy0 = math.floor(min_y / height)
    iy1 = math.floor(max_y / height)

    count = (ix1 - ix0 + 1) * (iy1 - iy0 + 1)
    if count > CELL_CAP:
        raise GridError(f"Zoom in: {count} cells exceeds {CELL_CAP}")

    parent_level = PARENT_LEVEL[level]
    cells: list[dict[str, Any]] = []
    for iy in range(iy0, iy1 + 1):
        for ix in range(ix0, ix1 + 1):
            alu_id = f"ALU-{level}-{_slug(ix)}-{_slug(iy)}"
            parent_id = None
            if parent_level is not None:
                p_width, p_height = LEVEL_SIZE[parent_level]
                pix = math.floor((ix * width) / p_width)
                piy = math.floor((iy * height) / p_height)
                parent_id = (
                    f"ALU-{parent_level}-{_slug(pix)}-{_slug(piy)}"
                )

            mx0 = ix * width
            mx1 = mx0 + width
            my0 = iy * height
            my1 = my0 + height
            ring = [
                _inverse(mx0, my0),
                _inverse(mx1, my0),
                _inverse(mx1, my1),
                _inverse(mx0, my1),
                _inverse(mx0, my0),
            ]
            cells.append(
                {
                    "alu_id": alu_id,
                    "parent_id": parent_id,
                    "level": level,
                    "area_sqm": width * height,
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[lon, lat] for lon, lat in ring]],
                    },
                }
            )
    return cells
