# AGENTS.md — Land Market

Read this first. Then read **only** your module `AGENTS.md` and the files listed for your
assigned batch. Do not scan the repo.

## Who are you?

| You are | Start here | Your branch |
|---|---|---|
| Backend dev / AI agent | `backend/AGENTS.md` | `backend/<name>` |
| Middleware dev / AI agent | `middleware/AGENTS.md` | `middleware/<name>` |
| AI / TinyFish dev | `middleware/AGENTS.md` (AI section) | `ai/<name>` |
| Frontend dev / AI agent | `frontend/AGENTS.md` | `frontend/<name>` |
| Lead / integrator | this file + `docs/team-workflow.md` | `main` (merge only) |

One person works on one module branch. Never push directly to `main`; open a PR.
Full rules: `docs/team-workflow.md`. Task ownership: `docs/task-ownership.md`.

## Repo map

| Path | Purpose |
|---|---|
| `frontend/` | React 19 + TypeScript + Vite + MapLibre app; log: `frontend/log-f.md` |
| `backend/` | FastAPI + PostGIS API, tests, SQL; log: `backend/log-b.md` |
| `middleware/` | TinyFish evidence service + Fastify + Hardhat escrow; log: `middleware/log-m.md` |
| `docs/` | Shared contracts, decisions, task context packs, reference docs |
| `whole_plan.md` | Master roadmap: task IDs, batches, progress, blockers |
| `SETUP.md` | Human runbook: install, env, run, checks |
| `docs/team-workflow.md` | Branch, merge, handoff and root-conflict rules |
| `docs/task-ownership.md` | Who owns each task and which paths they may edit |

Each module has hand-written `AGENTS.md` + `SETUP.md`, and generated read-only copies of
`whole_plan.md`, `docs/api-contract.md`, `docs/decisions.md`, `docs/checks.md`,
`docs/team-workflow.md`, `docs/task-ownership.md` and `docs/context/`.
Generated copies are refreshed by `npm run sync:docs`. Never edit a generated copy.

## Source of truth

1. `whole_plan.md` — task order, status, commit messages.
2. `docs/task-ownership.md` — which task belongs to which branch.
3. `docs/api-contract.md` — fixed request/response shapes and enums.
4. `docs/decisions.md` — IDs, hashes, ALU math, policy constants.
5. `docs/checks.md` — the six checks and decision mapping.
6. `docs/context/C*.md` — one self-contained pack per batch.
7. Module log — only that module's history and pending items.

Edit the **root** shared doc, then run `npm run sync:docs`. Never edit a module copy of
`whole_plan.md` or `docs/`.

## Context budget rules

- Read your module `AGENTS.md`, then the **current pending section** of its log.
- Read only the context pack for your batch and the code files it lists.
- Do **not** read other modules' code or logs.
- If a task needs a file not listed, stop and ask; do not explore randomly.
- Keep one module batch (3 tasks) per run.

## Commands (from repo root)

```bash
npm run install:all
npm run typecheck
npm run test:middleware
npm run sync:docs
npm run check:docs

docker compose up -d postgis
backend/.venv/bin/ruff check backend
backend/.venv/bin/pytest -q backend
npm --prefix frontend run build
npm --prefix middleware run compile
npm --prefix middleware test
```

Module-specific commands are in each module's `AGENTS.md` and `SETUP.md`.

## Commit protocol

1. Complete exactly 3 tasks assigned to your module (see `docs/task-ownership.md`).
2. Update **your** task markers in root `whole_plan.md` and your module log.
   Do not edit the progress header or phase counters; the lead owns those.
3. Run `npm run sync:docs && npm run check:docs`.
4. Stage only your module + the exact root files your task allows; never `git add -A`.
5. Commit with the batch message from `whole_plan.md` (or your module batch table).
6. Push your branch and open a PR. Do not push `main` and do not merge yourself.

## Hard rules

- Follow task ID order. Do not skip or reorder tasks.
- Stay inside your module folder. Cross-module changes need the lead's approval.
- No fake API keys, run IDs, transaction hashes, or government records.
- Demo data must carry `DEMO_FIXTURE_NOT_OFFICIAL` (DB) or `demo: true` (API).
- Never commit `.env` files or secrets.
- Prototype only: testnet funds, no legal title transfer, KYC is a stub.
- If blocked, leave the task `[]`, write `**BLOCKED:**`, and ask the human.

## Current state

- Progress: see the header of `whole_plan.md`.
- Next batch: `C0` baseline commit (lead), then backend `B1` (`T1.1`–`T1.3`).
- Nothing has been committed or pushed by the AI yet.
- **Hackathon deadline: 4 Nov 2026** (implementation ends). Tests and verifications on 5 Nov. Actual show/demo on 5 Nov.
