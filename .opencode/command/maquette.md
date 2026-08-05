---
description: Lance le processus de création de maquette Power BI pour un client (nom passé en argument).
agent: build
---

Tu lances le processus de maquette Power BI pour un client.

Charge le skill `powerbi-prototype` et démarre sa **Phase 0** (nom du client)
avec le nom suivant passé en argument (respecte stricto sensu la casse, ne
propose aucun nom) :

- Nom du client : `$ARGUMENTS` (si vide, demande-le à l'utilisateur)

Déroule ensuite le processus complet du skill :

1. **Confirmation du nom** (« Est-ce bien le client « X » ? — Oui / Modifier »),
   garde client existant (régénérer / refaire le questionnaire / modifier le
   nom), et passage en mode BUILD si l'utilisateur est en mode PLAN.
2. **Création du dossier** `clients/<Nom>/` avec `CLIENT.md` (copie du
   template, nom pré-rempli). Ne crée jamais de logo.
3. **Demande des deux seules fournitures** : `logo.png` (fond transparent,
   déposé dans le dossier) et la couleur primaire en hexadécimal — puis arrêt
   en attente.
4. **Questionnaire guidé** (Phase 1) : tu proposes, l'utilisateur valide ou
   ajuste — domaine métier → schéma de données → arbre de navigation + KPIs →
   couleurs secondaires (nommées en clair) + titre/sous-titre.
5. **Génération** (Phase 2) : tu écris `CLIENT.md` + `data-spec.json`, tu
   génères `donnees.xlsx` (`scripts/generate-data.py`) avec auto-contrôle
   bloquant via `scripts/extract-data.py`.
6. **Maquette** (Phase 3) : `views.json` raffiné, `scripts/render.py`, smoke
   test (exit 0 exigé avant livraison), puis indication d'ouverture du rendu.

L'utilisateur ne fournit QUE : le nom, le logo et la couleur primaire. Ne
lui réclame jamais de fichier de données ni de `CLIENT.md` rempli — les
données sont générées par le skill et `CLIENT.md` est écrit par toi.
