# Land Market

Prototype for **Kritical Hacks 2026**: a land-parcel marketplace where a government
**ULPIN** is verified with **TinyFish**-collected evidence, split into tradeable
**ALU** units, checked by six fixed rules, and settled through a testnet escrow.

> Prototype only. Demo records are not official government data, and a blockchain
> receipt is not a legal title transfer.

## Current status (2026-11-20)

- All module branches are merged into `main`; `main` is the delivery branch.
- 37 of 43 roadmap tasks are done (about 86 percent). Backend and frontend are feature complete; the middleware core works locally.
- Still open: live TinyFish proof (`T3.1`) and Sepolia deployment (`T6.3`), both waiting on API keys, plus the one-command demo runner (`T8.2`) and a public deployment (`T9.3-D`).
- Details: [`docs/status.md`](docs/status.md). Honest limits: [`docs/limitations.md`](docs/limitations.md).

## Get running

1. **Setup and run commands:** [`SETUP.md`](SETUP.md)
2. **Keys and wallets (what to get, where to put it):** [`docs/api-keys-setup.md`](docs/api-keys-setup.md)
3. **Check your env files:** `npm run check:env` (add `-- sepolia` for the testnet)
4. **Run the demo:** [`docs/demo-script.md`](docs/demo-script.md)

## Repository layout

| Path | What lives here |
|---|---|
| `frontend/` | React + TypeScript + Vite + MapLibre app, `log-f.md`, `AGENTS.md`, `SETUP.md` |
| `backend/` | FastAPI + PostGIS API, schema, tests, `log-b.md`, `AGENTS.md`, `SETUP.md` |
| `middleware/` | TinyFish evidence service, Fastify API, Hardhat escrow, `log-m.md`, `AGENTS.md`, `SETUP.md` |
| `docs/` | Contracts, decisions, architecture, keys, deployment, demo, task context packs |
| `scripts/` | `sync-docs`, `check-docs`, `check-env` |
| `whole_plan.md` | Master roadmap with task IDs (its progress header is stale; see `docs/status.md`) |
| `SETUP.md` | Local setup and run commands |

Each module folder also contains generated read-only copies of `whole_plan.md` and the
shared `docs/` contract files. Refresh them with `npm run sync:docs`; verify with
`npm run check:docs`. Never edit a generated copy.

## Documentation index

| Topic | File |
|---|---|
| How the pieces fit together | [`docs/architecture.md`](docs/architecture.md) |
| All keys and secrets, step by step | [`docs/api-keys-setup.md`](docs/api-keys-setup.md) |
| TinyFish key | [`docs/keys-tinyfish.md`](docs/keys-tinyfish.md) |
| Local chain setup | [`docs/keys-local.md`](docs/keys-local.md) |
| Sepolia wallets, RPC, faucet, deploy | [`docs/keys-sepolia.md`](docs/keys-sepolia.md) |
| Hosting and secret handling | [`docs/deployment.md`](docs/deployment.md) |
| The 7-step demo | [`docs/demo-script.md`](docs/demo-script.md) |
| Final delivery checklist | [`docs/submission-checklist.md`](docs/submission-checklist.md) |
| API shapes | [`docs/api-contract.md`](docs/api-contract.md) |
| Rules, formats, decisions | [`docs/decisions.md`](docs/decisions.md), [`docs/checks.md`](docs/checks.md) |
| What is not real | [`docs/limitations.md`](docs/limitations.md) |
| Proof records | [`docs/tinyfish-smoke.md`](docs/tinyfish-smoke.md), [`docs/deployments.md`](docs/deployments.md) |

## Quick start

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
cp middleware/.env.example middleware/.env

npm run install:all
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements-dev.txt

docker compose up -d postgis
```

Then run the three services from the repo root:

```bash
backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000
npm run dev:middleware
npm run dev:frontend
```

For the chain and keys, follow [`docs/api-keys-setup.md`](docs/api-keys-setup.md).

## Start here by role

| You are | Read |
|---|---|
| Backend dev | `backend/AGENTS.md`, `backend/SETUP.md`, `docs/task-ownership.md` |
| Middleware dev | `middleware/AGENTS.md`, `middleware/SETUP.md`, `docs/task-ownership.md` |
| Frontend dev | `frontend/AGENTS.md`, `frontend/SETUP.md`, `docs/task-ownership.md` |
| Lead | `docs/team-workflow.md`, `docs/status.md`, `whole_plan.md` |

## Logs

Each module keeps its own Hinglish gitlog:

- [`frontend/log-f.md`](frontend/log-f.md)
- [`backend/log-b.md`](backend/log-b.md)
- [`middleware/log-m.md`](middleware/log-m.md)

Format: `[.]` = completed, `[]` = pending, with date, time, and session.
