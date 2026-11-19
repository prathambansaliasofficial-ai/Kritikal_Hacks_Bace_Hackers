# prompts.md — Root (Paradew / Senior Head / `main` branch)

Roles: **Paradew** = senior head, works on `main` only to merge & supervise (does not own a feature branch).
**Sumit** = frontend (`frontend/<name>`). **Tanya** = middleware (`middleware/<name>` or `ai/<name>`). **Yash** = backend (`backend/<name>`).

### PLAYRULES (applies to all teammates — from deleted PLAYRULES.MD)
- Sirf apne module folder mein kaam karo — doosre module ka code mat chhedo
- main par kabhi direct push mat karo — apni branch par push karo, PR kholo, lead merge karega
- Task ID order mein kaam karo, skip mat karo
- `npm run sync:docs && npm run check:docs` har batch ke baad chalao
- Koi fake API key, fake TxHash, ya government record mat dalo

---

## MASTER PROMPT (NEVER comment out this block)

I am Paradew, senior head. You are acting as my AI on the `main` branch of the Land Market monorepo. Your job is supervision, merge coordination, and repo hygiene — NOT feature coding on feature branches.

STRICT SCOPE:
- Work ONLY on `main`. Never create or push to `frontend/`, `backend/`, `middleware/`, or `ai/` branches.
- Never write feature code inside `frontend/`, `backend/`, or `middleware/`. Those are owned by Sumit, Yash, and Tanya respectively.
- You may edit: root `whole_plan.md` (progress header + phase counters ONLY — the lead owns these; interns must not touch them), root `docs/*`, root `SETUP.md`, root `AGENTS.md`, root `Makefile`, root `package.json`, root `docker-compose.yml`, `scripts/`.
- You may NOT edit generated copies (`*/whole_plan.md`, `*/docs/**`).

Read order before every action:
1. Root `AGENTS.md` + `docs/team-workflow.md` + `docs/task-ownership.md`.
2. `whole_plan.md` — current batch, progress header, phase counters.
3. The specific PR / task being merged.

Hard rules (root level):
- One person = one module branch. `main` is merge-only; never push feature commits directly to `main`.
- Demo data carries `DEMO_FIXTURE_NOT_OFFICIAL` (DB) or `demo: true` (API). No fake keys, run IDs, TxHashes, or government records.
- Never commit `.env` files or secrets.
- After every merge: run `npm run sync:docs && npm run check:docs`.
- Progress header and phase counters in `whole_plan.md` are updated by the lead only — interns must not edit them.

When a module reports its batch (3 tasks) done:
1. Review the PR against `docs/task-ownership.md` (allowed paths, commit message, definition of done).
2. Merge the module branch into `main`.
3. Update `whole_plan.md` progress header + phase counters (lead privilege).
4. Run `npm run sync:docs && npm run check:docs`.
5. Confirm `git status --short` is clean on `main`.

---

## PROMPT BLOCKS (comment out each block when its task/batch is done)
Rule: When a prompt block below is completed, wrap its entire block in HTML comments `<!-- ... -->`. Keep the MASTER PROMPT above uncommented at all times.

<!-- PROMPT: ROOT — Review and merge a module batch (B1 / M1 / F1 etc.) — START -->
I am Paradew on `main`. A module (Sumit/frontend, Tanya/middleware, or Yash/backend) reports that batch <BATCH_NAME> (<TASK_IDs>) is complete on its branch `<module>/<name>`.

Do the following:
1. Fetch the branch: `git fetch origin <module>/<name>`.
2. Review the diff against `docs/task-ownership.md`: confirm only allowed paths were touched, commit message matches the batch table, and exactly 3 tasks are in the commit.
3. Verify Definition of Done for each task: task marker `[.]` in `whole_plan.md`, module log updated, `npm run sync:docs && npm run check:docs` passed, tests pass (`ruff`+`pytest` for backend; `typecheck`+`build` for frontend; `typecheck`+`compile`+`test` for middleware).
4. Merge into `main` (no fast-forward if you want a merge commit): `git checkout main && git pull && git merge --no-ff <module>/<name> -m "<batch commit message>"`.
5. Update `whole_plan.md`: progress header + phase counters (lead only). Move completed task blocks under "YEH SAB HO GYA" with `**Done:** <date> <time> IST — Session N`.
6. Run `npm run sync:docs && npm run check:docs`.
7. `git status --short` must be clean. `git push origin main` ONLY if you are the lead/Paradew — never by an intern.
8. Report: merge hash, tasks closed, any blockers found.
<!-- PROMPT: ROOT — Review and merge a module batch — END -->

<!-- PROMPT: ROOT — Update whole_plan.md progress header & phase counters — START -->
I am Paradew on `main`. Update `whole_plan.md` only:
- Progress line: `Progress: <X> / 35 tasks done (<Y>%)`.
- Current batch line.
- Move done task blocks from "ABHI YEH YEH KARNA HAI" to "YEH SAB HO GYA" with `### [.] <TASK_ID>` and a `**Done:** YYYY-MM-DD HH:MM IST — Session N` line.
- Do NOT edit any other module's task text, commit messages, or allowed paths.
- After editing, run `npm run sync:docs && npm run check:docs`.
- Report the exact lines changed.
<!-- PROMPT: ROOT — Update whole_plan.md progress header & phase counters — END -->

<!-- PROMPT: ROOT — Full repo verification before demo — START -->
I am Paradew on `main`. Run the full verification suite and report any failure:
- `npm run install:all`
- `npm run typecheck`
- `npm run test:middleware`
- `npm run sync:docs && npm run check:docs`
- `backend/.venv/bin/ruff check backend`
- `backend/.venv/bin/pytest -q backend`
- `npm --prefix frontend run build`
- `npm --prefix middleware run compile`
- `docker compose config`
- `git status --short` must be clean on `main`.
Report pass/fail per command and the final `git log --oneline -1`.
<!-- PROMPT: ROOT — Full repo verification before demo — END -->
