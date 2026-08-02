# Data Model & Visual Map: VELOH

Companion to `CLIENT.md`. `CLIENT.md` holds brand identity + the dynamic
navigation tree (pages / sub-pages / KPIs, with `[En consolidation]` flags).
This file documents the **data model** (`donnees.xlsx`), a **KPI glossary**
(definition + formula for every KPI in `CLIENT.md`), and a **per-page visual
map** (which chart, fed by which columns, for each sub-page).

> Read this **with** `CLIENT.md` when building a VELOH dashboard. The agent
> should not need to re-open or re-infer the xlsx structure — it is all here.

## Sync contract

- **`CLIENT.md` is the pilot file** (the one a human edits): brand identity,
  navigation tree, KPI labels, and `[En consolidation]` flags.
- **This `DATA.md` is a reference**, keyed by KPI ID (e.g. `1.1.2`): it holds
  the data model, each KPI's **formula** + reference value, and the per-page
  **visual map**. The KPI label printed here is only a reading hint — the
  authoritative label and any flag live in `CLIENT.md`.
- **Rule:** never set or clear `[En consolidation]` here. To flag a KPI as
  consolidated, edit `CLIENT.md` only — this file stays valid as-is. Update
  `DATA.md` only when a KPI's **formula**, source columns, or recommended
  visual changes.

## 1. Source & scope

- **File:** `./donnees.xlsx` (alongside this file).
- **Period:** January 2024 – July 2025 (19 months).
- **Volumes:** 50 registered cyclists, 80 bikes, 5 000 rides, 200 tracked
  components.
- **Nature:** fictitious / mockup data.

## 2. Data model (snowflake schema, Excel sheets = tables)

Central join key: **`ID_UTILISATEUR_VELO`** (surrogate from the junction table)
links the two fact tables and the component dimension to the cyclist & bike
dimensions.

| Sheet (table) | Role | Rows | Columns |
|---|---|---|---|
| `DIM_UTILISATEUR` | Dimension — cyclists | 50 | `ID_Utilisateur` (PK), `Nom`, `Prenom`, `Pays`, `Ville`, `Email` |
| `DIM_VELO` | Dimension — bikes | 80 | `ID_Velo` (PK), `Marque`, `Modele`, `Annee_Sortie` |
| `ASSOC_UTILISATEUR_VELO` | Junction — cyclist↔bike | 95 | `ID_UTILISATEUR_VELO` (PK), `ID_Utilisateur` (FK), `ID_Velo` (FK) |
| `DIM_COMPOSANT` | Dimension — components | 200 | `ID_Composant` (PK), `ID_UTILISATEUR_VELO` (FK), `Nom_Composant`, `Categorie_Composant`, `Duree_Vie_KM`, `Duree_Vie_Heures`, `Date_Installation` |
| `FAIT_SORTIES` | Fact — rides | 5 000 | `ID_Sortie` (PK), `ID_UTILISATEUR_VELO` (FK), `DATE_HEURE`, `DATE`, `NB_KM`, `MINUTES` |
| `FAIT_USURE_COMPOSANT` | Fact — component wear | 200 | `ID_Composant` (FK), `ID_UTILISATEUR_VELO` (FK), `KM_Parcourus`, `Heures_Utilisation`, `Pct_Usure_KM`, `Pct_Usure_Heures`, `KM_Restants`, `Statut_Alerte`, `Date_Derniere_Sortie` |

### Joins
```
DIM_UTILISATEUR ─┐
                 ├─ ASSOC_UTILISATEUR_VELO ─┬─ FAIT_SORTIES
DIM_VELO ────────┘    (ID_UTILISATEUR_VELO) ├─ DIM_COMPOSANT
                                           └─ FAIT_USURE_COMPOSANT
```
- Country / city come from `DIM_UTILISATEUR` (reached via the junction).
- Bike brand / model / year come from `DIM_VELO`.
- Component category, lifespan, install date from `DIM_COMPOSANT`.
- `Statut_Alerte` values in `FAIT_USURE_COMPOSANT`: `OK`, `Critique`, `Dépassé`.

## 3. KPI glossary

Notation: `Σ` = sum, `#` = count, `#D` = count distinct, `AVG`/`MED` = mean /
median. "Actif" = cyclist with ≥ 1 ride in the period. Figures shown are the
reference values used in the existing dashboard.

### Page 1 — Cyclistes
| KPI | Definition / formula | Ref |
|---|---|---|
| 1.1.1 Cyclistes actifs | `#D ID_Utilisateur` having ≥1 sortie | 40 (of 50 inscrits) |
| 1.1.2 Km totaux | `Σ FAIT_SORTIES.NB_KM` | 300 248 km |
| 1.1.3 Sorties | `# FAIT_SORTIES.ID_Sortie` | 5 000 |
| 1.1.4 Km / cycliste | `Σ NB_KM` / cyclistes actifs | 7 506 km |
| 1.1.5 Durée moy. / sortie | `AVG FAIT_SORTIES.MINUTES` | 2 h 11 (131 min) |
| 1.2.1 Pays couverts | `#D DIM_UTILISATEUR.Pays` | 3 |
| 1.2.2 Villes couvertes | `#D DIM_UTILISATEUR.Ville` | — |
| 1.2.3 Cyclistes par pays | `#D ID_Utilisateur` GROUP BY `Pays` | — |
| 1.3.1 Cyclistes avec vélo | `#D ID_Utilisateur` in `ASSOC_UTILISATEUR_VELO` | 50 |
| 1.3.2 Vélos attribués | `#D ID_Velo` in `ASSOC` | — |
| 1.3.3 Ratio vélos / cycliste | vélos attribués / cyclistes inscrits | — |

### Page 2 — Flotte vélos
| KPI | Definition / formula |
|---|---|
| 2.1.1 Vélos en flotte | `# DIM_VELO.ID_Velo` (80) |
| 2.1.2 Marques distinctes | `#D DIM_VELO.Marque` |
| 2.1.3 Année moyenne du parc | `AVG DIM_VELO.Annee_Sortie` |
| 2.1.4 Km total parcouru | `Σ NB_KM` via join bike → sorties |
| 2.2.1 Vélos par marque | `# ID_Velo` GROUP BY `Marque` |
| 2.2.2 Marque dominante | marque with max bike count |
| 2.3.1 Vélos affectés | `#D ID_Velo` in `ASSOC` |
| 2.3.2 Vélos disponibles | vélos en flotte − vélos affectés |
| 2.3.3 Cyclistes sans vélo | inscrits (50) − cyclistes avec vélo |

### Page 3 — Sorties
| KPI | Definition / formula |
|---|---|
| 3.1.1 Sorties totales | `# FAIT_SORTIES.ID_Sortie` (5 000) |
| 3.1.2 Km totaux | `Σ NB_KM` |
| 3.1.3 Durée totale | `Σ MINUTES` |
| 3.1.4 Vitesse moyenne | `Σ NB_KM` / (`Σ MINUTES` / 60) km/h |
| 3.2.1 Sorties / mois | `# ID_Sortie` GROUP BY `month(DATE)` |
| 3.2.2 Km / mois | `Σ NB_KM` GROUP BY `month(DATE)` |
| 3.3.1 Vitesse moyenne | `AVG( NB_KM / (MINUTES/60) )` per ride |
| 3.3.2 Plus longue sortie | `MAX NB_KM` |
| 3.3.3 Plus longue durée | `MAX MINUTES` |

### Page 4 — Composants & Usure
| KPI | Definition / formula |
|---|---|
| 4.1.1 Composants suivis | `# DIM_COMPOSANT.ID_Composant` (200) |
| 4.1.2 Catégories de composants | `#D Categorie_Composant` |
| 4.1.3 Âge moyen | `AVG( today − Date_Installation )` |
| 4.2.1 Usure moyenne (km) | `AVG FAIT_USURE.Pct_Usure_KM` |
| 4.2.2 Usure moyenne (heures) | `AVG Pct_Usure_Heures` |
| 4.2.3 Km restants médian | `MED KM_Restants` |
| 4.3.1 Alertes dépassées | `#` WHERE `Statut_Alerte = 'Dépassé'` |
| 4.3.2 Alertes critiques | `#` WHERE `Statut_Alerte = 'Critique'` |
| 4.3.3 Composants OK | `#` WHERE `Statut_Alerte = 'OK'` |
| 4.3.4 Taux de conformité | composants OK / total composants |

## 4. Per-page visual map

Chart-type codes refer to `POWERBI_COMPONENTS.md`:
`L`=line/area §3.3, `COL`=column §3.2A, `BAR`=horizontal bar §3.2B,
`STACK`=stacked column §3.2A, `DONUT`=donut/pie §3.4, `HEAT`=heatmap §3.5,
`PROG`=progress/bullet §3.6, `TBL`=table §3.7, `MULTI`=multi-metric card §1.2.

### Page 1 — Cyclistes
| Sub-page | Recommended visuals (type · title · source columns) |
|---|---|
| **1.1 Vue d'ensemble** ✅ *validated in existing dashboard* | `L` Km parcourus par mois · `Σ NB_KM` by `month(DATE)` · `DONUT` Répartition km par pays · `Σ NB_KM` by `DIM_UTILISATEUR.Pays` · `MULTI` Indicateurs d'activité (taux activité, cyclistes avec vélo, part km/pays) · `STACK` Sorties par mois et par pays · `# ID_Sortie` by month × `Pays` · `HEAT` Calendrier d'activité · `# sorties` by weekday(`DATE`) × month · `BAR` Top cyclistes · `Σ NB_KM` by `Nom` (top 8) |
| 1.2 Répartition géographique | `BAR` Cyclistes par pays · `#D ID_Utilisateur` by `Pays` · `BAR` Top villes · `#D ID_Utilisateur` by `Ville` · `DONUT` Part des km par pays · `Σ NB_KM` by `Pays` |
| 1.3 Affectations vélos | `DONUT` Cyclistes avec / sans vélo · `MULTI` Vélos attribués + ratio · `BAR` Nb de vélos par cycliste · `# ID_Velo` by `ID_Utilisateur` |

### Page 2 — Flotte vélos
| Sub-page | Recommended visuals |
|---|---|
| 2.1 Vue d'ensemble | `BAR` Km par vélo (top) · `Σ NB_KM` by `ID_Velo` · `COL` Vélos par année · `# ID_Velo` by `Annee_Sortie` · `DONUT` Part par marque · `# ID_Velo` by `Marque` |
| 2.2 Répartition par marque | `BAR` Vélos par marque · `# ID_Velo` by `Marque` (sorted desc, marque dominante highlighted) · `DONUT` Part de marché · same |
| 2.3 Affectations cyclistes | `DONUT` Vélos affectés vs disponibles · `PROG` Taux d'affectation · `BAR` Cyclistes sans vélo par pays · `#D ID_Utilisateur` sans vélo by `Pays` |

### Page 3 — Sorties
| Sub-page | Recommended visuals |
|---|---|
| 3.1 Vue d'ensemble | `L` Km par mois · `Σ NB_KM` by month · `COL` Sorties par mois · `# ID_Sortie` by month · `MULTI` Durée totale + vitesse moyenne |
| 3.2 Évolution temporelle | `L` Sorties / mois (dual-Y) · `# ID_Sortie` + `Σ NB_KM` by month · `L` Km / mois · `Σ NB_KM` by month |
| 3.3 Performance (km / durée) | `BAR` Top sorties (km) · top `NB_KM` rides · `BAR` Top sorties (durée) · top `MINUTES` rides · `DONUT` Distribution des vitesses moyennes (bandes) |

### Page 4 — Composants & Usure
| Sub-page | Recommended visuals |
|---|---|
| 4.1 Composants installés | `BAR` Composants par catégorie · `# ID_Composant` by `Categorie_Composant` · `COL` Installations par année · `#` by `year(Date_Installation)` |
| 4.2 État d'usure (km / heures) | `BAR` Usure moyenne par catégorie · `AVG Pct_Usure_KM` by `Categorie_Composant` · `PROG` Km restants médian vs durée de vie · `MED KM_Restants` / `Duree_Vie_KM` |
| 4.3 Alertes (OK / Critique / Dépassé) | `DONUT` Répartition par `Statut_Alerte` (OK / Critique / Dépassé) · `PROG` Taux de conformité · `BAR` Alertes par catégorie · `#` WHERE `Statut_Alerte ≠ 'OK'` by `Categorie_Composant` · `TBL` Détail composants en alerte |

> Only sub-page **1.1** is locked to the validated dashboard above. The other
> 11 are recommended defaults — coherent with the KPIs and available columns;
> adjust per stakeholder feedback.
