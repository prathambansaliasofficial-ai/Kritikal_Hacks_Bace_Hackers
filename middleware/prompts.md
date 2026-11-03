# prompts.md — Middleware (Tanya / `middleware/<name>` or `ai/<name>` branch)

Roles: **Tanya** = middleware owner. **Paradew** = senior head on `main` (merge/supervise only). **Sumit** = frontend. **Yash** = backend.

### PLAYRULES (applies to all teammates — from deleted PLAYRULES.MD)
- Sirf apne module folder mein kaam karo — doosre module ka code mat chhedo
- main par kabhi direct push mat karo — apni branch par push karo, PR kholo, lead merge karega
- Task ID order mein kaam karo, skip mat karo
- `npm run sync:docs && npm run check:docs` har batch ke baad chalao
- Koi fake API key, fake TxHash, ya government record mat dalo

---

## MASTER PROMPT (NEVER comment out this block)

I am Tanya, working on the `middleware/<name>` branch (or `ai/<name>` for TinyFish prompt/agent work) of the Land Market monorepo. You are my AI for middleware work only.

STRICT SCOPE:
- Work ONLY inside `middleware/`. Allowed (middleware engineer): `middleware/src/**`, `middleware/contracts/**`, `middleware/scripts/**`, `middleware/test/**`, `middleware/package.json`, `middleware/hardhat.config.ts`, `middleware/.env.example`, `middleware/README.md`, `middleware/log-m.md`, `middleware/AGENTS.md`, `middleware/SETUP.md`, `Makefile` (only T6.2), `docs/tinyfish-smoke.md` (only T3.1), `docs/deployments.md` (only T6.3).
- AI / TinyFish branch (`ai/<name>`) may edit only: `middleware/src/tinyfish/**`, `middleware/scripts/smoke-tinyfish.ts`, `middleware/tests/**` (AI-related tests only). AI may NOT edit: `middleware/src/server.ts`, `middleware/src/blockchain/**`, `middleware/contracts/**`, `middleware/scripts/deploy.ts`, `../backend/**`, `../frontend/**`.
- You may change YOUR OWN task markers in root `../whole_plan.md` (set `[]` → `[.]`).
- You may NOT edit `../frontend/`, `../backend/`, other root docs, or generated copies (`middleware/whole_plan.md`, `middleware/docs/**`).
- Never touch `main`. Work only on `middleware/<name>` or `ai/<name>`.

Read order for every task:
1. `middleware/AGENTS.md` + `middleware/SETUP.md`.
2. Your task block in root `whole_plan.md`.
3. The context pack for your batch (`docs/context/C3.md` … `C9.md`).
4. `docs/api-contract.md`, `docs/decisions.md`, `docs/checks.md`.

Fixed contracts (do not invent fields):
- `docs/api-contract.md` — `POST /verify/evidence`, `POST /escrow/settle`, `POST /escrow/refund`, `GET /escrow/status/{orderId}`.
- `docs/decisions.md` — evidence hash, order ID formula, chain IDs, money.
- `docs/checks.md` — middleware does not decide trades; backend does.

Middleware rules that matter:
- Error body is `{"error": string}`; backend uses `{"detail": string}`.
- Never invent a run ID, source URL, TxHash, or evidence value.
- `POST /verify/evidence` returns the real 21-field sheet or a 502.
- `GET /escrow/status` returns `{orderId, state, label}`; invalid bytes32 = 400, chain error = 502.
- Operator key only for `settle`/`refund`; never log or commit it.
- Testnet only; no mainnet funds.
- Demo data carries `demo: true`.

Definition of done (every task):
- [ ] Code matches the task block and `docs/api-contract.md`.
- [ ] `typecheck`, `compile`, and `test` pass.
- [ ] No fake run ID, TxHash, key, or source URL.
- [ ] `.env` is not staged; `.env.example` lists every new variable.
- [ ] `middleware/log-m.md` updated with date/time (IST)/session and exact commands.
- [ ] Your task marker in `../whole_plan.md` is `[.]`.
- [ ] `npm run sync:docs && npm run check:docs` pass.
- [ ] Commit uses the batch message from `docs/task-ownership.md` §2 (only after all 3 tasks of the batch).

Stop conditions — write `**BLOCKED:**` in the task block + `middleware/log-m.md` and ask Paradew:
- `TINYFISH_API_KEY` missing (T3.1 stays `[]`; never fake a run).
- Sepolia key/RPC missing (T6.3 stays `[]`).
- Chain/contract call needs a change to `LandMarketEscrow.sol` that changes the backend contract.
- Need to edit `frontend/` or `backend/`.
- Real portal blocks run with CAPTCHA (document it, try alternate source, then ask lead).

Commands (from repo root):
- `npm --prefix middleware install`
- `npm --prefix middleware run typecheck`
- `npm --prefix middleware run compile`
- `npm --prefix middleware test`
- `npm --prefix middleware run dev`
- `npm --prefix middleware run smoke:tinyfish`
- `npm --prefix middleware run node`
- `npm --prefix middleware run deploy:local`

---

## PROMPT BLOCKS (comment out each block when its task/batch is done)
Rule: When a prompt block below is completed, wrap its entire block in HTML comments `<!-- ... -->`. Keep the MASTER PROMPT above uncommented at all times. Commit only after all 3 tasks of a batch are done.

<!-- PROMPT: MIDDLEWARE — Batch M1 (T3.1, T5.3-M, T6.1-M) — START -->
I am Tanya on `middleware/<name>`. Complete batch M1 = T3.1, T5.3-M, T6.1-M. Commit message: `feat(evidence): add live proof, escrow status and deploy artifacts`.

Read: root `whole_plan.md` Phase 3 (T3.1), Phase 5 (T5.3-M), Phase 6 (T6.1-M), `docs/context/C3.md`, `docs/context/C5.md`, `docs/context/C6.md`, `docs/api-contract.md`, `docs/decisions.md`.

T3.1 — TinyFish live run proof (BLOCKED until `TINYFISH_API_KEY` arrives):
1. **BLOCKER:** get `TINYFISH_API_KEY` from human. Without key, keep task `[]`, never fake a run.
2. `middleware/.env`: add key (local only, never commit).
3. `npm --prefix middleware run smoke:tinyfish`.
4. Run on a real portal (BhuNaksha or officer-provided URL); note run ID, source URLs, status, latency.
5. `docs/tinyfish-smoke.md`: date, URL, goal, run ID, result summary, screenshot path. Key redacted — never commit.
6. CAPTCHA/block → document, try alternate source URL.
Files: `docs/tinyfish-smoke.md`, `middleware/.env` (local only), optionally `middleware/src/tinyfish/evidence.ts` goal tuning.
Done: real `COMPLETE` event + ≥1 real source URL documented. Verify: `npm --prefix middleware run smoke:tinyfish`.

T5.3-M — Escrow status endpoint (middleware slice):
1. `middleware/src/server.ts`: add `GET /escrow/status/:orderId` — reads contract `orderState` (0 None, 1 Funded, 2 Settled, 3 Refunded).
2. Invalid order ID → 400; chain error → 502.
3. Response exactly `{orderId, state, label}` per `docs/api-contract.md` §4.
Files: `middleware/src/server.ts`, `middleware/src/blockchain/escrow.ts`, middleware tests.
Done: `curl localhost:8090/escrow/status/<orderId>` returns correct state. Verify: local chain + curl.

T6.1-M — Deploy artifacts (middleware slice):
1. `middleware/scripts/deploy.ts`: after deploy, write `middleware/deployments/<network>.json` (address, chainId, deployer, operator, deployedAt).
2. Commit a small `middleware/deployments/localhost.json` example (no key), or document generation.
3. Commit addresses in docs; `.env` never committed.
Files: `middleware/scripts/deploy.ts`, `middleware/deployments/`.
Done: local deploy → address file ready. Verify: `npm --prefix middleware run deploy:local`.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`. If T3.1 is blocked, leave it `[]` with `**BLOCKED:**` and only close T5.3-M/T6.1-M.
- Update `middleware/log-m.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add middleware/ whole_plan.md docs/tinyfish-smoke.md docs/deployments.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(evidence): add live proof, escrow status and deploy artifacts"`.
- Push: `git push -u origin middleware/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers (especially T3.1 key).
<!-- PROMPT: MIDDLEWARE — Batch M1 — END -->

<!-- PROMPT: MIDDLEWARE — Batch M2 (T6.2, T6.3, T9.2) — START -->
I am Tanya on `middleware/<name>`. Complete batch M2 = T6.2, T6.3, T9.2. Commit message: `feat(chain): add local smoke, sepolia and multi-portal evidence`.

Read: root `whole_plan.md` Phase 6 (T6.2, T6.3), Phase 9 (T9.2), `docs/context/C6.md`, `docs/context/C9.md`, `docs/api-contract.md`, `docs/decisions.md`. T6.3 BLOCKED until funded Sepolia deployer key + RPC URL. T9.2 is AI-owned (`ai/<name>`) — middleware engineer does not do T9.2 unless you are the AI teammate.

T6.2 — Local chain smoke test:
1. `middleware/scripts/chain-smoke.ts`: buyer `createOrder`, operator `settle`, `orderState` check, events verify.
2. Add `npm run chain:smoke` script; Hardhat node assumed or spawned.
3. Root `Makefile` target `chain`: node start + deploy + smoke.
4. `middleware/README.md`: local chain steps.
Files: `middleware/scripts/chain-smoke.ts`, `middleware/package.json`, `Makefile`, `middleware/README.md`.
Done: `npm --prefix middleware run chain:smoke` passes.

T6.3 — Sepolia deploy + record (BLOCKED until funded Sepolia key + RPC):
1. **BLOCKER:** get funded Sepolia deployer key + RPC URL from human. Keep `[]` until then.
2. `npm --prefix middleware run deploy:sepolia`; address + tx link → `docs/deployments.md`.
3. `middleware/.env`: Sepolia address; check `GET /escrow/status`.
4. Key never committed or logged.
Files: `docs/deployments.md`, `middleware/.env` (local only).
Done: Sepolia address + block explorer link documented; status call works. Verify: `curl localhost:8090/escrow/status/<orderId>`.

T9.2 — Multi-portal evidence + confidence (AI branch `ai/<name>` only):
1. `middleware/src/tinyfish/portals.ts`: 7-portal registry.
2. Per-portal TinyFish run; field-level merge.
3. Source conflict → `NEEDS_REVIEW`; confidence score in evidence sheet.
4. Tests: AI tests only.
Files: `middleware/src/tinyfish/portals.ts`, `middleware/src/tinyfish/merge.ts`, AI tests; backend contract change only via lead.
Done: ≥2 portals merged; conflicts go to review.

After all 3 tasks (or the unblocked ones):
- Update each task marker in root `../whole_plan.md` to `[.]`. Move done blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`. Leave blocked tasks `[]` with `**BLOCKED:**`.
- Update `middleware/log-m.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add middleware/ whole_plan.md docs/deployments.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(chain): add local smoke, sepolia and multi-portal evidence"`.
- Push: `git push -u origin middleware/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers (T6.3 key/RPC).
<!-- PROMPT: MIDDLEWARE — Batch M2 — END -->

<!-- PROMPT: MIDDLEWARE — Batch M3 (T8.3-M, T9.3-M) — START -->
I am Tanya on `middleware/<name>`. Complete batch M3 = T8.3-M, T9.3-M. Commit message: `chore(middleware): harden and add production container`.

Read: root `whole_plan.md` Phase 8 (T8.3-M), Phase 9 (T9.3-M), `docs/context/C8.md`, `docs/context/C9.md`. T8.3-M depends on T6.3 (Sepolia).

T8.3-M — Middleware security/quality gate:
1. Secrets grep: `TINYFISH_API_KEY`, `OPERATOR_PRIVATE_KEY`, private keys — none in repo/logs.
2. `npm --prefix middleware run typecheck && npm --prefix middleware test && npm --prefix middleware run compile`.
3. `npm --prefix middleware audit --omit=dev`.
4. Confirm `.env` is ignored.
Done: all four commands pass; `.env` ignored.

T9.3-M — Middleware production container (stretch):
1. `middleware/Dockerfile`.
2. Host secrets via env; no key in image.
3. Chain RPC + TinyFish key from production env.
Done: Dockerfile present; secrets via env.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `middleware/log-m.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add middleware/ whole_plan.md` (NEVER `git add -A`).
- Commit: `git commit -m "chore(middleware): harden and add production container"`.
- Push: `git push -u origin middleware/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: MIDDLEWARE — Batch M3 — END -->
