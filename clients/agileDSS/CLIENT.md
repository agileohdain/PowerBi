# Client : agileDSS

> **Ce fichier est écrit PAR LE SKILL** `powerbi-prototype`, à partir de vos
> réponses au **questionnaire guidé** — vous n'avez rien à y saisir. C'est le
> contrat de marque lu par `scripts/render.py` pour générer la maquette. Le
> **seul** fichier que vous déposez est `logo.png` (fond transparent) ; les
> données (`donnees.xlsx`) sont **générées par le skill** depuis
> `data-spec.json`.

## Identité

* Brand Name: agileDSS
* Report Title: agileDSS — Pilotage de la performance financière
* Report Subtitle: CA · Marges · EBITDA · Coûts — 2024–2025

## Couleurs

> Seule la couleur **Primary** est fournie par le client (code hexadécimal,
> ex. `#00A1B1`). Les autres sont **proposées par le skill** — nommées en
> clair (« blanc pur », « gris bleuté très clair »…) — puis validées avec le
> client. Le bandeau est dessiné en CSS avec `Primary` : si un fond `bg.*`
> est déposé (optionnel), sa couleur de bandeau **doit être la même**.

* Primary / Banner Accent: #00853F   <!-- bandeau, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        #FFFFFF    <!-- zone logo, cards -->
* Canvas Background:      #F1F5F9    <!-- fond du canevas, pane filtres, footer -->
* Card Frame Color:       #FFFFFF    <!-- couleur des encadrés (défaut = Surface) -->
* Border / Divider:       #CBD5E1

## Contexte & Données

> Résumé des réponses au questionnaire — le skill le traduit en
> `data-spec.json` puis génère `donnees.xlsx` (2 années civiles closes) via
> `scripts/generate-data.py`.

* Domaine: performance opérationnelle et rentabilité — CA, marges (marge brute,
  EBITDA, résultat net) et structure de coûts (OPEX, CAPEX, masse salariale)
* Faits: FAIT_FINANCE — 1 ligne = 1 écriture comptable
* Mesures: REVENUS (€), MARGE_BRUTE (€, ≈58 % CA), EBITDA (€, ≈24 % CA),
  RESULTAT_NET (€, ≈12 % CA), OPEX (€), MASSE_SALARIALE (€), CAPEX (€)
* Dimensions: DIM_COMPTE (20 comptes, hiérarchie Catégorie → Compte),
  DIM_ENTITE (10 départements), DIM_CLIENT (100 clients, segment)
* Entité suivie: DIM_CLIENT (100 clients)

## Arbre de navigation

> Proposé par le skill et **validé par le client** pendant le questionnaire.
> Chaque sous-page liste ses cartes KPI.

### Page 1: Performance & Rentabilité

* Sub-page 1.1: Vue d'ensemble
  * KPI 1.1.1: Chiffre d'affaires
  * KPI 1.1.2: Résultat net
  * KPI 1.1.3: Taux de marge nette
  * KPI 1.1.4: Clients actifs
* Sub-page 1.2: Marges & EBITDA
  * KPI 1.2.1: Marge brute
  * KPI 1.2.2: Taux de marge brute
  * KPI 1.2.3: EBITDA
  * KPI 1.2.4: Taux de marge EBITDA

### Page 2: Structure des coûts

* Sub-page 2.1: Charges d'exploitation
  * KPI 2.1.1: OPEX
  * KPI 2.1.2: Couverture des charges
  * KPI 2.1.3: Part OPEX sur CA
  * KPI 2.1.4: Compte de charges dominant
* Sub-page 2.2: Masse salariale
  * KPI 2.2.1: Masse salariale
  * KPI 2.2.2: Masse salariale sur CA
  * KPI 2.2.3: Département en tête
* Sub-page 2.3: Investissements (CAPEX)
  * KPI 2.3.1: CAPEX
  * KPI 2.3.2: Poids des investissements
  * KPI 2.3.3: Compte d'investissement dominant
