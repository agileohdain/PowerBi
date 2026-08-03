---
name: powerbi-prototype
description: Génère des maquettes de dashboards Power BI haute-fidélité (canevas 16:9, bandeau/fond dessinés en CSS, cartes KPI, slicers, visuels ECharts, navigation dynamique deux-niveaux) en HTML/Tailwind/ECharts auto-suffisant. Au lancement, le skill demande si l'utilisateur veut être TÉLÉGUIDÉ (le skill pose les questions une à une — nom du client puis identité/couleurs/titre/arbre de navigation/KPIs — crée clients/<client>/ dès que le nom est connu et écrit CLIENT.md au fil du questionnement) ou PERSONNALISER LUI-MÊME (il prépare clients/<client>/ en amont, le skill génère en une passe). Use when the user wants to create a Power BI dashboard mockup for a client — e.g. "maquette power bi", "crée la maquette", "nouvelle maquette client".
triggers:
  - maquette power bi
  - maquette powerbi
  - crée la maquette
  - génère la maquette
  - nouvelle maquette
---

## Ce que je fais
Je produis des maquettes de dashboards Power BI en HTML auto-suffisant, fidèles au
langage visuel Power BI (canevas 16:9 fixe, bandeau et fond dessinés en CSS,
cartes KPI, slicers, graphiques ECharts, navigation à deux niveaux).

**Deux modes de démarrage** (demandé au lancement) :
- **Téléguidé** — je pose les questions une à une (nom du client, puis couleurs,
  titre, arbre de navigation, KPIs). Dès que le nom est connu, je crée le dossier
  `clients/<client>/` avec ses fichiers de base, puis j'écris `CLIENT.md` au fil
  du questionnement et je génère.
- **Personnaliser** — l'utilisateur prépare tout en amont dans `clients/<client>/`
  (voir README.md), je lis, je génère, je finis sans question de fond.

## Phase 0 — Questions d'ouverture (TOUJOURS, via l'outil `question`)

Poser ces deux questions **avant toute autre action** :

1. **Mode de démarrage** :
   > Souhaitez-vous être **téléguidé** par moi (je vous pose les questions et je
   > prépare tout), ou préférez-vous **personnaliser vous-même** (vous suivez les
   > étapes 1 à 3 du README et je génère ensuite) ?
2. **Données** :
   > Avez-vous **déjà les données** (`donnees.xlsx`), ou souhaitez-vous
   > que je les **crée pour vous** (jeu fictif réaliste) ?

Ensuite :
- Si **Personnaliser** → aller directement en Phase 2 (vérifier les entrées
  préparées par l'utilisateur).
- Si **Téléguidé** → continuer en Phase 1 (questionnement guidé).

## Phase 1 — Questionnement téléguidé (uniquement en mode Téléguidé)

Poser les questions **une par une** (outil `question` quand il y a des choix à
proposer, sinon question libre en français). Ordre obligatoire :

1. **Nom du client** → sert à nommer le dossier `clients/<client>/`
   (slug minuscule, espaces → tirets).
2. **Créer immédiatement le dossier `clients/<client>/`** avec ses fichiers de
   base (le dossier existe donc **dès que le nom est connu**, avant le reste du
   questionnement) :
   - `CLIENT.md` (copie de `templates/CLIENT.template.md`, nom client pré-rempli,
     le reste à remplir aux étapes suivantes),
   - `logo.png` (placeholder + rappel de déposer le vrai logo du client).
3. **Thème de couleurs** — proposer des préréglages (et remplir `CLIENT.md`) :
   - **Défaut** : Primary `#00A1B1`, Surface `#FFFFFF`, Canvas `#F1F5F9`,
     Card Frame `#FFFFFF`, Border `#CBD5E1`.
   - **Blanc** : Primary `#0F172A`, Surface `#FFFFFF`, Canvas `#FFFFFF`,
     Card Frame `#FFFFFF`, Border `#E2E8F0`.
   - **Noir** : Primary `#00A1B1`, Surface `#1E293B`, Canvas `#0F172A`,
     Card Frame `#1E293B`, Border `#334155`.
   - **Personnalisé** : demander **chaque variable** une par une, avec la valeur
     par défaut pré-remplie (proposition) : Primary / Banner Accent, Surface /
     Cards, Canvas Background, Card Frame Color, Border / Divider.
   - Quel que soit le choix, **dériver automatiquement**
     `--text-primary` / `--text-secondary` selon la luminance du Canvas
     (clair → `#0F172A`/`#64748B` ; sombre → `#F1F5F9`/`#94A3B8`).
4. **Titre du rapport** puis **sous-titre / période** (à reporter dans `CLIENT.md`).
5. **Arbre de navigation** — boucle par page, en commençant par la page 1 (à
   reporter dans `CLIENT.md`) :
   - Nom de la page.
   - Nombre de sous-pages, puis pour chaque sous-page : son nom.
   - Pour chaque sous-page : nombre de KPI, puis le nom de chaque KPI.
   - Pour chaque KPI : **« à mettre en consolidation ? »** (oui → flag
     `[En consolidation]`).
   - À la fin de la page : **« page suivante ou c'est terminé ? »** → boucler ou
     sortir.
6. **Finaliser `clients/<client>/CLIENT.md`** : le template copié en étape 2 est
   rempli de façon incrémentale (couleurs, titre, arbre) au fil des étapes 3-5 ;
   vérifier qu'il est complet avant de passer à la Phase 2.

## Phase 2 — Logo, fond et entrées

1. **Mode Téléguidé** : `clients/<client>/` (et son `CLIENT.md`) existent déjà —
   ils ont été créés en Phase 1 étape 2. **Mode Personnaliser** : vérifier que
   `clients/<client>/` et `CLIENT.md` existent (sinon → stop, renvoyer au README
   étapes 1-2).
2. **Logo (obligatoire)** : vérifier `clients/<client>/logo.png`. Si absent →
   **stop et demander impérativement** à l'utilisateur de déposer le logo du
   client (idéalement **fond transparent**, PNG) dans `clients/<client>/` avant
   de continuer.
3. **Fond `bg.*` (optionnel)** : si `bg.svg` **ou** `bg.png` est présent, il sera
   utilisé comme image de fond (prioritaire sur le rendu CSS). Sinon, le bandeau,
   la zone logo, le fond canevas et le pane filtres sont **dessinés en CSS** —
   ce n'est **pas bloquant**.
4. Lire `CLIENT.md`.

## Phase 3 — Données (selon la réponse « Données » de la Phase 0)

- Si l'utilisateur **a les données** : vérifier `donnees.xlsx` dans
  `clients/<client>/`. Lire le `.xlsx` et déduire modèle de données
  (tables/feuilles), formules KPI, colonnes source et carte visuelle par page.
  Si absent → **stop** et demander de déposer `donnees.xlsx`, ou proposer de
  les créer.
- Si l'utilisateur veut que je **crée les données** (ou si `donnees.xlsx` est
  absent) :
  1. Déduire de `CLIENT.md` un modèle en flocon (1 table de faits + 2-3 dimensions).
  2. Générer `donnees.xlsx` fictif réaliste (volumes 100-5000 lignes, période
     cohérente avec le titre/sous-titre) : feuilles = tables, valeurs réalistes.
  3. Déduire du fichier généré le modèle de données, le glossaire KPI
     (définition + formule + valeur de référence) et la carte visuelle par page
     (type de chart · titre · colonnes source).
  Faire des choix cohérents et poursuivre — pas de question de suivi ici.

## Phase 4 — Génération de la maquette HTML

1. Lire `CLIENT.md` (+ `references/POWERBI_LAYOUT.md` et
   `POWERBI_COMPONENTS.md`), et les données dans `donnees.xlsx` (model/filtres).
2. Produire `clients/<client>/maquette/index.html` — fichier **auto-suffisant** :
   - Tailwind via CDN, Apache ECharts via CDN.
   - Canevas 1920×1080 fixe, scaling CSS pour s'adapter au viewport (pas de scroll).
   - **Fond** :
     - Si `bg.svg`/`bg.png` présent → `background: url(./bg.svg) center/cover
       no-repeat` (adapter l'extension) ; **ne pas redessiner** le bandeau ni la
       zone logo en CSS (ils sont dans l'image).
     - Sinon → **dessiner en CSS** : bandeau haut (~97px) en `var(--primary)`
       avec zone logo (~245px) en `var(--surface)` contenant `logo.png`, fond
       canevas en `var(--canvas)`, pane filtres à gauche (fond `var(--canvas)`).
   - Variables CSS en `:root` lues depuis `CLIENT.md` :
     `--primary`, `--surface`, `--canvas`, `--border`, `--card-bg`,
     `--text-primary`, `--text-secondary`.
   - **Titre + sous-titre** positionnés par-dessus le bandeau (zone haute,
     ~0-97px), en `var(--surface)`.
   - Pane filtres à gauche avec **"Filtres" + icône en `var(--primary)`**.
   - Navigation L1 (pills) + L2 (liens texte) rendue depuis `CLIENT.md`.
   - Cartes KPI (avec état consolidation si flag présent) + visuels ECharts
     depuis la carte visuelle déduite de `donnees.xlsx`.
   - Logo `logo.png` affiché dans la zone logo (en haut à gauche).
   - Footer disclaimer "Données fictives".
3. Copier `logo.png` (+ `bg.*` si présent) à côté de `index.html` dans
   `maquette/` (la maquette doit être auto-portable).
4. Indiquer à l'utilisateur comment ouvrir le rendu (`start index.html`).

## Sources de données
- `CLIENT.md` — **fichier pilote** (écrit par le skill en mode Téléguidé, ou par
  l'utilisateur en mode Personnaliser) : identité de marque (couleurs via
  `--primary`/`--surface`/`--canvas`/`--border`/`--card-bg`), titre, arbre de
  navigation (pages / sous-pages / KPIs, flags `[En consolidation]`).
- `donnees.xlsx` — **données source** (déposées par l'utilisateur ou générées par
  le skill en Phase 3). Le skill en déduit le modèle de données, le glossaire KPI
  (formules) et la carte visuelle par page ; le skill s'appuie sur l'Excel seul,
  sans fichier de glossaire séparé.
- Exemple complet de référence : `clients/veloh/`.

## Règles de qualité
- **Ne jamais coder une couleur en dur** : toujours via `var(--xxx)`.
- Le **titre/sous-titre** sur le bandeau est TOUJOURS en `var(--surface)`.
- Le texte de pane "Filtres" + son icône est TOUJOURS en `var(--primary)`.
- Dériver `--text-primary`/`--text-secondary` selon la luminance de `--canvas`.
- Responsive : le canevas 1920×1080 est scaled pour s'adapter au viewport sans
  scrollbars, via `transform: scale(...)` calculé par un petit script.
- Une seule page de mockup pleinement validée par exécution ; les autres
  sous-pages sont des defaults cohérents.
