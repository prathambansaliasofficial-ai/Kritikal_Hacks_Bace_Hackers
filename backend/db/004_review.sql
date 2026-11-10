-- Review columns on evidence_sheets (T3.3).
ALTER TABLE evidence_sheets ADD COLUMN IF NOT EXISTS review_reason TEXT;
ALTER TABLE evidence_sheets ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ;
