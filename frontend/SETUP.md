# Frontend setup

React 19 + TypeScript + Vite + MapLibre. This file is only for the `frontend/` module.
Shared prerequisites and the full monorepo runbook are in `../SETUP.md`.

## 1. Env

```bash
cp frontend/.env.example frontend/.env
```

| Variable | Default | Meaning |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | FastAPI backend |
| `VITE_ESCROW_ADDRESS` | empty | escrow contract address (T6.1-F) |
| `VITE_CHAIN_ID` | `31337` | local Hardhat chain |
| `VITE_CHAIN_NAME` | `Hardhat Local` | wallet display name |
| `VITE_EXPLORER_URL` | empty | block explorer link |
| `VITE_OFFICER_TOKEN` | empty | prototype review token (T7.2) |

Missing contract address must show a visible warning, not crash the app.

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

Chain (only for T6.1-F onwards):

```bash
npm --prefix middleware run node
npm --prefix middleware run deploy:local
# copy the printed address into frontend/.env as VITE_ESCROW_ADDRESS
```

## 3. Checks

```bash
npm --prefix frontend run typecheck
npm --prefix frontend run build
npm --prefix frontend run preview
```

`build` already runs `tsc --noEmit`, so a type error fails the build.

## 4. Common errors

| Symptom | Fix |
|---|---|
| `fetch failed` / health pill red | backend is not running on `:8000` |
| `VITE_ESCROW_ADDRESS` warning | deploy the contract or paste the address in `.env` |
| wallet not found | install MetaMask or use a browser with `window.ethereum` |
| wrong network | use the in-app switch-to-chain button (T7.3) |
| map tiles blank | check network access to `demotiles.maplibre.org` |

## 5. Where the rules live

- API shapes: `docs/api-contract.md`
- Chain/order IDs/money: `docs/decisions.md`
- Six checks/decision: `docs/checks.md`
- Your task order: `AGENTS.md`

Do not add a new API field in the frontend only. Ask the backend owner and update the
root contract first.
