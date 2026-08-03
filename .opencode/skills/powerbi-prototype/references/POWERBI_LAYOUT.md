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
  **title/subtitle** in this band.
- **Logo zone right edge:** ~245 px — aligned with the filter pane below. Do
  **not** place content over the logo zone; only `logo.png` goes there.
- **Filter pane:** left 0-245 px, below the header.
- **Main content area:** x > 245 px, y > ~97 px (after the L1/L2 navigation rows).

### Header drawing rules
- **Default (no `bg.*`)**: draw in CSS —
  - full-width banner band, height ~97px, background `var(--primary)`;
  - logo zone: left 0-245px, background `var(--surface)`, containing
    `logo.png` (max height ~70px, centered);
  - canvas body background `var(--canvas)`.
- **If `bg.svg`/`bg.png` is present**: apply on the canvas
  `background: url(./bg.svg) center top / cover no-repeat;` (use `./bg.png` for
  the PNG fallback, 3840×2160 = 2× the 1920×1080 design) and **never redraw**
  the banner, logo zone, canvas fill, or filter panel in CSS.
- The **title/subtitle** are overlaid on the banner in `var(--surface)`.
- `--primary` (in `CLIENT.md`) is used for the charts/tabs ("Filtres", active
  pills, KPI accent bars) so they match the banner.

## 3. Left Filter Pane (width: ~245px)

Positioned directly beneath the header on the far left. **Default (no `bg.*`)**:
the pane is drawn in CSS — a rounded panel on `var(--canvas)` (or `var(--surface)`
card over the canvas) with a "Filtres" label + funnel icon in `var(--primary)`,
and the slicer controls stacked inside. **If `bg.*` is present**: the pane
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

## 4. Main Canvas Area (right of filter pane, under header)

> **Data sources for this area:** the navigation tree (pages → sub-pages →
> KPIs) comes from `CLIENT.md`; the **chart choices per sub-page** (type +
> source columns) are deduced from the per-client `donnees.xlsx` (deduced in
> Phase 3). Render the KPIs/visuals of the active sub-page as specified there —
> do not improvise alternative chart types.

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
