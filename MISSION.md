# Founder Notebook

Welcome to your Founder Notebook. This is the single source of truth for your startup project. As founder and lead decision-maker, use this file to define your concept, guide OpenCode, and track every important decision.

---

## Mission Statement

We aim to help Michael, who struggles with procrastination, by providing an Automation Academy that helps him obtain real-life experience with projects.

**20-Second Pitch (refined):** Finished a dozen courses but built zero machines? HandsOn Automation flips that. Pick one small build, follow a 5-step checklist with a real deadline and a coach beside you, and walk away with a finished project you can show.

---

## 0. Founder Decision (Official)

*Chosen startup direction — evaluated and locked in.*

| Criterion | Evaluation | Verdict |
| :--- | :--- | :--- |
| User | Clear persona: Michael, a learner held back by procrastination. One example person, not yet the whole market. | Pass |
| Problem | Procrastination is real and relatable, but broad. The link to automation projects needs to be shown, not assumed. | Pass |
| Value | Real-life experience with projects is a genuine benefit. Sharpen later into confidence, proof of skill, and a portfolio to show. | Pass |
| Feasibility | Very doable — guided project content plus a simple website fits my skills. | Pass |
| Clarity | Simple, one sentence, easy to read. | Pass |

**Next step:** strengthen the mission by explaining *why* building real projects (instead of taking more courses) is what defeats procrastination — finished machines are proof, and proof builds momentum.

---

## 1. Vision & Problem Discovery

*The foundation: Knowledge → Problem → Solution → Value → Product*

- **Domain / Industry:** Industrial automation & technical education (PLC, HMI, machine vision, SCADA)
- **Target Audience (Who is this for?):** Michael — one specific learner who has finished PLC/HMI/vision courses but has never built a real project, and keeps putting off starting. (I am personally this person — I finished many courses at Amazon FC with no personal projects yet.) Prove it with one person before chasing a market.
- **The Core Problem (What pain point are you solving?):** Learners finish course after course, but nothing bridges the gap between watching tutorials and building a real machine. Result: no personal projects, no confidence, and no proof of skill for a job or promotion.
- **Proposed Solution:** One guided build at a time — the One-Build Sprint. One tiny, finishable rig, a 5-step checklist, a fixed deadline, and a coach walking you through it.
- **Core Feature (the single most essential function):** The One-Build Sprint — a guided project with a checklist and a deadline that ends in a finished build. Nothing else matters until this works.
- **Value Proposition (Why choose this over existing alternatives?):** "Stop collecting courses. Start building machines." Courses explain theory; HandsOn Automation gives you the guided build path, troubleshooting practice, and a finished project you can show.

---

## Visual Identity & Design System

*Define the visual and emotional tone before generating code or copy.*

- **Company / Product Name:** HandsOn Automation
- **Tagline:** Stop collecting courses. Start building machines.
- **Brand Personality / Tone of Voice (e.g., Playful, Minimalist, Bold, Professional):** Geeky · Bright · Professional
- **Color Palette (chosen: "Electric Blueprint"):**
  - Primary: `#2563EB` (electric blue)
  - Secondary: `#7C3AED` (violet)
  - Accent: `#22D3EE` (cyan)
  - Background: `#F8FAFC` (cool off-white)
  - Surface / Card: `#FFFFFF`
  - Text (Primary / Muted): `#0F172A` / `#64748B`
- **Typography:**
  - Heading Font: Space Grotesk (Google Fonts) — bold, modern, geometric
  - Body Font: Inter (Google Fonts) — readable, professional
  - Mono Label Font: JetBrains Mono (Google Fonts) — for numbers, badges, step labels, code; this is the "geeky" touch
- **Button Styles:**
  - **Primary:** filled electric blue `#2563EB`, white text, weight 600, hover `#1D4ED8`, subtle lift `0 4px 12px rgba(37,99,235,.25)`
  - **Secondary:** outlined, 1.5px violet border `#7C3AED`, violet text, hover = soft violet fill `#F3F0FF`
  - **Ghost / Link:** no fill, primary-colored text, hover underline — used in navbar links
  - Sizes: large `52px` (hero), default `44px`, small `32px`; full width on mobile
- **Motion Budget:** Entrance effects capped at 3 (1 hero + 1 scroll + 1 form microinteraction). Hover transitions on cards/buttons (e.g., `translateY(-4px)` lift) count as interactive feedback, not entrance effects.
  - `6px` — inputs, buttons, small controls
  - `12px` — cards, panels, sections
  - `16px` — hero panel, large surfaces
  - `999px` (pill) — badges, tags, avatars, step counters

---

## Page Architecture

*Approved landing-page outline — Hero → Problem → Solution → Features → Social Proof → CTA*

### Hero
- **Headline:** "Stop collecting courses. Start building machines."
- One-build sprint — ship a finished project in about a week, with a 5-step checklist and a coach by your side.
- CTA button: **Start Your First Build**

### Problem
- **Headline:** "The course trap: a dozen certificates, zero finished machines."
- You finish course after course but never build a real project.
- No project means no proof, no confidence, no promotion.

### Solution
- **Headline:** "The One-Build Sprint — your first finished project, in about a week."
- Pick one small build from the project lab.
- Follow your checklist to a real deadline while a coach keeps you moving.
- Rendered as three steps: Pick a Build → Follow Your Checklist → Solve Real Troubleshooting Drills.

### Features
- **Headline:** "Everything you need to actually finish."
- Guided 5-step build checklists.
- Real deadlines that beat procrastination · troubleshooting drills · progress badges for every finished machine.

### Social Proof
- **Headline:** "People finish here."
- Quote (honest, no fabricated customer): "One tiny build, one real deadline, one finished machine. That's the whole deal — no more courses on the shelf." — The HandsOn Automation promise
- Metric (honest): "One-Build Sprint: 5 steps · 1 week · 1 machine you can show"

### CTA
- **Headline:** "Your first finished build is one click away."
- Join the One-Build Sprint — no more courses, just one real project.
- Same button: **Start Your First Build**

---

## 3. Website Structure & Page Architecture

*Outline the narrative flow and layout of the public-facing website.*

- **Primary Goal / Conversion Action:** Get the visitor to start their first build (primary CTA: "Start Your First Build") — the action is a sign-up that kicks off their One-Build Sprint (pick a build, get the 5-step checklist and deadline).
- **Page Sections:**
  1. **Navbar:** Logo + anchor links + primary CTA button (Start Your First Build)
  2. **Hero Section:** Headline ("Stop collecting courses. Start building machines."), subheadline, primary CTA, hero visual = a mock HMI "build status" panel
  3. **Problem Section:** The certificate-collector trap (courses done, projects zero)
  4. **How It Works:** 3 steps — Pick a Build → Follow the Guided Rig Plan → Solve Real Troubleshooting Drills
  5. **Features / Value Drivers:** Guided builds, simulated rigs, troubleshooting drills, progress badges
  6. **Project Gallery:** Sample builds (PLC↔Ignition mini rig, vision inspection station, sensor bench, drone log station)
  7. **Social Proof:** Testimonial placeholders
  8. **CTA Section:** One-Build Sprint sign-up form (Start Your First Build)
  9. **Footer:** Secondary links + single CTA

---

## 4. Decision Log

*Follow the cycle: Think → Ask → Evaluate → Decide → Build*

| Date | Topic / Area | Options Considered | Final Decision & Rationale | Status |
| :--- | :--- | :--- | :--- | :--- |
| 2026-09-19 | Startup idea | Automation Hands-On Academy / PatchBoard / DroneFlightLab / SmartInspect | Idea #1 (Guided hands-on automation builds) — it is my own lived problem: courses done, no real projects yet | Done |
| 2026-09-19 | Company name | LineReady / HandsOn Automation / TinkerWorks | HandsOn Automation — clearest, most honest about the value | Done |
| 2026-09-19 | Visual style | Industrial dark / Clean lab | Clean lab — white + navy + safety orange, modern SaaS feel | Done |
| 2026-09-19 | Primary CTA | Waitlist vs Demo vs Buy | Waitlist — low friction, valid for a landing page with no backend | Done |
| 2026-09-19 | Scope down | Full academy platform vs One-Build Sprint | One-Build Sprint — one persona, one guided build, one checklist, one deadline. Smallest thing that proves people finish | Done |
| 2026-09-19 | New color palette | Electric Blueprint / Neon Terminal / Circuit Pop | Electric Blueprint — geeky + bright + professional was the stated personality; blue+violet+cyan on cool off-white keeps it modern and trustworthy | Done |
| 2026-09-24 | Close the email-waitlist + launch-hardening loop | Leave specs as-written vs sync to what was actually built | Sync (founder-directed): honest waitlist email copy, fresh random admin token per run (no guessable default), whitelist-only serving, sharing/security polish batch folded in; checks green 92/92, feature marked complete | Done |
| 2026-09-24 | Next build after close-out | Start Stage 6 vs add the missing approved section | Project Gallery — the only page-architecture section not yet on the page; build it, then run Stage 6 | Done |
| 2026-09-24 | Security inspection | Accept HEAD serving private files vs seal HEAD too | Seal it — base-class `do_HEAD` bypassed the whitelist and leaked `data/` (PII emails) existence/size; route HEAD through the same auth + whitelist checks as GET; 3 tests added (23/23 green) | Done |

---

## 5. Notes & Prompts for OpenCode

*Use this section to draft prompt briefs, review feedback, and keep track of pending tasks.*

- [x] Define core problem statement and audience
- [x] Select startup name, color palette and typography
- [x] Draft website copy for hero section
- [x] Build responsive navbar and hero components
- [x] Implement problem / how-it-works / features sections
- [x] Add waitlist form and success interaction (now a server-driven signup: SQLite + dev-mode outbox)
- [ ] Final visual polish and responsive testing
- [x] Serve and verify the public URL
- [x] Close-out: launch-hardening + polish batch complete, specs synced, checks green (92/92)
- [x] Project Gallery section: PLC↔Ignition mini rig, vision inspection station, sensor bench, drone log station (107/107 checks green)
- [ ] Founder visual browser pass, then Stage 6 (1-Minute Human Test, commit/push, deploy)

---

## 6. Founder Reflection

*Answer after the site is live.*

- [ ] What did you learn about your user by being your own user?
- [ ] Which decision was easiest / hardest, and why?
- [ ] What would you test first with real visitors?