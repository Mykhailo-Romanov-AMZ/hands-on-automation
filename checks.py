#!/usr/bin/env python3
"""checks.py — contract checker for the HandsOn Automation landing page.

Plain Python, stdlib only. Run with:  python3 checks.py

The page is only "green" when every check passes (exit code 0).
This file is written BEFORE the page so it can be red first (TDD).

Checks come from build-lab/SPECS/2026-09-19-landing-page/requirements.md
and the approved Page Architecture in build-lab/MISSION.md.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
INDEX = HERE / "index.html"
STYLE = HERE / "style.css"
SCRIPT = HERE / "script.js"

html = INDEX.read_text() if INDEX.exists() else ""
css = STYLE.read_text() if STYLE.exists() else ""

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


# ---------------------------------------------------------------
# 1. Required files
# ---------------------------------------------------------------
check("files: index.html exists", INDEX.exists())
check("files: style.css exists", STYLE.exists())
check("files: script.js exists", SCRIPT.exists())

# ---------------------------------------------------------------
# 2. Design tokens (the contract from MISSION.md)
# ---------------------------------------------------------------
TOKENS = [
    "--color-primary",
    "--color-secondary",
    "--color-accent",
    "--color-background",
    "--color-surface",
    "--color-text",
    "--color-text-muted",
    "--color-primary-hover",
    "--font-heading",
    "--font-body",
    "--font-mono",
    "--radius-sm",
    "--radius-md",
    "--radius-lg",
    "--radius-pill",
    "--color-inverse",
    "--color-panel-muted",
]
for token in TOKENS:
    check(f"token: {token} defined in style.css", token in css)

# ---------------------------------------------------------------
# 3. No leftover old-palette colors anywhere
# ---------------------------------------------------------------
BANNED = ["#0B2545", "#13315C", "#FF6B2C", "#E85A1D", "#243B53", "#627D98", "#9FB3CC"]
for hex_code in BANNED:
    detail = ""
    if hex_code in html:
        detail += "found in index.html "
    if hex_code in css:
        detail += "found in style.css "
    check(f"no old palette color {hex_code}", not detail, detail.strip())

# ---------------------------------------------------------------
# 4. Every hex code in style.css must be from the allowed set
#    (no hardcoded colors sneaking in outside the token block)
# ---------------------------------------------------------------
ALLOWED = {
    "#2563EB",  # primary (electric blue)
    "#1D4ED8",  # primary hover
    "#7C3AED",  # secondary (violet)
    "#22D3EE",  # accent (cyan)
    "#F8FAFC",  # background
    "#FFFFFF",  # surface / white text
    "#0F172A",  # text
    "#64748B",  # text muted
    "#F3F0FF",  # secondary soft fill on hover
    "#8B98AD",  # panel-muted (text on dark hero panel, WCAG AA)
}
root_match = re.search(r":root\s*\{(.*?)\}", css, re.S)
root_block = root_match.group(1) if root_match else ""
outside_block = css.replace(root_match.group(0), "", 1) if root_match else css
hexes_in_css = re.findall(r"#[0-9A-Fa-f]{6}", css)
stray = sorted({h.upper() for h in hexes_in_css} - ALLOWED)
check("css: only allowed hex codes", not stray, ", ".join(stray))
hexes_outside = re.findall(r"#[0-9A-Fa-f]{6}", outside_block)
check(
    "css: no hex codes outside the :root token block",
    not hexes_outside,
    ", ".join(sorted(set(hexes_outside))),
)

# ---------------------------------------------------------------
# 5. Google Fonts (Space Grotesk, Inter, JetBrains Mono)
# ---------------------------------------------------------------
check("fonts: Google Fonts stylesheet linked", "fonts.googleapis.com" in html)
for font in ["Space+Grotesk", "Inter", "JetBrains+Mono"]:
    check(f"fonts: {font} requested", font in html)

# ---------------------------------------------------------------
# 6. Page Architecture sections + approved headlines
# ---------------------------------------------------------------
SECTIONS = [
    ("section id=navbar", 'id="navbar"'),
    ("section id=hero", 'id="hero"'),
    ("section id=problem", 'id="problem"'),
    ("section id=solution", 'id="solution"'),
    ("section id=features", 'id="features"'),
    ("section id=social-proof", 'id="social-proof"'),
    ("section id=cta", 'id="cta"'),
    ("footer id=footer", 'id="footer"'),
]
for name, marker in SECTIONS:
    check(f"page: {name} present", marker in html)

HEADLINES = [
    "Stop collecting courses. Start building machines.",
    "The course trap: a dozen certificates, zero finished machines.",
    "The One-Build Sprint",
    "Everything you need to actually finish.",
    "People finish here.",
    "Your first finished build is one click away.",
]
for headline in HEADLINES:
    check(f"copy: headline present ({headline[:44]}...)", headline in html)

# ---------------------------------------------------------------
# 7. CTA rules (one primary action; one sign-up form)
# ---------------------------------------------------------------
check("cta: 'Start Your First Build' text present", "Start Your First Build" in html)
form_count = len(re.findall(r"<form\b", html))
check("cta: exactly one sign-up form", form_count == 1, f"found {form_count}")

# ---------------------------------------------------------------
# 8. Radius + button token usage exists (not just defined)
# ---------------------------------------------------------------
for token, usage in [
    ("--radius-sm (6px controls)", "var(--radius-sm)"),
    ("--radius-md (12px cards)", "var(--radius-md)"),
    ("--radius-lg (16px hero/large)", "var(--radius-lg)"),
    ("--radius-pill (999px badges)", "var(--radius-pill)"),
]:
    check(f"radius rule used: {token}", usage.replace("var(", "").replace(")", "") in css
          and usage in css)

check("buttons: .btn-primary exists in css", ".btn-primary" in css)
check("buttons: .btn-secondary exists in css", ".btn-secondary" in css)

# ---------------------------------------------------------------
# 9. Motion budget: at most 3 animation-related items
# ---------------------------------------------------------------
keyframe_names = re.findall(r"@keyframes\s+([\w-]+)", css)
hero_anim = "heroPanelIn" in keyframe_names
reveal = ".reveal" in css and "IntersectionObserver" in SCRIPT.read_text() if SCRIPT.exists() else False
micro = "sprint-form" in html
budget_spent = [hero_anim, reveal, micro]
check("motion: hero effect present (1/3)", hero_anim)
check("motion: scroll reveal present (2/3)", reveal)
check("motion: CTA microinteraction present (3/3)", micro)
check(
    "motion: budget <= 3 effects",
    sum(1 for b in budget_spent if b) <= 3,
    f"spent {sum(1 for b in budget_spent if b)}/3",
)

# Feature-card hover lift: translateY(-4px) must actually win the
# cascade once a card is revealed (.reveal.visible comes later in the
# file, so the hover rule needs higher specificity).
check(
    "motion: feature-card hover lift present (translateY(-4px))",
    "transform: translateY(-4px)" in css and ".card.visible:hover" in css,
)
check(
    "motion: hover lift transitions smoothly (0.2s transform + shadow)",
    "transition: transform 0.2s ease, box-shadow 0.2s ease" in css,
)
check(
    "motion: hover lift disabled for reduced-motion users",
    "@media (prefers-reduced-motion" in css
    and ".card.visible:hover" in css
    and "transform: none" in css,
)

# Launch hardening: progressive enhancement + honest content.
check("motion: reveal effects gated behind html.js (no-JS content visible)",
      "html.js .reveal" in css)
check("a11y: <noscript> fallback present", "<noscript>" in html)
check("progressive: form posts natively",
      'action="/signup"' in html and 'method="post"' in html)
check("a11y: hero animation disabled for reduced motion",
      "prefers-reduced-motion" in css and ".hero-panel" in css and "animation: none" in css)
check("copy: social proof is honest (no fabricated customer)",
      "That's the whole deal" in html
      and "The HandsOn Automation promise" in html
      and "5 steps" in html)
check("copy: privacy line under the form",
      "We'll use your email only to send your One-Build Sprint plan" in html)

# Launch-hardening round 2: a11y contrast + interaction + responsive contracts.
check("a11y: hero-panel text uses the readable panel-muted token",
      "var(--color-panel-muted)" in css)
check("a11y: focus-visible outline uses the dark text token (visible on light)",
      "outline: 3px solid var(--color-text)" in css)
check("a11y: focus outline switched to accent on the dark CTA section",
      "outline-color: var(--color-accent)" in css)
check("interaction: double-submit guard disables the submit button",
      "submitButton.disabled = true" in SCRIPT.read_text()
      and "submitButton.disabled = false" in SCRIPT.read_text())
check("responsive: navbar can wrap on small screens",
      "flex-wrap: wrap" in css and "justify-content: center" in css)
check("responsive: anchor targets clear the sticky navbar",
      "scroll-margin-top" in css)

# ---------------------------------------------------------------
# 10. Polish batch: sharing meta + security headers
# ---------------------------------------------------------------
check("sharing: favicon <link rel=icon> present (no bare tab)",
      'rel="icon"' in html)
check("sharing: theme-color meta present (mobile chrome paints correctly)",
      'name="theme-color"' in html)
check("sharing: og:title present", 'property="og:title"' in html)
check("sharing: og:description present", 'property="og:description"' in html)
check("sharing: og:url present", 'property="og:url"' in html)
check("sharing: og:type present (website)", 'property="og:type"' in html)
check("sharing: og:site_name present", 'property="og:site_name"' in html)
check("sharing: twitter:card present (summary)",
      'name="twitter:card"' in html)
check("sharing: og:image NOT fabricated (no og:image meta tag — honest card)",
      'property="og:image"' not in html and 'name="og:image"' not in html)
check("sharing: og:image parked with an honest explanation in the source",
      "parked" in html.lower() and       "no-fabricated-card" in html.lower() and "honest park" in html.lower())

# Security headers must be present AND must not break the design contract
# (Google Fonts + local CSS/JS must keep loading under the CSP we ship).
server = open("server.py").read() if Path("server.py").exists() else ""
for header in [
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Content-Security-Policy",
]:
    check(f"security: server sends {header}", header in server)
check("security: server sends X-Content-Type-Options: nosniff",
      "X-Content-Type-Options" in server and "nosniff" in server)

check("security: CSP allows Google Fonts (fonts.googleapis.com)",
      "fonts.googleapis.com" in server)
check("security: CSP allows font files (fonts.gstatic.com)",
      "fonts.gstatic.com" in server)
check("security: CSP allows local CSS/JS (self, no remote script)",
      "script-src 'self'" in server and "style-src 'self'" in server)

# ---------------------------------------------------------------
# 11. Project Gallery (SPECS/2026-09-24-project-gallery)
# ---------------------------------------------------------------
gallery_pos = html.find('id="gallery"')
gallery_end = html.find("</section>", gallery_pos)
gallery_block = html[gallery_pos:gallery_end] if gallery_pos != -1 and gallery_end != -1 else ""
pos = lambda s: html.find(s)

check("gallery: section id=gallery present", gallery_pos != -1)
check(
    "gallery: #features before #gallery before #social-proof",
    pos('id="features"') < pos('id="gallery"') < pos('id="social-proof"'),
)
for name in [
    "PLC",
    "Ignition",
    "Vision inspection station",
    "Sensor bench",
    "Drone log station",
]:
    check(f"gallery: build card {name!r} present", name in html)
for word in ["testimonial", "review", "customer", "guarantee"]:
    check(
        f"gallery: honest copy (no {word!r} in gallery)",
        word not in gallery_block.lower(),
    )
check(
    "gallery: exactly 4 build cards (.gallery-card)",
    html.count("gallery-card") == 4,
    f"found {html.count('gallery-card')}",
)
check("gallery: navbar 'Builds' link to #gallery",
      'href="#gallery"' in html and "Builds" in html)
check("gallery: no new keyframes (motion budget unchanged)",
      set(keyframe_names) <= {"heroPanelIn"})
check("gallery: zero new JS (script.js has no #gallery hook)",
      "gallery" not in SCRIPT.read_text())

# ---------------------------------------------------------------
# Result
# ---------------------------------------------------------------
if failures:
    print(f"\n{len(failures)} check(s) FAILED.")
    sys.exit(1)
print("\nAll checks passed. The landing page matches the spec.")
sys.exit(0)