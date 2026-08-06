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

### Chart palette — ALWAYS derived from `--primary` (BLOCKING)

**Never** use a fixed rainbow palette (`red / blue / green / yellow / purple`).
A dashboard whose donut slices and brand-lines clash with the brand color looks
unprofessional. The chart palette is **derived from `--primary`** so every
visual harmonizes with the banner.

* Derive **one** palette per client with `derivePalette(C.primary)` and reuse it
  for **all** categorical coloring: donut slices (§3.4), hbar bars (§3.2.B) and
  multi-series temporal lines (§3.3). The first entry is the primary itself.
* The **"Autres"** residual bar/slice and the **N-1** temporal line use a single
  **neutral** (`C.neutral`), never a palette slot.
* One reserved, non-palette color family: the **trend-badge green/red/neutral**
  (§1.1) — semantic, not categorical.

```javascript
function hexToHsl(hex){
  const h = hex.replace('#',''); const r=parseInt(h.substr(0,2),16)/255,
    g=parseInt(h.substr(2,2),16)/255, b=parseInt(h.substr(4,2),16)/255;
  const mx=Math.max(r,g,b), mn=Math.min(r,g,b); let hh,s,l=(mx+mn)/2;
  if(mx===mn){hh=0;s=0;} else {
    const d=mx-mn; s=l>0.5?d/(2-mx-mn):d/(mx+mn);
    switch(mx){case r:hh=(g-b)/d+(g<b?6:0);break;case g:hh=(b-r)/d+2;break;default:hh=(r-g)/d+4;}
    hh*=60;
  }
  return [hh,s*100,l*100];
}
function hslToHex(h,s,l){
  s/=100; l/=100; const k=n=>(n+h/30)%12, a=s*Math.min(l,1-l),
    f=n=>l-a*Math.max(-1,Math.min(k(n)-3,Math.min(9-k(n),1))),
    tx=x=>Math.round(x*255).toString(16).padStart(2,'0');
  return '#'+tx(f(0))+tx(f(8))+tx(f(4));
}
// 6 colors anchored on primary: [primary, shade, tint, analogous, muted-complement, desaturated]
function derivePalette(primary){
  const [h,s,l] = hexToHsl(primary);
  return [
    primary,
    hslToHex(h, s, Math.max(15, l-18)),
    hslToHex(h, Math.max(10,s-12), Math.min(92,l+15)),
    hslToHex((h+28)%360, Math.max(18,s-8), Math.min(62,l)),
    hslToHex((h+180)%360, Math.max(14,s-22), Math.min(55,l)),
    hslToHex(h, Math.max(8,s-28), l)
  ];
}
// THEME block, resolved once (ECharts can't read CSS vars):
//   C = { primary, surface, canvas, border, cardBg, text, textSub,
//         palette: derivePalette(primary), neutral: <light grey from --border> }
```

The components below render in **light or dark** mode automatically once the
CSS variables are set (e.g. a dark client: `--primary:#E0BE7E`,
`--canvas:#0F172A`, `--surface:#1E293B`, `--border:#334155`).

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
    * *Positive:* `bg-emerald-100 text-emerald-800 border border-emerald-200` (e.g., `+12,5 % vs 2024`)
    * *Negative:* `bg-rose-100 text-rose-800 border border-rose-200` (e.g., `-4,2 % vs 2024`)
    * *Neutral (MANDATORY when |Δ| < 1 %):* `bg-slate-100 text-slate-600 border border-slate-200`,
      text `≈ stable vs <année N-1>` — never render a green `+0 %` (false signal)
      nor a red `-0,1 %` (noise). A near-zero variation is **information** ("flat"),
      not a success/failure.
    * **Badge wording uses the REAL year** (`vs 2024`, `vs {PREV_YEAR}`), never the
      jargon `vs N-1` — see §1.3.
  * **Accent Bar (optional):** `absolute left-0 top-0 bottom-0 w-1 bg-[var(--primary)]`

### 1.2. Multi-Metric Card (Multi-Row Card)
* **Usage:** Group multiple secondary metrics in one structured container.
* **CSS / Tailwind Rules:**
  * **Container:** `bg-[var(--surface)] border border-[var(--border)] rounded-lg p-4 shadow-sm flex flex-col divide-y divide-[var(--border)]`
  * **Row Item:** `py-2.5 first:pt-0 last:pb-0 flex items-center justify-between`
  * **Metric Label:** `text-xs font-medium text-[var(--text-secondary)]`
  * **Metric Value:** `text-sm font-semibold text-[var(--text-primary)] font-mono`

### 1.3. YoY ("vs N-1") Variation (MANDATORY on every time-derived KPI)

Every KPI whose value derives from the **time series** displays the **year-N
value** plus its variation **vs the prior year (N-1)**, on **all** pages /
sub-pages. The figure is **computed from `donnees.xlsx`, never invented**.

* **N = `CUR_YEAR`** (most recent year in `MONTH_META`), **N-1 = `CUR_YEAR - 1`**.
  The KPI value is the aggregate over **N's months**; the variation compares **N
  vs N-1 over comparable months only** — each month `m` of N against the **same
  month** of N-1. **Never** compare a partial N against a full N-1.
  ```javascript
  const _pct = (c,p) => p ? (c-p)/p*100 : null;      // % change, null when no base
  // aggregates(): curX = sum over N months ; prevX = sum over N-1 months present in N
  const yoy = { cKm,pKm, cRides,pRides, cMin,pMin, cActifs,pActifs };
  ```
* **Derived KPIs recompute their base** — e.g. *km/cycliste* compares
  `cKm/cActifs` vs `pKm/pActifs`, **not** the % of the already-rounded card values.
* **Render** a trend badge (§1.1) only when the value is finite. **Use the REAL
  prior-year number**, never the jargon `N-1`: format `±x,x % vs 2024` (French
  decimal comma, `PREV_YEAR` resolved). Up = green, down = red, **|Δ| < 1 % =
  neutral grey "≈ stable vs 2024"** (§1.1) — never a green `+0 %`. **Hide** the
  badge when YoY is not computable — never show a fabricated number.
  ```javascript
  const y = String(PREV_YEAR);
  const v = dynTrend(k.dyn, agg);                    // null when not computable
  if (v !== null) {
    if (Math.abs(v) < 1)      trend = '≈ stable vs ' + y;        // neutral (§1.1)
    else                       trend = `${v>=0?'+':'−'}${Math.abs(v).toLocaleString('fr-FR',{maximumFractionDigits:1})} % vs ${y}`;
  }
  ```
* **Static KPIs** (dimension counts with no time axis, e.g. *Pays couverts*,
  *Vélos en flotte*) carry **no** YoY badge — they are not time-derived.

### 1.4. KPI Value Semantics & Card Typography (BLOCKING)

* **One KPI = one meaningful number (or one short label).** A KPI card must never
  show a concatenation of raw counts like `36 / 9 / 5` for *"Cyclistes par pays"* —
  that is illegible and looks like a bug. Choose the single figure the label means:
  - a **count** (*Pays couverts* → `3`, *Villes couvertes* → `16`),
  - a **ratio / average** derived from the year-N aggregates (*Cyclistes par pays*
    → `actifs moyens / pays`, i.e. `actifs / NB_PAYS`, recomputed for year N and
    carrying its YoY badge),
  - or a **short named value** (*Marque dominante* → `Trek · Giant`).
* **Time-derived KPIs recompute from the year-N aggregates** (`agg.km`,
  `agg.rides`, `agg.actifs`, …) so the value reflects year N; **static dimension
  counts** are constants with no YoY badge (§1.3).
* **Card typography (match exactly):** label `11px / 600 / uppercase /
  var(--text-secondary)`; value `28px / 700 / var(--text-primary)`; a one-line
  **sub-label** `11px / var(--text-secondary)` under the value; the footer row
  holds **only the trend badge** (`min-height:22px` so cards align). Do not
  inflate the value to 30px+ or drop the sub-label.
* **Uniform card height (BLOCKING).** Every KPI card in a row is exactly the same
  height (`130px`), regardless of content: the footer stays one uniform line and
  no card grows taller than its neighbours.

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
* **Label = « Réinitialiser », never « Effacer » (BLOCKING).** A trash-can icon
  + "Effacer" reads as *destructive delete* (am I deleting data?). A reset
  action is **restorative** — use a **rotate / refresh arrow** icon
  (Feather `rotate-ccw`: `<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>`)
  and the label "Réinitialiser". The button **must also reset the date-range
  inputs** to their default window, not just the chiclets/dropdowns (a recurring
  bug: dates stay mutated while everything else resets, leaving the "Filtres
  actifs" badge logic inconsistent).
* **CSS / Tailwind Rules:**
  * `inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-[var(--text-secondary)] bg-[var(--surface)] border border-[var(--border)] rounded-md hover:bg-[var(--canvas)] hover:text-[var(--text-primary)] hover:border-[var(--primary)] transition-all cursor-pointer shadow-xs`
  * **Icon:** reset / refresh arrow (`w-3.5 h-3.5`), **not** a trash can.

### 2.7. Interactive filter pane (UI only — NOT data-bound)

The filter pane **looks and feels real** but is **not bound to the data**. Slicers
are fully interactive UI: clicking a year chiclet colors it, selecting a
quarter/month/dimension updates the displayed choice, dragging the date range
moves the handles, the **"● Filtres actifs"** badge appears as soon as any slicer
differs from its default, and **"Effacer"** resets the whole pane. **None of this
recomputes anything** — `aggregates()` and the visuals always show **year N**; a
filter change must never call `renderPage()` or alter a KPI/chart.

* **UI state, not data state.** Keep a `FILT` object for the *visual* state only
  (selected years, quarter, month, date window, one value per dimension). It
  drives the badge (`isFiltered()`) and the slicers' active classes — and nothing
  else. `aggregates()` (§6) ignores it entirely; the dashboard renders year N
  once (and on navigation), never on filter change.
* **Time slicers** — year chiclets (toggle multi-select, displayed in
  **chronological ascending order** `[N-1, N]`, never `[N, N-1]` which reads
  backwards), quarter & month (mutually exclusive — picking a quarter clears the
  month and vice-versa, so the two can never contradict each other like "T1" +
  "Août"), date range (two `JJ/MM/AAAA` inputs side by side in a flex row, kept
  in sync), clear button. **Quarter has ≤ 4 values → render it as chiclets too**
  (consistent with the ≤6 rule), not a dropdown.
* **The date-range inputs MUST feed the badge (BLOCKING).** A recurring bug: the
  period inputs have change-listeners but `isFiltered()` ignores them, so editing
  the dates never lights up "● Filtres actifs" while editing a chiclet does —
  inconsistent and confusing. Track `FILT.drFrom`/`FILT.drTo` and treat a value
  **differing from the default window** as an active filter (same as a selected
  chiclet). The reset button restores the default window.
* **Humanize every visible label (BLOCKING).** Raw dimension keys from the
  extractor are often machine-cased and unaccented (`Depasse`, `Saint_Bruno`,
  `2024-01`). Map them to a **human-readable label** before rendering in any
  chiclet, dropdown option, donut slice name, hbar category or legend entry:
  accent errors (`Depasse` → `Dépassé`), underscores → spaces, title-case names.
  Keep a single `LBL(key)` helper (or a `LABELS` map) applied at **every** call
  site that turns a key into user-facing text. A reviewer reading "Depasse" in a
  French dashboard reads it as a typo.
* **Dimension slicers (fill the pane to the footer).** Below the time slicers,
  add **one slicer per dimension** of the data model (extractor `META` dims, or
  the cyclisme `*_M` / count keys): chiclets if the dimension has ≤ ~6 values,
  otherwise a dropdown. This lengthens the pane to the bottom of the canvas
  without cramming — keep the standard gaps, never shrink the controls to fit.
* **Harmonized pane typography & heights (BLOCKING).** One type system for the
  whole pane: group labels `11px / 600 / uppercase / var(--text-secondary)`;
  every control (chiclet, dropdown, date input, clear button) at `12px`,
  height `32px`, `border-radius:8px`, `font-weight:500`. No stray smaller text.
  See POWERBI_LAYOUT.md §3.
* Default state = **no filter selected** (all chiclets inactive, dropdowns on
  "All/Toutes", full date window, badge hidden). The user toggles to see the UI
  react, but the data never moves.

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
* **Month x-axis:** when the category axis is the **month**, this is a temporal
  evolution chart — apply the §3.3 contract (fixed Jan→Dec `01`..`12` axis,
  year N vs N-1 as two clustered series, always full). `scale:true`
  stays **off** for bars (they must start at 0).

#### B. Horizontal Category Bar Charts (Single & Multi-Color)
* **ECharts Type:** `bar` with inverted axes (`yAxis: { type: 'category' }`, `xAxis: { type: 'value' }`)
* **Bar Styling:** `barHeight: 16`, `itemStyle: { borderRadius: [0, 4, 4, 0] }`
* **Individual Bar Coloring:** support array-based color assignment per category item (e.g., `#00A1B1`, `#2563EB`, `#5CB57D`, `#A7F3D0`, `#94A3B8`).
* **End-of-Bar Value Labels:** `label: { show: true, position: 'right', fontSize: 12, fontWeight: 'bold', color: '#0f172a', distance: 8 }`
* **Cardinality cap — top-10 + "Autres" (BLOCKING).** A horizontal bar chart of a
  dimension is unreadable past ~10 bars — the recurring *"Vélos par marque" = 25
  marques écrasées* regression. Cap it: render the **top 10** values plus a single
  **"Autres"** bar aggregating the rest — exactly the same pattern as the donut
  rule (§3.4). Always sort **descending**. (Contrast: *"Kilométrages par marque"*
  already looks good because it slices to ~12 — *"Vélos par marque"* must do the
  same.) Use a `topBars()` helper mirroring `topDonut`:
  ```javascript
  function topBars(dict, topN){
    const arr = Object.keys(dict).map(k=>({ name:k, value:dict[k] })).sort((a,b)=>b.value-a.value);
    const head = arr.slice(0, topN);
    const rest = arr.slice(topN).reduce((s,d)=>s+d.value, 0);
    if (rest>0) head.push({ name:'Autres', value:rest });
    return head;
  }
  ```
  Feed `topBars(MARQUE_VELOS, 10)` / `topBars(VILLE_CYCLISTES, 10)` — never the
  raw full-cardinality object. Color the **"Autres"** bar in a muted tone (e.g.
  `--border`/`--text-secondary`) so it reads as the residual, not as a peer.

---

### 3.3. Line & Area Charts — Temporal evolution (month axis)

A chart whose **x-axis is the month** is a *temporal evolution* visual. These
follow a dedicated contract: they **always show the full Jan→Dec N-vs-N-1
comparison** (the pane is decorative, §2.7, so nothing shrinks them). This
avoids the two recurring regressions: (a) the month axis showing the **full flat
list of every month** with `null` gaps, and (b) the curve crushed against the
bottom because the value axis is forced to `0`.

* **ECharts Type:** `line` (area = `line` + `areaStyle`).
* **Fixed Jan→Dec axis, 2-digit labels (BLOCKING).** The category axis is always
  the 12 calendar months labelled `01, 02, …, 12` — never the full flat list of
  every month in the data. Use `MONTH_AXIS`.
* **Always full N vs N-1 (BLOCKING).** Temporal charts are rebuilt from the
  **full** monthly arrays via `yearSeries()`/`yearRatio()` — there is no filter
  pipeline, so they never shrink.
* **Single-measure temporal → 2 series: N (solid) vs N-1 (dashed, lighter)
  (BLOCKING).** For a one-measure evolution (*Km par mois*, *Sorties par mois*,
  *Durée moyenne / sortie*…) render **two** lines on the Jan→Dec axis:
  * **Year N** (`CUR_YEAR` = latest year in `MONTH_META`) — resolved `--primary`,
    **solid**, `lineStyle.width: 2.5`, `symbolSize: 6` — the prominent curve the
    eye locks onto first.
  * **Year N-1** (`CUR_YEAR - 1`) — the **reference backdrop**: a **dashed**,
    **lighter** line in the neutral tone — `lineStyle:{ type:'dashed', width:1.5,
    color:C.neutral }`, `symbolSize: 4`, `itemStyle:{ color:C.neutral, opacity:0.7 }`.
    Dashed + thin so N-1 reads as context, not a peer of N.
  * A **legend** showing the two years (`legend.show: true`, `bottom: 0`).
* **Multi-series / stacked temporal (by dimension).** For an evolution split by a
  dimension (*top marques*, *empilé par pays*) keep **year N only** on the
  Jan→Dec axis — do **not** also split N-1 (8+ lines/stacks are unreadable). The
  dimension is the multi-series/stack (colors from `C.palette`, § palette); the
  axis is still fixed `01`..`12`.
* **Value axis `scale: true` on line/area (BLOCKING).** A line whose data lives
  far from 0 (e.g. *Durée moyenne / sortie* ≈ 120 min) must **zoom into its
  amplitude** — set `yAxis.scale = true` so ECharts does not force the axis to
  include 0. **Never** set `scale:true` on a bar/stacked value axis: bars must
  start at 0 for visual integrity.

Canonical helpers (declare once, reuse for every temporal chart):
```javascript
const CUR_YEAR  = Math.max(...MONTH_META.map(m=>m.year));
const PREV_YEAR = CUR_YEAR - 1;
const MONTH_AXIS = ['01','02','03','04','05','06','07','08','09','10','11','12'];
function yearSeries(arr, year){               // flat monthly array -> 12-point Jan..Dec
  const out = new Array(12).fill(null);
  for (let i=0;i<N_MONTHS;i++){ const m=MONTH_META[i]; if (m.year===year) out[m.month-1]=arr[i]; }
  return out;
}
function yearRatio(num, den, year){           // per-month ratio (e.g. minutes/rides)
  const out = new Array(12).fill(null);
  for (let i=0;i<N_MONTHS;i++){ const m=MONTH_META[i]; if (m.year===year && den[i]) out[m.month-1]=num[i]/den[i]; }
  return out;
}
```
Single-measure evolution option template (2 series, fixed axis, scale, legend):
```javascript
function evoLineOption(curData, prevData){
  const o = gridBase();
  o.xAxis.data = MONTH_AXIS;                  // 01..12 fixe, jamais la liste plate
  o.yAxis.scale = true;                       // ne pas ancrer à 0 (line/area seulement)
  o.legend = { show:true, bottom:0, itemGap:18, textStyle:{ color:C.textSub, fontSize:11 } };
  o.series = [
    { name:String(PREV_YEAR), type:'line', data:prevData, smooth:0.2, symbol:'circle', symbolSize:4,
      lineStyle:{ type:'dashed', width:1.5, color:C.neutral }, itemStyle:{ color:C.neutral, opacity:0.7 },
      connectNulls:true },
    { name:String(CUR_YEAR),  type:'line', data:curData,  smooth:0.2, symbol:'circle', symbolSize:6,
      lineStyle:{ width:2.5, color:C.primary }, itemStyle:{ color:C.primary, borderWidth:2, borderColor:'#fff' },
      connectNulls:true }
  ];
  return o;
}
```
(`C.neutral` = a resolved light grey derived from `--border`/`--text-secondary`
— defined once in the THEME block; the N-1 line is dashed + thinner than N.)
For a month-bar evolution use two clustered `bar` series on the same fixed axis,
**without** `scale:true` (bars must start at 0).

* **Line styling (general):** `smooth: 0.2`, markers `symbol:'circle'`,
  `itemStyle:{ borderWidth:2, borderColor:'#ffffff' }`. `connectNulls:true` so a
  partial current year (e.g. data stops in July) still draws a clean line.
  **Do NOT fill the area under the current-year line in a 2-series YoY chart** —
  an `areaStyle` that ends mid-axis renders as an abrupt grey rectangle that
  looks like a selection box or a rendering bug. The generated data covers 2
  complete closed years, so no partial-year cue is needed. A solid area fill is
  acceptable only on a **complete** single series, never on a partial current
  year.

---

### 3.4. Donut & Pie Charts
* **ECharts Type:** `pie`
* **Cardinality rule (BLOCKING — pick the chart by number of categories):** a
  donut/pie is only readable with **at most ~6 slices**. A dimension with more
  categories (e.g. **25 bike brands**, 16 cities) must **never** be rendered as a
  donut — use a **horizontal bar chart** (§3.2.B) instead. *"Vélos par marque"*
  (25 marques) is an **hbar**, not a donut. Feeding 9+ categories into a donut
  yields an unreadable rainbow ring + a legend that overflows the card — a
  recurring regression. When a *share-of-total* is wanted for a high-cardinality
  dimension, aggregate to **top-N (≤6) + "Autres"** before the donut.
* **Donut Sizing & anti-crop (BLOCKING):** `radius: ['48%', '66%']`,
  `center: ['35%', '50%']` (legend on the right; the centre overlay below anchors
  on the same `35%/50%`). **Do not** use `center:['30%','50%']` with the larger
  `['52%','72%']` radius — the leader-line `%` labels of left-side slices get
  pushed past the card's left edge and render clipped ("1,74 %" instead of
  "11,74 %"), a recurring regression. The `35%` center + slightly smaller ring
  leaves room for the left labels. Keep the centre overlay CSS in sync:
  `.donut-center{ left:35%; top:50%; transform:translate(-50%,-50%); }`.
* **Slice labels are ALWAYS on, French-formatted:** `label: { show: true,
  formatter: p => p.percent.toLocaleString('fr-FR', { maximumFractionDigits:1 })
  + ' %', fontSize: 10, color: <text-secondary>, distanceToLabelLine: 5 }`.
  Use the function form (not the string `'{d} %'`) so the decimal separator is a
  French comma (`10,5 %`) and the value is rounded to 1 decimal — the default
  `{d}` prints an Anglo dot and 2+ noisy decimals (`10.51 %`). Never render a
  donut with `label:{show:false}` — a bare ring with no % reads as broken.
* **Centre total is COMPUTED, never hardcoded.** The `dc-value` shown in the
  middle (e.g. the total km, total components) must be `fInt(values.reduce(+))`
  / `fKm(...)` derived from the same `items` array the slices use — never a
  magic string like `'200'` or `'50'`. A hardcoded centre drifts out of sync the
  day the data changes; compute it from the slice data.
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
* **Sub-page rows are CLICKABLE navigation, not decoration (BLOCKING).** Each
  sub-page row in the popover must navigate to that sub-page on click
  (`cursor:pointer`, hover background, calls the router `go(page, sub)`). A
  popover that merely *lists* the sub-pages without letting you reach them is a
  dead-end — the user opens it precisely to jump somewhere. The selected row is
  still shown but remains clickable (re-affirms the current page).
* **Keyboard reachable (BLOCKING).** Hover-only popovers are invisible to
  keyboard and touch users. Make the info `i` focusable (`tabindex="0"`) and
  show the popover on `:focus-within` in addition to `:hover`:
  ```css
  .info-ico{ /* ... */ tabindex via HTML attribute */ }
  .info-wrap:hover .popover,
  .info-wrap:focus-within .popover{ display:block; }
  ```
  Both triggers must work — never `:hover` alone.
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
  * `bg-[var(--card-bg)] border border-[var(--border)] rounded-lg p-4 shadow-xs flex flex-col justify-between h-full`
  * **Card Header:** `display:flex; align-items:baseline; justify-content:space-between; margin-bottom:8px; border-bottom:1px solid var(--border); padding-bottom:6px;` — the title sits on the **left**, the sub/unit on the **right** (`justify-content:space-between`), never inline next to the title.
  * **Card Title:** `font-size:13px; font-weight:600; color:var(--text-primary);` (sober — not 800).
  * **Subtitle / Unit:** `font-size:11px; color:var(--text-secondary);`
    right-aligned in the header.
  * **Subtitle wording uses the REAL years, never the jargon `N vs N-1`
    (BLOCKING).** A subtitle like *"km — N vs N-1"* repeated across three cards
    is insider shorthand; a reviewer reads *"km — 2025 vs 2024"* instantly.
    Resolve `CUR_YEAR`/`PREV_YEAR` into the subtitle string (`${CUR_YEAR} vs
    ${PREV_YEAR}`, `année ${CUR_YEAR}`). Same for KPI trend badges (§1.3) and
    the header subtitle period.

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

## 6. Data Architecture (MANDATORY)

Year-N visuals (§2.7) and N-vs-N-1 KPIs (§1.3) require the mockup to **embed the
data at month grain**. Do not hardcode final chart arrays only — embed the
underlying monthly series so year N and N-1 can be derived and compared.

* **Monthly fact series** (one value per month, chronologically ordered), one
  array per core measure — e.g. `KM[]`, `RIDES[]`, `MINUTES[]`.
* **`MONTH_META`** — `{year, month, quarter}` per index. Derive the two
  reference years once: `CUR_YEAR = max(year)`, `PREV_YEAR = CUR_YEAR - 1`.
* **Entity activity as a bitmask** — for "active entities" KPIs, one integer per
  entity where **bit `i` = active on month `i`**. `actifs` in year N = count of
  entities whose mask ∩ year-N-mask ≠ 0; `actifs` N-1 (comparable months) =
  mask ∩ (N-1 months present in N).
* **Per-dimension monthly series** for every dimension you chart
  (e.g. `KM_PAYS_M`, `KM_MARQUE_M`): `{dim: [per-month values]}`. Non-temporal
  visuals (donut/hbar/table) aggregate these over **year-N months**; temporal
  multi-series use `yearSeries(arr, CUR_YEAR)`.
* **Static dimension data** (counts with no time axis, e.g. `PAYS_CYCLISTES`,
  `MARQUE_VELOS`) stay as final `{name: value}` objects.
* **`aggregates()`** computes the **year-N** totals (KPI values) **and** the
  **N vs N-1** YoY block (comparable months, §1.3) — once, no filter state. Then
  `renderPage()` paints nav, KPI cards, visuals and the info popover from it.
  Temporal evolution charts (§3.3) read the full monthly arrays via
  `yearSeries()`/`yearRatio()`. Charts are disposed and re-initialised
  (`disposeCharts()` + `echarts.init`) inside `requestAnimationFrame`.
* **Chart registry — use this exact pattern.** Reassigning a `const` is a
  runtime `TypeError` that blanks the whole dashboard (the nav is painted, then
  `renderPage()` dies before the KPIs and visuals render):
  ```javascript
  let charts = {};
  function disposeCharts(){ for (const k of Object.keys(charts)) charts[k].dispose(); charts = {}; }
  ```
  Never write `const charts = {}` and later `charts = {}`. The registry must be
  declared with `let` (or mutated in place with `delete charts[k]`).
* **Chart init — use this exact pattern, with no guard beyond the element
  itself.** Every chart placeholder rendered in the HTML must receive an
  `echarts.init`. A guard that tests a property never set anywhere
  (`if (!el || !el.__chart) return;` — `el.__chart` is always `undefined`)
  returns **silently on every call**: no exception, no chart, empty cards in
  the browser while the smoke test's JS checks pass. The init must be
  unconditional once the element exists:
  ```javascript
  function renderCharts(list){
    requestAnimationFrame(() => {
      list.forEach(([id, opt]) => {
        const el = document.getElementById(id);
        if (!el) return;                       // seul guard autorisé
        charts[id] = echarts.init(el);         // jamais de condition sur une propriété maison
        charts[id].setOption(opt);
      });
    });
  }
  ```
  Likewise, do not gate init behind `window.echarts` checks that differ from
  the plain global `echarts` — the CDN script in `<head>` defines the global
  synchronously; a mismatched guard silently skips every chart.
* **DATA identifiers — declare once, reference exactly.** Every identifier a
  view references must be declared once in the DATA block, with the **exact
  same casing** (`CITY_CYCLISTES` ≠ `cityCyclistes` — a single typo throws
  `ReferenceError` and blanks that whole sub-page). Before delivering, run the
  smoke test (`scripts/smoke-test.js`, see SKILL.md Phase 3) which executes
  every view and catches these errors mechanically.
* **Separate static containers — never rewrite a parent's `innerHTML` by
  string concatenation.** Nav, KPI row and visuals live in **dedicated static
  containers** (`#navL1`, `#navL2`, `#kpis`, `#visuals`, see POWERBI_LAYOUT.md
  §4), each rewritten independently. Never build the navigation by prepending
  into a shared container (`c.innerHTML = navHtml + c.innerHTML`): re-parsing
  the serialized HTML destroys the live chart DOM nodes and their listeners on
  every render, and any error in one zone wipes the others.

> A mockup that only embeds final per-sub-page arrays **cannot** compute YoY —
> that is the regression this section exists to prevent.

### 6.1. Extraction des données (`scripts/extract-data.py`) — auto-détection

Do **not** hand-derive the data model from `donnees.xlsx` ad hoc — that is how
KPIs end up mis-interpreted and dimensions get dropped. Run the extractor and
embed **all** of its output:

```bash
python .opencode/skills/powerbi-prototype/scripts/extract-data.py clients/<client>/donnees.xlsx
```

The extractor is **generic (any domain)**. It auto-detects the model of any
star/snowflake Excel — no sheet/column name is hardcoded:
- **fact table** = the sheet with a date column **and** the most rows **and** ≥1
  numeric measure (so a date in a dimension like `Date_Installation` is *not*
  mistaken for the fact);
- **date column**, **measures** (numeric, non-ID), **dimensions** (categorical
  columns, reached directly or through join chains — bridge/junction tables
  supported), **standalone categorical aggregates** (sheets not joined to the
  fact, e.g. a `Statut` column), **activity masks** (the "person-like" entity
  dimension), and **scalars**. It prints a recap + a **proposed manifest** on
  stderr.

It emits `const DATA = {…}` with a **normalized contract**:
- `N`, `MONTH_META` — month grain.
- `FACTS[mesure][mois]` — every measure of the fact table, plus `FACTS._count`
  (row count per month).
- `BY_DIM[dim][valeur][mesure][mois]` — per-dimension series (aggregate over year-N
  months for donuts/hbars/tables, or `yearSeries` for temporal multi-series)
  (drives bars/lines/stacked and per-dim YoY).
- `DIM_COUNTS[dim][valeur]` — static counts from the dimension table (drives
  "X par <dim>" KPIs and the **hbar** of high-cardinality dims, top-10 + « Autres »
  via `topBars`, see §3.2.B; the donut-vs-hbar choice is §3.4).
- `CATEGORY_COUNTS[source][colonne][valeur]` — non-time categorical aggregates
  (e.g. component wear `Statut`), for donuts.
- `ACTIVE_MASKS[entité]` — bitmask per entity (bit `i` = active month `i`);
  empty unless an activity entity is found/declared.
- `SCALARS` — `NB_<feuille>`, `NB_<dim>`, `AVG_<col>` …
- `META` — provenance (fact sheet, date col, measures, dims, activity entity) so
  the mockup maps `CLIENT.md` KPIs/visuals to the right series.

**Manifest override (`data-manifest.json`).** If auto-detection picks wrong (or
you want to curate labels / force the activity entity), drop the proposed
manifest into `clients/<client>/data-manifest.json` (JSON) — it is then used
verbatim. Only the fact table (a dated sheet) is mandatory.

**Legacy cyclisme profile.** Existing cyclisme clients (Veloh, agiledss) use the
historical **data contract** (`KM`, `RIDES`, `USURE_STATUT`, `USER_MASKS`,
`KM_PAYS_M`, `KM_MARQUE_M`, …) — a data extraction format, never an HTML layout
reference. Emit it with:
```bash
python .opencode/skills/powerbi-prototype/scripts/extract-data.py clients/<client>/donnees.xlsx --profile cyclisme
```

If the extractor is missing a series a sub-page needs, **extend the extractor**
(don't hand-patch the HTML) so the next client benefits too.
