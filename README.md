# PowerBi

Dépôt d'apprentissage Power BI — rapports, sources de données Excel et tutoriels.

## Contenu du dépôt

| Dossier      | Description                                                   |
| ------------ | ------------------------------------------------------------- |
| `rapports/`  | Projets Power BI au format **PBIP** (Power BI Project)        |
| `excel/`     | Fichiers Excel utilisés comme sources de données             |
| `tutoriels/` | Notes, guides et exercices d'apprentissage                   |

## Prise en main

### 1. Cloner le dépôt
```bash
gh repo clone agileohdain/PowerBi
```

### 2. Activer le format PBIP dans Power BI Desktop
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
