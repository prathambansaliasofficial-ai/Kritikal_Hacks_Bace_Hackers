# Land Market

**A land-parcel marketplace prototype built for Kritikal Hacks 2026 by Team Bace Hackers.**

A government land identifier (**ULPIN**) is verified using evidence collected by **TinyFish**, divided into tradeable **ALU** units (Automated Land Units), checked against six fixed rules, and settled through a testnet escrow contract.

> **Prototype only.** Demo records are fictional and are not official government data. A blockchain receipt is not a legal title transfer. See [`docs/limitations.md`](docs/limitations.md).

Concept overview: [Bhoomi 2.0](https://github.com/prathambansaliasofficial-ai/Bhoomi2.0).

## Status (as of 20 November 2026)

- All module branches are merged into `main`, the delivery branch.
- 37 of 43 roadmap tasks are complete (about 86%). Backend and frontend are feature-complete; the middleware core runs locally.
- **Open items:** live TinyFish proof (`T3.1`) and Sepolia deployment (`T6.3`), both awaiting API keys; a one-command demo runner (`T8.2`); and a public deployment (`T9.3-D`).
- Details: [`docs/status.md`](docs/status.md).

## System Overview

| Module | Technology | Responsibility |
|---|---|---|
| `frontend/` | React, TypeScript, Vite, MapLibre | Marketplace interface and map view |
| `backend/` | FastAPI, PostgreSQL + PostGIS | API, schema, trade rule engine, tests |
| `middleware/` | TinyFish service, Fastify, Hardhat | Evidence collection and hashing; Solidity escrow on the Sepolia testnet |
| `docs/` | Markdown | Contracts, decisions, architecture, deployment, demo scripts |
| `scripts/` | Node | `sync-docs`, `check-docs`, `check-env` utilities |

**Trade rules (six fixed checks):** `LISTED`, `BUNDLE_INTACT`, `KYC_WALLET`, `ZONING_OK`, `FUNDS_IN_ESCROW`, `TRADE_MATCH`.

## Quick Start

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

Run the three services from the repository root:

```bash
backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000
npm run dev:middleware
npm run dev:frontend
```

Verify environment files with `npm run check:env` (add `-- sepolia` for the testnet). Keys and wallets: [`docs/api-keys-setup.md`](docs/api-keys-setup.md). Full setup: [`SETUP.md`](SETUP.md).

## Demo

- Seven-step demo: [`docs/demo-script.md`](docs/demo-script.md)
- Fast path with simulated payment (no wallet or gas): [`docs/demo-payment-mode.md`](docs/demo-payment-mode.md)

## Documentation Index

| Topic | File |
|---|---|
| Architecture | [`docs/architecture.md`](docs/architecture.md) |
| API contract | [`docs/api-contract.md`](docs/api-contract.md) |
| Rules and decisions | [`docs/decisions.md`](docs/decisions.md), [`docs/checks.md`](docs/checks.md) |
| Keys and secrets | [`docs/api-keys-setup.md`](docs/api-keys-setup.md) |
| Deployment | [`docs/deployment.md`](docs/deployment.md) |
| Limitations | [`docs/limitations.md`](docs/limitations.md) |
| Submission checklist | [`docs/submission-checklist.md`](docs/submission-checklist.md) |

## Development Conventions

Each module keeps a work log (`frontend/log-f.md`, `backend/log-b.md`, `middleware/log-m.md`) and an `AGENTS.md` guide. Generated copies of `whole_plan.md` and the shared `docs/` files inside each module are read-only; refresh them with `npm run sync:docs` and verify with `npm run check:docs`. The progress header in `whole_plan.md` is outdated; `docs/status.md` is authoritative.

## Team and Contribution

Team Bace Hackers: Pratham Bansal and Yash Baghel.

[Add: your specific contribution, e.g. which modules you built.]
