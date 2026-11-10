.PHONY: db-up db-check db-reset seed api mid web check

COMPOSE ?= docker compose

# --- database --------------------------------------------------------------

db-up:
	docker compose up -d postgis

db-check:
	PYTHONPATH=backend python backend/scripts/check_db.py

db-reset:
	@read -p "This deletes the PostGIS volume and ALL data. Continue? [y/N] " confirm; \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then echo "db-reset aborted"; exit 1; fi
	docker compose down -v
	docker compose up -d postgis

# --- demo seed -------------------------------------------------------------

seed:
	PYTHONPATH=backend python backend/scripts/seed.py

# --- services --------------------------------------------------------------

api:
	backend/.venv/bin/uvicorn app.api.main:app --app-dir backend --reload --port 8000

mid:
	npm run dev:middleware

web:
	npm run dev:frontend

# --- checks ----------------------------------------------------------------

check:
	backend/.venv/bin/ruff check backend
	backend/.venv/bin/pytest -q backend
