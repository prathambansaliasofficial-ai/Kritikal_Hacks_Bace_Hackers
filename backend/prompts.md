# prompts.md — Backend (Yash / `backend/<name>` branch)

Roles: **Yash** = backend owner. **Paradew** = senior head on `main` (merge/supervise only). **Sumit** = frontend. **Tanya** = middleware.

### PLAYRULES (applies to all teammates — from deleted PLAYRULES.MD)
- Sirf apne module folder mein kaam karo — doosre module ka code mat chhedo
- main par kabhi direct push mat karo — apni branch par push karo, PR kholo, lead merge karega
- Task ID order mein kaam karo, skip mat karo
- `npm run sync:docs && npm run check:docs` har batch ke baad chalao
- Koi fake API key, fake TxHash, ya government record mat dalo

---

## MASTER PROMPT (NEVER comment out this block)

I am Yash, working on the `backend/<name>` branch of the Land Market monorepo. You are my AI for backend work only.

STRICT SCOPE:
- Work ONLY inside `backend/` plus the exact root files named in each task. Allowed: `backend/app/**`, `backend/db/**`, `backend/scripts/**`, `backend/tests/**`, `backend/requirements*.txt`, `backend/pyproject.toml`, `backend/.env.example`, `backend/README.md`, `backend/log-b.md`, `backend/AGENTS.md`, `backend/SETUP.md`, `Makefile` (only T1.1, T1.3, T8.1), `SETUP.md` (only T1.1, T1.3), `docs/checks.md` (only T5.1, T5.2).
- You may change YOUR OWN task markers in root `../whole_plan.md` (set `[]` → `[.]`).
- You may NOT edit `../frontend/`, `../middleware/`, other root docs, or generated copies (`backend/whole_plan.md`, `backend/docs/**`).
- Never touch `main`. Work only on `backend/<name>`.

Read order for every task:
1. `backend/AGENTS.md` + `backend/SETUP.md`.
2. Your task block in root `whole_plan.md`.
3. The context pack for your batch (`docs/context/C1.md` … `C9.md`).
4. `docs/api-contract.md`, `docs/decisions.md`, `docs/checks.md`.

Fixed contracts (do not invent fields):
- `docs/api-contract.md` — request/response shapes, enums, error codes.
- `docs/decisions.md` — ALU math, evidence hash, order ID, money, chain constants.
- `docs/checks.md` — six checks, blocking flags, decision mapping.

Backend rules that matter:
- Money is `NUMERIC(78,0)` / decimal string, never float.
- Evidence hash is canonical JSON SHA-256 with `0x` prefix.
- Missing evidence field → `N/D`; never invent a value.
- `APPROVED → settle`, `REJECTED → refund`, `NEEDS_REVIEW → no chain call`.
- Demo rows carry `DEMO_FIXTURE_NOT_OFFICIAL`; API demo objects carry `demo: true`.
- Middleware down = 503, invalid sheet = 422, chain failure = 502. No state change on error.
- No direct `psycopg.connect` outside `backend/app/core/db.py` (after T1.2).

Definition of done (every task):
- [ ] Code matches the task block and `docs/api-contract.md`.
- [ ] Tests named in the task pass; `ruff` + `pytest` pass.
- [ ] `backend/log-b.md` updated with date/time (IST)/session and exact commands.
- [ ] Your task marker in `../whole_plan.md` is `[.]`.
- [ ] `npm run sync:docs && npm run check:docs` pass.
- [ ] Commit uses the batch message from `docs/task-ownership.md` §2 (only after all 3 tasks of the batch).

Stop conditions — write `**BLOCKED:**` in the task block + `backend/log-b.md` and ask Paradew:
- Needs a middleware endpoint not live and pack does not say "mock it".
- DB migration conflicts with existing table/column.
- `TINYFISH_API_KEY` or another human key needed.
- Need to edit `frontend/` or `middleware/`.
- Contract does not describe a shape you need.

Commands (from repo root):
- `docker compose up -d postgis`
- `backend/.venv/bin/ruff check backend`
- `backend/.venv/bin/pytest -q backend`
- `backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000`
- After T1.1: `make db-up`, `make db-check`, `make seed`, `make api`, `make check`.

---

## PROMPT BLOCKS (comment out each block when its task/batch is done)
Rule: When a prompt block below is completed, wrap its entire block in HTML comments `<!-- ... -->`. Keep the MASTER PROMPT above uncommented at all times. Commit only after all 3 tasks of a batch are done.

<!-- PROMPT: BACKEND — Batch B1 (T1.1, T1.2, T1.3) — START -->
I am Yash on `backend/<name>`. Complete batch B1 = T1.1, T1.2, T1.3. Commit message: `feat(db): add postgis checks, db helpers and demo seed`.

Read: root `whole_plan.md` Phase 1 (T1.1–T1.3), `docs/context/C1.md`, `docs/api-contract.md`, `docs/decisions.md`.

T1.1 — PostGIS boot + schema verify + Makefile:
1. `docker compose up -d postgis`; wait for healthy container.
2. `docker compose exec -T postgis psql -U landmarket -d landmarket -c "\dt"` → confirm 6 tables.
3. `backend/scripts/check_db.py`: PostGIS version, 6 table names, row counts; exit code 1 if DB unreachable.
4. Root `Makefile`: `db-up`, `db-check`, `db-reset` (yes prompt before volume delete), `seed`, `api`, `mid`, `web`, `check`.
5. Root `SETUP.md`: add Makefile commands.
Files: `backend/scripts/check_db.py`, `Makefile`, `SETUP.md`.
Done: `make db-check` shows PostGIS version + 6 tables; DB down → non-zero exit.

T1.2 — Database access layer:
1. `backend/app/core/db.py`: `@contextmanager db_connection()` — `psycopg.connect`, `row_factory=dict_row`, `connect_timeout=5`, commit/rollback/close.
2. `backend/app/repositories/base.py`: `fetch_one`, `fetch_all`, `execute`.
3. Health probe uses this layer; no direct `psycopg.connect` in routes.
4. `backend/tests/test_db.py`: bad `DATABASE_URL` → `check_database()` returns `unavailable`, does not raise.
Files: `backend/app/core/db.py`, `backend/app/repositories/base.py`, `backend/tests/test_db.py`.
Done: `rg "psycopg.connect" backend/app` matches only `core/db.py`; ruff/pytest pass.

T1.3 — Demo parcel/ALU/bundle seed data:
1. `backend/db/002_seed_demo.sql`: parcel `DEMO-ULPIN-001`, Kothrud polygon, `geometry_source='DEMO_FIXTURE_NOT_OFFICIAL'`, attributes `owner_name`, `district`, `zoning`; 1 parent ALU (100m) + 4 child ALUs (10m), deterministic IDs, parent links; 4 `parcel_alus` CONTAINS links.
2. `backend/scripts/seed.py`: execute SQL; idempotent (delete demo rows then insert on re-run).
3. `Makefile` `seed` target runs this script.
4. `SETUP.md`: note demo ULPIN.
Files: `backend/db/002_seed_demo.sql`, `backend/scripts/seed.py`, `Makefile`, `SETUP.md`.
Done: `make seed` → 1 parcel, 5 ALUs, 4 parcel_alus; re-run = no duplicates.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `backend/log-b.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add backend/ whole_plan.md Makefile SETUP.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(db): add postgis checks, db helpers and demo seed"`.
- Push: `git push -u origin backend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: BACKEND — Batch B1 — END -->

<!-- PROMPT: BACKEND — Batch B2 (T2.1, T2.2, T2.3) — START -->
I am Yash on `backend/<name>`. Complete batch B2 = T2.1, T2.2, T2.3. Commit message: `feat(api): expose parcels, alu grid and bundles`.

Read: root `whole_plan.md` Phase 2 (T2.1–T2.3), `docs/context/C2.md`, `docs/api-contract.md`, `docs/decisions.md`. Depends on C1 (B1 merged).

T2.1 — Parcel read API:
1. `backend/app/repositories/parcels.py`: parcel by ULPIN, parcels by bbox (`ST_AsGeoJSON`, `ST_MakeEnvelope(...,4326)`, `ST_Intersects`).
2. `backend/app/api/routes/parcels.py`: `GET /api/v1/parcels/{ulpin}` → GeoJSON Feature + attributes + `geometry_status`; missing → 404. `GET /api/v1/parcels?bbox=...&limit=100` → FeatureCollection; limit max 100.
3. Register router in `backend/app/api/main.py`.
4. Tests: invalid bbox 422, missing ULPIN 404, limit >100 clamp/reject.
Files: `backend/app/repositories/parcels.py`, `backend/app/api/routes/parcels.py`, `backend/app/api/main.py`, `backend/tests/test_parcels.py`.
Done: `GET /api/v1/parcels/DEMO-ULPIN-001` returns demo polygon.

T2.2 — Deterministic ALU grid endpoint:
1. `backend/app/services/alu_grid.py`: levels `1km`=1000m, `100m`, `10m`, `1m`, `0.1m2`=0.1m×1m. Web Mercator cell index → lon/lat.
2. ID format `ALU-{level}-{ix}-{iy}`; parent = next coarser level same formula.
3. `GET /api/v1/alus?bbox=...&level=...` → GeoJSON FeatureCollection; each feature `alu_id`, `parent_id`, `level`. Max 1500 cells; over → 422 "zoom in".
4. Tests: same input → same ID, parent-child relation, cap enforced.
Files: `backend/app/services/alu_grid.py`, `backend/app/api/routes/alus.py`, `backend/app/api/main.py`, `backend/tests/test_alu_grid.py`.
Done: deterministic output; >1500 → 422.

T2.3 — Bundle schema + API:
1. `backend/db/003_bundles.sql`: `bundles` (id, ulpin FK, name, status DRAFT/ACTIVE/PAUSED/ARCHIVED, created_by, timestamps), `bundle_alus` (bundle_id, alu_id, PK).
2. Routes: `POST /api/v1/bundles` `{ulpin,name,alu_ids,created_by}`; `GET /api/v1/bundles/{id}`; `PATCH /api/v1/bundles/{id}` `{status}`.
3. Validation: all ALUs exist and link to same parcel; duplicate ALU reject.
4. Tests: happy path, cross-parcel ALU reject, duplicate reject, invalid status transition.
Files: `backend/db/003_bundles.sql`, `backend/app/repositories/bundles.py`, `backend/app/api/routes/bundles.py`, `backend/app/api/main.py`, `backend/tests/test_bundles.py`.
Done: demo parcel's 4 ALUs form an ACTIVE bundle.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `backend/log-b.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add backend/ whole_plan.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(api): expose parcels, alu grid and bundles"`.
- Push: `git push -u origin backend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: BACKEND — Batch B2 — END -->

<!-- PROMPT: BACKEND — Batch B3 (T3.2, T3.3, T4.1) — START -->
I am Yash on `backend/<name>`. Complete batch B3 = T3.2, T3.3, T4.1. Commit message: `feat(evidence): persist evidence, review queue and wallet users`.

Read: root `whole_plan.md` Phase 3 (T3.2, T3.3) and Phase 4 (T4.1), `docs/context/C3.md`, `docs/context/C4.md`, `docs/api-contract.md`, `docs/decisions.md`. Depends on C2 (B2 merged). T3.1 (middleware TinyFish live run) may be blocked — mock middleware response per `docs/api-contract.md`; do not fake a run.

T3.2 — Evidence validate, hash, DB save:
1. `backend/app/services/evidence.py`: 21 fields; missing → `N/D`; canonical JSON (sorted keys) SHA-256 hash.
2. `POST /api/v1/verifications`: validate middleware response, save to `evidence_sheets`; response: `evidence_id`, `evidence_hash`, `status`, `fields`, `sources`, `tinyfish_run_id`.
3. `GET /api/v1/evidence/{id}`, `GET /api/v1/evidence?ulpin=...`.
4. Middleware down → 503; invalid sheet → 422; never invent raw data.
5. Tests: mocked middleware persistence + hash determinism.
Files: `backend/app/services/evidence.py`, `backend/app/repositories/evidence.py`, `backend/app/api/routes/verifications.py`, `backend/app/api/routes/evidence.py`, `backend/app/api/main.py`, `backend/tests/test_evidence.py`.
Done: after one verification → DB row + stable hash; GET returns same sheet.

T3.3 — Officer review queue:
1. `backend/db/004_review.sql`: `evidence_sheets` + `review_reason TEXT`, `reviewed_at TIMESTAMPTZ`.
2. Routes: `GET /api/v1/reviews?status=PENDING` (evidence + parcel summary); `POST /api/v1/reviews/{id}/decision` `{decision: APPROVE|REJECT, reason, officer}`.
3. Transitions: `PENDING/NEEDS_REVIEW` → `CLEAN` or `REJECTED`; repeat decision → 409.
4. Save `reviewed_by`, `review_reason`, `reviewed_at`. Auth = officer string stub; TODO for JWT T4.1.
5. Tests: valid transitions, invalid transition 409, reason required on reject.
Files: `backend/db/004_review.sql`, `backend/app/api/routes/reviews.py`, `backend/app/repositories/evidence.py`, `backend/app/api/main.py`, `backend/tests/test_reviews.py`.
Done: officer can approve/reject pending evidence; audit fields filled.

T4.1 — Wallet user + KYC stub:
1. `backend/db/005_users.sql`: `users` (id, wallet_address unique, role CITIZEN/OFFICER, kyc_status PENDING/VERIFIED/REJECTED, created_at, updated_at).
2. Routes: `POST /api/v1/users` upsert wallet; `GET /api/v1/users/{wallet}`; `POST /api/v1/users/{wallet}/kyc` `{status, reason}`.
3. KYC endpoint needs `X-Officer-Token` header matching `.env` `DEV_OFFICER_TOKEN`. Document as prototype stub.
4. Wallet format: `0x` + 40 hex.
5. Tests: invalid wallet 422, missing token 401, KYC update 200.
Files: `backend/db/005_users.sql`, `backend/app/api/routes/users.py`, `backend/app/repositories/users.py`, `backend/app/api/main.py`, `backend/.env.example`, `backend/tests/test_users.py`.
Done: demo buyer/seller KYC VERIFIED.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `backend/log-b.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add backend/ whole_plan.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(evidence): persist evidence, review queue and wallet users"`.
- Push: `git push -u origin backend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: BACKEND — Batch B3 — END -->

<!-- PROMPT: BACKEND — Batch B4 (T4.2, T4.3, T5.1) — START -->
I am Yash on `backend/<name>`. Complete batch B4 = T4.2, T4.3, T5.1. Commit message: `feat(market): add listings, orders and six checks`.

Read: root `whole_plan.md` Phase 4 (T4.2, T4.3) and Phase 5 (T5.1), `docs/context/C4.md`, `docs/context/C5.md`, `docs/api-contract.md`, `docs/decisions.md`, `docs/checks.md`. Depends on T4.1, T2.3 (T4.2); T4.2 (T4.3); T4.3 (T5.1).

T4.2 — Listing lifecycle:
1. `backend/db/006_listings_bundle.sql`: `listings` + `bundle_id BIGINT REFERENCES bundles(id)`; `alu_id` nullable.
2. Routes: `POST /api/v1/listings` `{bundle_id, seller_wallet, price_wei}`; `GET /api/v1/listings?status=LISTED`; `PATCH /api/v1/listings/{id}` `{status}`.
3. Rules: seller KYC VERIFIED, bundle ACTIVE, price > 0, one active listing per bundle.
4. Transitions: `DRAFT→LISTED→PAUSED/CANCELLED`; `PAUSED→LISTED`.
5. Tests: unverified seller reject, duplicate active listing reject, happy path.
Files: `backend/db/006_listings_bundle.sql`, `backend/app/api/routes/listings.py`, `backend/app/repositories/listings.py`, `backend/app/api/main.py`, `backend/tests/test_listings.py`.
Done: demo bundle LISTED.

T4.3 — Order lifecycle:
1. Routes: `POST /api/v1/orders` `{listing_id, buyer_wallet}`; `POST /api/v1/orders/{id}/funded` `{chain_order_id, tx_hash}`; `GET /api/v1/orders/{id}`.
2. Rules: buyer KYC VERIFIED, listing LISTED, buyer ≠ seller, price matches listing. Order `CREATED`; funding proof → `FUNDED`.
3. `chain_order_id` 32-byte hex, `tx_hash` 32-byte hex; duplicate funding → 409.
4. Tests: self-buy reject, wrong price reject, double funded reject, happy path.
Files: `backend/app/api/routes/orders.py`, `backend/app/repositories/orders.py`, `backend/app/api/main.py`, `backend/tests/test_orders.py`.
Done: CREATED → FUNDED order recorded in DB.

T5.1 — Six-check pure rule engine:
1. `backend/app/services/checks.py`: each check a pure function, output `CheckResult(name, passed, reason, blocking)`.
2. Exactly 6 checks: LISTED, BUNDLE_INTACT, KYC_WALLET, ZONING_OK, FUNDS_IN_ESCROW, TRADE_MATCH.
3. Rule policy in `docs/checks.md`; demo assumptions clearly marked.
4. Unit tests: pass + fail per check (≥12 tests).
Files: `backend/app/services/checks.py`, `docs/checks.md`, `backend/tests/test_checks.py`.
Done: 6 checks isolated-tested, no DB needed.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `backend/log-b.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add backend/ whole_plan.md docs/checks.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(market): add listings, orders and six checks"`.
- Push: `git push -u origin backend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: BACKEND — Batch B4 — END -->

<!-- PROMPT: BACKEND — Batch B5 (T5.2, T5.3-B, T8.1) — START -->
I am Yash on `backend/<name>`. Complete batch B5 = T5.2, T5.3-B, T8.1. Commit message: `feat(trade): evaluate, settle and integration-test orders`.

Read: root `whole_plan.md` Phase 5 (T5.2), Phase 5 backend slice (T5.3-B), Phase 8 (T8.1), `docs/context/C5.md`, `docs/context/C8.md`, `docs/api-contract.md`, `docs/checks.md`. Depends on T5.1, T5.3-M (middleware — mock until merged), C5.

T5.2 — Evaluate endpoint + decision policy:
1. `backend/db/007_order_checks.sql`: orders + `checks JSONB`, `decision TEXT`, `decided_at TIMESTAMPTZ`; decision APPROVED/NEEDS_REVIEW/REJECTED.
2. `POST /api/v1/orders/{id}/evaluate`: load context, run 6 checks, persist result.
3. Decision: all pass → APPROVED; blocking fail → REJECTED; only missing/N/D evidence → NEEDS_REVIEW. Mapping in `docs/checks.md`.
4. `GET /api/v1/orders/{id}` response includes per-check result + decision.
5. Tests: approve, reject, review scenarios.
Files: `backend/db/007_order_checks.sql`, `backend/app/api/routes/orders.py`, `backend/app/services/checks.py`, `docs/checks.md`, `backend/tests/test_evaluate.py`.
Done: order evaluated → decision saved in DB.

T5.3-B — Backend settle/refund wiring:
1. `backend/app/services/settlement.py`: APPROVED → settle, REJECTED → refund, NEEDS_REVIEW → no-op. Calls middleware.
2. Success → order `SETTLED/REFUNDED`, `tx_hash` saved; idempotent (repeat → 409/200).
3. Middleware/chain fail → order state unchanged; 502.
4. Tests: mocked middleware approve/reject/idempotency; manual local chain test.
Files: `backend/app/services/settlement.py`, `backend/app/api/routes/orders.py`, `backend/tests/test_settlement.py`.
Done: after evaluate, settle/refund called and tx hash in DB.

T8.1 — Real PostGIS integration tests:
1. `backend/tests/conftest.py`: `TEST_DATABASE_URL`, schema apply, per-test rollback.
2. Integration tests: parcel bbox, ALU grid, bundle validation, listing/order transitions, evaluate decision, evidence persistence.
3. Marker `@pytest.mark.integration`; default `pytest` stays fast, integration runs via separate command.
4. `Makefile` target `test-integration`.
Files: `backend/tests/conftest.py`, `backend/tests/test_integration_*.py`, `backend/pyproject.toml`, `Makefile`.
Done: DB up → all integration tests pass.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `backend/log-b.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add backend/ whole_plan.md Makefile` (NEVER `git add -A`).
- Commit: `git commit -m "feat(trade): evaluate, settle and integration-test orders"`.
- Push: `git push -u origin backend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: BACKEND — Batch B5 — END -->

<!-- PROMPT: BACKEND — Batch B6 (T8.3-B, T9.1) — START -->
I am Yash on `backend/<name>`. Complete batch B6 = T8.3-B, T9.1. Commit message: `chore(backend): harden and add alu locking`.

Read: root `whole_plan.md` Phase 8 (T8.3-B), Phase 9 (T9.1), `docs/context/C8.md`, `docs/context/C9.md`. Depends on T8.1, C5.

T8.3-B — Backend security/quality gate:
1. Input validation, CORS, error leakage on backend routes.
2. `ruff`, `pytest`, `pytest -m integration`.
3. Backend part of `docs/limitations.md` (demo data, KYC stub, testnet only).
Done: `ruff check backend && pytest -q backend` pass.

T9.1 — ALU locking + double-sell protection (stretch):
1. `backend/db/008_alu_locks.sql`: per-ALU unique active listing; sold ALU lock.
2. Tests: same ALU in two active listings → reject.
Files: `backend/db/008_alu_locks.sql`, `backend/app/services/alu_grid.py`, `backend/app/api/routes/alus.py`, `backend/tests/test_alu_locks.py`.
Done: one ALU cannot be in two active listings.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `backend/log-b.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add backend/ whole_plan.md docs/checks.md docs/limitations.md` (NEVER `git add -A`).
- Commit: `git commit -m "chore(backend): harden and add alu locking"`.
- Push: `git push -u origin backend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: BACKEND — Batch B6 — END -->
