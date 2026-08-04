# PowerBi

Dépôt Power BI — génération de **maquettes dashboard haute-fidélité** pour
clients (pré-vente / démo).

## Contenu du dépôt

| Dossier          | Description                                                            |
| ---------------- | --------------------------------------------------------------------- |
| `clients/`       | **1 dossier par client** : `CLIENT.md` (à remplir), logo, données, `bg.*` optionnel, maquette HTML |
| `clients/_template/` | Dossier modèle à copier pour créer un nouveau client              |
| `.opencode/`     | Skill opencode `powerbi-prototype` (génération des maquettes HTML)    |

---

## Workflow — créer une maquette pour un client

Dans opencode, lancez la **commande `/maquette`** suivie du nom du client :

```powershell
opencode
# puis dans opencode :
> /maquette MonClient
```

Le skill déroule alors le processus :
1. Le **nom du client est passé en argument** de `/maquette` (la **casse est
   conservée telle quelle** ; si aucun nom n'est fourni, il vous le demande, et
   il **ne propose pas de nom**).
2. Il **confirme le nom** — « Est-ce bien le client « MonClient » ? — **Oui /
   Modifier** » — et n'avance que si le nom est validé.
3. Si `clients/<nom>/` **existe déjà**, il vous demande de choisir :
   **régénérer** la maquette de ce client, ou **modifier le nom**.
4. S'il détecte que vous êtes en mode **PLAN**, il vous demande de passer en
   mode **BUILD** (créer le dossier nécessite d'écrire sur le disque) — une
   seule fois, sans retour PLAN par la suite.
5. Il **crée automatiquement** le dossier `clients/<client>/` avec `CLIENT.md`
   (nom pré-rempli) — **il ne crée aucun logo**.
6. Il vous demande de **déposer** dans `clients/<client>/` :
   - le **logo** `logo.png` (idéalement **fond transparent**) ;
   - les **données** `donnees.xlsx` (feuilles = tables) ;
   - le **`CLIENT.md` rempli** (voir « Remplir `CLIENT.md` » ci-dessous).
7. Il **parcourt `CLIENT.md`** : si une information n'est **pas renseignée**
   (encore sous forme `<...>`), ou si le logo / les données manquent, il
   **s'arrête** et vous demande de saisir **précisément** les informations
   manquantes. Il re-vérifie en boucle jusqu'à ce que tout soit complet.
8. Il déduit de `donnees.xlsx` le modèle de données, les formules KPI et la
   carte visuelle, puis **génère** `clients/<client>/maquette/index.html`
   (canevas 1920×1080, bandeau/fond en CSS, KPIs et graphiques ECharts
   par-dessus). Ouvrez ce fichier dans un navigateur.

La maquette générée est **interactive** :
- **Panneau de filtres fonctionnel** — année (chiclets), trimestre et mois
  (dropdowns), plage de dates (slider + champs synchronisés), bouton « Effacer »
  ; chaque changement recalcule les KPIs et re-rend les visuels, avec un badge
  « Filtres actifs ».
- **Variation vs N-1** sur chaque KPI temporel, sur toutes les pages (badge
  vert/rouge calculé sur périodes comparables).
- **Icône info** en haut à droite du bandeau : au survol, une infobulle décrit
  la page active et la sous-page sélectionnée.

Il n'y a **pas** de mode « Téléguidé » : `CLIENT.md` est **toujours rempli par
vous** ; le skill se contente de le vérifier et de demander les champs
manquants.

Les **données** (`donnees.xlsx`) sont **toujours fournies par vous** — le skill
ne génère pas de données fictives. Elles vivent **uniquement** dans
`donnees.xlsx` ; le skill s'appuie sur l'Excel seul, sans fichier de glossaire
séparé.

> **Création manuelle (alternative sans opencode)** : dans l'explorateur de
> fichiers, **copiez le dossier `clients/_template/`** et **renommez la copie**
> en `clients/<mon-client>/`, puis suivez les étapes ci-dessous.

### Remplir `CLIENT.md`

C'est le **seul fichier à éditer**. Il contient :
- L'identité de marque (nom)
- Les **couleurs** (voir tableau ci-dessous)
- Le **titre / sous-titre** du rapport
- L'**arbre de navigation** : pages → sous-pages → KPIs (avec flags `[En consolidation]`)

Remplissez **toute** valeur entre `<...>` (ex. `<Primary>`, `<Surface>`,
`<Canvas Background>`, `<Titre du rapport>`, `<Titre sous-page>`,
`<Libellé KPI>`). Si un champ reste non renseigné, le skill l'identifie et
s'arrête pour vous le demander.

### Déposer le logo et les données

Déposez dans `clients/<mon-client>/` :
- le **logo** `logo.png` (idéalement **fond transparent**) — affiché dans la
  zone logo du bandeau ;
- les **données** `donnees.xlsx` (feuilles = tables).

> **Optionnel — fond PowerPoint** : le bandeau et le fond sont **dessinés en
> CSS** par le skill. Si vous préférez un fond personnalisé authored dans
> PowerPoint, ouvrez `Maquette Power BI.pptx`, ajustez la forme « Banniere »
> (même couleur que `Primary`) puis **exportez** : tout sélectionner (Ctrl+A) →
> **clic droit → Enregistrer en tant qu'image** → dossier
> `clients/<mon-client>/`, nom **`bg`**, format **SVG** (PNG accepté). Si un
> `bg.*` est présent, il est utilisé en priorité sur le rendu CSS.

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
