# Middleware setup

TinyFish evidence service + Fastify API + Hardhat escrow. This file is only for the
`middleware/` module. Shared prerequisites are in `../SETUP.md`.

## 1. Env

```bash
cp middleware/.env.example middleware/.env
```

| Variable | Default | Meaning |
|---|---|---|
| `PORT` / `HOST` | `8090` / `127.0.0.1` | Fastify server |
| `TINYFISH_API_KEY` | empty | TinyFish API key (permanent, from hackathon organizers). Required for live evidence runs |
| `TINYFISH_URL` | empty | optional TinyFish URL; leave empty if using API key only |
| `DEFAULT_SOURCE_URL` | BhuNaksha | portal opened when no `sourceUrl` is sent |
| `TINYFISH_TIMEOUT_MS` | `290000` | agent timeout |
| `CHAIN_RPC_URL` | `http://127.0.0.1:8545` | local Hardhat RPC |
| `CHAIN_ID` | `31337` | local chain |
| `ESCROW_CONTRACT_ADDRESS` | empty | deployed escrow |
| `OPERATOR_PRIVATE_KEY` | empty | local Hardhat account #0 only |
| `SEPOLIA_RPC_URL` | empty | only for T6.3 |
| `DEPLOYER_PRIVATE_KEY` | empty | only for T6.3 |

Never commit `middleware/.env`. Never use a real key or mainnet funds.

## 2. Install and run

From the repo root:

```bash
npm --prefix middleware install
npm --prefix middleware run dev          # http://127.0.0.1:8090
curl -s localhost:8090/health | jq
```

## 3. Chain (local)

```bash
# terminal 1
npm --prefix middleware run node

# terminal 2
npm --prefix middleware run deploy:local
# copy the printed address into middleware/.env as ESCROW_CONTRACT_ADDRESS
```

After T6.2, `npm --prefix middleware run chain:smoke` runs the full create → settle check.

## 4. TinyFish

```bash
npm --prefix middleware run smoke:tinyfish   # needs a real TINYFISH_API_KEY
```

This fails without `TINYFISH_API_KEY` on purpose. Do not replace it with a fake pass.
For T3.1, record the real run ID, source URLs, status, and latency in
`../docs/tinyfish-smoke.md` (never the key).

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
| `TINYFISH_API_KEY is not set` | ask the lead; do not invent a key |
| `ESCROW_CONTRACT_ADDRESS is not set` | run `deploy:local` and paste the address |
| `ECONNREFUSED 127.0.0.1:8545` | start `npm --prefix middleware run node` |
| nonce / gas error on local chain | restart the node and redeploy |
| `orderId must be 0x...32 bytes` | compute with `ethers.id("landmarket-order:" + id)` |
| TinyFish timeout | retry once, then document the block and try an alternate source |

## 7. Where the rules live

- API shapes/errors: `docs/api-contract.md`
- Order ID, chain IDs, money: `docs/decisions.md`
- Evidence hash: `docs/decisions.md` §4
- Your task order: `AGENTS.md`

Do not change the contract shape in middleware only. Update the root contract first,
then `npm run sync:docs`.
