from __future__ import annotations

from dataclasses import dataclass

# All six checks are blocking: any failure rejects the trade and triggers a refund.
CHECK_NAMES = (
    "LISTED",
    "BUNDLE_INTACT",
    "KYC_WALLET",
    "ZONING_OK",
    "FUNDS_IN_ESCROW",
    "TRADE_MATCH",
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    reason: str
    blocking: bool


def check_listed(listing_status: str, order_listing_id: int, listing_id: int) -> CheckResult:
    """LISTED — listing status is LISTED and the order references this listing."""
    if listing_status != "LISTED":
        return CheckResult(
            "LISTED",
            False,
            f"Listing status is {listing_status}, not LISTED.",
            True,
        )
    if order_listing_id != listing_id:
        return CheckResult(
            "LISTED", False, "Order does not reference the listing being traded.", True
        )
    return CheckResult("LISTED", True, "Listing is LISTED.", True)


def check_bundle_intact(
    bundle_status: str, alus_present: bool, alu_in_other_active_order: bool
) -> CheckResult:
    """BUNDLE_INTACT — bundle is ACTIVE, all ALUs present, no ALU in another active order."""
    if bundle_status != "ACTIVE":
        return CheckResult(
            "BUNDLE_INTACT", False, f"Bundle status is {bundle_status}, not ACTIVE.", True
        )
    if not alus_present:
        return CheckResult(
            "BUNDLE_INTACT", False, "Not all bundle ALUs are present.", True
        )
    if alu_in_other_active_order:
        return CheckResult(
            "BUNDLE_INTACT",
            False,
            "An ALU in the bundle is locked by another active order.",
            True,
        )
    return CheckResult("BUNDLE_INTACT", True, "Bundle is ACTIVE and intact.", True)


def check_kyc_wallet(buyer_kyc: str, seller_kyc: str) -> CheckResult:
    """KYC_WALLET — both buyer and seller are KYC VERIFIED."""
    if buyer_kyc != "VERIFIED":
        return CheckResult(
            "KYC_WALLET", False, f"Buyer KYC is {buyer_kyc}, not VERIFIED.", True
        )
    if seller_kyc != "VERIFIED":
        return CheckResult(
            "KYC_WALLET", False, f"Seller KYC is {seller_kyc}, not VERIFIED.", True
        )
    return CheckResult("KYC_WALLET", True, "Buyer and seller KYC are VERIFIED.", True)


def check_zoning_ok(land_use_zoning: str | None) -> CheckResult:
    """ZONING_OK — evidence land_use_zoning is available/partial and not restricted/agricultural."""
    if land_use_zoning is None:
        return CheckResult(
            "ZONING_OK", False, "Zoning evidence is missing (N/D).", True
        )
    zoning = land_use_zoning.strip().lower()
    if zoning in ("restricted", "agricultural"):
        return CheckResult(
            "ZONING_OK", False, f"Zoning '{land_use_zoning}' is not tradeable.", True
        )
    if zoning in ("available", "partial", "residential", "commercial", "mixed"):
        return CheckResult(
            "ZONING_OK", True, f"Zoning '{land_use_zoning}' is tradeable.", True
        )
    return CheckResult(
        "ZONING_OK", False, f"Unrecognized zoning '{land_use_zoning}'.", True
    )


def check_funds_in_escrow(order_state: str, chain_state: int | None) -> CheckResult:
    """FUNDS_IN_ESCROW — order is FUNDED and chain state is Funded (1)."""
    if order_state != "FUNDED":
        return CheckResult(
            "FUNDS_IN_ESCROW", False, f"Order state is {order_state}, not FUNDED.", True
        )
    if chain_state != 1:
        return CheckResult(
            "FUNDS_IN_ESCROW",
            False,
            f"Chain state is {chain_state}, not Funded (1).",
            True,
        )
    return CheckResult("FUNDS_IN_ESCROW", True, "Funds are in escrow.", True)


def check_trade_match(
    listing_ulpin: str,
    bundle_ulpin: str | None,
    parcel_ulpin: str | None,
    evidence_ulpin: str | None,
    buyer_wallet: str,
    seller_wallet: str,
) -> CheckResult:
    """TRADE_MATCH — listing, bundle, parcel, evidence ULPINs and parties all agree."""
    if parcel_ulpin is not None and listing_ulpin != parcel_ulpin:
        return CheckResult(
            "TRADE_MATCH",
            False,
            f"Listing ULPIN {listing_ulpin} != parcel ULPIN {parcel_ulpin}.",
            True,
        )
    if bundle_ulpin is not None and listing_ulpin != bundle_ulpin:
        return CheckResult(
            "TRADE_MATCH",
            False,
            f"Listing ULPIN {listing_ulpin} != bundle ULPIN {bundle_ulpin}.",
            True,
        )
    if evidence_ulpin is not None and listing_ulpin != evidence_ulpin:
        return CheckResult(
            "TRADE_MATCH",
            False,
            f"Listing ULPIN {listing_ulpin} != evidence ULPIN {evidence_ulpin}.",
            True,
        )
    if buyer_wallet == seller_wallet:
        return CheckResult(
            "TRADE_MATCH", False, "Buyer and seller are the same wallet.", True
        )
    return CheckResult(
        "TRADE_MATCH",
        True,
        "Listing, bundle, parcel, evidence and parties match.",
        True,
    )
