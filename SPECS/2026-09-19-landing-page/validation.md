# Validation — Landing Page

## How we know this feature succeeded

The feature is complete when **all** of the following are true:

### 1. Automated checks (red → green)

- `python3 checks.py` was red before the page existed and is now **green** (exit 0, no failures).
- The checks confirm, from the code itself:
  - required files exist;
  - all Electric Blueprint tokens are defined and used (no hardcoded hex outside tokens);
  - no old-palette colors remain (`#0B2545`, `#FF6B2C`);
  - Google Fonts (Space Grotesk, Inter, JetBrains Mono) are linked;
  - every `Page Architecture` section + headline is present;
  - exactly one primary CTA action with the **Start Your First Build** text.

### 2. Live in the browser

- Server binds to `0.0.0.0` on port 3000.
- `curl http://localhost:3000/` returns the page (HTTP 200).
- Public URL `https://${CODIO_HOSTNAME}-3000.codio.io/` loads the same page from any browser.

### 3. Manual visual + behavior pass (checklist)

- [ ] Palette matches Electric Blueprint — no leftover navy/orange.
- [ ] Fonts render (Space Grotesk headings, Inter body, JetBrains Mono badges).
- [ ] Hero build-status panel animates in once on load.
- [ ] Sections reveal on scroll, in order: Navbar → Hero → Problem → Solution → Features → Social Proof → CTA → Footer.
- [ ] Copy matches the approved headlines in `## Page Architecture`.
- [ ] CTA form shows a success state after submit (client-side only).
- [ ] Exactly one primary action across the whole page.
- [ ] Responsive at 360px, 768px, and desktop widths; readable contrast and visible focus states.
- [ ] Motion budget respected: ≤ 1 hero + 1 scroll + 1 microinteraction.

## Specs sync (differences surfaced)

After the build, compare the implementation against `SPECS/` and this spec. If
anything changed during building, present those differences to the founder and
only update the specs (`build-lab/MISSION.md`, `ROADMAP.md`, or this folder)
**after the founder approves**. Do not silently edit the constitution.

## Merge-ready definition

The feature is mergeable (into the working folder / git when it exists) when:
automated checks are green, the live URL is verified, the manual checklist
passes, and the founder has approved any spec updates.