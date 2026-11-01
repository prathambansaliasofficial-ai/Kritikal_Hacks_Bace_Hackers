# Land Market middleware

Two jobs, one process:

1. `POST /verify/evidence` runs a TinyFish Web Agent and returns the 21-field
   evidence sheet.
2. `POST /escrow/settle` / `POST /escrow/refund` let the backend operator resolve
   a funded `LandMarketEscrow` order.

```bash
npm install
npx hardhat compile
npm test
npm run dev                     # http://127.0.0.1:8090
npm run smoke:tinyfish          # proves TinyFish works before portal wiring
```

Local chain:

```bash
npm run node                    # terminal 1
npm run deploy:local            # terminal 2, copy address into .env
```

Copy `.env.example` to `.env` and fill `TINYFISH_API_KEY` plus the operator key.
