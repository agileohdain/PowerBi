---
name: powerbi-prototype
description: Génère des maquettes de dashboards Power BI haute-fidélité (canevas 16:9, bandeau/fond en CSS, cartes KPI, slicers, visuels ECharts, navigation deux-niveaux) en HTML/Tailwind/ECharts auto-suffisant. Déclencheur principal : la commande /maquette suivie du nom du client (ex. "/maquette Veloh"). Use when the user wants to create a Power BI dashboard mockup for a client — e.g. a slash command /maquette, or natural phrasing like "maquette power bi", "crée la maquette", "nouvelle maquette client". Le corps du skill décrit le processus complet (confirmation nom, création du dossier client sans logo, dépôt logo/données/CLIENT.md rempli, vérification de complétude avec arrêt et questions).
---

## Ce que je fais
Je produis des maquettes de dashboards Power BI en HTML auto-suffisant, fidèles au
langage visuel Power BI (canevas 16:9 fixe, bandeau et fond dessinés en CSS,
cartes KPI, slicers, graphiques ECharts, navigation à deux niveaux).

**Flux de démarrage** (déclenché par la commande `/maquette <Nom>`) :
1. Le **déclencheur est la commande `/maquette`** suivie du nom du client (ex.
   `/maquette Veloh`). Le nom vient de l'argument de la commande ; si absent,
   je le demande. La **casse est respectée telle quelle**
   (majuscules/minuscules), **je ne propose pas de nom**.
2. Je **confirme le nom** par écrit : « Est-ce bien le client « X » ? — Oui /
   Modifier » (l'utilisateur peut corriger). **Je ne crée rien tant que le nom
   n'est pas confirmé.**
3. **Garde client existant** : si `clients/<Nom>/` existe déjà, je demande quoi
   faire (régénérer la maquette de ce client, ou modifier le nom) avant de créer
   quoique ce soit.
4. Si l'utilisateur est en mode **PLAN**, je lui demande de se mettre en
   mode **BUILD** une seule fois (pas de retour PLAN par la suite). Tout le
   reste du processus se déroule en BUILD.
5. Je **crée automatiquement le dossier** `clients/<client>/` (casse exacte)
   avec `CLIENT.md` (copie du template, nom pré-rempli). **Je ne crée aucun
   logo**.
6. Je **demande de déposer** dans `clients/<client>/` : le **logo** `logo.png`,
   les **données** `donnees.xlsx` **et le `CLIENT.md` rempli**. Je m'arrête pour
   attendre. Je **ne génère jamais** les données ni le logo.
7. Une fois le dépôt confirmé, je **parcours `CLIENT.md`** : si une information
   n'est **pas renseignée** (encore sous forme `<...>`), ou si `logo.png` /
   `donnees.xlsx` manquent, je **m'arrête** et je demande à l'utilisateur de
   saisir précisément les informations manquantes. Je re-vérifie en boucle
   jusqu'à ce que tout soit complet, puis je génère.
8. Je génère la maquette (Phase 4 ci-dessous).

Il n'y a **pas** de mode « Téléguidé » : `CLIENT.md` est **toujours rempli par
l'utilisateur** ; je me contente de le vérifier et de demander les champs
manquants.

## Phase 0 — Nom du client (déclencheur) + confirmation + création du dossier

1. **Le nom du client vient de l'argument de `/maquette`** (ex. `/maquette
   Veloh`). Si la commande est lancée sans argument, je demande le nom. La
   **casse est respectée telle quelle** (majuscules/minuscules) : le nom
   servira tel quel, avec la casse exacte, à nommer le dossier (ex. `Veloh` →
   `clients/Veloh/`). **Ne proposer aucun nom** — l'utilisateur saisit lui-même
   le client. Ne pas transformer en slug minuscule.
2. **Confirmer le nom** : reformuler par écrit, de façon claire et accueillante,
   « Est-ce bien le client « X » ? — Oui / Modifier ». L'utilisateur peut
   corriger ; boucler tant que le nom n'est pas validé. **Ne créer rien** tant
   que le nom n'est pas confirmé.
3. **Garde client existant** : si `clients/<Nom>/` existe déjà (par exemple le
   dossier d'un client déjà traité), demander via l'outil `question` :
   - **Régénérer la maquette de ce client** → sauter la création du dossier,
     vérifier le logo, les données et `CLIENT.md` (Phase 2), puis générer.
   - **Modifier le nom** → revenir à l'étape 2 (nouveau nom).
4. **Vérifier le mode** : si l'utilisateur est en mode **PLAN**, lui demander de
   se mettre en mode **BUILD** (nécessaire pour écrire le dossier). **Demander
   une seule fois, sans boucler plusieurs fois** — on ne revient pas en mode PLAN.
5. **Créer immédiatement le dossier `clients/<client>/`** (dès que le nom est
   confirmé et le dossier inexistant) avec `CLIENT.md` (copie de
   `templates/CLIENT.template.md`/`clients/_template/CLIENT.md`, nom du client
   pré-rempli sous `Brand Name` et en titre). **Ne créer aucun logo** (ni
   `logo.png` ni placeholder) — le logo est fourni par l'utilisateur.
6. **Demander de déposer les fichiers** dans `clients/<client>/` :
   - `logo.png` — le logo du client (de préférence **fond transparent**, PNG),
   - `donnees.xlsx` — les données source,
   - `CLIENT.md` — **rempli** par l'utilisateur (il édite la copie créée en
     étape 5, ou copie celle de `clients/_template/`).
   **S'arrêter** et attendre que ces éléments soient présents avant de continuer.

## Phase 1 — Vérification de `CLIENT.md`, du logo et des données

Après le dépôt, **vérifier la complétude** avant de générer :

1. **Logo (obligatoire)** : vérifier `clients/<client>/logo.png`. Si absent →
   **stop** et demander de déposer le logo du client dans `clients/<client>/`.
2. **Données (obligatoires)** : vérifier `clients/<client>/donnees.xlsx`. Si
   absent → **stop** et demander de déposer `donnees.xlsx`.
3. Lire `CLIENT.md` et **parcourir chaque champ** :
   - **Identité** : `Brand Name`, `Report Title`, `Report Subtitle` — aucun ne
     doit rester sous forme `<...>` (`<CLIENT_NAME>`, `<Titre du rapport>`,
     `<sous-titre / période>`).
   - **Couleurs** : `Primary / Banner Accent`, `Surface / Cards`,
     `Canvas Background`, `Card Frame Color`, `Border / Divider` — aucune ne
     doit rester sous forme `<...>` (`<Primary>`, `<Surface>`,
     `<Canvas Background>`, `<Card Frame>`, `<Border>`) ; attendre un code
     hexadécimal (ex. `#00A1B1`).
   - **Arbre de navigation** : chaque page/sous-page doit avoir un titre
     rempli et chaque `Libellé KPI` doit être renseigné (aucun `<Titre page N>`,
     `<Titre sous-page>`, `<Libellé KPI>` restant).
4. Si **un seul champ** est encore non rempli (marqueur `<...>`), ou si le
   logo / les données manquent → **s'arrêter** et demander à l'utilisateur de
   saisir **exactement** les informations manquantes (les lister clairement),
   en rappelant qu'il édite `CLIENT.md` lui-même. **Re-vérifier** en boucle
   jusqu'à complétude totale.
5. Propriété optionnelle : déduire `--text-primary` / `--text-secondary` selon
   la luminance du `Canvas Background` (clair → `#0F172A`/`#64748B` ; sombre →
   `#F1F5F9`/`#94A3B8`). Ce n'est pas un champ à vérifier.
6. **Fond `bg.*` (optionnel)** : si `bg.svg` **ou** `bg.png` est présent, il sera
   utilisé comme image de fond (prioritaire sur le rendu CSS). Sinon, le bandeau,
   la zone logo, le fond canevas et le pane filtres sont **dessinés en CSS** —
   ce n'est **pas bloquant**.

## Phase 2 — Données

Les **données sont toujours fournies par l'utilisateur** (déposées en Phase 0) —
le skill **ne génère jamais** `donnees.xlsx`. Lire le `donnees.xlsx` présent
dans `clients/<client>/` et en déduire le modèle de données (tables/feuilles),
les formules KPI, les colonnes source et la carte visuelle par page. (Vérifié en
Phase 1.)

**Extraction canonique (obligatoire)** : ne pas dériver le modèle à la main —
lancer l'extracteur et embarquer **tout** son bloc de données (jamais un sous-
ensemble, sinon des KPI sont mal interprétés et des dimensions manquent) :

```bash
python .opencode/skills/powerbi-prototype/scripts/extract-data.py clients/<client>/donnees.xlsx
```

L'extracteur est **générique (tout domaine)** : il **auto-détecte** la table de
faits, la colonne date, les mesures, les dimensions (jointures et ponts inclus),
les agrégats catégoriels et l'entité active, puis émet un contrat **normalisé**
(`FACTS` / `BY_DIM` / `DIM_COUNTS` / `CATEGORY_COUNTS` / `ACTIVE_MASKS` /
`SCALARS` / `META`). Il propose un manifeste sur `stderr` — copiez-le dans
`clients/<client>/data-manifest.json` pour corriger/forcer la détection. Pour un
client **cyclisme existant** (Veloh, agiledss), garder le contrat historique via
`--profile cyclisme`. Voir `references/POWERBI_COMPONENTS.md` §6.1 pour le
contrat complet et le mapping `CLIENT.md` → séries.

**Agréger au grain MENSUEL pour l'année N et la variation N-1** (obligatoire —
voir `references/POWERBI_COMPONENTS.md` §6). Le tableau de bord affiche
toujours **l'année N** (`CUR_YEAR` = année la plus récente de `MONTH_META`).
En plus des tableaux finaux par sous-page, le skill pré-calcule et **embarque
dans le HTML** :
- les **séries mensuelles** des mesures cœur (ex. `KM[]`, `RIDES[]`,
  `MINUTES[]`), chronologiques, avec `MONTH_META` (`{year, month, quarter}`) ;
- les **séries mensuelles par dimension** chartée (ex. `KM_PAYS_M`,
  `KM_MARQUE_M`), agrégées sur les mois de l'année N pour les visuels non-
  temporels ;
- un **masque d'activité par entité** (bit `i` = actif au mois `i`) pour les KPI
  de type « entités actives » (actifs en N = mask ∩ masque des mois de N) ;
- la **comparaison N vs N-1** sur mois comparables (mêmes mois que N), jamais
  une année N partielle contre une N-1 complète (voir §1.4).

Sans ce grain mensuel, ni l'**année N** ni la **variation vs N-1** ne sont
possibles — c'est la régression à éviter.

## Phase 3 — Génération de la maquette HTML

1. Lire `CLIENT.md` (+ `references/POWERBI_LAYOUT.md` et
   `POWERBI_COMPONENTS.md`), et les données dans `donnees.xlsx` (model/séries).
2. Produire `clients/<client>/maquette/index.html` — fichier **auto-suffisant** :
   - Tailwind via CDN, Apache ECharts via CDN.
   - Canevas 1920×1080 fixe, scaling CSS pour s'adapter au viewport (pas de scroll).
   - **Fond** :
     - Si `bg.svg`/`bg.png` présent → `background: url(./bg.svg) center/cover
       no-repeat` (adapter l'extension) ; **ne pas redessiner** le bandeau ni la
       zone logo en CSS (ils sont dans l'image).
    - Sinon → **dessiner en CSS** : bandeau haut (~97px) en `var(--primary)`
      avec zone logo (~245px) en `var(--surface)` contenant `logo.png`, fond
      canevas en `var(--canvas)`, pane filtres à gauche (fond `var(--surface)`).
    - **Cassure de l'en-tête** : la zone logo et la bannière sont des **trapèzes**
      (bords diagonaux) fidèles au `.pptx` template — le léger intervalle
      diagonal entre les deux laisse voir le fond canevas. Via `clip-path` :
      zone logo `polygon(0 0, 320px 0, 244px 97px, 0 97px)` ; bannière
      `polygon(342px 0, 100% 0, 100% 97px, 267px 97px)`.
   - Variables CSS en `:root` lues depuis `CLIENT.md` :
     `--primary`, `--surface`, `--canvas`, `--border`, `--card-bg`,
     `--text-primary`, `--text-secondary`.
   - **Titre + sous-titre** positionnés par-dessus le bandeau (zone haute,
      ~0-97px), en `var(--surface)`, **centrés horizontalement dans la zone du
      bandeau** (à droite de la cassure, ex. `left:360px; right:48px;
      text-align:center`).
    - Pane filtres à gauche avec **"Filtres" + icône en `var(--primary)`**,
      fond **`var(--surface)`** (blanc, identique à Surface/Cards), **panneau
      arrondi flottant** fidèle au template : `left:11px`, `top:116px` (gap ~19px
      sous le bandeau), `width:235px`, `border-radius:10px`, **sans bordure**.
      **Filtres interactifs, non liés aux données** : les slicers réagissent au
      clic (année en chiclets multi-sélection, trimestre/mois en dropdowns
      mutuellement exclusifs, plage de dates slider + champs synchronisés, **un
      slicer par dimension** du modèle — chiclets si ≤ ~6 valeurs sinon dropdown
      —, bouton « Effacer ») — le bouton cliqué se colore, le badge **« ● Filtres
      actifs »** s'affiche, « Effacer » réinitialise le pane — **mais aucun
      recompute** : KPIs et visuels montrent toujours l'année N. Les slicers de
      dimensions remplissent le pane jusqu'en bas (aérés, pas de tassement).
      Voir `POWERBI_COMPONENTS.md` §2.7.
   - **Icône information unique** en haut à droite du bandeau (~36px, circulaire,
     sur `var(--surface)`) : au **survol**, un popover explique la **page active
     ET la sous-page actuellement sélectionnée** (en évidence), puis liste les
     autres sous-pages — re-rendu à chaque navigation. **Survol sans zone
     morte** : icône + popover dans un **conteneur de survol partagé** (ou
     popover dont le haut chevauche le bas de l'icône) pour que l'infobulle ne
     se ferme pas quand on la survole. **Aucun** « i » par carte visuelle. Voir
     `POWERBI_COMPONENTS.md` §4.3.
   - Navigation L1 (pills) + L2 (liens texte) rendue depuis `CLIENT.md`, avec
     un **petit routeur JS** (`state = { page, subpage }`) rendant la **page et
     les sous-pages cliquables** ; chaque sous-page de `CLIENT.md` reçoit un
     **layout complet** (KPIs + visuels ECharts).
    - Cartes KPI (avec état consolidation si flag présent) + visuels ECharts
      depuis la carte visuelle déduite de `donnees.xlsx`. **KPI = valeur de
      l'année N + variation N vs N-1 obligatoire** sur **tout KPI dérivé de la
      série temporelle, sur toutes les pages** (badge `±x,x % vs N-1`,
      vert/rouge, calculé sur mois comparables, masqué si non calculable) — voir
      `POWERBI_COMPONENTS.md` §1.4. **Visuels non-temporels** (donut, hbar,
      table) : agrégats de l'année N. **Visuels temporels** : N vs N-1.
   - **Visuels principaux** : grille à **hauteurs égales** (`grid-template-rows:
     1fr 1fr`, aucune hauteur fixe en px), par défaut **2×2 avec 4 visuels** si
     les données supportent 4 visuels pertinents (sinon 3, le 3ᵉ en pleine
     largeur sur la 2ᵉ ligne). Chiffre central des donuts en **superposition
     HTML centrée** (jamais en `title`/`graphic` ECharts). Voir
     `POWERBI_LAYOUT.md` §4 et `POWERBI_COMPONENTS.md` §3.4.
   - Logo `logo.png` affiché dans la zone logo (en haut à gauche).
   - Footer disclaimer "Données fictives".
3. **Référencer** `logo.png` (+ `bg.*` si présent) **depuis le dossier parent**
   via `src="../logo.png"` — **ne pas copier** le logo dans `maquette/`
   (pas de doublon). La maquette assume que le dossier parent `clients/<client>/`
   contient `logo.png` et `donnees.xlsx`.
4. **Validation d'exécution (OBLIGATOIRE, bloquant)** : avant de livrer,
   exécuter le smoke test fourni et **corriger jusqu'à exit code 0** :
   ```bash
   node .opencode/skills/powerbi-prototype/scripts/smoke-test.js clients/<client>/maquette/index.html
   ```
   Ce test exécute le JS de la maquette dans Node (DOM et ECharts simulés) :
   il appelle `renderPage()`, vérifie que la rangée de KPI et les visuels sont
   remplis, parcourt **toutes** les sous-pages (`go(page, sub)`) et exécute
   chaque vue. Il vérifie aussi que **chaque rendu appelle bien
   `echarts.init`** (autant de charts initialisés que de conteneurs rendus) —
   une maquette peut tourner sans aucune exception tout en n'affichant
   **aucun visuel** (guard fautif qui retourne silencieusement à chaque
   appel). **Ne jamais livrer une maquette qui échoue ce test** — une seule
   erreur JS fatale (réassignation d'une `const`, `ReferenceError` sur un
   identifiant non déclaré ou mal orthographié, …) rend la page **vide** dans
   le navigateur : la navigation s'affiche mais ni les KPI ni les visuels.
   Voir aussi `POWERBI_LAYOUT.md` §4 (géométrie du conteneur) et
   `POWERBI_COMPONENTS.md` §6 (registre des charts, identifiants DATA).
5. Indiquer à l'utilisateur comment ouvrir le rendu (`start index.html`).

## Sources de données
- `CLIENT.md` — **fichier pilote, rempli par l'utilisateur** : identité de
  marque (couleurs via `--primary`/`--surface`/`--canvas`/`--border`/`--card-bg`),
  titre, arbre de navigation (pages / sous-pages / KPIs, flags `[En
  consolidation]`). Le skill vérifie qu'aucun marqueur `<...>` ne reste avant de
  générer.
- `donnees.xlsx` — **données source, toujours fournies par l'utilisateur**
  (déposées en Phase 0 ; le skill ne les génère jamais). Le skill en déduit le
  modèle de données, le glossaire KPI (formules) et la carte visuelle par page ;
  il s'appuie sur l'Excel seul, sans fichier de glossaire séparé.
- Modèle de départ : `clients/_template/` (à copier pour chaque nouveau
  client).

## Règles de qualité
- **Ne jamais coder une couleur en dur** : toujours via `var(--xxx)`.
- **Navigation L1/L2 compacte (bloquant)** : pills L1 en `text-xs` / `py-2.5 px-4`
  (hauteur ~34 px), liens L2 en `12px`. Jamais de classe `.pill` maison plus grosse
  (13 px / padding 11 px) — la navigation devient trop grande. Voir
  `POWERBI_LAYOUT.md` §4 Row 0a.
- **Typographie (bloquant)** : titre du rapport en `<h1>` 26 px/700 (jamais 800 +
  `letter-spacing:.5px`) ; titre de visuel 13 px/600 à **gauche**, sous-titre 11 px
  à **droite** (`justify-content:space-between`). Voir `POWERBI_LAYOUT.md` §2 et
  `POWERBI_COMPONENTS.md` §5.1.
- **Donut limité à ~6 tranches (bloquant)** : au-delà (ex. 25 marques) →
  **barres horizontales**, jamais un donut. *Vélos par marque* = hbar. Labels `{d} %`
  **toujours** visibles. Centre du donut `['30%','50%']` aligné sur l'overlay
  (`left:30%;top:50%`). Voir `POWERBI_COMPONENTS.md` §3.4.
- **hbar plafonné à 10 + « Autres » (bloquant)** : un hbar de dimension dépasse
  rarement 10 barres — au-delà (25 marques, 16 villes), agréger en **top 10 +
  barre « Autres »** (helper `topBars`, miroir de `topDonut`), tri descendant,
  barre « Autres » en ton neutre. Régression récurrente : *Vélos par marque* à 25
  barres écrasées (alors que *Kilométrages par marque*, déjà sliced ~12, est lisible).
  Voir `POWERBI_COMPONENTS.md` §3.2.B.
- **Grille 2×2 sans `.wide` quand 4 visuels (bloquant)** : `grid-column: 1 / -1`
  n'est QUE pour 3 visuels ; avec 4 il crée une 3ᵉ ligne tronquée (table coupée).
  Une table de détail est l'une des 4 cartes (corps scrollable). Voir
  `POWERBI_LAYOUT.md` §4 Rows 2–3.
- **Un KPI = une valeur parlante (bloquant)** : jamais de concaténation brute
  (`36 / 9 / 5`). Choisir le chiffre unique que le libellé signifie (comptage,
  ratio/moyenne recalculée pour l'année N, ou valeur nommée courte). Voir
  `POWERBI_COMPONENTS.md` §1.5.
- **Palette de visuels dérivée du primaire (bloquant)** : **jamais** de palette
  arc-en-ciel (vert/bleu/jaune/violet). Toute couleur catégorielle (tranches de
  donut, barres hbar, multi-séries) vient de `derivePalette(--primary)` (primaire
  + nuances harmonisées). Seuls « Autres » et la courbe N-1 utilisent un neutre.
  Couleurs sémantiques réservées : rouge consolidation `#FF0000`, vert/rouge des
  badges de variation. Voir `POWERBI_COMPONENTS.md` § palette.
- **Hauteurs des visuels normalisées** : les visuels principaux d'une sous-page
  sont rendus dans une grille à lignes égales (`grid-template-rows: 1fr 1fr`) —
  **jamais** de hauteur fixe en px. Disposition **par défaut 2×2 avec 4 visuels**
  lorsque les données supportent 4 visuels pertinents (sinon 3, le 3ᵉ en pleine
  largeur sur la 2ᵉ ligne, hauteurs toujours égales). Voir `POWERBI_LAYOUT.md`
  §4 Rows 2–3.
- **Chiffre central des donuts centré** : le chiffre/sous-titre est une
  **superposition HTML** centrée via CSS (`left/top` = centre du pie,
  `transform: translate(-50%,-50%)`) — **jamais** un `title`/`graphic` ECharts
  (non centrés sur l'ancre). Voir `POWERBI_COMPONENTS.md` §3.4.
- Le **titre/sous-titre** sur le bandeau est TOUJOURS en `var(--surface)`.
- Le texte de pane "Filtres" + son icône est TOUJOURS en `var(--primary)`.
- Dériver `--text-primary`/`--text-secondary` selon la luminance de `--canvas`.
- Responsive : le canevas 1920×1080 est scaled pour s'adapter au viewport sans
  scrollbars, via `transform: scale(...)` calculé par un petit script.
- **Filtres interactifs, non liés aux données (bloquant)** : les slicers sont
  interactifs (le clic colore le bouton, met à jour la sélection, affiche le
  badge « ● Filtres actifs », « Effacer » réinitialise) — **un slicer par
  dimension** (chiclets ≤6 valeurs sinon dropdown) remplit le pane jusqu'en bas,
  aéré — **mais aucun recompute** : le tableau de bord montre toujours l'année N
  (KPIs : valeur N + variation N vs N-1 ; visuels non-temporels : N ; visuels
  temporels : N vs N-1). Données au grain mensuel embarquées pour calculer
  l'année N et la variation N-1. Voir `POWERBI_COMPONENTS.md` §2.7 et §6.
- **Variation vs N-1 (bloquant)** : tout KPI dérivé de la série temporelle
  affiche sa variation N vs N-1, sur toutes les pages, calculée sur mois
  comparables (mêmes mois que N) ; badge masqué si non calculable, jamais inventé.
  Voir `POWERBI_COMPONENTS.md` §1.4.
- **Visuels temporels (axe mois) — Jan→Déc fixe, N vs N-1 (bloquant)** : tout
  line/bar d'évolution sur un axe mois affiche **12 points `01`..`12`**
  (Jan→Déc, jamais la liste plate des mois), en **2 séries** — **année N** en
  `--primary` **solide/fort**, **N-1 en pointillé + plus léger** (neutre, fin) —
  avec **légende**, et `yAxis.scale:true` (ne pas ancrer la courbe à 0, ex.
  *Durée moy. / sortie*). Multi-séries par dimension (top marques, empilé par
  pays) → axe Jan→Déc de l'**année N uniquement** (pas de split N-1, illisible),
  couleurs issues de la palette dérivée. Voir `POWERBI_COMPONENTS.md` §3.3.
- **Icône info** : une seule, en haut à droite du bandeau ; le popover explique
  la page active + la sous-page sélectionnée (re-rendu à chaque navigation) et
  reste atteignable au survol (conteneur de survol partagé). Voir §4.3.
- **Aucune erreur JS tolérée (bloquant)** : `renderPage()` et **chaque**
  sous-page doivent s'exécuter sans exception — vérifié mécaniquement par
  `scripts/smoke-test.js` (exit code 0 exigé avant livraison). Les cinq pièges
  classiques à éviter absolument :
  1. **Réassigner une `const`** (ex. registre de charts : `const charts={}` puis
     `charts={}` → `TypeError`, page vide). Utiliser le snippet canonique de
     `POWERBI_COMPONENTS.md` §6.
  2. **Référencer un identifiant non déclaré** dans une vue (la casse compte :
     `CITY_CYCLISTES` ≠ `cityCyclistes`). Tout identifiant utilisé doit être
     déclaré une fois dans le bloc DATA.
  3. **Placer la zone de contenu en `top:0`** : la navigation L1/L2 se dessine
     alors **par-dessus le bandeau** et masque le titre. Le conteneur de
     contenu commence sous le bandeau (`top:97px`) — voir `POWERBI_LAYOUT.md` §4.
  4. **Guarder l'init des charts avec une propriété jamais définie** (ex.
     `if (!el || !el.__chart) return;`) : `echarts.init` n'est jamais appelé,
     **aucune exception n'est levée** et toutes les cartes restent vides au
     navigateur. Le seul guard autorisé est `if (!el) return;` — le smoke test
     compte les `echarts.init` et exige un chart par conteneur rendu. Voir
     `POWERBI_COMPONENTS.md` §6.
  5. **Composer nav + KPI + visuels par concaténation d'innerHTML dans un
     conteneur partagé** (ex. `content.innerHTML = navHtml +
     content.innerHTML`) : re-parser le HTML sérialisé détruit le DOM vivant
     des charts et les listeners à chaque rendu. Utiliser des conteneurs
     statiques dédiés (`#navL1`, `#navL2`, `#kpis`, `#visuals`) — voir
     `POWERBI_LAYOUT.md` §4.
- Une seule page de mockup pleinement validée par exécution ; les autres
  sous-pages sont des defaults cohérents.
