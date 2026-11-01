<!--
  GENERATED FILE. Source: docs/context/README.md
  Do not edit this copy. Edit the root file, then run: npm run sync:docs
-->
# Context packs — index

One pack per batch. Read **only** the pack for your task and only the files it lists.
This is how we keep an intern focused on one slice and stop random repo scanning.

| Pack | Tasks | Primary owner |
|---|---|---|
| `C0.md` | C0 baseline | Lead |
| `C1.md` | T1.1, T1.2, T1.3 | Backend |
| `C2.md` | T2.1, T2.2, T2.3 | Backend |
| `C3.md` | T3.1 middleware, T3.2–T3.3 backend | Middleware + Backend |
| `C4.md` | T4.1, T4.2, T4.3 | Backend |
| `C5.md` | T5.1–T5.2 backend, T5.3-M middleware, T5.3-B backend | Backend + Middleware |
| `C6.md` | T6.1-M middleware, T6.1-F frontend, T6.2–T6.3 middleware | Middleware + Frontend |
| `C7A.md` | T7.1, T7.2, T7.3 | Frontend |
| `C7B.md` | T7.4, T7.5, T7.6 | Frontend |
| `C8.md` | T8.1 backend, T8.2 lead, T8.3-B/M/F | Backend + Middleware + Frontend + Lead |
| `C9.md` | T9.1 backend, T9.2 AI, T9.3-B/M/F | All (stretch only) |

## Pack format

Every pack starts with:

- **Tasks** — exact IDs.
- **Owner** — who may execute it.
- **Read first (only)** — the allowed files.
- **Do not read** — the boundary.
- **Depends on** — what must exist first.
- **Blocker** — keys or human decisions.

## Rules

- Do not edit a pack to fit your code. If the contract is wrong, ask the lead.
- Do not read another module's pack "for context".
- After changing a root doc, run `npm run sync:docs` so module copies refresh.
