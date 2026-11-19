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
Progress: **38 / 44 tasks done (86%)** (C0 gate not counted) (`C0` is a gate, not counted in the 35).
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
4. Task done karte hi heading `### [.] T1.1 — ...` ko `### [.] T1.1 — ...` karo, block ko `YEH SAB HO GYA` me move karo, aur `**Done:** YYYY-MM-DD HH:MM IST — Session N` line add karo. **Phase counter aur top progress line lead update karta hai** — intern unhe mat chhedo.
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

## Phase 6 — Blockchain deployment — [3/4]

### [.] T6.1-F — ABI + chain config (frontend slice)

**Done:** 2026-11-02 12:15 IST — Session 1

**Kya hua:** `frontend/src/lib/escrowAbi.json` banao Hardhat artifact se ABI copy kiya; `frontend/src/lib/chain.ts` me `VITE_ESCROW_ADDRESS`, `VITE_CHAIN_ID`, `VITE_CHAIN_NAME`, `VITE_EXPLORER_URL` padhne ka config banaya; missing address par UI warning dikhta hai, crash nahi hota; `frontend/.env.example` update kiya.

**Kya karta hai:** Frontend ab escrow contract address aur ABI use kar sakta hai; chain config centrally manage hoti hai.

**Files:** `frontend/src/lib/escrowAbi.json`, `frontend/src/lib/chain.ts`, `frontend/.env.example`, `frontend/src/App.tsx` (warning banner), `frontend/src/index.css` (banner style).

**Verify:** `npm --prefix frontend run typecheck && npm --prefix frontend run build` pass.

## Phase 7 — Frontend real flows — [6/6]

### [.] T7.1 — Map par parcel aur ALU layers

**Done:** 2026-11-02 14:30 IST — Session 1

**Kya hua:** `frontend/src/lib/api.ts` me typed `fetchParcel`, `fetchAlus`, `fetchListings` add kiye; `MapView.tsx` rewrite kiya MapLibre sources/layers ke saath (parcel fill + outline, ALU grid lines); zoom → ALU level mapping (>=20 → 1m, >=17 → 10m, >=14 → 100m, >=10 → 1km); `DEMO-ULPIN-001` auto-load; click popup me ULPIN/ALU ID; loading/error states; saare source/layer IDs `lm-` prefix se.

**Kya karta hai:** Demo parcel aur ALUs map par render hote hain; ALU layer zoom ke saath badalti hai.

**Files:** `frontend/src/lib/api.ts`, `frontend/src/components/MapView.tsx`, `frontend/src/index.css` (map loading/error styles).

**Verify:** `npm --prefix frontend run typecheck && npm --prefix frontend run build` pass.

### [.] T7.2 — Officer evidence + review UI

**Done:** 2026-11-02 15:45 IST — Session 1

**Kya hua:** `EvidencePanel.tsx` banaya - 21-field evidence table, status chips (AVAILABLE/PARTIAL/N/A/N/D), source links, run ID, evidence hash with copy button. `ReviewQueue.tsx` banaya - pending review list, Approve/Reject buttons with reason input, X-Officer-Token header. `api.ts` me evidence/review types aur functions add kiye. Error states: middleware down, missing key, no evidence.

**Kya karta hai:** Officer demo flow UI se chalta hai - evidence submit, review, approve/reject.

**Files:** `frontend/src/components/EvidencePanel.tsx`, `frontend/src/components/ReviewQueue.tsx`, `frontend/src/lib/api.ts`, `frontend/src/App.tsx`, `frontend/src/index.css`.

**Verify:** typecheck aur build pass.

### [.] T7.3 — Citizen wallet connect + chain switch

**Done:** 2026-11-02 17:30 IST — Session 1

**Kya hua:** `frontend/src/lib/wallet.ts` banaya - `connectWallet()`, `switchToConfiguredChain()`, `onAccountsChanged()`. `window.ethereum` connect, chain switch/add (local 31337), account change listener. No wallet par clear message. Shortened address + disconnect/reset UI. `WalletPill` component in `App.tsx` me integrate kiya.

**Kya karta hai:** Wallet connect/disconnect aur chain switch kaam karta hai.

**Files:** `frontend/src/lib/wallet.ts`, `frontend/src/App.tsx`, `frontend/src/index.css`.

**Verify:** `npm --prefix frontend run typecheck && npm --prefix frontend run build` pass.

### [.] T7.4 — Listing browse + buy flow

**Done:** 2026-11-05 17:22 IST — Session 11

**Kya hua:** `ethers` ^6.13 add kiya `frontend/package.json` me aur install kiya; `frontend/src/lib/web3.ts` banaya (`chainOrderId` via `ethers.id`, `getSigner`, `createOrder` contract call); `api.ts` me Order/OrderState/TradeDecision/CheckResult types + `createOrderApi`, `fundOrderApi`, `evaluateOrderApi`, `fetchOrderApi` add kiye; `ListingCard.tsx` banaya (bundle, ULPIN, price, seller KYC badge, ALU count, Buy); `TradeStatus.tsx` banaya (6 check rows, decision, chain state, tx hash, explorer link, `NEEDS_REVIEW` officer message, refresh + timeout); `App.tsx` me listings browse + buy flow + trade status wiring + demo banner; `index.css` styles add kiye.

**Kya karta hai:** Listings browse karke citizen local chain par buy flow shuru kar sakta hai; order create → createOrder → funded → evaluate → poll tak track hota hai.

**Files:** `frontend/src/components/ListingCard.tsx`, `frontend/src/components/TradeStatus.tsx`, `frontend/src/lib/api.ts`, `frontend/src/lib/web3.ts`, `frontend/src/App.tsx`, `frontend/src/index.css`, `frontend/package.json`.

**Verify:** `npm --prefix frontend run typecheck && npm --prefix frontend run build` pass.

### [.] T7.5 — Trade status panel

**Done:** 2026-11-05 17:22 IST — Session 11

**Kya hua:** `frontend/src/components/TradeStatus.tsx` banaya — cheh check rows (pass/fail/reason/blocking), decision, order state, chain state, tx hash, explorer link. `NEEDS_REVIEW` par "officer review" dikhta hai, settle claim nahi. Refresh button + clear timeout message. `App.tsx` me wire kiya.

**Kya karta hai:** Trade status panel contract ke saare fields dikhata hai.

**Files:** `frontend/src/components/TradeStatus.tsx`, `frontend/src/App.tsx`, `frontend/src/index.css`.

**Verify:** typecheck aur build pass.

### [.] T7.6 — Empty/error states, banner and responsive polish

**Done:** 2026-11-05 17:22 IST — Session 11

**Kya hua:** Loading/empty/error states map, listings, reviews, trade ke liye hain. Accessible labels, focus-visible outline, disabled buttons, `aria-live` status. Demo banner `Testnet only, not a legal title transfer.` visible. `DEMO_FIXTURE_NOT_OFFICIAL` badge listings par. Responsive 375px media query. Vite chunk-size warning pre-existing, documented in T7.6/T8.3-F scope.

**Kya karta hai:** UI polished, koi horizontal scroll nahi, states covered, banner visible.

**Files:** `frontend/src/**`, `frontend/README.md`, `frontend/log-f.md`.

**Verify:** manual + `npm --prefix frontend run build`.

### [.] T8.3-F — Frontend security/quality gate (frontend slice)

**Done:** 2026-11-05 20:38 IST — Session 12

**Kya hua:** `npm --prefix frontend run typecheck`, `build`, `audit --omit=dev` sab pass (0 vulnerabilities). Accessibility basics: `focus-visible` outline on interactive elements, disabled buttons while pending, `aria-live` status regions, accessible labels. Bundle chunk warning documented in `frontend/README.md`. `README.md` updated with final frontend commands (dev, typecheck, build, preview, audit).

**Kya karta hai:** Frontend quality gate saaf hua; build pass.

**Files:** `frontend/src/index.css`, `frontend/README.md`, `frontend/src/App.tsx`, `frontend/src/components/ListingCard.tsx`, `frontend/src/components/TradeStatus.tsx`.

**Verify:** `npm --prefix frontend run build`.

### [.] T9.3-F — Frontend production container (frontend slice)

**Done:** 2026-11-05 20:38 IST — Session 12

**Kya hua:** `frontend/Dockerfile` banaya — node:24-alpine builder stage (`npm ci` + `npm run build`) aur nginx:alpine serve stage (`/usr/share/nginx/html`, port 80). Public demo env/API base check document kiya `README.md` me (`VITE_API_BASE_URL`, `VITE_ESCROW_ADDRESS`, etc.).

**Kya karta hai:** Frontend static build ko production container me serve kiya ja sakta hai.

**Files:** `frontend/Dockerfile`, `frontend/README.md`.

**Verify:** Dockerfile present; `npm --prefix frontend run build` uses documented commands.

## Repo hygiene — 2026-10-29 22:11 IST

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

## Phase 1 — Data foundation — [3/3]

**Owner:** Backend. Context pack: `docs/context/C1.md`.

### [.] T1.1 — PostGIS boot karke schema verify karo

**Kya karna hai**
1. `docker compose up -d postgis` chalao; container healthy hone tak wait karo.
2. `docker compose exec -T postgis psql -U landmarket -d landmarket -c "\dt"` se 6 tables confirm karo.
3. `backend/scripts/check_db.py` banao — PostGIS version, 6 table names, row counts print kare;
   DB na mile to exit code 1 de.
4. Root `Makefile` banao: `db-up`, `db-check`, `db-reset` (volume delete se pehle `yes` prompt),
   `seed` (T1.3 ke baad kaam karega), `api`, `mid`, `web`, `check`.
5. `SETUP.md` me Makefile commands add karo.

**Files:** `backend/scripts/check_db.py`, `Makefile`, `SETUP.md`.
**Done criteria:** `make db-check` PostGIS version + 6 tables dikhata hai; DB band ho to non-zero exit.
**Verify:** `make db-up && make db-check`.

### [.] T1.2 — Database access layer banao

**Kya karna hai**
1. `backend/app/core/db.py` me `@contextmanager db_connection()` banao: `psycopg.connect`,
   `row_factory=dict_row`, `connect_timeout=5`, commit/rollback/close.
2. `backend/app/repositories/base.py` me `fetch_one`, `fetch_all`, `execute` helpers banao.
3. Health probe ko isi layer se chalao; routes me direct `psycopg.connect` na ho.
4. Unit test: galat `DATABASE_URL` par `check_database()` `unavailable` return kare, raise na kare.

**Files:** `backend/app/core/db.py`, `backend/app/repositories/base.py`,
`backend/tests/test_db.py`.
**Done criteria:** `rg "psycopg.connect" backend/app` sirf `core/db.py` me mile; ruff/pytest pass.
**Verify:** `backend/.venv/bin/ruff check backend && backend/.venv/bin/pytest -q backend`.

### [.] T1.3 — Demo parcel, ALU aur bundle ke liye seed data

**Kya karna hai**
1. `backend/db/002_seed_demo.sql` banao. Sab kuch clearly demo ho:
   - parcel `DEMO-ULPIN-001`, Kothrud ke paas chhota polygon, `geometry_source='DEMO_FIXTURE_NOT_OFFICIAL'`,
     attributes me `owner_name`, `district`, `zoning`.
   - 1 parent ALU (`100m`) + 4 child ALUs (`10m`), deterministic IDs, parent links.
   - `parcel_alus` me charo `CONTAINS` link.
2. `backend/scripts/seed.py` banao: SQL file execute kare, dobara chalane par duplicate na banaye
   (demo rows pehle delete kare, phir insert).
3. `Makefile` ka `seed` target is script ko chalao.
4. `SETUP.md` me demo ULPIN note karo.

**Files:** `backend/db/002_seed_demo.sql`, `backend/scripts/seed.py`, `Makefile`, `SETUP.md`.
**Done criteria:** `make seed` ke baad `DEMO-ULPIN-001`, 5 ALUs aur 4 parcel_alus rows hon.
**Verify:** `make db-check && make seed && make db-check`.

### Commit batch C1 — T1.1, T1.2, T1.3

**Message:** `feat(db): add postgis checks, db helpers and demo seed`

---

## Phase 2 — Parcel, ALU aur bundle API — [3/3]

**Owner:** Backend. Context pack: `docs/context/C2.md`.

### [.] T2.1 — Parcel read API

**Kya karna hai**
1. `backend/app/repositories/parcels.py` banao: ULPIN se parcel, bbox se parcels (PostGIS `ST_AsGeoJSON`,
   `ST_MakeEnvelope(...,4326)`, `ST_Intersects`).
2. `backend/app/api/routes/parcels.py`:
   - `GET /api/v1/parcels/{ulpin}` → GeoJSON Feature + attributes + `geometry_status`; missing par 404.
   - `GET /api/v1/parcels?bbox=minLon,minLat,maxLon,maxLat&limit=100` → FeatureCollection; limit max 100.
3. `app/api/main.py` me router register karo.
4. Tests: invalid bbox 422, missing ULPIN 404, limit >100 clamp/reject.

**Files:** `backend/app/repositories/parcels.py`, `backend/app/api/routes/parcels.py`,
`backend/app/api/main.py`, `backend/tests/test_parcels.py`.
**Done criteria:** `GET /api/v1/parcels/DEMO-ULPIN-001` demo polygon laut-ta hai.
**Verify:** `curl -s localhost:8000/api/v1/parcels/DEMO-ULPIN-001 | head`.

### [.] T2.2 — Deterministic ALU grid endpoint

**Kya karna hai**
1. `backend/app/services/alu_grid.py` banao. Levels: `1km`=1000m, `100m`, `10m`, `1m`,
   `0.1m2`=0.1m × 1m. Web Mercator meters me cell index nikalo, wapas lon/lat me convert karo.
2. ID format: `ALU-{level}-{ix}-{iy}`; parent ID next coarser level ke same formula se.
3. `GET /api/v1/alus?bbox=...&level=10m` → GeoJSON FeatureCollection, har feature me
   `alu_id`, `parent_id`, `level`. Max 1500 cells; zyada ho to 422 "zoom in" error.
4. Tests: same input par same ID, parent-child relation sahi, cap enforce.

**Files:** `backend/app/services/alu_grid.py`, `backend/app/api/routes/alus.py`,
`backend/app/api/main.py`, `backend/tests/test_alu_grid.py`.
**Done criteria:** Endpoint deterministic output deta hai; 1500 se zyada par 422.
**Verify:** `pytest -q backend/tests/test_alu_grid.py`.

### [.] T2.3 — Bundle schema aur API

**Kya karna hai**
1. `backend/db/003_bundles.sql`: `bundles` (id, ulpin FK, name, status `DRAFT/ACTIVE/PAUSED/ARCHIVED`,
   created_by, timestamps) aur `bundle_alus` (bundle_id, alu_id, PK).
2. Routes: `POST /api/v1/bundles` `{ulpin,name,alu_ids,created_by}`; `GET /api/v1/bundles/{id}`;
   `PATCH /api/v1/bundles/{id}` `{status}`.
3. Validation: saare ALU exist karein aur usi parcel se linked hon; duplicate ALU reject.
4. Tests: happy path, cross-parcel ALU reject, duplicate reject, invalid status transition.

**Files:** `backend/db/003_bundles.sql`, `backend/app/repositories/bundles.py`,
`backend/app/api/routes/bundles.py`, `backend/app/api/main.py`, `backend/tests/test_bundles.py`.
**Done criteria:** Demo parcel ke 4 ALUs ka ACTIVE bundle ban jaata hai.
**Verify:** `make db-reset && make seed` phir bundle POST.

### Commit batch C2 — T2.1, T2.2, T2.3

**Message:** `feat(api): expose parcels, alu grid and bundles`

---

## Phase 3 — TinyFish evidence pipeline — [2/3]

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

### [.] T3.2 — Evidence validate, hash aur DB me save karo

**Kya karna hai**
1. `backend/app/services/evidence.py`: 21 fields ki list, missing fields ko `N/D` banao,
   canonical JSON (sorted keys) ka SHA-256 hash nikalo.
2. `POST /api/v1/verifications` update karo: middleware response validate karke
   `evidence_sheets` me save kare; response me `evidence_id`, `evidence_hash`, `status`,
   `fields`, `sources`, `tinyfish_run_id` de.
3. `GET /api/v1/evidence/{id}` aur `GET /api/v1/evidence?ulpin=...` add karo.
4. Middleware down ho to 503, invalid sheet ho to 422; raw data kabhi invent na karo.
5. Tests: mocked middleware response se persistence + hash determinism.

**Files:** `backend/app/services/evidence.py`, `backend/app/repositories/evidence.py`,
`backend/app/api/routes/verifications.py`, `backend/app/api/routes/evidence.py`,
`backend/app/api/main.py`, `backend/tests/test_evidence.py`.
**Done criteria:** Ek verification ke baad DB row + stable hash; GET se same sheet mile.
**Verify:** `pytest -q backend/tests/test_evidence.py`.

### [.] T3.3 — Officer review queue

**Kya karna hai**
1. `backend/db/004_review.sql`: `evidence_sheets` me `review_reason TEXT`, `reviewed_at TIMESTAMPTZ`.
2. Routes: `GET /api/v1/reviews?status=PENDING` (evidence + parcel summary),
   `POST /api/v1/reviews/{id}/decision` `{decision: APPROVE|REJECT, reason, officer}`.
3. Transitions: `PENDING/NEEDS_REVIEW` → `CLEAN` ya `REJECTED`; dobara decision par 409.
4. `reviewed_by`, `review_reason`, `reviewed_at` save karo. Auth abhi officer string hai —
   JWT T4.1 me aayega, code me TODO note karo.
5. Tests: valid transitions, invalid transition 409, reason required on reject.

**Files:** `backend/db/004_review.sql`, `backend/app/api/routes/reviews.py`,
`backend/app/repositories/evidence.py`, `backend/app/api/main.py`, `backend/tests/test_reviews.py`.
**Done criteria:** Officer pending evidence approve/reject kar sakta hai; audit fields bharte hain.
**Verify:** `pytest -q backend/tests/test_reviews.py`.

### Commit batch C3 — T3.1, T3.2, T3.3

**Message:** `feat(evidence): add tinyfish proof, persistence and review queue`

---

## Phase 4 — Identity, listing aur order — [3/3]

**Owner:** Backend. Context pack: `docs/context/C4.md`.

### [.] T4.1 — Wallet user aur KYC stub

**Kya karna hai**
1. `backend/db/005_users.sql`: `users` (id, wallet_address unique, role `CITIZEN/OFFICER`,
   kyc_status `PENDING/VERIFIED/REJECTED`, created_at, updated_at).
2. Routes: `POST /api/v1/users` upsert wallet, `GET /api/v1/users/{wallet}`,
   `POST /api/v1/users/{wallet}/kyc` `{status, reason}`.
3. KYC endpoint ko `X-Officer-Token` header chahiye; value `.env` ke `DEV_OFFICER_TOKEN` se match kare.
   Ye prototype stub hai — document me clearly likho.
4. Wallet format validate karo (`0x` + 40 hex).
5. Tests: invalid wallet 422, missing token 401, KYC update 200.

**Files:** `backend/db/005_users.sql`, `backend/app/api/routes/users.py`,
`backend/app/repositories/users.py`, `backend/app/api/main.py`, `backend/.env.example`,
`backend/tests/test_users.py`.
**Done criteria:** Demo buyer/seller KYC VERIFIED ho jaate hain.
**Verify:** `pytest -q backend/tests/test_users.py`.

### [.] T4.2 — Listing create/browse/pause

**Kya karna hai**
1. `backend/db/006_listings_bundle.sql`: `listings` me `bundle_id BIGINT REFERENCES bundles(id)`;
   `alu_id` nullable rakho.
2. Routes: `POST /api/v1/listings` `{bundle_id, seller_wallet, price_wei}`; `GET /api/v1/listings?status=LISTED`;
   `PATCH /api/v1/listings/{id}` `{status}`.
3. Rules: seller KYC VERIFIED, bundle ACTIVE, price > 0, ek bundle par ek active listing.
4. Transitions: `DRAFT→LISTED→PAUSED/CANCELLED`, `PAUSED→LISTED`.
5. Tests: unverified seller reject, duplicate active listing reject, happy path.

**Files:** `backend/db/006_listings_bundle.sql`, `backend/app/api/routes/listings.py`,
`backend/app/repositories/listings.py`, `backend/app/api/main.py`, `backend/tests/test_listings.py`.
**Done criteria:** Demo bundle LISTED ho jaata hai.
**Verify:** `pytest -q backend/tests/test_listings.py`.

### [.] T4.3 — Order lifecycle

**Kya karna hai**
1. Routes: `POST /api/v1/orders` `{listing_id, buyer_wallet}`; `POST /api/v1/orders/{id}/funded`
   `{chain_order_id, tx_hash}`; `GET /api/v1/orders/{id}`.
2. Rules: buyer KYC VERIFIED, listing LISTED, buyer ≠ seller, price listing se match kare.
   Order `CREATED` par bane; funding proof aane par `FUNDED`.
3. `chain_order_id` 32-byte hex aur `tx_hash` 32-byte hex validate karo; duplicate funding 409.
4. Tests: self-buy reject, wrong price reject, double funded reject, happy path.

**Files:** `backend/app/api/routes/orders.py`, `backend/app/repositories/orders.py`,
`backend/app/api/main.py`, `backend/tests/test_orders.py`.
**Done criteria:** CREATED → FUNDED order DB me record hota hai.
**Verify:** `pytest -q backend/tests/test_orders.py`.

### Commit batch C4 — T4.1, T4.2, T4.3

**Message:** `feat(market): add wallet identity, listings and orders`

---

## Phase 5 — 6 checks aur settlement — [3/3]

**Owner split:** `T5.1`, `T5.2`, `T5.3-B` backend; `T5.3-M` middleware. Context pack: `docs/context/C5.md`.

### [.] T5.1 — 6 checks ka pure rule engine

**Kya karna hai**
1. `backend/app/services/checks.py` me har check alag pure function ho, output
   `CheckResult(name, passed, reason, blocking)`.
2. Checks exactly ye 6:
   - `LISTED` — listing status `LISTED` aur order usi listing ka ho.
   - `BUNDLE_INTACT` — bundle `ACTIVE`, saare ALU maujood, koi ALU kisi doosre active order me na ho.
   - `KYC_WALLET` — buyer aur seller dono `VERIFIED`.
   - `ZONING_OK` — evidence me `land_use_zoning` available/partial ho aur restricted/agricultural na ho.
   - `FUNDS_IN_ESCROW` — order `FUNDED` aur chain state `Funded (1)` ho.
   - `TRADE_MATCH` — listing, bundle, parcel ULPIN, evidence ULPIN aur buyer/seller match karein.
3. Rule policy `docs/checks.md` me likho; demo assumptions clearly mark karo.
4. Unit tests: har check ka pass aur fail case (kam se kam 12 tests).

**Files:** `backend/app/services/checks.py`, `docs/checks.md`, `backend/tests/test_checks.py`.
**Done criteria:** 6 checks isolated test ho jaate hain, DB ke bina.
**Verify:** `pytest -q backend/tests/test_checks.py`.

### [.] T5.2 — Evaluate endpoint aur decision policy

**Kya karna hai**
1. `backend/db/007_order_checks.sql`: orders me `checks JSONB`, `decision TEXT`,
   `decided_at TIMESTAMPTZ`; decision `APPROVED/NEEDS_REVIEW/REJECTED`.
2. `POST /api/v1/orders/{id}/evaluate`: context load karo, 6 checks chalao, result persist karo.
3. Decision: sab pass → `APPROVED`; blocking fail → `REJECTED`; sirf missing/N/D evidence →
   `NEEDS_REVIEW`. Exact mapping `docs/checks.md` me.
4. `GET /api/v1/orders/{id}` response me per-check result + decision de.
5. Tests: approve, reject, review scenarios.

**Files:** `backend/db/007_order_checks.sql`, `backend/app/api/routes/orders.py`,
`backend/app/services/checks.py`, `docs/checks.md`, `backend/tests/test_evaluate.py`.
**Done criteria:** Ek order evaluate hoke decision DB me save hota hai.
**Verify:** `pytest -q backend/tests/test_evaluate.py`.

### [.] T5.3-M — Middleware escrow status endpoint (middleware slice)

**Owner:** Middleware. Do this before backend `T5.3-B` if possible; backend can mock it.

**Kya karna hai**
1. `middleware/src/server.ts` me `GET /escrow/status/:orderId` add karo — contract
   `orderState` padhe (0 None, 1 Funded, 2 Settled, 3 Refunded).
2. Invalid order ID par 400, chain error par 502.
3. Response exactly `{orderId, state, label}` per `docs/api-contract.md` §4.

**Files:** `middleware/src/server.ts`, `middleware/src/blockchain/escrow.ts`, middleware tests.
**Done criteria:** `curl localhost:8090/escrow/status/<orderId>` sahi state deta hai.
**Verify:** local chain + `curl`.

### [.] T5.3-B — Backend settle/refund wiring (backend slice)

**Owner:** Backend. May mock `T5.3-M` until it is merged.

**Kya karna hai**
1. `backend/app/services/settlement.py`: `APPROVED` → settle, `REJECTED` → refund,
   `NEEDS_REVIEW` → kuch nahi. Calls middleware par jaayein.
2. Success par order state `SETTLED/REFUNDED`, `tx_hash` save; dobara call idempotent ho (409/200).
3. Middleware/chain fail par order state na badle; error 502.
4. Tests: mocked middleware se approve/reject/idempotency; manual local chain test.

**Files:** `backend/app/services/settlement.py`, `backend/app/api/routes/orders.py`,
`backend/tests/test_settlement.py`.
**Done criteria:** Evaluate ke baad settle/refund call hota hai aur tx hash DB me aata hai.
**Verify:** `pytest -q backend/tests/test_settlement.py`, phir local chain par manual.

### Commit batch C5 — T5.1, T5.2, T5.3-M, T5.3-B

**Message:** `feat(trade): implement six checks and escrow settlement`

---

## Phase 6 — Blockchain deployment — [3/4]

**Owner split:** `T6.1-M`, `T6.2`, `T6.3` middleware; `T6.1-F` frontend. Context pack: `docs/context/C6.md`.

### [.] T6.1-M — Deploy artifacts (middleware slice)

**Owner:** Middleware.

1. `middleware/scripts/deploy.ts` deploy ke baad `middleware/deployments/<network>.json` likhe:
   address, chainId, deployer, operator, deployedAt.
2. Commit a small `deployments/localhost.json` example (no key), or document generation.
3. Addresses docs me commit karo; `.env` kabhi nahi.

**Files:** `middleware/scripts/deploy.ts`, `middleware/deployments/`.
**Done criteria:** Local deploy ke baad address file ready.
**Verify:** `npm --prefix middleware run deploy:local`.

### [.] T6.2 — Local chain smoke test

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

## Phase 7 — Frontend real flows — [6/6]

**Owner:** Frontend. Context packs: `docs/context/C7A.md` (T7.1–T7.3), `docs/context/C7B.md` (T7.4–T7.6).

### Commit batch C7B — T7.4, T7.5, T7.6

**Message:** `feat(web): add wallet buy flow, trade status and demo polish`

---

## Phase 8 — E2E, demo aur hardening — [4/6]

**Owner split:** `T8.1` backend; `T8.2` lead; `T8.3-B/M/F` backend/middleware/frontend; `T8.3-D` lead. Context pack: `docs/context/C8.md`.

### [.] T8.1 — Real PostGIS integration tests

**Owner:** Backend. Context pack: `docs/context/C8.md`.

**Kya karna hai**
1. `backend/tests/conftest.py`: `TEST_DATABASE_URL` se connection, schema apply, per-test rollback.
2. Integration tests: parcel bbox, ALU grid, bundle validation, listing/order transitions,
   evaluate decision, evidence persistence.
3. Marker `@pytest.mark.integration`; default `pytest` fast rahe, integration alag command se chale.
4. `Makefile` me `test-integration` target.

**Files:** `backend/tests/conftest.py`, `backend/tests/test_integration_*.py`,
`backend/pyproject.toml`, `Makefile`.
**Done criteria:** DB up hone par saare integration tests pass.
**Verify:** `make db-up && make test-integration`.

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

### [.] T8.3-B — Backend security/quality gate (backend slice)

**Owner:** Backend.

1. Input validation, CORS, error leakage on backend routes.
2. `ruff`, `pytest`, `pytest -m integration`.
3. Backend part of `docs/limitations.md` (demo data, KYC stub, testnet only).
**Verify:** `backend/.venv/bin/ruff check backend && backend/.venv/bin/pytest -q backend`.

### [.] T8.3-M — Middleware security/quality gate (middleware slice)

**Owner:** Middleware.

1. Secrets grep (`TINYFISH_API_KEY`, `OPERATOR_PRIVATE_KEY`, private keys).
2. `npm --prefix middleware run typecheck && npm --prefix middleware test && npm --prefix middleware run compile`.
3. `npm --prefix middleware audit --omit=dev`.
**Verify:** all four commands pass; `.env` ignored.

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

### [.] T9.1 — ALU hierarchy, lock aur double-sell protection

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

### [.] T9.3-B — Backend production container (backend slice)

**Owner:** Backend. `backend/Dockerfile`.

### [.] T9.3-M — Middleware production container (middleware slice)

**Owner:** Middleware. `middleware/Dockerfile`.

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
