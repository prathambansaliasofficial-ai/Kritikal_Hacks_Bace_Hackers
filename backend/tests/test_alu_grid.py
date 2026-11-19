from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.main import app
from app.services.alu_grid import GridError, cells_for_bbox

client = TestClient(app)

BBOX_DEMO = (73.8055, 18.5055, 73.8095, 18.5095)
BBOX_10M = (73.8060, 18.5060, 73.8080, 18.5080)


def test_deterministic_same_ids() -> None:
    first = [c["alu_id"] for c in cells_for_bbox(BBOX_10M, "10m")]
    second = [c["alu_id"] for c in cells_for_bbox(BBOX_10M, "10m")]
    assert first == second


def test_child_parent_is_next_coarser() -> None:
    cells = cells_for_bbox(BBOX_10M, "10m")
    assert cells, "expected cells in demo bbox"
    for cell in cells:
        assert cell["level"] == "10m"
        assert cell["parent_id"] is not None
        assert cell["parent_id"].startswith("ALU-100m-")
        assert cell["area_sqm"] == 100


def test_top_level_parent_is_none() -> None:
    cells = cells_for_bbox(BBOX_DEMO, "1km")
    assert cells
    for cell in cells:
        assert cell["level"] == "1km"
        assert cell["parent_id"] is None


def test_negative_indices_use_m_slug() -> None:
    cells = cells_for_bbox((-0.0001, 0.0, 0.0001, 0.0001), "1m")
    ids = {c["alu_id"] for c in cells}
    assert any("-m" in cid for cid in ids), ids


def test_cap_enforced() -> None:
    try:
        cells_for_bbox((-180.0, -85.0, 180.0, 85.0), "0.1m2")
    except GridError as error:
        assert "exceeds 1500" in error.message
        return
    raise AssertionError("expected GridError over cap")


def test_unknown_level_422() -> None:
    response = client.get(
        "/api/v1/alus?bbox=73.8,18.5,73.9,18.6&level=99m"
    )
    assert response.status_code == 422


def test_over_cap_route_422(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.alus.cells_for_bbox",
        lambda bbox, level: (_ for _ in ()).throw(
            GridError("Zoom in: 2000 cells exceeds 1500")
        ),
    )
    response = client.get("/api/v1/alus?bbox=73.8,18.5,73.9,18.6&level=10m")
    assert response.status_code == 422
    assert "exceeds 1500" in response.json()["detail"]


def test_alus_feature_collection(monkeypatch) -> None:
    fake_cell = {
        "alu_id": "ALU-10m-DEMO-001",
        "parent_id": "ALU-100m-DEMO-000",
        "level": "10m",
        "area_sqm": 100,
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [73.8, 18.5],
                    [73.9, 18.5],
                    [73.9, 18.6],
                    [73.8, 18.6],
                    [73.8, 18.5],
                ]
            ],
        },
    }
    monkeypatch.setattr(
        "app.api.routes.alus.cells_for_bbox", lambda bbox, level: [fake_cell]
    )
    response = client.get("/api/v1/alus?bbox=73.8,18.5,73.9,18.6&level=10m")
    assert response.status_code == 200
    body = response.json()
    assert body["type"] == "FeatureCollection"
    assert len(body["features"]) == 1
    feature = body["features"][0]
    assert feature["id"] == "ALU-10m-DEMO-001"
    assert feature["properties"]["parent_id"] == "ALU-100m-DEMO-000"
    assert feature["properties"]["level"] == "10m"
    assert feature["properties"]["area_sqm"] == 100
    assert feature["properties"]["demo"] is True
