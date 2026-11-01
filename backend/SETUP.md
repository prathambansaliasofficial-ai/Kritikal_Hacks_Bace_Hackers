# Backend setup

FastAPI + PostGIS. This file is only for the `backend/` module.
Shared prerequisites and the full monorepo runbook are in `../SETUP.md`.

## 1. Python and env

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements-dev.txt
cp backend/.env.example backend/.env
```

| Variable | Default | Meaning |
|---|---|---|
| `DATABASE_URL` | `postgresql://landmarket:landmarket_dev@localhost:5432/landmarket` | PostGIS |
| `MIDDLEWARE_URL` | `http://127.0.0.1:8090` | TinyFish/escrow middleware |
| `MIDDLEWARE_TIMEOUT_SECONDS` | `90` | evidence run timeout |
| `CORS_ORIGINS` | `http://localhost:5173` | allowed frontend origin |
| `DEV_OFFICER_TOKEN` | empty | prototype review token (T4.1) |

## 2. Database

```bash
docker compose up -d postgis
docker compose exec -T postgis psql -U landmarket -d landmarket -c "SELECT postgis_version();"
```

`backend/db/001_init.sql` loads automatically on first container start. To re-apply:

```bash
docker compose exec -T postgis psql -U landmarket -d landmarket < backend/db/001_init.sql
```

After `T1.1`, use `make db-up`, `make db-check`, `make db-reset`, `make seed`.

## 3. Run

From the repo root:

```bash
backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000
curl -s localhost:8000/health | jq
```

`--app-dir backend` is required. Running plain `uvicorn app.api.main:app` from the root
fails with `ModuleNotFoundError: app`.

## 4. Checks

```bash
backend/.venv/bin/ruff check backend
backend/.venv/bin/pytest -q backend
backend/.venv/bin/pytest -q backend/tests/test_health.py
```

Integration tests (after `T8.1`) need a DB:

```bash
make db-up
make test-integration
```

## 5. Common errors

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: app` | add `--app-dir backend` |
| `connection refused` on `:5432` | `docker compose up -d postgis` |
| `postgis extension missing` | re-apply `backend/db/001_init.sql` |
| `pytest` cannot import `app` | run from repo root, or from `backend/` with `pytest` |
| middleware 503 | start `npm run dev:middleware` |
| evidence route returns 422 | middleware sheet must have exactly 21 fields |

## 6. Where the rules live

- API shapes/enums/error codes: `docs/api-contract.md`
- ALU math, hash, order ID, money, chain: `docs/decisions.md`
- Six checks/decision: `docs/checks.md`
- Your task order: `AGENTS.md`

Do not add a field that is not in the root contract. Update the root contract first,
then `npm run sync:docs`.
