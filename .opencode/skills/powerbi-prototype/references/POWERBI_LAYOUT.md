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
  toward the slanted edge.
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
- The **title/subtitle** are overlaid on the banner in `var(--surface)`.
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
(~19 px gap below the header), `width: 235px`, `bottom` leaves a small gap above
the footer, **no border**. A "Filtres" label + funnel icon in `var(--primary)`
and the slicer controls are stacked inside. **If `bg.*` is present**: the pane
background (rounded panel + "Filtres" label + funnel icon) comes from the
background image — the skill only overlays the **slicer controls** on top of it.

- **Alignment & spacing:** the pane starts immediately under the header (no gap
  above). Its left edge is flush with the canvas left edge; the gap to the main
  content area is the standard 16px. Internal padding 16px.
- **Right edge:** ~245px, aligned with the logo zone above.
- **Pane header ("Filtres" + funnel icon):** in `var(--primary)` (drawn in CSS
  by default, or part of `bg.*` when present — never both).
- **Slicers (stacked vertically, overlaid on the pane):**
  - Fiscal year (button slicer / chiclet).
  - Quarter (dropdown).
  - Month (dropdown).
  - Date range (dual-handle slider with start/end date inputs).
- **Clear all filters button** at the bottom of the pane, full-width.
- **These slicers are FUNCTIONAL, not decorative.** Each one is wired in JS to a
  shared filter-state object and re-renders the whole dashboard (KPIs + visuals)
  on change — see `POWERBI_COMPONENTS.md` §2.7 (wiring) and §6 (the monthly data
  architecture that makes it possible). Year chiclets are multi-select; quarter
  and month dropdowns are mutually exclusive; the date range keeps slider and
  date inputs in sync.
- **"Filtres actifs" badge:** show a small `● Filtres actifs` indicator in
  `var(--primary)` (e.g. under the pane header or in the pane header row)
  whenever at least one filter differs from the default.

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
  padding:0 20px 0 16px;display:flex;flex-direction:column;box-sizing:border-box;}
```

**Never set `top:0` on this container** — the L1 pills and L2 links would then
render **on top of the banner** (covering the title/subtitle), a fatal layout
regression. The nav rows, KPI row and visuals grid all flow inside this
container, in this order, with the visuals grid taking the remaining height
(`flex:1; min-height:0`).

**Static sub-containers (MANDATORY).** Inside `.content`, each zone lives in
its **own static element present in the HTML from the start** —
`#navL1` (L1 pills), `#navL2` (L2 links), `#kpis` (KPI row), `#visuals`
(visuals grid). Each render rewrites **only** the `innerHTML` of the zone it
owns. **Never** compose zones by string-concatenating into a shared container
(e.g. `content.innerHTML = navHtml + content.innerHTML`): re-parsing
serialized HTML destroys live chart DOM nodes and event listeners on every
render, and breaks the separation between navigation and content (see
`POWERBI_COMPONENTS.md` §6).

### Row 0a — Primary navigation (Level-1 tabs)
- Rendered dynamically from `CLIENT.md` Page list.
- Layout: `flex` row of pills, or `grid grid-cols-N` (N = number of pages).
- **Inactive tab:** `var(--surface)` bg, muted text, subtle border.
- **Active tab:** `var(--primary)` bg, `var(--surface)` text, bold.
- Height: ~40px.

### Row 0b — Secondary navigation (Level-2 sub-tabs)
- Rendered dynamically from the active page's sub-page list in `CLIENT.md`.
- Layout: `flex` row with a bottom border under the row.
- **Inactive sub-tab:** muted text, hover bg.
- **Active sub-tab:** `var(--primary)` text, bold, underline in `var(--primary)`.
- Height: ~32px.

### Row 1 — KPI cards (height: ~130px)
- Horizontal row of KPI cards (4–6 depending on page).
- See `POWERBI_COMPONENTS.md` §1 for card internals.
- Some cards may carry a **"consolidation" state** (red dashed border + label).

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

### Derived text tokens (auto-derived from canvas luminance)

The implementing agent must derive readable text colors from `--canvas`:
- **Light canvas** → `--text-primary: #0F172A`, `--text-secondary: #64748B`.
- **Dark canvas** → `--text-primary: #F1F5F9`, `--text-secondary: #94A3B8`.
- **On-primary text** → always `--surface` (readable on the banner regardless of theme).
