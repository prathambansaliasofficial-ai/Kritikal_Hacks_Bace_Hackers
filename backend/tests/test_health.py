from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_health_returns_service_metadata() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "Land Market API"
    assert body["status"] in {"ok", "degraded"}
    assert "database" in body


def test_verification_rejects_blank_ulpin() -> None:
    response = client.post("/api/v1/verifications", json={"ulpin": ""})

    assert response.status_code == 422
