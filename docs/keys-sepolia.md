# Path B: Sepolia testnet setup (step by step)

Do `docs/keys-tinyfish.md` first (or in parallel). This file covers wallets, the RPC URL,
test ETH, deploying the escrow contract, and wiring the addresses into the three apps.

## Step 1: Create three throwaway MetaMask accounts

1. Install MetaMask from https://metamask.io and create a wallet. **Use a fresh wallet or fresh accounts that never held real funds.**
2. Create three accounts and rename them so you do not mix them up:
   - **Operator**: also the contract deployer. Signs `settle()` and `refund()` through the middleware.
   - **Seller**: only its address is needed.
   - **Buyer**: the account you connect in the browser to buy.
3. Copy each account's public address (`0x` followed by 40 hex characters).
4. Export the **Operator** account's private key only: account menu (three dots), Account details, Show private key, then your password. Menu labels vary a little between MetaMask versions. You will paste it in Step 4. Do not paste it anywhere else.

## Step 2: Get a Sepolia RPC URL

Pick one free provider:

- **Alchemy**: sign up at https://dashboard.alchemy.com, create an app, choose the **Ethereum Sepolia** network, copy the HTTPS URL (it looks like `https://eth-sepolia.g.alchemy.com/v2/<your-key>`).
- **Infura**: sign up at https://app.infura.io, create an API key, enable Sepolia, copy the HTTPS URL (it looks like `https://sepolia.infura.io/v3/<your-key>`).

The URL contains your provider key, so treat the whole URL as a secret.

## Step 3: Get Sepolia test ETH

Send test ETH to the **Operator** address (gas) and to the **Buyer** address (order amount plus gas).
A demo order is around 0.01 ETH, so a small amount is enough.

Faucets that were working in late 2026 (limits and requirements change; most ask for a free
account or a small mainnet balance, so try another if one refuses):

- Alchemy Sepolia faucet (needs an Alchemy account)
- Google Cloud Web3 faucet (needs a Google account)
- Chainlink faucet
- QuickNode faucet
- pk910 Sepolia PoW faucet (no account; your browser mines for a while)

Check balances in MetaMask with the **Sepolia** network selected (turn on "Show test networks" if you do not see it).

> **Network lifecycle:** Sepolia was originally scheduled to end in September 2026, and an October 2026 update reported its support being extended through 2027. Confirm the current status at https://ethereum.org/en/developers/docs/networks/ before the final demo. This project runs on any EVM testnet if you change the chain ID, RPC URL and explorer URL.

## Step 4: Fill `middleware/.env`

```
CHAIN_ID=11155111
SEPOLIA_RPC_URL=<RPC URL from Step 2>
CHAIN_RPC_URL=<the same URL>
DEPLOYER_PRIVATE_KEY=<Operator key from Step 1>
OPERATOR_PRIVATE_KEY=<the same value>
ESCROW_CONTRACT_ADDRESS=
```

**Why the same key twice?** `deploy.ts` registers the deploying account as the only address
allowed to call `settle()` and `refund()`. If `OPERATOR_PRIVATE_KEY` is a different account,
every settlement reverts. `npm run check:env -- sepolia` checks this for you.

## Step 5: Deploy the escrow contract

```bash
npm --prefix middleware run compile
npm --prefix middleware run deploy:sepolia
```

The script prints the deployed address and writes `middleware/deployments/sepolia.json`.
If Hardhat cannot resolve `SEPOLIA_RPC_URL` or `DEPLOYER_PRIVATE_KEY`, export them in your
shell for that command, or store them with Hardhat's keystore (`npx hardhat keystore set <NAME>`
inside `middleware/`). The Hardhat config also loads `middleware/.env`.

Then:

1. Put the address in `middleware/.env` as `ESCROW_CONTRACT_ADDRESS`.
2. Open `https://sepolia.etherscan.io/address/<address>` and confirm the contract exists.
3. Record the address, transaction hash and explorer link in `docs/deployments.md` (completes roadmap task T6.3).
4. Commit `middleware/deployments/sepolia.json` (public addresses only).

## Step 6: Fill `frontend/.env` and `backend/.env`

`frontend/.env`:

```
VITE_API_BASE_URL=http://localhost:8000
VITE_ESCROW_ADDRESS=<contract address>
VITE_CHAIN_ID=11155111
VITE_CHAIN_NAME=Sepolia
VITE_EXPLORER_URL=https://sepolia.etherscan.io
VITE_OFFICER_TOKEN=<same as DEV_OFFICER_TOKEN, local demo only>
```

`backend/.env`:

```
DEV_OFFICER_TOKEN=<random string>
MIDDLEWARE_URL=http://127.0.0.1:8090
```

Restart all three services after saving.

## Step 7: Verify

1. In MetaMask select **Sepolia** and the **Buyer** account (the app also has a switch-network button).
2. Run `npm run check:env -- sepolia` and fix every FAIL line.
3. Open the middleware `/health` endpoint (port 8090): expect `tinyfishConfigured: true` and `chainConfigured: true`.
4. Run the demo: `docs/demo-script.md`.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `execution reverted` on settle/refund | `OPERATOR_PRIVATE_KEY` is not the key that deployed the contract. Use the same key as `DEPLOYER_PRIVATE_KEY`, or redeploy. |
| `insufficient funds` | The operator or buyer wallet has no Sepolia ETH. Use a faucet. |
| UI says escrow address not configured | `VITE_ESCROW_ADDRESS` is empty. Set it and restart the frontend. |
| MetaMask on the wrong network | Switch to Sepolia (chain ID 11155111) or use the in-app switch button. |
| `ECONNREFUSED` on port 8545 | You are on the local config. Start the local node, or set `CHAIN_RPC_URL` to the Sepolia URL. |
| RPC `401`/`429` | Provider key wrong, or free-tier rate limit. Wait, or use the other provider. |
