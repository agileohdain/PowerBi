---
name: powerbi-prototype
description: Génère des maquettes de dashboards Power BI haute-fidélité (canevas 16:9, fond PowerPoint exporté en image, cartes KPI, slicers, visuels ECharts, navigation dynamique deux-niveaux) en HTML/Tailwind/ECharts auto-suffisant. L'utilisateur prépare TOUT en amont (CLIENT.md + fond bg) — le skill ne pose aucune question et génère en une passe pour économiser les tokens. Use when the user wants to generate a Power BI dashboard mockup for a client already set up in clients/<client>/ — e.g. "maquette power bi", "crée la maquette pour <client>".
triggers:
  - maquette power bi
  - maquette powerbi
  - crée la maquette
  - génère la maquette
---

## Ce que je fais
Je produis des maquettes de dashboards Power BI en HTML auto-suffisant, fidèles au
langage visuel Power BI (canevas 16:9 fixe, fond visuel importé, cartes KPI,
slicers, graphiques ECharts, navigation à deux niveaux).

**Principe : aucune question.** Toute l'information provient de fichiers préparés
en amont par l'utilisateur dans `clients/<client>/`. Je lis, je génère, je finis.

## Pré-requis (préparés par l'utilisateur — voir README.md)
Avant de me lancer, le dossier `clients/<client>/` doit contenir :
- **`CLIENT.md`** — fichier pilote (obligatoire) : identité, couleurs, titre,
  arbre de navigation (pages / sous-pages / KPIs, flags `[En consolidation]`).
- **Fond `bg.*`** — fond visuel exporté depuis `powerpoint/Maquette Power BI.pptx`.
  Format **`bg.svg`** (préféré, vectoriel) ou **`bg.png`** (fallback). Contient le
  bandeau, la zone logo, le fond canevas et le pane filtres.
- **`logo.png`** — logo du client (déjà intégré au `.pptx`/fond par
  l'utilisateur ; ce fichier est optionnel pour le rendu HTML si le logo est
  dans l'image de fond).

Si le fond (`bg.svg` **ou** `bg.png`) est absent → appeler
`powerpoint/export-bg.ps1 -Path clients/<client>/fond.pptx -Output
clients/<client>/bg.png` (produit un PNG 2× ; ou `-Template` pour générer depuis
le master avec les couleurs de `CLIENT.md`). Si `CLIENT.md` est
absent → **stop** et demander à l'utilisateur de le créer depuis
`clients/_template/`.

## Sources de données
- `CLIENT.md` — **fichier pilote** (édité par l'utilisateur) : identité de marque
  (couleurs via `--primary`/`--surface`/`--canvas`/`--border`/`--card-bg`), titre,
  et l'arbre de navigation (pages / sous-pages / KPIs, avec flags
  `[En consolidation]`).
- `DATA.md` — modèle de données + glossaire KPI (formules) + carte visuelle par
  page (quel chart, nourri par quelles colonnes). À lire **avec** `CLIENT.md`.
  S'il n'existe pas encore, le générer (voir Phase 1).
- Exemple complet de référence : `clients/veloh/`.

## Références visuelles et techniques
- `references/POWERBI_LAYOUT.md` — grille canevas, zones (le bandeau = fond
  `bg.*`, ne PAS le redessiner en CSS), filtre pane, navigation deux-niveaux,
  footer, et le **contrat complet des variables couleur**.
- `references/POWERBI_COMPONENTS.md` — catalogue complet des composants
  (cartes KPI dont l'état "en consolidation", slicers, règles ECharts, tables,
  navigation, note info, footer), tous pilotés par les variables de `CLIENT.md`.

---

# Workflow (une seule passe, sans questions)

## Phase 0 — Vérifier les entrées
1. Localiser `clients/<client>/` (le `<client>` est donné dans la demande, ou
   inféré du dossier le plus récent).
2. Vérifier `CLIENT.md` présent. Si non → stop, demander de créer depuis
   `clients/_template/`.
3. Vérifier le fond présent (`bg.svg` **ou** `bg.png`). Si aucun des deux :
   - si `fond.pptx` existe → `export-bg.ps1 -Path .../fond.pptx -Output .../bg.png`
   - sinon → `export-bg.ps1 -Template -Output .../bg.png -Primary <p> -Surface <s> -Canvas <c>`
     (couleurs lues dans `CLIENT.md`)
4. Lire `CLIENT.md` (+ `DATA.md` si présent).

## Phase 1 — Données (si `donnees.xlsx` / `DATA.md` absents)
Si `DATA.md` et `donnees.xlsx` n'existent pas :
1. Déduire de `CLIENT.md` un modèle en flocon (1 table de faits + 2-3 dimensions).
2. Générer `donnees.xlsx` fictif réaliste (volumes 100-5000 lignes, période
   cohérente avec le titre/sous-titre).
3. Rédiger `DATA.md` (utiliser `templates/DATA.template.md`) : modèle de données,
   glossaire KPI (définition + formule + valeur de référence), carte visuelle par
   page (type de chart · titre · colonnes source).
**Aucune question de suivi** — faire des choix cohérents et poursuivre.

## Phase 2 — Génération de la maquette HTML
1. Lire `CLIENT.md` + `DATA.md` (+ `references/POWERBI_LAYOUT.md` et
   `POWERBI_COMPONENTS.md`).
2. Produire `clients/<client>/maquette/index.html` — fichier **auto-suffisant** :
   - Tailwind via CDN, Apache ECharts via CDN.
   - Canevas 1920×1080 fixe, scaling CSS pour s'adapter au viewport (pas de scroll).
   - **Fond = `bg.*`** (le `bg.svg`/`bg.png` fourni) appliqué sur le canevas
     (`background: url(./bg.svg) center/cover no-repeat` — adapter l'extension).
     **Ne pas redessiner le bandeau ni la zone logo en CSS** — ils sont dans l'image.
   - Variables CSS en `:root` lues depuis `CLIENT.md` :
     `--primary`, `--surface`, `--canvas`, `--border`, `--card-bg`,
     `--text-primary`, `--text-secondary`.
    - **Titre + sous-titre** positionnés par-dessus le bandeau du fond
      (zone haute, ~0-97px), en `var(--surface)`.
    - Pane filtres à gauche avec **"Filtres" + icône en `var(--primary)`**.
      (L'arrière-plan du pane vient du fond `bg.*` ; ne poser qu'un fond
      transparent/surface léger si nécessaire pour la lisibilité des slicers.)
   - Navigation L1 (pills) + L2 (liens texte) rendue depuis `CLIENT.md`.
   - Cartes KPI (avec état consolidation si flag présent) + visuels ECharts depuis
     la carte visuelle de `DATA.md`.
   - Footer disclaimer "Données fictives".
3. Copier le fond `bg.*` (+ `logo.png` si présent) à côté de `index.html` dans
   `maquette/` (la maquette doit être auto-portable).
4. Indiquer à l'utilisateur comment ouvrir le rendu (`start index.html`).

## Règles de qualité
- **Ne jamais coder une couleur en dur** : toujours via `var(--xxx)`.
- **Ne pas redessiner le bandeau / la zone logo / le fond en CSS** : ils sont
  dans le fond `bg.*`. Le skill ne pose que le titre, les slicers, les KPIs, les charts.
- Le **titre/sous-titre** sur le bandeau est TOUJOURS en `var(--surface)`
  (lisible quel que soit le thème).
- Le texte de pane "Filtres" + son icône est TOUJOURS en `var(--primary)`.
- Responsive : le canevas 1920×1080 est scaled pour s'adapter au viewport sans
  scrollbars, via `transform: scale(...)` calculé par un petit script.
- Une seule page de mockup pleinement validée par exécution ; les autres
  sous-pages sont des defaults cohérents.
