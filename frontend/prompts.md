# prompts.md — Frontend (Sumit / `frontend/<name>` branch)

Roles: **Sumit** = frontend owner. **Paradew** = senior head on `main` (merge/supervise only). **Tanya** = middleware. **Yash** = backend.

### PLAYRULES (applies to all teammates — from deleted PLAYRULES.MD)
- Sirf apne module folder mein kaam karo — doosre module ka code mat chhedo
- main par kabhi direct push mat karo — apni branch par push karo, PR kholo, lead merge karega
- Task ID order mein kaam karo, skip mat karo
- `npm run sync:docs && npm run check:docs` har batch ke baad chalao
- Koi fake API key, fake TxHash, ya government record mat dalo

---

## MASTER PROMPT (NEVER comment out this block)

I am Sumit, working on the `frontend/<name>` branch of the Land Market monorepo. You are my AI for frontend work only.

STRICT SCOPE:
- Work ONLY inside `frontend/`. You may edit: `frontend/src/**`, `frontend/package.json`, `frontend/.env.example`, `frontend/README.md`, `frontend/log-f.md`, `frontend/AGENTS.md`, `frontend/SETUP.md`.
- You may change YOUR OWN task markers in root `../whole_plan.md` (set `[]` → `[.]`).
- You may NOT edit `../backend/`, `../middleware/`, `../docs/`, or generated copies (`frontend/whole_plan.md`, `frontend/docs/**`).
- Never touch `main`. Work only on `frontend/<name>`.

Read order for every task:
1. `frontend/AGENTS.md` (this file's rules).
2. `frontend/SETUP.md`.
3. Your task block in root `whole_plan.md`.
4. The context pack listed for your batch (`docs/context/C7A.md`, `C7B.md`, `C6.md`, `C8.md`, `C9.md`).
5. The exact code files listed in that pack.

Fixed contracts (do not invent fields):
- `docs/api-contract.md` — every request/response shape, enum, error code.
- `docs/decisions.md` — chain ID, order ID formula, money format, ALU levels.
- `docs/checks.md` — the six checks and decision mapping.

Frontend rules that matter:
- Money is a decimal wei string in the API. Use `BigInt`, never `Number`.
- `chain_order_id = ethers.id("landmarket-order:" + String(order.id))`.
- Missing `VITE_ESCROW_ADDRESS` must show a clear warning, NOT crash.
- Demo banner text exactly: `Testnet only, not a legal title transfer.`
- Never display a fake tx hash, run ID, evidence hash, or source URL.
- Show all six check results in the fixed order from `docs/checks.md`.
- Demo data carries `demo: true` (API) / `DEMO_FIXTURE_NOT_OFFICIAL` (DB).

Definition of done (every task):
- [ ] Code uses only documented endpoints and enums.
- [ ] `npm --prefix frontend run typecheck && npm --prefix frontend run build` pass.
- [ ] Loading, error, empty states exist for every new data view.
- [ ] No fake data, fake hash, or invented source URL.
- [ ] `frontend/log-f.md` updated with date/time (IST)/session and exact commands.
- [ ] Your task marker in `../whole_plan.md` is `[.]`.
- [ ] `npm run sync:docs && npm run check:docs` pass.
- [ ] Commit uses the batch message from `docs/task-ownership.md` §2 (only after all 3 tasks of the batch).

Stop conditions — write `**BLOCKED:**` in the task block + `frontend/log-f.md` and ask Paradew:
- Backend endpoint / response shape missing from `docs/api-contract.md`.
- Dependency task not merged and pack does not say "mock it".
- About to add a package not in `package.json`.
- Need to edit another module.
- Test needs a real wallet, key, or TxHash you don't have.

Commands (from repo root):
- `npm --prefix frontend run dev`
- `npm --prefix frontend run typecheck`
- `npm --prefix frontend run build`
- `npm --prefix frontend run preview`

---

## PROMPT BLOCKS (comment out each block when its task/batch is done)
Rule: When a prompt block below is completed, wrap its entire block in HTML comments `<!-- ... -->`. Keep the MASTER PROMPT above uncommented at all times. Commit only after all 3 tasks of a batch are done.

<!-- PROMPT: FRONTEND — Batch F1 (T6.1-F, T7.1, T7.2) — START -->
I am Sumit on `frontend/<name>`. Complete batch F1 = T6.1-F, T7.1, T7.2. Commit message: `feat(web): add chain config, map layers and evidence review`.

Read: root `whole_plan.md` Phase 6 (T6.1-F) and Phase 7 (T7.1–T7.2), `docs/context/C6.md`, `docs/context/C7A.md`, `docs/api-contract.md`, `docs/decisions.md`, `docs/checks.md`.

T6.1-F — Deploy address + ABI frontend slice:
1. Copy escrow ABI artifact to `frontend/src/lib/escrowAbi.json`.
2. `frontend/src/lib/chain.ts`: read `VITE_ESCROW_ADDRESS`, `VITE_CHAIN_ID`, `VITE_CHAIN_NAME`, `VITE_EXPLORER_URL`; missing address → clear UI warning, no crash.
3. Update `frontend/.env.example`.
Done: local deploy → frontend can use contract address + ABI. Verify: `npm --prefix frontend run typecheck && npm --prefix frontend run build`.

T7.1 — Map parcel + ALU layers:
1. `frontend/src/lib/api.ts`: typed `fetchParcel`, `fetchAlus`, `fetchListings`.
2. MapLibre sources/layers: parcel fill + outline, ALU grid lines, selected highlight.
3. Zoom → ALU level: 10+→1km, 14+→100m, 17+→10m, 20+→1m.
4. `DEMO-ULPIN-001` auto-load; click popup shows ULPIN/ALU ID.
5. Loading/error/empty states.
Done: demo parcel + ALUs on map; build pass.

T7.2 — Officer evidence + review UI:
1. 21-field evidence table, status chips (AVAILABLE/PARTIAL/N/A/N/D), source links, run ID, evidence hash.
2. Review queue list + Approve/Reject buttons with reason input.
3. Hash copy button; sources clickable.
4. Error states: middleware down, missing key, no evidence.
Done: officer demo flow works from UI.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `frontend/log-f.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add frontend/ whole_plan.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(web): add chain config, map layers and evidence review"`.
- Push: `git push -u origin frontend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: FRONTEND — Batch F1 — END -->

<!-- PROMPT: FRONTEND — Batch F2 (T7.3, T7.4, T7.5) — START -->
I am Sumit on `frontend/<name>`. Complete batch F2 = T7.3, T7.4, T7.5. Commit message: `feat(web): add wallet, buy flow and trade status`.

Read: root `whole_plan.md` Phase 7 (T7.3–T7.5), `docs/context/C7B.md`, `docs/api-contract.md`, `docs/decisions.md`, `docs/checks.md`. Depends on T4.3, T5.2, C6 (backend/middleware must be merged or mocked per contract).

T7.3 — Citizen wallet connect + chain switch:
1. `frontend/src/lib/wallet.ts`: `window.ethereum` connect, chain switch/add (local 31337), account change listener; no wallet → clear message.
2. Shortened address + disconnect/reset UI.
3. No buy transaction yet (buy is T7.4).
Done: wallet connect/disconnect + chain switch works.

T7.4 — Listing browse + buy flow:
1. `frontend/src/components/ListingCard.tsx`: bundle, ULPIN, price, seller KYC badge, ALU count.
2. Buy sequence exactly: `POST /orders` → `ethers.id("landmarket-order:" + id)` → `createOrder(...)` with value → wait receipt → `POST /orders/{id}/funded` → `POST /orders/{id}/evaluate` → poll `GET /orders/{id}`.
3. Disable button while pending; wrong chain → switch prompt.
Done: end-to-end buy on local chain.

T7.5 — Trade status panel:
1. `frontend/src/components/TradeStatus.tsx`: six check rows (pass/fail/reason/blocking), decision, order state, chain state, tx hash, explorer link.
2. `NEEDS_REVIEW` → show "officer review", do not claim settle.
3. Refresh button + clear timeout message.
Done: status panel shows all contract fields.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `frontend/log-f.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add frontend/ whole_plan.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(web): add wallet, buy flow and trade status"`.
- Push: `git push -u origin frontend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: FRONTEND — Batch F2 — END -->

<!-- PROMPT: FRONTEND — Batch F3 (T7.6, T8.3-F, T9.3-F) — START -->
I am Sumit on `frontend/<name>`. Complete batch F3 = T7.6, T8.3-F, T9.3-F. Commit message: `feat(web): polish, harden and add production container`.

Read: root `whole_plan.md` Phase 7 (T7.6), Phase 8 (T8.3-F), Phase 9 (T9.3-F), `docs/context/C7B.md`, `docs/context/C8.md`, `docs/context/C9.md`.

T7.6 — Empty/error states, banner, responsive polish:
1. Loading/empty/error for map, listings, reviews, trade.
2. Accessible labels, focus-visible styles, disabled buttons, `aria-live` status.
3. Banner: `Testnet only, not a legal title transfer.`
4. Demo badge `DEMO_FIXTURE_NOT_OFFICIAL`; responsive at 375px and 1280px.
5. Vite chunk warning fix or document.
Done: no horizontal scroll; states covered; banner visible.

T8.3-F — Frontend quality gate:
1. `npm --prefix frontend run typecheck`, `build`, `audit --omit=dev`.
2. Accessibility basics, focus states, disabled buttons.
3. Chunk warning fix or documented.
4. README final frontend commands.
Done: build pass.

T9.3-F — Frontend Dockerfile (stretch):
1. `frontend/Dockerfile` (static build + serve).
2. Public demo env/API base check.
Done: Dockerfile present.

After all 3 tasks:
- Update each task marker in root `../whole_plan.md` to `[.]`. Move blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
- Update `frontend/log-f.md`: each item `[.]` with date/time (IST)/session.
- Run `npm run sync:docs && npm run check:docs`.
- Stage only: `git add frontend/ whole_plan.md` (NEVER `git add -A`).
- Commit: `git commit -m "feat(web): polish, harden and add production container"`.
- Push: `git push -u origin frontend/<name>`. Open PR. Never push `main`.
- Report: commit hash, tasks closed, any blockers.
<!-- PROMPT: FRONTEND — Batch F3 — END -->
