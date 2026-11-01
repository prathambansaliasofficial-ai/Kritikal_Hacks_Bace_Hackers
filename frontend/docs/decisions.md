<!--
  GENERATED FILE. Source: docs/decisions.md
  Do not edit this copy. Edit the root file, then run: npm run sync:docs
-->
# Decisions — fixed constants

These values are deliberately frozen so independent frontend/backend/middleware agents
produce compatible code. Change a value only with a matching update to `docs/api-contract.md`.

## 1. Demo boundary

- All seeded parcels, owners, zoning, and evidence are demo data.
- Parcel `geometry_source` and UI badges use `DEMO_FIXTURE_NOT_OFFICIAL`.
- TinyFish may read public pages, but no government record is modified or claimed official.
- Chain is local Hardhat or Sepolia testnet only. No mainnet, no real money.
- KYC is a prototype status flag. It is not identity verification.

## 2. Demo parcel and ALUs

Parcel polygon (closed ring, lon/lat WGS84):

```text
73.8055 18.5055, 73.8095 18.5055, 73.8095 18.5095, 73.8055 18.5095, 73.8055 18.5055
```

Seed IDs:

| ID | Level | Geometry (lon/lat box) | Parent |
|---|---|---|---|
| `DEMO-ULPIN-001` | parcel | `73.8055,18.5055 → 73.8095,18.5095` | — |
| `ALU-100m-DEMO-000` | `100m` | `73.8060,18.5060 → 73.8080,18.5080` | — |
| `ALU-10m-DEMO-001` | `10m` | `73.8060,18.5060 → 73.8070,18.5070` | `ALU-100m-DEMO-000` |
| `ALU-10m-DEMO-002` | `10m` | `73.8070,18.5060 → 73.8080,18.5070` | `ALU-100m-DEMO-000` |
| `ALU-10m-DEMO-003` | `10m` | `73.8060,18.5070 → 73.8070,18.5080` | `ALU-100m-DEMO-000` |
| `ALU-10m-DEMO-004` | `10m` | `73.8070,18.5070 → 73.8080,18.5080` | `ALU-100m-DEMO-000` |

All four child ALUs link to the parcel with `relationship='CONTAINS'`. Seed IDs are fixed
fixtures; generated grid IDs use the formula below.

## 3. Deterministic ALU grid

Web Mercator forward (metres):

```text
R  = 6378137
x  = R * lon * pi / 180
y  = R * ln(tan(pi/4 + (lat * pi/180) / 2))
```

Inverse, with `lat` clamped to `±85.05112878` before forward projection:

```text
lon = (x / R) * 180 / pi
lat = (2 * atan(exp(y / R)) - pi/2) * 180 / pi
```

Level sizes (width × height, metres), fine → coarse:

```text
0.1m2: 0.1 × 1.0
1m:    1 × 1
10m:   10 × 10
100m:  100 × 100
1km:   1000 × 1000
```

Cell index and ID:

```text
ix = floor(x / width)
iy = floor(y / height)
slug(n) = n < 0 ? "m" + abs(n) : str(n)
alu_id = f"ALU-{level}-{slug(ix)}-{slug(iy)}"
```

Parent = next coarser level (`0.1m2 → 1m → 10m → 100m → 1km`), using the parent's width/height
and the same `x`, `y`. `1km` has `parent_id = null`.

Polygon ring order:

```text
[x0,y0] → [x1,y0] → [x1,y1] → [x0,y1] → [x0,y0]
x0 = ix * width, x1 = x0 + width
y0 = iy * height, y1 = y0 + height
```

`area_sqm` = `width * height` as a number (`0.1` for `0.1m2`). Cell cap is 1500; over cap => 422.

## 4. Evidence hash

Canonical payload:

```json
{
  "ulpin": "DEMO-ULPIN-001",
  "fields": { "<21 keys>": { "value": null, "status": "N/D", "source": null, "retrieved_at": null } },
  "sources": ["https://..."]
}
```

Rules:

- Keep exactly the 21 keys from `docs/api-contract.md` §2.3.
- Missing fields become the `N/D` object above.
- `sources` is sorted and de-duplicated.
- Canonical JSON: `json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`.
- Hash: `"0x" + sha256(canonical.encode("utf-8")).hexdigest()` (64 lowercase hex chars).
- Store lowercase. Same sheet => same hash; never hash `rawResult`.

## 5. Order IDs and money

- Backend order ID: `orders.id` (`BIGSERIAL`, JSON number).
- Chain order ID:

```text
chain_order_id = keccak256(utf8("landmarket-order:" + str(order.id)))
```

Frontend uses `ethers.id("landmarket-order:" + String(order.id))`. Backend recomputes and
rejects a mismatch. Contract receives the same bytes32.
- Money is integer wei in a decimal string. Frontend uses `BigInt`; never `Number`.
- Demo price: `"10000000000000000"` wei (`0.01 ETH`).

## 6. Chain

| Item | Value |
|---|---|
| Local chain ID | `31337` |
| Local RPC | `http://127.0.0.1:8545` |
| Sepolia chain ID | `11155111` |
| Contract state | `0 None`, `1 Funded`, `2 Settled`, `3 Refunded` |
| Operator | backend signer; only address allowed to `settle`/`refund` |
| Buyer | `msg.sender` on `createOrder`; must not equal seller |
| Evidence anchor | `evidence_hash` passed to `createOrder` |

Settlement mapping: `APPROVED → settle`, `REJECTED → refund`, `NEEDS_REVIEW → no chain call`.
`SETTLED`/`REFUNDED` are terminal; repeat calls are idempotent at the API layer.

## 7. Auth and environment

Prototype officer auth: header `X-Officer-Token` must equal backend env `DEV_OFFICER_TOKEN`.
No JWT, no wallet signature. Document this as a stub.

| Service | Variables |
|---|---|
| backend | `DATABASE_URL`, `MIDDLEWARE_URL`, `MIDDLEWARE_TIMEOUT_SECONDS`, `CORS_ORIGINS`, `DEV_OFFICER_TOKEN` |
| middleware | `TINYFISH_API_KEY`, `DEFAULT_SOURCE_URL`, `TINYFISH_TIMEOUT_MS`, `CHAIN_RPC_URL`, `CHAIN_ID`, `ESCROW_CONTRACT_ADDRESS`, `OPERATOR_PRIVATE_KEY`, `SEPOLIA_RPC_URL`, `DEPLOYER_PRIVATE_KEY`, `PORT`, `HOST` |
| frontend | `VITE_API_BASE_URL`, `VITE_ESCROW_ADDRESS`, `VITE_CHAIN_ID`, `VITE_CHAIN_NAME`, `VITE_EXPLORER_URL`, `VITE_OFFICER_TOKEN` |

Never commit `.env` files or real keys. The only local private key allowed is Hardhat account #0.

## 8. Missing-data policy

- Never invent an evidence value, source, UUID, run ID, or transaction hash.
- Missing evidence field => `N/D`; missing whole sheet => verification fails, not fake pass.
- Failed middleware/chain call => 502/503 and no state change.
- Ambiguous evidence => `NEEDS_REVIEW`, never forced `APPROVED`.
- Any blocking check failure => `REJECTED` and refund path.

## 9. Future infrastructure (post-hackathon)

These are planned but NOT implemented for the 4 Nov hackathon demo:

- **Database**: Currently PostGIS (Docker). Planned migration to Supabase (PostgreSQL + PostGIS) after hackathon. `DATABASE_URL` will point to Supabase instance.
- **Deployment**: Currently local development (localhost:8000 backend, localhost:8090 middleware, localhost:5173 frontend). Planned deployment to Vercel (frontend) after hackathon. `VITE_API_BASE_URL` will point to production backend.
- TinyFish permanent API key (`TINYFISH_API_KEY`) is used for live evidence runs during the demo.
