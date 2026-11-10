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

## Session 7 — 2026-11-10 09:27 IST (batch B1: T1.1, T1.2, T1.3)

- [.] 09:27 — `backend/scripts/check_db.py` create; PostGIS version + 6 tables + row counts; DB down par exit 1 (verify kiya: exit=1).
- [.] 09:27 — Root `Makefile`: `db-up`, `db-check`, `db-reset`, `seed`, `api`, `mid`, `web`, `check` targets; `make -n` se sab parse kiye.
- [.] 09:27 — `backend/SETUP.md` me Makefile shortcuts section aur demo ULPIN (`DEMO-ULPIN-001`) note add kiya.
- [.] 09:27 — `app/core/db.py` me `db_connection()` context manager; `check_database()` isi layer se; failure par `unavailable`, raise nahi.
- [.] 09:27 — `app/repositories/base.py` (`fetch_one`, `fetch_all`, `execute`) + `app/repositories/__init__.py`.
- [.] 09:27 — `tests/test_db.py`: galat `DATABASE_URL` par `unavailable`.
- [.] 09:27 — `db/002_seed_demo.sql`: `DEMO-ULPIN-001`, `ALU-100m-DEMO-000`, `ALU-10m-DEMO-001`…`004`, 4 `CONTAINS` links, `DEMO_FIXTURE_NOT_OFFICIAL`.
- [.] 09:27 — `scripts/seed.py`: idempotent seed runner.
- [.] 09:28 — `ruff check backend` pass; `pytest -q backend` — 13 passed; `py_compile` scripts OK.
- [.] 09:28 — `../whole_plan.md` T1.1/T1.2/T1.3 blocks `YEH SAB HO GYA` me `[.]` kiya; `backend/log-b.md` update kiya.
- [.] 09:29 — Commit `feat(db): add postgis checks, db helpers and demo seed`; push `backend/yash`; PR khola.

## Session 8 — 2026-11-10 11:30 IST (batch B2: T2.1, T2.2, T2.3)

- [.] 11:30 — `app/repositories/parcels.py` (`get_parcel`, `list_parcels`); `app/api/routes/parcels.py` (GET /{ulpin} 404, GET ?bbox FeatureCollection, limit max 100, invalid bbox 422); router registered in `app/api/main.py`.
- [.] 11:30 — `app/services/alu_grid.py` (Web Mercator, `ALU-{level}-{slug(ix)}-{slug(iy)}`, parent next coarser, cap 1500 → `GridError`); `app/api/routes/alus.py` (unknown level 422, over-cap 422); shared `parse_bbox` in `app/api/routes/bbox.py`; routers registered in `app/api/main.py`.
- [.] 11:30 — `db/003_bundles.sql` (`bundles`, `bundle_alus`); `app/repositories/bundles.py` (`create_bundle`/404/422-duplicate, `get_bundle`, `set_bundle_status`/409-transition); `app/api/routes/bundles.py` (POST 201, GET, PATCH status); router registered in `app/api/main.py`.
- [.] 11:30 — Tests: `test_parcels.py`, `test_alu_grid.py`, `test_bundles.py` (happy, cross-parcel 422, duplicate 422, invalid transition 409, GET found/missing, PATCH happy).
- [.] 11:31 — `ruff check backend` clean; `pytest -q backend` — 33 passed.
- [.] 11:31 — `../whole_plan.md` T2.1/T2.2/T2.3 blocks `YEH SAB HO GYA` me `[.]` kiya; `backend/log-b.md` update kiya.
- [.] 11:32 — Commit `feat(api): expose parcels, alu grid and bundles`; push `backend/yash`; PR khola.

## Session 9 — 2026-11-10 14:00 IST (batch B3: T3.2, T3.3, T4.1)

- [.] 14:00 — `app/services/evidence.py` (EVIDENCE_FIELDS 21 keys, normalize_sheet, canonical_hash); `app/api/routes/verifications.py` (camelCase sourceUrl, 503/422/502, evidence_sheets persist, hash); `app/api/routes/evidence.py` (GET /{id}, GET ?ulpin); `app/repositories/evidence.py` (create/get/list); routers registered in app/api/main.py.
- [.] 14:00 — `db/004_review.sql` (review_reason, reviewed_at); `app/repositories/evidence.py` (list_reviews, decide_review APPROVE→CLEAN/REJECT→REJECTED, 409 repeat, 422 no-reason); `app/api/routes/reviews.py` (GET /reviews, POST /{id}/decision with X-Officer-Token 401); router registered in app/api/main.py.
- [.] 14:00 — `db/005_users.sql` (users table); `app/repositories/users.py` (is_valid_wallet 0x+40hex, upsert_user, get_user, update_kyc); `app/api/routes/users.py` (POST /users upsert, GET /users/{wallet}, POST /users/{wallet}/kyc with DEV_OFFICER_TOKEN); `app/core/config.py` dev_officer_token; `.env.example`/`.env` DEV_OFFICER_TOKEN; router registered in app/api/main.py.
- [.] 14:00 — Tests: test_evidence.py, test_reviews.py, test_users.py.
- [.] 14:05 — `ruff check backend` clean; `pytest -q backend` — 66 passed.
- [.] 14:05 — `../whole_plan.md` T3.2/T3.3/T4.1 blocks `YEH SAB HO GYA` me `[.]` kiya; `backend/log-b.md` update kiya.
- [.] 14:06 — Commit `feat(evidence): persist evidence, review queue and wallet users`; push `backend/yash`; PR khola.

## Session 10 — 2026-11-10 16:00 IST (batch B4/C4: T4.2, T4.3, T5.1)

- [.] 16:00 — `db/006_listings_bundle.sql` (bundle_id column); `app/repositories/listings.py` (create/list/get/patch with KYC+bundle+uniqueness rules); `app/api/routes/listings.py` (POST 201, GET ?status, PATCH status); router registered in app/api/main.py.
- [.] 16:00 — `app/repositories/orders.py` (create_order CREATED, fund_order with keccak256 chain_order_id match + CREATED→FUNDED, get_order); `app/api/routes/orders.py` (POST /orders, POST /funded, GET /{id}); `app/services/chain.py` (keccak-256 via pycryptodome, verified vs NIST vectors); `requirements.txt` pycryptodome; routers registered in app/api/main.py.
- [.] 16:00 — `app/services/checks.py` (CheckResult + 6 pure blocking checks); `docs/checks.md` (policy + decision mapping + demo assumptions); router/registry not needed (pure service).
- [.] 16:00 — Tests: test_listings.py, test_orders.py, test_checks.py (19 tests).
- [.] 16:05 — `ruff check backend` clean; `pytest -q backend` — 111 passed.
- [.] 16:05 — `../whole_plan.md` T4.2/T4.3/T5.1 blocks `YEH SAB HO GYA` me `[.]` kiya; `backend/log-b.md` update kiya.
- [.] 16:06 — Commit `feat(market): add listings, orders and six checks`; push `backend/yash`; PR khola.

## Session 11 — 2026-11-10 18:30 IST (batch B5/C5: T5.2, T5.3-B, T8.1)

- [.] 18:30 — `db/007_order_checks.sql` (checks/decision/decided_at columns); `app/services/checks.py` (run_checks, decide, check_results_to_api, missing_evidence flag); `app/api/routes/orders.py` (POST /orders/{id}/evaluate async — FUNDED guard, context load, chain state, run_checks/decide, save_evaluate, apply_decision); `app/services/chain_client.py` (middleware /escrow/status); routers registered in app/api/main.py.
- [.] 18:30 — `app/services/settlement.py` (apply_decision: APPROVED→settle, REJECTED→refund, NEEDS_REVIEW→no-op, idempotent terminal, 502 on chain fail, state unchanged).
- [.] 18:30 — `tests/conftest.py` (TEST_DATABASE_URL, apply_schema, db rollback fixture); `tests/test_integration.py` (@pytest.mark.integration: parcel+ALU, bundle+listing, order+evidence); `pyproject.toml` (integration marker, addopts -m not integration); root `Makefile` (test-integration target).
- [.] 18:30 — Tests: test_evaluate.py (approve/reject/review/409/404/502); test_checks.py run_checks/decide additions.
- [.] 18:35 — `ruff check backend` clean; `pytest -q backend` — 120 passed, 3 integration deselected.
- [.] 18:35 — `../whole_plan.md` T5.2/T5.3-B/T8.1 blocks `YEH SAB HO GYA` me `[.]` kiya + C5 commit block; `backend/log-b.md` update kiya.
- [.] 18:36 — Commit `feat(trade): evaluate, settle and integration-test orders`; push `backend/yash`; PR khola.

## Session 12 — 2026-11-10 19:30 IST (batch B6/C6: T8.3-B, T9.1)

- [.] 19:30 — `app/api/main.py` — global exception handler returns generic 500 (no stack-trace/internals leak); CORS specific origins; controlled `HTTPException` details.
- [.] 19:30 — `docs/limitations.md` — demo data, KYC stub, testnet only, error handling, validation, partial-bundle sale rules, out-of-scope.
- [.] 19:30 — `db/008_alu_locks.sql` — partial unique index on `listings(alu_id)` active statuses (one active listing per ALU).
- [.] 19:30 — `app/repositories/listings.py` — `alu_id` optional on create/patch; `alu_has_sold_listing`/`alu_has_active_listing` reject double-sell and sold-relist (409).
- [.] 19:30 — `tests/test_alu_locks.py` — same-ALU two active listings rejected, sold-ALU relist rejected, fresh ALU success.
- [.] 19:35 — `ruff check backend` clean; `pytest -q backend` — 126 passed, 3 integration deselected.
- [.] 19:35 — `../whole_plan.md` T8.3-B/T9.1 blocks `YEH SAB HO GYA` me `[.]` kiya + C6 commit block; `backend/log-b.md` update kiya.
- [.] 19:36 — Commit `chore(backend): harden and add alu locking`; push `backend/yash`; PR khola.

## Session 13 — 2026-11-10 20:00 IST (batch B6/C9 slice: T9.3-B)

- [.] 20:00 — `backend/Dockerfile` — multi-stage build (python:3.12-slim builder venv + slim runtime), non-root `appuser`, `backend/app` copied, `EXPOSE 8000`, healthcheck on `/health`, CMD `uvicorn app.api.main:app --app-dir backend --host 0.0.0.0 --port 8000`; `requirements-dev.txt` installed in builder so `pycryptodome` is available.
- [.] 20:05 — `../whole_plan.md` T9.3-B block `YEH SAB HO GYA` me `[.]` kiya + C6/C9 commit block; `backend/log-b.md` update kiya.
- [.] 20:06 — Commit `chore(backend): add production Dockerfile`; push `backend/yash`; PR khola.

## Git status

- [.] 2026-10-27 — Branch `main`; latest pushed commit `348538c` — `m` — `opencode.json`.
- [.] **C0 baseline commit** — `729e9eb` — `C0 FIRST WORTHY COMMIT- LOCKING ALREADY BUILT` — pushed to `main` on 2026-11-02.
- [.] Backend ka pushed commit hai; branch `backend/<name>` se `main` se nikaal sakte hain.

---

# ABHI YEH YEH KARNA HAI

## Phase 1 — Data foundation

### [.] T1.1 — PostGIS boot + schema verify — Session 7, 2026-11-10 09:27 IST

- [.] `docker compose up -d postgis`; health wait. (Docker daemon nahi chala is session me; `check_db.py` verify kiya: DB down par exit 1)
- [.] `backend/scripts/check_db.py` — PostGIS version + 6 tables + row counts; fail par exit 1.
- [.] Root `Makefile`: `db-up`, `db-check`, `db-reset`, `seed`, `api`, `mid`, `web`, `check`.
- [.] `SETUP.md` update.
- **Done criteria:** `make db-check` green; DB band ho to non-zero exit. (verify kiya: `check_db.py` exit=1 bina DB ke)

### [.] T1.2 — Database access layer — Session 7, 2026-11-10 09:27 IST

- [.] `app/core/db.py` me `db_connection()` context manager (`dict_row`, `connect_timeout=5`, commit/rollback/close).
- [.] `app/repositories/base.py` — `fetch_one`, `fetch_all`, `execute`; `app/repositories/__init__.py`.
- [.] Health probe `check_database()` isi layer se; failure par `{"status": "unavailable", ...}`, raise nahi; routes me direct `psycopg.connect` nahi.
- [.] `tests/test_db.py` — galat URL par `unavailable`, raise nahi.
- **Done criteria:** `rg "psycopg.connect" backend/app` sirf `core/db.py` me; ruff/pytest pass. (verify kiya: sirf core/db.py; 13 tests pass)

### [.] T1.3 — Demo seed data — Session 7, 2026-11-10 09:27 IST

- [.] `backend/db/002_seed_demo.sql` — `DEMO-ULPIN-001`, demo polygon, `geometry_source='DEMO_FIXTURE_NOT_OFFICIAL'`, 1 parent + 4 child ALUs, 4 parcel_alus `CONTAINS` links (`overlap_percentage=100`).
- [.] `backend/scripts/seed.py` — idempotent seed runner (demo rows pehle delete, phir insert).
- [.] `Makefile` ka `seed` target add kiya.
- **Done criteria:** `make seed` ke baad 1 parcel, 5 ALUs, 4 links; dobara chalane par duplicate nahi (delete-then-insert exact IDs se guarantee). Live DB check Docker ke bina nahi chala sakte.

### Commit batch C1 — T1.1, T1.2, T1.3

**Message:** `feat(db): add postgis checks, db helpers and demo seed`

## Phase 2 — Parcel, ALU aur bundle API

### [.] T2.1 — Parcel read API — Session 8, 2026-11-10 11:30 IST

- [.] `GET /api/v1/parcels/{ulpin}` — GeoJSON Feature + attributes + `geometry_status` + `demo: true`; missing 404 `{"detail":"Parcel not found"}`.
- [.] `GET /api/v1/parcels?bbox=...&limit=100` — FeatureCollection; limit max 100 (422 over), invalid bbox 422.
- [.] Repository `backend/app/repositories/parcels.py`: `get_parcel`, `list_parcels` with `ST_AsGeoJSON`, `ST_MakeEnvelope(...,4326)`, `ST_Intersects`.
- [.] `backend/app/api/routes/parcels.py` + router registered in `app/api/main.py`.
- [.] Tests: `tests/test_parcels.py` (found/missing/invalid-bbox/limit-over-max/feature-collection).
- **Done criteria:** ruff clean, pytest pass; missing→404, invalid bbox→422, limit 101→422 (mocked repo; live DB needs Docker).

### [.] T2.2 — Deterministic ALU grid endpoint — Session 8, 2026-11-10 11:30 IST

- [.] `app/services/alu_grid.py` — levels `1km/100m/10m/1m/0.1m2`, Web Mercator forward/inverse per `docs/decisions.md` §3.
- [.] ID `ALU-{level}-{slug(ix)}-{slug(iy)}`; negative indices use `m` slug; parent = next coarser level (`1km` → null); closed GeoJSON polygon; `area_sqm`.
- [.] `GET /api/v1/alus?bbox=...&level=10m` → FeatureCollection; unknown level 422; >1500 cells → 422 `"Zoom in: N cells exceeds 1500"`.
- [.] Shared `parse_bbox` in `app/api/routes/bbox.py`. Router registered in `app/api/main.py`.
- [.] Tests: `tests/test_alu_grid.py` (determinism, parent-child, cap, negative `m` slug, unknown level, over-cap route, feature shape).
- **Done criteria:** ruff clean, `pytest -q backend/tests/test_alu_grid.py` pass; deterministic output; 1500+ → 422.

### [.] T2.3 — Bundle schema + API — Session 8, 2026-11-10 11:30 IST

- [.] `db/003_bundles.sql` — `bundles` (id, ulpin FK, name, status, created_by, timestamps) + `bundle_alus` (bundle_id, alu_id PK).
- [.] `backend/app/repositories/bundles.py` — `create_bundle`, `get_bundle`, `set_bundle_status`; validation: ULPIN exists (404), ALUs exist + same parcel (422), duplicate ALU (422), allowed status transitions (else 409).
- [.] `backend/app/api/routes/bundles.py` — POST /bundles (201), GET /bundles/{id}, PATCH /bundles/{id} status; router registered in `app/api/main.py`.
- [.] Tests: `tests/test_bundles.py` (happy path, cross-parcel 422, duplicate 422, invalid transition 409, GET found/missing, PATCH happy).
- **Done criteria:** ruff clean, pytest pass (mocked repo; live DB needs Docker).

### Commit batch C2 — T2.1, T2.2, T2.3 — Session 8, 2026-11-10 11:30 IST

**Message:** `feat(api): expose parcels, alu grid and bundles`

## Phase 3 — Evidence pipeline (backend slice: T3.2, T3.3)

### [.] T3.2 — Evidence validate, hash, DB save — Session 9, 2026-11-10 14:00 IST

- [.] `app/services/evidence.py` — EVIDENCE_FIELDS (21 keys), normalize_sheet (missing/invalid → N/D), canonical_hash (0x + sha256 canonical JSON).
- [.] `POST /api/v1/verifications` — middleware ko camelCase `sourceUrl` bhejta hai; middleware down 503, invalid sheet 422, other error 502; `evidence_sheets` me save; return `{ulpin,status,evidence_id,evidence_hash,tinyfish_run_id,fields,sources}`.
- [.] `GET /api/v1/evidence/{id}`, `GET /api/v1/evidence?ulpin=`.
- [.] `app/repositories/evidence.py` — create_evidence_sheet, get_evidence_sheet, list_evidence_sheets.
- [.] Tests: `test_evidence.py` (normalize, hash determinism, happy path, 503, 422, 502, blank ulpin).
- **Done criteria:** ruff clean, pytest pass; mocked middleware persistence + hash determinism.

### [.] T3.3 — Officer review queue — Session 9, 2026-11-10 14:00 IST

- [.] `db/004_review.sql` — `review_reason TEXT`, `reviewed_at TIMESTAMPTZ` (IF NOT EXISTS).
- [.] `app/repositories/evidence.py` — list_reviews, decide_review (APPROVE→CLEAN, REJECT→REJECTED; PENDING/NEEDS_REVIEW se hi; repeat → 409; reject bina reason → 422).
- [.] `app/api/routes/reviews.py` — GET /reviews?status=, POST /reviews/{id}/decision with X-Officer-Token (401 missing/wrong); reviewed_by/review_reason/reviewed_at save.
- [.] Tests: `test_reviews.py` (pending items, approve, reject, 401, 422, 409, 404).
- **Done criteria:** ruff clean, pytest pass.

### Commit batch C3 — T3.2, T3.3, T4.1 — Session 9, 2026-11-10 14:00 IST

**Message:** `feat(evidence): persist evidence, review queue and wallet users`

## Phase 4 — Identity, listing, order

### [.] T4.1 — Wallet user + KYC stub — Session 9, 2026-11-10 14:00 IST

- [.] `db/005_users.sql` — users (wallet_address UNIQUE, role CITIZEN/OFFICER, kyc_status PENDING/VERIFIED/REJECTED).
- [.] `app/repositories/users.py` — is_valid_wallet (`^0x[a-fA-F0-9]{40}$`), upsert_user, get_user, update_kyc.
- [.] `app/api/routes/users.py` — POST /users upsert (200), GET /users/{wallet} (404/422), POST /users/{wallet}/kyc (X-Officer-Token vs DEV_OFFICER_TOKEN → 401/402/409, KYC update 200).
- [.] `app/core/config.py` — `dev_officer_token` field; `.env.example` aur `.env` me DEV_OFFICER_TOKEN add kiya.
- [.] Tests: `test_users.py` (invalid wallet 422, upsert, get found/missing, 401, KYC 200).
- **Done criteria:** ruff clean, pytest pass.

### [.] T4.2 — Listing lifecycle — Session 10, 2026-11-10 16:00 IST

- [.] `db/006_listings_bundle.sql` — `listings` me `bundle_id BIGINT REFERENCES bundles(id)` (IF NOT EXISTS) + index.
- [.] `app/repositories/listings.py` — `create_listing`, `list_listings`, `get_listing`, `patch_listing_status`; rules: seller KYC VERIFIED (409), bundle ACTIVE (409), price_wei > 0 (422), one active listing per bundle (409), allowed transitions (else 409).
- [.] `app/api/routes/listings.py` — POST /listings (201), GET /listings?status= (default LISTED), PATCH /listings/{id} status; router registered in app/api/main.py.
- [.] Tests: `test_listings.py` (happy, unverified 409, duplicate active 409, invalid transition 409, GET items, invalid price 422).
- **Done criteria:** ruff clean, pytest pass (mocked repo; live DB needs Docker).

### [.] T4.3 — Order lifecycle — Session 10, 2026-11-10 16:00 IST

- [.] `app/repositories/orders.py` — `create_order` (buyer KYC VERIFIED, listing LISTED, buyer≠seller, amount=price → CREATED; self-buy/unverified/wrong-price 409), `fund_order` (bytes32 validation 422, chain_order_id = keccak256("landmarket-order:"+id) matched else 422, CREATED→FUNDED, duplicate 409), `get_order`.
- [.] `app/api/routes/orders.py` — POST /orders (201), POST /orders/{id}/funded, GET /orders/{id} order shape with `chain_order_id`; router registered in app/api/main.py.
- [.] `app/services/chain.py` — keccak-256 via pycryptodome (verified vs NIST vectors); `requirements.txt` me pycryptodome add kiya.
- [.] Tests: `test_orders.py` (happy, self-buy 409, unverified 409, duplicate funding 409, invalid bytes32 422, chain mismatch 422, GET found/missing).
- **Done criteria:** ruff clean, pytest pass (mocked repo; live DB needs Docker).

### [.] T5.1 — 6-check rule engine — Session 10, 2026-11-10 16:00 IST

- [.] `app/services/checks.py` — `CheckResult(name, passed, reason, blocking)` dataclass + 6 pure functions: `check_listed`, `check_bundle_intact`, `check_kyc_wallet`, `check_zoning_ok`, `check_funds_in_escrow`, `check_trade_match`; sab blocking.
- [.] `docs/checks.md` — policy, decision mapping (APPROVED/REJECTED/NEEDS_REVIEW), demo assumptions.
- [.] Tests: `test_checks.py` — 19 tests (pass/fail per check, all 6 check names).
- **Done criteria:** ruff clean, pytest pass; DB-independent pure functions.

### Commit batch C4 — T4.2, T4.3, T5.1 — Session 10, 2026-11-10 16:00 IST

**Message:** `feat(market): add listings, orders and six checks`

## Phase 5 — 6 checks aur settlement

### [.] T5.2 — Evaluate endpoint — Session 11, 2026-11-10 18:30 IST

- [.] `db/007_order_checks.sql` — `checks JSONB`, `decision TEXT`, `decided_at TIMESTAMPTZ`.
- [.] `POST /api/v1/orders/{id}/evaluate` — order FUNDED (warna 409), context load, run_checks + decide, persist decision, settlement trigger; middleware chain-state fail → 502, koi persist nahi.
- [.] `GET /api/v1/orders/{id}` me per-check result + decision.
- [.] `app/services/chain_client.py` — middleware `GET /escrow/status/{orderId}` call.
- [.] Tests: `test_evaluate.py` (approve→settle, reject→refund, review→no-op, non-funded 409, not-found 404, chain down 502).
- **Done criteria:** ruff clean, pytest pass (mocked repo + middleware + settlement; live DB needs Docker).

### [.] T5.3-B — Settle/refund + tx hash (backend slice) — Session 11, 2026-11-10 18:30 IST

- [.] `app/services/settlement.py` — `apply_decision`: APPROVED→settle, REJECTED→refund, NEEDS_REVIEW→no-op; terminal state idempotent; chain fail → 502, state unchanged; DB state + tx_hash save.
- [.] Called from evaluate after persisting decision.
- [.] Middleware `T5.3-M` tak mock kiya ja sakta hai.
- **Done criteria:** ruff clean, pytest pass; live chain/manual test needs Docker + middleware.

### Commit batch C5 — T5.2, T5.3-B, T8.1 — Session 11, 2026-11-10 18:30 IST

**Message:** `feat(trade): evaluate, settle and integration-test orders`

## Phase 8 — E2E aur hardening

### [.] T8.1 — Real PostGIS integration tests — Session 11, 2026-11-10 18:30 IST

- [.] `tests/conftest.py` — `TEST_DATABASE_URL`, `apply_schema` (sab 0*.sql), `db` fixture per-test rollback.
- [.] `tests/test_integration.py` — `@pytest.mark.integration`: parcel+ALU, bundle+listing, order+evidence persistence.
- [.] `pyproject.toml` — `integration` marker + `addopts = ["-m", "not integration"]` (default pytest fast).
- [.] Root `Makefile` — `test-integration` target (`pytest -m integration -q backend -o addopts=""`).
- **Done criteria:** ruff clean, `pytest -q backend` 120 passed, 3 integration deselected. Live `make db-up && make test-integration` needs Docker (nahi chala is session me).

### [.] T8.3-B — Backend quality gate — Session 12, 2026-11-10 19:30 IST

- [.] `ruff`, `pytest` pass (126 tests; integration deselected, needs Docker).
- [.] Input validation/CORS/error leakage review: global exception handler in `app/api/main.py`
  returns generic 500 (no internals leak); CORS specific origins; all route errors controlled
  `HTTPException` details.
- [.] Docs: `docs/limitations.md` written (demo data, KYC stub, testnet only, error handling,
  validation, partial-bundle sale rules, out-of-scope).
- **Done criteria:** ruff clean, `pytest -q backend` pass.

### [.] T9.1 — ALU locking + double-sell protection (backend part) — Session 12, 2026-11-10 19:30 IST

- [.] `db/008_alu_locks.sql` — partial unique index on `listings(alu_id)` where status IN
  (DRAFT,LISTED,PAUSED) → one active listing per ALU; sold-ALU lock documented.
- [.] `app/repositories/listings.py` — `create_listing`/`patch_listing_status` accept optional
  `alu_id`; `alu_has_sold_listing` + `alu_has_active_listing` reject double-sell and relisting
  sold ALUs (409).
- [.] Tests: `tests/test_alu_locks.py` — same-ALU two active listings rejected, sold-ALU relist
  rejected, fresh ALU success.
- **Done criteria:** ruff clean, pytest pass; Ek ALU do active listings me nahi aa sakta.

### Commit batch C6 — T8.3-B, T9.1 — Session 12, 2026-11-10 19:30 IST

**Message:** `chore(backend): harden and add alu locking`

---

## Agla batch

**B1 — T1.1, T1.2, T1.3**
Commit message: `feat(db): add postgis checks, db helpers and demo seed`
Pehle lead ka `C0` baseline commit aane do, phir `git switch main && git pull` karke
`backend/<name>` branch banao. Do not push `main`.
