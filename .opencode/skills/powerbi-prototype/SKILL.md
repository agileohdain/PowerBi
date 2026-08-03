---
name: powerbi-prototype
description: Génère des maquettes de dashboards Power BI haute-fidélité (canevas 16:9, bandeau/fond en CSS, cartes KPI, slicers, visuels ECharts, navigation deux-niveaux) en HTML/Tailwind/ECharts auto-suffisant. Déclencheur principal : la commande /maquette suivie du nom du client (ex. "/maquette Veloh"). Use when the user wants to create a Power BI dashboard mockup for a client — e.g. a slash command /maquette, or natural phrasing like "maquette power bi", "crée la maquette", "nouvelle maquette client". Le corps du skill décrit le processus complet (confirmation nom, création du dossier client sans logo, dépôt logo/données/CLIENT.md rempli, vérification de complétude avec arrêt et questions).
---

## Ce que je fais
Je produis des maquettes de dashboards Power BI en HTML auto-suffisant, fidèles au
langage visuel Power BI (canevas 16:9 fixe, bandeau et fond dessinés en CSS,
cartes KPI, slicers, graphiques ECharts, navigation à deux niveaux).

**Flux de démarrage** (déclenché par la commande `/maquette <Nom>`) :
1. Le **déclencheur est la commande `/maquette`** suivie du nom du client (ex.
   `/maquette Veloh`). Le nom vient de l'argument de la commande ; si absent,
   je le demande. La **casse est respectée telle quelle**
   (majuscules/minuscules), **je ne propose pas de nom**.
2. Je **confirme le nom** par écrit : « Est-ce bien le client « X » ? — Oui /
   Modifier » (l'utilisateur peut corriger). **Je ne crée rien tant que le nom
   n'est pas confirmé.**
3. **Garde client existant** : si `clients/<Nom>/` existe déjà, je demande quoi
   faire (régénérer la maquette de ce client, ou modifier le nom) avant de créer
   quoique ce soit.
4. Si l'utilisateur est en mode **PLAN**, je lui demande de se mettre en
   mode **BUILD** une seule fois (pas de retour PLAN par la suite). Tout le
   reste du processus se déroule en BUILD.
5. Je **crée automatiquement le dossier** `clients/<client>/` (casse exacte)
   avec `CLIENT.md` (copie du template, nom pré-rempli). **Je ne crée aucun
   logo**.
6. Je **demande de déposer** dans `clients/<client>/` : le **logo** `logo.png`,
   les **données** `donnees.xlsx` **et le `CLIENT.md` rempli**. Je m'arrête pour
   attendre. Je **ne génère jamais** les données ni le logo.
7. Une fois le dépôt confirmé, je **parcours `CLIENT.md`** : si une information
   n'est **pas renseignée** (encore sous forme `<...>`), ou si `logo.png` /
   `donnees.xlsx` manquent, je **m'arrête** et je demande à l'utilisateur de
   saisir précisément les informations manquantes. Je re-vérifie en boucle
   jusqu'à ce que tout soit complet, puis je génère.
8. Je génère la maquette (Phase 4 ci-dessous).

Il n'y a **pas** de mode « Téléguidé » : `CLIENT.md` est **toujours rempli par
l'utilisateur** ; je me contente de le vérifier et de demander les champs
manquants.

## Phase 0 — Nom du client (déclencheur) + confirmation + création du dossier

1. **Le nom du client vient de l'argument de `/maquette`** (ex. `/maquette
   Veloh`). Si la commande est lancée sans argument, je demande le nom. La
   **casse est respectée telle quelle** (majuscules/minuscules) : le nom
   servira tel quel, avec la casse exacte, à nommer le dossier (ex. `Veloh` →
   `clients/Veloh/`). **Ne proposer aucun nom** — l'utilisateur saisit lui-même
   le client. Ne pas transformer en slug minuscule.
2. **Confirmer le nom** : reformuler par écrit, de façon claire et accueillante,
   « Est-ce bien le client « X » ? — Oui / Modifier ». L'utilisateur peut
   corriger ; boucler tant que le nom n'est pas validé. **Ne créer rien** tant
   que le nom n'est pas confirmé.
3. **Garde client existant** : si `clients/<Nom>/` existe déjà (par exemple le
   dossier d'un client déjà traité), demander via l'outil `question` :
   - **Régénérer la maquette de ce client** → sauter la création du dossier,
     vérifier le logo, les données et `CLIENT.md` (Phase 2), puis générer.
   - **Modifier le nom** → revenir à l'étape 2 (nouveau nom).
4. **Vérifier le mode** : si l'utilisateur est en mode **PLAN**, lui demander de
   se mettre en mode **BUILD** (nécessaire pour écrire le dossier). **Demander
   une seule fois, sans boucler plusieurs fois** — on ne revient pas en mode PLAN.
5. **Créer immédiatement le dossier `clients/<client>/`** (dès que le nom est
   confirmé et le dossier inexistant) avec `CLIENT.md` (copie de
   `templates/CLIENT.template.md`/`clients/_template/CLIENT.md`, nom du client
   pré-rempli sous `Brand Name` et en titre). **Ne créer aucun logo** (ni
   `logo.png` ni placeholder) — le logo est fourni par l'utilisateur.
6. **Demander de déposer les fichiers** dans `clients/<client>/` :
   - `logo.png` — le logo du client (de préférence **fond transparent**, PNG),
   - `donnees.xlsx` — les données source,
   - `CLIENT.md` — **rempli** par l'utilisateur (il édite la copie créée en
     étape 5, ou copie celle de `clients/_template/`).
   **S'arrêter** et attendre que ces éléments soient présents avant de continuer.

## Phase 1 — Vérification de `CLIENT.md`, du logo et des données

Après le dépôt, **vérifier la complétude** avant de générer :

1. **Logo (obligatoire)** : vérifier `clients/<client>/logo.png`. Si absent →
   **stop** et demander de déposer le logo du client dans `clients/<client>/`.
2. **Données (obligatoires)** : vérifier `clients/<client>/donnees.xlsx`. Si
   absent → **stop** et demander de déposer `donnees.xlsx`.
3. Lire `CLIENT.md` et **parcourir chaque champ** :
   - **Identité** : `Brand Name`, `Report Title`, `Report Subtitle` — aucun ne
     doit rester sous forme `<...>` (`<CLIENT_NAME>`, `<Titre du rapport>`,
     `<sous-titre / période>`).
   - **Couleurs** : `Primary / Banner Accent`, `Surface / Cards`,
     `Canvas Background`, `Card Frame Color`, `Border / Divider` — aucune ne
     doit rester sous forme `<...>` (`<Primary>`, `<Surface>`,
     `<Canvas Background>`, `<Card Frame>`, `<Border>`) ; attendre un code
     hexadécimal (ex. `#00A1B1`).
   - **Arbre de navigation** : chaque page/sous-page doit avoir un titre
     rempli et chaque `Libellé KPI` doit être renseigné (aucun `<Titre page N>`,
     `<Titre sous-page>`, `<Libellé KPI>` restant).
4. Si **un seul champ** est encore non rempli (marqueur `<...>`), ou si le
   logo / les données manquent → **s'arrêter** et demander à l'utilisateur de
   saisir **exactement** les informations manquantes (les lister clairement),
   en rappelant qu'il édite `CLIENT.md` lui-même. **Re-vérifier** en boucle
   jusqu'à complétude totale.
5. Propriété optionnelle : déduire `--text-primary` / `--text-secondary` selon
   la luminance du `Canvas Background` (clair → `#0F172A`/`#64748B` ; sombre →
   `#F1F5F9`/`#94A3B8`). Ce n'est pas un champ à vérifier.
6. **Fond `bg.*` (optionnel)** : si `bg.svg` **ou** `bg.png` est présent, il sera
   utilisé comme image de fond (prioritaire sur le rendu CSS). Sinon, le bandeau,
   la zone logo, le fond canevas et le pane filtres sont **dessinés en CSS** —
   ce n'est **pas bloquant**.

## Phase 2 — Données

Les **données sont toujours fournies par l'utilisateur** (déposées en Phase 0) —
le skill **ne génère jamais** `donnees.xlsx`. Lire le `donnees.xlsx` présent
dans `clients/<client>/` et en déduire le modèle de données (tables/feuilles),
les formules KPI, les colonnes source et la carte visuelle par page. (Vérifié en
Phase 1.)

## Phase 3 — Génération de la maquette HTML

1. Lire `CLIENT.md` (+ `references/POWERBI_LAYOUT.md` et
   `POWERBI_COMPONENTS.md`), et les données dans `donnees.xlsx` (model/filtres).
2. Produire `clients/<client>/maquette/index.html` — fichier **auto-suffisant** :
   - Tailwind via CDN, Apache ECharts via CDN.
   - Canevas 1920×1080 fixe, scaling CSS pour s'adapter au viewport (pas de scroll).
   - **Fond** :
     - Si `bg.svg`/`bg.png` présent → `background: url(./bg.svg) center/cover
       no-repeat` (adapter l'extension) ; **ne pas redessiner** le bandeau ni la
       zone logo en CSS (ils sont dans l'image).
     - Sinon → **dessiner en CSS** : bandeau haut (~97px) en `var(--primary)`
       avec zone logo (~245px) en `var(--surface)` contenant `logo.png`, fond
       canevas en `var(--canvas)`, pane filtres à gauche (fond `var(--canvas)`).
   - Variables CSS en `:root` lues depuis `CLIENT.md` :
     `--primary`, `--surface`, `--canvas`, `--border`, `--card-bg`,
     `--text-primary`, `--text-secondary`.
   - **Titre + sous-titre** positionnés par-dessus le bandeau (zone haute,
     ~0-97px), en `var(--surface)`.
   - Pane filtres à gauche avec **"Filtres" + icône en `var(--primary)`**.
   - Navigation L1 (pills) + L2 (liens texte) rendue depuis `CLIENT.md`.
   - Cartes KPI (avec état consolidation si flag présent) + visuels ECharts
     depuis la carte visuelle déduite de `donnees.xlsx`.
   - Logo `logo.png` affiché dans la zone logo (en haut à gauche).
   - Footer disclaimer "Données fictives".
3. Copier `logo.png` (+ `bg.*` si présent) à côté de `index.html` dans
   `maquette/` (la maquette doit être auto-portable).
4. Indiquer à l'utilisateur comment ouvrir le rendu (`start index.html`).

## Sources de données
- `CLIENT.md` — **fichier pilote, rempli par l'utilisateur** : identité de
  marque (couleurs via `--primary`/`--surface`/`--canvas`/`--border`/`--card-bg`),
  titre, arbre de navigation (pages / sous-pages / KPIs, flags `[En
  consolidation]`). Le skill vérifie qu'aucun marqueur `<...>` ne reste avant de
  générer.
- `donnees.xlsx` — **données source, toujours fournies par l'utilisateur**
  (déposées en Phase 0 ; le skill ne les génère jamais). Le skill en déduit le
  modèle de données, le glossaire KPI (formules) et la carte visuelle par page ;
  il s'appuie sur l'Excel seul, sans fichier de glossaire séparé.
- Exemple complet de référence : `clients/veloh/`.

## Règles de qualité
- **Ne jamais coder une couleur en dur** : toujours via `var(--xxx)`.
- Le **titre/sous-titre** sur le bandeau est TOUJOURS en `var(--surface)`.
- Le texte de pane "Filtres" + son icône est TOUJOURS en `var(--primary)`.
- Dériver `--text-primary`/`--text-secondary` selon la luminance de `--canvas`.
- Responsive : le canevas 1920×1080 est scaled pour s'adapter au viewport sans
  scrollbars, via `transform: scale(...)` calculé par un petit script.
- Une seule page de mockup pleinement validée par exécution ; les autres
  sous-pages sont des defaults cohérents.
