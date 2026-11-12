# Log-B — Backend Gitlog

Last updated: **2026-10-29 22:10 IST**
Progress: **Phase 0 done; C1 (T1.1–T1.3) next hai.**

Format: `[.]` = completed, `[]` = pending. Har item par date, time (IST) aur session.
Task IDs `../whole_plan.md` se match karte hain.
Branch: `backend/<name>` only. Owner map: `../docs/task-ownership.md`.

---

# YEH SAB HO GYA

## Session 1 — 2026-10-29 21:24 IST (log setup)

### Log files

- [.] 21:24 — `backend/log-b.md` aur `../whole_plan.md` create; purana `backend-logbook.md` remove.
- [.] 21:24 — Backend source code change: koi nahi.

## Session 2 — 2026-10-29 21:40–21:43 IST (scaffold)

### Project setup (T0.3)

- [.] 21:40 — FastAPI backend skeleton create kiya.
- [.] 21:40 — Files: `backend/requirements.txt`, `requirements-dev.txt`, `pyproject.toml`,
  `.env.example`, `.env`, `README.md`.
- [.] 21:40 — Files: `app/__init__.py`, `app/core/{config,db}.py`, `app/api/main.py`,
  `app/api/routes/{health,verifications}.py`, `tests/test_health.py`.
- [.] 21:41 — Python 3.14 venv create + dev dependencies install.

### Database schema

- [.] 21:40 — `db/001_init.sql`: postgis extension + `parcels`, `alus`, `parcel_alus`,
  `evidence_sheets`, `listings`, `orders` tables aur GIST/status indexes.

### API routes

- [.] 21:41 — `GET /health` — PostGIS probe, DB down par bhi service up.
- [.] 21:41 — `POST /api/v1/verifications` — middleware `/verify/evidence` proxy.

### Verification

- [.] 21:42 — `ruff check .` pass.
- [.] 21:42 — `pytest -q` — 2 passed.

## Session 3 — 2026-10-29 21:47 IST (log format rewrite)

- [.] 21:47 — `backend/log-b.md` ko `[.]`/`[]` format me rewrite kiya; date/time/session add kiya.

## Session 4 — 2026-10-29 21:54 IST (master roadmap)

- [.] 21:54 — `../whole_plan.md` roadmap me backend tasks T1.1 se T5.3 tak define kiye.
- [.] 21:56 — `backend/log-b.md` me `YEH SAB HO GYA` / `ABHI YEH YEH KARNA HAI` sections add kiye.

## Session 5 — 2026-10-29 22:10 IST (file organization + verification)

### File organization

- [.] 22:05 — `log-b.md` root se `backend/log-b.md` me move kiya; backend ka log ab backend folder me hai.
- [.] 22:05 — Root se empty/junk files delete kiye; reference docs `docs/` folder me move kiye.

### Verification

- [.] 22:09 — `ruff check .` pass.
- [.] 22:09 — `pytest -q` — 2 passed (2 deprecation warnings).
- [.] 22:09 — `docker compose config` valid.
- [.] 22:10 — Repo paths (`../whole_plan.md`, `backend/log-b.md`) fix kiye.

## Session 6 — 2026-10-29 23:30 IST (planning refresh)

- [.] Module AGENTS.md + SETUP.md added; generated boss-file copies created.
- [.] Branch rule: `backend/<name>` only, PR into `main`.
- [.] T3.1 is middleware-owned; backend does T3.2/T3.3 with a mocked middleware.
- [.] T5.3 split into T5.3-M (middleware) and T5.3-B (backend).
- [.] Module batch plan B1–B6 added in `../docs/task-ownership.md`.

## Git status

- [.] 2026-10-27 — Branch `main`; latest pushed commit `348538c` — `m` — `opencode.json`.
- [.] **C0 baseline commit** — `729e9eb` — `C0 FIRST WORTHY COMMIT- LOCKING ALREADY BUILT` — pushed to `main` on 2026-11-02.
- [.] Backend ka pushed commit hai; branch `backend/<name>` se `main` se nikaal sakte hain.

---

# ABHI YEH YEH KARNA HAI

## Phase 1 — Data foundation

### [] T1.1 — PostGIS boot + schema verify

- [] `docker compose up -d postgis`; health wait.
- [] `backend/scripts/check_db.py` — PostGIS version + 6 tables + row counts; fail par exit 1.
- [] Root `Makefile`: `db-up`, `db-check`, `db-reset`, `seed`, `api`, `mid`, `web`, `check`.
- [] `SETUP.md` update.
- **Done criteria:** `make db-check` green; DB band ho to non-zero exit.

### [] T1.2 — Database access layer

- [] `app/core/db.py` me `db_connection()` context manager (`dict_row`, timeout, commit/rollback).
- [] `app/repositories/base.py` — `fetch_one`, `fetch_all`, `execute`.
- [] Health probe isi layer se chale; routes me direct `psycopg.connect` na ho.
- [] `tests/test_db.py` — galat URL par `unavailable`, raise nahi.
- **Done criteria:** `rg "psycopg.connect" backend/app` sirf `core/db.py` me; ruff/pytest pass.

### [] T1.3 — Demo seed data

- [] `backend/db/002_seed_demo.sql` — `DEMO-ULPIN-001`, demo polygon,
  `geometry_source='DEMO_FIXTURE_NOT_OFFICIAL'`, 1 parent + 4 child ALUs, 4 parcel_alus links.
- [] `backend/scripts/seed.py` — idempotent seed runner.
- [] `Makefile` ka `seed` target.
- **Done criteria:** `make seed` ke baad 1 parcel, 5 ALUs, 4 links; dobara chalane par duplicate nahi.

### Commit batch C1 — T1.1, T1.2, T1.3

**Message:** `feat(db): add postgis checks, db helpers and demo seed`

## Phase 2 — Parcel, ALU aur bundle API

### [] T2.1 — Parcel read API

- [] `GET /api/v1/parcels/{ulpin}` — GeoJSON + attributes; missing 404.
- [] `GET /api/v1/parcels?bbox=...&limit=100` — FeatureCollection, limit max 100.
- [] Repository me `ST_AsGeoJSON`, `ST_MakeEnvelope`, `ST_Intersects`.
- [] Tests: invalid bbox 422, missing 404, limit validation.

### [] T2.2 — Deterministic ALU grid endpoint

- [] `app/services/alu_grid.py` — levels `1km/100m/10m/1m/0.1m2`; Web Mercator cell math.
- [] ID `ALU-{level}-{ix}-{iy}`; parent next coarser level.
- [] `GET /api/v1/alus?bbox=...&level=...`; max 1500 cells, zyada par 422.
- [] Tests: determinism, parent relation, cap.

### [] T2.3 — Bundle schema + API

- [] `db/003_bundles.sql` — `bundles`, `bundle_alus`.
- [] `POST /api/v1/bundles`, `GET /{id}`, `PATCH /{id}` status.
- [] Validation: ALUs exist + same parcel; duplicate reject.
- [] Tests: happy path, cross-parcel reject, duplicate reject.

### Commit batch C2 — T2.1, T2.2, T2.3

**Message:** `feat(api): expose parcels, alu grid and bundles`

## Phase 3 — Evidence pipeline (backend slice: T3.2, T3.3)

### [] T3.2 — Evidence validate, hash, DB save

- [] `app/services/evidence.py` — 21 fields, missing → `N/D`, canonical JSON SHA-256.
- [] Verification route response me `evidence_id`, `evidence_hash`, `status`, `fields`, `sources`.
- [] `GET /api/v1/evidence/{id}`, `GET /api/v1/evidence?ulpin=`.
- [] Middleware down 503, invalid sheet 422.
- [] Tests: mocked middleware, hash determinism.

### [] T3.3 — Officer review queue

- [] `db/004_review.sql` — `review_reason`, `reviewed_at`.
- [] `GET /api/v1/reviews?status=PENDING`, `POST /api/v1/reviews/{id}/decision`.
- [] Transitions `PENDING/NEEDS_REVIEW → CLEAN/REJECTED`; duplicate 409.
- [] Audit fields save; auth TODO for T4.1.
- [] Tests: transitions, 409, reject reason required.

### Commit batch C3 — backend slice T3.2, T3.3

**Message:** `feat(evidence): add tinyfish proof, persistence and review queue`

## Phase 4 — Identity, listing, order

### [] T4.1 — Wallet user + KYC stub

- [] `db/005_users.sql` — wallet, role, kyc_status.
- [] Routes: upsert user, get user, KYC update with `X-Officer-Token`.
- [] Wallet `0x` + 40 hex validation.
- [] Tests: 422/401/200.

### [] T4.2 — Listing lifecycle

- [] `db/006_listings_bundle.sql` — `bundle_id` column.
- [] `POST /api/v1/listings`, `GET ?status=LISTED`, `PATCH /{id}`.
- [] Rules: seller KYC VERIFIED, bundle ACTIVE, price > 0, one active listing per bundle.
- [] Tests: unverified reject, duplicate reject, happy path.

### [] T4.3 — Order lifecycle

- [] `POST /api/v1/orders`, `POST /{id}/funded`, `GET /{id}`.
- [] Rules: buyer KYC, listing LISTED, buyer ≠ seller, price match.
- [] Hex validation for `chain_order_id`/`tx_hash`; duplicate funding 409.
- [] Tests: self-buy, wrong price, double funding, happy path.

### Commit batch C4 — T4.1, T4.2, T4.3

**Message:** `feat(market): add wallet identity, listings and orders`

## Phase 5 — 6 checks aur settlement

### [] T5.1 — 6-check rule engine

- [] `app/services/checks.py` — LISTED, BUNDLE_INTACT, KYC_WALLET, ZONING_OK,
  FUNDS_IN_ESCROW, TRADE_MATCH.
- [] `docs/checks.md` — policy + demo assumptions.
- [] 12+ unit tests (pass/fail per check).

### [] T5.2 — Evaluate endpoint

- [] `db/007_order_checks.sql` — `checks`, `decision`, `decided_at`.
- [] `POST /api/v1/orders/{id}/evaluate`; all pass → APPROVED, blocking fail → REJECTED,
  missing/N/D → NEEDS_REVIEW.
- [] `GET /orders/{id}` me per-check result + decision.
- [] Tests: approve/reject/review.

### [] T5.3-B — Settle/refund + tx hash (backend slice)

- [] `app/services/settlement.py` — APPROVED → settle, REJECTED → refund, NEEDS_REVIEW → no-op.
- [] Order `SETTLED/REFUNDED`, `tx_hash` save; idempotent.
- [] Chain fail par state na badle; 502.
- [] Tests: mocked middleware, idempotency.

### Commit batch C5 — T5.1, T5.2, T5.3

**Message:** `feat(trade): implement six checks and escrow settlement`

## Phase 8 — E2E aur hardening

### [] T8.1 — Real PostGIS integration tests

- [] `tests/conftest.py` — `TEST_DATABASE_URL`, schema apply, per-test rollback.
- [] Integration tests: parcels, ALUs, bundles, listings, orders, evaluate, evidence.
- [] Marker `integration`; `Makefile` target `test-integration`.

### [] T8.3-B — Backend quality gate

- [] `ruff`, `pytest`, `npm audit` (middleware), secret grep.
- [] Input validation/CORS/error leakage review.
- [] Docs: setup, demo, limitations.

## Phase 9 — Stretch

### [] T9.1 — ALU locking + double-sell protection (backend part)

- [] `db/008_alu_locks.sql` — active listing per ALU unique; sold lock.
- [] Tests: same ALU two active listings reject.

---

## Agla batch

**B1 — T1.1, T1.2, T1.3**
Commit message: `feat(db): add postgis checks, db helpers and demo seed`
Pehle lead ka `C0` baseline commit aane do, phir `git switch main && git pull` karke
`backend/<name>` branch banao. Do not push `main`.

## NEEDS FROM OTHER MODULE

Format: `- [] needs: <target module> | what: <endpoint/field/behaviour> | contract ref: <§> | requested by: <session>`
Mark `[.]` when the other module delivered it.

(none yet)
