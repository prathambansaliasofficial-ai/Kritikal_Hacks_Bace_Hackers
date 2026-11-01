# C7B — Buy flow, trade status and polish

**Tasks:** T7.4, T7.5, T7.6
**Owner:** Frontend. Branch: `frontend/<name>`. Commit batch: `C7B`.
**Read first (only):** this pack, `docs/api-contract.md` §2.4, §3 orders, §5,
`docs/decisions.md` §5–6, `frontend/src/lib/wallet.ts`, `frontend/src/lib/chain.ts`,
`frontend/src/lib/api.ts`, `frontend/src/App.tsx`.
**Do not read:** backend/middleware source, other logs.
**Depends on:** C7A, C4 (orders), C5 (evaluate/settlement), C6 (contract).

## T7.4 — Listing browse + buy

Create `ListingCard.tsx` and extend `TradeStatus.tsx`. Browse `LISTED` listings; show bundle,
ULPIN, price in ETH, seller KYC badge, ALU count.

Buy sequence (exact):

1. `POST /api/v1/orders {listing_id, buyer_wallet}` → order `CREATED`;
2. `chain_order_id = ethers.id("landmarket-order:" + String(order.id))`;
3. `createOrder(chainOrderId, seller, evidenceHash)` with `value = BigInt(order.amount_wei)`;
4. wait for receipt; `POST /api/v1/orders/{id}/funded {chain_order_id, tx_hash}`;
5. `POST /api/v1/orders/{id}/evaluate`;
6. poll `GET /api/v1/orders/{id}` until `SETTLED`/`REFUNDED` or timeout.

Use `evidence_hash` from the order/listing response; do not compute a fake one. Disable the
button while pending. Wrong chain => prompt to switch.

## T7.5 — Trade status

`TradeStatus.tsx` shows: six check rows with pass/fail/reason, blocking badge, decision,
order state, chain state, tx hash, and explorer link when configured. `NEEDS_REVIEW` shows
"officer review" and no settle claim. Add a refresh button and a clear timeout message.

## T7.6 — Empty/error states + demo banner

- loading/empty/error for map, listings, reviews, trade;
- accessible labels, focus-visible styles, disabled buttons, aria-live for status;
- visible banner: `Testnet only, not a legal title transfer.`
- demo badge: `DEMO_FIXTURE_NOT_OFFICIAL` on demo parcel/evidence;
- responsive at 375px and 1280px; no horizontal scroll;
- document the remaining Vite chunk-size warning if not code-split.

## Finish

- Update only your own task markers `[]` → `[.]`; the lead updates phase counters.
- Update your module log; run `npm run sync:docs && npm run check:docs`.
- Commit: `feat(web): add wallet buy flow, trade status and demo polish`
- Verify: manual local-chain buy + `npm --prefix frontend run typecheck && npm --prefix frontend run build`.
