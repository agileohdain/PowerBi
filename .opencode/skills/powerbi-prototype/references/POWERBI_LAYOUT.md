# Power BI Layout Specification

## 1. Canvas & Grid — Fixed PPT Slide Frame

- **Aspect ratio:** 16:9 — like a PowerPoint slide (13.333" × 7.5").
- **Fixed design resolution:** **1920 × 1080**. The dashboard is laid out for
  exactly this frame, like a slide.
- **Scale to fit (no scrollbars):** render the 1920×1080 canvas inside a
  full-viewport wrapper and scale it to the available space with CSS
  `transform: scale(...)`, preserving the 16:9 ratio, with `overflow: hidden`
  on the wrapper. The canvas must **never** produce horizontal or vertical
  scrollbars — header, filter pane, KPI row, charts, table and footer are all
  designed to fit inside the 1920×1080 frame.
  - Pattern: the `.slide` is `position: absolute; left: 0; top: 0; width: 1920px;
    height: 1080px; transform-origin: top left` inside a full-viewport
    `overflow: hidden` wrapper. A small script computes
    `s = min(viewportW/1920, viewportH/1080)` and **centers** the scaled canvas
    with a single transform:
    `translate((viewportW-1920*s)/2, (viewportH-1080*s)/2) scale(s)`. Do **not**
    center via flexbox on the unscaled box — that crops the canvas on the left
    whenever the viewport is narrower than 1920px.
- **Base grid:** 8px snap grid.
- **Outer padding:** 16px around canvas edges.
- **Card gaps:** 12px between visual cards.

### Spacing & rhythm system (BLOCKING — no ad-hoc paddings)

Inconsistent gaps read as sloppy. Normalise every vertical rhythm to the grid:

- **One spacing scale.** Only ever use `4 / 8 / 12 / 16 / 20 / 24` px (multiples
  of 4, on the 8px grid). Never an arbitrary value (no `10px`, `14px`, `19px`
  gaps between sibling blocks).
- **Content column rhythm.** The `.content` column is a single `flex` column with
  ONE consistent `gap:12px` between its blocks (`#navL1`, `#navL2`, `#kpis`,
  `#visuals`) — **no per-block `padding-top/bottom` hack**. The `.visuals` grid
  takes the remaining height (`flex:1; min-height:0`); its bottom gap to the
  footer equals the inter-card gap.
- **Filter pane internal rhythm.** The pane is a `flex` column with `gap:12px`
  between each slicer group (label + control) and `padding:16px`. The **"Effacer"
  button is pinned to the bottom** (`margin-top:auto`) so the pane reads as a
  finished panel.
- **Control height.** Every filter control (chiclet, dropdown, date input, clear
  button) shares the same height (~32px) and border-radius (8px) — a chiclet row,
  a select and the date fields align on one consistent baseline.

## 2. Header — CSS by default, `bg.svg`/`bg.png` as optional fallback

The header (logo zone + primary banner) is **drawn in CSS** from the brand
variables by default. If the user has exported a background image from their
`clients/<client>/Maquette Power BI.pptx` ("Enregistrer en tant qu'image" →
`bg.svg` preferred, vector, crisp, or `bg.png` fallback), that image takes
**priority**: apply it on the canvas and do **not** redraw the header in CSS.
In both cases the skill only overlays the title/subtitle and content.

```
┌─────────────┬╲──────────────────────────────────────────────┐
│  Zone logo  │ ╲  Bannière (Primary)                          │
│  (Surface)  │  ╲  → titre + sous-titre (var(--surface))      │
└─────────────┴───╲────────────────────────────────────────────┘
└── height ≈ 97 px (de 1080) ─┘   Corps : Canvas
```

### Geometry (for content placement)
- **Header height:** ~97 px at the 1080 design height. Place the
  **title/subtitle** in this band, **centered horizontally in the banner zone**
  (right of the diagonal break), e.g. `left:360px; right:48px; text-align:center`.
- **Logo zone (trapezoid):** `clip-path: polygon(0 0, 320px 0, 244px 97px, 0 97px)`
  — top edge 0→320 px, bottom edge 0→244 px (aligned with the filter pane below).
  Only `logo.png` goes there; do **not** place content over it. **Center the logo
  on the trapezoid centroid (~142 px), not on the full 320 px box** — add
  `padding-right: 36px` to the flex container so it doesn't appear shifted right
  toward the slanted edge. **Canonical CSS (do not deviate — BLOCKING):**
  ```css
  .logo-zone{position:absolute;left:0;top:0;width:320px;height:97px;
    background:var(--surface);
    clip-path:polygon(0 0,320px 0,244px 97px,0 97px);
    display:flex;align-items:center;justify-content:center;
    padding-right:36px;z-index:2;}
  .logo-zone img{max-height:70px;max-width:230px;object-fit:contain;}
  ```
  **Never** use `justify-content:flex-end` (pushes the logo against the slanted
  edge) nor `justify-content:flex-start`/`left` (collapses it onto the canvas
  edge): the logo must sit **visually centred in the white trapezoid**. The
  centroid of the `0→320 / 0→244` trapezoid is ≈ **142 px** from the left, so the
  flex container is `justify-content:center` **plus** `padding-right:36px` (which
  recentres the content box on the centroid, not on the 160 px mid-point of the
  full 320 px width).
- **Filter pane:** a rounded panel, `left: 11px`, `top: 116px` (~19 px gap under
  the header), width `235px`, `border-radius: 10px`, no border.
- **Main content area:** x > ~262 px, y > ~97 px (after the L1/L2 navigation rows).

### Header drawing rules
- **Default (no `bg.*`)**: draw in CSS —
  - **Bannière** (trapezoid) `var(--primary)`: full-width band, `clip-path:
    polygon(342px 0, 100% 0, 100% 97px, 267px 97px)`. The diagonal gap between
    this and the logo zone (342→320 px at top, 267→244 px at bottom) lets the
    canvas background show through = the **cassure** (diagonal break) seen in
    the `.pptx` template.
  - **Zone logo** (trapezoid) `var(--surface)`: left 0-320 px, height 97 px,
    containing `logo.png` (max height ~70px, centered).
  - canvas body background `var(--canvas)`.
- **If `bg.svg`/`bg.png` is present**: apply on the canvas
  `background: url(./bg.svg) center top / cover no-repeat;` (use `./bg.png` for
  the PNG fallback, 3840×2160 = 2× the 1920×1080 design) and **never redraw**
  the banner, logo zone, canvas fill, or filter panel in CSS.
- The **title/subtitle** are overlaid on the banner. Their color is
  **`var(--on-primary)`** — a token derived for WCAG AA contrast (see the
  on-primary rule below), **not** a hardcoded `var(--surface)`.
- **On-primary text contrast — WCAG AA, BLOCKING.** White text on a light brand
  color (e.g. `#B69E7F` taupe, `#F4D35E` yellow) fails AA badly (ratio ≈ 2,5:1,
  threshold 4,5:1) — the report title becomes hard to read, especially projected.
  Derive a single `--on-primary` token at runtime by comparing contrast:
  ```javascript
  function relLum(hex){ /* relative luminance per WCAG */ }
  function contrast(a,b){ const L=x=>{const c=relLum(x);return Math.max(c,.05)/Math.min...}; ... }
  // Pick the most legible of surface vs a dark text:
  const ON_PRIMARY = contrast(C.surface, C.primary) >= 4.5 ? C.surface : C.text;
  document.documentElement.style.setProperty('--on-primary', ON_PRIMARY);
  ```
  Apply `var(--on-primary)` to **everything sitting on the banner**: the `<h1>`
  title, the `<p>` subtitle, the active L1 pill text, the active chiclet text,
  the info-`i` glyph (when on primary). One token, one decision, AA-compliant on
  any brand color. **Never** blindly write `color:var(--surface)` on the banner.
- **Banner typography (do not deviate):** the report title is a single `<h1>`
  — `font-size:26px; font-weight:700; letter-spacing:.02em;` — and the subtitle a
  `<p>` — `font-size:13px; opacity:.92;`. **Never** use `font-weight:800` +
  `letter-spacing:.5px` (heavier, wider) nor a decorative class; keep it sober.
- A **single info button `i`** (~36 px circle) sits at the far right of the
  banner (`right: ~18px`, vertically centered). On **hover** it opens a popover
  explaining the **active page and all its sub-pages** (from `desc` fields in
  the navigation data). No per-visual info icons — only this one header icon.
- `--primary` (in `CLIENT.md`) is used for the charts/tabs ("Filtres", active
  pills, KPI accent bars) so they match the banner.

## 3. Left Filter Pane (rounded panel)

Positioned beneath the header on the far left — a **white panel `var(--surface)`**
(identical to Surface/Cards), **rounded** (`border-radius: 10px`), **floating**
with margins matching the `.pptx` template: `left: 11px`, `top: 116px`
(~19 px gap below the header), `width: 235px`, **extends down to the footer**
(`bottom: 40px`, same gap as the content column) so the pane fills the whole
left rail — **no border**. A "Filtres" label + funnel icon in `var(--primary)`
and the slicer controls are stacked inside. **If `bg.*` is present**: the pane
background (rounded panel + "Filtres" label + funnel icon) comes from the
background image — the skill only overlays the **slicer controls** on top of it.

- **Full height (BLOCKING).** The pane must descend to the footer
  (`top:116px; bottom:40px`) — never stop mid-canvas leaving an empty gap below.
  It is a `flex` column; the **"Effacer"** button sits at the bottom
  (`margin-top:auto`).
- **Alignment & spacing:** the pane starts immediately under the header (no gap
  above). Its left edge is flush with the canvas left edge; the gap to the main
  content area is the standard 16px. Internal `padding:16px`, inter-group
  `gap:12px` (see §1 spacing system).
- **Right edge:** ~245px, aligned with the logo zone above.
- **Pane header ("Filtres" + funnel icon):** in `var(--primary)` (drawn in CSS
  by default, or part of `bg.*` when present — never both).
- **Harmonized typography (BLOCKING).** One type system for the whole pane:
  - **Group labels** (Année, Pays, …): `11px / 600 / uppercase / var(--text-secondary)`,
    `letter-spacing:.05em` — same for every group.
  - **Controls** (chiclets, dropdowns, date inputs, clear button): `12px`,
    height `32px`, `border-radius:8px`, `font-weight:500`. A chiclet row and a
    select line up on the same baseline.
  - No stray smaller text (no `10px` note, no `11px` input against `12px` select).
- **Slicers (stacked vertically, overlaid on the pane):** time slicers then
  **one slicer per data dimension** (chiclets if ≤ ~6 values, else dropdown) —
  enough to fill the pane to the footer without cramming:
  - Fiscal year (button slicer / chiclet).
  - Quarter (dropdown).
  - Month (dropdown).
  - Date range (dual-handle slider with start/end date inputs).
  - Per-dimension slicers (chiclet or dropdown).
- **Clear all filters button** pinned to the bottom of the pane, full-width.
- **Interactive but NOT data-bound.** The slicers are fully interactive UI
  (click/select/drag updates their own visual state, the "● Filtres actifs" badge
  appears, "Effacer" resets) but **none of it recomputes** the dashboard — KPIs
  and visuals always show year N. See `POWERBI_COMPONENTS.md` §2.7.

## 4. Main Canvas Area (right of filter pane, under header)

> **Data sources for this area:** the navigation tree (pages → sub-pages →
> KPIs) comes from `CLIENT.md`; the **chart choices per sub-page** (type +
> source columns) are deduced from the per-client `donnees.xlsx` (deduced in
> Phase 3). Render the KPIs/visuals of the active sub-page as specified there —
> do not improvise alternative chart types.

### Container geometry (MANDATORY — never overlap the header)

The whole content column (L1 nav, L2 nav, KPI row, visuals) lives in **one
absolutely-positioned container that starts BELOW the header** and stops above
the footer. Use exactly:

```css
.content{position:absolute;left:262px;top:97px;right:0;bottom:40px;
  padding:8px 20px 0 16px;display:flex;flex-direction:column;gap:12px;
  box-sizing:border-box;}
```

**Never set `top:0` on this container** — the L1 pills and L2 links would then
render **on top of the banner** (covering the title/subtitle), a fatal layout
regression. The nav rows, KPI row and visuals grid all flow inside this
container, in this order, separated by the single `gap:12px` (§1 spacing system)
— **never** with per-block `padding-top/bottom` hacks. The visuals grid takes the
remaining height (`flex:1; min-height:0`) and its bottom edge stops at the footer
gap (`bottom:40px`), flush with the filter pane's bottom edge.

**Static sub-containers (MANDATORY).** Inside `.content`, each zone lives in
its **own static element present in the HTML from the start** —
`#navL1` (L1 pills), `#navL2` (L2 links), `#kpis` (KPI row), `#visuals`
(visuals grid). Each render rewrites **only** the `innerHTML` of the zone it
owns. **Never** compose zones by string-concatenating into a shared container
(e.g. `content.innerHTML = navHtml + content.innerHTML`): re-parsing
serialized HTML destroys live chart DOM nodes and event listeners on every
render, and breaks the separation between navigation and content (see
`POWERBI_COMPONENTS.md` §6).

### Row 0a — Primary navigation (Level-1 tabs) — COMPACT
- Rendered dynamically from `CLIENT.md` Page list.
- Layout: `flex` row of pills (`flex flex-row gap-3 w-full my-2`), one `flex-1` pill per page.
- **The pills must stay SMALL — this is a recurring regression.** Use exactly the
  Power BI pill metrics (do **not** invent a bigger custom `.pill` class):
  `font-size: 12px` (`text-xs`), `padding: 10px 16px` (`py-2.5 px-4`),
  `border-radius: 8px` (`rounded-lg`). Total pill height ≈ **34 px**, never ~48 px.
  - **Inactive tab:** `background:var(--surface); color:var(--text-secondary);
    border:1px solid var(--border); font-weight:500; cursor:pointer;`
  - **Active tab:** `background:var(--primary); color:var(--surface); font-weight:600;
    cursor:default;`
- Reference implementation uses inline Tailwind:
  `class="flex-1 py-2.5 px-4 rounded-lg text-xs text-center ..."`.
- **Anti-pattern to forbid:** a bespoke pill rule such as
  `.pill{ padding:11px 10px; font-size:13px; font-weight:600; border-radius:9px }`
  (bigger text + fatter padding) — it makes the navigation row noticeably too tall.

### Row 0b — Secondary navigation (Level-2 sub-tabs) — COMPACT
- Rendered dynamically from the active page's sub-page list in `CLIENT.md`.
- Layout: `flex` row with a bottom border under the row (`border-bottom:1px solid
  var(--border)`), height ≈ 32 px.
- **Discreet text links, `font-size:12px`** — no pill chrome, no big type.
  - **Inactive:** `color:var(--text-secondary); font-weight:500; padding-bottom:4px;`
  - **Active:** `color:var(--primary); font-weight:600; border-bottom:2px solid
    var(--primary); padding-bottom:4px;`

### Row 1 — KPI cards (height: 130px, fixed & uniform)
- Horizontal row of KPI cards (4–6 depending on page), each `flex:1`, **fixed
  height `130px`** so every card is exactly the same height regardless of content
  (the consolidation flag must never make one card taller than its neighbours).
- See `POWERBI_COMPONENTS.md` §1 for card internals.
- Some cards may carry a **"consolidation" state** (amber accent bar + amber
  pill, **never** a red dashed frame — see `POWERBI_COMPONENTS.md` §1.3).
- **Consolidation pill goes top-right** of the card (absolute, `top:12px;
  right:12px`), NOT in the footer — so the footer holds only the trend badge and
  stays one uniform line on every card. See `POWERBI_COMPONENTS.md` §1.3.

### Rows 2–3 — Main visuals (equal heights, no fixed px)
- **All main visuals on a sub-page share the exact same height.** Render them in
  a single CSS grid: `grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr`
  (two equal rows, two equal columns). The grid uses all remaining vertical
  space (`flex: 1; min-height: 0` inside the content area).
- **Never set a fixed pixel height on a visual card** (e.g. no `height: 300px`
  on a bottom row) — that breaks the equal-height rule.
- **Default arrangement: 4 main visuals in a 2×2 grid** whenever the source data
  (`donnees.xlsx`) supports 4 meaningful visuals (derived from available
  measures: line/bar/donut/hbar). Do **not** add filler visuals just to reach 4.
- **`grid-column: 1 / -1` (pleine largeur) is for 3 visuals ONLY — never with 4.**
  With 4 cards, one of them marked `.wide` (`grid-column: 1 / -1`) overflows the
  2×2 grid into a **3rd implicit row** that only grows to its content height → the
  wide card (usually the detail table) is rendered **truncated** (squashed, cut
  off). This is a recurring regression ("détail par pays tronqué"). Rule:
  - **4 visuals** → all four stay in the plain 2×2 grid, **no** `.wide`. A detail
    **table is simply one of the four equal cards** (its body scrolls:
    `flex:1; min-height:0; overflow:auto`).
  - **3 visuals** → the 3rd visual (or detail table) spans the full width of the
    second row (`grid-column: 1 / -1`); its height still equals the two upper cards.
- If only 3 visuals are justified, keep 2 columns: the 3rd visual (or the detail
  table) spans the full width of the second row (`grid-column: 1 / -1`) — its
  height equals the two upper cards.
- Charts: see `POWERBI_COMPONENTS.md` §3; tables: see
  `POWERBI_COMPONENTS.md` §3.7. Donut center callouts: see §3.4.

## 5. Footer (height: ~28px)

- Centered disclaimer text, small, muted.
- Example: *"Fictitious data — High-fidelity Power BI mockup."*
- `var(--canvas)` background, `var(--border)` top border.

## 6. Color variable contract (from CLIENT.md)

| CSS variable | CLIENT.md field | Usage |
|---|---|---|
| `--primary` | Primary / Banner Accent | Header banner, "Filtres" label + funnel icon, active tabs, KPI accent bars, chart primary series |
| `--surface` | Surface / Cards | Card backgrounds (when `--card-bg` not set), logo zone, **filter pane bg**, active-tab text on primary |
| `--canvas` | Canvas Background | Page background color, footer bg |
| `--card-bg` | Card Frame Color (default = `--surface`) | Explicit color for the "encadrés" / card frames — lets the user choose a different card color than the surface |
| `--bg-image` | Background Image (optional) | Optional `url(...)` applied to the canvas background. `none` by default. When set, render the image with a subtle dark/white overlay (per canvas luminance) to preserve readability |
| `--border` | Border / Divider | Card borders, dividers, table gridlines |
| `--on-primary` | derived (contrast vs primary) | **All text/glyphs sitting on the banner** (title, subtitle, active L1 pill text, active chiclet text) — picked for WCAG AA. See §2 on-primary rule. |

### Derived text tokens (auto-derived from canvas luminance)

The implementing agent must derive readable text colors from `--canvas`:
- **Light canvas** → `--text-primary: #0F172A`, `--text-secondary: #64748B`.
- **Dark canvas** → `--text-primary: #F1F5F9`, `--text-secondary: #94A3B8`.
- **On-primary text** → **`--on-primary`**, derived from a contrast test against
  `--primary` (§2): `--surface` when its contrast with `--primary` is ≥ 4,5:1,
  otherwise a dark text color (`--text-primary`). **Never** assume white — a
  light brand color (taupe, yellow) makes white text fail AA.

### 6.1. Color coherence check (UX/UI — blocking in SKILL Phase 1)

The user usually provides **only `Primary`**. The skill checks (SKILL.md Phase 1,
step 3b) that the other colors are coherent with the primary; any **missing** or
**incoherent** color gets a canonical proposal before generation.

**Mode.** Derived from the luminance of the provided `Canvas` (L < 0,5 → dark);
otherwise light mode by default.

| Field | Light mode (canonical) | Dark mode (canonical) | UX rationale |
|---|---|---|---|
| `Surface / Cards` | `#FFFFFF` | `#1E293B` | Elevated above the canvas — cards must "pop" |
| `Canvas Background` | `#F1F5F9` | `#0F172A` | Neutral very light/dark backdrop, never saturated (the primary is the accent) |
| `Card Frame Color` | = `Surface` | = `Surface` | One single card-frame knob by default |
| `Border / Divider` | `#CBD5E1` | `#334155` | Soft neutral grey: visible but never harsh |

**Coherence rules (every filled color is tested):**
1. **Surface vs Canvas** — the `Surface` must be lighter than the `Canvas`
   (light mode) / lighter than the canvas (dark mode, elevated tone). A surface
   darker than the canvas = invisible cards → propose the canonical.
2. **Neutral canvas** — low saturation (≤ ~12 %). A saturated/vivid canvas
   (e.g. `Canvas = Primary`) clashes with the accent → propose the neutral
   canonical (or a very light tint of the primary, L ≥ ~95 %, S ≤ ~10 %).
3. **Soft neutral border** — desaturated grey, contrast vs `Surface` between
   ~1,2 and ~2,0. A brand-colored or near-black border (contrast > 3) →
   propose the canonical.
4. **Card Frame** — defaults to `Surface`. A different `Card Frame` is accepted
   only if it still contrasts with the `Canvas` (cards visible); otherwise →
   propose `= Surface`.
5. **On-primary text** — not checked here: `--on-primary` is derived at runtime
   for WCAG AA (§2). A light `Primary` does not make the palette incoherent —
   the token adapts.

**Proposal format (blocking stop)** — a table
`field | current value | proposed value | UX reason`, then the user accepts or
edits `CLIENT.md`; re-check in a loop until coherent.
