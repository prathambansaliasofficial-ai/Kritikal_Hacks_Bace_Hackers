<!--
  GENERATED FILE. Source: whole_plan.md
  Do not edit this copy. Edit the root file, then run: npm run sync:docs
-->
RED BRANCH: FRONTEND 
YELLOW BRANCH: MIDDLEWARE 
BLUE BRANCH: BACKEND 
EVERYONE WORK ON THEIR SPECIFIC BRANCH ONLY



# Land Market — Master Roadmap (Zero → One)

Last updated: **2026-10-29 23:30 IST**
Status markers: `[.]` = done, `[]` = pending.
Progress: **5 / 35 tasks done (14%)** (`C0` is a gate, not counted in the 35).
Current batch: **C0 — baseline commit** (lead only, already-built scaffold).
Next module batch: **backend `B1` — T1.1, T1.2, T1.3**.
MVP cut line: **Phase 8 ke end tak**. Phase 9 sirf time bache to.

> Ye file hi single source of truth hai. Koi bhi AI kaam shuru karne se pehle yahi file padhe,
> phir apne module ke task ID order me kaam kare. Task complete hone par block ko neeche
> `YEH SAB HO GYA` section me move kare, heading ka marker badle, aur apni module log update kare.

## Team model (pehle ye padho)

- Ek person = ek module branch: `backend/<name>`, `middleware/<name>`, `ai/<name>`,
  `frontend/<name>`. `main` sirf lead merge karta hai.
- Kaun kaunsa task karega: `docs/task-ownership.md`.
- Branch, PR, merge order, conflict rules: `docs/team-workflow.md`.
- Module ke andar kaise chalana hai: `frontend/AGENTS.md`, `backend/AGENTS.md`,
  `middleware/AGENTS.md` + unka `SETUP.md`.

**Cross-module tasks** (`T3.1`, `T5.3`, `T6.1`, `T8.3`, `T9.3`) are split by module.
Do only your slice; the other owner does theirs. The suffix map is in
`docs/task-ownership.md` §1.

## AI worker ke liye 7 hard rules

1. Apne module ke task ID ascending order me karo. Doosre module ka task skip karo, use apne
   branch par mat lo. Cross-module task ka sirf apna slice karo (`docs/task-ownership.md`).
2. Apne module ke **3 tasks** complete hone tak commit mat karo. Batch ke end me given commit
   message use karo (module batch table: `docs/task-ownership.md` §2).
3. Har task ke saath code + test + docs update karo. "Baad me dekhenge" allowed nahi.
4. Task done karte hi heading `### [] T1.1 — ...` ko `### [.] T1.1 — ...` karo, block ko `YEH SAB HO GYA` me move karo, aur `**Done:** YYYY-MM-DD HH:MM IST — Session N` line add karo. **Phase counter aur top progress line lead update karta hai** — intern unhe mat chhedo.
5. Har batch ke baad sirf apni module log update karo: `frontend/log-f.md`,
   `backend/log-b.md`, ya `middleware/log-m.md` — completed item `[.]`, pending item `[]`.
6. Blocker aaye to task ko `[]` hi rakho, `**BLOCKED:**` line likho, aur human se poocho. Fake data, fake API key, fake transaction hash — kabhi nahi.
7. Demo data ko hamesha `DEMO_FIXTURE_NOT_OFFICIAL` label karo. Live government data ka claim mat karo.

## Repo map (files apni jagah par)

```
root/                  whole-project files: opencode.json, package.json,
                       docker-compose.yml, .env*, SETUP.md, whole_plan.md
frontend/              app code + log-f.md + AGENTS.md + SETUP.md + generated docs/
backend/               API + DB + log-b.md + AGENTS.md + SETUP.md + generated docs/
middleware/            TinyFish + chain + log-m.md + AGENTS.md + SETUP.md + generated docs/
docs/                  contracts, decisions, context packs, branch workflow, references
scripts/               sync-docs.mjs, check-docs.mjs, demo.sh
```

Naya module-specific file uske module folder me rakho. Root me sirf wo file rakho jo poore
project ne use karni ho. Logs apne module folder me hi rahenge:
`frontend/log-f.md`, `backend/log-b.md`, `middleware/log-m.md`.

`frontend/whole_plan.md`, `backend/whole_plan.md`, `middleware/whole_plan.md` aur
`*/docs/**` **generated read-only copies** hain. Inhe haath se mat edit karo:
root file edit karo, phir `npm run sync:docs`.

## Commit rule (har module batch ke baad)

```bash
# 1. Sirf apne module + task-allowed root files stage karo (git add -A mat karo)
git add backend/ whole_plan.md          # example: backend branch
git commit -m "<batch ka diya hua message>"

# 2. Hash note karo
git log -1 --format=%h

# 3. Generated module copies refresh karo (root docs edit kiye ho to)
npm run sync:docs
npm run check:docs

# 4. Apni branch push karo; main par sirf lead merge karta hai
git push -u origin backend/<your-name>
```

Commit message format: `type(scope): chhota imperative sentence` — 72 characters se kam.
Push ke baad PR kholo. `git push origin main` **kabhi nahi**.

## Definition of done (har task)

- [ ] Code task block + `docs/api-contract.md` se match karta hai.
- [ ] Task ke named tests + module checks pass.
- [ ] Koi fake key / run ID / TxHash / government record nahi.
- [ ] Demo data labelled (`DEMO_FIXTURE_NOT_OFFICIAL` / `demo: true`).
- [ ] Module log updated; apna task marker `[.]`.
- [ ] `npm run sync:docs && npm run check:docs` pass.
- [ ] Commit message batch table se match karta hai.

## MVP demo definition (Phase 8 ke end me ye chalna chahiye)

1. Officer demo ULPIN submit karta hai.
2. TinyFish asli agent run karke 21-field evidence sheet laata hai.
3. Evidence DB me hash ke saath save hoti hai; officer approve/reject kar sakta hai.
4. Parcel aur uske ALU bundle map par dikhte hain.
5. Citizen wallet connect karke listing kharidta hai; paisa escrow contract me jaata hai.
6. Backend 6 checks chalata hai; pass par `settle()`, hard fail par `refund()`.
7. UI par har check ka result, decision, tx hash aur explorer link dikhta hai.

---

# YEH SAB HO GYA

## Phase 0 — Foundation — [5/5]

### [.] T0.1 — Monorepo aur local setup

**Done:** 2026-10-29 21:39 IST — Session 2

**Kya hua:** Root config files aur `SETUP.md` banaye.
**Kya karta hai:** Koi bhi developer teen services (web, API, evidence/chain) ek hi repo me
setup kar sakta hai; secrets `.env` me rehte hain, git me nahi jaate.
**Files:** `.gitignore`, `.editorconfig`, `.nvmrc`, `.env.example`, `docker-compose.yml`,
`package.json`, `SETUP.md`.

### [.] T0.2 — Frontend shell

**Done:** 2026-10-29 21:42 IST — Session 2

**Kya hua:** React 19 + TypeScript + Vite + MapLibre shell, health pills, ULPIN form.
**Kya karta hai:** Demo ki entry screen ready hai; abhi data fake/placeholder hai.
**Files:** `frontend/` (package/tsconfig/vite/index + `src/App.tsx`, `src/components/MapView.tsx`,
`src/lib/api.ts`, `src/index.css`).
**Proof:** `npm --prefix frontend run typecheck` aur `build` pass.

### [.] T0.3 — Backend skeleton aur database schema

**Done:** 2026-10-29 21:42 IST — Session 2

**Kya hua:** FastAPI health + verification proxy, PostGIS schema.
**Kya karta hai:** API request receive karta hai; DB me parcel, ALU, evidence, listing aur
order rakhne ki jagah ready hai.
**Files:** `backend/requirements*.txt`, `backend/pyproject.toml`, `backend/app/**`,
`backend/db/001_init.sql`, `backend/tests/test_health.py`.
**Proof:** `ruff check .` pass, `pytest -q` 2 passed.

### [.] T0.4 — Middleware aur escrow contract

**Done:** 2026-10-29 21:45 IST — Session 2

**Kya hua:** TinyFish evidence collector, Fastify routes, `LandMarketEscrow` contract + tests.
**Kya karta hai:** Evidence laata hai; buyer ka paisa tab tak hold karta hai jab tak checks pass
na ho; pass par seller ko, fail par buyer ko wapas.
**Files:** `middleware/package.json`, `hardhat.config.ts`, `contracts/LandMarketEscrow.sol`,
`test/LandMarketEscrow.test.ts`, `scripts/deploy.ts`, `scripts/smoke-tinyfish.ts`,
`src/config.ts`, `src/server.ts`, `src/tinyfish/evidence.ts`, `src/blockchain/escrow.ts`.
**Proof:** `typecheck` pass, `compile` pass, `hardhat test` 4 passing, prod audit 0.

### [.] T0.5 — Logs aur roadmap

**Done:** 2026-10-29 21:54 IST — Session 4

**Kya hua:** Hinglish logs ko `[.]`/`[]` format me rewrite kiya aur ye master roadmap banaya.
**Kya karta hai:** Har AI ko pata rahega kya done hai, kya pending, next commit message kya hai.
**Files:** `frontend/log-f.md`, `backend/log-b.md`, `middleware/log-m.md`, `whole_plan.md`.

## C0 — Baseline commit — [1/1]

### [.] C0 — Jo bana hua hai use git me lock karo

**Done:** 2026-11-02 12:00 IST — Session C0

**Kya hua:** Baseline commit `729e9eb` — `C0 FIRST WORTHY COMMIT- LOCKING ALREADY BUILT` — already pushed to `main`. All scaffold files locked: `.gitignore`, `.editorconfig`, `.nvmrc`, `.env.example`, `docker-compose.yml`, `package.json`, `README.md`, `SETUP.md`, `AGENTS.md`, `whole_plan.md`, `docs/`, `scripts/`, `frontend/`, `backend/`, `middleware/`. Junk file `test.txt` deletion staged. No `.env` or secrets committed.

**Kya karta hai:** Monorepo scaffold ab `main` par hai; interns ab `main` se apne branches bana sakte hain (`backend/<name>`, `middleware/<name>`, `frontend/<name>`, `ai/<name>`).

**Files:** `.gitignore`, `.editorconfig`, `.nvmrc`, `.env.example`, `docker-compose.yml`, `package.json`, `README.md`, `SETUP.md`, `AGENTS.md`, `whole_plan.md`, `docs/`, `scripts/`, `frontend/`, `backend/`, `middleware/`.

**Verify:** `git log --oneline -1` shows `729e9eb`; `git status --short` is clean.

### [.] T1.1 — PostGIS boot karke schema verify karo

**Done:** 2026-11-10 09:27 IST — Session 7

**Kya hua:** `backend/scripts/check_db.py` banaya — PostGIS version, 6 table names, row counts print karta hai; DB na mile to exit code 1 deta hai. Root `Makefile` banaya: `db-up`, `db-check`, `db-reset` (volume delete se pehle prompt), `seed`, `api`, `mid`, `web`, `check`. `backend/SETUP.md` me Makefile shortcuts aur demo ULPIN note add kiya.
**Kya karta hai:** DB health check failure par exit 1 deta hai (fail closed); repo root se service start/check shortcuts ready.
**Files:** `backend/scripts/check_db.py`, `Makefile`, `backend/SETUP.md`.
**Verify:** `ruff check backend` + `pytest -q backend` pass (13 passed); `check_db.py` exit code 1 jab DB down ho (verify kiya). Live `make db-up && make db-check` ke liye Docker chahiye, jo is session me nahi chala.

### [.] T1.2 — Database access layer banao

**Done:** 2026-11-10 09:27 IST — Session 7

**Kya hua:** `app/core/db.py` me `@contextmanager db_connection()` banaya (`dict_row`, `connect_timeout=5`, commit/rollback/close). `check_database()` ab isi layer par chalta hai; failure par `{"status": "unavailable", ...}` return karta hai, raise nahi. `app/repositories/base.py` me `fetch_one`, `fetch_all`, `execute` banaye. Health route `check_database` se chale; routes me koi direct `psycopg.connect` nahi. `tests/test_db.py`: galat URL par `unavailable`, raise nahi.
**Kya karta hai:** Pure API ke liye ek DB access point.
**Files:** `backend/app/core/db.py`, `backend/app/repositories/__init__.py`, `backend/app/repositories/base.py`, `backend/tests/test_db.py`.
**Verify:** `rg "psycopg.connect" backend/app` sirf `core/db.py` me; ruff + pytest pass.

### [.] T1.3 — Demo parcel, ALU aur bundle ke liye seed data

**Done:** 2026-11-10 09:27 IST — Session 7

**Kya hua:** `db/002_seed_demo.sql` banaya: parcel `DEMO-ULPIN-001`, `geometry_source='DEMO_FIXTURE_NOT_OFFICIAL'`, attributes `{"owner_name": "Demo Owner", "district": "Pune", "zoning": "Residential"}`; parent `ALU-100m-DEMO-000`; children `ALU-10m-DEMO-001`…`004` parent-linked; 4 `parcel_alus` `CONTAINS`, `overlap_percentage=100`. `scripts/seed.py` banaya (idempotent: demo rows pehle delete, phir insert). `Makefile` ka `seed` target add kiya; `SETUP.md` me demo ULPIN note add kiya.
**Kya karta hai:** Demo parcel + 5 ALUs + 4 links; dobara chalane par duplicate nahi.
**Files:** `backend/db/002_seed_demo.sql`, `backend/scripts/seed.py`, `Makefile`, `backend/SETUP.md`.
**Verify:** `make seed` ke baad 1 parcel, 5 ALUs, 4 links; idempotency delete-then-insert exact IDs se guarantee hai. Live `make db-check && make seed && make db-check` ke liye Docker chahiye, jo is session me nahi chala.

### Commit batch C1 — T1.1, T1.2, T1.3

**Message:** `feat(db): add postgis checks, db helpers and demo seed`

### [.] T2.1 — Parcel read API

**Done:** 2026-11-10 11:30 IST — Session 8

**Kya hua:** `backend/app/repositories/parcels.py` banaya — `get_parcel(ulpin)` aur `list_parcels(bbox, limit)` with
`ST_AsGeoJSON`, `ST_MakeEnvelope(...,4326)`, `ST_Intersects`. `backend/app/api/routes/parcels.py`:
`GET /api/v1/parcels/{ulpin}` → Parcel Feature (missing 404), `GET /api/v1/parcels?bbox=...&limit=100` → FeatureCollection
(limit max 100, invalid bbox 422). Router registered in `app/api/main.py`. `demo: true` set when
`geometry_source='DEMO_FIXTURE_NOT_OFFICIAL'`.
**Kya karta hai:** GeoJSON parcel read API; bbox + limit validation at the route.
**Files:** `backend/app/repositories/parcels.py`, `backend/app/api/routes/parcels.py`, `backend/app/api/main.py`,
`backend/tests/test_parcels.py`.
**Verify:** ruff clean, `pytest -q backend` 33 passed; missing→404, invalid bbox→422, limit 101→422 (unit-tested via
mocked repo; live DB needs Docker).

### [.] T2.2 — Deterministic ALU grid endpoint

**Done:** 2026-11-10 11:30 IST — Session 8

**Kya hua:** `backend/app/services/alu_grid.py` banaya exactly `docs/decisions.md` §3: Web Mercator forward/inverse,
`ALU-{level}-{slug(ix)}-{slug(iy)}` IDs, parent = next coarser level (`1km` → null), closed GeoJSON polygon ring,
`area_sqm`, hard cap 1500 with `GridError("Zoom in: N cells exceeds 1500")`. `backend/app/api/routes/alus.py`:
`GET /api/v1/alus?bbox=...&level=10m` → FeatureCollection; unknown level 422; over-cap → 422. Shared `parse_bbox` in
`app/api/routes/bbox.py`. Router registered in `app/api/main.py`.
**Kya karta hai:** Deterministic ALU grid cells for a bbox/level with parent links and 1500-cell cap.
**Files:** `backend/app/services/alu_grid.py`, `backend/app/api/routes/alus.py`, `backend/app/api/routes/bbox.py`,
`backend/app/api/main.py`, `backend/tests/test_alu_grid.py`.
**Verify:** ruff clean; `pytest -q backend/tests/test_alu_grid.py` pass (determinism, parent-child, cap, negative `m` slug,
unknown level 422, over-cap route 422, feature collection shape).

### [.] T2.3 — Bundle schema aur API

**Done:** 2026-11-10 11:30 IST — Session 8

**Kya hua:** `db/003_bundles.sql` banaya: `bundles` (id, ulpin FK, name, status DRAFT/ACTIVE/PAUSED/ARCHIVED,
created_by, timestamps) aur `bundle_alus` (bundle_id, alu_id PK). `backend/app/repositories/bundles.py`:
`create_bundle`, `get_bundle`, `set_bundle_status` with validation (ULPIN exists → 404; ALUs exist + linked to parcel →
422; duplicate ALU → 422; allowed transitions DRAFT→ACTIVE/PAUSED/ARCHIVED, ACTIVE→PAUSED/ARCHIVED, PAUSED→ACTIVE/ARCHIVED,
else 409). `backend/app/api/routes/bundles.py`: POST /bundles (201), GET /bundles/{id}, PATCH /bundles/{id} status.
Router registered in `app/api/main.py`.
**Kya karta hai:** Bundle create/read/status with parcel-scoped ALU validation and status-transition rules.
**Files:** `backend/db/003_bundles.sql`, `backend/app/repositories/bundles.py`, `backend/app/api/routes/bundles.py`,
`backend/app/api/main.py`, `backend/tests/test_bundles.py`.
**Verify:** ruff clean; `pytest -q backend` pass (happy path, cross-parcel 422, duplicate 422, invalid transition 409,
GET found/missing, PATCH happy) via mocked repo; live DB needs Docker.

### Commit batch C2 — T2.1, T2.2, T2.3

**Message:** `feat(api): expose parcels, alu grid and bundles`

### [.] T3.2 — Evidence validate, hash aur DB me save karo

**Done:** 2026-11-10 14:00 IST — Session 9

**Kya hua:** `backend/app/services/evidence.py` banaya — EVIDENCE_FIELDS (21 keys), normalize_sheet (missing/invalid → N/D, extra dropped), canonical_hash (0x + sha256 canonical JSON per decisions §4). `POST /api/v1/verifications` update kiya: middleware ko camelCase `sourceUrl` bhejta hai; response validate karta hai (middleware down 503, invalid sheet 422, other error 502); `evidence_sheets` me payload/source_refs/tinyfish_run_id/status='PENDING' save karta hai; hash payload ke andar aur top-level `evidence_hash` dono mein store karta hai; return `{ulpin,status,evidence_id,evidence_hash,tinyfish_run_id,fields,sources}`. `backend/app/api/routes/evidence.py`: GET /evidence/{id}, GET /evidence?ulpin=. `backend/app/repositories/evidence.py`: create_evidence_sheet, get_evidence_sheet, list_evidence_sheets. Routers registered in app/api/main.py.
**Kya karta hai:** TinyFish evidence validate → hash → persist, evidence GET endpoints.
**Files:** `backend/app/services/evidence.py`, `backend/app/repositories/evidence.py`, `backend/app/api/routes/verifications.py`, `backend/app/api/routes/evidence.py`, `backend/app/api/main.py`, `backend/tests/test_evidence.py`.
**Verify:** ruff clean; `pytest -q backend/tests/test_evidence.py` pass (normalize, hash determinism, happy path, middleware down 503, invalid sheet 422, middleware error 502, blank ulpin 422).

### [.] T3.3 — Officer review queue

**Done:** 2026-11-10 14:00 IST — Session 9

**Kya hua:** `backend/db/004_review.sql` banaya — evidence_sheets me `review_reason TEXT`, `reviewed_at TIMESTAMPTZ` (IF NOT EXISTS). `backend/app/repositories/evidence.py` me list_reviews aur decide_review (APPROVE→CLEAN, REJECT→REJECTED, PENDING/NEEDS_REVIEW se hi allowed, repeat → ValueError→409, reject bina reason → 422). `backend/app/api/routes/reviews.py`: GET /reviews?status=PENDING|NEEDS_REVIEW, POST /reviews/{id}/decision with X-Officer-Token (401 missing/wrong); reviewed_by, review_reason, reviewed_at save karta hai. Router registered in app/api/main.py.
**Kya karta hai:** Officer review queue aur evidence approve/reject transition.
**Files:** `backend/db/004_review.sql`, `backend/app/api/routes/reviews.py`, `backend/app/repositories/evidence.py`, `backend/app/api/main.py`, `backend/tests/test_reviews.py`.
**Verify:** ruff clean; `pytest -q backend/tests/test_reviews.py` pass (pending items, approve, reject, 401 missing/wrong token, 422 reject-no-reason, 409 already-decided, 404 not found).

### [.] T4.1 — Wallet user aur KYC stub

**Done:** 2026-11-10 14:00 IST — Session 9

**Kya hua:** `backend/db/005_users.sql` banaya — users (id, wallet_address UNIQUE, role CITIZEN/OFFICER, kyc_status PENDING/VERIFIED/REJECTED, timestamps). `backend/app/repositories/users.py` — is_valid_wallet (`^0x[a-fA-F0-9]{40}$`), upsert_user, get_user, update_kyc. `backend/app/api/routes/users.py`: POST /users (upsert, 200), GET /users/{wallet} (404 missing, 422 invalid wallet), POST /users/{wallet}/kyc (X-Officer-Token vs DEV_OFFICER_TOKEN, 401/402/409, KYC update 200). `backend/.env.example` aur `backend/.env` me DEV_OFFICER_TOKEN add kiya; `app/core/config.py` me `dev_officer_token` field add kiya. Router registered in app/api/main.py.
**Kya karta hai:** Wallet user upsert aur prototype KYC stub (officer token auth).
**Files:** `backend/db/005_users.sql`, `backend/app/api/routes/users.py`, `backend/app/repositories/users.py`, `backend/app/api/main.py`, `backend/.env.example`, `backend/.env`, `backend/app/core/config.py`, `backend/tests/test_users.py`.
**Verify:** ruff clean; `pytest -q backend/tests/test_users.py` pass (invalid wallet 422, upsert, get found/missing, missing/wrong token 401, KYC update 200).

### Commit batch C3 — T3.2, T3.3, T4.1

**Message:** `feat(evidence): persist evidence, review queue and wallet users`

### [.] T4.2 — Listing create/browse/pause

**Done:** 2026-11-10 16:00 IST — Session 10

**Kya hua:** `db/006_listings_bundle.sql` banaya — `listings` me `bundle_id BIGINT REFERENCES bundles(id)` column (IF NOT EXISTS) aur index. `backend/app/repositories/listings.py` banaya — `create_listing`, `list_listings`, `get_listing`, `patch_listing_status` with rules: seller KYC VERIFIED (409), bundle ACTIVE (409), price_wei > 0 (422), one active listing per bundle (409), allowed transitions DRAFT→LISTED/CANCELLED, LISTED→PAUSED/CANCELLED, PAUSED→LISTED/CANCELLED (else 409). `backend/app/api/routes/listings.py`: POST /listings (201), GET /listings?status= (default LISTED), PATCH /listings/{id} status. Router registered in app/api/main.py.
**Kya karta hai:** Listing lifecycle with bundle-scoped uniqueness and status transitions.
**Files:** `backend/db/006_listings_bundle.sql`, `backend/app/api/routes/listings.py`, `backend/app/repositories/listings.py`, `backend/app/api/main.py`, `backend/tests/test_listings.py`.
**Verify:** ruff clean; `pytest -q backend/tests/test_listings.py` pass (happy, unverified 409, duplicate active 409, invalid transition 409, GET items, invalid price 422) via mocked repo; live DB needs Docker.

### [.] T4.3 — Order lifecycle

**Done:** 2026-11-10 16:00 IST — Session 10

**Kya hua:** `backend/app/repositories/orders.py` banaya — `create_order` (buyer KYC VERIFIED, listing LISTED, buyer≠seller, amount=listing price → CREATED; self-buy/unverified/wrong-price 409), `fund_order` (bytes32 validation 422, chain_order_id recomputed via keccak256 per decisions §5 and matched else 422, CREATED→FUNDED, duplicate 409), `get_order`. `backend/app/api/routes/orders.py`: POST /orders (201), POST /orders/{id}/funded, GET /orders/{id} returning order shape with `chain_order_id`. `app/services/chain.py` — pure-Python keccak-256 via pycryptodome (verified against NIST vectors) added to `requirements.txt`. Router registered in app/api/main.py.
**Kya karta hai:** Order create/fund lifecycle with chain order ID commitment.
**Files:** `backend/app/repositories/orders.py`, `backend/app/api/routes/orders.py`, `backend/app/api/main.py`, `backend/app/services/chain.py`, `backend/requirements.txt`, `backend/tests/test_orders.py`.
**Verify:** ruff clean; `pytest -q backend/tests/test_orders.py` pass (happy, self-buy 409, unverified 409, duplicate funding 409, invalid bytes32 422, chain_order mismatch 422, GET found/missing) via mocked repo; live DB needs Docker.

### [.] T5.1 — 6 checks ka pure rule engine

**Done:** 2026-11-10 16:00 IST — Session 10

**Kya hua:** `backend/app/services/checks.py` banaya — `CheckResult(name, passed, reason, blocking)` dataclass aur 6 pure functions: `check_listed`, `check_bundle_intact`, `check_kyc_wallet`, `check_zoning_ok`, `check_funds_in_escrow`, `check_trade_match`. Sab blocking. `docs/checks.md` banaya — policy, decision mapping (APPROVED/REJECTED/NEEDS_REVIEW), aur demo assumptions. `backend/tests/test_checks.py` — 19 tests (pass/fail per check, 6 check names covered).
**Kya karta hai:** DB-free six-check rule engine for trade decisions.
**Files:** `backend/app/services/checks.py`, `docs/checks.md`, `backend/tests/test_checks.py`.
**Verify:** ruff clean; `pytest -q backend/tests/test_checks.py` pass (19 tests); DB-independent.

### Commit batch C4 — T4.2, T4.3, T5.1

**Message:** `feat(market): add listings, orders and six checks`

### [.] T5.2 — Evaluate endpoint aur decision policy

**Done:** 2026-11-10 18:30 IST — Session 11

**Kya hua:** `backend/db/007_order_checks.sql` banaya — orders me `checks JSONB`, `decision TEXT`, `decided_at TIMESTAMPTZ` column (IF NOT EXISTS). `backend/app/services/checks.py` me `run_checks(context)` aur `decide(results)` aur `check_results_to_api()` banaye — `missing_evidence` flag se ZONING_OK missing = NEEDS_REVIEW, blocking fail = REJECTED, sab pass = APPROVED. `backend/app/api/routes/orders.py` me `POST /api/v1/orders/{id}/evaluate` (async) banaya — order FUNDED ho (warna 409), listing/bundle/ALUs/users/evidence load karo, middleware se chain state lo (failure → 502, koi persist nahi), run_checks + decide karo, `save_evaluate` se DB me save karo, phir `apply_decision` (settle/refund/no-op) call karo. `backend/app/services/chain_client.py` banaya — middleware `GET /escrow/status/{orderId}` call kar ke chain state wapas kare (failure → ChainClientError → 502). Router registered in app/api/main.py.
**Kya karta hai:** Order evaluate → 6 checks → decision persist → settlement trigger.
**Files:** `backend/db/007_order_checks.sql`, `backend/app/api/routes/orders.py`, `backend/app/services/checks.py`, `backend/app/services/chain_client.py`, `backend/app/services/settlement.py`, `backend/tests/test_evaluate.py`.
**Verify:** ruff clean; `pytest -q backend/tests/test_evaluate.py` pass (approve→settle, reject→refund, review→no-op, non-funded 404/409, not-found 404, chain down 502) via mocked repo + middleware + settlement; live DB needs Docker.

### [.] T5.3-B — Backend settle/refund wiring (backend slice)

**Done:** 2026-11-10 18:30 IST — Session 11

**Kya hua:** `backend/app/services/settlement.py` banaya — `apply_decision(order, decision)` async: APPROVED → POST /escrow/settle (state SETTLED), REJECTED → POST /escrow/refund (state REFUNDED), NEEDS_REVIEW → no-op; terminal state pe idempotent (dobara call → current state, koi middleware call nahi); middleware/chain fail par SettlementError → 502, state unchanged; success par DB me state + tx_hash save. `backend/app/api/routes/orders.py` me evaluate se call kiya jaata hai. Middleware `T5.3-M` tak mock kiya ja sakta hai.
**Kya karta hai:** APPROVED→settle, REJECTED→refund, NEEDS_REVIEW→no-op, idempotent, fail-safe.
**Files:** `backend/app/services/settlement.py`, `backend/app/api/routes/orders.py`, `backend/tests/test_evaluate.py`.
**Verify:** ruff clean; pytest pass (evaluate tests cover approve/reject/review settlement paths) via mocked middleware; live chain/manual test needs Docker + middleware.

### [.] T8.1 — Real PostGIS integration tests

**Done:** 2026-11-10 18:30 IST — Session 11

**Kya hua:** `backend/tests/conftest.py` banaya — `TEST_DATABASE_URL`, `apply_schema` (sab 0*.sql migration ek baar), `db` fixture (per-test rollback). `backend/tests/test_integration.py` banaya — `@pytest.mark.integration` test: parcel+ALU persistence, bundle+listing flow, order+evidence persistence. `backend/pyproject.toml` me `integration` marker aur `addopts = ["-m", "not integration"]` add kiya (default pytest fast, integration alag command se). Root `Makefile` me `test-integration` target add kiya. `backend/tests/test_checks.py` me `run_checks`/`decide` unit tests (all-pass→APPROVED, hard-fail→REJECTED, zoning-missing→NEEDS_REVIEW) add kiye.
**Kya karta hai:** Real PostGIS DB par integration tests; default pytest chalna fast rahe, integration `make test-integration` se.
**Files:** `backend/tests/conftest.py`, `backend/tests/test_integration.py`, `backend/pyproject.toml`, `Makefile`, `backend/tests/test_checks.py`.
**Verify:** ruff clean; `pytest -q backend` — 120 passed, 3 integration deselected (default fast). Live `make db-up && make test-integration` needs Docker (nahi chala is session me).


### Commit batch C5 — T5.2, T5.3-B, T8.1

**Message:** `feat(trade): evaluate, settle and integration-test orders`



---


- [.] 22:05 — Logs apne module folders me move kiye: `frontend/log-f.md`,
  `backend/log-b.md`, `middleware/log-m.md`.
- [.] 22:05 — Junk/empty files delete kiye: `react.txt`, `test.js`, `README of this project.md`.
- [.] 22:05 — Reference docs `docs/` me move kiye: hackathon rules, tech-stack guide,
  old-project reference.
- [.] 22:10 — Root `README.md` project overview ke saath recreate kiya.
- [.] 22:10 — `opencode.json` se hardcoded API key hataya; key ab environment se aayegi.
  Key git history me kabhi commit nahi hui.
- [.] 22:11 — Frontend typecheck/build, backend ruff/pytest, middleware typecheck/test,
  `docker compose config`, aur JSON validation pass.
- [.] Commit/push — C0 me hoga.

---

# ABHI YEH YEH KARNA HAI

## Phase 1 — Data foundation — [0/3]

**Owner:** Backend. Context pack: `docs/context/C1.md`.



---

## Phase 2 — Parcel, ALU aur bundle API — [0/3]

**Owner:** Backend. Context pack: `docs/context/C2.md`.


---

## Phase 3 — TinyFish evidence pipeline — [0/3]

**Owner split:** `T3.1` middleware/AI; `T3.2`–`T3.3` backend. Context pack: `docs/context/C3.md`.

### [] T3.1 — TinyFish live run ka asli proof

**Owner:** Middleware / AI branch. Backend `T3.2` does **not** wait for this; use a
mocked middleware response until the key arrives.

**BLOCKED:** human se `TINYFISH_API_KEY` chahiye. Key na mile to task `[]` rakho,
fake run mat karo.

**Kya karna hai**
1. **BLOCKER:** human se `TINYFISH_API_KEY` lo. Key na mile to task `[]` rakho, fake run mat karo.
2. `middleware/.env` me key daalo; `npm --prefix middleware run smoke:tinyfish` chalao.
3. Asli ULPIN ke liye BhuNaksha ya jo portal officer de, us par ek run karo; run ID, source URLs,
   status aur latency note karo.
4. `docs/tinyfish-smoke.md` banao: date, URL, goal, run ID, result summary, screenshot path.
   Key kabhi commit mat karo.
5. Agar CAPTCHA/block aaye to wahi document karo aur alternate source URL try karo.

**Files:** `docs/tinyfish-smoke.md`, `middleware/.env` (local only), zarurat ho to
`middleware/src/tinyfish/evidence.ts` goal tuning.
**Done criteria:** Real `COMPLETE` event + kam se kam 1 asli source URL document ho.
**Verify:** `npm --prefix middleware run smoke:tinyfish`.


---


## Phase 4 — Identity, listing aur order — [0/3]

**Owner:** Backend. Context pack: `docs/context/C4.md`.


---

## Phase 5 — 6 checks aur settlement — [0/3]

**Owner split:** `T5.1`, `T5.2`, `T5.3-B` backend; `T5.3-M` middleware. Context pack: `docs/context/C5.md`.



### [] T5.3-M — Middleware escrow status endpoint (middleware slice)

**Owner:** Middleware. Do this before backend `T5.3-B` if possible; backend can mock it.

**Kya karna hai**
1. `middleware/src/server.ts` me `GET /escrow/status/:orderId` add karo — contract
   `orderState` padhe (0 None, 1 Funded, 2 Settled, 3 Refunded).
2. Invalid order ID par 400, chain error par 502.
3. Response exactly `{orderId, state, label}` per `docs/api-contract.md` §4.

**Files:** `middleware/src/server.ts`, `middleware/src/blockchain/escrow.ts`, middleware tests.
**Done criteria:** `curl localhost:8090/escrow/status/<orderId>` sahi state deta hai.
**Verify:** local chain + `curl`.


---


## Phase 6 — Blockchain deployment — [0/3]

**Owner split:** `T6.1-M`, `T6.2`, `T6.3` middleware; `T6.1-F` frontend. Context pack: `docs/context/C6.md`.

### [] T6.1-M — Deploy artifacts (middleware slice)

**Owner:** Middleware.

1. `middleware/scripts/deploy.ts` deploy ke baad `middleware/deployments/<network>.json` likhe:
   address, chainId, deployer, operator, deployedAt.
2. Commit a small `deployments/localhost.json` example (no key), or document generation.
3. Addresses docs me commit karo; `.env` kabhi nahi.

**Files:** `middleware/scripts/deploy.ts`, `middleware/deployments/`.
**Done criteria:** Local deploy ke baad address file ready.
**Verify:** `npm --prefix middleware run deploy:local`.

### [] T6.1-F — ABI + chain config (frontend slice)

**Owner:** Frontend. Can use the artifact from a local middleware build.

1. ABI ko `frontend/src/lib/escrowAbi.json` me copy karo (artifact se).
2. Frontend config `VITE_ESCROW_ADDRESS`, `VITE_CHAIN_ID`, `VITE_CHAIN_NAME`,
   `VITE_EXPLORER_URL` padhe; missing ho to UI par clear warning dikhe, crash na ho.
3. `frontend/.env.example` update karo.

**Files:** `frontend/src/lib/escrowAbi.json`, `frontend/src/lib/chain.ts`, `frontend/.env.example`.
**Done criteria:** Missing address shows warning; configured address works.
**Verify:** `npm --prefix frontend run typecheck && npm --prefix frontend run build`.

### [] T6.2 — Local chain smoke test

**Owner:** Middleware.

**Kya karna hai**

**Kya karna hai**
1. `middleware/scripts/chain-smoke.ts`: buyer se `createOrder`, operator se `settle`,
   `orderState` check, events verify.
2. `npm run chain:smoke` script add karo; Hardhat node assume kare ya khud spawn kare.
3. Root `Makefile` me `chain` target: node start + deploy + smoke.
4. README me local chain steps.

**Files:** `middleware/scripts/chain-smoke.ts`, `middleware/package.json`, `Makefile`,
`middleware/README.md`.
**Done criteria:** `npm --prefix middleware run chain:smoke` pass.
**Verify:** terminal 1 `npm --prefix middleware run node`, terminal 2 smoke.

### [] T6.3 — Sepolia deploy aur record

**Owner:** Middleware.

**BLOCKED:** funded Sepolia deployer key + RPC URL chahiye. Milne tak task `[]` rakho.

**Kya karna hai**
1. **BLOCKER:** human se funded Sepolia deployer key + RPC URL lo.
2. `npm --prefix middleware run deploy:sepolia` chalao; address + tx link
   `docs/deployments.md` me likho.
3. Middleware `.env` me Sepolia address daal ke `GET /escrow/status` check karo.
4. Key kabhi commit/log me na aaye.

**Files:** `docs/deployments.md`, `middleware/.env` (local only).
**Done criteria:** Sepolia address + block explorer link documented; status call kaam kare.
**Verify:** `curl localhost:8090/escrow/status/<orderId>`.

### Commit batch C6 — T6.1, T6.2, T6.3

**Message:** `feat(chain): add deploy artifacts, local smoke and sepolia docs`

---

## Phase 7 — Frontend real flows — [0/6]

**Owner:** Frontend. Context packs: `docs/context/C7A.md` (T7.1–T7.3), `docs/context/C7B.md` (T7.4–T7.6).

### [] T7.1 — Map par parcel aur ALU layers

**Owner:** Frontend. Context pack: `docs/context/C7A.md`.

**Kya karna hai**
1. `frontend/src/lib/api.ts` me typed `fetchParcel`, `fetchAlus`, `fetchListings` add karo.
2. MapLibre me sources/layers: parcel fill + outline, ALU grid lines, selected parcel highlight.
3. Zoom level → ALU level mapping (10+ → 1km, 14+ → 100m, 17+ → 10m, 20+ → 1m).
4. Demo ULPIN `DEMO-ULPIN-001` auto-load; click par popup me ULPIN/ALU ID.
5. Loading/error/empty states.

**Files:** `frontend/src/lib/api.ts`, `frontend/src/components/MapView.tsx`,
`frontend/src/App.tsx`, `frontend/src/index.css`.
**Done criteria:** Demo parcel aur ALUs map par dikhte hain; typecheck/build pass.
**Verify:** `npm --prefix frontend run typecheck && npm --prefix frontend run build`.

### [] T7.2 — Officer evidence + review UI

**Owner:** Frontend. Context pack: `docs/context/C7A.md`.

**Kya karna hai**
1. ULPIN submit par evidence response ko table me dikhao: 21 fields, status chips
   (`AVAILABLE/PARTIAL/N/A/N/D`), source links, run ID, evidence hash.
2. Review queue list + Approve/Reject buttons with reason input.
3. Hash ko copy button ke saath dikhao; sources clickable hon.
4. Error states: middleware down, missing key, no evidence.

**Files:** `frontend/src/components/EvidencePanel.tsx`, `frontend/src/components/ReviewQueue.tsx`,
`frontend/src/lib/api.ts`, `frontend/src/App.tsx`, `frontend/src/index.css`.
**Done criteria:** Officer demo flow UI se chalta hai.
**Verify:** manual + build.

### [] T7.3 — Citizen wallet connect + chain switch

**Owner:** Frontend. Context pack: `docs/context/C7A.md`.

**Kya karna hai**
1. `frontend/src/lib/wallet.ts`: `window.ethereum` connect, chain switch/add (local 31337),
   account change listener; wallet na ho to clear message.
2. Shortened address + disconnect/reset UI.
3. No buy transaction yet; buy is `T7.4`.

**Files:** `frontend/src/lib/wallet.ts`, `frontend/src/App.tsx`, `frontend/src/index.css`.
**Done criteria:** Wallet connect/disconnect aur chain switch kaam karta hai.
**Verify:** manual in browser + build.

### Commit batch C7A — T7.1, T7.2, T7.3

**Message:** `feat(web): add map layers, evidence review and wallet connect`

### [] T7.4 — Listing browse + buy flow

**Owner:** Frontend. Context pack: `docs/context/C7B.md`.

**Kya karna hai**
1. `frontend/src/components/ListingCard.tsx`: bundle, ULPIN, price, seller KYC badge, ALU count.
2. Buy sequence exactly:
   `POST /orders` → `ethers.id("landmarket-order:" + id)` → `createOrder(...)` with value →
   wait receipt → `POST /orders/{id}/funded` → `POST /orders/{id}/evaluate` → poll `GET /orders/{id}`.
3. Disable button while pending; wrong chain par switch prompt.

**Files:** `frontend/src/components/ListingCard.tsx`, `frontend/src/lib/api.ts`,
`frontend/src/lib/wallet.ts`, `frontend/src/App.tsx`, `frontend/src/index.css`.
**Done criteria:** Local chain par end-to-end buy ho jaata hai.
**Verify:** manual demo on local chain + build.

### [] T7.5 — Trade status panel

**Owner:** Frontend. Context pack: `docs/context/C7B.md`.

**Kya karna hai**
1. `frontend/src/components/TradeStatus.tsx`: six check rows (pass/fail/reason/blocking),
   decision, order state, chain state, tx hash, explorer link.
2. `NEEDS_REVIEW` par "officer review" dikhao, settle claim mat karo.
3. Refresh button + clear timeout message.

**Files:** `frontend/src/components/TradeStatus.tsx`, `frontend/src/App.tsx`, `frontend/src/index.css`.
**Done criteria:** Status panel contract ke saare fields dikhata hai.
**Verify:** manual + build.

### [] T7.6 — Empty/error states, banner and responsive polish

**Owner:** Frontend. Context pack: `docs/context/C7B.md`.

**Kya karna hai**
1. Loading/empty/error for map, listings, reviews, trade.
2. Accessible labels, focus-visible styles, disabled buttons, `aria-live` status.
3. Visible banner: `Testnet only, not a legal title transfer.`
4. Demo badge `DEMO_FIXTURE_NOT_OFFICIAL`; responsive at 375px and 1280px.
5. Vite chunk warning fix ya document karo.

**Files:** `frontend/src/**`, `frontend/README.md`, `frontend/log-f.md`.
**Done criteria:** No horizontal scroll; states covered; banner visible.
**Verify:** manual + `npm --prefix frontend run build`.

### Commit batch C7B — T7.4, T7.5, T7.6

**Message:** `feat(web): add wallet buy flow, trade status and demo polish`

---

## Phase 8 — E2E, demo aur hardening — [0/3]

**Owner split:** `T8.1` backend; `T8.2` lead; `T8.3-B/M/F` backend/middleware/frontend; `T8.3-D` lead. Context pack: `docs/context/C8.md`.


### [] T8.2 — One-command demo runner

**Owner:** Lead / shared branch. Interns do not do this task.

**Kya karna hai**
1. `scripts/demo.sh`: DB up, seed, API + middleware + frontend background start, chain deploy,
   URLs print, Ctrl+C par cleanup.
2. `docs/demo-script.md`: 7-step demo, expected output, fallback agar TinyFish key na ho.
3. `docs/submission-checklist.md`: repo, video, screenshots, contract address, TinyFish proof.

**Files:** `scripts/demo.sh`, `docs/demo-script.md`, `docs/submission-checklist.md`, `Makefile`.
**Done criteria:** Fresh terminal se `make demo` chal ke URL deta hai.
**Verify:** `make demo`.

### [] T8.3-B — Backend security/quality gate (backend slice)

**Owner:** Backend.

1. Input validation, CORS, error leakage on backend routes.
2. `ruff`, `pytest`, `pytest -m integration`.
3. Backend part of `docs/limitations.md` (demo data, KYC stub, testnet only).
**Verify:** `backend/.venv/bin/ruff check backend && backend/.venv/bin/pytest -q backend`.

### [] T8.3-M — Middleware security/quality gate (middleware slice)

**Owner:** Middleware.

1. Secrets grep (`TINYFISH_API_KEY`, `OPERATOR_PRIVATE_KEY`, private keys).
2. `npm --prefix middleware run typecheck && npm --prefix middleware test && npm --prefix middleware run compile`.
3. `npm --prefix middleware audit --omit=dev`.
**Verify:** all four commands pass; `.env` ignored.

### [] T8.3-F — Frontend security/quality gate (frontend slice)

**Owner:** Frontend.

1. `npm --prefix frontend run typecheck`, `build`, `audit --omit=dev`.
2. Accessibility basics, focus states, disabled buttons.
3. Chunk warning fix or documented.
**Verify:** `npm --prefix frontend run build`.

### [] T8.3-D — Final docs and architecture (lead slice)

**Owner:** Lead.

1. README/SETUP final commands; `docs/architecture.md`, `docs/limitations.md`.
2. Verify the 7-step demo + submission checklist.
**Verify:** `make check` (after `T8.2`).

### Commit batch C8 — T8.1, T8.2, T8.3-B, T8.3-M, T8.3-F, T8.3-D

**Message:** `test: add integration suite, demo runner and hardening`

---

## Phase 9 — Stretch (sirf time bache to) — [0/3]

**Owner split:** `T9.1` backend; `T9.2` AI; `T9.3-B/M/F` backend/middleware/frontend; `T9.3-D` lead. Context pack: `docs/context/C9.md`.

### [] T9.1 — ALU hierarchy, lock aur double-sell protection

**Kya karna hai:** Generated ALUs ko select par persist karo; parent chain maintain karo;
active listing ke liye per-ALU unique index; sold ALUs lock; partial bundle sale rules document karo.
**Files:** `backend/db/008_alu_locks.sql`, `backend/app/services/alu_grid.py`,
`backend/app/api/routes/alus.py`, `backend/tests/test_alu_locks.py`.
**Done criteria:** Ek ALU do active listings me nahi aa sakta.

### [] T9.2 — Multi-portal evidence + confidence

**Owner:** AI branch. Do not edit backend directly; contract changes go through the lead.

**Kya karna hai:** 7 portal registry, per-portal TinyFish run, field-level merge,
source conflict par `NEEDS_REVIEW`, confidence score evidence sheet me.

**Files:** `middleware/src/tinyfish/portals.ts`, `middleware/src/tinyfish/merge.ts`,
AI tests; backend contract change only via lead.
**Done criteria:** Kam se kam 2 portals ka merged sheet + conflicts review me jaate hain.

### [] T9.3-B — Backend production container (backend slice)

**Owner:** Backend. `backend/Dockerfile`.

### [] T9.3-M — Middleware production container (middleware slice)

**Owner:** Middleware. `middleware/Dockerfile`.

### [] T9.3-F — Frontend production container (frontend slice)

**Owner:** Frontend. `frontend/Dockerfile`.

### [] T9.3-D — Public demo deployment (lead slice)

**Owner:** Lead.

**Kya karna hai:** `docker-compose.prod.yml`, public tunnel (Cloudflare Tunnel ya similar),
env secrets host par, demo URL + health checks.
**Files:** `docker-compose.prod.yml`, `docs/deployment.md`.
**Done criteria:** Public URL se demo chalta hai, secrets repo me nahi.

### Commit batch C9 — T9.1, T9.2, T9.3-B, T9.3-M, T9.3-F, T9.3-D

**Message:** `feat: add alu locking, multi-portal evidence and deployment`

---

## Blockers / human decisions

| # | Kya chahiye | Kis task par block | Kaise unblock |
|---|---|---|---|
| B1 | `TINYFISH_API_KEY` | T3.1, live demo | Human key de; tab tak mock tests se aage badho |
| B2 | Sepolia RPC + funded deployer key | T6.3 | Human funded test wallet de |
| B3 | ALU trading policy (kaunsa level tradeable) | T2.3 / T9.1 | Default: demo me `10m` ALUs tradeable; document me confirm |
| B4 | Officer auth (real login?) | T3.3 / T4.1 | Prototype me `X-Officer-Token` env stub |

## Prototype boundaries (repeat, yaad rakho)

- Government records demo ho sakte hain, official claim nahi.
- Blockchain testnet practice hai, real money nahi.
- Platform record official title/deed update nahi karta; legal conveyance out of scope.
- KYC/OTP prototype stub hai, real identity verification nahi.
- TinyFish evidence collect karta hai; trade decision backend ke fixed rules leta hai.
