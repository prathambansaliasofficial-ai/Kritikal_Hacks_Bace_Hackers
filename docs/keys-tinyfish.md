# Key 1: TinyFish API key (live land evidence)

The middleware uses TinyFish Web Agent to collect the 21-field evidence sheet for a ULPIN.
Without a key, the live evidence call fails by design (`503`/`502`), and a trade cannot reach
`APPROVED` because the `ZONING_OK` check has no evidence (the order ends in `NEEDS_REVIEW`).
Unit tests use a mock, so they pass with no key.

## Get the key

1. Go to https://agent.tinyfish.ai and sign up or log in. New accounts have been getting free credits.
2. Open https://agent.tinyfish.ai/api-keys and click **Create API Key**.
3. **Copy it immediately.** TinyFish shows the key only once.
4. If the hackathon organisers gave you a permanent key, use that one and skip steps 1-3.

## Put it in the project

Open `middleware/.env` (copy it from `middleware/.env.example` if it does not exist) and set:

```
TINYFISH_API_KEY=<paste the key here, no quotes, no spaces>
```

Restart the middleware (`npm run dev:middleware`).

## Prove it works (completes roadmap task T3.1)

```bash
npm --prefix middleware run smoke:tinyfish
```

Success prints a JSON evidence sheet that includes a run ID and source URLs.
Then record the run ID, date, source URL, status and latency in `docs/tinyfish-smoke.md`.
Never write the key itself anywhere in the repo.

Also open the middleware `/health` endpoint (port 8090): it should show `tinyfishConfigured: true`.

## Errors

| Symptom | Meaning / fix |
|---|---|
| `TINYFISH_API_KEY is not set` | Missing in `middleware/.env`, or the middleware was not restarted. |
| `401` | Key wrong, has extra whitespace, or was revoked. Create a new one. |
| `402` | TinyFish wallet balance too low. Add credit in the TinyFish dashboard. |
| Timeout | Retry once. The agent timeout is `TINYFISH_TIMEOUT_MS` (default 290000). Government portals can be slow. |

## If the key leaks

Revoke it on https://agent.tinyfish.ai/api-keys and create a new one.

## Optional settings in the same file

| Variable | Default | Meaning |
|---|---|---|
| `DEFAULT_SOURCE_URL` | `https://bhunaksha.nic.in/bhunaksha/` | Portal opened when a request has no `source_url` |
| `TINYFISH_TIMEOUT_MS` | `290000` | Agent timeout |
| `TINYFISH_URL` | empty | Leave empty |
