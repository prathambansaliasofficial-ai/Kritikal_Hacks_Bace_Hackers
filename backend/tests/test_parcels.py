from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)

FAKE_PARCEL = {
    "type": "Feature",
    "id": "DEMO-ULPIN-001",
    "geometry": {
        "type": "MultiPolygon",
        "coordinates": [[[[73.8055, 18.5055]]]],
    },
    "properties": {
        "ulpin": "DEMO-ULPIN-001",
        "geometry_status": "AVAILABLE",
        "attributes": {
            "owner_name": "Demo Owner",
            "district": "Pune",
            "zoning": "Residential",
        },
        "demo": True,
    },
}


def test_get_parcel_found(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.parcels.parcels_repo.get_parcel", lambda ulpin: FAKE_PARCEL
    )
    response = client.get("/api/v1/parcels/DEMO-ULPIN-001")
    assert response.status_code == 200
    body = response.json()
    assert body["type"] == "Feature"
    assert body["id"] == "DEMO-ULPIN-001"
    assert body["properties"]["ulpin"] == "DEMO-ULPIN-001"
    assert body["properties"]["geometry_status"] == "AVAILABLE"
    assert body["properties"]["attributes"] == {
        "owner_name": "Demo Owner",
        "district": "Pune",
        "zoning": "Residential",
    }
    assert body["properties"]["demo"] is True


def test_get_parcel_missing_404(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.parcels.parcels_repo.get_parcel", lambda ulpin: None
    )
    response = client.get("/api/v1/parcels/NOPE-999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Parcel not found"


def test_list_parcels_invalid_bbox_422() -> None:
    response = client.get("/api/v1/parcels?bbox=73.8,18.5")
    assert response.status_code == 422

    response = client.get("/api/v1/parcels?bbox=73.8,18.5,73.9")
    assert response.status_code == 422

    response = client.get("/api/v1/parcels?bbox=73.9,18.5,73.8,18.6")
    assert response.status_code == 422


def test_list_parcels_limit_over_max_422() -> None:
    response = client.get("/api/v1/parcels?bbox=73.8,18.5,73.9,18.6&limit=101")
    assert response.status_code == 422


def test_list_parcels_feature_collection(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.parcels.parcels_repo.list_parcels",
        lambda bbox, limit: [FAKE_PARCEL],
    )
    response = client.get("/api/v1/parcels?bbox=73.8,18.5,73.9,18.6&limit=10")
    assert response.status_code == 200
    body = response.json()
    assert body["type"] == "FeatureCollection"
    assert len(body["features"]) == 1
    assert body["features"][0]["id"] == "DEMO-ULPIN-001"
