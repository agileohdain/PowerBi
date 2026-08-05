# Dossier template

Copiez ce dossier dans l'explorateur de fichiers et renommez la copie pour créer
un nouveau client (`clients/<mon-client>/`).

Contenu du template :

- `CLIENT.md` — **le seul fichier à éditer** (identité, couleurs, navigation,
  KPIs). Remplissez **toute** valeur `<...>` : le skill s'arrête et pose des
  questions tant qu'un champ n'est pas renseigné.
- `bg.svg` (ou `bg.png`) — **optionnel** : si vous déposez une image de fond
  personnalisée (any source, ~3840×2160), elle est appliquée sur le canevas à la
  place du bandeau/fond dessinés en CSS. Sa couleur de bandeau **doit valoir**
  `Primary` pour que graphiques et onglets matchent.

Procédure complète : voir le README.md à la racine du dépôt.

Fichiers à déposer par l'utilisateur (le skill ne les crée jamais) :
- `logo.png` — le logo du client (fond transparent)
- `donnees.xlsx` — les données source (feuilles = tables)

Fichiers produits par le skill (ne pas créer à la main) :
- `maquette/index.html` (la maquette) — **interactive** : panneau de filtres
  **fonctionnel** (année, trimestre, mois, plage de dates, bouton Effacer) et
  KPIs temporels avec **variation vs N-1**.
