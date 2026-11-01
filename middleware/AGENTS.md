# AGENTS.md — Middleware and AI module

**You own:** `middleware/`.  
**Branches:** `middleware/<your-name>` for service/chain work, `ai/<your-name>` for
TinyFish prompt/agent work. Never `main`.  
**Full rules:** `docs/team-workflow.md` · **Task map:** `docs/task-ownership.md`.

If you are an AI agent: read this file, `middleware/SETUP.md`, your task block in
`whole_plan.md`, and **only** the context pack for your batch. Do not scan other modules.

## 1. Your task queue

| Task | Owner | What it is | Context pack |
|---|---|---|---|
| `T3.1` | Middleware | real TinyFish run proof | `docs/context/C3.md` |
| `T5.3-M` | Middleware | `GET /escrow/status/{orderId}` | `docs/context/C5.md` |
| `T6.1-M` | Middleware | deploy writes `deployments/<network>.json` | `docs/context/C6.md` |
| `T6.2` | Middleware | local chain smoke test | `docs/context/C6.md` |
| `T6.3` | Middleware | Sepolia deploy + record | `docs/context/C6.md` |
| `T9.2` | AI | multi-portal evidence + confidence (stretch) | `docs/context/C9.md` |
| `T8.3-M` | Middleware | middleware quality gate | `docs/context/C8.md` |
| `T9.3-M` | Middleware | middleware Dockerfile (stretch) | `docs/context/C9.md` |

Module batches: `M1` = T3.1/T5.3-M/T6.1-M, `M2` = T6.2/T6.3/T9.2,
`M3` = T8.3-M/T9.3-M. Commit messages are in `docs/task-ownership.md` §2.

## 2. AI / TinyFish branch rules

If you are the AI teammate, your branch is `ai/<your-name>` and you may edit only:

```
middleware/src/tinyfish/**
middleware/scripts/smoke-tinyfish.ts
middleware/tests/**            (only AI-related tests)
```

You may **not** edit:

```
middleware/src/server.ts
middleware/src/blockchain/**
middleware/contracts/**
middleware/scripts/deploy.ts
../backend/**
../frontend/**
```

Need a new response field? Update `docs/api-contract.md` with the lead first, then
ask the middleware owner to wire it. Do not change the backend or frontend yourself.

## 3. Files you may edit (middleware engineer)

```
middleware/src/**
middleware/contracts/**
middleware/scripts/**
middleware/test/**
middleware/package.json
middleware/hardhat.config.ts
middleware/.env.example
middleware/README.md
middleware/log-m.md
middleware/AGENTS.md
middleware/SETUP.md
Makefile                 (only T6.2)
docs/tinyfish-smoke.md   (only T3.1)
docs/deployments.md      (only T6.3)
```

You may also change **your own task markers** in root `../whole_plan.md`.
You may **not** edit `../frontend/`, `../backend/`, other root docs, or generated copies
(`middleware/whole_plan.md`, `middleware/docs/**`).

## 4. Fixed contracts (do not invent fields)

- `docs/api-contract.md` — `POST /verify/evidence`, `POST /escrow/settle`,
  `POST /escrow/refund`, `GET /escrow/status/{orderId}`.
- `docs/decisions.md` — evidence hash, order ID formula, chain IDs, money.
- `docs/checks.md` — the middleware does not decide trades; backend does.

Rules that matter on the middleware:

- Error body is `{"error": string}`; backend uses `{"detail": string}`.
- Never invent a run ID, source URL, TxHash, or evidence value.
- `POST /verify/evidence` returns the real 21-field sheet or a 502.
- `GET /escrow/status` returns `{orderId, state, label}`; invalid bytes32 = 400,
  chain error = 502.
- Operator key is only for `settle`/`refund`; never log or commit it.
- Testnet only; no mainnet funds.

## 5. Commands (from repo root)

```bash
npm --prefix middleware install
npm --prefix middleware run typecheck
npm --prefix middleware run compile
npm --prefix middleware test
npm --prefix middleware run dev
npm --prefix middleware run smoke:tinyfish
npm --prefix middleware run node
npm --prefix middleware run deploy:local
```

## 6. Definition of done

- [ ] Code matches the task block and `docs/api-contract.md`.
- [ ] `typecheck`, `compile`, and `test` pass.
- [ ] No fake run ID, TxHash, key, or source URL.
- [ ] `.env` is not staged; `.env.example` lists every new variable.
- [ ] `middleware/log-m.md` updated with date/time/session and exact commands.
- [ ] Your task marker in `../whole_plan.md` is `[.]`.
- [ ] `npm run sync:docs && npm run check:docs` pass.
- [ ] Commit uses the batch message from `docs/task-ownership.md`.

## 7. Stop conditions

Stop and write `**BLOCKED:**` in the task block + log if:

- `TINYFISH_API_KEY` is missing (T3.1 must stay `[]`; never fake a run),
- Sepolia key/RPC is missing (T6.3 stays `[]`),
- the chain/contract call needs a change to `LandMarketEscrow.sol` that changes the
  backend contract,
- you need to edit `frontend/` or `backend/`,
- a real portal blocks the run with CAPTCHA (document it, try an alternate source,
  then ask the lead).

Ask the lead with: task ID, what you tried, exact error, smallest unblock.
