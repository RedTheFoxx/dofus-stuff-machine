---
phase: 05-base-locale-hors-ligne-et-resynchronisation
plan: 02
subsystem: documentation
tags: [markdown, pytest, flask-test-client, ast-litteraux, copie-verte-avant-mutation, morsures, commandes-destructrices, refus-db-sync, creation-de-la-base, documentation-francaise, crlf]

# Dependency graph
requires: [05-01]
provides:
  - "docs/base-locale.md : les quatre sections des cas non evidents du critere 3 (le premier contact cree la base sur les deux surfaces, le refus de la synchronisation hors-ligne avec son message reel, l'ecran web de synchronisation qui contacte l'API meme hors-ligne) et la section des commandes destructrices du critere 4 (une ligne par commande, cible reelle de chacune, mise hors parcours) ; la page passe de 8 a 12 sections, la ligne de retour restant la derniere ligne non vide"
  - "tests/test_docs_base_locale.py : quatre tests de plus (9 au total) — test_le_premier_contact_cree_la_base, test_le_refus_de_la_synchronisation, test_la_synchronisation_web_contacte_l_api, test_commandes_destructrices — avec les lecteurs _routes_declarees, _litteraux_du_module, _litteraux_de_fonction, _constats_bloc_refus et _constats_effet_clear, et les sept motifs du plan (MOTIF_CREATION, MOTIF_ROUTE, MOTIF_REFUS, MOTIF_SYNCHRO_WEB, MOTIF_DESTRUCTRICES, MOTIF_EFFET, MOTIF_EXEMPLE)"
  - "Le critere 4 delimite au perimetre de la phase : la constante LIMITE_PERIMETRE et la docstring de test_commandes_destructrices declarent que le controle porte sur docs/base-locale.md et sur ce module, l'occurrence de README.md ligne 80 restant consignee pour la phase 6 (D-87) sans qu'aucun constat ne rougisse a cause d'elle"
affects: [05-03, verification-phase-5]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (88 000) est consigne tel quel : il mesure le pessimisme de l'estimate,
# pas un travail non fait (les trois taches sont livrees, 10/10 morsures detectees).
actuals:
  tokens: 11182     # chars/4 sur le diff realise (44 729 caracteres ajoutes, 2 fichiers, 3 commits)
  tasks: 3
  commits: 3        # MESURE : git rev-list --count 7c83f70e0d38ab91c240fa24887fff08ca1c85e0..HEAD
  plan_head_before: 7c83f70e0d38ab91c240fa24887fff08ca1c85e0

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; stdlib seulement (ast, re)
  patterns:
    - "Morsure sur copie verte avant mutation : chacune des dix derivees est jouee dans un repertoire temporaire (`mktemp -d`), jamais sur l'arbre reel ni sous `.data/`, et la copie est mesuree VERTE avant la mutation pour que la morsure prouve quelque chose (D-84)"
    - "Motif de morsure porte par une constante ASCII du module, jamais ecrit en clair dans une ligne d'assertion : pytest reproduit la ligne du `assert`, une valeur en clair y serait trouvee meme sans constat produit (regle posee au plan 03-03)"
    - "Les deux oracles d'une tranche verticale sont proteges : quand le code mute, l'exception (`OperationalError` cote ligne de commande, erreur remontee par la route sous `TESTING = True`) est convertie en CONSTAT portant le motif du controle, au lieu de remonter en traceback — sans quoi la morsure rapporterait `MUTATION NON DETECTEE` sur un module correct (lecon de la vague 1)"
    - "Un litteral de message est pinces comme constante du module et exige de DEUX sources : du code, lu par `ast` (faible : il dit ce qu'il ecrit), et du rendu ou de la page (fort). `main()` n'etant jamais execute, l'ecran de la ligne de commande n'a pas d'autre rendu observable (D-15, D-78)"
    - "Un fait de structure est lu par `ast` plutot que par le texte : le refus hors-ligne est un `if <args>.offline:` portant `return 1` dont AUCUN appel de synchronisation ne descend — le refus precede l'appel reseau (D-78)"
    - "Les chemins d'ecran cites entre accents graves sont exiges declares par les DECORATEURS `get`/`post` de `routes.py`, lus sur la liste de decorateurs des fonctions : `request.args.get(\"page\", 1)` n'est pas un chemin, et un decorateur `@bp.route(...)` hors ensemble ne peut pas etre cite par la page (D-76)"
    - "La reconnaissance d'une commande destructrice est faite LIGNE A LIGNE sur le texte entier de la page : chaque ligne porteuse doit avertir sur elle-meme, meme si une autre ligne de la page porte deja l'avertissement (D-80)"

key-files:
  created: []
  modified:
    - docs/base-locale.md
    - tests/test_docs_base_locale.py

key-decisions:
  - "Le lecteur `_routes_declarees` lit les decorateurs des fonctions (`ast.FunctionDef.decorator_list`) et non tout appel d'attribut nomme `get` ou `post` du fichier : sans cette precision, `request.args.get(\"page\", 1)` entrerait dans l'ensemble des chemins declares. La lecture reste strictement celle du plan (un appel dont la fonction est un attribut `get`/`post` et dont le premier argument est un litteral de chaine), et elle est plus etroite : la page ne peut citer qu'un chemin reellement declare."
  - "Le constat « ces commandes ne sont l'etape d'aucun parcours » porte MOTIF_DESTRUCTRICES, et les constats du bloc de commandes et des lignes d'exemple portent MOTIF_EXEMPLE. Le plan groupe la mise hors parcours et l'absence d'exemple sous un seul motif ; les separer fait dire a chaque constat ce qu'il controle, et la morsure `bloc_console_ajoute` (qui cherche « bloc de commandes ») reste portee par le constat de la balise."
  - "Le libelle `FICHIER :` de l'ecran web est exige par l'ensemble des libelles produits (`_libelles_produits`) et non par une recherche dans le corps entier : une recherche textuelle confondrait le libelle d'une ligne avec le nom d'un fichier cite en prose, et aurait exige d'ecrire le libelle en clair dans la ligne d'assertion."
  - "Les deux phrases de la tache 2 (message de refus de `db sync`, phrase du corps de confirmation de l'ecran de synchronisation) sont pinces comme constantes du module ; la comparaison de la phrase rendue passe par `normalize`, l'apostrophe sortant en `&#39;` dans le HTML (D-11), et la citation de la page est comparee apres la meme normalisation."
  - "Le module ne poste jamais vers `/db/sync` ni `/db/clear` : un quatrieme controle de `test_la_synchronisation_web_contacte_l_api` lit le module lui-meme par `ast` et refuse tout appel `post`. La garde de cloture du plan 05-01 refuse deja la paire de confirmation (`data={\"confirm\": ...}`) ; les deux controles sont complementaires et aucun POST n'est emis."
  - "`LIMITE_PERIMETRE` est une constante de texte et la docstring du test la CITE nommement, la citation etant elle-meme controlee : le perimetre du critere 4 est ecrit noir sur blanc dans le module, et un retrait de la citation rougit. Aucun message de constat ne mentionne `README.md` ; l'occurrence de `README.md` ligne 80 est consignee pour la phase 6 (D-87, Pitfall 8)."
  - "Les sections sont inserees par un script (`inserer_section.py`, hors du depot livre : `.gsd-tmp/`) qui refuse une page portant le marqueur `## Source de vérité` autrement qu'une fois, puis les deux fichiers sont ramenes en CRLF : les pages de `docs/` sont verifiees OCTET PAR OCTET par les controles des phases 1 a 5, un outil ecrivant en LF aurait fait rougir la suite avant tout commit."

patterns-established:
  - "Pattern 11 : un fait de code sans rendu observable (`main()` jamais execute) est prouve par trois ancrages qui se renforcent — le litteral lu par `ast`, la STRUCTURE du bloc (le `return 1` du refus, dont aucun appel reseau ne descend) et la sonde du parseur public sur la forme analysee"
  - "Pattern 12 : la portee d'un controle d'absence est ecrite dans le module (`LIMITE_PERIMETRE`) et citee par la docstring du test, verifiee par le test lui-meme : un controle dont le perimetre est implicite finit par rougir pour un fichier hors mandat"
  - "Pattern 13 : une commande destructrice est reconnue LIGNE A LIGNE, sa cible reelle etant distinguee de sa voisine — la meme famille de commandes qui vide un support different (`db clear` vide la base SQLite, `PURGE OUI` supprime les sauvegardes du navigateur) ne peut pas etre decrite par une phrase commune (Pitfall 7)"

requirements-completed: [BASE-03]

coverage:
  - id: D1
    description: "Le premier contact cree la base, et le fait est prouve hors de `.data/` sur les deux surfaces : `_print_db_status` sur un `Database(data_dir=tmp_path / \"absent_cli\")` cree le dossier puis le fichier et rend `Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0` ; `GET /db/status` sur une application dont `data_dir` pointe `tmp_path / \"absent_web\"` rend 200, cree le fichier et affiche `FICHIER :` ; la section cite `db status`, le chemin `/db/status` et `--offline`"
    requirement: "BASE-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_base_locale.py#test_le_premier_contact_cree_la_base (les deux oracles proteges, exception convertie en constat portant MOTIF_CREATION, base refermee par `_sortie_db_status`)"
        status: pass
      - kind: integration
        ref: "batterie de morsures 05-02 tache 1 : 2/2 detectees (creation retiree du code, chemin d'ecran invente dans la page), copie verte avant chaque mutation, 14 s"
        status: pass
    human_judgment: false
  - id: D2
    description: "Le refus de la synchronisation hors-ligne est cite avec son message reel et precede l'appel reseau : le litteral `Erreur : --offline incompatible avec db sync` est lu par `ast` dans `dofus_stuff/cli.py`, le bloc `if args.offline:` du `main` porte un `return 1` sans appel a `ensure_up_to_date` descendant, et `parse_args([\"--offline\", \"db\", \"sync\"])` rend `offline is True` et `db_command == \"sync\"` ; `main()` n'est jamais execute"
    requirement: "BASE-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_le_refus_de_la_synchronisation (litteral, structure du bloc de refus, sonde du parseur public, citation verbatim et marque de code de retour non nul dans la page)"
        status: pass
      - kind: integration
        ref: "batterie de morsures 05-02 tache 2 : 2/2 sur ce controle (message de refus renomme, bloc de refus desactive), copie verte avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D3
    description: "L'ecran web de synchronisation contacte l'API meme hors-ligne : l'appel `ensure_up_to_date` de `dofus_stuff/web/routes.py` porte l'argument nomme `offline` egal au litteral `False`, la phrase `CETTE OPERATION CONTACTE L'API DOFUSDUDE` et l'invite `CONFIRMER ? (O=OUI / N=NON)` sont lues dans l'ecran et retrouvees dans le corps rendu de `GET /db/sync`, la section cite la phrase et dit le cas hors-ligne, et le module n'emet aucun POST"
    requirement: "BASE-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_base_locale.py#test_la_synchronisation_web_contacte_l_api (rendu de GET /db/sync par le client de test, aucun POST emis, controle du module par ast)"
        status: pass
      - kind: integration
        ref: "batterie de morsures 05-02 tache 2 : 2/2 sur ce controle (offline=False remplace par True, phrase du corps de confirmation renommee), copie verte avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D4
    description: "Les deux commandes destructrices sont signalees sur la meme ligne que la commande et hors de tout parcours : la ligne 129 (db clear, alias de cache) porte une marque destructrice et nomme la base locale, la ligne 131 (PURGE OUI) porte une marque destructrice et nomme les sauvegardes du navigateur, la section dit que ces commandes ne sont l'etape d'aucun parcours, la page ne porte aucun bloc de commandes et aucune ligne d'exemple ne porte un jeton destructeur ; l'effet de chacune est lu dans le code sans etre execute (`DELETE FROM items`, `DELETE FROM meta` et aucun appel de suppression dans `Database.clear` ; libelle de `GET /saves` et traitement dans `dofus_stuff/web/static/js/terminal.js`)"
    requirement: "BASE-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_base_locale.py#test_commandes_destructrices (reconnaissance ligne a ligne, cibles distinctes, hors parcours, effet de clear par ast, libelle de rendu et fichier JS)"
        status: pass
      - kind: integration
        ref: "batterie de morsures 05-02 tache 3 : 4/4 detectees (bloc console ajoute, ligne porteuse sans avertissement, cible de la seconde commande confondue, litteral de suppression retire du code), copie verte avant chaque mutation, 25 s"
        status: pass
    human_judgment: false
  - id: D5
    description: "Le perimetre du critere 4 est declare dans le module et l'occurrence de `README.md` ligne 80 n'est pas concernee : `LIMITE_PERIMETRE` porte le perimetre, la docstring de `test_commandes_destructrices` la cite (citation controlee par le test), aucun constat ne mentionne le README, et la suite ne rougit pas a cause de lui"
    requirement: "BASE-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_commandes_destructrices (section 6 : citation de LIMITE_PERIMETRE dans la docstring) et `grep -n README tests/test_docs_base_locale.py` : aucune occurrence dans un message de constat"
        status: pass
      - kind: integration
        ref: "suite complete verte (214 passed) avec README.md ligne 80 laissee telle quelle — aucun controle de cette phase ne la juge (D-87, Pitfall 8)"
        status: pass
    human_judgment: false
  - id: D6
    description: "`.data/dofus.sqlite3` garde taille, `mtime_ns` et SHA-256 autour de la suite complete : les bases que ce plan ouvre viennent de `tmp_path` (dossier absent de la ligne de commande, dossier absent du web), aucune commande destructrice n'est executee, aucune synchronisation n'est lancee et le module ne poste rien"
    requirement: "BASE-03"
    verification:
      - kind: integration
        ref: "empreinte mesuree avant et apres chacune des trois suites completes : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b — identique"
        status: pass
    human_judgment: false

# Metrics
duration: 7min
completed: 2026-09-11
status: complete
---

# Phase 5 : Base locale, hors-ligne et resynchronisation — Plan 05-02 Summary

**La page `docs/base-locale.md` raconte maintenant les cas non evidents du critere 3 — le premier contact qui cree la base sur les deux surfaces, le refus de la synchronisation hors-ligne avec son message reel, l'ecran web qui contacte l'API meme hors-ligne — et les deux commandes destructrices du critere 4, chacune signalee sur sa ligne avec la cible qu'elle detruit reellement et hors de tout parcours. Chaque fait est adosse soit a un litteral lu par `ast`, soit a un corps rendu, soit a une sortie capturee : `main()` n'est jamais execute, aucun POST n'est emis, aucune commande destructrice n'est lancee, et dix derives epinglees font rougir la suite sur une copie verte avant mutation. `.data/dofus.sqlite3` est intact.**

## Performance

- **Duration:** 7 min entre le debut de session (21:36:24 UTC) et la fin du plan (21:43:43 UTC) ; 3 min 56 s entre le premier et le dernier commit de tache (mesure `git log --format=%cI` : 23:38:21 +02:00 -> 23:42:17 +02:00)
- **Started:** 2026-09-11T21:36:24Z
- **Completed:** 2026-09-11T21:43:43Z
- **Tasks:** 3
- **Files modified:** 2 (804 insertions, 0 suppression) — `docs/base-locale.md` (8/16/10 lignes par tache, 141 lignes au total), `tests/test_docs_base_locale.py` (204/289/277 lignes, 1 738 lignes au total)
- **Commits:** 3, zero fichier supprime (`git diff --diff-filter=D --name-only` sur les trois commits : vide)
- **Duree des batteries de morsures :** tache 1 : 14 s · tache 2 : 27 s · tache 3 : 25 s (D-84, cout assume et conforme aux ordres de grandeur annonces par le plan : 10-20 s puis 20-30 s)

## Accomplishments

- **Les quatre sections manquantes de la page sont livrees, et la page est complete du point de vue de ses criteres.** Elle passe de 8 a 12 sections de niveau 2 : `## Le premier contact crée la base`, `## La synchronisation refuse le mode hors-ligne`, `## L'écran de synchronisation du web contacte l'API`, `## Les commandes destructrices`, toutes inserees AVANT `## Source de vérité`, qui reste le dernier titre, `[Retour au sommaire](sommaire.md)` la derniere ligne non vide, 141 lignes en CRLF sans BOM, aucun bloc de code, aucun nombre de quatre chiffres ou plus.
- **Le premier contact est prouve sur les deux surfaces, hors de `.data/`, et l'oracle est protege.** `_print_db_status` sur un `Database(data_dir=tmp_path / "absent_cli")` jamais ouvert cree le dossier puis le fichier et rend `Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0` ; `GET /db/status` sur une application dont `data_dir` pointe `tmp_path / "absent_web"` rend 200, cree le fichier et porte le libelle `FICHIER :`. Un temoin sur la base peuplee de la fixture `app` prouve que ce libelle est celui du rendu reel, pas un libelle fantome.
- **Les deux oracles convertissent leur exception en constat, et c'est ce qui rend la morsure discriminante.** Quand la creation du dossier est retiree de `Database.open`, `sqlite3.connect` echoue (`OperationalError: unable to open database file`) et l'erreur remonte sous `TESTING = True` cote web : les deux appels sont enfermes dans un `try`, l'exception devient un constat portant `MOTIF_CREATION` (surface, exception, fichier producteur), et la morsure `creation_retiree` est detectee au lieu de mourir sur une trace. La base ouverte cote ligne de commande est refermee par `_sortie_db_status` (`db.close()` en `finally`) : sans cela, le nettoyage du dossier temporaire echoue sur Windows (`PermissionError [WinError 32]`).
- **Le refus hors-ligne est adosse a trois ancrages qui se renforcent** (Pattern 11) : le litteral `Erreur : --offline incompatible avec db sync` lu par `ast` dans `dofus_stuff/cli.py` ; la **structure** du refus — un `if args.offline:` portant un `return` de valeur 1, dont **aucun** appel a `ensure_up_to_date` ne descend, donc un refus qui precede l'appel reseau ; et la sonde publique `parse_args(["--offline", "db", "sync"])`, qui rend `offline is True` et `db_command == "sync"`. `main()` n'est jamais execute et la synchronisation n'est jamais lancee.
- **L'ecran web est adosse a l'appel et au rendu, sans jamais poster.** L'appel `ensure_up_to_date` de `routes.py` doit porter l'argument nomme `offline` egal au litteral `False` — c'est le fait qui prouve que le mode hors-ligne ne s'applique pas a cet ecran —, la phrase `CETTE OPERATION CONTACTE L'API DOFUSDUDE` et l'invite `CONFIRMER ? (O=OUI / N=NON)` sont lues dans l'ecran par `ast` **et** retrouvees dans le corps rendu de `GET /db/sync` apres normalisation (l'apostrophe sort en `&#39;`), et un quatrieme controle lit le module lui-meme par `ast` pour refuser tout appel `post`.
- **Les deux commandes destructrices sont reconnues ligne a ligne, avec la cible de chacune** (Pattern 13). `db clear` (et son alias de cache `cache clear`) est sur la ligne 129 : destructrice, elle vide la base locale, les deux instructions de suppression lues dans le code y sont citees, et la page dit que `le fichier n'est pas supprimé du disque`. `PURGE OUI` est sur la ligne 131 et dit qu'elle supprime les sauvegardes du navigateur — **pas** la base. Le controle exige l'avertissement sur **chaque** ligne porteuse, l'absence de tout bloc de commandes, l'absence de jeton destructeur dans toute ligne d'exemple, et la mise hors parcours des deux commandes.
- **L'effet de chaque commande est lu sans etre execute** (D-81) : `DELETE FROM items` et `DELETE FROM meta` sont exiges dans le corps de `Database.clear`, lu par `ast`, avec **aucun** appel de suppression (`APPELS_SUPPRESSION` reutilise) — le fichier est vide, jamais efface ; et la seconde commande est prouvee au rendu de `GET /saves` (ligne de statut `N OUVRIR | DEL N | PURGE OUI — ENTREE=VALIDER`) et par la lecture de `dofus_stuff/web/static/js/terminal.js` (la comparaison `upper === "PURGE OUI"` et l'appel `localStorage.removeItem(SAVES_KEY)`).
- **Le perimetre du critere 4 est ecrit dans le module et verifie par le test lui-meme** (Pattern 12) : `LIMITE_PERIMETRE` declare que le controle porte sur `docs/base-locale.md` et sur ce module, la docstring de `test_commandes_destructrices` la cite nommement, et cette citation est controlee. L'occurrence de `README.md` ligne 80 reste consignee pour la phase 6 : aucune occurrence du mot `README` n'existe dans un message de constat du module (`grep -n README` : la constante wave 1, les commentaires, la constante de perimetre et la docstring seulement).
- **Dix morsures sur copie verte avant mutation** (2 + 4 + 4), toutes detectees avec leur motif nomme — voir § Verification. Aucune n'a eu besoin d'etre corrigee pour mordre : les six `sed` et les quatre injections ont ete contre-mesures un par un (`verifier-les-mutations.sh`, hors depot), et chacun mute reellement sa cible.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : le premier contact cree la base (tranche verticale, `type="tracer"`)** — `b0ee16a` (feat)
2. **Tache 2 : le refus hors-ligne et l'ecran de synchronisation du web** — `482346c` (feat)
3. **Tache 3 : les commandes destructrices, sur leur ligne et hors de tout parcours** — `c382a60` (feat)

**Plan metadata:** `docs(05-02): complete les cas non evidents et les commandes destructrices` (voir le commit de metadonnees du plan, qui porte ce SUMMARY et la mise a jour de STATE/ROADMAP).

## Files Created/Modified

- `docs/base-locale.md` — **modifie** (8/16/10 lignes ajoutees, 141 lignes au total, 13 213 octets, CRLF sur les 141 lignes, UTF-8 sans BOM). Douze titres de niveau 2 dans l'ordre : `## Le fichier de la base`, `## Les catégories stockées`, `## La fenêtre de re-check de 24 heures`, `## Le mode hors-ligne du web`, `## Le mode hors-ligne de la ligne de commande`, `## L'état de la base en ligne de commande`, `## L'état de la base dans l'interface web`, `## Le premier contact crée la base`, `## La synchronisation refuse le mode hors-ligne`, `## L'écran de synchronisation du web contacte l'API`, `## Les commandes destructrices`, `## Source de vérité`. Aucun bloc de code (0 occurrence de triple accent grave), aucun nombre de quatre chiffres ou plus, aucun chemin absolu de poste, aucun jeton de brouillon ; la ligne de retour reste la derniere ligne non vide. Chemins d'ecran cites et exiges declares : `/db/status` (tache 1), `/db/sync` (tache 2).
- `tests/test_docs_base_locale.py` — **modifie** (204/289/277 lignes, 1 738 lignes au total). Quatre tests de plus (**9 au total**) — `test_le_premier_contact_cree_la_base`, `test_le_refus_de_la_synchronisation`, `test_la_synchronisation_web_contacte_l_api`, `test_commandes_destructrices` ; constantes de motif `MOTIF_CREATION`, `MOTIF_ROUTE`, `MOTIF_REFUS`, `MOTIF_SYNCHRO_WEB`, `MOTIF_DESTRUCTRICES`, `MOTIF_EFFET`, `MOTIF_EXEMPLE` (les sept du plan) ; constantes de contenu `MARQUES_CREATION`, `LIBELLE_FICHIER_RENDU`, `CHEMIN_ECRAN`, `MARQUES_HORS_LIGNE`, `MARQUES_CODE_RETOUR`, `MESSAGE_REFUS`, `PHRASE_SYNCHRO`, `INVITE_CONFIRMATION`, `COMMANDE_DESTRUCTRICE`, `JETON_PURGE`, `BALISE_COMMANDE`, `MARQUES_DESTRUCTRICES`, `MARQUES_BASE`, `MARQUES_SAUVEGARDES`, `MARQUES_HORS_PARCOURS`, `MARQUES_FICHIER_CONSERVE`, `SUPPRESSION_ITEMS`, `SUPPRESSION_META`, `COMPARAISON_PURGE`, `RETRAIT_SAUVEGARDES`, `LIMITE_PERIMETRE` ; lecteurs `_routes_declarees`, `_litteraux_du_module`, `_litteraux_de_fonction`, `_constats_bloc_refus`, `_constats_effet_clear` ; titres `TITRE_CREATION`, `TITRE_REFUS`, `TITRE_SYNCHRO_WEB`, `TITRE_DESTRUCTRICES` ajoutes a `TITRES_SECTION_ATTENDUS` (12 titres). Les gardes de cloture du plan 05-01 (`RACINES_INTERDITES`, `APPELS_SUPPRESSION`, `APPEL_PRODUIT`, `APPELS_SYNCHRO_PRODUIT`, `CONFIRMATIONS_INTERDITES`) sont reutilisees telles quelles, jamais recopiees ni adoucies.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocage : une fixture requise par l'action manquait a la signature du plan] `lignes_exemple` ajoutee a `test_commandes_destructrices`**

- **Found during:** Tache 3 (lecture de l'action avant ecriture)
- **Issue:** l'action impose d'exiger qu'« aucune ligne d'exemple (`lignes_exemple(texte)`) ne porte l'un des deux jetons », mais la signature epinglee par le plan (`test_commandes_destructrices(docs_dir, section, client, normalize)`) ne nomme pas la fixture `lignes_exemple` de `tests/conftest.py`. Sans elle, le controle ne peut pas etre ecrit, et le remplacer par une lecture maison du scanner de blocs reviendrait a recopier un helper partage (D-12).
- **Fix:** la fixture `lignes_exemple` est ajoutee a la signature ; le helper partage est consomme tel quel, jamais reecrit.
- **Files modified:** `tests/test_docs_base_locale.py` (meme commit que la tache 3)
- **Verification:** `./.venv/Scripts/python.exe -m pytest tests/test_docs_base_locale.py -q` -> `9 passed` ; la morsure `bloc_console_ajoute` est detectee avec son motif et le controle des lignes d'exemple reste atteignable.
- **Committed in:** `c382a60`

### Ecarts d'interpretation (documentes, jamais des affaiblissements)

- **`_routes_declarees` lit les decorateurs des fonctions** et non tout appel d'attribut nomme `get`/`post` du fichier : la lecture litterale de la phrase du plan aurait fait entrer `request.args.get("page", 1)` dans l'ensemble des chemins declares. La lecture retenue est strictement plus etroite (un chemin cite doit etre un chemin d'ecran declare) ; aucune assertion n'est adoucie pour autant, et la morsure `route_inventee` reste detectee.
- **Le constat de mise hors parcours porte `MOTIF_DESTRUCTRICES`, ceux du bloc de commandes et des lignes d'exemple portent `MOTIF_EXEMPLE`** : le plan groupe les deux regles sous un seul motif, mais chaque constat dit ainsi ce qu'il controle. La morsure `bloc_console_ajoute` (qui cherche « bloc de commandes ») reste portee par le constat de `BALISE_COMMANDE`.
- **Le libelle `FICHIER :` est exige via `_libelles_produits`** (l'ensemble des libelles d'un rendu) et non par une recherche dans le corps entier : la recherche textuelle aurait exige d'ecrire le libelle en clair dans la ligne d'assertion, ou elle serait trouvee par pytest meme sans constat produit (regle du plan 03-03).

---

**Total deviations:** 1 auto-fixed (Rule 3, une fixture manquante a la signature pour ecrire le controle exige par l'action) et 3 ecarts d'interpretation documentes, tous plus stricts que la lettre du plan. Aucun ecart de perimetre : aucun fichier de `dofus_stuff/**` n'a ete modifie (`git diff --stat` sur les trois commits : `docs/base-locale.md` et `tests/test_docs_base_locale.py` seuls), `pyproject.toml` est inchange, et rien n'a ete publie, deploye, achete ou supprime.
**Impact on plan:** aucun affaiblissement d'un controle pour obtenir le vert ; les quatre ecarts rendent les controles plus etroits ou plus lisibles, jamais plus permissifs.

## Issues Encountered

- **Un premier jet rouge, corrige dans la tache 1 (jamais commite)** : la verification du libelle `FICHIER :` comparait la chaine exacte `"FICHIER :"` a la liste des lignes du corps rendu, alors que la ligne rendue est `FICHIER : C:\...\dofus.sqlite3`. Le constat reel (« le corps rendu ... ne porte pas le libelle ») a ete obtenu, corrige par `_libelles_produits` (la partie avant ` :` de chaque ligne), et la suite est repassee verte avant le commit de la tache. Aucun vert n'a ete obtenu en adoucissant l'assertion.
- **Aucune morsure n'a eu besoin d'etre corrigee** : contrairement aux deux corrections de la vague 1, les dix morsures de ce plan ont ete discriminantes a la premiere execution. Les douze mutations ont malgre tout ete contre-mesurees une par une (`.gsd-tmp/verifier-les-mutations.sh`, hors depot) : `purge_cible_confondue` a d'abord ete controlee AVANT que la tache 3 n'ecrive la phrase cible (0 substitution, mesure honnete), puis recontrolee apres (1 substitution).
- **Fins de ligne** : les insertions de sections et les ajouts de code sont d'abord ecrits en LF ; les deux fichiers ont ete ramenes en CRLF apres chaque tache, controle a l'appui (141/141 et 1 738/1 738 lignes CRLF, BOM absent), avant tout commit. Aucun commit du plan ne porte un fichier en LF.
- **Aucun fichier hors perimetre touche** : `git status --short` ne montre, pour les trois commits, que `docs/base-locale.md` et `tests/test_docs_base_locale.py` ; `doc-agent.toml`, `.doc-agent/`, `gsd-auto*.toml`, `.planning/state.json` et `.gsd-tmp/` ne sont jamais indexes (D-91, indexation par chemin explicite).

## Verification (sorties reelles, verbatim)

**Suite complete et integrite de `.data/dofus.sqlite3`** (mesuree avant et apres chaque suite ; les mesures sont identiques) :

```
$ ./.venv/Scripts/python.exe -m pytest tests/test_docs_base_locale.py -q     # apres la tache 1
6 passed in 0.24s

$ ./.venv/Scripts/python.exe -m pytest -q                                    # apres la tache 1
211 passed in 4.20s
empreinte .data/ identique autour de la suite complete : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b

$ ./.venv/Scripts/python.exe -m pytest -q                                    # apres la tache 2
213 passed in 4.27s
empreinte .data/ identique autour de la suite complete : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b

$ ./.venv/Scripts/python.exe -m pytest tests/test_docs_base_locale.py -q     # apres la tache 3
9 passed in 0.33s

$ ./.venv/Scripts/python.exe -m pytest -q                                    # apres la tache 3
214 passed in 4.46s
empreinte .data/ identique autour de la suite complete : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b
```

**Morsures, tache 1 (2/2, 14 s) :**

```
mutation detectee (creation_retiree), motif "creation de la base par le premier contact"
mutation detectee (route_inventee), motif "chemin d ecran cite par la page"
morsures 05-02 tache 1 : 2/2 detectees (copie verte avant chaque mutation)
```

**Morsures, tache 2 (4/4, 27 s) :**

```
mutation detectee (refus_message_renomme), motif "refus de la synchronisation hors-ligne"
mutation detectee (refus_desactive), motif "refus de la synchronisation hors-ligne"
mutation detectee (synchro_web_hors_ligne_retire), motif "synchronisation web hors-ligne"
mutation detectee (corps_confirmation_renomme), motif "synchronisation web hors-ligne"
morsures 05-02 tache 2 : 4/4 detectees (copie verte avant chaque mutation)
```

**Morsures, tache 3 (4/4, 25 s) :**

```
mutation detectee (bloc_console_ajoute), motif "bloc de commandes"
mutation detectee (ligne_sans_avertissement_added), motif "commandes destructrices"
mutation detectee (purge_cible_confondue), motif "commandes destructrices"
mutation detectee (effet_clear_retire), motif "effet de la commande destructrice"
morsures 05-02 tache 3 : 4/4 detectees (copie verte avant chaque mutation)
```

**Contre-mesure des mutations** (chaque `sed` et chaque injection mute reellement sa cible ; script hors depot, copie temporaire) :

```
refus_message_renomme : original=0 mute=1
refus_desactive : if_args_offline=0 if_false=1
synchro_web : offline_false=0 offline_true=1
corps_confirmation_renomme : ancienne=0 nouvelle=1
bloc_console_ajoute : bloc=1
ligne_sans_avertissement : sauvage=1
purge_cible_confondue : ancienne=0 nouvelle=1
effet_clear_retire : delete_items=0 select_1=1
creation_retiree : mkdir=0 pass=1
route_inventee : jeton=1
```

**Octets et forme des fichiers livres :**

```
docs/base-locale.md 141 lignes, 141 CRLF, 141 LF, BOM False, 13213 octets
tests/test_docs_base_locale.py 1738 lignes, 1738 CRLF, 1738 LF, BOM False, 91524 octets
sections H2 : 12 | blocs de code : 0 | nombres a 4 chiffres : []
lignes porteuses : 129 (db clear, marque destructrice + base locale) et 131 (PURGE OUI, marque destructrice + sauvegardes du navigateur)
```

**Porte de retour de la tranche verticale (tache 1, `type="tracer"`) :** le `<verify>` complet a ete rejoue de bout en bout APRES le commit de la tache (mode standard, `human_verify_mode: end-of-phase`, verification entierement automatisee) : module `6 passed`, suite complete `211 passed` avec empreinte inchangee, batterie `2/2` detectee. Aucun point d'arret : la tranche verticale est verte de bout en bout avant toute tache d'expansion.

## Limites declarees (et ce qui n'est PAS revendique)

- **Deux verites sont en `backstop` dans les `must_haves` du plan et ne sont PAS revendiquees ici** : l'execution JavaScript de `PURGE OUI` dans un navigateur (aucun navigateur n'est lance, aucun JavaScript n'est compile : le controle s'arrete au libelle rendu par `GET /saves` et a la lecture de `dofus_stuff/web/static/js/terminal.js`, A2 de la recherche) et l'appreciation de redaction « aucune invitation » (la page ne presente aucune des deux commandes comme une etape ; c'est un jugement humain, et la prose libre de la page n'est verifiee par aucun test — D-85). Le module le declare dans sa docstring, et ce SUMMARY ne les declare pas vertes.
- **Ce qui est prouve pour le refus hors-ligne s'arrete au litteral, a la structure et a l'analyse des arguments** : la sortie reelle de `main()` sur `stderr` et son code de retour observe demanderaient d'executer le produit (D-15) ; ce plan ne le fait pas et ne le revendique pas.
- **La mesure d'empreinte locale de `.data/` autour des rendus appartient au plan 05-03** (critere 5) et n'est pas revendiquee ici ; ce plan mesure l'empreinte autour de la suite complete (avant/apres), pas autour de chaque rendu.
- **L'occurrence de `README.md` ligne 80 est hors du mandat de cette phase** (D-87) : elle est consignee dans `LIMITE_PERIMETRE` et pour la phase 6, proprietaire de la completude ; aucun controle de ce plan ne rougit a cause d'elle, et aucun constat ne la mentionne.

## Known Stubs

Aucun. La page ne porte ni marqueur de brouillon, ni `TODO`/`FIXME`, ni texte de remplacement : les quatre sections ajoutees par ce plan etaient les dernieres attendues par la phase, et chacune est vraie et ancree sur le code, le rendu ou une sortie capturee. Aucune valeur vide ne remonte a l'affichage.

## User Setup Required

None — no external service configuration required. Aucune dependance ajoutee (`pyproject.toml` inchange), aucun serveur lance, aucun socket ouvert, aucun reseau, aucune synchronisation Dofusdude, aucune commande destructive executee (ni `db clear`, ni `PURGE OUI`, ni le POST de confirmation de l'ecran de vidage), rien d'ecrit sous `.data/` ni sous `.doc-agent/`. Les bases que ce plan ouvre viennent de `tmp_path` : `Database(data_dir=tmp_path / "absent_cli")` et une application `create_app(data_dir=tmp_path / "absent_web", ...)`.

## Next Phase Readiness

- **Pret pour le plan 05-03 (vague 3, critere 5)** : la page est complete du point de vue de ses criteres (le plan 05-03 ajoute les controles d'ancrage et de cloture, pas de section) ; `tests/test_docs_base_locale.py` est a 9 tests verts et la suite complete a 214 tests verts.
- **Contrats deja poses et reutilisables par la vague 3** : `_routes_declarees` (chemins declares par les decorateurs `get`/`post`), `_litteraux_de_fonction` (litteraux d'une fonction lue par `ast`), `_constats_effet_clear` (effet lu sans execution), `MOTIF_VOLATILE` et `MOTIF_CRLF` (cloture de la page), `LIMITE_PERIMETRE` (perimetre declare, motif reutilisable pour un controle dont la portee doit etre ecrite), et le motif `MOTIF_ROUTE` lisible par tout controle qui cite un chemin d'ecran.
- **Contrat pour la verification de phase** : dix morsures rejouables sur copie verte avant mutation (aucune n'ecrit dans l'arbre de travail), `tests/test_docs_base_locale.py` a 9 tests verts, la suite complete a 214 tests verts sans `failed` ni `error`, aucune suppression de fichier, aucune ecriture hors de `tmp_path`, et l'empreinte de `.data/dofus.sqlite3` inchangee (`24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`).
- **Point d'attention pour la vague 3** : l'ordre de `TITRES_SECTION_ATTENDUS` doit rester celui de la page (12 titres, `## Source de vérité` en dernier) ; toute section ajoutee apres la vague 3 devra s'inserer avant ce dernier titre et la constante devra suivre le meme ordre.
- **Mesure utile pour la verification de phase : les filtres `-k` de la carte de verification de `05-VALIDATION.md` ne selectionnent pas tous un test.** Mesure reelle sur le module (9 tests) : `.venv/Scripts/python.exe -m pytest tests/test_docs_base_locale.py -q -k destructrices` -> `1 passed, 8 deselected` (il selectionne `test_commandes_destructrices`) ; `-k db_status` -> `9 deselected` ; `-k db_sync_offline` -> `9 deselected` ; `-k synchro_web` -> `9 deselected` (`test_la_synchronisation_web_contacte_l_api` ne contient pas la sous-chaine `synchro_web`). Les commandes `<automated>` du plan, elles, portent sur le module entier ou sur la suite entiere et sont vertes : la carte de verification doit donc lancer le module (ou les noms reels des tests) pour les trois lignes concernees, faute de quoi `pytest` sort en « no tests ran » (code 5) et non en echec. La meme imprecision existe sur les lignes du plan 05-01 (`-k fichier_categories` : `9 deselected`, mesure), elle n'a pas ete corrigee ici — `05-VALIDATION.md` n'est pas un artefact de ce plan.
- **Bookkeeping : `REQUIREMENTS.md` n'est pas modifie par ce plan, volontairement.** Le frontmatter de ce SUMMARY declare `requirements-completed: [BASE-03]`, mais les cases de `.planning/REQUIREMENTS.md` (BASE-01 a BASE-03, table de tracabilite « Pending ») restent telles quelles, comme le plan 05-01 les a laissees : la phase 5 revendique `BASE-03` en 05-02 **et** en 05-03, et la completude d'une exigence se constate a la fin de la phase (`/gsd:verify-work`), pas sur un plan isole. `STATE.md` (`completed_plans` 16 -> 17, position 2/3) et `ROADMAP.md` (05-02 coche) sont, eux, mis a jour par le commit de metadonnees de ce plan.

## Self-Check: PASSED

- `docs/base-locale.md` : FOUND (12 titres de niveau 2, 141 lignes CRLF, UTF-8 sans BOM)
- `tests/test_docs_base_locale.py` : FOUND (9 tests collectes)
- Commit `b0ee16a` : FOUND ; commit `482346c` : FOUND ; commit `c382a60` : FOUND ; base du plan `7c83f70` : FOUND ; 3 commits mesures par `git rev-list --count 7c83f70..HEAD`
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_base_locale.py -q` : `9 passed in 0.33s`
- `./.venv/Scripts/python.exe -m pytest -q` : `214 passed in 4.46s`
- Batteries de morsures : 2/2 + 4/4 + 4/4, copie verte verifiee avant chaque mutation
- Empreinte de `.data/dofus.sqlite3` : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique avant et apres chacune des trois suites completes
