---
phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
plan: 01
subsystem: documentation
tags: [markdown, pytest, docs-fr, link-integrity, doc-harness]

# Dependency graph
requires: []
provides:
  - "docs/sommaire.md : point d'entree unique de la documentation (parcours conseille + index thematique)"
  - "docs/installation.md : squelette au gabarit D-01 (complete par le plan 01-02)"
  - "README.md : section « Documentation utilisateur » a lien unique (SOMM-01, D-10)"
  - "tests/conftest.py : helper de normalisation _normalize (D-11) et fixtures de session docs_dir / normalize (D-12)"
  - "tests/test_docs_structure.py : helpers _pages / problemes_liens / problemes_index et six invariants executes sur l'arbre livre"
affects: [01-02, 01-03, 01-04, phase-02, phase-03, phase-04, phase-05, phase-06]

# Actuals (#2632) — mesure sur le meme barème que l'estimate du plan (chars/4 du diff realise, pas un compteur de harnais).
actuals:
  tokens: 2379
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Lecture de page Markdown avec encoding=\"utf-8\" explicite (jamais read_text() nu)"
    - "Fonctions d'invariant pures au niveau module, parametrees par docs_dir: Path, renvoyant list[str] (liste vide = conforme)"
    - "Normalisation D-11 : html.unescape + NFKD + suppression des diacritiques + \\s+ -> espace + minuscules"
    - "Messages d'echec localisants a trois elements (page, cible/libelle attendu, chemin de reference) — D-13"

key-files:
  created:
    - docs/sommaire.md
    - docs/installation.md
    - tests/test_docs_structure.py
  modified:
    - README.md
    - tests/conftest.py

key-decisions:
  - "Le sommaire ne porte aucune cible de lien hors des entrees du tableau d'index : pas de ligne de retour vers ../README.md, aucun lien dans l'introduction ni dans le parcours conseille — condition pour que l'egalite d'ensembles sommaire <-> docs/**/*.md reste un vrai signal (SOMM-02, D-05, D-06)"
  - "Le parcours conseille des sept themes est ecrit en texte numerote simple, sans lien markdown : une cible absente ferait rougir problemes_index sans aucune liste blanche possible"
  - "Les imports ajoutes a tests/conftest.py vivent en tete de fichier, les fixtures et le helper en fin de fichier (le plan nommait les deux emplacements pour le meme bloc ; la carte de patrons tranche pour l'en-tete)"
  - "Fins de ligne CRLF conservees sur les trois fichiers touches (core.autocrlf=true) et ecriture des pages via bytes pour eviter un diff integral"
  - "Les commits de ce plan atterrissent sur main : l'orchestrateur a dispatche un executant sequentiel sur l'arbre principal avec branching_strategy: \"none\" (voir Issues Encountered)"

patterns-established:
  - "Harnais documentaire : le code est la source de verite, la doc est le reflet, le test est le juge — les invariants sont des fonctions pures testables contre l'arbre livre ET contre une copie jetable"
  - "Invariant tolerant au dossier absent : problemes_liens / problemes_index renvoient « docs/sommaire.md : absent » au lieu de lever FileNotFoundError (D-13)"
  - "Detection de morsure : chaque derive injectee dans une copie jetable est refusee et la derive est nommee dans le message"

requirements-completed: [SOMM-01, SOMM-02]

coverage:
  - id: D1
    description: "README.md ouvre la documentation par une section unique « Documentation utilisateur » a un seul lien vers docs/sommaire.md, la cible existant sur disque"
    requirement: "SOMM-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_readme_links_to_sommaire"
        status: pass
    human_judgment: false
  - id: D2
    description: "docs/sommaire.md liste exactement les pages presentes sous docs/ (une seule en phase 1) et toutes ses cibles de liens resolvent"
    requirement: "SOMM-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_sommaire_lists_every_document"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_sommaire_links_resolve"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_all_relative_links_resolve"
        status: pass
    human_judgment: false
  - id: D3
    description: "docs/installation.md existe au gabarit leger D-01 (H1 unique, sections courtes, bloc « Source de verite », ligne de retour) ; le contenu complet arrive au plan 01-02"
    verification:
      - kind: other
        ref: "sonde de la tache 1 : chaine README -> docs/sommaire.md -> docs/installation.md resolue (verifiee avant et apres commit)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Comparaison de libelles normalisee (D-11) et fixtures de documentation D-12 disponibles sans modifier les fixtures existantes"
    verification:
      - kind: unit
        ref: "tests/conftest.py#_normalize / docs_dir / normalize (exercises par le module de structure)"
        status: pass
      - kind: unit
        ref: "git diff PLAN_HEAD_BEFORE..HEAD -- tests/conftest.py : 25 insertions, 0 suppression (fixtures catalog/app/client byte-identiques)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Lisibilite pour un lecteur qui n'a jamais vu le projet : clarte du parcours conseille et des libelles d'index (critere « user-friendly » du besoin initial)"
    verification: []
    human_judgment: true
    rationale: "Aucun test ne juge la clarte d'une prose : les invariants prouvent la structure, l'exhaustivite et l'absence de lien mort, pas la qualite redactionnelle ni l'ordre pedagogique ressenti par un lecteur non technique."

# Metrics
duration: 2min
completed: 2026-09-11
status: complete
---

# Phase 1 Plan 01 : Chaine documentaire README -> sommaire -> installation, et ses six premiers invariants

**La chaine README.md -> docs/sommaire.md -> docs/installation.md existe sur disque, gardee par six tests pytest alimentes par les nouvelles fixtures de documentation de tests/conftest.py (sans import du produit, sans reseau, sans ecriture sous .data/).**

## Performance

- **Duration:** 2 min
- **Started:** 2026-09-11T10:22:13Z
- **Completed:** 2026-09-11T10:24:02Z
- **Tasks:** 2/2
- **Files modified:** 5 (3 crees, 2 modifies)

## Accomplishments

- `README.md` gagne la section « Documentation utilisateur » placee avant `## Base locale Dofus`, avec un lien markdown unique vers `docs/sommaire.md` ; la ligne existante vers `GUIDE_WIZARD.md` est inchangee (le diff ne compte que 4 lignes ajoutees, 0 supprimee).
- `docs/sommaire.md` est le point d'entree unique : parcours conseille numerote des sept themes (Installation -> Parcours simplifie -> Wizard avance -> CLI -> Base locale -> Depannage -> Glossaire) puis tableau d'index a une entree `[Installation](installation.md)`. Aucune autre cible de lien : l'egalite d'ensembles sommaire <-> `docs/**/*.md` reste donc un vrai signal pour les cinq phases suivantes (D-05, D-06).
- `docs/installation.md` pose le squelette au gabarit D-01 : H1 `# Installation`, cinq sections (Prerequis, Installation, Verification, Premier lancement, Source de verite), trois chemins reels (`pyproject.toml`, `fetcher.py`, `dofus_stuff/cli.py`) et la ligne de retour vers `sommaire.md`.
- `tests/conftest.py` expose `_normalize` (D-11) et deux fixtures de session `docs_dir` / `normalize` ; le diff porte **25 insertions et 0 suppression** : `catalog`, `app`, `client` et `_sample_items` sont byte-identiques a l'etat anterieur (D-12).
- `tests/test_docs_structure.py` livre six invariants executes sur l'arbre livre : 6 passed en 0,02 s ; suite complete : 142 passed (136 existants + 6 nouveaux), aucune regression.
- Le harnais **mord** : sur une copie jetable (hors depot, `tempfile`), les six derives injectees sont refusees et nommees — lien mort, cible hors racine du depot, cible absolue, page non listee, cible listee absente, ancre `#` vue par le motif `LINK`.
- `.data/dofus.sqlite3` est intact (mtime et taille identiques avant/apres la suite) : aucun acces reseau, aucun appel a `main()`.

## Task Commits

Each task was committed atomically:

1. **Tache 1 (tracer) : chaine documentaire README -> sommaire -> installation** - `a8f080b` (docs)
2. **Tache 2 : fixtures de documentation et six invariants de structure** - `53dbc4b` (test)

**Plan metadata:** commit `docs(01-01): complete ...` (ce SUMMARY.md + STATE.md + ROADMAP.md), cree immediatement apres ce fichier.

_Note : les deux commits ne portent respectivement que les trois chemins de documentation, puis les deux chemins de test — aucun autre chemin n'est touche (verifie par `git show --name-only`)._

## Files Created/Modified

- `README.md` (+4 lignes) — section « Documentation utilisateur » : phrase d'intention + lien unique vers `docs/sommaire.md` (SOMM-01, D-10).
- `docs/sommaire.md` (nouveau, 19 lignes) — point d'entree unique : parcours conseille en texte simple + index thematique a une entree (D-04, D-05).
- `docs/installation.md` (nouveau, 33 lignes) — squelette D-01 : prerequis Python 3.11+, `pip install -e ".[dev]"`, `pytest -q` via l'interpreteur epingle, premier lancement `python fetcher.py --offline db status`, bloc « Source de verite », retour au sommaire.
- `tests/conftest.py` (+25 lignes) — `_normalize(text: str) -> str` (D-11) et fixtures de session `docs_dir` / `normalize` (D-12) ; fixture existantes intactes.
- `tests/test_docs_structure.py` (nouveau, 189 lignes) — motifs `LINK` / `H1`, helpers `_pages`, `problemes_liens`, `problemes_index`, six tests a messages localisants (D-13).

## Decisions Made

- **Aucune cible de lien hors de l'index dans `docs/sommaire.md`** : ni ligne de retour vers `../README.md`, ni lien dans l'introduction, ni lien dans le parcours conseille. Motif : une cible `../README.md` ne resout pas dans l'espace de noms `docs/`, donc `test_sommaire_lists_every_document` serait rouge sur l'arbre livre et l'etape « arbre sain avant mutation » du plan 01-03 le serait par construction (SOMM-02, D-05, D-06).
- **Parcours conseille en texte numerote simple** : les sept themes de D-04 sont lisibles et verifiables dans l'ordre, mais ne creent aucune cible de lien ; une cible absente ferait rougir `problemes_index` sans liste blanche possible.
- **Emplacement du bloc ajoute a `tests/conftest.py`** : le plan nomme a la fois « en fin de fichier » et « les imports » ; la carte de patrons (`01-PATTERNS.md`) tranche pour les imports en tete de fichier et les fixtures/helper en fin de fichier. Les fixtures existantes restent byte-identiques.
- **Fins de ligne conservees en CRLF** sur les cinq chemins touches (`core.autocrlf=true` sur ce poste) : le diff ne montre que les lignes reellement ajoutees, aucune reecriture integrale.
- **Factorisation du message « sommaire absent »** en un helper prive `_sommaire_absent()` plutot que de dupliquer la chaine dans les deux fonctions d'invariant : `problemes_liens` et `problemes_index` renvoient le meme probleme lisible au lieu de lever (D-13).
- **Aucune decision produit nouvelle** : le cadrage derive de l'objectif est repris tel quel du `Goal` de la phase et des decisions D-01, D-04 a D-06, D-10 a D-12 ; le seul ecart au decoupage indicatif du ROADMAP (ce plan cree `tests/conftest.py` et six tests, et non le plan 01-03) etait deja assume dans le plan.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fins de ligne CRLF ecrasees par la premiere ecriture de `README.md`**
- **Found during:** Tache 1 (chaine documentaire)
- **Issue:** une premiere insertion en mode texte a converti les 121 fins de ligne CRLF du `README.md` en LF (lecture en texte universel + ecriture `newline=""`), laissant un fichier mixte et un diff non representatif.
- **Fix:** les trois fichiers touches ont ete reecrits en bytes avec conversion explicite `\n` -> `\r\n` ; controle `CRLF: 125 / LF-only: 0` sur `README.md` apres correction.
- **Files modified:** `README.md` (les pages nouvelles ont ete ecrites directement en CRLF)
- **Verification:** `git diff --numstat README.md` -> `4 0 README.md` (4 insertions, 0 suppression)
- **Committed in:** `a8f080b` (Tache 1)

**2. [Rule 3 - Blocking] Emplacement ambigu du bloc ajoute a `tests/conftest.py`**
- **Found during:** Tache 2 (fixtures et invariants)
- **Issue:** le plan situe l'ensemble « imports + `_normalize` + fixtures » en fin de fichier ; poser les imports apres la fixture `client` aurait ete non idiomatique et fragile.
- **Fix:** imports stdlib ajoutes en tete de fichier (`html`, `re`, `unicodedata`, `pathlib.Path`), helper `_normalize` et fixtures de session en fin de fichier — lecture confirmee par `01-PATTERNS.md` (« imports en tete de fichier »).
- **Files modified:** `tests/conftest.py`
- **Verification:** `git diff --numstat tests/conftest.py` -> `25 0` (aucune suppression ⇒ fixtures existantes intactes) ; suite complete 142 passed
- **Committed in:** `53dbc4b` (Tache 2)

**3. [Rule 3 - Blocking] Helper prive `_sommaire_absent()` ajoute**
- **Found during:** Tache 2
- **Issue:** le plan exige que `problemes_liens` **et** `problemes_index` renvoient un probleme lisible `docs/sommaire.md : absent` au lieu de lever (D-13) ; sans factorisation, la meme chaine de message etait dupliquee dans les deux fonctions.
- **Fix:** helper prive `_sommaire_absent() -> list[str]` au niveau module, appele par les deux fonctions. Les trois helpers nommes par le plan (`_pages`, `problemes_liens`, `problemes_index`) restent presents au niveau module.
- **Files modified:** `tests/test_docs_structure.py`
- **Verification:** `pytest tests/test_docs_structure.py -q` -> 6 passed ; dossier `docs/` absent simule (copie jetable sans sommaire) -> les deux fonctions renvoient la liste de problemes, aucune exception
- **Committed in:** `53dbc4b` (Tache 2)

---

**Total deviations:** 3 auto-fixed (3 blocking)
**Impact on plan:** Aucun ecart de perimetre, aucune decision produit : les trois correctifs portent sur l'hygiene du diff et sur la lisibilite du code du harnais. Les fichiers du `files_modified` du plan sont exactement ceux touches.

## Issues Encountered

- **En-tete de branche `main`.** Le protocole d'execution de l'agent interdit par defaut de committer sur la branche protegee (`main`), mais l'orchestrateur a dispatche cet executant comme **sequentiel sur l'arbre principal** et `git.base-branch --is-protected main` renvoie `true` sans override `git.allow_default_branch_commits`. La configuration du projet porte `git.branching_strategy: "none"` et l'historique de la phase est integralement sur `main` : les deux commits de ce plan y sont donc poses, conformement a la consigne de dispatch. Aucun `update-ref`, aucun `push`, aucun reset destructeur n'a ete execute ; aucun `git clean` ni `git stash`.
- **Controle de morsure du harnais execute hors depot.** La verification « le harnais mord » a ete faite sur une copie `tempfile.mkdtemp()` de `docs/`, jamais sur l'arbre livre (la mutation de l'arbre reel appartient au plan 01-03). Aucune ecriture n'a eu lieu sous `docs/`, `.planning/` ou `.data/`.
- **Fichiers non suivis preexistants laisses intacts** : `.doc-agent/`, `doc-agent.toml`, `gsd-auto.toml`, `gsd-auto-rules.toml`, `.gsd/`, `.planning/milestone.lock`, `.planning/state.json`, ainsi que la modification preexistante de `.gitignore`. Aucun `git add .` n'a ete employe : chaque commit nomme ses chemins explicitement.

## Known Stubs

| Fichier | Ligne | Raison |
|---------|-------|--------|
| `docs/installation.md` | page entiere | Squelette volontairement partiel au gabarit D-01 : le chemin pas-a-pas complet (environnement virtuel, lancement web, pilotage clavier avant lancement, erreurs frequentes) est livre par le **plan 01-02**. Le plan le declare explicitement (« volontairement partiel — le contenu complet arrive dans le plan 01-02 ») ; les cinq sections et le bloc « Source de verite » presents suffisent a la sonde de la tache 1. Son exhaustivite documentaire n'est donc **pas** revendiquee par ce plan. |

Aucun autre stub : les six invariants lissent l'arbre livre sans valeur codee en dur, et aucune sortie d'interface ne recoit de donnee vide ou fictive.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Pret pour le plan 01-02** : `docs/installation.md` existe au gabarit D-01 avec ses cinq sections ; il n'y a qu'a developer le contenu (environnement virtuel, lancement web, clavier avant lancement, erreurs frequentes) sans changer la tete ni la ligne de retour.
- **Pret pour le plan 01-03** : `tests/conftest.py` expose `_normalize`, `docs_dir`, `normalize` et `tests/test_docs_structure.py` expose `LINK`, `H1`, `_pages`, `problemes_liens`, `problemes_index` — la verification d'exhaustivite bidirectionnelle et le test de mutation peuvent s'appuyer dessus directement (l'egalite d'ensembles est deja un vrai signal, une seule page etant livree).
- **Signal reste discriminant** : le sommaire ne portant qu'une cible, toute page ajoutee par une phase ulterieure sans ligne d'index fera echouer `test_sommaire_lists_every_document` — c'est le garde-fou attendu jusqu'en phase 6 (D-05, D-06).
- **Point d'attention mesure** : l'`estimate` du plan (42 000 tokens) est tres au-dessus de l'`actual` mesure sur le meme barème (2 379 tokens, soit 9 516 caracteres de diff realise). L'ecart suggere que l'estimate a ete exprime a l'echelle de tout le contexte du plan plutot qu'a celle du diff ; il est enregistre tel quel, sans arrondi, pour calibrer les prochains (ADR-2629).
- **Blocage** : aucun.

---
*Phase: 01-socle-documentaire-installation-et-harnais-v-rifiable*
*Completed: 2026-09-11*

## Self-Check: PASSED

- Fichiers crees presents sur disque : `docs/sommaire.md`, `docs/installation.md`, `tests/test_docs_structure.py`, `.planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-01-SUMMARY.md` ; chemins modifies `README.md`, `tests/conftest.py` — tous verifies par `[ -f ]`.
- Commits presents dans l'historique : `a8f080b` (tache 1), `53dbc4b` (tache 2) — verifies par `git log --oneline --all`.
- Criteres d'acceptation des deux taches rejoues apres commit : README (section avant `## Base locale Dofus`, cible `docs/sommaire.md` x1, ligne `GUIDE_WIZARD.md` inchangee), section du sommaire (H1, sept themes ordonnes, index `Installation` -> `installation.md`), cibles de liens du sommaire = `{installation.md}`, structure de `docs/installation.md` (H1, cinq sections, trois chemins, retour au sommaire) — tous PASS.
- Sonde de bout en bout rejouee apres commit : `chaine README -> docs/sommaire.md -> docs/installation.md resolue`.
- Verification de plan : `pytest tests/test_docs_structure.py -q` -> 6 passed ; `pytest -q` -> 142 passed ; `git status --porcelain` ne montre aucun chemin de ce plan hors des cinq chemins livres ; `.data/dofus.sqlite3` inchangé (mtime 1788730056, taille 24 989 696 avant et apres).
- Claim du correctif 3 verifiee : `docs/` absent (chemin inexistant) -> `problemes_liens` et `problemes_index` renvoient la liste de problemes `docs/sommaire.md : absent`, aucune exception.
