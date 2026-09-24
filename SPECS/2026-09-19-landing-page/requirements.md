# Feature Spec — Landing Page (2026-09-19)

## Context

HandsOn Automation helps learners like Michael stop collecting courses and start
building machines. The business decisions are locked in `build-lab/MISSION.md`:
the **Electric Blueprint** design system and the approved **Page Architecture**
(Hero → Problem → Solution → Features → Social Proof → CTA).

This feature delivers the public-facing landing page that communicates the
product and its single CTA, **Start Your First Build**.

## Decisions (approved by founder)

| Decision | Choice | Why |
| :--- | :--- | :--- |
| Existing code | **Rebuild from scratch** | The current `index.html` / `style.css` / `script.js` use the old navy-orange palette, which is no longer the brand. |
| Backward compatibility | **None — old files replaced** | Keeping legacy code would conflict with the new design system. |
| Git | Skip for now | The folder is not a git repo yet; git init/branch happens at Stage 6. |
| Scope | Full landing page | All 8 sections, built in layers (see `plan.md`). |

## Scope

### In scope

- `build-lab/index.html` — semantic HTML5, all sections and copy from `Page Architecture`.
- `build-lab/style.css` — full Electric Blueprint design tokens as CSS custom properties; every component uses tokens only.
- `build-lab/script.js` — vanilla JS: scroll reveals, CTA form success state, and a small isolated logging helper. *(Updated 2026-09-24: the success state was later superseded by the server-driven waitlist flow — see `SPECS/2026-09-19-email-waitlist/`.)*
- `build-lab/checks.py` — a plain-Python validation harness written *before* the page (TDD: it is red until the page is complete).
- One primary CTA: **Start Your First Build**.
- Responsive layout (works at 360px and up), accessibility basics, motion budget.

### Out of scope

- No login, dashboards, payment, backend APIs, or databases — this is a frontend landing page (per `SPECS/MISSION.md`). *(Updated 2026-09-24: the email-waitlist feature later added a small stdlib `server.py` + SQLite waitlist, founder-approved — see `SPECS/2026-09-19-email-waitlist/`.)*
- No JavaScript frameworks or npm packages (per `SPECS/TECH.md`).
- No waitlist persistence — the form shows a client-side success state only. *(Updated 2026-09-24: superseded — the fake client-only success was replaced by a real server-driven signup.)*

## Requirements

### 1. Design tokens (the contract)

`style.css` must define CSS custom properties for every value in `MISSION.md`,
and components must use them. No hardcoded hex codes outside the token block.

- Colors: primary `#2563EB`, secondary `#7C3AED`, accent `#22D3EE`, background `#F8FAFC`, surface `#FFFFFF`, inverse (white on dark) `#FFFFFF`, text `#0F172A` / muted `#64748B`, primary hover `#1D4ED8`.
- Fonts (Google Fonts): Space Grotesk (headings), Inter (body), JetBrains Mono (labels/badges/code).
- Button styles: filled primary, outlined secondary, ghost/link; sizes 52 / 44 / 32 px.
- Radius rules: 6px controls · 12px cards · 16px hero/large · 999px (pill) badges.

### 2. Page structure

Semantic landmarks and section copy must match the approved `## Page Architecture`:

1. **Navbar** — logo + anchor links + the primary CTA button.
2. **Hero** — headline "Stop collecting courses. Start building machines.", subheadline, CTA, hero visual = mock HMI "build status" panel.
3. **Problem** — "The course trap: a dozen certificates, zero finished machines."
4. **Solution** — "The One-Build Sprint — your first finished project, in about a week." + bullets "Pick one small build from the project lab." / "Follow your checklist to a real deadline while a coach keeps you moving." Rendered as 3 steps: Pick a Build → Follow Your Checklist → Solve Real Troubleshooting Drills.
5. **Features** — "Everything you need to actually finish."
6. **Social Proof** — "People finish here." + testimonial and metric placeholders. *(Updated 2026-09-24: replaced by the honest social-proof copy in launch-hardening — the HandsOn Automation promise, no fabricated customer.)*
7. **CTA** — "Your first finished build is one click away." + Start Your First Build form.
8. **Footer** — secondary links + single CTA.

Exactly **one** primary CTA on the page (the button text **Start Your First Build** may repeat in navbar, hero, and final CTA — all are the same single action).

### 3. Behavior & motion budget

Maximum **3 animations total**: 1 hero effect + 1 scroll effect + 1 microinteraction.
CSS keyframes + `IntersectionObserver` only.

### 4. Logging

One small logging helper in `script.js` (e.g. a `log(label, data)` function using
`console.debug`). Business/handling logic must not embed logging — event handlers
and the reveal/CTA logic call the helper, keeping logging separate from logic.

### 5. Validation harness (TDD)

`checks.py` is plain Python, stdlib only, run with `python3 checks.py`. It fails
(red) until the page satisfies the contracts:

- Required files exist.
- Required design token variables exist in `style.css`.
- No hardcoded hex codes outside the token block (search classifies equal tokens as OK).
- Required Google Fonts are linked.
- Required sections/landmarks exist in `index.html`.
- Exactly one unique primary CTA action; font families and radius values are used.
- No leftover old-palette codes (`#0B2545`, `#FF6B2C`, etc.).