# PowerBi — Une maquette Power BI en 5 minutes, pas en 5 heures

Un **nom**, un **logo**, une **couleur primaire** — trois choses suffisent pour
obtenir un dashboard interactif, prêt à montrer en démo ou en pré-vente. Pas de
Power BI Desktop, pas de licence, **pas de données à préparer** : le skill
**propose**, vous **validez**.

## Quickstart

```powershell
opencode
# puis, dans opencode :
> /maquette MonClient
```

1. **Fournissez** `logo.png` (fond transparent) + la **couleur primaire** (hex,
   ex. `#FA8FF8`).
2. **Validez** le questionnaire guidé : domaine métier → modèle de données →
   navigation + KPIs → couleurs secondaires (nommées en clair) → titre.
3. Ouvrez le rendu : `start clients/MonClient/maquette/index.html`. **Fait.**

> Les **données fictives sont générées par le skill** (2 années civiles closes,
> ex. 2024–2025) — vous ne fournissez jamais d'Excel. Le skill ne crée jamais
> le logo, et ne lit jamais la maquette d'un autre client.

## Ce que vous obtenez

Un **`maquette/index.html`** auto-suffisant, fidèle au langage visuel Power BI :

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
└── maquette/
    └── index.html    ← le rendu, prêt à ouvrir
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
