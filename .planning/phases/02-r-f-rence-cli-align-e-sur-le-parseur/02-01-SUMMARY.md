---
phase: 02-r-f-rence-cli-align-e-sur-le-parseur
plan: 01
subsystem: docs
tags: [docs-fr, cli, argparse, ancrage-code, hors-ligne, utf8, sommaire, console-blocks]

# Dependency graph
requires:
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plan 01-02 : docs/installation.md, gabarit de page (H1 unique, phrase d'introduction, sections courtes, bloc « Source de vérité » accentue, ligne de retour vers le sommaire)"
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plan 01-03 : tests/test_docs_structure.py (14 tests) — problemes_liens, problemes_index, problemes_h1, problemes_retour_sommaire, problemes_encodage, pages_listees et le test de mutation"
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plan 01-01 : docs/sommaire.md (point d'entree unique, tableau Index) et tests/conftest.py (fixtures docs_dir et normalize)"
provides:
  - "docs/cli.md : H1 « CLI », phrase d'introduction, « ## Options globales » (tableau des quatre options globales avec role et defaut mesure, plus deux paragraphes adosses aux mesures M5 : code 2 pour db status --offline, code 1 pour --offline db sync)"
  - "docs/cli.md : une section par sous-commande dans l'ordre du parseur (version, self-test, search, item, list, optimize, db, cache), chacune avec son synopsis et un exemple marque dans un bloc ```console"
  - "docs/cli.md : les 30 options d'optimize en quatre tables thematiques (profil et objectifs, contraintes de selection, caracteristiques de base et scrolls, RNG et performances) avec leur defaut mesure ; les onze options sans help sont donnees par nom et defaut, sans semantique inventee (D-19)"
  - "docs/cli.md : section « ## db » (cinq sous-commandes en jetons nus, trois descriptions verbatim, stats/fill signales comme alias sans description dans l'aide), sous-section « ### `db clear`, commande destructrice », paragraphe sur db sync / cache fill, section « ## cache » declarant l'alias sans description dupliquee"
  - "docs/cli.md : bloc « ## Source de vérité » nommant build_parser() et quatre chemins existants, plus la ligne « [Retour au sommaire](sommaire.md) »"
  - "docs/sommaire.md : ligne d'index « | [CLI](cli.md) | Commandes, options et exemples de fetcher.py | » ajoutee au tableau Index"
affects: [02-02, 02-03, phase-03, phase-05, phase-06]

# Mesure #3968 — le registre de plan est sur disque, le compte n'est jamais narre.
plan_head_before: c5efa09a4e2f5e5c1f22e73734e760d0238e6a2a
commits: 3

# Actuals (#2632) — meme barème que l'estimate du plan (chars/4 du diff realise, pas un compteur de harnais).
# L'estimate du plan portait 52000 ; la mesure du diff realise est de 2362. L'ecart est docummente
# dans « Decisions Made » : l'estimate comptait le travail d'agent, cette mesure-ci ne compte que le
# diff livre. Le chiffre mesure n'est pas arrondi pour se rapprocher de l'estimate.
actuals:
  tokens: 2362
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Marqueur d'exemple : seule une ligne d'un bloc de code dont la balise d'ouverture est exactement « console » compte comme exemple a recopier (D-24) ; les sorties d'erreur citent le parseur dans des blocs « text », jamais « console »"
    - "Exemple marque = une seule ligne complete commencant par « python fetcher.py », sans prompt, sans commentaire de fin de ligne, sans continuation par antislash et sans metacaractere de shell (quatre formes mesurees M4 comme cassant shlex.split ou rendant le controle aveugle)"
    - "Defaut mesure plutot que recopie : chaque defaut du tableau vient d'un parse_args reel ; l'aide de --data-dir, qui imprime un chemin absolu propre au poste, est remplacee par « le dossier .data/ a la racine du depot » (A4, Pitfall 17)"
    - "Avertissement destructeur co-localise : toute ligne qui nomme db clear ou cache clear porte le mot « destruct* » sur la meme ligne, pour qu'un controle puisse exiger leur co-presence sans analyse semantique (D-22)"
    - "Ordre global-avant-sous-commande enseigne par un temoin unique : la ligne « python fetcher.py --offline optimize --demo » est le seul exemple marque portant la paire --offline puis optimize, l'assertion 4a de 02-03 restant ainsi observable (D-27)"

key-files:
  created:
    - docs/cli.md
  modified:
    - docs/sommaire.md

key-decisions:
  - "Forme de la page : « ## Options globales » suit immediatement la phrase d'introduction et precede « ## version ». C'est ce qui garantit que la mutation de 02-02 (« option inventee » inseree avant « ## version ») tombe bien dans le corps de la section des options globales, donc dans le perimetre de la garde non vide de _options_des_tables"
  - "« ## Source de vérité » est la derniere section de la page, apres « ## cache », juste avant la ligne de retour : la page garde ainsi le gabarit de docs/installation.md sans ajouter de titre de niveau 2 hors des dix prevus (Options globales, huit sous-commandes, Source de verite)"
  - "Le mode interactif est decrit en prose : « python fetcher.py --offline optimize » n'apparait dans aucun bloc « console ». Le temoin marque de l'ordre global-avant-sous-commande reste donc unique (02-01 tache 2) et la mutation d'ordre de 02-03 t1 garde son motif « --offline optimize »"
  - "Le tableau « ## db » porte les cinq jetons nus (status, stats, sync, fill, clear) et jamais la forme « db clear » : l'avertissement destructeur reste concentre sur les trois lignes qui doivent le porter (une ligne de titre, une ligne de corps, une ligne du bloc Source de verite), ce qui rend le controle de co-presence falsifiable et localise"
  - "Les trois descriptions verbatim de l'aide (« Afficher l'état de la base », « Forcer la synchronisation complète », « Vider la base locale ») sont citees une seule fois, dans « ## db », avec les apostrophes et accents exacts lus dans dofus_stuff/cli.py ; « ## cache » declare l'alias et renvoie a cette section, sans en reprendre aucune — la comparaison normalisee de 02-02 (D-20, D-11) reste donc verte sur les deux formes"
  - "« db sync » et « cache fill » sont decrits comme reecrivant la base et exigeant le reseau, avec l'incompatibilite mesuree avec --offline (code 1), et ne portent pas le jeton d'avertissement destructeur : classement A2 (dofus_stuff/database.py ne supprime rien d'autre que les donnees derivees de l'API, aucun stuff utilisateur n'est stocke en base)"
  - "La regle « toutes les commandes portent --offline » de docs/installation.md n'est pas reconduite : la page dit au contraire que les commandes de synchronisation sont les seules a ne pas s'employer hors-ligne. Un renvoi vers la page de la base locale est fait en prose, sans lien markdown, pour ne pas creer de cible morte tant que cette page n'existe pas (problemes_liens)"
  - "L'option --all de db clear n'est pas documentee et la chaine « --all » n'apparait nulle part ailleurs qu'a l'interieur des options --allow-* : le parseur l'accepte mais aucune ligne de code ne la lit, la documenter serait inventer une semantique (D-19, mesure M7)"
  - "Ecart assume avec .claude/CLAUDE.md §2 (DOCS-06), qui prescrit « un tableau commande -> role -> exemple » couvrant toutes les sous-commandes : la phase 2 est gouvernee par les decisions D-16 a D-18 de 02-CONTEXT.md, qui fixent une section par sous-commande avec ses propres tables d'options et interdisent la table recapitulative unique (D-17). La substance de DOCS-06 reste tenue section par section (chaque sous-commande a son role, ses options et son exemple) ; la forme en tableau unique serait un second referentiel a maintenir"
  - "Le fichier est ecrit par l'outil d'ecriture puis normalise en CRLF sans BOM dans le meme processus : les pages de docs/ sont en CRLF (mesure de la recherche), et le H1 comme les motifs de tableaux de 02-02/02-03 sont sensibles a cette convention"
  - "L'ecart entre l'estimate du plan (52000 jetons) et l'actuals mesure (2362) est reel et non arrondi : l'estimate portait sur le travail d'agent (lecture de la recherche, mesures, redaction), l'actuals ne compte que le diff livre, conformement au barème chars/4 demande"

patterns-established:
  - "Chaque commande enseignee est une ligne unique analysable par le parseur public, jamais un fragment ni une ligne de sortie : un bloc « console » ne contient donc que des commandes"
  - "Une sortie d'erreur du parseur est citee dans un bloc « text » : elle documente le comportement mesure sans devenir un exemple a recopier"
  - "L'aide du parseur qui imprime une valeur propre au poste (chemin absolu de --data-dir) est remplacee par sa description portable, la valeur absolue n'apparaissant jamais dans la page"

requirements-completed: [CLI-01, CLI-02, CLI-03]

coverage:
  - id: D1
    description: "La page docs/cli.md est livree avec son entree d'index « | [CLI](cli.md) | » dans docs/sommaire.md, meme unite de travail : exhaustivite bidirectionnelle, H1 egal au libelle d'index, ligne de retour vers le sommaire, encodage strict, longueur minimale et liens resolus"
    requirement: "CLI-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_h1_matches_sommaire_entry"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_sommaire_lists_every_document"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_pages_have_back_link"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_documents_are_utf8_and_not_drafts"
        status: pass
    human_judgment: false
  - id: D2
    description: "Le contenu de la page reflete la surface mesuree du parseur : huit sous-commandes dans l'ordre reel, quatre options globales avec defaut, trente options d'optimize en quatre tables thematiques avec defaut, un exemple marque par sous-commande, bloc Source de verite nommant build_parser()"
    requirement: "CLI-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_documents_are_utf8_and_not_drafts"
        status: pass
      - kind: other
        ref: "sonde locale (hors suite) : shlex.split sur les 8 lignes des blocs console, puis build_parser().parse_args ; 4 et 30 options extraites des lignes de tableau des sections Options globales et optimize, toutes acceptees par le parseur public"
        status: pass
    human_judgment: true
    rationale: "Les contrats d'ancrage page -> parseur de cette page sont livres par les plans 02-02 et 02-03 (tests/test_docs_cli.py, fixture lignes_exemple) : a la fin de ce plan, la justesse du contenu est mesuree par des sondes de plan et par les invariants structurels, pas encore par un test commite. La classification « destructeur » et la qualite « hors parcours recommande » figurent par ailleurs dans la table « Manual-Only Verifications » de 02-VALIDATION.md."
  - id: D3
    description: "La commande destructrice (db clear et son alias cache clear) est citee, chaque ligne qui la nomme porte l'avertissement sur la meme ligne, et aucun exemple marque ne la propose a la recopie"
    requirement: "CLI-03"
    verification:
      - kind: other
        ref: "grep -E '(db|cache) +clear' docs/cli.md (3 lignes) | grep -cv destruct (0 ligne sans avertissement) ; aucun bloc console ne cite clear, sync ni fill"
        status: pass
    human_judgment: true
    rationale: "Le test commite de co-presence et d'exclusion arrive avec 02-03 (test_commande_destructrice_avertie_et_jamais_dans_un_exemple). La seconde moitie du critere 4b — « jamais dans un parcours recommande » — est declaree non decidable mecaniquement dans 02-VALIDATION.md et reste une lecture humaine de la page."

# Metrics
duration: 3min
completed: 2026-09-11
status: complete
---

# Phase 2 Plan 01: Référence CLI alignée sur le parseur — page livrée avec son entrée d'index

**`docs/cli.md` livre la surface CLI mesurée (huit sous-commandes dans l'ordre du parseur, quatre options globales, trente options d'`optimize` en quatre tables thématiques, un exemple marqué par sous-commande, avertissement destructeur co-localisé) et son entrée d'index dans `docs/sommaire.md`, sans qu'aucune ligne de `dofus_stuff/**` ne soit touchée.**

## Performance

- **Duration:** 3 min
- **Started:** 2026-09-11T12:15:18Z
- **Completed:** 2026-09-11T12:18:23Z
- **Tasks:** 3 / 3
- **Files modified:** 2 (`docs/cli.md` créé, `docs/sommaire.md` une ligne ajoutée)

## Accomplishments

- **Tranchant de bout en bout prouvé avant toute largeur** : la page et son entrée d'index livrées ensemble (tâche 1) font passer `tests/test_docs_structure.py` au vert — `problemes_index`, `problemes_h1`, `problemes_retour_sommaire`, `problemes_encodage` et `problemes_liens` ne signalent rien. La phase 1 avait mesuré qu'une page sans entrée d'index produit deux problèmes nommés (Pitfall 15) : c'est exactement le mode d'échec évité ici.
- **Options documentées par la mesure, jamais par relecture** : les 4 options globales et les 30 options d'`optimize` viennent des mesures M2 et M2.3 de `02-RESEARCH.md`, avec leurs défauts réels (`--timeout` 15, `--limit` 10, `--page` 1, `--size` 5, `--top-k` 30, `--time-limit` 5.0, `--jet` `average`) ; les onze options sans `help` sont données par leur nom et leur défaut, sans sémantique inventée (D-19).
- **Deux pièges d'ordre réels documentés avec leur cause** : la forme fautive `db status --offline` (code 2, `fetcher.py: error: unrecognized arguments: --offline`) et l'incompatibilité `--offline` / synchronisation (code 1, `Erreur : --offline incompatible avec db sync`). La règle « toutes les commandes portent `--offline` » de la page d'installation n'est pas reconduite : elle serait mécaniquement fausse ici.
- **Commandes qui vident ou réécrivent la base traitées séparément** : `db clear` et `cache clear` portent leur avertissement sur chaque ligne qui les nomme et n'apparaissent dans aucun exemple marqué ; `db sync` et `cache fill` sont décrits comme réécrivant la base et exigeant le réseau, sans porter ce jeton (classement A2).
- **Alias `cache` sans description dupliquée** : les trois descriptions verbatim de l'aide sont citées une seule fois, dans `## db`, avec les apostrophes et accents exacts du parseur ; `## cache` déclare l'alias et renvoie à cette section.

## Task Commits

Chaque tâche a été commitée atomiquement :

1. **Tâche 1 (tranchant) : chaîne `docs/sommaire.md` -> `docs/cli.md` et invariants de phase 1 verts** - `8c96674` (docs)
2. **Tâche 2 : options globales et les 30 options d'`optimize` avec leurs défauts mesurés** - `d778063` (docs)
3. **Tâche 3 : alias `cache`, commandes qui réécrivent la base, avertissement destructeur** - `dcb65bc` (docs)

**Plan metadata:** voir le commit de complétion du plan (SUMMARY, STATE, ROADMAP, REQUIREMENTS, WINDOWS.md).

_Note : le plan n'a pas de tâche `tdd`, donc un commit par tâche._

## Files Created/Modified

- `docs/cli.md` (créé, 195 lignes, CRLF, UTF-8 strict sans BOM) — H1 `# CLI`, phrase d'introduction, `## Options globales` (tableau des quatre options + les deux paragraphes d'ordre et d'incompatibilité), `## version`, `## self-test`, `## search`, `## item`, `## list`, `## optimize` (quatre sous-titres de tables), `## db` (tableau des cinq sous-commandes, sous-section destructrice, paragraphe de synchronisation), `## cache`, `## Source de vérité`, ligne de retour.
- `docs/sommaire.md` (modifié, +1 ligne) — ligne d'index `| [CLI](cli.md) | Commandes, options et exemples de fetcher.py |` ajoutée au tableau `## Index`, à la suite de la ligne d'installation. Le parcours conseillé en texte numéroté est inchangé (ce n'est pas un lien, aucun invariant ne le voit).

## Decisions Made

- **Forme et ordre des sections.** `## Options globales` suit immédiatement l'introduction et précède `## version` ; `## Source de vérité` est la dernière section, après `## cache`. La première position est ce qui fait tomber la mutation « option inventée » de 02-02 dans le corps de la section des options globales (donc dans le périmètre de la garde non vide `_options_des_tables`) ; la dernière respecte le gabarit de `docs/installation.md` (bloc Source de vérité avant la ligne de retour) tout en gardant les dix titres de niveau 2 prévus.
- **Le mode interactif est décrit en prose, jamais en exemple marqué.** `python fetcher.py --offline optimize` apparaît une seule fois, dans une phrase de `## optimize`, et dans aucun bloc `console`. Conséquence voulue : le témoin marqué de l'ordre global-avant-sous-commande reste unique (`python fetcher.py --offline optimize --demo`), la vérité « seul témoin » du plan reste vraie et la mutation d'ordre de 02-03 t1 garde son motif observable.
- **Tableau `## db` en jetons nus.** `status`, `stats`, `sync`, `fill`, `clear` — la forme « db clear » n'y figure pas, ce qui concentre l'obligation d'avertissement sur trois lignes seulement et rend le contrôle de co-présence falsifiable et localisé.
- **Descriptions verbatim une seule fois.** Les littéraux `Afficher l'état de la base`, `Forcer la synchronisation complète` et `Vider la base locale` sont lus dans `dofus_stuff/cli.py` (apostrophe droite pour le premier) et cités dans `## db` uniquement ; `## cache` n'en reprend aucun. Vérifié par comparaison normalisée des deux côtés.
- **`db sync` / `cache fill` hors du jeton destructeur.** Ils réécrivent la base (`replace_kind` / `pull_all`) et exigent le réseau ; ils ne détruisent aucune donnée propre à l'utilisateur (les stuffs sauvegardés vivent côté navigateur). Classement A2 du plan, reporté dans les décisions de ce résumé pour qu'un relecteur ne lise pas D-23 comme violée.
- **Renvoi vers la page de la base locale en prose, sans lien.** La fenêtre 24 h et la resynchronisation sont annoncées comme traitées avec la base locale, mais sans cible markdown : `docs/base-locale.md` n'existe pas encore et un lien ferait rougir `problemes_liens` (leçon de la phase 1 : le sommaire ne contient aucune cible hors index).
- **`--all` non documentée.** Le parseur accepte `db clear --all` mais aucune ligne de code ne la lit ; la page ne la mentionne pas (la chaîne `--all` n'apparaît que comme préfixe des options `--allow-*` légitimes).
- **Écart assumé avec `.claude/CLAUDE.md` §2 (DOCS-06)**, qui prescrit un tableau « commande → rôle → exemple » couvrant toutes les sous-commandes. La phase 2 est gouvernée par D-16 à D-18, qui fixent une section par sous-commande et interdisent la table récapitulative unique (D-17). La substance de DOCS-06 est tenue section par section ; la forme en tableau unique serait un second référentiel à maintenir.
- **Barème de l'`actuals`.** 2362 jetons = chars/4 du diff réalisé (`docs/cli.md` 9381 octets + 66 octets ajoutés à `docs/sommaire.md`). L'estimate du plan portait 52000 pour le travail d'agent complet (lecture de la recherche, mesures, rédaction) : l'écart est réel, il n'est pas arrondi pour se rapprocher de l'estimate.

## Deviations from Plan

### Documented deviations

**1. [Rule 2 - CLAUDE.md] Forme du référentiel CLI en sections plutôt qu'en tableau unique**
- **Found during :** tâches 1 à 3 (rédaction de la page)
- **Issue :** `.claude/CLAUDE.md` §2, ligne `cli.md` (DOCS-06), prescrit « un tableau « commande → rôle → exemple » couvrant **toutes** les sous-commandes du parseur et **toutes** les options globales ; un encadré d'avertissement sur `db clear` ». Les décisions D-16 à D-18 de `02-CONTEXT.md`, reprises par le plan, imposent au contraire une section par sous-commande avec ses propres tables d'options et interdisent la table récapitulative unique (D-17).
- **Fix :** la page suit le plan et les décisions de phase : une section par sous-commande, un tableau d'options dans chaque section qui en a, un tableau des options globales, un tableau des cinq sous-commandes de `db`, un exemple marqué par sous-commande, et la sous-section d'avertissement sur la commande destructrice. Chaque exigence de fond de DOCS-06 est tenue (toutes les sous-commandes avec rôle et exemple, toutes les options globales, avertissement sur `db clear`), sans le second référentiel que D-17 écarte.
- **Files modified :** `docs/cli.md`
- **Verification :** les 34 jetons d'options et les 8 sous-commandes sont présents ; les invariants structurels et la suite complète restent verts.
- **Committed in :** `8c96674`, `d778063`, `dcb65bc` (réparti sur les trois tâches, chacune ajoutant sa part)

Aucun écart de règle 1 (bogue) ni de règle 3 (blocage) : aucun bogue n'a été rencontré, aucune dépendance n'a été installée, aucun paquet n'a été ajouté.

**Total deviations :** 1 documentée (règle 2, pilotée par CLAUDE.md).
**Impact on plan :** aucun élargissement de périmètre. La page reste strictement celle décrite par le plan ; le seul écart porte sur la forme du référentiel, tranchée par les décisions de phase.

## Issues Encountered

- **En-tête de branche `main` (même situation que 01-01 à 01-04).** Le protocole d'exécution de l'agent interdit par défaut de committer sur la branche protégée, mais `git.base-branch --is-protected main` renvoie `true` sans override `git.allow_default_branch_commits`, alors que `.planning/config.json` porte `git.branching_strategy: "none"` et que l'historique des deux phases est intégralement sur `main`. L'orchestrateur a dispatché cet exécutant comme **séquentiel sur l'arbre principal** : les trois commits y sont donc posés, conformément à la consigne de dispatch. Aucun `update-ref`, aucun `push`, aucun reset destructeur, aucun `git clean` ni `git stash` n'a été exécuté.
- **Conventions de fin de ligne.** Les pages de `docs/` sont en CRLF (mesure de la recherche). Les deux fichiers ont été écrits puis normalisés en CRLF sans BOM dans le même processus, et vérifiés (89 puis 195 lignes CRLF, `BOM=False`).
- Aucun autre problème rencontré : aucun test en échec, aucune valeur de retour inattendue, aucune resynchronisation, aucune base ouverte.

## Known Stubs

Aucun. Les onze options d'`optimize` sans `help` (`--base-vit`, `--base-str`, `--base-cha`, `--base-agi`, `--base-wis` et les six `--scroll-*`) sont décrites par leur nom et leur défaut : c'est la forme prescrite par D-19 (aucune sémantique inventée), pas une valeur de remplissage. La colonne « Rôle » porte explicitement « aucune description dans l'aide du parseur », et une phrase de la section explique pourquoi. Aucun jeton de brouillon (`todo`, `a completer`, `lorem`) ne figure dans la page : `problemes_encodage` est vert.

## Threat Flags

Aucune surface nouvelle par rapport au modèle de menaces du plan. La page ne fait que *nommer* des commandes existantes : aucun point d'entrée réseau, aucune voie d'authentification, aucune écriture disque et aucun changement de schéma ne sont introduits. Les mitigations du registre STRIDE du plan sont appliquées comme écrites :

- **T-02-01 (perte de la base locale, high)** — les trois lignes qui nomment `db clear` ou `cache clear` portent l'avertissement sur la même ligne, aucun bloc `console` ne cite ces commandes, et aucune commande du produit n'a été exécutée à aucun moment (preuve : horodatage de `.data/dofus.sqlite3` inchangé, `Sep 6 23:27` avant et après).
- **T-02-02 (quota Dofusdude, medium)** — `db sync` et `cache fill` sont décrits comme exigeant le réseau, avec l'incompatibilité mesurée avec `--offline`, et n'apparaissent dans aucun exemple marqué.
- **T-02-04 (information disclosure, low)** — la page décrit « le dossier `.data/` à la racine du dépôt » et ne recopie jamais la valeur absolue imprimée par l'aide de `--data-dir` ; les quatre chemins cités entre accents graves existent tous sur disque.
- **T-02-05 (option inventée, high)** — aucun jeton n'est écrit de mémoire : les 4 + 30 options et leurs défauts viennent des mesures M2 et M2.3, et les contrôles des plans 02-02 et 02-03 les rejoueront sur `build_parser().parse_args`.

## User Setup Required

None - aucune configuration externe, aucun service, aucune variable d'environnement.

## Next Phase Readiness

La page et son entrée d'index sont livrées, et la suite complète est verte (**158 passed** avec `.venv/Scripts/python.exe -m pytest -q`). Ce que les plans suivants trouvent sur disque :

- **02-02** (vague 2) peut écrire `tests/test_docs_cli.py` : les 8 sous-commandes, les 4 options globales et les 30 options d'`optimize` sont citées par la page ; les sections `## Options globales` et `## optimize` ont chacune des lignes de tableau non vides, ne citant que des options acceptées par le parseur public (mesuré : 4 et 30, aucune refusée) ; `## cache` existe, cite `db`, déclare l'alias et ne reprend aucune des trois descriptions de `## db` ; le bloc `## Source de vérité` nomme `build_parser()`.
- **02-03** (vague 3) peut extraire les exemples marqués : 8 blocs `console`, une ligne chacun, tous commençant par `python fetcher.py`, chacun atteignant une sous-commande distincte (les huit noms épinglés), tous acceptés par `build_parser().parse_args` ; l'unique témoin de l'ordre global-avant-sous-commande est `python fetcher.py --offline optimize --demo`.
- **Limite honnête conservée (D-26)** : ce plan livre la page et son entrée d'index ; la complétude parser → page n'est pas revendiquée. Une sous-commande ou une option ajoutée plus tard au parseur et non documentée ne fera pas échouer la suite.
- **Aucune modification de `dofus_stuff/**`, de `README.md`, de `GUIDE_WIZARD.md` ni de `.data/`.** `README.md` garde son lien unique vers `docs/sommaire.md` et n'a pas été touché (D-29).

---

## Self-Check: PASSED

- `docs/cli.md` : **FOUND** (195 lignes, H1 `# CLI`, bloc `## Source de vérité`, `[Retour au sommaire](sommaire.md)` en dernière ligne)
- `docs/sommaire.md` : **FOUND** (ligne `| [CLI](cli.md) | ... |`)
- Commit `8c96674` : **FOUND**
- Commit `d778063` : **FOUND**
- Commit `dcb65bc` : **FOUND**
- `./.venv/Scripts/python.exe -m pytest -q` : **158 passed**

*Phase: 02-r-f-rence-cli-align-e-sur-le-parseur*
*Completed: 2026-09-11*
