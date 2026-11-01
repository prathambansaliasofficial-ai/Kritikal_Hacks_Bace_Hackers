# AGENTS.md — Frontend module

**You own:** `frontend/` only.  
**Branch:** `frontend/<your-name>` (never `main`).  
**Full rules:** `docs/team-workflow.md` · **Task map:** `docs/task-ownership.md`.

If you are an AI agent: read this file, `frontend/SETUP.md`, your task block in
`whole_plan.md`, and **only** the context pack for your batch. Do not scan other modules.

## 1. Your task queue

Do these in order. Do not start a later task until the earlier one is merged or the
dependency is explicitly mocked.

| Task | What it is | Context pack |
|---|---|---|
| `T6.1-F` | frontend chain config + ABI slice of T6.1 | `docs/context/C6.md` |
| `T7.1` | parcel + ALU map layers | `docs/context/C7A.md` |
| `T7.2` | officer evidence + review UI | `docs/context/C7A.md` |
| `T7.3` | wallet connect + chain switch | `docs/context/C7A.md` |
| `T7.4` | listing browse + buy flow | `docs/context/C7B.md` |
| `T7.5` | trade status (checks, decision, tx hash) | `docs/context/C7B.md` |
| `T7.6` | empty/error states + demo banner + responsive | `docs/context/C7B.md` |
| `T8.3-F` | frontend quality gate | `docs/context/C8.md` |
| `T9.3-F` | frontend Dockerfile (stretch) | `docs/context/C9.md` |

Module batches: `F1` = T6.1-F + T7.1 + T7.2, `F2` = T7.3 + T7.4 + T7.5,
`F3` = T7.6 + T8.3-F + T9.3-F. Commit messages are in `docs/task-ownership.md` §2.

## 2. Files you may edit

```
frontend/src/**
frontend/package.json
frontend/.env.example
frontend/README.md
frontend/log-f.md
frontend/AGENTS.md
frontend/SETUP.md
```

You may also change **your own task markers** in root `../whole_plan.md`.
You may **not** edit `../backend/`, `../middleware/`, `../docs/`, or generated copies
(`frontend/whole_plan.md`, `frontend/docs/**`).

## 3. Read order for every task

1. This file.
2. `frontend/SETUP.md`.
3. Your task block in `whole_plan.md`.
4. The context pack listed above.
5. The exact code files listed in that pack.

Stop and ask if the pack lists a file that does not exist, or the API shape you need is
not in `docs/api-contract.md`.

## 4. Fixed contracts (do not invent fields)

- `docs/api-contract.md` — every request/response shape, enum, and error code.
- `docs/decisions.md` — chain ID, order ID formula, money format, ALU levels.
- `docs/checks.md` — the six checks and decision mapping.

Rules that matter on the frontend:

- Money is a **decimal wei string** in the API. Use `BigInt`, never `Number`.
- `chain_order_id = ethers.id("landmarket-order:" + String(order.id))`.
- Missing `VITE_ESCROW_ADDRESS` must show a warning, not crash.
- Demo banner text must be exactly: `Testnet only, not a legal title transfer.`
- Never display a fake tx hash, run ID, evidence hash, or source URL.
- Show all six check results in the fixed order from `docs/checks.md`.

## 5. Commands (from repo root)

```bash
npm --prefix frontend run dev
npm --prefix frontend run typecheck
npm --prefix frontend run build
npm --prefix frontend run preview
```

To test against live services, start backend and middleware first (see `SETUP.md`).

## 6. Definition of done

- [ ] Code uses only documented endpoints and enums.
- [ ] `npm --prefix frontend run typecheck && npm --prefix frontend run build` pass.
- [ ] Loading, error, empty states exist for every new data view.
- [ ] No fake data, fake hash, or invented source URL.
- [ ] `frontend/log-f.md` updated with date/time/session and exact commands.
- [ ] Your task marker in `../whole_plan.md` is `[.]`.
- [ ] `npm run sync:docs && npm run check:docs` pass.
- [ ] Commit uses the batch message from `docs/task-ownership.md`.

## 7. Stop conditions

Stop and write `**BLOCKED:**` in the task block + log if:

- the backend endpoint or response shape is missing from `docs/api-contract.md`,
- a dependency task is not merged and the pack does not say "mock it",
- a package is not in `package.json` and you are about to add a new dependency,
- you need to edit another module,
- a test needs a real wallet, key, or TxHash you do not have.

Ask the lead with: task ID, what you tried, exact error, smallest unblock.
