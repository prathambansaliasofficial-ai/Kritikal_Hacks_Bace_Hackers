-- Wallet users + KYC stub (T4.1). KYC is a prototype status flag, not identity verification.
CREATE TABLE IF NOT EXISTS users (
    id            BIGSERIAL PRIMARY KEY,
    wallet_address TEXT UNIQUE NOT NULL,
    role          TEXT NOT NULL DEFAULT 'CITIZEN'
                  CHECK (role IN ('CITIZEN', 'OFFICER')),
    kyc_status    TEXT NOT NULL DEFAULT 'PENDING'
                  CHECK (kyc_status IN ('PENDING', 'VERIFIED', 'REJECTED')),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS users_wallet_idx ON users (wallet_address);
