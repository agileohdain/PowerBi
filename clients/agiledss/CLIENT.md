# Client : agiledss

> **Ce fichier est écrit PAR LE SKILL** `powerbi-prototype`, à partir de vos
> réponses au **questionnaire guidé** — vous n'avez rien à y saisir. C'est le
> contrat de marque lu par `scripts/render.py` pour générer la maquette. Le
> **seul** fichier que vous déposez est `logo.png` (fond transparent) ; les
> données (`donnees.xlsx`) sont **générées par le skill** depuis
> `data-spec.json`.

## Identité

* Brand Name: agiledss
* Report Title: agiledss — Pilotage de la performance financière
* Report Subtitle: Rentabilité · Trésorerie · Investissements — 2024–2025

## Couleurs

> Seule la couleur **Primary** est fournie par le client (code hexadécimal).
> Les autres sont **proposées par le skill** — nommées en clair — puis
> validées avec le client. Le bandeau est dessiné en CSS avec `Primary` : si
> un fond `bg.*` est déposé (optionnel), sa couleur de bandeau **doit être la
> même`.

* Primary / Banner Accent: #FA8FF8   <!-- rose/violet très clair — bandeau, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        #FFFFFF    <!-- blanc pur — zone logo, cards -->
* Canvas Background:      #F1F5F9    <!-- gris bleuté très clair — fond du canevas, pane filtres, footer -->
* Card Frame Color:       #FFFFFF    <!-- blanc pur (défaut = Surface) — encadrés des cartes -->
* Border / Divider:       #CBD5E1    <!-- gris ardoise — bordures, séparateurs -->

## Contexte & Données

> Résumé des réponses au questionnaire — le skill le traduit en
> `data-spec.json` puis génère `donnees.xlsx` (2 années civiles closes) via
> `scripts/generate-data.py`.

* Domaine: pilotage d'une performance financière : rentabilité, trésorerie/cash et investissements/solvabilité
* Faits: FAIT_ENTREE — 1 ligne = 1 écriture comptable datée (facture encaissée ou charge payée)
* Mesures: MONTANT (k€), MONTANT_PREVU (k€, budgété)
* Dimensions: Categorie (4), SousFamille (13), Zone (6) — entités, Segment (3), Region (5) — clients
* Entité suivie: DIM_CLIENT (120 clients) — clients actifs par mois
* Tables annexes: FAIT_CREANCE (statuts, délai de paiement/DSO, encours), FAIT_INVESTISSEMENT (statuts, ROI, enveloppes)

## Arbre de navigation

> Proposé par le skill et **validé par le client** pendant le questionnaire.
> Chaque sous-page liste ses cartes KPI.

### Page 1: Synthèse

* Sub-page 1.1: Vue d'ensemble
  * KPI 1.1.1: Flux financier (MONTANT, k€, YoY)
  * KPI 1.1.2: Clients actifs (YoY)
  * KPI 1.1.3: Réalisation budgétaire (MONTANT/MONTANT_PREVU, YoY)
  * KPI 1.1.4: DSO moyen (jours)
  * KPI 1.1.5: ROI moyen

### Page 2: Performance & Rentabilité

* Sub-page 2.1: Chiffre d'affaires & volume
  * KPI 2.1.1: Volume financier (MONTANT, k€, YoY)
  * KPI 2.1.2: Écritures traitées (_count, YoY)
  * KPI 2.1.3: Taux de réalisation du budget (YoY)
  * KPI 2.1.4: Segment client dominant
* Sub-page 2.2: Structure des coûts
  * KPI 2.2.1: Budget engagé (MONTANT_PREVU, k€, YoY)
  * KPI 2.2.2: Taux d'engagement (MONTANT/MONTANT_PREVU, YoY)
  * KPI 2.2.3: Nature dominante
  * KPI 2.2.4: Poste le plus important

### Page 3: Trésorerie & Cash

* Sub-page 3.1: Liquidités & encours
  * KPI 3.1.1: Clients actifs (YoY)
  * KPI 3.1.2: DSO moyen (jours)
  * KPI 3.1.3: Encours moyen des créances (k€)
  * KPI 3.1.4: Créances au portefeuille
* Sub-page 3.2: Réalisation budgétaire
  * KPI 3.2.1: Budget annuel (MONTANT_PREVU, k€, YoY)
  * KPI 3.2.2: Écart réalisé vs prévu (YoY)
  * KPI 3.2.3: Flux moyen par écriture (MONTANT/_count, YoY)
  * KPI 3.2.4: Écritures traitées (YoY)

### Page 4: Investissements & Rentabilité

* Sub-page 4.1: Portefeuille d'investissements
  * KPI 4.1.1: ROI moyen
  * KPI 4.1.2: Enveloppe moyenne par projet (k€)
  * KPI 4.1.3: Projets suivis
  * KPI 4.1.4: Statut dominant
* Sub-page 4.2: ROI & solvabilité
  * KPI 4.2.1: ROI moyen
  * KPI 4.2.2: Réalisation budgétaire (YoY)
  * KPI 4.2.3: Flux moyen par écriture (YoY)
  * KPI 4.2.4: Projets en cours
