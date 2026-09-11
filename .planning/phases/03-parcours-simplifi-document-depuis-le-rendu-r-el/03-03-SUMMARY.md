---
phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
plan: 03
subsystem: documentation
tags: [markdown, pytest, flask-test-client, ast, ancrage-litteral-js, msgpack, dofusbook, localStorage, documentation-francaise]

# Dependency graph
requires:
  - phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
    provides: "docs/parcours-simplifie.md (les cinq sections precedentes, le bloc Source de verite et la ligne de retour) et tests/test_docs_parcours.py (helpers _lignes_du_corps, _statut, _touches, _attribut, _valeurs_tableau, constantes de titres dont TITRE_SAUVEGARDE), suite verte a 178 tests"
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "harnais documentaire partage (docs_dir, section, normalize) et invariants de docs/ (liens, sommaire, H1, encodage, comptage des couples)"
provides:
  - "docs/parcours-simplifie.md : la section « Sauvegarder et exporter », inseree avant « Source de verite » (saisies SAVE [NOM] / SAVES / DB de l'ecran de resultat, ecran SAV-01 et sa ligne de statut, limite de sauvegarde du navigateur dite honnetement, export Dofusbook avec la prysma exclue)"
  - "tests/test_docs_parcours.py : _entete, _champ_saisie, _litteral_js, _url_import, les constantes des deux ecrans / de la limite / de l'export, et les tests test_ecrans_de_sauvegarde_et_export (V8), test_sauvegarde_navigateur_et_export_dofusbook (V9, V10), test_aucun_post_db_sans_patch"
affects: [03-04]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
actuals:
  tokens: 7569     # chars/4 sur le diff realise (30 275 caracteres ajoutes, 0 retire)
  tasks: 2
  commits: 2       # MESURE : git rev-list --count 0030bbf9d4bac6e0add162111bf2ce9968225576..HEAD
  plan_head_before: 0030bbf9d4bac6e0add162111bf2ce9968225576

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (contrainte projet C1)
  patterns:
    - "Ancrage par lecture de litteral source quand le comportement n'est pas executable : les constantes du client de sauvegarde sont extraites du fichier JS a chaque execution, et la page doit citer cette valeur — le controle est nomme pour ce qu'il est (litteraux), jamais presente comme une preuve de comportement"
    - "Epreuve d'une surface publique pure : build_dofusbook_url appelee directement, charge utile decodee (base64 puis msgpack), et l'ordre des groupes volontairement non re-teste car deja prouve par tests/test_web.py:713-750 (D-12)"
    - "Ecran rendu par injection d'etat de session plutot que par un POST : le rendu du resultat est obtenu sans lancer le solveur et sans poster la saisie DB, qui ouvrirait un navigateur cote serveur"
    - "Garde de surete du harnais par ast sur le module lui-meme (aucun import de navigateur, aucun post de cmd=DB), plutot qu'une consigne en commentaire"
    - "Motif de morsure porte par une constante du module, jamais ecrit en clair dans la ligne d'assertion : pytest reproduit la ligne source du assert, un motif en clair y serait trouve sans qu'aucun constat soit produit"

key-files:
  created: []
  modified:
    - docs/parcours-simplifie.md
    - tests/test_docs_parcours.py

key-decisions:
  - "La section est rattachee aux deux ecrans qui l'exposent (D-38) : les libelles du resultat (SAVE [NOM], SAVES, DB), l'ecran SAV-01 (en-tete, corps d'attente, ligne de statut, champ cmd de 40 caracteres, touche ESC) et les libelles hydrates par le client (BACK LISTE, DB DOFUSBOOK, SAUVEGARDES PURGEES) sont lus sur le rendu ou sur la ligne du JS qui les porte ; aucune commande de fetcher.py n'est recopiee (D-37), et la section ne porte aucun bloc balise console."
  - "La limite de sauvegarde est ancree sur les valeurs du fichier JS lues a chaque execution (cle dofus-stuff-machine.saves, valeur de MAX_SAVES) : la page doit citer la valeur courante, donc passer MAX_SAVES a 50 rougit sans que la page change (D-42)."
  - "L'eviction est dite honnetement (ECR-5) : la section contient la tournure « les plus anciennes sont remplacees » et l'assertion refuse la tournure « 20 maximum » seule — exacte mais trompeuse, puisque la sauvegarde en trop remplace la plus ancienne sans message d'echec (terminal.js:294-318, shift silencieux)."
  - "Le controle du JavaScript est nomme comme un controle de LITTERAUX, dans le docstring du module et a la ligne de son constat : aucun moteur JS n'est disponible ici (ni localStorage, ni shift), donc l'eviction reelle reste non testee et le module ne pretend pas le contraire (T-13)."
  - "L'export est prouve par la surface publique pure build_dofusbook_url : 17 emplacements fournis, charge utile decodee de forme [caracs(51), points(51), niveau, flags, counts(10), ids], niveau respecte, sum(counts) == 16 et identifiant de la prysma absent des ids. L'ordre des dix groupes n'est PAS re-teste : il est deja prouve par tests/test_web.py:713-750, que le module cite en commentaire (D-12)."
  - "Le nombre d'emplacements exportes cite par la page est celui du calcul (sum(counts)), jamais un 16 ecrit de memoire ; l'URL d'import est lue sur l'attribut public du module par importlib et exigee entre accents graves, car c'est une adresse technique et non un lien externe (D-01)."
  - "Le rendu du resultat est obtenu en injectant optimize_result_lines dans la session, exactement comme tests/test_web.py:668-671 : aucune saisie n'est postee sur cet ecran, et la suite ne peut donc pas lancer de navigateur (T-12). Le comportement de DB reste couvert, patche, par tests/test_web.py:668."
  - "Le module porte sa propre garde ast interdisant tout import de webbrowser et tout appel dont l'argument nomme data est un dictionnaire litteral portant cmd=DB : la surete du harnais est verifiee, pas seulement commentee."

patterns-established:
  - "Pattern 1 : valeur de code citee par une page = extraction du porteur a chaque execution (motif epingle + message nommant le fichier et la ligne), jamais une constante ecrite de memoire"
  - "Pattern 2 : deux ecrans rendus puis leurs libelles exiges a l'ecran ET sur la page, avec un seul point d'assertion qui nomme page, libelle attendu et fichier de code"
  - "Pattern 3 : garde ast auto-referente (le module s'analyse lui-meme) pour interdire une action a effet de bord avant qu'elle n'existe"

requirements-completed: [SIMP-03]

coverage:
  - id: D1
    description: "docs/parcours-simplifie.md : la section « Sauvegarder et exporter » existe avant « Source de verite », cite les saisies du resultat (SAVE [NOM], SAVES), le texte d'attente et la ligne de statut de l'ecran des sauvegardes, et ne recopie aucune commande (aucun bloc console)"
    requirement: "SIMP-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_ecrans_de_sauvegarde_et_export"
        status: pass
    human_judgment: false
  - id: D2
    description: "L'ecran SAV-01 est rendu par le client de test Flask et ses libelles exiges : SAV-01 dans l'en-tete, CHARGEMENT DES SAUVEGARDES LOCALES… dans le corps, N OUVRIR | DEL N | PURGE OUI en tete de la ligne de statut, data-mode=saves, champ cmd de 40 caracteres, couple ESC/Retour"
    requirement: "SIMP-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_ecrans_de_sauvegarde_et_export"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 1 : 2/2 detectees (statut de /saves reformule, statut du resultat reformule), copie verte verifiee avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D3
    description: "L'ecran de resultat est rendu sans lancer le solveur (injection de optimize_result_lines) et sa ligne de statut porte ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB, avec data-mode=result ; aucune saisie DB n'est postee"
    requirement: "SIMP-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_ecrans_de_sauvegarde_et_export"
        status: pass
    human_judgment: false
  - id: D4
    description: "La limite de sauvegarde du navigateur est ancree sur les valeurs du fichier JS : la page cite la valeur courante de MAX_SAVES et la cle de stockage, donc passer MAX_SAVES a 50 ou renommer la cle rougit sans que la page change"
    requirement: "SIMP-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_sauvegarde_navigateur_et_export_dofusbook"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 2 : mutation max_saves detectee (motif « MAX_SAVES = 50 » dans le constat), copie verte verifiee avant mutation"
        status: pass
    human_judgment: false
  - id: D5
    description: "L'eviction est dite honnetement : la section porte la tournure « les plus anciennes sont remplacees » et l'assertion refuse « 20 maximum » seule ; les libelles du client (DB DOFUSBOOK, BACK LISTE, SAUVEGARDES PURGEES) sont exiges dans la page ET sur une ligne du fichier JS"
    requirement: "SIMP-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_sauvegarde_navigateur_et_export_dofusbook"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 2 : mutation tournure_fausse detectee (motif « 20 maximum »), copie verte verifiee avant mutation"
        status: pass
    human_judgment: false
  - id: D6
    description: "L'export Dofusbook est prouve par la surface publique pure : charge utile decodee de forme [caracs(51), points(51), niveau, flags, counts(10), ids], niveau respecte, sum(counts) == 16, identifiant de la prysma absent des ids ; la page cite le nombre calcule, dit que la prysma n'est pas exportee et cite l'URL d'import du module entre accents graves"
    requirement: "SIMP-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_sauvegarde_navigateur_et_export_dofusbook"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 2 : mutations export_prysma (motif « nombre d'emplacements exportes mesure », constats reels 17 pour 17 et identifiant 999 present) et url_import (motif DOFUSBOOK_IMPORT_URL) detectees, copie verte verifiee avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D7
    description: "Le harnais ne peut pas lancer de navigateur : aucun import de webbrowser dans le module d'ancrage et aucun appel dont l'argument nomme data soit un dictionnaire litteral portant cmd=DB (garde ast auto-referente)"
    requirement: "SIMP-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_parcours.py#test_aucun_post_db_sans_patch"
        status: pass
    human_judgment: false
  - id: D8
    description: "Le comportement du navigateur (compteur de sauvegardes, eviction de la plus ancienne, purge, hydratation de la liste) n'est pas executable dans cet environnement : la page et le module le nomment comme une limite, et seul un lecteur avec un navigateur peut le constater"
    requirement: "SIMP-03"
    verification: []
    human_judgment: true
    rationale: "Aucun moteur JavaScript n'est disponible ici (ni localStorage, ni shift) et l'ajout de playwright ou node est interdit par la contrainte projet C1 : le test prouve que la page et le code ne divergent pas sur les constantes et les libelles, pas que le navigateur se comporte ainsi. La mesure de non-regression .data/ (plan 03-04) ne couvre pas ce point."

# Metrics
duration: 4 min
completed: 2026-09-11
status: complete
---

# Phase 3 Plan 03: Sauvegarder et exporter Summary

**Le critere 3 est tenu dans ses deux moities les plus desagreables : la limite de sauvegarde du navigateur est ancree sur les litteraux du fichier JS (valeur de `MAX_SAVES` et cle `dofus-stuff-machine.saves` extraites a chaque execution) avec l'eviction silencieuse dite honnetement — « 20 maximum » seule etant refusee par le test — et l'export Dofusbook est prouve pur (seize emplacements exportes, identifiant de la `prysma` absent des `ids`, URL d'import lue sur l'attribut public du module).**

## Performance

- **Duration:** 216 s ≈ 4 min pour les deux taches (mesure : `date +%s` 1789145855 → 1789146071, du garde de racine au vert de la batterie de la tache 2 ; la cloture SUMMARY puis STATE/ROADMAP suit)
- **Started:** 2026-09-11T16:57:35Z
- **Completed:** 2026-09-11T17:01:11Z (fin de la verification de la tache 2)
- **Tasks:** 2
- **Files modified:** 2 (0 cree, 2 modifies)

## Accomplishments

- `docs/parcours-simplifie.md` gagne la section « Sauvegarder et exporter », inseree **avant** « Source de verite » : les saisies annoncees par la ligne de statut du resultat (`SAVE [NOM]`, `SAVES`, `DB`), l'ecran `SAV-01` (texte d'attente `CHARGEMENT DES SAUVEGARDES LOCALES…`, ligne de statut `N OUVRIR | DEL N | PURGE OUI`, statuts hydrates `PAGE n/total — … | ESC` et `PAGE n/total — BACK LISTE | DB DOFUSBOOK | ESC MENU`, purge confirmee par `SAUVEGARDES PURGEES`), la limite du navigateur (**20** sauvegardes, cle `dofus-stuff-machine.saves`, **les plus anciennes sont remplacees** sans message d'echec) et l'export Dofusbook (**16 emplacements au plus**, la `prysma` **n'est pas exportee**, URL d'import en accents graves). Aucun bloc de commandes, aucun lien externe (D-37, D-01).
- `tests/test_docs_parcours.py` gagne le helper `_entete`, la lecture du champ de saisie (`_champ_saisie`), l'extraction des litteraux du JS (`_litteral_js`), la lecture de l'URL publique (`_url_import`), les constantes des deux ecrans et de la limite, et trois tests : `test_ecrans_de_sauvegarde_et_export` (V8), `test_sauvegarde_navigateur_et_export_dofusbook` (V9, V10) et `test_aucun_post_db_sans_patch` (garde ast auto-referente).
- Les deux ecrans sont **reellement rendus** : `GET /saves` (client neuf) donne l'en-tete `PGM: SAV-01`, le corps `CHARGEMENT DES SAUVEGARDES LOCALES…`, la ligne de statut `N OUVRIR | DEL N | PURGE OUI — ENTREE=VALIDER`, `data-mode="saves"`, le champ `cmd` en `maxlength="40"` et le couple `ESC`/`Retour` ; l'ecran de resultat est obtenu **sans lancer le solveur** en injectant `optimize_result_lines` (patron de `tests/test_web.py:668-671`) et porte `ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB — ENTREE=VALIDER` avec `data-mode="result"`. Aucune saisie n'est postee : le harnais ne peut pas ouvrir de navigateur.
- L'export est eprouve sur la surface publique pure : 17 emplacements fournis (les seize exportes plus `prysma`), charge utile decodee `[caracs(51), points(51), niveau=137, flags=0, counts(10), ids]`, `sum(counts) == 16`, identifiant `999` de la `prysma` **absent** des `ids`. L'ordre des dix groupes n'est pas re-teste : il est deja prouve par `tests/test_web.py:713-750`, cite en commentaire (D-12).
- **Six morsures** detectees sur une copie verte verifiee avant chaque mutation : statut de `/saves` reformule et statut du resultat reformule (tache 1, 2/2) ; `MAX_SAVES` porte a 50, tournure interdite « 20 maximum » ajoutee dans la page, `prysma` ajoutee au groupe des familiers, URL d'import modifiee dans le module (tache 2, 4/4). Pour la mutation de l'export, la sortie montre des constats reels (« 17 pour 17 emplacements fournis ; attendu 16 », « l'identifiant 999 de la `prysma` figure dans les identifiants exportes »), pas un echo de la ligne source.
- Suite complete verte : **181 passed** (178 avant ce plan + 3 nouveaux). `.data/dofus.sqlite3` intact apres chaque tache.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : la section « Sauvegarder et exporter » et le controle des deux ecrans qui les exposent** - `f96f9bf` (feat)
2. **Tache 2 : la limite de sauvegarde ancree sur les litteraux du JS et l'export Dofusbook ancree sur sa surface publique** - `a51939e` (feat)

**Plan metadata:** `HEAD` apres le commit de cloture de ce plan (docs: complete plan).

_Note: `TDD_MODE=false` pour cette phase — aucun cycle RED/GREEN/REFACTOR n'etait requis. `MVP_MODE=true`, `ISOLATION=none` : execution sequentielle sur l'arbre principal, les mises a jour STATE/ROADMAP sont faites par cet executeur._

## Files Created/Modified

- `docs/parcours-simplifie.md` (modifie, +22 lignes, 199 lignes au total, CRLF, UTF-8 sans BOM) — la section `## Sauvegarder et exporter` et ses trois sous-sections, inseree entre `## Correspondance des libelles` et `## Source de verite`, qui reste la derniere section avant la ligne de retour au sommaire.
- `tests/test_docs_parcours.py` (modifie, +556 lignes, 1 879 lignes au total, CRLF, UTF-8 sans BOM) — imports (`base64`, `importlib`, `msgpack`, `build_dofusbook_url`), le paragraphe de limite nommee (controle de litteraux) dans le docstring, les constantes des deux ecrans (`ECRAN_SAUVEGARDES`, `ATTENTE_SAUVEGARDES`, `STATUT_SAUVEGARDES`, `STATUT_RESULTAT`, `TOUCHES_SAUVEGARDES`, `MODE_*`, `CHAMP_SAUVEGARDES`, `FRAGMENTS_PAGE_SAUVEGARDE`, `BALISE_COMMANDE`, `SESSION_RESULTAT`, `LIGNES_RESULTAT_INJECTE`), les constantes de la limite et de l'export (`MOTIF_SAVES_KEY`, `MOTIF_MAX_SAVES`, `LIGNE_*`, `TOURNURE_*`, `LIBELLES_JS_SAUVEGARDE`, `MOTIF_EMPREINTE_EXPORT`, `SLOTS_EXPORT`, `NOMBRE_*`, `ID_PRYSMARADITE`, `NIVEAU_EXPORT`), les helpers `_entete`, `_champ_saisie`, `_litteral_js`, `_url_import` et les trois tests.

## Decisions Made

- **Rattachement aux ecrans (D-38).** La section derive des libelles **rendus** : ligne de statut du resultat, ecran `SAV-01` (en-tete, corps, statut, coquille, champ, touche) et libelles hydrates par le client (`BACK LISTE`, `DB DOFUSBOOK`, `SAUVEGARDES PURGEES`) exiges aussi sur la ligne du fichier JS qui les porte. Aucune commande de `fetcher.py` n'est recopiee (D-37) et la section ne porte aucun bloc balise `console`.
- **Aucune constante ecrite de memoire (D-42).** La valeur de la limite et la cle de stockage sont extraites du fichier JS a chaque execution ; le nombre d'emplacements exportes vient de `sum(counts)` de la charge utile decodee ; l'URL d'import est lue sur l'attribut public du module par `importlib`. Chaque message d'echec nomme la page, la valeur attendue et le fichier de code.
- **Eviction honnete (ECR-5, D-41).** La page dit que la sauvegarde en trop **remplace la plus ancienne sans message d'echec**, et le test refuse la tournure « 20 maximum » seule : c'est exact mais trompeur, puisque le code fait `shift()` silencieusement (`terminal.js:294-318`).
- **Le nombre « 16 » est un calcul, pas une valeur recopiee.** La page cite le total mesure a chaque execution ; l'ordre des dix groupes n'est pas re-teste, il l'est deja par `tests/test_web.py:713-750`, que le module cite en commentaire au lieu de le dupliquer (D-12).
- **Champ de saisie lu dans sa balise.** `_champ_saisie` lit les attributs **dans** la balise `<input class="field">` ; une recherche libre de `name="..."` aurait trouve d'abord le `<meta name="viewport">` de l'en-tete HTML (piege mesure a l'ecriture, pas suppose).
- **Motif de morsure en constante.** `MOTIF_EMPREINTE_EXPORT` et les tournures epinglees sont portees par des constantes du module, jamais ecrites en clair dans la ligne d'assertion : pytest reproduit la ligne source du `assert` dans sa sortie, un motif en clair y serait trouve meme si aucun constat n'etait produit (la morsure cesserait d'etre discriminante). Les constantes de tournure ne doivent pas non plus etre un fragment deja present dans la ligne d'assertion.
- **Surete du harnais.** La garde `ast` `test_aucun_post_db_sans_patch` interdit tout import de `webbrowser` et tout appel dont l'argument nomme `data` porte un dictionnaire litteral `cmd=DB` (comparaison insensible a la casse, la route repliant la saisie avant d'ouvrir le navigateur). Le comportement de `DB` reste couvert, patche, par `tests/test_web.py:668`.
- **La page ne promet pas ce qu'elle ne peut pas prouver.** Elle ne decrit pas le chemin d'echec de l'ouverture du navigateur (l'adresse y est coupee a 100 caracteres : une phrase « recopiez cette adresse » serait fausse), ne fige aucune valeur volatile et n'annonce aucun comportement JS comme mesure.

## Deviations from Plan

### Auto-fixed Issues

None — le plan a ete execute comme ecrit. Aucune regle 1, 2, 3 ou 4 n'a ete declenchee : aucune ecriture sous `.data/`, aucun solveur lance hors fixture, aucune dependance ajoutee, aucun chemin `dofus_stuff/**` modifie, aucun secret, aucun reseau. Les quatre blocs `<verify>` du plan (deux passes du module, deux batteries de morsures sur copie verte, une passe de la suite complete) ont tous ete executes et sont cites ci-dessus.

### Non-deviations worth recording

- **La fixture `app` n'est pas consommee par `test_sauvegarde_navigateur_et_export_dofusbook`.** Le plan ecrit la signature `(app, docs_dir, section, normalize)` ; ce controle ne rend aucun ecran (les deux ecrans qui exposent la sauvegarde et l'export sont rendus par `test_ecrans_de_sauvegarde_et_export`) et la fixture a donc ete retiree de la signature, comme la fixture `section` l'a ete au plan 03-01. Le test, son nom, ses constats et son assertion unique sont inchanges.
- **Un paragraphe de la section decrit les statuts hydrates par le client** (`PAGE n/total — N OUVRIR | DEL N | PURGE OUI | ESC`, `PAGE n/total — BACK LISTE | DB DOFUSBOOK | ESC MENU`, `SAUVEGARDES PURGEES`). C'est ce qui rend verifiables les trois libelles requis par la tache 2 (« exiges dans la page **et** sur une ligne du fichier JS ») : la page doit nommer ces libelles pour que le controle bidirectionnel ait un sens (patron `LIBELLES_SOURCE`).
- **L'enumeration des seize emplacements exportes** (six Dofus, deux anneaux, amulette, ceinture, bottes, coiffe, cape, arme, bouclier, familier) vient des commentaires de `_GROUP_SLOTS` (`dofus_stuff/web/dofusbook_export.py:26-37`) ; elle accompagne le nombre mesure et ne fait que deriver la table deja livree par le plan 03-02.
- **Imports ajoutes au module** (`base64`, `importlib`, `msgpack`, `build_dofusbook_url`) : tous en stdlib ou deja dependance du produit, l'importation de `build_dofusbook_url` servant aussi a ce que la cloture transitive de la garde `ast` existante traverse ce module pur.

## Issues Encountered

- **Cible d'extraction de l'en-tete.** L'en-tete n'existe pas comme texte isole dans la reponse : `_entete` la decoupe sur le marqueur `<div class="row header" id="header-row">` (`screen.html:24`) et rend une chaine vide si le marqueur disparait, l'echec nommant alors l'identifiant d'ecran attendu et `routes.py:1280-1295`.
- **Le motif de l'URL d'import n'est pas pris pour un chemin de code.** La page cite `https://www.dofusbook.net/fr/equipement/dofus-stuffer/objets` entre accents graves : le motif `CHEMIN_CITE` du module (qui exige une extension `.py`, `.js`, …) ne l'attrape pas, donc le controle d'existence des chemins cites reste valide — verifie, la suite complete est verte.
- **Le caractere `…` entre dans la page avec `CHARGEMENT DES SAUVEGARDES LOCALES…`.** Le controle « aucun point de suspension » du plan 03-02 est **scope** a la section « Correspondance des libelles » : la suite reste verte sans exception (mesure, pas supposition).
- **Invariant des couples numero ↔ libelle.** La section ajoutee ne contient aucun motif `numero. Libelle` : la page compte toujours 23 couples exactement (`19` classes + `4` elements), verifie avant commit.
- **Fins de ligne.** Les deux fichiers modifies sont restes 100 % CRLF, UTF-8 sans BOM (mesure octet par octet apres chaque ecriture). La mutation `tournure_fausse` du plan ancre sur `^## Sauvegarder et exporter$` dans un fichier CRLF : mesure faite sur cet hote, le `sed` GNU (MSYS) lit et ecrit en mode texte et l'insertion prend, aucune adaptation du harnais n'a ete necessaire.
- Aucun blocage : ce plan n'exige ni geste humain, ni secret, ni acces reseau, ni synchronisation Dofusdude. `.data/dofus.sqlite3` n'a jamais ete ouvert (24 989 696 octets et `mtime_ns` 1788730056843137500 avant et apres chaque tache), la fixture `app` construisant sa propre base sous `tmp_path`.

## Known Stubs

None — aucun stub, aucun `TODO`, aucun test en `skip`, aucune `<verify>` non executee. Les quatre blocs `<automated>` du plan ont ete executes, dont les deux batteries de morsures (2/2 et 4/4), et la batterie de la tache 1 a ete rejouee apres la tache 2 pour verifier que le module agrandi n'a rien perdu.

## Threat Flags

Aucune surface nouvelle : ce plan n'ajoute aucun endpoint, aucune route, aucune dependance et aucun secret ; il etend une page `docs/` et un module de test qui lisent le depot et rendent des ecrans en processus. Les menaces du `<threat_model>` sont couvertes : T-12 (aucun post de `DB`, garde `ast` auto-referente, comportement couvert par `tests/test_web.py:668`), T-13 (le controle du JS est nomme comme un controle de litteraux, dans le docstring du module et dans le constat), T-14 (export mesure a chaque execution : `sum(counts) == 16` et identifiant de la `prysma` absent des `ids`), T-15 (la valeur citee par la page est comparee a celle extraite du JS, donc `MAX_SAVES = 50` rougit), T-16 (aucune ecriture sous `.data/`, empreinte comparee apres chaque tache).

## Next Phase Readiness

- **Pret pour 03-04** : la page et le module sont en place ; les sections du plan 03-04 (`## Ce que l'outil suppose`, `## Ce que l'outil ne fait pas`) s'inserent **avant** `## Source de verite`, la ligne `[Retour au sommaire](sommaire.md)` restant la derniere.
- **Contraintes a honorer par le plan suivant** : ne pas ajouter de second exemplaire des couples des deux menus (le controle de la vague 1 en compte 23 exactement, et la page ne doit pas gagner de motif `numero. Libelle`), ne pas ajouter de ligne de tableau portant un libelle de slot hors de la section « Correspondance des libelles » sans mettre a jour `SLOTS_MESURE`, et savoir que le module **interdit** desormais de poster `DB` sans patcher `webbrowser.open_new_tab` (la garde `ast` le signalera).
- **Ce qui reste non teste et le sait** : le comportement du navigateur (compteur, eviction, purge, hydratation de la liste). Aucun moteur JS n'est disponible et `playwright`/`node` sont exclus (C1) : la page et le module le nomment comme une limite, et l'entree `D8` de la couverture route ce point vers une relecture humaine, jamais vers un feu vert automatique.
- **Aucun blocage.** `03-VALIDATION.md` reste a mettre a jour par `/gsd:validate-phase`, pas par cet executeur.

## Self-Check: PASSED

- `docs/parcours-simplifie.md` : FOUND (199 lignes, CRLF, UTF-8 sans BOM, `## Sauvegarder et exporter` avant `## Source de verite`, derniere ligne `[Retour au sommaire](sommaire.md)`)
- `tests/test_docs_parcours.py` : FOUND (1 879 lignes, CRLF, UTF-8 sans BOM, 12 tests verts dans le module)
- Commit `f96f9bf` : FOUND — feat(03-03) decrit la sauvegarde et l'export depuis les ecrans qui les exposent
- Commit `a51939e` : FOUND — feat(03-03) ancre la limite de sauvegarde sur le JS et l'export sur sa surface publique
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_parcours.py -q` : 12 passed
- `./.venv/Scripts/python.exe -m pytest -q` : 181 passed (178 avant ce plan)
- Batterie de morsures de la tache 1 : 2/2 detectees, copie verte avant chaque mutation ; rejouee apres la tache 2, toujours 2/2
- Batterie de morsures de la tache 2 : 4/4 detectees, copie verte avant chaque mutation
- `.data/dofus.sqlite3` : 24 989 696 octets, `mtime_ns` 1788730056843137500 — identique avant et apres chaque tache
- Commits mesures : `git rev-list --count 0030bbf9d4bac6e0add162111bf2ce9968225576..HEAD` = 2

---

*Phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el*
*Completed: 2026-09-11*

