from __future__ import annotations

from fastapi.testclient import TestClient

import app.api.routes.orders as oreg
from app.api.main import app
from app.repositories.orders import OrderError

client = TestClient(app)

GOOD_BUYER = "0x2222222222222222222222222222222222222222"
GOOD_SELLER = "0x3333333333333333333333333333333333333333"
GOOD_BYTES32 = "0x17e154661ceb2ad6498e30d294d0ec717c016dc5b58d0dc0d04b9211ea7c9d62"


def _install_repo_mocks(monkeypatch, create=None, get=None, fund=None):
    if create is not None:
        monkeypatch.setattr(oreg.orders_repo, "create_order", create)
    if get is not None:
        monkeypatch.setattr(oreg.orders_repo, "get_order", get)
    if fund is not None:
        monkeypatch.setattr(oreg.orders_repo, "fund_order", fund)


class TestCreateOrder:
    def test_happy_path_created(self, monkeypatch) -> None:
        created = {
            "id": 7,
            "listing_id": 3,
            "buyer_wallet": GOOD_BUYER,
            "seller_wallet": GOOD_SELLER,
            "amount_wei": "10000000000000000",
            "state": "CREATED",
            "chain_order": None,
            "tx_hash": None,
            "evidence_hash": None,
            "created_at": "2026-10-29T16:40:00+00:00",
            "updated_at": "2026-10-29T16:40:00+00:00",
        }

        def create(listing_id, buyer_wallet):
            assert listing_id == 3
            assert buyer_wallet == GOOD_BUYER
            return created

        _install_repo_mocks(monkeypatch, create=create)
        response = client.post(
            "/api/v1/orders",
            json={"listing_id": 3, "buyer_wallet": GOOD_BUYER},
        )
        assert response.status_code == 201, response.text
        body = response.json()
        assert body["id"] == 7
        assert body["state"] == "CREATED"
        assert body["amount_wei"] == "10000000000000000"
        assert body["chain_order_id"] is None
        assert body["checks"] == []
        assert body["decision"] is None

    def test_self_buy_409(self, monkeypatch) -> None:
        def raise_err(listing_id, buyer_wallet):
            raise OrderError(409, "Buyer cannot be the seller")

        _install_repo_mocks(monkeypatch, create=raise_err)
        response = client.post(
            "/api/v1/orders",
            json={"listing_id": 3, "buyer_wallet": GOOD_SELLER},
        )
        assert response.status_code == 409

    def test_unverified_buyer_409(self, monkeypatch) -> None:
        def raise_err(listing_id, buyer_wallet):
            raise OrderError(409, "Buyer KYC not VERIFIED")

        _install_repo_mocks(monkeypatch, create=raise_err)
        response = client.post(
            "/api/v1/orders",
            json={"listing_id": 3, "buyer_wallet": GOOD_BUYER},
        )
        assert response.status_code == 409

    def test_listing_not_listed_409(self, monkeypatch) -> None:
        def raise_err(listing_id, buyer_wallet):
            raise OrderError(409, "Listing is not LISTED")

        _install_repo_mocks(monkeypatch, create=raise_err)
        response = client.post(
            "/api/v1/orders",
            json={"listing_id": 3, "buyer_wallet": GOOD_BUYER},
        )
        assert response.status_code == 409

    def test_missing_fields_422(self) -> None:
        response = client.post("/api/v1/orders", json={"listing_id": 3})
        assert response.status_code == 422


class TestFundOrder:
    def test_happy_path_funded(self, monkeypatch) -> None:
        funded = {
            "id": 7,
            "listing_id": 3,
            "buyer_wallet": GOOD_BUYER,
            "seller_wallet": GOOD_SELLER,
            "amount_wei": "10000000000000000",
            "state": "FUNDED",
            "chain_order": GOOD_BYTES32,
            "tx_hash": "0xabcdef" + "0" * 58,
            "evidence_hash": None,
            "created_at": "2026-10-29T16:40:00+00:00",
            "updated_at": "2026-10-29T17:00:00+00:00",
        }

        def fund(order_id, chain_order_id, tx_hash):
            assert order_id == 7
            return funded

        _install_repo_mocks(monkeypatch, fund=fund)
        response = client.post(
            "/api/v1/orders/7/funded",
            json={"chain_order_id": GOOD_BYTES32, "tx_hash": funded["tx_hash"]},
        )
        assert response.status_code == 200, response.text
        assert response.json()["state"] == "FUNDED"
        assert response.json()["chain_order_id"] == GOOD_BYTES32

    def test_duplicate_funding_409(self, monkeypatch) -> None:
        def raise_err(order_id, chain_order_id, tx_hash):
            raise OrderError(409, "Order is not CREATED")

        _install_repo_mocks(monkeypatch, fund=raise_err)
        response = client.post(
            "/api/v1/orders/7/funded",
            json={"chain_order_id": GOOD_BYTES32, "tx_hash": "0x" + "1" * 64},
        )
        assert response.status_code == 409

    def test_invalid_bytes32_422(self, monkeypatch) -> None:
        def raise_err(order_id, chain_order_id, tx_hash):
            raise OrderError(422, "chain_order_id must be 0x + 64 hex chars")

        _install_repo_mocks(monkeypatch, fund=raise_err)
        response = client.post(
            "/api/v1/orders/7/funded",
            json={"chain_order_id": "not-bytes32", "tx_hash": "0x" + "1" * 64},
        )
        assert response.status_code == 422

    def test_chain_order_mismatch_422(self, monkeypatch) -> None:
        def raise_err(order_id, chain_order_id, tx_hash):
            raise OrderError(422, "chain_order_id does not match the order")

        _install_repo_mocks(monkeypatch, fund=raise_err)
        response = client.post(
            "/api/v1/orders/7/funded",
            json={"chain_order_id": GOOD_BYTES32, "tx_hash": "0x" + "1" * 64},
        )
        assert response.status_code == 422

    def test_not_found_404(self, monkeypatch) -> None:
        _install_repo_mocks(monkeypatch, fund=lambda order_id, c, t: None)
        response = client.post(
            "/api/v1/orders/999/funded",
            json={"chain_order_id": GOOD_BYTES32, "tx_hash": "0x" + "1" * 64},
        )
        assert response.status_code == 404


class TestGetOrder:
    def test_found(self, monkeypatch) -> None:
        order = {
            "id": 7,
            "listing_id": 3,
            "buyer_wallet": GOOD_BUYER,
            "seller_wallet": GOOD_SELLER,
            "amount_wei": "10000000000000000",
            "state": "FUNDED",
            "chain_order": GOOD_BYTES32,
            "tx_hash": "0x" + "1" * 64,
            "evidence_hash": None,
            "created_at": "2026-10-29T16:40:00+00:00",
            "updated_at": "2026-10-29T17:00:00+00:00",
        }
        monkeypatch.setattr(oreg.orders_repo, "get_order", lambda order_id: order)
        response = client.get("/api/v1/orders/7")
        assert response.status_code == 200
        assert response.json()["chain_order_id"] == GOOD_BYTES32
        assert response.json()["checks"] == []

    def test_missing_404(self, monkeypatch) -> None:
        monkeypatch.setattr(oreg.orders_repo, "get_order", lambda order_id: None)
        response = client.get("/api/v1/orders/999")
        assert response.status_code == 404
