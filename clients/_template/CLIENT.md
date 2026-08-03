# Client : <CLIENT_NAME>

> **C'est le SEUL fichier à éditer** pour un client. Le skill `powerbi-prototype`
> le lit pour générer la maquette (aucune question ne vous sera posée).
> `DATA.md` (modèle de données + formules KPI) est généré par le skill.

## Identité

* Brand Name: <CLIENT_NAME>
* Report Title: <Titre du rapport>
* Report Subtitle: <sous-titre / période>

## Couleurs

> **Important :** la couleur `Primary` ci-dessous **doit être la même** que celle
> du bandeau que vous réglez dans le `.pptx` (étape 3 du README). Le skill
> l'utilise pour les graphiques et onglets, qui doivent matcher le bandeau.

* Primary / Banner Accent: #00A1B1   <!-- bandeau pptx, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        #FFFFFF    <!-- zone logo, texte sur primaire, cards -->
* Canvas Background:      #F1F5F9    <!-- fond du canevas, pane filtres, footer -->
* Card Frame Color:       #FFFFFF    <!-- couleur des encadrés (défaut = Surface) -->
* Border / Divider:       #CBD5E1

## Arbre de navigation

> Chaque sous-page liste ses cartes KPI. Un KPI marqué `[En consolidation]` est
> rendu avec un cadre rouge pointillé (voir
> `.opencode/skills/powerbi-prototype/references/POWERBI_COMPONENTS.md` §1.3) ;
> tous les autres sont des cards normales.

### Page 1: <Titre page 1>

* Sub-page 1.1: <Titre sous-page>
  * KPI 1.1.1: <Libellé KPI>
  * KPI 1.1.2: <Libellé KPI> [En consolidation]
* Sub-page 1.2: <Titre sous-page>
  * KPI 1.2.1: <Libellé KPI>

### Page 2: <Titre page 2>

* Sub-page 2.1: <Titre sous-page>
  * KPI 2.1.1: <Libellé KPI>
