# Land Market: setup

Prototype monorepo for Kritical Hacks 2026: one land parcel (ULPIN) is verified with
TinyFish, split into tradeable **ALU** units, checked by six fixed rules, and settled
through a testnet escrow.

```
frontend/   React 19 + TS + Vite + MapLibre + log-f.md + AGENTS.md
backend/    FastAPI + PostGIS + log-b.md + AGENTS.md
middleware/ TinyFish agent + Fastify API + Hardhat escrow + log-m.md + AGENTS.md
docs/       architecture, keys, deployment, demo, contracts, reference docs
```

All work is merged into `main`. Clone it and run from there.

## 1. Prerequisites

- Node 24 (`nvm use` reads `.nvmrc`)
- Python 3.12+ (tested on 3.14)
- Docker Desktop (for PostGIS)
- MetaMask in your browser (for the buy flow)
- Foundry is not needed; Hardhat runs from `middleware/`

## 2. Env files and keys

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
cp middleware/.env.example middleware/.env
```

`.env` files are git-ignored. Never force-add them.

**Which keys do I need, and where do I get them?** Read [`docs/api-keys-setup.md`](docs/api-keys-setup.md).
In short:

| Goal | What you need | Guide |
|---|---|---|
| Run the app and tests | Nothing external | this file |
| Live land evidence | TinyFish API key | `docs/keys-tinyfish.md` |
| Local chain demo | Local Hardhat node, no accounts | `docs/keys-local.md` |
| Public testnet demo | Sepolia RPC URL, a throwaway operator wallet, test ETH | `docs/keys-sepolia.md` |

After editing env files, validate them (values are never printed):

```bash
npm run check:env               # local chain
npm run check:env -- sepolia    # Sepolia testnet
```

## 3. Install

```bash
npm run install:all
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements-dev.txt
```

## 4. Database

```bash
make db-up        # docker compose up -d postgis
make db-check     # PostGIS version + tables + row counts
make seed         # demo parcel DEMO-ULPIN-001 + ALUs
```

The schema files in `backend/db/` load automatically on the first container start.
`make db-reset && make seed` is the clean demo path (it asks before deleting the volume).

## 5. Chain (local)

```bash
npm --prefix middleware run node            # terminal 1
npm --prefix middleware run deploy:local    # terminal 2, prints the contract address
```

Put the address in `middleware/.env` (`ESCROW_CONTRACT_ADDRESS`) and `frontend/.env`
(`VITE_ESCROW_ADDRESS`). Details and the operator key: `docs/keys-local.md`.
For Sepolia use `docs/keys-sepolia.md` instead.

## 6. Run (3 terminals, from the repo root)

```bash
# terminal 1: backend  (http://localhost:8000, API docs at /docs)
backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000

# terminal 2: middleware  (http://127.0.0.1:8090)
npm run dev:middleware

# terminal 3: frontend  (http://localhost:5173)
npm run dev:frontend
```

`--app-dir backend` is required because the Python package lives in `backend/app`.
Restart a service after changing its `.env` file.

## 7. Checks

```bash
npm run typecheck
npm run check:docs
npm run check:env
npm --prefix frontend run build
npm --prefix middleware run compile
npm --prefix middleware test
backend/.venv/bin/ruff check backend
backend/.venv/bin/pytest -q backend
make test-integration                          # needs the database running
npm --prefix middleware run smoke:tinyfish     # needs a real TinyFish key
```

`smoke:tinyfish` fails without a key by design: it proves the real integration is wired.
Never replace it with a fake pass.

## 8. Demo flow

The full 7-step demo, with setup and fallbacks, is in [`docs/demo-script.md`](docs/demo-script.md).
In short:

1. The frontend shows the parcel and its ALU grid from PostGIS.
2. The backend asks the middleware to collect evidence; TinyFish returns the 21-field sheet, stored with its hash.
3. An officer reviews the evidence.
4. The buyer's wallet sends the price into the escrow contract.
5. The backend runs the six checks. `APPROVED` calls `settle()`, `REJECTED` calls `refund()`, missing evidence goes to officer review.
6. The UI shows the order state and the transaction hash.

What is intentionally not real (demo data, KYC stub, testnet only): [`docs/limitations.md`](docs/limitations.md).

## 9. If something breaks

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: app` | Run uvicorn with `--app-dir backend` |
| `postgis_version()` fails | `make db-up` and wait for healthy |
| Frontend API calls fail | Backend not on `:8000`, or `VITE_API_BASE_URL` is wrong |
| Browser blocks API calls (CORS) | Add the frontend URL to `CORS_ORIGINS` in `backend/.env` |
| `TINYFISH_API_KEY is not set` | Add it to `middleware/.env` and restart; see `docs/keys-tinyfish.md` |
| UI says escrow address not configured | Set `VITE_ESCROW_ADDRESS` in `frontend/.env`, restart the frontend |
| Settlement reverts | `OPERATOR_PRIVATE_KEY` must be the key that deployed the contract |
| `npm run sync:docs` fails | You are not at the repo root, or `scripts/` is missing |
| Module copy is stale | Run `npm run sync:docs`; never hand-edit the copy |

More key-related errors: the troubleshooting tables in `docs/keys-sepolia.md` and `docs/keys-tinyfish.md`.

## 10. Deploying

Hosting steps, where each secret lives, and the security rules are in
[`docs/deployment.md`](docs/deployment.md). Two rules matter most: keep the middleware private,
and leave `VITE_OFFICER_TOKEN` empty on any public frontend.

For module-only commands, read `frontend/SETUP.md`, `backend/SETUP.md`, or
`middleware/SETUP.md`.
