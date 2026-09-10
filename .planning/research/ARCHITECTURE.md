# Architecture Research — Ensemble documentaire `docs/` et son harnais de vérification

**Domain:** Documentation utilisateur (FR) d'un produit Python 3.11+ / Flask / ortools **déjà livré**
— architecture d'un *système documentaire* : arborescence `docs/`, contrat d'index, ancrage de
chaque page sur le code réel, et contrôles `pytest` qui détectent la dérive.
**Researched:** 2026-09-10 (HEAD `19b5c96`, dernier commit fonctionnel `1d475f9`)
**Confidence:** **HIGH** sur l'architecture cible, les artefacts d'ancrage et les contrôles proposés —
chaque affirmation est vérifiée par **deux moyens indépendants** : lecture du code, puis **rendu réel
des écrans** via le client de test Flask (hors-ligne, sans réseau, sans écriture sous `.data/`).
**MEDIUM** sur l'ordonnancement des phases et le découpage des invariants (jugement d'ingénierie, pas
un fait de code).

**Note de méthode (seam de recherche).** `gsd_run query research-plan` a été exécuté : il propose
`context7` et `websearch`. Aucun de ces fournisseurs n'est disponible sur cet hôte — `gsd_run query
websearch` répond `{"available": false, "reason": "BRAVE_API_KEY not set"}`, aucun outil MCP
`context7` n'est exposé, et `.planning/config.json` déclare tous les drapeaux de recherche à `false`.
`gsd_run query classify-confidence` confirme `MEDIUM` (context7) et `LOW` (websearch). **Aucun
résultat n'a donc été inventé ni mis en cache** : toutes les sources de ce document sont des fichiers
du dépôt, lus ou exécutés localement (cf. § Sources). Pour une tâche *brownfield* dont la source de
vérité est le code du dépôt, c'est aussi la source la plus fiable.

**Périmètre.** Ce document arbitre l'**architecture** : quels composants documentaires existent,
quelle est leur frontière, quel artefact de code chacun doit refléter, quels contrôles prouvent
l'absence de dérive, et dans quel ordre les construire. Il ne re-décide pas le *layout* (posé dans
`.planning/research/STACK.md` §2) ni le *contenu* des parcours lecteur (`FEATURES.md`) : il les
consomme et les rend exécutables.

---

## 1. Standard Architecture

### 1.1 Vue d'ensemble

Le système à concevoir n'est pas le produit : c'est une **couche documentaire adossée au produit**,
avec une règle de sens unique et vérifiable.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│ A. PRODUIT (figé — aucune modification dans ce milestone)                     │
│                                                                               │
│   fetcher.py ──► dofus_stuff/cli.py            (argparse : commandes/options) │
│                  dofus_stuff/catalog.py        (catalogue mémoire)            │
│                  dofus_stuff/database.py       (.data/dofus.sqlite3)          │
│                  dofus_stuff/sync.py           (fenêtre 24 h, offline)        │
│                  dofus_stuff/optimize/**       (solveur, profil, reco)        │
│                  dofus_stuff/web/routes.py     (écrans, libellés, codes PGM)  │
│                  dofus_stuff/web/optimize_wizard.py (WIZARD_STEPS/TITLES)     │
│                  dofus_stuff/web/templates/screen.html                        │
│                  dofus_stuff/web/static/js/terminal.js (clavier, localStorage)│
└───────────────────────────────┬───────────────────────────────────────────────┘
                                │  LU (jamais modifié) : imports de symboles,
                                │  parse_args sans exécution, rendu via test client
                                ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│ B. ARTEFACTS D'ANCRAGE (le « contrat » que la doc doit refléter)               │
│                                                                               │
│  build_parser()            WIZARD_STEPS / STEP_TITLES        CHECK_INTERVAL_  │
│  CLASSES / ELEMENTS        SLOT_GROUP_LABELS                 SECONDS = 86400  │
│  codes PGM (MNU-01, …)     libellés des écrans rendus        DB_NAME, ITEM_   │
│  messages d'erreur flash   touches du clavier (terminal.js)  KINDS            │
└───────────────────────────────┬───────────────────────────────────────────────┘
                                │  RÉDIGÉ POUR (prose libre, libellés verbatim)
                                ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│ C. CONTRAT DOCUMENTAIRE  docs/                                                │
│                                                                               │
│   sommaire.md  ◄── index unique : liste exhaustive des pages, labels = H1     │
│     ├─ installation.md      ├─ cli.md              ├─ depannage.md            │
│     ├─ parcours-simplifie.md├─ base-locale.md      └─ glossaire.md            │
│     └─ wizard-avance.md                                                       │
│   (chaque page : H1 unique, ligne [← Sommaire](sommaire.md), liens relatifs   │
│    fichier-à-fichier, bloc « Source de vérité », libellés verbatim)           │
│   README.md ──► « Documentation utilisateur » ──► docs/sommaire.md            │
│   GUIDE_WIZARD.md ──► aiguillage corrigé ──► docs/wizard-avance.md            │
└───────────────────────────────┬───────────────────────────────────────────────┘
                                │  RELU PAR
                                ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│ D. HARNAIS DE VÉRIFICATION  tests/  (pytest seul, zéro dépendance nouvelle)   │
│                                                                               │
│   conftest.py            + fixture docs_dir  (racine du dépôt + docs/)        │
│   test_docs_structure.py   lien interne résolu · index exhaustif · H1 ·       │
│                            absence de renvois obsolètes · UTF-8 · rubriques   │
│   test_docs_code_anchor.py commandes/options CLI réellement parsables ·       │
│                            libellés de flux & d'étapes rendus réellement      │
└───────────────────────────────┬───────────────────────────────────────────────┘
                                │  DECLENCHEUR
                                ▼
                        `pytest` (136 tests verts aujourd'hui)
                        → toute dérive code→doc produit un test ROUGE
                          qui nomme le document fautif
```

### 1.2 Règle de sens (la décision structurante)

**Le code est la source de vérité ; la documentation est le reflet vérifié ; le test est le juge.**
Corollaire opérationnel, hérité de `PROJECT.md` : *si la doc et le code divergent, on corrige la doc*,
jamais `dofus_stuff/**`. Cela donne une architecture **unidirectionnelle**, sans boucle de rétroaction
sur le produit : le harnais de tests *observe*, il ne modifie rien.

### 1.3 Responsabilités des composants et frontières

| Composant | Responsabilité (ce qu'il possède) | Ne fait pas | Communique avec |
|-----------|-----------------------------------|-------------|-----------------|
| `docs/sommaire.md` | **L'index unique** : liste exhaustive des pages, un label par page (= son H1), parcours conseillé en 3 étapes | Ne décrit aucun écran ni aucune commande (pas de contenu dupliqué) | Toutes les pages `docs/*.md` (liens), `README.md` (entrant), `test_docs_structure.py` (exhaustivité) |
| `docs/installation.md` | Le trajet « zéro → premier lancement » : prérequis, installation, preuve que ça marche (CLI + web), `pytest` | N'explique pas le wizard ni la base locale en profondeur (renvois) | `pyproject.toml`, `dofus_stuff/web/__main__.py`, `README.md` |
| `docs/parcours-simplifie.md` | Le flux **classe → éléments → niveau** et la lecture du résultat | Ne décrit pas les 9 écrans avancés (renvoi vers `wizard-avance.md`) | `dofus_stuff/web/routes.py` (`optimize_quick`, `menu`), `dofus_stuff/optimize/recommend.py` |
| `docs/wizard-avance.md` | **Source unique** du wizard : 9 étapes, formats d'édition, commandes, sauvegardes, export Dofusbook | Ne re-décrit pas le menu principal ni l'installation (renvois) | `dofus_stuff/web/optimize_wizard.py`, `routes.py`, `terminal.js`, `screen.html` |
| `docs/cli.md` | La surface CLI : sous-commandes, options globales, options `optimize`, sortie de `db status` | Ne re-décrit pas l'installation (renvoi) ; ne présente pas le parseur de ligne compacte comme une commande (il n'est branché sur aucune sous-commande) | `dofus_stuff/cli.py` (`build_parser`, `_print_db_status`) |
| `docs/base-locale.md` | Le stockage local : `.data/dofus.sqlite3`, hors-ligne par défaut, fenêtre 24 h, catégories, écrans base | Ne donne **aucune valeur volatile** (nombre d'objets, version, horodatage) | `dofus_stuff/database.py`, `dofus_stuff/sync.py`, `dofus_stuff/api.py`, `routes.py` (`DB-01..DB-04`) |
| `docs/depannage.md` | Symptôme → cause → geste, pour les erreurs réellement produites par le code | N'introduit aucune commande qui n'existe pas dans le parseur | Tous les précédents (renvois) ; messages d'erreur du code |
| `docs/glossaire.md` | Le vocabulaire Dofus **et** le vocabulaire outil, trié | N'est pas un index (c'est `sommaire.md`) | `model/solver_spec.py` (B/P/C/W, PA/PM/PO), `optimize/recommend.py` (éléments), `optimize_wizard.py` (slots) |
| `README.md` | Point d'entrée produit + section « Documentation utilisateur » (DOCS-02) | Ne duplique pas la doc utilisateur ; ne renvoie plus vers une page périmée | `docs/sommaire.md` (sortant), `pyproject.toml` (`readme = "README.md"`) |
| `GUIDE_WIZARD.md` | **Aiguillage** : « ce guide est déplacé », arborescence de menus corrigée, lien vers `docs/wizard-avance.md` | N'est plus une seconde description concurrente du wizard | `docs/wizard-avance.md` |
| `tests/conftest.py` | Les fixtures : `docs_dir` (nouvelle), plus `catalog` / `app` / `client` (existantes) | Ne contient aucune assertion | Les deux modules de tests de doc, les tests web existants |
| `tests/test_docs_structure.py` | Les invariants **internes à la doc** : liens, index, H1, UTF-8, absence de renvois obsolètes, rubriques obligatoires | Ne lit **aucun** code Python du produit | `docs/**`, `README.md`, `GUIDE_WIZARD.md` (disque uniquement) |
| `tests/test_docs_code_anchor.py` | Les invariants **doc ↔ code** : commandes CLI réellement parsables, libellés réellement rendus, chemins des blocs « Source de vérité » | Ne lance **jamais** `main()`, ne contacte **aucun** réseau, n'ouvre **jamais** `.data/dofus.sqlite3` du dépôt | `dofus_stuff.cli`, `dofus_stuff.web.*`, `dofus_stuff.sync`, `terminal.js` (texte), `docs/**` |

**Frontière clé n° 1 — structure vs ancrage.** Les deux modules de tests ne doivent pas se mélanger :
`test_docs_structure.py` est *auto-suffisant* (il ne lit que des fichiers Markdown ; il reste évaluable
même sans `ortools`) ; `test_docs_code_anchor.py` *importe le produit*. Cette séparation rend le
diagnostic immédiat : échec de structure = problème de doc ; échec d'ancrage = divergence code/doc ou
symbole renommé.

**Frontière clé n° 2 — lecture par symbole, pas par texte.** Pour tout code **importable**, le harnais
importe le symbole (`build_parser`, `WIZARD_STEPS`, `STEP_TITLES`, `CHECK_INTERVAL_SECONDS`) et compare
des valeurs. Il ne grep pas les `.py` : un `grep` resterait vert après un renommage de fonction. Seul
`terminal.js` (non importable depuis Python) est lu **comme texte**, avec des motifs ciblés
(`key === "F3"`, `key === "Escape"`, `SAVES_KEY = "dofus-stuff-machine.saves"`, `MAX_SAVES = 20`),
parce qu'il n'existe aucune autre voie.

---

## 2. Recommended Project Structure

```
dofus-stuff-machine/
├── README.md                          # + section « Documentation utilisateur » (§3.4)
├── GUIDE_WIZARD.md                    # réduit à un aiguillage corrigé (DOCS-10)
├── docs/
│   ├── sommaire.md                    # INDEX UNIQUE (DOCS-01) — pivot édité par toutes les phases doc
│   ├── installation.md                # DOCS-03
│   ├── parcours-simplifie.md          # DOCS-04
│   ├── wizard-avance.md               # DOCS-05 (contenu migré de GUIDE_WIZARD.md)
│   ├── cli.md                         # DOCS-06
│   ├── base-locale.md                 # DOCS-07
│   ├── depannage.md                   # DOCS-08
│   └── glossaire.md                   # DOCS-09
├── tests/
│   ├── conftest.py                    # PIVOT : + fixture `docs_dir` (édité une seule fois)
│   ├── test_docs_structure.py         # DOCS-01, 02, 08, 09, 10, 11
│   ├── test_docs_code_anchor.py       # DOCS-06, 07, 12 (+ chemins des blocs Source de vérité)
│   └── (6 modules existants inchangés : test_web, test_screens, test_recommend, …)
└── dofus_stuff/                       # INTOUCHÉ
```

### 2.1 Rationale de structure

- **`docs/` à plat (pas de sous-dossier).** 8 fichiers : un niveau rend l'exhaustivité de l'index
  triviale à lire et à tester. Les sous-dossiers deviendraient utiles au-delà de ~15 pages (§8) ; le
  test d'exhaustivité est écrit **récursif** dès maintenant (`Path.rglob("*.md")`) pour ne pas avoir à
  le réécrire le jour où un sous-dossier apparaît.
- **`docs/` à la racine, hors paquet.** Aucune publication n'est autorisée ; embarquer la doc dans le
  wheel (`package-data` ou déplacement sous `dofus_stuff/`) ne servirait aucun consommateur et
  toucherait au packaging. `.gitignore` n'ignore pas `docs/` (vérifié) : la doc est versionnée.
- **Noms de fichiers ASCII kebab-case, contenu accentué.** Le dépôt est développé sous Windows
  (`C:/Users/...`, CRLF observés) : un système de fichiers insensible à la casse face à un git sensible
  transforme un renommage « casse seule » en piège. Décision déjà prise en `STACK.md` §2.1 —
  l'architecture s'y conforme.
- **Un fichier = un thème = une exigence DOCS.** C'est ce découpage qui permet l'assertion « ce libellé
  doit être **dans ce fichier** », donc un message d'échec actionnable (« ajouter
  `AVANCE : personnaliser les réglages` dans docs/parcours-simplifie.md »).
- **Deux modules de tests, pas un.** Même granularité que les modules existants (un module par
  famille) ; la séparation structure/ancrage matérialise la frontière n° 1 du §1.3.

---

## 3. Le contrat d'index (`docs/sommaire.md`) — spécification

L'index est le seul composant dont **toutes** les pages dépendent : c'est le pivot le plus sensible du
milestone. Contrat explicite :

| # | Règle | Pourquoi |
|---|-------|----------|
| I1 | **Un seul index** : `docs/sommaire.md`. Interdits : `docs/index.md`, `docs/README.md`, `docs/00-index.md` | Deux index concurrents reproduisent exactement la dérive constatée entre `README.md` et `GUIDE_WIZARD.md` |
| I2 | Le sommaire **liste chaque page livrée** par un lien relatif (`](installation.md)`), et **rien d'autre** ne doit exister sous `docs/` (fichier non listé ⇒ test rouge) | Exhaustivité bidirectionnelle : ni orphelin, ni lien mort |
| I3 | Le **label** de chaque entrée du sommaire est **le H1 de la page, mot pour mot** | Rend la table des matières vérifiable sans heuristique |
| I4 | `README.md` pointe **une fois** vers `docs/sommaire.md` via une section « Documentation utilisateur » | DOCS-02 ; un point d'entrée unique côté produit |
| I5 | Chaque page `docs/*.md` (sauf le sommaire) commence par le H1 puis la ligne `[← Sommaire](sommaire.md)` | Navigation fichier-à-fichier homogène, testable |
| I6 | Le sommaire se termine par un **parcours conseillé** en 3 étapes : installation → parcours simplifié → glossaire | Un index exhaustif n'est pas pour autant un parcours |
| I7 | Un fichier n'est **jamais** cité par un chemin absolu, une ancre ou une URL `file://` | Voir §3.1 |

### 3.1 Contrat de liens (le sous-contrat qui évite 80 % des faux positifs)

- **Liens relatifs, de fichier à fichier** : `](installation.md)`, `](../README.md)`.
- **Aucune ancre** : `](installation.md#prerequis)` est **rejeté** par le test. Raison : l'algorithme de
  slug GitHub (minuscules, ponctuation supprimée, espaces → `-`, déduplication `-1`) devrait être
  réimplémenté côté test — source de faux négatifs et de réécritures. À 8 pages, la navigation
  fichier-à-fichier suffit.
- **Aucun chemin absolu** : `](/docs/…)`, `](C:\…)`, `](file://…)` rejetés.
- **Aucun lien externe vérifié par test** : `api.dofusdu.de`, `docs.dofusdu.de`, `dofusbook.net`
  restent du texte. Le mode hors-ligne est la politique par défaut du projet ; un test qui sort sur le
  réseau échouerait pour une cause étrangère au dépôt.

### 3.2 Contrat de contenu qui rend l'ancrage possible

1. **Bloc « Source de vérité » en tête de chaque page** — la page *déclare* l'artefact qu'elle reflète :

   ```markdown
   > **Source de vérité :** `dofus_stuff/web/routes.py` (`optimize_quick`, `menu`),
   > `dofus_stuff/web/optimize_wizard.py` (`WIZARD_STEPS`, `STEP_TITLES`)
   > **Ancrage vérifié par :** `tests/test_docs_code_anchor.py::test_libelles_parcours_simplifie`
   ```

   Règle vérifiable, zéro dépendance : **tout jeton entre backticks finissant par `.py` doit exister
   sur disque** relativement à la racine. Un fichier renommé ou déplacé casse le test.
2. **Libellés d'écran et commandes reproduits verbatim** (en backticks ou bloc de code) ; la prose qui
   les entoure est libre. C'est ce qui autorise une comparaison **normalisée** (accents, casse, tirets
   ignorés) sans fragilité typographique.
3. **Aucune valeur volatile** : ni nombre d'objets, ni version de jeu, ni horodatage de dernier check.
   On documente le **format** de la sortie (`Fichier :`, `Version jeu :`, `Dernier check : il y a Xh`,
   `Entrées :`, `Par catégorie :`) et on laisse `db status` produire les chiffres.
4. **UTF-8 strict, sans BOM**, ligne vide finale, aucun marqueur de brouillon (`TODO`, `À COMPLÉTER`,
   `Lorem`).

### 3.3 Contrat de nomenclature des tests

- Noms de fonctions **en anglais**, docstrings **en français** — convention observée dans les modules
  existants (`test_menu_option_4_optimize` avec docstring française). Les tests de doc s'y conforment.
- Localisation : racine du dépôt via `Path(__file__).resolve().parents[1]` (les tests vivent dans
  `tests/`, un niveau sous la racine — vérifié). Les tests restent donc exécutables depuis n'importe
  quel répertoire courant, comme les tests actuels qui s'appuient sur `pythonpath = ["."]`.

### 3.4 Entrée `README.md` (DOCS-02) et sort de `GUIDE_WIZARD.md` (DOCS-10)

- `README.md` reçoit une section « Documentation utilisateur » juste après la phrase d'introduction et
  **avant** `## Base locale Dofus`, avec un lien vers `docs/sommaire.md` et la liste des 7 pages. La
  ligne 59 actuelle (`**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)`) devient un renvoi vers
  `docs/wizard-avance.md` : `README.md` est le `readme` déclaré du paquet (`pyproject.toml`), il doit
  rester le point d'entrée unique et ne plus envoyer vers une page périmée.
- `GUIDE_WIZARD.md` est réduit à un **aiguillage d'une quinzaine de lignes** : titre, phrase « ce guide
  a été déplacé », arborescence de menus **corrigée** en bloc de code, lien vers
  `docs/wizard-avance.md`. Le contenu détaillé migre dans `docs/wizard-avance.md`, qui devient la
  **source unique** ; deux descriptions concurrentes du même parcours sont précisément la cause de la
  désynchronisation constatée.

---

## 4. Ancrage : quelle page reflète quel artefact

C'est la table de référence du milestone. Chaque cellule « source de vérité » nomme un artefact
**réellement présent** (lu et, pour les écrans, rendu) ; chaque cellule « contrôle » nomme le test qui
le lit.

| Document | Source de vérité (artefact réel) | Contrôle qui le lit |
|----------|----------------------------------|---------------------|
| `docs/sommaire.md` | L'ensemble des fichiers `docs/**/*.md`, le H1 de chacun, et la section « Documentation utilisateur » de `README.md` | `test_docs_structure.py` : exhaustivité bidirectionnelle, H1 ↔ label |
| `docs/installation.md` | `pyproject.toml` (`requires-python = ">=3.11"`, `[project.scripts]` : `dofus-stuff`, `dofus-stuff-web`, extra `dev` = `pytest>=8.0`, `[tool.pytest.ini_options]`) ; `dofus_stuff/web/__main__.py::build_parser` (`--data-dir`, `--offline`/`--no-offline`, `--online`, `--timeout`, `--host` (127.0.0.1), `--port` (5000), `--debug`) ; `dofus_stuff/web/__init__.py` (`DOFUS_DATA_DIR`, `DOFUS_OFFLINE` défaut vrai, `DOFUS_TIMEOUT`, `DOFUS_SECRET_KEY`) ; `dofus_stuff/__main__.py` | `test_docs_code_anchor.py::test_web_entry_flags_documented`, `::test_source_of_truth_paths_exist` |
| `docs/parcours-simplifie.md` | `dofus_stuff/web/routes.py` : `menu` (`MNU-01`, libellés `1. RECHERCHE D'OBJETS` … `5. SYSTEME`), `menu_post` (`"4"` → `optimize_entry`), `optimize_quick` (`steps = ("classe", "elements", "niveau")`, `pgm="OPT-SIMPLE"`, titre `** RECOMMANDATION DE STUFF **`, `VOTRE STUFF EN 3 CHOIX`, `1/3 - Quelle est votre classe ?`, `2/3 - Quels éléments privilégier ?`, `3/3 - Quel est votre niveau ? (1 à 200)`, `AVANCE : personnaliser les réglages`, `ENTREE=CALCULER`, messages `Saisissez le nom ou le numéro de votre classe.` / `Exemple : feu, terre air, ou multi.` / `Saisissez un niveau entre 1 et 200.`) ; `dofus_stuff/optimize/recommend.py` (`CLASSES` = 19 noms, `ELEMENTS` = terre/feu/eau/air) | `test_docs_code_anchor.py::test_menu_labels_documented`, `::test_libelles_parcours_simplifie` |
| `docs/wizard-avance.md` | `dofus_stuff/web/optimize_wizard.py` : `WIZARD_STEPS` (9), `STEP_TITLES`, `SLOT_GROUP_LABELS`, `TYPE_FILTER_LABELS`, `RESISTANCE_STATS`, `DAMAGE_STATS`, `MISC_STATS`, `body_items` (`+ID` / `-ID` / `!ID` / `CLEAR`), `body_recap` (`GO = LANCER`, `RESET = REINITIALISER`, `1-8 = RETOUR ECRAN`, `SAVES = STUFFS SAUVEGARDES`) ; `routes.py::_wizard_edit_screen` (`FORMAT : BASE POINTS CIBLE POIDS`, `FORMAT : BASE EXO CIBLE POIDS`, `NOUVELLE VALEUR (ENTREE VIDE = ANNULER) :`) ; `terminal.js` (`SAVES_KEY`, `MAX_SAVES = 20`, touches `F3`/`Escape`/`F7`/`F8`/`PageUp`/`PageDown`) ; `templates/screen.html` (`data-f3-url`, `data-esc-url`, `data-f7-url`, `data-f8-url`, `data-mode`) | `test_docs_code_anchor.py::test_etapes_wizard_documentees`, `::test_commandes_wizard_documentees`, `::test_touches_clavier_documentees` |
| `docs/cli.md` | `dofus_stuff/cli.py::build_parser` (sous-commandes `version`, `self-test`, `search`, `item`, `list`, `optimize`, `db` et alias `cache` ; options globales `--timeout`, `--data-dir`, `--force-sync`, `--offline` ; options `optimize` ; sous-commandes `status`/`sync`/`clear` + alias muets `stats`/`fill`) ; `_print_db_status` ; `profile_input.prompt_optimize_interactive` (prompts `Niveau [demo] :`, `Jets (min|average|max) [average] :`, `Caractéristique(s) à maxer (ex: intelligence) :`) ; `fetcher.py` (shim) | `test_docs_code_anchor.py::test_commandes_cli_documentees`, `::test_options_globales_documentees`, `::test_exemples_cli_analysables` |
| `docs/base-locale.md` | `dofus_stuff/database.py` (`DB_NAME = "dofus.sqlite3"`, `DEFAULT_DATA_DIR`, `ITEM_KINDS` = equipment/resources/consumables/quest/cosmetics/mounts/sets, tables `meta` et `items`) ; `dofus_stuff/sync.py` (`CHECK_INTERVAL_SECONDS = 24 * 60 * 60`, actions `skip`/`touch`/`sync`, `Base locale vide et --offline : impossible de synchroniser`) ; `dofus_stuff/api.py` (`BASE_URL`, `DEFAULT_TIMEOUT = 15`, `SYNC_TIMEOUT = 120`, `SYNC_SOURCES`) ; `routes.py` (`DB-01`..`DB-04`, `FICHIER :`, `VERSION JEU :`, `DERNIER CHECK : IL Y A XH`, `ENTREES :`, `PAR CATEGORIE :`, `OPERATION DESTRUCTIVE`, `CETTE OPERATION CONTACTE L'API DOFUSDUDE`) | `test_docs_code_anchor.py::test_base_locale_documentee`, `::test_db_status_fields_documented` |
| `docs/depannage.md` | Messages d'erreur réellement produits : `routes.py` (`OPTION INVALIDE — SAISIR 1 A 5`, `ID INVALIDE — ENTIER ATTENDU`, `SAISIE REQUISE`, `AUCUN RESULTAT`), `catalog.py` (`Équipement introuvable : #…`, `Panoplie introuvable : #…`), `sync.py` (base vide + `--offline`), `cli.py` (`--offline incompatible avec db sync`), `terminal.js` (`AUCUN SLOT SAUVEGARDE — RE-SAUVEGARDER DEPUIS UN RESULTAT`, `ECHEC LOCALSTORAGE (QUOTA ?)`, reprise du focus), pagination `PAGE x/y` (`_screen` + `screens.py`) | `test_docs_structure.py::test_rubriques_depannage_presentes` + `test_docs_code_anchor.py::test_messages_erreur_ancres` (le message existe dans le code **et** dans la doc) |
| `docs/glossaire.md` | `model/solver_spec.py` (`MAIN_CARACS`, `EXO_STATS = ("PA", "PM", "Portée")`, `StatGoal` : champs `base` / `points` / `target` / `weight`, docstring « (+ exo pour PA/PM/PO, scroll = parchemins) », `SLOT_GROUPS`) ; `optimize/recommend.py` (`ELEMENTS`) ; `cli.py` (`--jet` ∈ `min`, `average`, `max`) | `test_docs_structure.py::test_glossaire_entrees_presentes` |

**Lecture utile pour le roadmap.** Chaque page a *un* propriétaire de contenu et *des* artefacts
d'ancrage identifiés ; toute exigence est couverte soit par une comparaison au code, soit — pour
DOCS-08 et DOCS-09, qui n'ont pas d'équivalent littéral dans le code — par une assertion explicite de
**présence de rubriques/entrées**. L'absence d'ancrage code y est donc *déclarée*, pas dissimulée.

---

## 5. Architectural Patterns

### Pattern 1 — Index unique + exhaustivité bidirectionnelle

**What:** un seul sommaire ; l'ensemble des liens sortants du sommaire doit être **égal** à l'ensemble
des fichiers `docs/**/*.md` (moins le sommaire lui-même).
**When:** dès que `docs/` contient plus d'un fichier.
**Trade-offs:** (+) supprime la classe de bugs « page créée mais jamais indexée » **et** « lien mort »
avec une seule assertion lisible ; (−) tout fichier déposé dans `docs/` fait échouer la suite — c'est
voulu (aucun brouillon en zone versionnée).

```python
_LINK = re.compile(r"\[(?P<label>[^\]]*)\]\((?P<target>[^)\s]+)\)")

def _docs_pages(docs_dir: Path) -> set[str]:
    return {p.name for p in docs_dir.rglob("*.md") if p.name != "sommaire.md"}

def _sommaire_targets(sommaire: Path) -> set[str]:
    return {
        m.group("target")
        for m in _LINK.finditer(sommaire.read_text(encoding="utf-8"))
        if not _is_external_or_anchor(m.group("target"))
    }

def test_sommaire_est_exhaustif(docs_dir: Path) -> None:
    """Aucun document orphelin, aucun lien mort dans le sommaire."""
    assert _sommaire_targets(docs_dir / "sommaire.md") == _docs_pages(docs_dir)
```

### Pattern 2 — Séparer invariant « auto-ajustant » et invariant « de complétude »

**What:** l'exhaustivité de type Pattern 1 valide **ce qui existe** (elle reste verte tout le
milestone) ; la **complétude** (« les 7 thèmes sont livrés ») est une assertion *distincte*, portée par
une liste épinglée.
**When:** dès qu'un milestone livre l'index avant ses pages — c'est notre cas.
**Trade-offs:** (+) le harnais est utile dès la première phase, sans test rouge « normal » ; (−) il
faut se souvenir d'introduire la liste épinglée à la fin — d'où la règle ci-dessous.

Sans cette séparation, un `assert files == links` purement bidirectionnel **passe** après suppression
simultanée d'une page et de sa ligne d'index : c'est le trou que comble la liste épinglée. Règle de
séquencement : **la liste épinglée est un critère de sortie de la dernière phase doc**, jamais de la
première.

```python
# Complétude exigée (DOCS-03 … DOCS-09). Introduite en fin de parcours (phase 6).
PAGES_REQUISES = {
    "installation.md", "parcours-simplifie.md", "wizard-avance.md",
    "cli.md", "base-locale.md", "depannage.md", "glossaire.md",
}
```

### Pattern 3 — Ancrage bidirectionnel (doc ↔ code), jamais à sens unique

**What:** deux assertions par sujet : (a) *ce que la doc cite existe dans le code* — sondes passées au
vrai parseur, libellés extraits du vrai rendu ; (b) *ce que le code expose est cité dans la doc* —
chaque commande réelle apparaît dans le fichier compétent.
**When:** sur toute surface à interface stable (CLI, libellés d'écran, constantes).
**Trade-offs:** (+) rend impossible **l'invention** (une option fantôme fait échouer `parse_args`) et
**l'oubli** (une option réelle non citée fait échouer la seconde assertion) ; (−) la liste des sondes
est un artefact à maintenir — prix assumé et **écrit dans le test**, pas caché.

```python
def test_exemples_cli_analysables() -> None:
    """Chaque exemple de docs/cli.md est réellement analysable par le parseur."""
    parser = build_parser()                      # symbole importé (ré-exporté pour tests/scripts)
    doc = (_DOCS / "cli.md").read_text(encoding="utf-8")
    for exemple in EXEMPLES_DOCUMENTES:          # ex. "--offline optimize --demo"
        assert exemple in doc, f"exemple absent de docs/cli.md : {exemple}"
        ns = parser.parse_args(shlex.split(exemple))   # parse_args seul : aucun effet de bord
        assert ns.command
```

**Garde-fous de sûreté (non négociables, hérités des règles projet) :** `parse_args` **jamais**
`main()` (donc aucun prompt interactif, aucune synchronisation Dofusdude) ; `db clear` / `cache clear`
sont *parsés* pour prouver que la doc cite une commande réelle, **jamais exécutés** ; aucun test
n'écrit, ne droppe ni ne supprime sous `.data/` ; aucune socket ouverte.

**Limite honnête de l'ancrage CLI.** Les sondes sont une liste statique : l'ajout futur d'une option
au parseur ne fera pas échouer le test tant que la sonde n'est pas ajoutée. L'alternative — introspecter
`parser._subparsers._group_actions[0].choices` (vérifié : renvoie bien
`['cache','db','item','list','optimize','search','self-test','version']`) — détecte automatiquement les
nouveautés **au prix d'une API privée d'`argparse`**. Recommandation : sondes statiques (robustes,
lisibles) pour le sens « la doc n'invente rien », et une assertion complémentaire de type « toute
option listée dans `EXEMPLES_DOCUMENTES` est documentée » pour le sens « rien n'est oublié ». Le
roadmap doit choisir explicitement ; les deux sont exécutables aujourd'hui (voir § Sources, sonde n° 1).

### Pattern 4 — Observer par rendu réel plutôt que par lecture de source

**What:** pour les libellés d'écran, on n'analyse pas `routes.py` : on *rend* l'écran avec le client de
test Flask déjà en place (`tests/conftest.py`) et on compare le texte réellement affiché.
**When:** tout ce qui est visible par l'utilisateur (titres, entrées de menu, messages d'erreur, codes
PGM, barre de statut).
**Trade-offs:** (+) couvre les transformations invisibles à la lecture — troncature à 18 caractères des
libellés de stats (`% Dommages aux sor…`), pagination, échappement HTML : exactement ce qu'un `grep`
sur le code source rate ; (−) le test dépend de la fixture `client`, donc de Flask et d'un catalogue en
mémoire — acceptable, la suite existante en dépend déjà (`136 passed in 1.82s`).

```python
def test_libelles_parcours_simplifie(client) -> None:
    """Les libellés du flux classe → éléments → niveau sont ceux réellement rendus."""
    ecran_1 = client.get("/optimize/quick/classe").data.decode()
    ecran_2 = client.post("/optimize/quick/classe", data={"cmd": "Cra"},
                          follow_redirects=True).data.decode()
    ecran_3 = client.post("/optimize/quick/elements", data={"cmd": "terre air"},
                          follow_redirects=True).data.decode()
    doc = _norm((_DOCS / "parcours-simplifie.md").read_text(encoding="utf-8"))
    rendus = {  # chaque libellé est épinglé sur l'écran où il est réellement rendu
        "1/3 - Quelle est votre classe ?": ecran_1,
        "2/3 - Quels éléments privilégier ?": ecran_2,
        "3/3 - Quel est votre niveau ? (1 à 200)": ecran_3,
        "AVANCE : personnaliser les réglages": ecran_2 + ecran_3,
    }
    for libelle, ecran in rendus.items():
        assert _norm(libelle) in _norm(ecran), f"libellé non rendu : {libelle}"
        assert _norm(libelle) in doc, f"libellé absent de docs/parcours-simplifie.md : {libelle}"
```

*Détail vérifié qui justifie ce pattern :* `POST /optimize/quick/classe` répond l'écran **2/3** (le
`follow_redirects` saute une étape), et non le 1/3. Une assertion naïve « 1/3 après avoir répondu à la
classe » échoue ; le 1/3 s'obtient par `GET /optimize/quick/classe`. Le test doit donc épingler chaque
libellé **sur l'écran où il est réellement rendu**, ce qui suppose de rendre réellement les écrans.

### Pattern 5 — Comparaison normalisée des libellés

**What:** normaliser **les deux côtés** avant comparaison : NFD + suppression des diacritiques +
`casefold` + `’`/`–`/`—` → `'`/`-` + espaces (dont insécables) écrasés.
**When:** à chaque comparaison « libellé de doc ↔ libellé rendu ».
**Trade-offs:** (+) insensible aux accents, à la casse et à la typographie — indispensable puisque le
code affiche `RECOMMANDATION DE STUFF`, `CARACTERISTIQUES`, `PA / PM / PO` **sans accents** quand la
prose française en est pleine, et que `GUIDE_WIZARD.md` utilise des apostrophes typographiques (`’`) là
où `routes.py` utilise `'` ; (−) ne détecte pas une faute d'accent *dans la doc* — acceptable, le
contrat est « le même libellé », pas « la même typographie ».

```python
def _norm(texte: str) -> str:
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    for src, dst in (("’", "'"), ("–", "-"), ("—", "-"), ("\u00a0", " ")):
        texte = texte.replace(src, dst)
    return " ".join(texte.casefold().split())
```

**Preuve d'exécution (sonde n° 2) :** `_norm("RECOMMANDATION DE STUFF")` → `recommandation de stuff` ;
`_norm("1/3 - Quelle est votre classe ?")` → `1/3 - quelle est votre classe ?`. Les deux libellés sont
bien retrouvés tels quels dans le HTML rendu (vérifié écran par écran).

### Pattern 6 — Contrat « Source de vérité » validé par existence de chemin

**What:** chaque page déclare ses artefacts dans un bloc connu ; le test extrait les jetons finissant
par `.py` et vérifie leur existence sur disque.
**When:** obligatoire en tête de chaque page `docs/`.
**Trade-offs:** (+) un renommage ou un déplacement de module casse la doc *avant* qu'un lecteur ne s'y
trompe, sans import ni exécution ; (−) ne vérifie pas que la page dit la vérité *sur* ce module — c'est
le rôle des Patterns 3 et 4. Les deux se complètent : **chemin** (le fichier existe) + **symbole** (le
contenu correspond).

### Pattern 7 — Isolation des tests de doc du produit « lourd »

**What:** les tests qui n'ont besoin que de texte (`test_docs_structure.py`) n'importent **rien** du
produit ; ceux qui vérifient le rendu utilisent la fixture `client` existante.
**When:** toujours — c'est cette séparation qui garde le diagnostic lisible et la suite rapide.
**Trade-offs:** (+) un échec de lien se lit « problème de doc » sans bruit Flask/ortools ; (−) deux
modules à maintenir au lieu d'un. Coût mesuré : la suite complète tourne en **1,82 s** avec 136 tests ;
les ajouts proposés restent dans cette enveloppe (lecture de fichiers + quelques requêtes de test
client), sans nouvelle dépendance.

---

## 6. Catalogue des contrôles d'intégrité

Chaque contrôle nomme l'artefact **réel** qu'il lit. La priorité indique l'ordre d'implémentation
conseillé (P1 = première phase, P4 = dernière).

### 6.0 Fixture partagée (`tests/conftest.py`)

```python
@pytest.fixture(scope="session")
def docs_dir() -> Path:
    """Racine du dépôt + dossier docs/ (les tests vivent un niveau sous la racine)."""
    return Path(__file__).resolve().parents[1] / "docs"
```

Pivot édité **une seule fois** (phase 1). Le fichier héberge déjà `catalog`, `app` et `client` :
aucune restructuration n'est nécessaire, seule une fixture s'ajoute.

### 6.1 `tests/test_docs_structure.py` — invariants internes (DOCS-01, 02, 08, 09, 10, 11)

| Prio | Test | Lit | Assertion | Exigence |
|------|------|-----|-----------|----------|
| P1 | `test_docs_tree_matches_contract` | `docs/**/*.md` (disque) | `docs/` existe et contient `sommaire.md` | DOCS-01 |
| P1 | `test_sommaire_est_exhaustif` | `docs/sommaire.md` + disque | cibles du sommaire **==** pages existantes (Pattern 1) | DOCS-01/11 |
| P1 | `test_tous_les_liens_relatifs_resolvent` | `README.md`, `GUIDE_WIZARD.md`, `docs/**/*.md` | chaque `](cible)` sans schéma ni `#` : `(source.parent / cible).exists()` | DOCS-11 |
| P1 | `test_aucun_lien_ancre_ni_absolu` | mêmes fichiers | aucune cible ne contient `#`, ne commence par `/`, `C:` ou un schéma `\w+:` | §3.1 |
| P1 | `test_h1_unique_et_label_conforme` | chaque page + sommaire | exactement un `^# ` par page ; texte normalisé == label du sommaire (Pattern 5) | DOCS-01 |
| P1 | `test_ligne_sommaire_presente` | chaque page ≠ sommaire | contient `](sommaire.md)` | §3 I5 |
| P1 | `test_readme_pointe_le_sommaire` | `README.md` | contient `](docs/sommaire.md)` | DOCS-02 |
| P1 | `test_utf8_sans_placeholder` | tous les `.md` de la doc | décodage UTF-8 **strict** (un fichier cp1252 lève) ; aucun `TODO` / `À COMPLÉTER` / `Lorem` | anti-brouillon |
| P2 | `test_aucun_renvoi_obsolete` | `README.md`, `GUIDE_WIZARD.md`, `docs/**` | normalisé : `3. OPTIMISATION DE STUFF` **absent** partout ; `4. OPTIMISATION DE STUFF` et `5. SYSTEME` présents dans les pages qui décrivent le menu ; motif `tapez\s+`?3`?\s+puis` absent | DOCS-10 |
| P3 | `test_rubriques_depannage_presentes` | `docs/depannage.md` | les 5 rubriques requises : base absente, saisie invalide, calcul long, clavier inactif (focus du champ), résultat paginé (`F8`) | DOCS-08 |
| P3 | `test_glossaire_entrees_presentes` | `docs/glossaire.md` | entrées requises : stuff, slot, solveur, poids, cible, ID Ankama, jet, exo, panoplie, dofus, trophée, prysmaradite | DOCS-09 |
| P4 | `test_pages_requises_livrees` | disque + `PAGES_REQUISES` | la liste épinglée est présente **et** indexée (Pattern 2) | complétude |

**Preuve que ce harnais attrape la désynchronisation constatée (et n'est pas décoratif) :**
`GUIDE_WIZARD.md:35` contient ``Tapez `3` puis **Entrée** pour ouvrir l’optimisation`` et
`GUIDE_WIZARD.md:40` contient `3. OPTIMISATION DE STUFF`, alors que `routes.py::menu` expose
`4. OPTIMISATION DE STUFF` et `5. SYSTEME`. Le contrôle P2 est donc **rouge avant correction** sur
l'état actuel du dépôt. Attention à la normalisation : les apostrophes de `GUIDE_WIZARD.md` sont
typographiques (`’`), pas ASCII — sans le remplacement du Pattern 5, le motif ne matche pas et le test
passe à tort.

### 6.2 `tests/test_docs_code_anchor.py` — invariants doc ↔ code (DOCS-06, 07, 12)

| Prio | Test | Lit (artefact réel) | Assertion |
|------|------|---------------------|-----------|
| P1 | `test_source_of_truth_paths_exist` | blocs `> **Source de vérité :**` de chaque page + disque | chaque jeton `` `…py` `` existe relativement à la racine (Pattern 6) |
| P1 | `test_web_entry_flags_documented` | `dofus_stuff/web/__main__.py::build_parser()` | `--data-dir --offline --online --timeout --host --port --debug` sont parsables **et** cités dans `installation.md` / `base-locale.md` |
| P1 | `test_source_de_verite_modules_importables` | les chemins cités dans les blocs | un chemin `.py` cité doit être **importable** (module du paquet `dofus_stuff`) ou explicitement hors paquet (`fetcher.py`) — évite de citer un fichier existant mais sans rapport |
| P2 | `test_commandes_cli_documentees` | `dofus_stuff/cli.py::build_parser()` | sondes `["version"]`, `["self-test"]`, `["search", "Cape"]`, `["item", "44"]`, `["list"]`, `["optimize", "--demo"]`, `["db", "status"]`, `["db", "sync"]`, `["db", "clear"]`, `["cache", "stats"]`, `["cache", "fill"]` : chacune **parse** et son nom figure dans `cli.md` (normalisé) |
| P2 | `test_options_globales_documentees` | `build_parser()` | `--timeout`, `--data-dir`, `--force-sync`, `--offline` parsables **devant** une sous-commande et cités dans `cli.md` |
| P2 | `test_options_optimize_documentees` | `build_parser()` (sous-parseur `optimize`) | chaque option de `LISTE_OPTIONS_OPTIMIZE` (constante du test, tenue en un seul endroit) parse sans erreur **et** est citée dans `cli.md` — sens « la doc n'invente aucune option » |
| P2 | `test_exemples_cli_analysables` | `shlex` + `build_parser()` + `docs/cli.md` | chaque exemple documenté apparaît verbatim dans `cli.md` **et** est analysable (Pattern 3) |
| P3 | `test_menu_labels_documented` | client Flask : `GET /` (rendu de `MNU-01`) | les 5 libellés du menu réel apparaissent dans `installation.md` + `parcours-simplifie.md` ; `3. OPTIMISATION DE STUFF` **absent** |
| P3 | `test_libelles_parcours_simplifie` | client Flask : `GET /optimize/quick/classe`, `POST …/classe`, `POST …/elements` + `docs/parcours-simplifie.md` | `1/3`, `2/3`, `3/3`, `AVANCE : personnaliser les réglages`, `VOTRE STUFF EN 3 CHOIX` + les 3 messages de validation réels : présents des **deux** côtés (Patterns 4 et 5) |
| P3 | `test_etapes_wizard_documentees` | `optimize_wizard.WIZARD_STEPS`, `STEP_TITLES` + `docs/wizard-avance.md` | chaque titre présent dans la doc, **dans l'ordre** de `WIZARD_STEPS`, et la doc annonce 9 écrans (`len(WIZARD_STEPS) == 9`) |
| P3 | `test_commandes_wizard_documentees` | `optimize_wizard.body_items` / `body_recap` + `routes.py::_wizard_edit_screen` (via rendu `OPT-WED` obtenu en posant `SESSION_WIZARD_EDIT` par `session_transaction`) | `+ID`, `-ID`, `!ID`, `CLEAR`, `GO`, `RESET`, `SAVES`, `FORMAT : BASE POINTS CIBLE POIDS`, `FORMAT : BASE EXO CIBLE POIDS` présents dans le code **et** dans `wizard-avance.md` |
| P3 | `test_identifiants_ecrans_documentes` | client Flask : `GET /` (`MNU-01`), `/system` (`SYS-01`), `/db` (`DB-01`), `/db/status` (`DB-02`), `/db/sync` (`DB-03`), `/db/clear` (`DB-04`), `/version` (`VER-01`), `/self-test` (`TST-01`), `/search` (`SRC-01`), `/item` (`ITM-01`), `/list` (`LST-01`), `/sets` (`PAN-01`), `/saves` (`SAV-01`), `/quit` (`END-01`), `/optimize/quick/classe` (`OPT-SIMPLE`) | chaque code PGM est réellement émis **et** cité dans la page qui décrit cet écran ; inverse : tout code PGM cité par la doc existe dans l'ensemble réel (aucun identifiant inventé) |
| P4 | `test_touches_clavier_documentees` | `terminal.js` (texte : `key === "F3"`, `key === "Escape"`, `key === "F7"`, `key === "F8"`, `key === "PageUp"`, `key === "PageDown"`) + `screen.html` (`data-f3-url`, `data-esc-url`, `data-f7-url`, `data-f8-url`) | les touches réellement câblées sont documentées dans `wizard-avance.md` (et `F3`/`ESC` dans `parcours-simplifie.md`) |
| P4 | `test_db_status_fields_documented` | `cli.py::_print_db_status` (libellés), `routes.py::db_status` (`DB-02`), `dofus_stuff/sync.py::CHECK_INTERVAL_SECONDS` | `Fichier :`, `Version jeu :`, `Dernier check :`, `Entrées :`, `Par catégorie :` et la fenêtre **24 h** figurent dans `base-locale.md` ; la doc ne contient **aucune** valeur volatile |

### 6.3 Ce que le harnais ne fait pas (frontières explicites)

| Interdit | Raison |
|----------|--------|
| Lancer `python fetcher.py …` / `main()` / `optimize_stuff()` | Effets de bord (prompt interactif, synchronisation réseau, écriture SQLite) ; `parse_args` suffit à prouver l'existence d'une commande |
| Ouvrir, lire ou écrire `.data/dofus.sqlite3` | Contrainte projet (lecture seule, jamais de `db clear` / drop) ; de plus une valeur volatile ne prouve aucun critère documentaire |
| Vérifier les liens externes (`api.dofusdu.de`, `dofusbook.net`) | Hors-ligne par défaut ; introduirait un échec réseau non imputable au dépôt |
| Comparer un rendu HTML octet à octet | Fragile aux accents/espaces ; l'objet du test est la doc, pas le rendu (Pattern 5 préféré) |
| Modifier `dofus_stuff/**` pour « aligner » la doc | Le périmètre est documentaire ; modifier le code changerait le produit |
| Vérifier le *fond* (la prose est-elle juste ?) | Non décidable automatiquement ; les contrôles prouvent l'**ancrage** (libellés, commandes, chemins), pas la véracité d'une explication — d'où l'exigence de rédiger depuis le code (§7) |

---

## 7. Data Flow

### 7.1 Flux d'écriture (comment un fait de code entre dans la doc)

```
lecture du code réel  ──►  rédaction de la page  ──►  bloc « Source de vérité »  ──►  test d'ancrage
   (Read / rendu)          (prose FR libre          (déclaration explicite           (assertion
                            + libellés verbatim)      de l'artefact)                   code ↔ doc)
```

Règle : **on n'écrit jamais une page sans avoir lu (ou rendu) l'artefact concerné dans la même
phase.** C'est ce qui évite la « doc d'un produit imaginaire » — le risque dominant identifié dans
`PROJECT.md`.

### 7.2 Flux de détection de dérive (le cœur de la solution)

```
développeur modifie routes.py (ex. libellé « 2/3 - … »)   ou   step ajouté à WIZARD_STEPS
        │                                                              │
        ▼                                                              ▼
            `pytest`  (suite unique, 136+ tests, ~2 s)
        │
        ├─ test_docs_structure.py     → vert (la doc reste cohérente avec elle-même)
        └─ test_docs_code_anchor.py   → ROUGE
                 message d'échec : « libellé absent de docs/parcours-simplifie.md : 2/3 - … »
        │
        ▼
   correction de la DOC dans le même commit  →  `pytest` vert
```

Propriété importante : le harnais **ne peut pas** corriger la doc, il nomme le document fautif. Le
cycle est donc : *rouge explicite → correction ciblée → vert*. C'est la réponse structurelle à la
désynchronisation constatée (flux simplifié `1d475f9` jamais répercuté dans `GUIDE_WIZARD.md`).

### 7.3 Flux de lecture du code par le harnais (sans effet de bord)

```
test_docs_code_anchor.py
   ├─ import dofus_stuff.cli            → build_parser()      → parse_args(argv)   (aucune exécution)
   ├─ import dofus_stuff.web.__main__   → build_parser()      → parse_args(argv)
   ├─ import dofus_stuff.web.optimize_wizard → WIZARD_STEPS, STEP_TITLES, SLOT_GROUP_LABELS, …
   ├─ import dofus_stuff.sync           → CHECK_INTERVAL_SECONDS
   ├─ fixture `client` (conftest)       → rendu réel des écrans → libellés, codes PGM, statuts
   └─ lecture texte de terminal.js      → motif `key === "…"`, `SAVES_KEY`, `MAX_SAVES`
```

Aucun nœud de ce graphe n'écrit sur disque, n'ouvre de socket, ni ne touche `.data/`.

### 7.4 Flux de lecture d'une page par un humain (contrainte de conception)

```
README.md  ──►  docs/sommaire.md  ──►  la page du besoin  ──►  [← Sommaire] pour revenir
                     │
                     └── parcours conseillé (3 étapes) : installation → parcours simplifié → glossaire
```

C'est ce trajet, et lui seul, que `test_readme_pointe_le_sommaire`,
`test_sommaire_est_exhaustif` et `test_ligne_sommaire_presente` protègent : un point d'entrée, un
index, un retour.

---

## 8. Ordre de construction et fichiers pivots

### 8.1 Fichiers pivots (dépendances partagées)

| Pivot | Pourquoi c'est un pivot | Contrainte de séquencement |
|-------|------------------------|----------------------------|
| `docs/sommaire.md` | **Chaque phase doc y ajoute une ligne** (Pattern 1 rend l'omission fatale) | Fichier **sérié** : une phase à la fois. Chaque plan de phase doit lister explicitement « ajouter l'entrée X dans `sommaire.md` » comme tâche à part entière, jamais comme effet de bord |
| `tests/conftest.py` | La fixture `docs_dir` sert aux deux modules de tests | Édité **une seule fois** (phase 1), jamais après |
| `tests/test_docs_structure.py` | Contrôle transversal de toutes les pages | Sérié : une phase ajoute ses contrôles à la fin du fichier |
| `tests/test_docs_code_anchor.py` | Contrôle transversal de toutes les pages | Sérié, même règle |
| `README.md` | Point d'entrée produit (DOCS-02) **et** cible du contrôle de renvois obsolètes | Touché en phase 1 (section + lien) et en phase 4 (ligne 59 vers `docs/wizard-avance.md`) — donc jamais en parallèle |
| `GUIDE_WIZARD.md` | Source de contenu **et** cible du contrôle DOCS-10 | Une seule phase propriétaire (phase 4) : migration du contenu, puis réduction à l'aiguillage |

Le dépôt suit `parallelization: true` côté GSD, mais **ces six fichiers restent séquentiels**. Les
phases peuvent paralléliser la *rédaction des pages* (chacune étant propriétaire d'un fichier `docs/`
distinct) ; elles ne peuvent pas paralléliser leurs entrées d'index ni les deux modules de tests.

### 8.2 Ordre de construction recommandé

| # | Livre | Contenu | Pivot(s) touché(s) | Exigences prouvées |
|---|-------|---------|--------------------|--------------------|
| **1** | Socle doc + harnais de structure | `docs/sommaire.md` + `docs/installation.md` (contenu réel, pas de brouillon) ; section « Documentation utilisateur » de `README.md` ; fixture `docs_dir` ; `tests/test_docs_structure.py` (P1) ; `tests/test_docs_code_anchor.py` avec P1 (chemins + entrée web) | **tous les pivots une première fois** | DOCS-01, DOCS-02, DOCS-03, DOCS-11 |
| **2** | CLI | `docs/cli.md` + entrée d'index + contrôles P2 CLI (`test_commandes_cli_documentees`, options globales, options `optimize`, exemples analysables) | `sommaire.md`, `test_docs_code_anchor.py` | DOCS-06 |
| **3** | Parcours simplifié | `docs/parcours-simplifie.md` + entrée d'index + P3 (`test_menu_labels_documented`, `test_libelles_parcours_simplifie`) | `sommaire.md`, `test_docs_code_anchor.py` | DOCS-04 |
| **4** | Wizard avancé + résorption de la dette `GUIDE_WIZARD` | `docs/wizard-avance.md` (contenu migré) ; `GUIDE_WIZARD.md` réduit à l'aiguillage ; `README.md` ligne 59 corrigée ; P2 structure (`test_aucun_renvoi_obsolete`) ; P3/P4 wizard | `sommaire.md`, `GUIDE_WIZARD.md`, `README.md`, `test_docs_*.py` | DOCS-05, DOCS-10 |
| **5** | Base locale | `docs/base-locale.md` + entrée d'index + P4 (`test_db_status_fields_documented`) | `sommaire.md`, `test_docs_code_anchor.py` | DOCS-07 |
| **6** | Dépannage + glossaire + complétude | `docs/depannage.md`, `docs/glossaire.md` + entrées d'index + P3 (`test_rubriques_depannage_presentes`, `test_glossaire_entrees_presentes`) + **P4 `test_pages_requises_livrees`** (liste épinglée, Pattern 2) | `sommaire.md`, les deux modules | DOCS-08, DOCS-09 |
| **7** | Clôture | parcours conseillé final du sommaire ; `pytest` complet vert ; vérification que `README.md` ne renvoie plus vers `GUIDE_WIZARD.md` pour l'usage produit | `sommaire.md`, `README.md` | DOCS-11/12 consolidés |

**Justifications de l'ordre :**

1. **Phase 1 d'abord** parce que l'index et la fixture sont les deux pivots dont tout dépend, et parce
   que les invariants P1 (liens, exhaustivité auto-ajustante, UTF-8) sont vérifiables dès deux pages.
2. **Phase 4 avant les autres pages de contenu** parce qu'elle **réduit la dispersion** : tant que
   `GUIDE_WIZARD.md` décrit encore le wizard en entier, deux sources concurrentes existent et toute
   correction peut être appliquée au mauvais endroit.
3. **La complétude (liste épinglée) en phase 6**, pas en phase 1 : sinon la suite est rouge tout le
   milestone pour une raison « normale », ce qui détruit la valeur de signal du harnais (Pattern 2).
4. **Le contrôle de renvois obsolètes (`test_aucun_renvoi_obsolete`) en phase 4**, au moment précis où
   `GUIDE_WIZARD.md` et `README.md` sont corrigés : il est rouge avant, vert après. L'introduire en
   phase 1 le laisserait rouge six phases — même problème de signal.
5. **CLI (phase 2) avant parcours simplifié (phase 3)** parce que `docs/installation.md` (phase 1) cite
   déjà des commandes : la phase 2 ferme la boucle d'ancrage CLI avant que la documentation d'usage ne
   s'appuie dessus.

### 8.3 Critères de sortie par phase (vérifiables)

- `pytest` vert **à la fin de chaque phase** (aucun test rouge « en attente » n'est acceptable).
- Les contrôles introduits dans la phase passent, et **au moins un** a été vu rouge sur l'état
  antérieur quand la phase corrige une dérive (phase 4). Une phase qui corrige sans jamais avoir vu
  rouge n'a pas prouvé que son test mordait.
- Le bloc « Source de vérité » de chaque page livrée cite des chemins existants (contrôle P1, introduit
  en phase 1 : il protège aussi les pages suivantes).
- Aucune phase ne modifie `dofus_stuff/**` (vérifiable par `git status --short` : seuls `docs/`,
  `README.md`, `GUIDE_WIZARD.md`, `tests/` apparaissent).

---

## 9. Considérations de montée en charge

| Échelle de doc | Ajustement d'architecture | Effet sur le harnais |
|----------------|--------------------------|----------------------|
| **8 pages (cible actuelle)** | `docs/` à plat, index unique | Les contrôles proposés sont ceux du §6 — rien à changer |
| **~15–25 pages** | Sous-dossiers thématiques (`docs/technique/`, `docs/guide/`) **à l'intérieur** de `docs/`, `sommaire.md` reste l'index unique | Le test d'exhaustivité est **déjà récursif** (`rglob`) : il fonctionne sans réécriture. Les cibles de liens du sommaire deviennent des chemins relatifs avec sous-dossier (`technique/cli.md`), ce que le contrôle de résolution gère déjà |
| **> 25 pages / plusieurs publics** | Envisager une séparation en deux index (usage / technique) | **Ne pas** ajouter de générateur de site : la publication reste hors périmètre. Un second index réintroduit le risque de dérive que l'architecture combat — à n'accepter qu'avec un test d'exhaustivité par index |

**Points de rupture, dans l'ordre où ils apparaissent :**

1. **`docs/sommaire.md` devient un point de conflit** dès que deux phases doc avancent en parallèle :
   premier point de friction (§8.1). Remède : index sérié, ou propriété exclusive de l'index à une phase.
2. **La liste des sondes CLI vieillit** si le parseur grandit sans que les sondes suivent : le test
   reste vert alors qu'une option n'est pas documentée. Remède documenté au §5 (Pattern 3, limite
   honnête) : décider explicitement entre sondes statiques et introspection `argparse`.
3. **Le nombre de contrôles d'ancrage web croît linéairement avec le nombre d'écrans** : chaque nouvel
   écran (`pgm`) et chaque libellé ajouté demande une assertion. Coût acceptable (rendu en mémoire,
   suite à ~2 s), mais le tableau de sondes du §6.2 doit rester **en un seul endroit** par famille
   (sinon la maintenance se disperse).

---

## 10. Anti-Patterns

### Anti-Pattern 1 — Deux index concurrents

**Ce qui se fait :** créer `docs/index.md` (ou `docs/README.md`) « pour la convention », en plus du
`sommaire.md` exigé.
**Pourquoi c'est faux :** deux tables des matières dérivent l'une de l'autre — exactement la
désynchronisation observée entre `README.md` et `GUIDE_WIZARD.md`, déplacée d'un cran.
**À faire à la place :** un seul `docs/sommaire.md`, référencé depuis `README.md` (§3 I1/I4).

### Anti-Pattern 2 — Documenter en lisant le code au `grep`, pas en le rendant

**Ce qui se fait :** rédiger le guide des écrans à partir des chaînes trouvées dans `routes.py`.
**Pourquoi c'est faux :** les libellés réellement affichés passent par `clip`/`wrap_line`/`paginate`
(`screens.py`) et sont **tronqués** (`% Dommages aux sor…`), et la mise en page décide de ce qui tombe
en page 2. Une relecture du code produit une doc plausible mais fausse — le risque nommé dans
`PROJECT.md`.
**À faire à la place :** rendre chaque écran avec la fixture `client` avant de le décrire, et épingler
les libellés par écran (Pattern 4).

### Anti-Pattern 3 — Test d'ancrage qui exécute le produit

**Ce qui se fait :** appeler `main(["optimize", …])` ou `optimize_stuff()` pour « prouver que la
commande existe ».
**Pourquoi c'est faux :** effets de bord réels — prompt interactif, synchronisation Dofusdude,
écriture SQLite. Un test de documentation deviendrait plus dangereux que le code qu'il vérifie, et
violerait les règles projet (hors-ligne, aucune écriture sous `.data/`).
**À faire à la place :** `build_parser().parse_args(argv)` uniquement (§5 Pattern 3, garde-fous).

### Anti-Pattern 4 — Comparer le rendu ou le code octet à octet

**Ce qui se fait :** asserter l'égalité exacte d'un extrait HTML, ou d'une ligne de `routes.py`, avec
le texte de la doc.
**Pourquoi c'est faux :** la moindre retouche de ponctuation ou d'espace produit un échec qui ne
signale aucune dérive de fond ; le test perd sa crédibilité et finit désactivé.
**À faire à la place :** comparaison de libellés **normalisés** (Pattern 5), et assertions de
*presence* pour le reste.

### Anti-Pattern 5 — Ancrer une valeur volatile de la base

**Ce qui se fait :** écrire « la base contient 18 288 objets », « version `3.6.10.11` », « dernier check
il y a 3 h » dans la documentation.
**Pourquoi c'est faux :** la resynchronisation invalide ces chiffres dès le premier `--force-sync` :
la doc devient périmée sans qu'aucun test ne puisse le signaler sans lire `.data/`.
**À faire à la place :** décrire le **format** (`Entrées :`, `Dernier check : il y a Xh`), jamais les
valeurs ; et garder les tests de doc hors de `.data/` (§6.3).

### Anti-Pattern 6 — Ajouter un outillage documentaire

**Ce qui se fait :** installer MkDocs, un vérificateur de liens tiers, `markdownlint` ou des hooks
`pre-commit`, « puisque c'est de la doc ».
**Pourquoi c'est faux :** `pyproject.toml` déclare `pytest>=8.0` comme seul outillage de vérification
et le périmètre exclut tout site généré ; chaque dépendance ajoute un mode d'échec étranger au besoin.
**À faire à la place :** `pathlib` + `re` + `unicodedata` + `shlex` (bibliothèque standard) et la suite
`pytest` existante. **Zéro dépendance nouvelle** — c'est aussi ce qui rend les contrôles exécutables
aujourd'hui.

### Anti-Pattern 7 — Modifier `dofus_stuff/**` pour « aligner la doc »

**Ce qui se fait :** renommer un libellé d'écran ou ajouter une option pour que la doc redevienne
vraie.
**Pourquoi c'est faux :** le produit est figé (milestone documentaire) ; ce serait un changement
fonctionnel déguisé, avec son propre risque de régression.
**À faire à la place :** corriger la doc ; si le code semble faux, c'est un constat à remonter, pas un
correctif dans cette phase.

### Anti-Pattern 8 — Fabriquer un ancre `page.md#section`

**Ce qui se fait :** lier une section précise via une ancre pour « mieux naviguer ».
**Pourquoi c'est faux :** il faudrait réimplémenter l'algorithme de slug GitHub dans le test (source de
faux négatifs) ou renoncer à vérifier le lien.
**À faire à la place :** liens de fichier à fichier (§3.1) ; le contrôle rejette toute cible contenant
`#`.

### Anti-Pattern 9 — Un test « exhaustif » purement bidirectionnel

**Ce qui se fait :** `assert set(fichiers) == set(liens_du_sommaire)` et rien d'autre.
**Pourquoi c'est faux :** supprimer une page **et** sa ligne d'index laisse le test vert, et toute la
documentation d'un thème peut disparaître silencieusement.
**À faire à la place :** l'invariant bidirectionnel **plus** la liste épinglée des pages requises
(Pattern 2), introduite en fin de parcours.

---

## 11. Points d'intégration

### 11.1 Services externes

| Service | Modèle d'intégration | Notes |
|---------|----------------------|-------|
| **Aucun** | — | L'architecture est hors-ligne par construction : les tests ne contactent ni `api.dofusdu.de` (fournisseur de données du produit), ni `dofusbook.net` (export), ni GitHub (rendu Markdown). Les URL restent du texte non vérifié (§3.1) |

### 11.2 Frontières internes

| Frontière | Moyen de communication | Considérations |
|-----------|-----------------------|----------------|
| `docs/cli.md` ↔ `dofus_stuff/cli.py::build_parser` | Import du symbole + `parse_args(argv)` | `build_parser` est explicitement ré-exporté (`__all__ = ["main", "build_parser", "collect_self_test_checks", "run_self_test"]`) : c'est une frontière **publique**, prévue pour les tests. Ne jamais passer par `main()` |
| `docs/installation.md` ↔ `dofus_stuff/web/__main__.py::build_parser` | Import du symbole + `parse_args(argv)` | **Deux parseurs distincts** dans le projet (CLI produit et entrée web) : le contrôle doit viser le bon fichier, sinon il passe à côté des options web |
| `docs/**` ↔ `dofus_stuff/web/routes.py` | Fixture `client` de `tests/conftest.py` (rendu réel) | La fixture crée un `Catalog` en mémoire et `create_app(..., load_catalog=False)` dans un `tmp_path` : **jamais** `.data/` du dépôt. Réutilisée telle quelle, sans modification |
| `docs/wizard-avance.md` ↔ `dofus_stuff/web/optimize_wizard.py` | Import des constantes (`WIZARD_STEPS`, `STEP_TITLES`, `SLOT_GROUP_LABELS`, `TYPE_FILTER_LABELS`, `RESISTANCE_STATS`, `DAMAGE_STATS`, `MISC_STATS`) | Ces constantes sont la « carte » du wizard : un renommage d'étape casse le test, pas la doc silencieusement |
| `docs/base-locale.md` ↔ `dofus_stuff/database.py`, `sync.py`, `api.py` | Import de constantes (`DB_NAME`, `DEFAULT_DATA_DIR`, `ITEM_KINDS`, `CHECK_INTERVAL_SECONDS`, `DEFAULT_TIMEOUT`, `SYNC_TIMEOUT`) | Ne lire **aucune** valeur d'exécution : les constantes prouvent la politique (24 h, hors-ligne), pas l'état de la base |
| `docs/wizard-avance.md` ↔ `dofus_stuff/web/static/js/terminal.js` | **Lecture texte** avec motifs ciblés | Seule entorse assumée à la frontière n° 2 du §1.3 : le JS n'est pas importable depuis pytest. Motifs à épingler : `key === "F3"`, `key === "Escape"`, `key === "F7"`, `key === "F8"`, `key === "PageUp"`, `key === "PageDown"`, `SAVES_KEY`, `MAX_SAVES` |
| `docs/**` ↔ `README.md`, `GUIDE_WIZARD.md` | Liens relatifs + contrôles de structure | Frontière d'entrée du lecteur ; c'est ici que le contrôle des renvois obsolètes mord (DOCS-10) |
| `tests/conftest.py` ↔ les deux modules de tests de doc | Fixture `docs_dir` (+ fixtures existantes `catalog`/`app`/`client`) | Pivot sérié, édité une seule fois (§8.1) |

### 11.3 Matrice de traçabilité exigence → artefact → contrôle

| Exigence | Artefact livré | Contrôle principal |
|----------|----------------|--------------------|
| DOCS-01 | `docs/sommaire.md` + 7 pages | `test_sommaire_est_exhaustif`, `test_h1_unique_et_label_conforme` |
| DOCS-02 | section de `README.md` | `test_readme_pointe_le_sommaire` |
| DOCS-03 | `docs/installation.md` | `test_web_entry_flags_documented` + `test_source_of_truth_paths_exist` |
| DOCS-04 | `docs/parcours-simplifie.md` | `test_libelles_parcours_simplifie`, `test_menu_labels_documented` |
| DOCS-05 | `docs/wizard-avance.md` | `test_etapes_wizard_documentees`, `test_commandes_wizard_documentees` |
| DOCS-06 | `docs/cli.md` | `test_commandes_cli_documentees`, `test_exemples_cli_analysables` |
| DOCS-07 | `docs/base-locale.md` | `test_db_status_fields_documented`, `test_base_locale_documentee` |
| DOCS-08 | `docs/depannage.md` | `test_rubriques_depannage_presentes`, `test_messages_erreur_ancres` |
| DOCS-09 | `docs/glossaire.md` | `test_glossaire_entrees_presentes` |
| DOCS-10 | `GUIDE_WIZARD.md` (aiguillage corrigé) | `test_aucun_renvoi_obsolete` (rouge avant, vert après) |
| DOCS-11 | toutes les pages | `test_tous_les_liens_relatifs_resolvent`, `test_aucun_lien_ancre_ni_absolu`, `test_utf8_sans_placeholder` |
| DOCS-12 | pages voyageant sur le code | `test_identifiants_ecrans_documentes`, `test_touches_clavier_documentees`, `test_options_*_documentees` |

---

## Sources

**Toutes les sources sont des fichiers du dépôt, lus ou exécutés localement.** Aucun fournisseur web
n'était disponible (voir la note de méthode en tête) : `gsd_run query websearch` a renvoyé
`{"available": false, "reason": "BRAVE_API_KEY not set"}`, `gsd_run query classify-confidence` a
renvoyé `MEDIUM` (context7) / `LOW` (websearch), et aucun résultat n'a été mis en cache puisque aucun
digest n'a pu être produit.

### Fichiers lus (ancrage de l'architecture)

| Fichier | Ce qui en a été tiré |
|---------|----------------------|
| `.planning/PROJECT.md` | Périmètre, contraintes, exigences DOCS-01…DOCS-12, règles de sûreté |
| `pyproject.toml` | `requires-python`, dépendances (`flask`, `msgpack`, `ortools`), extra `dev` (`pytest>=8.0`), `[project.scripts]`, `[tool.pytest.ini_options]` (`testpaths`, `pythonpath`) |
| `README.md` (121 l.) | Point d'entrée produit, ligne 59 (renvoi vers `GUIDE_WIZARD.md`), options globales documentées |
| `GUIDE_WIZARD.md` (330 l.) | Contenu à migrer + les deux renvois périmés (l. 35 et 40) |
| `dofus_stuff/cli.py` (443 l.) | `build_parser` (toutes les sous-commandes/options réelles), `_print_db_status`, `__all__` |
| `dofus_stuff/web/routes.py` (1384 l.) | Codes PGM, titres, libellés du menu et du flux simplifié, messages d'erreur, écrans `DB-01..DB-04`, `OPT-03`, `SAV-01` |
| `dofus_stuff/web/optimize_wizard.py` (450 l.) | `WIZARD_STEPS`, `STEP_TITLES`, libellés de slots/filtres, `body_items`, `body_recap` |
| `dofus_stuff/web/screens.py` (119 l.) | `COLS`, `BODY_LINES`, `clip`/`wrap_line`/`paginate` (justifie le Pattern 4) |
| `dofus_stuff/web/templates/screen.html` | Attributs de navigation (`data-f3-url`, `data-esc-url`, `data-f7-url`, `data-f8-url`, `data-mode`) |
| `dofus_stuff/web/static/js/terminal.js` | Touches réellement câblées, `SAVES_KEY`, `MAX_SAVES`, reprise du focus |
| `dofus_stuff/web/__main__.py`, `web/__init__.py` | Options et variables d'environnement de l'entrée web (DOCS-03) |
| `dofus_stuff/database.py`, `sync.py`, `api.py` | `DB_NAME`, `ITEM_KINDS`, `CHECK_INTERVAL_SECONDS`, `SYNC_SOURCES`, messages hors-ligne (DOCS-07) |
| `dofus_stuff/optimize/recommend.py` | `CLASSES` (19), `ELEMENTS` (DOCS-04/09) |
| `dofus_stuff/model/solver_spec.py` | `MAIN_CARACS`, `EXO_STATS`, `StatGoal`, `SLOT_GROUPS`, `TYPE_FILTER_KEYS` (DOCS-05/09) |
| `dofus_stuff/catalog.py` | Messages `Équipement introuvable : #…` / `Panoplie introuvable : #…`, recherche sensible à la casse (DOCS-08) |
| `tests/conftest.py`, `tests/test_web.py`, `tests/test_screens.py`, `tests/test_recommend.py` | Fixtures disponibles (`catalog`, `app`, `client`), conventions de nommage des tests, patterns `session_transaction` |
| `.gitignore`, `.planning/config.json` | `docs/` non ignoré ; drapeaux de recherche tous à `false` |

### Sondes exécutées (reproductibles)

| # | Sonde | Résultat |
|---|-------|----------|
| 1 | `dofus_stuff.cli.build_parser().parse_args(...)` sur 13 sondes (dont `db clear`, `cache stats`, `cache fill`) | Toutes parsent, sans exécution ; sous-commandes réelles = `cache, db, item, list, optimize, search, self-test, version` ; options globales = `--data-dir, --force-sync, --offline, --timeout` ; sous-commandes `db` = `clear, fill, stats, status, sync` |
| 2 | Rendu de 14 écrans via `create_app(offline=True, catalog=…, load_catalog=False)` + client de test (base et catalogue en `tmp_path`) | Tous les codes PGM vérifiés présents (`MNU-01` … `END-01`, `OPT-SIMPLE`) ; libellés `1/3`, `2/3`, `3/3`, `AVANCE : personnaliser les réglages` et les 3 messages de validation confirmés **rendus** ; `WIZARD_STEPS` = 9 étapes ; `data-esc-url` confirmé (`/system` depuis `VER-01`) |
| 3 | `_norm()` (NFD + sans diacritiques + `casefold` + apostrophes/tirets) sur `RECOMMANDATION DE STUFF` et `1/3 - Quelle est votre classe ?` | Normalisation stable ; confirme la nécessité du remplacement d'apostrophe typographique (`GUIDE_WIZARD.md`) et du tiret cadratin (`** WIZARD — …`) |
| 4 | `shlex.split` sur un exemple de doc + extraction de liens `\[…\]\(…\)` sur un échantillon | Découpage et extraction conformes ; détection des cibles `#ancre`, absolues et `https:` opérationnelle |
| 5 | `.venv/Scripts/python.exe -m pytest` sur l'état actuel | **136 passed in 1.82s** — base saine sur laquelle greffer les tests de doc ; aucun test existant ne touche `.data/` du dépôt (vérifié par recherche) |

*Confidence des sources :* **HIGH** pour tout ce qui précède (lecture directe + exécution locale,
recoupées par deux moyens indépendants — code et rendu). **MEDIUM** pour l'ordonnancement des phases,
le découpage invariant auto-ajustant / complétude, et l'arbitrage sondes statiques vs introspection
`argparse` : ce sont des choix d'ingénierie argumentés, pas des faits observables.

---
*Architecture research for: documentation utilisateur FR de dofus-stuff-machine (milestone brownfield)*
*Researched: 2026-09-10 (HEAD `19b5c96`)*

