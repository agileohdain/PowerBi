# Client : <CLIENT_NAME>

> **C'est le SEUL fichier à éditer** pour un client. Le skill `powerbi-prototype`
> le lit pour générer la maquette (aucune question ne vous sera posée).
> `DATA.md` (modèle de données + formules KPI) est généré par le skill.

## Identité

* Brand Name: veloh
* Report Title: VELOH — Pilotage de flotte cyclable	
* Report Subtitle: Cyclistes · Flotte · Sorties · Composants — Janv. 2024 – Juil. 2025

## Couleurs

> **Important :** la couleur `Primary` ci-dessous **doit être la même** que celle
> du bandeau que vous réglez dans le `.pptx` (étape 3 du README). Le skill
> l'utilise pour les graphiques et onglets, qui doivent matcher le bandeau.

* Primary / Banner Accent: #B69E7F   <!-- bandeau pptx, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        #FFFFFF    <!-- zone logo, texte sur primaire, cards -->
* Canvas Background:      #F1F5F9    <!-- fond du canevas, pane filtres, footer -->
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