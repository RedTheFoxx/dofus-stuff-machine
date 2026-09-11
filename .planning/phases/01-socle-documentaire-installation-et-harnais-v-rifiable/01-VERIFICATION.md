---
phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
verified: 2026-09-11T10:59:18Z
status: passed
score: 8/8 critères vérifiés (5/5 critères de succès du ROADMAP)
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-01-PLAN.md
  - .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-01-SUMMARY.md
  - .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-02-PLAN.md
  - .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-02-SUMMARY.md
  - .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-03-PLAN.md
  - .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-03-SUMMARY.md
  - .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-04-PLAN.md
  - .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-04-SUMMARY.md
  - README.md
  - docs/installation.md
  - docs/sommaire.md
  - tests/conftest.py
  - tests/test_docs_code_anchor.py
  - tests/test_docs_structure.py
covered_digest: "v1:sha256:60a3026d2ada1a7e5f351d055aa064978273523b4312f39a1a814ae0059dac6c"
behavior_unverified: 0
overrides_applied: 0
---

# Phase 1 : Socle documentaire, installation et harnais vérifiable — Rapport de vérification

**Objectif de phase** (verbatim, `.planning/ROADMAP.md`) : « Un lecteur découvre la documentation depuis le `README.md` racine, installe l'outil et l'utilise en CLI comme en web ; les invariants documentaires et l'ancrage au code sont vérifiés par pytest dès les deux premières pages. »
**Vérifié le :** 2026-09-11T10:59:18Z
**Statut :** `passed`
**Re-vérification :** non — vérification initiale (aucun `*-VERIFICATION.md` antérieur dans le dossier de phase)

## Verdict

Les huit critères dérivés des quatre plans et les cinq critères de succès du ROADMAP sont **atteints et démontrés**, pas seulement affirmés. Les deux claims les plus risqués ont été falsifiés par mes propres mutations sur copies jetables :

1. **Critère 5 (« les deux sens »)** — la revue avait mesuré qu'une option inventée **par la page** laissait la suite verte (CR-01). Le correctif `3f221b3` ajoute `test_options_citees_par_la_page_sont_acceptees_par_le_parseur`. Mutation rejouée par mes soins : `--serve` ajouté au tableau d'options de la page → **1 failed, 157 passed**, message nommant l'option et la source (`dofus_stuff/web/__main__.py`). Le sens inverse (option du parseur absente de la page) est refusé de la même manière.
2. **Critère 7 (« le harnais mord »)** — le test de mutation n'est pas vacillant : en aveuglant `problemes_index` dans une copie jetable (`return []`), le test de mutation **échoue lui-même** en nommant la page injectée. Un harnais cassé ne peut donc pas produire un faux vert.

Aucun critère n'est `FAIL` ou `PARTIAL`. Aucun marqueur de dette, aucun blocage, aucune vérification humaine indispensable (voir « Vérification humaine requise »).

**Méthode (contraintes respectées) :** interpréteur épinglé `.venv/Scripts/python.exe` uniquement ; `main()` jamais exécuté ; aucune écriture sous `.data/` ; aucune connexion réseau ; aucune écriture dans le dépôt (toutes les mutations ont été appliquées à des copies jetables sous le répertoire temporaire système, supprimées après mesure).

## 1. Reproductibilité de la suite (interpréteur épinglé)

```bash
cd C:/Users/Red/Documents/Projets/dofus-stuff-machine
.venv/Scripts/python.exe -m pytest -q
```

```
........................................................................ [ 45%]
........................................................................ [ 91%]
..............                                                           [100%]
158 passed in 1.62s
```

- **158 passed**, durée réelle 1,62 s, **aucun warning** (rejoué aussi en `-W error::DeprecationWarning` → `158 passed in 1.65s`, le `filterwarnings` de `pyproject.toml` couvrant le seul warning connu d'ortools).
- Composition : `tests/test_docs_structure.py` = **14 tests**, `tests/test_docs_code_anchor.py` = **8 tests**, soit **22 nouveaux**.
- **Absence de régression mesurée sur l'état antérieur :** l'arbre d'avant phase (`git archive f6bd550 | tar -x`, copie jetable) donne `136 passed in 1.79s`. `136 + 22 = 158` : aucun test antérieur perdu, aucun test ignoré.

## 2. Grille des critères

| # | Critère | Verdict | Preuve (commande / observation) |
|---|---------|---------|---------------------------------|
| 1 | `README.md` → `docs/sommaire.md` ; sommaire index unique, cibles = pages de `docs/`, aucun autre lien, libellés normalisés uniques | ✓ PASS | `README.md:7` porte une section « Documentation utilisateur » avec l'unique lien `[Sommaire de la documentation](docs/sommaire.md)` ; lecture octet : `docs/sommaire.md` n'a qu'un lien, `['installation.md']`, et `docs/` ne contient que `installation.md` + `sommaire.md` → égalité d'ensembles. Mutations : T8 (libellé dupliqué) → `1 failed` « libelle d'index « installation » deja porte par « Installation » » ; T9 (entrée retirée) → `4 failed` « page non listee dans docs/sommaire.md » ; T10 (0 lien README) → `1 failed` « 0 lien(s) vers docs/sommaire.md » ; T11 (2 liens) → `1 failed` « 2 lien(s) » ; T7 (lien externe ajouté au sommaire) → `2 failed`. |
| 2 | Chaque page : un seul H1 = libellé d'index, ligne de retour, UTF-8 strict sans marqueur de brouillon | ✓ PASS | Mesure octet : `docs/installation.md` `bom=False h1=['Installation'] crlf=141 lf_only=0 liens=['sommaire.md']` ; `docs/sommaire.md` `bom=False h1=['Sommaire de la documentation'] crlf=19 lf_only=0`. Mutations : T3 (H1 `Installation provisoire`) → `2 failed` nommant le H1 et le libellé attendu ; T12 (ligne de retour supprimée) → `1 failed` « aucune ligne de retour vers docs/sommaire.md » ; T15 (BOM UTF-8) → `2 failed` ; T13/T14 (cible `sommaire .md` / `sommaire.md "titre"`) → `1 failed` « aucune ligne de retour » (forme de lien invalide détectée, pas de faux vert). |
| 3 | `docs/installation.md` documente prérequis 3.11+, la commande d'installation unique, l'invocation pytest épinglée, le premier contact hors-ligne, le pilotage clavier **avant** le lancement web, les défauts mode/adresse, et un dépannage issu de `dofus_stuff/sync.py` | ✓ PASS | Lecture de la page : sections dans l'ordre `Prérequis` (`requires-python = ">=3.11"`), `Installation` (`pip install -e ".[dev]"`, aucune mention de `uv` — `grep -in '\buv\b'` vide, `pyproject.toml` déclare `setuptools>=68` + extra `dev: pytest>=8.0`), `Vérification` (`.venv/Scripts/python.exe -m pytest -q`), `Premier lancement` (`python fetcher.py --offline db status`), `Pilotage clavier`, `Lancement de l'interface web` (`http://127.0.0.1:5000`, hors-ligne par défaut), `Erreurs fréquentes`, `Source de vérité`. Message de dépannage ancré sur `dofus_stuff/sync.py:43` (`raise RuntimeError("Base locale vide et --offline : impossible de synchroniser")` sous `if offline:`), préfixe `Erreur : ` et code 1 vérifiés dans `dofus_stuff/cli.py:430-433` (`except Exception … print(f"Erreur : {exc}") … return 1`). Mutation T6 (section clavier déplacée après le lancement web) → `1 failed` nommant les deux positions. |
| 4 | Chaque commande exécutable montrée fonctionne contre le code figé (exemples CLI ré-analysés par le vrai parseur ; `--offline` avant la sous-commande) | ✓ PASS | Sonde directe du parseur public : `python fetcher.py --offline db status` → accepté `('db', True)` ; `python fetcher.py --offline version` → accepté `('version', True)` ; forme fautive `db status --offline` → `SystemExit 2` + `error: unrecognized arguments: --offline` (exactement ce que la page cite). Comportement du chemin `db status` prouvé sans exécuter `main()` : `Database(data_dir=<tmp>).open()` puis `cli._print_db_status(db)` → crée `dofus.sqlite3` dans un répertoire inexistant et imprime `Fichier : …` / `Version jeu : (aucune)` / `Dernier check : (aucun)` / `Entrées : 0`, soit les quatre caractéristiques promises par la page. `.venv/Scripts/python.exe -m pytest -q` → `158 passed`. Limites assumées : § 8. |
| 5 | Surface des options web ancrée **dans les deux sens** | ✓ PASS | Sonde : surface `format_help()` = `['--data-dir','--debug','--host','--no-offline','--offline','--online','--port','--timeout']`, égale à la surface citée par la section « Lancement de l'interface web ». Mutations : **T1 (option inventée `--serve` dans la page) → `1 failed, 157 passed`** avec `option(s) citee(s) par la section « ## Lancement de l'interface web » mais refusee(s) par le parseur : --serve` ; **T2 (option `--timeout` retirée de la page) → `1 failed, 157 passed`** nommant les deux surfaces comparées. Les deux sens sont donc démontrés, pas affirmés. |
| 6 | Les libellés d'écran cités sont produits par `dofus_stuff/web/routes.py` | ✓ PASS | Lignes porteuses vérifiées : `routes.py:67 ("F3","Quitter")`, `:68 ("ESC","Retour")`, `:138 f7_label = "Precedent" if f7_url else "Page prec"`, `:139 f8_label = "Suivant" … "Page suiv"`, `:208 fkeys=[("F3","Quitter")]` (page : le menu principal n'affiche que F3). Mutation **T5 (code relabellisé `("ESC","Retourner")`) → `1 failed, 157 passed`** avec « libellé « Retour » cité par la page n'est plus produit par dofus_stuff/web/routes.py ». Touches citées (`F3`/`Escape`/`F7`/`F8`/`PageUp`/`PageDown`/`Enter`) confirmées dans `dofus_stuff/web/static/js/terminal.js:551,557,563,569,575,585,595`. |
| 7 | Harnais falsifiable : test de mutation sur copie `tmp_path` de `docs/`, l'invariant échoue **en nommant** la dérive | ✓ PASS | `tests/test_docs_structure.py::test_mutation_detecte_les_trois_derives` copie `docs/` sous `tmp_path` (`shutil.copytree`), vérifie l'état sain puis injecte 3 dérives et exige que chacune soit **nommée**. Preuve de non-vacuité (ma mutation) : **T4** — `problemes_index` rendu aveugle (`return []`) → le test de mutation lui-même **échoue** : « copie de docs/ : la page page-injectee-mutation.md non listee dans sommaire.md n'est pas detectee par problemes_index() ». Les 3 classes de dérive sont refusées sur l'arbre livré : lien mort (T12/T13), page non listée (T9), H1 divergent (T3). L'arbre livré n'est jamais muté (assertions finales du test + `git status --porcelain -- docs` vide après exécution). |
| 8 | Pas de régression ; `.data/dofus.sqlite3` intacte ; aucun fichier `dofus_stuff/**` modifié ; aucune dépendance nouvelle | ✓ PASS | `136 passed` avant phase (`f6bd550`) vs `158 passed` livré ; `.data/dofus.sqlite3` = `24989696 1788730056` (2026-09-06 23:27:36, antérieur à la phase) identique avant et après mes exécutions ; `git status --porcelain -- dofus_stuff` vide ; `git diff --numstat 0bef7bc^..HEAD` ne touche que `README.md` (4+/0-), `docs/installation.md` (141+/0-), `docs/sommaire.md` (19+/0-), `tests/conftest.py` (25+/0-), `tests/test_docs_code_anchor.py` (298+/0-), `tests/test_docs_structure.py` (603+/0-) et `.planning/**` ; **aucune suppression de ligne** dans les fichiers livrés ; `pyproject.toml` intact (dernière modification `166f854`, 2026-07-25) ; `find docs -type d` → `docs` seulement. |

**Score :** 8/8 critères vérifiés — `behavior_unverified: 0`.

## 3. Couverture des critères de succès du ROADMAP

| SC | Énoncé (ROADMAP phase 1) | Verdict | Critères ci-dessus |
|----|--------------------------|---------|--------------------|
| 1 | `README.md` porte une section « Documentation utilisateur » dont la cible `docs/sommaire.md` existe (lien résolu par un test) | ✓ PASS | C1 (`test_readme_links_to_sommaire`, T10/T11) |
| 2 | `docs/sommaire.md` liste exactement les pages présentes, chaque page a un unique H1 = libellé d'index + ligne de retour (contrôle bidirectionnel) | ✓ PASS | C1, C2 (T3/T8/T9/T12) |
| 3 | `docs/installation.md` mène de Python 3.11+ au premier lancement CLI **et** web et décrit le pilotage clavier **avant** le lancement | ✓ PASS | C3 (T6) |
| 4 | Chaque option d'entrée web citée est acceptée par le parseur réel, et chaque chemin `.py` d'un bloc « Source de vérité » existe | ✓ PASS | C4, C5, C6 (T1, T2, T5) |
| 5 | Une dérive injectée dans une copie de `docs/` fait échouer la suite, verte sur l'état livré, sans `main()`, sans `.data/`, sans réseau | ✓ PASS | C7, C8 (T4 + batterie T1–T17) |

## 4. Batterie de mutations (copies jetables uniquement)

Toutes les mutations ont été appliquées à des copies complètes de l'arbre sous le répertoire temporaire système ; `docs/` du dépôt n'a jamais été touché. Chaque ligne est une exécution réelle de la suite complète (sauf T4, T8 : test ciblé).

| # | Dérive injectée | Résultat | Message d'échec (extrait) |
|---|-----------------|----------|---------------------------|
| T1 | page : option `--serve` inventée | 1 failed, 157 passed | « option(s) citee(s) par la section … mais refusee(s) par le parseur : --serve ; attendu chaque option citee acceptee par dofus_stuff/web/__main__.py::build_parser().parse_args() » |
| T2 | page : option `--timeout` retirée | 1 failed, 157 passed | « surface citee … = ['--data-dir','--debug','--host','--no-offline','--offline','--online','--port'] ; attendu la surface de …format_help() = [… '--timeout'] » |
| T3 | H1 → « Installation provisoire » | 2 failed, 156 passed | « H1 « Installation provisoire » different du libelle d'index « Installation » » |
| T4 | harnais aveuglé (`problemes_index` → `[]`) | 1 failed | « la page page-injectee-mutation.md non listee dans sommaire.md n'est pas detectee par problemes_index() » (test ciblé) |
| T5 | code : `("ESC","Retour")` → `("ESC","Retourner")` | 1 failed, 157 passed | « libellé « Retour » … n'est plus produit par dofus_stuff/web/routes.py ; attendu « ESC » et le littéral "Retour" sur une même ligne » |
| T6 | section clavier déplacée après le lancement web | 1 failed, 157 passed | « ordre fautif … doit preceder la commande « python -m dofus_stuff.web » » |
| T7 | sommaire : lien externe ajouté | 2 failed, 156 passed | « cible listee absente sur disque : https://dofusdu.de/ » |
| T8 | sommaire : libellé dupliqué (`installation`) | 1 failed | « libelle d'index « installation » deja porte par « Installation » » (test ciblé) |
| T9 | sommaire : entrée d'index retirée | 4 failed, 154 passed | « installation.md : page non listee dans docs/sommaire.md » |
| T10 | README : lien vers le sommaire supprimé | 1 failed, 157 passed | « README.md : 0 lien(s) vers docs/sommaire.md » |
| T11 | README : second lien vers le sommaire | 1 failed, 157 passed | « README.md : 2 lien(s) vers docs/sommaire.md » |
| T12 | page : ligne de retour supprimée | 2 failed, 156 passed | « aucune ligne de retour vers docs/sommaire.md » |
| T13 | lien de retour `(sommaire .md)` | 2 failed, 156 passed | « aucune ligne de retour vers docs/sommaire.md » |
| T14 | lien de retour `(sommaire.md "titre")` | 2 failed, 156 passed | « aucune ligne de retour vers docs/sommaire.md » |
| T15 | page : BOM UTF-8 ajouté | 2 failed, 156 passed | « 0 titre(s) H1 dans …installation.md » (voir § 7, IN-02) |
| T16 | `docs/installation.md` supprimée | 12 failed, 146 passed | 6 messages nommés (`test_docs_structure`) + 6 `FileNotFoundError` (`test_docs_code_anchor`, voir § 7, IN-03) |
| T17 | sommaire : `installation.md#prerequis` | 6 failed, 152 passed | « ancre interdite : installation.md#prerequis » (règle nommée) + messages secondaires (voir § 7) |

**17/17 dérives refusées.** Aucune mutation n'a produit de faux vert silencieux.

## 5. Ancrage au produit vérifié indépendamment (hors tests)

| Claim de la page | Vérification indépendante | Verdict |
|---|---|---|
| Adresse par défaut `http://127.0.0.1:5000` | `build_parser().parse_args([])` → `host=127.0.0.1, port=5000, offline=True` | ✓ |
| Hors-ligne par défaut, `--online` ≡ `--no-offline` | `argparse` : les trois options acceptées ; `grep offline = False if args.online else args.offline` | ✓ |
| « l'interface démarre quand même sans base peuplée » | `Database.open()` fait `mkdir(parents=True, exist_ok=True)` + `sqlite3.connect` (base créée sur répertoire absent, mesuré) | ✓ |
| Message d'erreur hors-ligne, code 1, préfixe `Erreur : ` | `sync.py:43` (garde `if offline:`) + `cli.py:430-433` | ✓ |
| Touches clavier réellement actives | `terminal.js:551/557/563/569/575/585/595` (`F3`, `Escape`, `F7`, `F8`, `PageUp`, `PageDown`, `Enter`) | ✓ |
| Barre de raccourcis dynamique, F3 seul sur le menu principal | `routes.py:208 fkeys=[("F3","Quitter")]`, `:138-141` | ✓ |
| « aucun autre gestionnaire de paquets » | `grep -in '\buv\b' docs/*.md` vide ; `pyproject.toml` = `setuptools>=68` + extra `dev` | ✓ |

## 6. Non-intrusion (mesures avant/après)

| Contrôle | Commande | Résultat |
|---|---|---|
| `.data/dofus.sqlite3` intacte | `stat -c '%s %Y' .data/dofus.sqlite3` | `24989696 1788730056` — identique à l'empreinte d'avant phase (2026-09-06 23:27:36), aucune écriture |
| `dofus_stuff/**` intact | `git status --porcelain -- dofus_stuff` | vide |
| Fichiers livrés non modifiés depuis leurs commits | `git status --porcelain -- docs README.md tests` | vide |
| Aucune dépendance nouvelle | `git log -1 --format='%h %ad %s' -- pyproject.toml` | `166f854 2026-07-25 …` (antérieur à la phase) |
| Périmètre du diff de phase | `git diff --numstat 0bef7bc^..HEAD` | README.md, docs/**, tests/** + `.planning/**` uniquement ; 0 suppression dans les fichiers livrés |
| Aucun sous-dossier sous `docs/` | `find docs -type d` | `docs` seulement |
| Aucune écriture pendant la vérification | `git status --porcelain` (avant/après) | inchangé : ` M .gitignore` (ligne `.gsd-auto/`, datée 2026-09-10 23:07, antérieure à l'exécution — hors périmètre) + non suivis préexistants du harnais |

## 7. Observations résiduelles (aucune ne rend un critère faux)

Reproduites par mes soins sur copies jetables. Dans **tous** les cas la suite est rouge et au moins un message nomme la dérive : ce sont des défauts de **diagnostic**, pas de détection.

| Réf. | Observation mesurée | Nature |
|---|---|---|
| IN-01 | Lien externe ajouté au sommaire (T7) → « cible listee absente sur disque : https://dofusdu.de/ » : la page est refusée (strict), mais le message désigne une absence qui n'existe pas. | Message imprécis |
| IN-02 | Page avec BOM UTF-8 (T15) → « 0 titre(s) H1 » alors que la cause est le BOM (`_lire_page` lit en `utf-8`, pas `utf-8-sig`). | Message imprécis |
| IN-03 | `docs/installation.md` supprimée (T16) → les 6 tests de `test_docs_code_anchor.py` lèvent un `FileNotFoundError` brut (chemin nommé, mais sans la valeur attendue ni le fichier source, contrairement à D-13), alors que `test_docs_structure.py` produit 6 messages nommés. | Robustesse du message |
| Résidu WR-03 | Cible `installation.md#prerequis` (T17) → la règle « ancre interdite » est bien nommée (correctif appliqué), mais `problemes_index` ajoute « cible listee absente sur disque : installation.md#prerequis » et une page « non listee » : deux messages secondaires faux. | Messages secondaires |
| Couplage du test de mutation | La dérive (a) du test de mutation cherche le littéral `(sommaire.md)` dans `installation.md` : si une phase ultérieure changeait la forme de la ligne de retour (latitude pourtant ouverte par `01-CONTEXT.md`, section « Claude's Discretion »), le test échouerait en annonçant une dérive « non détectée » alors que la cause serait le couplage (reproduit en T13/T14). | Fragilité du harnais (état futur hypothétique) |

## 8. Limites assumées de la vérification (hors critères)

Ces points ne sont **pas** des critères de la phase et aucun critère n'en dépend ; ils sont déclarés pour ne pas laisser croire à une exécution qui n'a pas eu lieu :

1. **`pip install -e ".[dev]"` et `python -m venv .venv` n'ont pas été exécutés** (mutation de l'environnement + accès réseau interdits par les règles de la phase). Contrôle substitué prouvant le même critère : `pyproject.toml` déclare `setuptools>=68` + `requires-python = ">=3.11"` + extra `dev: pytest>=8.0`, la page cite cette commande unique, et l'invocation épinglée qu'elle prescrit tourne réellement (`158 passed`).
2. **`python -m dofus_stuff.web` n'a pas été lancé** (démarrage de serveur + exécution de `main()` interdits). Contrôle substitué : défauts dérivés du parseur réel (`127.0.0.1:5000`, hors-ligne), surface d'options égale dans les deux sens, point d'entrée `dofus_stuff/web/__main__.py` présent et importable.
3. **`python fetcher.py --offline db status` n'a pas été exécuté via `main()`.** Contrôle substitué par le chemin réellement emprunté par la commande : `Database(...).open()` + `_print_db_status()` sur un `data_dir` temporaire → base créée, quatre caractéristiques imprimées, aucune écriture sous `.data/`, aucun réseau.

## 9. Couverture des exigences

| Exigence | Plan source | Description | Statut | Preuve |
|---|---|---|---|---|
| SOMM-01 | 01-01 | Sommaire trouvable depuis `README.md` | ✓ SATISFIED | `test_readme_links_to_sommaire` (T10/T11) |
| SOMM-02 | 01-01 | Chaque page listée, et réciproquement | ✓ SATISFIED | `problemes_index`, `test_sommaire_lists_every_document`, `test_sommaire_links_resolve` (T7/T9) |
| SOMM-03 | 01-03 | H1 unique = libellé d'index + ligne de retour | ✓ SATISFIED | `problemes_h1`, `problemes_retour_sommaire` (T3/T12) |
| INST-01 | 01-02 | Installation (3.11+, `pip install -e ".[dev]"`) puis vérification | ✓ SATISFIED | Page + `pyproject.toml` + `158 passed` (§ 8, limite 1) |
| INST-02 | 01-02 | Démarrer le web, connaître mode et adresse | ✓ SATISFIED | `test_adresse_par_defaut_documentee`, surface d'options bidirectionnelle (T1/T2) |
| INST-03 | 01-02 | Pilotage clavier décrit avant le lancement | ✓ SATISFIED | `test_pilotage_clavier_avant_lancement` (T6) + ancrage touches/labels (T5) |
| GARD-01 | 01-03 | La suite échoue sur lien mort, sommaire divergent, H1 divergent | ✓ SATISFIED | Batterie T3/T9/T12/T13/T15 + test de mutation (T4) |
| GARD-02 | 01-04 | La suite échoue si un libellé cité n'est plus produit par le code | ✓ SATISFIED | `test_libelles_cites_sont_produits_par_le_code` (T5), chemins « Source de vérité » et exemples CLI (T1/T2) |

**Exigences orphelines :** aucune. `REQUIREMENTS.md` mappe exactement SOMM-01…03, INST-01…03, GARD-01…02 à la phase 1, et les quatre plans les déclarent tous (`01-01: SOMM-01, SOMM-02` · `01-02: INST-01, INST-02, INST-03` · `01-03: SOMM-03, GARD-01` · `01-04: GARD-02`).

## 10. Anti-patterns et marqueurs de dette

| Fichier | Ligne | Motif | Gravité | Impact |
|---|---|---|---|---|
| — | — | Aucun `TBD`/`FIXME`/`XXX`/`HACK`/`PLACEHOLDER` dans les fichiers modifiés par la phase (recherche insensible à la casse) | — | Aucun |
| `tests/test_docs_structure.py` | 312 | `JETONS_BROUILLON = ("todo", "a completer", "lorem")` | ℹ️ Info | Faux positif de la recherche : c'est le vocabulaire du contrôle de brouillon, pas une dette. |

Aucun `test.skip`, aucun test `xfail`, aucun `pass` de complaisance dans les deux modules ajoutés. Aucun blocage anti-pattern.

## 11. Éléments reportés (hors périmètre phase 1, par contrat)

Non des écarts : `docs/cli.md` et ses contrôles (phase 2), `parcours-simplifie.md` (phase 3), `wizard-avance.md` + résorption de `GUIDE_WIZARD.md` et contrôle des renvois obsolètes (phase 4), `base-locale.md` (phase 5), liste épinglée des 8 pages, test de mutation global et audit final (phase 6). Le sommaire de la phase 1 ne liste donc qu'`installation.md`, conformément à D-05.

## Gaps

**Aucun écart.** Aucun critère `FAIL` ni `PARTIAL`, aucun artefact `MISSING`/`STUB`, aucun lien `NOT_WIRED`, aucun blocage. Les huit critères dérivés et les cinq critères de succès du ROADMAP sont atteints, chacun avec la commande ou l'observation qui le démontre (sections 2 et 3). Les observations de la section 7 n'affaiblissent aucun critère : dans chacune, la suite est rouge et nomme la dérive — c'est le diagnostic qui est perfectible.

## Vérification humaine requise

**Aucune.** Les critères de la phase sont tous décidables par contrôle automatique, et chaque critère est couvert par un contrôle exécuté (suite épinglée, sondes de parseur, sondes de fichiers, 17 mutations). Les seuls points non exécutés (installation dans un environnement neuf, démarrage du serveur) sont documentés en § 8 comme limites de vérification **hors critères**, chacune remplacée par un contrôle automatique qui prouve le même critère — conformément à la règle du projet qui demande de substituer un contrôle automatique à une validation manuelle. Aucune validation humaine n'est donc invoquée ni inventée.

---

_Fichiers couverts (15) et empreinte : `v1:sha256:60a3026d2ada1a7e5f351d055aa064978273523b4312f39a1a814ae0059dac6c`, calculés par `gsd_run query verification.fingerprint`._
_Vérifié le : 2026-09-11T10:59:18Z_
_Vérificateur : gsd-verifier (hôte automatisé) — non commité, laissé à l'orchestrateur._
