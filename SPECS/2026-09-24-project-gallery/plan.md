# Plan — Project Gallery (Sample Builds)

Red/Green TDD: checks are added to `build-lab/checks.py` **before** the section
is built and must fail first (red), then the HTML/CSS makes them pass (green).

Run after every group:
- `python3 checks.py` (automated contract checks)
- `python3 -m unittest discover -s tests` stays green (server.py is untouched)

---

## Group 1 — Tests first (red)

- [x] Add a new check group to `build-lab/checks.py` ("Project Gallery"):
  - order: `id="features"` before `id="gallery"` before `id="social-proof"`;
  - `id="gallery"` present;
  - exactly **4** `.gallery-card` elements;
  - all four build names present (PLC ↔ Ignition mini rig, Vision inspection
    station, Sensor bench, Drone log station);
  - navbar link `href="#gallery"` present;
  - honest framing: banned fabricated words (`testimonial`, `review`,
    `customer`, `guarantee`) absent from the gallery; the approved one-liners
    present;
  - motion budget: no new `@keyframes` name beyond `heroPanelIn`;
  - `script.js` not modified in this feature (gallery costs zero new JS).
- [x] Run `python3 checks.py` → **red** on the new checks (9 failed; section did
      not exist yet). Verified failure is the TDD starting point.

## Group 2 — Build (green)

- [x] `index.html`:
  - Add `<section id="gallery">` between `#features` and `#social-proof`
    (section head: mono-pill "PROJECT GALLERY" + heading).
  - Add the 4 build cards (`class="card gallery-card reveal"`), each with a
    mono tag + the approved one-liner copy from requirements.md.
  - Add `<nav>`/navbar link: `Builds` → `#gallery`.
- [x] `style.css`:
  - `.gallery-grid` (auto-fit, mirrors `.feature-grid`).
  - No new hex codes (all via tokens — the existing hex checks must stay green),
    no new keyframes, no new entrance effects; hover lift comes free from the
    existing `.card.visible:hover` rule.
- [x] `script.js`: untouched.
- [x] Run `python3 checks.py` → **green** (107/107, including the existing 92).

## Group 3 — Live verification + spec sync

- [x] Restart `server.py` (bound `0.0.0.0:3000`); confirm startup banner + URLs.
- [x] Verify `http://localhost:3000/` and the Codio public URL respond (HTTP 200)
      and contain the `#gallery` section.
- [x] Check order visually/local: navbar "Builds" → scrolls to gallery between
      Features and Social Proof.
- [x] Full suite: `python3 checks.py` + `python3 -m unittest discover -s tests`
      green.
- [x] Surface any spec differences to the founder; update `SPECS/` only after
      approval. *(No differences to surface — implementation matched the spec.)*
- [ ] Founder visual pass: gallery cards read honestly, hover lift works,
      reduced-motion still disables reveal. *(Pending — part of the visual
      browser pass before Stage 6.)*