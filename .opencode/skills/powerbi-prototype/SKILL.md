# Skill: powerbi-prototype

## Ce que je fais
Je produis des maquettes de dashboards Power BI en HTML auto-suffisant (canevas
16:9, bandeau aux couleurs du client, cartes KPI avec variation N vs N-1,
slicers, visuels ECharts, navigation à deux niveaux).

**L'utilisateur ne fournit QUE trois choses** : le **nom du client**, le
**logo** (`logo.png`) et la **couleur primaire** (hex). Tout le reste est
**télé-guidé par questionnaire** : je propose, l'utilisateur valide ou ajuste.
Les données (`donnees.xlsx`) sont **générées par moi** (`scripts/generate-data.py`,
2 années civiles closes) — jamais fournies par l'utilisateur. Je ne crée
**jamais** le logo.

## Interdictions de lecture (bloquant — gain de temps critique)

- **Ne JAMAIS lire `references/`** (`TEMPLATE.md`, `template.html`) : ils
  documentent le moteur de rendu pour sa maintenance. Le HTML/CSS/JS n'est
  plus jamais écrit à la main — il sort de `render.py` + `template.html`.
  Tout ce dont j'ai besoin en run est dans ce fichier.
- **Ne JAMAIS lire la maquette d'un autre client** (pas de
  `glob clients/*/presentation`). Chaque maquette dérive de `CLIENT.md` +
  `nav.json` + les données extraites.
- **Ne pas relire `generate-data.py` / `extract-data.py` à chaque run** — la
  section « Patterns réutilisables » + les 2 fichiers d'exemple
  (`clients/_template/data-spec.example.json`, `nav.example.json`) suffisent.
- **Ne JAMAIS relancer le smoke test à la main** : `render.py` l'exécute déjà
  (exit 0 exigé — s'il échoue, `render.py` échoue).

## Flux de démarrage (déclenché par `/maquette <Nom>`)

1. Le nom vient de l'argument (si absent, je le demande). **Casse respectée
   telle quelle**, je ne propose aucun nom.
2. Je confirme le nom via l'outil `question` (option **Oui** + saisie libre) —
   je ne crée rien tant qu'il n'est pas confirmé.
3. Garde client existant : si `clients/<Nom>/` existe, je demande (régénérer
   la maquette / refaire le questionnaire / modifier le nom).
4. Si l'utilisateur est en mode PLAN, je demande le passage en BUILD **une
   seule fois**.
5. Je crée `clients/<client>/` avec `CLIENT.md` (copie du template, nom
   pré-rempli). Aucun logo créé.
6. Je demande les **deux fournitures en UNE seule question** directive dont
   voici le libellé canonique (à recopier, `<Nom>` substitué) :

   > **2 fournitures pour démarrer :**
   >
   > 1. **LOGO** — déposez votre logo (PNG, fond transparent) **exactement**
   >    ici : `clients/<Nom>/logo.png`
   > 2. **COULEUR PRIMAIRE** — ci-dessous, **sélectionnez « Type your own
   >    answer »** puis saisissez **uniquement** le code hex (ex. `#00A1B1`).
   >
   > ⚠️ Ne cochez pas d'option : choisissez « Type your own answer » et
   > collez le code hex.

   Options : **une seule**, échappatoire —
   `{"label": "Pas encore prêt", "description": "Je dépose le logo / cherche le hex d'abord"}`.
   Le chemin normal est la **saisie libre** (le hex) ; je n'accepte que ça.
   Un clic sur l'échappatoire → j'attends. Je m'arrête pour attendre.
7. Questionnaire guidé (Phase 1, **2 questions**), génération (Phase 2),
   maquette + pitch (Phase 3).

## Phase 1 — Questionnaire guidé (2 validations)

**Pattern** : je propose un artefact complet (jamais de page blanche),
l'utilisateur valide ou ajuste en texte libre. Une itération suffit en général.
Les décisions techniques (formules KPI, types de charts, dispatch dans les
pages) sont miennes — l'utilisateur ne les voit jamais.

**Validations via l'outil `question`** (bloquant) : options cliquables
concrètes, jamais de prompt texte seul, **jamais** d'option « Ajuster » (la
saisie libre « Type your own answer » est ajoutée d'office) — chaque question
se termine par « Sinon « Type your own answer ». ». Présentations **compactes**
(tableaux courts, pas de paragraphes).

**Question 1 — Domaine métier** : « Que pilote ce dashboard ? » via l'outil
`question`, avec des domaines d'exemple cliquables (Ventes / E-commerce,
Finance & contrôle de gestion, RH & paie, Logistique & flotte, Production &
maintenance, Santé, Éducation, Énergie & utilities…) + saisie libre.

**Question 2 — Proposition globale unique** : je présente en une seule
proposition compacte, cohérente de bout en bout :
- **Schéma en étoile** : table de faits (`FAIT_X` — « 1 ligne = 1 événement
  daté »), **mesures** (2-3 max) avec unité et ordre de grandeur (« NB_KM,
  ~55 km par sortie »), saisonnalité/tendance si pertinentes, **dimensions**
  + cardinalités (≤ 40 modalités — limite de l'extracteur), **entité
  « personne »** nommée pour matcher la regex (`DIM_CLIENT`, `DIM_UTILISATEUR`,
  `DIM_EMPLOYE`… — requis pour les KPI « actifs »), tables catégorielles
  annexes éventuelles.
- **Arbre de navigation** : pages → sous-pages → KPIs (chaque KPI calculable
  depuis le schéma). Je décide seul : 3-5 KPIs par sous-page, ≤ 4 visuels par
  sous-page.
- **Couleurs secondaires + titre/sous-titre** : le Primary vient du client ;
  je propose les valeurs canoniques du mode (table ci-dessous), **chaque
  couleur nommée en clair** (« Surface : blanc pur `#FFFFFF` » — l'utilisateur
  valide des mots, pas des hex). Si le client impose ses secondaires, j'applique
  les règles de cohérence ci-dessous et propose une correction argumentée si
  ça jure. Titre et sous-titre déduits du domaine.

→ Une seule validation via l'outil `question` : **Valider** / **Version plus
riche** / **Version plus compacte** (+ saisie libre). En cas d'ajustement, je
re-présente uniquement la partie modifiée.

**Couleurs canoniques et cohérence** (mode dérivé de la luminance du Primary /
du canvas souhaité) :

| Champ | Mode clair | Mode sombre | Raison UX |
|---|---|---|---|
| Surface / Cards | `#FFFFFF` | `#1E293B` | les cartes « surgissent » du canevas |
| Canvas Background | `#F1F5F9` | `#0F172A` | fond neutre, jamais saturé |
| Card Frame Color | = Surface | = Surface | un seul réglage par défaut |
| Border / Divider | `#CBD5E1` | `#334155` | gris neutre visible mais doux |

Règles de cohérence (toute couleur imposée est testée) : Surface plus claire
que le Canvas (cartes invisibles sinon) ; Canvas peu saturé (≤ ~12 %) ; Border
gris désaturé (contraste vs Surface entre ~1,2 et ~2,0) ; Card Frame = Surface
sauf s'il contraste avec le Canvas. Le texte sur bandeau (`--on-primary`) est
dérivé automatiquement par `render.py` (WCAG AA) — un Primary clair n'est
jamais un problème.

## Phase 2 — Génération (CLIENT.md + data-spec.json + donnees.xlsx)

1. **J'écris `CLIENT.md`** complet (identité, couleurs validées, « Contexte &
   Données », arbre validé) et **`data-spec.json`** (schéma validé + un `seed`
   fixe — schéma : `clients/_template/data-spec.example.json`).
2. **Je génère les données** :
   ```bash
   python .opencode/skills/powerbi-prototype/scripts/generate-data.py clients/<client>/data-spec.json
   ```
   Le générateur écrit `donnees.xlsx` conforme **par construction** aux
   contraintes de l'extracteur (dates typées, PK 1re colonne unique, FK nommées
   comme les PK, cardinalités ≤ 40, entité personne bien nommée), sur les
   **2 années civiles closes** (en 2026 → 2024+2025).
3. **Auto-contrôle bloquant** : le générateur relance l'extracteur sur le
   fichier produit et compare au spec — toute divergence est bloquante
   (corriger le spec, relancer). Je présente le modèle détecté en une ligne.

## Phase 3 — Maquette & pitch (nav.json → build-views.py → render.py)

1. **J'écris `nav.json`** : l'arbre validé en Phase 1, en intentions courtes
   (schéma ci-dessous). C'est la **seule** chose que j'écris en Phase 3 —
   aucun HTML, aucun `views.json` à la main.
2. **Génération mécanique de `views.json`** :
   ```bash
   python .opencode/skills/powerbi-prototype/scripts/build-views.py <client>
   ```
   Il étend `nav.json` en `views.json` complet (dispatch KPI/visuels, donut
   ≤ 6 modalités sinon hbar top-10, humanisation, formats) et **valide chaque
   référence** contre les données (mesure/dimension/scalaire inconnu = erreur
   bloquante avec la liste des identifiants disponibles — corriger `nav.json`,
   relancer). Peut se chaîner avec `render.py` : `build-views.py <client>
   && render.py <client>` (render lance déjà le smoke test — ne pas le
   relancer à la main).
3. **Génération de la maquette** :
   ```bash
   python .opencode/skills/powerbi-prototype/scripts/render.py <client>
   ```
   Il parse `CLIENT.md` (couleurs, `--on-primary` WCAG), injecte DATA + SPEC
   dans le template, écrit `presentation/maquette.html` **puis lance le smoke
   test** (exit 0 exigé — toutes les sous-pages s'exécutent, chaque visuel
   initialisé et alimenté en données). Le logo est référencé via `../logo.png`.
4. **Boucle de validation avant pitch** — smoke test vert, je pose via l'outil
   `question` : *« La maquette est prête. Passer au pitch de présentation ?
   Sinon « Type your own answer » pour ajuster la maquette (elle sera
   régénérée). »* — option cliquable : **Génération de pitch.md**.
   - Ajustement en texte libre : je modifie `nav.json` (ou `CLIENT.md` /
     `data-spec.json` + régénération de `donnees.xlsx` si le modèle change),
     je relance `build-views.py` puis `render.py`, puis je **repose la même
     question**. On boucle jusqu'à « Génération de pitch.md ».
5. **Pitch du conseiller** :
   ```bash
   python .opencode/skills/powerbi-prototype/scripts/generate-pitch.py <client>
   ```
   Il écrit `presentation/pitch.md` : storytelling (ouverture, pages →
   sous-pages, clôture) limité aux KPI/visuels percutants (flag `pitch: true`
   dans nav.json, à défaut heuristique), valeurs réelles année N + variation
   vs N-1, transitions et durées.
6. J'indique l'ouverture : `start clients/<client>/presentation/maquette.html`
   (et la lecture de `presentation/pitch.md` avant de présenter).

**Cas « régénérer la maquette » (client existant)** : je réutilise `CLIENT.md`
+ `data-spec.json` existants (je régénère `donnees.xlsx` si le spec existe) ;
si `nav.json` existe je passe à l'étape 2, sinon je l'écris depuis l'arbre de
`CLIENT.md`.

## Schéma nav.json (complet — rien d'autre n'est supporté)

```json
{
  "labels": {"<clé brute des données>": "<libellé affiché (accents, casse)>"},
  "pages": [
    {"name": "…", "desc": "… (popover info ; {CUR_YEAR}/{PREV_YEAR} substitués)",
     "subs": [
       {"name": "…",
        "kpis": [
          {"type": "count",  "label": "…"},
          {"type": "sum",    "m": "MESURE", "label": "…", "fmt": "eur"},
          {"type": "active", "label": "…"},
          {"type": "ratio",  "num": "MESURE", "den": "_count", "label": "…", "fmt": "pct"},
          {"type": "scalar", "from": "NB_MA_DIM", "label": "…", "sub": "…"},
          {"type": "top",    "from": "MaDim", "label": "…"}
        ],
        "visuals": [
          {"type": "line",       "m": "MESURE", "title": "…"},
          {"type": "ratio-line", "num": "MESURE", "den": "_count", "title": "…"},
          {"type": "dim",   "dim": "MaDim", "m": "MESURE", "title": "…"},
          {"type": "cat",   "from": "MA_FEUILLE.MaColonne", "title": "…"},
          {"type": "stacked", "dim": "MaDim", "m": "MESURE", "title": "…"},
          {"type": "table", "dim": "MaDim", "m": "MESURE", "cols": ["AUTRE_MESURE"], "title": "…"}
        ]}
     ]}
  ]
}
```

- **KPI** : `count` (volume de la faits) · `sum` (mesure) · `active` (entités
  actives — requiert l'entité personne) · `ratio` (`den` : `_count` | `ACTIVE`
  | mesure | `SCALARS.x`) · `scalar` (statique, sans YoY) · `top` (valeur
  dominante d'une dim ou catégorie).
- **Visuels** : `dim`/`cat` → **donut si ≤ 6 modalités, sinon hbar top-10**
  (automatique ; override `"as": "donut"|"hbar"`, `"top"` réglable). `m`/
  `den` optionnels (défaut `_count`). `table` accepte `"cat"` au lieu de
  `"dim"`, et `"share": "NB_X"` ajoute une colonne « Part » en %.
- **Défauts automatiques** si absents : `label`/`title` humanisés (la map
  `labels` couvre les accents), `fmt`/`unit` inférés du nom de mesure
  (PCT/TAUX→pct, COUT/PRIX/MONTANT→eur, KM→km, DUREE/DELAI→dur, sinon int),
  `sub` standard (« en {CUR_YEAR} », « année {CUR_YEAR} »…).
- **`"pitch": true`** optionnel sur tout KPI/visuel = mis en avant dans
  `pitch.md`.
- **Bornes (bloquant côté build-views)** : 3-5 KPI et ≤ 4 visuels par
  sous-page (6 KPI max) ; toute référence inconnue = erreur listant les
  identifiants disponibles.
- Exemple complet : `clients/_template/nav.example.json`.

## Patterns réutilisables (assemblage, pas invention)

> La STRUCTURE d'une maquette est générique (schéma en étoile + catalogue de
> types KPI/visuels). Seul le CONTENU (mesures, dimensions, libellés, arbre,
> couleurs) est spécifique au client. Phase 2 = ASSEMBLER depuis cette section,
> jamais réinventer la structure.

### Checklist structurelle (toujours vraie)
- 1 faits `FAIT_*`, pk `ID_*`, date_col `DATE`, « 1 ligne = 1 événement daté ».
- Mesures : ≤ 3 additives (somme sensée) + au plus 1 mesure flag 0/1 PAR KPI
  de taux nécessaire.
- Dimensions : colonnes ≤ 40 modalités (viser 3-6 → donut) ; 1 feuille « personne »
  (regex client|utilisateur|employe|...) pour les KPI `active`.
- 1 `extra_sheet` si besoin d'un donut « statut » ET/OU de scalars hors-ligne
  (`AVG_<col>`).

### Catalogue de motifs (intention métier → recette)

| Intention | data-spec | nav.json |
|---|---|---|
| Volume | faits | `{type:"count"}` |
| Total d'une grandeur | mesure additive | `{type:"sum", m, fmt:auto}` |
| Moyenne / panier | mesure | `{type:"ratio", num:M, den:"_count", fmt:eur\|km}` |
| Taux / précision / respect | mesure 0/1 (avg ~p, std ~0.05, min 0) | `{type:"ratio", num:FLAG, den:"_count", fmt:"pct"}` |
| Coût par unité | 2 mesures (€ + volume) | `{type:"ratio", num:€, den:VOL, sub:"€/unité"}` |
| Actifs / entités servies | dim personne | `{type:"active"}` |
| Couverture / cardinalité | dim col | `{type:"scalar", from:"NB_<COL>"}` |
| Valeur dominante | dim col / cat | `{type:"top", from:"<Col>"}` ou `from:"CATEGORY_COUNTS.<SHEET>.<COL>"` |
| Répartition ≤ 6 | dim/cat | `{type:"dim"\|"cat"}` → donut auto |
| Répartition > 6 | dim | `{type:"dim", as:"hbar", top:10}` |
| Détail tabulaire | dim/cat + mesure | `{type:"table", dim\|cat, m?, cols?, share:"NB_<X>"}` |
| Évolution | mesure / flag | `{type:"line", m}` / `{type:"ratio-line", num, den}` |

Formats auto : PCT/TAUX→pct, COUT/PRIX/MONTANT→eur, KM→km, DUREE/DELAI→dur.

## Sources de données

- `CLIENT.md` — contrat de marque écrit par le skill (identité, couleurs,
  contexte, arbre) ; `render.py` n'y lit que l'identité et les couleurs.
- `data-spec.json` — spec de génération (écrit par le skill). Schéma :
  `clients/_template/data-spec.example.json`.
- `donnees.xlsx` — généré par `generate-data.py`. Contrat extrait : `FACTS` /
  `BY_DIM` / `DIM_COUNTS` / `CATEGORY_COUNTS` / `ACTIVE_MASKS` / `SCALARS` /
  `META`, grain mensuel (détaillé dans `references/TEMPLATE.md` — maintenance).
- `.data-cache.json` — cache du contrat DATA (partagé entre les scripts,
  invalidé automatiquement si le xlsx change). Ne pas l'éditer.
- `data-manifest.json` — optionnel : override de l'auto-détection de
  l'extracteur.
- `nav.json` — arbre de navigation en intentions (écrit par le skill).
- `views.json` — carte visuelle complète (**générée par `build-views.py`,
  jamais écrite à la main**). Schéma : `clients/_template/views.json`.
- `logo.png` — fourni par l'utilisateur (jamais créé par le skill). `bg.svg`/
  `bg.png` — optionnel (fond personnalisé).
- `presentation/maquette.html` — le rendu. `presentation/pitch.md` — script du
  conseiller.
- Modèle de départ : `clients/_template/`.

## Règles (tout le reste est garanti par les scripts et le template)

- **Données générées, jamais demandées (bloquant)** : l'utilisateur ne fournit
  que nom + logo + couleur primaire. Ne jamais réclamer un Excel.
- **Couleurs secondaires nommées en clair (bloquant)** : toute couleur proposée
  est accompagnée de son nom en toutes lettres, jamais d'un hex seul à valider.
- **Un KPI = une valeur parlante** : je choisis le chiffre unique que le
  libellé signifie (build-views.py fait le reste).
- **Formats `fmt`/`unit`** : `int | km | eur | f1 | dur | pct | text`.
- **Espacement : grille 8px stricte (bloquant)** : tout gap/padding/margin du
  template est un multiple de 8 (8/16/24) — le rythme structural est
  `var(--gap)` (= 16px). Si j'ajuste la maquette (boucle d'ajustement), je ne
  réintroduis **jamais** de valeur hors-grille (6, 10, 12, 14 px), ni le footer
  (supprimé) : la mention « Données fictives » reste dans l'infobulle
  (`.pop-note`, rendue par `renderInfo()`).
- **Aucune erreur JS tolérée (bloquant)** : le smoke test de `render.py` doit
  passer (exit 0) avant toute livraison — s'il échoue, je corrige `nav.json`
  (jamais le HTML) et je relance `build-views.py` + `render.py`.
