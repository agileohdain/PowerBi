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
4. **Questionnaire guidé** (Phase 1, **2 questions**) : 1) domaine métier ;
   2) proposition globale unique (schéma de données + arbre de navigation avec
   KPIs + couleurs secondaires nommées en clair + titre/sous-titre) validée en
   une fois — tu proposes, l'utilisateur valide ou ajuste.
5. **Génération** (Phase 2) : tu écris `CLIENT.md` + `data-spec.json`, tu
   génères `donnees.xlsx` (`scripts/generate-data.py`) avec auto-contrôle
   bloquant via `scripts/extract-data.py`.
6. **Maquette** (Phase 3) : tu écris `nav.json` (l'arbre validé, en intentions
   courtes — schéma dans le skill), puis `scripts/build-views.py` génère
   `views.json` mécaniquement, puis `scripts/render.py` produit
   `presentation/maquette.html` et lance le smoke test (exit 0 exigé — ne pas
   le relancer à la main), boucle d'ajustement, puis
   `scripts/generate-pitch.py` et indication d'ouverture du rendu.

Ne lis jamais `references/` ni `template.html` pendant la génération : tout ce
dont tu as besoin est dans le skill.

L'utilisateur ne fournit QUE : le nom, le logo et la couleur primaire. Ne
lui réclame jamais de fichier de données ni de `CLIENT.md` rempli — les
données sont générées par le skill et `CLIENT.md` est écrit par toi.
