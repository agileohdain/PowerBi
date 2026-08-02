# PowerBi

Dépôt Power BI — génération de **maquettes dashboard haute-fidélité** pour
clients (pré-vente / démo) + apprentissage (rapports PBIP, Excel, tutoriels).

## Contenu du dépôt

| Dossier          | Description                                                              |
| ---------------- | ----------------------------------------------------------------------- |
| `.opencode/`     | **Skill opencode `powerbi-prototype`** (génération de maquettes HTML)   |
| `brands/`        | Identité par client (`CLIENT.md`, `DATA.md`, logo, Excel, Output)       |
| `mockups/`       | Maquettes HTML générées (1 sous-dossier par client)                     |
| `rapports/`      | Projets Power BI au format **PBIP** (Power BI Project)                  |
| `excel/`         | Fichiers Excel utilisés comme sources de données                        |
| `tutoriels/`     | Notes, guides et exercices d'apprentissage                              |

---

## Skill `powerbi-prototype` — maquettes Power BI en HTML

Génère des dashboards Power BI en HTML/ECharts **auto-suffisants** (ouvrables
dans un navigateur), re-skinables par client via des variables CSS.

### Pré-requis
- [opencode](https://opencode.ai) installé
- Le skill est déclaré dans `opencode.json` (`skills.paths: [".opencode/skills"]`)

### Utilisation
1. Démarrer opencode à la racine du dépôt.
2. Lancer le skill, par exemple :
   > *"Crée une maquette Power BI pour le client acme-commerce"*
3. Le skill enchaîne **3 phases guidées** :
   - **Brief** : nom, secteur, couleurs (primaire, fond, encadrés), image de fond,
     logo, arbre de navigation, KPIs.
   - **Données** : génère un Excel fictif réaliste + un `DATA.md` (modèle,
     formules, carte visuelle), affiné par 2-3 questions.
   - **Maquette** : produit `mockups/<client>/index.html` (canevas 1920×1080,
     ECharts, navigation 2-niveaux, footer "données fictives").
4. Ouvrir `mockups/<client>/index.html` dans un navigateur.

### Exemple de référence
`brands/veloh/` — client complet (cycling fleet) avec :
`CLIENT.md`, `DATA.md`, `donnees.xlsx`, `logo.png`, et le rendu
`Output/veloh-dashboard.html`.

### Variables de marque (`CLIENT.md` → CSS `:root`)
| Variable      | Rôle                                                    |
| ------------- | ------------------------------------------------------- |
| `--primary`   | Header banner, "Filtres" + icône, onglets actifs, série |
| `--surface`   | Zone logo, texte sur primaire                           |
| `--canvas`    | Fond du canevas (couleur)                               |
| `--card-bg`   | Couleur des encadrés / cards                            |
| `--bg-image`  | Image de fond optionnelle (`url(...)` ou `none`)        |
| `--border`    | Bordures, séparateurs                                   |

Voir `.opencode/skills/powerbi-prototype/references/POWERBI_LAYOUT.md` §6 pour
le contract complet.

---

## Prise en main (Git)

### 1. Cloner le dépôt
```bash
gh repo clone agileohdain/PowerBi
```

### 2. Activer le format PBIP dans Power BI Desktop (pour les rapports .pbip)
`File` → `Options and settings` → `Options` → `Preview features`
→ cocher **Power BI Project (.pbip) save option**.

### 3. Workflow Git usuel
```bash
git add .                          # indexer les modifications
git commit -m "message explicite"  # créer un commit
git push origin main               # envoyer vers GitHub
```

## Format PBIP — pourquoi ?

Le format **PBIP** sauvegarde un rapport sous forme de **dossier** contenant des fichiers
JSON/XML lisibles. Cela permet à Git de :
- afficher les **différences** entre versions,
- suivre l'historique des modifications du modèle et des visuels,
- faciliter la **collaboration** (revue de code, merge).

> Le format `.pbix` classique est binaire : Git ne peut pas afficher les différences.

## Conventions de commit

- Messages en français, à l'infinitif : `Ajoute rapport ventes 2024`
- Un commit = un changement logique (ne pas mélanger sujets)

## Auteur

[agileohdain](https://github.com/agileohdain)
