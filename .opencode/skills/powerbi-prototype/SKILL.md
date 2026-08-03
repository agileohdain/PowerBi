---
name: powerbi-prototype
description: Génère des maquettes de dashboards Power BI haute-fidélité (canevas 16:9, bandeau/fond dessinés en CSS, cartes KPI, slicers, visuels ECharts, navigation dynamique deux-niveaux) en HTML/Tailwind/ECharts auto-suffisant. Dès que l'utilisateur lance "AgileDSS", le skill demande "Quel est le nouveau client ?" (respect strict des majuscules/minuscules, sans proposer de nom — l'utilisateur saisit lui-même), demande de passer en mode BUILD si nécessaire, crée automatiquement clients/<client>/ avec CLIENT.md, demande de repasser en mode PLAN, demande de déposer les données (donnees.xlsx) et le logo (logo.png) — jamais générés par le skill — puis demande si l'utilisateur veut être TÉLÉGUIDÉ (le skill pose les questions une à une — couleurs/titre/arbre de navigation/KPIs — et écrit CLIENT.md au fil du questionnement) ou PERSONNALISER (l'utilisateur édite lui-même CLIENT.md, le skill génère en une passe). Use when the user wants to create a Power BI dashboard mockup for a client — e.g. "AgileDSS", "maquette power bi", "nouvelle maquette client".
triggers:
  - AgileDSS
  - agiledss
  - maquette power bi
  - maquette powerbi
  - génère la maquette
  - nouvelle maquette
---

## Ce que je fais
Je produis des maquettes de dashboards Power BI en HTML auto-suffisant, fidèles au
langage visuel Power BI (canevas 16:9 fixe, bandeau et fond dessinés en CSS,
cartes KPI, slicers, graphiques ECharts, navigation à deux niveaux).

**Flux de démarrage** (déclenché par « AgileDSS ») :
1. Je demande **« Quel est le nouveau client ? »** — formulation soignée et
   attractive, en précisant que la **casse est respectée telle quelle**
   (majuscules/minuscules). **Je ne propose pas de nom** : l'utilisateur
   saisit lui-même le client.
2. Si l'utilisateur est en mode **PLAN**, je lui demande de se mettre en
   mode **BUILD** (une fois, sans boucler plusieurs fois).
3. Je **crée automatiquement le dossier** `clients/<client>/` (casse exacte)
   avec ses fichiers de base : `CLIENT.md` (copie du template, nom pré-rempli)
   et un placeholder `logo.png`.
4. Une fois le dossier créé, je demande à l'utilisateur de **repasser en mode
   PLAN** (et pas en BUILD).
5. Je **demande de déposer le logo du client et les données Excel** avec le
   bon nom (`donnees.xlsx` et `logo.png`), puis je m'arrête pour attendre. Je
   **ne génère jamais** les données.
6. Une fois le dépôt confirmé, je demande le **mode** :
   - **Téléguidé** — je pose les questions une à une (couleurs, titre, arbre de
     navigation, KPIs) et j'écris `CLIENT.md` au fil du questionnement.
   - **Personnaliser** — l'utilisateur édite lui-même `CLIENT.md` (voir README.md),
     je lis, je génère, je finis sans question de fond.

## Phase 0 — Nouveau client + création du dossier

1. **Demander : « Quel est le nouveau client ? »** — question libre en français,
   formulée de façon claire et accueillante. Précisez que **la casse est
   respectée telle quelle** (majuscules/minuscules) : le nom servira tel quel,
   avec la casse exacte, à nommer le dossier (ex. `Diallo` → `clients/Diallo/`).
   **Ne proposer aucun nom** — l'utilisateur saisit lui-même le nouveau client.
   Ne pas transformer en slug minuscule.
2. **Vérifier le mode** : si l'utilisateur est en mode **PLAN**, lui demander de
   se mettre en mode **BUILD** (nécessaire pour écrire le dossier). **Demander
   une seule fois, sans boucler plusieurs fois.**
3. **Créer immédiatement le dossier `clients/<client>/`** (dès que le nom est
   connu) avec ses fichiers de base :
   - `CLIENT.md` (copie de `templates/CLIENT.template.md`, nom client pré-rempli,
     le reste à remplir aux étapes suivantes),
   - `logo.png` (placeholder + rappel de déposer le vrai logo du client).
4. **Demander de repasser en mode PLAN** (et pas en BUILD).
5. **Demander le dépôt du logo du client et des données Excel**, avec le bon
   nom : `logo.png` et `donnees.xlsx` dans `clients/<client>/`. **S'arrêter**
   et attendre que l'utilisateur ait déposé les deux fichiers avant de
   continuer.

## Phase 1 — Choix du mode (après dépôt des données et du logo, via l'outil `question`)

Poser cette question :

> Souhaitez-vous être **téléguidé** par moi (je vous pose les questions et je
> prépare tout), ou préférez-vous **personnaliser vous-même** (vous suivez les
> étapes 1 à 3 du README et je génère ensuite) ?

Ensuite :
- Si **Personnaliser** → aller directement en Phase 3 (vérifier les entrées
  préparées par l'utilisateur).
- Si **Téléguidé** → continuer en Phase 2 (questionnement guidé).

## Phase 2 — Questionnement téléguidé (uniquement en mode Téléguidé)

Poser les questions **une par une** (outil `question` quand il y a des choix à
proposer, sinon question libre en français). Ordre obligatoire :

Le dossier `clients/<client>/` et son `CLIENT.md` ont déjà été créés en Phase 0.

1. **Thème de couleurs** — proposer des préréglages (et remplir `CLIENT.md`) :
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
6. **Finaliser `clients/<client>/CLIENT.md`** : le template copié en Phase 0 est
   rempli de façon incrémentale (couleurs, titre, arbre) au fil des étapes 1-5 ;
   vérifier qu'il est complet avant de passer à la Phase 3.

## Phase 3 — Logo, fond et entrées

1. **Mode Téléguidé** : `clients/<client>/` (et son `CLIENT.md`) existent déjà —
   ils ont été créés en Phase 0. **Mode Personnaliser** : vérifier que
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

## Phase 4 — Données

Les **données sont toujours fournies par l'utilisateur** (déposées en Phase 0) —
le skill **ne génère jamais** `donnees.xlsx`. Vérifier que `donnees.xlsx` est
présent dans `clients/<client>/`. Lire le `.xlsx` et en déduire le modèle de
données (tables/feuilles), les formules KPI, les colonnes source et la carte
visuelle par page. Si absent → **stop** et demander de déposer `donnees.xlsx`
avant de continuer.

## Phase 5 — Génération de la maquette HTML

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
- `donnees.xlsx` — **données source, toujours fournies par l'utilisateur**
  (déposées en Phase 0 ; le skill ne les génère jamais). Le skill en déduit le
  modèle de données, le glossaire KPI (formules) et la carte visuelle par page ;
  il s'appuie sur l'Excel seul, sans fichier de glossaire séparé.
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
