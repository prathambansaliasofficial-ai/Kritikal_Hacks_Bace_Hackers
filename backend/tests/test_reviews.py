from __future__ import annotations

from fastapi.testclient import TestClient

import app.api.routes.reviews as rmod
from app.api.main import app

client = TestClient(app)


def _settings_with_token(token: str = "test-officer-token"):
    from app.core.config import Settings

    return Settings(dev_officer_token=token)


def _install_repo_mocks(monkeypatch, rows, decide_result):
    monkeypatch.setattr(
        rmod.evidence_repo, "list_reviews", lambda status: rows
    )
    monkeypatch.setattr(rmod.evidence_repo, "decide_review", lambda *a, **k: decide_result)


class TestListReviews:
    def test_pending_items(self, monkeypatch) -> None:
        rows = [
            {
                "evidence_id": 1,
                "ulpin": "DEMO-ULPIN-001",
                "status": "PENDING",
                "payload": {"evidence_hash": "0xabc"},
                "created_at": "2026-10-29T16:40:00+00:00",
            }
        ]
        _install_repo_mocks(monkeypatch, rows, None)
        response = client.get("/api/v1/reviews?status=PENDING")
        assert response.status_code == 200
        body = response.json()
        assert len(body["items"]) == 1
        assert body["items"][0]["evidence_id"] == 1
        assert body["items"][0]["evidence_hash"] == "0xabc"

    def test_invalid_status_422(self) -> None:
        response = client.get("/api/v1/reviews?status=APPROVED")
        assert response.status_code == 422


class TestDecideReview:
    def _auth_headers(self, token: str | None = "test-officer-token") -> dict:
        return {"X-Officer-Token": token} if token is not None else {}

    def test_approve_happy(self, monkeypatch) -> None:
        monkeypatch.setattr(
            rmod, "get_settings", lambda: _settings_with_token()
        )
        updated = {
            "evidence_id": 1,
            "ulpin": "DEMO-ULPIN-001",
            "status": "CLEAN",
            "payload": {"evidence_hash": "0xabc"},
            "reviewed_by": "officer@demo",
            "review_reason": "Looks good",
            "reviewed_at": "2026-10-29T17:00:00+00:00",
            "created_at": "2026-10-29T16:40:00+00:00",
        }
        _install_repo_mocks(monkeypatch, [], updated)
        response = client.post(
            "/api/v1/reviews/1/decision",
            json={"decision": "APPROVE", "reason": "Looks good", "officer": "officer@demo"},
            headers=self._auth_headers(),
        )
        assert response.status_code == 200, response.text
        assert response.json()["status"] == "CLEAN"

    def test_reject_happy(self, monkeypatch) -> None:
        monkeypatch.setattr(
            rmod, "get_settings", lambda: _settings_with_token()
        )
        updated = {
            "evidence_id": 1,
            "ulpin": "DEMO-ULPIN-001",
            "status": "REJECTED",
            "payload": {"evidence_hash": "0xabc"},
            "reviewed_by": "officer@demo",
            "review_reason": "Bad",
            "reviewed_at": "2026-10-29T17:00:00+00:00",
            "created_at": "2026-10-29T16:40:00+00:00",
        }
        _install_repo_mocks(monkeypatch, [], updated)
        response = client.post(
            "/api/v1/reviews/1/decision",
            json={"decision": "REJECT", "reason": "Bad", "officer": "officer@demo"},
            headers=self._auth_headers(),
        )
        assert response.status_code == 200
        assert response.json()["status"] == "REJECTED"

    def test_missing_token_401(self, monkeypatch) -> None:
        monkeypatch.setattr(
            rmod, "get_settings", lambda: _settings_with_token()
        )
        _install_repo_mocks(monkeypatch, [], None)
        response = client.post(
            "/api/v1/reviews/1/decision",
            json={"decision": "APPROVE", "reason": "x"},
        )
        assert response.status_code == 401

    def test_wrong_token_401(self, monkeypatch) -> None:
        monkeypatch.setattr(
            rmod, "get_settings", lambda: _settings_with_token("real-token")
        )
        _install_repo_mocks(monkeypatch, [], None)
        response = client.post(
            "/api/v1/reviews/1/decision",
            json={"decision": "APPROVE", "reason": "x"},
            headers=self._auth_headers("wrong"),
        )
        assert response.status_code == 401

    def test_reject_without_reason_422(self, monkeypatch) -> None:
        monkeypatch.setattr(
            rmod, "get_settings", lambda: _settings_with_token()
        )

        def boom(*args, **kwargs):
            raise ValueError("reason_required")

        monkeypatch.setattr(rmod.evidence_repo, "decide_review", boom)
        response = client.post(
            "/api/v1/reviews/1/decision",
            json={"decision": "REJECT", "reason": ""},
            headers=self._auth_headers(),
        )
        assert response.status_code == 422

    def test_already_decided_409(self, monkeypatch) -> None:
        monkeypatch.setattr(
            rmod, "get_settings", lambda: _settings_with_token()
        )

        def boom(*args, **kwargs):
            raise ValueError("already_decided")

        monkeypatch.setattr(rmod.evidence_repo, "decide_review", boom)
        response = client.post(
            "/api/v1/reviews/1/decision",
            json={"decision": "APPROVE", "reason": "x"},
            headers=self._auth_headers(),
        )
        assert response.status_code == 409

    def test_not_found_404(self, monkeypatch) -> None:
        monkeypatch.setattr(
            rmod, "get_settings", lambda: _settings_with_token()
        )
        _install_repo_mocks(monkeypatch, [], None)
        response = client.post(
            "/api/v1/reviews/999/decision",
            json={"decision": "APPROVE", "reason": "x"},
            headers=self._auth_headers(),
        )
        assert response.status_code == 404
