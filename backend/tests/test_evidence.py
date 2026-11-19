from __future__ import annotations

from typing import Any

import httpx
from fastapi.testclient import TestClient

from app.api.main import app
from app.services.evidence import (
    EVIDENCE_FIELDS,
    ND_FIELD,
    canonical_hash,
    normalize_sheet,
)

client = TestClient(app)


class FakeResponse:
    def __init__(self, status_code: int, json_data: dict[str, Any]):
        self.status_code = status_code
        self._json = json_data
        self.text = str(json_data)

    def json(self) -> dict[str, Any]:
        return self._json


class FakeClient:
    def __init__(self, timeout: float | None = None):
        self.status_code = 200
        self.json_data: dict[str, Any] = {}
        self.raise_on_post: Exception | None = None
        self.last_request: Any = None

    async def __aenter__(self) -> FakeClient:
        return self

    async def __aexit__(self, *args: object) -> bool:
        return False

    async def post(self, url: str, json: Any = None) -> FakeResponse:
        self.last_request = json
        if self.raise_on_post is not None:
            raise self.raise_on_post
        return FakeResponse(self.status_code, self.json_data)


class TestEvidenceService:
    def test_missing_fields_become_nd(self) -> None:
        result = normalize_sheet({})
        assert len(result) == 21
        for key in EVIDENCE_FIELDS:
            assert result[key] == ND_FIELD, f"field {key} should be N/D"

    def test_extra_fields_are_dropped(self) -> None:
        result = normalize_sheet({"fake_field": {"value": "x"}})
        assert len(result) == 21
        assert "fake_field" not in result

    def test_non_dict_fields_become_all_nd(self) -> None:
        result = normalize_sheet("not a dict")
        assert len(result) == 21
        for key in EVIDENCE_FIELDS:
            assert result[key] == ND_FIELD

    def test_partial_fields_kept(self) -> None:
        input_fields = {
            "ulpin": {
                "value": "DEMO-ULPIN-001",
                "status": "AVAILABLE",
                "source": "https://example.gov",
                "retrieved_at": "2026-10-29T16:40:00Z",
            }
        }
        result = normalize_sheet(input_fields)
        assert result["ulpin"]["value"] == "DEMO-ULPIN-001"
        for key in EVIDENCE_FIELDS:
            if key != "ulpin":
                assert result[key] == ND_FIELD, f"field {key} should be N/D"

    def test_hash_deterministic(self) -> None:
        fields = normalize_sheet({})
        sources = ["https://example.gov/parcel/DEMO-ULPIN-001"]
        h1 = canonical_hash("DEMO-ULPIN-001", fields, sources)
        h2 = canonical_hash("DEMO-ULPIN-001", fields, sources)
        assert h1 == h2
        assert h1.startswith("0x")
        assert len(h1) == 66

    def test_hash_changes_with_input(self) -> None:
        fields = normalize_sheet({})
        h1 = canonical_hash("DEMO-ULPIN-001", fields, ["https://a.com"])
        h2 = canonical_hash("DEMO-ULPIN-002", fields, ["https://a.com"])
        assert h1 != h2

    def test_sources_sorted_and_deduped(self) -> None:
        fields = normalize_sheet({})
        h1 = canonical_hash("DEMO-ULPIN-001", fields, ["https://b.com", "https://a.com", "https://a.com"])
        h2 = canonical_hash("DEMO-ULPIN-001", fields, ["https://a.com", "https://b.com"])
        assert h1 == h2

    def test_hash_is_lowercase(self) -> None:
        fields = normalize_sheet({})
        h = canonical_hash("DEMO-ULPIN-001", fields, ["https://example.gov"])
        assert h[2:] == h[2:].lower()


def _install_fake_client(monkeypatch, vmod, status_code: int, json_data: dict) -> FakeClient:
    fake = FakeClient()
    fake.status_code = status_code
    fake.json_data = json_data
    monkeypatch.setattr(vmod.httpx, "AsyncClient", lambda timeout=None: fake)
    return fake


class TestVerificationRoute:
    def test_happy_path(self, monkeypatch) -> None:
        import app.api.routes.verifications as vmod

        created: dict[str, Any] = {}
        monkeypatch.setattr(
            vmod.evidence_repo,
            "create_evidence_sheet",
            lambda ulpin, payload, source_refs, tinyfish_run_id, evidence_hash: created.update(
                {
                    "ulpin": ulpin,
                    "payload": payload,
                    "source_refs": source_refs,
                    "tinyfish_run_id": tinyfish_run_id,
                    "evidence_hash": evidence_hash,
                }
            )
            or 7,
        )
        fake = _install_fake_client(
            monkeypatch,
            vmod,
            200,
            {
                "runId": "run_abc",
                "agentStatus": "PENDING",
                "fields": {
                    "ulpin": {
                        "value": "DEMO-ULPIN-001",
                        "status": "AVAILABLE",
                        "source": "https://example.gov/parcel/DEMO-ULPIN-001",
                        "retrieved_at": "2026-10-29T16:40:00Z",
                    }
                },
                "sources": ["https://example.gov/parcel/DEMO-ULPIN-001"],
            },
        )
        response = client.post(
            "/api/v1/verifications",
            json={"ulpin": "DEMO-ULPIN-001", "source_url": "https://example.gov", "goal": "demo"},
        )
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["ulpin"] == "DEMO-ULPIN-001"
        assert body["status"] == "PENDING"
        assert body["evidence_id"] == 7
        assert body["evidence_hash"].startswith("0x")
        assert len(body["evidence_hash"]) == 66
        assert body["tinyfish_run_id"] == "run_abc"
        assert len(body["fields"]) == 21
        assert body["fields"]["ulpin"]["status"] == "AVAILABLE"
        assert body["sources"] == ["https://example.gov/parcel/DEMO-ULPIN-001"]
        assert created["tinyfish_run_id"] == "run_abc"
        assert created["source_refs"] == ["https://example.gov/parcel/DEMO-ULPIN-001"]
        # middleware was called with camelCase sourceUrl
        sent = fake.last_request
        assert sent is not None
        assert "sourceUrl" in sent
        assert "source_url" not in sent
        assert sent["ulpin"] == "DEMO-ULPIN-001"

    def test_middleware_down_503(self, monkeypatch) -> None:
        import app.api.routes.verifications as vmod

        fake = FakeClient()
        fake.raise_on_post = httpx.RequestError("boom", request=httpx.Request("POST", "http://x"))
        monkeypatch.setattr(vmod.httpx, "AsyncClient", lambda timeout=None: fake)
        response = client.post("/api/v1/verifications", json={"ulpin": "DEMO-ULPIN-001"})
        assert response.status_code == 503

    def test_invalid_sheet_422(self, monkeypatch) -> None:
        import app.api.routes.verifications as vmod

        _install_fake_client(
            monkeypatch,
            vmod,
            200,
            {"runId": "run_abc", "agentStatus": "PENDING", "fields": "not-a-dict"},
        )
        response = client.post("/api/v1/verifications", json={"ulpin": "DEMO-ULPIN-001"})
        assert response.status_code == 422

    def test_middleware_error_502(self, monkeypatch) -> None:
        import app.api.routes.verifications as vmod

        _install_fake_client(monkeypatch, vmod, 502, {})
        response = client.post("/api/v1/verifications", json={"ulpin": "DEMO-ULPIN-001"})
        assert response.status_code == 502

    def test_blank_ulpin_422(self) -> None:
        response = client.post("/api/v1/verifications", json={"ulpin": ""})
        assert response.status_code == 422
