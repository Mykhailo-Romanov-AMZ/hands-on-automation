# Validation — Launch Hardening

## 1. Automated checks (red → green)

- `python3 -m unittest discover -s tests`: red before the lockdown, green after.
  - previously leaked paths now 404: `/data/signups.db`, `/data/outbox.log`, `/server.py`,
    `/checks.py`, `/tests/test_signup.py`, any `/SPECS/**`;
  - public assets still 200: `/`, `/style.css`, `/script.js`, `/index.html`;
  - `/subscribers` → 404 without token, 404 with wrong token, 200 with the right token;
  - outbox entries carry `"mode": "dev-stub"`;
  - `/signup` rate limit triggers 429 after 10/hour per IP;
  - oversized body → 413; path traversal → 403/404.
- `python3 checks.py` (landing-page harness): green, including new checks for
  `html.js`-gated reveal, `<noscript>`, native form action, reduced-motion hero,
  and the honest social-proof copy.

## 2. Live in the browser

- `server.py` bound to `0.0.0.0:3000`; localhost + public URL respond 200.
- Startup banner announces DEV MODE and prints the founder-only `/subscribers` token URL.
- Public probes confirm: data/source/spec files → 404; `/subscribers` → 404 without token.

## 3. Manual visual + behavior pass (checklist)

- [ ] Hover/scroll animations unchanged for normal visitors.
- [ ] OS reduced-motion: hero panel does not animate; reveal content still visible.
- [ ] Disable JS: whole page still readable; `<noscript>` note appears; native form submit saves the email.
- [ ] Double-clicking **Start Your First Build** sends exactly one signup.
- [ ] Social Proof reads the honest copy (no fabricated customer).
- [ ] Privacy line visible under the form.

## 4. Specs sync (differences surfaced)

Updates to `build-lab/MISSION.md` and the feature specs are applied **only after the
founder approves** the surfaced differences (honest social-proof copy, privacy note,
motion-budget wording stays unchanged).

## Merge-ready definition

All automated checks green (red→green history intact), live URL verified, manual
checklist passes, and the founder has approved the spec updates.