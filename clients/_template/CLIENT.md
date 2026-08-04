# Client : <CLIENT_NAME>

> **C'est le SEUL fichier de configuration** pour un client. Le skill
> `powerbi-prototype` le lit pour générer la maquette. Remplissez **toute**
> valeur entre `<...>` (elles servent de marqueurs « à compléter »). Les
> **données** (`donnees.xlsx`) et le **logo** (`logo.png`, fond transparent)
> sont **toujours fournis par vous** — déposez-les dans ce dossier.

## Identité

* Brand Name: <CLIENT_NAME>
* Report Title: <Titre du rapport>
* Report Subtitle: <sous-titre / période>

## Couleurs

> **Note :** le bandeau est dessiné en CSS avec `Primary`. Si vous fournissez un
> fond `bg.*` exporté du `.pptx` (optionnel), sa couleur de bandeau **doit être
> la même** que `Primary` pour que graphiques et onglets matchent. Remplissez
> chaque valeur par un code hexadécimal (ex. `#00A1B1`).

* Primary / Banner Accent: <Primary>   <!-- bandeau pptx, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        <Surface>    <!-- zone logo, texte sur primaire, cards -->
* Canvas Background:      <Canvas Background>   <!-- fond du canevas, pane filtres, footer -->
* Card Frame Color:       <Card Frame> <!-- couleur des encadrés (défaut = Surface) -->
* Border / Divider:       <Border>

## Arbre de navigation

> Chaque sous-page liste ses cartes KPI. Un KPI marqué `[En consolidation]` est
> rendu avec un cadre rouge pointillé (voir
> `.opencode/skills/powerbi-prototype/references/POWERBI_COMPONENTS.md` §1.3) ;
> tous les autres sont des cards normales.
>
> La maquette générée est **interactive** : le panneau de filtres est
> **fonctionnel** (année, trimestre, mois, plage de dates) et chaque KPI dérivé
> de la série temporelle affiche automatiquement sa **variation vs N-1**.

### Page 1: <Titre page 1>

* Sub-page 1.1: <Titre sous-page>
  * KPI 1.1.1: <Libellé KPI>
  * KPI 1.1.2: <Libellé KPI> [En consolidation]
* Sub-page 1.2: <Titre sous-page>
  * KPI 1.2.1: <Libellé KPI>

### Page 2: <Titre page 2>

* Sub-page 2.1: <Titre sous-page>
  * KPI 2.1.1: <Libellé KPI>
