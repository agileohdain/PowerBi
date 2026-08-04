# Power BI Component Catalog

This catalog defines the HTML, Tailwind CSS, and Apache ECharts implementation
rules to accurately replicate the aesthetic and interactivity of Power BI native
visual components. All brand-driven colors use CSS variables bound to the active
`CLIENT.md` so the dashboard re-skins per client.

## Color variable contract

| Variable | Source (CLIENT.md) | Used for |
|---|---|---|
| `var(--primary)` | Primary / Banner Accent | Active tabs, accent bars, primary chart series, banners, **"Filtres" label + funnel icon** |
| `var(--surface)` | Surface / Cards | Logo zone, on-primary text. Card backgrounds fall back to this when `--card-bg` is not set |
| `var(--card-bg)` | Card Frame Color (default = `--surface`) | Card / KPI frame backgrounds. **Prefer `var(--card-bg)` over `var(--surface)` for any card container** so the user can pick a card color independently from the logo zone (e.g. white cards on a colored surface) |
| `var(--canvas)` | Canvas Background | Page background, footer |
| `var(--bg-image)` | Background Image (optional) | Optional `url(...)` on the canvas. `none` by default |
| `var(--border)` | Border / Divider | Card borders, dividers, table gridlines |
| `var(--text-primary)` | derived (canvas luminance) | Primary text |
| `var(--text-secondary)` | derived (canvas luminance) | Secondary / muted text |

> See `POWERBI_LAYOUT.md` §6 for the derivation rules and the full contract.
> **Rule of thumb:** anywhere a card / KPI / table-header background is specified
> as `var(--surface)` below, render it with `var(--card-bg)` instead — that is the
> single knob the user turns to change "la couleur des encadrés".

### Reference palette (light-client example — Fonds de solidarité mockups)

The mockup SVGs in `images/` use this palette; it documents the intended
aesthetic for a light client and is **not** hardcoded:

| Role | Hex | Note |
|---|---|---|
| Primary (teal) | `#00A1B1` | Banner, active tabs, primary series |
| Secondary (green) | `#5CB57D` | Positive variance, secondary series |
| Dark accent (deep teal) | `#004250` | Header text on teal, deep emphasis |
| Consolidation alert (red) | `#FF0000` | Dashed border for "in consolidation" KPIs |
| Neutral gray | `#7F7F7F` | Axes, dividers, disabled states |

For a dark client (e.g. VELOH), `--primary: #E0BE7E`, `--canvas: #0F172A`,
`--surface: #1E293B`, `--border: #334155` — the same components render in dark
mode automatically.

---

## 1. Cards & KPIs

### 1.1. Single Metric KPI Card ("New Card Visual")
* **Usage:** Display a primary key metric with a contextual variance indicator (e.g., YoY / vs prior period).
* **CSS / Tailwind Rules:**
  * **Container:** `bg-[var(--surface)] border border-[var(--border)] rounded-lg p-4 shadow-sm relative overflow-hidden`
  * **Icon badge (optional):** a circular tinted chip holding the metric icon —
    `w-9 h-9 rounded-full flex items-center justify-center` with a soft
    `var(--primary)` tint background (e.g. `bg-[var(--primary)]/10`) and
    `var(--primary)` icon color.
  * **Title / Label:** `text-xs font-medium text-[var(--text-secondary)] uppercase tracking-wider mb-1`
  * **Callout Value:** `text-3xl font-bold text-[var(--text-primary)] tracking-tight my-1` (28px–36px)
  * **Trend Badge:** `inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold`
    * *Positive:* `bg-emerald-100 text-emerald-800 border border-emerald-200` (e.g., `+12.5% vs PY`)
    * *Negative:* `bg-rose-100 text-rose-800 border border-rose-200` (e.g., `-4.2% vs PY`)
    * *Neutral:* `bg-[var(--canvas)] text-[var(--text-secondary)] border border-[var(--border)]`
  * **Accent Bar (optional):** `absolute left-0 top-0 bottom-0 w-1 bg-[var(--primary)]`

### 1.2. Multi-Metric Card (Multi-Row Card)
* **Usage:** Group multiple secondary metrics in one structured container.
* **CSS / Tailwind Rules:**
  * **Container:** `bg-[var(--surface)] border border-[var(--border)] rounded-lg p-4 shadow-sm flex flex-col divide-y divide-[var(--border)]`
  * **Row Item:** `py-2.5 first:pt-0 last:pb-0 flex items-center justify-between`
  * **Metric Label:** `text-xs font-medium text-[var(--text-secondary)]`
  * **Metric Value:** `text-sm font-semibold text-[var(--text-primary)] font-mono`

### 1.3. Consolidation-State KPI Card (NEW)
* **Usage:** A KPI whose data is still being consolidated; visually flagged so
  reviewers do not mistake it for a final figure.
* **Trigger (data-driven, mandatory):** render a KPI in this consolidation
  state **only** when that KPI is explicitly marked `[En consolidation]` in the
  active `CLIENT.md` (see its Dynamic Navigation Structure KPI lists). If a KPI
  has no such marker, render it as a normal §1.1 card. Never apply the
  consolidation frame on your own initiative. The flag lives **only** in
  `CLIENT.md`.
* **CSS / Tailwind Rules:**
  * Start from §1.1, then override the container border:
    `border-2 border-dashed border-[#FF0000]`
  * **Flag label:** a small red pill in the card footer —
    `text-[10px] font-semibold uppercase tracking-wide text-[#FF0000] bg-[#FF0000]/10 px-1.5 py-0.5 rounded`
    with text such as "Indicateur en consolidation".
  * The value is still rendered but the dashed red frame + label make the
    provisional state unmistakable.

### 1.4. YoY ("vs N-1") Variation (MANDATORY on every time-derived KPI)

Every KPI whose value derives from the **time series** must display its
variation **vs the prior year (N-1)**, on **all** pages / sub-pages — not only
the first one. The figure is **computed from `donnees.xlsx`, never invented**.

* **Comparable periods only** — always compare matched months: a current-year
  month `i` against the **same month of the previous year** `i-12`. **Never**
  compare a partial current year against a full prior year. The YoY block exists
  **only** when at least one current-year month is selected.
  ```javascript
  const _pct = (c,p) => p ? (c-p)/p*100 : null;      // % change, null when no base
  // inside aggregates(): accumulate cX (i>=12) and pX (i-12) over monthPass() months
  const yoy = { has:cMask!==0, cKm,pKm, cRides,pRides, cMin,pMin, cActifs,pActifs };
  ```
* **Derived KPIs recompute their base** — e.g. *km/cycliste* compares
  `cKm/cActifs` vs `pKm/pActifs`, **not** the % of the already-rounded card values.
* **Render** a trend badge (§1.1) only when the value is finite: up = green,
  down = red, format `±x,x % vs N-1` (French decimal comma). **Hide** the badge
  when YoY is not computable — never show a fabricated number.
  ```javascript
  const v = dynTrend(k.dyn, agg);                    // null when not computable
  if (v!==null) trend = `${v>=0?'+':'−'}${Math.abs(v).toLocaleString('fr-FR',{maximumFractionDigits:1})} % vs N-1`;
  ```
* **Static KPIs** (dimension counts with no time axis, e.g. *Pays couverts*,
  *Vélos en flotte*) carry **no** YoY badge — they are not time-derived.

---

## 2. Slicers & Filters

### 2.1. Button Slicer ("Tile Slicer / Chiclet")
* **Usage:** Quick horizontal category filtering (e.g., Year, Region, Channel).
* **HTML Structure:** `flex flex-row flex-wrap gap-2 items-center` container with interactive targets.
* **CSS / Tailwind Rules:**
  * **Inactive State:** `px-3 py-1.5 rounded-md text-xs font-medium bg-[var(--canvas)] text-[var(--text-secondary)] border border-[var(--border)] hover:bg-[var(--border)] transition-colors cursor-pointer`
  * **Active State:** `px-3 py-1.5 rounded-md text-xs font-semibold bg-[var(--primary)] text-[var(--surface)] border border-[var(--primary)] shadow-xs cursor-pointer`
  * **Hover / Focus State:** `ring-2 ring-offset-1 ring-[var(--primary)]`

### 2.2. Dropdown Slicer
* **Usage:** Compact dropdown selector with an option list.
* **HTML Structure:** `relative` wrapper with a header button and a floating options panel.
* **CSS / Tailwind Rules:**
  * **Trigger Button:** `w-full flex items-center justify-between px-3 py-2 bg-[var(--surface)] border border-[var(--border)] rounded-md text-xs text-[var(--text-primary)] hover:border-[var(--primary)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]`
  * **Chevron Icon:** `w-4 h-4 text-[var(--text-secondary)] stroke-2`
  * **Default State:** Display `All` or `All categories` in muted text (`text-[var(--text-secondary)]`).

### 2.3. Date Range Slider
* **Usage:** Continuous time-range filtering via a dual-handle slider.
* **HTML Structure:** Dual-handle track with Start Date and End Date input fields.
* **CSS / Tailwind Rules:**
  * **Date Inputs:** `px-2 py-1 text-xs border border-[var(--border)] rounded bg-[var(--surface)] text-[var(--text-primary)] focus:outline-none focus:border-[var(--primary)]`
  * **Slider Track:** `h-1.5 bg-[var(--border)] rounded-full relative`
  * **Active Range:** `absolute h-full bg-[var(--primary)] rounded-full`
  * **Handles:** `w-4 h-4 rounded-full bg-[var(--surface)] border-2 border-[var(--primary)] shadow cursor-pointer`

### 2.4. Hierarchy / Tree Slicer
* **Usage:** Multi-level collapsible tree view (e.g., Category > Subcategory > Product).
* **HTML Structure:** Nested `<ul class="space-y-1">` list with expand/collapse icons.
* **CSS / Tailwind Rules:**
  * **Parent Item:** `flex items-center gap-2 text-xs font-medium text-[var(--text-primary)] py-1 px-2 rounded hover:bg-[var(--canvas)] cursor-pointer`
  * **Checkbox:** `w-3.5 h-3.5 rounded border-[var(--border)] text-[var(--primary)] focus:ring-[var(--primary)]`
  * **Child Indent:** `pl-5 space-y-1 border-l border-[var(--border)] ml-2`

### 2.5. Filter Pane Header
* **Usage:** Structured header for the left filter drawer.
* **HTML Structure & CSS:**
  * **Container:** `flex items-center gap-2 pb-2 mb-4 border-b border-[var(--border)] text-[var(--text-primary)] font-medium text-sm`
  * **Icon:** Funnel / Filter icon `w-4 h-4 text-[var(--text-secondary)]`

### 2.6. Clear All Filters Button
* **CSS / Tailwind Rules:**
  * `inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-[var(--text-secondary)] bg-[var(--surface)] border border-[var(--border)] rounded-md hover:bg-[var(--canvas)] hover:text-[var(--text-primary)] hover:border-[var(--primary)] transition-all cursor-pointer shadow-xs`
  * **Icon:** reset / filter icon with a clear badge (`w-3.5 h-3.5`).

### 2.7. Functional Slicers (MANDATORY — the pane must actually filter)

The filter pane is **not decorative**. Every slicer is **wired in JavaScript**
and drives the whole dashboard: any change recomputes the KPI values and
re-renders every visual (time-based charts are filtered period-by-period).

* **Single source of truth — one filter-state object** over the monthly series
  embedded from `donnees.xlsx` (see §6). A single gate decides if a month is in:
  ```javascript
  const FILT = { years:new Set(), quarter:0, month:0, start:0, end:N_MONTHS-1 };
  function monthPass(i){ const m=MONTH_META[i];
    if (FILT.years.size && !FILT.years.has(m.year)) return false;
    if (FILT.quarter && m.quarter!==FILT.quarter) return false;
    if (FILT.month   && m.month  !==FILT.month ) return false;
    return i>=FILT.start && i<=FILT.end; }
  function isFiltered(){ return FILT.years.size>0||FILT.quarter>0||FILT.month>0||FILT.start>0||FILT.end<N_MONTHS-1; }
  ```
* **`aggregates()`** walks the months, keeps only `monthPass(i)`, and rebuilds
  **all** KPI aggregates + chart series (including the YoY block, §1.4). **Every
  slicer handler ends with `renderPage()`** (which disposes and re-inits charts).
* **Year chiclets** — multi-select toggle: a click adds/removes the year from
  `FILT.years` and toggles `.active`. No year selected = all years.
* **Quarter & Month dropdowns are mutually exclusive** — selecting a quarter
  resets the month to `0`, and vice-versa.
* **Date range** — a dual-handle slider **and** two `JJ/MM/AAAA` inputs, kept in
  sync (dragging a handle updates the inputs; typing a date moves the handles),
  each mapped to a month index. Clamp `start ≤ end`.
* **Clear-all button** resets `FILT` to defaults, clears the UI state and
  re-renders.
* **"Filtres actifs" badge** — show a small indicator (e.g. `● Filtres actifs`,
  in `var(--primary)`) whenever `isFiltered()` is true; empty otherwise.

---

## 3. Data Visualizations & Tables

### 3.1. Apache ECharts Global Configuration
For all ECharts integrated into the dashboard:
* **Background:** `backgroundColor: 'transparent'` (required for seamless container integration).
* **Typography:** `fontFamily: 'Inter, system-ui, -apple-system, sans-serif'`
* **Text color:** derive from canvas luminance — use `var(--text-primary)` for axis labels and `var(--text-secondary)` for muted elements. For ECharts (which does not read CSS variables directly), pass the resolved hex at render time.
* **Grid Padding:** `grid: { top: 30, right: 20, bottom: 30, left: 40, containLabel: true }`
* **Axis Line Styling:** `axisLine: { lineStyle: { color: '#94a3b8' } }`, `axisTick: { show: false }`
* **Grid Lines:**
  * **Horizontal Grid:** `splitLine: { lineStyle: { color: '#e2e8f0', type: 'dashed' } }`
  * **Vertical Grid:** Disabled by default (`splitLine: { show: false }`)
* **Tooltip Style (native Power BI look):**
  ```javascript
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#ffffff',
    borderColor: '#cbd5e1',
    borderWidth: 1,
    padding: [8, 12],
    textStyle: { color: '#0f172a', fontSize: 12 },
    extraCssText: 'box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1); border-radius: 6px;'
  }
  ```

### 3.2. Column & Bar Charts

#### A. Vertical Column Charts (Clustered & Stacked)
* **ECharts Type:** `bar`
* **Bar Width & Radius:** `barMaxWidth: 24`, `itemStyle: { borderRadius: [3, 3, 0, 0] }`
* **Data Labels:**
  * **Clustered:** positioned on top of bars (`label: { show: true, position: 'top', fontSize: 11, color: '#334155' }`).
  * **Stacked:** totals callout on top of the stack or embedded inside segments (`stack: 'total'`).
* **Primary series color:** the resolved `--primary` hex; secondary series use the brand secondary (e.g. `#5CB57D`) or a derived tint.

#### B. Horizontal Category Bar Charts (Single & Multi-Color)
* **ECharts Type:** `bar` with inverted axes (`yAxis: { type: 'category' }`, `xAxis: { type: 'value' }`)
* **Bar Styling:** `barHeight: 16`, `itemStyle: { borderRadius: [0, 4, 4, 0] }`
* **Individual Bar Coloring:** support array-based color assignment per category item (e.g., `#00A1B1`, `#2563EB`, `#5CB57D`, `#A7F3D0`, `#94A3B8`).
* **End-of-Bar Value Labels:** `label: { show: true, position: 'right', fontSize: 12, fontWeight: 'bold', color: '#0f172a', distance: 8 }`

---

### 3.3. Line & Area Charts
* **ECharts Type:** `line`
* **Line Styling:**
  * **Stroke Width:** `lineStyle: { width: 2.5 }`
  * **Smoothing:** `smooth: 0.2` (or crisp stepped lines)
  * **Fill Opacity (Area):** `areaStyle: { opacity: 0.12 }`
* **Markers & Points:** `symbol: 'circle'`, `symbolSize: 6`, `itemStyle: { borderWidth: 2, borderColor: '#ffffff' }`
* **End-of-Line / Value Labels:** `label: { show: true, position: 'top', fontSize: 10, color: '#475569' }`
* **Multi-Series / Dual Y-Axis:** independent scaling support for count vs currency values.

---

### 3.4. Donut & Pie Charts
* **ECharts Type:** `pie`
* **Donut Sizing:** `radius: ['52%', '72%']`, `center: ['30%', '50%']`
* **Center Metric Callout — MUST be a CSS overlay, not an ECharts `title` /
  `graphic`:**
  * ECharts `title` and `graphic.text` do **not** center text on their anchor
    (they anchor by the bounding-box edge and ignore `textAlign`/`textVerticalAlign`),
    so the number drifts off-center. Render the callout as a positioned HTML
    overlay instead, for pixel-perfect, verifiable centering:
    * Synchronize the overlay anchor with the pie `center`: both use the same
      `left`/`top` value (e.g. `center: ['30%','50%']` → overlay
      `left: 30%; top: 50%`).
    * Wrap the chart: `.chart-holder { position: relative; flex: 1; min-height: 0; }`
      with the ECharts div inside as `position: absolute; inset: 0;`.
    * Overlay:
      ```css
      .donut-center{position:absolute;left:30%;top:50%;transform:translate(-50%,-50%);
        display:flex;flex-direction:column;align-items:center;pointer-events:none;line-height:1;text-align:center;}
      .donut-center .dc-value{font-size:22px;font-weight:700;color:var(--text-primary);}
      .donut-center .dc-sub{font-size:11px;color:var(--text-secondary);margin-top:4px;}
      ```
    * Main Value: `dc-value` (e.g. `126.4 k`, 22px bold). Sub-label: `dc-sub`
      (e.g. `calls received`, 11px muted).
* **Leader Line Labels:** `label: { show: true, formatter: '{c}\n({d}%)', distanceToLabelLine: 5 }`
* **Legend:** `legend: { orient: 'vertical', right: 16, top: 'center', itemGap: 12, textStyle: { color: '#475569', fontSize: 11 } }`

---

### 3.5. Heatmap & Intensity Matrix Visuals
* **ECharts Type:** `heatmap`
* **Usage:** Time/day distribution matrices (e.g., days of the week vs hours of the day).
* **Grid Formatting:** cell borders `itemStyle: { borderWidth: 2, borderColor: '#ffffff' }`
* **Visual Map / Color Gradient:**
  * Low Intensity: light pale green/yellow (`#FEF9C3` / `#E0F2FE`)
  * High Intensity: deep teal/navy blue (`#004250` / `#005F73`)
* **In-Cell Labels:** `label: { show: true, fontSize: 10, color: '#0f172a', formatter: '{c}%' }`

---

### 3.6. Progress Bars & Target Bullet Visuals
* **Usage:** Displaying progress toward a percentage goal (e.g., Satisfaction Index, Effort Score).
* **Structure HTML / Tailwind:**
  * **Layout:** flex row with Label (left), Progress Track (center), Value + Badge (right).
  * **Track Background:** `w-full h-3 bg-[var(--canvas)] rounded-full overflow-hidden`
  * **Filled Bar:** `h-full bg-[var(--primary)] rounded-full transition-all`
  * **Metric Callout:** `text-sm font-bold text-[var(--text-primary)]` + Trend pill (`text-xs font-semibold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded`)

---

### 3.7. Data Matrix & Table
* **Usage:** Detailed tabular data display.
* **HTML Structure:** standard HTML table `<table class="w-full text-left border-collapse">`.
* **CSS / Tailwind Rules:**
  * **Header (`<thead>`):** `bg-[var(--primary)] text-[var(--surface)] font-semibold text-xs`
  * **Header Cells (`<th>`):** `px-3 py-2 border-b border-[var(--border)] uppercase tracking-wider`
  * **Body Rows (`<tbody> tr`):** `hover:bg-[var(--canvas)] transition-colors`
  * **Zebra Striping:** even rows `bg-[var(--surface)]`, odd rows `bg-[var(--canvas)]` (subtle).
  * **Data Cells (`<td>`):** `px-3 py-2 text-xs text-[var(--text-primary)] border-b border-[var(--border)] font-normal`
  * **Numeric Values:** right-aligned with monospace font (`text-right font-mono`).

---

## 4. Buttons & Action Controls

### 4.1. Two-Tier Dynamic Navigation System

#### 4.1.1. Level-1 Primary Navigation (Tile / Pill Style)
* **Usage:** Main section switcher driven by the `CLIENT.md` page configuration. Adapts layout based on the total number of main pages.
* **HTML Structure:** `flex flex-row gap-3 w-full my-2` or `grid grid-cols-N gap-3 w-full my-2` (where N equals the number of pages defined in `CLIENT.md`).
* **Inactive Tab:** `flex-1 py-2.5 px-4 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-xs font-medium text-[var(--text-secondary)] hover:bg-[var(--canvas)] transition-all text-center cursor-pointer shadow-2xs`
* **Active Tab:** `flex-1 py-2.5 px-4 bg-[var(--primary)] text-[var(--surface)] font-semibold text-xs rounded-lg text-center shadow-sm cursor-default`

#### 4.1.2. Level-2 Secondary Sub-Navigation (Discreet Text-Link Style)
* **Usage:** Sub-view switcher displayed directly underneath the active primary tab. Driven dynamically by the active page's sub-pages list in `CLIENT.md`.
* **Style:** **discreet text links** — no pill background, no border box, no button chrome. Just spaced text items with a single bottom rule under the row.
* **HTML Structure:** `flex flex-row items-center gap-6 w-full mb-3 pb-1 border-b border-[var(--border)]`
* **Inactive Sub-Tab:** `text-[12px] font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] cursor-pointer bg-transparent border-0` (plain text link, generous horizontal spacing).
* **Active Sub-Tab:** `text-[12px] font-semibold text-[var(--primary)] cursor-default bg-transparent border-0 border-b-2 border-[var(--primary)] pb-1` — the only emphasis is the `var(--primary)` text color, the bold weight, and a 2px `var(--primary)` underline.

### 4.2. View / Bookmark Toggle
* **Usage:** Segmented toggle control (e.g., "Executive View" vs "Detailed View").
* **HTML Structure:** `inline-flex p-1 bg-[var(--border)] rounded-lg`
* **Inactive Button:** `px-3 py-1 text-xs font-medium text-[var(--text-secondary)] rounded-md hover:text-[var(--text-primary)] cursor-pointer`
* **Active Button:** `px-3 py-1 text-xs font-semibold text-[var(--text-primary)] bg-[var(--surface)] rounded-md shadow-xs cursor-default`

### 4.3. Info / Tooltip (single header button + hover popover)
* **Usage:** **one** info button `i`, large, in the top-right of the **header
  banner**. On **hover** it opens a popover explaining the **active page and all
  of its sub-pages**. Do **not** render a separate `i` icon on each visual/card.
* **Size:** clearly visible — **`w-9 h-9` (36px)**-ish circle with a serif
  `i` glyph (`text-lg`, bold).
* **CSS / Tailwind Rules (icon):**
  * `w-9 h-9 rounded-full bg-[var(--surface)] text-[var(--primary)] inline-flex items-center justify-center text-lg font-serif font-extrabold cursor-help shadow-md`
* **Popover (hover) — MANDATORY.** A white card (`var(--surface)`, `border`,
  `border-radius: 10px`, shadow) anchored at the top-right (`right: 16px`,
  `z-index` high, width ~400px). Content **leads with the ACTIVE page and the
  currently SELECTED sub-page**: page title (`var(--primary)`, uppercase) + page
  description, then a divider, then each sub-page with a colored dot (blue =
  active, `var(--primary)` = inactive), its name and description — the selected
  one visually emphasised. **Re-render the popover on every navigation change**
  (same `renderPage()` pass).
* **Hover reachability (do not leave a dead zone).** If the popover `top` sits
  well below the icon, the pointer crosses a non-hover gap while moving from the
  icon to the card and the popover closes before it can be read. Prevent this by
  wrapping the icon and the popover in a **shared hover container** and toggling
  on the container — guaranteed continuous hover:
  ```css
  .info-wrap{position:absolute;top:26px;right:16px;z-index:70;}
  .info-wrap .popover{position:absolute;top:44px;right:0;width:400px;display:none;}
  .info-wrap:hover .popover{display:block;}
  ```
  (Alternative: position the popover so its top edge overlaps the icon's bottom
  edge — `top` ≈ icon bottom − 2px — so hover never breaks.)

---

## 5. Containers & Structural Shapes

### 5.1. Card Container
* **Usage:** Standard enclosing card component for any Power BI visual on the canvas grid.
* **CSS / Tailwind Rules:**
  * `bg-[var(--surface)] border border-[var(--border)] rounded-lg p-4 shadow-xs flex flex-col justify-between h-full`
  * **Card Header:** `flex items-center justify-between mb-3 border-b border-[var(--border)] pb-2`
  * **Card Title:** `text-sm font-semibold text-[var(--text-primary)] tracking-tight`
  * **Subtitle / Unit:** `text-xs text-[var(--text-secondary)] font-normal ml-2`

### 5.2. Info Note Bar (NEW)
* **Usage:** A small informational note rendered at the bottom of a card or
  section — an info icon plus one line of context text (e.g., a methodology
  reminder or a data caveat).
* **CSS / Tailwind Rules:**
  * **Container:** `flex items-start gap-2 mt-3 pt-2 border-t border-[var(--border)] text-[var(--text-secondary)] text-[11px] leading-snug`
  * **Icon:** `w-4 h-4 flex-shrink-0 mt-0.5 text-[var(--text-secondary)]` (info / ⓘ glyph).
  * **Text:** `font-normal`.

### 5.3. Header Line / Divider
* **Usage:** Clean visual separator between dashboard sections or header panels.
* **CSS / Tailwind Rules:**
  * `w-full h-px bg-[var(--border)] my-4`

### 5.4. Footer Disclaimer (NEW)
* **Usage:** Centered disclaimer at the bottom of the canvas marking the data
  as fictitious / mockup.
* **CSS / Tailwind Rules:**
  * **Container:** `w-full text-center py-2 text-[11px] text-[var(--text-secondary)] bg-[var(--canvas)] border-t border-[var(--border)]`
  * **Text example:** *"Fictitious data — High-fidelity Power BI mockup."*

---

## 6. Data Architecture & Interactivity (MANDATORY)

Functional filters (§2.7) and YoY KPIs (§1.4) are only possible if the mockup
**embeds the data at month grain**. Do not hardcode final chart arrays only —
embed the underlying monthly series so they can be filtered and compared.

* **Monthly fact series** (one value per month, chronologically ordered), one
  array per core measure — e.g. `KM[]`, `RIDES[]`, `MINUTES[]`.
* **`MONTH_META`** derived from the labels — `{year, month, quarter}` per index —
  so year/quarter/month filtering needs no re-parsing:
  ```javascript
  const MONTH_META = KM_LABELS.map((_,i)=>({year:…, month:i%12+1, quarter:Math.floor((i%12)/3)+1}));
  ```
* **Entity activity as a bitmask** — for "active entities" KPIs (e.g. active
  cyclists), store one integer per entity where **bit `i` = active on month `i`**.
  `actifs` for any filtered period = count of entities whose mask ∩ period-mask ≠ 0.
  This makes the KPI correct under **any** filter combination.
* **Per-dimension monthly series** for every dimension you chart or filter by
  (e.g. `KM_PAYS_M`, `KM_MARQUE_M`): `{dim: [per-month values]}` so bars/lines
  and YoY stay correct when the period changes.
* **Static dimension data** (donuts, tables with no time axis) may stay as final
  `{name, value}` arrays.
* **`aggregates()`** is the single recompute entry point: it folds the months
  passing `monthPass()` into KPI aggregates **and** chart series **and** the YoY
  block, then `renderPage()` paints nav, KPI cards, visuals, info popover and the
  "Filtres actifs" badge from it. Charts are disposed and re-initialised
  (`disposeCharts()` + `echarts.init`) inside `requestAnimationFrame`.

> A mockup that only embeds final per-sub-page arrays **cannot** filter or
> compute YoY — that is the regression this section exists to prevent.
