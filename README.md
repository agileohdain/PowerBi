# PowerBi — Maquettes dashboard en minutes, pas en heures

Produisez une **maquette Power BI haute-fidélité** à partir de **trois éléments**
— un logo, un fichier Excel, un `CLIENT.md` rempli — et ouvrez un dashboard
interactif dans votre navigateur. Pas de Power BI Desktop, pas de licence, pas
de rendering manuel : le skill génère un `index.html` auto-suffisant (canevas
16:9, bandeau aux couleurs du client, KPIs et graphiques ECharts) prêt à montrer
en pré-vente ou en démo.

> **Le problème résolu** : un client veut « voir à quoi ça ressemblerait ».
> Avant, on ouvrait PowerPoint. Maintenant, on dépose un logo + un Excel, on
> remplit un seul fichier texte, et on obtient un dashboard navigable avec
**filtres, variation vs N-1, et arbre de navigation à deux niveaux**.

---

## Quickstart — 3 étapes

```powershell
opencode
# puis dans opencode :
> /maquette MonClient
```

1. **`/maquette <Nom>`** — le skill crée `clients/MonClient/` avec un
   `CLIENT.md` pré-rempli du nom.
2. **Déposez** dans ce dossier : `logo.png` (fond transparent),
   `donnees.xlsx` (les données source), et **éditez `CLIENT.md`** (couleurs,
   titre, arbre de navigation). Le skill s'arrête et vous réclame exactement ce
   qui manque tant que tout n'est pas complet et cohérent.
3. **`start clients/MonClient/maquette/index.html`** — le dashboard s'ouvre
   dans le navigateur. Fait.

> Le skill **ne génère jamais** les données ni le logo — vous les fournissez.
> Il ne **lit jamais** la maquette d'un autre client : chaque dashboard est
> construit depuis les specs + votre `CLIENT.md` + votre Excel.

---

## Ce que vous obtenez

Un fichier **`maquette/index.html`** unique, ouvert dans n'importe quel
navigateur, qui rend fidèlement le langage visuel Power BI :

- **Canevas 1920×1080** (16:9, slide PowerPoint) qui se scale au viewport —
  pas de scrollbars, pas de déformation.
- **Bandeau + zone logo en trapèzes** (CSS, aux couleurs exactes du client)
  avec la cassure diagonale signature du template.
- **KPIs temporels avec variation N vs N-1** — chaque indicateur dérivé de la
  série temporelle affiche sa valeur de l'année N **et** son badge
  `±x,x % vs 2024` (vert/rouge/neutre, calculé sur mois comparables).
- **Panneau de filtres interactif** — année (chiclets), trimestre (chiclets),
  mois (dropdown), plage de dates (slider + champs synchronisés), un slicer par
  dimension du modèle. Les clics réagissent et affichent un badge
  « ● Filtres actifs », mais **les visuels montrent toujours l'année N** : la
  maquette reste lisible, pas un tableau figé.
- **Navigation à deux niveaux** : pills L1 + liens L2, chaque sous-page a son
  propre layout (KPIs + visuels). Une **icône info** en haut à droite ouvre un
  popover décrivant la page active et permettant de sauter à une sous-page.
- **Visuels ECharts** : lignes N-vs-N-1 (axe Jan→Déc fixe), donuts (≤6
  tranches), barres horizontales (top-10 + « Autres »), tables de détail,
  multi-séries par dimension. Palette catégorielle **dérivée du primaire** —
  jamais d'arc-en-ciel.
- **KPIs « en consolidation »** signalés par un pill ambre discret (pas de
  rouge qui hurle « faute »).

---

## Garde-fous qualité (automatiques)

Le skill **refuse de livrer une maquette cassée** :

- **Smoke test JS** (`scripts/smoke-test.js`) exécuté avant chaque livraison :
  il parcourt toutes les sous-pages, vérifie qu'aucune erreur JS n'est levée et
  que chaque visuel reçoit bien son `echarts.init`. **Exit code 0 obligatoire**.
- **Cohérence des couleurs vs `Primary`** : si vous ne donnez que la couleur
  principale (cas le plus fréquent), le skill propose les couleurs secondaires
  canoniques (mode clair/sombre) et corrige toute incohérence (surface plus
  sombre que le canevas, bordure couleur de marque, canevas saturé…). Bloquant
  jusqu'à acceptation.
- **Contraste WCAG AA** : le texte sur le bandeau est dérivé automatiquement
  (`--on-primary`) selon la luminance du `Primary` — un primaire clair (taupe,
  jaune) ne rend jamais le titre illisible.
- **Données au grain mensuel** embarquées dans le HTML : l'année N et la
  variation vs N-1 sont toujours calculées sur **mois comparables** (jamais une
  année partielle contre une complète).

---

## Anatomie d'un dossier client

```
clients/MonClient/
├── CLIENT.md          ← le SEUL fichier à éditer (identité, couleurs, navigation)
├── logo.png           ← fourni par vous (fond transparent)
├── donnees.xlsx       ← fourni par vous (feuilles = tables)
├── bg.svg             ← optionnel : fond personnalisé (any source, ~3840×2160)
└── maquette/
    └── index.html     ← généré par le skill (auto-suffisant)
```

Le dossier modèle à copier est `clients/_template/`.

---

## Remplir `CLIENT.md`

C'est **le seul fichier à éditer**. Il contient :

- **Identité** : `Brand Name`, `Report Title`, `Report Subtitle`.
- **Couleurs** : `Primary` (obligatoire) + `Surface`/`Canvas`/`Card Frame`/`Border`
  (le skill propose des canoniques si elles manquent ou jurent).
- **Arbre de navigation** : pages → sous-pages → KPIs (avec flags
  `[En consolidation]`).

Remplissez **toute** valeur entre `<...>`. Si un champ reste vide, le skill
l'identifie, s'arrête, et vous le demande précisément — il re-vérifie en boucle.

### Variables de marque (`CLIENT.md` → CSS `:root`)

| Variable      | Rôle                                                        |
| ------------- | ----------------------------------------------------------- |
| `--primary`   | Bandeau (CSS), "Filtres" + icône, onglets actifs, série principale |
| `--surface`   | Zone logo, cards, pane filtres                              |
| `--canvas`    | Fond du canevas (couleur)                                   |
| `--card-bg`   | Couleur des encadrés / cards                                |
| `--border`    | Bordures, séparateurs                                       |

> Le bandeau est dessiné en CSS avec `--primary`. Si vous fournissez un fond
> `bg.*` (optionnel), la couleur du bandeau de l'image **doit être la
> même** que `--primary`. Les couleurs de texte sont dérivées automatiquement
> selon la luminance du canvas.

---

## Workflow détaillé (référence)

Pour le détail, voici ce que le skill déroule lors de `/maquette <Nom>` :

1. Le **nom est passé en argument** (la casse est conservée ; si absent, il
   vous le demande, **sans proposer de nom**).
2. Il **confirme** : « Est-ce bien le client « X » ? — Oui / Modifier ».
3. Si `clients/<nom>/` **existe déjà**, il demande : régénérer, ou modifier le
   nom.
4. Il **crée** le dossier + `CLIENT.md` (nom pré-rempli), **sans logo**.
5. Il vous demande de **déposer** `logo.png`, `donnees.xlsx`, et le `CLIENT.md`
   rempli.
6. Il **parcourt `CLIENT.md`** : arrêt + demande précise des champs manquants
   (identité, navigation, logo, données) **et** des couleurs incohérentes.
   Boucle jusqu'à complétude et cohérence.
7. Il **extrait le modèle** de `donnees.xlsx` (`scripts/extract-data.py`,
   auto-détection de la table de faits, mesures, dimensions, masques d'activité)
   et **génère** `maquette/index.html`.
8. Il **valide** par le smoke test (exit 0) et vous indique comment ouvrir.

---

## Prise en main (Git)

```bash
gh repo clone agileohdain/PowerBi
```

> Un clone est une **copie locale en lecture seule** : votre collègue ne peut
> pas modifier le dépôt sans être ajouté comme **collaborateur** (accès en
> écriture). Sinon, contribution via **fork + pull request**. Ce dépôt est
> **public** → tout son contenu (et l'historique) est lisible par tous ;
> passez-le en **Privé** (*Settings → Danger Zone*) pour restreindre.

### Workflow Git usuel

```bash
git add .                          # indexer les modifications
git commit -m "message explicite"  # créer un commit
git push origin main               # envoyer vers GitHub
```

### Conventions de commit

- Messages en français, à l'infinitif : `Ajoute maquette client acme`.
- Un commit = un changement logique.

---

## Auteur

[agileohdain](https://github.com/agileohdain)
