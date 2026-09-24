# Plan — Landing Page

Approach: **Red/Green TDD**. The validation harness (`checks.py`) is written
first. Each build group ends by running `python3 checks.py`; the page is only
"green" when all checks pass.

Run after every group:
- `python3 checks.py` (automated contract checks)
- manual look at the page via the local server (see Group 6 for the Codio URL)

> **State (2026-09-24): fully built and hardened (107/107 checks).** All groups
> below are complete; items left unticked are deliberately deferred by design
> (git commit happens at Stage 6). The client-side CTA success state was later
> replaced by the server-driven waitlist (see requirements.md notes + the
> email-waitlist spec).

---

## Group 1 — Validation harness (written first, stays red)

- [x] Write `build-lab/checks.py` (plain Python, stdlib only).
- [x] Checks: required files exist (`index.html`, `style.css`, `script.js`).
- [x] Checks: required design-token variables exist in `style.css` (colors, fonts, radius).
- [x] Checks: no hardcoded hex codes outside the token block; old palette colors (`#0B2545`, `#FF6B2C`) are banned.
- [x] Checks: Google Fonts links for Space Grotesk, Inter, JetBrains Mono present in `index.html`.
- [x] Checks: each required `<section>`/landmark exists with the approved headline text.
- [x] Checks: exactly one primary CTA action; radius values used; CTA button text present.
- [x] Run `python3 checks.py` → **red** (no page yet). Verified failure is the TDD starting point.

## Group 2 — Base shell + design tokens

- [x] Replace `build-lab/index.html` with a minimal semantic skeleton (head + empty main).
- [x] Replace `build-lab/style.css`: reset, all Electric Blueprint tokens as CSS custom properties, base typography scale (Space Grotesk headings, Inter body), spacing scale, button + radius tokens referenced.
- [x] Run `python3 checks.py` → token + fonts + files checks pass; section checks still red.
- [x] Commit point (only if the user asks to commit). *(Not done — no git repo yet; commit happens at Stage 6.)* Minimal JS not needed yet.

## Group 3 — Navbar + Hero

- [x] Navbar: logo, anchor links, primary CTA button (ghost/link style links; filled primary button).
- [x] Hero: approved headline + subheadline + CTA (52px button), hero visual = mock HMI "build status" panel (badges use JetBrains Mono + pill radius).
- [x] Hero effect #1 (motion budget 1/3): the build-status panel animates in on load (CSS keyframes).
- [x] Run `python3 checks.py` → section checks for hero + navbar CTA pass.

## Group 4 — Content sections (Problem, Solution, Features, Social Proof, Footer)

- [x] Problem section: "The course trap: a dozen certificates, zero finished machines." + 2 supporting bullets.
- [x] Solution section: "The One-Build Sprint — your first finished project, in about a week." + pick-a-build / checklist/deadline bullets.
- [x] Features section: "Everything you need to actually finish." + checklist/deadline/drill/badge cards (12px radius cards).
- [x] Social Proof: "People finish here." + testimonial placeholder + metric placeholder (pill badge). *(Later replaced by the honest copy — see requirements.md.)*
- [x] Footer: secondary links + single CTA.
- [x] Scroll effect #2 (motion budget 2/3): `IntersectionObserver` reveal-on-scroll, added to `script.js`.
- [x] Run `python3 checks.py` → section checks pass.

## Group 5 — CTA + interactions + logging

- [x] CTA section: "Your first finished build is one click away." + form with **Start Your First Build** button.
- [x] Microinteraction #3 (motion budget 3/3): form submit shows a client-side success state (no backend). *(Later superseded by the server-driven waitlist flow — fetch to `POST /signup`.)*
- [x] Add the isolated `log(label, data)` helper to `script.js`; call it from event handlers and the reveal logic — never embed logging inside logic.
- [x] Ensure exactly one primary CTA action across the page.
- [x] Run `python3 checks.py` → **green** (all checks pass).

## Group 6 — Polish, verify, ship-ready

- [x] 5-Point Quality Audit (from Stage 5 of `ROADMAP.md`): fix Critical + Important issues.
- [x] Responsive check at 360px, 768px, desktop; accessibility basics (labels, contrast, focus states).
- [x] Motion budget audit: exactly ≤ 3 purposeful animations.
- [x] Start the server bound to `0.0.0.0` on port 3000; verify `http://localhost:3000/` and the Codio public URL (`https://${CODIO_HOSTNAME}-3000.codio.io/`) respond.
- [x] Cross-check: `grep` the page for old palette hex codes → zero matches.
- [x] Update `SPECS/ROADMAP.md` current state / stage checkboxes if the founder approves. *(Done 2026-09-24 during the close-out sync.)*
- [ ] Commit + push only when the user explicitly asks. *(Deferred to Stage 6.)*