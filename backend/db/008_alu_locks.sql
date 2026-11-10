-- ALU locking + double-sell protection (T9.1).
--
-- Active listing per ALU: DRAFT, LISTED and PAUSED count as "active" for this
-- rule. A partial unique index guarantees an ALU can be in at most one active
-- listing, so the same ALU cannot be double-sold.
--
-- Sold ALU lock: an ALU that already has a SOLD listing cannot be re-listed.
-- The unique index above does not cover SOLD (terminal), so the repository
-- layer rejects any create/patch-to-active that would relist a sold ALU.
-- Both are enforced together: DB index for active uniqueness, repository for
-- the sold lock.

CREATE UNIQUE INDEX IF NOT EXISTS listings_alu_active_idx
    ON listings (alu_id)
    WHERE alu_id IS NOT NULL
      AND status IN ('DRAFT', 'LISTED', 'PAUSED');
