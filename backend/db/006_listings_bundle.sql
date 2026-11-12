-- Link listings to bundles (T4.2).
ALTER TABLE listings ADD COLUMN IF NOT EXISTS bundle_id BIGINT REFERENCES bundles (id);

CREATE INDEX IF NOT EXISTS listings_bundle_id_idx ON listings (bundle_id);
