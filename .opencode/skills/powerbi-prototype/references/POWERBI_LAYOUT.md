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

## 2. Header — Logo column + accent line + diagonal banner (height: 80px)

The header has three parts: a **rectangular logo zone** on the left whose right
edge **aligns with the filter pane below it**, a slim **accent line** in the
primary color marking that edge, and a **primary banner** with a diagonal left
edge filling the rest. All backgrounds are driven by the active `CLIENT.md`.

```
┌──────────┬─┬╲──────────────────────────────────────────────┐
│ Zone A   │A│╲╲  Zone C (banner)                             │
│ (logo)   │c│ ╲╲  background: var(--primary)                  │
│ var(--   │c│   ╲╲  title + subtitle           ⓘ  (right)     │
│ surface) │e│    ╲╲                                          │
│          │n│     ╲╲                                         │
└──────────┴─t──────╲╲────────────────────────────────────────┘
  width = filter pane (200px) — right edges aligned
```

### Zone A — Logo (left, width = filter pane = 200px)
- **Background:** `var(--surface)` (cards/surface from `CLIENT.md`).
- **Shape:** **rectangle** (no diagonal). Its **right edge is vertical and
  exactly aligned with the filter pane's right edge** below it — both are the
  same width (200px), forming one continuous left column. Do **not** let the
  logo zone overhang past the filter pane.
- **Content:** client logo (`./logo.png`), **centered horizontally and
  vertically** (`flex items-center justify-center`).
- **Size:** logo height ≈ 60–70% of the header height (≈ 48–56px), `object-fit:
  contain`, max-width ≈ 88% of the 200px zone (≈ 176px).

### Accent line — primary edge marker
- **What:** a slim vertical bar in `var(--primary)` marking the logo zone /
  filter pane right edge.
- **Geometry:** `position: absolute; left: 200px; top: 0; height: 100%;
  width: 4px; background: var(--primary)`.

### Zone C — Primary banner (from x=204px to the right edge)
- **Background:** `var(--primary)` (primary / banner accent from `CLIENT.md`).
- **Left edge:** diagonal cut — the banner starts flush at the accent line at
  the bottom and recedes to the right toward the top (~48px over the header
  height). The canvas shows through the small diagonal gap.
- **CSS hint:** `left: 204px; clip-path: polygon(48px 0, 100% 0, 100% 100%, 0 100%);`
- **Content:**
  - **Title:** report title, centered, bold, `var(--surface)` text color
    (readable on the primary banner).
  - **Subtitle:** one-line context under the title, **same color as the title**
    (`var(--surface)`), only a lighter weight / slightly smaller size. **Never**
    render the subtitle in `var(--primary)` on the `var(--primary)` banner — it
    would be invisible.
  - **Info icon (ⓘ):** top-right corner, `var(--surface)` tint, opens a help
    popover explaining the report or a metric. See `POWERBI_COMPONENTS.md` §4.3
    for its size.

> **Theme note:** Because every zone reads a CSS variable from `CLIENT.md`, the
> same layout renders light (e.g. white surface + teal banner) or dark
> (e.g. slate surface + yellow banner) with no code change.

## 3. Left Filter Pane (width: 200px)

Positioned directly beneath the header on the far left. Keep it **compact** —
the pane must not force any horizontal overflow of the canvas.

- **Alignment & spacing:** the pane starts immediately under the header (no gap
  above). Its left edge is flush with the canvas left edge; the gap to the main
  content area is the standard 16px. Internal padding 16px.
- **Right edge aligned with the logo zone:** the pane is exactly as wide as the
  header logo zone (both 200px), so their right edges form one continuous
  vertical line — marked in the header by the primary accent line (see §2).
- **Pane header:** funnel icon + "Filtres" label, both **colored in
  `var(--primary)`** (the primary accent), with a bottom border `var(--border)`.
  The icon (fill/stroke) and the "Filtres" text MUST read in `var(--primary)` —
  not in `--text-secondary` / `--text-primary`. This makes the filter pane
  header part of the brand re-skin (it changes with the client's primary).
- **Slicers (stacked vertically, full-width of the 200px pane):**
  - Fiscal year (button slicer / chiclet).
  - Quarter (dropdown).
  - Month (dropdown).
  - Date range (dual-handle slider with start/end date inputs).
- **Background:** `var(--canvas)`.
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
