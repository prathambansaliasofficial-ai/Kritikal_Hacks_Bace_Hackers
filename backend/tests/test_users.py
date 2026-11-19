from __future__ import annotations

from fastapi.testclient import TestClient

import app.api.routes.users as urom
from app.api.main import app

client = TestClient(app)

GOOD_WALLET = "0x2222222222222222222222222222222222222222"
BAD_WALLET = "not-a-wallet"


def _settings_with_token(token: str = "test-officer-token"):
    from app.core.config import Settings

    return Settings(dev_officer_token=token)


class TestUsers:
    def test_invalid_wallet_422(self, monkeypatch) -> None:
        monkeypatch.setattr(
            urom, "get_settings", lambda: _settings_with_token()
        )
        response = client.post("/api/v1/users", json={"wallet_address": BAD_WALLET})
        assert response.status_code == 422

    def test_upsert_user_happy(self, monkeypatch) -> None:
        created = {
            "id": 1,
            "wallet_address": GOOD_WALLET,
            "role": "CITIZEN",
            "kyc_status": "PENDING",
            "created_at": "2026-10-29T16:40:00+00:00",
            "updated_at": "2026-10-29T16:40:00+00:00",
        }
        monkeypatch.setattr(
            urom.users_repo, "upsert_user", lambda wallet, role: created
        )
        response = client.post(
            "/api/v1/users",
            json={"wallet_address": GOOD_WALLET, "role": "CITIZEN"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["wallet_address"] == GOOD_WALLET
        assert body["role"] == "CITIZEN"
        assert body["kyc_status"] == "PENDING"

    def test_upsert_invalid_role_422(self, monkeypatch) -> None:
        monkeypatch.setattr(
            urom, "get_settings", lambda: _settings_with_token()
        )
        response = client.post(
            "/api/v1/users",
            json={"wallet_address": GOOD_WALLET, "role": "ADMIN"},
        )
        assert response.status_code == 422

    def test_get_user_found(self, monkeypatch) -> None:
        user = {
            "id": 1,
            "wallet_address": GOOD_WALLET,
            "role": "CITIZEN",
            "kyc_status": "PENDING",
            "created_at": "2026-10-29T16:40:00+00:00",
            "updated_at": "2026-10-29T16:40:00+00:00",
        }
        monkeypatch.setattr(urom.users_repo, "get_user", lambda wallet: user)
        response = client.get(f"/api/v1/users/{GOOD_WALLET}")
        assert response.status_code == 200
        assert response.json()["wallet_address"] == GOOD_WALLET

    def test_get_user_missing_404(self, monkeypatch) -> None:
        monkeypatch.setattr(urom.users_repo, "get_user", lambda wallet: None)
        response = client.get(f"/api/v1/users/{GOOD_WALLET}")
        assert response.status_code == 404

    def test_get_user_invalid_wallet_422(self) -> None:
        response = client.get(f"/api/v1/users/{BAD_WALLET}")
        assert response.status_code == 422


class TestKyc:
    def _headers(self, token: str | None = "test-officer-token") -> dict[str, str]:
        return {"X-Officer-Token": token} if token is not None else {}

    def test_missing_token_401(self, monkeypatch) -> None:
        monkeypatch.setattr(
            urom, "get_settings", lambda: _settings_with_token()
        )
        response = client.post(
            f"/api/v1/users/{GOOD_WALLET}/kyc",
            json={"status": "VERIFIED", "reason": "demo"},
        )
        assert response.status_code == 401

    def test_wrong_token_401(self, monkeypatch) -> None:
        monkeypatch.setattr(
            urom, "get_settings", lambda: _settings_with_token("real-token")
        )
        response = client.post(
            f"/api/v1/users/{GOOD_WALLET}/kyc",
            json={"status": "VERIFIED", "reason": "demo"},
            headers=self._headers("wrong"),
        )
        assert response.status_code == 401

    def test_invalid_wallet_422(self, monkeypatch) -> None:
        monkeypatch.setattr(
            urom, "get_settings", lambda: _settings_with_token()
        )
        response = client.post(
            f"/api/v1/users/{BAD_WALLET}/kyc",
            json={"status": "VERIFIED", "reason": "demo"},
            headers=self._headers(),
        )
        assert response.status_code == 422

    def test_invalid_status_422(self, monkeypatch) -> None:
        monkeypatch.setattr(
            urom, "get_settings", lambda: _settings_with_token()
        )
        response = client.post(
            f"/api/v1/users/{GOOD_WALLET}/kyc",
            json={"status": "FOO", "reason": "demo"},
            headers=self._headers(),
        )
        assert response.status_code == 422

    def test_kyc_update_200(self, monkeypatch) -> None:
        monkeypatch.setattr(
            urom, "get_settings", lambda: _settings_with_token()
        )
        updated = {
            "id": 1,
            "wallet_address": GOOD_WALLET,
            "role": "CITIZEN",
            "kyc_status": "VERIFIED",
            "created_at": "2026-10-29T16:40:00+00:00",
            "updated_at": "2026-10-29T17:00:00+00:00",
        }
        monkeypatch.setattr(
            urom.users_repo, "update_kyc", lambda wallet, status, reason: updated
        )
        response = client.post(
            f"/api/v1/users/{GOOD_WALLET}/kyc",
            json={"status": "VERIFIED", "reason": "demo KYC"},
            headers=self._headers(),
        )
        assert response.status_code == 200
        assert response.json()["kyc_status"] == "VERIFIED"
