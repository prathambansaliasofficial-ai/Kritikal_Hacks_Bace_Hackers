# Demo payment mode (no wallet, no gas, no payment gateway)

Use this when you need to present the project quickly. The buyer's payment into escrow is
**simulated** inside the middleware. Nothing touches a blockchain, MetaMask, a faucet or any
payment service. Real mode (Hardhat or Sepolia) is unchanged and is the default.

## What is simulated and what is still real

| Part | In demo payment mode |
|---|---|
| Buyer paying into escrow | **Simulated.** An in-memory escrow in the middleware records the order as Funded |
| Settle / refund | **Simulated.** Moves the in-memory order to Settled or Refunded and returns a fake transaction hash |
| Evidence (TinyFish), database, six checks, order states, listings, KYC stub | **Real** |
| Money | **None.** No ETH, no rupees |

Say this out loud when you present: *"The escrow is simulated for the demo; the real contract is in `middleware/contracts` and runs on a testnet."* The transaction hashes are fake and will not open on any explorer.

## Limits you should know

- **A TinyFish key is still needed.** An order can only be created for a parcel that has an evidence sheet (the order stores its evidence hash). Get the key with `docs/keys-tinyfish.md`. Without it, the buy flow stops at "Evidence hash not set on order".
- **The outcome depends on the evidence.** `ZONING_OK` reads the zoning TinyFish returned. If it fails you will see `REJECTED` (refund) or `NEEDS_REVIEW` instead of `APPROVED`. All three are valid things to show, but check once before the demo.
- **Escrow state is in memory.** If you restart the middleware, orders that were funded before the restart are forgotten. Make a fresh order after a restart.
- **Never enable it in a public deployment.** It exists only for presentations.

## Setup (about 20 minutes)

### 1. Env files

```bash
cp backend/.env.example backend/.env
cp middleware/.env.example middleware/.env
cp frontend/.env.example frontend/.env
```

Set these values:

| File | Variable | Value |
|---|---|---|
| `middleware/.env` | `DEMO_PAYMENT` | `true` |
| `middleware/.env` | `TINYFISH_API_KEY` | your TinyFish key |
| `backend/.env` | `DEV_OFFICER_TOKEN` | any random string |
| `frontend/.env` | `VITE_DEMO_PAYMENT` | `true` |
| `frontend/.env` | `VITE_DEMO_BUYER_WALLET` | `0x1111111111111111111111111111111111111111` (any made-up address; no real wallet needed) |
| `frontend/.env` | `VITE_OFFICER_TOKEN` | same as `DEV_OFFICER_TOKEN` (local demo only) |

Then check:

```bash
npm run check:env -- demo
```

### 2. Start everything (3 terminals, see `SETUP.md` section 6)

Database first: `make db-up`, then `make db-reset` and `make seed`. Then run the backend, `npm run dev:middleware` and `npm run dev:frontend`.

Open the middleware `/health` endpoint (port 8090). You want `demoPayment: true` and `chainConfigured: true`. The frontend top bar shows a "DEMO PAYMENT MODE" banner.

### 3. Create the demo seller, buyer and listing

Open the backend API page at `http://127.0.0.1:8000/docs` and run these in order (each endpoint has a "Try it out" button). Use the same buyer address you put in `VITE_DEMO_BUYER_WALLET`.

1. `POST /api/v1/users` with `{"wallet_address":"0x2222222222222222222222222222222222222222","role":"CITIZEN"}` (seller).
2. `POST /api/v1/users` with `{"wallet_address":"0x1111111111111111111111111111111111111111","role":"CITIZEN"}` (buyer).
3. `POST /api/v1/users/{wallet}/kyc` for **both** wallets, header `X-Officer-Token` = your officer token, body `{"status":"VERIFIED","reason":"demo KYC"}`.
4. `POST /api/v1/bundles` with `{"ulpin":"DEMO-ULPIN-001","name":"Demo south bundle","alu_ids":["ALU-10m-DEMO-001","ALU-10m-DEMO-002"],"created_by":"0x2222222222222222222222222222222222222222"}`. Note the returned `id`.
5. `PATCH /api/v1/bundles/{id}` with `{"status":"ACTIVE"}`.
6. `POST /api/v1/listings` with `{"bundle_id":<id>,"seller_wallet":"0x2222222222222222222222222222222222222222","price_wei":"10000000000000000"}`. Note the listing `id`.
7. `PATCH /api/v1/listings/{id}` with `{"status":"LISTED"}`.
8. `POST /api/v1/verifications` with `{"ulpin":"DEMO-ULPIN-001"}`. This runs the real TinyFish agent and can take a few minutes. (You can also do it from the frontend's "Officer verification" form.)
9. Optional: approve the evidence in the frontend's Review Queue, or with `POST /api/v1/reviews/{evidence_id}/decision`.

If the ALU ids in step 4 are rejected, list the real ones with `GET /api/v1/alus` (bbox and level `10m`) and use two of those.

## The demo itself

1. Open the frontend. Point at the banner, the map and the ALU grid.
2. Show the evidence sheet (21 fields, sources, hash).
3. Show the listing card and press **Buy**. There is no wallet popup in demo mode.
4. Watch the status: order created, simulated payment, six checks, decision.
5. Show the final state (`SETTLED` on approval, `REFUNDED` on rejection) and the checks list.
6. Reset for another run: `make db-reset && make seed`, redo step 3, and restart the middleware.

## Switching back to real payments

Remove `DEMO_PAYMENT` from `middleware/.env` (or set it to `false`) and `VITE_DEMO_PAYMENT` from `frontend/.env`, then follow `docs/keys-local.md` or `docs/keys-sepolia.md`. The middleware refuses demo payments when the flag is off.

## How it works

- Middleware: with `DEMO_PAYMENT=true`, `settle`, `refund` and `status` use an in-memory map, and `POST /escrow/demo-fund` records the funding. With the flag off, `demo-fund` returns 403.
- Backend: `POST /api/v1/orders/{id}/demo-pay` calls the middleware, then marks the order `FUNDED` with the simulated hash. The six checks and settlement run exactly as in real mode.
- Frontend: with `VITE_DEMO_PAYMENT=true`, **Buy** skips MetaMask and calls `demo-pay`.
