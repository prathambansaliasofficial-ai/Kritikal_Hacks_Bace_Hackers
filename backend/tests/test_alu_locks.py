from __future__ import annotations

from app.repositories import listings as listings_repo
from app.repositories.listings import ListingError

BUYER = "0x2222222222222222222222222222222222222222"


def _bundle(status="ACTIVE"):
    return {"id": 1, "ulpin": "DEMO-ULPIN-001", "status": status, "name": "b", "created_by": BUYER}


def _seller(kyc="VERIFIED"):
    return {
        "id": 1,
        "wallet_address": BUYER,
        "role": "CITIZEN",
        "kyc_status": kyc,
    }


def _row(listing_id: int, alu_id: str, status: str) -> dict:
    return {
        "id": listing_id,
        "bundle_id": 1,
        "ulpin": "DEMO-ULPIN-001",
        "seller_wallet": BUYER,
        "price_wei": "100",
        "status": status,
        "alu_id": alu_id,
        "created_at": "2026-10-29T16:40:00+00:00",
    }


def _install_create_mocks(monkeypatch, active=True, sold=False):
    monkeypatch.setattr(listings_repo, "get_bundle", lambda bid: _bundle())
    monkeypatch.setattr(listings_repo, "get_seller", lambda w: _seller())
    monkeypatch.setattr(
        listings_repo,
        "count_active_listings_for_bundle",
        lambda bid, eid=None, **kw: 0,
    )
    monkeypatch.setattr(
        listings_repo,
        "alu_has_sold_listing",
        lambda aid, eid=None, **kw: sold,
    )
    monkeypatch.setattr(
        listings_repo,
        "alu_has_active_listing",
        lambda aid, eid=None, **kw: active,
    )
    monkeypatch.setattr(
        listings_repo,
        "fetch_one",
        lambda *a, **k: _row(9, "ALU-10m-001", "DRAFT"),
    )


class TestAluLocks:
    def test_create_active_alu_rejected(self, monkeypatch) -> None:
        _install_create_mocks(monkeypatch, active=True, sold=False)
        try:
            listings_repo.create_listing(
                1, BUYER, "100", alu_id="ALU-10m-001"
            )
        except ListingError as error:
            assert error.status_code == 409
            assert "active" in error.detail.lower()
            return
        raise AssertionError("expected ListingError 409")

    def test_create_sold_alu_rejected(self, monkeypatch) -> None:
        _install_create_mocks(monkeypatch, active=False, sold=True)
        try:
            listings_repo.create_listing(
                1, BUYER, "100", alu_id="ALU-10m-001"
            )
        except ListingError as error:
            assert error.status_code == 409
            assert "sold" in error.detail.lower()
            return
        raise AssertionError("expected ListingError 409")

    def test_create_fresh_alu_success(self, monkeypatch) -> None:
        _install_create_mocks(monkeypatch, active=False, sold=False)
        row = listings_repo.create_listing(
            1, BUYER, "100", alu_id="ALU-10m-001"
        )
        assert row["status"] == "DRAFT"
        assert row["alu_id"] == "ALU-10m-001"

    def test_patch_to_listed_active_alu_rejected(self, monkeypatch) -> None:
        listing = _row(3, "ALU-10m-001", "DRAFT")
        monkeypatch.setattr(listings_repo, "get_listing", lambda lid: listing)
        monkeypatch.setattr(
            listings_repo,
            "count_active_listings_for_bundle",
            lambda bid, eid=None, **kw: 0,
        )
        monkeypatch.setattr(
            listings_repo,
            "alu_has_sold_listing",
            lambda aid, eid=None, **kw: False,
        )
        monkeypatch.setattr(
            listings_repo,
            "alu_has_active_listing",
            lambda aid, eid=None, **kw: True,
        )
        monkeypatch.setattr(
            listings_repo,
            "fetch_one",
            lambda *a, **k: _row(3, "ALU-10m-001", "LISTED"),
        )
        try:
            listings_repo.patch_listing_status(3, "LISTED")
        except ListingError as error:
            assert error.status_code == 409
            assert "active" in error.detail.lower()
            return
        raise AssertionError("expected ListingError 409")

    def test_patch_to_listed_sold_alu_rejected(self, monkeypatch) -> None:
        listing = _row(3, "ALU-10m-001", "DRAFT")
        monkeypatch.setattr(listings_repo, "get_listing", lambda lid: listing)
        monkeypatch.setattr(
            listings_repo,
            "count_active_listings_for_bundle",
            lambda bid, eid=None, **kw: 0,
        )
        monkeypatch.setattr(
            listings_repo,
            "alu_has_sold_listing",
            lambda aid, eid=None, **kw: True,
        )
        monkeypatch.setattr(
            listings_repo,
            "alu_has_active_listing",
            lambda aid, eid=None, **kw: False,
        )
        try:
            listings_repo.patch_listing_status(3, "LISTED")
        except ListingError as error:
            assert error.status_code == 409
            assert "sold" in error.detail.lower()
            return
        raise AssertionError("expected ListingError 409")

    def test_patch_to_listed_fresh_alu_success(self, monkeypatch) -> None:
        listing = _row(3, "ALU-10m-001", "DRAFT")
        monkeypatch.setattr(listings_repo, "get_listing", lambda lid: listing)
        monkeypatch.setattr(
            listings_repo,
            "count_active_listings_for_bundle",
            lambda bid, eid=None, **kw: 0,
        )
        monkeypatch.setattr(
            listings_repo,
            "alu_has_sold_listing",
            lambda aid, eid=None, **kw: False,
        )
        monkeypatch.setattr(
            listings_repo,
            "alu_has_active_listing",
            lambda aid, eid=None, **kw: False,
        )
        monkeypatch.setattr(
            listings_repo,
            "fetch_one",
            lambda *a, **k: _row(3, "ALU-10m-001", "LISTED"),
        )
        row = listings_repo.patch_listing_status(3, "LISTED")
        assert row["status"] == "LISTED"
