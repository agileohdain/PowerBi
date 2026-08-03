# PowerBi

Dépôt Power BI — génération de **maquettes dashboard haute-fidélité** pour
clients (pré-vente / démo).

## Contenu du dépôt

| Dossier          | Description                                                            |
| ---------------- | --------------------------------------------------------------------- |
| `clients/`       | **1 dossier par client** : `CLIENT.md` (à remplir), données, fond `bg`, maquette HTML |
| `powerpoint/`    | Template PowerPoint du fond (`Maquette Power BI.pptx`) + `export-bg.ps1` |
| `.opencode/`     | Skill opencode `powerbi-prototype` (génération des maquettes HTML)    |

---

## Workflow — créer une maquette pour un client

Le principe : **vous préparez tout en amont** (identité, navigation, fond
visuel), puis le skill génère la maquette en une seule passe — sans questions,
pour économiser les tokens.

### Étape 1 — Créer le dossier client

Dans l'explorateur de fichiers, **copiez le dossier `clients/_template/`** et
**renommez la copie** en `clients/<mon-client>/`.

Vous obtenez un dossier avec un `CLIENT.md` à remplir.

### Étape 2 — Remplir `CLIENT.md`

C'est le **seul fichier à éditer**. Il contient :
- L'identité de marque (nom)
- Les **couleurs** (voir tableau ci-dessous)
- Le **titre / sous-titre** du rapport
- L'**arbre de navigation** : pages → sous-pages → KPIs (avec flags `[En consolidation]`)

### Étape 3 — Personnaliser le fond visuel (PowerPoint)

Le visuel du bandeau / fond est authored dans PowerPoint, pas en CSS.

1. Dupliquer `powerpoint/Maquette Power BI.pptx` (ne pas modifier l'original).
2. Dans la copie : sélectionner la forme **« Banniere »** → changer sa couleur
   de remplissage (mettre la **même couleur que `Primary`** dans `CLIENT.md`).
3. Ajouter le **logo** du client dans la zone « Zone logo » (en haut à gauche).
4. Enregistrer la copie, par exemple `clients/<mon-client>/fond.pptx`.

### Étape 4 — Exporter le fond (`bg.svg`)

Dans PowerPoint, sur votre copie personnalisée :

1. **Sélectionnez tout** (Ctrl+A).
2. **Clic droit → Enregistrer en tant qu'image**.
3. Choisissez le format **SVG** et enregistrez sous
   `clients/<mon-client>/bg.svg`.

> **Pourquoi SVG ?** Vectoriel, donc toujours net (l'export PNG manuel de
> PowerPoint sort à basse résolution). Le **PNG est aussi accepté** (`bg.png`),
> et il est même **préférable si vous comptez réutiliser ce fond dans un vrai
> rapport Power BI Desktop** (Power BI gère mieux le raster en fond de canevas).
>
> Vous pouvez aussi **sauter cette étape** : le skill génère le fond
> automatiquement (en PNG, via `export-bg.ps1`) si `bg.svg`/`bg.png` est absent.

### Étape 5 — Lancer le skill opencode

```powershell
opencode
# puis dans opencode :
> Crée la maquette pour le client <mon-client>
```

Le skill :
1. Lit `CLIENT.md` (+ `bg.svg`/`bg.png`).
2. Si pas de `donnees.xlsx` : génère un Excel fictif réaliste + `DATA.md`.
3. Si pas de `bg.*` : génère le fond automatiquement (`export-bg.ps1`).
4. Génère `clients/<mon-client>/maquette/index.html` (canevas 1920×1080,
   `bg.*` en fond, KPIs et graphiques ECharts par-dessus).

Ouvrez `clients/<mon-client>/maquette/index.html` dans un navigateur.

---

## Variables de marque (`CLIENT.md` → CSS `:root`)

| Variable      | Rôle                                                        |
| ------------- | ----------------------------------------------------------- |
| `--primary`   | Bandeau, "Filtres" + icône, onglets actifs, série principale |
| `--surface`   | Zone logo, texte sur primaire                               |
| `--canvas`    | Fond du canevas (couleur)                                   |
| `--card-bg`   | Couleur des encadrés / cards                                |
| `--border`    | Bordures, séparateurs                                       |

> **Important** : la couleur du bandeau dans le `.pptx` (étape 3) **doit être la
> même** que `--primary` dans `CLIENT.md` — le skill l'utilise pour les graphiques
> et onglets, qui doivent visuellement matcher le bandeau.

---

## Exemple : `clients/veloh/`

Client complet (flotte cyclable, thème sombre) :
`CLIENT.md`, `DATA.md`, `donnees.xlsx`, `logo.png`, `bg.png`, et la maquette
`maquette/index.html`.

---

## Prise en main (Git)

```bash
gh repo clone agileohdain/PowerBi
```

> Un clone est une **copie locale en lecture seule** : votre collègue ne peut
> pas modifier votre dépôt GitHub sans que vous l'ajoutiez comme **collaborateur**
> (accès en écriture). Sans ça, il contribue via un **fork + pull request**.
> Note : ce dépôt est **public** → tout son contenu (et l'historique) est lisible
> par tous. Passez-le en **Privé** (*Settings → Danger Zone*) pour restreindre.

### Workflow Git usuel
```bash
git add .                          # indexer les modifications
git commit -m "message explicite"  # créer un commit
git push origin main               # envoyer vers GitHub
```

### Conventions de commit
- Messages en français, à l'infinitif : `Ajoute maquette client acme`
- Un commit = un changement logique

## Auteur

[agileohdain](https://github.com/agileohdain)
