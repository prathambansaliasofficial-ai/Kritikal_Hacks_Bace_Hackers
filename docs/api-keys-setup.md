# Keys and secrets: what you need, where to get them, where they go

This is the index and summary for every key, token and secret in Land Market.
Each item has a step-by-step guide:

| Guide | Covers |
|---|---|
| [`docs/keys-tinyfish.md`](keys-tinyfish.md) | TinyFish API key (live evidence) |
| [`docs/keys-local.md`](keys-local.md) | Path A: local Hardhat chain demo, no blockchain accounts |
| [`docs/keys-sepolia.md`](keys-sepolia.md) | Path B: wallets, RPC URL, faucet, deploy, wiring, for the Sepolia testnet |
| [`docs/deployment.md`](deployment.md) | Where secrets live on a server, security rules, hosting, GitHub secrets |

**Suggested order:** Path A first (about 10 minutes, proves the app works), then the
TinyFish key, then Path B.

> **Golden rules**
> 1. Real keys live only in `.env` files (git-ignored) or in your hosting provider's secret store. Never in code, docs, logs, issues, screenshots or chat.
> 2. Use **throwaway wallets** that never held real money. Never put a mainnet key anywhere in this project.
> 3. After you edit a `.env` file, **restart** the service that reads it. Vite (`frontend/`) reads `VITE_*` values only at start/build time.
> 4. Check your setup with `npm run check:env` (local) or `npm run check:env -- sepolia`. It prints PASS/WARN/FAIL and never prints secret values.

## 1. What you need (summary)

| # | Item | Needed for | Required? | Where to get it | Where it goes |
|---|---|---|---|---|---|
| 1 | TinyFish API key | Live land evidence (21-field sheet) | Needed for the real evidence flow and the **APPROVED** trade path | https://agent.tinyfish.ai/api-keys | `middleware/.env` as `TINYFISH_API_KEY` |
| 2 | MetaMask, 3 accounts | Operator/deployer, seller, buyer | Yes, for the chain demo | https://metamask.io | Browser extension |
| 3 | Sepolia RPC URL | Deploy + talk to Sepolia | Sepolia only | Free Alchemy or Infura account | `middleware/.env` as `SEPOLIA_RPC_URL` and `CHAIN_RPC_URL` |
| 4 | Operator/deployer wallet key | Deploy the contract; authorise settle/refund | Yes (Sepolia: one **new** wallet) | Export from a throwaway MetaMask account | `middleware/.env` as `DEPLOYER_PRIVATE_KEY` **and** `OPERATOR_PRIVATE_KEY` (same value) |
| 5 | Sepolia test ETH | Gas + the escrowed amount | Sepolia only | A faucet | Operator wallet and buyer wallet |
| 6 | Escrow contract address | Everything that talks to the chain | After deploy | Printed by the deploy script; saved in `middleware/deployments/<network>.json` | `middleware/.env` as `ESCROW_CONTRACT_ADDRESS`; `frontend/.env` as `VITE_ESCROW_ADDRESS` |
| 7 | Officer token | Officer-only API calls (KYC, evidence review) | Yes | You invent it (random string) | `backend/.env` as `DEV_OFFICER_TOKEN`; optionally `frontend/.env` as `VITE_OFFICER_TOKEN` (local only, see `docs/deployment.md`) |
| 8 | Database URL | PostGIS | Default works locally | Docker (local) or Supabase (hosted) | `backend/.env` as `DATABASE_URL` |

You do **not** need an Etherscan API key (the explorer link is just a URL), an OpenAI/Anthropic key, any GitHub secret (the repo has no CI workflows yet), or a paid plan.

## 2. Where each variable is read

| Variable | File | Read by |
|---|---|---|
| `TINYFISH_API_KEY`, `TINYFISH_URL`, `DEFAULT_SOURCE_URL`, `TINYFISH_TIMEOUT_MS` | `middleware/.env` | middleware (`src/tinyfish/evidence.ts`) |
| `CHAIN_RPC_URL`, `CHAIN_ID`, `ESCROW_CONTRACT_ADDRESS`, `OPERATOR_PRIVATE_KEY` | `middleware/.env` | middleware (`src/blockchain/escrow.ts`) |
| `SEPOLIA_RPC_URL`, `DEPLOYER_PRIVATE_KEY` | `middleware/.env` | Hardhat (`hardhat.config.ts`), deploy only |
| `DATABASE_URL`, `MIDDLEWARE_URL`, `MIDDLEWARE_TIMEOUT_SECONDS`, `CORS_ORIGINS`, `DEV_OFFICER_TOKEN` | `backend/.env` | backend (`app/core/config.py`) |
| `VITE_API_BASE_URL`, `VITE_ESCROW_ADDRESS`, `VITE_CHAIN_ID`, `VITE_CHAIN_NAME`, `VITE_EXPLORER_URL`, `VITE_OFFICER_TOKEN` | `frontend/.env` | frontend, **baked into the public JS bundle** |
| `POSTGRES_*` | `.env` (root) | `docker-compose.yml` (local PostGIS) |

## 3. Security checklist

- [ ] No `.env` file is tracked: `git ls-files` shows none.
- [ ] The operator wallet is a throwaway, Sepolia-only wallet.
- [ ] The middleware is not reachable from the internet (its settle/refund endpoints have no authentication).
- [ ] `VITE_OFFICER_TOKEN` is empty on any public frontend.
- [ ] `DEV_OFFICER_TOKEN` is not the example value `dev-officer-token` before you share a URL.
- [ ] Secret scanning and push protection are on (repo Settings, Code security).

If a key leaks: revoke the TinyFish key at https://agent.tinyfish.ai/api-keys and create a new one; rotate the RPC key in your provider dashboard; for a leaked operator key, stop using that wallet, create a new one and redeploy the contract (the operator address is fixed at deploy time).
