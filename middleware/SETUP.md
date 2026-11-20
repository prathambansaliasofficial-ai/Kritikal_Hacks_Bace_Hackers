# Middleware setup

TinyFish evidence service + Fastify API + Hardhat escrow. This file is only for the
`middleware/` module. Shared prerequisites are in `../SETUP.md`; keys are in
`../docs/api-keys-setup.md`.

## 1. Env

```bash
cp middleware/.env.example middleware/.env
```

| Variable | Default | Meaning |
|---|---|---|
| `PORT` / `HOST` | `8090` / `127.0.0.1` | Fastify server. Keep `HOST` private: settle/refund have no auth |
| `TINYFISH_API_KEY` | empty | TinyFish key from https://agent.tinyfish.ai/api-keys (or the hackathon key). Needed for live evidence. See `../docs/keys-tinyfish.md` |
| `TINYFISH_URL` | empty | Leave empty |
| `DEFAULT_SOURCE_URL` | BhuNaksha | Portal opened when no `sourceUrl` is sent |
| `TINYFISH_TIMEOUT_MS` | `290000` | Agent timeout |
| `CHAIN_RPC_URL` | `http://127.0.0.1:8545` | Local Hardhat RPC. On Sepolia: same URL as `SEPOLIA_RPC_URL` |
| `CHAIN_ID` | `31337` | `31337` local, `11155111` Sepolia |
| `ESCROW_CONTRACT_ADDRESS` | empty | Address printed by the deploy script |
| `OPERATOR_PRIVATE_KEY` | empty | Signs settle/refund. Must be the account that deployed the contract. Throwaway keys only |
| `SEPOLIA_RPC_URL` | empty | Sepolia only (deploy). See `../docs/keys-sepolia.md` |
| `DEPLOYER_PRIVATE_KEY` | empty | Sepolia only (deploy). Must equal `OPERATOR_PRIVATE_KEY` |

Never commit `middleware/.env`. Never use a real wallet key or mainnet funds.
Validate with `npm run check:env` (add `-- sepolia` for the testnet) from the repo root.

## 2. Install and run

From the repo root:

```bash
npm --prefix middleware install
npm --prefix middleware run dev          # http://127.0.0.1:8090
```

Open `http://127.0.0.1:8090/health` in a browser: it reports whether TinyFish and the chain are configured.

## 3. Chain

Local:

```bash
# terminal 1
npm --prefix middleware run node

# terminal 2
npm --prefix middleware run deploy:local
# copy the printed address into middleware/.env as ESCROW_CONTRACT_ADDRESS
```

Sepolia (needs the Sepolia variables above; full walkthrough in `../docs/keys-sepolia.md`):

```bash
npm --prefix middleware run compile
npm --prefix middleware run deploy:sepolia
```

`hardhat.config.ts` loads `middleware/.env`, so the Sepolia variables can live there.
`npm --prefix middleware run chain:smoke` runs the full create, settle check against the configured chain.

## 4. TinyFish

```bash
npm --prefix middleware run smoke:tinyfish   # needs a real TINYFISH_API_KEY
```

This fails without a key on purpose. Do not replace it with a fake pass.
Record the real run ID, source URLs, status and latency in `../docs/tinyfish-smoke.md` (never the key).

## 5. Checks

```bash
npm --prefix middleware run typecheck
npm --prefix middleware run compile
npm --prefix middleware test
npm --prefix middleware run smoke:tinyfish   # needs key
```

## 6. Common errors

| Symptom | Fix |
|---|---|
| `TINYFISH_API_KEY is not set` | Add it to `middleware/.env` and restart (`../docs/keys-tinyfish.md`) |
| `ESCROW_CONTRACT_ADDRESS is not set` | Run a deploy script and paste the address |
| `ECONNREFUSED 127.0.0.1:8545` | Start the local node: `npm --prefix middleware run node` |
| settle/refund reverts | `OPERATOR_PRIVATE_KEY` is not the deployer key |
| `insufficient funds` | Fund the operator wallet with Sepolia test ETH |
| nonce / gas error on local chain | Restart the node and redeploy |
| `orderId must be 0x...32 bytes` | Compute with `ethers.id("landmarket-order:" + id)` |
| TinyFish `401` / `402` | Bad key / wallet balance too low (`../docs/keys-tinyfish.md`) |
| TinyFish timeout | Retry once, then document the block and try an alternate source |

## 7. Where the rules live

- API shapes/errors: `docs/api-contract.md`
- Order ID, chain IDs, money: `docs/decisions.md`
- Evidence hash: `docs/decisions.md` section 4
- Your task order: `AGENTS.md`

Do not change the contract shape in middleware only. Update the root contract first,
then `npm run sync:docs`.
