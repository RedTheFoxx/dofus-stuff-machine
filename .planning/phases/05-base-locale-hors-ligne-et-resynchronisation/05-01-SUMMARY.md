---
phase: 05-base-locale-hors-ligne-et-resynchronisation
plan: 01
subsystem: documentation
tags: [markdown, pytest, flask-test-client, argparse-help, copie-verte-avant-mutation, morsures, ast-gardes, sqlite-hors-ligne, documentation-francaise, crlf, accents]

# Dependency graph
requires: []
provides:
  - "docs/base-locale.md : la page de la base locale — fichier et dossier lus dans `dofus_stuff/database.py`, sept categories stockees, fenetre de re-check de 24 h lue dans `dofus_stuff/sync.py`, les deux defauts hors-ligne enonces par surface, et les champs de l'etat de la base par surface dans leur forme exacte ; il reste quatre sections a y ajouter au plan 05-02"
  - "La ligne d'index « Base locale » de `docs/sommaire.md` (exactement une ligne ajoutee, en fin de table) et les deux renvois de `docs/parcours-simplifie.md` devenus des liens vers la page"
  - "tests/test_docs_base_locale.py : le module neuf de la page (5 tests) — garde de cloture reecrite, page et index, valeurs fondatrices, deux defauts hors-ligne par surface, champs de l'etat par surface, avec la bijection des libelles dans les deux sens et la conditionnalite du champ par categorie mesuree sur les deux etats"
  - "La levee de la dette D-44/D-63 dans le meme commit que la page : `PAGES_INEXISTANTES` videe et ses deux commentaires remis en verite dans `tests/test_docs_parcours.py`"
affects: [05-02, 05-03, verification-phase-5]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (92 000) est consigne tel quel : il mesure le pessimisme de l'estimate,
# pas un travail non fait (les trois taches sont livrees, 13/13 morsures detectees).
actuals:
  tokens: 15506     # chars/4 sur le diff realise (62 025 caracteres ajoutes, 5 fichiers, 3 commits)
  tasks: 3
  commits: 3        # MESURE : git rev-list --count 07e6784868cd6444c5f7e82569b3633ed1f1ee5f..HEAD
  plan_head_before: 07e6784868cd6444c5f7e82569b3633ed1f1ee5f

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; uniquement la stdlib (ast, io, re, hashlib, contextlib)
  patterns:
    - "Morsure sur copie verte avant mutation : chaque derive est jouee dans un repertoire temporaire, jamais sur l'arbre reel ni sur `.data/`, et la copie doit etre verte AVANT la mutation pour que la morsure prouve quelque chose (D-84)"
    - "Motif de morsure porte par une constante ASCII du module, jamais ecrit en clair dans une ligne d'assertion : pytest reproduit la ligne du `assert`, une valeur en clair y serait trouvee meme sans constat produit (regle posee au plan 03-03)"
    - "Le constat nomme : la surface, la valeur fautive, la valeur lue (sortie capturee, rendu ou aide de parseur) et le fichier de code producteur (D-83, D-75)"
    - "Les libelles de l'etat sont compares EXACTEMENT, dans les deux sens (code vers page et page vers code) ; `normalize` n'est employe que pour diagnostiquer un ecart lisse, jamais pour l'effacer — `Entrées :` et `ENTREES :` sont deux chaines distinctes du code (Pitfall 4)"
    - "La conditionnalite d'un champ se mesure sur deux etats (base vide et base peuplee) : une seule mesure ne prouverait rien (Pitfall 3)"
    - "Le rendu web se lit sur le corps de l'ecran (`_lignes_du_corps`), jamais sur la reponse entiere, qui porterait la coquille et la ligne de statut (D-11)"

key-files:
  created:
    - docs/base-locale.md
    - tests/test_docs_base_locale.py
  modified:
    - docs/sommaire.md
    - docs/parcours-simplifie.md
    - tests/test_docs_parcours.py

key-decisions:
  - "Le module neuf ne porte PAS `from __future__ import annotations` : la morsure `import_interdit` insere un import interdit en tete du fichier, et un import `__future__` place apres une autre instruction est une erreur de syntaxe — la premiere execution de la batterie a montre que le module mourait a la collecte au lieu de produire le constat de sa garde. Mesure du mecanisme : `ast.parse` accepte cette source, `compile` la refuse (`from __future__ imports must occur at the beginning of the file`), et c'est `compile` que la reecriture d'assertions de pytest utilise. Le commentaire pose au-dessus des imports explique pourquoi, et les annotations du module restent valides sans l'import differe."
  - "Le constat de conditionnalite porte `MOTIF_CONDITION` en tete : la premiere execution de la batterie de la tache 3 a montre que le test rougissait bien mais avec `MOTIF_CHAMPS_WEB` seul, donc la morsure `categorie_inconditionnelle` n'etait pas retrouvee par son motif nomme. Le constat porte desormais les deux motifs (condition en tete, surface en fin) : la morsure est discriminante, l'affaiblissement du controle n'a jamais ete une option."
  - "`normalize` n'est employe dans la tache 3 que pour diagnostiquer : un libelle rendu qui manque a la page alors que sa forme normalisee s'y trouve signale une page qui a lisse un ecart de casse ou d'accent. La comparaison des libelles, elle, reste exacte."
  - "Les phrases d'aide des deux parseurs sont pinces comme constantes du module (relevees sur le rendu, verifiees a l'execution contre `format_help()` et l'aide capturee de `--help`) : la phrase est exigee du parseur ET de la section de sa surface, ce qui interdit de l'attribuer a la mauvaise surface (D-71, D-72)."
  - "Les accolades et les accents graves ne sont pas employes dans les messages de constat, et les motifs sont en ASCII : les sorties restent lisibles et recherchables telles quelles dans un terminal Windows."
  - "`PAGES_INEXISTANTES` est videe dans le meme commit que la page (Pitfall 1) : le commit 1 porte les deux, sans quoi la suite aurait ete rouge entre deux commits."

patterns-established:
  - "Pattern 9 : une phrase d'aide de parseur est exigee de deux sources — le parseur qui la rend et la section de la page qui la cite — ce qui prouve a la fois que la page dit vrai et qu'elle la range dans la bonne surface"
  - "Pattern 10 : la bijection des libelles est verifiee dans les deux sens (produit vers cite et cite vers produit), une seule direction laissant passer un libelle invente par la page"

requirements-completed: [BASE-01, BASE-02]

coverage:
  - id: D1
    description: "`docs/base-locale.md` decrit le fichier `dofus.sqlite3`, le dossier `.data/`, les sept categories stockees et la fenetre de re-check de 24 h, chaque valeur lue dans une constante publique du code (`DB_NAME`, `DEFAULT_DATA_DIR`, `ITEM_KINDS`, `CHECK_INTERVAL_SECONDS`) et jamais recopiee de memoire"
    requirement: "BASE-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_page_et_index_de_la_base_locale"
        status: pass
      - kind: unit
        ref: "batterie de morsures 05-01 tache 1 : 7/7 detectees (fichier renomme, categorie retiree, ligne d'index retiree, H1 desaligne, import interdit, data_dir par defaut, confirmation destructive)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Les deux defauts hors-ligne sont enonces separement, chacun dans la section de sa surface, avec la phrase d'aide que son propre parseur rend — web hors-ligne par defaut (`parse_args([]).offline is True`, `--no-offline`, `--online`), ligne de commande en ligne par defaut (`parse_args([\"db\", \"status\"]).offline is False`, `--offline` requis)"
    requirement: "BASE-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_defauts_hors_ligne"
        status: pass
      - kind: unit
        ref: "batterie de morsures 05-01 tache 2 : 3/3 detectees (defaut web inverse, defaut CLI force, aide du web remplacee)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Les champs de l'etat de la base sont decrits par leurs noms et par surface, dans la forme exacte de chaque surface (accent et casse compris), avec leurs etats vides et la conditionnalite du champ par categorie mesuree sur une base vide et sur une base peuplee"
    requirement: "BASE-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_base_locale.py#test_champs_de_la_ligne_de_commande (sortie capturee de `_print_db_status`, base vide sous `tmp_path` et base peuplee de la fixture `app`, chaque base refermee dans un `finally`)"
        status: pass
      - kind: integration
        ref: "tests/test_docs_base_locale.py#test_champs_de_la_surface_web (`GET /db/status` sur la base peuplee et sur une base vide construite par `create_app` sous `tmp_path`)"
        status: pass
      - kind: unit
        ref: "batterie de morsures 05-01 tache 3 : 3/3 detectees (Entrées : renomme cote CLI, ENTREES : renomme cote web, champ par categorie rendu inconditionnel)"
        status: pass
    human_judgment: false
  - id: D4
    description: "La dette D-44/D-63 est levee dans le meme commit que la page : la reserve `PAGES_INEXISTANTES` est videe, ses deux commentaires sont remis en verite, et les deux renvois de `docs/parcours-simplifie.md` sont devenus des liens vers `base-locale.md`"
    requirement: "BASE-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py (32 tests du module) : vert avec la reserve videe et les deux liens poses, les deux boucles consommatrices et le controle de legitimite du lien laisses intacts"
        status: pass
      - kind: integration
        ref: "git diff --diff-filter=D --name-only pour les trois commits : 0 fichier supprime"
        status: pass
    human_judgment: false
  - id: D5
    description: "La garde de cloture du module neuf est reecrite et non recopiee : racines de risque interdites, `main` interdit, suppressions interdites, `DEFAULT_DATA_DIR` jamais passe comme `data_dir`, aucune paire de confirmation destructive, et l'import de `dofus_stuff.database` — matiere de la page — n'est plus interdit"
    requirement: "BASE-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_garde_de_cloture_du_harnais (auto-analyse par `ast.parse(Path(__file__).read_text())`)"
        status: pass
      - kind: unit
        ref: "morsures `import_interdit`, `data_dir_defaut` et `confirmation_interdite` : detectees sur copie verte avant mutation"
        status: pass
    human_judgment: false
  - id: D6
    description: "`.data/dofus.sqlite3` garde taille, `mtime_ns` et SHA-256 avant et apres chaque suite complete : les tests de ce plan ne touchent la base reelle que par aucune voie — la base peuplee qu'ils lisent est celle de la fixture `app`, construite sous `tmp_path`"
    requirement: "BASE-01"
    verification:
      - kind: integration
        ref: "empreinte mesuree avant et apres chacune des trois suites completes : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b — identique"
        status: pass
    human_judgment: false

# Metrics
duration: 14min
completed: 2026-09-11
status: complete
---

# Phase 5 : Base locale, hors-ligne et resynchronisation — Plan 05-01 Summary

**La page `docs/base-locale.md` existe, elle est indexee, et elle dit vrai : le nom du fichier, le dossier, les sept categories, la fenetre de 24 h, les deux defauts hors-ligne — enonces separement, chacun dans la section de sa surface — et les cinq champs de l'etat de la base dans la forme exacte de chaque surface. Chaque valeur est lue dans une constante publique, une aide de parseur rendue ou une sortie capturee ; treize derives epinglees font rougir la suite sur une copie verte avant mutation, et `.data/dofus.sqlite3` est intact.**

## Performance

- **Duration:** 14 min entre le premier et le dernier commit de tache (mesure `git log --format=%cI` : 23:15:47 +02:00 -> 23:29:34 +02:00)
- **Started:** 2026-09-11T23:15:47+02:00
- **Completed:** 2026-09-11T23:29:34+02:00
- **Tasks:** 3
- **Files modified:** 5 (1 099 insertions, 19 suppressions) — `docs/base-locale.md` (107 lignes), `tests/test_docs_base_locale.py` (968 lignes), `tests/test_docs_parcours.py` (21/17), `docs/parcours-simplifie.md` (2/2), `docs/sommaire.md` (1)
- **Commits:** 3, zero fichier supprime (`git diff --diff-filter=D --name-only` sur les trois commits : vide)

## Accomplishments

- **La page est une tranche verticale livree au premier commit, pas un squelette.** `docs/base-locale.md` ouvre par un `H1` egal a son libelle d'index, porte ses sections dans l'ordre, se termine par `[Retour au sommaire](sommaire.md)` et par le bloc `## Source de vérité`, en octets CRLF sans BOM — le gabarit verrouille des phases precedentes (D-69, D-90).
- **Aucune valeur n'est recopiee de memoire** (D-74, T-05-01). `dofus.sqlite3` et `.data/` sont exiges egaux a `DB_NAME` et a `DEFAULT_DATA_DIR.name`, les sept categories a `ITEM_KINDS` (lui-meme egal a `tuple(kind for _, _, kind in SYNC_SOURCES)`), la fenetre de re-check a `CHECK_INTERVAL_SECONDS` et a son expression `24 * 60 * 60`. Retirer `"cosmetics"` de `ITEM_KINDS` ou renommer `DB_NAME` fait rougir le module : mesure, pas intention.
- **Les deux defauts hors-ligne sont mesures sur les parseurs publics, jamais supposes** (D-14) : `parse_args([]).offline is True` et `parse_args(["--no-offline"]).offline is False` cote web, `parse_args(["--online"])` arbitre au lancement, `parse_args(["db", "status"]).offline is False` cote ligne de commande. Les deux phrases d'aide sont exigees **du parseur** (`format_help()`, et l'aide de `--help` capturee sous `redirect_stdout`, `SystemExit(0)` intercepte) **et** de la section de leur propre surface — une section qui citerait l'aide de l'autre surface rougit.
- **Les champs de l'etat sont verifies par bijection exacte, dans les deux sens** : chaque libelle produit par `_print_db_status` doit etre cite par la section ligne de commande, et chaque libelle cite doit etre produit ; idem cote web sur les lignes du corps rendu par `GET /db/status`. La comparaison reste exacte — `Entrées :` (accentue, ligne de commande) et `ENTREES :` (sans accent, web) sont deux chaines distinctes du code et la page ne les lisse pas (Pitfall 4).
- **La conditionnalite du champ par categorie est prouvee sur les deux etats** (Pitfall 3) : la section ligne de commande est confrontee a une base vide creee sous `tmp_path` **et** a la base peuplee de la fixture `app` (avec `db.close()` dans un `finally`, sans quoi le nettoyage du dossier temporaire echoue sur Windows) ; la section web au rendu de `GET /db/status` sur une base peuplee **et** sur une base vide construite par `create_app(data_dir=tmp_path / "web_vide", ...)`, dont la reponse rend 200 sur un dossier absent et cree bel et bien le dossier.
- **La garde de cloture du module neuf est reecrite, pas recopiee** (Pitfall 2) : elle interdit les racines de risque (`sqlite3`, `subprocess`, `socket`, `multiprocessing`, `ctypes`, `webbrowser`, `urllib`, `requests`, `http`, `ftplib`, `smtplib`), l'appel `main`, les appels de suppression, `DEFAULT_DATA_DIR` passe comme `data_dir` et les quatre valeurs de confirmation destructrice (`O`, `Y`, `OUI`, `YES`) ; elle n'interdit plus l'import de `dofus_stuff.database`, qui est la matiere de la page. Le module s'auto-analyse par `ast.parse(Path(__file__).read_text(encoding="utf-8"))` — jamais par recherche de chaines, alors qu'il cite lui-meme ces noms dans ses messages.
- **La dette D-44/D-63 est levee dans le meme commit que sa cible** : `PAGES_INEXISTANTES = ()` et ses deux commentaires remis en verite, les deux renvois en prose de `docs/parcours-simplifie.md` devenus des liens, les deux boucles consommatrices de la reserve et le controle de legitimite du lien laisses intacts (D-63, D-86).
- **Treize morsures sur copie verte avant mutation** (7 + 3 + 3), toutes detectees avec leur motif nomme — voir § Verification.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : tranche verticale de la page, sa ligne d'index et son harnais** — `ee903cf` (feat)
2. **Tache 2 : les deux defauts hors-ligne, surface par surface** — `179c03d` (feat)
3. **Tache 3 : les champs de l'etat de la base, surface par surface** — `d863511` (feat)

**Plan metadata:** `docs(05-01): complete la page de la base locale` (voir le commit de metadonnees du plan, qui porte ce SUMMARY et la mise a jour de STATE/ROADMAP).

## Files Created/Modified

- `docs/base-locale.md` — **nouveau** (107 lignes). Huit titres de niveau 2 dans l'ordre : `## Le fichier de la base`, `## Les catégories stockées`, `## La fenêtre de re-check de 24 heures`, `## Le mode hors-ligne du web`, `## Le mode hors-ligne de la ligne de commande`, `## L'état de la base en ligne de commande`, `## L'état de la base dans l'interface web`, puis `## Source de vérité` ; `H1` = `# Base locale` ; ligne de retour en derniere ligne non vide ; CRLF sur toutes les lignes, UTF-8 sans BOM ; aucun lien externe, aucun jeton de brouillon, aucune valeur volatile (ni horodatage, ni version de jeu, ni nombre d'objets, ni duree calculee). Les quatre sections restantes appartiennent au plan 05-02.
- `tests/test_docs_base_locale.py` — **nouveau** (5 tests, 968 lignes). Garde de cloture reecrite (`RACINES_INTERDITES`, `APPELS_SUPPRESSION`, `APPEL_PRODUIT`, `APPELS_SYNCHRO_PRODUIT`, `CONFIRMATIONS_INTERDITES`, `MOTIF_GARDE`, `MOTIF_DATA_DIR`, `MOTIF_CONFIRMATION`) ; constantes de motif `MOTIF_FICHIER`, `MOTIF_CATEGORIES`, `MOTIF_FENETRE`, `MOTIF_INDEX`, `MOTIF_H1`, `MOTIF_DEFAUTS`, `MOTIF_CHAMPS_CLI`, `MOTIF_CHAMPS_WEB`, `MOTIF_CONDITION`, `MOTIF_VOLATILES`, `MOTIF_CRLF` ; constantes de contenu `MOTIF_VOLATILE`, `MOTIF_LIBELLE_CITE`, `AIDE_WEB_OFFLINE`, `AIDE_CLI_OFFLINE`, `MARQUES_DEFAUT_WEB`, `MARQUES_EXIGENCE_CLI`, `PREFIXE_LIGNE_CATEGORIE`, `TITRES_SECTION_ATTENDUS` (6 titres) ; helpers `_texte_page`, `_lignes_du_corps`, `_statut`, `_libelles_produits`, `_libelles_cites`, `_constats_bijection`, `_constats_conditionnels`, `_sortie_db_status`. Les trois helpers partages (`_texte_page`, `_lignes_du_corps`, `_statut`) sont repris du patron de la phase 4 ; les cinq autres sont **locaux** et ne recopient aucun helper de `tests/conftest.py` (D-12) — la lecture des libelles d'etat et la comparaison de bijection n'existaient dans aucune phase precedente. *Note pour la tenue du ledger de phase : les lignes « helpers locaux » et « constantes de contenu » du tableau d'artefacts de `05-01-PLAN.md` ne nomment pas ces cinq helpers ni `AIDE_WEB_OFFLINE`/`AIDE_CLI_OFFLINE`/`MARQUES_DEFAUT_WEB`/`MARQUES_EXIGENCE_CLI`/`MOTIF_LIBELLE_CITE`/`PREFIXE_LIGNE_CATEGORIE`/`TITRES_SECTION_ATTENDUS` : ce sont des ajouts locaux a ce module, sans effet sur les plans 05-02 et 05-03.*
- `tests/test_docs_parcours.py` — **modifie** (21/17). `PAGES_INEXISTANTES` videe et ses deux commentaires remis en verite ; les deux boucles consommatrices (~2494, ~2627) et le controle de legitimite du lien (~2934-2943) sont intacts.
- `docs/parcours-simplifie.md` — **modifie** (2/2). Les deux renvois vers la base locale sont devenus des liens vers `base-locale.md`.
- `docs/sommaire.md` — **modifie** (+1). Une seule ligne d'index, en fin de table, sans remaniement des lignes existantes (D-70).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocage : morsure non discriminante] `from __future__ import annotations` retiré du module neuf**

- **Found during:** Tache 1 (batterie de morsures, premiere execution — 6/7 detectees)
- **Issue:** la morsure `import_interdit` insere `import socket` **en tete du fichier** pour prouver que la garde de cloture mord. Le module portait alors `from __future__ import annotations` en deuxieme ligne : la mutation produisait une **erreur de syntaxe** sous la reecriture d'assertions de pytest, le module mourait a la collecte et la sortie ne portait aucune ligne du garde — la morsure sortait en `MUTATION NON DETECTEE (import_interdit)`, et le constat attendu n'existait pas.
- **Mesure du mecanisme** (pas une supposition) : une source `import socket` puis `from __future__ import annotations` est acceptee par `ast.parse` mais refusee par `compile` — `SyntaxError: from __future__ imports must occur at the beginning of the file` — et c'est `compile` que la reecriture d'assertions emploie.
- **Fix:** l'import differe a ete retire, avec un commentaire qui explique pourquoi et constate que les annotations du module (`ast.expr | None`, `list[tuple[int, str]]`) sont valides sans lui. La morsure est desormais discriminante : la sortie porte la ligne du garde avec `MOTIF_GARDE`.
- **Files modified:** `tests/test_docs_base_locale.py` (meme commit que la tache 1)
- **Verification:** apres correction, sortie reelle `mutation detectee (import_interdit), motif "garde de cloture du harnais"`. Batterie complete : **7/7**.
- **Committed in:** `ee903cf`

**2. [Rule 3 — Blocage : motif nomme absent du constat] Le constat de conditionnalite porte desormais `MOTIF_CONDITION`**

- **Found during:** Tache 3 (batterie de morsures, premiere execution — 2/3 detectees)
- **Issue:** la morsure `categorie_inconditionnelle` rend le champ par categorie inconditionnel (`if True:`). Le test **rougissait bien**, mais le constat produit portait `MOTIF_CHAMPS_WEB` sans `MOTIF_CONDITION` : la batterie, qui cherche la chaine `champ conditionnel`, rapportait `MUTATION NON DETECTEE`. L'affaiblissement du controle (garder le test tel quel) aurait laisse la morsure sans preuve rejouable.
- **Fix:** le constat de conditionnalite est desormais prefixe de `MOTIF_CONDITION` et se termine par le motif de surface, de sorte que les deux morsures de la meme famille (`champ_cli_renomme` / `champ_web_renomme` d'un cote, `categorie_inconditionnelle` de l'autre) trouvent chacune leur motif nomme.
- **Files modified:** `tests/test_docs_base_locale.py` (meme commit que la tache 3)
- **Verification:** apres correction, sorties reelles `mutation detectee (champ_cli_renomme), motif "champs de la ligne de commande"`, `mutation detectee (champ_web_renomme), motif "champs de la surface web"`, `mutation detectee (categorie_inconditionnelle), motif "champ conditionnel"`. Batterie complete : **3/3**.
- **Committed in:** `d863511`

---

**Total deviations:** 2 auto-fixed, toutes deux dans le harnais de test et toutes deux du meme type : une morsure qui ne mordait pas encore de maniere discriminante. Aucun ecart de perimetre : aucun fichier de `dofus_stuff/**` n'a ete modifie, `pyproject.toml` est inchange, et rien n'a ete publie, deploye, achete ou supprime.
**Impact on plan:** aucun affaiblissement d'un controle pour obtenir le vert ; les deux corrections ont rendu les morsures plus strictes, jamais plus permissives.

## Issues Encountered

- **Deux tours de normalisation des fins de ligne** : les insertions de sections dans `docs/base-locale.md` et dans le module ont d'abord produit des lignes en LF, detectees immediatement par le controle de CRLF de la page (« la page porte 71 fin(s) de ligne pour 51 retour(s) chariot »). Le fichier a ete repasse en CRLF dans le meme tour, avant tout commit : aucun commit du plan ne porte un fichier en LF.
- **Le module est passe de 2 a 5 tests sans toucher aux gardes existantes** : `tests/test_docs_structure.py` et `tests/test_docs_parcours.py` gardent leurs gardes ; le second n'a vu que la reserve videe et les deux commentaires remis en verite. `git diff --stat` sur les trois commits : 5 fichiers, aucun autre.
- **Constats en ASCII, sorties lisibles** : les messages ne portent ni accolades ni accents graves (le modulo des dicts est ecrit en clair) pour rester lisibles et recherchables tels quels dans un terminal Windows.

## Verification (sorties reelles, verbatim)

**Suite complete et integrite de `.data/dofus.sqlite3`** (mesuree avant et apres chaque suite ; les trois mesures sont identiques) :

```
$ ./.venv/Scripts/python.exe -m pytest -q          # apres la tache 1
207 passed in 3.57s

$ ./.venv/Scripts/python.exe -m pytest -q          # apres la tache 2
208 passed in 3.59s

$ ./.venv/Scripts/python.exe -m pytest -q          # apres la tache 3
210 passed in 3.83s

$ ./.venv/Scripts/python.exe -m pytest tests/test_docs_base_locale.py -q   # apres la tache 3
5 passed in 0.16s

$ empreinte de .data/dofus.sqlite3 avant/apres chacune des trois suites
24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b   # identique
```

**Morsures, tache 1 (7/7) :**

```
mutation detectee (fichier_renomme), motif "nom du fichier de la base"
mutation detectee (categorie_retiree), motif "categories stockees"
mutation detectee (ligne_index_retiree), motif "index du sommaire"
mutation detectee (h1_desaligne), motif "titre de niveau 1"
mutation detectee (import_interdit), motif "garde de cloture du harnais"
mutation detectee (data_dir_defaut), motif "repertoire de donnees non isole"
mutation detectee (confirmation_interdite), motif "confirmation d une action destructive"
morsures 05-01 tache 1 : 7/7 detectees (copie verte avant chaque mutation)
```

**Morsures, tache 2 (3/3) :**

```
mutation detectee (defaut_web_inverse), motif "defauts hors-ligne"
mutation detectee (defaut_cli_force), motif "defauts hors-ligne"
mutation detectee (aide_web_remplacee), motif "defauts hors-ligne"
morsures 05-01 tache 2 : 3/3 detectees (copie verte avant chaque mutation)
```

**Morsures, tache 3 (3/3) :**

```
mutation detectee (champ_cli_renomme), motif "champs de la ligne de commande"
mutation detectee (champ_web_renomme), motif "champs de la surface web"
mutation detectee (categorie_inconditionnelle), motif "champ conditionnel"
morsures 05-01 tache 3 : 3/3 detectees (copie verte avant chaque mutation)
```

**Morsure corrigee, avant/apres (tache 3, constat encore non nomme) :**

```
MUTATION NON DETECTEE (categorie_inconditionnelle) : motif "champ conditionnel" absent de la sortie
E       AssertionError: base-locale.md : constats sur les champs de la surface web : champs de la surface web :
        la surface web — dofus_stuff/web/routes.py rend la meme liste de libelles sur une base vide et sur une
        base peuplee (DERNIER CHECK :, ENTREES :, FICHIER :, PAR CATEGORIE :, VERSION JEU :) ; attendu au moins
        un libelle conditionnel, la ligne par categorie n'etant ecrite que si des objets existent
        (dofus_stuff/web/routes.py, ## L'état de la base dans l'interface web)
1 failed, 207 passed, 2 skipped in 4.16s
```

Les trois batteries verifient que la copie est **verte avant** chaque mutation (la ligne `COPIE ROUGE AVANT MUTATION` n'est jamais apparue) et qu'aucune n'ecrit dans l'arbre de travail : chaque derive vit dans un repertoire temporaire.

## Limites declarees (et ce qui n'est PAS revendique)

- **Non automatisable, declare en `backstop` par le plan et non revendique ici** : la prose libre de la page (l'absence d'invitation a lancer une commande destructrice) et le rendu Markdown sur un service distant. Aucun controle de ce plan ne les couvre et ce SUMMARY ne les declare pas verts. Aucun blocage : rien de ce plan ne depend d'un geste humain, d'un secret ou d'un reseau.
- **Portee reelle du controle de conditionnalite** : `_constats_conditionnels` prouve que la liste des libelles **change** entre une base vide et une base peuplee (donc qu'au moins un champ est conditionnel) ; il ne prouve pas nommement que ce champ est `Par catégorie :` / `PAR CATEGORIE :`. Le nom du champ est, lui, verifie par la bijection des libelles des deux etats. Les quatre sections restantes de la page (creation de la base, refus hors-ligne, synchronisation web, commandes destructrices) appartiennent au plan 05-02 et ne sont pas revendiquees par ce plan.

## Known Stubs

Aucun. La page ne porte ni marqueur de brouillon, ni `TODO`/`FIXME`, ni texte de remplacement : elle est volontairement incomplete (quatre sections a venir au plan 05-02), mais chaque section presente est vraie et ancree sur le code. Aucune valeur vide ne remonte a l'affichage.

## User Setup Required

None — no external service configuration required. Aucune dependance ajoutee (`pyproject.toml` inchange), aucun serveur lance, aucun socket ouvert, aucun reseau, aucune synchronisation Dofusdude, aucune commande destructive executee, rien d'ecrit sous `.data/` ni sous `.doc-agent/`. La base peuplee que lisent les tests est celle de la fixture `app`, construite sous `tmp_path` ; la base vide est construite de la meme facon.

## Next Phase Readiness

- **Pret pour le plan 05-02 (vague 2)** : les quatre sections a ajouter (`## La base locale se cree au premier contact`, `## Le refus de la synchronisation hors-ligne`, `## La synchronisation demandee depuis le web`, `## Les commandes destructrices`) s'inserent avant `## Source de vérité` ; `TITRES_SECTION_ATTENDUS` est une constante du module et la ligne a completer y est nommee (« completion »), ce qui presente le seul point d'attention : l'ordre du tuple doit suivre l'ordre de la page.
- **Contrats deja poses et reutilisables par la vague 2** : `_lignes_du_corps` (corps rendu, jamais la reponse entiere), `_statut` (ligne de statut, seule source des messages de refus), `MOTIF_VOLATILE` et `MOTIF_CRLF` (cloture de la page), `MOTIF_CONDITION` (un champ qui se mesure sur deux etats), et la garde de cloture reecrite, qui autorise l'import de `dofus_stuff.database` tout en refusant `DEFAULT_DATA_DIR` comme `data_dir` et toute paire de confirmation destructive.
- **Contrat pour la verification de phase** : treize morsures rejouables sur copie verte avant mutation (aucune n'ecrit dans l'arbre de travail), `tests/test_docs_base_locale.py` a 5 tests verts, la suite complete a 210 tests verts sans `failed` ni `error`, aucune suppression de fichier, et l'empreinte de `.data/dofus.sqlite3` inchangee.

## Self-Check: PASSED

- `docs/base-locale.md` : FOUND (8 titres de niveau 2, CRLF sur toutes les lignes, UTF-8 sans BOM)
- `tests/test_docs_base_locale.py` : FOUND (5 tests collectes)
- Commit `ee903cf` : FOUND ; commit `179c03d` : FOUND ; commit `d863511` : FOUND
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_base_locale.py -q` : `5 passed in 0.16s`
- `./.venv/Scripts/python.exe -m pytest -q` : `210 passed in 3.83s`
- Batteries de morsures : 7/7 + 3/3 + 3/3 detectees, sur copie verte avant mutation
- Empreinte de `.data/dofus.sqlite3` avant et apres la session : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique
- `git diff --diff-filter=D --name-only` sur les trois commits : vide (aucune suppression)

---

*Phase: 05-base-locale-hors-ligne-et-resynchronisation*
*Completed: 2026-09-11*
