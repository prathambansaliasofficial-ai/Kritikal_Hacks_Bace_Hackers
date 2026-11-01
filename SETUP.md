# Land Market — setup

Prototype monorepo for Kritical Hacks 2026: one land parcel (ULPIN) is verified with
TinyFish, split into tradeable **ALU** units, checked by six fixed rules, and settled
through a testnet escrow.

```
frontend/   React 19 + TS + Vite + MapLibre + log-f.md + AGENTS.md
backend/    FastAPI + PostGIS + log-b.md + AGENTS.md
middleware/ TinyFish agent + Fastify API + Hardhat escrow + log-m.md + AGENTS.md
docs/       contracts, task packs, branch workflow, reference docs
```

Read `docs/team-workflow.md` for branches and `docs/task-ownership.md` for who does what.

## 1. Prerequisites

- Node 24 (`nvm use` reads `.nvmrc`)
- Python 3.12+ (tested on 3.14)
- Docker Desktop (for PostGIS)
- Foundry not needed; Hardhat is used from `middleware/`

## 2. Branch setup (do this once)

Wait for the lead's `C0` baseline commit, then:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
git switch -c backend/<your-name>     # or middleware/<name>, ai/<name>, frontend/<name>
```

Do not work on `main`. Do not push to `main`.

## 3. Env files

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
cp middleware/.env.example middleware/.env
```

- `middleware/.env` needs `TINYFISH_API_KEY` (permanent key from hackathon organizers) for live evidence runs.
- For blockchain: start `npm --prefix middleware run node`, then
  `npm --prefix middleware run deploy:local`, and paste the printed address into
  `middleware/.env` as `ESCROW_CONTRACT_ADDRESS`.
- The operator key for local dev is Hardhat account #0. Never use a real key.
- `.env` files are ignored by git. Never force-add them.

## 4. Install

```bash
npm run install:all
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements-dev.txt
```

## 5. Database

```bash
docker compose up -d postgis
docker compose exec -T postgis psql -U landmarket -d landmarket -c "SELECT postgis_version();"
```

Schema loads automatically on the first container start from `backend/db/001_init.sql`.
To re-apply manually:

```bash
docker compose exec -T postgis psql -U landmarket -d landmarket < backend/db/001_init.sql
```

Later migrations (`002_seed_demo.sql`, `003_bundles.sql`, ...) are applied by the
task that creates them. `make db-reset && make seed` is the clean demo path once
`T1.1`/`T1.3` are done.

## 6. Run (3 terminals, from repo root)

```bash
# terminal 1 — backend
backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000

# terminal 2 — middleware
npm run dev:middleware                                  # http://127.0.0.1:8090

# terminal 3 — frontend
npm run dev:frontend                                    # http://localhost:5173
```

Chain (optional, separate terminal):

```bash
npm --prefix middleware run node
npm --prefix middleware run deploy:local
```

`--app-dir backend` is required because the Python package lives in `backend/app`.
Do not run `uvicorn` from the repo root without it.

## 7. Checks

```bash
npm run typecheck
npm run check:docs
npm --prefix frontend run build
npm --prefix middleware run compile
npm --prefix middleware test
backend/.venv/bin/ruff check backend
backend/.venv/bin/pytest -q backend
npm --prefix middleware run smoke:tinyfish   # needs a real TINYFISH_API_KEY
```

`smoke:tinyfish` fails without a key by design: it proves the real integration is wired.
Never replace it with a fake pass.

## 8. Demo flow

1. Frontend par ULPIN daalo → PostGIS se parcel/ALU bounds.
2. Backend middleware ko `POST /verify/evidence` bhejta hai.
3. TinyFish 21 fields laata hai; sheet evidence hash ke saath attach hoti hai.
4. 6 checks pass → escrow `settle()`. Fail/ambiguous → `refund()` ya officer queue.
5. Har settlement ka event chain par, UI me tx hash.

Abhi implement nahi hua: JWT/KYC, real portal auth, title registry writes, mainnet,
aur 6 checks ki actual rule engine (`app/api/routes/verifications.py` me TODO).

## 9. If something breaks

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: app` | run uvicorn with `--app-dir backend` |
| `postgis_version()` fails | `docker compose up -d postgis` and wait for healthy |
| frontend API calls fail | backend not on `:8000` or `VITE_API_BASE_URL` wrong |
| `TINYFISH_API_KEY is not set` | add `TINYFISH_API_KEY` (permanent hackathon key) to `middleware/.env` |
| `npm run sync:docs` fails | you are not at repo root, or `scripts/` is missing |
| module copy is stale | run `npm run sync:docs`, never hand-edit the copy |

## 10. Future infrastructure (after 4 Nov hackathon)

- **Database**: Migrate from local PostGIS (Docker) to Supabase. Update `DATABASE_URL` in `backend/.env` to Supabase connection string.
- **Frontend deployment**: Deploy to Vercel. Set `VITE_API_BASE_URL` to production backend URL.
- **Middleware deployment**: Deploy middleware service (Railway/Render/Vercel) and set `ESCROW_CONTRACT_ADDRESS` to deployed contract.
- These are NOT part of the hackathon demo (4 Nov). Tests and verifications happen on 5 Nov.

For module-only commands, read `frontend/SETUP.md`, `backend/SETUP.md`, or
`middleware/SETUP.md`.
