---
phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
plan: 03
subsystem: testing
tags: [pytest, docs-fr, markdown, mutation-test, doc-harness, utf8]

# Dependency graph
requires:
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plans 01-01 et 01-02 : tests/conftest.py (fixture docs_dir, _normalize expose par la fixture normalize), tests/test_docs_structure.py (motifs LINK / H1 / LIENS_EXTERNES, helpers _pages / _sommaire_absent / problemes_liens / problemes_index / _page / _section, huit invariants), docs/sommaire.md a une entree et docs/installation.md complet (H1 Installation, ligne de retour [Retour au sommaire](sommaire.md))"
provides:
  - "tests/test_docs_structure.py : helpers purs pages_listees(docs_dir), problemes_h1(docs_dir, normalize), problemes_retour_sommaire(docs_dir), problemes_encodage(docs_dir, normalize)"
  - "cinq invariants de gabarit : H1 unique egal au libelle d'index (SOMM-03), ligne de retour resolue vers sommaire.md (SOMM-03, D-01), UTF-8 strict sans jeton de brouillon ni page de moins de 300 caracteres (GARD-01), libelles d'index normalises uniques et sommaire non auto-liste (SOMM-02), normalisation de D-11 elle-meme testee (D-12)"
  - "test_mutation_detecte_les_trois_derives : preuve executable du critere de succes 5 (copie tmp_path/docs, trois derives nommees, arbre livre intact)"
affects: [01-04, phase-02, phase-03, phase-04, phase-05, phase-06]

# Mesure #3968 — le registre de plan est sur disque, le compte n'est jamais narre.
plan_head_before: 80b0550f0c9e59ce0ffc4485399892747ff87e74
commits: 2

# Actuals (#2632) — meme barème que l'estimate du plan (chars/4 du diff realise, pas un compteur de harnais).
actuals:
  tokens: 3072
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Invariant de contenu teste deux fois : la meme fonction pure (docs_dir: Path en parametre) s'execute contre l'arbre livre et contre une copie shutil.copytree sous tmp_path"
    - "Lecture stricte centralisee : _lire_page(page) -> str | None lit en encoding=\"utf-8\" et renvoie None au lieu de lever, ce qui laisse chaque invariant nommer le fichier fautif (D-13)"
    - "Comparaison toujours normalisee : la fonction de D-11 est passee en parametre des helpers (jamais redefinie dans le module de test, D-12)"
    - "Mutation en trois temps separes : chaque derive est injectee puis immediatement confrontee a son invariant, avec exigence que le message nomme la cible injectee"

key-files:
  created: []
  modified:
    - tests/test_docs_structure.py

key-decisions:
  - "Le test de mutation s'arrete sur une egalite d'ensemble avant toute injection (problemes_liens + problemes_index + problemes_h1 tous vides) : si l'arbre livre etait deja en derive, le test echoue en le disant au lieu de prouver une detection sur un etat faux"
  - "Chaque derive est verifiee par un any(<cible injectee> in probleme ...) et non par un simple « la liste est non vide » : un harnais casse pour une autre raison ne peut pas faire passer le test (Pitfall 9 de la recherche)"
  - "L'arbre livre est relu dans le meme corps de test apres les mutations : presence de (sommaire.md), H1 « # Installation » en tete, absence de docs/glossaire.md — la propriete visee est « rien n'a ete ecrit dans docs/ » (T-01-07)"
  - "La derive (c) remplace la premiere occurrence de « # Installation » (count=1) : sans cela, la sous-chaine presente dans « ## Installation » aurait aussi ete renommee et la mutation n'aurait plus isole le H1"
  - "Trois nouvelles constantes de module (LIEN_LIBELLE, JETONS_BROUILLON, LONGUEUR_MINIMALE) plutot que des litteraux disperses : la cible d'index est relue avec son libelle, sans introduire une deuxieme definition de l'ensemble d'index de 01-01"
  - "Aucune ecriture dans docs/ ni sous .data/ : la mutation vit exclusivement dans tmp_path/docs, et le test des invariants de longueur, de brouillon et de decodage ne s'execute que sur des fichiers Markdown (D-15, T-01-08)"

patterns-established:
  - "Preuve d'echec locale : une derive injectee doit apparaitre nommee dans le message de l'invariant qui la refuse — « quelque chose a echoue » n'est pas une preuve (critere de succes 5)"
  - "Un invariant de contenu tolerant a l'encodage : le fichier illisible devient un probleme localisant, jamais une exception qui masquerait la page fautive"

requirements-completed: [SOMM-03, GARD-01]

coverage:
  - id: D1
    description: "Chaque page de docs/ porte un unique H1 dont la valeur normalisee egale son libelle d'index du sommaire"
    requirement: "SOMM-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_h1_matches_sommaire_entry"
        status: pass
    human_judgment: false
  - id: D2
    description: "Chaque page de contenu porte une ligne de retour dont la cible resolue est docs/sommaire.md"
    requirement: "SOMM-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_pages_have_back_link"
        status: pass
    human_judgment: false
  - id: D3
    description: "Chaque page est decodable en UTF-8 strict, sans jeton de brouillon (TODO / A COMPLETER / Lorem) et d'au moins 300 caracteres"
    requirement: "GARD-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_documents_are_utf8_and_not_drafts"
        status: pass
    human_judgment: false
  - id: D4
    description: "Deux entrees d'index de docs/sommaire.md ne portent pas le meme libelle normalise et le sommaire ne se liste pas lui-meme"
    requirement: "SOMM-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_sommaire_index_labels_are_unique"
        status: pass
    human_judgment: false
  - id: D5
    description: "Le comportement de normalisation de D-11 est lui-meme teste : accents et casse, entite HTML et apostrophe droite, espaces multiples, fins de ligne CRLF et LF"
    requirement: "GARD-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_normalisation_insensible_aux_accents_et_casse"
        status: pass
    human_judgment: false
  - id: D6
    description: "Une derive injectee dans une copie de travail de docs/ (lien mort, page non listee, H1 divergent) est detectee avec un message nommant la cible injectee, l'arbre livre restant sain"
    requirement: "GARD-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_mutation_detecte_les_trois_derives"
        status: pass
    human_judgment: false

# Metrics
duration: 3min
completed: 2026-09-11
status: complete
---

# Phase 1 Plan 03 : gabarit de page verifie et preuve que le harnais mord

**`tests/test_docs_structure.py` passe a 14 tests : H1 unique egal au libelle d'index, ligne de retour resolue vers `sommaire.md`, UTF-8 strict sans jeton de brouillon, libelles d'index uniques et normalisation elle-meme testee, plus un test de mutation qui injecte les trois derives du critere de succes 5 dans une copie `tmp_path/docs` et exige que chacune soit nommee — suite complete 150 passed, `docs/` et `.data/dofus.sqlite3` inchanges.**

## Performance

- **Duration:** 3 min (10:31:30Z -> 10:34:16Z)
- **Started:** 2026-09-11T10:31:30Z (tete du plan precedent, `80b0550`)
- **Completed:** 2026-09-11T10:34:16Z
- **Tasks:** 2/2
- **Files modified:** 1 (0 cree, 1 modifie)

## Accomplishments

- **Gabarit de page garde automatiquement (SOMM-03).** `problemes_h1(docs_dir, normalize)` exige exactement un H1 par page de contenu et compare sa valeur normalisee au libelle de la ligne d'index du sommaire ; `problemes_retour_sommaire(docs_dir)` exige au moins un lien dont la **cible resolue** est `sommaire.md`. Le sommaire lui-meme est exclu des deux : il ne se renvoie pas a lui-meme (definition d'ensemble inchangee depuis 01-01).
- **Encodage et redaction verifies (GARD-01).** `problemes_encodage(docs_dir, normalize)` decode chaque page en UTF-8 strict, refuse les jetons de brouillon `TODO`, `A COMPLETER` et `Lorem` compares sur le texte **normalise** (donc insensibles a la casse et aux accents), et impose au moins `LONGUEUR_MINIMALE = 300` caracteres. Les deux pages livrees passent : `installation.md` (141 lignes) et `sommaire.md` (19 lignes, 382 caracteres).
- **Libelles d'index non ambigus (SOMM-02).** `test_sommaire_index_labels_are_unique` interdit deux entrees portant le meme libelle normalise — l'entree `[Installation](installation.md)` reste unique — et interdit au sommaire de se lister lui-meme comme cible.
- **La normalisation de D-11 est testee, pas seulement utilisee (D-12).** `test_normalisation_insensible_aux_accents_et_casse` prouve les quatre equivalences exigees : `Éléments` ≡ `elements`, `l&#39;objet` ≡ `l'objet`, `A  <tab> B` ≡ `A B`, `a<CRLF>b` ≡ `a<LF>b`. Quatre assertions, quatre messages citant la reference (`tests/conftest.py::_normalize`).
- **Le harnais mord, et le prouve (critere de succes 5).** `test_mutation_detecte_les_trois_derives` copie `docs/` sous `tmp_path` (`shutil.copytree`), verifie d'abord que l'arbre livre est sain sur trois invariants, puis injecte les trois derives **dans la copie seule** : lien mort `sommaire.mrd`, page `glossaire.md` absente de l'index, H1 `# Installation provisoire`. Chaque assertion exige que le message de l'invariant contienne la cible injectee — un test qui se contenterait de « quelque chose a echoue » ne prouverait rien.
- **Prouve que rien n'est ecrit dans l'arbre livre (T-01-07).** Dans le meme corps de test, `docs/installation.md` reel est relu apres les mutations : la ligne `(sommaire.md)` et le H1 `# Installation` en tete sont toujours la, et `docs/glossaire.md` n'existe pas. Mesure independante apres la suite : `docs/` ne contient que `installation.md` et `sommaire.md` ; `.data/dofus.sqlite3` garde son horodatage (`1788730056`) et sa taille (24 989 696 octets).
- **Aucune dependance, aucun import du produit.** Le module n'importe que `re`, `shutil` et `pathlib.Path` ; aucune socket, aucune base, aucun `main()` (D-15, T-01-08) ; toutes les lectures passent par `encoding="utf-8"` explicite.
- **Non-regression mesuree.** Suite complete : **150 passed** (144 existants + 6 nouveaux), soit 14 tests dans le module de structure ; aucune suppression de ligne, aucune reecriture de fin de ligne dans le diff.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : H1 egal au libelle d'index, ligne de retour, encodage et normalisation testee** - `8e29a4e` (test) — 211 insertions, 0 suppression
2. **Tache 2 : preuve de detection des trois derives (critere de succes 5)** - `c931419` (test) — 73 insertions, 0 suppression

**Plan metadata:** commit `docs(01-03): complete ...` (ce SUMMARY.md + STATE.md + ROADMAP.md + REQUIREMENTS.md), cree immediatement apres ce fichier.

_Note : chaque commit nomme son seul chemin (`git show --name-only` ne montre que `tests/test_docs_structure.py`) ; `git diff --diff-filter=D` est vide sur les deux commits._

## Files Created/Modified

- `tests/test_docs_structure.py` (290 -> 574 lignes) — trois constantes (`LIEN_LIBELLE`, `JETONS_BROUILLON`, `LONGUEUR_MINIMALE`), helper prive `_lire_page`, quatre helpers purs (`pages_listees`, `problemes_h1`, `problemes_retour_sommaire`, `problemes_encodage`), cinq tests de gabarit (`test_h1_matches_sommaire_entry`, `test_pages_have_back_link`, `test_documents_are_utf8_and_not_drafts`, `test_sommaire_index_labels_are_unique`, `test_normalisation_insensible_aux_accents_et_casse`) et le test de mutation `test_mutation_detecte_les_trois_derives` ; import `shutil` ajoute en tete.

## Decisions Made

- **Etat sain verifie avant toute injection.** Le test de mutation commence par exiger `problemes_liens(docs_dir) == []`, `problemes_index(docs_dir) == []` et `problemes_h1(docs_dir, normalize) == []` avec un message explicite. Sans cette etape, une derive preexistante rendrait la detection indiscernable d'un etat deja faux.
- **Chaque derive est nommee, pas seulement comptee.** Les trois assertions finales sont des `any("<cible injectee>" in probleme for probleme in problemes)` : elles echouent si l'invariant renvoie une liste vide **ou** une liste qui ne parle pas de la derive injectee (Pitfall 9 de la recherche, exigence du plan).
- **Une seule definition de l'ensemble d'index.** `pages_listees` relit les couples (libelle, cible) du sommaire avec un motif a deux groupes ; `problemes_index` de 01-01 continue d'utiliser `LINK` sur la meme source. Aucune liste blanche, aucune seconde definition (SOMM-02, D-06).
- **Helper de lecture tolerant.** `_lire_page` renvoie `None` sur `UnicodeDecodeError` : un fichier non UTF-8 devient un probleme localisant (page + attendu + reference) au lieu d'une exception qui interromprait l'invariant et violerait D-13.
- **Longueur minimale mesuree sur le texte brut.** `len(texte.strip())` (et non le texte normalise) : la constante represente une quantite de contenu livree ; `sommaire.md` la franchit (382 caracteres) sans marge artificielle.
- **Derive (c) ciblee par `count=1`.** `"# Installation"` est aussi une sous-chaine de `"## Installation"` ; remplacer la seule premiere occurrence isole le H1 et evite de renommer une section au passage.
- **Aucune decision produit nouvelle.** Le contenu des pages, la definition d'ensemble d'index et la forme de la ligne de retour viennent de 01-01/01-02 ; ce plan n'ajoute que le controle.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] La fixture `normalize` ajoutee a la signature de `test_sommaire_index_labels_are_unique`**
- **Found during:** Tache 1 (libelles d'index uniques)
- **Issue:** le plan nomme `test_sommaire_index_labels_are_unique(docs_dir)` sans parametre `normalize`, tout en exigeant que deux entrees ne portent pas le meme libelle **normalise**. Or D-12 interdit de redefinir la normalisation dans le module de test : sans la fixture, la comparaison serait textuelle et l'exigence ne serait pas tenue (deux libelles differant par la casse ou une entite HTML passeraient).
- **Fix:** la fixture `normalize` de `tests/conftest.py` est ajoutee en parametre du test ; aucune normalisation locale n'est ecrite, `_normalize` reste l'unique implementation.
- **Files modified:** `tests/test_docs_structure.py`
- **Verification:** `pytest tests/test_docs_structure.py -q` -> 14 passed ; l'assertion compare `normalize(libelle)` entre entrees et le message d'echec cite les deux libelles en clair
- **Committed in:** `8e29a4e` (Tache 1)

**2. [Rule 3 - Blocking] Fins de ligne du fichier passees en LF par l'outil d'edition**
- **Found during:** Tache 2 (ajout du test de mutation)
- **Issue:** l'edition de `tests/test_docs_structure.py` a reecrit le fichier entier en LF alors que le depot le suit en CRLF (defaut deja rencontre par 01-01 et 01-02) ; laisser l'etat ainsi aurait produit un diff non representatif de 574 lignes.
- **Fix:** normalisation explicite du fichier complet en bytes avant commit (`\r\n` -> `\n` -> `\r\n`), sans toucher au contenu.
- **Files modified:** `tests/test_docs_structure.py`
- **Verification:** `wc -l` = 574 et `grep -c $'\r$'` = 574 ; `git diff --numstat` des deux taches : `211 0` et `73 0` (aucune suppression, aucune reecriture integrale)
- **Committed in:** `8e29a4e` (Tache 1, apres chaque edition) et `c931419` (Tache 2)

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Aucun ecart de perimetre, aucune decision produit : les deux correctifs portent sur la conformite a une exigence du plan (comparaison normalisee de D-11) et sur la nettete du diff. Le seul chemin livre est exactement celui du `files_modified` du plan (`tests/test_docs_structure.py`) — aucune page, aucun fichier de `dofus_stuff/**`, aucune entree de sommaire.

## Issues Encountered

- **En-tete de branche `main` (meme situation que 01-01 et 01-02).** L'orchestrateur a dispatche cet executant comme **sequentiel sur l'arbre principal** (`git.branching_strategy: "none"`, historique de la phase integralement sur `main`) ; les deux commits y sont donc poses, conformement a la consigne de dispatch. Aucun `update-ref`, aucun `push`, aucun reset destructeur, aucun `git clean` ni `git stash`.
- **Controle de morsure des nouveaux invariants execute hors depot.** Avant le commit de la tache 1, les quatre helpers ont ete confrontes a des copies jetables (`tempfile.mkdtemp()`, supprimees apres mesure) : ligne de retour retiree -> `documentation.md` nomme avec la cible resolue attendue ; fichier ecrit en cp1252 -> « fichier non decodable en UTF-8 strict » ; jeton `A COMPLETER` et `Lorem` -> deux problemes nommant le jeton normalise ; page de 21 caracteres -> probleme nommant la longueur et le seuil. L'arbre livre est reste sain et `docs/` inchange sur les six mesures.
- **Aucun test ignore, aucune verification non jouee.** Les deux commandes `<automated>` de chaque tache ont ete executees avec l'interpreteur epingle `./.venv/Scripts/python.exe` (jamais `python -m pytest`, l'interpreteur ambiant n'a pas pytest) ; le test de mutation a ete rejoue seul, puis dans la suite complete.
- **Fichiers non suivis preexistants laisses intacts** : `.doc-agent/`, `.gsd/`, `doc-agent.toml`, `gsd-auto.toml`, `gsd-auto-rules.toml`, `.planning/milestone.lock`, `.planning/state.json`, ainsi que la modification preexistante de `.gitignore`. Aucun `git add .` : chaque commit nomme son chemin.
- **Branche protegee et hooks.** Les commits sont passes par les hooks normaux (aucun `--no-verify`) ; aucune suppression de fichier suivi n'a ete detectee sur les deux commits.

## Known Stubs

Aucun. Le module ne porte aucune valeur codee en dur issue d'un run : les seuils (`300` caracteres, trois jetons de brouillon) sont des constantes nommees et intentionnelles, les pages sont lues sur disque, et aucune donnee fictive n'alimente une assertion. Le seul nombre « en dur » du plan qui aurait pu devenir un stub — la liste des pages attendues — n'existe pas : l'ensemble d'index reste derive du sommaire, donc il grandira avec les phases 2 a 6 sans modification de ce module.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Pret pour le plan 01-04** : le module de structure est clos (`tests/test_docs_structure.py`, 14 tests) et n'a plus besoin d'etre touche ; `tests/test_docs_code_anchor.py` peut ancrer les options d'entree web, l'adresse par defaut, les commandes `fetcher.py` des blocs de code et les chemins du bloc « Source de verite » de `docs/installation.md` sans dependre de ce plan.
- **Pret pour les phases 2 a 6** : toute page ajoutee sous `docs/` qui manque d'entree d'index, de H1 divergent, de ligne de retour, de brouillon ou trop courte est refusee par un invariant deja en place ; `pages_listees` et `problemes_h1` donnent le point d'accroche pour les libelles d'index des pages suivantes.
- **Signal toujours discriminant** : `docs/sommaire.md` ne porte qu'une cible, donc l'egalite d'ensembles remaine un vrai signal ; le test de mutation ne depend que des trois derives qu'il exerce, pas d'un etat complet du somme des phases.
- **Point d'attention mesure** : l'`estimate` du plan (48 000 tokens) reste tres au-dessus de l'`actual` mesure sur le meme barème (3 072 tokens, soit 12 290 caracteres ajoutes). Comme aux plans 01-01 et 01-02, l'ecart suggere un estimate exprime a l'echelle du contexte du plan plutot qu'a celle du diff ; il est enregistre tel quel, sans arrondi, pour calibrer les prochains (ADR-2629).
- **Blocage** : aucun.

---
*Phase: 01-socle-documentaire-installation-et-harnais-v-rifiable*
*Completed: 2026-09-11*

## Self-Check: PASSED

- Fichier livre present sur disque : `tests/test_docs_structure.py` (574 lignes, 574 CRLF) et ce SUMMARY — verifies par `[ -f ]` et `wc -l`.
- Commits presents dans l'historique : `8e29a4e` (tache 1), `c931419` (tache 2) — verifies par `git log --oneline`.
- Criteres d'acceptation des deux taches rejoues apres commit : helpers niveau module (`pages_listees` l.314, `problemes_h1` l.325, `problemes_retour_sommaire` l.371, `problemes_encodage` l.406), aucun import de `dofus_stuff`, aucun `read_bytes` ni `read_text()` nu, `encoding="utf-8"` sur les huit lectures/ecritures — tous PASS.
- Verification de plan : `pytest tests/test_docs_structure.py -q` -> 14 passed ; `pytest tests/test_docs_structure.py::test_mutation_detecte_les_trois_derives -q` -> 1 passed ; `pytest -q` -> 150 passed (144 existants + 6 nouveaux, aucune regression) ; `.data/dofus.sqlite3` inchange (mtime 1788730056, 24 989 696 octets) ; `docs/` ne contient que `installation.md` et `sommaire.md` ; `git status --porcelain` ne montre aucun chemin de ce plan hors des deux commits.
- Mesure du registre de plan : `plan_head_before` = `80b0550f0c9e59ce0ffc4485399892747ff87e74`, `git rev-list --count 80b0550..HEAD` = 2 (le commit de metadonnees de ce SUMMARY est le +1 attendu par verify-work).
