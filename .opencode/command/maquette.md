---
description: Lance le processus de création de maquette Power BI pour un client (nom passé en argument).
agent: build
---

Tu lances le processus de maquette Power BI pour un client.

Charge le skill `powerbi-prototype` et démarre sa **Phase 0** (nom du client)
avec le nom suivant passé en argument (respecte stricto sensu la casse, ne
propose aucun nom) :

- Nom du client : `$ARGUMENTS` (si vide, demande-le à l'utilisateur)

Déroule ensuite le processus complet du skill (confirmation du nom, gestion
du dossier existant, création du dossier client, dépôt du logo et des
données, choix Téléguidé/Personnaliser, puis génération de la maquette).
