# Client Identity & Navigation Config: <CLIENT_NAME>

> **Pilot file.** C'est le seul fichier à éditer pour un client — identité de
> marque, arbre de navigation, libellés KPI, et flags `[En consolidation]`.
> `DATA.md` contient le modèle de données + les formules par KPI + la carte
> visuelle ; il suit ce fichier et ne re-déclare jamais les flags ni les libellés.

* Brand Name: <CLIENT_NAME>
* Logo Path: ./logo.png
* Logo Position: Top-Left (Header)
* Background Image (optional): none          <!-- ou ./bg.png -->
* Report Title: <Titre du rapport>
* Report Subtitle: <sous-titre / période>

## Colors (drives the dashboard CSS variables)

* Primary / Banner Accent: #00A1B1            <!-- header, "Filtres", onglets actifs, série primaire -->
* Surface / Cards: #FFFFFF                     <!-- zone logo, texte sur primaire -->
* Canvas Background: #F1F5F9                   <!-- fond du canevas, pane filtres, footer -->
* Card Frame Color: #FFFFFF                    <!-- couleur des encadrés (défaut = Surface) -->
* Border / Divider: #CBD5E1

## Dynamic Navigation Structure

Chaque sous-page liste ses cartes KPI. Un KPI marqué `[En consolidation]` est
rendu avec le cadre rouge pointillé en consolidation
(voir `references/POWERBI_COMPONENTS.md` §1.3) ; tous les autres sont rendus
comme des cards normales.

### Page 1: <Titre page 1>

* Sub-page 1.1: <Titre sous-page>
  * KPI 1.1.1: <Libellé KPI>
  * KPI 1.1.2: <Libellé KPI> [En consolidation]
* Sub-page 1.2: <Titre sous-page>
  * KPI 1.2.1: <Libellé KPI>

### Page 2: <Titre page 2>

* Sub-page 2.1: <Titre sous-page>
  * KPI 2.1.1: <Libellé KPI>
