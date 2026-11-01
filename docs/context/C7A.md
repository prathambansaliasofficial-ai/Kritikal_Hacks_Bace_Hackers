# C7A — Map, review UI and wallet connect

**Tasks:** T7.1, T7.2, T7.3
**Owner:** Frontend. Branch: `frontend/<name>`. Commit batch: `C7A`.
**Read first (only):** this pack, `docs/api-contract.md` §2–3 and §5,
`frontend/src/lib/api.ts`, `frontend/src/App.tsx`, `frontend/src/components/MapView.tsx`,
`frontend/src/index.css`, `frontend/src/lib/chain.ts`, `frontend/src/lib/escrowAbi.json`.
**Do not read:** backend/middleware source, other logs.
**Depends on:** C2 (parcels/ALUs), C3 (evidence/review), C4 (users), C6 (chain config).

## T7.1 — Parcel + ALU map

Extend `frontend/src/lib/api.ts` with typed:

```ts
fetchParcel(ulpin: string): Promise<ParcelFeature>
fetchAlus(bbox: BBox, level: AluLevel): Promise<FeatureCollection<AluFeature>>
fetchListings(status?: ListingStatus): Promise<{items: Listing[]}>
```

MapLibre: parcel fill + outline, ALU grid line layer, selected highlight. Zoom → level:
`>=20 → 1m`, `>=17 → 10m`, `>=14 → 100m`, `>=10 → 1km`, else no ALU layer.
Auto-load `DEMO-ULPIN-001`; click popup shows ULPIN / ALU ID. Add loading, error, empty states.
Use `source`/`layer` IDs prefixed `lm-`.

## T7.2 — Officer evidence + review

Create `EvidencePanel.tsx` and `ReviewQueue.tsx`. Evidence table renders all 21 fields with
status chips `AVAILABLE/PARTIAL/N/A/N/D`, source links, run ID, and copyable evidence hash.
Queue lists pending items; Approve/Reject opens a reason field; reject requires reason.
Send `X-Officer-Token` from `VITE_OFFICER_TOKEN` (add to `.env.example`; prototype only).
Errors: middleware down, missing key, empty evidence. Do not invent a field or source.

## T7.3 — Wallet connect + chain switch

Create `frontend/src/lib/wallet.ts`:

```ts
export async function connectWallet(): Promise<string>
export async function switchToConfiguredChain(): Promise<void>
export function onAccountsChanged(cb: (account: string | null) => void): () => void
```

Handle no `window.ethereum` with a clear message. Add/switch local chain `31337`
(name/RPC from `chainConfig`). Show shortened address and disconnect/reset. No buy transaction
yet; that is C7B.

## Finish

- Update only your own task markers `[]` → `[.]`; the lead updates phase counters.
- Update your module log; run `npm run sync:docs && npm run check:docs`.
- Commit: `feat(web): add map layers, evidence review and wallet connect`
- Verify: `npm --prefix frontend run typecheck && npm --prefix frontend run build`.
