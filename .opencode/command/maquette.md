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
du dossier existant, création du dossier client, dépôt du logo, des données
et du `CLIENT.md` rempli par l'utilisateur, vérification de complétude avec
arrêt et demande précise des champs manquants, puis génération de la
maquette). Il n'y a **pas** de mode « Téléguidé » : `CLIENT.md` est toujours
rempli par l'utilisateur ; tu te contentes de le vérifier.
