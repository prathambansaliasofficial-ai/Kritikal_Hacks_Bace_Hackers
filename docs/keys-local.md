# Path A: local demo setup (no blockchain accounts needed)

Uses a local Hardhat chain with built-in test accounts. The only external key is the
TinyFish key (see `docs/keys-tinyfish.md`), and it is optional if you only want to run the
app and the tests.

## 1. Create env files

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp middleware/.env.example middleware/.env
cp frontend/.env.example frontend/.env
```

## 2. Start the local chain and deploy the contract

```bash
npm --prefix middleware run node            # terminal 1, leave running
npm --prefix middleware run deploy:local    # terminal 2, prints the contract address
```

The node prints a list of test accounts with their keys when it starts.
These are public, well-known development keys. Use them for local work only.

## 3. Fill the env files

| File | Variable | Value |
|---|---|---|
| `middleware/.env` | `ESCROW_CONTRACT_ADDRESS` | the address printed by `deploy:local` |
| `middleware/.env` | `OPERATOR_PRIVATE_KEY` | the first (account 0) test key printed by the node. It must be the account that deployed the contract |
| `middleware/.env` | `TINYFISH_API_KEY` | your TinyFish key (optional) |
| `backend/.env` | `DEV_OFFICER_TOKEN` | any random string |
| `frontend/.env` | `VITE_ESCROW_ADDRESS` | the same contract address |
| `frontend/.env` | `VITE_OFFICER_TOKEN` | the same string as `DEV_OFFICER_TOKEN` (local only) |

Generate a random token with:

```bash
node -e "console.log(require('crypto').randomBytes(16).toString('hex'))"
```

## 4. Verify

```bash
npm run check:env
```

Then start the three services (see `SETUP.md` section 6) and open the middleware
`/health` endpoint on port 8090. You want `chainConfigured: true`, and
`tinyfishConfigured: true` if you added a key.

## 5. MetaMask on the local chain (optional)

Add a custom network: RPC `http://127.0.0.1:8545`, chain ID `31337`, currency ETH.
Import one of the printed test accounts to act as the buyer.
These accounts are public. Never send real funds to them.

## 6. Restarting

The local chain forgets everything when it stops. After restarting `node`, run
`deploy:local` again and update `ESCROW_CONTRACT_ADDRESS` and `VITE_ESCROW_ADDRESS`
(the address is usually the same on a fresh node, but check).
