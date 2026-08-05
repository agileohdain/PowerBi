# PowerBi — Maquettes dashboard en minutes, pas en heures

Produisez une **maquette Power BI haute-fidélité** à partir de **trois choses**
— un **nom**, un **logo**, une **couleur primaire** — et ouvrez un dashboard
interactif dans votre navigateur. Pas de Power BI Desktop, pas de licence, pas
de données à préparer : le skill vous **télé-guide par questionnaire** (il
propose, vous validez), **génère les données fictives** lui-même, puis produit
un `index.html` auto-suffisant (canevas 16:9, bandeau aux couleurs du client,
KPIs et graphiques ECharts) prêt à montrer en pré-vente ou en démo.

> **Le problème résolu** : un client veut « voir à quoi ça ressemblerait ».
> Avant, on ouvrait PowerPoint. Maintenant, on donne un nom, un logo et une
> couleur, on répond à quelques questions, et on obtient un dashboard navigable
> avec **filtres, variation vs N-1, et arbre de navigation à deux niveaux**.

---

## Quickstart — 4 étapes

```powershell
opencode
# puis dans opencode :
> /maquette MonClient
```

1. **`/maquette <Nom>`** — le skill confirme le nom (casse exacte) et crée
   `clients/MonClient/`.
2. **Fournissez** : `logo.png` (fond transparent, déposé dans le dossier) **et
   la couleur primaire** en hexadécimal (ex. `#00A1B1`).
3. **Répondez au questionnaire guidé** — le skill propose, vous validez ou
   ajustez : domaine métier → modèle de données → arbre de navigation + KPIs →
   couleurs secondaires (nommées en clair : « blanc pur `#FFFFFF` », « gris
   bleuté très clair `#F1F5F9` »…) → titre. Les **données fictives sont générées
   par le skill** (2 années civiles complètes, ex. 2024–2025).
4. **`start clients/MonClient/maquette/index.html`** — le dashboard s'ouvre
   dans le navigateur. Fait.

> Le skill **génère toujours** les données (`donnees.xlsx`) à partir de vos
> réponses — vous ne fournissez jamais de fichier de données. Il ne crée
> **jamais** le logo, et ne **lit jamais** la maquette d'un autre client.

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
  « ● Filtres actifs », mais **les visuels montrent toujours l'année N**.
- **Navigation à deux niveaux** : pills L1 + liens L2, chaque sous-page a son
  propre layout (KPIs + visuels). Une **icône info** en haut à droite ouvre un
  popover décrivant la page active et permettant de sauter à une sous-page.
- **Visuels ECharts** : lignes N-vs-N-1 (axe Jan→Déc fixe), donuts (≤6
  tranches), barres horizontales (top-10 + « Autres »), tables de détail.
  Palette catégorielle **dérivée du primaire** — jamais d'arc-en-ciel.
- **Données fictives réalistes** : saisonnalité, tendance annuelle, entités
  actives suivies mois par mois — le footer l'indique (« Données fictives »).

---

## Garde-fous qualité (automatiques)

Le skill **refuse de livrer une maquette cassée** :

- **Smoke test JS** (`scripts/smoke-test.js`) exécuté avant chaque livraison :
  il parcourt toutes les sous-pages, vérifie qu'aucune erreur JS n'est levée,
  que chaque visuel reçoit son `echarts.init` **et qu'aucun visuel n'est vide
  de données**. **Exit code 0 obligatoire**.
- **Données conformes par construction** : le générateur
  (`scripts/generate-data.py`) écrit un Excel que l'extracteur comprend à coup
  sûr (dates typées, clés cohérentes, cardinalités maîtrisées), puis
  **s'auto-contrôle** en relançant l'extracteur — toute divergence est
  bloquante.
- **Cohérence des couleurs vs `Primary`** : vous ne donnez que la couleur
  principale ; le skill propose les secondaires canoniques (mode clair/sombre)
  **nommées en clair**, et corrige toute incohérence.
- **Contraste WCAG AA** : le texte sur le bandeau est dérivé automatiquement
  (`--on-primary`) selon la luminance du `Primary` — un primaire clair (taupe,
  jaune) ne rend jamais le titre illisible.
- **Données au grain mensuel** : l'année N (complète) et la variation vs N-1
  sont calculées sur **mois comparables**.

---

## Anatomie d'un dossier client

```
clients/MonClient/
├── CLIENT.md            ← écrit par le skill (identité, couleurs, contexte, navigation)
├── data-spec.json       ← écrit par le skill (spec de génération des données)
├── donnees.xlsx         ← GÉNÉRÉ par le skill (2 années civiles closes)
├── logo.png             ← fourni par vous (fond transparent) — SEUL fichier déposé
├── bg.svg               ← optionnel : fond personnalisé (~3840×2160)
├── views.json           ← carte visuelle déclarative (brouillon auto + raffinement)
└── maquette/
    └── index.html       ← généré par le skill (auto-suffisant)
```

Le dossier modèle est `clients/_template/`.

---

## Le questionnaire guidé (ce qu'on vous demande — et ce qu'on ne vous demande pas)

Après le logo et la couleur primaire, le skill déroule **4 questions** :

1. **Domaine métier** — « Que pilote ce dashboard ? » (une phrase suffit).
2. **Modèle de données proposé** — table de faits, mesures (unités, ordres de
   grandeur), dimensions, volumes. Vous validez ou ajustez.
3. **Arbre de navigation + KPIs proposés** — pages, sous-pages, indicateurs.
   Vous validez, ajustez en texte libre, ou demandez une version plus
   riche/compacte.
4. **Couleurs secondaires + titre proposés** — chaque couleur est nommée en
   clair (« blanc pur », « gris ardoise »…), pas seulement en hex.

Le skill décide seul de tout le reste : formules des KPIs, types de visuels,
disposition, badges de variation, palette harmonisée.

### Variables de marque (`CLIENT.md` → CSS `:root`)

| Variable      | Rôle                                                        |
| ------------- | ----------------------------------------------------------- |
| `--primary`   | Bandeau (CSS), "Filtres" + icône, onglets actifs, série principale |
| `--surface`   | Zone logo, cards, pane filtres                              |
| `--canvas`    | Fond du canevas (couleur)                                   |
| `--card-bg`   | Couleur des encadrés / cards                                |
| `--border`    | Bordures, séparateurs                                       |

> Le bandeau est dessiné en CSS avec `--primary`. Si vous fournissez un fond
> `bg.*` (optionnel), la couleur du bandeau de l'image **doit être la même**
> que `--primary`. Les couleurs de texte sont dérivées automatiquement selon
> la luminance du canvas.

---

## Workflow détaillé (référence)

Pour le détail, voici ce que le skill déroule lors de `/maquette <Nom>` :

1. Le **nom est passé en argument** (casse conservée ; si absent, il le
   demande, **sans proposer de nom**).
2. Il **confirme** : « Est-ce bien le client « X » ? — Oui / Modifier ».
3. Si `clients/<nom>/` **existe déjà**, il demande : régénérer (réutilise les
   specs existants), refaire le questionnaire, ou modifier le nom.
4. Il **crée** le dossier + `CLIENT.md` (nom pré-rempli), **sans logo**.
5. Il réclame **le logo** et **la couleur primaire** (hex).
6. Il déroule le **questionnaire guidé** (domaine → modèle → navigation →
   couleurs/titre), avec validation à chaque étape.
7. Il **écrit** `CLIENT.md` + `data-spec.json`, **génère** `donnees.xlsx`
   (`scripts/generate-data.py`) et vérifie le modèle détecté par
   `scripts/extract-data.py` (auto-contrôle bloquant).
8. Il **génère** `maquette/index.html` (`scripts/render.py`) et **valide** par
   le smoke test (exit 0), puis indique comment ouvrir le rendu.

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
