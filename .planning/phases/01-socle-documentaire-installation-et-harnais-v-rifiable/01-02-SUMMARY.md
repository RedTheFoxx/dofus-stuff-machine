---
phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
plan: 02
subsystem: documentation
tags: [markdown, pytest, docs-fr, installation, clavier, hors-ligne]

# Dependency graph
requires:
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plan 01-01 : docs/installation.md au gabarit D-01, tests/conftest.py (fixture docs_dir, _normalize), tests/test_docs_structure.py (helpers _pages / problemes_liens / problemes_index, motifs LINK / H1)"
provides:
  - "docs/installation.md complet : Prerequis, Installation, Verification, Premier lancement, Pilotage clavier, Lancement de l'interface web, Erreurs frequentes, Source de verite (141 lignes, 8 sections)"
  - "tests/test_docs_structure.py : test_pilotage_clavier_avant_lancement et test_no_destructive_command_in_installation, helpers prives _page et _section"
  - "premier contact CLI enseigne et integralement hors-ligne : python fetcher.py --offline db status"
  - "surface d'entree complete du parseur web sur la page (sept options), adresse derivee des defauts reels (http://127.0.0.1:5000)"
affects: [01-03, 01-04, phase-02, phase-04, phase-06]

# Actuals (#2632) — mesure sur le meme barème que l'estimate du plan (chars/4 du diff realise, pas un compteur de harnais).
actuals:
  tokens: 2695
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Section markdown isolee par extraction texte : _section(texte, titre) coupe du titre jusqu'au prochain H2 (motif H2 en MULTILINE) — controle d'ordre base sur la section, pas sur la premiere occurrence d'une touche"
    - "Page d'installation sans aucune commande executable en ligne : chaque commande fetcher.py est ecrite sous sa forme hors-ligne, option globale avant la sous-commande"
    - "Forme fautive d'ordre des options citee en prose entre accents graves (jamais en bloc de code), pour rester hors du controle d'ancrage des commandes"
    - "Ecran decrit par ses libelles litterels produits par le code (six libelles de routes.py) et par la touche qui les declenche"

key-files:
  created: []
  modified:
    - docs/installation.md
    - tests/test_docs_structure.py

key-decisions:
  - "Le premier contact CLI enseigne reste python fetcher.py --offline db status ; la commande db sync n'est nommee qu'en prose comme hors du chemin minimal, jamais dans un bloc de code : aucune commande fetcher.py de la page ne peut atteindre l'API Dofusdude (T-01-06)"
  - "Le message d'erreur hors-ligne est reproduit par la seule forme qui l'atteint reellement (python fetcher.py --offline version) et attribue au fichier qui le leve (dofus_stuff/sync.py) : la forme sans drapeau n'echoue pas comme la page l'ecrirait (D-02, Pitfall 1 de la recherche)"
  - "La forme fautive db status --offline est ecrite en prose entre accents graves, pas en ligne de commande : le controle d'ancrage du plan 01-04 analyse les blocs de code et exige une commande analysable et hors-ligne"
  - "La section Source de verite liste des chemins reels, y compris un chemin .js (dofus_stuff/web/static/js/terminal.js) : D-01 nomme les chemins reels du code, et l'ancrage du plan 01-04 ne controle que les chemins .py"
  - "La page declare explicitement que seule l'adresse locale par defaut est documentee, sans jamais citer d'autre adresse d'ecoute (T-01-02, securite_block_on high)"
  - "Le nombre de tests n'est jamais ecrit dans la page : la page dit qu'il varie a chaque phase et n'est pas une valeur de reference"
  - "Les deux nouvelles gardes portent sur docs/installation.md seulement : un controle d'absence de db clear sur tout docs/** ferait echouer la phase 2, qui doit au contraire avertir sur db clear dans cli.md"

patterns-established:
  - "Toute garde d'ordre ou d'absence s'ecrit en fonction de test parametree par docs_dir, avec message localisant a trois elements (page, cible attendue, fichier source) — D-13"
  - "Une page de documentation utilisateur ne contient que des commandes reellement executables : l'exemple fautif vit dans la prose"

requirements-completed: [INST-01, INST-02, INST-03]

coverage:
  - id: D1
    description: "docs/installation.md mene un lecteur neuf de Python 3.11+ au premier contact CLI hors-ligne : commande reelle pip install -e \".[dev]\", verification .venv/Scripts/python.exe -m pytest -q sans compteur cite, puis python fetcher.py --offline db status"
    requirement: "INST-01"
    verification:
      - kind: other
        ref: "sonde de la tache 1 : grep pip install -e \".[dev]\", .venv/Scripts/python.exe -m pytest -q, python fetcher.py --offline db status, dofus_stuff/sync.py — rejouee avant et apres commit (bac3c1f)"
        status: pass
    human_judgment: false
  - id: D2
    description: "La page decrit une erreur reellement rencontree sous une forme reproduisible telle qu'ecrite : python fetcher.py --offline version echoue sur une base vide avec Base locale vide et --offline : impossible de synchroniser (leve par dofus_stuff/sync.py), et l'ordre fautif db status --offline est refuse avec fetcher.py: error: unrecognized arguments: --offline et le code 2 (dofus_stuff/cli.py)"
    requirement: "INST-01"
    verification:
      - kind: other
        ref: "sonde de la tache 1 : le message et la commande sont extraits de la page et recoupes avec la garde if offline: de dofus_stuff/sync.py et avec le parseur reel ; rejouee avant et apres commit"
        status: pass
    human_judgment: false
  - id: D3
    description: "La page annonce le mode de demarrage et l'adresse reels de l'interface web : python -m dofus_stuff.web, hors-ligne par defaut (--no-offline / --online), adresse http://127.0.0.1:5000 et les sept options d'entree --data-dir, --offline, --no-offline, --online, --timeout, --host, --port ; aucune autre adresse d'ecoute recommandee, --debug presente comme reserve au developpement"
    requirement: "INST-02"
    verification:
      - kind: other
        ref: "sonde de la tache 2 : grep http://127.0.0.1:5000 et python -m dofus_stuff.web ; presence des sept options verifiee sur la section ; ancrage automatique contre les defauts reels du parseur prevu au plan 01-04"
        status: pass
    human_judgment: false
  - id: D4
    description: "Le pilotage clavier est decrit AVANT la commande de lancement web, avec le champ de saisie (validation par Entree), F3, F7, F8, ESC, PageUp et PageDown, et la barre de raccourcis dynamique expliquee"
    requirement: "INST-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_pilotage_clavier_avant_lancement"
        status: pass
    human_judgment: false
  - id: D5
    description: "Les six libelles d'ecran produits par dofus_stuff/web/routes.py sont cites litteralement dans la section clavier : Quitter, Retour, Precedent, Page prec, Suivant, Page suiv"
    requirement: "INST-03"
    verification:
      - kind: other
        ref: "sonde de la tache 2 : les six chaines sont presentes dans la section Pilotage clavier ; leur ancrage automatique sur routes.py appartient aux phases 3 a 5 (GARD-02)"
        status: pass
    human_judgment: false
  - id: D6
    description: "La page d'installation ne porte aucun jeton de commande destructrice (base videe, sauvegardes purgees) et garde le seul premier contact CLI autorise"
    requirement: "INST-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_no_destructive_command_in_installation"
        status: pass
    human_judgment: false
  - id: D7
    description: "Lisibilite pour un lecteur qui n'a jamais vu le projet : clarte du chemin pas-a-pas, du tableau des touches et de la section des erreurs frequentes (critere « user-friendly » du besoin initial)"
    verification: []
    human_judgment: true
    rationale: "Aucun test ne juge la clarte d'une prose ni l'utilite d'un encadre d'erreur : les invariants prouvent l'ordre des sections, la presence des touches, des options et des libelles, pas la qualite redactionnelle ressentie par un lecteur non technique."

# Metrics
duration: 4min
completed: 2026-09-11
status: complete
---

# Phase 1 Plan 02 : page d'installation complete, du prerequis Python au premier lancement CLI puis web

**`docs/installation.md` passe du squelette a 141 lignes auto-suffisantes — chemin minimal `pip install -e ".[dev]"` -> verification pytest -> premier contact CLI hors-ligne, clavier decrit avant la commande de lancement web, adresse et mode reels du parseur, erreurs reellement rencontrees — gardees par deux nouveaux tests pytest (144 passed, aucun reseau, `.data/` intact).**

## Performance

- **Duration:** 4 min
- **Started:** 2026-09-11T10:25:14Z (tete du plan precedent, `4c3b29a`)
- **Completed:** 2026-09-11T10:29:08Z
- **Tasks:** 2/2
- **Files modified:** 2 (0 cree, 2 modifies)

## Accomplishments

- **Chemin minimal complet et hors-ligne (INST-01).** `docs/installation.md` ouvre sur les prerequis (`Python 3.11+` lu dans `pyproject.toml`, extra `dev` portant `pytest`) puis enchaine `python -m venv .venv`, la commande reelle `pip install -e ".[dev]"`, la verification `.venv/Scripts/python.exe -m pytest -q` — avec la mention explicite que le nombre de tests affiche varie a chaque phase et n'est pas une valeur de reference.
- **Premier contact CLI hors-ligne (T-01-06).** `python fetcher.py --offline db status` est enseigne comme premier contact : aucune connexion, aucune resynchronisation Dofusdude, base **creee** si absente. Les autres commandes (`version`, `search`, `self-test`, `optimize`) sont annoncees comme exigeant une base deja peuplee ; la synchronisation (`db sync`) n'est nommee qu'en prose comme hors du chemin minimal. **Aucune commande `fetcher.py` executable de la page n'omet le drapeau hors-ligne** (les deux seules sont `--offline db status` et `--offline version`).
- **Erreurs reellement rencontrees (D-02).** Le message `Erreur : Base locale vide et --offline : impossible de synchroniser` est reproduit par la seule forme qui l'atteint (`python fetcher.py --offline version`) et attribue a la garde `if offline:` de `ensure_up_to_date` dans `dofus_stuff/sync.py` ; l'ordre fautif `db status --offline` est decrit en prose avec la ligne reelle du parseur (`fetcher.py: error: unrecognized arguments: --offline`, code 2, source `dofus_stuff/cli.py`) ; la regle de securite du mode hors-ligne ferme la section.
- **Clavier avant lancement (D-09, INST-03).** Nouvelle section `## Pilotage clavier` placee avant `## Lancement de l'interface web` : champ de saisie valide par Entree (`Enter`), `F3` (quitter), `F7` / `F8` (precedent / suivant), `ESC` (retour, evenement `Escape`), `PageUp` / `PageDown` (pagination), plus l'explication que la barre de raccourcis est construite dynamiquement (le menu principal n'affiche que `F3`). Les **six libelles d'ecran** produits par `dofus_stuff/web/routes.py` sont ecrits litteralement : « Quitter », « Retour », « Precedent », « Page prec », « Suivant », « Page suiv » (GARD-02).
- **Mode et adresse reels (INST-02, T-01-02).** `python -m dofus_stuff.web` demarre hors-ligne par defaut, `--no-offline` / `--online` autorisent l'API, l'adresse par defaut annoncee est `http://127.0.0.1:5000` et la surface d'entree complete du parseur est nommee : `--data-dir`, `--offline`, `--no-offline`, `--online`, `--timeout`, `--host`, `--port`. La page declare que seule l'adresse locale par defaut est documentee — aucune autre adresse d'ecoute n'y est ecrite (exposer ce serveur de developpement sans authentification serait un constat bloquant). `--debug` n'apparait que suivi de la mention qu'il est reserve au developpement (T-01-03).
- **Deux gardes automatiques, non vacues.** `test_pilotage_clavier_avant_lancement` (ordre de section mesure, extraction de la section jusqu'au H2 suivant, les six touches exigees **dans** la section) et `test_no_destructive_command_in_installation` (presence de `--offline db status`, absence de `db clear` et de `PURGE`). Les six derives injectees dans une copie jetable hors depot sont refusees et nommees ; sur l'arbre livre, les deux tests passent.
- **Non-intrusion mesuree.** Suite complete : **144 passed** (142 existants + 2 nouveaux), soit aucune regression ; `.data/dofus.sqlite3` inchange (mtime `1788730056`, 24 989 696 octets avant et apres) ; `git status --porcelain -- dofus_stuff` vide ; aucun fichier cree sous `docs/` (donc aucune entree de sommaire a ajouter).
- **Diff propre.** `git diff --numstat` du plan : `109 1 docs/installation.md` (la seule suppression est le remplacement de la phrase sur les gestionnaires de paquets) et `101 0 tests/test_docs_structure.py` — aucune reecriture integrale de fin de ligne ; H1 `# Installation` et ligne `[Retour au sommaire](sommaire.md)` conserves.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : chemin minimal d'installation, verification et premier contact CLI** - `bac3c1f` (docs)
2. **Tache 2 : clavier avant lancement, mode et adresse web, et leurs deux gardes** - `7cebd53` (docs)

**Plan metadata:** commit `docs(01-02): complete ...` (ce SUMMARY.md + STATE.md + ROADMAP.md + REQUIREMENTS.md), cree immediatement apres ce fichier.

_Note : les deux commits nomment leurs chemins explicitement ; `git show --name-only` ne montre aucun autre fichier, et aucune suppression de fichier suivi n'est presente (`git diff --diff-filter=D` vide)._

## Files Created/Modified

- `docs/installation.md` (33 -> 141 lignes) — huit sections : `## Prerequis`, `## Installation`, `## Verification`, `## Premier lancement`, `## Pilotage clavier`, `## Lancement de l'interface web`, `## Erreurs frequentes`, `## Source de verite` ; la section « Source de verite » gagne `dofus_stuff/sync.py`, `dofus_stuff/web/__main__.py`, `dofus_stuff/web/routes.py` et `dofus_stuff/web/static/js/terminal.js` (D-03).
- `tests/test_docs_structure.py` (+101 lignes) — constantes `H2`, `TITRE_CLAVIER`, `LANCEMENT_WEB`, `TOUCHES_CLAVIER`, `COMMANDE_DESTRUCTRICE`, `JETON_PURGE` ; helpers prives `_page(docs_dir, nom)` (appuye sur `_pages`) et `_section(texte, titre)` ; tests `test_pilotage_clavier_avant_lancement` et `test_no_destructive_command_in_installation` (8 tests dans le module).

## Decisions Made

- **Le seul contact CLI enseigne est hors-ligne, et `db sync` n'existe pas comme commande de la page.** Le plan laisse la possibilite de nommer `db sync` ; elle n'est ecrite qu'en prose entre accents graves (« obtenir une base peuplee suppose une synchronisation reseau »), jamais en bloc de code. Motif : le controle d'ancrage du plan 01-04 analyse les blocs de code et exige que chaque commande `fetcher.py` qui y figure soit analysable **et** hors-ligne (T-01-06) ; une commande `db sync` y aurait ete un ecart sanctionne.
- **La forme fautive d'ordre des options est en prose, pas en ligne de commande.** `db status --offline` et la ligne `fetcher.py: error: unrecognized arguments: --offline` sont cites entre accents graves dans `## Erreurs frequentes` ; aucune commande fautive n'est presentee sous forme executable (exigence explicite de la tache 1 et du plan 01-04).
- **La page ne nomme aucun gestionnaire de paquets alternatif.** La phrase dit que `pip` suffit et qu'aucun autre gestionnaire n'est utilise, au lieu de citer les outils ecartes : le critere d'acceptation interdit de citer un autre gestionnaire que `pip` (D-08).
- **Aucun compteur de tests dans la prose.** La section `## Verification` dit explicitement que le nombre affiche change a chaque phase et n'est pas une valeur de reference ; le seul compteur du projet vit dans ce SUMMARY et dans les commits, jamais dans `docs/`.
- **Les deux nouvelles gardes portent sur `docs/installation.md` seul.** Un controle d'absence de `db clear` sur tout `docs/**` ferait echouer la phase 2, dont la carte prescrit justement un encadre d'avertissement sur `db clear` dans `cli.md` ; l'absence est donc exigee sur la page d'installation, celle que le lecteur suit aveuglement (T-01-05).
- **`dofus_stuff/web/static/js/terminal.js` figure dans la section « Source de verite ».** D-01 demande les chemins reels du code et le plan nomme explicitement ce chemin parmi les deux a ajouter ; l'ancrage automatique des phases suivantes ne controle que les chemins `.py`, qui sont tous existants (`__main__.py`, `routes.py`).
- **Ordre interne de `## Erreurs frequentes`** : erreur reellement rencontree (base vide), puis erreur d'ordre des options, puis rappel de l'ordre correct, puis regle de securite du mode hors-ligne — le rappel arrive apres l'erreur qu'il corrige.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Parenthese fermante en double a la fin de `tests/test_docs_structure.py`**
- **Found during:** Tache 2 (ajout des deux gardes)
- **Issue:** l'insertion des nouveaux tests apres la derniere assertion de `test_readme_links_to_sommaire` a laisse la parenthese fermante d'origine en fin de fichier ; `pytest` a echoue immediatement sur `SyntaxError: unmatched ')'` (module entier en erreur, aucun test collecte).
- **Fix:** suppression exacte de la ligne surnumeraire ; module recharge puis verifie.
- **Files modified:** `tests/test_docs_structure.py`
- **Verification:** `pytest tests/test_docs_structure.py -q` -> 8 passed ; suite complete -> 144 passed
- **Committed in:** `7cebd53` (Tache 2)

**2. [Rule 3 - Blocking] Forme fautive d'ordre des options initialement ecrite en bloc de code**
- **Found during:** Tache 1 (section des erreurs frequentes)
- **Issue:** le rappel d'ordre a d'abord ete ecrit sous la forme d'un bloc ```text contenant `python fetcher.py [options globales] <sous-commande> …` : cette ligne n'est analysable ni par `shlex` ni par le parseur, donc le controle d'ancrage du plan 01-04 (qui exige de chaque commande `fetcher.py` des blocs de code qu'elle soit analysable et hors-ligne) l'aurait refusee.
- **Fix:** le bloc a ete remplace par une phrase de prose disant que les options globales se placent avant la sous-commande, avec l'exemple correct `python fetcher.py --offline db status` et le rappel de la forme fautive en accents graves.
- **Files modified:** `docs/installation.md`
- **Verification:** sonde « blocs de code » rejouee : seules deux commandes `fetcher.py` subsistent dans les blocs, toutes deux en forme `--offline <sous-commande>` ; grep des motifs obligatoires toujours vert
- **Committed in:** `bac3c1f` (Tache 1)

**3. [Rule 3 - Blocking] Gestionnaires de paquets alternatifs nommes dans la prose**
- **Found during:** Tache 1 (section installation)
- **Issue:** la phrase initiale citait `uv`, `pipx` et `poetry` pour dire qu'ils ne sont pas utilises — ce qui contredit le critere d'acceptation « la page ne cite aucun gestionnaire de paquets autre que `pip` » (D-08) et aurait fait diverger la page d'un controle mecanique sur ces jetons.
- **Fix:** phrase remplacee par « `pip` suffit, aucun autre gestionnaire de paquets n'est utilise par le projet » ; la seule suppression du diff de la page porte sur cette phrase.
- **Files modified:** `docs/installation.md`
- **Verification:** `pipx` et `poetry` absents de la page ; criterion d'acceptation rejoue
- **Committed in:** `bac3c1f` (Tache 1)

**4. [Rule 3 - Blocking] Fins de ligne LF introduites par les ecritures d'outil**
- **Found during:** Taches 1 et 2 (les deux fichiers livres sont integralement CRLF dans le depot)
- **Issue:** les ecritures d'outil produisent des fins de ligne LF ; laisser le fichier en LF (ou en melange) produirait un diff non representatif sur des fichiers suivis en CRLF (defaut deja rencontre par le plan 01-01).
- **Fix:** normalisation explicite du fichier complet en bytes (`\r\n` -> `\n` -> `\r\n`) apres chaque ecriture, avant commit.
- **Files modified:** `docs/installation.md`, `tests/test_docs_structure.py`
- **Verification:** comptage `grep -c $'\r$'` = nombre total de lignes pour les deux fichiers ; `git diff --numstat` du plan : `109 1` et `101 0` (aucune reecriture integrale, aucune suppression de ligne non voulue)
- **Committed in:** `bac3c1f` (Tache 1) et `7cebd53` (Tache 2)

---

**Total deviations:** 4 auto-fixed (1 bug, 3 blocking)
**Impact on plan:** Aucun ecart de perimetre, aucune decision produit : les quatre correctifs portent sur la conformite aux criteres d'acceptation du plan, sur la nettete du diff et sur la validite syntaxique du module de test. Les chemins livres sont exactement ceux du `files_modified` du plan (`docs/installation.md`, `tests/test_docs_structure.py`) — aucune autre page, aucun fichier de `dofus_stuff/**`, aucune entree de sommaire.

## Issues Encountered

- **En-tete de branche `main` (meme situation que le plan 01-01).** L'orchestrateur a dispatche cet executant comme **sequentiel sur l'arbre principal** (`git.branching_strategy: "none"`, historique de la phase integralement sur `main`) ; les deux commits y sont donc poses, conformement a la consigne de dispatch. Aucun `update-ref`, aucun `push`, aucun reset destructeur, aucun `git clean` ni `git stash`.
- **Controle de morsure des deux nouvelles gardes execute hors depot.** Les six derives (titre clavier renomme, touche `F8` retiree de la section, commande de lancement supprimee, `db clear` injecte, jeton `PURGE` injecte, premier contact CLI altere) ont ete injectees dans des copies `tempfile.mkdtemp()` de `docs/`, jamais dans l'arbre livre : la mutation de l'arbre reel appartient au plan 01-03. Resultat : les six derives sont refusees avec un message nommant la page, la touche ou le jeton, et le fichier source ; l'arbre livre reste vert.
- **Le test de mutation du plan 01-03 n'a pas ete execute** (`test_mutation_detecte_les_trois_derives` n'existe pas encore) : le plan de ce plan 01-02 le declaraite explicitement attendu seulement apres 01-03.
- **Fichiers non suivis preexistants laisses intacts** : `.doc-agent/`, `.gsd/`, `doc-agent.toml`, `gsd-auto.toml`, `gsd-auto-rules.toml`, `.planning/milestone.lock`, `.planning/state.json`, ainsi que la modification preexistante de `.gitignore`. Aucun `git add .` : chaque commit nomme ses chemins.
- **Sondes d'acceptation rejouees apres commit** (et non seulement avant) : motifs obligatoires, forme hors-ligne de chaque commande `fetcher.py` des blocs de code, absence de compteur de tests, presence des sept options web, six libelles d'ecran, H1 et ligne de retour — tous PASS sur `7cebd53`.

## Known Stubs

Aucun. Aucune valeur codee en dur, aucun libelle d'attente, aucun `TODO` : les deux tests lisent l'arbre livre sans donnee fictive, et la page ne contient que des valeurs derivees du produit (`3.11`, `pip install -e ".[dev]"`, `.venv/Scripts/python.exe -m pytest -q`, `http://127.0.0.1:5000`, libelles de `routes.py`).

## Threat Flags

Aucun. Les surfaces documentaires nouvelles sont toutes couvertes par le `<threat_model>` du plan : adresse d'ecoute (T-01-02, seule l'adresse locale par defaut est ecrite), mode debogage (T-01-03, `--debug` signale comme reserve au developpement, hors chemin minimal), commandes destructrices (T-01-05, garde automatique), quota Dofusdude (T-01-06, toutes les commandes executable sont hors-ligne), valeurs de configuration (T-01-01, aucune valeur par defaut de configuration ni variable d'environnement recopiee).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Pret pour le plan 01-03** : les gardes de structure se sont ajoutees sans toucher aux helpers existants ; `tempfile`/`shutil` sont les seuls modules a ajouter au futur test de mutation, et la copie jetable de `docs/` fonctionne (verifiee six fois ici).
- **Pret pour le plan 01-04** : la page porte deja la surface qu'il ancrera — lancement web hors-ligne par defaut, sept options d'entree, adresse derivee des defauts reels du parseur (`http://127.0.0.1:5000`), six libelles d'ecran ecrits litteralement, et chaque commande `fetcher.py` des blocs de code munie du drapeau hors-ligne place avant la sous-commande. Le contexte de `## Erreurs frequentes` (option globale apres la sous-commande) peut etre relu sans crainte : aucune commande fautive n'y est executable.
- **Signal de sommaire inchange** : le plan n'ajoute aucune page sous `docs/`, donc `docs/sommaire.md` garde sa seule entree et l'egalite d'ensembles reste un vrai signal (`problemes_liens` et `problemes_index` renvoient tous deux la liste vide).
- **Point d'attention mesure** : l'`estimate` du plan (46 000 tokens) reste tres au-dessus de l'`actual` mesure sur le meme barème (2 695 tokens, soit 10 783 caracteres ajoutes). Comme au plan 01-01, l'ecart suggere un estimate exprime a l'echelle du contexte du plan plutot qu'a celle du diff ; il est enregistre tel quel, sans arrondi, pour calibrer les prochains (ADR-2629).
- **Blocage** : aucun.

---
*Phase: 01-socle-documentaire-installation-et-harnais-v-rifiable*
*Completed: 2026-09-11*

## Self-Check: PASSED

- Fichiers livres presents sur disque : `docs/installation.md` (141 lignes), `tests/test_docs_structure.py` (291 lignes) et ce SUMMARY — verifies par `[ -f ]`.
- Commits presents dans l'historique : `bac3c1f` (tache 1), `7cebd53` (tache 2) — verifies par `git log --oneline --all`.
- Criteres d'acceptation rejoues apres commit : motifs obligatoires de la page (`pip install -e ".[dev]"`, `.venv/Scripts/python.exe -m pytest -q`, `python fetcher.py --offline db status`, `python fetcher.py --offline version`, `dofus_stuff/sync.py`, `http://127.0.0.1:5000`, `python -m dofus_stuff.web`) — tous PASS.
- Verification de plan : `pytest tests/test_docs_structure.py -q` -> 8 passed ; `pytest -q` -> 144 passed (142 existants + 2 nouveaux, aucune regression) ; `.data/dofus.sqlite3` inchange (mtime 1788730056, 24 989 696 octets avant et apres) ; `git status --porcelain -- dofus_stuff` vide.
- Morsure des deux nouvelles gardes verifiee sur six derives injectees dans des copies jetables hors depot : les six sont refusees et nommees (page, touche/jeton, fichier source).
