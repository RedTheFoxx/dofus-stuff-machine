---
phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
plan: 04
subsystem: testing
tags: [pytest, docs-fr, argparse, ancrage-code, hors-ligne, utf8]

# Dependency graph
requires:
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plan 01-01 : tests/conftest.py (fixture docs_dir, _normalize expose par la fixture normalize), docs/installation.md"
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plan 01-02 : docs/installation.md complet (chemin minimal hors-ligne, sept options d'entree web, adresse http://127.0.0.1:5000, six libelles d'ecran, section Source de verite)"
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plan 01-03 : tests/test_docs_structure.py clos (14 tests) et arbre documentaire fige comme etat de reference sain"
provides:
  - "tests/test_docs_code_anchor.py : helpers _section(texte, titre), _lignes_de_code(texte) et _sections(texte) ; constantes SONDES_WEB, OPTIONS_WEB, LIBELLES_SOURCE, TITRE_SOURCE"
  - "ancrage des chemins du bloc « Source de verite » (test_sources_de_verite_exist)"
  - "ancrage des commandes fetcher.py des blocs de code : decoupees par shlex, acceptees par dofus_stuff/cli.py::build_parser() et munies du drapeau hors-ligne (test_cli_examples_of_installation_page_parse)"
  - "adresse par defaut derivee de build_parser().parse_args([]) et aucune autre adresse d'ecoute toleree (test_adresse_par_defaut_documentee)"
  - "sept options d'entree web verifiees dans les deux sens, --debug hors du chemin minimal (test_documented_entry_options_parse / _appear_in_help / _are_documented)"
  - "libelles d'ecran et message hors-ligne ancres sur la ligne du fichier source qui les porte (test_libelles_cites_sont_produits_par_le_code)"
affects: [phase-02, phase-03, phase-04, phase-05, phase-06]

# Mesure #3968 — le registre de plan est sur disque, le compte n'est jamais narre.
plan_head_before: 7978d9c4d22154c3ea27d797c3ca96c93e86e2f8
commits: 2

# Actuals (#2632) — meme barème que l'estimate du plan (chars/4 du diff realise, pas un compteur de harnais).
actuals:
  tokens: 2478
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Ancrage par surface publique : build_parser() / parse_args() / format_help(), jamais d'API privee d'argparse (D-14)"
    - "SystemExit d'argparse converti en AssertionError localisante citant la page, l'option ou la commande fautive et le module source (D-13, D-14)"
    - "Valeur attendue toujours derivee du produit : f\"http://{args.host}:{args.port}\" depuis parse_args([]), jamais les litteraux 127.0.0.1 / 5000 ecrits dans le test"
    - "Decoupage d'une commande documentee par shlex.split puis validation par parse_args : la commande est analysee, jamais executee"
    - "Ancrage d'un libelle sur une ligne porteuse : la meme ligne doit contenir le jeton du code et le litteral entre guillemets doubles, ce qui rend discriminante une simple presence de sous-chaine"

key-files:
  created:
    - tests/test_docs_code_anchor.py
  modified: []

key-decisions:
  - "docs/installation.md n'a finalement pas ete modifie : les trois contrôles de la tache 1 passent sur la page livree par 01-02, aucune divergence page/code n'a ete trouvee. Le chemin figure dans files_modified du plan par precaution, pas parce qu'une correction etait attendue ; le diff du plan ne porte donc que le module de test (232 insertions, 0 suppression)"
  - "La section « Source de verite » est reperee par son titre reel, accents compris, declare dans la constante TITRE_SOURCE : la comparaison reste exacte (aucune normalisation locale, D-12) et un renommage du titre devient un echec nommant la page et le titre attendu"
  - "Le helper _sections(texte) enumere les sections de niveau 2 et sert de base a _section(texte, titre) ; il permet aussi d'exiger que la section qui cite --debug contienne la mention « developpement » sans dupliquer le balayage des titres"
  - "Le perimetre page d'un libelle est la section « ## Pilotage clavier » et non la page entiere : « Retour » n'est satisfait ni par la ligne de retour [Retour au sommaire](sommaire.md), ni par « Retourne l'URL Dofusbook » de dofus_stuff/web/routes.py:1342"
  - "Le message hors-ligne (section_page = None) est cherche dans la page entiere : sa longueur exacte (« Base locale vide et --offline : impossible de synchroniser ») rend la confusion avec du texte etranger impossible, et il n'apparait que dans « ## Erreurs frequentes »"
  - "La commande fetcher.py est jugee sur deux exigences separees et sur deux messages distincts : analyse acceptee par le parseur reel, puis presence du drapeau --offline dans le reste d'argv. L'ordre fautif (option globale apres la sous-commande) ne peut pas passer, argparse sortant par SystemExit ; la page decrit cet ordre fautif en prose, hors bloc de code"
  - "Les chemins ancres sont ceux du bloc « Source de verite » limites aux extensions .py et .toml : le chemin .js (dofus_stuff/web/static/js/terminal.js) y reste decrit par la page sans etre controle, conformement a la decision du plan 01-02 (« l'ancrage du plan 01-04 ne controle que les chemins .py »)"
  - "Le contrôle de --debug est porte au niveau de la section, non du paragraphe : une mention de « developpement » n'importe ou dans la meme section satisfait l'exigence (la page la porte deux fois : « reservee au developpement » et « serveur de developpement »). Le test mord si la section ne qualifie plus du tout le mode debogage — verifie par mutation"
  - "Aucune decision produit nouvelle : le contenu de la page, la surface du parseur et les libelles viennent de 01-02 et du produit fige ; ce plan n'ajoute que l'ancrage"

patterns-established:
  - "Un test d'ancrage n'ecrit rien : la mutation de controle s'injecte dans une copie jetable de docs/, l'arbre livre n'est jamais touche (T-01-07)"
  - "Une valeur documentee n'est jamais recopiee en dur dans un test : elle est recalculee depuis le parseur reel, ce qui fait echouer la suite des que le produit change de defaut"
  - "Une correspondance de libelle est prouvee sur sa ligne porteuse (jeton + litteral entre guillemets), pas par recherche de sous-chaine dans le fichier : c'est ce qui distingue « Retour » de « Retourne l'URL Dofusbook »"

requirements-completed: [GARD-02]

coverage:
  - id: D1
    description: "Chaque chemin .py ou .toml cite par le bloc « Source de verite » de docs/installation.md existe sur disque, resolu depuis la racine du depot (D-03)"
    requirement: "GARD-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_code_anchor.py#test_sources_de_verite_exist"
        status: pass
    human_judgment: false
  - id: D2
    description: "Chaque commande fetcher.py des blocs de code de la page se decoupe (shlex), est acceptee par dofus_stuff/cli.py::build_parser().parse_args et porte le drapeau --offline place avant sa sous-commande : aucune commande documentee ne peut atteindre l'API Dofusdude (T-01-06)"
    requirement: "GARD-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_code_anchor.py#test_cli_examples_of_installation_page_parse"
        status: pass
    human_judgment: false
  - id: D3
    description: "L'adresse citee par la page est derivee des defauts reels du parseur web (http://127.0.0.1:5000) et toute autre adresse hote:port citee par la page fait echouer le test (T-01-02)"
    requirement: "GARD-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_code_anchor.py#test_adresse_par_defaut_documentee"
        status: pass
    human_judgment: false
  - id: D4
    description: "Les huit sondes de la surface d'entree web sont acceptees par parse_args et presentes dans format_help(), et les sept options de la surface publique sont citees par la page ; --debug n'y est cite qu'accompagne de la mention qu'il est reserve au developpement (T-01-03, D-14)"
    requirement: "GARD-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_code_anchor.py#test_documented_entry_options_parse"
        status: pass
      - kind: unit
        ref: "tests/test_docs_code_anchor.py#test_documented_entry_options_appear_in_help"
        status: pass
      - kind: unit
        ref: "tests/test_docs_code_anchor.py#test_documented_entry_options_are_documented"
        status: pass
    human_judgment: false
  - id: D5
    description: "Les six libelles d'ecran cites dans la section « ## Pilotage clavier » et le message d'erreur hors-ligne cite par la page sont encore produits par la ligne du fichier source qui les porte : renommer un libelle dans dofus_stuff/web/routes.py ou le message dans dofus_stuff/sync.py rend la suite rouge (GARD-02)"
    requirement: "GARD-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_code_anchor.py#test_libelles_cites_sont_produits_par_le_code"
        status: pass
    human_judgment: false
  - id: D6
    description: "Lisibilite et valeur localisante des messages d'echec produits par le module (contrepartie de D-13 : un harnais qui echoue sans dire quelle page, quelle option et quel fichier source est un defaut du harnais)"
    verification: []
    human_judgment: true
    rationale: "Aucun test ne juge la clarte d'un message d'echec : les assertions prouvent que le message cite la page, la cible et le fichier source, pas qu'un lecteur non technique comprend l'ecart en le lisant."

# Metrics
duration: 2min
completed: 2026-09-11
status: complete
---

# Phase 1 Plan 04 : ancrage de la page d'installation sur le code reel, du chemin Source de verite aux libelles d'ecran

**`tests/test_docs_code_anchor.py` livre sept tests d'ancrage : les chemins du bloc « Source de verite » existent, les deux commandes `fetcher.py` des blocs de code sont analysees par le parseur reel et hors-ligne, l'adresse `http://127.0.0.1:5000` est recalculee depuis `build_parser().parse_args([])`, les sept options d'entree web sont verifiees dans les deux sens, et les six libelles d'ecran plus le message d'erreur hors-ligne sont ancres sur la ligne du fichier qui les porte — suite complete 157 passed, `docs/` et `.data/dofus.sqlite3` inchanges, aucune introspection privee d'argparse.**

## Performance

- **Duration:** 2 min (10:37:48Z -> 10:39:47Z)
- **Started:** 2026-09-11T10:37:48Z (tete du plan precedent, `7978d9c`)
- **Completed:** 2026-09-11T10:39:47Z
- **Tasks:** 2/2
- **Files modified:** 1 (1 cree, 0 modifie)

## Accomplishments

- **Chemins du bloc « Source de verite » ancres (D-03, critere 4).** `test_sources_de_verite_exist` isole la section par son titre reel (`TITRE_SOURCE = "## Source de verite"`, accents compris), y releve chaque chemin `` `…` `` d'extension `.py` ou `.toml` — `pyproject.toml`, `fetcher.py`, `dofus_stuff/cli.py`, `dofus_stuff/sync.py`, `dofus_stuff/web/__main__.py`, `dofus_stuff/web/routes.py` — et exige `(RACINE_DEPOT / chemin).exists()`, la racine etant derivee de `Path(__file__).resolve().parents[1]` (jamais du repertoire courant). Une section vide en chemins echoue explicitement au lieu de passer a vide.
- **Commandes documentees analysees et hors-ligne (critere 4, T-01-06, Open Question 3).** `test_cli_examples_of_installation_page_parse` extrait des blocs de code Markdown les seules lignes citant `fetcher.py` — `python fetcher.py --offline db status` et `python fetcher.py --offline version` —, les decoupe par `shlex.split`, retire les jetons jusqu'a `fetcher.py` et exige **deux** choses avec **deux** messages : l'acceptation par `dofus_stuff/cli.py::build_parser().parse_args()` (un `SystemExit` devient une `AssertionError` citant la page, la commande et `dofus_stuff/cli.py`), puis la presence de `--offline` dans le reste d'argv. Aucune commande de la page ne peut donc atteindre l'API Dofusdude ; l'exemple d'ordre fautif (`db status --offline`) vit en prose, hors bloc de code.
- **Adresse par defaut derivee, jamais recopiee (INST-02, T-01-02).** `test_adresse_par_defaut_documentee` construit `http://{args.host}:{args.port}` depuis `build_parser().parse_args([])`, exige sa presence dans la page, puis relit toute adresse de forme IPv4:port du texte et refuse toute valeur differente de celle du parseur : une page qui recommanderait `0.0.0.0` ou un autre port echoue, la comparaison portant sur l'adresse reconstruite et non sur un motif approchant.
- **Surface d'entree web verifiee dans les deux sens (D-14, INST-02, T-01-03).** `SONDES_WEB` couvre les huit sondes (`--data-dir`, `--offline`, `--no-offline`, `--online`, `--timeout`, `--host`, `--port`, `--debug`) : `test_documented_entry_options_parse` exige que chacune soit acceptee par `build_parser().parse_args(argv)`, `test_documented_entry_options_appear_in_help` exige que le premier jeton de chacune figure dans `format_help()`, et `test_documented_entry_options_are_documented` exige que les **sept** options de la surface reelle soient citees par la page (comparaison normalisee de D-11, via la fixture `normalize`) et que toute section citant `--debug` le qualifie de reserve au developpement. Aucune introspection privee d'argparse : ni `_subparsers`, ni `_group_actions`, ni `_actions` — verifie par recherche sur le module livre.
- **Libelles d'ecran et message hors-ligne ancres dans les deux sens (GARD-02).** `LIBELLES_SOURCE` porte sept quadruplets `(libelle, fichier source, jeton porteur, section de la page)` : `Quitter`/`F3`, `Retour`/`ESC`, `Precedent`/`f7_label`, `Page prec`/`f7_label`, `Suivant`/`f8_label`, `Page suiv`/`f8_label` dans `dofus_stuff/web/routes.py` (section `## Pilotage clavier`), et le message `Base locale vide et --offline : impossible de synchroniser` sur `RuntimeError` dans `dofus_stuff/sync.py` (page entiere). Chaque entree exige (i) le libelle dans le perimetre declare de la page et (ii) une **ligne** du fichier source ou figurent a la fois le jeton porteur et le libelle entre guillemets doubles — la sous-chaine `Retourne l'URL Dofusbook` de `dofus_stuff/web/routes.py:1342` ne satisfait donc pas `Retour`, qui exige `ESC` et `"Retour"` sur la meme ligne.
- **Le harnais mord, et le prouve sur copies jetables (T-01-07).** Douze derives injectees dans des copies `tempfile.mkdtemp()` de `docs/` (et deux simulations par rebinding des constantes de module, sans toucher au produit) sont toutes refusees et nommees : chemin de source de verite inexistant, titre de section renomme, commande sans `--offline`, commande en ordre fautif, sous-commande inventee, adresse joker citee en plus de la bonne, adresse absente, option web inconnue, option web retiree partout de la page, `--debug` sans aucune mention du developpement, `Retour` retire de la section clavier, libelle exige sur un autre jeton porteur. L'arbre livre n'a jamais ete mute.
- **Non-intrusion mesuree.** Suite complete : **157 passed** (150 existants + 7 nouveaux), 7 passed dans le module, aucune regression ; `.data/dofus.sqlite3` inchange (horodatage `1788730056`, 24 989 696 octets avant et apres) ; `git status --porcelain -- dofus_stuff` vide ; `docs/` inchange (aucune correction de page necessaire).
- **Diff propre.** `git diff --numstat` du plan : `232 0 tests/test_docs_code_anchor.py` — le seul chemin livre est celui du module de test, aucune suppression de ligne suivie, aucune ecriture hors de ce chemin.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : chemins du bloc Source de verite, exemples CLI hors-ligne et adresse par defaut** - `913f479` (test) — 129 lignes
2. **Tache 2 : surface des options d'entree web et libelles ecran ancres dans les deux sens** - `d5f6734` (test) — 103 lignes

**Plan metadata:** commit `docs(01-04): complete ...` (ce SUMMARY.md + STATE.md + ROADMAP.md + REQUIREMENTS.md), cree immediatement apres ce fichier.

_Note : chaque commit nomme son seul chemin (`git show --name-only` ne montre que `tests/test_docs_code_anchor.py`) ; `git diff --diff-filter=D` est vide sur les deux commits. Le registre de plan mesure `git rev-list --count 7978d9c4d22154c3ea27d797c3ca96c93e86e2f8..HEAD` = 2._

## Files Created/Modified

- `tests/test_docs_code_anchor.py` (nouveau, 232 lignes, CRLF) — docstring francaise ; imports publics `from dofus_stuff.cli import build_parser as build_cli_parser` et `from dofus_stuff.web.__main__ import build_parser` ; constantes `RACINE_DEPOT`, `PAGE`, `SOURCE_WEB`, `SOURCE_CLI`, `TITRE_SOURCE`, `CHEMIN_CITE`, `TITRE_H2`, `DELIMITEUR_CODE`, `ADRESSE_ECOUTE`, `SONDES_WEB`, `OPTIONS_WEB`, `JETON_DEBUG`, `MENTION_DEVELOPPEMENT`, `LIBELLES_SOURCE` ; helpers `_sections`, `_section`, `_lignes_de_code` ; sept tests (`test_sources_de_verite_exist`, `test_cli_examples_of_installation_page_parse`, `test_adresse_par_defaut_documentee`, `test_documented_entry_options_parse`, `test_documented_entry_options_appear_in_help`, `test_documented_entry_options_are_documented`, `test_libelles_cites_sont_produits_par_le_code`).
- `docs/installation.md` — **non modifie** : declare dans `files_modified` par precaution (une divergence page/code aurait ete corrigee cote page, le produit etant fige), mais les trois contrôles de la tache 1 passent sur la page livree par 01-02, donc aucune correction n'a ete necessaire.

## Decisions Made

- **Aucune correction de la page.** Les trois tests de la tache 1 passent sur `docs/installation.md` telle que livree par 01-02 : chemins reels, deux commandes `fetcher.py` hors-ligne, adresse `http://127.0.0.1:5000` egale aux defauts du parseur. Le plan n'ajoute aucune section a la page ; il n'avait le droit que de corriger une valeur divergente, et il n'y en avait pas.
- **Section reperee par son titre reel, accents compris.** `TITRE_SOURCE = "## Source de verite"` est compare tel quel (`titre.strip().lstrip("#").strip()`), sans reintroduire de normalisation locale (D-12 : `_normalize` reste l'unique implementation, portee par `tests/conftest.py`). Un renommage du titre de section produit un echec nommant la page et le titre attendu.
- **Helper `_sections(texte)` ajoute sous `_section`.** Enumerer les sections de niveau 2 sert deux besoins du plan : extraire une section nommee (`_section(texte, titre)`, signature du plan conservee) et verifier que la section qui cite `--debug` porte la mention du developpement. Factoriser ce balayage evite de le dupliquer ; `_section` et `_lignes_de_code` gardent la signature declaree par le plan.
- **Perimetre page d'un libelle = la section, pas la page.** « Retour » n'est cherche que dans `## Pilotage clavier`, ce qui rend l'entree discriminante : ni la ligne de retour `[Retour au sommaire](sommaire.md)`, ni la prose ne peuvent la satisfaire.
- **Message hors-ligne cherche dans la page entiere.** La chaine exacte est trop longue pour se confondre avec du texte etranger ; la page ne la porte que dans `## Erreurs frequentes`, donc la portee large ne cree pas de faux positif.
- **Ancrage source = co-occurrence sur une ligne.** Le libelle est exige comme litteral entre guillemets doubles sur une ligne qui porte aussi le jeton du code, ce qui est exactement la forme du produit fige (`("ESC", "Retour")`, `f7_label = "Precedent" if f7_url else "Page prec"`, `raise RuntimeError("Base locale vide et --offline : impossible de synchroniser")`). La simple presence de la sous-chaine, elle, ne prouve rien.
- **Chemins ancres limites a `.py` et `.toml`.** `dofus_stuff/web/static/js/terminal.js` reste decrit par la page sans etre controle, conformement a la decision du plan 01-02 (« l'ancrage du plan 01-04 ne controle que les chemins .py ») ; etendre le controle a `.js` aurait contredit cette decision sans rien prouver de plus.
- **Le `SystemExit` d'argparse ne traverse jamais un test.** Chaque sonde d'argv (web et CLI) le convertit en `AssertionError` citant page, option/commande et module source, au lieu de laisser une trace `argparse.py` sans page ni fichier (Pitfall 3, D-13).
- **`--debug` qualifie au niveau de la section.** L'exigence du plan est portee telle quelle : la section qui cite `--debug` doit contenir la mention `developpement` (normalisee, donc insensible a la casse et aux accents). La tolerance mesuree : la page porte deux fois cette mention dans la meme section (« reservee au developpement », « serveur de developpement »), donc retirer une seule des deux ne fait pas rougir le test ; retirer les deux le fait rougir (verifie par mutation).
- **Aucune decision produit nouvelle.** Contenu de la page, surface du parseur et libelles viennent de 01-02 et du produit fige ; ce plan n'ajoute que le controle.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Helper prive `_sections(texte)` ajoute sous `_section`**
- **Found during:** Tache 1 (helpers du module) puis Tache 2 (contrôle de `--debug`)
- **Issue:** le plan nomme deux helpers (`_section(texte, titre)`, `_lignes_de_code(texte)`), mais deux besoins exigent d'enumerer les sections de niveau 2 : extraire une section nommee et retrouver « la section qui porte `--debug` » (tache 2). Sans factorisation, le balayage des titres aurait ete ecrit deux fois, ou `_section` aurait du retourner une structure que sa signature interdit.
- **Fix:** helper prive `_sections(texte) -> list[tuple[str, str]]` (couples titre/corps, dans l'ordre du fichier), sur lequel `_section` est construit ; `_section(texte, titre)` et `_lignes_de_code(texte)` conservent exactement la signature declaree par le plan.
- **Files modified:** `tests/test_docs_code_anchor.py`
- **Verification:** `pytest tests/test_docs_code_anchor.py -q` -> 7 passed ; mutation « titre de section renomme » -> echec nommant la page et le titre attendu ; mutation « `--debug` sans mention du developpement » -> echec nommant la section fautive
- **Committed in:** `913f479` (Tache 1, helper) et `d5f6734` (Tache 2, second usage)

**2. [Rule 3 - Blocking] Fins de ligne du fichier nouveau passees en CRLF**
- **Found during:** Taches 1 et 2
- **Issue:** l'ecriture d'outil produit des fins de ligne LF alors que le depot est integralement CRLF (`core.autocrlf=true` mesure : `tests/test_docs_structure.py` 574 CRLF / 0 LF, `tests/conftest.py` 135 / 0) — defaut deja rencontre et documente par les plans 01-01 a 01-03.
- **Fix:** normalisation explicite du fichier en bytes (`\r\n` -> `\n` -> `\r\n`) apres chaque ecriture, avant chaque commit.
- **Files modified:** `tests/test_docs_code_anchor.py`
- **Verification:** comptage apres chaque etape : `CRLF 232 / LF-only 0` et 232 lignes ; `git diff --numstat` du plan `232 0` (aucune reecriture integrale, aucune suppression)
- **Committed in:** `913f479` (Tache 1) et `d5f6734` (Tache 2)

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Aucun ecart de perimetre, aucune decision produit. Les deux correctifs portent sur l'hygiene du diff et sur la factorisation interne du module. Le plan declare deux chemins dans `files_modified` ; un seul a ete livre, parce qu'aucune divergence page/code n'a ete trouvee — c'est exactement la condition sous laquelle le plan autorisait `docs/installation.md` a rester intact.

## Issues Encountered

- **En-tete de branche `main` (meme situation que 01-01, 01-02 et 01-03).** L'orchestrateur a dispatche cet executant comme **sequentiel sur l'arbre principal** (`git.branching_strategy: "none"`, historique de la phase integralement sur `main`) ; les deux commits y sont donc poses, conformement a la consigne de dispatch. Aucun `update-ref`, aucun `push`, aucun reset destructeur, aucun `git clean` ni `git stash`.
- **Morsure du harnais verifiee hors depot.** Les douze mesures de morsure ont ete faites sur des copies `tempfile.mkdtemp()` de `docs/` (supprimees apres mesure) et, pour les deux cas qui exigeraient de muter le produit, par rebinding des constantes de module (`LIBELLES_SOURCE`, `SONDES_WEB`) dans un processus jetable : aucun fichier de `dofus_stuff/**` n'a ete touche, `docs/` n'a jamais ete mute.
- **Bruit d'argparse sur les sondes negatives.** Une commande refusee fait imprimer a `argparse` sa ligne `usage:` sur la sortie d'erreur avant le `SystemExit` que le test convertit. C'est le comportement d'argparse lui-meme ; le message d'echec du test reste localisant (page, commande, module source) et c'est lui que pytest affiche.
- **Aucun test ignore, aucune verification non jouee.** Les deux commandes `<automated>` de chaque tache ont ete executees avec l'interpreteur epingle `./.venv/Scripts/python.exe` (jamais `python -m pytest` : l'interpreteur ambiant n'a pas pytest), plus la suite complete apres chaque tache.
- **Fichiers non suivis preexistants laisses intacts** : `.doc-agent/`, `.gsd/`, `doc-agent.toml`, `gsd-auto.toml`, `gsd-auto-rules.toml`, `.planning/milestone.lock`, `.planning/state.json`, ainsi que la modification preexistante de `.gitignore`. Aucun `git add .` : chaque commit nomme son chemin.

## Known Stubs

Aucun. Le module ne porte aucune valeur issue d'un run : les seuls nombres « en dur » sont des valeurs d'argv de sonde (`"5"`, `"5000"`, `"x"`, `127.0.0.1`) qui ne sont jamais comparees a un defaut, l'adresse attendue etant recalculee depuis le parseur. Les libelles ancres sont les chaines du produit fige, et chaque assertion lit un fichier du depot ou interroge le parseur public — aucune donnee fictive, aucun `TODO`, aucune sortie d'interface alimentee par une valeur vide.

## Threat Flags

Aucun. Les surfaces nouvelles sont celles du `<threat_model>` du plan et sont toutes couvertes : adresse d'ecoute (T-01-02, toute adresse autre que celle du parseur fait echouer le test), mode debogage (T-01-03, `--debug` n'est tolere dans la page que qualifie de reserve au developpement), quota Dofusdude (T-01-06, chaque commande des blocs de code doit porter `--offline`), absence d'execution, de base et de reseau (T-01-08, aucun `subprocess`, aucun `main()`, aucune fixture `app`/`catalog`, aucune socket).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Pret pour les phases 2 a 5** : le module accepte leurs completements sans changement de structure — ajouter des entrees a `LIBELLES_SOURCE`, des sondes a `SONDES_WEB`, des chemins au bloc « Source de verite » des pages suivantes et des exemples CLI suffit ; `_section` sert des qu'une page livrera ses propres sections.
- **Pret pour la phase 6** : le test de mutation global (critere de succes 5, deja porte par `tests/test_docs_structure.py`) et la liste epinglee des pages n'exigent aucune modification de ce module ; il est concu pour des pages qui n'existent pas encore.
- **Point d'attention mesure** : l'`estimate` du plan (44 000 tokens) reste tres au-dessus de l'`actual` mesure sur le meme barème (2 478 tokens, soit 9 912 caracteres ecrits). Comme aux plans 01-01 a 01-03, l'ecart suggere un estimate exprime a l'echelle du contexte du plan plutot qu'a celle du diff ; il est enregistre tel quel, sans arrondi, pour calibrer les prochains (ADR-2629).
- **Ce que ce module ne couvre pas, et qui reste assume** : les libelles d'ecran rendus par le client de test Flask appartiennent aux phases 3 a 5 (l'hypothese GARD-02 du plan le dit) ; la phase 1 n'ancre que ce que sa page cite, adosse a une option, a une commande ou a un chemin.
- **Blocage** : aucun.

---
*Phase: 01-socle-documentaire-installation-et-harnais-v-rifiable*
*Completed: 2026-09-11*

## Self-Check: PASSED

- Fichiers livres presents sur disque : `tests/test_docs_code_anchor.py` (232 lignes, 232 CRLF) et ce SUMMARY (232 CRLF) — verifies par `[ -f ]` et comptage.
- Commits presents dans l'historique : `913f479` (tache 1), `d5f6734` (tache 2) — verifies par `git log --oneline --all`.
- Criteres d'acceptation des deux taches rejoues apres commit : helpers `_sections` / `_section` / `_lignes_de_code` au niveau module, `SONDES_WEB` (8 sondes) et `LIBELLES_SOURCE` (7 quadruplets) declares, aucun `parser._` ni autre attribut prive d'argparse, aucun `subprocess`, aucun `main(`, aucune socket, aucune ecriture sous `.data/` — tous PASS.
- Verification de plan rejouee apres commit : `pytest tests/test_docs_code_anchor.py -q` -> 7 passed ; `pytest -q` -> 157 passed (150 existants + 7 nouveaux, aucune regression) ; `git status --porcelain` ne montre pour ce plan que `tests/test_docs_code_anchor.py` (et le present SUMMARY avant commit) — `docs/installation.md` et `dofus_stuff/**` inchanges ; `.data/dofus.sqlite3` inchange (horodatage `1788730056`, 24 989 696 octets avant et apres).
- Morsure verifiee sur douze derives, toutes refusees et nommees, chacune injectee dans une copie jetable de `docs/` ou dans un processus jetable par rebinding de constante : chemin de source de verite inexistant, titre de section renomme, commande sans `--offline`, commande en ordre fautif, sous-commande inventee, adresse joker en plus de la bonne adresse, adresse absente, option web inconnue, option web retiree partout de la page, `--debug` sans aucune mention du developpement, `Retour` retire de la section clavier, libelle exige sur un autre jeton porteur.
- Mesure du registre de plan : `plan_head_before` = `7978d9c4d22154c3ea27d797c3ca96c93e86e2f8`, `git rev-list --count 7978d9c..HEAD` = 2 (le commit de metadonnees de ce SUMMARY est le +1 attendu par verify-work).
