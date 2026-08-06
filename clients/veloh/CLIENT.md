# Client : veloh

> **Ce fichier est écrit PAR LE SKILL** `powerbi-prototype`, à partir de vos
> réponses au **questionnaire guidé** — vous n'avez rien à y saisir. C'est le
> contrat de marque lu par `scripts/render.py` pour générer la maquette. Le
> **seul** fichier que vous déposez est `logo.png` (fond transparent) ; les
> données (`donnees.xlsx`) sont **générées par le skill** depuis
> `data-spec.json`.

## Identité

* Brand Name: veloh
* Report Title: Pilotage Supply Chain
* Report Subtitle: Livraisons, flux & qualité logistique · 2024–2025

## Couleurs

> Seule la couleur **Primary** est fournie par le client (code hexadécimal,
> ex. `#00A1B1`). Les autres sont **proposées par le skill** — nommées en
> clair (« blanc pur », « gris bleuté très clair »…) — puis validées avec le
> client. Le bandeau est dessiné en CSS avec `Primary` : si un fond `bg.*`
> est déposé (optionnel), sa couleur de bandeau **doit être la même**.

* Primary / Banner Accent: #2563EB   <!-- bandeau, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        #FFFFFF    <!-- blanc pur — zone logo, cards -->
* Canvas Background:      #F1F5F9   <!-- gris bleuté très clair — fond du canevas, panneau filtres, footer -->
* Card Frame Color:       #FFFFFF <!-- blanc pur (= Surface) — couleur des encadrés -->
* Border / Divider:       #CBD5E1   <!-- gris neutre doux -->

## Contexte & Données

> Résumé des réponses au questionnaire — le skill le traduit en
> `data-spec.json` puis génère `donnees.xlsx` (2 années civiles closes) via
> `scripts/generate-data.py`.

* Domaine: pilotage de la performance de la chaîne logistique (précision des livraisons, rotation des stocks, optimisation des coûts de transport)
* Faits: FAIT_LIVRAISON — 1 ligne = 1 livraison expédiée datée
* Mesures: COUT_TRANSPORT (€, ~420/livraison, +5%/an), QUANTITE (unités, ~110/livraison, +3%/an), DISTANCE_KM (km, ~160/livraison), A_TEMPS (flag 0/1, ~93% à temps)
* Dimensions: Type client (4 modalités), Zone (5 modalités), Univers produit (3 modalités), Famille produit (5 modalités, hiérarchie sous Univers), Mode transport (4 modalités)
* Entité suivie: DIM_CLIENT (140 destinataires de livraison)
* Saisonnalité: pic d'activité juin & novembre, creux août
* Feuille annexe: FAIT_INCIDENT (tickets — statut Ouvert/En cours/Résolu, délai de résolution en heures)

## Arbre de navigation

> Proposé par le skill et **validé par le client** pendant le questionnaire.
> Chaque sous-page liste ses cartes KPI.

### Page 1: Livraisons

* Sub-page 1.1: Vue d'ensemble
  * KPI 1.1.1: Livraisons (volume)
  * KPI 1.1.2: Taux à temps
  * KPI 1.1.3: Clients livrés (actifs)
  * KPI 1.1.4: Quantité livrée
  * Visuels: courbe coût mensuel · donut Zone · donut Type client · table par Zone
* Sub-page 1.2: Coût & distance
  * KPI 1.2.1: Coût transport total
  * KPI 1.2.2: Coût/km
  * KPI 1.2.3: Distance moyenne
  * Visuels: ratio-line coût/km mensuel · empilé coût par Mode · donut Mode

### Page 2: Stocks & flux

* Sub-page 2.1: Écoulement
  * KPI 2.1.1: Quantité écoulée
  * KPI 2.1.2: Familles actives
  * KPI 2.1.3: Famille dominante
  * KPI 2.1.4: Coût unitaire
  * Visuels: empilé quantité par Famille · donut Famille · courbe quantité

### Page 3: Qualité & incidents

* Sub-page 3.1: Incidents
  * KPI 3.1.1: Tickets
  * KPI 3.1.2: Délai moyen de résolution
  * KPI 3.1.3: Statut dominant
  * Visuels: donut Statut · table Statut (part %)
