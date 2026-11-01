# Land Market

Prototype for **Kritical Hacks 2026**: a land-parcel marketplace where a government
**ULPIN** is verified with **TinyFish**-collected evidence, split into tradeable
**ALU** units, checked by six fixed rules, and settled through a testnet escrow.

> Prototype only. Demo records are not official government data, and a blockchain
> receipt is not a legal title transfer.

## Repository layout

| Path | What lives here |
|---|---|
| `frontend/` | React + TypeScript + Vite + MapLibre app, `log-f.md`, `AGENTS.md`, `SETUP.md` |
| `backend/` | FastAPI + PostGIS API, schema, tests, `log-b.md`, `AGENTS.md`, `SETUP.md` |
| `middleware/` | TinyFish evidence service, Fastify API, Hardhat escrow, `log-m.md`, `AGENTS.md`, `SETUP.md` |
| `docs/` | Contracts, decisions, task context packs, branch workflow, reference docs |
| `whole_plan.md` | Master roadmap, task IDs, commit batches, and current progress |
| `SETUP.md` | Local setup and run commands |

Each module folder also contains generated read-only copies of `whole_plan.md` and the
shared `docs/` contract files. Refresh them with `npm run sync:docs`; verify with
`npm run check:docs`. Never edit a generated copy.

## Start here by role

| You are | Read |
|---|---|
| Backend dev | `backend/AGENTS.md` → `backend/SETUP.md` → `docs/task-ownership.md` |
| Middleware dev | `middleware/AGENTS.md` → `middleware/SETUP.md` → `docs/task-ownership.md` |
| AI / TinyFish dev | `middleware/AGENTS.md` §AI → `docs/task-ownership.md` |
| Frontend dev | `frontend/AGENTS.md` → `frontend/SETUP.md` → `docs/task-ownership.md` |
| Lead | `docs/team-workflow.md` → `whole_plan.md` |

One person = one module branch (`backend/<name>`, `middleware/<name>`, `ai/<name>`,
`frontend/<name>`). Never push to `main`; open a PR.

## Quick start

Full instructions are in [`SETUP.md`](SETUP.md).

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

## Current status

- Scaffold complete: frontend shell, API skeleton, PostGIS schema, TinyFish
  evidence collector, and escrow contract with passing tests.
- Roadmap progress: see the header of [`whole_plan.md`](whole_plan.md).
- Live TinyFish runs need `TINYFISH_API_KEY` in `middleware/.env`.
- Nothing is committed or pushed yet; baseline commit `C0` is the next step.

## Logs

Each module keeps its own Hinglish gitlog:

- [`frontend/log-f.md`](frontend/log-f.md)
- [`backend/log-b.md`](backend/log-b.md)
- [`middleware/log-m.md`](middleware/log-m.md)

Format: `[.]` = completed, `[]` = pending, with date, time, and session.
