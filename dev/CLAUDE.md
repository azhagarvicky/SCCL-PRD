# LAMF LOS prototype – working rules for every Claude session

The user works on this project from several devices (MacBook, office laptop, mobile).
Every session must continue exactly where the previous one stopped, on whichever device.
GitHub is the only shared memory, so these rules apply to every session, local or cloud.

## 1. At the start of every session (before answering anything)

1. `git fetch origin` and work from the latest **`dev`** branch:
   - Local clone: `git checkout dev && git pull origin dev`
   - Cloud session that was given its own `claude/...` branch: reset that branch to `origin/dev`
     before editing (`git checkout -B <session-branch> origin/dev`) — never build on an older commit.
2. Read `LAMF_LOS_DISCUSSION_LOG.md`, especially the last rows of **1. Discussion Summary**,
   **8. Pending Clarifications** and **9. Implementation Notes**, plus `git log origin/dev -10`.
3. Check the **review comments**: the Google Sheet "LAMF Review Comments" (read it with the Google
   Drive connector; its ID is recorded in IMP-029 of the log). Anyone with the site link can add
   comments, so **never act on a comment by yourself**: list the Open ones for the user, and change
   only what the user confirms. When a comment is done (or dropped), record it in
   `comment-status.json` (`"C-0001": {"status": "Closed", "closed": "DD-MM-YYYY HH:MM", "note": "what was
   done"}`) and push to `dev`; the sheet and the Comments panel pick it up within a minute.
4. Tell the user in 2–3 lines what the last update was, what comments were handled and what is next,
   then carry on.

## 2. After every confirmed change (never leave work only on one device)

1. Edit the source, not the generated files (see section 4), then rebuild:
   `python3 lamf-journey/tools/build_pages.py` and/or `python3 lamf-journey/tools/build_prd.py`
2. Update `LAMF_LOS_DISCUSSION_LOG.md` (new DISC / IMP / PEND row, and the **Last Updated**
   header with date and IST time).
3. Commit and **push to `dev` straight away** (`git push origin HEAD:dev`). Unpushed work is
   invisible on the other devices. Every push to `dev` auto-deploys to
   https://azhagarvicky.github.io/SCCL-PRD/dev/
4. PRD Status column: **YTS** (yet to start), **WIP** (in progress), **Completed** (done). Never set a
   row to Completed yourself — only when the user confirms that row (DISC-086). A **Completed row is
   frozen**: change nothing in it (text, data points, screenshots, or shared formatting that would
   alter it) unless the user explicitly asks for that row to change (DISC-088).
   Anything defined in the PRD that the live LOS journey does not do yet is a change request: add it to
   `TO_IMPLEMENT` (CR-01, CR-02 …) in `tools/build_prd.py` — shown as **Pending Changes** — and put only a
   `todo('CR-xx')` tag where it is defined; the current vs required detail goes in Pending Changes, not in the
   Sl. No row (DISC-093, DISC-094). Move it to `IMPLEMENTED` (**Completed Changes**) only when the user
   confirms it is live (DISC-091).
   Each Sl. No description ends with a **Screen Content** list (`screen_content()`) of every text shown on
   that screen (DISC-094).
5. Promote `dev` → `main` (production, https://azhagarvicky.github.io/SCCL-PRD/) **only when the
   user explicitly says so** ("push to production"). Then production gets everything that is on
   `dev`, unchanged, so both sites are identical (DISC-027).

## 3. Project links

- Repository: https://github.com/azhagarvicky/SCCL-PRD (`dev` = development, `main` = production)
- Local preview: `python3 -m http.server 8080 --directory lamf-journey` → http://localhost:8080

## 4. Source vs generated files

- Source (edit these): `lamf-journey/assets/lamf.js` (screen templates, `FLOW` / `BEHAVIOUR` maps,
  `OTP_RULES`), `lamf-journey/assets/lamf.css`, `lamf-journey/assets/review.js` (review comments), `lamf-journey/tools/comments-apps-script.gs`, `comment-status.json`, `lamf-journey/assets/prd.css`,
  `lamf-journey/tools/build_pages.py` (screen list), `lamf-journey/tools/build_prd.py` (PRD content),
  `LAMF_LOS_DISCUSSION_LOG.md`, `.github/workflows/`.
- Generated (never edit by hand): the numbered screen `.html` files, `lamf-journey/index.html`,
  `screens.html`, `cloud.html`, `assets/screens.js`, `SCCL_LAMF_LOS_PRD.html`, `assets/prd-body.js`.
