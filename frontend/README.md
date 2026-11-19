# Land Market frontend

React 19 + TypeScript + Vite + MapLibre GL.

```bash
npm install
npm run dev          # http://localhost:5173
npm run typecheck    # tsc --noEmit
npm run build        # typecheck + vite build
npm run preview
npm run audit --omit=dev   # npm audit (dev deps excluded)
```

## Env

Copy `frontend/.env.example` to `frontend/.env` and set:

| Variable | Default | Meaning |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | FastAPI backend |
| `VITE_ESCROW_ADDRESS` | empty | escrow contract address (T6.1-F) |
| `VITE_CHAIN_ID` | `31337` | local Hardhat chain |
| `VITE_CHAIN_NAME` | `Hardhat Local` | wallet display name |
| `VITE_EXPLORER_URL` | empty | block explorer link |
| `VITE_OFFICER_TOKEN` | empty | prototype review token (T7.2) |

Missing `VITE_ESCROW_ADDRESS` shows a visible warning banner, it does not crash.

## What it ships

- Map parcel + ALU layers (MapLibre, `lm-*` source/layer IDs), zoom → ALU level, `DEMO-ULPIN-001` auto-load, click popup.
- Officer evidence panel (21 fields) + review queue (approve/reject).
- Citizen wallet connect + chain switch (`window.ethereum`, local 31337).
- Listings browse + buy flow: `POST /orders` → `ethers.id("landmarket-order:" + id)` → `createOrder(...)` with `value` → `/funded` → `/evaluate` → poll `GET /orders/{id}`.
- Trade status panel: six checks (fixed order), decision, order/chain state, tx hash, explorer link, `NEEDS_REVIEW` → officer review.
- Demo banner: `Testnet only, not a legal title transfer.` (`DEMO_FIXTURE_NOT_OFFICIAL` badge on demo data).

## Accessibility

- `focus-visible` outline on interactive elements.
- Disabled buttons while pending / not listed.
- `aria-live="polite"` status regions; accessible labels on inputs and buttons.

## Bundle chunk warning

The production JS bundle is ~1.5 MB after minification and exceeds Vite's 500 kB chunk-size warning limit. The app is a single-page demo shell, so code-splitting was not introduced; the warning is documented here. To resolve, split `ListingCard`/`TradeStatus`/evidence/review into dynamic `import()` chunks or raise `build.chunkSizeWarningLimit` in `vite.config.ts`.
