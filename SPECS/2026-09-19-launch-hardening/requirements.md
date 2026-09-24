# Requirements — Launch Hardening

Fixes the Critical + Important findings from the pre-launch review. No Polish-tier work here.
*(Update 2026-09-24: the sharing/security polish batch — favicon, theme-color, OG/social meta
tags, security headers — was folded into this round after all; `checks.py` section 10 validates it.)*

## Context

The pre-launch review found (Critical) that every file under `build-lab/` — including
`data/signups.db` and `data/outbox.log` — is publicly downloadable, and that `/subscribers`
lists all emails with no access control. Several Important interaction/accessibility issues
also block a responsible launch.

## Decisions (founder-approved, 2026-09-19)

| # | Area | Decision |
| :--- | :--- | :--- |
| A | File serving | **Whitelist only** `index.html`, `style.css`, `script.js`. Everything else → 404. The previous "stay inside the project folder" rule is replaced by "only public assets". *(Updated 2026-09-24: `do_HEAD` was routed through the same whitelist/auth checks as GET. The base-class `do_HEAD` called the base `send_head()` and served ANY private file — a HEAD request leaked existence + Content-Length of `data/signups.db`, `data/outbox.log`, and the source files. 3 tests added.)* |
| A | `/subscribers` | Requires `?token=<ADMIN_TOKEN>`. Wrong/missing token → 404 (no hint). Token from the `ADMIN_TOKEN` env var, else a **fresh random token per run** (`secrets.token_urlsafe(16)`) loudly warned at startup — never a guessable default. Startup prints the full founder URL with token. *(Updated 2026-09-24: built reality is a fresh random token, not a fixed dev default.)* |
| B | Dev-mode email | Loud: startup banner says emails are stubbed. Every outbox entry gains `"mode": "dev-stub"`. A real provider is still the documented launch gate. |
| C | Social proof | Honest copy replaces the fabricated testimonial + metric (exact wording in plan.md Group 3). |
| D | Privacy | Microcopy under the form: usage promise + "leave the list anytime". |
| E | Double submit | Submit button disabled while the POST is in flight; re-enabled on error. |
| F | No-JS | Reveal effects gated behind `html.js` (content visible without JS). `<noscript>` note shown. Form gets native `action="/signup" method="post"` so a JS-less submit still saves the email (server already accepts form-encoded). |
| G | Reduced motion | Hero entrance animation disabled inside the existing `prefers-reduced-motion` block. |
| H | Rate limit | Simple in-memory per-IP cap on `POST /signup` (10/hour) → 429 with a friendly JSON error; the page shows the existing "couldn't join right now" message. |

## Out of scope (Polish tier, later round)

- **Security headers** — done in this round after all (server.py + `checks.py` section 10). *(Updated 2026-09-24.)*
- Access-log file — still open.
- **Tests for traversal/413** — folded in as Group 1 "security extras". *(Updated 2026-09-24.)*
- Git init — Stage 6.
- `/subscribers` styling — only minimal readable inline styling.
- **Skip-link target** — done (`index.html` `<a class="skip" href="#hero">`). *(Updated 2026-09-24.)*
- `.blink` rename — still open.
- Second-signup UX — still open.