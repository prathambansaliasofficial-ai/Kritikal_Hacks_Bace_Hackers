# Keys and secrets: what you need, where to get them, where they go

This is the single guide for every key, token and secret in Land Market.
Follow **Path A** for a local demo, then **Path B** for the Sepolia testnet demo.
Hosting and security notes are in `docs/deployment.md`.

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
