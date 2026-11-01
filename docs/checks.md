# Six checks and decision policy

`backend/app/services/checks.py` implements these as pure functions. Each returns exactly:

```json
{ "name": "LISTED", "passed": true, "reason": "Listing is LISTED.", "blocking": true }
```

Names and order are fixed: `LISTED`, `BUNDLE_INTACT`, `KYC_WALLET`, `ZONING_OK`,
`FUNDS_IN_ESCROW`, `TRADE_MATCH`.

## Decision mapping

```text
any blocking check fails       -> REJECTED
else any non-blocking fails     -> NEEDS_REVIEW
else all pass                   -> APPROVED
```

Settlement: `APPROVED` → `settle()`; `REJECTED` → `refund()`; `NEEDS_REVIEW` → no chain call.
A middleware/chain outage is an API error (502/503), not a check result and not a decision.

## 1. LISTED — blocking

Pass when the order's listing exists and `listing.status == 'LISTED'`. A `SOLD`,
`PAUSED`, `CANCELLED`, or `DRAFT` listing fails.

## 2. BUNDLE_INTACT — blocking

Pass when all are true:

- listing has a `bundle_id`, bundle exists, `bundle.status == 'ACTIVE'`;
- `bundle_alus` contains at least one ALU;
- every bundle ALU exists and is linked to the listing's parcel with `CONTAINS`;
- no **other** order for the same bundle is in `CREATED`, `FUNDED`, or `SETTLED`
  (exclude the current order; `FAILED`/`REFUNDED` do not block).

This is a demo lock. Full per-ALU locking is stretch task T9.1.

## 3. KYC_WALLET — blocking

Pass when buyer and seller user rows exist, differ, and both have
`kyc_status == 'VERIFIED'`. Missing user or any other status fails.

## 4. ZONING_OK — non-blocking

Read evidence field `land_use_zoning`:

- `AVAILABLE` or `PARTIAL` with non-empty value:
  - value contains any restricted term (case-insensitive): `agricultural`, `restricted`,
    `forest`, `no-development`, `no development` → fail with `blocking: true`;
  - otherwise pass.
- `N/A`, `N/D`, missing field, or empty value → fail with `blocking: false` (review).

Demo assumption: residential/commercial/mixed values are tradeable. This is not legal advice.

## 5. FUNDS_IN_ESCROW — blocking

Pass when `order.state == 'FUNDED'` and middleware `GET /escrow/status/{chain_order_id}`
returns `state == 1`. `CREATED`, `SETTLED`, `REFUNDED`, or chain state `0/2/3` fails.
If the status call fails, evaluate returns 502; do not store a decision.

## 6. TRADE_MATCH — blocking

Pass when all are true:

- listing ULPIN == bundle ULPIN == parcel ULPIN;
- evidence ULPIN == parcel ULPIN;
- buyer wallet != seller wallet;
- `order.amount_wei == listing.price_wei`;
- backend-recomputed `chain_order_id` matches the stored value.

Missing evidence ULPIN fails with `blocking: false` (review); the other mismatches are
blocking. Evidence does not decide the trade by itself.

## Demo fixtures

- Parcel: `DEMO-ULPIN-001`; bundle: four `10m` ALUs.
- Buyer: `0x1111111111111111111111111111111111111111`.
- Seller: `0x2222222222222222222222222222222222222222`.
- Officer: `0x3333333333333333333333333333333333333333`.
- Price: `10000000000000000` wei.
- Evidence zoning: `Residential`; missing case: `N/D` → `NEEDS_REVIEW`.
