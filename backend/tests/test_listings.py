from __future__ import annotations

from fastapi.testclient import TestClient

import app.api.routes.listings as lmod
from app.api.main import app
from app.repositories.listings import ListingError

client = TestClient(app)


def _install_repo_mocks(monkeypatch, create=None, list_fn=None, patch=None):
    if create is not None:
        monkeypatch.setattr(lmod.listings_repo, "create_listing", create)
    if list_fn is not None:
        monkeypatch.setattr(lmod.listings_repo, "list_listings", list_fn)
    if patch is not None:
        monkeypatch.setattr(lmod.listings_repo, "patch_listing_status", patch)


class TestCreateListing:
    def test_happy_path_create_draft(self, monkeypatch) -> None:
        created = {
            "id": 3,
            "bundle_id": 1,
            "ulpin": "DEMO-ULPIN-001",
            "seller_wallet": "0x2222222222222222222222222222222222222222",
            "price_wei": "10000000000000000",
            "status": "DRAFT",
            "created_at": "2026-10-29T16:40:00+00:00",
        }

        def create(bundle_id, seller_wallet, price_wei):
            assert bundle_id == 1
            return created

        _install_repo_mocks(monkeypatch, create=create)
        response = client.post(
            "/api/v1/listings",
            json={
                "bundle_id": 1,
                "seller_wallet": "0x2222222222222222222222222222222222222222",
                "price_wei": "10000000000000000",
            },
        )
        assert response.status_code == 201, response.text
        assert response.json()["id"] == 3
        assert response.json()["status"] == "DRAFT"

    def test_unknown_bundle_404(self, monkeypatch) -> None:
        def raise_err(bundle_id, seller_wallet, price_wei):
            raise ListingError(404, "Bundle not found")

        _install_repo_mocks(monkeypatch, create=raise_err)
        response = client.post(
            "/api/v1/listings",
            json={
                "bundle_id": 999,
                "seller_wallet": "0x2222222222222222222222222222222222222222",
                "price_wei": "100",
            },
        )
        assert response.status_code == 404

    def test_unverified_seller_409(self, monkeypatch) -> None:
        def raise_err(bundle_id, seller_wallet, price_wei):
            raise ListingError(409, "Seller KYC not VERIFIED")

        _install_repo_mocks(monkeypatch, create=raise_err)
        response = client.post(
            "/api/v1/listings",
            json={
                "bundle_id": 1,
                "seller_wallet": "0x2222222222222222222222222222222222222222",
                "price_wei": "100",
            },
        )
        assert response.status_code == 409

    def test_bundle_not_active_409(self, monkeypatch) -> None:
        def raise_err(bundle_id, seller_wallet, price_wei):
            raise ListingError(409, "Bundle is not ACTIVE")

        _install_repo_mocks(monkeypatch, create=raise_err)
        response = client.post(
            "/api/v1/listings",
            json={
                "bundle_id": 1,
                "seller_wallet": "0x2222222222222222222222222222222222222222",
                "price_wei": "100",
            },
        )
        assert response.status_code == 409

    def test_duplicate_active_listing_409(self, monkeypatch) -> None:
        def raise_err(bundle_id, seller_wallet, price_wei):
            raise ListingError(409, "Bundle already has an active listing")

        _install_repo_mocks(monkeypatch, create=raise_err)
        response = client.post(
            "/api/v1/listings",
            json={
                "bundle_id": 1,
                "seller_wallet": "0x2222222222222222222222222222222222222222",
                "price_wei": "100",
            },
        )
        assert response.status_code == 409

    def test_invalid_price_422(self, monkeypatch) -> None:
        def create(bundle_id, seller_wallet, price_wei):
            if int(price_wei) <= 0:
                raise ListingError(422, "price_wei must be greater than 0")
            return {"id": 3, "status": "DRAFT"}

        _install_repo_mocks(monkeypatch, create=create)
        response = client.post(
            "/api/v1/listings",
            json={
                "bundle_id": 1,
                "seller_wallet": "0x2222222222222222222222222222222222222222",
                "price_wei": "0",
            },
        )
        assert response.status_code == 422


class TestListListings:
    def test_items_returned(self, monkeypatch) -> None:
        items = [
            {
                "id": 3,
                "bundle_id": 1,
                "ulpin": "DEMO-ULPIN-001",
                "seller_wallet": "0x2222222222222222222222222222222222222222",
                "price_wei": "10000000000000000",
                "status": "LISTED",
                "created_at": "2026-10-29T16:40:00+00:00",
            }
        ]
        _install_repo_mocks(monkeypatch, list_fn=lambda status="LISTED": items)
        response = client.get("/api/v1/listings?status=LISTED")
        assert response.status_code == 200
        assert response.json()["items"] == items


class TestPatchListing:
    def test_draft_to_listed_happy(self, monkeypatch) -> None:
        updated = {
            "id": 3,
            "bundle_id": 1,
            "ulpin": "DEMO-ULPIN-001",
            "seller_wallet": "0x2222222222222222222222222222222222222222",
            "price_wei": "10000000000000000",
            "status": "LISTED",
            "created_at": "2026-10-29T16:40:00+00:00",
        }

        def patch(listing_id, status):
            assert listing_id == 3
            assert status == "LISTED"
            return updated

        _install_repo_mocks(monkeypatch, patch=patch)
        response = client.patch("/api/v1/listings/3", json={"status": "LISTED"})
        assert response.status_code == 200
        assert response.json()["status"] == "LISTED"

    def test_invalid_transition_409(self, monkeypatch) -> None:
        def raise_err(listing_id, status):
            raise ListingError(409, "invalid transition DRAFT -> SOLD")

        _install_repo_mocks(monkeypatch, patch=raise_err)
        response = client.patch("/api/v1/listings/3", json={"status": "SOLD"})
        assert response.status_code == 409

    def test_duplicate_active_on_listed_409(self, monkeypatch) -> None:
        def raise_err(listing_id, status):
            raise ListingError(409, "Bundle already has an active listing")

        _install_repo_mocks(monkeypatch, patch=raise_err)
        response = client.patch("/api/v1/listings/3", json={"status": "LISTED"})
        assert response.status_code == 409

    def test_not_found_404(self, monkeypatch) -> None:
        _install_repo_mocks(monkeypatch, patch=lambda listing_id, status: None)
        response = client.patch("/api/v1/listings/999", json={"status": "LISTED"})
        assert response.status_code == 404
