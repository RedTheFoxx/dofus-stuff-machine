---
phase: 06-depannage-glossaire-completude-et-preuve-finale
plan: 04
subsystem: documentation
tags: [markdown, pytest, preuve-de-morsure, mutation-en-processus, copie-sous-tmp-path, garde-de-cloture-ast, empreinte-de-la-base, audit-de-perimetre, greffon-de-refus-reseau, documentation-francaise]

# Dependency graph
requires:
  - phase: 06-01
    provides: "tests/test_docs_depannage.py sur lequel porte la famille « messages du depannage » : la table MESSAGES (32 entrees, 3 modes de mesure dont source_literal et web_render), la fonction pure problemes_messages (bijection message <-> rubrique), et la sonde _produire, qui est exactement la sonde que la mutation ecran_muet_declare fait refuser"
  - phase: 06-02
    provides: "docs/glossaire.md et problemes_glossaire / problemes_parcours dans tests/test_docs_glossaire.py (familles « glossaire » et « index et parcours ») : la table des 27 termes avec leur employeur mesure, et le parcours conseille a permutation de libelles"
  - phase: 06-03
    provides: "tests/test_docs_completude.py sur lequel portent les familles « page livree » et « readme » : PAGES_EPINGLEES (les huit pages avec leur seuil de lignes non vides), problemes_pages_epinglees, problemes_couverture_index et problemes_readme (trois familles de constat du README : avertissement, renvoi, disparition)"
  - phase: 05-base-locale-hors-ligne-et-resynchronisation
    provides: "Le patron de la morsure sur copie verte avant mutation et de la garde de cloture auto-analysee par `ast` (phases 3 a 5), et le relevé de l'empreinte de la base du depot (taille, mtime_ns, SHA-256) tel que 05-03 puis 06-03 l'ont consigne"
provides:
  - "tests/test_docs_mutation.py : la preuve de morsure en processus (1035 lignes, 6 tests) — construction de la copie du depot sous `tmp_path` (`docs/`, `tests/`, `dofus_stuff/`, `README.md`, `GUIDE_WIZARD.md`, `pyproject.toml`), redirection de `RACINE_DEPOT` des trois modules d'ancrage vers cette copie, precondition de copie verte mesuree avant chaque mutation, table unique FAMILLES (5 familles, 14 mutations) avec les motifs attendus **lus** dans les modules d'ancrage, et garde de cloture auto-analysee par `ast`"
  - "Les cinq familles de derive declarees et prouvees mordantes, chacune par le controle de son module d'ancrage : page_livree (2 mutations), index_et_parcours (3), messages_du_depannage (4, dont la fermeture du trou museliere), glossaire (2), readme (3) — 14 mutations, aucune muette, aucun skip, aucun xfail"
  - "L'empreinte en lecture seule de la base du depot : CHEMIN_BASE, EMPREINTE_BASE (24989696, 1788730056843137500, e3793d64...) et test_la_base_du_depot_est_intacte, qui compare les trois valeurs lues en octets (`read_bytes()` + `hashlib.sha256`) sans jamais ouvrir la base par SQLite — l'import de `sqlite3` est refuse par la garde de cloture"
  - "La couverture des livrables mecanisee : test_chaque_livrable_est_couvert_par_une_mutation derive la liste des cibles de FAMILLES (jamais une seconde liste) et exige que chaque livrable de la phase y figure — les quatre pages et le module d'ancrage des messages"
  - "Les deux executions finales mesurees : la suite entiere (249 passed in 6.01s) et la suite sous le greffon de refus reseau et de piege `main()` (249 passed in 6.12s, six pieges armes avant la collecte), plus l'audit de perimetre rendu contre les huit chemins declares et le jeu tolere nomme"
affects: [verification-phase-6, milestone-documentation]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (85 000) est consigne tel quel : il mesure le pessimisme de l'estimate,
# pas un travail non fait (les trois taches sont livrees, 14/14 morsures detectees).
actuals:
  tokens: 12412     # chars/4 sur le diff realise (49 648 caracteres de patch, 1 fichier, 1 035 insertions)
  tasks: 3
  commits: 3        # MESURE : git rev-list --count e2fabdc..9cd7de2 = 3 ; le compte final est 4 avec le commit de metadonnees de ce plan (le dernier de la branche)
  plan_head_before: e2fabdcdb32c4d1e405edf007dc4feab8476bdb0

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; stdlib seulement (ast, hashlib, importlib.util, re, shutil, sys, pathlib)
  patterns:
    - "Morsure sur copie **redirigee** : la copie du depot vit sous `tmp_path` et `_rediriger` patche `RACINE_DEPOT` du module d'ancrage charge depuis cette copie — les fonctions de constats lisent la racine de leur module, donc sans cette redirection un controle lirait le depot reel et la mutation porterait sur une copie que personne ne lit (faux vert). Les trois modules (06-01, 06-02, 06-03) lisant deja `RACINE_DEPOT`, aucune adaptation d'un module d'ancrage n'a ete necessaire : la seule exigence de forme de l'hypothese du plan est tenue par les trois modules livres"
    - "Une copie fraiche par mutation, mesuree **verte avant** la mutation : le controle de la famille est appele sur la copie intacte et doit ne rien produire, sinon la morsure ne serait pas discriminante — la precondition est elle-meme un test (`test_la_copie_est_verte_avant_toute_mutation`), qui parcourt les treize contrats des trois modules d'ancrage sur la meme copie intacte"
    - "La batterie est **intolerante** a une mutation inerte : mesure faite avec un temoin (une mutation videe, faite sur une copie du module, hors depot) — le test echoue en nommant la famille, le fichier cible, le motif attendu et « constats reellement produits : aucun ». Un controle qui ne peut pas rougir est le defaut que ce plan existe pour exclure"
    - "Un motif attendu est **lu** dans le module d'ancrage par le nom de sa constante, jamais recopie d'un module a l'autre : `_motifs_attendus` refuse un nom introuvable (`MOTIF_MOTIF_INTROUVABLE`), sinon un renommage du constat dans le module d'ancrage laisserait la batterie verte"
    - "Un ecran muet est traite par une **sonde**, pas par une phrase : declarer comme rendu par l'interface web le message d'attente de la ligne de commande (`source_literal` -> `web_render`) fait refuser la sonde du module d'ancrage — le trou museliere est ferme par un controle, et la mutation qui le ferme porte le meme motif (`message non produit par le code`) que la mutation du litteral du produit"
    - "Une page est rendue **absente** par `Path.rename` vers `<copie>/../retires/`, jamais par `unlink`/`remove`/`rmdir`/`rmtree` : ces quatre noms d'appel sont refuses par la garde de cloture du module, qui s'auto-analyse par `ast` — une suppression litterale ferait rougir la garde sur une livraison conforme"
    - "Le `git status` du controle de non-modification du depot et l'audit de perimetre prennent leur decision **hors** de la boucle de lecture : `HORS` est accumule puis teste apres la boucle, jamais un `exit` execute dans un sous-shell de pipeline (lecon du plan 04-03, ou l'`exit 1` d'un `while read` alimente par un pipe ne pouvait pas faire echouer la commande)"
    - "Le greffon de preuve est **actif**, pas declaratif : `pytest_configure` l'arme avant la collecte et avant `tests/conftest.py`, et `verifie_arme()` tente les quatre appels reseau (chacun doit lever) puis verifie **par identite** que les deux noms `main` ne sont plus les fonctions du produit — appeler un `main()` non piege est precisement ce que la phase refuse"

key-files:
  created:
    - tests/test_docs_mutation.py
  modified: []

key-decisions:
  - "La morsure se prouve **en processus**, par les fonctions de constats des modules d'ancrage : le harnais interdit `subprocess` (et la garde de cloture de ce module refuse l'import), re-lancer pytest depuis un test serait un sous-processus, donc la copie vit sous `tmp_path` et la fonction de constats est appelee sur elle. La suite entiere est rejouee par une **commande d'executeur**, jamais par une assertion : le rapport en cite le compteur et la duree lus, et cette limite est ecrite dans la docstring du module."
  - "La mutation `ecran_muet_declare` porte sur la **declaration** de provenance (`tests/test_docs_depannage.py` de la copie) et non sur une page : la page de depannage reste exacte, c'est la declaration qui pretend un rendu que le produit ne produit pas. La sonde du module d'ancrage refuse alors avec `message non produit par le code` (le constat nomme les dix-neuf routes sondees et le message) : le trou museliere est ferme par un controle, et non par une note de rapport."
  - "Les trois mutations du README portent **deux** motifs : `MOTIF_README` (le motif de base du controle) et la famille de constat concernee (`renvoi non destructif manquant`, `avertissement manquant`, `commande de base disparue de la page`). La morsure est cherchee par appartenance de sous-chaine : exiger le motif de base seul aurait laisse passer une mutation qui rougit pour une autre raison que la famille visee."
  - "L'empreinte de la base du depot est ecrite **apres re-mesure sur le disque** par l'executeur, jamais d'apres le plan : `24989696`, `1788730056843137500`, `e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — les trois valeurs sont identiques a celles consignees par 06-03 et par 05-03, mesure faite avant d'ecrire la constante. La lecture passe par `read_bytes()` et `hashlib.sha256`, et l'absence de `sqlite3` dans le module est **refusee par la garde de cloture**, donc le controle et la regle `D-104` sont coherents."
  - "`test_chaque_livrable_est_couvert_par_une_mutation` **derive** ses cibles de `FAMILLES` : la table est la seule source du contrat, et une seconde liste de livrables aurait ete une seconde source de verite (D-14). La liste des livrables (`LIVRABLES_DE_LA_PHASE`) est le sujet du controle, ses cibles sont les fichiers reellement mutees."
  - "Le perimetre de la copie est **declare et limite** : la copie porte `docs/`, `tests/`, `dofus_stuff/`, `README.md`, `GUIDE_WIZARD.md` et `pyproject.toml`, et rien d'autre du depot — `.data/` n'est jamais copie, et aucune base du depot n'est approchee (les sondes du produit construisent les leurs sous `tmp_path`)."
  - "La garde de cloture de ce module **ne recopie pas** celle des phases precedentes : elle refuse les racines de base/processus/socket/reseau, l'appel a `main`, les appels du solveur et les quatre appels de suppression, et elle verifie en plus qu'aucun **litteral** des deux chemins destructifs (`/db/clear`, `/db/sync`) n'est ecrit hors de la constante qui les declare. Sa limite est ecrite : c'est une demonstration **statique et indirecte** — elle dit ce que ce module importe et appelle, et la preuve que le depot n'a pas bouge est l'audit de perimetre et l'empreinte de la base, pas cette garde."
  - "`tests/test_docs_mutation.py` ne porte **pas** `from __future__ import annotations` : la mutation `ecran_muet_declare` reecrit une ligne de `tests/test_docs_depannage.py`, pas ce module, et un import `__future__` ajoute apres une autre instruction serait une erreur de `compile` (patron herite des plans 05-01 et 06-01)."

patterns-established:
  - "Pattern 28 : une preuve de morsure **en processus** construit une copie du depot sous `tmp_path` et **redirige la racine** que lisent les modules d'ancrage (`module.RACINE_DEPOT = copie`) — sans cette redirection la mutation porterait sur une copie que personne ne lit, et la morsure serait un faux vert ; une copie **fraiche** par mutation, mesuree **verte avant** la mutation, est la precondition (elle est elle-meme un test sur les treize contrats)"
  - "Pattern 29 : une batterie de mutation **intolerante** est prouvee telle par un **temoin negatif** : une mutation inerte (une mutation videe de son effet) doit faire echouer le test en nommant la famille, le fichier cible, le motif attendu et « constats reellement produits : aucun » — un controle qui ne peut pas rougir est le defaut que la batterie existe pour exclure"
  - "Pattern 30 : un motif attendu est **lu** dans le module d'ancrage par le nom de sa constante (`getattr(module, nom)`), jamais recopie : un nom introuvable est un constat (`MOTIF_MOTIF_INTROUVABLE`), sinon un renommage du constat laisserait la batterie verte ; une mutation peut porter **deux** motifs (le motif de base du controle et la famille de constat visee), la morsure etant cherchee par appartenance de sous-chaine"
  - "Pattern 31 : un trou « museliere » (un ecran qui ne rend rien) est ferme par une **mutation de declaration** : declarer que l'interface web rend un message que la ligne de commande produit, et exiger que la sonde du module d'ancrage **refuse** — la mutation qui ferme le trou porte le meme motif (`message non produit par le code`) que la mutation du litteral du produit, donc une sonde muette est un constat et jamais un vert"
  - "Pattern 32 : deux jeux de chemins nommes pour un audit de perimetre — les **huit chemins de livrable** declares par les plans, et un **jeu tolere nomme** (outillage et bookkeeping d'execution) ; la divergence est ecrite dans le rapport, et la decision (`HORS` non vide, `dofus_stuff` non vide) est prise **apres** la boucle de lecture, jamais par un `exit` dans un sous-shell de pipeline"

requirements-completed: [GARD-04]

coverage:
  - id: D1
    description: "**Critere 4 du ROADMAP, mecanise** : chaque derive declaree est injectee sur une **copie** de `tmp_path` et le controle correspondant rougit **avec son motif**, en processus, sans sous-processus et sans toucher au depot — la copie est mesuree **verte avant** la mutation, et la racine des trois modules d'ancrage est redirigee vers elle"
    requirement: "GARD-04"
    verification:
      - kind: unit
        ref: "`tests/test_docs_mutation.py::test_la_copie_est_verte_avant_toute_mutation` (les treize contrats des trois modules d'ancrage sur une copie intacte) et `::test_chaque_derive_declenche_son_motif` ; `.venv/Scripts/python.exe -m pytest tests/test_docs_mutation.py -q` -> `4 passed in 1.80s` (tache 2), `6 passed` (tache 3)"
        status: pass
      - kind: integration
        ref: "`.gsd-tmp/06-04-morsures.txt` (rapport de mesure hors livrable) : `14 mutations mordantes sur 14 declarees`, chacune avec le motif observe — `page epinglee absente ou non fichier`, `page videe ou tronquee`, `page livree non indexee`, `parcours conseille`, `parcours conseille en liens`, `message non cite par sa rubrique`, `message cite non declare`, `message non produit par le code` (deux fois), `terme declare absent de la page`, `terme non employe par le fichier cite`, `invitation a detruire les donnees` avec (`renvoi non destructif manquant`, `avertissement manquant`, `commande de base disparue de la page`)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Les **cinq familles** de derive sont declarees et couvertes, chacune par au moins une mutation et un motif attendu : toute famille declaree sans mutation, et toute entree incomplete (module d'ancrage, fichier cible, fonction de constats, mutation, motifs), est un constat `livrable non couvert par une mutation` — jamais un silence"
    requirement: "GARD-04"
    verification:
      - kind: unit
        ref: "`tests/test_docs_mutation.py::test_les_familles_declarent_leurs_mutations` ; mesure de la table : `page_livree` 2 mutations, `index_et_parcours` 3, `messages_du_depannage` 4, `glossaire` 2, `readme` 3, soit 14 entrees"
        status: pass
    human_judgment: false
  - id: D3
    description: "Le **trou museliere** est ferme par un controle : l'ecran de sortie du produit (`GET /quit`) ne rend aucun message et n'accepte pas `POST` (mesure de `06-RESEARCH.md` : 405, aucune ligne de statut), donc une declaration qui lui preterait un message fait **refuser** la sonde du module d'ancrage (`message non produit par le code`) au lieu d'etre une note de rapport"
    requirement: "GARD-04"
    verification:
      - kind: integration
        ref: "mutation `_mutation_ecran_muet_declare` (dans la copie de `tests/test_docs_depannage.py` : `source_literal` -> `web_render` sur la ligne du message d'attente de la ligne de commande) -> constat `message non produit par le code : aucune des routes sondees (19 routes, de GET /version a GET /optimize/wizard/recap) ne porte : « Calcul en cours (CP-SAT)… » (famille calcul, mode web_render)`"
        status: pass
    human_judgment: false
  - id: D4
    description: "**GARD-03, volet donnees** : la base du depot est verifiee par une **empreinte en lecture seule** (taille, `mtime_ns`, SHA-256 lus en octets), jamais ouverte par SQLite, et le controle nomme les trois valeurs attendues et les trois valeurs lues"
    requirement: "GARD-03"
    verification:
      - kind: unit
        ref: "`tests/test_docs_mutation.py::test_la_base_du_depot_est_intacte` ; `.venv/Scripts/python.exe -m pytest tests/test_docs_mutation.py -q -k \"base_du_depot or couvert\"` -> `2 passed, 4 deselected in 0.03s` (tache 3) ; garde de cloture : aucun `sqlite3` importe dans le module"
        status: pass
      - kind: integration
        ref: "triple mesuree sur le disque avant d'ecrire la constante : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`, identique avant et apres les deux executions finales"
        status: pass
    human_judgment: false
  - id: D5
    description: "**GARD-04** : la verification s'execute avec `.venv/Scripts/python.exe -m pytest -q`, sans ecrire sous `.data/`, sans executer `main()` et sans ouvrir de connexion reseau — le greffon de refus reseau et de piege `main()` est arme **avant la collecte** et la suite qu'il encadre est verte"
    requirement: "GARD-04"
    verification:
      - kind: integration
        ref: "`PYTHONPATH=\"$PWD/.gsd-tmp\" .venv/Scripts/python.exe -m pytest -q -p no_net` (greffon `.gsd-tmp/no_net.py`, hors livrable) -> `249 passed in 6.12s`, ligne d'armement `greffon de preuve 06-04 : 6 pieges armes avant la collecte -> socket.socket, socket.create_connection, socket.socketpair, urllib.request.urlopen, dofus_stuff.cli.main, dofus_stuff.web.__main__.main` ; `verifie_arme()` -> `PIEGE ARME` (les quatre appels levents, les deux `main` verifies **par identite**, jamais appeles)"
        status: pass
      - kind: unit
        ref: "`tests/test_docs_mutation.py::test_garde_de_cloture_du_harnais` (auto-analyse par `ast`) et controle d'executeur par `ast` sur la batterie : `fonctions attendues manquantes : []`, `skip/xfail rencontres : 0`"
        status: pass
    human_judgment: false
  - id: D6
    description: "**Critere 5 du ROADMAP** : le rapport cite un **compteur reel** et une **duree reelle**, tous deux **lus** dans la sortie des deux executions finales (la suite entiere, puis la suite sous le greffon), et la triple d'empreinte de la base du depot avant et apres — aucun chiffre pre-rempli, aucun repris d'une session anterieure"
    requirement: "GARD-04"
    verification:
      - kind: integration
        ref: "`.gsd-tmp/06-04-suite-entiere.txt` -> `249 passed in 6.01s` ; `.gsd-tmp/06-04-suite-sans-reseau.txt` -> `249 passed in 6.12s` ; `AVANT taille=24989696 mtime_ns=1788730056843137500 sha256=e3793d64...` et `APRES` identique, comparaison faite par le bloc `<automated>` de la tache 3 (verdict : `base du depot intacte et identique avant et apres les deux executions`)"
        status: pass
    human_judgment: false
  - id: D7
    description: "La batterie est **intolerante** et aucun controle ne saute : une mutation qui ne mord pas fait echouer la batterie, aucun `skip` et aucun `xfail` n'existe dans le module, et la garde de cloture verifie qu'aucun litteral des deux chemins destructifs (`/db/clear`, `/db/sync`) n'est ecrit hors de la constante qui les declare"
    requirement: "GARD-04"
    verification:
      - kind: integration
        ref: "**temoin negatif** (mesure d'executeur, copie du module hors depot : `tests/test_docs_mutation_temoin.py` creee puis supprimee) : mutation de la page videe **videe de son effet** -> `1 failed` avec `morsure(s) non observee(s) sur une copie pourtant mesuree verte avant mutation : page_livree (docs/glossaire.md) : motif(s) attendu(s) absent(s) : page videe ou tronquee ; motifs lus dans test_docs_completude.py ; constats reellement produits : aucun`"
        status: pass
      - kind: unit
        ref: "`test_garde_de_cloture_du_harnais` : imports refuses (base, processus, socket, reseau), appel a `main` refuse, appels du solveur refuses, quatre appels de suppression refuses, litteraux destructifs hors constante refuses — 0 constat sur le module livre"
        status: pass
    human_judgment: false
  - id: D8
    description: "L'audit de perimetre est rendu contre **deux jeux de chemins nommes** (les huit chemins de livrable declares par les quatre plans, et le jeu tolere d'outillage et de bookkeeping), `dofus_stuff/**` n'a pas bouge, et les commits sont locaux, par chemin explicite"
    requirement: "GARD-04"
    verification:
      - kind: integration
        ref: "bloc `<automated>` de la tache 3 -> `audit de perimetre : huit chemins de livrable declares, jeu tolere nomme (outillage et bookkeeping d'execution) ecarte, dofus_stuff/** absent` ; perimetre mesure : ` M .gitignore`, ` M .planning/config.json`, ` M tests/test_docs_mutation.py`, `?? .doc-agent/`, `?? .gsd-tmp/`, `?? .gsd/`, `?? .planning/state.json`, `?? doc-agent.toml`, `?? gsd-auto-rules.toml`, `?? gsd-auto.toml` ; `git status --porcelain -- dofus_stuff` vide"
        status: pass
      - kind: integration
        ref: "quatre commits locaux par chemin explicite : `41b6b54` (tache 1), `0d3ec3b` (tache 2), `9cd7de2` (tache 3), puis le commit de metadonnees de ce plan ; `git diff --diff-filter=D --name-only` vide sur l'intervalle (aucun fichier supprime)"
        status: pass
    human_judgment: false

# Metrics
duration: 22min
completed: 2026-09-12
status: complete
---

# Phase 6 : Depannage, glossaire, completude et preuve finale — Plan 06-04 Summary

**La documentation livree n'est plus seulement gardee par des controles verts : elle est accompagnee de la preuve que ces controles rougissent quand elle derive.** `tests/test_docs_mutation.py` (1035 lignes, 6 tests) construit une **copie** du depot sous `tmp_path`, redirige vers elle la racine que lisent les trois modules d'ancrage, mesure la copie **verte avant** chaque mutation, puis injecte **quatorze derives** reparties en **cinq familles** — page livree, index et parcours, messages du depannage (dont la fermeture du **trou museliere** par la sonde), glossaire, README — et exige que le controle de la famille rougisse **avec son motif**, lu dans le module d'ancrage. Les 14 mutations mordent (14/14), aucune famille n'est muette, aucun `skip`, aucun `xfail`. La suite finale est verte deux fois : `249 passed in 6.01s` (suite entiere) et `249 passed in 6.12s` (suite sous le greffon de refus reseau et de piege `main()`, six pieges armes avant la collecte), avec l'empreinte de `.data/dofus.sqlite3` identique **avant et apres** les deux executions : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`.

## Performance

- **Duration:** ~22 min (mesure : de l'horodatage de l'ecriture de l'affectation de ce plan, `2026-09-12T02:23:49` heure locale, au dernier commit de tache, `02:45:53` — soit **22 min 04 s** ; l'intervalle entre le premier et le dernier commit de tache est de **6 min 16 s**, de `02:39:37` a `02:45:53`). La passe a ete interrompue une fois par la compaction du contexte, pendant l'ecriture du module ; l'etat a ete repris de `.gsd-auto/`, sans rejouer un seul appel d'outil.
- **Started:** 2026-09-12T00:23:49Z (horodatage pris a l'ecriture de l'affectation, apres la lecture du plan et de la recherche)
- **Completed:** 2026-09-12T00:45:53Z (dernier commit de tache ; le commit de metadonnees ferme ce plan)
- **Tasks:** 3
- **Files:** 1 — un module cree (`tests/test_docs_mutation.py`, 1035 lignes, 6 tests) ; aucun fichier modifie, aucun fichier supprime.
- **Commits:** 4 (3 commits de tache + le commit de metadonnees de ce plan), **aucun fichier supprime** (`git diff --diff-filter=D --name-only` vide) ; diff cumule : `1 file changed, 1035 insertions(+)` (49 648 caracteres de patch).
- **Estimate vs actuals :** estimate `85 000` tokens, mesure `12 412` (chars/4 du diff realise) — l'estimate etait pessimiste d'un facteur ~6,8, comme les phases 5, 06-01, 06-02 et 06-03 l'ont consigne ; aucune tache n'a ete sautee pour autant (les trois taches sont livrees, 14/14 morsures detectees).

## Accomplishments

- **La morsure est prouvee sur une copie que le controle **lit vraiment** (D-97).** `_copie_du_depot` copie `docs/`, `tests/`, `dofus_stuff/`, `README.md`, `GUIDE_WIZARD.md` et `pyproject.toml` sous `tmp_path` — `.data/` n'est jamais copie — puis `_charger_modules` charge les trois modules d'ancrage **depuis cette copie** et `_rediriger` patche leur `RACINE_DEPOT`. Sans cette redirection, un controle lirait le depot reel, la mutation porterait sur une copie que personne ne lit, et la morsure serait un faux vert. Les trois modules livres par 06-01, 06-02 et 06-03 lisant deja `RACINE_DEPOT`, **aucune adaptation d'un module d'ancrage n'a ete necessaire** : la seule exigence de forme posee par l'hypothese du plan est tenue par les trois modules, et `files_modified` reste le seul module de ce plan.
- **La copie est mesuree verte avant chaque mutation, et c'est un test (D-97).** `test_la_copie_est_verte_avant_toute_mutation` parcourt les **treize contrats** des trois modules d'ancrage (`problemes_pages_epinglees`, `problemes_couverture_index`, `problemes_readme`, `problemes_messages`, `problemes_rubriques`, `problemes_page`, `problemes_renvois`, `problemes_budget`, `problemes_clavier`, la sonde `_produire`, `problemes_glossaire`, `problemes_page_glossaire`, `problemes_parcours`) sur une copie **intacte** et exige zero constat, et `test_chaque_derive_declenche_son_motif` **remesure** la copie fraiche avant d'appliquer chaque mutation. Une morsure sur une copie deja rouge ne prouverait rien : la precondition est donc une mesure, jamais une supposition.
- **Quatorze mutations mordent, chacune avec le motif de son module d'ancrage.** Mesure d'executeur (`.gsd-tmp/06-04-morsures.txt`, outil hors livrable) : `14 mutations mordantes sur 14 declarees`.
  - **`page_livree` (2)** — `docs/cli.md` renommee hors de `docs/` (jamais supprimee : la garde de cloture refuse `remove`/`unlink`/`rmdir`/`rmtree`) rougit avec `page epinglee absente ou non fichier` ; `docs/glossaire.md` reduite a son titre rougit avec `page videe ou tronquee : 1 ligne(s) non vide(s) ... attendu au moins 30`.
  - **`index_et_parcours` (3)** — la ligne d'index du glossaire retiree rougit avec `page livree non indexee` ; le libelle du parcours renomme rougit avec `parcours conseille` (le constat nomme « Glossaire detaille » comme libelle qui ne reprend aucun libelle d'index) ; l'entree numerotee convertie en lien Markdown rougit avec `parcours conseille en liens`.
  - **`messages_du_depannage` (4)** — la ligne du message de saisie requise retiree rougit avec `message non cite par sa rubrique` ; une ligne de message non declare inseree dans la rubrique de la base rougit avec `message cite non declare` (« MESSAGE INEXISTANT DU PRODUIT ») ; le litteral du produit renomme **dans la copie de `dofus_stuff/sync.py`** rougit avec `message non produit par le code` (la page ne bouge pas, c'est le produit qui derive) ; et `ecran_muet_declare` rougit avec le meme motif.
  - **`glossaire` (2)** — la ligne du terme `bouclier` retiree rougit avec `terme declare absent de la page` ; l'employeur de `panoplie` pointe vers `dofus_stuff/sync.py` (page **et** declaration mutees) et rougit avec `terme non employe par le fichier cite`.
  - **`readme` (3)** — les trois mutations portent `invitation a detruire les donnees` **et** la famille de constat : `renvoi non destructif manquant` (renvoi vers `docs/base-locale.md` retire), `avertissement manquant` (`détruit`/`irréversible` remplaces par des mots neutres), `commande de base disparue de la page` (ligne de `python fetcher.py db clear` retiree).
- **Le trou museliere est ferme par un controle, pas par une phrase (D-98).** `_mutation_ecran_muet_declare` passe de `source_literal` a `web_render` **la seule ligne** qui declare le message d'attente de la ligne de commande dans la copie de `tests/test_docs_depannage.py` : la declaration affirme alors un rendu par l'interface web. La sonde du module d'ancrage refuse, et le constat nomme les **dix-neuf routes sondees** et le message : `message non produit par le code : aucune des routes sondees (GET /version, GET /db/status, POST /search, ..., GET /optimize/wizard/recap) ne porte : « Calcul en cours (CP-SAT)… » (famille calcul, mode web_render)`. La mutation porte le **meme motif** que celle du litteral du produit : une sonde muette est un constat, jamais un vert.
- **Un motif attendu est lu, jamais recopie (D-14, D-17).** `_motifs_attendus` cherche le nom de la constante dans le module d'ancrage et refuse un nom introuvable (`MOTIF_MOTIF_INTROUVABLE`) : un motif recopie d'un module a l'autre serait une seconde source de verite et resterait vert apres un renommage du constat. La morsure est cherchee par **appartenance de sous-chaine** — et cette limite est ecrite dans la docstring et dans ce rapport : elle prouve que le controle rougit **avec ce motif**, jamais que ce motif est la seule cause du rouge.
- **La batterie est intolerante, et sa tolerance est mesuree.** Un **temoin negatif** (mesure d'executeur, hors livrable : une copie du module dont la mutation de la page videe a ete videe de son effet) rend `1 failed` avec `morsure(s) non observee(s) sur une copie pourtant mesuree verte avant mutation : page_livree (docs/glossaire.md) : motif(s) attendu(s) absent(s) : page videe ou tronquee ; ... constats reellement produits : aucun`. La batterie ne peut donc pas passer pour verte sur une mutation inerte, et aucun `skip` ni `xfail` n'existe dans le module (controle d'executeur par `ast` : `skip/xfail rencontres : 0`).
- **La base du depot est prouvee intacte en lecture seule (`GARD-03`, D-104).** `test_la_base_du_depot_est_intacte` lit les **octets** (`read_bytes()` + `hashlib.sha256`) et compare les **trois** valeurs a `EMPREINTE_BASE`, mesuree sur le disque avant d'ecrire la constante : `24989696`, `1788730056843137500`, `e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identiques a celles consignees par 06-03 et 05-03. Un SHA-256 seul laisserait passer un fichier reecrit a l'identique et une taille seule ne verrait rien du contenu : les trois valeurs sont exigees et citees. L'import de `sqlite3` est **refuse par la garde de cloture**, donc le controle et la regle tiennent ensemble.
- **Chaque livrable de la phase est couvert par une mutation declaree (critere 4).** `test_chaque_livrable_est_couvert_par_une_mutation` **derive** ses cibles de `FAMILLES` (la table est la seule source du contrat) et exige que `docs/depannage.md`, `docs/glossaire.md`, `docs/sommaire.md`, `README.md` et le module d'ancrage des messages y figurent : une page livree sans mutation est un constat nomme.
- **Les deux executions finales sont citees, jamais estimees (critere 5).** Suite entiere : `249 passed in 6.01s` (`.gsd-tmp/06-04-suite-entiere.txt`, 235 avant la phase 6 et 243 avant ce plan). Suite sous le greffon de refus reseau et de piege `main()` : `249 passed in 6.12s` (`.gsd-tmp/06-04-suite-sans-reseau.txt`), avec la ligne d'armement `greffon de preuve 06-04 : 6 pieges armes avant la collecte -> socket.socket, socket.create_connection, socket.socketpair, urllib.request.urlopen, dofus_stuff.cli.main, dofus_stuff.web.__main__.main`. La seconde execution n'est **pas** un doublon de la premiere : c'est elle qui satisfait le membre « aucune connexion reseau, `main()` jamais execute » du critere 5, les pieges etant armes **avant la collecte** et donc avant `tests/conftest.py`, et `verifie_arme()` verifiant par **identite** — jamais par un appel — que les deux noms `main` ne sont plus les fonctions du produit.
- **L'audit de perimetre est rendu contre deux jeux de chemins nommes, et sa divergence est ecrite.** Verdict du bloc de la tache 3 : `audit de perimetre : huit chemins de livrable declares, jeu tolere nomme (outillage et bookkeeping d'execution) ecarte, dofus_stuff/** absent`. Perimetre mesure : ` M .gitignore`, ` M .planning/config.json`, ` M tests/test_docs_mutation.py`, `?? .doc-agent/`, `?? .gsd-tmp/`, `?? .gsd/`, `?? .planning/state.json`, `?? doc-agent.toml`, `?? gsd-auto-rules.toml`, `?? gsd-auto.toml` ; `git status --porcelain -- dofus_stuff` **vide**. La divergence est donc celle que `06-RESEARCH.md` § E.3 avait mesuree : la formulation du critere de la phase est fausse a la lettre (`git status` ne montre pas « seulement `docs/`, `README.md`, `GUIDE_WIZARD.md` et `tests/` »), et la version appliquee est la version mesuree — huit chemins de livrable declares pour les quatre plans de la phase, plus un jeu tolere **nomme** (outillage et bookkeeping d'execution, presents ou modifies avant la phase par l'automatisation, jamais des livrables).

## Task Commits

Each task was committed atomically, par chemin explicite (jamais `git add .`) :

1. **Tache 1 : la tranche verticale de la preuve de morsure (`type="tracer"`) — la copie du depot, la redirection de la racine, et la famille `page_livree`** — `41b6b54` (test) : `tests/test_docs_mutation.py` (640 lignes) — `1 file changed, 640 insertions(+)`.
2. **Tache 2 : les quatre familles restantes et le trou museliere** — `0d3ec3b` (test) : `tests/test_docs_mutation.py` (+325 lignes) — `1 file changed, 325 insertions(+)`.
3. **Tache 3 : l'empreinte de la base du depot et la couverture des livrables** — `9cd7de2` (test) : `tests/test_docs_mutation.py` (+70 lignes) — `1 file changed, 70 insertions(+)`. **Aucun fichier supprime** (`git diff --diff-filter=D --name-only` vide sur l'intervalle et apres chaque commit).

**Plan metadata:** le commit de metadonnees de ce plan `docs(06-04): complete la preuve de morsure, l'empreinte de la base et l'audit de perimetre` porte ce SUMMARY, la position de `STATE.md` (dont `progress.completed_plans` portee de 22 a 23, `state_head` = `9cd7de2`, la ligne `Phase 6 P04` du tableau Per-Plan Metrics, et la correction de la ligne `Phase 6 P03` qui y figurait **deux fois**), `ROADMAP.md` (`**Plans**: 4/4 plans executed`, les deux cases 06-04 cochees, la ligne de la phase 6 portee a `4/4`) et `GARD-04` completée dans `REQUIREMENTS.md` (case cochee et statut du tableau de tracabilite porte a `Complete`). `git rev-list --count e2fabdc..9cd7de2` = **3** : trois commits de tache, aucun commit intermediaire de correction.

**Note de methode (deviation rapportee) :** le module a ete ecrit en une passe (bloc par bloc) et les **trois etats intermediaires** de tache ont ete reconstruits aux frontieres des taches — l'etat de la tache 1 (`FAMILLES` reduite a `page_livree`, garde de cloture, copie, redirection, deux tests), puis celui de la tache 2 (les quatre familles, `FAMILLES_DECLAREES`, les douze mutations restantes, le trou museliere, `test_les_familles_declarent_leurs_mutations`), puis l'etat final de la tache 3 (l'empreinte, `LIVRABLES_DE_LA_PHASE`, `test_la_base_du_depot_est_intacte`, `test_chaque_livrable_est_couvert_par_une_mutation`). Chaque etat a ete **remesure vert** avant son commit (`.gsd-tmp/06-04-decoupe.py`, outil hors livrable) : `2 passed, 1 deselected` + `246 passed` (tache 1), `4 passed` + `247 passed` (tache 2), `6 passed` + `249 passed` (tache 3). Aucun controle n'a ete affaibli pour obtenir un etat intermediaire vert, et le diff cumule final est identique au contenu ecrit d'un seul tenant (`1 file changed, 1035 insertions(+)`).

## Files Created/Modified

- `tests/test_docs_mutation.py` — **cree** (640 lignes en tache 1, 965 en tache 2, 1035 a la fin de la tache 3 ; >= 240 lignes exigees, 6 tests). Docstring de contrat, de la decision sur le trou museliere et de six limites nommees ; garde de cloture auto-analysee par `ast` ; constantes `RACINE_DEPOT`, `DOSSIER_DOCS`, `SOMMAIRE`, `MODULES_ANCRAGE`, `FICHIERS_HORS_DOCS`, `DOSSIERS_COPIES`, `FICHIERS_COPIES`, `DOSSIER_RETIRES`, les cinq `FAMILLE_*`, `FAMILLES_DECLAREES`, `LIVRABLES_DE_LA_PHASE`, `CONTROLES_DE_LA_COPIE` (13 entrees), `SONDES_DE_LA_COPIE`, `CHEMIN_BASE`, `EMPREINTE_BASE`, `RACINES_INTERDITES` (11), `APPELS_SUPPRESSION` (4), `APPEL_PRODUIT`, `APPELS_CALCUL_PRODUIT`, `CHEMINS_DESTRUCTIFS`, `MOTIF_LIGNE_INDEX_GLOSSAIRE` et huit constantes `MOTIF_*` ; helpers `_lire`, `_ecrire`, `_exiger_mutation`, `_remplacer`, `_retirer_lignes`, `_suivant`, `_charger_module`, `_rediriger`, `_charger_modules`, `_copie_du_depot`, `_controles`, `_sondes_du_produit`, `_mesure`, `_appliquer`, `_motifs_attendus`, `_imports_du_module`, `_appels_du_module`, `_litteraux_de_chemin_destructif` ; table unique `FAMILLES` (14 entrees) ; quatorze fonctions de mutation ; **6 tests**. Les fixtures partagees de `tests/conftest.py` (`client`, `sections`, `normalize`) sont **reutilisees telles quelles**, jamais recopiees (D-12) : le module ne definit ni client de test, ni normalisation, ni lecteur de section.
- `docs/**` — **aucun octet modifie** : les pages citees (dont `docs/cli.md` et `docs/glossaire.md`, rendues absentes ou videes) ne le sont que **dans la copie** sous `tmp_path`.
- `README.md` — **aucun octet modifie** : la copie du README est mutee trois fois, le depot ne l'est pas.
- `dofus_stuff/**` — **aucun octet modifie** (`D-103` : `git status --porcelain -- dofus_stuff` vide, mesure de l'audit) ; les mutations de la famille des messages visent la copie de `dofus_stuff/sync.py`, jamais le fichier du depot. `pyproject.toml` inchange (aucune dependance ajoutee) ; `.data/**` jamais approche.
- `.gsd-tmp/` (hors livrable, non suivi par git) — l'outillage d'executeur de ce plan : `06-04-decoupe.py` (reconstruction des etats de tache), `test_rapport_morsures.py` (rapport famille par famille), `06-04-morsures.txt` (`14 mutations mordantes sur 14 declarees`, source des lignes de ce rapport), `no_net.py` (le greffon de refus reseau et de piege `main()`, arme avant la collecte), `06-04-suite-entiere.txt` (`249 passed in 6.01s`), `06-04-suite-sans-reseau.txt` (`249 passed in 6.12s`). Ce jeu est tolere par l'audit de perimetre au titre du « jeu tolere nomme ».

## Decisions Made

- **La morsure se prouve en processus, par les fonctions de constats des modules d'ancrage, et la suite entiere est rejouee par une commande d'executeur.** Le harnais interdit `subprocess` (la garde de cloture de ce module refuse l'import), re-lancer pytest depuis un test serait un sous-processus, donc la copie vit sous `tmp_path` et la fonction de constats est appelee sur elle. Cette limite est ecrite dans la docstring du module et dans ce rapport.
- **Une page est rendue absente par `Path.rename` vers `<copie>/../retires/`, jamais par un appel de suppression.** `APPELS_SUPPRESSION` refuse `remove`, `unlink`, `rmdir` et `rmtree`, y compris dans ce module qui s'auto-analyse : une suppression litterale ferait rougir la garde de cloture sur une livraison conforme, ce qui serait un defaut du module et non de la livraison.
- **Le trou museliere est ferme par une mutation de declaration, qui porte le meme motif que celle du litteral du produit** (`message non produit par le code`) : une declaration de rendu que le produit ne produit pas est un constat, jamais un vert muet. Le constat nomme les dix-neuf routes sondees et le message.
- **Les trois mutations du README portent deux motifs** (`invitation a detruire les donnees` **et** la famille : renvoi, avertissement, disparition). La morsure etant cherchee par appartenance de sous-chaine, exiger le motif de base seul aurait laisse passer une mutation qui rougit pour une autre raison que la famille visee.
- **`test_chaque_livrable_est_couvert_par_une_mutation` derive ses cibles de `FAMILLES`** : la table est la seule source du contrat, et une seconde liste de livrables aurait ete une seconde source de verite (D-14).
- **L'empreinte de la base du depot est ecrite apres re-mesure sur le disque**, jamais d'apres le plan : `24989696`, `1788730056843137500`, `e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identiques aux valeurs consignees par 06-03 et 05-03. Les **trois** valeurs (et pas une seule) sont exigees et citees dans le constat.
- **La garde de cloture de ce module ne recopie pas celles des phases precedentes** : elle refuse les racines de base, de processus, de socket et de reseau, l'appel a `main`, les appels du solveur, les quatre appels de suppression, et elle verifie en plus qu'aucun **litteral** des deux chemins destructifs (`/db/clear`, `/db/sync`) n'est ecrit hors de la constante qui les declare. Sa limite est ecrite : c'est une demonstration **statique et indirecte**.
- **La batterie est intolerante, et sa tolerance est mesuree par un temoin negatif** (hors livrable) : une mutation videe de son effet fait echouer le test en nommant la famille, le fichier cible, le motif attendu et `constats reellement produits : aucun`.
- **Le greffon de preuve est hors livrable et non suivi par git** (`.gsd-tmp/no_net.py`), meme statut que le script de mesure du plan 06-01 : il ne peut pas etre pris pour un livrable, et l'audit de perimetre le declare comme outillage tolere.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - blocage d'execution] Le module a du etre ecrit en une passe, puis decoupe aux frontieres des taches**

- **Found during:** Tache 1 (ecriture de la tranche verticale), puis repris apres l'interruption de la passe par la compaction du contexte.
- **Issue:** le module de 1035 lignes a ete ecrit d'un seul tenant (bloc par bloc, par l'outil d'ecriture), alors que le plan exige **un commit atomique par tache** avec des etats intermediaires coherents (la table `FAMILLES` remplie progressivement, `test_les_familles_declarent_leurs_mutations` en tache 2, l'empreinte et les deux tests de cloture en tache 3). Un commit unique pour les trois taches aurait rendu le perimetre de chaque tache illisible dans l'historique, et le decoupage par `git add -p` aurait produit des etats intermediaires non mesurables (donc non verifiables).
- **Fix:** les trois etats ont ete **generes** par un outil d'executeur hors livrable (`.gsd-tmp/06-04-decoupe.py`, retraits verifies exactement une fois chacun, `compile` de chaque etat), puis **remesures verts** avant chacun des trois commits : etat de la tache 1 (`2 passed, 1 deselected` sur la batterie, `246 passed` sur la suite), etat de la tache 2 (`4 passed`, `247 passed`), etat final (`6 passed`, `249 passed`). Le commit initial unique a ete annule par `git reset --soft HEAD~1` (aucun fichier touche) et remplace par les trois commits de tache.
- **Files modified:** `tests/test_docs_mutation.py` (contenu final identique a la version ecrite d'un seul tenant).
- **Verification:** `git rev-list --count e2fabdc..9cd7de2` = `3` ; `git log --oneline` montre `41b6b54`, `0d3ec3b`, `9cd7de2` dans l'ordre des taches ; le diff cumule final est `1 file changed, 1035 insertions(+)` ; `git diff --diff-filter=D --name-only` vide.
- **Committed in:** `41b6b54` (tache 1), `0d3ec3b` (tache 2), `9cd7de2` (tache 3).

### Ajouts de robustesse (Rule 2, signales comme tels)

**2. [Rule 2] Le refus d'une sonde est converti en constat cherchable, jamais en erreur de collecte**

- **Found during:** Tache 2 (la mutation `ecran_muet_declare`).
- **Issue:** la mutation du trou museliere ne fait pas « rendre un constat » a la sonde `_produire` : elle la fait **lever** (`assert` du module d'ancrage, `message non produit par le code`). Sans traitement, la batterie aurait echoue par exception ou aurait compte la mutation comme non mordante sur un controle qui mord pourtant — exactement l'inverse du besoin, puisque la sonde muette est le constat vise.
- **Fix:** `_mesure` enferme l'appel dans `try`/`except AssertionError` et rend le refus comme un **texte**, ou le motif attendu est cherche comme dans un constat ; une sonde dont le retour n'est pas une liste de constats (`SONDES_DE_LA_COPIE`) est traitee comme telle. Le constat produit nomme les dix-neuf routes sondees, le message et sa famille.
- **Files modified:** `tests/test_docs_mutation.py`.
- **Verification:** la mutation mord avec `message non produit par le code` (14/14 mordantes) et le temoin negatif (mutation inerte) fait toujours echouer la batterie.
- **Committed in:** `0d3ec3b` (tache 2).

**3. [Rule 2] Chaque mutation refuse d'etre un no-op silencieux**

- **Found during:** Taches 1 et 2 (ecriture des quatorze mutations).
- **Issue:** une mutation dont l'ancre a disparu de la copie (une page corrigee par un plan ulterieur, un libelle deplace) ecrirait un fichier inchange : la morsure ne serait pas observee, la batterie rapporterait un **echec de mutation** alors que la cause serait une ancre morte — un faux rouge qui userait la batterie au lieu de la garder.
- **Fix:** `_exiger_mutation` est appele par chaque mutation avant toute ecriture (presence du titre, de la ligne de terme, de l'ancre de rubrique, du litteral du produit, de la declaration de provenance) et leve `MOTIF_MUTATION_SANS_OBJET` en nommant l'ancre et le fichier. Les mutations qui remplacent un fragment passent par `_remplacer`, qui exige l'unicite du fragment.
- **Files modified:** `tests/test_docs_mutation.py`.
- **Verification:** les quatorze mutations mordent sur la copie livree (aucune ancre morte sur l'etat actuel) ; un renommage de page ferait echouer la mutation en la nommant « sans objet » plutot que de la faire passer pour une derive de la famille.
- **Committed in:** `41b6b54` (tache 1, famille `page_livree`), `0d3ec3b` (tache 2, les douze autres).

**4. [Rule 2] La garde de cloture refuse aussi un litteral destructif range dans une table de routes**

- **Found during:** Tache 1 (reecriture de la garde de cloture pour le risque reel du module).
- **Issue:** refuser l'**appel** `post("/db/clear")` ne suffit pas : un chemin destructif ecrit dans une table de routes puis poste indirectement passerait la garde par nom d'appel tout en joignant le meme point d'entree.
- **Fix:** `_litteraux_de_chemin_destructif` parcourt l'arbre `ast` du module, exclut la constante `CHEMINS_DESTRUCTIFS` (qui **declare** les deux chemins, et se detecte sinon elle-meme) et refuse tout autre litteral qui commence par l'un des deux. Les onze racines interdites, l'appel a `main`, les deux appels du solveur et les quatre appels de suppression restent refuses par ailleurs.
- **Files modified:** `tests/test_docs_mutation.py`.
- **Verification:** `test_garde_de_cloture_du_harnais` rend 0 constat sur le module livre ; les deux chemins ne figurent que dans la constante qui les declare.
- **Committed in:** `41b6b54` (tache 1).

### Mesure rapportee (hors perimetre du plan, faite par l'executeur)

**5. La tolerance de la batterie a ete mesuree par un temoin negatif**

- **Ce qui a ete mesure :** une copie du module, **hors depot** (`tests/test_docs_mutation_temoin.py`, creee puis supprimee dans la meme passe), dont la mutation de la page videe a ete **videe de son effet**. Resultat : `1 failed` avec `morsure(s) non observee(s) sur une copie pourtant mesuree verte avant mutation : page_livree (docs/glossaire.md) : motif(s) attendu(s) absent(s) : page videe ou tronquee ; motifs lus dans test_docs_completude.py ; constats reellement produits : aucun`.
- **Pourquoi :** le plan exige que « toute mutation dont la morsure n'est pas observee fasse echouer la batterie, jamais un avertissement discret » ; sans cette mesure, l'affirmation reposerait sur la lecture du code. Le fichier temoin a ete **supprime** et `tests/` ne le porte plus (`ls tests | grep temoin` -> aucun).
- **Aucun fichier du depot conserve :** la mesure n'a laisse aucun livrable ni fichier non suivi dans `tests/`.

## Verification

Les **neuf** blocs `<automated>` du plan (trois par tache) ont ete joues dans l'ordre, chacun avec son resultat **reel** :

| Tache | Bloc `<automated>` | Resultat observe | `fails_when` |
|-------|--------------------|------------------|--------------|
| 1 | `pytest tests/test_docs_mutation.py -q -k "copie_est_verte or chaque_derive"` | `2 passed, 1 deselected in 0.61s` (etat de tache 1) ; `2 passed, 4 deselected in 1.69s` (etat final) | aucun `failed`/`error` |
| 1 | controle `ast` : fonctions de la batterie presentes + `skip`/`xfail` | `fonctions attendues manquantes : []` ; `skip/xfail rencontres : 0` ; exit `0` (rejoue apres le commit du traceur) | exit non nul |
| 1 | `pytest -q` | `246 passed in 4.81s` (etat de tache 1) ; `249 passed in 6.10s` (etat final, remesure apres le commit) | aucun `failed`/`error` |
| 2 | `pytest tests/test_docs_mutation.py -q` | `4 passed in 1.80s` | aucun `failed`/`error` |
| 2 | batterie + `git status` des chemins de livrable | `4 passed in 1.66s` puis `batterie : depot intact (les livrables ne changent pas, la copie vit dans tmp_path)` ; exit `0` | pas de `BATTERIE ROUGE OU NON SELECTIONNEE`, pas de `FICHIER DU DEPOT MODIFIE PAR LA BATTERIE` |
| 2 | `pytest -q` | `247 passed in 5.93s` | aucun `failed`/`error` |
| 3 | `pytest tests/test_docs_mutation.py -q -k "base_du_depot or couvert"` | `2 passed, 4 deselected in 0.03s` | aucun `failed`/`error`, pas de `no tests ran` |
| 3 | greffon + empreinte avant/apres + deux suites | `PIEGE ARME` ; `AVANT taille=24989696 mtime_ns=1788730056843137500 sha256=e3793d64...` ; `249 passed in 6.06s` ; `249 passed in 6.06s` ; `APRES` identique ; `base du depot intacte et identique avant et apres les deux executions...` ; exit `0` | pas de `GREFFON ABSENT`, `GREFFON PRESENT MAIS NON ARME`, `SUITE FINALE ROUGE`, `SUITE SOUS GREFFON ROUGE`, `EMPREINTE DE LA BASE DU DEPOT MODIFIEE` |
| 3 | audit de perimetre (`git status --porcelain` + jeu tolere) | `audit de perimetre : huit chemins de livrable declares, jeu tolere nomme (outillage et bookkeeping d'execution) ecarte, dofus_stuff/** absent` ; exit `0` | pas de `HORS PERIMETRE`, `GIT EN ECHEC`, `AUCUN CHANGEMENT` |

**Les deux executions finales citees par ce rapport** (re-mesurees en fichiers, `.gsd-tmp/06-04-suite-entiere.txt` et `.gsd-tmp/06-04-suite-sans-reseau.txt`, apres le bloc ci-dessus) :

- suite **entiere** : `.venv/Scripts/python.exe -m pytest -q` -> **`249 passed in 6.01s`** (`rc=0`) ;
- suite sous le **greffon de refus reseau et de piege `main()`** : `PYTHONPATH="$PWD/.gsd-tmp" .venv/Scripts/python.exe -m pytest -q -p no_net` -> **`249 passed in 6.12s`** (`rc=0`), precede de la ligne `greffon de preuve 06-04 : 6 pieges armes avant la collecte -> socket.socket, socket.create_connection, socket.socketpair, urllib.request.urlopen, dofus_stuff.cli.main, dofus_stuff.web.__main__.main` ;
- empreinte de `.data/dofus.sqlite3` **avant** : `taille=24989696 mtime_ns=1788730056843137500 sha256=e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` ; **apres** : identique.

**Portes du plan :** la porte de retour apres le traceur a ete rejouee sur ses trois blocs (batterie `2 passed`, controle `ast` exit `0`, suite `246 passed`) avant de passer a la tache 2 ; aucun point d'arret (`checkpoint`) n'etait pose par le plan, et le mode du projet est `end-of-phase` avec des blocs `<automated>` uniquement — aucun point d'arret humain n'a ete franchi ni invoque.

## Issues Encountered

- **La passe a ete interrompue une fois par la compaction du contexte**, pendant l'ecriture du module. Reprise depuis `.gsd-auto/` (affectation + memoire de travail) : le contexte lu a servi a reprendre a l'etape suivante, sans rejouer un appel d'outil deja fait, et le module a ete ecrit en entier, mesure, puis decoupe aux frontieres des taches (voir § Deviations, point 1).
- **Aucun echec de controle** : les neuf blocs `<automated>` sont verts a la premiere execution, les quatorze mutations mordent a la premiere execution, et aucune assertion n'a ete affaiblie. Un seul aller-retour de mise au point a eu lieu sur un **outil d'executeur** (l'ancre du temoin negatif construite par concatenation, hors livrable), jamais sur le module livre.

## User Setup Required

None : aucun paquet installe, aucune dependance ajoutee (`shutil`, `hashlib`, `importlib`, `ast`, `re`, `sys`, `pathlib` sont de la bibliotheque standard), aucune variable d'environnement requise, aucun service externe, aucun appel reseau, aucune resynchronisation Dofusdude.

## Threat Flags

Aucun drapeau nouveau : les six menaces `mitigate` du plan sont couvertes par le module et ses mesures, et aucune surface nouvelle n'est introduite.

- **T-06-04-01 (Repudiation — une preuve qui ne prouve rien)** : la copie est verte avant chaque mutation (precondition testee), la mutation porte sur une copie fraiche, le motif attendu est exige dans les constats, et la tolerance est **mesuree** (temoin negatif).
- **T-06-04-02 (Tampering — le depot)** : toutes les mutations vivent sous `tmp_path` ; le bloc de la tache 2 refuse qu'un chemin de livrable bouge pendant la batterie, et l'audit de la tache 3 rend `dofus_stuff/** absent` et aucun chemin hors des huit declares et du jeu tolere nomme.
- **T-06-04-03 (Tampering / Information disclosure — `.data/dofus.sqlite3`)** : empreinte en lecture seule (octets, `mtime_ns`, SHA-256) avant et apres la suite finale, identique ; le module n'importe jamais `sqlite3` (la garde de cloture le refuse).
- **T-06-04-04 (Elevation of privilege — sous-processus, reseau, chemins destructifs)** : garde `ast` reecrite (onze racines interdites dont `subprocess`, point d'entree du produit, appels de calcul et de suppression, litteraux de `CHEMINS_DESTRUCTIFS`), et suite finale rejouee sous le greffon qui arme six pieges avant la collecte.
- **T-06-04-05 (Spoofing — un rapport qui arrange)** : les compteurs et durees de ce rapport sont **lus** dans la sortie des deux executions finales (fichiers conserves sous `.gsd-tmp/`), l'empreinte de la base est mesuree avant et apres, la liste des limites est ecrite, et la divergence de l'audit de perimetre est nommee.
- **T-06-04-06 (Repudiation — le trou museliere)** : la mutation `ecran_muet_declare` fait refuser la sonde du module d'ancrage (`message non produit par le code`), donc l'ecran muet ne peut pas etre couvert par une declaration rendue.
- **T-06-04-SC (Installations de paquets)** : `accept` et tenu — aucune dependance ajoutee, aucun paquet installe.

## Self-Check: PASSED

- `tests/test_docs_mutation.py` existe (1035 lignes, 6 tests ; `pytest tests/test_docs_mutation.py -q` -> `6 passed`).
- `git log --oneline e2fabdc..HEAD` contient les trois commits de tache : `41b6b54`, `0d3ec3b`, `9cd7de2`.
- `git diff --diff-filter=D --name-only e2fabdc..9cd7de2` est vide : aucun fichier supprime.
- Les quatorze mutations mordent (14/14) et la tolerance de la batterie est mesuree par un temoin negatif.
- `.data/dofus.sqlite3` : empreinte identique avant et apres les deux executions finales (et apres chaque batterie et chaque suite de tache).
- Aucun fichier de `dofus_stuff/**`, de `docs/**`, ni `README.md`, ni `pyproject.toml` modifie ; `tests/` ne porte plus aucun fichier temoin.
- Les deux suites finales sont vertes et leurs compteurs et durees sont cites : `249 passed in 6.01s` et `249 passed in 6.12s`.

## Limites declarees

Ecrites dans la docstring du module (`06-04-SUMMARY.md` les reprend) — aucune n'est presentee comme resolue :

1. **La morsure est cherchee par appartenance de sous-chaine** : le motif attendu doit apparaitre dans les constats produits. Elle prouve que le controle rougit **avec ce motif**, jamais que ce motif est la seule cause du rouge, ni que le constat appartient bien a la famille visee. C'est le trou de lecture que la mutation du README comble partiellement en exigeant **deux** motifs.
2. **Seules les cinq familles declarees sont couvertes** : une derive hors de ces familles (un renommage de fichier dans `docs/`, une page ajoutee hors index) est interceptee par les gardes livrees « autant que » par elles, mais cette couverture n'est pas demontree exhaustivement (`D-85`, backstop du plan).
3. **La mutation d'un module d'ancrage est prouvee en rechargeant le module depuis la copie** (`_mutation_ecran_muet_declare`), et la mutation d'un litteral du produit porte sur la copie de `dofus_stuff/`, jamais sur `dofus_stuff/**` du depot (`D-103`).
4. **La suite entiere n'est pas rejouee par le module** (aucun sous-processus) : il prouve la morsure au niveau des fonctions de controle ; le rejeu complet, ses compteurs et ses durees vivent dans ce rapport, et l'ordre de rejeu (suite entiere, puis suite sous le greffon) est une commande d'executeur.
5. **Le rendu Markdown hors GitHub, la prose des pages et l'exhaustivite des derives non declarees restent hors d'atteinte**, comme les modules d'ancrage le declarent deja ; l'ordre de lecture du parcours conseille reste libre (limite de 06-02).
6. **La garde de cloture est une demonstration statique et indirecte** : elle dit ce que ce module importe et appelle, pas ce qu'un autre chemin ferait.
7. **L'ecran muet est traite par la sonde, jamais par un rendu** : `GET /quit` ne rend aucun message et n'accepte pas `POST` (mesure : 405, aucune ligne de statut) ; le controle prouve qu'une **declaration** de rendu non produite est refusee, il ne fabrique pas un ecran.
8. **La mesure d'empreinte de la base du depot est locale au processus de test** : elle est vraie par construction pour ce module (qui n'ouvre aucune base) et pour la suite ; elle ne voit pas une ecriture faite par un autre processus pendant la meme fenetre.
9. **La divergence de l'audit de perimetre est declaree, pas masquee** : la formulation du critere 5 du ROADMAP (« `git status` ne montre que `docs/`, `README.md`, `GUIDE_WIZARD.md` et `tests/` ») est **fausse a la lettre** ; l'audit applique la version mesuree par `06-RESEARCH.md` § E.3 — les huit chemins de livrable declares par les quatre plans, plus un jeu tolere nomme (`.gitignore`, `.planning/**`, `.gsd-tmp/`, `.gsd/`, `.doc-agent/`, `doc-agent.toml`, `gsd-auto-rules.toml`, `gsd-auto.toml`), outillage et bookkeeping d'execution presents ou modifies **avant** la phase, jamais des livrables.
10. **Derive heritee, nommee a l'identique et NON corrigee (`D-101`)** : `windows_ledger_table_drift`, ligne `id=5` du registre `.planning/WINDOWS.md`, verdict d'outil consigne dans `04-03-SUMMARY.md:220` et `05-03-SUMMARY.md:238`, heritee de la phase 3. `windows fixed 5` n'a **jamais** ete tente et le registre n'a pas ete reecrit : c'est une action hors perimetre, et la derive n'est presentee ici ni comme corrigee, ni comme resolue.

## Next Phase Readiness

- **Le plan 06-04 est le dernier plan de la phase 6 et du milestone documentaire** : les quatre plans de la phase sont livres (06-01 `docs/depannage.md`, 06-02 `docs/glossaire.md`, 06-03 la completude et le `README.md`, 06-04 la preuve de morsure), et la phase n'a plus de plan a executer.
- **Ce qui reste ouvert apres ce plan, et qui n'est pas de son ressort** : la **verification de phase** (`/gsd:verify-work` sur la phase 6), qui relit les quatre SUMMARY, les criteres 1 a 5 du ROADMAP et la section de preuve de `06-VALIDATION.md` ; les taches de verification de ce plan sont vertes, mais aucune verification humaine n'a ete revendiquee ici.
- **La reserve de la phase est levee, pas deplacee** : les quatorze derives declarees par les quatre plans mordent avec leur motif, `GARD-04` est completee (suite verte sans ecriture sous `.data/`, sans `main()`, sans connexion reseau) et `GARD-03` reste tenue (empreinte de la base intacte, `dofus_stuff/**` non modifie).
- **Reserve connue, non corrigee** : la derive preexistante du registre `.planning/WINDOWS.md` (`windows_ledger_table_drift`, `id=5`) reste declaree ; aucune ligne de ce plan ne la presente comme resolue.
- **Aucun nouveau milestone** n'est ouvert par ce plan : le besoin initial (une documentation utilisateur en francais, livree et gardee) est couvert par les phases 1 a 6.

---
*Phase: 06-depannage-glossaire-completude-et-preuve-finale*
*Completed: 2026-09-12*
