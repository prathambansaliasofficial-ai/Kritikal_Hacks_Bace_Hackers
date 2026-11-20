# Frontend setup

React 19 + TypeScript + Vite + MapLibre. This file is only for the `frontend/` module.
Shared prerequisites and the full monorepo runbook are in `../SETUP.md`; keys are in
`../docs/api-keys-setup.md`.

## 1. Env

```bash
cp frontend/.env.example frontend/.env
```

| Variable | Local default | Sepolia value | Meaning |
|---|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | your backend URL | FastAPI backend |
| `VITE_ESCROW_ADDRESS` | empty | deployed address | Escrow contract (same as middleware `ESCROW_CONTRACT_ADDRESS`) |
| `VITE_CHAIN_ID` | `31337` | `11155111` | Chain the wallet must be on |
| `VITE_CHAIN_NAME` | `Hardhat Local` | `Sepolia` | Wallet display name |
| `VITE_EXPLORER_URL` | empty | `https://sepolia.etherscan.io` | Block explorer base URL for tx links |
| `VITE_OFFICER_TOKEN` | empty | **leave empty** | Shows the officer review screen when set. Same value as backend `DEV_OFFICER_TOKEN`. **Public in the built site**, so use it for local demos only |

A missing contract address shows a visible warning, not a crash. Vite reads these values
at start and build time: restart `npm --prefix frontend run dev` (or rebuild) after editing.

## 2. Install and run

From the repo root:

```bash
npm --prefix frontend install
npm --prefix frontend run dev        # http://localhost:5173
```

The UI calls the backend at `VITE_API_BASE_URL`. Start these two services too:

```bash
backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000
npm run dev:middleware
```

Chain: deploy the contract (`../docs/keys-local.md` or `../docs/keys-sepolia.md`) and put the
address in `frontend/.env` as `VITE_ESCROW_ADDRESS`.

## 3. Checks

```bash
npm --prefix frontend run typecheck
npm --prefix frontend run build
npm --prefix frontend run preview
```

`build` already runs `tsc --noEmit`, so a type error fails the build.
There are no automated frontend tests; the checks above are the gate.

## 4. Common errors

| Symptom | Fix |
|---|---|
| `fetch failed` / health pill red | Backend is not running on `:8000`, or `VITE_API_BASE_URL` is wrong |
| Browser blocks calls (CORS) | Add this site's URL to `CORS_ORIGINS` in `backend/.env` |
| Escrow address warning | Set `VITE_ESCROW_ADDRESS` and restart the dev server |
| Wallet not found | Install MetaMask or use a browser with `window.ethereum` |
| Wrong network | Use the in-app switch-to-chain button, or switch in MetaMask |
| Review screen missing | `VITE_OFFICER_TOKEN` is empty (by design on public builds) |
| Map tiles blank | Check network access to `demotiles.maplibre.org` |

## 5. Where the rules live

- API shapes: `docs/api-contract.md`
- Chain/order IDs/money: `docs/decisions.md`
- Six checks/decision: `docs/checks.md`
- Your task order: `AGENTS.md`

Do not add a new API field in the frontend only. Ask the backend owner and update the
root contract first.
