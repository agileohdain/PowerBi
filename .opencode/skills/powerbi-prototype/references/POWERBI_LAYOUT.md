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

## 2. Header — imported background image (`bg.svg`/`bg.png`)

The entire header (logo zone + accent + diagonal primary banner) is **authored
in PowerPoint** by the user (`powerpoint/Maquette Power BI.pptx`) and **exported
as a background image** — preferably `bg.svg` (vector, crisp), or `bg.png` as a
fallback (e.g. via `powerpoint/export-bg.ps1`). The skill does **NOT** draw the
header in CSS — it applies the background image on the canvas and overlays only
the title/subtitle and content.

```
┌─────────────┬╲──────────────────────────────────────────────┐
│  Zone logo  │ ╲  Bannière (Primary)                          │
│  (Surface)  │  ╲  → titre + sous-titre (var(--surface))      │
└─────────────┴───╲────────────────────────────────────────────┘
└── height ≈ 97 px (de 1080) ─┘   Corps : Canvas
```

### Geometry (for content placement — the chrome itself comes from the image)
- **Header height:** ~97 px at the 1080 design height (~0 to ~618 000 EMU on a
  6 858 000 EMU slide). Place the **title/subtitle** in this band.
- **Logo zone right edge:** ~245 px (≈ 1 558 925 EMU) — aligned with the filter
  pane below. Do **not** place content over the logo zone.
- **Filter pane:** left 0-245 px, below the header. Its background is part of
  the background image (white rounded panel + "Filtres" label + funnel icon, in
  `var(--primary)`).
- **Main content area:** x > 245 px, y > ~97 px (after the L1/L2 navigation rows).

### Background image rules
- Apply on the canvas: `background: url(./bg.svg) center top / cover no-repeat;`
  (use `./bg.png` if the PNG fallback was provided). SVG is crisp at any scale;
  the PNG fallback is 3840×2160 (2× the 1920×1080 design).
- **Never redraw** the banner, logo zone, canvas fill, or filter panel in CSS.
- The **title/subtitle** are overlaid on the banner in `var(--surface)`.
- The user keeps `--primary` (in `CLIENT.md`) **in sync** with the banner color
  they set in the `.pptx` — so the charts/tabs ("Filtres", active pills, KPI
  accent bars) match the banner.

## 3. Left Filter Pane (width: ~245px)

Positioned directly beneath the header on the far left. The pane **background**
(rounded panel + "Filtres" label + funnel icon) comes from the background image
(`bg.svg`/`bg.png`) — the skill only overlays the **slicer controls** on top of it.

- **Alignment & spacing:** the pane starts immediately under the header (no gap
  above). Its left edge is flush with the canvas left edge; the gap to the main
  content area is the standard 16px. Internal padding 16px.
- **Right edge:** ~245px (≈ 1 558 925 EMU), aligned with the logo zone above —
  both edges form one continuous vertical line in the background image.
- **Pane header ("Filtres" + funnel icon):** rendered in the background image
  in `var(--primary)`. Do **not** redraw it.
- **Slicers (stacked vertically, overlaid on the pane):**
  - Fiscal year (button slicer / chiclet).
  - Quarter (dropdown).
  - Month (dropdown).
  - Date range (dual-handle slider with start/end date inputs).
- **Clear all filters button** at the bottom of the pane, full-width.

## 4. Main Canvas Area (right of filter pane, under header)

> **Data sources for this area:** the navigation tree (pages → sub-pages →
> KPIs) comes from `CLIENT.md`; the **chart choices per sub-page** (type +
> source columns) come from the per-client `DATA.md` visual map. Render the
> KPIs/visuals of the active sub-page as specified there — do not improvise
> alternative chart types when a `DATA.md` map exists.

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

### Row 2 — Main visuals (height: ~450px)
- 2–3 chart cards side by side (line, donut, stacked column, etc.).
- See `POWERBI_COMPONENTS.md` §3 for chart specs.

### Row 3 — Detail table / matrix (height: ~300px)
- Full-width data table or secondary charts (heatmap, horizontal bars).
- See `POWERBI_COMPONENTS.md` §3.6–3.7.

## 5. Footer (height: ~28px)

- Centered disclaimer text, small, muted.
- Example: *"Fictitious data — High-fidelity Power BI mockup."*
- `var(--canvas)` background, `var(--border)` top border.

## 6. Color variable contract (from CLIENT.md)

| CSS variable | CLIENT.md field | Usage |
|---|---|---|
| `--primary` | Primary / Banner Accent | Header banner, "Filtres" label + funnel icon, active tabs, KPI accent bars, chart primary series |
| `--surface` | Surface / Cards | Card backgrounds (when `--card-bg` not set), logo zone, active-tab text on primary |
| `--canvas` | Canvas Background | Page background color, filter pane bg, footer bg |
| `--card-bg` | Card Frame Color (default = `--surface`) | Explicit color for the "encadrés" / card frames — lets the user choose a different card color than the surface |
| `--bg-image` | Background Image (optional) | Optional `url(...)` applied to the canvas background. `none` by default. When set, render the image with a subtle dark/white overlay (per canvas luminance) to preserve readability |
| `--border` | Border / Divider | Card borders, dividers, table gridlines |

### Derived text tokens (auto-derived from canvas luminance)

The implementing agent must derive readable text colors from `--canvas`:
- **Light canvas** → `--text-primary: #0F172A`, `--text-secondary: #64748B`.
- **Dark canvas** → `--text-primary: #F1F5F9`, `--text-secondary: #94A3B8`.
- **On-primary text** → always `--surface` (readable on the banner regardless of theme).
