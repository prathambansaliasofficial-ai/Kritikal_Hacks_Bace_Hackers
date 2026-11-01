<!--
  GENERATED FILE. Source: docs/api-contract.md
  Do not edit this copy. Edit the root file, then run: npm run sync:docs
-->
# API Contract — v1 target

This file fixes the shared shapes **before** the tasks that implement them. If code and this
file disagree, fix the code or update this file in the same batch. Do not invent extra fields.

Status: endpoints marked with a task ID are **not implemented until that task is done**.
Base URLs: backend `http://localhost:8000`, middleware `http://127.0.0.1:8090`.
All bodies are JSON. Timestamps are ISO-8601 UTC. `Content-Type: application/json`.

## 1. Common rules

| Item | Rule |
|---|---|
| ULPIN | string, 3–64 chars, `^[A-Za-z0-9/_.-]+$` |
| wallet | string, `^0x[a-fA-F0-9]{40}$` |
| bytes32 | string, `^0x[a-fA-F0-9]{64}$` |
| money | decimal **string** in wei, e.g. `"10000000000000000"`; never a JS float |
| order ID | backend `BIGSERIAL` as JSON number |
| error | FastAPI: `{"detail": string}`; middleware: `{"error": string}` |
| auth | prototype only: `X-Officer-Token: <DEV_OFFICER_TOKEN>` |
| CORS | frontend origin `http://localhost:5173` |
| demo data | every demo record/response property includes `demo: true`; DB source field is `DEMO_FIXTURE_NOT_OFFICIAL` |

Enums (exact strings):

- `GeometryStatus`: `AVAILABLE`, `N/D`
- `AluLevel`: `1km`, `100m`, `10m`, `1m`, `0.1m2`
- `BundleStatus`: `DRAFT`, `ACTIVE`, `PAUSED`, `ARCHIVED`
- `UserRole`: `CITIZEN`, `OFFICER`
- `KycStatus`: `PENDING`, `VERIFIED`, `REJECTED`
- `ListingStatus`: `DRAFT`, `LISTED`, `PAUSED`, `SOLD`, `CANCELLED`
- `OrderState`: `CREATED`, `FUNDED`, `SETTLED`, `REFUNDED`, `FAILED`
- `EvidenceStatus`: `PENDING`, `CLEAN`, `NEEDS_REVIEW`, `REJECTED`
- `ReviewDecision`: `APPROVE`, `REJECT`
- `TradeDecision`: `APPROVED`, `NEEDS_REVIEW`, `REJECTED`
- `CheckName`: `LISTED`, `BUNDLE_INTACT`, `KYC_WALLET`, `ZONING_OK`, `FUNDS_IN_ESCROW`, `TRADE_MATCH`
- `ChainOrderState`: `0` None, `1` Funded, `2` Settled, `3` Refunded

## 2. Shared objects

### 2.1 Parcel Feature

```json
{
  "type": "Feature",
  "id": "DEMO-ULPIN-001",
  "geometry": { "type": "MultiPolygon", "coordinates": [[[[73.8055, 18.5055]]]] },
  "properties": {
    "ulpin": "DEMO-ULPIN-001",
    "geometry_status": "AVAILABLE",
    "attributes": { "owner_name": "Demo Owner", "district": "Pune", "zoning": "Residential" },
    "demo": true
  }
}
```

`geometry` is whatever `ST_AsGeoJSON(geometry)` returns (Polygon or MultiPolygon).

### 2.2 ALU Feature

```json
{
  "type": "Feature",
  "id": "ALU-10m-2067-1260",
  "geometry": { "type": "Polygon", "coordinates": [[[73.806, 18.506]]] },
  "properties": {
    "alu_id": "ALU-10m-2067-1260",
    "parent_id": "ALU-100m-206-126",
    "level": "10m",
    "area_sqm": 100,
    "demo": true
  }
}
```

### 2.3 Evidence field and sheet

Exactly 21 keys, no more, no fewer:

`ulpin`, `cadastral_map`, `satellite_imagery`, `record_of_rights`, `registration_deeds`,
`master_plan`, `building_permissions`, `completion_occupancy`, `encumbrances`,
`mortgages_liens`, `land_use_zoning`, `utility_infrastructure`, `property_tax_arrears`,
`valuation_circle_rate`, `infrastructure_row`, `environmental_buffers`, `restriction_zones`,
`service_linkages`, `litigation_stays`, `change_detection`, `workflow_tracking`.

```json
{
  "value": "Residential",
  "status": "AVAILABLE",
  "source": "https://example.gov/parcel/DEMO-ULPIN-001",
  "retrieved_at": "2026-10-29T16:40:00Z"
}
```

`EvidenceField.status` is one of `AVAILABLE`, `PARTIAL`, `N/A`, `N/D`. Missing field =>
`{"value": null, "status": "N/D", "source": null, "retrieved_at": null}`.

```json
{
  "id": 1,
  "ulpin": "DEMO-ULPIN-001",
  "status": "PENDING",
  "evidence_hash": "0x<64 hex>",
  "tinyfish_run_id": "run_...",
  "fields": { "ulpin": { "...": "..." } },
  "sources": ["https://..."],
  "created_at": "2026-10-29T16:40:00Z"
}
```

### 2.4 Check result and order

```json
{
  "name": "LISTED",
  "passed": true,
  "reason": "Listing is LISTED.",
  "blocking": true
}
```

```json
{
  "id": 7,
  "listing_id": 3,
  "buyer_wallet": "0x1111111111111111111111111111111111111111",
  "seller_wallet": "0x2222222222222222222222222222222222222222",
  "amount_wei": "10000000000000000",
  "state": "FUNDED",
  "chain_order_id": "0x<64 hex>",
  "tx_hash": "0x<64 hex>",
  "evidence_hash": "0x<64 hex>",
  "checks": [],
  "decision": null,
  "decided_at": null,
  "created_at": "2026-10-29T16:40:00Z",
  "updated_at": "2026-10-29T16:40:00Z"
}
```

`decision` is `null` until evaluate, then one of `APPROVED`, `NEEDS_REVIEW`, `REJECTED`.
`checks` is `[]` until evaluate, then exactly six `CheckResult` objects in the order listed above.

## 3. Backend endpoints

### `GET /health` — T0.3 (implemented)

```json
{
  "status": "ok",
  "service": "Land Market API",
  "environment": "development",
  "database": { "status": "ok", "postgis_version": "3.5.0", "error": null }
}
```

### `GET /api/v1/parcels/{ulpin}` — T2.1

Returns `Parcel Feature`. Unknown ULPIN => `404 {"detail":"Parcel not found"}`.

### `GET /api/v1/parcels?bbox=minLon,minLat,maxLon,maxLat&limit=100` — T2.1

Returns `{"type":"FeatureCollection","features":[ParcelFeature...]}`.
`limit` default 100, max 100; invalid bbox => 422.

### `GET /api/v1/alus?bbox=minLon,minLat,maxLon,maxLat&level=10m` — T2.2

Returns `{"type":"FeatureCollection","features":[AluFeature...]}`.
Unknown level => 422. More than 1500 cells => `422 {"detail":"Zoom in: 1501 cells exceeds 1500"}`.

### `POST /api/v1/bundles` — T2.3

Request:

```json
{
  "ulpin": "DEMO-ULPIN-001",
  "name": "Demo south bundle",
  "alu_ids": ["ALU-10m-DEMO-001", "ALU-10m-DEMO-002"],
  "created_by": "0x2222222222222222222222222222222222222222"
}
```

Response `201`:

```json
{
  "id": 1,
  "ulpin": "DEMO-ULPIN-001",
  "name": "Demo south bundle",
  "status": "DRAFT",
  "alus": [{ "alu_id": "ALU-10m-DEMO-001", "level": "10m" }],
  "created_by": "0x2222222222222222222222222222222222222222",
  "created_at": "2026-10-29T16:40:00Z"
}
```

Errors: ALU not in parcel / duplicate ALU => 422; unknown ULPIN => 404.

### `GET /api/v1/bundles/{id}` — T2.3

Returns the bundle object above. Missing => 404.

### `PATCH /api/v1/bundles/{id}` — T2.3

Request `{"status":"ACTIVE"}`. Allowed transitions: `DRAFT→ACTIVE`, `ACTIVE→PAUSED`,
`PAUSED→ACTIVE`, any non-ARCHIVED→`ARCHIVED`. Invalid => 409.

### `POST /api/v1/verifications` — T3.2

Request `{"ulpin":"DEMO-ULPIN-001","source_url":"https://...","goal":"optional"}`.
The backend calls middleware `/verify/evidence`, validates the 21 fields, stores the sheet,
and returns:

```json
{
  "ulpin": "DEMO-ULPIN-001",
  "status": "PENDING",
  "evidence_id": 1,
  "evidence_hash": "0x<64 hex>",
  "tinyfish_run_id": "run_...",
  "fields": { "ulpin": { "...": "..." } },
  "sources": ["https://..."]
}
```

Middleware down => 503. Invalid/inexact 21-field sheet => 422.

### `GET /api/v1/evidence/{id}` — T3.2

Returns the full evidence sheet object (§2.3). Missing => 404.

### `GET /api/v1/evidence?ulpin=DEMO-ULPIN-001` — T3.2

Returns `{"items":[EvidenceSheet...]}` newest first. Unknown ULPIN => empty list.

### `GET /api/v1/reviews?status=PENDING` — T3.3

Returns:

```json
{
  "items": [
    {
      "evidence_id": 1,
      "ulpin": "DEMO-ULPIN-001",
      "status": "PENDING",
      "evidence_hash": "0x<64 hex>",
      "created_at": "2026-10-29T16:40:00Z"
    }
  ]
}
```

Allowed filter: `PENDING`, `NEEDS_REVIEW`; default `PENDING`.

### `POST /api/v1/reviews/{id}/decision` — T3.3

Headers: `X-Officer-Token`. Request:

```json
{ "decision": "APPROVE", "reason": "Evidence matches the demo parcel.", "officer": "officer@demo" }
```

`REJECT` requires non-empty `reason`. Response: updated EvidenceSheet. Wrong transition => 409.
Missing/wrong token => 401.

### `POST /api/v1/users` — T4.1

Request `{"wallet_address":"0x...","role":"CITIZEN"}`. Upsert by wallet. Response `200`:

```json
{
  "wallet_address": "0x2222222222222222222222222222222222222222",
  "role": "CITIZEN",
  "kyc_status": "PENDING",
  "created_at": "2026-10-29T16:40:00Z",
  "updated_at": "2026-10-29T16:40:00Z"
}
```

### `GET /api/v1/users/{wallet}` — T4.1

Returns the user object. Missing => 404. Invalid wallet => 422.

### `POST /api/v1/users/{wallet}/kyc` — T4.1

Headers: `X-Officer-Token`. Request `{"status":"VERIFIED","reason":"demo KYC"}`.
Response: updated user. Invalid wallet => 422; bad token => 401.

### `POST /api/v1/listings` — T4.2

Request:

```json
{
  "bundle_id": 1,
  "seller_wallet": "0x2222222222222222222222222222222222222222",
  "price_wei": "10000000000000000"
}
```

Response `201`:

```json
{
  "id": 3,
  "bundle_id": 1,
  "ulpin": "DEMO-ULPIN-001",
  "seller_wallet": "0x2222222222222222222222222222222222222222",
  "price_wei": "10000000000000000",
  "status": "DRAFT",
  "created_at": "2026-10-29T16:40:00Z"
}
```

Rules: seller KYC `VERIFIED`, bundle `ACTIVE`, price > 0, no other active listing for bundle.
Violations => 409. Unknown bundle/seller => 404.

### `GET /api/v1/listings?status=LISTED` — T4.2

Returns `{"items":[Listing...]}`. Default filter `LISTED`.

### `PATCH /api/v1/listings/{id}` — T4.2

Request `{"status":"LISTED"}`. Allowed: `DRAFT→LISTED`, `LISTED→PAUSED|CANCELLED`,
`PAUSED→LISTED|CANCELLED`, `LISTED→SOLD` only by settlement. Invalid => 409.

### `POST /api/v1/orders` — T4.3

Request `{"listing_id":3,"buyer_wallet":"0x..."}`. Response `201`:

```json
{
  "id": 7,
  "listing_id": 3,
  "buyer_wallet": "0x1111111111111111111111111111111111111111",
  "seller_wallet": "0x2222222222222222222222222222222222222222",
  "amount_wei": "10000000000000000",
  "state": "CREATED",
  "chain_order_id": null,
  "tx_hash": null,
  "evidence_hash": null,
  "checks": [],
  "decision": null,
  "created_at": "2026-10-29T16:40:00Z",
  "updated_at": "2026-10-29T16:40:00Z"
}
```

Rules: buyer KYC `VERIFIED`, listing `LISTED`, buyer ≠ seller, amount = listing price.
Self-buy / unverified / not listed => 409.

### `POST /api/v1/orders/{id}/funded` — T4.3

Request `{"chain_order_id":"0x<64 hex>","tx_hash":"0x<64 hex>"}`.
State `CREATED→FUNDED`. Duplicate funding => 409. Wrong bytes32 => 422.
Backend recomputes `chain_order_id` as defined in `docs/decisions.md`; mismatch => 422.

### `POST /api/v1/orders/{id}/evaluate` — T5.2

Runs six checks, stores `checks`, `decision`, `decided_at`, and triggers settlement:
`APPROVED` → settle; `REJECTED` → refund; `NEEDS_REVIEW` → no chain call.
Response: updated order object. Order not `FUNDED` => 409.

### `GET /api/v1/orders/{id}` — T4.3 / T5.2

Returns the order object with `checks` and `decision`. Missing => 404.

## 4. Middleware endpoints

### `GET /health` — T0.4 (implemented)

```json
{ "status": "ok", "service": "land-market-middleware", "tinyfishConfigured": true, "chainConfigured": true }
```

### `POST /verify/evidence` — T0.4

Request `{"ulpin":"DEMO-ULPIN-001","sourceUrl":"https://...","goal":"optional"}`.
Response: `EvidenceSheet` with `sourceUrl`, `agentStatus`, `runId`, `fields`, `sources`,
`rawResult`. TinyFish failure => 502.

### `POST /escrow/settle` — T0.4

Request `{"orderId":"0x<64 hex>"}`. Response:

```json
{ "orderId": "0x<64 hex>", "txHash": "0x<64 hex>", "blockNumber": 12, "status": 1 }
```

### `POST /escrow/refund` — T0.4

Same request/response as settle.

### `GET /escrow/status/{orderId}` — T5.3

Response `{"orderId":"0x<64 hex>","state":1,"label":"Funded"}`.
Invalid order ID => 400; chain error => 502.

## 5. Frontend wallet/chain rules

- Chain: local Hardhat `31337`; Sepolia `11155111` only after T6.3.
- `chain_order_id = keccak256(utf8("landmarket-order:" + String(order.id)))`, computed with
  `ethers.id(...)` and sent to both backend and contract.
- Escrow call: `createOrder(bytes32 orderId, address seller, bytes32 evidenceHash)` with
  `value = amount_wei`.
- Money never goes through `Number`; use `BigInt` / decimal strings.
- Missing `VITE_ESCROW_ADDRESS` => visible warning, no crash.
- Review actions use `VITE_OFFICER_TOKEN` as the `X-Officer-Token` header (prototype only).
- Demo banner text: `Testnet only, not a legal title transfer.`

## 6. Change protocol

Any shape change must update this file and `docs/decisions.md` in the same PR, then run
`npm run sync:docs && npm run check:docs`. Module copies are snapshots, not editable sources.
