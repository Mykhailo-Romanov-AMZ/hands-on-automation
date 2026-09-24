# Roadmap

This is the six-stage journey from blank canvas to live startup. Each stage builds on the last — do not skip ahead.

---

## Current State

> **In progress — Stage 5 done, Stage 6 next.** Landing page built and hardened; automated checks green (**107/107** checks, **23/23** server tests, including the launch-hardening contracts, the Project Gallery, and the newer security fix that sealed a HEAD-request whitelist bypass); all Critical + Important findings from the pre-launch review fixed; public URL live. The email-waitlist, launch-hardening, and Project Gallery loops are closed — feature specs synced to what was actually built and marked complete in `build-lab/MISSION.md`. Pending: the founder's visual browser pass (manual checklists in the feature specs + the new gallery), then Stage 6.

---

## Stage 1 — Find Something Worth Building
**Goal:** Identify a real problem worth solving.

- [ ] Use OpenCode as an interviewer to explore your interests and frustrations
- [ ] Evaluate your best ideas against the 5-Point Filter (User, Problem, Value, Feasibility, Clarity)
- [ ] Write your Founder Decision into `build-lab/MISSION.md`

---

## Stage 2 — Turn the Problem into a Product
**Goal:** Scope down to the simplest useful version.

- [ ] Pass the 20-Second Simplicity Check
- [ ] Define your Target User, Core Solution, and Primary CTA
- [ ] Update `build-lab/MISSION.md` with the refined scope

---

## Stage 3 — Give the Company a Visual Identity
**Goal:** Lock in your design system before writing any code.

- [ ] Choose 3 personality words that define your brand
- [ ] Define your color palette (Background, Primary, Accent, Text)
- [ ] Choose typography (heading font + body font) and UI rules (border radius, spacing)
- [ ] Save the full design system into `build-lab/MISSION.md`

---

## Stage 4 — Plan the Website
**Goal:** Map the story your landing page will tell.

- [ ] Draft the 8-section page architecture (Navbar → Hero → Problem → Solution → Features → Social Proof → CTA → Footer)
- [ ] Answer the core page questions for each section
- [ ] Save the page outline into `build-lab/MISSION.md`

---

## Stage 5 — Build It with Your AI Team
**Goal:** Construct the landing page in focused, reviewable layers.

- [x] Step 1: Base shell + CSS design tokens in `build-lab/index.html` and `build-lab/style.css`
- [x] Step 2: Navbar and Hero section
- [x] Step 3: Content sections (Problem, Solution, Features, Social Proof, Footer)
- [x] Add one professional component and apply the motion budget
- [x] Run the 5-Point Quality Audit and fix Critical + Important issues

---

### 5-Point Quality Audit

Run before calling the site ship-ready. Inspect the live page through five lenses — one point each:

1. **User** — does every section speak to the target learner?
2. **Problem** — is the problem (and its emotional cost) clear?
3. **Value** — is the offer and the single primary call-to-action obvious?
4. **Feasibility** — does it run: server responds, no broken links, JS valid, assets load, responsive breakpoints work?
5. **Clarity** — WCAG AA contrast on the token pairings, visible focus states, motion budget ≤ 3 effects.

Fix all Critical and Important findings before shipping.

---

## Stage 6 — Test, Show, and Ship
**Goal:** Get real feedback and launch publicly.

- [ ] Run the 1-Minute Human Test with a peer
- [ ] Triage feedback and fix the 3 most critical items
- [ ] Commit and push to GitHub
- [ ] Deploy to GitHub Pages, Vercel, or Netlify
- [ ] Submit: Startup Name, Value Prop, GitHub URL, Public URL

---

## Reflection
**Goal:** Capture what you learned as a founder.

- [ ] Answer the 5 Founder Reflection questions in `build-lab/MISSION.md`

---

## Long-Term Vision

Once the landing page is live, natural next steps could include:
- Adding a real waitlist form connected to a simple backend
- Building out individual feature pages
- Iterating on copy based on real visitor behavior
- Expanding the design system into a full component library
