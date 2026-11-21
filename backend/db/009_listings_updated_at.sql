-- Listings repository sets updated_at on status changes (T4.2/T9.1),
-- so the column must exist.
ALTER TABLE listings ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now();
