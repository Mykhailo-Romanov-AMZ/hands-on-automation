# Validation — Email Waitlist (One-Build Sprint Signup)

How we know this feature succeeded. The feature is complete when **all** of the following are true:

## 1. Automated checks (red → green)

- `python3 -m unittest discover -s tests` was **red** before `server.py` existed and is now **green** (exit 0).
- The tests confirm, from the code itself:
  - valid `POST /signup` → 201, row in SQLite, line in `outbox.log`;
  - malformed email → 400, nothing stored;
  - duplicate email → 409, still exactly one row;
  - `GET /subscribers` → 200 with the signed-up email, newest first;
  - `GET /` → 200 static homepage.
- `python3 checks.py` (the landing-page harness) still passes (60/60 at the time; **107/107** after launch-hardening + gallery) — no regression.

## 2. Live in the browser

- `server.py` binds to `0.0.0.0:3000` (confirmed with `ss -tlnp`).
- `curl http://localhost:3000/` returns HTTP 200.
- Public URL `https://${CODIO_HOSTNAME}-3000.codio.io/` loads the page from any browser.
- `curl -X POST /signup -d '{"email": ...}'` → 201; the same email again → 409; a malformed email → 400.
- `curl /subscribers` → 200 and the signed-up email appears in the table.
- `data/outbox.log` contains the stubbed welcome email (subject + body from `requirements.md`).

## 3. Manual visual + behavior pass (checklist)

- [ ] Submitting the CTA form shows the approved success copy ("You're in the sprint…") only after the server confirms.
- [ ] Second submit with the same email shows the "already on the list" error, not success.
- [ ] A malformed email shows the invalid-email error and the form stays usable (focus returns to the input).
- [ ] `/subscribers` renders as a readable table, newest signup first.
- [ ] The page still looks and behaves exactly as before for a visitor who never signs up (no visual regressions).

## 4. Specs sync (differences surfaced)

Compare the implementation against `SPECS/` and this spec after building. Present any
differences to the founder and update the specs (`build-lab/MISSION.md`, `ROADMAP.md`, or
this folder) **only after the founder approves**. Do not silently edit the constitution.

## Merge-ready definition

The feature is mergeable when: the red→green test history is intact (tests failed first,
then passed), automated checks are green, the live URL is verified, the manual checklist
passes, and the founder has approved any spec updates.