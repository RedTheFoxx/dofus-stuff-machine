# Phase 2: Référence CLI alignée sur le parseur - Research

**Researched:** 2026-09-11
**Domain:** Référence CLI Markdown (`docs/cli.md`) ancrée sur le parseur `argparse` réel, vérifiée par `pytest` (zéro dépendance nouvelle)
**Confidence:** HIGH — la surface documentée de cette phase est **mesurée**, pas relue : chaque sous-commande, chaque option, chaque défaut, chaque code de retour et chaque résultat `shlex` cité ci-dessous vient d'une exécution réelle avec l'interpréteur épinglé `.venv/Scripts/python.exe`, jamais d'une lecture approximative du source.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Profondeur & structure par sous-commande
- **D-16:** Une section par sous-commande, **dans l'ordre réel du parseur** (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db`), chacune avec : synopsis, options propres et leurs **valeurs par défaut réellement lues dans le parseur**, un exemple.
- **D-17:** **Pas de table récapitulative en fin de page.** Une table unique dupliquerait le parseur et deviendrait un second référentiel à maintenir — contraire au principe « une seule source par énoncé » (même raison que D-10 pour le lien unique `README.md` → `docs/sommaire.md`). La source de vérité est le parseur ; la page le décrit.

#### Surface des options d'`optimize`
- **D-18:** **Toutes** les options d'`optimize` sont documentées, en **tables groupées par thème** (profil/poids, contraintes, caractéristiques de base & scrolls, RNG/perf), avec synopsis et défaut issus du code réel (~30 options : `--base-*`, `--scroll-*`, `--level`, `--top-k` défaut 30, `--seed` défaut `None`, options de contraintes et de perf).
  — **Reversibility:** costly — Si un groupe thématique est mal découpé, le corriger impose de réécrire les tables de la page et de re-valider les contrôles d'ancrage des options déjà écrits en phase 2, ainsi que la section de `docs/cli.md` que les phases 3 et 6 citeront comme référence.
- **D-19:** **Aucune sémantique inventée.** Une option dont le sens n'est pas lisible dans le code est décrite par son synopsis et son défaut, sans interprétation ajoutée. Le critère 2 du ROADMAP n'exige que « chaque option **documentée** » soit acceptée par le parseur ; la complétude retenue ici vient de l'utilité pour le lecteur, pas d'une obligation de tout documenter, et la page reste honnête sur ce qu'elle ne dit pas.

#### Alias `cache` et commandes destructrices
- **D-20:** `cache` est présenté **comme alias de `db`**, sans description dupliquée. Les sous-commandes masquées du help (`stats`, `fill`, `argparse.SUPPRESS`) sont signalées **comme telles** et rattachées à leur nom canonique.
- **D-21:** Le lien d'alias est prouvé **par le parseur public**, sans recopier de texte : `cache <sous-commande>` et `db <sous-commande>` doivent produire un espace de noms équivalent. Aucune API privée d'`argparse` (D-14).
- **D-22:** `db clear` est mentionné **hors parcours recommandé**, avec l'**avertissement destructif sur la même ligne**, et jamais proposé comme étape. Le nom exact du drapeau est **lu dans le parseur** au moment de rédiger, pas inventé. Aucun `db clear` n'est exécuté, à aucun moment.
- **D-23:** La liste des sous-commandes réellement destructrices (`db clear`, et `db sync` / `cache fill` qui réécrivent la base) est dérivée du code, pas supposée ; toute commande retenue comme destructrice doit apparaître **avec** son avertissement et **en dehors** de tout parcours conseillé.

#### Ancrage des exemples et limite du contrôle
- **D-24:** Seules comptent comme « exemples » les lignes situées dans des **blocs de code balisés comme tels** (marqueur explicite), pas les commandes citées en prose — sinon le contrôle devient fragile.
- **D-25:** Vérification d'un exemple : présence **verbatim** dans la page **et** analyse par `shlex.split(...)` → `build_parser().parse_args(...)`, parseur public uniquement (D-14).
- **D-26:** **Limite honnête consignée dans le test lui-même** : une sous-commande ou une option ajoutée plus tard au parseur et **non documentée ne fera pas échouer la suite** (le contrôle est page → parseur plus une liste explicite). Aucune exhaustivité totale n'est revendiquée.
- **D-27:** L'**ordre réel** est illustré : au moins un exemple hors-ligne place l'option globale **avant** la sous-commande (`--offline optimize …`), conformément au comportement mesuré en phase 1.

#### Sommaire et README
- **D-28:** `docs/sommaire.md` gagne **l'entrée `cli.md` maintenant** (le sommaire croît par phase, D-05) ; la liste épinglée des 8 pages reste en phase 6 (D-05). Le test d'exhaustivité bidirectionnelle (D-06) doit rester vert sans exception.
- **D-29:** `README.md` garde son **lien unique** vers `docs/sommaire.md` — aucun lien direct vers `cli.md` (D-10).

#### Gabarit et ancrage au code
- **D-30:** `docs/cli.md` suit le gabarit de D-01 : H1 unique, phrase d'introduction, sections courtes, bloc **« Source de vérité »** pointant vers `dofus_stuff/cli.py` § `build_parser()` et `fetcher.py` (point d'entrée), et ligne de retour vers `docs/sommaire.md`. Chaque chemin `.py` du bloc doit exister sur disque (D-03).
- **D-31:** Les conventions de test de la phase 1 s'appliquent sans modification : comparaisons après normalisation (D-11), helpers dans le `tests/conftest.py` existant (D-12), message d'échec citant **la page, la valeur attendue et le fichier de code** (D-13), exécution de référence `.venv/Scripts/python.exe -m pytest -q` sans exécuter `main()`, sans écrire sous `.data/`, sans connexion réseau (D-15).

### Claude's Discretion
- Découpage exact des groupes thématiques des tables d'`optimize` (D-18 fixe le principe, pas le nombre de groupes).
- Forme du marqueur qui identifie une ligne comme « exemple » (D-24), tant qu'il reste détectable par test sans ambiguïté.
- Formulation du synopsis de chaque sous-commande et de la phrase d'introduction de la page.
- Ordre des groupes à l'intérieur des tables, dès lors que les options et leurs défauts sont exacts.
- Découpage interne des nouveaux tests (module dédié `tests/test_docs_cli.py` ou extension d'un module existant) — seule contrainte : ne pas dupliquer les helpers de `tests/conftest.py` (D-12).

### Deferred Ideas (OUT OF SCOPE)
- **Table récapitulative unique de toute la surface CLI** — écartée (D-17) : second référentiel à maintenir, contraire à « une seule source par énoncé ».
- **Documenter une sémantique non lisible dans le code** (intention d'une option, valeur recommandée) — hors périmètre (D-19) ; relèverait d'un guide d'usage, pas d'une référence.
- **Complétude prouvée dans les deux sens pour toute la surface CLI** (toute sous-commande/option du parseur doit être documentée) — non retenue (D-26) : rendrait toute évolution future du parseur bloquante. Reste un contrôle page → parseur plus une liste explicite.
- **Dépannage par message d'erreur, glossaire, liste épinglée des 8 pages** — phases 5 et 6.
- **Parcours simplifié du rendu réel** — phase 3.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (verbatim de `.planning/REQUIREMENTS.md:41-43`) | Research Support |
|----|--------------------------------------------------------------|------------------|
| CLI-01 | Chaque sous-commande documentée de `fetcher.py` est réellement analysable par le parseur d'arguments du code — dérivé de DOCS-06 | § « Mesures » M1 : les 8 sous-commandes documentables mesurées (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db`, `cache`) ; **sonde mesurée par sous-commande obligatoire** (`db` et `cache` nus sortent en code 2, `db_command` requis) ; `cache` n'est ni un `aliases=` ni un `set_defaults` (M1.3) |
| CLI-02 | Chaque option globale et chaque option d'optimisation documentée est réellement analysable par le parseur — dérivé de DOCS-06 | § « Mesures » M2 : défauts réels lus par `parse_args` (jamais par le texte source), surface globale = 4 options + `--help`, surface d'`optimize` = 30 options mesurées ; mode interactif = absence de `--level`/`--max` (`needs_interactive_optimize`) |
| CLI-03 | Chaque exemple de commande cité dans `docs/cli.md` est analysable et apparaît verbatim dans la page — dérivé de DOCS-06 | § « Mesures » M4 (`shlex`) et § « Architecture Patterns » Pattern 2-3 : marqueur de bloc, extraction, `shlex.split` → `parse_args`, et la limite honnête de l'assertion « verbatim » |

### Success Criteria (verbatim de `.planning/ROADMAP.md` § Phase 2)

1. Chaque sous-commande documentée (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db` et l'alias `cache`) est analysée sans erreur par le parseur d'arguments réel (`build_parser().parse_args`).
2. Chaque option globale documentée (`--timeout`, `--data-dir`, `--force-sync`, `--offline`) et chaque option d'`optimize` documentée est réellement acceptée par le parseur.
3. Chaque exemple de commande de la page apparaît verbatim dans `docs/cli.md` et son découpage en arguments (`shlex`) est analysable par le parseur.
4. L'ordre réel est illustré : au moins un exemple hors-ligne place l'option globale avant la sous-commande (`--offline optimize …`), et `db clear` n'apparaît qu'accompagné de son avertissement destructif, jamais dans un parcours recommandé.
5. La suite reste verte avec l'interpréteur épinglé, sans exécuter `main()` ni écrire sous `.data/`.
</phase_requirements>

## Project Constraints (from CLAUDE.md)

`./CLAUDE.md` **n'existe pas** à la racine ; le chemin configuré est `.claude/CLAUDE.md` (`project_code: null`, `claude_md_path: "./.claude/CLAUDE.md"` dans `.planning/config.json`). Directives applicables extraites de ce fichier :

| # | Directive (source) | Conséquence pour cette phase |
|---|--------------------|-----------------------------|
| C1 | Interpréteur de référence **obligatoire** : `.venv/Scripts/python.exe -m pytest` ; « l'interpréteur ambiant de l'hôte (Python 3.14.7) n'a pas pytest installé » (`.claude/CLAUDE.md:64`, `:218`) | Toute commande citée, tout relevé de compteur, toute vérification passe par ce chemin. Mesuré : `.venv/Scripts/python.exe --version` → `3.14.7`, `pytest 9.1.1` |
| C2 | **Aucune nouvelle dépendance**, aucun linter Markdown, aucun `pre-commit`, aucun job CI (`.claude/CLAUDE.md:203-210`, § « What NOT to Use » ; § « Development Tools ») | Le marqueur de bloc, l'extraction et la comparaison restent en bibliothèque standard (`re`, `shlex`, `pathlib`) ; aucune bibliothèque Markdown n'est installée (mesuré : `markdown`, `markdown_it`, `commonmark` **absents**) |
| C3 | Documentation **intégralement en français** ; code, chemins, identifiants inchangés ; **noms de fonctions de test en anglais, docstrings en français** (`.claude/CLAUDE.md:113-118`) | `docs/cli.md` en français ; les nouveaux tests suivent la convention observée des modules existants |
| C4 | `.data/` est en **lecture seule** : jamais de `db clear`, de drop SQLite, de suppression sous `.data/` (`.claude/CLAUDE.md:24`) | Les sondes de cette phase n'ouvrent aucune base ; tout essai CLI en sous-processus a utilisé un `--data-dir` temporaire (mesuré, `.data/dofus.sqlite3` intact) |
| C5 | Aucun réseau, aucune publication, aucune PR ; **commits locaux uniquement** (`commit_docs: true`) (`.claude/CLAUDE.md:64-67`) | Aucun contrôle de cette phase n'ouvre de socket ; le livrable est commité localement |
| C6 | « Les tests **parsent** `db clear` / `cache clear` pour vérifier que la doc cite une commande » ; « les tests n'appellent jamais `main()` : `parse_args` seul, donc aucun prompt interactif » (`.claude/CLAUDE.md:154-156`) | **Parser `db clear` est prescrit** (ce n'est pas l'exécuter) ; la distinction parse / exécution doit être écrite dans le test, car D-22 interdit l'exécution |
| C7 | §4.3 prescrit les noms et assertions des tests CLI : `test_documented_cli_commands_parse` (sondes `["version"]`, `["self-test"]`, `["search","x"]`, `["item","44"]`, `["list"]`, `["optimize","--demo"]`, `["db","status"]`, `["db","sync"]`, `["db","clear"]` + alias `cache …`, « et le nom de commande est présent dans `docs/cli.md` »), `test_documented_global_options_parse`, `test_documented_cli_examples_parse_and_appear` (`.claude/CLAUDE.md:134-146`) | Ces trois tests sont **la forme prescrite de CLI-01/CLI-02/CLI-03** : la liste de sondes explicite de C7 est la « liste explicite » de D-26. La sonde `["db","clear"]` de C7 est un `parse_args`, jamais une exécution |
| C8 | `.claude/CLAUDE.md:72-84` prescrit pour `cli.md` « un tableau « commande → rôle → exemple » couvrant toutes les sous-commandes du parseur et toutes les options globales ; un encadré d'avertissement sur `db clear` » | **Arbitrage explicite** : la *forme* « tableau récapitulatif unique » est écartée par D-17 (décision de phase, plus récente et motivée) ; l'*intention* de C8 est conservée (toutes les sous-commandes, toutes les options globales, un avertissement `db clear`). Les tables par section (D-18) satisfont la partie « tableau » pour les options. **Le plan doit écrire cet arbitrage** pour que le plan-checker ne le lise pas comme une violation |
| C9 | `.claude/CLAUDE.md:96-106` (snippet d'entrée README) liste 7 **liens directs** vers les pages `docs/` | **Superseded** par D-10/D-29 (lien unique vers `docs/sommaire.md`). Mesuré : `README.md:7` porte déjà le lien unique. **Aucun lien direct vers `cli.md` ne doit être ajouté** — et la suite ne le détecterait pas (voir Pitfall 9) |
| C10 | `.claude/CLAUDE.md:95-101` prescrit un H1 `# Documentation dofus-stuff-machine` pour le sommaire, alors que `docs/sommaire.md:1` porte `# Sommaire de la documentation` | Déjà divergé (et sans effet : `problemes_h1` ignore `sommaire.md`, `tests/test_docs_structure.py:337-345`) ; la phase 2 ne touche pas au H1 du sommaire |
| C11 | §11 : une chaîne de génération de doc **hors dépôt** (`doc-agent.toml`, `output = "docs"`, `.doc-agent/state.json` en `status: "running"`, non suivis par git) peut réécrire `docs/` — « ne rien supprimer, ne pas en dépendre » (`.claude/CLAUDE.md:228`) | Risque d'environnement, pas de conception : le harnais doit rester le juge (mesuré : état gelé au 2026-09-09, aucun processus actif observé ; aucune resynchronisation tentée) |
| C12 | « GSD Workflow Enforcement » : toute écriture passe par un workflow GSD (`.claude/CLAUDE.md:279-292`) | Exécution via `gsd-execute-phase`, pas d'édition directe hors workflow |

## Summary

La phase 2 n'ajoute aucune technologie : elle livre **une page Markdown** (`docs/cli.md`), **une ligne d'index** dans `docs/sommaire.md` et **un module de tests** qui compare la page au parseur réel. Le produit est gelé (`dofus_stuff/**` intouchable), la vérification est `pytest` + bibliothèque standard, et le seul risque réel est celui déjà identifié par le cadrage : un harnais qui *prétend* garder la page mais ne la garde qu'à moitié — exactement la conclusion de la revue de la phase 1 (1 critique + 5 avertissements, tous dans le harnais : `.planning/phases/01-…/01-REVIEW.md`).

La recherche a produit la **surface mesurée** que la page doit décrire, et elle contredit trois hypothèses naturelles écrites dans le cadrage :

1. **`argparse.SUPPRESS` ne masque pas une sous-commande du `--help` sur l'interpréteur épinglé.** Mesuré sur Python 3.14.7 : `add_parser("cache", help=argparse.SUPPRESS)` fait apparaître dans l'aide la ligne `    cache               ==SUPPRESS==` — le placeholder littéral. `stats` et `fill` apparaissent de la même façon dans l'aide de `db`. En revanche, `SUPPRESS` sur une **option** (`clear --all`) la retire bien de l'aide *et* de la ligne d'usage, tout en la laissant acceptée par `parse_args`. Conséquence pour la page et pour les tests : la page doit dire « sous-commande sans description dans l'aide », pas « sous-commande invisible » ; et **aucune liste de surface ne peut être dérivée du texte de l'aide** (elle ne verrait ni `--all`, ni la distinction description/absence de description).
2. **La sonde `parse_args(["db"])` échoue.** `db` et `cache` déclarent `add_subparsers(dest="db_command", required=True)` : `parse_args(["db"])` et `parse_args(["cache"])` sortent en **code 2** (`the following arguments are required: db_command`). Le critère 1 ne peut donc pas être prouvé par une liste de noms nus : il faut une sonde d'argv par sous-commande (`["db","status"]`, `["cache","status"]`, `["optimize","--demo"]`, …), ce que `.claude/CLAUDE.md:134-146` prescrit déjà.
3. **`cache` n'est pas un alias `argparse`.** `dofus_stuff/cli.py:179-195` construit `db` puis `cache` dans une boucle `for db_name in ("db", "cache")` avec les mêmes sous-parseurs. Il n'y a ni `aliases=`, ni `set_defaults`. Mesuré : `vars(db_ns) == vars(cache_ns)` est **faux** (`command` vaut `'db'` ou `'cache'`), mais l'égalité est **vraie sur toutes les autres clés**, y compris `db_command`, pour les cinq sous-commandes et avec des options globales. La preuve d'alias de D-21 doit donc s'écrire « égalité des espaces de noms **modulo la clé `command`** », sinon elle est impossible à satisfaire.

Le reste de la recherche est du même ordre : code de retour 2 et ligne `fetcher.py: error: unrecognized arguments: --offline` pour l'ordre fautif, `Erreur : --offline incompatible avec db sync` (code 1) pour la combinaison interdite, suppression **totale et sans confirmation** des tables `items` et `meta` par `db clear` (`dofus_stuff/database.py:146-152`), et les pièges de `shlex.split` mesurés sur les lignes qui vont réellement apparaître (antislashs Windows avalés silencieusement, commentaire en fin de ligne transformé en arguments, continuation `\` en fin de ligne levant `ValueError`).

**Primary recommendation:** écrire `docs/cli.md` **depuis les tableaux mesurés de ce document** (§ « Mesures »), marquer chaque exemple par un bloc de code étiqueté ` ```console ` (une ligne = une commande complète, sans prompt, sans commentaire, sans continuation), puis prouver la page par un unique module `tests/test_docs_cli.py` qui (a) sonde le parseur public par argv complets, (b) exige la présence des noms et options **d'une liste épinglée explicite** dans la page, (c) extrait les exemples marqués, les découpe avec `shlex.split` et les passe à `build_parser().parse_args`, (d) vérifie l'ordre global-avant-sous-commande et la co-présence `db clear` + avertissement — et qui **écrit noir sur blanc, dans le module, ce qu'il ne garantit pas** (D-26).

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Surface documentée (sous-commandes, options, défauts, synopsis) | Code produit (`dofus_stuff/cli.py` § `build_parser()`) | Doc (`docs/cli.md`) | Le parseur est la source unique ; la page le décrit, elle ne le complète pas (D-16, D-17, D-19) |
| Exemples exécutables cités par la page | Doc (`docs/cli.md`, blocs `console`) | Harnais (`tests/test_docs_cli.py`) | L'exemple est un contenu éditorial ; sa validité est un invariant (D-24, D-25) |
| Preuve d'alias `db` ↔ `cache` | Code produit (`dofus_stuff/cli.py:179-195`) | Harnais | L'alias est une propriété du parseur, pas une phrase de la page : elle se prouve par deux `parse_args` équivalents (D-21, D-14) |
| Avertissement destructeur (`db clear`) | Doc (`docs/cli.md`, hors bloc marqué) | Harnais | Le texte porte l'avertissement, le test exige sa co-présence sur la même ligne et son absence des exemples (D-22) |
| Index et gabarit de page (H1, retour sommaire, UTF-8, brouillons) | Doc (`docs/sommaire.md`, `docs/cli.md`) | Harnais **phase 1** (`tests/test_docs_structure.py`) | Déjà en place et déjà éprouvé : la phase 2 n'ajoute **aucun** contrôle de structure, elle déclenche ceux de la phase 1 en livrant la page et son entrée (D-28, D-06) |
| Ancrage des chemins du bloc « Source de vérité » | Doc (`docs/cli.md` § Source de vérité) | Harnais | Contrat D-03 étendu à la nouvelle page : chemins existants + `build_parser()` nommé (D-30) |
| Lecture de fichier, extraction de blocs, normalisation | Harnais (`tests/conftest.py`) | — | Point unique de lecture (`encoding="utf-8"`) et de découpage Markdown (D-12) : deux scanners concurrents divergeraient (leçon WR-04 de la phase 1) |
| Garde-fou de sûreté (aucune exécution, aucun `.data/`, aucun réseau) | Harnais | — | Seul le harnais peut prouver qu'il ne fait pas de mal : `parse_args` uniquement, `db clear` **parsé** jamais exécuté (C6), `shlex` au lieu de `subprocess` |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `pytest` | 9.1.1 (mesuré : `.venv/Scripts/python.exe -m pytest --version`) | Seule capacité de vérification de la phase | Déjà déclaré (`pyproject.toml:18-21`, `pytest>=8.0`) et déjà configuré (`pyproject.toml:38-39` : `testpaths = ["tests"]`, `pythonpath = ["."]`) ; aucune installation |
| Bibliothèque standard : `argparse`, `shlex`, `re`, `pathlib` | Python 3.14.7 dans `.venv` (plancher déclaré `>=3.11`) | Surface du parseur, découpage des exemples, extraction du marqueur et des options, chemins | Couvre 100 % du besoin ; `shlex` **découpe sans exécuter** (C6/D-22) |
| Markdown « nu » (aucune bibliothèque) | — | Format de `docs/cli.md` | Décision amont (STACK/SUMMARY) reconduite par C2 ; mesuré : `markdown`, `markdown_it`, `commonmark` **non installés** |

**Installation:** aucune. `pip install -e ".[dev]"` est le geste *documenté* par `docs/installation.md`, pas un geste de cette phase.

**Version verification:** `./.venv/Scripts/python.exe --version` → `3.14.7` ; `-m pytest --version` → `pytest 9.1.1` ; plancher déclaré `requires-python = ">=3.11"` (`pyproject.toml:10`, lu). Toutes observées le 2026-09-11.

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `dofus_stuff.cli.build_parser` | module local | Surface publique du parseur CLI | **Toujours** : c'est l'unique source d'ancrage de la phase (`parse_args`, `format_usage`, `format_help`) ; jamais `main()`, jamais d'attribut privé (D-14) |
| Fixtures `docs_dir` / `normalize` de `tests/conftest.py` (`:126-135`) | — | Lecture de `docs/`, comparaison de libellés | Pour tout contrôle lisant une page ; `normalize` a été créé exactement pour « exposer `_normalize` aux modules de test **sans import inter-modules** » |
| `tests/test_docs_structure.py` (`pages_listees`, `problemes_index`, `problemes_h1`, `problemes_retour_sommaire`, `problemes_encodage`) | — | Invariants de structure déjà écrits | **Réutilisés indirectement** : livrer `docs/cli.md` + son entrée d'index suffit à les activer (D-28). Ne rien réécrire, ne rien dupliquer |
| Client de test Flask (`app.test_client()`) | Flask 3.1.3 | — | **Hors périmètre de la phase 2** (aucun libellé d'écran n'est ancré ici) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `shlex.split` sur un exemple | `subprocess.run(exemple)` | Interdit : exécuterait `db clear` / `db sync` et ouvrirait le réseau. `shlex` découpe sans exécuter (C4, C6) |
| Extraire la surface du parseur depuis `format_help()` | Lire `parser._subparsers._group_actions` | API privée interdite par D-14 ; et mesuré : `format_help()` **ne voit pas** `--all` (SUPPRESS) et affiche `==SUPPRESS==` là où il n'y a pas de description |
| Comparer `vars(db_ns) == vars(cache_ns)` | Comparer modulo `command` | Mesuré : l'égalité brute est **toujours fausse** (`command` = `'db'` vs `'cache'`) ; la comparaison brute produirait un test impossible à satisfaire |
| Un second parseur Markdown maison pour le marqueur | Réutiliser/étendre `_lignes_de_code` (`tests/test_docs_code_anchor.py:128-138`) | Un second scanner de blocs de code divergerait du premier (leçon WR-04 : deux invariants du même fichier en désaccord) ; voir Pattern 1 |
| Documenter `db clear --all` | L'omettre | `--all` est accepté mais **jamais lu** par le code (grep `\.all\b` dans `dofus_stuff/cli.py` : aucune occurrence) : le documenter serait inventer une sémantique (D-19). Il doit être **omis**, ce que la limite D-26 autorise explicitement |

## Package Legitimacy Audit

> **Non applicable.** Cette phase n'installe **aucun** paquet : `pytest` est déjà déclaré (`pyproject.toml:18-21`) et présent dans `.venv` (9.1.1 mesuré) ; la politique du projet interdit toute nouvelle dépendance (C2) et aucune bibliothèque Markdown n'est installée (mesuré).

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| (aucun) | — | — | — | — | — | Aucune installation dans cette phase |

**Packages removed due to [SLOP] verdict:** none — aucun verdict n'est inventé : la phase n'installe rien, donc le gate de légitimité n'a pas d'objet.
**Packages flagged as suspicious [SUS]:** none.

## Mesures : la surface réelle du parseur (source de vérité de la page)

Tout ce qui suit est **mesuré**, jamais déduit du texte source : les défauts viennent d'un `parse_args` réel (l'objet `Namespace`), les surfaces des lignes d'usage et d'aide réelles, les codes de retour d'exécutions réelles en sous-processus. Les sondes en sous-processus ont toutes reçu un `--data-dir` **temporaire** ; `.data/dofus.sqlite3` est resté intact (horodatage `Sep 6 23:27` avant et après).

### M1 — Sous-commandes : liste ordonnée et relation `db` / `cache`

`dofus_stuff/cli.py:52` — `    subparsers = parser.add_subparsers(dest="command", required=True)` — puis, dans l'ordre du fichier :

| # | Sous-commande | Déclaration (verbatim) | Ligne |
|---|---------------|------------------------|-------|
| 1 | `version` | `subparsers.add_parser("version", help="Afficher la version Dofus de la base locale")` | `cli.py:54` |
| 2 | `self-test` | `subparsers.add_parser("self-test", help="Vérifier la base locale et des objets connus")` | `cli.py:55` |
| 3 | `search` | `subparsers.add_parser("search", help="Rechercher des objets (local)")` | `cli.py:57` |
| 4 | `item` | `subparsers.add_parser("item", help="Détail d'un équipement par ID Ankama")` | `cli.py:61` |
| 5 | `list` | `subparsers.add_parser("list", help="Lister une page d'équipements")` | `cli.py:64` |
| 6 | `optimize` | `subparsers.add_parser("optimize", help="Optimiser un stuff pour un niveau et une/des caractéristiques", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=_OPTIMIZE_EPILOG)` | `cli.py:68-73` |
| 7 | `db` | `subparsers.add_parser(db_name, help="Gérer la base locale" if db_name == "db" else argparse.SUPPRESS)` (boucle `for db_name in ("db", "cache")`) | `cli.py:179-183` |
| 8 | `cache` | idem, seconde itération de la même boucle — `help` vaut `argparse.SUPPRESS` | `cli.py:179-183` |

**Témoin public de cette liste (mesuré) :** `build_parser().format_usage()` contient `usage: fetcher.py [-h] [--timeout TIMEOUT] [--data-dir DATA_DIR]` puis `{version,self-test,search,item,list,optimize,db,cache}` — extraction par `re.search(r"\{([^}]*)\}", ...)` → exactement `['version', 'self-test', 'search', 'item', 'list', 'optimize', 'db', 'cache']`, **`cache` compris**. C'est la seule surface textuelle qui reste complète malgré `SUPPRESS` (M3), mais elle se replie si la liste s'allonge : ne l'utiliser que comme témoin secondaire, jamais comme source de la liste épinglée.

**Sous-commandes de `db` et de `cache` (identiques, mesuré) :** `status`, `stats`, `sync`, `fill`, `clear` — `cli.py:184-194`. `status` = « Afficher l'état de la base », `sync` = « Forcer la synchronisation complète », `clear` = « Vider la base locale » ; `stats` et `fill` sont déclarés avec `help=argparse.SUPPRESS`.

**M1.3 — Comment `cache` est relié à `db` (vérifié, pas supposé).** Aucun `aliases=`, aucun `set_defaults`, aucune table d'alias : la relation est une **boucle** qui appelle `add_parser` deux fois avec les mêmes sous-parseurs (`cli.py:179-195`). Vérifié par trois mesures indépendantes :

1. Lecture des lignes `cli.py:179-195` — la boucle et le `if db_name == "db"` sont visibles ; aucune occurrence de `aliases` ni de `set_defaults` dans `cli.py`.
2. `parse_args(["db", s])` et `parse_args(["cache", s])` pour `s ∈ {status, stats, sync, fill, clear}` : les deux réussissent, `db_command` est identique, seule la clé `command` diffère (`'db'` vs `'cache'`). Avec `--offline --force-sync --timeout 9 --data-dir T` devant la sous-commande, la comparaison reste vraie sur les 4 globales.
3. Conséquence mesurée pour le test de D-21 : `vars(db_ns) == vars(cache_ns)` est **faux dans les 6 cas** testés (dont `clear --all`) ; l'égalité devient **vraie** si l'on retire la clé `command`. Le contrôle doit donc s'écrire `{k: v for k, v in vars(ns).items() if k != "command"}` et exiger en plus `command in {"db", "cache"}`.

**Analogues de sous-commandes (lues dans le code, `cli.py:283-285`, jamais exécutées) :** `_normalize_db_command` applique `aliases = {"stats": "status", "fill": "sync"}` — `db stats` = `db status` (lecture seule) et `db fill` = `db sync` (réécriture réseau). C'est le fondement mesurable de la phrase « `stats`/`fill` sont des alias sans description dans l'aide » (D-20).

### M2 — Options : globales, par sous-commande, et les 30 d'`optimize`

**Options globales (racine), mesurées** — `parse_args(["version"])` → `Namespace(timeout=15, data_dir=WindowsPath('C:/Users/Red/Documents/Projets/dofus-stuff-machine/.data'), force_sync=False, offline=False, command='version')` :

| Option | `action` / `type` | Défaut **mesuré** | `help` (verbatim) | Ligne |
|--------|-------------------|-------------------|-------------------|-------|
| `--timeout` | `int` | `15` | `Timeout HTTP (s)` | `cli.py:34` |
| `--data-dir` | `Path` | `DEFAULT_DATA_DIR` = `<racine du dépôt>/.data` (absolu, dépendant de la machine — la valeur imprimée est `C:\Users\Red\Documents\Projets\dofus-stuff-machine\.data`) | `f"Répertoire de la base locale (défaut : {DEFAULT_DATA_DIR})"` | `cli.py:35-40` |
| `--force-sync` | `store_true` | `False` | `Ignorer la fenêtre 24h et forcer une vérif / sync version` | `cli.py:41-45` |
| `--offline` | `store_true` | `False` | `Ne pas contacter l'API (échoue si la base locale est vide)` | `cli.py:46-50` |
| `-h`, `--help` | auto | — | `show this help message and exit` | `argparse` |

Mesure obligatoire pour la rédaction : **`--data-dir` imprime un chemin absolu propre à la machine** (`help=f"...{DEFAULT_DATA_DIR}"`, `cli.py:39`). La page doit écrire « par défaut, le dossier `.data/` à la racine du dépôt » — jamais la valeur absolue — et aucun test ne doit comparer cette ligne d'aide au texte de la page.

**Défauts et surfaces par sous-commande (mesurés par `parse_args`) :**

| Sous-commande | Positionnels | Options propres | Défauts mesurés (valeur de l'attribut) |
|---------------|--------------|-----------------|-----------------------------------------|
| `version` | — | — | — |
| `self-test` | — | — | — |
| `search` | `query` (`Terme de recherche (sensible à la casse)`) | `--limit` (`Nombre max de résultats`) | `limit=10` |
| `item` | `ankama_id` (`ID Ankama de l'objet`) | — | — (`type=int`, requis) |
| `list` | — | `--page` (`Numéro de page`), `--size` (`Taille de page`) | `page=1`, `size=5` |
| `optimize` | — | 30 options (M2.3) | voir M2.3 |
| `db` / `cache` | sous-commande requise (`db_command`) | — (sauf `clear --all`, M3) | `db_command` requis : `parse_args(["db"])` → `SystemExit(2)` |

**M2.3 — Les 30 options d'`optimize`, mesurées** (`parse_args(["optimize"])` → `Namespace(... level=None, max_stats=None, base_int=0.0, base_vit=0.0, base_str=0.0, base_cha=0.0, base_agi=0.0, base_wis=0.0, scroll_int=0.0, scroll_vit=0.0, scroll_str=0.0, scroll_cha=0.0, scroll_agi=0.0, scroll_wis=0.0, jet='average', top_k=30, time_limit=5.0, no_cpsat=False, classic_only=False, demo=False, target=None, weight=None, ban=None, force=None, seed=None, stop_when_satisfied=False, auto_points=False, allow_power=False, allow_damages=False, allow_crit_damages=False)` — soit exactement **31 attributs** dont 30 options documentables (+ `command`) :

| Option | Forme (verbatim du source) | Défaut mesuré | `help` (verbatim, `∅` = pas de `help`) | Ligne |
|--------|----------------------------|---------------|----------------------------------------|-------|
| `--level` | `type=int` | `None` | `Niveau du personnage` | `cli.py:74` |
| `--max` | `dest="max_stats", nargs="+"` | `None` | `Caractéristique(s) à maximiser (ex: intelligence)` | `cli.py:75-80` |
| `--base-int` | `type=float` | `0.0` | `Intelligence hors stuff (capital déjà converti)` | `cli.py:81-86` |
| `--base-vit` | `type=float` | `0.0` | `∅` | `cli.py:87` |
| `--base-str` | `type=float` | `0.0` | `∅` | `cli.py:88` |
| `--base-cha` | `type=float` | `0.0` | `∅` | `cli.py:89` |
| `--base-agi` | `type=float` | `0.0` | `∅` | `cli.py:90` |
| `--base-wis` | `type=float` | `0.0` | `∅` | `cli.py:91` |
| `--scroll-int` | `type=float` | `0.0` | `∅` | `cli.py:92` |
| `--scroll-vit` | `type=float` | `0.0` | `∅` | `cli.py:93` |
| `--scroll-str` | `type=float` | `0.0` | `∅` | `cli.py:94` |
| `--scroll-cha` | `type=float` | `0.0` | `∅` | `cli.py:95` |
| `--scroll-agi` | `type=float` | `0.0` | `∅` | `cli.py:96` |
| `--scroll-wis` | `type=float` | `0.0` | `∅` | `cli.py:97` |
| `--jet` | `choices=("min","average","max")` | `'average'` | `Mode de jets d'objets (défaut: average)` | `cli.py:98-103` |
| `--top-k` | `type=int` | `30` | `Candidats top-K par slot` | `cli.py:104` |
| `--time-limit` | `type=float` | `5.0` | `Timeout CP-SAT en secondes` | `cli.py:105-110` |
| `--no-cpsat` | `store_true` | `False` | `Désactiver CP-SAT (greedy + local uniquement)` | `cli.py:111-115` |
| `--classic-only` | `store_true` | `False` | `Ignorer Dofus/Trophées, familier et prysmaradite` | `cli.py:116-120` |
| `--demo` | `store_true` | `False` | `Profil démo niveau 123 / max INT (ignore --level/--max/bases)` | `cli.py:121-125` |
| `--target` | `nargs="+"` | `None` | `Cibles STAT=valeur (ex: intelligence=1200 pa=11)` | `cli.py:126-131` |
| `--weight` | `nargs="+"` | `None` | `Poids STAT=valeur (ex: intelligence=2 vitalite=0.5)` | `cli.py:132-137` |
| `--ban` | `nargs="+", type=int` | `None` | `Ankama IDs interdits` | `cli.py:138-144` |
| `--force` | `nargs="+", type=int` | `None` | `Ankama IDs obligatoires` | `cli.py:145-151` |
| `--seed` | `type=int` | `None` | `Seed RNG` | `cli.py:152` |
| `--stop-when-satisfied` | `store_true` | `False` | `Arrêter dès que les cibles sont atteintes` | `cli.py:153-157` |
| `--auto-points` | `store_true` | `False` | `Répartir automatiquement les points de caracs` | `cli.py:158-162` |
| `--allow-power` | `store_true` | `False` | `Autoriser la puissance à la place des caracs` | `cli.py:163-167` |
| `--allow-damages` | `store_true` | `False` | `Autoriser les dommages à la place des dommages élémentaires` | `cli.py:168-172` |
| `--allow-crit-damages` | `store_true` | `False` | `Autoriser les dommages critiques à la place des dommages élémentaires` | `cli.py:173-177` |

**Note D-19 (déjà satisfaite par la mesure) :** **onze** options n'ont **aucun `help`** — `--base-vit`, `--base-str`, `--base-cha`, `--base-agi`, `--base-wis`, `--scroll-int`, `--scroll-vit`, `--scroll-str`, `--scroll-cha`, `--scroll-agi`, `--scroll-wis` (mesuré sur les 30 déclarations `add_argument` du bloc `cli.py:74-177`). Les 30 options se répartissent donc en **19 avec `help` et 11 sans**. Mesure associée : un heuristique de texte qui conclut « pas d'aide » quand rien ne suit le métavar sur la même ligne se trompe sur `--jet`, `--time-limit` et `--stop-when-satisfied` (argparse replie leur aide sur la ligne suivante) — la comptabilité doit se faire sur le source, pas sur le texte de l'aide. La page les décrit par synopsis + défaut, sans sémantique inventée.

**M2.4 — Le mode interactif (mesuré, jamais exécuté).** `needs_interactive_optimize` (`dofus_stuff/optimize/profile_input.py:405-413`) renvoie `True` si et seulement si `demo` est faux **et** `level` est `None` **et** `max_stats` est falsy :

```python
def needs_interactive_optimize(args) -> bool:
    """True si aucun profil n'est fourni via flags."""
    if getattr(args, "demo", False):
        return False
    if getattr(args, "level", None) is not None:
        return False
    if getattr(args, "max_stats", None):
        return False
    return True
```

Donc `python fetcher.py --offline optimize` (sans `--level`, sans `--max`, sans `--demo`) est **valide pour le parseur** et déclenche les questions guidées citées par l'épilog (`cli.py:24-31` : `fetcher.py optimize --offline optimize` puis `(mode interactif : questions guidées)`). Un exemple de ce type est donc légitime dans la page ; le harnais le **parse** sans jamais l'exécuter (C6).

### M3 — `argparse.SUPPRESS` : ce qu'il masque réellement (mesuré sur Python 3.14.7)

`argparse.SUPPRESS` vaut la chaîne `'==SUPPRESS=='`. Sa mécanique **diffère selon le type d'entrée**, et c'est le piège central de cette phase :

| Cas | Déclaration réelle | Effet **mesuré** sur `format_help()` | Effet mesuré sur `format_usage()` |
|-----|--------------------|--------------------------------------|-----------------------------------|
| Sous-commande | `subparsers.add_parser("cache", help=argparse.SUPPRESS)` (`cli.py:180-183`) | L'entrée **reste**, avec le texte littéral `==SUPPRESS==` : la ligne exacte est `    cache               ==SUPPRESS==` | `cache` reste dans le métavar : `{version,self-test,search,item,list,optimize,db,cache}` |
| Sous-commande de sous-parseur | `db_sub.add_parser("stats", help=argparse.SUPPRESS)`, idem `fill` (`cli.py:186`, `:188`) | Les entrées **restent** : `    stats               ==SUPPRESS==` et `    fill                ==SUPPRESS==` dans l'aide de `db` **et** dans celle de `cache` (2 occurrences par aide) | `stats` et `fill` restent dans `{status,stats,sync,fill,clear}` |
| Option | `clear_parser.add_argument("--all", action="store_true", help=argparse.SUPPRESS)` (`cli.py:190-194`) | L'entrée **disparaît** de la table de `db clear` (aide de `db clear` : seules `usage:` et `-h, --help`) | `--all` **disparaît aussi de la ligne d'usage** (`usage: fetcher.py db clear [-h]`) |
| Contrôle (repro minimale hors dépôt) | `q.add_argument("--cache", help=argparse.SUPPRESS)` | Disparaît (`'--cache' present dans l'aide : False`) | — |

**Conséquences mécaniques, mesurées, pour un test qui comparerait une liste documentée à `format_help()` :**

1. **Une surface dérivée du texte de l'aide est structurellement incomplète** : `--all` est accepté par le parseur mais invisible partout (`False` dans l'aide *et* dans l'usage). Aucun test ne peut donc « découvrir » `--all` depuis une sortie texte ; c'est la justification mesurée de la limite D-26 et la raison pour laquelle la page l'omet.
2. **Un filtre naïf « ignorer les lignes dont la description est `==SUPPRESS==` » ferait échouer le critère 1** : il retirerait `cache` de la liste autoritative, et le test exigerait alors que la page **omette** `cache` — exactement l'inverse du critère 1 qui exige de le documenter. Il retirerait aussi `stats`/`fill`, que D-20 demande de **signaler comme alias sans description**.
3. **Aucune assertion ne doit prétendre que `SUPPRESS` « masque » une sous-commande du `--help`.** La formulation exacte que la page peut porter est : « `cache` et les sous-commandes `stats`/`fill` n'ont **pas de description dans l'aide** (elles y apparaissent sous la forme `==SUPPRESS==`) ». Un test qui exigerait l'**absence** de `stats`/`fill` de `format_help()` échouerait toujours ; un test qui exigerait leur **présence** dans la page est en revanche satisfiable et c'est la formulation de D-20.

### M4 — `shlex.split` sur les lignes qui vont réellement apparaître (mesuré)

Résultats bruts (ligne → `shlex.split` → verdict `parse_args`), tous produits par exécution :

| Ligne | `shlex.split` | `parse_args` |
|-------|---------------|--------------|
| `python fetcher.py --offline db status` | `['python','fetcher.py','--offline','db','status']` | **OK** (`command='db'`, `db_command='status'`) |
| `python fetcher.py --offline search "Épée de Boisaille"` | `['python','fetcher.py','--offline','search','Épée de Boisaille']` | **OK** (accents conservés) |
| `python fetcher.py --offline search "Cape d'Atcham" --limit 5` | `[... "Cape d'Atcham", '--limit', '5']` | **OK** (apostrophe dans guillemets) |
| `python fetcher.py --offline search Epée --limit=10` | `[... 'Epée', '--limit=10']` | **OK** (`=`-joint accepté par argparse) |
| `python fetcher.py --offline optimize --target intelligence=1200 pa=11` | `[... '--target', 'intelligence=1200', 'pa=11']` | **OK** (`nargs='+'`, deux jetons) |
| `python fetcher.py --offline optimize --target "intelligence=1200 pa=11"` | `[... '--target', 'intelligence=1200 pa=11']` | **OK** (un jeton, sémantique différente) |
| `python fetcher.py --offline optimize --ban 123 --force 44 100` | `[... '--ban','123','--force','44','100']` | **OK** |
| `python fetcher.py --offline optimize` | `[... '--offline','optimize']` | **OK** (mode interactif, jamais exécuté) |
| `python fetcher.py --timeout 30 --data-dir .data --offline db status` | `[... '--data-dir','.data']` | **OK** |
| **`python fetcher.py --data-dir C:\Users\Red\.data --offline db status`** | `[... '--data-dir', 'C:UsersRed.data']` — **les antislashs sont avalés silencieusement** | **OK** (!) — la valeur est fausse, la sonde passe |
| **`python fetcher.py --data-dir "C:\Users\Red\.data" --offline db status`** | `[... '--data-dir', 'C:\\Users\\Red\\.data']` — préservés | **OK**, `data_dir` = `C:\Users\Red\.data` |
| `python fetcher.py --data-dir C:/Users/Red/.data --offline db status` | `[... 'C:/Users/Red/.data']` | **OK**, `Path` normalise en `C:\Users\Red\.data` |
| **`python fetcher.py --offline db status   # etat de la base`** | `[... 'db','status','#','etat','de','la','base']` | **SystemExit(2)** |
| `python fetcher.py --offline search *` | `[... 'search','*']` | **OK** (le glob reste littéral : `shlex` n'étend rien, le shell le ferait) |
| `python fetcher.py --offline search $HOME` | `[... 'search','$HOME']` | **OK** (aucune expansion : la page ne doit pas montrer de variable de shell) |
| **`python fetcher.py --offline optimize --demo \`** (continuation) | `ValueError: No escaped character` | **non analysable** — l'exception doit devenir une assertion D-13 |
| `python fetcher.py --offline search "Cape d'Atcham` (guillemet non fermé) | `ValueError: No closing quotation` | **non analysable** |

**Règles de rédaction qui en découlent (chacune adossée à une ligne mesurée ci-dessus) :**

- Un chemin Windows dans `--data-dir` **doit** être entre guillemets (`"C:\Users\Red\.data"`), sinon `shlex` le mutile sans que la sonde s'en aperçoive ; mieux vaut écrire une forme portable (`.data`, ou `C:/Users/…`).
- **Aucun commentaire en fin de ligne** dans un exemple marqué : `# …` devient des arguments et le parseur sort en code 2.
- **Aucune continuation** de ligne par `\` : `shlex.split` lève `ValueError`.
- **Aucun métacaractère de shell** (`*`, `$`, `~`) : `shlex` ne les étend pas, donc la page enseignerait un comportement que le lecteur n'obtiendra pas ; `parse_args` les accepte en silence, ce qui rend le contrôle aveugle.
- Le `ValueError` de `shlex` **et** le `SystemExit(2)` de `parse_args` doivent tous deux être convertis en `AssertionError` localisante (page + valeur attendue + fichier de code, D-13) : laisser passer un `SystemExit` produit un `FAILED` accompagné de la trace d'`argparse`, ce que la phase 1 a déjà identifié comme un défaut de harnais.

### M5 — Ordre des options globales : codes de retour et messages réels (mesurés en sous-processus)

Toutes les exécutions ci-dessous ont été lancées avec l'interpréteur épinglé et un `--data-dir` temporaire (`"$T/base"`) ; `stderr` est recopié verbatim.

| Commande | Code | `stderr` |
|----------|------|----------|
| `python fetcher.py --data-dir <tmp> --offline db status` | **0** | *(vide)* — `stdout` : `Fichier : …\base\dofus.sqlite3`, `Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0` |
| `python fetcher.py --data-dir <tmp> db status --offline` | **2** | `usage: fetcher.py [-h] [--timeout TIMEOUT] [--data-dir DATA_DIR]` / `                  [--force-sync] [--offline]` / `                  {version,self-test,search,item,list,optimize,db,cache} ...` puis **`fetcher.py: error: unrecognized arguments: --offline`** |
| `python fetcher.py --data-dir <tmp> --offline db sync` | **1** | **`Erreur : --offline incompatible avec db sync`** |
| `python fetcher.py --data-dir <tmp> --offline version` | **1** | `Erreur : Base locale vide et --offline : impossible de synchroniser` |
| `python fetcher.py --data-dir <tmp> status` | **2** | `… invalid choice: 'status' (choose from 'version', 'self-test', 'search', 'item', 'list', 'optimize', 'db', 'cache')` |

**Pourquoi argparse se comporte ainsi (explication mécanique, lisible dans le source) :** les quatre options globales sont déclarées sur le **parseur racine** (`cli.py:34-50`), c'est-à-dire sur l'objet qui traite les arguments *avant* de déléguer à une sous-commande ; `add_subparsers(...)` (`cli.py:52`) consomme le jeton de sous-commande puis remet les arguments restants au sous-parseur, qui ne connaît que ses propres options. Un `--offline` placé après `db status` n'est donc reconnu par **aucun** des deux niveaux : le sous-parseur `db` n'a pas cette option, et la racine a déjà fini son analyse — d'où le diagnostic `unrecognized arguments` de la racine et le code 2. Ce n'est pas une convention de style mais une contrainte du parseur : la page peut l'affirmer **avec sa cause**, pas seulement « par observation ».

**Corollaire pour la page (donnée mesurée) :** `--offline` et `db sync` sont **incompatibles** ; toute commande `db sync` (ou `cache fill`) doit donc être montrée **sans** `--offline`. Cela interdit de reconduire à `docs/cli.md` la règle de la page d'installation (« toutes les commandes `fetcher.py` portent `--offline` », vérifiée par `tests/test_docs_code_anchor.py:184-189`) : elle est propre à `installation.md` et serait mécaniquement fausse ici.

### M6 — Commandes destructrices : inventaire dérivé du code (rien n'a été exécuté)

| Commande | Effet réel (lu dans le code, jamais exécuté) | Confirmation ? | Preuve |
|----------|----------------------------------------------|----------------|--------|
| `db clear` / `cache clear` | `DELETE FROM items` **et** `DELETE FROM meta`, `commit()` — la base locale est vidée **entièrement** (objets + métadonnées de version) | **aucune** : `main()` appelle directement `db.clear()` puis affiche `Base vidée : N entrée(s) supprimée(s).` | `dofus_stuff/database.py:146-152` (verbatim ci-dessous) ; `cli.py:357-360` |
| `db clear --all` | identique : le drapeau est **accepté mais jamais lu** (`grep '\.all\b' dofus_stuff/cli.py` → aucune occurrence) | aucune | `cli.py:190-194` + absence de lecture |
| `db sync` / `cache fill` | `ensure_up_to_date(db, force=True, offline=False, …)` : **réécrit** la base (`replace_kind` fait `DELETE FROM items WHERE kind = ?` puis réinsère) | non | `cli.py:344-355`, `dofus_stuff/database.py:117-132`, `dofus_stuff/sync.py:16-70` |
| `db stats` / `cache stats` | **lecture seule** : `_normalize_db_command` renvoie `status` → `_print_db_status` | sans objet | `cli.py:283-285`, `cli.py:336-342` |
| `--force-sync` (globale) | force la fenêtre de vérification de 24 h pour les commandes qui chargent le catalogue ; avec `--offline` et une base non vide, `ensure_up_to_date` sort en `{"action": "skip", "reason": "offline"}` | sans objet | `cli.py:41-45`, `sync.py:34-45` |

Verbatim de la seule suppression définitive (`dofus_stuff/database.py:146-152`) :

```python
    def clear(self) -> int:
        """Vide items + meta. Retourne le nombre d'items supprimés."""
        conn = self._require_conn()
        cur = conn.execute("DELETE FROM items")
        conn.execute("DELETE FROM meta")
        conn.commit()
        return cur.rowcount
```

**Ce que le test de la page peut exiger (et rien de plus) :** (a) `db clear` (et son alias `cache clear`) **apparaît** dans la page ; (b) toute ligne qui contient ce jeton contient aussi un avertissement destructeur (jeton normalisé `destruct`, qui couvre « destructif », « destructrice », « destruction » — `normalize("destructrice")` ne contient **pas** `destructif`, mesuré par construction de la normalisation) ; (c) ce jeton **n'apparaît sur aucune ligne d'exemple marquée**. La qualité « hors parcours recommandé » n'est pas décidable mécaniquement en général : elle est approchée par (c), qui interdit de le présenter comme une commande à recopier (voir Open Question 2).

**Séparation stricte à écrire dans le test (C6 / D-22) :** `db clear` et `cache clear` sont **parsés** (sonde `parse_args`) pour prouver que la page cite une commande réelle, et **jamais exécutés**. Le commentaire du module doit le dire, car un lecteur ultérieur pourrait confondre les deux.

### M7 — Frontières à ne pas franchir dans la page (mesures négatives utiles)

- **L'épilog du parseur est un piège.** `_OPTIMIZE_EPILOG` (`cli.py:24-31`) utilise `%(prog)s` dans le sous-parseur `optimize`, dont le `prog` est `<prog racine> optimize` : la ligne imprimée est `  fetcher.py optimize --offline optimize --demo` — la sous-commande est **dupliquée**, et passée telle quelle à `parse_args` (`['optimize','--offline','optimize','--demo']`) elle sort en **code 2**. Le texte de l'épilog dépend en outre du `prog` réel (lancé par `python -` il devient `  - optimize --offline optimize --demo`). **Conclusion : la page ne recopie jamais les exemples de l'épilog, et aucun test ne les dérive.**
- **`--help` global :** présent sur chaque parseur (`-h, --help`) ; à exclure explicitement de toute surface dérivée de l'aide, comme le fait déjà `_options_aide_web()` (`tests/test_docs_code_anchor.py:123-126`).
- **`db`/`cache` nus :** `SystemExit(2)` (`the following arguments are required: db_command`) — une sonde « une sous-commande = un jeton nu » est fausse pour ces deux-là.
- **`python fetcher.py cache fill` :** parse, mais c'est un `sync` réseau — la page ne doit jamais le donner dans un parcours hors-ligne.
- **Aucune sonde de cette phase n'a exécuté `main()`** : la totalité des mesures ci-dessus passe par `build_parser()`/`parse_args` (jamais de `Catalog`, de `Database` ni de `main()` dans le processus de test), et les cinq relevés en sous-processus ont tous reçu un `--data-dir` sous le dossier temporaire du système.

## Architecture Patterns

### System Architecture Diagram

```
          docs/cli.md (contenu rédigé, français)
          ┌───────────────────────────────────────────────┐
          │ H1 « CLI » + intro + 1 section par sous-cmd   │
          │ tables d'options (défauts mesurés)            │
          │ blocs ```console  = exemples marqués          │
          │ prose + blocs ```text = avertissement db clear│
          │ ## Source de vérité → build_parser(), fetcher │
          │ [Retour au sommaire](sommaire.md)             │
          └───────────────┬───────────────────────────────┘
                          │ livrée dans la même unité de travail
                          ▼
          docs/sommaire.md ──(1 ligne d'index « CLI »)──► cli.md
                          │
                          │ déclenche (sans nouveau code)
                          ▼
   tests/test_docs_structure.py  ──►  H1 = libellé d'index, retour sommaire,
   (phase 1, inchangé)                exhaustivité bidirectionnelle sommaire ↔ docs/**,
                                      UTF-8 strict, pas de jeton de brouillon
                                             ── rouge si la page ou l'entrée manque ──┐
                                                                                     │
   dofus_stuff/cli.py :: build_parser()  ─── source de vérité (lecture seule)          │
        │                                                                              │
        │  parse_args / format_usage / format_help  (D-14 : API publique uniquement)   │
        ▼                                                                              │
   tests/test_docs_cli.py  ──►  1. liste épinglée de sous-commandes : page présente ?  │
   (nouveau, phase 2)           2. sonde d'argv par sous-commande : parse_args OK ?    │
                                3. liste épinglée d'options + sonde de valeur : OK ?    │
                                4. exemples ```console : shlex.split → parse_args      │
                                5. ≥1 exemple global-avant-sous-commande                │
                                6. jeton destructeur + avertissement même ligne,        │
                                   jamais sur une ligne d'exemple ─────────────────────┘
                                7. cache ≡ db (espaces de noms modulo `command`)
```

Le flux est **page → parseur** pour chaque contrôle, plus une **liste épinglée explicite** qui joue le rôle du sens inverse (D-26) : la page ne peut pas inventer une sous-commande ou une option (le parseur la refuse), et la liste épinglée empêche la page de disparaître silencieusement en supprimant une section (le contrôle de présence échoue). Aucun contrôle n'exécute la moindre commande du produit.

### Recommended Project Structure

```
docs/
├── sommaire.md          # + 1 ligne d'index « [CLI](cli.md) » (D-28) — seule modification d'une page existante
├── installation.md      # inchangée (phase 1)
└── cli.md               # NOUVELLE page (D-16, D-18, D-20, D-22, D-30)
tests/
├── conftest.py          # + scanner de blocs partagé, exposé en fixture (D-12)
├── test_docs_structure.py   # inchangé — activé par la nouvelle page et son entrée
├── test_docs_code_anchor.py # signature d'un test adaptée (un seul scanner de blocs, D-12)
└── test_docs_cli.py     # NOUVEAU module : CLI-01, CLI-02, CLI-03
README.md                # inchangé (D-29)
dofus_stuff/**           # intact (gelé pour cette phase)
```

### Pattern 1 : marqueur de bloc partagé — la balise `console`

**What:** un « exemple de commande » de `docs/cli.md` est **une ligne non vide d'un bloc de code dont la balise d'ouverture est `` ```console ``**. Toute autre ligne (prose, inline code, bloc `` ```text ``) est hors du contrôle — c'est l'application de D-24.

**When to use:** uniquement dans `tests/test_docs_cli.py` pour l'extraction des exemples. Les autres balises de la page (`text` pour les sorties et l'avertissement) restent libres.

**Pourquoi la balise plutôt qu'un préfixe de ligne (alternatives mesurées, écartées) :**

| Candidat | Verdict | Raison |
|----------|---------|--------|
| Balise de bloc `` ```console `` (retenu) | retenu | Correspond littéralement à D-24 (« blocs de code **balisés** comme tels ») ; impossible à confondre avec une commande citée en prose ; la ligne de la page **est** la commande, donc l'assertion « verbatim » de D-25 porte sur le texte réel ; aucune interaction avec l'avertissement `db clear` (qui vit hors bloc marqué) |
| Préfixe de prompt `$ ` dans une ligne de bloc | écarté | Éloigne la ligne de la commande réelle (il faut retirer `$ ` avant `shlex`), et entre en tension avec le critère 4 : l'avertissement doit tenir sur la même ligne que `db clear`, ce qui obligerait à un commentaire — interdit par M4 |
| Préfixe de ligne `python fetcher.py ` sans délimiteur de bloc | écarté | Ne satisfait pas D-24 : une mention en prose qui commence la ligne compterait comme exemple ; le contrôle sortirait du périmètre « blocs de code » |
| Balise existante `` ```bash `` | écarté | `installation.md` l'utilise déjà pour des commandes qui ne sont **pas** des exemples de la page CLI ; réutiliser la balise rendrait le marqueur ambigu (« quel `bash` compte ? ») |

**Règles de rédaction qui vont avec (chacune vérifiable, chacune adossée à M4) :** un bloc `console` ne contient que des lignes de commande complètes, commençant par `python fetcher.py `, sans prompt, sans commentaire, sans continuation `\`, sans métacaractère de shell. Ce sont exactement les quatre cas mesurés comme cassant `shlex`/`parse_args` ou comme les rendant aveugles.

**Implémentation (un seul scanner de blocs, D-12) :** le scanner actuel `tests/test_docs_code_anchor.py:128-138` jette la balise et renvoie les lignes de **tous** les blocs :

```python
def _lignes_de_code(texte: str) -> list[str]:
    """Lignes situées entre les délimiteurs de blocs de code Markdown (trois accents graves)."""
    lignes: list[str] = []
    dans_bloc = False
    for ligne in texte.splitlines():
        if DELIMITEUR_CODE.match(ligne):
            dans_bloc = not dans_bloc
            continue
        if dans_bloc:
            lignes.append(ligne)
    return lignes
```

Il doit être **remplacé, à un seul endroit**, par un scanner qui conserve la balise, dans `tests/conftest.py` (D-12), exposé aux modules par des fixtures — c'est le patron déjà utilisé par `normalize` (« Expose `_normalize` aux modules de test **sans import inter-modules** », `tests/conftest.py:132-135`) :

```python
# tests/conftest.py (nouveau bloc, après _normalize)
BALISE_EXEMPLE = "console"
DELIMITEUR_BLOC = re.compile(r"^\s*```(?P<balise>[A-Za-z0-9_-]*)\s*$")

def _blocs_de_code(texte: str) -> list[tuple[str, list[str]]]:
    """Blocs de code Markdown : (balise d'ouverture, lignes), dans l'ordre du fichier."""
    blocs: list[tuple[str, list[str]]] = []
    balise, lignes, dans_bloc = "", [], False
    for ligne in texte.splitlines():
        trouve = DELIMITEUR_BLOC.match(ligne)
        if trouve:
            if dans_bloc:
                blocs.append((balise, lignes))
            else:
                balise, lignes = trouve.group("balise"), []
            dans_bloc = not dans_bloc
            continue
        if dans_bloc:
            lignes.append(ligne)
    return blocs

def _lignes_de_code(texte: str) -> list[str]:
    """Lignes de tous les blocs de code, toutes balises confondues (comportement phase 1)."""
    return [ligne for _, lignes in _blocs_de_code(texte) for ligne in lignes]

def _lignes_exemple(texte: str) -> list[str]:
    """Lignes non vides des blocs marqués ```console — Les « exemples » de D-24."""
    return [
        ligne.strip()
        for balise, lignes in _blocs_de_code(texte)
        if balise == BALISE_EXEMPLE
        for ligne in lignes
        if ligne.strip()
    ]
```

`tests/test_docs_code_anchor.py` est alors modifié **au minimum** : son test `test_cli_examples_of_installation_page_parse(docs_dir)` (`:158`) reçoit la fixture `lignes_de_code` et appelle `lignes_de_code(texte)` au lieu de `_lignes_de_code(texte)`. Comportement identique au caractère près (même boucle, même bascule).

> **Différence assumée, vérifiée :** `DELIMITEUR_BLOC` exige que la ligne de clôture soit **exactement** une clôture (balise vide ou identifiant), là où `DELIMITEUR_CODE` (`^\s*````) acceptait toute ligne commençant par trois accents graves. Mesuré sur les pages livrées (`grep '^\s*```` sur `docs/`) : `installation.md` ne contient que des clôtures nues et les balises `` ```bash `` / `` ```text `` — aucune ligne de contenu ne commence par trois accents graves. La différence est donc sans effet aujourd'hui, et **plus stricte** (une clôture mal formée serait signalée plutôt qu'absorbée).

> **Régression obligatoire (leçon CR-01/WR-05) :** après ce déplacement, prouver que le test de la page d'installation **mord encore** — dans une copie jetable, retirer `--offline` d'une commande de `installation.md` et vérifier que `test_cli_examples_of_installation_page_parse` échoue en nommant le drapeau manquant. Un déplacement de helper qui n'est pas prouvé par une mutation est une perte de couverture silencieuse.

### Pattern 2 : ancrage page → parseur avec liste épinglée (CLI-01, CLI-02)

**What:** deux listes épinglées portent le contrat : les **sous-commandes** documentables (nom + sonde d'argv) et les **options** (nom + valeur d'essai). Pour chaque entrée : (a) le nom apparaît dans la page, sinon échec nommant la page, le nom attendu et `dofus_stuff/cli.py` ; (b) la sonde est acceptée par `build_parser().parse_args`, sinon échec nommant la sonde et le fichier.

**When to use:** c'est la forme prescrite par `.claude/CLAUDE.md:134-146` (C7) et la façon dont D-26 rend la « liste explicite » opposable.

**Sondes de sous-commandes — mesurées, aucune n'est un jeton nu** (`db` et `cache` nus sortent en code 2) :

```python
# tests/test_docs_cli.py
SONDES_SOUS_COMMANDES = (
    ("version", ["version"]),
    ("self-test", ["self-test"]),
    ("search", ["search", "Atcham"]),
    ("item", ["item", "44"]),
    ("list", ["list"]),
    ("optimize", ["optimize", "--demo"]),
    ("db", ["db", "status"]),
    ("cache", ["cache", "status"]),
)
```

**Sondes d'options globales** (les 4 du critère 2, avec valeur d'essai pour les options à valeur) :

```python
SONDES_GLOBALES = (
    ("--timeout", ["--timeout", "5", "version"]),
    ("--data-dir", ["--data-dir", "x", "version"]),
    ("--force-sync", ["--force-sync", "version"]),
    ("--offline", ["--offline", "db", "status"]),
)
```

**Sondes des 30 options d'`optimize` : `(option, valeur d'essai|None)` — table mesurée, verdict mesuré : 30/30 acceptées.** La valeur d'essai est **obligatoire** pour toute option à valeur, et en particulier pour une option à `choices` : mesuré, la sonde tri-état de la phase 1 (`[opt]`, `[opt,"1"]`, `[opt,"x"]`, `tests/test_docs_code_anchor.py:107-121`) **déclare à tort `--jet` comme inventée** (les trois essais échouent, seul `average` passe).

| `--level` `"123"` | `--max` `"intelligence"` | `--base-int` `"100"` | `--base-vit` `"100"` | `--base-str` `"100"` | `--base-cha` `"100"` |
| `--base-agi` `"100"` | `--base-wis` `"100"` | `--scroll-int` `"50"` | `--scroll-vit` `"50"` | `--scroll-str` `"50"` | `--scroll-cha` `"50"` |
| `--scroll-agi` `"50"` | `--scroll-wis` `"50"` | `--jet` `"average"` | `--top-k` `"40"` | `--time-limit` `"10"` | `--no-cpsat` `None` |
| `--classic-only` `None` | `--demo` `None` | `--target` `"intelligence=1200"` | `--weight` `"intelligence=2"` | `--ban` `"123"` | `--force` `"44"` |
| `--seed` `"7"` | `--stop-when-satisfied` `None` | `--auto-points` `None` | `--allow-power` `None` | `--allow-damages` `None` | `--allow-crit-damages` `None` |

(Le tableau est donné sur 6 colonnes ; la structure à écrire dans le module est un tuple de 30 couples `("--level", "123")`, avec `None` pour les `store_true`. Sondage : `["optimize", option]` si `None`, sinon `["optimize", option, valeur]`.)

**Direction page → parseur des options d'`optimize` (piège de périmètre) :** les options **citées** par la page doivent être extraites **des tables d'options** de la section `optimize` (lignes commençant par `|` contenant un jeton `` `--xxx` ``), **jamais du texte entier de la section** : les exemples de la section citent aussi `--offline`, option globale refusée par le sous-parseur `optimize`. C'est exactement la classe d'erreur WR-01 de la phase 1 (un motif appliqué à un périmètre trop large ou trop étroit produit un faux diagnostic).

### Pattern 3 : extraction et validation des exemples (CLI-03, critères 3 et 4a)

**What:** pour chaque ligne de `_lignes_exemple(texte)` :

1. la ligne apparaît **verbatim** dans le fichier — assert `exemple in texte`, sans normalisation (D-11 ne s'applique **pas** aux commandes : une option se compare telle quelle, accents et espaces compris) ;
2. elle commence par les deux jetons attendus (`argv[:2] == ["python", "fetcher.py"]`) — plus robuste que `argv.index("fetcher.py")` employé en phase 1, qui casse si une valeur vaut `fetcher.py` ;
3. `shlex.split` réussit (un `ValueError` devient une assertion D-13) ;
4. le reste (`argv[2:]`) est accepté par `build_parser().parse_args` (`SystemExit` converti en assertion D-13, jamais laissé traverser) ;
5. chaque sous-commande de la liste épinglée possède **au moins un** exemple marqué (couverture : c'est la partie **falsifiable** de l'assertion de présence, cf. Validation Architecture) ;
6. **au moins un** exemple porte une option globale **avant** sa sous-commande et la sous-commande `optimize` : `argv[2:4] == ["--offline", "optimize"]` (critère 4a, D-27).

**When to use:** le contrôle des exemples ne s'applique qu'aux blocs `console` ; les commandes citées en prose (par exemple la forme fautive `db status --offline` décrite dans l'installation), les blocs `text` et les blocs d'avertissement en sont exclus par construction (D-24).

### Pattern 4 : avertissement destructeur co-localisé (critère 4b, D-22)

**What:** trois assertions, toutes mécaniques, sur le **texte brut** de la page (jamais par section : l'en-tête de page échapperait à une règle évaluée par section — leçon WR-02) :

1. **présence** : la page cite le jeton destructeur `db clear` (sinon la règle suivante serait vide, donc infalsifiable) ;
2. **co-présence sur la même ligne** : toute ligne contenant `db clear` (ou `cache clear`) contient aussi le jeton normalisé `destruct` — qui couvre « destructif », « destructrice », « destruction » (comparaison sur la ligne **normalisée**, D-11) ;
3. **jamais un exemple** : aucune ligne de `_lignes_exemple(texte)` ne contient le jeton destructeur — c'est la traduction testable de « jamais proposé comme étape » (D-22).

```python
JETON_DESTRUCTEUR = re.compile(r"\b(?:db|cache)\s+clear\b")
JETON_AVERTISSEMENT = "destruct"
```

**Limite écrite dans le test (D-26) :** « hors parcours recommandé » n'est pas décidable en général ; (2) et (3) l'approchent — une phrase qui encadrerait `db clear` d'un numéro d'étape **et** de l'avertissement passerait. Le commentaire du test doit le dire.

### Pattern 5 : preuve d'alias par espace de noms (D-21)

**What:** pour chacune des cinq sous-commandes de `db` (`status`, `stats`, `sync`, `fill`, `clear`), comparer les espaces de noms **modulo la clé `command`** :

```python
def _espace_de_noms(argv: list[str]) -> dict:
    ns = build_cli_parser().parse_args(argv)
    return {cle: valeur for cle, valeur in vars(ns).items() if cle != "command"}

for sous_commande in ("status", "stats", "sync", "fill", "clear"):
    assert _espace_de_noms(["db", sous_commande]) == _espace_de_noms(["cache", sous_commande])
```

Plus la partie « page » de la même affirmation : la section `cache` de la page doit déclarer l'alias (elle doit contenir `db` **et** le jeton normalisé `alias`) **et ne doit pas dupliquer la description** de `db` : mesurable en exigeant que les trois `help` du groupe (`Afficher l'état de la base`, `Forcer la synchronisation complète`, `Vider la base locale`) **n'apparaissent pas** dans la section `cache` — ils n'appartiennent qu'à la section `db` (D-20). C'est un ancrage au code en plus d'un contrôle anti-duplication.

### Anti-Patterns to Avoid

- **Un contrôle à sens unique qui se nomme comme s'il était bidirectionnel** (CR-01 de la phase 1) : nommer explicitement `test_..._documentees_et_acceptees` un test qui ne fait que page → parseur, ou écrire une docstring « les deux sens sont vérifiés ». Nommer ce qui est fait, et consigner la limite (D-26).
- **Dériver la surface autoritative de `format_help()`** : mesuré, `--all` y est invisible et `==SUPPRESS==` y remplace des descriptions (M3). La liste autoritative est **épinglée dans le test**, elle ne se découvre pas.
- **Comparer deux choses de nature différente** (WR-04) : un jeton de page `` `--limit=10` `` n'est pas l'option `--limit` ; un nom de page n'est pas une cible d'index. Extraire d'un côté comme de l'autre la même forme (`--[a-z-]+` sans `=valeur`).
- **Un motif trop étroit** (WR-01/WR-03) : restreindre les chemins cités aux `.py`, ou chercher `#` seulement en début de cible ; ici : chercher le jeton destructeur avec `(?:db|cache)`, pas seulement `db`, et l'insensibilité aux espaces multiples.
- **Une règle évaluée par section** (WR-02) : l'en-tête de la page et les lignes hors `##` échapperaient au contrôle. La règle destructive et la règle d'exemple s'appliquent au **texte entier**.
- **Un test de mutation qui nomme en dur une page ou un nom qu'une phase ultérieure livrera légitimement** (WR-05) : ne pas encoder de mutation en dur dans ce module ; les dérives sont injectées pendant l'exécution, dans une copie jetable, jamais sur l'arbre livré (le test de mutation formel est prévu en phase 6, GARD-03).
- **Un helper de test dupliqué** : deux scanners de blocs de code, ou une seconde implémentation de la normalisation, divergeront (WR-04 : deux invariants du même fichier en désaccord). Un seul scanner (Pattern 1), une seule normalisation (`normalize`).
- **Lire un fichier de doc sans encodage explicite** : `read_text(encoding="utf-8")` partout (fins de ligne CRLF sur ce poste).
- **Laisser échapper un `SystemExit`** : `pytest` le rapporte en `FAILED` avec la trace d'`argparse`, message non localisant ; la convention de la phase 1 est de le convertir (Pattern 4 de la phase 1, `tests/test_docs_code_anchor.py:107-121`).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Découper une ligne de commande | Un `split(" ")` maison, une regex de tokens | `shlex.split` | Mesuré : guillemets, apostrophes, accents, `--limit=10` sont traités correctement ; les cas refusés (guillemet non fermé, antislash final) lèvent un `ValueError` exploitable, pas un découpage silencieusement faux |
| Vérifier qu'une commande existe | Exécuter la commande, ou lire l'aide | `build_parser().parse_args(argv)` | Exécuter `db clear`/`db sync` est interdit (C4, D-22) et l'aide est incomplète (M3) ; `parse_args` est l'API publique prescrite par D-14 |
| Parser le Markdown | Un parseur Markdown, une bibliothèque tierce | Le scanner de blocs de `tests/conftest.py` (Pattern 1) | Aucune bibliothèque Markdown n'est installée (mesuré) et C2 l'interdit ; le format est contraint |
| Normaliser accents/casse/entités | Un `.lower()` local | La fixture `normalize` (`tests/conftest.py:118-135`) | D-11/D-12 : une seconde normalisation divergerait, et le comportement de l'officielle est **déjà testé** (`test_normalisation_insensible_aux_accents_et_casse`) |
| Prouver la complétude des pages et du sommaire | Un nouveau contrôle d'index | Les tests existants de `tests/test_docs_structure.py` | Livrer la page **et** son entrée les active ; les réécrire dupliquerait la logique d'égalité d'ensembles corrigée en WR-04 |
| Lire les défauts d'une option | Déduire le défaut du texte source ou de l'aide | `parse_args` et l'attribut du `Namespace` | Mesuré : `--data-dir` imprime un chemin absolu machine-dépendant, et 11 options n'ont aucun `help` |

**Key insight:** dans ce domaine, le danger n'est pas d'écrire du code trop compliqué, mais d'écrire un contrôle qui **ne peut pas échouer** : un contrôle qui lit sa propre liste, un contrôle qui dérive sa surface de l'aide (incomplète par construction), un contrôle qui laisse passer un `SystemExit` (rapporté comme une erreur d'`argparse`, pas comme une dérive documentaire). Chaque contrôle de cette phase doit être doublé d'une mutation qui le fait rougir — c'est l'objet de la Validation Architecture.

## Common Pitfalls

### Pitfall 1 : croire que `argparse.SUPPRESS` cache une sous-commande de `--help`
**What goes wrong:** la page écrit « `cache` est invisible dans `--help` », ou le test exige l'absence de `stats`/`fill` de `format_help()`. Les deux sont faux : mesuré, la ligne `    cache               ==SUPPRESS==` est **présente** dans l'aide racine, et `    stats` / `    fill` dans celle de `db`.
**Why it happens:** la documentation d'`argparse` décrit `SUPPRESS` comme « l'aide de cette entrée est supprimée » — vrai pour une **option** (mesuré : `--all` disparaît de l'aide *et* de l'usage), faux pour un **sous-parseur** créé par `add_parser(help=SUPPRESS)`, qui conserve son entrée avec le placeholder littéral.
**How to avoid:** formuler « sans description dans l'aide » et n'écrire aucun test sur la présence/absence des entrées `SUPPRESS` — seulement sur ce que la page doit **signaler** (D-20).
**Warning signs:** un test qui appelle `format_help()` pour décider ce que la page doit contenir.

### Pitfall 2 : sonder une sous-commande par son nom nu
**What goes wrong:** `parse_args(["db"])` et `parse_args(["cache"])` sortent en **code 2** (`the following arguments are required: db_command`) : un contrôle qui sonde « une sous-commande = un jeton » déclare `db` et `cache` invalides et échoue sur une page correcte.
**Why it happens:** `db_sub = db_parser.add_subparsers(dest="db_command", required=True)` (`cli.py:184`).
**How to avoid:** sondes d'argv complets (Pattern 2), comme prescrit par `.claude/CLAUDE.md:134-146`.
**Warning signs:** un échec `SystemExit: 2` sur `db` ou `cache` alors que la page les documente.

### Pitfall 3 : comparer les espaces de noms `db` / `cache` sans retirer `command`
**What goes wrong:** `vars(db_ns) == vars(cache_ns)` est **toujours faux** (`command` vaut `'db'` ou `'cache'`) : le test de D-21 échoue sur un parseur correct.
**Why it happens:** chaque `add_parser` écrit le nom choisi dans `dest="command"` ; il n'y a pas d'alias `argparse`, donc rien ne réconcilie la clé.
**How to avoid:** égalité modulo `command` **plus** assertion que `command in {"db","cache"}` (Pattern 5). Mesuré vrai pour les 5 sous-commandes, `clear --all` compris, et avec les 4 options globales.

### Pitfall 4 : reconduire « toutes les commandes portent `--offline` »
**What goes wrong:** la règle de `installation.md` (vérifiée par `test_cli_examples_of_installation_page_parse`, `tests/test_docs_code_anchor.py:184-189`) appliquée à `cli.md` interdit mécaniquement le seul exemple légitime de `db sync` : mesuré, `--offline db sync` sort en **code 1** avec `Erreur : --offline incompatible avec db sync` (`cli.py:345-347`).
**How to avoid:** sur `cli.md`, exiger `--offline` uniquement là où le critère 4 le demande (au moins un exemple `--offline optimize …`, D-27) et documenter l'incompatibilité comme **fait mesuré**, avec sa cause.
**Warning signs:** un exemple `db sync` ou `cache fill` portant `--offline`.

### Pitfall 5 : dériver la liste des options de l'aide du parseur
**What goes wrong:** `--all` est accepté mais invisible dans l'aide **et** dans l'usage ; `--jet`, `--time-limit`, `--stop-when-satisfied` ont leur aide repliée sur la ligne suivante (donc un heuristique de texte conclut à tort « pas d'aide ») ; `--data-dir` imprime un chemin absolu propre à la machine.
**How to avoid:** liste épinglée écrite dans le test + sondes `parse_args` avec valeur d'essai (Pattern 2). L'aide ne sert qu'à des témoins secondaires (par ex. la ligne d'usage `{version,…,cache}`), jamais à la décision.

### Pitfall 6 : recopier les exemples de l'épilog du parseur
**What goes wrong:** `format_help()` du sous-parseur `optimize` imprime `  fetcher.py optimize --offline optimize --demo` — la sous-commande est dupliquée (le `%(prog)s` de l'épilog vaut déjà `fetcher.py optimize`) et cette ligne, passée à `parse_args`, sort en **code 2**. Le texte dépend aussi du `prog` réel (`python -` → `  - optimize --offline optimize --demo`).
**How to avoid:** la page écrit ses propres exemples ; aucun test ne les dérive de `format_help()`.

### Pitfall 7 : sonder les options d'`optimize` sans valeur d'essai
**What goes wrong:** la sonde tri-état héritée de la phase 1 (`[opt]`, `[opt,"1"]`, `[opt,"x"]`) **déclare `--jet` inventée** : mesuré, ses trois essais échouent parce que `--jet` a `choices=("min","average","max")` ; seul `average` passe.
**How to avoid:** table `(option, valeur d'essai|None)` (Pattern 2) ; mesuré 30/30 acceptées.

### Pitfall 8 : écrire un chemin Windows brut dans un exemple
**What goes wrong:** `--data-dir C:\Users\Red\.data` est **muté silencieusement** par `shlex` en `C:UsersRed.data` et `parse_args` l'**accepte** : le contrôle passe, la page enseigne une commande qui ne fait pas ce qu'elle dit.
**How to avoid:** dans un exemple marqué, chemin portable (`.data`, `C:/Users/…`) ou guillemets explicites (`"C:\Users\Red\.data"`, mesuré préservé) ; jamais de `*`, `$`, `~` (non étendus par `shlex`, acceptés par le parseur : le contrôle est aveugle).

### Pitfall 9 : laisser un commentaire ou une continuation dans un exemple marqué
**What goes wrong:** mesuré — `python fetcher.py --offline db status   # etat de la base` devient `[…,'#','etat','de','la','base']` → **code 2** ; une ligne terminée par `\` lève `ValueError: No escaped character`. Les deux cas sont des règles de rédaction, pas des dérives du parseur.
**How to avoid:** les énoncer dans les messages d'échec du test (un commentaire explicatif va **hors** du bloc `console`, en prose ou dans un bloc `text`).

### Pitfall 10 : périmètres d'extraction incohérents (WR-01/WR-03 transposés)
**What goes wrong (trois variantes mesurées ou dérivables) :**
- chercher les options citées dans **toute** la section `optimize` fait remonter `--offline` (globale, refusée par le sous-parseur) → faux échec ;
- chercher le jeton destructeur avec `\bdb\s+clear\b` seulement manque **`cache clear`**, qui vide la base exactement de la même façon ;
- chercher `` `--limit` `` alors que la page écrit `` `--limit=10` `` compare deux formes différentes → faux échec ou faux succès.
**How to avoid:** extraire les options **des lignes de tableau** de la section (`` ^\| ``), normaliser les jetons (`--[a-z][a-z-]*` sans `=valeur`), et couvrir `(?:db|cache)\s+clear` avec `\s+`.

### Pitfall 11 : évaluer une règle par section alors qu'un périmètre échappe (WR-02 transposé)
**What goes wrong:** une règle « la section contenant `db clear` doit porter l'avertissement » laisse passer l'en-tête de page (avant le premier `##`) ; c'est exactement le trou constaté sur `--debug` en phase 1.
**How to avoid:** évaluer les règles destructrice et d'exemple **ligne à ligne sur le texte entier** ; réserver les périmètres par section aux tables d'options, où le périmètre *est* la section.

### Pitfall 12 : un contrôle à sens unique nommé comme bidirectionnel (CR-01)
**What goes wrong:** la phase 1 a livré deux tests dont la docstring annonçait un contrôle « des deux sens » qui n'existait que dans un sens ; une option inventée par la page passait inaperçue.
**How to avoid:** nom et docstring descriptifs de ce qui est réellement testé ; la limite D-26 écrite **dans le module** ; la double direction obtenue par la liste épinglée (présence dans la page) + `parse_args` (validité), pas par une prétention.

### Pitfall 13 : un test de mutation qui code en dur un nom futur (WR-05)
**What goes wrong:** la mutation de la phase 1 injectait `glossaire.md`, page livrée par la phase 6 : le harnais serait devenu rouge sans dérive.
**How to avoid:** ce module n'encode **aucune** mutation ; les dérives sont injectées à la main dans une copie jetable pendant l'exécution (le test de mutation formel est prévu en phase 6). Et aucune assertion ne dépend d'un nom de page que cette phase ne livre pas.

### Pitfall 14 : oublier le lien unique du README (C9 vs D-29)
**What goes wrong:** `.claude/CLAUDE.md:96-106` montre une entrée README à 7 liens directs, dont `docs/cli.md`. L'ajouter violerait D-29 — **et aucun test ne le verrait** (`test_readme_links_to_sommaire` ne compte que les liens vers `sommaire.md`).
**How to avoid:** ne pas toucher `README.md`. Optionnel (hors critère opposable, mais bon marché) : une assertion « le README ne lie aucune page de `docs/` autre que `sommaire.md` » — cf. Open Question 3.

### Pitfall 15 : livrer la page sans son entrée d'index
**What goes wrong:** `problemes_index` (`tests/test_docs_structure.py:92-131`) compare les cibles du sommaire et les pages présentes : une page `docs/cli.md` sans ligne d'index rend la suite **rouge**.
**Preuve mesurée** (copie jetable de `docs/`, page `cli.md` ajoutée, invariants appelés directement) :
- sans entrée d'index → `problemes_index` : `cli.md : page non listee dans docs/sommaire.md ; attendu une ligne d'index pointant vers cli.md (SOMM-02, D-06)` **et** `problemes_h1` : `docs/cli.md : page non listee dans docs/sommaire.md ; attendu une ligne d'index dont le libelle egale le H1 de …` (2 problèmes) ;
- avec l'entrée `| [CLI](cli.md) | … |` **et** le H1 `# CLI` → `problemes_index`, `problemes_h1`, `problemes_retour_sommaire` et `problemes_encodage` renvoient **0 problème** chacun. La configuration visée par la phase est donc satisfiable telle quelle.
**How to avoid:** page + entrée dans la **même** unité de travail (D-28) ; c'est un comportement voulu du harnais, pas un obstacle.

### Pitfall 16 : écrire sous `.data/` ou exécuter une commande par confort
**What goes wrong:** appeler `main()`, ou ouvrir `Database(DEFAULT_DATA_DIR)`, ou exécuter `db sync` pour vérifier un exemple « pour de vrai ». C'est interdit (C4, D-22) et inutile : `parse_args` prouve le critère.
**How to avoid:** `build_parser()`/`parse_args` uniquement ; toute mesure en sous-processus avec un `--data-dir` temporaire ; la distinction « parser `db clear` (prescrit par C6) » / « exécuter `db clear` (interdit) » écrite dans le module.
**Warning signs:** un import de `Database`/`Catalog` dans le nouveau module de test ; un `.sqlite3` créé sous `.data/` pendant la suite (horodatage de `.data/dofus.sqlite3` : `Sep 6 23:27` avant et après cette recherche).

### Pitfall 17 : citer un compteur de tests ou un défaut non re-mesuré
**What goes wrong:** recopier « 158 passed » d'un document vers un rapport alors que la phase a ajouté des tests ; citer la valeur absolue du défaut de `--data-dir` alors qu'elle dépend du poste.
**How to avoid:** re-mesurer avant citation (`./.venv/Scripts/python.exe -m pytest -q` → `158 passed in 1.71s` le 2026-09-11, **avant** les ajouts de cette phase) ; décrire `--data-dir` par « le dossier `.data/` du dépôt ».

## Code Examples

### Conversion d'un échec d'`argparse` ou de `shlex` en assertion localisante (D-13)

```python
# Source : patron de la phase 1 (tests/test_docs_code_anchor.py:107-121, :158-189), appliqué à cli.md
import io, shlex
from contextlib import redirect_stderr

from dofus_stuff.cli import build_parser

SOURCE_CLI = "dofus_stuff/cli.py"

def _argv_de_exemple(page: str, exemple: str) -> list[str]:
    """Tokens d'un exemple, hors `python fetcher.py` ; ValueError shlex converti (D-13)."""
    try:
        argv = shlex.split(exemple)
    except ValueError as exc:
        raise AssertionError(
            f"{page} : exemple « {exemple} » non découpable ({exc}) ; attendu une ligne de "
            f"commande complète, sans guillemet non fermé ni continuation, dans un bloc "
            f"```console (source : {SOURCE_CLI})"
        ) from None
    assert argv[:2] == ["python", "fetcher.py"], (
        f"{page} : exemple « {exemple} » ne commence pas par « python fetcher.py » ; attendu "
        f"le point d'entrée du dépôt (source : fetcher.py)"
    )
    return argv[2:]

def _accepte(argv: list[str]) -> bool:
    """Le parseur public accepte-t-il cet argv ? SystemExit absorbé (D-14)."""
    try:
        with redirect_stderr(io.StringIO()):
            build_parser().parse_args(argv)
    except SystemExit:
        return False
    return True
```

### Contrôle du jeton destructeur sur le texte entier (critère 4b)

```python
# Source : décisions D-22/D-23 + mesures M6 ; texte entier, jamais par section (WR-02)
JETON_DESTRUCTEUR = re.compile(r"\b(?:db|cache)\s+clear\b")
JETON_AVERTISSEMENT = "destruct"   # couvre « destructif », « destructrice », « destruction »

def _lignes_destructrices(texte: str) -> list[tuple[int, str]]:
    return [
        (numero, ligne)
        for numero, ligne in enumerate(texte.splitlines(), 1)
        if JETON_DESTRUCTEUR.search(ligne)
    ]

# 1) présence exigée (sinon la règle 2 serait vide, donc infalsifiable)
# 2) co-présence de l'avertissement sur la MÊME ligne, après normalisation (D-11)
# 3) aucune ligne d'exemple marquée ne porte le jeton (D-22 : jamais une étape)
```

### Preuve d'alias `cache` ≡ `db` (D-21, mesure M1.3)

```python
# Source : mesure — vars() bruts diffèrent toujours (clé `command`), égaux modulo `command`
def _espace_de_noms(argv: list[str]) -> dict:
    ns = build_parser().parse_args(argv)
    return {cle: valeur for cle, valeur in vars(ns).items() if cle != "command"}

for sous_commande in ("status", "stats", "sync", "fill", "clear"):
    gauche, droite = _espace_de_noms(["db", sous_commande]), _espace_de_noms(["cache", sous_commande])
    assert gauche == droite, (
        f"docs/cli.md : l'alias `cache {sous_commande}` n'est pas équivalent à "
        f"`db {sous_commande}` ({gauche} != {droite}) ; attendu deux espaces de noms égaux "
        f"hors clé `command` (source : {SOURCE_CLI}::build_parser())"
    )
```

### Entrée d'index et en-tête de page (contraintes structurelles déjà actives)

```markdown
<!-- docs/sommaire.md : l'ajout de cette ligne active l'égalité d'ensembles (D-06) -->
| [CLI](cli.md) | Commandes, options et exemples de `fetcher.py` |

<!-- docs/cli.md : H1 unique, STRICTEMENT égal (après normalisation) au libellé d'index -->
# CLI
```

Le libellé exact (« CLI », « Ligne de commande », …) relève de la discrétion ; seule contrainte mécanique : `normalize(H1) == normalize(libelle_d_index)` (`problemes_h1`, `tests/test_docs_structure.py:337-381`), la page restant ≥ 300 caractères et sans jeton de brouillon (`problemes_encodage`, `:418-450`).

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Doc CLI écrite puis relue à la main | Page **ancrée** : chaque sous-commande, option et exemple est vérifié par le parseur réel | Décisions du milestone (`workflow.verifier: true`, `nyquist_validation: true`) | Le défaut mesuré du dépôt (`GUIDE_WIZARD.md` périmé depuis `1d475f9` sans qu'aucun test ne réagisse) est traité page par page |
| Surface déduite de `--help` | Sondes `parse_args` + liste épinglée | Mesure M3 de cette recherche (SUPPRESS et `--all` invisibles) | Un contrôle qui « lit l'aide » est structurellement incomplet : la décision est de ne plus s'y fier |
| `str.split()` / regex pour découper une commande | `shlex.split` | Décision du milestone (D-25) et usage phase 1 | Guillemets, apostrophes et `=`-joints corrects ; les cas non découpables deviennent des assertions explicites |
| Test de mutation encodé en dur dans le module | Dérives injectées dans une copie jetable, hors arbre livré | Leçon WR-05 (un nom de page codé en dur est devenu une fausse alerte) | Le test de mutation formel reste planifié en phase 6 (GARD-03), pas dupliqué ici |
| « `SUPPRESS` masque l'entrée » | « l'entrée reste, sans description » | Mesure sur Python 3.14.7 (`argparse.SUPPRESS = '==SUPPRESS=='`) | Change la phrase de la page et interdit tout contrôle fondé sur l'absence |

**Deprecated/outdated :**
- **Dériver une surface du texte de `format_help()`** : incomplet par construction (`--all`), ambigu (`==SUPPRESS==`), machine-dépendant (`--data-dir`).
- **Recopier les exemples de l'épilog du parseur** : le `%(prog)s` de l'épilog d'`optimize` produit une sous-commande dupliquée et une ligne refusée par le parseur.
- **Documenter `db clear --all`** : drapeau accepté mais jamais lu (D-19 : aucune sémantique inventée).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Le marqueur choisi peut être la balise de bloc `` ```console `` sans qu'aucune page existante ne l'utilise (vérifié : `installation.md` n'emploie que `` ```bash `` et `` ```text ``) | Pattern 1 | Faible : changer de balise = changer une constante ; le contrôle reste identique |
| A2 | `db sync` / `cache fill` sont classés « réécriture », pas « destruction » : ils re-téléchargent ce qui est déjà dérivé de l'API et ne touchent aucune donnée propre à l'utilisateur (les stuffs sauvegardés vivent côté navigateur, `dofus_stuff/web/routes.py:1280-1295` (docstring `"""Liste / consultation des stuffs sauvegardés (hydraté côté navigateur)."""`, ligne 1283)) | Pattern 4 / M6 | **Moyen** : D-23 nomme `db sync` et `cache fill` parmi les « destructrices ». Le plan doit **écrire le classement et sa raison mesurée** ; sinon un relecteur peut lire D-23 comme violée. Si le porteur du projet veut un avertissement sur `sync`/`fill`, la forme est celle du critère 4bis : mention + « réécrit la base, nécessite le réseau », jamais dans un parcours hors-ligne |
| A3 | Le jeton d'avertissement est `destruct` (normalisé), qui couvre les variantes françaises | Pattern 4 | Faible : un test qui échoue dit exactement le jeton attendu |
| A4 | Les valeurs absolues de `--data-dir` et le contenu de `.data/` n'apparaissent jamais dans la page | M2, Pitfall 17 | Moyen si la page fige un chemin de poste : le lecteur d'une autre machine suivrait une commande fausse |
| A5 | Aucun test de cette phase n'a besoin d'ouvrir une base ou d'appeler `main()` | M7, C6 | Faible : la contrainte est structurelle (le module n'importe que `build_parser`) |
| A6 | Le compteur de tests de référence est `158 passed` (mesuré le 2026-09-11 **avant** les ajouts de la phase) | Pitfall 17 | Faible, mais toute citation doit être re-mesurée au moment de l'écrire |

**Si ce tableau est vide :** il ne l'est pas — A2 est le point à faire trancher dans le plan (et non par une nouvelle question au porteur du projet, absent).

## Open Questions

1. **Quelle forme exacte pour l'avertissement destructeur, et couvre-t-il `sync`/`fill` ?**
   - What we know: le critère 4 (opposable) n'exige l'avertissement que pour `db clear` ; D-23 nomme aussi `db sync` / `cache fill` comme réécrivant la base ; mesuré : `db clear` détruit `items` **et** `meta` sans confirmation, `db sync` re-télécharge.
   - What's unclear: si un avertissement est exigé sur `sync`, la coexistence avec un parcours « peupler la base » (phase 1 renvoie déjà à `db sync`) devient contradictoire — la phase 5 documentera ce parcours.
   - Recommendation: **avertissement destructeur pour `db clear` uniquement** (règles 1-2-3 du Pattern 4), **mention « réécrit la base, nécessite le réseau, incompatible avec `--offline` »** pour `sync`/`fill`, sans jeton `destruct`, et jamais dans un exemple marqué. Le plan écrit cette classification et sa raison mesurée.
2. **Comment prouver « hors parcours recommandé » ?**
   - What we know: (a) co-présence même ligne et (b) absence des exemples marqués sont mesurables.
   - What's unclear: rien ne distingue mécaniquement une phrase qui encadre `db clear` d'un « conseil ».
   - Recommendation: s'en tenir à (a)+(b), et **écrire cette limite dans le test** (D-26) ; ne pas inventer un contrôle sémantique.
3. **Faut-il ajouter un garde-fou « le README ne lie que `sommaire.md` » ?**
   - What we know: `.claude/CLAUDE.md:96-106` invite exactement à la dérive que D-29 interdit, et aucun test ne la verrait (Pitfall 14).
   - What's unclear: cette assertion ne correspond à aucun des 5 critères de la phase.
   - Recommendation: **optionnel mais recommandé** (une assertion de 5 lignes) ; à marquer « hors critère opposable » dans le plan pour ne pas gonfler le périmètre. Si le porteur du projet préfère le périmètre strict, c'est un non-problème : la phase n'a aucun besoin de modifier `README.md`.
4. **`--force-sync` : que peut-on en dire sans inventer de sémantique ?**
   - What we know: mesuré dans le code : `force=True` force la vérification de version même dans la fenêtre de 24 h (`sync.py:34-45`) ; avec `--offline` et une base non vide, la synchronisation est sautée (`{"action": "skip", "reason": "offline"}`) ; pour `db sync`, `--force-sync` est sans effet (le `force=True` est écrit en dur, `cli.py:348-354`).
   - Recommendation: la page décrit `--force-sync` par son `help` (« Ignorer la fenêtre 24h et forcer une vérif / sync version ») et par sa place (option globale, avant la sous-commande), sans plus — la mécanique 24 h relève de la page « base locale » (phase 5).
5. **Faut-il introduire la convention `` ```console `` dans `installation.md` aussi ?**
   - Recommendation: **non** — hors périmètre, la page d'installation est verte avec sa propre règle (« chaque commande `fetcher.py` d'un bloc de code porte `--offline` »), et la modifier rouvrirait une page livrée sans nécessité. La divergence de marqueur est assumée et documentée dans `tests/conftest.py` (le helper `lignes_de_code` reste disponible pour la page d'installation).

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `.venv/Scripts/python.exe` | Tous les contrôles (C1) | ✓ | `3.14.7` (plancher déclaré `>=3.11`, `pyproject.toml:10`) | — (interpréteur de référence obligatoire) |
| `pytest` dans `.venv` | CLI-01/02/03 | ✓ | `9.1.1` | — |
| Interpréteur ambiant (`python`) | — | ✗ pour `pytest` | mesuré : `C:\Users\Red\Documents\Projets\gsd-core-automated\.venv\Scripts\python.exe: No module named pytest` | Utiliser `.venv/Scripts/python.exe` (obligatoire) |
| `shlex`, `re`, `pathlib`, `argparse` (stdlib) | Découpage, extraction, sondes du parseur | ✓ | inclus dans 3.14.7 | — |
| Bibliothèque Markdown (`markdown`, `markdown_it`, `commonmark`) | — | ✗ (vérifié : les trois `find_spec` sont `None`) | — | Le scanner de blocs maison de la phase 1, étendu (Pattern 1) ; aucune installation autorisée (C2) |
| `git` | Commits locaux | ✓ | `2.55.0.windows.4` | — |
| Base locale `.data/dofus.sqlite3` | **Aucun** besoin de cette phase (lecture/écriture interdites en test) | présente | `24989696` octets, horodatée `Sep 6 23:27` (inchangée après toute la campagne de mesure) | Les contrôles n'en dépendent pas |
| Générateur de doc hors dépôt (`.doc-agent/`, `doc-agent.toml` → `output = "docs"`) | — | état gelé (`state.json` : `stage: "PLAN"`, `2026-09-09`), non suivi par git | — | Risque : s'il repart, il peut réécrire `docs/`. « Ne rien supprimer, ne pas en dépendre » (C11) ; le harnais est le juge (il deviendrait rouge) |
| Recherche externe / réseau | Aucun besoin | ✗ (politique ; `brave_search: false`, providers MCP absents) | — | Toutes les sources de cette recherche sont locales, lues ou exécutées |

**Missing dependencies with no fallback:** aucune — le harnais n'a besoin que du venv, de `pytest` et de la bibliothèque standard.

**Missing dependencies with fallback:** bibliothèque Markdown (fallback : scanner maison étendu, Pattern 1) ; recherche externe (fallback : mesures internes au dépôt).

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest` 9.1.1, exécuté par `.venv/Scripts/python.exe` (Python 3.14.7) |
| Config file | `pyproject.toml` — `[tool.pytest.ini_options]` : `testpaths = ["tests"]`, `pythonpath = ["."]` (lignes 38-39) |
| Quick run command | `./.venv/Scripts/python.exe -m pytest tests/test_docs_cli.py tests/test_docs_structure.py tests/test_docs_code_anchor.py -q` |
| Full suite command | `./.venv/Scripts/python.exe -m pytest -q` (re-mesuré le 2026-09-11, **avant** les ajouts de la phase : `158 passed in 1.71s`) |

### Critères de succès → prédicat machine → mutation qui doit le faire échouer

| Critère | Prédicat machine (test) | Mutation qui **doit** faire passer au rouge | Prédicat falsifiable ? |
|---------|-------------------------|--------------------------------------------|------------------------|
| **1.** Chaque sous-commande documentée est analysée sans erreur | `tests/test_docs_cli.py::test_sous_commandes_documentees_et_acceptees` : pour chacune des 8 entrées de `SONDES_SOUS_COMMANDES` — (a) le nom est présent dans le texte de `docs/cli.md`, (b) `build_parser().parse_args(sonde)` ne lève pas | (a) supprimer la section `cache` de la page → rouge « `docs/cli.md` ne cite pas la sous-commande `cache` » ; (b) écrire `cache2` dans la page → rouge ; (c) dans une copie jetable de `dofus_stuff/cli.py`, renommer `self-test` en `selftest` → rouge (le parseur refuse la sonde de la page) | ✅ oui (3 mutations indépendantes) |
| **2.** Chaque option globale et chaque option d'`optimize` documentée est réellement acceptée | `test_options_globales_documentees_et_acceptees` + `test_options_optimize_documentees_et_acceptees` : liste épinglée (4 globales, 30 options avec valeur d'essai) → présence dans la page **et** `parse_args` OK ; options citées **dans les tables** de la section `optimize` → refusées ⇒ rouge | (a) écrire `--top-kk` dans la table des options d'`optimize` → rouge (« refusée par `dofus_stuff/cli.py` ») ; (b) supprimer la ligne `--allow-power` de la page → rouge (présence) ; (c) **mutation inverse, doit rester verte** : ajouter `--verbose` au parseur sans toucher la page → la suite **reste verte** (limite D-26 assumée) | ✅ oui pour (a) et (b) ; (c) est la limite, écrite dans le module |
| **3.** Chaque exemple apparaît verbatim dans la page et est analysable | `test_exemples_marques_sont_analysables` : chaque ligne des blocs `` ```console `` → présent verbatim dans le fichier (`exemple in texte`, sans normalisation), préfixe `python fetcher.py`, `shlex.split` sans `ValueError`, `parse_args` sans `SystemExit` ; **plus** ≥ 1 exemple par sous-commande documentée | (a) `--limit` → `--limite` dans un exemple → rouge (parseur) ; (b) ajouter `# commentaire` à un exemple → rouge (arguments excédentaires) ; (c) supprimer le seul exemple de `list` → rouge (couverture) ; (d) guillemet non fermé → rouge (`ValueError`) | ✅ oui pour la **parseabilité** et la **couverture** ; ⚠️ l'assertion « verbatim » est **tautologique** (la ligne est extraite de la page) : c'est une *garantie de construction*, pas une exigence de validation — le module doit l'écrire tel quel |
| **4.** Ordre réel illustré + `db clear` averti, jamais dans un parcours | `test_exemple_hors_ligne_avec_option_globale_avant_sous_commande` : ∃ exemple avec `argv[2:4] == ["--offline", "optimize"]` — et `test_commande_destructrice_avertie_et_jamais_dans_un_exemple` : (1) la page cite `(db\|cache) clear`, (2) toute ligne le citant contient `destruct` après normalisation, (3) aucune ligne d'exemple marquée ne le contient | (a) réécrire l'exemple en `optimize --offline --demo` → rouge (présence **et** parseur) ; (b) retirer l'avertissement de la ligne `db clear` → rouge ; (c) déplacer la mention dans un bloc `` ```console `` → rouge ; (d) supprimer la mention → rouge (présence, sinon (2) serait vide) | ✅ oui pour (1)(2)(3) ; ⚠️ « hors parcours **recommandé** » n'est pas décidable en général — (3) l'approxime et le module écrit cette limite |
| **5.** Suite verte, sans `main()`, sans écriture sous `.data/` | Commande épinglée → code 0 ; **plus** une propriété statique du nouveau module : il n'importe que `build_parser` (`Database`, `Catalog`, `main` absents) — assertion sur le texte source du module de test lui-même | (a) toute dérive introduite ci-dessus rend la suite rouge (condition de régression) ; (b) injecter `from dofus_stuff.database import Database; Database(DEFAULT_DATA_DIR)` dans une copie jetable du module de test → l'assertion statique devient rouge ; (c) **mesure accompagnante** : horodatage de `.data/dofus.sqlite3` identique avant/après la suite | ⚠️ partiellement : « la suite est verte » est une **condition d'exécution** (elle ne peut pas être falsifiée par une dérive documentaire, seulement par une régression) ; la partie falsifiable est la propriété statique (b) et l'horodatage (c), consignés dans le SUMMARY de la phase |

**Ce dont le prédicat ne peut pas être rendu falsifiable (à écrire tel quel dans le module, D-26) :** (i) l'assertion « verbatim » de CLI-03 ; (ii) la complétude parser → page (une option ou une sous-commande ajoutée au parseur et non documentée **ne fait pas échouer la suite** — c'est le choix explicite de D-26) ; (iii) la qualité « hors parcours recommandé » ; (iv) le caractère « destructeur » lui-même, qui est un classement humain dérivé du code (A2), pas un prédicat.

### Inventaire de tests proposé — `tests/test_docs_cli.py` (nouveau module)

| Nom (anglais) | Docstring (français) | Critère / exigence |
|---------------|----------------------|--------------------|
| `test_sous_commandes_documentees_et_acceptees` | « Chaque sous-commande documentée est citée par la page et analysée par le parseur réel. » | 1 / CLI-01 |
| `test_options_globales_documentees_et_acceptees` | « Chaque option globale documentée est citée par la page et acceptée avant sa sous-commande. » | 2 / CLI-02 |
| `test_options_optimize_documentees_et_acceptees` | « Les 30 options d'`optimize` sont citées par la page et acceptées ; les options citées dans ses tables existent. » | 2 / CLI-02 |
| `test_exemples_marques_sont_analysables` | « Chaque ligne des blocs `console` se découpe (`shlex`) et passe `build_parser().parse_args`. » | 3 / CLI-03 |
| `test_chaque_sous_commande_a_un_exemple` | « Chaque sous-commande documentée possède au moins un exemple marqué. » | 3 / CLI-03 |
| `test_exemple_hors_ligne_avec_option_globale_avant_sous_commande` | « Au moins un exemple hors-ligne place l'option globale avant `optimize`. » | 4 / D-27 |
| `test_commande_destructrice_avertie_et_jamais_dans_un_exemple` | « `db clear`/`cache clear` est cité avec son avertissement sur la même ligne et jamais comme exemple. » | 4 / D-22 |
| `test_alias_cache_equivalent_a_db_dans_le_parseur` | « `cache <sous-commande>` produit le même espace de noms que `db <sous-commande>` (hors clé `command`). » | D-21 |
| `test_source_de_verite_de_la_page_cli` | « Le bloc « Source de vérité » de `docs/cli.md` cite `build_parser()` et des chemins existants. » | D-30 / D-03 |
| `test_sans_execution_ni_base_locale` | « Ce module n'exécute ni `main()` ni aucune base : il n'importe que le parseur. » | 5 / C6 |

**Helpers : réutilisés vs nouveaux (D-12, question de recherche 7)**

| Élément | Statut | Où |
|---------|--------|-----|
| `docs_dir`, `normalize` (fixtures, `tests/conftest.py:126-135`) | **réutilisés tels quels** | `tests/conftest.py` |
| `_blocs_de_code`, `_lignes_de_code`, `_lignes_exemple`, `BALISE_EXEMPLE` | **nouveaux** (un seul scanner ; `_lignes_de_code` y est **déplacé** depuis `tests/test_docs_code_anchor.py:128-138`, qui le consomme désormais par fixture) | `tests/conftest.py` |
| `_sections`, `_section`, `_option_acceptee`, `OPTION_LONGUE`, `JETON_AIDE` | **déjà présents**, à réutiliser sans les recopier | `tests/test_docs_code_anchor.py:79-126` (import inter-modules à éviter : préférer une fixture dans `conftest.py` si le besoin est partagé) |
| `pages_listees`, `problemes_index`, `problemes_h1`, `problemes_retour_sommaire`, `problemes_encodage`, `_pages`, `_lire_page` | **déjà présents, déjà actifs** : livrer la page + l'entrée d'index suffit | `tests/test_docs_structure.py` (aucun import nécessaire) |
| `SONDES_SOUS_COMMANDES`, `SONDES_GLOBALES`, `SONDES_OPTIMIZE`, `JETON_DESTRUCTEUR`, `JETON_AVERTISSEMENT` | **nouveaux**, spécifiques à la CLI, à garder **dans le module de test CLI** (D-12 : le `conftest` ne reçoit que le partagé) | `tests/test_docs_cli.py` |

### Sampling Rate

- **Per task commit :** `./.venv/Scripts/python.exe -m pytest tests/test_docs_cli.py -q` (+ `tests/test_docs_structure.py` dès que la page ou l'entrée d'index est touchée)
- **Per wave merge :** `./.venv/Scripts/python.exe -m pytest -q`
- **Phase gate :** suite complète verte **et** chacune des mutations des critères 1 à 4 réellement injectée puis constatée rouge (dans une copie jetable, jamais sous `docs/` du dépôt), avec le compteur re-mesuré au moment de la citation.

### Wave 0 Gaps

- [ ] `docs/cli.md` — page complète (D-16, D-18, D-20, D-22, D-30) et ses blocs `` ```console ``
- [ ] `docs/sommaire.md` — ligne d'index `| [CLI](cli.md) | … |` (D-28), dans la **même** unité de travail que la page
- [ ] `tests/conftest.py` — scanner de blocs partagé + fixtures (Pattern 1)
- [ ] `tests/test_docs_code_anchor.py` — un test passe à la fixture (aucun changement de comportement) + preuve de non-régression par mutation
- [ ] `tests/test_docs_cli.py` — les 10 tests ci-dessus
- [ ] Framework : **aucun** (`pytest` 9.1.1 déjà installé et configuré)

## Security Domain

`security_enforcement: true` et `security_block_on: "high"` dans `.planning/config.json` ; `human_verify_mode: "end-of-phase"`.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | non | Aucune authentification dans le périmètre (documentation locale d'un outil mono-utilisateur) |
| V3 Session Management | non | Aucune session |
| V4 Access Control | non | Seul point d'accès pertinent : la base locale, que cette phase ne fait que **nommer** (aucune ouverture) |
| V5 Input Validation | oui | Validation des entrées documentées par le parseur réel (`build_parser().parse_args` avec sondes d'argv explicites) ; découpage `shlex` sans exécution ; extraction bornée par balise de bloc ; normalisation avant comparaison de libellés ; aucun chemin machine absolut dans la page |
| V6 Cryptography | non | Aucune cryptographie ; aucun secret ne doit apparaître dans la page (nommer les variables d'environnement, jamais leur valeur) |

### Known Threat Patterns for {doc CLI ancrée sur un parseur local}

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| La page présente une commande destructrice comme une étape (`db clear`, `cache clear`) | Tampering / Denial of Service | Règles 1-2-3 du Pattern 4 : présence + avertissement même ligne + jamais sur une ligne d'exemple marquée ; `db clear` **parsé**, jamais exécuté (C6) |
| La page incite à une commande réseau depuis un parcours hors-ligne (`db sync`, `cache fill` sans avertissement) | Denial of Service (quota Dofusdude) | M6 : ces commandes sont nommées avec leur effet (« réécrit la base, nécessite le réseau ») et l'incompatibilité mesurée `--offline` × `db sync` est documentée |
| Un exemple documenté exécute autre chose que ce qu'il montre (antislashs avalés par `shlex`, glob non étendu) | Tampering (faux sentiment de sécurité) | M4 : chemins portables ou guillemetés, aucun métacaractère de shell, aucun commentaire en fin de ligne |
| Le harnais écrit sous `.data/` ou ouvre une base | Tampering (perte de la base de développement) | Le nouveau module n'importe que `build_parser` (assertion statique, critère 5) ; aucune fixture de la phase n'ouvre de base ; les mesures en sous-processus ont utilisé un `--data-dir` temporaire |
| Le harnais exécute une commande par confort (`subprocess`, `main()`) | Elevation of Privilege / Tampering | `shlex` + `parse_args` uniquement ; `main()` jamais appelé (C6, D-15) ; l'assertion statique du critère 5 le vérifie |
| La page fige un chemin absolu de poste (`--data-dir` par défaut, chemin utilisateur) | Information Disclosure | M2 : décrire « le dossier `.data/` du dépôt », jamais la valeur absolue ; aucun test ne compare la page à la ligne d'aide de `--data-dir` |

Aucun secret, identifiant ou validation humaine n'est nécessaire : **aucun blocage d'exécution** de nature sécurité.

## Sources

### Primary (HIGH confidence) — dépôt réel, lu ou exécuté (2026-09-11)

Fichiers lus (chemins relatifs à la racine) :

- `dofus_stuff/cli.py` — **lu intégralement** : `:24-31` (épilog d'exemples), `:32-33` (`build_parser()`, description), `:34-50` (options globales `--timeout`/`--data-dir`/`--force-sync`/`--offline`), `:52` (`add_subparsers(dest="command", required=True)`), `:54-55` (`version`, `self-test`), `:57-59` (`search`, `query`, `--limit` défaut `10`), `:61-62` (`item`, `ankama_id`), `:64-66` (`list`, `--page` `1`, `--size` `5`), `:68-73` (`optimize` + `RawDescriptionHelpFormatter` + épilog), `:74-177` (les 30 options d'`optimize`), `:179-195` (boucle `db`/`cache`, `argparse.SUPPRESS` sur `cache`/`stats`/`fill`, `clear --all`), `:283-285` (`_normalize_db_command`, alias `stats`→`status`, `fill`→`sync`), `:330-362` (`main()` : statut, sync + garde `--offline`, clear) — **jamais exécuté**
- `fetcher.py:1-11` — shim `from dofus_stuff.cli import main`
- `dofus_stuff/database.py:117-132` (`replace_kind` : `DELETE FROM items WHERE kind = ?` puis réinsertion), `:146-152` (`clear` : `DELETE FROM items` + `DELETE FROM meta`), `DEFAULT_DATA_DIR` (chemin absolu selon la machine)
- `dofus_stuff/sync.py:16-70` (`ensure_up_to_date` : `force`, garde `if offline:` avec le message « Base locale vide et --offline : impossible de synchroniser », `pull_all`)
- `dofus_stuff/optimize/profile_input.py:405-413` (`needs_interactive_optimize`)
- `dofus_stuff/web/routes.py:1280-1295` (`saves` : stuffs « hydraté côté navigateur », jeton d'écran `PURGE OUI` non utilisé dans cette phase)
- `tests/conftest.py:118-135` (`_normalize`, fixtures `docs_dir` et `normalize`), `tests/test_docs_code_anchor.py:18-31` (constantes), `:79-126` (`_sections`, `_section`, `_option_acceptee`, `_options_aide_web`), `:128-138` (`_lignes_de_code`), `:141-283` (tests existants), `tests/test_docs_structure.py:24-131` (`_pages`, `problemes_liens`, `problemes_index`), `:326-450` (`pages_listees`, `problemes_h1`, `problemes_retour_sommaire`, `problemes_encodage`), `:533-…` (test de mutation)
- `docs/sommaire.md` (index à une entrée + parcours en texte), `docs/installation.md` (gabarit D-01, blocs `` ```bash ``/`` ```text ``, règle `--offline`), `README.md:1-7` (section « Documentation utilisateur », lien unique)
- `pyproject.toml:10` (`requires-python = ">=3.11"`), `:18-21` (extra `dev`), `:22-24` (scripts), `:38-39` (`testpaths`, `pythonpath`)
- `.planning/ROADMAP.md` § Phase 2, `.planning/REQUIREMENTS.md:41-43` et table de traçabilité, `.planning/config.json` (`nyquist_validation: true`, `security_enforcement: true`, `commit_docs: true`, `claude_md_path`), `.claude/CLAUDE.md:1-31`, `:62-67`, `:72-106`, `:109-157`, `:224-232`
- `.planning/phases/01-…/01-REVIEW.md` (9 findings : CR-01, WR-01…WR-05, IN-01…IN-03) et `01-REVIEW-FIX.md` (6 corrigés, 3 Info laissés ouverts)

Commandes exécutées et **résultats observés** (interpréteur épinglé, `sys.argv[0]` fixé à `fetcher.py` pour les sondes in-process) :

- `./.venv/Scripts/python.exe -m pytest -q` → **`158 passed in 1.71s`** (avant tout ajout de la phase) ; `python -m pytest --version` avec l'interpréteur ambiant → `No module named pytest` ; `git --version` → `2.55.0.windows.4`
- Sondes du parseur : surfaces et défauts par `parse_args` (M1, M2), `format_help()`/`format_usage()` par sous-parseur (M3), repro minimale `argparse` hors dépôt (SUPPRESS option vs sous-parser), équivalence `db`/`cache` modulo `command` (6 variantes, y compris `clear --all` et les 4 globales), sonde tri-état sur `--jet` (faux négatif mesuré), table des 30 valeurs d'essai (30/30 acceptées), ligne d'usage `{version,…,cache}` extraite par `re.search(r"\{([^}]*)\}", …)`
- Sous-processus avec `--data-dir` temporaire : `--offline db status` → **0** ; `db status --offline` → **2** + `fetcher.py: error: unrecognized arguments: --offline` ; `--offline db sync` → **1** + `Erreur : --offline incompatible avec db sync` ; `--offline version` → **1** + `Erreur : Base locale vide et --offline : impossible de synchroniser` ; `status` nu → **2** (`invalid choice … cache`)
- `shlex.split` sur 20 lignes candidates (M4) : antislashs Windows avalés (`C:UsersRed.data` accepté par le parseur), chemin guillemeté préservé, `#` → arguments excédentaires (code 2), continuation `\` → `ValueError: No escaped character`, `*`/`$` non étendus
- Reconnaissance : `.data/dofus.sqlite3` horodatée `Sep 6 23:27` **avant et après** la campagne entière (aucune écriture sous `.data/`) ; `git status --porcelain` ne montre aucune modification de `dofus_stuff/`, `docs/`, `tests/`
- Sonde d'index (copie jetable de `docs/`, invariants de la phase 1 appelés par chargement de module) : page `cli.md` **sans** entrée d'index → `problemes_index` renvoie `cli.md : page non listee dans docs/sommaire.md ; attendu une ligne d'index pointant vers cli.md (SOMM-02, D-06)` et `problemes_h1` un second problème ; **avec** `| [CLI](cli.md) | … |` + H1 `# CLI` → **0 problème** pour `problemes_index`, `problemes_h1`, `problemes_retour_sommaire`, `problemes_encodage`. L'arbre livré est resté intact (`docs/cli.md` absent du dépôt)
- `find_spec` : `markdown`, `markdown_it`, `commonmark` → `None` (aucune bibliothèque Markdown installée)

### Secondary (MEDIUM confidence) — cadrage amont local (`[CITED]`)

- `.planning/research/SUMMARY.md`, `STACK.md`, `ARCHITECTURE.md`, `PITFALLS.md`, `FEATURES.md` — structure `docs/` à plat, « le code est la source de vérité, la doc est le reflet, le test est le juge », pièges mesurés (136 tests ne lisant aucune doc, `GUIDE_WIZARD.md` périmé depuis `1d475f9`)
- `.planning/phases/01-…/01-CONTEXT.md` (D-01…D-15) et `01-RESEARCH.md` (patrons d'ancrage, conversion `SystemExit`)

### Tertiary (LOW confidence)

- **Aucune.** Aucune source externe n'a été sollicitée ni citée ; les fournisseurs de recherche sont indisponibles sur cet hôte (`brave_search: false`, aucun outil MCP `context7`/`exa`/`tavily`). Aucun digest, aucun résultat et aucun compteur n'a été inventé pour combler ce manque.

## Metadata

**Confidence breakdown:**

- Standard stack : HIGH — aucune dépendance nouvelle ; `pytest` 9.1.1 et l'interpréteur épinglé déjà présents et mesurés, bibliothèque standard suffisante.
- Architecture : HIGH — le mécanisme d'ancrage est exécuté, pas supposé : la surface du parseur, les défauts, les codes de retour et les résultats `shlex` sont tous mesurés sur l'arbre réel ; le seul choix de conception restant (marqueur de bloc) est un choix assumé de discrétion, avec ses alternatives écartées et la raison de chaque écart.
- Pitfalls : HIGH — chaque piège est adossé soit à une mesure directe (SUPPRESS, sondes nues, `--jet`, antislashs, commentaire, continuation), soit à une leçon documentée de la revue de la phase 1 (CR-01, WR-01…WR-05) ; les deux limites non décidables mécaniquement sont écrites comme telles.
- Ancrage temporel : le compteur de tests (`158`) et les horodatages sont des instantanés datés, à re-mesurer avant toute citation.

**Research date:** 2026-09-11
**Valid until:** 30 jours (domaine stable : le produit est gelé pour cette phase) — à re-mesurer immédiatement si `dofus_stuff/cli.py` change (toute la surface documentée en dépend).
