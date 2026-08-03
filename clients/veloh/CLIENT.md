# Client Identity & Navigation Config: VELOH

> **Pilot file.** This is the single file to edit for a client — brand
> identity, navigation tree, KPI labels, and `[En consolidation]` flags.
> The data model, per-KPI formulas and visual map are deduced from
> `donnees.xlsx`; this file never re-declares flags or labels.

* Brand Name: VELOH
* Logo Path: ./logo.png
* Logo Position: Top-Left (Header)
* Colors:

  * Primary / Banner Accent: #E0BE7E
  * Border / Divider: #334155
  * Surface / Cards: #1E293B
  * Canvas Background: #0F172A

## Dynamic Navigation Structure

Each sub-page lists its KPI cards. A KPI marked `[En consolidation]` is rendered
with the red dashed consolidation frame (see the skill's component catalog §1.3);
all other KPIs render as normal cards.

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
* Sub-page 2.3: Affectations cyclistes
  * KPI 2.3.1: Vélos affectés
  * KPI 2.3.2: Vélos disponibles
  * KPI 2.3.3: Cyclistes sans vélo

### Page 3: Sorties

* Sub-page 3.1: Vue d'ensemble
  * KPI 3.1.1: Sorties totales
  * KPI 3.1.2: Km totaux
  * KPI 3.1.3: Durée totale
  * KPI 3.1.4: Vitesse moyenne
* Sub-page 3.2: Évolution temporelle
  * KPI 3.2.1: Sorties / mois
  * KPI 3.2.2: Km / mois
* Sub-page 3.3: Performance (km / durée)
  * KPI 3.3.1: Vitesse moyenne
  * KPI 3.3.2: Plus longue sortie
  * KPI 3.3.3: Plus longue durée

### Page 4: Composants & Usure

* Sub-page 4.1: Composants installés
  * KPI 4.1.1: Composants suivis
  * KPI 4.1.2: Catégories de composants
  * KPI 4.1.3: Âge moyen
* Sub-page 4.2: État d'usure (km / heures)
  * KPI 4.2.1: Usure moyenne (km)
  * KPI 4.2.2: Usure moyenne (heures)
  * KPI 4.2.3: Km restants médian
* Sub-page 4.3: Alertes (OK / Critique / Dépassé)
  * KPI 4.3.1: Alertes dépassées
  * KPI 4.3.2: Alertes critiques
  * KPI 4.3.3: Composants OK
  * KPI 4.3.4: Taux de conformité

