# Checks — six-check trade rule engine

Policy for `backend/app/services/checks.py`. These rules decide whether a trade
(order) may be settled, rejected, or needs officer review. They are prototype
assumptions for the hackathon demo and are intentionally simple.

## Decision mapping

| Outcome | Condition |
|---------|-----------|
| `APPROVED` | All six checks pass |
| `REJECTED` | Any check fails (all checks are blocking) |
| `NEEDS_REVIEW` | No blocking check failed, but evidence is missing / N/D |

A blocking check failure triggers the refund path; `NEEDS_REVIEW` triggers no
chain call and sends the evidence to the officer review queue.

## The six checks

All checks return `CheckResult(name, passed, reason, blocking)`. Every check is
blocking (`blocking=true`), so a failure rejects the trade.

### 1. LISTED
The listing referenced by the order must exist and have status `LISTED`, and the
order must reference that listing.

- Pass: listing `status == "LISTED"` and order.listing_id == listing.id.
- Fail: any other listing status, or order references a different listing.

### 2. BUNDLE_INTACT
The listing's bundle must be `ACTIVE`, every ALU in the bundle must be present,
and no ALU in the bundle may be locked by another active order.

- Pass: bundle `status == "ACTIVE"`, all ALUs present, no ALU conflict.
- Fail: bundle not ACTIVE, missing ALU, or ALU in another active order.

### 3. KYC_WALLET
Both buyer and seller must have KYC status `VERIFIED`.

- Pass: `buyer.kyc_status == "VERIFIED"` and `seller.kyc_status == "VERIFIED"`.
- Fail: either party is `PENDING` or `REJECTED`.

### 4. ZONING_OK
Evidence field `land_use_zoning` must be present and indicate a tradeable zone
(`available`, `partial`, `residential`, `commercial`, `mixed`). It must not be
`restricted` or `agricultural`.

- Pass: zoning available/partial/tradeable.
- Fail: zoning restricted/agricultural or unrecognized.
- Missing (N/D): fails but contributes to `NEEDS_REVIEW` when no other check
  blocked.

### 5. FUNDS_IN_ESCROW
The order must be `FUNDED` and the chain escrow state must be `Funded (1)`.

- Pass: `order.state == "FUNDED"` and chain state `1`.
- Fail: order not FUNDED, or chain not Funded.

### 6. TRADE_MATCH
Listing ULPIN, bundle ULPIN, parcel ULPIN, and evidence ULPIN must all refer to
the same parcel, and buyer and seller must be different wallets.

- Pass: all ULPINs equal and buyer != seller.
- Fail: any ULPIN mismatch, or buyer == seller.

## Demo assumptions

- All seeded data is `DEMO_FIXTURE_NOT_OFFICIAL`; not an official land record.
- KYC is a prototype status flag, not identity verification.
- Chain is local Hardhat (31337) or Sepolia testnet; no mainnet, no real money.
- Evidence is collected by TinyFish; the backend applies these fixed rules.
- Missing evidence defaults to `N/D` and never forces an approval.
