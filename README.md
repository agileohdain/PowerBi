# PowerBi — Une maquette Power BI en HTML, pour valider votre futur rapport

Un **nom**, un **logo**, une **couleur primaire** — trois choses suffisent pour
obtenir un dashboard interactif, prêt à montrer en démo ou en pré-vente. Pas de
Power BI Desktop, pas de licence, **pas de données à préparer** : le skill
**propose**, vous **validez**.

> **Maquette HTML, pas Power BI.** Le rendu (`presentation/maquette.html`) est
> une **maquette web auto-suffisante** qui imite fidèlement le langage visuel de
> Power BI — ce n'est **pas** un fichier `.pbix` ni une application Power BI
> Desktop/Service. Son objectif est double : **valider le contenu** de votre
> futur rapport (navigation, KPIs, visuels) avant de le construire dans l'outil
> final, et permettre au client de **se projeter sur l'outil final** en amont du
> développement.

## Prérequis

Avant de lancer `/maquette`, votre poste doit disposer de :

| Outil | Pourquoi | Installation |
|---|---|---|
| **Node.js 18+** | exécuter opencode + le smoke test | [nodejs.org](https://nodejs.org) |
| **Python 3** | générer et extraire les données (`donnees.xlsx`) | [python.org](https://python.org) |
| **openpyxl** (Python) | lecture/écriture du `.xlsx` — **bloquant sans lui** | `pip install openpyxl` |
| **opencode** (CLI) | l'agent IA qui pilote le skill | `npm install -g opencode-ai` |
| **Clé de modèle** | ex. OpenRouter (`sk-or-…`) | `opencode auth login` |

> ⚠️ Sans `openpyxl`, la Phase 2 (génération des données) échoue avec
> `ERREUR: openpyxl manquant -> pip install openpyxl`.

## Quickstart

```powershell
pip install openpyxl   # une seule fois — requis pour la génération des données
opencode
# puis, dans opencode :
> /maquette MonClient
```

1. **Fournissez** `logo.png` (fond transparent) + la **couleur primaire** (hex,
   ex. `#FA8FF8`).
2. **Validez** le questionnaire guidé : domaine métier → modèle de données →
   navigation + KPIs → couleurs secondaires (nommées en clair) → titre.
3. Ouvrez le rendu : `start clients/MonClient/presentation/maquette.html`. **Fait.**
   Un **pitch de présentation** (`presentation/pitch.md`) est proposé à la fin
   pour scénariser la démo.

> Les **données fictives sont générées par le skill** (2 années civiles closes,
> ex. 2024–2025) — vous ne fournissez jamais d'Excel. Le skill ne crée jamais
> le logo, et ne lit jamais la maquette d'un autre client.

> Chaque validation du questionnaire est un **menu à choix cliquable**
> (Valider / Ajuster / …) — la saisie libre reste toujours possible.

## Ce que vous obtenez

Un **`presentation/maquette.html`** auto-suffisant, fidèle au langage visuel
Power BI (à **ouvrir dans le navigateur** — aucune application Power BI
requise) :

- **Canevas 1920×1080** (16:9) scaled au viewport — zéro scrollbar.
- **Bandeau trapézoïdal** aux couleurs exactes du client + zone logo.
- **KPIs avec variation N vs N-1** — `±x,x % vs 2024` (vert / rouge / neutre,
  calculé sur mois comparables).
- **Panneau de filtres interactif** — année, trimestre, mois, plage de dates,
  un slicer par dimension (badge « ● Filtres actifs », bouton Réinitialiser).
- **Navigation à deux niveaux** (pills + liens) + popover info cliquable.
- **Visuels ECharts** : courbes N-vs-N-1 (axe Jan→Déc fixe), barres mensuelles
  empilées par dimension, donuts (≤6 tranches), barres horizontales (top-10 +
  « Autres »), tables de détail. Palette catégorielle **dérivée du primaire** —
  jamais d'arc-en-ciel.

## Garde-fous automatiques

Le skill **refuse de livrer une maquette cassée** :

- **Smoke test JS** avant chaque livraison : toutes les sous-pages s'exécutent,
  chaque visuel reçoit son `echarts.init` et **est alimenté en données** —
  exit 0 exigé.
- **Données conformes par construction** : le générateur relance l'extracteur
  en auto-contrôle **bloquant**.
- **Contraste WCAG AA** dérivé automatiquement (`--on-primary`) — un primaire
  clair ne rend jamais le titre illisible.

## Dossier client

```
clients/MonClient/
├── CLIENT.md         ← écrit par le skill (marque, couleurs, navigation)
├── data-spec.json    ← écrit par le skill (spec des données)
├── donnees.xlsx      ← GÉNÉRÉ par le skill (2 années closes)
├── logo.png          ← fourni par vous — SEUL fichier déposé
├── views.json        ← carte visuelle déclarative
└── presentation/
    ├── maquette.html ← le rendu, prêt à ouvrir
    └── pitch.md      ← script du conseiller (storytelling + chiffres réels)
```

Modèle de départ : `clients/_template/`.

## Installation

```bash
gh repo clone agileohdain/PowerBi
```

## Installer OpenCode

```powershell
npm install -g opencode-ai    # Node 18+ requis
```

OpenCode est un **agent IA en terminal** : il lit, écrit et exécute dans votre
projet, avec deux modes complémentaires :

- **PLAN** — analyse et plan d'action, lecture seule ;
- **BUILD** — écriture de fichiers, exécution de commandes.

**Conseil pour démarrer** : passez par [OpenRouter](https://openrouter.ai) —
une seule clé API donne accès à tous les modèles, facturés à l'usage :

```powershell
opencode auth login   # collez votre clé OpenRouter (sk-or-…)
```

Puis configurez les agents dans `opencode.json` :

```json
{
  "agent": {
    "plan":  { "model": "openrouter/z-ai/glm-5.2" },
    "build": { "model": "openrouter/deepseek/deepseek-v4-flash-0731" }
  }
}
```

- **PLAN = GLM 5.2** — raisonnement et plans solides ;
- **BUILD = DeepSeek V4 Flash 0731** — génération de code rapide et fiable.

> Identifiants exacts des modèles : [openrouter.ai/models](https://openrouter.ai/models).

## Auteur

[agileohdain](https://github.com/agileohdain)
