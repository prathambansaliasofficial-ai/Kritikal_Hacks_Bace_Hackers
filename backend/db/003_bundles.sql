-- Bundle schema (T2.3). Bundles group ALUs of a single parcel for marketplace listings.
CREATE TABLE IF NOT EXISTS bundles (
    id          BIGSERIAL PRIMARY KEY,
    ulpin       TEXT NOT NULL REFERENCES parcels (ulpin) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'DRAFT'
                CHECK (status IN ('DRAFT', 'ACTIVE', 'PAUSED', 'ARCHIVED')),
    created_by  TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS bundle_alus (
    bundle_id BIGINT NOT NULL REFERENCES bundles (id) ON DELETE CASCADE,
    alu_id    TEXT NOT NULL REFERENCES alus (alu_id) ON DELETE CASCADE,
    PRIMARY KEY (bundle_id, alu_id)
);
