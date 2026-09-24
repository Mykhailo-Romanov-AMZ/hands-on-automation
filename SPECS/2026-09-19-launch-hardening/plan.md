# Plan — Launch Hardening

Red/Green TDD. Tests first, red, then implementation, green.

---

## Group 0 — Feature spec

- [x] `SPECS/2026-09-19-launch-hardening/` created (this file + requirements.md + validation.md).

## Group 1 — Tests first (red)

- [x] `tests/test_signup.py` additions (temp DB/outbox, port 0, threaded server):
  - **A1** `GET /data/signups.db` → 404; `GET /data/outbox.log` → 404; `GET /server.py` → 404; `GET /SPECS/requirements.md` → 404; `GET /checks.py` → 404; `GET /tests/test_signup.py` → 404; `GET /style.css`, `GET /script.js`, `GET /` → 200.
  - **A2** `GET /subscribers` (no token) → 404; wrong token → 404; correct token → 200; correct token but bad path `/subscribers/` → 404.
  - **B** outbox entry includes `"mode": "dev-stub"`.
  - **H** 11th signup from one IP within the window → 429; first 10 → 201.
  - **security extras** oversized body → 413 stays; path traversal `/../etc/passwd` → 403/404.
- [x] `create_server(db, outbox, addr, admin_token=...)` gains the token parameter (tests pass their own).
- [x] `checks.py` additions (red first):
  - `.reveal` rules gated by `html.js` (no-JS content visible).
  - `<noscript>` element present in `index.html`.
  - form has `action="/signup"` and `method="post"`.
  - reduced-motion block disables `.hero-panel` animation.
  - honest social-proof copy present (Group 3 wording).
- [x] Run `python3 -m unittest discover -s tests` and `python3 checks.py` → **red**.

## Group 2 — Server lockdown (A, B, H, security) — green

- [x] `WHITELISTED = {"index.html", "style.css", "script.js"}`; `/` maps to `index.html`; everything else 404 (keep project-confinement guard as defence in depth).
- [x] **HEAD respects the whitelist** (2026-09-24): override `do_HEAD` to route through `_static(head=True)` / `_subscribers(head=True)`; base-class `do_HEAD` bypassed the whitelist and leaked private files via `send_head()`. Tests: HEAD on private files → 404, public files → 200, no body, `/subscribers` token control intact.
- [x] `/subscribers?token=...` → compare with `server.admin_token` (constant-time `hmac.compare_digest`); mismatch/missing → 404. Startup prints `https://.../subscribers?token=...`.
- [x] `POST /signup` rate limit: per-IP deque of timestamps, 10/hour → 429.
- [x] Outbox entries add `"mode": "dev-stub"`.
- [x] Startup banner loud: `DEV MODE: welcome emails are stubbed — no real email is sent yet.`
- [x] `python3 -m unittest discover -s tests` → green.

## Group 3 — Frontend (C, D, E, F, G) — green

- [x] **C — honest social proof** in `index.html`:
  - Quote: `"One tiny build, one real deadline, one finished machine. That's the whole deal — no more courses on the shelf."`
  - Attribution: `— The HandsOn Automation promise`
  - Metric: `One-Build Sprint: 5 steps · 1 week · 1 machine you can show`
- [x] **D — privacy microcopy** under the form: `We'll use your email only to send your One-Build Sprint plan. No spam — and you can leave the list anytime.`
- [x] **E — double-submit guard** in `script.js`: disable button while `fetch` is pending, re-enable on failure.
- [x] **F — no-JS**: tiny inline script adds `js` class to `<html>`; CSS gates `.reveal` styles on `html.js`; add `<noscript>` note; form gains `action="/signup" method="post"` (keep `novalidate`).
- [x] **G — reduced motion**: `.hero-panel { animation: none; }` inside the `prefers-reduced-motion` block.
- [x] `python3 checks.py` → green; `node --check script.js` → clean.

## Group 4 — Live verification + spec sync

- [x] Restart `server.py` (bound `0.0.0.0:3000`); check startup banner + founder URL printed.
- [x] Live probes: leaked paths → 404 (local + public URL); `/subscribers` without/with token; POST valid/duplicate/invalid; rate-limit 429.
- [x] Full suite: unittest + checks.py + `node --check`; localhost + public URL 200.
- [x] Spec-sync `MISSION.md` (Social Proof copy + privacy note) and both feature specs — **founder approval required** before editing constitution files. *(Founder directed the fixes; social-proof copy, privacy note, and honest waitlist copy applied.)*