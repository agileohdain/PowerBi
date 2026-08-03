# PowerBi

Dépôt Power BI — génération de **maquettes dashboard haute-fidélité** pour
clients (pré-vente / démo).

## Contenu du dépôt

| Dossier          | Description                                                            |
| ---------------- | --------------------------------------------------------------------- |
| `clients/`       | **1 dossier par client** : `CLIENT.md` (à remplir), `.pptx` du fond, `bg.*`, maquette HTML |
| `.opencode/`     | Skill opencode `powerbi-prototype` (génération des maquettes HTML)    |

---

## Workflow — créer une maquette pour un client

Le skill propose **deux modes** au lancement (dans opencode) :

```powershell
opencode
# puis dans opencode :
> Crée la maquette pour le client <mon-client>
```

1. **Téléguidé** — le skill vous pose toutes les questions (nom du client,
   couleurs avec thèmes préréglés, titre/sous-titre, arbre de navigation
   pages → sous-pages → KPIs avec flags consolidation), écrit `CLIENT.md` pour
   vous, crée (si besoin) les données fictives, puis génère la maquette.
2. **Personnaliser vous-même** — vous préparez tout en amont (étapes 1 à 3
   ci-dessous), puis le skill génère la maquette en une seule passe.

Dans les deux cas, il vous sera aussi demandé si vous **avez déjà les données**
(`donnees.xlsx`) ou si le skill doit les **créer pour vous** (jeu fictif
réaliste). Les données vivent **uniquement** dans `donnees.xlsx` — le skill
s'appuie sur l'Excel seul, sans fichier de glossaire séparé.

### Mode Personnaliser — préparation manuelle

#### Étape 1 — Créer le dossier client

Dans l'explorateur de fichiers, **copiez le dossier `clients/_template/`** et
**renommez la copie** en `clients/<mon-client>/`.

#### Étape 2 — Remplir `CLIENT.md`

C'est le **seul fichier à éditer**. Il contient :
- L'identité de marque (nom)
- Les **couleurs** (voir tableau ci-dessous)
- Le **titre / sous-titre** du rapport
- L'**arbre de navigation** : pages → sous-pages → KPIs (avec flags `[En consolidation]`)

#### Étape 3 — Déposer le logo

Déposez le **logo du client** dans `clients/<mon-client>/logo.png` (idéalement
**fond transparent**). Le skill l'affiche dans la zone logo du bandeau.

> **Optionnel — fond PowerPoint** : le bandeau et le fond sont désormais
> **dessinés en CSS** par le skill. Si vous préférez un fond personnalisé
> authored dans PowerPoint, ouvrez `Maquette Power BI.pptx`, ajustez la forme
> « Banniere » (même couleur que `Primary`) puis **exportez** : tout sélectionner
> (Ctrl+A) → **clic droit → Enregistrer en tant qu'image** → dossier
> `clients/<mon-client>/`, nom **`bg`**, format **SVG** (PNG accepté). Si un
> `bg.*` est présent, il est utilisé en priorité sur le rendu CSS.

### Génération

Le skill :
1. Pose les questions d'ouverture (mode + données).
2. Lit (ou écrit, en mode Téléguidé) `CLIENT.md`.
3. Si pas de `donnees.xlsx` et création demandée : génère un Excel fictif
   réaliste.
4. Déduit de `donnees.xlsx` le modèle de données, les formules KPI et la carte
   visuelle, puis génère `clients/<mon-client>/maquette/index.html` (canevas
   1920×1080, bandeau/fond en CSS, KPIs et graphiques ECharts par-dessus).

Ouvrez `clients/<mon-client>/maquette/index.html` dans un navigateur.

---

## Variables de marque (`CLIENT.md` → CSS `:root`)

| Variable      | Rôle                                                        |
| ------------- | ----------------------------------------------------------- |
| `--primary`   | Bandeau (CSS), "Filtres" + icône, onglets actifs, série principale |
| `--surface`   | Zone logo, texte sur primaire                               |
| `--canvas`    | Fond du canevas (couleur)                                   |
| `--card-bg`   | Couleur des encadrés / cards                                |
| `--border`    | Bordures, séparateurs                                       |

> Le bandeau est dessiné en CSS avec `--primary`. Si vous fournissez un fond
> `bg.*` (optionnel), la couleur du bandeau dans le `.pptx` **doit être la
> même** que `--primary` pour que graphiques et onglets matchent le bandeau.
> Les couleurs de texte (`--text-primary` / `--text-secondary`) sont dérivées
> automatiquement selon la luminance du canvas.

---

## Exemple : `clients/veloh/`

Client complet (flotte cyclable, thème sombre) :
`CLIENT.md`, `donnees.xlsx`, `logo.png`, `bg.png`, et la maquette
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
