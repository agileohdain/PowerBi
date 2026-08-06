# Client : agileDSS

> **Ce fichier est écrit PAR LE SKILL** `powerbi-prototype`, à partir de vos
> réponses au **questionnaire guidé** — vous n'avez rien à y saisir. C'est le
> contrat de marque lu par `scripts/render.py` pour générer la maquette. Le
> **seul** fichier que vous déposez est `logo.png` (fond transparent) ; les
> données (`donnees.xlsx`) sont **générées par le skill** depuis
> `data-spec.json`.

## Identité

* Brand Name: agileDSS
* Report Title: AGILEDSS — Chaîne logistique · Performance livraisons & stocks
* Report Subtitle: Livraisons · Transporteurs · Stocks — 2024-2025

## Couleurs

> Seule la couleur **Primary** est fournie par le client (code hexadécimal,
> ex. `#00A1B1`). Les autres sont **proposées par le skill** — nommées en
> clair (« blanc pur », « gris bleuté très clair »…) — puis validées avec le
> client. Le bandeau est dessiné en CSS avec `Primary` : si un fond `bg.*`
> est déposé (optionnel), sa couleur de bandeau **doit être la même**.

* Primary / Banner Accent: #2563EB   <!-- bandeau bleu roi, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        #FFFFFF    <!-- blanc pur — zone logo, cards -->
* Canvas Background:      #F1F5F9    <!-- gris bleuté très clair — fond du canevas, pane filtres, footer -->
* Card Frame Color:       #FFFFFF    <!-- blanc pur (défaut = Surface) -->
* Border / Divider:       #CBD5E1    <!-- gris ardoise — encadrés, divisseurs, grille des tables -->

## Contexte & Données

> Résumé des réponses au questionnaire — le skill le traduit en
> `data-spec.json` puis génère `donnees.xlsx` (2 années civiles closes) via
> `scripts/generate-data.py`.

* Domaine: performance opérationnelle d'une chaîne logistique — précision des livraisons, rotation des stocks, optimisation des coûts de transport
* Faits: FAIT_LIVRAISON — 1 ligne = 1 livraison datée (~700/mois sur 2024-2025)
* Mesures: COUT_TRANSPORT (€, ~85 €/livraison), NB_COLIS (nb, ~2,4/livraison), RETARD (min, ~8 min)
* Dimensions: DIM_CLIENT (30 clients, Segment + Zone), DIM_ENTREPOT (6, Region), DIM_TYPE_LIVRAISON (3), DIM_TRANSPORTEUR (6, Prestataire)
* Entité suivie: DIM_CLIENT (30 individus) — requise pour les KPI « actifs »
* Table annexe: FAIT_STOCK (NB_UNITES + Statut catégoriel — Rupture/Tension/Nominal/Surstock)

## Arbre de navigation

> Proposé par le skill et **validé par le client** pendant le questionnaire.
> Chaque sous-page liste ses cartes KPI.

### Page 1: Performance logistique

* Sub-page 1.1: Vue d'ensemble
  * KPI 1.1.1: Livraisons (nb)
  * KPI 1.1.2: Coût de transport total (€)
  * KPI 1.1.3: Taux OTIF (%)
  * KPI 1.1.4: Volume de colis
* Sub-page 1.2: Précision OTIF
  * KPI 1.2.1: Taux OTIF (%)
  * KPI 1.2.2: Retard moyen (min)
  * KPI 1.2.3: Coût moyen par livraison (€)
  * KPI 1.2.4: Livraisons (nb)
* Sub-page 1.3: Transporteurs
  * KPI 1.3.1: Transporteurs (nb)
  * KPI 1.3.2: Coût moyen par livraison (€)
  * KPI 1.3.3: Taux OTIF global (%)
  * KPI 1.3.4: Volume de colis

### Page 2: Stocks & Coûts

* Sub-page 2.1: État des stocks
  * KPI 2.1.1: Unités en stock (moyenne)
  * KPI 2.1.2: Statut des stocks (Rupture/Tension/Nominal/Surstock)
  * KPI 2.1.3: Part de ruptures (%)
* Sub-page 2.2: Coûts de transport
  * KPI 2.2.1: Coût total mensuel (€)
  * KPI 2.2.2: Coût moyen par livraison (€)
  * KPI 2.2.3: Coût par région (€)
  * KPI 2.2.4: Coût moyen par colis (€)
