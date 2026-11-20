# Submission checklist

Tick each item before final delivery. Items marked (key) need your own keys; see `docs/api-keys-setup.md`.

## Repository

- [ ] Everything is on `main`; old role branches were removed.
- [ ] No secrets in the repo: `git ls-files` shows no `.env` file and no private key or API key in any tracked file.
- [ ] GitHub secret scanning and push protection are enabled.
- [ ] `README.md` and `SETUP.md` match the real commands.
- [ ] `docs/limitations.md` is honest about demo data, KYC stub and testnet only.

## Proof of the real integrations

- [ ] (key) TinyFish live run recorded in `docs/tinyfish-smoke.md` (run ID, date, source URL, status). Roadmap task T3.1.
- [ ] (key) Escrow contract deployed to Sepolia; address, tx hash and explorer link in `docs/deployments.md`. Roadmap task T6.3.
- [ ] (key) One full buy flow completed on that deployment, with the settlement transaction hash recorded.

## Quality gates (run from the repo root)

- [ ] `npm run typecheck`
- [ ] `npm run check:docs`
- [ ] `npm run check:env` (and `npm run check:env -- sepolia`)
- [ ] `npm --prefix frontend run build`
- [ ] `npm --prefix middleware run compile` and `npm --prefix middleware test`
- [ ] `backend/.venv/bin/ruff check backend` and `backend/.venv/bin/pytest -q backend`
- [ ] `make test-integration` (needs the database running)
- [ ] `npm --prefix middleware audit --omit=dev` reviewed

## Demo material

- [ ] Demo rehearsed once end to end with `docs/demo-script.md`.
- [ ] Screen recording of the full flow (7 steps) saved as the fallback.
- [ ] Screenshots: map with ALU grid, evidence sheet, six checks, settled order with explorer link.
- [ ] Public demo URL, if any, and how it is protected (`docs/deployment.md`).

## Say it clearly in the submission

- [ ] Prototype only. Demo records are not official government data.
- [ ] A blockchain receipt is not a legal title transfer.
- [ ] Testnet only. No real money, no mainnet.
- [ ] KYC and the officer token are demo stubs.
