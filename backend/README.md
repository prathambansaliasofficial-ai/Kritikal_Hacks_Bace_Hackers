# Land Market backend

FastAPI service that owns the fixed trade rules and proxies evidence requests to
the TinyFish middleware.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.api.main:app --reload --port 8000
```

- `GET /health` — API + PostGIS probe (stays up if the DB is down)
- `POST /api/v1/verifications` — `{"ulpin": "..."}` forwarded to `POST /verify/evidence`
- Schema lives in `db/001_init.sql` and is loaded by the root `docker-compose.yml`.

The six checks (listed, bundle intact, KYC wallet, zoning OK, funds in escrow,
parcel match) are not implemented yet; they will sit in `app/` next to the
21-field evidence sheet returned by the middleware.
