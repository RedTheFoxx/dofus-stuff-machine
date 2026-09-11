---
phase: 02-r-f-rence-cli-align-e-sur-le-parseur
plan: 03
subsystem: tests
tags:
  [
    docs-fr,
    cli,
    exemples-verifies,
    shlex,
    argparse,
    ancrage-code,
    commande-destructrice,
    mutation,
    hors-ligne,
  ]

# Dependency graph
requires:
  - phase: 02-r-f-rence-cli-align-e-sur-le-parseur
    provides: "plan 02-01 : docs/cli.md (huit sous-commandes, quatre options globales, trente options d'optimize en tables thematiques, sections « ## db » et « ## cache », bloc « ## Source de verite ») avec ses huit exemples marques `console`"
  - phase: 02-r-f-rence-cli-align-e-sur-le-parseur
    provides: "plan 02-02 : tests/conftest.py (scanner de blocs unique _blocs_de_code conservant la balise d'ouverture, _lignes_de_code, _sections, _section(texte, titre, page) ou la page est obligatoire ; fixtures lignes_de_code, sections, section) et tests/test_docs_cli.py (listes epinglees de sondes et cinq tests page -> parseur)"
provides:
  - "tests/conftest.py : constante BALISE_EXEMPLE valant \"console\", helper _lignes_exemple(texte) et fixture de portee session lignes_exemple — projection marquee du scanner unique, sans second scanner de blocs (D-12, D-24)"
  - "tests/test_docs_cli.py : cinq tests de CLI-03 — exemples marques analysables (shlex.split puis build_parser().parse_args), couverture des huit sous-commandes par les exemples, forme « option globale avant sous-commande », garde de la commande destructrice (presence, co-presence sur la meme ligne, jamais un exemple) et propriete statique « aucun test n'execute rien » verifiee par ast"
  - "preuve de morsure : cinq mutations etiquetees pour la tache 1 et quatre pour la tache 2, toutes executees dans des copies jetables (`mktemp -d`), toutes detectees, avec le constat attribue verifie dans la sortie de pytest"
affects: [phase-03, phase-05, phase-06]

# Mesure #3968 — le registre de plan est sur disque, le compte n'est jamais narre.
plan_head_before: 802d0c51c31c5d3039aba3a041e998b51dbe09e8
commits: 2

# Actuals (#2632) — meme barème que l'estimate du plan (chars/4 du diff realise, pas un compteur de
# harnais). L'estimate du plan portait 44000 ; la mesure du diff realise est de 4565. L'ecart est
# reel et n'est pas arrondi : l'estimate comptait le travail d'agent (lectures, mesures du parseur,
# neuf mutations, verification du constat attribue), cette mesure-ci ne compte que les caracteres
# ajoutes au depot.
actuals:
  tokens: 4565
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Projection marquee = une vue de plus sur le scanner unique : `_lignes_exemple` filtre les blocs dont la balise d'ouverture vaut `BALISE_EXEMPLE`, `_blocs_de_code` n'est jamais reduplique (D-12, lecon WR-04)"
    - "La fixture partagee expose le *helper*, jamais les lignes d'une page : chaque test appelle `lignes_exemple(texte)` ; iterer la fixture elle-meme leve `TypeError: 'function' object is not iterable`, contrat ecrit dans sa docstring"
    - "Exemple = un bloc de code marque, jamais une commande citee en prose (D-24) ; l'analyse passe par `shlex.split` puis `build_parser().parse_args`, parseur public seul (D-25, D-14), sans jamais executer la commande"
    - "Quatre regles de redaction rappelees dans les messages d'echec, parce qu'elles sont invisibles au controle : commentaire en fin de ligne (code 2), continuation par antislash (`ValueError`), metacaractere de shell accepte mais non etendu, chemin Windows non guillemete avale par `shlex` sans que le parseur proteste"
    - "Regle textuelle evaluee sur le texte entier, ligne a ligne, jamais par section : l'entete de page echapperait a une regle evaluee par section (lecon WR-02)"
    - "Constats accumules et joints a *une seule* assertion des que deux regles portent sur la meme ligne : une assertion par constat rend inatteignable un motif attribue par le registre de mutation (T-02-14)"
    - "Forme attendue portee par une constante de module (`FORME_ATTENDUE`) et non par un litteral dans l'assertion : pytest imprime la source de l'assertion en echec, un litteral ferait croire a la detection"
    - "Propriete « le harnais n'execute rien » verifiee par `ast` et non par recherche de chaines : le module cite lui-meme les noms interdits, une recherche textuelle se detecterait elle-meme"

key-files:
  created: []
  modified:
    - tests/conftest.py
    - tests/test_docs_cli.py

key-decisions:
  - "Le nom de sous-commande d'un exemple est projete comme le premier jeton positionnel (options globales sautees, valeur des options a valeur sautee), puis compare aux huit noms epingles : le constat « atteinte sans etre documentee » reste ainsi atteignable au lieu d'etre structurellement vide"
  - "Le motif du jeton destructeur est une alternance `(db|cache)` suivie d'espaces puis de `clear`, delimitee sur les mots : il couvre `cache clear` autant que `db clear` (lecon WR-01), et la co-presence de l'avertissement est comparee sur la ligne normalisee (D-11)"
  - "Les trois constats de la garde destructrice sont joints a une seule assertion, mesure a l'appui : l'assertion par constat rapportait la mutation « mention destructrice glissee dans un bloc d'exemple » comme NON DETECTEE sur une page correcte, la co-presence levant avant le constat d'exemple"
  - "Tache 1 et tache 2 commitees separement : le module a ete reduit au perimetre de la tache 1 (constantes et tests de la garde retires), verifie vert a 8 tests, commite, puis la version finale restauree depuis une copie hors depot et commitee — la separation est reelle dans l'historique, pas seulement dans le message"

patterns-established:
  - "Un exemple de la page est prouve *analysable* : la ligne est extraite de la page, decoupee par `shlex.split` et soumise a `build_parser().parse_args` — parse, jamais execute"
  - "Chaque test de contenu porte une garde « non vide » (au moins un bloc marque, au moins un exemple portant l'ordre attendu) et chaque garde est prouvee mordante par une mutation etiquetee"
  - "Les limites non decidables mechaniquement sont ecrites dans le module de test lui-meme (D-26), pas seulement dans le plan"

requirements-completed: [CLI-03]

coverage:
  - id: D1
    description: "Chaque ligne des blocs marques `console` de docs/cli.md est decoupee par shlex.split puis acceptee par build_parser().parse_args ; un exemple fautif produit une assertion nommant la page, la ligne et dofus_stuff/cli.py"
    requirement: CLI-03
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_exemples_marques_sont_analysables"
        status: pass
      - kind: unit
        ref: "batterie de mutation 02-03 tache 1 (5/5 detectees, motifs attribues verifies)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Les sous-commandes atteintes par les exemples marques sont exactement les huit noms epingles, et un manque est nomme"
    requirement: CLI-03
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_chaque_sous_commande_a_un_exemple"
        status: pass
    human_judgment: false
  - id: D3
    description: "Au moins un exemple marque place l'option globale avant sa sous-commande (`python fetcher.py --offline optimize --demo`), enseignant l'ordre reel du parseur"
    requirement: CLI-03
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_exemple_hors_ligne_avec_option_globale_avant_sous_commande"
        status: pass
    human_judgment: false
  - id: D4
    description: "Toute ligne citant db clear ou cache clear porte l'avertissement destructeur sur la meme ligne, au moins une ligne les cite, et aucun exemple marque ne les cite"
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_commande_destructrice_avertie_et_jamais_dans_un_exemple"
        status: pass
      - kind: unit
        ref: "batterie de mutation 02-03 tache 2 (4/4 detectees)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Le module d'ancrage n'importe du produit que dofus_stuff.cli, n'importe ni subprocess, ni socket, ni sqlite3, n'appelle pas main et n'ouvre ni base ni connexion"
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_sans_execution_ni_base_locale"
        status: pass
      - kind: other
        ref: "horodatage de .data/dofus.sqlite3 inchange : 2026-09-06 23:27:36 +0200 avant et apres la suite complete"
        status: pass
    human_judgment: false

# Metrics
duration: ~5 min
completed: 2026-09-11
status: complete
---

# Phase 2 Plan 3: exemples marques analyses par le parseur, garde destructrice et ancrage sans execution Summary

**Les huit exemples de `docs/cli.md` sont prouves analysables par `shlex.split` + `build_parser().parse_args`, chaque sous-commande documentee a son exemple, `--offline` y precede `optimize`, la commande destructrice n'apparait que sur des lignes qui portent son avertissement et jamais dans un bloc d'exemple, et le module de test prouve par `ast` qu'il n'importe que le parseur et n'execute rien**

## Performance

- **Duration:** ~5 min (mesure : dispatch horodate `assignment-c2e5a3446dfb40fe9b2104e07e423a6e.json` a 14:28:16 +0200, dernier commit de tache a 14:33:08 +0200)
- **Started:** 2026-09-11T14:28:16+02:00
- **Completed:** 2026-09-11T14:33:08+02:00
- **Tasks:** 2 / 2
- **Files modified:** 2 (`tests/conftest.py`, `tests/test_docs_cli.py`)

## Accomplishments

- **CLI-03 est vrai et falsifiable.** Les huit exemples marques de la page sont extraits des seuls blocs `console` (D-24), decoupes par `shlex.split` puis acceptes par `build_parser().parse_args` (D-25) : un jeton d'option renomme fait rougir la suite, mesure par la mutation `--page` -> `--pages`.
- **L'ordre reel du parseur est enseigne, pas seulement decrit (critere 4a, D-27).** `python fetcher.py --offline optimize --demo` est exige par un test dedie ; inverser l'ordre fait rougir ce test *et* l'analyse par le parseur.
- **Le critere 4b est couvert par trois constats sur le texte entier de la page, ligne a ligne** : presence de la commande destructrice (`infalsifiable` si la page la retirait), co-presence de l'avertissement sur chacune de ses lignes (D-11/D-22), absence dans tout exemple marque (« commande a recopier »). Les lecons WR-01 (motif `(db|cache) clear`, pas seulement `db clear`) et WR-02 (perimetre = texte entier, jamais une section) sont appliquees.
- **Le critere 5 est prouve sur le module lui-meme.** `test_sans_execution_ni_base_locale` analyse l'arbre `ast` du module : seul `dofus_stuff.cli` est importe du produit, `subprocess` / `socket` / `sqlite3` sont absents, aucun appel a `main`, et l'import de `build_parser` est bien present.
- **Les limites honnetes de D-26 sont dans le module**, pas seulement dans le plan : la ligne etant extraite de la page, l'exigence « verbatim » est une garantie de construction ; la completude parser -> page n'est pas revendiquee ; « hors parcours recommande » n'est pas decidable mecaniquement et n'est approche que par la co-presence et l'absence en exemple.
- **Neuf preuves de morsure, aucune sur l'arbre livre.** Les mutations vivent dans des copies jetables (`mktemp -d` avec `docs/` et `tests/`) ; `.data/dofus.sqlite3` garde son horodatage d'origine et `docs/` du depot est bit a bit celui de 02-01.

## Task Commits

Chaque tache a ete commitee atomiquement :

1. **Tache 1 : exemples marques analysables, couverture par sous-commande, ordre global avant sous-commande** - `d7b1999` (test)
2. **Tache 2 : garde de la commande destructrice et propriete statique sans execution** - `95580b0` (test)

**Plan metadata:** le present commit (docs: complete plan)

## Files Created/Modified

- `tests/conftest.py` (261 lignes) - constante `BALISE_EXEMPLE` valant `console`, helper `_lignes_exemple(texte)` (lignes non vides, bords rognes, des seuls blocs dont la balise d'ouverture est `console`) et fixture de portee session `lignes_exemple` qui **expose le helper**. `_blocs_de_code` et `_lignes_de_code` sont inchanges : aucune seconde implementation du scanner (D-12).
- `tests/test_docs_cli.py` (746 lignes) - constantes `FORME_ATTENDUE`, `OPTIONS_GLOBALES_A_VALEUR`, `JETON_DESTRUCTEUR`, `JETON_AVERTISSEMENT`, `INTERDITS_EXECUTION`, `IMPORT_PRODUIT_AUTORISE` ; helpers `_jetons`, `_exemple_accepte`, `_sous_commande_atteinte` ; tests `test_exemples_marques_sont_analysables`, `test_chaque_sous_commande_a_un_exemple`, `test_exemple_hors_ligne_avec_option_globale_avant_sous_commande`, `test_commande_destructrice_avertie_et_jamais_dans_un_exemple`, `test_sans_execution_ni_base_locale` ; commentaires de limite (D-26) et de separation « analyse, jamais execute ».

## Verification

- `./.venv/Scripts/python.exe -m pytest tests/test_docs_cli.py -q` : **10 passed** (5 tests de 02-02 + 5 de ce plan).
- `./.venv/Scripts/python.exe -m pytest -q` (suite complete, reference re-mesuree au moment ou elle est citee, Pitfall 17) : **168 passed** — 163 avant ce plan, soit exactement les 5 tests ajoutes.
- `git status --porcelain -- docs tests` : vide apres les deux commits ; `git status --porcelain -- dofus_stuff README.md GUIDE_WIZARD.md .data` : vide.
- Horodatage de `.data/dofus.sqlite3` : `2026-09-06 23:27:36 +0200` avant et apres la suite complete — aucun test n'ouvre la base locale, n'ecrit sous `.data/`, ni n'ouvre de connexion (D-15).
- Encodage et fins de ligne : `tests/conftest.py` et `tests/test_docs_cli.py` en UTF-8 strict sans BOM, integralement CRLF (0 ligne en LF seul), convention des fichiers `tests/`.

## Mutation Battery

Les neuf batteries sont lancees par la fonction `MUT` du `<verify>` du plan, telles qu'ecrites (copie jetable de `docs/` et `tests/`, mutation par `sed -i` ou `printf`, puis `pytest tests/test_docs_cli.py -q` sur la copie). Un verdict est rendu « mutation detectee » seulement si la sortie contient a la fois un compteur `N failed`, une ligne `AssertionError: ...cli.md` et le motif attribue.

### Tache 1 (5 mutations)

| Mutation | Motif cherche | Verdict | Compteur | Constat attribue verifie dans la sortie |
|----------|---------------|---------|----------|------------------------------------------|
| blocs d'exemple renommes (marqueur `console` retire) | `aucun bloc marque` | detectee | 4 failed | `aucun bloc marque` (garde non vide du test 1) |
| jeton d'option renomme dans un exemple (`--page` -> `--pages`) | `--pages` | detectee | 2 failed | `refuse par` + la ligne fautive `... list --pages 2` |
| guillemet non ferme dans un exemple (`search "Atcham`) | `guillemet` | detectee | 4 failed | `non decoupable par shlex.split` |
| seul exemple d'une sous-commande supprime (`list`) | `sans exemple` | detectee | 2 failed | `sans exemple` (constat de couverture) |
| ordre global/sous-commande inverse dans le seul temoin | `--offline optimize` | detectee | 3 failed | `ne porte la forme` (constat d'ordre) |

### Tache 2 (4 mutations)

| Mutation | Motif cherche | Verdict | Compteur | Constat attribue verifie dans la sortie |
|----------|---------------|---------|----------|------------------------------------------|
| avertissement destructeur retire de la ligne qui cite la commande | `destruct` | detectee | 2 failed | `sans l'avertissement attendu` (constat de co-presence) |
| mention destructrice glissee dans un bloc d'exemple | `recopier` | detectee | 2 failed | `commande a recopier` (constat d'exemple) |
| mention destructrice supprimee de la page entiere | `infalsifiable` | detectee | 2 failed | `infalsifiable` (garde de presence) |
| import de `dofus_stuff.database` injecte dans la copie du module de test | `dofus_stuff.database` | detectee | 2 failed | `hors du parseur public` (constat ast) |

**9 verdicts sur 9, aucun « MUTATION NON DETECTEE ».**

### Controle de discrimination des neuf motifs (mesure ajoutee)

Le registre de mutation du plan couvre la phase entiere ; il avertit aussi que les copies jetables sont rouges **par construction** sur le controle d'existence des chemins de 02-02 (l'arbre produit n'est pas copie, le message nomme `fetcher.py` et `dofus_stuff/cli.py`). Un motif attribue pourrait donc etre satisfait sans mutation, comme l'a mesure 02-02 sur `build_parser`. Controle re-mesure ici sur une copie **non mutee** : `1 failed, 9 passed` — et **0 occurrence** de chacun des neuf motifs (`aucun bloc marque`, `--pages`, `guillemet`, `sans exemple`, `--offline optimize`, `infalsifiable`, `destruct`, `recopier`, `dofus_stuff.database`). Les neuf verdicts sont donc des verdicts sur leur mutation, pas des artefacts de la rougeur parasitaire.

Deux mesures d'attribution vont plus loin que le motif seul, parce que ces motifs apparaissent aussi dans le nom du test en echec (ligne `FAILED ...`) :

- mutation « avertissement retire » -> la sortie contient `sans l'avertissement attendu`, phrase presente uniquement dans le constat de co-presence ;
- mutation « mention destructrice glissee dans un bloc d'exemple » -> la sortie contient `commande a recopier`, phrase presente uniquement dans le constat d'exemple (l'assertion imprimee porte, elle, « garde de la commande destructrice »).

## Assertions declarees non falsifiables (registre du plan, reprises ici)

| Assertion | Raison mesuree |
|-----------|----------------|
| Presence verbatim de la ligne dans la page (test 1b) | La ligne est *extraite* de la page : l'assertion est une garantie de construction, tautologique par nature (D-26). Ecrit tel quel dans le module. |
| « Hors parcours recommande » (seconde moitie du critere 4b) | Non decidable mecaniquement : approche par la co-presence sur la meme ligne et par l'absence dans tout bloc marque ; la limite est ecrite dans le module. |
| Le caractere « destructeur » de `db clear` / `cache clear` | Aucun attribut du parseur ne declare cette propriete : classement humain derive de `dofus_stuff/database.py` (`Database.clear` supprime `items` et `meta` sans confirmation). La mutation de co-presence prouve que le classement retenu est applique, pas qu'il est complet. |
| « La suite est verte » (critere de succession 5) | Condition d'execution, falsifiable seulement par une regression du produit ; sa partie falsifiable est l'assertion statique `ast` et l'horodatage inchange de `.data/dofus.sqlite3`, tous deux consignes ci-dessus. |

## Decisions Made

- **Projection du nom de sous-commande par premier jeton positionnel.** Le plan decrivait « retenir le premier jeton appartenant a l'ensemble des huit noms epingles » ; le helper `_sous_commande_atteinte` projette ce premier jeton puis la comparaison aux huit noms produit les deux constats (manquante / atteinte sans etre documentee). Sur la page livree le resultat est identique, mais le second constat reste atteignable au lieu d'etre structurellement vide — une branche morte serait infalsifiable (T-02-14).
- **Une seule assertion pour la garde destructrice**, avec le motif de la page insere *avant* la phrase d'avertissement attendue. Mesure a l'appui : avec une assertion par constat, la mutation « mention destructrice glissee dans un bloc d'exemple » etait rapportee `MUTATION NON DETECTEE` alors que la page reste correcte ; la co-presence levait avant le constat d'exemple et le motif `recopier` n'etait jamais atteint.
- **`FORME_ATTENDUE` portee par une constante de module**, jamais un litteral dans le corps du test : pytest imprime la source de l'assertion en echec, un litteral ferait croire a la detection meme si le message ne portait pas la forme attendue.
- **Regles destructrice et d'exemple evaluees sur le texte entier**, ligne a ligne ; seules les tables d'options de 02-02 utilisent un perimetre de section. L'entete de page echapperait a une regle evaluee par section (lecon WR-02).

## Deviations from Plan

### Auto-fixed Issues

**1. [Regle 2 - Fonctionnalite critique manquante] Le constat « atteinte sans etre documentee » etait structurellement inatteignable**
- **Found during :** tache 1 (test de couverture par sous-commande)
- **Issue :** la lettre du plan filtrait les jetons des exemples par l'ensemble des huit noms epingles, puis exigeait l'egalite avec ce meme ensemble : la partie « atteinte sans etre documentee » du message ne pouvait jamais etre produite par aucune page, ce qui en faisait une branche morte — donc une assertion sans preuve possible (T-02-14).
- **Fix :** `_sous_commande_atteinte(ligne)` projette le premier jeton positionnel de l'exemple (les options globales sont sautees, la valeur d'une option a valeur aussi, via `OPTIONS_GLOBALES_A_VALEUR`), et la comparaison a l'ensemble epingle produit les deux constats. Le contrat du plan est conserve : sur la page livree l'ensemble atteint est exactement les huit noms, et un manque est nomme « sans exemple ».
- **Files modified :** `tests/test_docs_cli.py`
- **Verification :** la mutation « seul exemple d'une sous-commande supprime (`list`) » fait rougir le test avec le constat `sans exemple` (batterie tache 1, 5/5) ; une page correcte reste verte (168 passed).
- **Committed in :** `d7b1999` (commit de la tache 1)

**Total deviations :** 1 auto-documentee (regle 2). Aucun ecart de regle 1 (bogue), de regle 3 (blocage) ni de regle 4 (decision d'architecture) : aucune dependance installee, aucun paquet ajoute, aucune modification de `dofus_stuff/**`, de `docs/**`, de `README.md`, de `GUIDE_WIZARD.md` ni de `.data/`.

**Impact on plan :** aucun elargissement de perimetre, aucune assertion affaiblie. L'ecart renforce au contraire la propriete de Nyquist : la seule branche qui aurait pu rester sans preuve est devenue un constat atteignable, et l'affaiblissement inverse (garder une branche morte) aurait laisse une assertion non prouvable.

## Issues Encountered

- **En-tete de branche `main` (meme situation que 01-01 a 01-04, 02-01 et 02-02).** Le protocole d'execution interdit par defaut de committer sur la branche protegee : `git.base-branch --is-protected main` renvoie `true` et `.planning/config.json` ne porte pas d'override `git.allow_default_branch_commits`, alors qu'il porte `git.branching_strategy: "none"` et que l'historique des deux phases est integralement sur `main`. L'orchestrateur a dispatche cet executant comme **sequentiel sur l'arbre principal** : les deux commits y sont donc poses, conformement a la consigne de dispatch. Aucun `update-ref`, aucun `push`, aucun reset destructeur, aucun `git clean`, aucun `git stash`.
- **Deux taches dans un meme fichier, deux commits distincts.** Le chemin le plus simple (un seul commit pour les deux taches) aurait viole la contrainte « une tache, un commit ». Le module a donc ete reduit au perimetre de la tache 1 (import `ast`, constantes `JETON_DESTRUCTEUR` / `JETON_AVERTISSEMENT` / `INTERDITS_EXECUTION` / `IMPORT_PRODUIT_AUTORISE`, tests 4 et 5 et les deux phrases de commentaire qui les annoncent retires), verifie vert (**8 passed**), commite, puis la version finale restauree depuis une copie **hors depot** (`%TEMP%\02-03-final-test_docs_cli.py`, jamais dans l'arbre suivi) et commitee. Le commit 2 ne porte aucune suppression : `git diff --diff-filter=D --name-only HEAD~1 HEAD` du commit 1 est vide, et le commit 2 est fait de 149 insertions et 3 remplacements (l'en-tete et la limite D-26 completes par la tache 2).
- **Fins de ligne CRLF.** Les outils d'edition ecrivent en LF ; les deux fichiers ont ete re-normalises en CRLF apres chaque modification, et le controle final (`git diff` sur 0 ligne de LF seul) confirme que les diff ne portent que des lignes reelles, pas un basculement d'encodage.
- **`/tmp` de Git Bash n'est pas `/tmp` pour l'interpreteur natif.** La copie de sauvegarde a du etre adressee par son chemin Windows (`C:\Users\Red\AppData\Local\Temp\...`) ; la premiere tentative a echoue avant toute ecriture, sans effet sur l'arbre de travail.
- **Aucune base ouverte, aucun reseau.** `.data/dofus.sqlite3` porte toujours son horodatage d'origine (`2026-09-06 23:27:36 +0200`) : aucun test de ce plan n'ouvre la base locale ni ne contacte l'API, et aucune commande destructive n'a ete *executee* — `db clear` et `cache clear` ne sont que cites par la page et analyses par le parseur.

## Known Stubs

Aucun. Les cinq tests portent des assertions reelles (aucune valeur codee en dur laissee « pour plus tard », aucun `skip`, aucun `TODO`) ; les sondes s'appuient sur les listes epinglees mesurees de 02-02. Les quatre assertions que le registre du plan declare **non falsifiables** sont declarees avec leur raison mesuree, ici et dans le module : presence verbatim de la ligne (tautologique par construction), « hors parcours recommande » (non decidable), caractere destructeur de `db clear` / `cache clear` (classement humain derive du code), « la suite est verte » (condition d'execution, approchee par l'assertion `ast` et l'horodatage de `.data/`). Aucun stub n'a ete ajoute a `.planning/WINDOWS.md`.

## Threat Flags

Aucune surface nouvelle par rapport au modele de menaces du plan. Les mitigations du registre STRIDE sont appliquees comme ecrites :

- **T-02-11 (perte de la base locale, high)** — trois constats sur le texte entier : la page doit citer la commande (sinon la regle est vide, donc infalsifiable), chaque ligne qui la cite porte l'avertissement sur la meme ligne, et aucun bloc marque ne la contient. Motif `(db|cache) clear` avec espaces quelconques.
- **T-02-12 (exemple faux, controle aveugle, high)** — chaque exemple passe par `shlex.split` puis `build_parser().parse_args`, et les quatre regles de redaction mesurees sont rappelees dans les messages d'echec, `shlex` avalant silencieusement un chemin Windows non guillemete que le parseur accepte.
- **T-02-13 (execution non voulue par le harnais, high)** — `test_sans_execution_ni_base_locale` verifie par `ast` l'absence d'import de `subprocess`, `socket`, `sqlite3` et de tout module du produit hors `dofus_stuff.cli`, ainsi que l'absence d'appel a `main`.
- **T-02-14 (regle infalsifiable, medium)** — chaque test de ce plan porte sa garde non vide (au moins un bloc marque, au moins un exemple par sous-commande, au moins une ligne citant la commande destructrice, au moins un exemple portant l'ordre attendu), et les neuf mutations etiquetees des deux batteries sont toutes detectees, avec controle de discrimination des neuf motifs sur une copie non mutee.
- **T-02-15 (quota Dofusdude, medium)** — aucun exemple marque ne contient `db sync` ni `cache fill` : les commandes qui exigent le reseau ne sont jamais des exemples a recopier.
- **T-02-SC** — aucune installation : le module n'ajoute que `ast` et `shlex` de la bibliotheque standard, plus `pytest` deja present dans `.venv`.

## User Setup Required

None - aucune configuration externe, aucun service, aucune variable d'environnement.

## Next Phase Readiness

Le module d'ancrage CLI est clos pour la phase 2, et la suite complete est verte (**168 passed** avec `.venv/Scripts/python.exe`). Ce que la phase suivante trouve sur disque :

- **CLI-03 prouve dans les deux directions utiles** : page -> parseur (exemples analysables, sous-commandes atteintes, ordre des options) et propriete du harnais (aucune execution, aucune base, aucune socket). La completude parser -> page reste volontairement non revendiquee (D-26), ecrit dans le module.
- **Les helpers partages sont complets** : `tests/conftest.py` porte desormais le scanner unique, les helpers de section et les deux projections de blocs (`lignes_de_code`, `lignes_exemple`), chacun expose par une fixture de portee session — aucun module de test ne redefinit un scanner.
- **Les dix contrats de `tests/test_docs_cli.py`** couvrent CLI-01, CLI-02 et CLI-03 ; `02-VALIDATION.md` peut pointer sur les tableaux de mutation de `02-02-SUMMARY.md` et de ce resume sans reconstituer la couverture de son cote.
- **Aucune modification de `dofus_stuff/**`, de `docs/`, de `README.md`, de `GUIDE_WIZARD.md` ni de `.data/`.** `docs/` reste exactement ce que 02-01 a livre, et les neuf mutations n'ont touche que des copies jetables.

---

## Self-Check: PASSED

- `tests/test_docs_cli.py` : **FOUND** (746 lignes, 5 tests ajoutes, `test_commande_destructrice_avertie_et_jamais_dans_un_exemple` present, UTF-8 sans BOM, 100 % CRLF)
- `tests/conftest.py` : **FOUND** (261 lignes, `BALISE_EXEMPLE`, `_lignes_exemple`, fixture `lignes_exemple`, scanner unique conserve)
- Commit `d7b1999` : **FOUND** (tache 1 : `tests/conftest.py` + `tests/test_docs_cli.py`)
- Commit `95580b0` : **FOUND** (tache 2 : `tests/test_docs_cli.py`)
- `./.venv/Scripts/python.exe -m pytest -q` : **168 passed**
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_cli.py -q` : **10 passed**
- Batterie de mutations : **9 detectees / 9** ; discrimination des neuf motifs sur copie non mutee : **0 occurrence chacun**
- `git rev-list --count 802d0c5..HEAD` : **2** (compte mesure depuis le registre de plan, pas narre)
- `.data/dofus.sqlite3` : horodatage `2026-09-06 23:27:36 +0200` inchange

*Phase: 02-r-f-rence-cli-align-e-sur-le-parseur*
*Completed: 2026-09-11*
