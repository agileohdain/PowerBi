# Skill: powerbi-prototype

## Ce que je fais
Je produis des maquettes de dashboards Power BI en HTML auto-suffisant, fidèles au
langage visuel Power BI (canevas 16:9 fixe, bandeau et fond dessinés en CSS,
cartes KPI, slicers, graphiques ECharts, navigation à deux niveaux).

**L'utilisateur ne fournit QUE trois choses** : le **nom du client**, le **logo**
(`logo.png`) et la **couleur primaire** (code hexadécimal). Tout le reste —
contexte métier, modèle de données, arbre de navigation, KPIs, couleurs
secondaires, titre — est **télé-guidé par questionnaire** : je propose un artefact
complet, l'utilisateur valide ou ajuste. Les données (`donnees.xlsx`) sont
**générées par moi** (`scripts/generate-data.py`, 2 années civiles closes) —
l'utilisateur ne fournit **jamais** de données, et je ne crée **jamais** le logo.

**Flux de démarrage** (déclenché par la commande `/maquette <Nom>`) :
1. Le **déclencheur est la commande `/maquette`** suivie du nom du client (ex.
   `/maquette Veloh`). Le nom vient de l'argument ; si absent, je le demande. La
   **casse est respectée telle quelle**, **je ne propose pas de nom**.
2. Je **confirme le nom** par écrit : « Est-ce bien le client « X » ? — Oui /
   Modifier ». **Je ne crée rien tant que le nom n'est pas confirmé.**
3. **Garde client existant** : si `clients/<Nom>/` existe déjà, je demande quoi
   faire (régénérer la maquette, refaire le questionnaire, ou modifier le nom).
4. Si l'utilisateur est en mode **PLAN**, je lui demande de se mettre en mode
   **BUILD** une seule fois (pas de retour PLAN par la suite).
5. Je **crée le dossier** `clients/<client>/` (casse exacte) avec `CLIENT.md`
   (copie du template, nom pré-rempli). **Je ne crée aucun logo.**
6. Je **demande** : le **logo** `logo.png` à déposer **et** la **couleur
   primaire** en hexadécimal. Je m'arrête pour attendre.
7. Je déroule le **questionnaire guidé** (Phase 1) — domaine, schéma de données,
   arbre de navigation, couleurs secondaires, titre — avec validation à chaque
   étape.
8. Je **génère** `CLIENT.md`, `data-spec.json`, `donnees.xlsx` (Phase 2), puis la
   maquette (Phase 3 : `views.json` + `render.py` + smoke test).

## Phase 0 — Nom + logo + couleur primaire

1. **Le nom du client vient de l'argument de `/maquette`** (ex. `/maquette
   Veloh`). Si la commande est lancée sans argument, je demande le nom. La
   **casse est respectée telle quelle** (majuscules/minuscules) : le nom servira
   tel quel à nommer le dossier (ex. `Veloh` → `clients/Veloh/`). **Ne proposer
   aucun nom** — l'utilisateur saisit lui-même le client. Ne pas transformer en
   slug minuscule.
2. **Confirmer le nom** : reformuler par écrit « Est-ce bien le client « X » ? —
   Oui / Modifier ». L'utilisateur peut corriger ; boucler tant que le nom n'est
   pas validé. **Ne créer rien** tant que le nom n'est pas confirmé.
3. **Garde client existant** : si `clients/<Nom>/` existe déjà, demander via
   l'outil `question` :
   - **Régénérer la maquette** → réutilise `CLIENT.md` + `data-spec.json`
     existants (les relire, régénérer `donnees.xlsx` si le spec existe, puis
     Phase 3) ;
   - **Refaire le questionnaire** → repartir en Phase 1 (les nouvelles réponses
     écrasent `CLIENT.md` / `data-spec.json` / `views.json`) ;
   - **Modifier le nom** → revenir à l'étape 2 (nouveau nom).
4. **Vérifier le mode** : si l'utilisateur est en mode **PLAN**, lui demander de
   se mettre en mode **BUILD** (nécessaire pour écrire le dossier). **Demander
   une seule fois, sans boucler** — on ne revient pas en mode PLAN.
5. **Créer immédiatement le dossier `clients/<client>/`** (dès que le nom est
   confirmé et le dossier inexistant) avec `CLIENT.md` (copie de
   `clients/_template/CLIENT.md`, nom pré-rempli sous `Brand Name` et en titre).
   **Ne créer aucun logo** (ni `logo.png` ni placeholder).
6. **Demander les deux seules fournitures** :
   - `logo.png` — déposé dans `clients/<client>/` (de préférence **fond
     transparent**, PNG) ;
   - la **couleur primaire** en **hexadécimal** (ex. `#00A1B1`) — saisie dans le
     chat, pas dans un fichier.
   **S'arrêter** et attendre ces deux éléments avant d'attaquer le questionnaire.

## Phase 1 — Questionnaire guidé (proposer → valider/ajuster)

**Pattern uniforme** : je **propose un artefact complet** (jamais de page blanche
à remplir), l'utilisateur **valide** ou **ajuste en texte libre** ; je re-présente
la version corrigée. Une itération suffit en général. Ce que l'utilisateur ne
voit jamais : les décisions techniques (formules KPI, nombre de visuels, types de
charts) — je les prends seul.

1. **Domaine métier** (question ouverte) : « Que pilote ce dashboard ? » —
   ex. « une flotte de vélos partagés », « les ventes d'un e-commerce ».
2. **Schéma de données proposé** : je traduis le domaine en **schéma en étoile**
   et je le présente en clair avant de générer :
   - table de faits (`FAIT_X` — « 1 ligne = 1 événement daté ») ;
   - **mesures** (2-3 max) avec unité et ordre de grandeur (« NB_KM, ~55 km par
     sortie »), saisonnalité et tendance annuelle si pertinentes ;
   - **dimensions** + cardinalités (≤ 40 modalités — limite de l'extracteur) ;
   - **entité « personne »** nommée pour matcher `PERSON_RE` (`DIM_CLIENT`,
     `DIM_UTILISATEUR`, `DIM_EMPLOYE`…) — requis pour les KPI « actifs » ;
   - tables catégorielles annexes éventuelles (ex. statuts d'alerte).
   → **Validation** de l'utilisateur (il peut changer tailles, modalités,
   mesures).
3. **Arbre de navigation proposé** : pages → sous-pages → KPIs, présenté en clair
   dans le chat, cohérent avec le schéma validé (chaque KPI est calculable depuis
   le modèle). Question unique : **Valider / Ajuster / Version plus riche /
   Version plus compacte**. *Ajuster* = texte libre (« renomme X », « fusionne
   1.2 et 1.3 », « ajoute une page Maintenance ») → je re-présente la version
   corrigée. **Je décide seul** : nombre de KPIs par sous-page (3-5), visuels
   associés (≤ 4 par sous-page, grille 2×2), formules (sum/ratio/scalar/top),
   badges de variation.
4. **Couleurs secondaires + titre/sous-titre proposés** :
   - le **Primary** vient du client (Phase 0) ; je détermine le **mode** (clair /
     sombre) et je propose les valeurs canoniques (`POWERBI_LAYOUT.md` §6.1) ;
   - **chaque couleur est nommée en clair** en plus de l'hex — ex. « Surface :
     blanc pur `#FFFFFF` », « Canvas : gris bleuté très clair `#F1F5F9` »,
     « Bordures : gris ardoise `#CBD5E1` » — l'utilisateur ne connaît pas les
     codes hex, il valide des mots ;
   - si le client demande ses propres secondaires, je vérifie la **cohérence vs
     Primary** (surface plus claire que le canevas, bordure neutre, canevas peu
     saturé) et je propose une correction argumentée si ça jure ;
   - je propose aussi **Report Title** et **Report Subtitle** déduits du domaine
     (ex. « VELOH — Pilotage de flotte cyclable » / « Cyclistes · Flotte ·
     Sorties — 2024–2025 »).
   → **Validation** unique pour l'ensemble.

## Phase 2 — Génération (CLIENT.md + data-spec.json + donnees.xlsx)

Les **données sont générées par le skill** — jamais fournies par l'utilisateur.

1. **J'écris `CLIENT.md`** complet (identité, couleurs validées, section
   « Contexte & Données », arbre de navigation validé) et **`data-spec.json`**
   (schéma validé, avec un `seed` fixe pour la reproductibilité — schéma :
   `clients/_template/data-spec.example.json`).
2. **Je génère les données** :
   ```bash
   python .opencode/skills/powerbi-prototype/scripts/generate-data.py clients/<client>/data-spec.json
   ```
   Le générateur écrit `donnees.xlsx` qui respecte **par construction** les
   contraintes de l'extracteur (dates **typées**, PK en 1re colonne unique, clés
   étrangères nommées exactement comme les PK, cardinalités ≤ 40, entité personne
   nommée correctement). **Période : les 2 années civiles closes précédant
   l'année courante** (dynamique : en 2026 → 2024+2025) — l'année N est toujours
   complète, la variation vs N-1 comparable sur 12 mois.
3. **Auto-contrôle intégré** : le générateur relance `extract-data.py` sur le
   fichier produit et compare le modèle détecté au spec — **toute divergence est
   bloquante** (corriger le spec, relancer). Je présente le modèle détecté à
   l'utilisateur (faits / mesures / dimensions / entité active) en une ligne.

## Phase 3 — Maquette (`views.json` + `render.py`)

1. **Brouillon déclaratif** depuis le contrat normalisé :
   ```bash
   python .opencode/skills/powerbi-prototype/scripts/extract-data.py clients/<client>/donnees.xlsx --suggest-views > clients/<client>/views.json
   ```
   Je **raffine** ensuite `views.json` pour épouser l'arbre validé (pages →
   sous-pages → KPIs + visuels, ≤ 4 visuels par sous-page). C'est la **seule**
   étape de curation : aucun HTML n'est écrit à la main. Schéma :
   `clients/_template/views.json` ; exemple : `clients/agileDSS/views.json`.
   J'humanise les libellés bruts via `labels` (accents, casse — ex. `Liege` →
   `Liège`).
2. **Génération** (parse `CLIENT.md` → variables CSS dont `--on-primary` WCAG,
   extraction → DATA, injection DATA + SPEC dans le template, écriture de
   `maquette/index.html`, **puis smoke test**) :
   ```bash
   python .opencode/skills/powerbi-prototype/scripts/render.py <client>
   ```
   Si `data-manifest.json` existe dans le dossier client, il est passé à
   l'extracteur (override de l'auto-détection — format = celui du « manifeste
   proposé » : `dims` = liste de **noms**).
3. **Référencer** `logo.png` (+ `bg.*` si présent) **depuis le dossier parent**
   via `src="../logo.png"` — **ne pas copier** le logo dans `maquette/`.
4. **Validation d'exécution (OBLIGATOIRE, bloquant)** — le smoke test est lancé
   par `render.py`, exit code 0 exigé :
   ```bash
   node .opencode/skills/powerbi-prototype/scripts/smoke-test.js clients/<client>/maquette/index.html
   ```
   Il exécute le JS de la maquette dans Node (DOM et ECharts simulés), appelle
   `renderPage()`, parcourt **toutes** les sous-pages, vérifie que chaque rendu
   appelle `echarts.init` (autant de charts que de conteneurs) **et qu'aucun
   visuel n'est sans données** (un `from:`/`measure` de `views.json` qui ne
   résout rien dans DATA = échec). **Ne jamais livrer une maquette qui échoue.**
5. Indiquer à l'utilisateur comment ouvrir le rendu (`start index.html`).

## Sources de données

- `CLIENT.md` — **contrat de marque écrit par le skill** (jamais rempli par
  l'utilisateur) : identité (`Report Title`, `Report Subtitle`), couleurs
  (`--primary`/`--surface`/`--canvas`/`--border`/`--card-bg`), contexte métier
  et arbre de navigation validés. `render.py` n'y lit que l'identité et les
  couleurs ; l'arbre de navigation vit dans `views.json`.
- `data-spec.json` — **spec de génération des données** (écrit par le skill
  après validation du questionnaire). Schéma documenté :
  `clients/_template/data-spec.example.json`.
- `donnees.xlsx` — **généré par `generate-data.py`** (jamais fourni par
  l'utilisateur). `extract-data.py` en déduit le contrat normalisé
  (`FACTS`/`BY_DIM`/`DIM_COUNTS`/`CATEGORY_COUNTS`/`ACTIVE_MASKS`/`SCALARS`/
  `META`, grain mensuel).
- `data-manifest.json` — optionnel : override de l'auto-détection, honoré par
  `render.py` (format : celui du « manifeste proposé » de l'extracteur).
- `logo.png` — **fourni par l'utilisateur** (jamais créé par le skill).
- `bg.svg`/`bg.png` — optionnel, fourni par l'utilisateur (fond personnalisé).
- `views.json` — carte visuelle déclarative (brouillon auto + raffinement).
- Modèle de départ : `clients/_template/`.

## Règles de qualité

- **Ne jamais coder une couleur en dur** : toujours via `var(--xxx)`.
- **Couleurs secondaires nommées en clair (bloquant)** : toute couleur proposée
  à l'utilisateur est accompagnée de son nom en toutes lettres (« blanc pur »,
  « gris bleuté très clair », « taupe »…) — jamais un hex seul à valider.
- **Données générées, jamais demandées (bloquant)** : l'utilisateur ne fournit
  que nom + logo + couleur primaire. Toute donnée vient de `generate-data.py`
  via un `data-spec.json` validé ; ne jamais réclamer un Excel à l'utilisateur.
- **Pas de maquette de référence (bloquant)** : ne **jamais** rechercher ni lire
  `clients/<autre>/maquette/index.html` (pas de `glob clients/*/maquette`).
  Chaque maquette est générée depuis `POWERBI_LAYOUT.md` +
  `POWERBI_COMPONENTS.md` + `CLIENT.md` + les données extraites. Le « profil
  cyclisme legacy » (`--profile cyclisme`) est un **contrat de données** de
  l'extracteur, jamais un HTML de référence.
- **Navigation L1/L2 compacte (bloquant)** : pills L1 en `text-xs` / `py-2.5 px-4`
  (hauteur ~34 px), liens L2 en `12px`. Voir `POWERBI_LAYOUT.md` §4 Row 0a.
- **Typographie (bloquant)** : titre du rapport en `<h1>` 26 px/700 ; titre de
  visuel 13 px/600 à **gauche**, sous-titre 11 px à **droite**
  (`justify-content:space-between`). Voir `POWERBI_LAYOUT.md` §2 et
  `POWERBI_COMPONENTS.md` §5.1.
- **Donut limité à ~6 tranches (bloquant)** : au-delà → **barres horizontales**,
  jamais un donut. Labels `%` **toujours** visibles. Voir `POWERBI_COMPONENTS.md`
  §3.4.
- **hbar plafonné à 10 + « Autres » (bloquant)** : tri descendant, barre
  « Autres » en ton neutre. Voir `POWERBI_COMPONENTS.md` §3.2.B.
- **Grille 2×2 sans `.wide` quand 4 visuels (bloquant)** : `grid-column: 1 / -1`
  n'est QUE pour 3 visuels ; avec 4 il crée une 3ᵉ ligne tronquée. Une table de
  détail est l'une des 4 cartes (corps scrollable). Voir `POWERBI_LAYOUT.md` §4
  Rows 2–3.
- **Un KPI = une valeur parlante (bloquant)** : jamais de concaténation brute
  (`36 / 9 / 5`). Choisir le chiffre unique que le libellé signifie. Voir
  `POWERBI_COMPONENTS.md` §1.4.
- **Palette de visuels dérivée du primaire (bloquant)** : **jamais** de palette
  arc-en-ciel. Toute couleur catégorielle vient de `derivePalette(--primary)`.
  Seuls « Autres » et la courbe N-1 utilisent un neutre. Couleurs sémantiques
  réservées : vert/rouge/neutre des badges de variation. Voir
  `POWERBI_COMPONENTS.md` § palette.
- **Hauteurs des visuels normalisées** : grille à lignes égales
  (`grid-template-rows: 1fr 1fr`) — **jamais** de hauteur fixe en px. Disposition
  **par défaut 2×2 avec 4 visuels** lorsque les données supportent 4 visuels
  pertinents (sinon 3, le 3ᵉ en pleine largeur). Voir `POWERBI_LAYOUT.md` §4.
- **Chiffre central des donuts centré** : superposition HTML centrée via CSS —
  **jamais** un `title`/`graphic` ECharts. Total central **calculé** depuis les
  tranches, jamais hardcodé. Voir `POWERBI_COMPONENTS.md` §3.4.
- Le **titre/sous-titre** sur le bandeau est TOUJOURS en `var(--on-primary)`.
- Le texte de pane "Filtres" + son icône est TOUJOURS en `var(--primary)`.
- Dériver `--text-primary`/`--text-secondary` selon la luminance de `--canvas`.
- Responsive : le canevas 1920×1080 est scaled pour s'adapter au viewport sans
  scrollbars, via `transform: scale(...)`.
- **Espacements normalisés (bloquant)** : une seule échelle (`4/8/12/16/20/24`
  px). Colonne `.content` en `flex` avec **un seul `gap:12px`**. Rangée KPI à
  hauteur **fixe uniforme** (`130px`). Voir `POWERBI_LAYOUT.md` §1 & §4.
- **Pane filtres jusqu'en bas (bloquant)** : le pane descend jusqu'au footer
  (`top:116px; bottom:40px`), « Réinitialiser » épinglé en bas
  (`margin-top:auto`). Labels `11px/600/uppercase/--text-secondary`, contrôles
  `12px` / hauteur `32px` / `border-radius:8px`. Voir `POWERBI_LAYOUT.md` §3.
- **Filtres interactifs, non liés aux données (bloquant)** : les slicers
  réagissent au clic (badge « ● Filtres actifs », « Réinitialiser ») — **un
  slicer par dimension** — **mais aucun recompute** : le tableau de bord montre
  toujours l'année N. Voir `POWERBI_COMPONENTS.md` §2.7 et §6.
- **Variation vs N-1 (bloquant)** : tout KPI dérivé de la série temporelle
  affiche sa variation N vs N-1, sur toutes les pages, calculée sur mois
  comparables ; badge masqué si non calculable, jamais inventé. Voir
  `POWERBI_COMPONENTS.md` §1.3.
- **Badge de variation : état neutre (bloquant)** : `|Δ| < 1 %` → badge **neutre
  gris** `≈ stable vs <année>` — jamais un vert `+0 %` ni un rouge `-0,1 %`.
  **Libellé en année réelle** (`vs 2024`), jamais le jargon `vs N-1`. Voir
  `POWERBI_COMPONENTS.md` §1.1/§1.3.
- **Contraste on-primary WCAG AA (bloquant)** : le texte sur le bandeau utilise
  un token `--on-primary` **dérivé** (`--surface` si contraste ≥ 4,5:1 avec
  `--primary`, sinon texte sombre). **Jamais** de `color:var(--surface)` codé en
  dur sur le bandeau. Voir `POWERBI_LAYOUT.md` §2 & §6.
- **Libellés en années réelles (bloquant)** : sous-titres de visuels et badges
  affichent `${CUR_YEAR} vs ${PREV_YEAR}` (ex. `2025 vs 2024`), jamais `N vs
  N-1`. Voir `POWERBI_COMPONENTS.md` §5.1 & §1.3.
- **Aire sous la courbe N interdite si année partielle (bloquant)** : pas
  d'`areaStyle` sur N ; signaler l'année en cours par une `markLine` verticale
  pointillée. Voir `POWERBI_COMPONENTS.md` §3.3.
- **Donut anti-rognage (bloquant)** : `center:['35%','50%']`,
  `radius:['48%','66%']`, overlay `left:35%`. Labels `%` au format français
  (`10,5 %`). Voir `POWERBI_COMPONENTS.md` §3.4.
- **Filtres : bouton « Réinitialiser » + plage de dates liée au badge
  (bloquant)** : icône **rotate-ccw** + label « Réinitialiser ». Trimestre
  (≤ 4 valeurs) en **chiclets**, mutuellement exclusif avec Mois. Voir
  `POWERBI_COMPONENTS.md` §2.6 & §2.7.
- **Humanisation des libellés (bloquant)** : les clés brutes de l'extracteur
  (`Depasse`, `Saint_Bruno`, `2024-01`) sont **mappées** via `labels` dans
  `views.json` avant tout affichage. Voir `POWERBI_COMPONENTS.md` §2.7.
- **Popover info cliquable + clavier (bloquant)** : les lignes de sous-pages
  naviguent au clic (`go(page, sub)`), ouverture aussi au `:focus-within`. Voir
  `POWERBI_COMPONENTS.md` §4.3.
- **Visuels temporels (axe mois) — Jan→Déc fixe, N vs N-1 (bloquant)** : 12
  points `01`..`12`, **année N** en `--primary` solide, **N-1 en pointillé +
  neutre**, légende, `yAxis.scale:true`. Voir `POWERBI_COMPONENTS.md` §3.3.
- **Icône info** : une seule, en haut à droite du bandeau ; le popover explique
  la page active + la sous-page sélectionnée (re-rendu à chaque navigation).
  Voir `POWERBI_COMPONENTS.md` §4.3.
- **Formats KPI/visuels** : `int | km | eur | f1 | dur | pct | text`
  (`eur` = montant formaté fr-FR, ex. `12,3 k €`).
- **Aucune erreur JS tolérée (bloquant)** : `renderPage()` et **chaque**
  sous-page doivent s'exécuter sans exception, chaque visuel initialisé et
  **alimenté en données** — vérifié mécaniquement par `scripts/smoke-test.js`
  (exit code 0 exigé avant livraison). Les cinq pièges classiques :
  1. **Réassigner une `const`** (ex. registre de charts). Utiliser le snippet
     canonique de `POWERBI_COMPONENTS.md` §6.
  2. **Référencer un identifiant non déclaré** dans une vue (la casse compte).
  3. **Placer la zone de contenu en `top:0`** : la navigation se dessine
     **par-dessus le bandeau**. Le conteneur commence sous le bandeau
     (`top:97px`) — voir `POWERBI_LAYOUT.md` §4.
  4. **Guarder l'init des charts avec une propriété jamais définie** : le seul
     guard autorisé est `if (!el) return;`. Voir `POWERBI_COMPONENTS.md` §6.
  5. **Composer nav + KPI + visuels par concaténation d'innerHTML dans un
     conteneur partagé** : utiliser des conteneurs statiques dédiés (`#navL1`,
     `#navL2`, `#kpis`, `#visuals`) — voir `POWERBI_LAYOUT.md` §4.
- Valider la maquette **en cours** via le smoke test (exit 0) ; les sous-pages
  non couvertes par le test restent des defaults cohérents. **Ne jamais** lire
  la maquette d'un autre client comme référence de layout.
