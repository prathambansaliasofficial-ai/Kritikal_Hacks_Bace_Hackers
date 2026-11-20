# Project status

**As of 2026-11-20.** This file is the current status. The progress header inside
`whole_plan.md` was last edited on 2026-10-29 and is out of date; the task markers in
`whole_plan.md` are still correct.

## Delivery state

- All module branches (`backend/yash`, `frontend/sumit`, `middleware/tanya`, `lead/review-loop`, `integration/mvp`) are merged into `main` through PRs #1 to #5. The old `blue`, `red` and `yellow` baseline branches were deleted.
- 37 of 43 roadmap tasks are done, about 86 percent.

## By area

| Area | Done | Open |
|---|---|---|
| Backend | All planned tasks (data model, parcels/ALUs/bundles, evidence, review, users/KYC stub, listings, orders, six checks, settlement calls, ALU locking, integration tests, hardening) | None |
| Frontend | All planned tasks (map layers, evidence review, wallet connect, buy flow, trade status, production build) | No automated frontend tests; typecheck and build only |
| Middleware | Escrow contract, settle/refund/status API, local deploy and chain smoke test, TinyFish evidence module with mock tests | `T3.1` live TinyFish run (needs key), `T6.3` Sepolia deploy (needs keys), `T9.2` multi-portal evidence (optional) |
| Lead and docs | Architecture, keys guide, demo script, submission checklist, deployment guide (this update) | `T8.2` one-command `scripts/demo.sh` and `make demo`; `T9.3-D` actual public deployment |

## What still needs the owner's keys

| Task | Needs | Guide |
|---|---|---|
| `T3.1` TinyFish live proof | TinyFish API key | `docs/keys-tinyfish.md` |
| `T6.3` Sepolia deploy | Sepolia RPC URL, throwaway operator wallet with test ETH | `docs/keys-sepolia.md` |
| Full APPROVED demo | Both of the above | `docs/demo-script.md` |

## Known caveats

- Test counts in the logs (126 backend unit tests) were not re-run for this update.
- `docs/deployment.md` and the `check:env` script were written without being run on a live deployment.
- See `docs/limitations.md` for what is intentionally not real.
