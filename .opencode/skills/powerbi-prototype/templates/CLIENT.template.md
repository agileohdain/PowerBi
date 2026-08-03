# Client : <CLIENT_NAME>

> **C'est le SEUL fichier de configuration** pour un client. Le skill
> `powerbi-prototype` le lit pour générer la maquette. En mode **Téléguidé**,
> le skill l'écrit pour vous à partir de vos réponses ; en mode
> **Personnaliser**, vous l'éditez vous-même. Les **données** (`donnees.xlsx`)
> sont déposées par vous ou générées par le skill. Déposez aussi `logo.png`
> (fond transparent) dans le même dossier.

## Identité

* Brand Name: <CLIENT_NAME>
* Report Title: <Titre du rapport>
* Report Subtitle: <sous-titre / période>

## Couleurs

> **Note :** le bandeau est dessiné en CSS avec `Primary`. Si vous fournissez un
> fond `bg.*` exporté du `.pptx` (optionnel), sa couleur de bandeau **doit être
> la même** que `Primary` pour que graphiques et onglets matchent.

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
