# Requirements — Email Waitlist (One-Build Sprint Signup)

## Context

The landing page's CTA form (`#sprint-form`) currently only pretends to work:
it shows a success message in the browser and saves nothing. This feature makes
the signup real in **dev mode**: the email is saved to disk, a welcome email is
"sent" (stubbed, not real), and the founder can view the subscriber list.

## Decisions (founder-approved, 2026-09-19)

| Decision | Choice | Reason |
| :--- | :--- | :--- |
| What happens on join | Save to a list **and** send the welcome email | The list is the founder's asset; the email is the promised experience |
| Email provider | **Dev mode** — no real provider yet | No credentials exist; everything works end-to-end except the final SMTP hop |
| Viewing the list | `GET /subscribers` — simple HTML table | Beginner-friendly, easy to demo |
| Backward compatibility | The old client-only success behavior is **intentionally replaced** by a server-driven flow | The fake success was a placeholder; no one depends on it |

## Scope

### Server

- New file `build-lab/server.py` — Python **stdlib only** (`http.server.ThreadingHTTPServer` + `sqlite3`). No frameworks, no ORMs, no migrations.
- Binds to `0.0.0.0:3000` (Codio public URL works).
- Serves the existing static files (`index.html`, `style.css`, `script.js`) **and** two new endpoints.

### Endpoints

| Method + path | Request | Success | Errors |
| :--- | :--- | :--- | :--- |
| `POST /signup` | `{ "email": "michael@machineworks.com" }` (JSON or form-encoded) | 201 — `{ "status": "ok" }` | 400 invalid email · 409 duplicate email |
| `GET /subscribers` | — | 200 — HTML table, newest first | — |

### Storage (SQLite)

- Database file: `build-lab/data/signups.db`
- Table: `signups(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL DEFAULT (datetime('now')))`
- Plain SQL only: `CREATE TABLE IF NOT EXISTS`, `INSERT`, `SELECT ... ORDER BY created_at DESC, id DESC` (newest first; `id` breaks the 1-second ties that `datetime('now')` produces).
- The `data/` folder is created automatically by the server.

### Outbox (dev-mode "email sending")

- File: `build-lab/data/outbox.log`
- On every successful signup, append one JSON line with: `sent_at`, `mode`, `to`, `subject`, `body`.
- Every entry carries `"mode": "dev-stub"` so the founder always knows the email was **not** really delivered.
- Subject: **You're on the One-Build Sprint list** · Body: **You're on the list. We'll email your first build plan when the One-Build Sprint opens.**
- *(Updated 2026-09-24 — honest waitlist copy: the sprint is not open yet, so we promise the plan when it opens, never an immediate delivery we cannot make.)*
- Swapping in a real provider later = replacing one `send_welcome_email()` function body.

### Frontend

- `script.js`: submit `#sprint-form` with `fetch(POST /signup)` instead of faking success.
- Success: show the approved copy ("You're in the sprint. Your first build plan is on its way.").
- Errors: inline message under the form —
  - 400: "That email doesn't look right — double-check it and try again."
  - 409: "You're already on the list. Your build plan is on its way."
  - network/500: "Couldn't join right now. Please try again in a minute."
- Motion budget unchanged: still exactly **3** effects (the form microinteraction is the same one).

## Engineering rules (from `SPECS/TECH.md` + feature-spec skill)

- Server-side email validation is the single source of truth (no regex-only checks in the client; a light pre-check is allowed).
- Logging is separated from business logic with a `log_request` decorator; handlers stay clean.
- Static serving is confined to the project folder (resolve paths inside `build-lab/`, no `..` escapes). *(Updated 2026-09-24: superseded by launch-hardening decision A — only the whitelist `{index.html, style.css, script.js}` is served; everything else returns 404.)*
- Request bodies are capped (max 10 KB).
- **No regression:** the existing landing-page harness `python3 checks.py` must stay green (60/60).

## Out of scope (for now)

- Real email delivery (SMTP/API provider) — dev-mode stub only.
- Unsubscribe / double opt-in. A `status` column can be added later without a migration tool.
- Sending the founder a notification when someone signs up.