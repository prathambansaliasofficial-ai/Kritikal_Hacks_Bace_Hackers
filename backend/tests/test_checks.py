from __future__ import annotations

from app.services.checks import (
    CheckResult,
    check_bundle_intact,
    check_funds_in_escrow,
    check_kyc_wallet,
    check_listed,
    check_trade_match,
    check_zoning_ok,
)

LISTED_PASS = CheckResult("LISTED", True, "Listing is LISTED.", True)


def test_listed_pass() -> None:
    result = check_listed("LISTED", 3, 3)
    assert result == LISTED_PASS
    assert result.passed is True


def test_listed_fail_status() -> None:
    result = check_listed("DRAFT", 3, 3)
    assert result.passed is False
    assert result.blocking is True
    assert "DRAFT" in result.reason


def test_listed_fail_mismatch() -> None:
    result = check_listed("LISTED", 3, 4)
    assert result.passed is False
    assert result.blocking is True


def test_bundle_intact_pass() -> None:
    result = check_bundle_intact("ACTIVE", True, False)
    assert result.passed is True
    assert result.blocking is True


def test_bundle_intact_fail_not_active() -> None:
    result = check_bundle_intact("PAUSED", True, False)
    assert result.passed is False
    assert result.blocking is True


def test_bundle_intact_fail_missing_alu() -> None:
    result = check_bundle_intact("ACTIVE", False, False)
    assert result.passed is False
    assert result.blocking is True


def test_bundle_intact_fail_alu_conflict() -> None:
    result = check_bundle_intact("ACTIVE", True, True)
    assert result.passed is False
    assert result.blocking is True


def test_kyc_wallet_pass() -> None:
    result = check_kyc_wallet("VERIFIED", "VERIFIED")
    assert result.passed is True
    assert result.blocking is True


def test_kyc_wallet_fail_buyer() -> None:
    result = check_kyc_wallet("PENDING", "VERIFIED")
    assert result.passed is False
    assert result.blocking is True


def test_kyc_wallet_fail_seller() -> None:
    result = check_kyc_wallet("VERIFIED", "REJECTED")
    assert result.passed is False
    assert result.blocking is True


def test_zoning_ok_pass_available() -> None:
    result = check_zoning_ok("available")
    assert result.passed is True


def test_zoning_ok_pass_partial() -> None:
    result = check_zoning_ok("partial")
    assert result.passed is True


def test_zoning_ok_fail_restricted() -> None:
    result = check_zoning_ok("restricted")
    assert result.passed is False
    assert result.blocking is True


def test_zoning_ok_fail_agricultural() -> None:
    result = check_zoning_ok("agricultural")
    assert result.passed is False
    assert result.blocking is True


def test_zoning_ok_fail_missing() -> None:
    result = check_zoning_ok(None)
    assert result.passed is False
    assert result.blocking is True


def test_funds_in_escrow_pass() -> None:
    result = check_funds_in_escrow("FUNDED", 1)
    assert result.passed is True


def test_funds_in_escrow_fail_not_funded() -> None:
    result = check_funds_in_escrow("CREATED", 1)
    assert result.passed is False
    assert result.blocking is True


def test_funds_in_escrow_fail_chain_not_funded() -> None:
    result = check_funds_in_escrow("FUNDED", 0)
    assert result.passed is False
    assert result.blocking is True


def test_trade_match_pass() -> None:
    result = check_trade_match("D-U-001", "D-U-001", "D-U-001", "D-U-001", "0xbuyer", "0xseller")
    assert result.passed is True


def test_trade_match_fail_ulpin_mismatch() -> None:
    result = check_trade_match("D-U-001", "D-U-002", "D-U-001", "D-U-001", "0xbuyer", "0xseller")
    assert result.passed is False
    assert result.blocking is True


def test_trade_match_fail_same_party() -> None:
    result = check_trade_match("D-U-001", "D-U-001", "D-U-001", "D-U-001", "0xsame", "0xsame")
    assert result.passed is False
    assert result.blocking is True


def test_all_check_names_covered() -> None:
    from app.services.checks import CHECK_NAMES

    assert len(CHECK_NAMES) == 6
    assert set(CHECK_NAMES) == {
        "LISTED",
        "BUNDLE_INTACT",
        "KYC_WALLET",
        "ZONING_OK",
        "FUNDS_IN_ESCROW",
        "TRADE_MATCH",
    }


def _base_context() -> dict:
    return {
        "listing_status": "LISTED",
        "order_listing_id": 3,
        "listing_id": 3,
        "bundle_status": "ACTIVE",
        "alus_present": True,
        "alu_in_other_active_order": False,
        "buyer_kyc": "VERIFIED",
        "seller_kyc": "VERIFIED",
        "land_use_zoning": "Residential",
        "order_state": "FUNDED",
        "chain_state": 1,
        "listing_ulpin": "DEMO-ULPIN-001",
        "bundle_ulpin": "DEMO-ULPIN-001",
        "parcel_ulpin": "DEMO-ULPIN-001",
        "evidence_ulpin": "DEMO-ULPIN-001",
        "buyer_wallet": "0xbuyer",
        "seller_wallet": "0xseller",
    }


def test_run_checks_all_pass_approved() -> None:
    from app.services.checks import decide, run_checks

    results = run_checks(_base_context())
    assert len(results) == 6
    assert all(r.passed for r in results)
    assert decide(results) == "APPROVED"


def test_run_checks_hard_fail_rejected() -> None:
    from app.services.checks import decide, run_checks

    ctx = _base_context()
    ctx["listing_status"] = "DRAFT"
    results = run_checks(ctx)
    assert any(not r.passed and r.name == "LISTED" for r in results)
    assert decide(results) == "REJECTED"


def test_run_checks_zoning_missing_review() -> None:
    from app.services.checks import decide, run_checks

    ctx = _base_context()
    ctx["land_use_zoning"] = None
    results = run_checks(ctx)
    zoning = [r for r in results if r.name == "ZONING_OK"][0]
    assert not zoning.passed
    assert zoning.missing_evidence is True
    assert decide(results) == "NEEDS_REVIEW"
