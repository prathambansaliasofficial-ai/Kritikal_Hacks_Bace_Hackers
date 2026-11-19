# Limitations — backend (prototype)

This document captures the deliberate scope boundaries of the Land Market
prototype backend. These are NOT bugs; they are documented prototype decisions
for the Kritical Hacks 2026 demo (4 Nov 2026).

## 1. Demo data (no official claim)

All seeded parcels, ALUs, owners, zoning, and evidence are demo fixtures. Every
demo record carries `DEMO_FIXTURE_NOT_OFFICIAL` in its `geometry_source`
(DB) or `demo: true` (API responses). The backend makes no claim that any
government record is official, modified, or legally valid.

## 2. KYC is a stub (not identity verification)

KYC is a prototype status flag (`PENDING`/`VERIFIED`/`REJECTED`) updated through
`POST /api/v1/users/{wallet}/kyc` gated by `X-Officer-Token` (`DEV_OFFICER_TOKEN`).
There is no JWT, no wallet signature, no real identity verification, and no OTP.
Officer auth is a stub; replace with real auth before production.

## 3. Testnet only (no real money)

The escrow chain is local Hardhat (chain ID 31337) or Sepolia testnet only.
No mainnet, no real money, no legal title transfer. `money` is integer wei in a
decimal string (`NUMERIC(78,0)`); never a float. Settlement calls
`POST /escrow/settle` / `POST /escrow/refund` on the middleware; mainnet
deployment is out of scope.

## 4. TinyFish evidence (no real portal guarantee)

Evidence is collected by the TinyFish middleware. The backend validates the
exact 21-field sheet, hashes it (canonical JSON SHA-256 with `0x` prefix), and
persists it. Missing fields become `N/D`; values are never invented. If the
TinyFish key is unavailable, tests mock the middleware; no live run is faked.

## 5. Error handling

All backend errors return `{"detail": string}` with an HTTP status code
(400/401/402/404/409/422/502/503). A global exception handler returns a generic
500 for any unhandled error; no stack traces or internals leak. Failed
middleware/chain calls cause no state change.

## 6. Validation

- ULPIN: `^[A-Za-z0-9/_.-]+$`, 3–64 chars.
- Wallet: `^0x[a-fA-F0-9]{40}$`.
- bytes32 (`chain_order_id`/`tx_hash`): `^0x[a-fA-F0-9]{64}$`.
- bbox: `minLon,minLat,maxLon,maxLat`, ranges `[-180,180]`/`[-90,90]`, min ≤ max.
- limit: 1–100 (parcels); ALU grid capped at 1500 cells (422 over cap).

## 7. Partial-bundle sale rules

A listing references a bundle (and optionally a single ALU via `alu_id`). An
ALU can be in at most one active listing (DRAFT/LISTED/PAUSED) — enforced by a
partial unique index on `listings(alu_id)`. A sold ALU (`status = SOLD`) is
locked and cannot be re-listed — enforced by the repository layer. Listings are
bundle-scoped: one active listing per bundle. Partial sale of a bundle (selling
individual ALUs within an active bundle listing) is NOT supported in this
prototype; each ALU needs its own active listing to be tradeable.

## 8. Out of scope

- Real title/registry writes, legal conveyance, mainnet deployment,
  JWT/OAuth auth, production DB (Supabase migration is post-hackathon),
  public demo URL (lead's `T9.3-D`).
