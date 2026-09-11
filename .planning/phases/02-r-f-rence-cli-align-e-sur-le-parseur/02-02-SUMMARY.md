---
phase: 02-r-f-rence-cli-align-e-sur-le-parseur
plan: 02
subsystem: tests
tags:
  [
    docs-fr,
    cli,
    argparse,
    ancrage-code,
    alias-cache,
    anti-duplication,
    helpers-partages,
    mutation,
    hors-ligne,
  ]

# Dependency graph
requires:
  - phase: 02-r-f-rence-cli-align-e-sur-le-parseur
    provides: "plan 02-01 : docs/cli.md (huit sous-commandes, quatre options globales, trente options d'optimize en tables thematiques, section « ## cache » declarant l'alias, bloc « ## Source de verite » nommant build_parser(), entree d'index)"
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "plans 01-01 et 01-03 : tests/conftest.py (fixtures docs_dir, normalize) et tests/test_docs_code_anchor.py (ancrage page -> parseur public, messages d'echec localisants, scanner de blocs local)"
provides:
  - "tests/conftest.py : scanner de blocs unique (_blocs_de_code avec balise conservee, _lignes_de_code) et helpers de section (_sections, _section(texte, titre, page) ou la page est obligatoire), exposes par les fixtures de portee session lignes_de_code, sections et section (D-12)"
  - "tests/test_docs_cli.py : listes epinglees SONDES_SOUS_COMMANDES (8 sondes d'argv complets), SONDES_GLOBALES (4) et SONDES_OPTIMIZE (30 couples option/valeur d'essai), helpers _texte_page, _accepte, _espace_de_noms_brut, _espace_de_noms, _options_des_tables, _option_globale_acceptee, _option_optimize_acceptee, et cinq tests d'ancrage page -> parseur"
  - "preuve de morsure : deux mutations pour la tache 1 (drapeau hors-ligne retire de la page d'installation ; section « Source de verite » renommee) et huit mutations etiquetees pour la tache 2, toutes executees dans des copies jetables, jamais sur l'arbre livre"
affects: [02-03, phase-03, phase-05, phase-06]

# Mesure #3968 — le registre de plan est sur disque, le compte n'est jamais narre.
plan_head_before: 7a9c49bbd0dde073ff4317233cd65787b8807baa
commits: 2

# Actuals (#2632) — meme barème que l'estimate du plan (chars/4 du diff realise, pas un compteur de
# harnais). L'estimate du plan portait 48000 ; la mesure du diff realise est de 5686. L'ecart est
# reel et n'est pas arrondi : l'estimate comptait le travail d'agent (lectures, mesures du parseur,
# huit mutations), cette mesure-ci ne compte que les caracteres ajoutes au depot.
actuals:
  tokens: 5686
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Un seul scanner de blocs de code, une seule famille de helpers de section : implementation privee en haut de tests/conftest.py + fixture de portee session, sur le mecanisme deja utilise par la fixture normalize (D-12, lecon WR-04)"
    - "Sonde de sous-commande = un argv complet, jamais un jeton nu : parse_args([\"db\"]) et parse_args([\"cache\"]) sortent en code 2 parce que db_command est requis (mesure M1, Pitfall 2)"
    - "Sonde d'option = (option, valeur d'essai) epinglee ; une option a choices est refusee par les trois essais generiques de la phase 1, qui declaraient --jet inventee (Pitfall 7). Une option citee par une table et non epinglee rejoue les trois essais generiques, ce qui laisse --candidats-top refuse et donc le motif attribue atteignable"
    - "Options citees extraites des seules lignes de tableau (premier caractere significatif « | ») : le texte de la section optimize cite aussi --offline, option globale que le sous-parseur optimize refuse (Pitfall 10)"
    - "Espace de noms lu en deux vues : brute (pour exiger command == db ou cache) et privee de la cle command (pour comparer l'alias) ; l'egalite brute de vars() est toujours fausse (D-21, Pitfall 3)"
    - "Un seul point d'assertion par test : chaque test accumule ses constats et n'asserte qu'une fois, sinon l'ordre d'evaluation rend inatteignables des motifs attribues a une autre assertion du meme test"
    - "Controle page -> parseur asymetrique et assume (D-26) : la table des options globales doit exister par le parseur, jamais l'inverse ; aucune egalite d'ensembles avec la surface du parseur"

key-files:
  created:
    - tests/test_docs_cli.py
  modified:
    - tests/conftest.py
    - tests/test_docs_code_anchor.py

key-decisions:
  - "Le scanner de blocs et les helpers de section sont deplaces, pas recopies : tests/conftest.py les expose par les fixtures lignes_de_code, sections et section ; tests/test_docs_code_anchor.py perd ses cinq definitions locales (43 lignes, 298 -> 255) et ses cinq tests passent PAGE a chaque appel, leurs assertions restant inchangees au caractere pres"
  - "_section(texte, titre, page) exige la page, sans valeur par defaut : le helper partage ne peut plus lire la constante du module appelant, et un appel sans page leve TypeError des l'execution au lieu de perdre silencieusement le nom de la page dans son message d'echec (D-13, D-31)"
  - "Le message d'echec du helper partage nomme desormais la page passee par l'appelant (« installation.md : section ... introuvable ») : les deux mutations de non-regression de la tache 1 le prouvent, la morsure de la phase 1 survit donc au deplacement"
  - "Marqueurs d'equivalence de la section « ## cache » : la page livree declare l'alias en prose (« cache est le second nom de db ... equivaut a db <sous-commande> ») sans employer le mot « alias » ; le controle exige l'un des marqueurs normalises alias / second nom / equivaut, et la page n'a pas ete modifiee pour faire passer le test"
  - "Deux vues de l'espace de noms plutot qu'un accesseur unique : la vue brute porte command == db ou cache, la vue privee de command supporte la comparaison d'alias ; un accesseur unique aurait fait rougir le second constat sur une page correcte (advisory du plan checker)"
  - "Witness de discrimination de la batterie : sept des huit motifs attribues sont absents de la sortie d'une copie « sans » non mutee (0 ligne chacun) ; « build_parser » y est deja present trois fois parce que le module est rouge par construction sans arbre produit et que pytest cite la source — la morsure discriminante de cette mutation est donc re-mesuree sur une copie incluant l'arbre produit (5 passed avant mutation, 1 failed apres, message nommant build_parser())"
  - "La table « ## Options globales » est le seul endroit ou le mode d'echec CR-01 de la phase 1 subsistait : toute option longue citee par ses lignes de tableau est desormais sondee sur le parseur racine, et une option inventee est nommee (la sonde essaie [option, version], [option, 5, version] puis [option, x, version], trois formes necessaires et mesurees)"
  - "Limite D-26 ecrite dans le module : la completude parser -> page n'est pas revendiquee ; la limite mesuree propre a la direction page -> parseur (argparse accepte le prefixe non ambigu d'une option reelle, mesure avec --force-sync renomme en --force-synchronisation) y figure aussi, avec sa consequence sur le choix des jetons des mutations"

patterns-established:
  - "Un helper de test partage se deplace avec sa preuve de morsure : tout deplacement de couverture est suivi d'une mutation dans une copie jetable (D-12, lecon CR-01/WR-05)"
  - "Un controle d'ancrage qui peut etre sature par une table vide porte une garde non vide explicite (« aucune option »), sinon la regle est vide donc infalsifiable"
  - "Une assertion qui ne peut pas etre brisee seule (section absente, egalite stricte d'alias, acceptation stricte sans prefixe) est declaree avec sa raison mesuree dans le registre du plan, pas silencieusement omise"

requirements-completed: [CLI-01, CLI-02]

coverage:
  - id: C1
    description: "CLI-01 : les huit sous-commandes documentees de docs/cli.md sont citees par la page et acceptees par une sonde d'argv complet (db et cache jamais sondes par un jeton nu)"
    requirement: "CLI-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_sous_commandes_documentees_et_acceptees"
        status: pass
      - kind: other
        ref: "mutation « sous-commande renommee (cache) » : echec portant introuvable, page nommee"
        status: pass
      - kind: other
        ref: "mutation « derive du parseur » : self-test renomme dans la copie de dofus_stuff/cli.py, echec nommant la sonde fautive"
        status: pass
    human_judgment: false
  - id: C2
    description: "CLI-02 : les quatre options globales et les trente options d'optimize documentees sont citees et acceptees avec leur valeur d'essai, et toute option longue citee par les lignes de tableau des sections « Options globales » et « optimize » est acceptee par le parseur correspondant"
    requirement: "CLI-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_options_globales_documentees_et_acceptees"
        status: pass
      - kind: unit
        ref: "tests/test_docs_cli.py#test_options_optimize_documentees_et_acceptees"
        status: pass
      - kind: other
        ref: "mutations « option inventee dans la table globale » (--serve) et « lignes de tableau supprimees » (aucune option)"
        status: pass
      - kind: other
        ref: "mutations « jetons epingles renommes » (--candidats-top) et « derive du parseur » (--top-k, --force-sync renommes cote produit)"
        status: pass
    human_judgment: false
  - id: C3
    description: "D-21/D-20 : l'alias cache est prouve par le parseur public pour les cinq sous-commandes, modulo la cle command, et la section cache ne reproduit aucune des trois descriptions du groupe db (comparaison normalisee des deux cotes)"
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_alias_cache_equivalent_a_db_dans_le_parseur"
        status: pass
      - kind: other
        ref: "mutation « description de db dupliquee dans la section cache (forme accentuee de la page) » : echec portant dupliqu"
        status: pass
    human_judgment: false
  - id: C4
    description: "D-30 : le bloc « Source de verite » de la page nomme build_parser() et chaque chemin entre accents graves de la page existe depuis la racine du depot"
    verification:
      - kind: unit
        ref: "tests/test_docs_cli.py#test_source_de_verite_de_la_page_cli"
        status: pass
      - kind: other
        ref: "mutations « chemin cite par la page absent du depot » (cli-inexistant.py) et « jeton build_parser() retire »"
        status: pass
    human_judgment: false

# Metrics
duration: 7min
completed: 2026-09-11
status: complete
---

# Phase 2 Plan 02: Référence CLI alignée sur le parseur — ancrage page → parseur et scanner partagé

**`tests/test_docs_cli.py` ancre la page CLI livrée sur le parseur réel (huit sous-commandes par sondes d'argv complets, quatre options globales, trente options d'`optimize`, alias `cache` ≡ `db` modulo la clé `command`, bloc « Source de vérité »), pendant que `tests/conftest.py` devient le seul porteur du scanner de blocs et des helpers de section — dix mutations dans des copies jetables prouvent que chaque contrat mord.**

## Performance

- **Duration:** 7 min
- **Started:** 2026-09-11T12:19:54Z (fin du plan 02-01, début de la vague 2)
- **Completed:** 2026-09-11T12:26:25Z
- **Tasks:** 2 / 2
- **Files modified:** 3 (`tests/test_docs_cli.py` créé — 415 lignes ; `tests/conftest.py` +93 lignes — 228 ; `tests/test_docs_code_anchor.py` +10/−53 lignes — 255)

## Accomplishments

- **Un seul scanner de blocs, prouvé par mutation.** Le scanner et les helpers de section ont été **déplacés** (jamais recopiés) dans `tests/conftest.py`, exposés par les fixtures `lignes_de_code`, `sections` et `section`. Les deux mutations de non-régression de la tâche 1 mordent : retirer `--offline` de la copie de `docs/installation.md` fait échouer `test_cli_examples_of_installation_page_parse` en nommant `installation.md` **et** le drapeau, et renommer « Source de vérité » fait échouer `test_sources_de_verite_exist` avec `AssertionError: installation.md … introuvable` — D-13 survit donc au déplacement.
- **`_section` exige désormais la page.** Aucune valeur par défaut : `_section("## A\nx", "## A")` lève `TypeError: _section() missing 1 required positional argument: 'page'`. Un appelant ne peut plus perdre le nom de la page en silence (D-13, D-31).
- **Zéro écart de comportement sur la page d'installation.** Les assertions des huit tests de `tests/test_docs_code_anchor.py` sont inchangées au caractère près ; seules cinq signatures reçoivent une fixture et leurs appels passent `PAGE`. La suite complète passe de **158 à 163 passed** (5 tests ajoutés) avec l'interpréteur épinglé.
- **Les trente options d'`optimize` sondées avec leur valeur d'essai.** Mesure : les 30 sondes sont acceptées, la table de la section `## optimize` en cite exactement 30, et le sous-parseur en refuse une seule forme — celle d'une option inventée. La sonde tri-état héritée de la phase 1 aurait déclaré `--jet` inventée (Pitfall 7) : la valeur d'essai épinglée est ce qui évite le faux négatif.
- **Le mode d'échec CR-01 est fermé là où il subsistait.** Une cinquième option globale inventée dans la table `## Options globales` fait rougir la suite : la mutation insère `| --serve | … |` et l'échec nomme `--serve`, accepté par aucune des trois formes d'argv essayées.
- **L'alias `cache` prouvé par le parseur, pas par du texte.** Égalité des espaces de noms modulo `command` pour les cinq sous-commandes (`status`, `stats`, `sync`, `fill`, `clear`), **et** constat que chaque espace brut porte bien `command == db` ou `cache` : les deux vues sont nécessaires (l'égalité brute de `vars()` est toujours fausse).
- **Anti-duplication de D-20 mesurée dans la forme que la page emploie.** La mutation insère `Forcer la synchronisation complète` (forme **accentuée**) dans la copie de `## cache` ; la comparaison normalisée des deux côtés fait rougir l'assertion avec le motif `dupliqu`. Un contrôle brut sur des littéraux non accentués serait resté vert sur cette dérive.
- **Dix mutations, dix morsures, aucune écriture dans `docs/`.** Les deux mutations de la tâche 1 et les huit mutations étiquetées de la tâche 2 ont toutes été exécutées dans des copies `mktemp -d` ; `git status --porcelain -- docs` reste vide, `docs/` est exactement ce que 02-01 a livré.

## Mutation battery (résultats mesurés)

| Mutation (copie jetable) | Motif attribué | Verdict mesuré |
|--------------------------|----------------|----------------|
| T1 — `--offline db status` → `db status` dans la copie de `docs/installation.md` | `installation.md` + `--offline` | `mutation detectee : drapeau hors-ligne retire, echec nommant installation.md et le drapeau` |
| T1 — `## Source de vérité` → `## Source renommee` (copie de la page d'installation) | `installation.md` + `introuvable` | `mutation detectee : section renommee, echec du helper partage nommant installation.md` |
| T2 — jetons épinglés renommés dans la page (`--top-k` → `--candidats-top`, `--timeout` → `--delai-http`) | `--candidats-top` | `mutation detectee` |
| T2 — table globale : ligne `--serve` inventée | `--serve` | `mutation detectee` |
| T2 — toutes les lignes de tableau supprimées | `aucune option` | `mutation detectee` |
| T2 — sous-commande `cache` renommée dans la page | `introuvable` | `mutation detectee` |
| T2 — description de `db` dupliquée dans `## cache` (forme accentuée) | `dupliqu` | `mutation detectee` |
| T2 — dérive du parseur (`self-test`, `--force-sync`, `--top-k`, `cache` retiré) | `self-test` | `mutation detectee` |
| T2 — chemin cité absent du dépôt (`cli-inexistant.py`, copie **produit**) | `cli-inexistant.py` | `mutation detectee` |
| T2 — jeton `build_parser()` retiré de la section Source de vérité | `build_parser` | `mutation detectee` — voir « Limite de lecture » ci-dessous |
| Contrôle de discrimination, copie « sans » **non mutée** | 7 des 8 motifs absents (0 ligne chacun) | `mutation detectee` pourtant vrai pour `build_parser` (3 lignes) : verdict non discriminant dans cette copie |
| Contrôle de discrimination, copie « produit » **non mutée** | suite verte (`5 passed`) | 0 occurrence de `build_parser` |
| Mutation `build_parser()` re-mesurée sur la copie **produit** | `build_parser` | `1 failed, 4 passed`, puis `mutation detectee` — verdict discriminant obtenu |

**Limite de lecture des copies jetables (mesurée, et corrigée par la mesure).** Six des huit mutations ne copient que `docs/` et `tests/` : dans ces copies, le contrôle d'existence des chemins rougit **par construction**, l'arbre produit n'y étant pas. Le registre du plan affirmait qu'aucun motif attribué ne pouvait venir de cette rougeur parasite ; la mesure le dément pour un seul motif : `build_parser` apparaît **trois fois** dans la sortie de la copie non mutée (pytest cite la source du test en échec, qui importe `build_parser as build_cli_parser`). Le verdict de cette mutation est donc non discriminant **dans une copie « sans »**, et il a été re-mesuré sur une copie incluant l'arbre produit, où la suite est verte avant mutation (`5 passed`) et rouge après (`1 failed`), le message nommant `build_parser()`. Les sept autres motifs sont absents de la copie non mutée (0 occurrence chacun) : leurs verdicts sont des verdicts sur la mutation. Les deux mutations de la tâche 1 sont, elles, exécutées sans arbre produit et leurs motifs (`installation.md`, `--offline`, `introuvable`) sont exactement ceux du message d'échec provoqué par la mutation.

## Task Commits

Chaque tâche a été commitée atomiquement :

1. **Tâche 1 : scanner de blocs et helpers de section déplacés dans `tests/conftest.py`** - `1ba8139` (test)
2. **Tâche 2 : ancrage des sous-commandes, des options globales et des options d'`optimize`** - `e7dc8a7` (test)

**Plan metadata:** voir le commit de complétion du plan (SUMMARY, STATE, ROADMAP, REQUIREMENTS, WINDOWS.md).

## Files Created/Modified

- `tests/test_docs_cli.py` (créé, 415 lignes, CRLF, UTF-8 strict sans BOM) — docstring de limites (D-26 et préfixe non ambigu), constantes `RACINE_DEPOT`, `PAGE`, `SOURCE_CLI`, titres de sections, `JETON_BUILD_PARSER`, `JETON_AIDE`, `DESCRIPTIONS_DB`, `JETONS_ALIAS`, `SONDES_SOUS_COMMANDES` (8), `SONDES_GLOBALES` (4), `SONDES_OPTIMIZE` (30), `SOUS_COMMANDES_DB` (5), helpers `_texte_page`, `_accepte`, `_espace_de_noms_brut`, `_espace_de_noms`, `_options_des_tables`, `_cite_token`, `_option_globale_acceptee`, `_argv_optimize`, `_option_optimize_acceptee`, et cinq tests.
- `tests/conftest.py` (modifié, +93 lignes, 228 lignes) — `TITRE_H2`, `DELIMITEUR_BLOC`, `_blocs_de_code` (balise conservée), `_lignes_de_code`, `_sections`, `_section(texte, titre, page)`, fixtures `lignes_de_code`, `sections`, `section`. Les fixtures existantes (`docs_dir`, `normalize`, `app`, `catalog`, `client`) sont inchangées.
- `tests/test_docs_code_anchor.py` (modifié, +10/−53 lignes, 255 lignes) — suppression des cinq définitions devenues doublons, cinq tests consommant les fixtures et passant `PAGE`, assertions inchangées.

## Decisions Made

- **Déplacement plutôt que recopie du scanner.** `tests/conftest.py` est le seul porteur : `grep -rn "_lignes_de_code" tests/` ne renvoie qu'une définition (plus ses usages par fixture). `tests/test_docs_structure.py` garde son `_section` local, de sémantique différente (retourne `None` si absent) et non touché.
- **La page reste un argument obligatoire du helper partagé.** Le message d'échec nomme la page **passée par l'appelant** ; les appelants de la page d'installation passent leur constante `PAGE` (`installation.md`) et le module CLI passe la sienne (`cli.md`). C'est ce qui rend le déplacement sans perte pour D-13.
- **Marqueurs d'alias adaptés à la page livrée.** La recherche attendait le jeton littéral `alias` dans la section `## cache` ; la page livrée par 02-01 déclare l'alias par « `cache` est le second nom de `db` … équivaut à `db <sous-commande>` ». Comme la page ne doit pas être modifiée pour faire passer un test, le contrôle exige l'un des marqueurs normalisés `alias` / `second nom` / `equivaut` : il reste falsifiable (supprimer la phrase d'équivalence le fait rougir) et il ne réécrit pas la page.
- **Deux vues de l'espace de noms.** `_espace_de_noms_brut` porte le constat `command == db` ou `cache` ; `_espace_de_noms` retire la clé pour comparer l'alias. Un accesseur unique aurait fait rougir le second constat sur une page correcte.
- **Présence d'un jeton vérifiée en jeton autonome.** `_cite_token` exige que le jeton ne soit ni précédé ni suivi d'un caractère de mot ou d'un tiret : la page cite `--force` (optimize) **et** `--force-sync` (global), une recherche de sous-chaîne aurait déclaré `--force` présente à tort.
- **Extraction limitée aux lignes de tableau.** `_options_des_tables` n'examine que les lignes dont le premier caractère significatif est `|` : le texte de la section `## optimize` cite `--offline`, option globale que le sous-parseur `optimize` refuse (Pitfall 10) — une extraction sur tout le texte aurait produit un faux échec sur une page correcte.
- **Constat cumulés, une seule assertion par test.** Mesuré pendant la planification et confirmé ici : avec une assertion par constat, l'ordre « présence d'abord, direction ensuite » rend inatteignables les motifs `--candidats-top` et `aucune option`, et la batterie rapporte `MUTATION NON DETECTEE` sur une implémentation correcte.
- **Barème de l'`actuals`.** 5686 jetons = chars/4 des caractères ajoutés au diff réalisé (`tests/test_docs_cli.py` 415 lignes, `tests/conftest.py` +93, `tests/test_docs_code_anchor.py` +10/−53 ; 22742 caractères ajoutés, 2376 supprimés). L'estimate du plan portait 48000 pour le travail d'agent complet (lecture de la recherche et du plan, mesures du parseur, dix mutations en copies jetables) : l'écart est réel et n'est pas arrondi pour se rapprocher de l'estimate.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Adéquation au livrable] Marqueurs d'équivalence de la section `## cache` au lieu du jeton littéral `alias`**

- **Found during :** tâche 2 (rédaction de `test_alias_cache_equivalent_a_db_dans_le_parseur`)
- **Issue :** le plan et `02-RESEARCH.md` (Pattern 5) attendaient que la section `## cache` de la page contienne le jeton normalisé `alias`. Mesure : la page livrée par 02-01 — dont le contenu est verrouillé par D-19/D-20 — déclare l'alias en prose (« `cache` est le second nom de `db` : la forme `cache <sous-commande>` équivaut à `db <sous-commande>` ») et n'emploie le mot `alias` que dans la section `## db` (table des sous-commandes `stats`/`fill`). Une assertion sur `alias` dans `## cache` aurait donc rougi sur une page correcte.
- **Fix :** le contrôle exige que la section `## cache` cite `db` **et** porte l'un des marqueurs normalisés `alias` / `second nom` / `equivaut` (comparaison normalisée des deux côtés, D-11). La page n'a pas été modifiée : c'est le test qui dérive son attente de la page mesurée, pas la page qui s'aligne sur un test.
- **Files modified :** `tests/test_docs_cli.py`
- **Verification :** `tests/test_docs_cli.py` est vert sur la page livrée (5 passed) ; supprimer la phrase d'équivalence ferait rougir le test (le marqueur est vérifié, pas supposé) ; `.planning/WINDOWS.md` porte l'entrée correspondante.
- **Committed in :** `e7dc8a7`

**2. [Rule 2 - Mesure] Verdict de la mutation `build_parser()` re-mesuré sur une copie incluant l'arbre produit**

- **Found during :** tâche 2 (exécution de la batterie de huit mutations)
- **Issue :** l'advisory du plan checker était exacte. Dans une copie jetable sans arbre produit, le module est rouge **par construction** (contrôle d'existence des chemins) et pytest cite la source du test en échec : la sortie d'une copie **non mutée** contient déjà trois occurrences de `build_parser`. Le motif `build_parser` cherché par la batterie était donc satisfait sans mutation, et le verdict `mutation detectee` de cette ligne ne prouvait rien de propre.
- **Fix :** le verdict a été re-mesuré sur une copie incluant l'arbre produit — suite **verte avant la mutation** (`5 passed`, 0 occurrence de `build_parser`), **rouge après** (`1 failed, 4 passed`) avec un message qui nomme littéralement `build_parser()`. Aucune assertion n'a été retirée ni affaiblie ; la limite de lecture est écrite ici et dans `.planning/WINDOWS.md`.
- **Files modified :** aucun (mesure et documentation) ; le module porte déjà le message qui nomme le jeton et la page.
- **Verification :** contrôle de discrimination des huit motifs exécuté sur les copies non mutées — sept motifs absents (0 ligne chacun), `build_parser` présent (3 lignes) dans la copie « sans » seulement ; copie « produit » non mutée : 0 occurrence et suite verte.
- **Committed in :** `e7dc8a7`

**Total deviations :** 2 auto-documentées (règle 2). Aucun écart de règle 1 (bogue), de règle 3 (blocage) ni de règle 4 (décision d'architecture) : aucun bogue rencontré, aucune dépendance installée, aucun paquet ajouté, aucune modification de `dofus_stuff/**` ni de `docs/`.

**Impact on plan :** aucun élargissement de périmètre et aucune assertion affaiblie. La première déviation adapte une attente à la page livrée (le plan interdit de modifier la page pour faire passer un test) ; la seconde renforce au contraire la preuve de morsure en la déplaçant vers une copie où la suite est verte avant mutation.

## Issues Encountered

- **En-tête de branche `main` (même situation que 01-01 à 01-04 et 02-01).** Le protocole d'exécution de l'agent interdit par défaut de committer sur la branche protégée : `git.base-branch --is-protected main` renvoie `true` et `.planning/config.json` n'a pas d'override `git.allow_default_branch_commits`, alors qu'il porte `git.branching_strategy: "none"` et que l'historique des deux phases est intégralement sur `main`. L'orchestrateur a dispatché cet exécutant comme **séquentiel sur l'arbre principal** : les deux commits y sont donc posés, conformément à la consigne de dispatch. Aucun `update-ref`, aucun `push`, aucun reset destructeur, aucun `git clean` ni `git stash` n'a été exécuté.
- **`sed -i` sur des copies jetables uniquement.** Les dix mutations écrivent dans des dossiers `mktemp -d` ; aucun fichier de `docs/` ni de `dofus_stuff/` du dépôt n'a été touché (preuve : `git status --porcelain -- docs` vide, `dofus_stuff/cli.py` inchangé).
- **Aucune base ouverte, aucun réseau.** `.data/dofus.sqlite3` porte toujours son horodatage d'origine (`2026-09-06 23:27`) : aucun test de ce plan n'ouvre la base locale ni ne contacte l'API.

## Known Stubs

Aucun. Les cinq tests contiennent des assertions réelles (aucune valeur codée en dur laissée en place « pour plus tard », aucun `skip`, aucun `TODO`) ; les listes épinglées portent des sondes mesurées, pas des attentes vides. Les trois assertions que le registre du plan déclare **non isolablement mutables** (section `## Source de vérité` absente — même chemin d'échec que la mutation de section de la tâche 1 ; égalité d'alias au sens strict — les deux branches sont construites par la même boucle ; acceptation stricte sans préfixe non ambigu — `argparse` accepte le préfixe d'une option réelle) sont déclarées avec leur raison mesurée dans la section « Mutation battery » ci-dessus et dans le module, pas silencieusement omises.

## Threat Flags

Aucune surface nouvelle par rapport au modèle de menaces du plan. Les mitigations du registre STRIDE sont appliquées comme écrites :

- **T-02-06 (option ou sous-commande inventée, high)** — chaque jeton épinglé est sondé sur `build_parser().parse_args` par un argv complet, et toute option citée par une table est sondée sur le parseur correspondant ; les refus sont nommés avec la page, la valeur attendue et `dofus_stuff/cli.py`.
- **T-02-07 (contrôle qui ne peut pas échouer, high)** — gardes non vides « aucune option » sur les tables des sections `## Options globales` et `## optimize` ; l'alias est prouvé par deux `parse_args` équivalents, jamais par du texte ; les constats sont cumulés pour que chaque motif attribué reste atteignable ; les huit verdicts de la batterie ont été contrôlés contre la sortie d'une copie non mutée.
- **T-02-08 (perte de la base locale, high)** — le module n'importe que `build_parser` : aucun `main()`, aucune sous-processus, aucune socket, aucun import de `Database` ni de `Catalog`. `db clear` et `cache clear` sont *parsés*, jamais exécutés ; l'horodatage de `.data/dofus.sqlite3` est inchangé.
- **T-02-09 (couverture perdue par déplacement de helper, medium)** — le déplacement du scanner et des helpers de section est suivi de deux mutations dans une copie jetable, toutes deux détectées (`installation.md` nommé, drapeau nommé, `introuvable`).
- **T-02-10 (information disclosure, low)** — les messages d'échec citent des chemins du dépôt et la racine résolue depuis `tests/`, jamais la valeur absolue d'un `--data-dir` ni un contenu de `.data/`.
- **T-02-SC** — aucune installation : le module n'utilise que `io`, `re`, `contextlib`, `pathlib` et `pytest`, tous déjà présents.

## User Setup Required

None - aucune configuration externe, aucun service, aucune variable d'environnement.

## Next Phase Readiness

Le module d'ancrage CLI et les helpers partagés sont livrés, et la suite complète est verte (**163 passed** avec `.venv/Scripts/python.exe -m pytest -q`, référence re-mesurée après ce plan). Ce que le plan suivant trouve sur disque :

- **02-03** peut ajouter la projection des blocs marqués `console` au scanner de `tests/conftest.py` : `_blocs_de_code` conserve déjà la balise d'ouverture (elle vaut `""` pour une clôture nue), il ne manque que la constante de balise et la projection `_lignes_exemple` prévues par le plan 02-03. Les huit lignes de commande de la page sont dans des blocs `console`, toutes acceptées par `build_parser().parse_args`.
- **02-03** peut s'appuyer sur les fixtures `lignes_de_code`, `sections` et `section` plutôt que de redéfinir un scanner : le seul porteur de ces helpers est `tests/conftest.py`, et une seconde définition les ferait diverger (leçon WR-04).
- **La garde destructrice (02-03)** dispose de ses points d'appui : la page cite `db clear` hors de tout exemple et `DESCRIPTIONS_DB` / `JETONS_ALIAS` montrent la forme des contrôles textuels normalisés retenus.
- **Limite honnête conservée (D-26)** : la complétude parser → page n'est pas revendiquée, et la limite de `argparse` sur le préfixe non ambigu d'une option réelle est écrite dans le module ; aucune assertion de ce plan ne dépend d'un nom de page que la phase ne livre pas (leçon WR-05).
- **Aucune modification de `dofus_stuff/**`, de `docs/`, de `README.md` ni de `.data/`.** `docs/` reste exactement ce que 02-01 a livré.

---

## Self-Check: PASSED

- `tests/test_docs_cli.py` : **FOUND** (415 lignes, CRLF, UTF-8 strict sans BOM, 5 tests verts)
- `tests/conftest.py` : **FOUND** (228 lignes, `_blocs_de_code`, `_lignes_de_code`, `_sections`, `_section`, fixtures `lignes_de_code`, `sections`, `section`)
- `tests/test_docs_code_anchor.py` : **FOUND** (255 lignes, huit tests récoltés, plus aucune définition locale des helpers déplacés)
- Commit `1ba8139` : **FOUND**
- Commit `e7dc8a7` : **FOUND**
- `./.venv/Scripts/python.exe -m pytest -q` : **163 passed**
- `git rev-list --count 7a9c49b..HEAD` : **2** (compte mesuré, pas narré)

*Phase: 02-r-f-rence-cli-align-e-sur-le-parseur*
*Completed: 2026-09-11*
