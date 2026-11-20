# Demo script (7 steps)

Prototype only. Demo records are not official government data, and a blockchain receipt
is not a legal title transfer. Say this out loud at the start.

## Before the demo: one-time setup

1. Keys and chain: `docs/api-keys-setup.md` (local or Sepolia). Run `npm run check:env` (add `-- sepolia` for Sepolia) until there are no FAIL lines.
2. Start everything (see `SETUP.md` section 6): database, backend, middleware, frontend.
3. Load demo data: `make db-reset && make seed` (parcel `DEMO-ULPIN-001` and its ALUs).
4. Create the demo people and listing. Open the backend's API docs page at `http://127.0.0.1:8000/docs` and call, in order (shapes are in `docs/api-contract.md`):
   - `POST /api/v1/users` for the **seller** wallet and the **buyer** wallet (role `CITIZEN`).
   - `POST /api/v1/users/{wallet}/kyc` for both, header `X-Officer-Token` = your officer token, body status `VERIFIED`.
   - `POST /api/v1/bundles` with ULPIN `DEMO-ULPIN-001`, two ALU ids (for example `ALU-10m-DEMO-001` and `ALU-10m-DEMO-002`), `created_by` = seller wallet. Then `PATCH /api/v1/bundles/{id}` to make it `ACTIVE`.
   - `POST /api/v1/listings` for that bundle with the seller wallet and `price_wei` `10000000000000000` (0.01 ETH), then `PATCH /api/v1/listings/{id}` with status `LISTED`.
5. Run live evidence once so the trade can be approved: `POST /api/v1/verifications` with ULPIN `DEMO-ULPIN-001` (needs the TinyFish key). Approve it in the officer review step below.
6. Wallet: MetaMask on the right network with the **Buyer** account selected and funded.

## The 7 steps

| # | What you do | What to point out | Expected result |
|---|---|---|---|
| 1 | Open the frontend. Show the map and the demo parcel. | Parcel `DEMO-ULPIN-001` and its 100 m / 10 m ALU grid. | Map loads with parcel and ALU layers; health pill is green. |
| 2 | Show the verification of the ULPIN. | TinyFish collected a 21-field sheet; each field has a source, status and timestamp. Missing fields show `N/D`, not guesses. | Evidence sheet with an evidence hash and a TinyFish run ID. |
| 3 | Officer review (local demo only). | The officer approves or rejects the evidence. The rules never accept evidence on their own. | Evidence status changes after the decision. |
| 4 | Browse the active listing and its bundle of ALUs. | The bundle is intact: no ALU can be sold twice. | Listing shows price and the bundle's ALUs. |
| 5 | Connect the Buyer wallet and buy. | The buyer's wallet sends the order amount into the escrow contract. | MetaMask asks to confirm; the transaction hash appears. |
| 6 | Trigger evaluation and show the six checks. | `LISTED`, `BUNDLE_INTACT`, `KYC_WALLET`, `ZONING_OK`, `FUNDS_IN_ESCROW`, `TRADE_MATCH`. | All six pass: decision `APPROVED`. |
| 7 | Show settlement. | Approved trades call `settle()`; rejected ones call `refund()`; missing evidence goes to officer review with no chain call. | Order state `SETTLED` with a transaction hash linking to the explorer (Sepolia). |

## Fallbacks

| Problem | What to do |
|---|---|
| No TinyFish key or portal is down | Live verification returns `503`/`502` by design. Show the recorded run in `docs/tinyfish-smoke.md` and the saved evidence in the database. Without evidence, step 6 ends as `NEEDS_REVIEW`: explain that this is the safe path, not a bug. |
| Wallet or RPC problem | Switch to the local chain (`docs/keys-local.md`) and run the same steps. |
| Settlement did not run | Check the middleware log and that `OPERATOR_PRIVATE_KEY` equals the deployer key. |
| Everything fails | Show the recorded screen capture from the submission checklist. |

## Reset between runs

`make db-reset && make seed`, then redo setup step 4. On the local chain, restart the node and redeploy.
