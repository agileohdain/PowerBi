# Dossier template

Ce dossier sert de modèle au skill `powerbi-prototype` : c'est lui qui crée et
remplit `clients/<mon-client>/` pendant la commande `/maquette <Nom>`.
**Vous n'avez rien à copier ni à éditer à la main.**

Contenu du template :

- `CLIENT.md` — **écrit par le skill** à partir de vos réponses au
  questionnaire guidé (identité, couleurs, contexte & données, arbre de
  navigation). Vous ne le remplissez pas.
- `views.json` — schéma de la carte visuelle déclarative (pages → sous-pages →
  KPIs + visuels), raffiné par le skill après génération d'un brouillon.
- `data-spec.example.json` — exemple documenté du spec de génération des
  données (lu par `scripts/generate-data.py`).
- `bg.svg` (ou `bg.png`) — **optionnel** : si vous déposez une image de fond
  personnalisée (~3840×2160), elle est appliquée sur le canevas à la place du
  bandeau/fond dessinés en CSS. Sa couleur de bandeau **doit valoir**
  `Primary` pour que graphiques et onglets matchent.

Procédure complète : voir le README.md à la racine du dépôt.

Fichier déposé par l'utilisateur (le skill ne le crée jamais) :
- `logo.png` — le logo du client (fond transparent)

Fichiers produits par le skill (ne pas créer à la main) :
- `CLIENT.md` et `data-spec.json` — écrits après le questionnaire guidé
- `donnees.xlsx` — **données fictives générées** (2 années civiles closes)
- `views.json` — carte visuelle raffinée
- `presentation/maquette.html` — la maquette, **interactive** : panneau de
  filtres fonctionnel (année, trimestre, mois, plage de dates, bouton
  Réinitialiser) et KPIs temporels avec **variation vs N-1**.
- `presentation/pitch.md` — **script du conseiller** (storytelling + chiffres
  réels), généré par `generate-pitch.py` à la fin de la Phase 3.
