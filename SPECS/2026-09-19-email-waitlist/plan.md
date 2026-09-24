# Plan — Email Waitlist (One-Build Sprint Signup)

Red/Green TDD: tests are written **before** the feature code and must fail first.

---

## Group 1 — Tests first (red)

- [x] Create `tests/test_signup.py` (stdlib `unittest`, no external packages).
- [x] Tests use a **temporary** database + outbox (temp dir), never the real `data/`.
- [x] Test: `POST /signup` with a valid email → 201 + email row exists in SQLite + a line appears in `outbox.log`.
- [x] Test: `POST /signup` with a malformed email → 400 + nothing stored.
- [x] Test: duplicate email → 409 + still only one row in the table.
- [x] Test: `GET /subscribers` → 200 + HTML contains the signed-up email + newest first ordering.
- [x] Test: `GET /` → 200 + serves `index.html`.
- [x] Run `python3 -m unittest discover -s tests` → **red** (`server.py` does not exist yet).

## Group 2 — Server (green)

- [x] Implement `build-lab/server.py` (stdlib only): `ThreadingHTTPServer(("0.0.0.0", 3000))`.
- [x] `static file serving`: only files inside `build-lab/`, no path traversal; fall back to `index.html` only at `/`. *(Later superseded by the launch-hardening whitelist — see requirements.md.)*
- [x] SQLite helpers: `open_db(path)` + `init_db(conn)` (`CREATE TABLE IF NOT EXISTS`).
- [x] `POST /signup`: parse body (JSON or form-encoded), **server-side email validation**, `INSERT`, append `outbox.log`, return proper status codes.
- [x] `GET /subscribers`: `SELECT ... ORDER BY created_at DESC, id DESC` (newest first; `id` breaks 1-second ties), render a minimal HTML table (design-token colors optional; plain readable HTML is fine).
- [x] `log_request` decorator logs method + path + status for every handler (logging never mixed into business logic).
- [x] Body-size cap (10 KB) on requests.
- [x] All tests green: `python3 -m unittest discover -s tests`.

## Group 3 — Frontend wiring

- [x] `script.js`: replace the fake-success submit handler with `fetch("/signup", ...)`.
- [x] Success → hide form, show approved copy (`#form-success`).
- [x] Error states → inline message (400 invalid / 409 duplicate / 500-network), focus returns to the email input, form stays usable.
- [x] `aria-live` region reused for errors too (accessible).
- [x] Motion budget still exactly 3 effects.
- [x] `python3 checks.py` still green (60/60) — no regressions.

## Group 4 — Live verification + spec sync

- [x] Stop the old `python3 -m http.server` process (port 3000) and start `server.py` bound to `0.0.0.0:3000`.
- [x] Verify `http://localhost:3000/` and the Codio public URL respond (HTTP 200).
- [x] `curl -X POST /signup` → 201; repeat → 409; bad email → 400.
- [x] `curl /subscribers` shows the new row; `data/outbox.log` contains the welcome email.
- [x] Run full test suite + `checks.py` one final time.
- [x] Surface any spec differences to the founder; update `SPECS/` only after approval.
- [ ] Founder manual pass: submit form in browser → success copy; view `/subscribers`. *(Pending — part of the founder's visual browser pass, see ROADMAP.)*