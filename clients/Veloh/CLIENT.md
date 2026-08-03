# Client : Veloh

> **C'est le SEUL fichier de configuration** pour un client. Le skill
> `powerbi-prototype` le lit pour générer la maquette. Remplissez **toute**
> valeur entre `<...>` (elles servent de marqueurs « à compléter »). Les
> **données** (`donnees.xlsx`) et le **logo** (`logo.png`, fond transparent)
> sont **toujours fournis par vous** — déposez-les dans ce dossier.

## Identité

* Brand Name: Veloh
* Report Title: VELOH — Pilotage de flotte cyclable	
* Report Subtitle: Cyclistes · Flotte · Sorties · Composants — Janv. 2024 – Juil. 2025

## Couleurs

> **Note :** le bandeau est dessiné en CSS avec `Primary`. Si vous fournissez un
> fond `bg.*` exporté du `.pptx` (optionnel), sa couleur de bandeau **doit être
> la même** que `Primary` pour que graphiques et onglets matchent. Remplissez
> chaque valeur par un code hexadécimal (ex. `#00A1B1`).

* Primary / Banner Accent: #B69E7F   <!-- bandeau pptx, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        #FFFFFF    <!-- zone logo, texte sur primaire, cards, pane filtres -->
* Canvas Background:      #F1F5F9    <!-- fond du canevas, footer -->
* Card Frame Color:       #FFFFFF    <!-- couleur des encadrés (défaut = Surface) -->
* Border / Divider:       #CBD5E1

## Arbre de navigation

> Chaque sous-page liste ses cartes KPI. Un KPI marqué `[En consolidation]` est
> rendu avec un cadre rouge pointillé (voir
> `.opencode/skills/powerbi-prototype/references/POWERBI_COMPONENTS.md` §1.3) ;
> tous les autres sont des cards normales.

### Page 1: Cyclistes (Active)

* Sub-page 1.1: Vue d'ensemble (Active)
  * KPI 1.1.1: Cyclistes actifs [En consolidation]
  * KPI 1.1.2: Kilomètres totaux 
  * KPI 1.1.3: Sorties
  * KPI 1.1.4: Km / cycliste
  * KPI 1.1.5: Durée moy. / sortie
* Sub-page 1.2: Répartition géographique
  * KPI 1.2.1: Pays couverts [En consolidation]
  * KPI 1.2.2: Villes couvertes
  * KPI 1.2.3: Cyclistes par pays
* Sub-page 1.3: Affectations vélos
  * KPI 1.3.1: Cyclistes avec vélo [En consolidation]
  * KPI 1.3.2: Vélos attribués
  * KPI 1.3.3: Ratio vélos / cycliste

### Page 2: Flotte vélos

* Sub-page 2.1: Vue d'ensemble
  * KPI 2.1.1: Vélos en flotte
  * KPI 2.1.2: Marques distinctes
  * KPI 2.1.3: Année moyenne du parc
  * KPI 2.1.4: Km total parcouru
* Sub-page 2.2: Répartition par marque
  * KPI 2.2.1: Vélos par marque
  * KPI 2.2.2: Marque dominante

