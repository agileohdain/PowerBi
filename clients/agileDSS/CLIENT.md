# Client : agileDSS

> **Ce fichier est écrit PAR LE SKILL** `powerbi-prototype`, à partir de vos
> réponses au **questionnaire guidé** — vous n'avez rien à y saisir. C'est le
> contrat de marque lu par `scripts/render.py` pour générer la maquette. Le
> **seul** fichier que vous déposez est `logo.png` (fond transparent) ; les
> données (`donnees.xlsx`) sont **générées par le skill** depuis
> `data-spec.json`.

## Identité

* Brand Name: agileDSS
* Report Title: Pilotage SaaS · Santé financière & rétention
* Report Subtitle: MRR · Attrition · LTV/CAC — 2 ans d'activité

## Couleurs

> Seule la couleur **Primary** est fournie par le client (code hexadécimal,
> ex. `#00A1B1`). Les autres sont **proposées par le skill** — nommées en
> clair (« blanc pur », « gris bleuté très clair »…) — puis validées avec le
> client. Le bandeau est dessiné en CSS avec `Primary` : si un fond `bg.*`
> est déposé (optionnel), sa couleur de bandeau **doit être la même**.

* Primary / Banner Accent: #4c857b   <!-- bandeau, "Filtres", onglets actifs, série primaire -->
* Surface / Cards:        #FFFFFF    <!-- zone logo, cards -->
* Canvas Background:      #F1F5F9   <!-- fond du canevas, pane filtres, footer -->
* Card Frame Color:       #FFFFFF   <!-- couleur des encadrés (défaut = Surface) -->
* Border / Divider:       #CBD5E1

## Contexte & Données

> Résumé des réponses au questionnaire — le skill le traduit en
> `data-spec.json` puis génère `donnees.xlsx` (2 années civiles closes) via
> `scripts/generate-data.py`.

* Domaine: santé financière et rétention client d'un SaaS (MRR/ARR, churn, LTV/CAC)
* Faits: FAIT_ABONNEMENT — 1 ligne = 1 mois d'abonnement facturé
* Mesures: MRR (€ récurrent mensuel), FLAG_CHURN (0/1 résiliation du mois)
* Dimensions: Segment (3), Region (4), Plan (3), Canal (4)
* Entité suivie: DIM_CLIENT (200 comptes)

## Arbre de navigation

> Proposé par le skill et **validé par le client** pendant le questionnaire.
> Chaque sous-page liste ses cartes KPI.

### Page 1: Performances financières

* Sub-page 1.1: Vue d'ensemble
  * KPI 1.1.1: CA récurrent (MRR)
  * KPI 1.1.2: Abonnements
  * KPI 1.1.3: Clients actifs
  * KPI 1.1.4: Revenu moyen / abonné
  * KPI 1.1.5: Taux d'attrition
* Sub-page 1.2: Profitabilité client
  * KPI 1.2.1: Coût d'acquisition moyen
  * KPI 1.2.2: Durée de vie moyenne
  * KPI 1.2.3: Revenu moyen / abonné (ARPA)
  * KPI 1.2.4: Segment dominant

### Page 2: Rétention & acquisition

* Sub-page 2.1: Attrition
  * KPI 2.1.1: Taux d'attrition
  * KPI 2.1.2: Abonnements résiliés
  * KPI 2.1.3: Clients actifs
  * KPI 2.1.4: Plan dominant
  * KPI 2.1.5: Régions couvertes
* Sub-page 2.2: Acquisition
  * KPI 2.2.1: CAC moyen
  * KPI 2.2.2: Revenu moyen / abonné (ARPA)
  * KPI 2.2.3: Région dominante
  * KPI 2.2.4: MRR généré