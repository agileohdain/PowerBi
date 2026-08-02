# Data Model & Visual Map: <CLIENT_NAME>

Compagnon de `CLIENT.md`. `CLIENT.md` porte l'identité de marque + l'arbre de
navigation dynamique (pages / sous-pages / KPIs, avec flags `[En consolidation]`).
Ce fichier documente le **modèle de données** (`donnees.xlsx`), un **glossaire
KPI** (définition + formule pour chaque KPI), et une **carte visuelle par page**
(type de chart · colonnes source).

> À lire **avec** `CLIENT.md` quand tu construis un dashboard pour ce client.
> L'agent ne devrait pas avoir à rouvrir ou ré-inférer le `.xlsx`.

## Sync contract

- **`CLIENT.md` est le fichier pilote** (édité par un humain) : identité,
  arbre de navigation, libellés KPI, flags `[En consolidation]`.
- **Ce `DATA.md` est une référence**, indexée par KPI ID (ex. `1.1.2`) :
  modèle de données, **formule** + valeur de référence de chaque KPI, et carte
  visuelle par page. Le libellé KPI imprimé ici n'est qu'un indice de lecture —
  le libellé et les flags autoritatifs vivent dans `CLIENT.md`.
- **Règle :** ne jamais positionner ou lever `[En consolidation]` ici. Pour
  flaguer un KPI en consolidation, éditer `CLIENT.md` uniquement. Mettre à jour
  `DATA.md` seulement quand la **formule**, les colonnes source, ou le visuel
  recommandé d'un KPI changent.

## 1. Source & scope

- **File:** `./donnees.xlsx` (à côté de ce fichier).
- **Period:** <mois début> – <mois fin> (<N> mois).
- **Volumes:** <N lignes de tel fait>, <N dimensions>.
- **Nature:** fictitious / mockup data.

## 2. Data model (snowflake schema, feuilles Excel = tables)

Clé de jointure centrale : **`<KEY>`** (surrogate de la table jonction) qui
relie les tables de faits et la dimension aux autres dimensions.

| Sheet (table) | Role | Rows | Columns |
|---|---|---|---|
| `DIM_xxx` | Dimension — xxx | N | `ID_xxx` (PK), ... |
| `FAIT_xxx` | Fact — xxx | N | `ID_xxx` (PK), `<KEY>` (FK), ... |

### Joins
```
DIM_xxx ─┐
         ├─ ASSOC_xxx ─┬─ FAIT_xxx
DIM_yyy ─┘   (<KEY>)   └─ DIM_zzz
```

## 3. KPI glossary

Notation : `Σ` = somme, `#` = compte, `#D` = compte distinct, `AVG`/`MED` =
moyenne / médiane.

### Page 1 — <Titre page 1>
| KPI | Definition / formula | Ref |
|---|---|---|
| 1.1.1 <Libellé KPI> | `#D ID_xxx` ... | <valeur> |

## 4. Per-page visual map

Les codes de type de chart renvoient à `references/POWERBI_COMPONENTS.md` :
`L`=line/area §3.3, `COL`=column §3.2A, `BAR`=horizontal bar §3.2B,
`STACK`=stacked column §3.2A, `DONUT`=donut/pie §3.4, `HEAT`=heatmap §3.5,
`PROG`=progress/bullet §3.6, `TBL`=table §3.7, `MULTI`=multi-metric card §1.2.

### Page 1 — <Titre page 1>
| Sub-page | Recommended visuals (type · title · source columns) |
|---|---|
| **1.1 <sous-page>** | `L` <titre> · `<colonne>` by `<dimension>` · `DONUT` <titre> · ... |
