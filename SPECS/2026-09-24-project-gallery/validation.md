# Validation — Project Gallery (Sample Builds)

How we know this feature succeeded. The feature is complete when **all** of the
following are true:

## 1. Automated checks (red → green)

- `python3 checks.py` was **red** on the new gallery checks before the section
  existed, and is now **green** (exit 0) with the new contract group passing:
  - `#gallery` sits between `#features` and `#social-proof` (source order);
  - exactly **4** build cards (`.gallery-card`);
  - all four build names and one-liners present;
  - navbar "Builds" link → `#gallery`;
  - no fabricated copy and no new keyframes — the motion budget is unchanged
    (3/3) and `script.js` is untouched.
- `python3 -m unittest discover -s tests` (23 tests) — still green; server.py was
  not modified by this feature.

## 2. Live in the browser

- `server.py` binds to `0.0.0.0:3000`; `curl http://localhost:3000/` and the
  public URL `https://${CODIO_HOSTNAME}-3000.codio.io/` return HTTP 200 and
  contain `id="gallery"`.
- Navbar **Builds** link scrolls to the gallery, positioned between Features and
  Social Proof.

## 3. Manual visual + behavior pass (checklist)

- [ ] Gallery reads as "what you'll learn to build" — honest, no fake results.
- [ ] Cards reveal on scroll (existing `.reveal` effect), hover lift works.
- [ ] Responsive grid at 360px, 768px, desktop; contrast + focus states fine.
- [ ] OS reduced-motion: no gallery entrance animation, content still visible.
- [ ] Page still has exactly one primary CTA (cards are link-free).

## 4. Specs sync (differences surfaced)

Compare the implementation against `SPECS/` and this spec after building.
Present any differences to the founder and update the specs (`build-lab/MISSION.md`,
`ROADMAP.md`, or this folder) **only after the founder approves**. Do not
silently edit the constitution.

## Merge-ready definition

The feature is mergeable when: the red→green check history is intact, automated
checks are green (checks.py + unittest), the live URL is verified, the manual
checklist passes, and the founder has approved any spec updates.