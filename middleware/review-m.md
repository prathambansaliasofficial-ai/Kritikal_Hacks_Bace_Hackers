# Review-M — Middleware review loop
Last reviewed commit: a19a23d

## Format spec

```
## R-<n> — reviewing <author-session-id> (commit <abc123>..<def456>) — by <reviewer-session-id>
Checked: <kya actually kiya gaya: diff read, typecheck/compile/test aur result, kaunsa api-contract.md section compare kiya>
- [BLOCKER|MAJOR|NIT] <file>:<line> — <problem + why>. Expected: <contract/rule>
Verdict: CHANGES_REQUESTED | APPROVED
Status: OPEN | RESOLVED (fixed in <hash>)
```

Rules:
- Reviewer edits only `middleware/review-m.md`, never `middleware/src/` source code.
- Every entry must have a `Checked:` line (proof of what was actually done).
- Every comment needs severity `[BLOCKER]` / `[MAJOR]` / `[NIT]`.
- Entry needs `Verdict` (`APPROVED` / `CHANGES_REQUESTED`) and `Status` (`OPEN` / `RESOLVED`).
- Open `[BLOCKER]` = no new middleware task may start.
- Archive entries older than the last 5 to `middleware/archive/review-<x>-YYYY-MM.md`.

## Entries

(none yet)
