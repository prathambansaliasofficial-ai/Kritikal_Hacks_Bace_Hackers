# AGENTS.md — Backend module

**You own:** `backend/` plus the exact root files named in your task.  
**Branch:** `backend/<your-name>` (never `main`).  
**Full rules:** `docs/team-workflow.md` · **Task map:** `docs/task-ownership.md`.

If you are an AI agent: read this file, `backend/SETUP.md`, your task block in
`whole_plan.md`, and **only** the context pack for your batch. Do not scan other modules.

## 1. Your task queue

| Task | What it is | Context pack |
|---|---|---|
| `T1.1` | PostGIS boot + schema check + `Makefile` | `docs/context/C1.md` |
| `T1.2` | DB access layer (`db_connection`, repositories) | `docs/context/C1.md` |
| `T1.3` | demo parcel/ALU seed | `docs/context/C1.md` |
| `T2.1` | parcel read API | `docs/context/C2.md` |
| `T2.2` | deterministic ALU grid endpoint | `docs/context/C2.md` |
| `T2.3` | bundle schema + API | `docs/context/C2.md` |
| `T3.2` | evidence validate/hash/persist | `docs/context/C3.md` |
| `T3.3` | officer review queue | `docs/context/C3.md` |
| `T4.1` | wallet user + KYC stub | `docs/context/C4.md` |
| `T4.2` | listing lifecycle | `docs/context/C4.md` |
| `T4.3` | order lifecycle | `docs/context/C4.md` |
| `T5.1` | six-check pure rule engine | `docs/context/C5.md` |
| `T5.2` | evaluate endpoint + decision | `docs/context/C5.md` |
| `T5.3-B` | backend settlement slice of T5.3 | `docs/context/C5.md` |
| `T8.1` | real PostGIS integration tests | `docs/context/C8.md` |
| `T8.3-B` | backend quality gate | `docs/context/C8.md` |
| `T9.1` | ALU locking (stretch) | `docs/context/C9.md` |

Module batches: `B1` = T1.1–T1.3, `B2` = T2.1–T2.3, `B3` = T3.2/T3.3/T4.1,
`B4` = T4.2/T4.3/T5.1, `B5` = T5.2/T5.3-B/T8.1, `B6` = T8.3-B/T9.1.
Commit messages are in `docs/task-ownership.md` §2.

## 2. Cross-module tasks (do not do the other half)

| Task | Your slice | Not yours |
|---|---|---|
| `T3.1` | none — middleware owns the live TinyFish proof | do not wait; mock middleware for T3.2 |
| `T5.3-M` | none — middleware adds `GET /escrow/status/{orderId}` | backend only writes `T5.3-B` |
| `T6.1` | none | middleware + frontend own it |
| `T8.2` | none | lead owns the demo runner |
| `T9.2` | contract review only | AI/middleware own the portal merge |

If a middleware endpoint is not live yet, use the exact shape in
`docs/api-contract.md` and mock it in tests. Never invent an alternate shape.

## 3. Files you may edit

```
backend/app/**
backend/db/**
backend/scripts/**
backend/tests/**
backend/requirements*.txt
backend/pyproject.toml
backend/.env.example
backend/README.md
backend/log-b.md
backend/AGENTS.md
backend/SETUP.md
Makefile                 (only T1.1, T1.3, T8.1)
SETUP.md                 (only T1.1, T1.3)
docs/checks.md           (only T5.1, T5.2)
```

You may also change **your own task markers** in root `../whole_plan.md`.
You may **not** edit `../frontend/`, `../middleware/`, other root docs, or generated
copies (`backend/whole_plan.md`, `backend/docs/**`).

## 4. Fixed contracts (do not invent fields)

- `docs/api-contract.md` — request/response shapes, enums, error codes.
- `docs/decisions.md` — ALU math, evidence hash, order ID, money, chain constants.
- `docs/checks.md` — six checks, blocking flags, decision mapping.

Rules that matter on the backend:

- Money is `NUMERIC(78,0)` / decimal string, never float.
- Evidence hash is canonical JSON SHA-256 with `0x` prefix (decisions §4).
- Missing evidence field becomes `N/D`; never invent a value.
- `APPROVED → settle`, `REJECTED → refund`, `NEEDS_REVIEW → no chain call`.
- Demo rows carry `DEMO_FIXTURE_NOT_OFFICIAL`; API demo objects carry `demo: true`.
- Middleware down = 503, invalid sheet = 422, chain failure = 502. No state change on error.

## 5. Commands (from repo root)

```bash
docker compose up -d postgis
backend/.venv/bin/ruff check backend
backend/.venv/bin/pytest -q backend
backend/.venv/bin/pytest -q backend/tests/test_<area>.py
backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000
```

After `T1.1`, the `Makefile` targets are the short path (`make db-up`, `make db-check`,
`make seed`, `make api`, `make check`).

## 6. Definition of done

- [ ] Code matches the task block and `docs/api-contract.md`.
- [ ] Tests named in the task pass; `ruff` + `pytest` pass.
- [ ] No direct `psycopg.connect` outside `backend/app/core/db.py` (after T1.2).
- [ ] No fake key, run ID, TxHash, or government record.
- [ ] Demo data labelled correctly.
- [ ] `backend/log-b.md` updated with date/time/session and exact commands.
- [ ] Your task marker in `../whole_plan.md` is `[.]`.
- [ ] `npm run sync:docs && npm run check:docs` pass.
- [ ] Commit uses the batch message from `docs/task-ownership.md`.

## 7. Stop conditions

Stop and write `**BLOCKED:**` in the task block + log if:

- the task needs a middleware endpoint that is not live and the pack does not say "mock it",
- a DB migration conflicts with an existing table/column,
- `TINYFISH_API_KEY` or another human key is needed,
- you need to edit `frontend/` or `middleware/`,
- the contract does not describe a shape you need.

Ask the lead with: task ID, what you tried, exact error, smallest unblock.
