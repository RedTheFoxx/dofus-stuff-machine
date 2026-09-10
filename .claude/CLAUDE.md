<!-- GSD:project-start source:PROJECT.md -->

## Project

**dofus-stuff-machine — Documentation utilisateur**

`dofus-stuff-machine` est un outil Python qui aide les joueurs de Dofus à constituer
une panoplie (un « stuff ») : base locale Dofusdude en SQLite, catalogue en mémoire,
CLI `fetcher.py`, interface web type terminal rétro (Flask) et solveur ortools.

Ce projet-ci ne modifie pas ces fonctionnalités : il livre la **documentation
user-friendly en français** qui manque au produit — un ensemble `docs/` clair,
exact et vérifié automatiquement, destiné d'abord au joueur qui veut un stuff,
avec des sections techniques identifiées (CLI, base locale, dépannage).

**Core Value:** Un utilisateur qui n'a jamais vu le projet peut installer l'outil, lancer le flux
simplifié **classe → éléments → niveau**, lire son résultat et retrouver chaque
commande/menu cité dans le code réel — sans lire le code et sans rencontrer de
documentation périmée.

### Constraints

- **Technique** : Python 3.11+, package `dofus_stuff`, pytest comme seul outillage de vérification — pas de nouvelle dépendance pour la documentation.
- **Langue** : documentation intégralement en français ; le code, les chemins et les identifiants techniques restent inchangés.
- **Données** : lecture seule sur `.data/` — jamais de `db clear`, de drop SQLite ni de suppression sous `.data/`.
- **Réseau** : mode hors-ligne par défaut ; aucune resynchronisation Dofusdude sauf nécessité démontrée ; aucune publication ni déploiement distant.
- **Vérification** : les critères de « fait » doivent être prouvés par des tests pytest réellement exécutés — aucune validation manuelle ni résultat inventé.
- **Périmètre** : strictement documentaire, limité au besoin initial ; pas de nouveau milestone après livraison.

<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->

## Technology Stack

## Verdict

## 1. Recommended Stack

### Core Technologies (au sens « ce qui porte la doc »)

| Technologie | Version | Purpose | Why Recommended | Conf. |
|-------------|---------|---------|-----------------|-------|
| Markdown « nu » (CommonMark + GFM) | format, pas de paquet | Support unique de la doc utilisateur | `README.md` et `GUIDE_WIZARD.md` sont déjà du Markdown français : continuité de format, lisible tel quel sur disque (terminal/éditeur) **et** rendu par GitHub, aucun build à lancer, aucun artefact à garder synchronisé | HIGH |
| Python ≥ 3.11 (stdlib : `pathlib`, `re`, `unicodedata`, `shlex`) | 3.11+ (déclaré `requires-python = ">=3.11"`) | Écrire le vérificateur documentaire | Le vérificateur n'a besoin que de lire des fichiers, résoudre des chemins relatifs, normaliser les accents et analyser des `argv` : 4 modules stdlib suffisent. Aucune dépendance à ajouter, donc aucune tension avec la contrainte « pytest seul outillage » | HIGH |
| pytest | `>=8.0` déclaré ; **9.1.1 observé** dans `.venv` (`.venv/Scripts/pytest.exe`) | Prouver les critères DOCS-11 / DOCS-12 | Déjà présent, déjà configuré (`testpaths`, `pythonpath`), déjà utilisé par 6 modules de tests : les tests de doc s'ajoutent sans toucher à la configuration | HIGH |
| Le rendu GitHub | n/a | Second consommateur de la doc | La revue du dépôt passe par GitHub : liens relatifs et titres doivent y résoudre. C'est un consommateur à **ne pas** casser, mais pas un outil à installer | HIGH |

### Supporting Libraries

| Library | Version | Purpose | When to Use | Conf. |
|---------|---------|---------|-------------|-------|
| **Aucune dépendance tierce** | — | — | — | HIGH |
| `pathlib.Path` (stdlib) | 3.11+ | Localiser `docs/` et résoudre chaque lien relatif depuis le fichier source | Dans les tests de doc : `Path(__file__).resolve().parents[1]` = racine du dépôt (les tests vivent dans `tests/`, un niveau sous la racine — vérifié) | HIGH |
| `re` (stdlib) | 3.11+ | Extraire les liens `[...](...)`, les blocs « Source de vérité », les blocs de code | Vérification de liens et extraction des chemins `.py` cités | HIGH |
| `unicodedata` (stdlib) | 3.11+ | Comparer des libellés d'écran accentués sans faux négatifs | Le code affiche `RECOMMANDATION DE STUFF`, `CARACTERISTIQUES`, `PA / PM / PO` (sans accents) alors que la prose française est accentuée : on compare en NFD + suppression des diacritiques + `casefold` | HIGH |
| `shlex` (stdlib) | 3.11+ | Découper un exemple CLI en `argv` avant de le passer à `build_parser().parse_args` | Test d'ancrage CLI (DOCS-06) : les exemples de la doc deviennent réellement analysables par le parseur | HIGH |
| `flask.Flask.test_client` (déjà là via `flask>=3.0`) | 3.x | Vérifier que les libellés cités existent à l'écran | Test d'ancrage web (DOCS-12) : réutilise la fixture `client` de `tests/conftest.py` | HIGH |

### Development Tools

| Tool | Purpose | Notes | Conf. |
|------|---------|-------|-------|
| `.venv/Scripts/python.exe -m pytest` | Exécuter les tests de doc | **Obligatoire comme interpréteur de référence** : l'interpréteur ambiant de l'hôte (Python 3.14.7) n'a pas pytest installé ; le venv du projet a pytest 9.1.1 | HIGH |
| `git` (commits locaux) | Historiser la doc et les tests | `commit_docs: true` dans `.planning/config.json` ; **aucun push, aucune PR publiée** (règle projet) | HIGH |
| Aucun linter Markdown, aucun `pre-commit`, aucun job CI | — | À ne pas ajouter : le contrôle reproductible demandé est pytest, exécutable en local | HIGH |

## 2. Layout documentaire prescriptif (le cœur de la réponse)

### Arborescence cible

### Table fichier → exigence → contenu prescrit

| Fichier `docs/` | Exigence | Contenu prescrit (et rien de plus) | Vérifié par |
|-----------------|----------|------------------------------------|-------------|
| `sommaire.md` | DOCS-01 | H1, une phrase d'intention, **la liste exhaustive** des 7 autres pages avec 1 ligne de description chacune, un « parcours conseillé » en 3 étapes (installation → parcours simplifié → glossaire) | `test_docs_structure.py` |
| `installation.md` | DOCS-03 | Prérequis (Python 3.11+), `pip install -e ".[dev]"`, `python fetcher.py version`, `python -m dofus_stuff.web`, `pytest` ; l'URL `http://127.0.0.1:5000` | structure + exemples CLI analysables |
| `parcours-simplifie.md` | DOCS-04 | Les 3 écrans réels (`OPT-SIMPLE`, « RECOMMANDATION DE STUFF »), les entrées acceptées (`Cra`, `1`, `terre air`, `1 3`, `multi`, niveau `1`–`200`), les messages d'erreur réels, le raccourci `AVANCE` | `test_docs_code_anchor.py` |
| `wizard-avance.md` | DOCS-05 | Les **9** étapes dans l'ordre de `WIZARD_STEPS` avec les titres de `STEP_TITLES`, la convention `BASE POINTS CIBLE POIDS` / `BASE EXO CIBLE POIDS`, les filtres de `TYPE_FILTER_KEYS`, les commandes `+ID` / `-ID` / `!ID` / `CLEAR`, `GO` / `RESET` / `SAVES` | `test_docs_code_anchor.py` |
| `cli.md` | DOCS-06 | Un tableau « commande → rôle → exemple » couvrant **toutes** les sous-commandes du parseur et **toutes** les options globales ; un encadré d'avertissement sur `db clear` | `test_docs_code_anchor.py` |
| `base-locale.md` | DOCS-07 | `.data/dofus.sqlite3`, mode hors-ligne par défaut, fenêtre de re-check **24 h**, `db status` / `db sync` / `--force-sync` / `--offline`, sortie de `db status` décrite par ses libellés de champs | `test_docs_code_anchor.py` |
| `depannage.md` | DOCS-08 | 5 rubriques : base absente, saisie invalide, calcul long, clavier inactif (focus du champ), résultat paginé (F8) | `test_docs_structure.py` |
| `glossaire.md` | DOCS-09 | Stuff, slot, solveur, poids, cible, ID Ankama, jet, exo, panoplie, dofus, trophée, prysmaradite — trié alphabétiquement | `test_docs_structure.py` |

### 2.1 Nommage des fichiers — règle ferme

- **ASCII minuscules, kebab-case, extension `.md`** : `parcours-simplifie.md`, jamais
- Un fichier = un thème = une exigence DOCS. Aucun fichier fourre-tout, aucun sous-dossier : à

### 2.2 Sommaire — `docs/sommaire.md`

- Nom imposé : **`sommaire.md`** (H1 : `# Documentation dofus-stuff-machine`). C'est ce chemin
- Le sommaire liste les 7 autres pages ; **tout fichier présent dans `docs/` et non listé fait

### 2.3 Entrée README (DOCS-02)

## Documentation utilisateur

- [Installation et premier lancement](docs/installation.md)
- [Obtenir un stuff en 3 questions](docs/parcours-simplifie.md)
- [Wizard avancé, écran par écran](docs/wizard-avance.md)
- [Ligne de commande](docs/cli.md)
- [Base locale et mode hors-ligne](docs/base-locale.md)
- [Dépannage / FAQ](docs/depannage.md)
- [Glossaire](docs/glossaire.md)

### 2.4 `GUIDE_WIZARD.md` — arbitrage (confiance MEDIUM, décision de goût)

## 3. Conventions qui rendent la doc vérifiable automatiquement

## 4. Design de vérification pytest (DOCS-11 / DOCS-12)

### 4.1 Emplacement et style

- Deux modules, granularité identique aux modules existants (`test_web.py`, `test_screens.py`,
- **Noms de fonctions en anglais, docstrings en français** — convention observée des tests
- Fixture partagée `docs_dir` ajoutée à `tests/conftest.py` (le fichier de fixtures est déjà en

### 4.2 `tests/test_docs_structure.py` — DOCS-01, DOCS-02, DOCS-10, DOCS-11

| Test (docstring française) | Assertion | Critère prouvé |
|------------------------------|-----------|----------------|
| `test_docs_directory_has_sommaire` | `docs/` existe et contient `sommaire.md` + les 7 pages attendues, et **aucun `.md` non listé** | DOCS-01 |
| `test_sommaire_lists_every_document` | Chaque `.md` sous `docs/` (hors sommaire) est lié depuis `sommaire.md` | DOCS-01 |
| `test_sommaire_links_resolve` | Chaque lien du sommaire pointe vers un fichier existant | DOCS-11 |
| `test_all_relative_links_resolve` | Pour chaque `.md` de la doc (`README.md`, `GUIDE_WIZARD.md`, `docs/**`), chaque cible `](…)` sans schéma et sans `#` résout relativement au fichier source | DOCS-11 |
| `test_no_anchor_or_absolute_links` | Aucune cible de lien ne contient `#`, ne commence par `/` ou `C:` | convention §3.2 |
| `test_readme_links_to_sommaire` | `README.md` contient `](docs/sommaire.md)` | DOCS-02 |
| `test_h1_matches_sommaire_entry` | 1 seul H1 par page, texte = libellé du sommaire | DOCS-01/11 |
| `test_no_obsolete_menu_references` | La chaîne `3. OPTIMISATION DE STUFF` n'apparaît **nulle part** dans `README.md`, `GUIDE_WIZARD.md`, `docs/**` ; `4. OPTIMISATION DE STUFF` et `5. SYSTEME` y apparaissent (le menu réel compte 5 entrées) ; le motif ``Tapez\s+`?3`?\s+puis`` a disparu | DOCS-10 |
| `test_documents_are_utf8_and_not_drafts` | Décodage UTF-8 strict ; aucune occurrence `TODO` / `À COMPLÉTER` / `Lorem` ; chaque page ≥ 20 lignes | anti-placeholder |
| `test_troubleshooting_sections_present` | `depannage.md` contient les 5 rubriques ; `glossaire.md` contient les entrées attendues | DOCS-08/09 |

### 4.3 `tests/test_docs_code_anchor.py` — DOCS-06, DOCS-12

| Test | Assertion | API réellement utilisée |
|------|-----------|------------------------|
| `test_sources_de_verite_exist` | Dans chaque bloc « Source de vérité », les chemins `` `…py` `` existent relativement à la racine | lecture disque |
| `test_documented_cli_commands_parse` | Sondes `["version"]`, `["self-test"]`, `["search","x"]`, `["item","44"]`, `["list"]`, `["optimize","--demo"]`, `["db","status"]`, `["db","sync"]`, `["db","clear"]` et les alias `cache …` : `build_parser().parse_args(argv)` **n'échoue pas**, et le nom de commande est présent dans `docs/cli.md` | `dofus_stuff.cli.build_parser` (ré-exporté « pour tests / scripts ») |
| `test_documented_global_options_parse` | `--timeout`, `--data-dir`, `--force-sync`, `--offline` parsés devant `version` et présents dans `docs/cli.md` | idem |
| `test_documented_cli_examples_parse_and_appear` | Table d'exemples du test (découpés via `shlex.split`) : chacun **apparaît verbatim** dans `docs/cli.md` **et** est analysable par le parseur (ancrage bidirectionnel : la doc ne peut ni inventer une option ni en oublier une) | `shlex` + `build_parser` |
| `test_menu_labels_documented` | `client.get("/")` contient `MENU PRINCIPAL`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME` ; ces libellés apparaissent dans la doc | fixture `client` (Flask `test_client`) |
| `test_libelles_parcours_simplifie` | Le client atteint l'écran `OPT-SIMPLE` et la doc reprend, à la casse et aux accents près, `1/3 - Quelle est votre classe ?`, `2/3 - Quels éléments privilégier ?`, `3/3 - Quel est votre niveau ? (1 à 200)`, `AVANCE : personnaliser les réglages`, ainsi que les messages de validation réels (`Saisissez le nom ou le numéro de votre classe.`, `Exemple : feu, terre air, ou multi.`, `Saisissez un niveau entre 1 et 200.`) | `client.post("/optimize/quick/…")` + normalisation `unicodedata` |
| `test_etapes_wizard_documentees` | Chaque titre de `STEP_TITLES` apparaît dans `docs/wizard-avance.md` (normalisé), dans l'ordre de `WIZARD_STEPS`, et la doc annonce bien **9 écrans** (`len(WIZARD_STEPS) == 9`) | `dofus_stuff.web.optimize_wizard` (`WIZARD_STEPS`, `STEP_TITLES`) |
| `test_identifiants_ecrans_documentes` | Les identifiants d'écran réellement émis (`MNU-01`, `SYS-01`, `ITM-01`, `PAN-01`, `PAN-02`, `SAV-01`, `OPT-SIMPLE`) apparaissent dans la doc là où elle décrit ces écrans | constantes `pgm` de `routes.py` |
| `test_db_status_fields_documented` | `base-locale.md` reprend les libellés de sortie de `_print_db_status` (`Fichier :`, `Version jeu :`, `Dernier check :`, `Entrées :`, `Par catégorie :`) et la fenêtre **24 h** | `dofus_stuff.cli`, `dofus_stuff.sync.CHECK_INTERVAL_SECONDS` |

### 4.4 Commandes d'exécution (à utiliser telles quelles)

# Interpréteur du projet : l'interpréteur ambiant n'a pas pytest

### 4.5 Garde-fous de sûreté des tests

- Les tests **parsent** `db clear` / `cache clear` pour vérifier que la doc cite une commande
- Les tests n'ouvrent aucune socket (liens externes non vérifiés).
- Les tests n'appellent jamais `main()` : `parse_args` seul, donc aucun prompt interactif

## 5. Traçabilité exigences → artefacts de la stack

| Exigence | Artefact | Test |
|----------|----------|------|
| DOCS-01 | `docs/sommaire.md` + 7 pages | `test_docs_structure.py` (exhaustivité bidirectionnelle) |
| DOCS-02 | section « Documentation utilisateur » de `README.md` | `test_readme_links_to_sommaire` |
| DOCS-03 | `docs/installation.md` | structure + exemples CLI analysables |
| DOCS-04 | `docs/parcours-simplifie.md` | `test_libelles_parcours_simplifie` |
| DOCS-05 | `docs/wizard-avance.md` | `test_etapes_wizard_documentees` |
| DOCS-06 | `docs/cli.md` | `test_documented_cli_*` |
| DOCS-07 | `docs/base-locale.md` | `test_db_status_fields_documented` |
| DOCS-08 | `docs/depannage.md` | `test_troubleshooting_sections_present` |
| DOCS-09 | `docs/glossaire.md` | `test_troubleshooting_sections_present` (partie glossaire) |
| DOCS-10 | `GUIDE_WIZARD.md` (aiguillage corrigé) | `test_no_obsolete_menu_references` |
| DOCS-11 | toutes les pages | `tests/test_docs_structure.py` (5 tests de liens/sommaire) |
| DOCS-12 | `docs/parcours-simplifie.md`, `docs/wizard-avance.md`, `docs/cli.md`, `docs/base-locale.md` | `tests/test_docs_code_anchor.py` |

## 6. Installation

# Environnement déjà présent dans le dépôt (.venv avec pytest 9.1.1)

# Aucune dépendance documentaire à installer.

## 7. Alternatives Considered

| Recommended | Alternative | When to Use Alternative | Conf. |
|-------------|-------------|-------------------------|-------|
| Markdown nu + `pytest` | **MkDocs (+ thème Material)** | Si le besoin devenait un site publié avec recherche plein texte et navigation latérale — hors périmètre explicite (PROJECT.md « Out of Scope ») et suppose une publication distante, interdite ici | HIGH |
| Markdown nu | **Sphinx** | Projet multi-langages avec API autodoc et `toctree` : surdimensionné pour 8 pages utilisateur, ajoute `sphinx` + un thème + un `conf.py` | HIGH |
| Markdown nu | **mdBook / Docusaurus / VitePress** | Si la doc devait être un site statique multi-format : introduit une toolchain non-Python (Rust/Node) dans un dépôt Python — coût de maintenance injustifié | HIGH |
| `docs/` multi-fichiers | **README unique enrichi** | Si la doc tenait en ~200 lignes : ici 8 thèmes distincts, un seul fichier rendrait le test d'exhaustivité inutile et la lecture pénible | MEDIUM |
| Tests maison (`pathlib` + `re`) | **`pytest-linkcheck` / `linkchecker` / `markdown-link-check` (Node)** | Si les liens **externes** devaient être surveillés en CI : ce n'est pas le besoin ici (hors-ligne par défaut) et cela ajoute une dépendance + une source de flakiness réseau | HIGH |
| Comparaison de libellés normalisés (accents/casse ignorés) | **Comparaison octet à octet d'un rendu HTML de référence** | Si l'UI produisait des captures de référence : fragile aux accents et aux espaces, et l'objet du test est la doc, pas le rendu | MEDIUM |
| Rédaction manuelle sourcée par les fichiers du dépôt | **Générateur LLM local (`.doc-agent`, `doc-agent.toml` → `output = "docs"`, `language = "fr"`)** | Utilisable comme brouillon si le modèle local répond : mais `.doc-agent/state.json` montre un run **bloqué en stage PLAN** (`status: "running"`), non versionné, et un générateur ne peut pas *prouver* l'ancrage au code — c'est le rôle des tests DOCS-12. À ne pas mettre sur le chemin critique | MEDIUM |

## 8. What NOT to Use

| Avoid | Why | Use Instead | Conf. |
|-------|-----|-------------|-------|
| MkDocs / MkDocs Material / `mkdocs.yml` | Dépendance + configuration + build + risque de doc « générée mais non publiée » ; PROJECT.md l'exclut explicitement | Markdown nu dans `docs/` | HIGH |
| Sphinx (`conf.py`, `autodoc`) | Outillage de référence d'API pour développeurs ; le public visé est « Utilisateur + dev », pas « Développeur » (hors périmètre) | `docs/` en prose française | HIGH |
| Plugin pytest tiers (`pytest-linkcheck`, `pytest-md-report`) | Ajoute une dépendance et une compatibilité à maintenir pour 5 assertions de liens | Tests maison avec `pathlib` | HIGH |
| `markdownlint`, `prettier`, hooks `pre-commit` | Non demandés ; un outil qui reformate des liens introduit des échecs que pytest ne couvre pas, et ajoute un outillage non-Python | Conventions écrites (§3) + tests | MEDIUM |
| Traductions de la doc (`docs/en/`, gettext, `mkdocs-static-i18n`) | Besoin explicitement « en Français » ; toute infrastructure i18n est du surdimensionnement | Doc française unique | HIGH |
| Embarquer `docs/` dans le paquet (`package-data`, ou déplacement sous `dofus_stuff/`) | Aucune publication n'est autorisée ; cela gonflerait le wheel et forcerait une reconfiguration du packaging sans bénéfice | `docs/` à la racine, hors paquet | HIGH |
| Vérifier les liens externes (`api.dofusdu.de`, `dofusdu.de`) dans les tests | Dépendance réseau, hors-ligne par défaut, échec non imputable au dépôt | Asserter la présence du texte du lien uniquement | HIGH |
| Lire `.data/dofus.sqlite3` dans les tests de doc | Contrainte projet (lecture seule, aucune resynchronisation) ; et une valeur volatile ne prouve aucun critère documentaire | Décrire les champs de sortie, pas les valeurs | HIGH |
| Ancrer un chiffre de base (`18288` objets, `3.6.10.11`) dans la doc | Obsolète dès la première resynchronisation — reproduit exactement le défaut qu'on corrige | Formuler en termes de champs / de format | HIGH |
| `page.md#ancre` dans les liens | Réimplémente l'algorithme de slug GitHub côté test : source de faux négatifs et de réécritures | Liens de fichier à fichier | MEDIUM |
| Réécrire `dofus_stuff/**` pour « aligner » la doc | Le périmètre est documentaire ; modifier le code changerait le produit | Corriger la doc | HIGH |
| Ajouter `docs/` au `.gitignore` | La doc doit être versionnée (`commit_docs: true`) et `docs/` n'est pas ignoré aujourd'hui | Aucune modification de `.gitignore` | HIGH |
| Créer `docs/index.md` en plus de `docs/sommaire.md` | Deux index concurrents = la même dérive que `GUIDE_WIZARD.md` vs `README.md` | Un seul `sommaire.md` | HIGH |

## 9. Stack Patterns by Variant

## 10. Version Compatibility

| Élément | Compatible avec | Notes | Conf. |
|---------|-----------------|-------|-------|
| `pytest>=8.0` (déclaré) | pytest **9.1.1** installé dans `.venv` | Aucune API exotique utilisée (fixtures, `tmp_path`, `test_client`) : compatible 8 et 9 | HIGH |
| Interpréteur ambiant Python **3.14.7** | ❌ pas de pytest installé | Les tests doivent être lancés avec `.venv/Scripts/python.exe` ; une exécution avec l'interpréteur ambiant échouerait avant toute assertion | HIGH |
| `requires-python = ">=3.11"` | code existant | La doc et les tests n'utilisent que des constructions 3.11+ (`pathlib`, `unicodedata`, `X \| None` déjà en usage) | HIGH |
| GitHub Flavored Markdown | chemins ASCII minuscules | Les liens relatifs résolvent sur GitHub ; noms accentués ⇒ percent-encoding (lisibilité des diffs dégradée) | MEDIUM |
| Windows (CRLF, FS insensible à la casse) | git (sensible à la casse, aucun `.gitattributes`) | Éviter les renommages « casse seule » des fichiers de doc ; ne pas asserter sur les octets de fin de ligne | HIGH |
| Markdown ↔ `readme = "README.md"` (`pyproject.toml`) | tout ajout au README est du Markdown livrable | Garder l'entrée doc courte et valide ; pas de HTML brut | HIGH |

## 11. Risques & points de coordination repérés (à porter au roadmap)

| Risque | Constat (fichier lu) | Mitigation prescrite | Conf. |
|--------|----------------------|----------------------|-------|
| Un générateur de doc local cible déjà `docs/` | `doc-agent.toml` : `output = "docs"`, `language = "fr"`, modèle local ; `.doc-agent/state.json` en `status: "running"`, `stage: "PLAN"` — **non suivis par git** (`git status` : `?? .doc-agent/`, `?? doc-agent.toml`) | Ne rien supprimer, ne pas en dépendre ; livrer `docs/` à la main. Si ce run repart et réécrit `docs/`, les tests DOCS-11/12 échouent **bruyamment** — c'est le garde-fou voulu | HIGH |
| Deux descriptions concurrentes du wizard | `README.md:59` → `GUIDE_WIZARD.md` ; `GUIDE_WIZARD.md:35-45` décrit `3. OPTIMISATION DE STUFF` alors que `routes.py:188-206` liste 5 entrées avec `4. OPTIMISATION DE STUFF` | Source unique `docs/wizard-avance.md` + aiguillage corrigé + `test_no_obsolete_menu_references` | HIGH |
| `docs/` non ignoré par git | `.gitignore` ne contient pas `docs/` (entrées observées : `__pycache__/`, `*.py[cod]`, `.venv/`, `venv/`, `.env`, `.data/`, `*.egg-info/`, `.eggs/`, `dist/`, `build/`, `.pytest_cache/`, `.coverage`, `htmlcov/`, `.gsd-auto/`) | Aucune modification nécessaire ; la doc est committée (commit local uniquement) | HIGH |
| Aucun `.gitattributes` | vérifié : absent du dépôt | Ne pas en ajouter dans ce périmètre ; se contenter de tests tolérants aux fins de ligne | MEDIUM |
| Tentation de documenter des valeurs réelles de la base | Sonde SQLite **en lecture seule** (`file:.data/dofus.sqlite3?mode=ro`) : `game_version = 3.6.10.11`, `last_checked_at` présent, 18288 lignes dans `items` | Interdire ces valeurs dans la prose ; décrire le format de `db status` | HIGH |

## Sources

- `.planning/PROJECT.md` — contexte brownfield, contraintes, DOCS-01…DOCS-12, hors-périmètre
- `pyproject.toml` — dépendances runtime (`flask`, `msgpack`, `ortools`), extra `dev` réduit à
- `README.md` — structure existante, renvoi `GUIDE_WIZARD.md` ligne 59, exemples CLI
- `GUIDE_WIZARD.md` — contenu du wizard et **désynchronisation** du menu (lignes 35-45 : `3. OPTIMISATION DE STUFF`)
- `dofus_stuff/cli.py` — `build_parser()` : sous-commandes `version`, `self-test`, `search`,
- `dofus_stuff/web/routes.py` — menu réel (`MNU-01`, 5 entrées), `SYS-01`, `ITM-01`,
- `dofus_stuff/web/optimize_wizard.py` — `WIZARD_STEPS` (9 étapes), `STEP_TITLES`
- `dofus_stuff/web/__init__.py`, `dofus_stuff/web/__main__.py` — `create_app(data_dir, offline,
- `dofus_stuff/model/solver_spec.py` — `SLOT_GROUPS`, `DEFAULT_SLOT_GROUPS`, `TYPE_FILTER_KEYS`, `MAIN_CARACS`, `EXO_STATS`
- `dofus_stuff/optimize/recommend.py` — `CLASSES` (19 classes), `ELEMENTS` (`terre/feu/eau/air`)
- `dofus_stuff/sync.py` — `CHECK_INTERVAL_SECONDS = 24 * 60 * 60`
- `dofus_stuff/database.py` — `DEFAULT_DATA_DIR` = `<racine du dépôt>/.data`
- `tests/conftest.py` — fixtures `catalog`, `app`, `client` (`create_app(..., offline=True,
- `tests/test_web.py`, `tests/test_screens.py`, `tests/test_recommend.py`, `tests/test_optimize.py` —
- `.gitignore` (diff non committé : ajout de `.gsd-auto/`), `doc-agent.toml`, `.doc-agent/state.json`
- `.planning/config.json` — `commit_docs: true`, `search_gitignored: false`, tous les fournisseurs
- Sonde SQLite **lecture seule** (URI `?mode=ro`) sur `.data/dofus.sqlite3` — tables `items`, `meta` ;

<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
