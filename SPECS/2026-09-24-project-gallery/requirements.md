# Requirements — Project Gallery (Sample Builds)

## Context

The landing page tells the story Hero → Problem → Solution → Features → Social
Proof → CTA. The approved Page Architecture in `build-lab/MISSION.md` (§3, item 6)
also calls for a **Project Gallery** of sample builds — the one approved section
not yet on the page. This feature adds it, so a visitor can see *what* a
One-Build Sprint looks like before they sign up.

## Decisions (founder-approved, 2026-09-24)

| Decision | Choice | Why |
| :--- | :--- | :--- |
| Placement | Between **Features** and **Social Proof** | Builds, then proof that people finish builds, flows naturally |
| Interactivity | **Static cards + hover lift only** | The motion budget is already 3/3; cards reuse `.reveal` (2/3) and the existing card hover lift (interactive feedback, not budgeted) — zero new entrance effects |
| Navbar | Add a **"Builds"** anchor link | One quick hop to the new section, matches the existing link pattern |
| Card copy | **"What you'll learn to build" framing** | Honest — examples of sprint kit, never fabricated customer results or fake metrics |
| Backward compatibility | **Pure additive** | New `<section>` added between existing sections; nothing existing is replaced |

## Scope

### In scope

- `build-lab/index.html`:
  - New `<section id="gallery">` placed between `#features` and `#social-proof`.
  - Section head follows the established pattern (mono-pill label + heading).
  - Exactly **4** build cards, each reusing the existing `card` + `reveal`
    classes, with a JetBrains Mono tag and a one-line honest description.
  - Navbar gains `<a href="#gallery">Builds</a>`.
- `build-lab/style.css`:
  - A `.gallery-grid` (same responsive auto-fit pattern as `.feature-grid`).
  - Cards use design tokens only — no new hex codes, no new keyframes.
  - No new entrance animation (budget stays 3/3).
- `build-lab/script.js`: **no changes needed** — the existing
  `IntersectionObserver` already observes every `.reveal` element present in the
  DOM, so the static cards animate on scroll for free.

### Card copy (honest "what you'll learn to build")

These four are one-line samples of sprint kit — what *you* could build in the
sprint. No fabricated testimonials, no made-up metrics.

| Tag | Name | One-liner |
| :--- | :--- | :--- |
| BUILD 01 | PLC ↔ Ignition mini rig | A micro-PLC wired to a live Ignition screen — ladder logic and HMI on a rig you can touch. |
| BUILD 02 | Vision inspection station | A camera checks parts against a pass/fail rule and lights the verdict. |
| BUILD 03 | Sensor bench | Temperature, pressure, and proximity sensors feeding one live dashboard. |
| BUILD 04 | Drone log station | A ground station that logs flight telemetry and flags out-of-range readings. |

### Motion budget

- Stays exactly **3/3**. The gallery adds **no new entrance effect**: cards reuse
  the existing `.reveal` scroll effect and the existing card hover lift
  (`translateY(-4px)`, interactive feedback only).

### Validation harness (TDD)

Add a new check group to `build-lab/checks.py` (plain Python, stdlib):

- Order: `#features` comes before `#gallery`, which comes before `#social-proof`.
- Section present: `id="gallery"` exists.
- Exactly **4** cards (`.gallery-card`).
- All four build names present (PLC↔Ignition mini rig, Vision inspection
  station, Sensor bench, Drone log station).
- Navbar "Builds" link present (`href="#gallery"`).
- No fabricated copy: gallery section shows no made-up quote/testimonial words
  (banned snippet list) — honest framing only.
- No new keyframes beyond the existing `heroPanelIn`.
- `script.js` unchanged (gallery costs the page zero new JS).

## Out of scope

- No click-through build pages / detail views.
- No filtering, sorting, or tabs.
- No photos or generated images — text-only cards keep it simple and honest.
- No new motion budget allocation.
- No changes to the single primary CTA — cards are link-free so the page still
  has exactly one action.

## Engineering rules (from `SPECS/TECH.md` + feature-spec skill)

- TDD first: checks added and run red before any HTML/CSS is written.
- Backward compatibility is intentionally preserved (pure additive).
- Beginner-friendly, obvious code only: plain HTML sections, CSS grid, tokens.