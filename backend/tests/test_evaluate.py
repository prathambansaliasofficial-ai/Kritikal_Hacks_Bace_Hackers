from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

import app.api.routes.orders as oreg
from app.api.main import app

client = TestClient(app)

BUYER = "0x2222222222222222222222222222222222222222"
SELLER = "0x3333333333333333333333333333333333333333"
GOOD_BYTES32 = "0x17e154661ceb2ad6498e30d294d0ec717c016dc5b58d0dc0d04b9211ea7c9d62"


def _order(state: str, **overrides: Any) -> dict[str, Any]:
    base = {
        "id": 7,
        "listing_id": 3,
        "buyer_wallet": BUYER,
        "seller_wallet": SELLER,
        "amount_wei": "10000000000000000",
        "state": state,
        "chain_order": GOOD_BYTES32,
        "tx_hash": None,
        "evidence_hash": None,
        "checks": [],
        "decision": None,
        "decided_at": None,
        "created_at": "2026-10-29T16:40:00+00:00",
        "updated_at": "2026-10-29T16:40:00+00:00",
    }
    base.update(overrides)
    return base


LISTING = {
    "id": 3,
    "bundle_id": 1,
    "ulpin": "DEMO-ULPIN-001",
    "seller_wallet": SELLER,
    "price_wei": "10000000000000000",
    "status": "LISTED",
}

BUNDLE = {
    "id": 1,
    "ulpin": "DEMO-ULPIN-001",
    "name": "Demo bundle",
    "status": "ACTIVE",
    "created_by": SELLER,
}


def _install_evaluate_mocks(
    monkeypatch,
    order_row: dict[str, Any],
    chain_state: int = 1,
    apply_called: list[str] | None = None,
    chain_fail: bool = False,
) -> None:
    current: dict[str, Any] = dict(order_row)

    def get_order(order_id: int) -> dict[str, Any]:
        return current

    monkeypatch.setattr(oreg.orders_repo, "get_order", get_order)
    monkeypatch.setattr(oreg.listings_repo, "get_listing", lambda listing_id: LISTING)
    monkeypatch.setattr(oreg.bundles_repo, "get_bundle", lambda bundle_id: BUNDLE)
    monkeypatch.setattr(
        oreg.bundles_repo,
        "get_bundle_alu_ids",
        lambda bundle_id: ["ALU-10m-DEMO-001", "ALU-10m-DEMO-002"],
    )
    monkeypatch.setattr(
        oreg.alus_repo,
        "alus_present_in_parcel",
        lambda ulpin, alu_ids: True,
    )
    monkeypatch.setattr(
        oreg.orders_repo,
        "alu_in_other_active_order",
        lambda alu_ids, order_id: False,
    )
    monkeypatch.setattr(
        oreg.users_repo,
        "get_user",
        lambda wallet: {"wallet_address": wallet, "kyc_status": "VERIFIED"},
    )
    monkeypatch.setattr(
        oreg.evidence_repo,
        "get_latest_evidence_for_ulpin",
        lambda ulpin: {
            "id": 1,
            "ulpin": ulpin,
            "status": "PENDING",
            "payload": {
                "ulpin": ulpin,
                "fields": {
                    "land_use_zoning": {
                        "value": "Residential",
                        "status": "AVAILABLE",
                        "source": "https://example.gov",
                        "retrieved_at": "2026-10-29T16:40:00Z",
                    }
                },
                "sources": ["https://example.gov"],
            },
            "created_at": "2026-10-29T16:40:00+00:00",
        },
    )

    async def fake_chain_state(chain_order_id: str) -> int:
        if chain_fail:
            raise oreg.ChainClientError("chain down")
        return chain_state

    monkeypatch.setattr(oreg, "get_chain_state", fake_chain_state)

    def save_evaluate(order_id, checks, decision):
        current["checks"] = checks
        current["decision"] = decision
        current["decided_at"] = "2026-10-29T17:00:00+00:00"
        return True

    monkeypatch.setattr(oreg.orders_repo, "save_evaluate", save_evaluate)

    async def fake_apply_decision(order: dict, decision: str) -> dict:
        if apply_called is not None:
            apply_called.append(decision)
        if decision == "APPROVED":
            current["state"] = "SETTLED"
            current["tx_hash"] = "0xsettled"
        elif decision == "REJECTED":
            current["state"] = "REFUNDED"
            current["tx_hash"] = "0xrefunded"
        return current

    monkeypatch.setattr(oreg, "apply_decision", fake_apply_decision)


class TestEvaluate:
    def test_approve_settle(self, monkeypatch) -> None:
        apply_called: list[str] = []
        _install_evaluate_mocks(
            monkeypatch,
            _order("FUNDED"),
            chain_state=1,
            apply_called=apply_called,
        )
        response = client.post("/api/v1/orders/7/evaluate")
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["decision"] == "APPROVED"
        assert body["state"] == "SETTLED"
        assert body["tx_hash"] == "0xsettled"
        assert len(body["checks"]) == 6
        assert apply_called == ["APPROVED"]

    def test_reject_refund(self, monkeypatch) -> None:
        apply_called: list[str] = []
        _install_evaluate_mocks(
            monkeypatch,
            _order("FUNDED"),
            chain_state=1,
            apply_called=apply_called,
        )
        listing_draft = dict(LISTING, status="DRAFT")
        monkeypatch.setattr(
            oreg.listings_repo, "get_listing", lambda listing_id: listing_draft
        )
        response = client.post("/api/v1/orders/7/evaluate")
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["decision"] == "REJECTED"
        assert body["state"] == "REFUNDED"
        assert apply_called == ["REJECTED"]
        assert any(c["name"] == "LISTED" and not c["passed"] for c in body["checks"])

    def test_review_missing_evidence(self, monkeypatch) -> None:
        apply_called: list[str] = []
        _install_evaluate_mocks(
            monkeypatch,
            _order("FUNDED"),
            chain_state=1,
            apply_called=apply_called,
        )
        monkeypatch.setattr(
            oreg.evidence_repo,
            "get_latest_evidence_for_ulpin",
            lambda ulpin: {
                "id": 1,
                "ulpin": ulpin,
                "status": "PENDING",
                "payload": {"ulpin": ulpin, "fields": {}, "sources": []},
                "created_at": "2026-10-29T16:40:00+00:00",
            },
        )
        response = client.post("/api/v1/orders/7/evaluate")
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["decision"] == "NEEDS_REVIEW"
        assert body["state"] == "FUNDED"  # no state change
        assert apply_called == ["NEEDS_REVIEW"]  # apply_decision invoked but no-ops
        assert any(c["name"] == "ZONING_OK" and not c["passed"] for c in body["checks"])

    def test_non_funded_409(self, monkeypatch) -> None:
        _install_evaluate_mocks(monkeypatch, _order("CREATED"))
        response = client.post("/api/v1/orders/7/evaluate")
        assert response.status_code == 409

    def test_not_found_404(self, monkeypatch) -> None:
        monkeypatch.setattr(oreg.orders_repo, "get_order", lambda order_id: None)
        response = client.post("/api/v1/orders/999/evaluate")
        assert response.status_code == 404

    def test_chain_down_502(self, monkeypatch) -> None:
        _install_evaluate_mocks(monkeypatch, _order("FUNDED"), chain_state=1, chain_fail=True)
        response = client.post("/api/v1/orders/7/evaluate")
        assert response.status_code == 502
