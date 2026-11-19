from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.main import app
from app.repositories.bundles import BundleError

client = TestClient(app)

FAKE_BUNDLE = {
    "id": 1,
    "ulpin": "DEMO-ULPIN-001",
    "name": "Demo south bundle",
    "status": "DRAFT",
    "alus": [
        {"alu_id": "ALU-10m-DEMO-001", "level": "10m"},
        {"alu_id": "ALU-10m-DEMO-002", "level": "10m"},
    ],
    "created_by": "0x2222222222222222222222222222222222222222",
    "created_at": "2026-10-29T16:40:00+00:00",
}


def _post_bundle(payload: dict) -> object:
    return client.post("/api/v1/bundles", json=payload)


def test_create_bundle_happy(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.bundles.bundles_repo.create_bundle",
        lambda ulpin, name, alu_ids, created_by: FAKE_BUNDLE,
    )
    response = _post_bundle(
        {
            "ulpin": "DEMO-ULPIN-001",
            "name": "Demo south bundle",
            "alu_ids": ["ALU-10m-DEMO-001", "ALU-10m-DEMO-002"],
            "created_by": "0x2222222222222222222222222222222222222222",
        }
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["ulpin"] == "DEMO-ULPIN-001"
    assert body["status"] == "DRAFT"
    assert len(body["alus"]) == 2


def test_create_bundle_cross_parcel_422(monkeypatch) -> None:
    def raise_err(ulpin, name, alu_ids, created_by):
        raise BundleError(
            422, "ALU not found or not in parcel DEMO-ULPIN-001: [ALU-999]"
        )

    monkeypatch.setattr(
        "app.api.routes.bundles.bundles_repo.create_bundle", raise_err
    )
    response = _post_bundle(
        {
            "ulpin": "DEMO-ULPIN-001",
            "name": "x",
            "alu_ids": ["ALU-999"],
            "created_by": "0x2222222222222222222222222222222222222222",
        }
    )
    assert response.status_code == 422


def test_create_bundle_duplicate_422(monkeypatch) -> None:
    def raise_err(ulpin, name, alu_ids, created_by):
        raise BundleError(422, "duplicate ALU in request: [ALU-10m-DEMO-001]")

    monkeypatch.setattr(
        "app.api.routes.bundles.bundles_repo.create_bundle", raise_err
    )
    response = _post_bundle(
        {
            "ulpin": "DEMO-ULPIN-001",
            "name": "x",
            "alu_ids": ["ALU-10m-DEMO-001", "ALU-10m-DEMO-001"],
            "created_by": "0x2222222222222222222222222222222222222222",
        }
    )
    assert response.status_code == 422


def test_get_bundle_found(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.bundles.bundles_repo.get_bundle",
        lambda bundle_id: FAKE_BUNDLE,
    )
    response = client.get("/api/v1/bundles/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_bundle_missing_404(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.bundles.bundles_repo.get_bundle",
        lambda bundle_id: None,
    )
    response = client.get("/api/v1/bundles/999")
    assert response.status_code == 404


def test_patch_bundle_invalid_transition_409(monkeypatch) -> None:
    def raise_err(bundle_id, status):
        raise BundleError(409, "invalid transition ARCHIVED -> ACTIVE")

    monkeypatch.setattr(
        "app.api.routes.bundles.bundles_repo.set_bundle_status", raise_err
    )
    response = client.patch("/api/v1/bundles/1", json={"status": "ACTIVE"})
    assert response.status_code == 409


def test_patch_bundle_happy(monkeypatch) -> None:
    updated = dict(FAKE_BUNDLE, status="ACTIVE")
    monkeypatch.setattr(
        "app.api.routes.bundles.bundles_repo.set_bundle_status",
        lambda bundle_id, status: updated,
    )
    response = client.patch("/api/v1/bundles/1", json={"status": "ACTIVE"})
    assert response.status_code == 200
    assert response.json()["status"] == "ACTIVE"
