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
3. Tell the user in 2–3 lines what the last update was and what is next, then carry on.

## 2. After every confirmed change (never leave work only on one device)

1. Edit the source, not the generated files (see section 4), then rebuild:
   `python3 lamf-journey/tools/build_pages.py` and/or `python3 lamf-journey/tools/build_prd.py`
2. Update `LAMF_LOS_DISCUSSION_LOG.md` (new DISC / IMP / PEND row, and the **Last Updated**
   header with date and IST time).
3. Commit and **push to `dev` straight away** (`git push origin HEAD:dev`). Unpushed work is
   invisible on the other devices. Every push to `dev` auto-deploys to
   https://azhagarvicky.github.io/SCCL-PRD/dev/
4. Promote `dev` → `main` (production, https://azhagarvicky.github.io/SCCL-PRD/) **only when the
   user explicitly says so**.

## 3. Project links

- Repository: https://github.com/azhagarvicky/SCCL-PRD (`dev` = development, `main` = production)
- Local preview: `python3 -m http.server 8080 --directory lamf-journey` → http://localhost:8080

## 4. Source vs generated files

- Source (edit these): `lamf-journey/assets/lamf.js` (screen templates, `FLOW` / `BEHAVIOUR` maps,
  `OTP_RULES`), `lamf-journey/assets/lamf.css`, `lamf-journey/assets/prd.css`,
  `lamf-journey/tools/build_pages.py` (screen list), `lamf-journey/tools/build_prd.py` (PRD content),
  `LAMF_LOS_DISCUSSION_LOG.md`, `.github/workflows/`.
- Generated (never edit by hand): the numbered screen `.html` files, `lamf-journey/index.html`,
  `screens.html`, `cloud.html`, `assets/screens.js`, `SCCL_LAMF_LOS_PRD.html`, `assets/prd-body.js`.
