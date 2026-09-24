# Tech Stack & Engineering Rules

## Languages & Tools

| What | How |
|---|---|
| Structure | HTML5 — semantic tags (`<header>`, `<section>`, `<footer>`, etc.) |
| Styling | CSS3 — CSS custom properties (variables) for your design tokens |
| Interactivity | Vanilla JavaScript — no libraries, no frameworks |
| Animations | CSS keyframes + `IntersectionObserver` for scroll effects |
| Version Control | Git + GitHub |
| Deployment | GitHub Pages, Vercel, or Netlify |
| AI Coworker | OpenCode (your junior engineer in the terminal) |

## File Structure

All your project files live in the `build-lab/` folder:

```
build-lab/
├── index.html      ← The main page
├── style.css       ← All styles and design tokens
├── script.js       ← Interactions and animations
└── MISSION.md      ← Your Founder Notebook (fill this in as you go)
```

The `SPECS/` folder holds your project constitution (these files). It is not part of the website — it is your planning space.

## Engineering Rules

### Keep it simple
Write the most obvious solution, not the cleverest one. If a beginner can't read your code and understand it in 30 seconds, simplify it.

### One thing at a time
Build in layers: foundation first, then hero, then sections. Never generate the whole site in one prompt.

### Design tokens first
Before writing any component, define your CSS variables (colors, fonts, spacing) in `style.css`. Every component uses those variables — never hardcoded hex codes.

### No frameworks
No React, Vue, Angular, or npm packages. Everything runs in plain HTML, CSS, and JavaScript. This keeps the project simple and deployable anywhere.

### Motion budget
Maximum: 1 hero effect + 1 scroll effect + 1 microinteraction (entrance effects only). Hover
transitions on cards/buttons are interactive feedback, not entrance effects — they do not count
toward the 1+1+1 budget, but every animation, transition, and hover must have a purpose.

### Think before you prompt
Follow the cycle: **Think → Ask → Evaluate → Decide → Build**. Never accept AI output without reviewing it first.

### Better AI Requests
Every prompt to OpenCode should include:
1. **Context** — what are we building?
2. **Goal** — what needs to happen right now?
3. **Constraints** — what must not change?
4. **Design** — reference `build-lab/MISSION.md` for tokens.
5. **Validation** — how will you know it worked?
