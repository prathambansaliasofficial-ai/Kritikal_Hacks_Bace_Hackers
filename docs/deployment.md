# Deployment and secret handling

The hackathon demo runs on a laptop (`SETUP.md`). This file covers putting it on a server
and what to protect. Nothing here has been deployed or tested by the team yet: treat it as
the checklist, and record real results in `docs/deployments.md`.

## What runs where

| Service | Folder | Port | Public? |
|---|---|---|---|
| Frontend (static site) | `frontend/` | 5173 dev / any static host | Yes |
| Backend API | `backend/` | 8000 | Yes (the browser calls it) |
| Middleware (TinyFish + escrow operator) | `middleware/` | 8090 | **No. Private only** |
| PostGIS database | `docker-compose.yml` or Supabase | 5432 | **No. Private only** |
| Chain | Sepolia (public testnet) | n/a | n/a |

## Where each secret lives in production

| Secret | Set it in | Never in |
|---|---|---|
| `TINYFISH_API_KEY` | Middleware host's secret settings | repo, frontend |
| `OPERATOR_PRIVATE_KEY` | Middleware host's secret settings | repo, frontend, backend |
| `DATABASE_URL` | Backend host's secret settings | repo, frontend |
| `DEV_OFFICER_TOKEN` | Backend host's secret settings | repo |
| `CORS_ORIGINS` | Backend host (plain setting) | n/a |
| `MIDDLEWARE_URL` | Backend host (private address of the middleware) | n/a |
| `VITE_*` values | Frontend build settings | n/a (they become public) |

`DEPLOYER_PRIVATE_KEY` and `SEPOLIA_RPC_URL` are needed only on the machine where you run
`deploy:sepolia`. They do not need to exist on any server.

## Must-do security rules

1. **Keep the middleware private.** `POST /escrow/settle` and `POST /escrow/refund` have no authentication. Anyone who can reach port 8090 can trigger settlement with the operator key. Bind to `127.0.0.1`, or place it on a private network where only the backend can connect. Do not publish it through a tunnel or a public URL.
2. **Do not set `VITE_OFFICER_TOKEN` on a public frontend.** Every `VITE_*` value is embedded in the JavaScript that visitors download. With it set, the officer review screen appears and the token is exposed. Leave it empty on public deployments and do officer actions from a trusted machine using the backend's API docs page.
3. **Change the officer token** from the example value before sharing any URL, and treat it as a demo stub (see `docs/limitations.md`), not real authentication.
4. **Operator wallet:** Sepolia-only, throwaway, funded with a small amount. Never reuse a wallet that holds real funds.
5. **Backend CORS:** set `CORS_ORIGINS` to the exact frontend URL (comma-separated for several). The default only allows `http://localhost:5173`.
6. **Database:** do not expose port 5432 publicly. Change the default Postgres password from `landmarket_dev` for any shared environment.

## Option 1: Frontend on a static host, rest on your own machine or VM

1. Build with the right values: set `VITE_API_BASE_URL` (public backend URL), `VITE_ESCROW_ADDRESS`, `VITE_CHAIN_ID=11155111`, `VITE_CHAIN_NAME=Sepolia`, `VITE_EXPLORER_URL=https://sepolia.etherscan.io`, then `npm --prefix frontend run build`.
2. Upload `frontend/dist/` to a static host (Vercel, Netlify, Cloudflare Pages, GitHub Pages). On Vercel, set the root directory to `frontend` and add the same variables in the project's Environment Variables, then redeploy.
3. Run the backend and middleware on a VM or container host with the secrets above. Use the Dockerfiles in `backend/` and `middleware/`.
4. Expose only the backend over HTTPS. A tunnel such as Cloudflare Tunnel pointing at port 8000 is enough for a demo.
5. Add the frontend's URL to `CORS_ORIGINS` on the backend.

## Option 2: Hosted database (Supabase)

1. Create a Supabase project and enable the **postgis** extension (Database, Extensions).
2. Copy the connection string from Project Settings, Database, and set it as `DATABASE_URL` for the backend.
3. Apply the SQL files in `backend/db/` in numeric order (`001_init.sql` first) using the Supabase SQL editor or `psql`. Skip the seed file if you do not want demo data.
4. This path has not been tested by the team. If the backend cannot connect, check that the connection string uses the pooled or direct host Supabase shows you and that SSL is allowed.

## Pre-launch checklist

- [ ] `git ls-files` shows no `.env` file.
- [ ] Secret scanning and push protection are on (repo Settings, Code security).
- [ ] Middleware is not reachable from the internet.
- [ ] `VITE_OFFICER_TOKEN` is empty in the production frontend build.
- [ ] `CORS_ORIGINS` is the real frontend URL.
- [ ] Contract address and explorer link are in `docs/deployments.md`.
- [ ] One full buy flow was completed on the deployed stack and the tx hash recorded.

## GitHub secrets

The repository has no GitHub Actions workflows today, so no GitHub secret is needed. If you
add one later, create secrets under Settings, Secrets and variables, Actions, and use the
names `TINYFISH_API_KEY`, `SEPOLIA_RPC_URL`, `DEPLOYER_PRIVATE_KEY`. A CI job that only runs
tests and builds needs none of them.
