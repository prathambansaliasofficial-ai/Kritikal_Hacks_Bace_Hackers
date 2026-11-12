<!--
  GENERATED FILE. Source: docs/task-ownership.md
  Do not edit this copy. Edit the root file, then run: npm run sync:docs
-->
# Task ownership map

Use this file to answer **"is this task mine?"** before reading code.
The full task text stays in `whole_plan.md`; this file only assigns work.

Branch names: `backend/<name>`, `middleware/<name>`, `ai/<name>`, `frontend/<name>`.
Full workflow: `docs/team-workflow.md`.

## 1. Owner per task

| Task | Owner | Branch | Allowed edit paths | Depends on |
|---|---|---|---|---|
| `C0` | Lead | `main` | repo root + all modules (baseline only) | — |
| `T1.1` | Backend | `backend/*` | `backend/scripts/`, `Makefile`, `SETUP.md` | C0 |
| `T1.2` | Backend | `backend/*` | `backend/app/core/`, `backend/app/repositories/`, `backend/tests/` | T1.1 |
| `T1.3` | Backend | `backend/*` | `backend/db/`, `backend/scripts/`, `Makefile`, `SETUP.md` | T1.2 |
| `T2.1` | Backend | `backend/*` | `backend/app/repositories/`, `backend/app/api/`, `backend/tests/` | C1 |
| `T2.2` | Backend | `backend/*` | `backend/app/services/`, `backend/app/api/`, `backend/tests/` | C1 |
| `T2.3` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/tests/` | C1 |
| `T3.1` | Middleware | `middleware/*` | `middleware/`, `docs/tinyfish-smoke.md` | `TINYFISH_API_KEY` |
| `T3.2` | Backend | `backend/*` | `backend/app/services/`, `backend/app/repositories/`, `backend/app/api/`, `backend/tests/` | C2 |
| `T3.3` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/tests/` | T3.2 |
| `T4.1` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/.env.example`, `backend/tests/` | C2 |
| `T4.2` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/tests/` | T4.1, T2.3 |
| `T4.3` | Backend | `backend/*` | `backend/app/`, `backend/tests/` | T4.2 |
| `T5.1` | Backend | `backend/*` | `backend/app/services/`, `docs/checks.md`, `backend/tests/` | T4.3 |
| `T5.2` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `docs/checks.md`, `backend/tests/` | T5.1 |
| `T5.3-M` | Middleware | `middleware/*` | `middleware/src/server.ts`, `middleware/src/blockchain/`, tests | T0.4 |
| `T5.3-B` | Backend | `backend/*` | `backend/app/services/`, `backend/app/api/`, `backend/tests/` | T5.2, T5.3-M |
| `T6.1-M` | Middleware | `middleware/*` | `middleware/scripts/`, `middleware/deployments/` | T5.3-M |
| `T6.1-F` | Frontend | `frontend/*` | `frontend/src/lib/`, `frontend/.env.example` | T6.1-M |
| `T6.2` | Middleware | `middleware/*` | `middleware/scripts/`, `middleware/package.json`, `Makefile`, `middleware/README.md` | T6.1-M |
| `T6.3` | Middleware | `middleware/*` | `middleware/`, `docs/deployments.md` | Sepolia key/RPC |
| `T7.1` | Frontend | `frontend/*` | `frontend/src/` | T2.1, T2.2 |
| `T7.2` | Frontend | `frontend/*` | `frontend/src/` | T3.2, T3.3 |
| `T7.3` | Frontend | `frontend/*` | `frontend/src/` | T6.1-F |
| `T7.4` | Frontend | `frontend/*` | `frontend/src/` | T4.3, T5.2, C6 |
| `T7.5` | Frontend | `frontend/*` | `frontend/src/` | T7.4 |
| `T7.6` | Frontend | `frontend/*` | `frontend/src/` | T7.1–T7.5 |
| `T8.1` | Backend | `backend/*` | `backend/tests/`, `backend/pyproject.toml`, `Makefile` | C5 |
| `T8.2` | Lead | `main` / shared | `scripts/`, `docs/`, `Makefile` | C1–C7B |
| `T8.3-B` | Backend | `backend/*` | `backend/` | T8.1 |
| `T8.3-M` | Middleware | `middleware/*` | `middleware/` | T6.3 |
| `T8.3-F` | Frontend | `frontend/*` | `frontend/` | T7.6 |
| `T8.3-D` | Lead | `main` / shared | `README.md`, `SETUP.md`, `docs/` | T8.3-B/M/F |
| `T9.1` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/tests/` | C5 |
| `T9.2` | AI | `ai/*` | `middleware/src/tinyfish/`, AI tests; contract changes via lead | T3.1 |
| `T9.3-M` | Middleware | `middleware/*` | `middleware/Dockerfile` | T6.3 |
| `T9.3-B` | Backend | `backend/*` | `backend/Dockerfile` | C5 |
| `T9.3-F` | Frontend | `frontend/*` | `frontend/Dockerfile` | T7.6 |
## 1. Owner per task

| Task | Owner | Branch | Allowed edit paths | Depends on |
|---|---|---|---|---|
| `C0` | Lead | `main` | repo root + all modules (baseline only) | — |
| `T1.1` | Backend | `backend/*` | `backend/scripts/`, `Makefile`, `SETUP.md` | C0 |
| `T1.2` | Backend | `backend/*` | `backend/app/core/`, `backend/app/repositories/`, `backend/tests/` | T1.1 |
| `T1.3` | Backend | `backend/*` | `backend/db/`, `backend/scripts/`, `Makefile`, `SETUP.md` | T1.2 |
| `T2.1` | Backend | `backend/*` | `backend/app/repositories/`, `backend/app/api/`, `backend/tests/` | C1 |
| `T2.2` | Backend | `backend/*` | `backend/app/services/`, `backend/app/api/`, `backend/tests/` | C1 |
| `T2.3` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/tests/` | C1 |
| `T3.1` | Middleware | `middleware/*` | `middleware/`, `docs/tinyfish-smoke.md` | `TINYFISH_API_KEY` |
| `T3.2` | Backend | `backend/*` | `backend/app/services/`, `backend/app/repositories/`, `backend/app/api/`, `backend/tests/` | C2 |
| `T3.3` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/tests/` | T3.2 |
| `T4.1` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/.env.example`, `backend/tests/` | C2 |
| `T4.2` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/tests/` | T4.1, T2.3 |
| `T4.3` | Backend | `backend/*` | `backend/app/`, `backend/tests/` | T4.2 |
| `T5.1` | Backend | `backend/*` | `backend/app/services/`, `docs/checks.md`, `backend/tests/` | T4.3 |
| `T5.2` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `docs/checks.md`, `backend/tests/` | T5.1 |
| `T5.3-M` | Middleware | `middleware/*` | `middleware/src/server.ts`, `middleware/src/blockchain/`, tests | T0.4 |
| `T5.3-B` | Backend | `backend/*` | `backend/app/services/`, `backend/app/api/`, `backend/tests/` | T5.2, T5.3-M |
| `T6.1-M` | Middleware | `middleware/*` | `middleware/scripts/`, `middleware/deployments/` | T5.3-M |
| `T6.1-F` | Frontend | `frontend/*` | `frontend/src/lib/`, `frontend/.env.example` | T6.1-M |
| `T6.2` | Middleware | `middleware/*` | `middleware/scripts/`, `middleware/package.json`, `Makefile`, `middleware/README.md` | T6.1-M |
| `T6.3` | Middleware | `middleware/*` | `middleware/`, `docs/deployments.md` | Sepolia key/RPC |
| `T7.1` | Frontend | `frontend/*` | `frontend/src/` | T2.1, T2.2 |
| `T7.2` | Frontend | `frontend/*` | `frontend/src/` | T3.2, T3.3 |
| `T7.3` | Frontend | `frontend/*` | `frontend/src/` | T6.1-F |
| `T7.4` | Frontend | `frontend/*` | `frontend/src/` | T4.3, T5.2, C6 |
| `T7.5` | Frontend | `frontend/*` | `frontend/src/` | T7.4 |
| `T7.6` | Frontend | `frontend/*` | `frontend/src/` | T7.1–T7.5 |
| `T8.1` | Backend | `backend/*` | `backend/tests/`, `backend/pyproject.toml`, `Makefile` | C5 |
| `T8.2` | Lead | `main` / shared | `scripts/`, `docs/`, `Makefile` | C1–C7B |
| `T8.3-B` | Backend | `backend/*` | `backend/` | T8.1 |
| `T8.3-M` | Middleware | `middleware/*` | `middleware/` | T6.3 |
| `T8.3-F` | Frontend | `frontend/*` | `frontend/` | T7.6 |
| `T8.3-D` | Lead | `main` / shared | `README.md`, `SETUP.md`, `docs/` | T8.3-B/M/F |
| `T9.1` | Backend | `backend/*` | `backend/db/`, `backend/app/`, `backend/tests/` | C5 |
| `T9.2` | AI | `ai/*` | `middleware/src/tinyfish/`, AI tests; contract changes via lead | T3.1 |
| `T9.3-B` | Backend | `backend/*` | `backend/Dockerfile` | C5 |
| `T9.3-F` | Frontend | `frontend/*` | `frontend/Dockerfile` | T7.6 |
| `T9.3-M` | Middleware | `middleware/*` | `middleware/Dockerfile` | T6.3 |
| `T9.3-D` | Lead | `main` / shared | `docker-compose.prod.yml`, `docs/deployment.md` | T9.3-B/M/F |

## 2. Review file ownership

| Review file | Written by | Code access |
|---|---|---|
| `frontend/review-f.md` | Frontend reviewer | Read-only on `frontend/` source |
| `backend/review-b.md` | Backend reviewer | Read-only on `backend/` source |
| `middleware/review-m.md` | Middleware reviewer | Read-only on `middleware/` source |

Reviewer review comments mein `[BLOCKER]` / `[MAJOR]` / `[NIT]` severity aur `Verdict` + `Status` set karti hai. Reviewer source code nahi edit karti; sirf apni review file edit karti hai. Review fix commit: `fix(scope): resolve R-<n>`.

`T5.3`, `T6.1`, `T8.3`, `T9.3` in `whole_plan.md` are split by module using the
suffixes above. Do only your row.

## 2. Module batches (3 tasks per run)

Each module owns its own batches. The cross-module batch names in `whole_plan.md`
are for the lead's merge log; your branch commits only your slice.

### Backend branch

| Batch | Tasks | Commit message |
|---|---|---|
| `B1` | T1.1, T1.2, T1.3 | `feat(db): add postgis checks, db helpers and demo seed` |
| `B2` | T2.1, T2.2, T2.3 | `feat(api): expose parcels, alu grid and bundles` |
| `B3` | T3.2, T3.3, T4.1 | `feat(evidence): persist evidence, review queue and wallet users` |
| `B4` | T4.2, T4.3, T5.1 | `feat(market): add listings, orders and six checks` |
| `B5` | T5.2, T5.3-B, T8.1 | `feat(trade): evaluate, settle and integration-test orders` |
| `B6` | T8.3-B, T9.1 | `chore(backend): harden and add alu locking` |

### Middleware / AI branch

| Batch | Tasks | Commit message |
|---|---|---|
| `M1` | T3.1, T5.3-M, T6.1-M | `feat(evidence): add live proof, escrow status and deploy artifacts` |
| `M2` | T6.2, T6.3, T9.2 | `feat(chain): add local smoke, sepolia and multi-portal evidence` |
| `M3` | T8.3-M, T9.3-M | `chore(middleware): harden and add production container` |

If `TINYFISH_API_KEY` or the Sepolia key is missing, do the unblocked tasks in the
batch and leave the blocked task `[]` with `**BLOCKED:**`.

### Frontend branch

| Batch | Tasks | Commit message |
|---|---|---|
| `F1` | T6.1-F, T7.1, T7.2 | `feat(web): add chain config, map layers and evidence review` |
| `F2` | T7.3, T7.4, T7.5 | `feat(web): add wallet, buy flow and trade status` |
| `F3` | T7.6, T8.3-F, T9.3-F | `feat(web): polish, harden and add production container` |

### Lead

| Batch | Tasks | Commit message |
|---|---|---|
| `C0` | C0 | `chore: scaffold land market monorepo and roadmap` |
| `D1` | T8.2 | `test: add one-command demo runner and submission docs` |

## 3. Cross-module task rule

When `whole_plan.md` shows one task spanning two modules, use the split row above:

- The middleware owner does the middleware slice first (or publishes the contract).
- The backend/frontend owner codes against `docs/api-contract.md` and may mock the
  missing side in tests.
- Both owners mention the other in the PR description.
- The lead merges both slices under the same batch name.

## 4. "Can I start?" checklist

Before starting any task:

- [ ] My task ID is in my owner row above.
- [ ] My dependency is merged, or my context pack says "mock it".
- [ ] I know the exact files I may touch.
- [ ] I know the command that proves the task is done.
- [ ] I know the commit message.
