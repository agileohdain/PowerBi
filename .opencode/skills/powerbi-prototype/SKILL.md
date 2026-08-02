---
name: powerbi-prototype
description: Génère des maquettes de dashboards Power BI haute-fidélité (canevas 16:9, en-tête diagonal trois-zones, cartes KPI, slicers, visuels ECharts, navigation dynamique deux-niveaux) en HTML/Tailwind/ECharts auto-suffisant. Re-skin complet par client via les variables CSS du fichier brands/<client>/CLIENT.md. Use when the user wants to prototype, mock up, or replicate a Power BI dashboard for a client — e.g. "maquette Power BI", "dashboard démo", "rapport analytique", "prototype pré-vente".
triggers:
  - maquette power bi
  - maquette powerbi
  - dashboard power bi
  - dashboard démo
  - rapport analytique
  - prototype pré-vente
  - mockup client
---

## Ce que je fais
Je produis des maquettes de dashboards Power BI en HTML auto-suffisant, fidèles au
langage visuel Power BI (canevas 16:9 fixe, en-tête diagonal trois-zones, cartes KPI,
slicers, graphiques ECharts, navigation dynamique à deux niveaux). Tout le dashboard
se re-skinne par client via les variables CSS du fichier `brands/<client>/CLIENT.md`.

## Quand me déclencher
Quand l'utilisateur veut prototyper / reproduire un dashboard Power BI pour un client
(pré-vente, démo, maquette) : "rapport analytique", "maquette power bi", "dashboard
démo client", etc.

## Sources de données (lues depuis `brands/<client>/`)
- `CLIENT.md` — **fichier pilote** (édité par l'utilisateur) : identité de marque
  (couleurs via `--primary`/`--surface`/`--canvas`/`--border`/`--card-bg`/`--bg-image`,
  logo, image de fond optionnelle) + l'arbre de navigation dynamique
  (pages / sous-pages / KPIs, avec flags `[En consolidation]`).
- `DATA.md` — modèle de données + glossaire KPI (formules) + carte visuelle par page
  (quel chart, nourri par quelles colonnes). À lire **avec** `CLIENT.md` pour ne jamais
  avoir à ré-ouvrir ou ré-inférer le `.xlsx`.
- Exemple complet de référence : `brands/veloh/` (CLIENT.md + DATA.md + donnees.xlsx
  + logo + Output/).

## Références visuelles et techniques
- `references/POWERBI_LAYOUT.md` — grille canevas, en-tête trois-zones diagonal
  (zone logo → ligne accent → bannière primaire), filtre pane, navigation deux-niveaux,
  architecture des lignes, footer, et le **contrat complet des variables couleur**.
- `references/POWERBI_COMPONENTS.md` — catalogue complet des composants
  (cartes KPI dont l'état "en consolidation", slicers, règles ECharts, tables,
  navigation, note info, footer), tous pilotés par les variables de `CLIENT.md`.
- `references/images/mockup-{1-overview,2-volume,3-quality}.svg` — mockups de
  référence (SVG = XML lisible, couleurs et positions extraites directement).
- Palette de référence (client clair, tirée des mockups) : primaire teal `#00A1B1`,
  secondaire vert `#5CB57D`, teal profond `#004250`, rouge consolidation `#FF0000`,
  gris neutre `#7F7F7F`. **Ne pas coder ces couleurs en dur** — pour un client donné
  elles sont remplacées par les variables de `CLIENT.md`.

---

# Workflow en 3 phases

## Phase 1 — Brief guidé (obligatoire avant toute génération)
Si `brands/<client>/CLIENT.md` n'existe pas encore, poser ces questions à
l'utilisateur (regroupées, pas une à une) et créer le dossier + le `CLIENT.md` :

1. **Nom du client / entreprise** + secteur d'activité
2. **Couleur primaire** (header, accents, "Filtres", onglets actifs) — hex accepté
3. **Couleur de fond** du canevas (`--canvas`)
4. **Couleur des encadrés / cards** (`--card-bg`, défaut = même que surface)
5. **Couleur surface** (logo zone, texte sur primaire)
6. **Couleur bordures** (`--border`)
7. **Image de fond** optionnelle (`--bg-image` : chemin `./bg.png` ou `none`)
8. **Logo** (fichier `./logo.png` à fournir, sinon placeholder)
9. **Titre du rapport** + sous-titre / période
10. **Arbre de navigation** : pages → sous-pages → KPIs (libellés), et quels KPIs
    sont `[En consolidation]`
11. Style visuel (clair / sombre / corporate / moderne)

→ Une fois répondu, créer `brands/<client-slug>/CLIENT.md` (utiliser
`templates/CLIENT.template.md` comme base) + `logo.png`.

## Phase 2 — Données fictives (si pas déjà présentes)
Si `brands/<client>/DATA.md` et `donnees.xlsx` n'existent pas :
1. Déduire du brief un modèle en flocon (1 table de faits + 2-3 dimensions).
2. Générer un fichier `donnees.xlsx` fictif réaliste (volumes 100-5000 lignes,
   période cohérente avec le brief).
3. Rédiger `DATA.md` (utiliser `templates/DATA.template.md`) : modèle de données,
   glossaire KPI (définition + formule + valeur de référence), carte visuelle par
   page (type de chart · titre · colonnes source).
4. Poser 2-3 questions d'affinage (granularité temporelle, KPIs manquants, etc.).

## Phase 3 — Génération de la maquette HTML
1. Lire `CLIENT.md` + `DATA.md` du client.
2. Lire `references/POWERBI_LAYOUT.md` + `references/POWERBI_COMPONENTS.md`.
3. Produire `mockups/<client-slug>/index.html` — fichier **auto-suffisant** :
   - Tailwind via CDN, Apache ECharts via CDN.
   - Canevas 1920×1080 fixe, scaling CSS pour s'adapter au viewport (pas de scroll).
   - Variables CSS en `:root` lues depuis `CLIENT.md` :
     `--primary`, `--surface`, `--canvas`, `--border`, `--card-bg`, `--bg-image`,
     `--text-primary`, `--text-secondary`.
   - En-tête 3-zones (logo zone + accent line + bannière primaire diagonale).
   - Pane filtres à gauche avec **"Filtres" + icône en `var(--primary)`**.
   - Navigation L1 (pills) + L2 (liens texte) rendue depuis `CLIENT.md`.
   - Cartes KPI (avec état consolidation si flag présent) + visuels ECharts depuis
     la carte visuelle de `DATA.md`.
   - Footer disclaimer "Données fictives".
4. Copier `logo.png` (+ `bg.png` si image de fond) à côté de `index.html`.
5. Indiquer à l'utilisateur comment ouvrir le rendu (`start index.html`).

## Règles de qualité
- **Ne jamais coder une couleur en dur** : toujours via `var(--xxx)`.
- Le texte sur bannière primaire est TOUJOURS `var(--surface)` (lisible quel que
  soit le thème) — jamais `var(--primary)` sur `var(--primary)`.
- Le texte de pane "Filtres" + son icône est TOUJOURS en `var(--primary)`.
- Une seule page de mockup pleinement validée par exécution (cf. veloH 1.1) ;
  les autres sous-pages sont des defaults cohérents.
- Responsive : le canevas 1920×1080 est scaled pour s'adapter au viewport sans
  scrollbars, via `transform: scale(...)` calculé par un petit script.
- Si le client fournit une image de fond (`--bg-image`), l'appliquer sur le canevas
  avec un overlay discret pour préserver la lisibilité.
