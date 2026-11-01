-- Land Market prototype schema.
-- Runs automatically on first PostGIS container start (docker-entrypoint-initdb.d).
-- Apply manually with: docker compose exec -T postgis psql -U landmarket -d landmarket < backend/db/001_init.sql

CREATE EXTENSION IF NOT EXISTS postgis;

-- Canonical, authoritative parcel record keyed by the government ULPIN.
CREATE TABLE IF NOT EXISTS parcels (
    ulpin            TEXT PRIMARY KEY,
    geometry         geometry(MultiPolygon, 4326),
    geometry_source  TEXT,
    geometry_status  TEXT NOT NULL DEFAULT 'N/D'
                     CHECK (geometry_status IN ('AVAILABLE', 'N/D')),
    attributes       JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS parcels_geometry_idx ON parcels USING GIST (geometry);

-- Autonomous Land Units: deterministic hierarchy levels 1km -> 0.1m2.
CREATE TABLE IF NOT EXISTS alus (
    alu_id     TEXT PRIMARY KEY,
    parent_id  TEXT REFERENCES alus (alu_id) ON DELETE CASCADE,
    level      TEXT NOT NULL
               CHECK (level IN ('1km', '100m', '10m', '1m', '0.1m2')),
    geometry   geometry(Polygon, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS alus_geometry_idx ON alus USING GIST (geometry);
CREATE INDEX IF NOT EXISTS alus_parent_idx ON alus (parent_id);

-- Parcel <-> ALU linkage (a parcel can cover many ALUs).
CREATE TABLE IF NOT EXISTS parcel_alus (
    ulpin              TEXT NOT NULL REFERENCES parcels (ulpin) ON DELETE CASCADE,
    alu_id             TEXT NOT NULL REFERENCES alus (alu_id) ON DELETE CASCADE,
    relationship       TEXT NOT NULL DEFAULT 'INTERSECTS'
                       CHECK (relationship IN ('CONTAINS', 'INTERSECTS')),
    overlap_percentage NUMERIC(6, 3),
    PRIMARY KEY (ulpin, alu_id)
);

-- 21-field evidence sheet captured by TinyFish and the human-review outcome.
CREATE TABLE IF NOT EXISTS evidence_sheets (
    id             BIGSERIAL PRIMARY KEY,
    ulpin          TEXT NOT NULL,
    status         TEXT NOT NULL DEFAULT 'PENDING'
                   CHECK (status IN ('PENDING', 'CLEAN', 'NEEDS_REVIEW', 'REJECTED')),
    payload        JSONB NOT NULL DEFAULT '{}'::jsonb,
    source_refs    JSONB NOT NULL DEFAULT '[]'::jsonb,
    tinyfish_run_id TEXT,
    reviewed_by    TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS evidence_sheets_ulpin_idx ON evidence_sheets (ulpin);
CREATE INDEX IF NOT EXISTS evidence_sheets_status_idx ON evidence_sheets (status);

-- Marketplace listings and orders (amounts are prototype accounting units in wei).
CREATE TABLE IF NOT EXISTS listings (
    id            BIGSERIAL PRIMARY KEY,
    ulpin         TEXT NOT NULL REFERENCES parcels (ulpin) ON DELETE CASCADE,
    alu_id        TEXT REFERENCES alus (alu_id) ON DELETE SET NULL,
    seller_wallet TEXT NOT NULL,
    price_wei     NUMERIC(78, 0) NOT NULL CHECK (price_wei > 0),
    status        TEXT NOT NULL DEFAULT 'DRAFT'
                  CHECK (status IN ('DRAFT', 'LISTED', 'PAUSED', 'SOLD', 'CANCELLED')),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS listings_status_idx ON listings (status);

CREATE TABLE IF NOT EXISTS orders (
    id           BIGSERIAL PRIMARY KEY,
    listing_id   BIGINT NOT NULL REFERENCES listings (id) ON DELETE CASCADE,
    buyer_wallet TEXT NOT NULL,
    amount_wei   NUMERIC(78, 0) NOT NULL CHECK (amount_wei > 0),
    state        TEXT NOT NULL DEFAULT 'CREATED'
                 CHECK (state IN ('CREATED', 'FUNDED', 'SETTLED', 'REFUNDED', 'FAILED')),
    chain_order  TEXT,
    tx_hash      TEXT,
    evidence_hash TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS orders_state_idx ON orders (state);
