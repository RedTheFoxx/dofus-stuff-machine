---
phase: 06-depannage-glossaire-completude-et-preuve-finale
plan: 01
subsystem: documentation
tags: [markdown, pytest, depannage, messages-reels, provenance, bijection-rubrique-message, mecanisme-du-clavier, pagination-a-deux-formes, budget-de-calcul, morsures, copie-verte-avant-mutation, documentation-francaise]

# Dependency graph
requires: []
provides:
  - "docs/depannage.md : la page unique du sujet (13 354 octets, 96 lignes, 96 fins de ligne pour 96 retours chariot, sans BOM) — cinq sections de niveau 2 dans l'ordre du critere 1 (`## Base absente ou vide`, `## Saisie invalide`, `## Calcul long`, `## Clavier inactif`, `## Résultat paginé`), un seul titre de niveau 1 (`# Dépannage`, egal au libelle d'index), le bloc `## Source de vérité` en derniere section et `[Retour au sommaire](sommaire.md)` en derniere ligne non vide ; chaque ligne de tableau a pour premiere cellule un message **entre accents graves** dans le corps de la rubrique de sa famille"
  - "docs/sommaire.md : exactement **une** ligne de plus, `| [Dépannage](depannage.md) | Retrouver la marche à suivre par le message affiché |`, ajoutee en fin de table `## Index` (24 lignes avant et apres la regle d'index : le parcours conseille reste du texte, jamais converti en liens)"
  - "tests/test_docs_depannage.py : le module d'ancrage message → rubrique (1 253 lignes, 62 895 octets, 9 tests) — garde de cloture auto-analysee par `ast`, table `MESSAGES` de provenance (32 entrees), fonctions pures `problemes_rubriques`, `problemes_messages`, `problemes_budget`, `problemes_renvois`, `problemes_page`, `problemes_clavier`, sonde `_produire` et lecteurs locaux"
  - "les 20 constantes de motif `MOTIF_*` du plan, plus `MOTIF_BUDGET` (le motif du controle de budget ajoute en tache 2) : chaque constat porte un motif ASCII nomme, jamais ecrit en clair dans une ligne d'assertion"
  - "la mesure de provenance : 19 routes sondees par le client de test Flask en processus (2 `GET` sur une application a catalogue vide, 11 refus postes, 5 etapes du parcours simplifie conduit pas a pas, le recapitulatif du wizard en `GET`), 2 bases construites sous `tmp_path` (vide et peuplee par la fixture `app`), 2 captures reelles de `_print_db_status`, 9 litteraux lus dans les 4 fichiers producteurs nommes"
  - "la couverture du critere 1 du ROADMAP et de `AIDE-01` : les cinq familles indexees par le message reellement produit, et aucun message invente pour la famille qui n'en produit pas (D-76, D-93)"
affects: [06-02, 06-03, 06-04, verification-phase-6]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (85 000) est consigne tel quel : il mesure le pessimisme de l'estimate,
# pas un travail non fait (les trois taches sont livrees, 8/8 morsures du plan detectees).
actuals:
  tokens: 19295     # chars/4 sur le diff realise (77 181 caracteres de patch, 3 fichiers, 1 350 insertions)
  tasks: 3
  commits: 3        # MESURE : 3 commits de tache (git rev-list --count 110951f...0c672f7 = 3) ; le compte final est 4 avec le commit de metadonnees de ce plan (le dernier de la branche, `git log -1`)
  plan_head_before: 110951f83d9baff3805c0bcb464525bf51f93514

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; stdlib seulement (ast, re, hashlib, io, contextlib, pathlib)
  patterns:
    - "Morsure sur copie verte avant mutation (D-84) : chaque derive est jouee dans un repertoire temporaire (`mktemp -d`), la copie est mesuree VERTE sur `tests/test_docs_depannage.py` avant la mutation, puis la suite complete est rejouee apres — la copie sans `.data/` n'est jamais rouge pour une raison etrangere (mesure : `225 passed, 3 skipped`, les trois sauts etant nommes)"
    - "Mutation ecrite par `python -c` qui lit et reecrit avec `newline=\"\"` : les CR des fichiers CRLF du depot (`dofus_stuff/web/routes.py`, `docs/depannage.md`) sont preserves. Le `sed -i` de ce poste les retire, ce qui produit une mutation hors sujet et une batterie qui crie `MUTATION NON DETECTEE` pour une raison qui n'est pas la derive visee (lecon payee une fois, tache 3)"
    - "Motif de morsure porte par une constante ASCII du module, jamais ecrit en clair dans une ligne d'assertion : pytest reproduit la ligne source du `assert`, une valeur en clair y serait trouvee meme sans constat produit. Les textes de fin de message de chaque `assert` sont relus pour la meme raison — aucune chaine de motif n'y figure (regle posee au plan 03-03, tenue ici sur les 9 tests)"
    - "Le contrat va du **produit vers la page** : chaque message declare est retrouve par sa provenance (capture reelle, rendu de client de test, litteral du fichier producteur), puis exige dans la ligne de tableau de la rubrique de sa famille ; et la table `MESSAGES` est en **bijection** avec les lignes citees, famille par famille — un message en trop comme un message manquant sont des constats nommes"
    - "Une famille sans message est declaree comme **mecanisme** (`RUBRIQUES_MECANISME`), et son controle exige les jetons dans la page **et** dans le fichier qui les porte, le rendu des ecrans sans champ, et l'absence de toute entree de `MESSAGES` pour elle (D-76)"

key-files:
  created:
    - docs/depannage.md
    - tests/test_docs_depannage.py
  modified:
    - docs/sommaire.md

key-decisions:
  - "La table `MESSAGES` est ecrite avec les **quatre** familles des la tache 1 (32 entrees : base 10, saisie 13, calcul 4, pagination 5) et les pages qui les citent aussi : `RUBRIQUES` declarant les cinq rubriques du critere 1 des la tache 1, et `test_rubriques_de_depannage` (test de la tache 1) exigeant de chacune un corps non vide adosse a `MESSAGES`, toute page partielle aurait ete rouge des la premiere tache. Les taches 2 et 3 ont donc livre les deux controles nommes par leurs criteres d'acceptation (le budget du calcul, les renvois D-17) au lieu de reecrire des lignes deja livrees — detail en § Deviations."
  - "Modes de provenance : `cli_status` (sortie capturee de `_print_db_status` sous `contextlib.redirect_stdout`, 3 entrees), `web_render` (statut ou corps rendu par le client de test Flask en processus, 20 entrees), `source_literal` (litteral lu dans le fichier producteur nomme, 9 entrees). `source_literal` prouve une chaine **presente** dans le fichier, jamais un chemin d'execution : la limite est ecrite dans la docstring du module, comme l'exige D-85."
  - "La comparaison de provenance est une **appartenance de sous-chaine** sur le texte produit : la limite est ecrite dans la docstring (un message declare contenu dans un autre message passerait) ; la bijection rubrique <-> table `MESSAGES` est, elle, une egalite de deux ensembles de chaines, et c'est elle qui porte la fidelite du contrat."
  - "La ligne de tableau est exigeable (`^|\\s*`message`\\s*|`) parce que la page cite les messages entre accents graves en premiere cellule : le message de l'etat de la base est lu en **ligne de corps** (`Fichier :` suivi d'un chemin de dossier temporaire), et la page cite donc le libelle, jamais la ligne entiere (D-73, D-75)."
  - "`OPTION_BUDGET = \"--time-limit\"` et `problemes_budget` (tache 2) : le controle du calcul long est **localise a la rubrique**, exige l'option de budget lue sur l'aide du parseur et refuse `JETONS_PROMESSE_DUREE` dans cette rubrique seule — le controle de page ne distingue pas la rubrique qui porte le budget des autres."
  - "`RENVOIS_RUBRIQUES` et `problemes_renvois` (tache 3) : les rubriques « clavier » et « pagination » doivent porter un lien markdown dont la **cible nue** est `installation.md` et `parcours-simplifie.md` (fragment admis) — cette page indexe, elle ne redefinit pas (D-17). Le motif du constat est celui de la famille concernee, donc la batterie du plan reste servie par la meme constante."
  - "`_texte_page` garde le nom et le role que la phase 5 lui a epingles (lecture d'une page de `docs/`), et non le nom `_texte_rendu` de l'inventaire d'artefacts du plan : la phase 5 n'avait aucun `_texte_rendu`, et les rendus sont lus par `_lignes_du_corps` / `_statut` / `_sonde`. Le renommage aurait duplique un lecteur sous un second nom (D-12)."

patterns-established:
  - "Pattern 17 : un message d'erreur se documente **par sa provenance mesuree**, jamais par sa forme supposee — la table porte le mode de mesure (`cli_status`, `web_render`, `source_literal`) et le fichier producteur, et la bijection rubrique <-> table est controlee famille par famille"
  - "Pattern 18 : une famille sans message se declare **mecanisme** et se controle sur trois faits (le jeton dans la page, le jeton dans le fichier qui le porte, l'absence de champ de saisie sur les ecrans concernes), jamais par une chaine ecrite pour remplir la rubrique"
  - "Pattern 19 : un ecran peut porter la pagination a **deux endroits avec deux regles** — le controle mesure les deux formes sur les deux ecrans et n'assied jamais une assertion sur une forme qui ne tient pas partout (piege mesure : `routes.py:144-145` retire `PAGE n/n` du statut quand l'ecran n'a qu'une page)"

requirements-completed: [AIDE-01]

coverage:
  - id: D1
    description: "Les cinq familles du critere 1 sont cinq sections de niveau 2, dans l'ordre du critere, chacune avec un corps non vide, et chaque entree de `MESSAGES` est citee verbatim (`| `message` | ... |`) dans le corps de la rubrique de sa famille — aucun message cite sans declaration, aucun message declare sans citation, famille par famille (`test_rubriques_de_depannage`, `test_les_cinq_familles_sont_couvertes`)"
    requirement: "AIDE-01"
    verification:
      - kind: unit
        ref: "`.venv/Scripts/python.exe -m pytest tests/test_docs_depannage.py -q` -> `9 passed in 0.29s` ; `python -m pytest tests/test_docs_depannage.py tests/test_docs_structure.py -q` -> `23 passed in 0.37s`"
        status: pass
      - kind: integration
        ref: "morsures `rubrique_retiree` -> « rubrique de depannage absente », `message_supprime` -> « message non cite par sa rubrique », `message_invente` -> « message cite non declare »"
        status: pass
    human_judgment: false
  - id: D2
    description: "Chaque message declare est confronte a sa provenance reelle : 32 entrees mesurees (base 10, saisie 13, calcul 4, pagination 5), 19 routes sondees par le client Flask en processus, 2 bases construites sous `tmp_path`, 2 captures de `_print_db_status` (base vide et base peuplee), et 9 litteraux lus dans `dofus_stuff/cli.py`, `sync.py`, `web/routes.py`, `optimize/profile_input.py` — un message non retrouve par sa provenance produit `message non produit par le code` (D-19, D-93)"
    requirement: "AIDE-01"
    verification:
      - kind: integration
        ref: "morsure `refus_niveau_renomme` (`Saisissez un niveau entre 1 et 200` -> `... 300` dans `dofus_stuff/web/routes.py`) -> « message non produit par le code » ; morsure `source_renommee` (libelle de `sync.py`) -> meme motif"
        status: pass
    human_judgment: false
  - id: D3
    description: "La famille « clavier inactif » est un mecanisme : la rubrique porte `autofocus`, `activeElement` et `preventDefault`, chacun exige **aussi** dans le fichier qui le porte (`screen.html`, `terminal.js`), les trois ecrans sans champ (`/version`, `/db/status`, `/quit`) ne rendent aucun `id=\"main-input\"`, et `MESSAGES` ne porte aucune entree pour cette famille ; la pagination est mesuree sur ses deux formes (motif compose present dans le corps des deux ecrans, present dans le statut du seul ecran a plus d'une page)"
    requirement: "AIDE-01"
    verification:
      - kind: integration
        ref: "morsure `jeton_mecanisme_retire` (`activeElement` -> `elementActif` dans la page) -> « mecanisme du clavier » ; morsure `pagination_inconditionnelle` (`routes.py:144` `if total > 1:` -> `if True:`) -> « formes de la pagination »"
        status: pass
      - kind: unit
        ref: "morsure supplementaire hors plan : le renvoi de la rubrique « Clavier inactif » vers `installation.md` remplace par de la prose -> « mecanisme du clavier : la rubrique « Clavier inactif » de depannage.md ne renvoie pas vers installation.md (cibles lues : []) »"
        status: pass
    human_judgment: false
  - id: D4
    description: "La page respecte le gabarit verrouille et ne fige aucune valeur de poste : un seul titre de niveau 1 egal au libelle d'index, `## Source de vérité` en dernier, `[Retour au sommaire](sommaire.md)` en derniere ligne non vide, octets CRLF sans BOM, aucun nombre de quatre chiffres ou plus, aucun motif de chemin de poste, aucun lien externe, aucun bloc de commandes, chaque chemin cite entre accents graves existant depuis la racine du depot ; la rubrique « Calcul long » cite le budget (`--time-limit`) et ne promet aucune duree (D-73, D-75, D-102)"
    requirement: "AIDE-01"
    verification:
      - kind: unit
        ref: "`docs/depannage.md` : 13 354 octets, 96 lignes, 96 fins de ligne pour 96 retours chariot, BOM absent ; `docs/sommaire.md` : 24 lignes (>= 24 exige), contenant `| [Dépannage](depannage.md) |`"
        status: pass
      - kind: unit
        ref: "`problemes_budget` : la rubrique « Calcul long » cite `--time-limit` et ne porte aucun jeton de `JETONS_PROMESSE_DUREE` ; `test_page_close_et_sans_valeur_volatile` vert sur la page livree"
        status: pass
    human_judgment: false
  - id: D5
    description: "La suite entiere est verte avec l'interpreteur epingle et son compteur est releve tel qu'observe : `.venv/Scripts/python.exe -m pytest -q` rend **228 passed** (219 avant ce plan, 9 tests ajoutes), et `.data/dofus.sqlite3` garde taille, mtime_ns et SHA-256 — y compris autour des trois batteries de morsures, qui ne touchent que des copies sous `mktemp -d`"
    requirement: "AIDE-01"
    verification:
      - kind: integration
        ref: "`.venv/Scripts/python.exe -m pytest -q` -> `228 passed in 4.36s` ; `python -m pytest -q --ignore=tests/test_docs_depannage.py` -> `219 passed in 4.13s` ; copie sans `.data/` -> `225 passed, 3 skipped in 4.79s` (sauts nommes)"
        status: pass
      - kind: integration
        ref: "empreinte `.data/dofus.sqlite3` : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique avant le plan, apres chaque tache et apres la suite complete"
        status: pass
      - kind: unit
        ref: "`test_garde_de_cloture_du_harnais` vert : analyse `ast` de ce module — aucun import de base (`sqlite3`), de processus, de socket ou de reseau, aucun appel a `main`, `optimize_stuff` ou `_run_optimize_and_redirect`, aucun appel a `remove`/`unlink`/`rmdir`/`rmtree`, aucune base construite hors `tmp_path` / `web_config` (et `DEFAULT_DATA_DIR` jamais passe), aucun litteral de `/db/clear` ni `/db/sync` ; la garde ne fait pas d'assertion `ast` sur `skip`/`xfail`, et la mesure complementaire est un comptage : le module ne contient **aucune** occurrence de `skip` ni de `xfail` (0 sur 1 253 lignes)"
        status: pass
    human_judgment: false

# Metrics
duration: 4min
completed: 2026-09-12
status: complete
---

# Phase 6 : Depannage, glossaire, completude et preuve finale — Plan 06-01 Summary

**La page de depannage existe et son index aussi : cinq rubriques — les cinq familles du critere 1 — ou chaque ligne de tableau est un message **reellement produit**, retrouve par sa provenance mesuree (capture de la ligne de commande, rendu du client de test Flask, litteral lu dans le fichier producteur) avant d'etre exige dans le corps de la rubrique de sa famille. La famille qui ne produit aucun message est declaree **mecanisme** et se controle sur ses jetons reels et sur le rendu des ecrans sans champ, jamais sur une chaine inventee. Les huit derives du plan — plus une derive supplementaire sur les renvois D-17 — ont toutes ete detectees sur une copie verte avant mutation, avec le motif exact que la batterie cherche, et la suite entiere est verte : **228 passed** (219 avant ce plan) avec la base du depot intacte (empreinte identique avant et apres).**

## Performance

- **Duration:** ~4 min entre le premier et le dernier commit de tache (mesure `git log --format=%cI` : `2026-09-12T01:46:44+02:00` -> `2026-09-12T01:50:22+02:00`, soit **3 min 38 s**) ; les batteries de morsures ont coûte 24 s (tache 1), 12 s (tache 2) et 13 s (tache 3).
- **Started:** 2026-09-12T01:44:00+02:00 (environ)
- **Completed:** 2026-09-12T01:50:22+02:00
- **Tasks:** 3
- **Files:** 3 — un fichier cree (`tests/test_docs_depannage.py`, 1 253 lignes, 62 895 octets), une page creee (`docs/depannage.md`, 96 lignes, 13 354 octets) et une ligne ajoutee (`docs/sommaire.md`, 1 insertion, 24 lignes avant et apres).
- **Commits:** 3, **zero fichier supprime** (`git diff --diff-filter=D --name-only 110951f..HEAD` : vide) ; diff cumule : `3 files changed, 1350 insertions(+)` (77 181 caracteres de patch).
- **Estimate vs actuals :** estimate `85 000` tokens, mesure `19 295` (chars/4 du diff realise) — l'estimate etait pessimiste d'un facteur ~4, comme la phase 5 l'a consigne ; aucune tache n'a ete sautee pour autant.

## Accomplishments

- **La page est indexee par le message, jamais par un symptome imagine (D-93).** `docs/depannage.md` porte les cinq sections du critere 1 dans l'ordre (`## Base absente ou vide`, `## Saisie invalide`, `## Calcul long`, `## Clavier inactif`, `## Résultat paginé`), un seul titre de niveau 1 (`# Dépannage`, egal au libelle d'index), le bloc `## Source de vérité` en dernier, et `[Retour au sommaire](sommaire.md)` en derniere ligne non vide ; octets **CRLF sans BOM** (96 fins de ligne pour 96 retours chariot).
- **Chaque message declare est confronte a sa provenance reelle, puis exige dans sa rubrique.** La table `MESSAGES` porte **32 entrees** — base 10, saisie 13, calcul 4, pagination 5 — reparties en trois modes de mesure : `cli_status` (3, capture de `_print_db_status` par `contextlib.redirect_stdout`), `web_render` (20, statut ou corps rendu par le client de test Flask en processus), `source_literal` (9, litteral lu dans le fichier producteur nomme : `dofus_stuff/cli.py` x3, `dofus_stuff/sync.py`, `dofus_stuff/web/routes.py` x4, `dofus_stuff/optimize/profile_input.py`). La bijection rubrique <-> table est controlee **famille par famille** : un message declare non cite, comme un message cite non declare, produit un constat nomme.
- **La sonde `_produire` est unique et chacune de ses 19 prises est verifiee.** 2 `GET` sur une application a catalogue vide (base absente, creee par le premier contact), 11 refus postes (`/search` x3, `/list`, `/item` x2, `/`, `/system`, `/db`, `/optimize/quick/classe`, `/optimize/wizard/slots`), le parcours simplifie **conduit pas a pas** (classe, elements, puis l'etape du niveau), et le recapitulatif du wizard en `GET` seul : **aucun niveau valide n'est jamais poste**, aucun calcul n'est lance. Si un message declare en mode `cli_status` ou `web_render` n'etait observe nulle part, `_produire` leve elle-meme un constat nommant les routes sondees — une sonde muette ne passe pas pour un vert (T-06-01-05). Mesure : la premiere execution a effectivement leve ce constat pour « Exemple : feu, terre air, ou multi. », la sonde a ete corrigee (le refus des elements est sonde **avant** de conduire l'etape), puis verte.
- **La famille sans message est un mecanisme (D-76).** « Clavier inactif » ne porte aucune entree de `MESSAGES` — et cette absence est controlee : la rubrique cite `autofocus`, `activeElement` et `preventDefault`, chacun est **aussi** exige dans le fichier qui le porte (`dofus_stuff/web/templates/screen.html`, `dofus_stuff/web/static/js/terminal.js`), et les trois ecrans sans champ (`/version`, `/db/status`, `/quit`) sont rendus pour verifier qu'ils ne portent **aucun** `id=\"main-input\"`.
- **La pagination est mesuree sur ses deux formes, sans assertion positionnelle fausse.** `routes.py:144-145` ne compose `PAGE n/n` dans la ligne de **statut** que si l'ecran compte plus d'une page (mesure : `/list?page=1&size=1` -> `PAGE 1/3 — ENTREE=VALIDER` ; `/sets?page=1&size=1` -> `ENTREE=VALIDER`), alors que la ligne de **corps** porte le motif sur les deux ecrans. `test_pagination_a_deux_formes` exige donc le motif compose dans le corps des deux ecrans et dans le statut du seul ecran pagine : une assertion qui l'exigerait partout serait rouge sur un produit correct (piege deja paye par le jalon).
- **La page n'ouvre aucune porte de sortie et ne fige aucune valeur de poste (D-73, D-75).** Aucun nombre de quatre chiffres ou plus, aucun motif de chemin de poste, aucun lien externe, aucun bloc de commandes, chaque chemin cite entre accents graves du bloc « Source de vérité » existe depuis la racine du depot ; le seul bloc de messages a copier est du texte, jamais une commande. Les lignes de la base locale sont citees par leur **libelle** (`Fichier : ` suivi d'un chemin de dossier temporaire dans la sortie reelle) precisement parce que la ligne entiere porterait une valeur volatile.
- **Le budget remplace la duree promise (D-19).** La rubrique « Calcul long » cite le **seul** message d'attente du produit et le budget (`--time-limit`, et le champ rendu `DUREE`), et `problemes_budget` refuse tout jeton de `JETONS_PROMESSE_DUREE` **dans cette rubrique** — controle localise, ajoute en tache 2 pour satisfaire le critere d'acceptation qui le nomme.
- **La page indexe sans redefinir (D-17).** `problemes_renvois` exige des rubriques « clavier » et « pagination » un lien markdown dont la **cible nue** est `installation.md` et `parcours-simplifie.md` (fragment admis) : la page renvoie vers ce qui est deja ecrit ailleurs, ajoute en tache 3 pour satisfaire le critere d'acceptation qui le nomme, et mord (morsure supplementaire : la cible remplacee par de la prose produit « mecanisme du clavier : ... ne renvoie pas vers installation.md (cibles lues : []) »).
- **La garde de cloture du harnais est auto-analysee par `ast`.** Elle refuse les imports qui tireraient la base ou le reseau (`sqlite3`, `subprocess`, `socket`, `urllib`, `requests`, `http`, ...), l'appel a `main()`, l'appel a `optimize_stuff` / `_run_optimize_and_redirect`, les appels `remove`/`unlink`/`rmdir`/`rmtree`, toute base construite avec un `data_dir` hors de `tmp_path` / `web_config`, et tout litteral de `/db/clear` ou `/db/sync`. Le module ne contient **aucune** occurrence de `skip` ni de `xfail` (mesure : 0 sur 1 253 lignes) — aucun saut ne peut masquer un controle.
- **Huit derives du plan, plus une derive supplementaire, toutes detectees** : voir § Verification. Aucune n'a eu besoin d'etre corrigee pour mordre.
- **La base du depot n'est jamais touchee.** Les trois batteries travaillent dans des copies sous `mktemp -d` ; l'empreinte `.data/dofus.sqlite3` (taille, mtime_ns, SHA-256) est identique avant le plan, apres chaque tache et apres la suite complete.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : tranche verticale — la page, sa ligne d'index et le harnais d'ancrage (`type=\"tracer\"`)** — `0f4cc45` (feat) : `docs/depannage.md` (96 lignes), `docs/sommaire.md` (1 insertion), `tests/test_docs_depannage.py` (1 167 insertions).
2. **Tache 2 : le budget du calcul long, ancre dans sa rubrique** — `f0bfec4` (test) : `OPTION_BUDGET`, `problemes_budget`, et leur branchement dans `test_messages_de_calcul_long` (46 insertions, 2 suppressions).
3. **Tache 3 : les renvois de mecanisme et la garde des cinq familles** — `0c672f7` (test) : `MOTIF_LIEN_DIRECT`, `RENVOIS_RUBRIQUES`, `problemes_renvois`, branches dans `test_les_cinq_familles_sont_couvertes` (43 insertions, 1 suppression).

**Plan metadata:** le commit de metadonnees de ce plan — `docs(06-01): complete la page de depannage indexee par le message reel` (le dernier de la branche, `git log -1`) : il porte ce SUMMARY, la position de `STATE.md`, la progression de `ROADMAP.md` et `AIDE-01` dans `REQUIREMENTS.md`.

## Files Created/Modified

- `docs/depannage.md` — **cree** (96 lignes, 13 354 octets, 96 fins de ligne pour 96 retours chariot, BOM absent, >= 90 lignes exigees). Un titre H1, cinq sections de niveau 2 dans l'ordre du critere 1, `## Source de vérité` en dernier, la ligne de retour en derniere ligne non vide. Chaque rubrique porte une phrase d'indexation (ce que la famille couvre, ou elle est lue), ses lignes de tableau (message + surface + geste) et ses renvois vers les pages qui decrivent deja le sujet (`cli.md`, `installation.md`, `base-locale.md`, `parcours-simplifie.md`, `wizard-avance.md`, `sommaire.md`).
- `docs/sommaire.md` — **modifie d'une ligne** : `| [Dépannage](depannage.md) | Retrouver la marche à suivre par le message affiché |`, ajoutee en fin de table `## Index` (>= 24 lignes exigees : 24 mesurees). La liste « Parcours conseillé » n'est **pas** convertie en liens (mesure : `problemes_index`, `problemes_h1` et `test_sommaire_index_labels_are_unique` lisent tout lien de `sommaire.md` comme une entree d'index ; un parcours en liens re-emettrait les libelles de l'index et ferait rougir trois gardes vertes).
- `tests/test_docs_depannage.py` — **cree** (1 253 lignes, 62 895 octets, 9 tests, >= 220 lignes exigees ; 1 253 fins de ligne pour 1 253 retours chariot, BOM absent). Contrat et limites dans la docstring du module ; garde de cloture auto-analysee ; table `MESSAGES` de provenance ; constantes `RUBRIQUES`, `RUBRIQUES_MECANISME`, `MECANISMES_CLAVIER`, `ECRANS_SANS_CHAMP`, les 20 `MOTIF_*` (dont `MOTIF_BUDGET`) et les constantes de contenu `MOTIF_VOLATILE`, `MOTIF_CHEMIN_POSTE`, `JETONS_PROMESSE_DUREE`, `MARQUEUR_CORPS`, `MARQUEUR_STATUT`, `MARQUEUR_SAISIE`, `LIEN_RETOUR`, `OPTION_BUDGET`, `RENVOIS_RUBRIQUES` ; lecteurs et sondes `_texte_page`, `_corps_par_titre`, `_lignes_du_corps`, `_statut`, `_sonde`, `_ajouter`, `_capture_cli`, `_produire`, `_rendus_sans_champ` ; fonctions pures `problemes_rubriques`, `problemes_messages`, `problemes_clavier`, `problemes_budget`, `problemes_renvois`, `problemes_page` ; analyseurs `ast` `_imports_du_module`, `_appels_du_module`, `_nom_appele`, `_noms_isoles`, `_cibles_data_dir`, `_litteraux_de_chemin_destructif`. Les helpers partages de `conftest.py` (`docs_dir`, `sections`, `normalize`, `client`) et les gardes de `tests/test_docs_structure.py` sont **reutilises tels quels**, jamais recopies (D-12).
- `dofus_stuff/**` — **aucun octet modifie** (mesure : `git status --short -- dofus_stuff` vide sur les trois commits ; le code est le referentiel, la page s'y conforme — D-103). `pyproject.toml` inchange, aucune dependance ajoutee.

## Verification

Toutes les commandes ont ete executees avec l'interpreteur epingle `./.venv/Scripts/python.exe` (D-15), jamais un `python` nu. Les batteries sont rejouables et **hors du depot** (`.gsd-tmp/batterie-06-01-t1.sh`, `-t2.sh`, `-t3.sh`, non suivies par git) : chacune copie l'arbre dans `mktemp -d`, mesure la copie **verte** avant mutation, mute la copie seule (par `python -c` avec `newline=\"\"`, donc sans perdre les CR), rejoue la suite complete, puis exige `[0-9]+ (failed|error)` **et** le motif nomme.

### Tache 1 — `0f4cc45`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_depannage.py -q` (premiere execution) | `3 failed, 6 passed in 0.39s` — constat `message non produit par le code` pour « Exemple : feu, terre air, ou multi. » : la sonde ne l'atteignait pas (voir § Issues) |
| `python -m pytest tests/test_docs_depannage.py -q` (apres correction de la sonde) | `9 passed in 0.31s` |
| `python -m pytest tests/test_docs_depannage.py tests/test_docs_structure.py -q` | `23 passed in 0.37s` — gardes existantes de `docs/` inchangees |
| `python -m pytest -q` | `228 passed in 4.52s` |
| batterie (4 morsures) | `mutation detectee (rubrique_retiree), motif \"rubrique de depannage absente\"` |
| | `mutation detectee (message_supprime), motif \"message non cite par sa rubrique\"` |
| | `mutation detectee (message_invente), motif \"message cite non declare\"` |
| | `mutation detectee (source_renommee), motif \"message non produit par le code\"` |
| **batterie du plan (tache 1)** | **`morsures 06-01 tache 1 : 4/4 detectees (copie verte avant chaque mutation)`** (24 s) |
| copie verte avant mutation (mesure commune aux trois batteries) | `225 passed, 3 skipped in 4.86s` — sauts **nommes** : `tests\\test_docs_base_locale.py:2323: base locale du depot absente`, `tests\\test_docs_parcours.py:2678: base locale absente : la mesure d'empreinte n'a pas d'objet`, `tests\\test_docs_wizard.py:2296: base locale absente : la mesure d'empreinte n'a pas d'objet` (la copie n'emporte pas `.data/`, ce qui est voulu) |

**Porte de retroaction du `type=\"tracer\"`** (mode automatise, `HUMAN_VERIFY_MODE=end-of-phase`, `<verify>` entierement automatise) : apres la tache 1, le module a ete rejoue vert (`9 passed`), les gardes existantes vertes (`23 passed`) et la batterie de la tache rejouee (`4/4`), puis l'execution s'est poursuivie sans point d'arret — aucun echec observe.

### Tache 2 — `f0bfec4`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_depannage.py -q` | `9 passed in 0.33s` |
| batterie (2 morsures) | `mutation detectee (saisie_hors_rubrique), motif \"message non cite par sa rubrique\"` |
| | `mutation detectee (refus_niveau_renomme), motif \"message non produit par le code\"` |
| **batterie du plan (tache 2)** | **`morsures 06-01 tache 2 : 2/2 detectees (copie verte avant chaque mutation)`** (12 s) |
| contre-mesure du controle ajoute (`problemes_budget`) | la rubrique « Calcul long » de la page livree cite `--time-limit` et ne porte aucun jeton de `JETONS_PROMESSE_DUREE` : `test_messages_de_calcul_long` vert, et le controle est branche dans ce test (donc une rubrique sans budget comme une duree promise rougissent le meme test) |

### Tache 3 — `0c672f7`

| Commande | Resultat observe |
|---|---|
| batterie (2 morsures) | `mutation detectee (jeton_mecanisme_retire), motif \"mecanisme du clavier\"` |
| | `mutation detectee (pagination_inconditionnelle), motif \"formes de la pagination\"` |
| **batterie du plan (tache 3)** | **`morsures 06-01 tache 3 : 2/2 detectees (copie verte avant chaque mutation)`** (13 s) |
| morsure supplementaire (renvoi D-17 retire de la rubrique « Clavier inactif », copie sous `mktemp -d`) | `1 failed, 8 passed` — `E AssertionError: depannage.md : constats sur les cinq familles : mecanisme du clavier : la rubrique « Clavier inactif » de depannage.md ne renvoie pas vers installation.md (cibles lues : []) ; attendu le renvoi vers la page qui decrit deja ce mecanisme, cette page indexant sans le redefinir (D-17)` |
| `python -m pytest -q` | `228 passed in 4.36s` |
| `python -m pytest -q --ignore=tests/test_docs_depannage.py` | `219 passed in 4.13s` (le compte avant ce plan) |
| **porte de fin de plan** (`pytest -q` encadre par deux mesures d'empreinte) | `228 passed in 4.36s` et empreinte `.data/dofus.sqlite3` **identique** : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` |

**Bilan des morsures : 9 jouees, 9 detectees, 0 corrigee pour mordre** — 4 (tache 1) + 2 (tache 2) + 2 (tache 3) + 1 supplementaire (les renvois D-17, ajoutes par le critere d'acceptation de la tache 3). Les trois batteries ont d'abord mesure la copie **verte** (`tests/test_docs_depannage.py` sans echec sur la copie avant mutation), donc aucune morsure n'est sterile ni tolerante ; chaque constat retrouve porte le motif de la **seule** derive visee.

**Aucun verrou ni coupee de securite** : aucun `git add .` (les trois commits indexent des chemins explicites), aucun fichier de `dofus_stuff/**`, `doc-agent.toml`, `.doc-agent/`, `gsd-auto*.toml`, `.planning/state.json`, `.gsd/` ni `.gsd-tmp/` n'est entre dans un commit ; aucun `push` ; aucun `db clear`, `db sync`, `db status`, `drop` ou suppression sous `.data/` ou `.doc-agent/` ; aucune dependance ajoutee.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocage : le decoupage de la page en trois taches ne peut pas rester vert] la page entiere et la table `MESSAGES` complete sont livrees en tache 1**

- **Found during:** Tache 1 (lecture de l'action avant ecriture)
- **Issue:** l'action de la tache 1 fige `RUBRIQUES` = **les cinq** rubriques du critere 1 et fait de `test_rubriques_de_depannage` un test de la tache 1 ; ce controle exige de chaque rubrique declaree qu'elle existe **et** que son corps soit adosse a `MESSAGES`. Une page ne portant que la rubrique « base » (ou des rubriques vides) est donc rouge des la tache 1, et des qu'une rubrique existe avec ses lignes, `problemes_messages` refuse toute ligne non declaree (`message cite non declare`). L'action de la tache 1 decrit par ailleurs `_produire` **de bout en bout**, y compris le parcours simplifie conduit pas a pas et le refus de niveau, c'est-a-dire la sonde des familles des taches 2 et 3.
- **Fix:** la tache 1 livre la page dans son entier (cinq rubriques, 32 entrees de `MESSAGES`) et le harnais complet ; les taches 2 et 3 livrent les **deux controles** que leurs criteres d'acceptation nomment et qui n'existaient pas encore — `problemes_budget` (l'option de budget lue sur le parseur, aucune duree promise dans la rubrique) et `problemes_renvois` (les renvois D-17 des rubriques « clavier » et « pagination ») —, chacun avec sa morsure, plus leurs bits de table. Aucun controle n'a ete affaibli pour obtenir le vert : le contraire (deux controles nommes par les criteres) a ete ajoute.
- **Files modified:** `tests/test_docs_depannage.py` (taches 2 et 3 : commits `f0bfec4` et `0c672f7`)
- **Verification:** `9 passed` sur le module aux trois taches ; `228 passed` sur la suite ; 9/9 morsures detectees.
- **Committed in:** `0f4cc45` (page et table), `f0bfec4` et `0c672f7` (les deux controles).

**2. [Rule 2 — Controle manquant pour un critere d'acceptation nomme] `MOTIF_BUDGET` et `MOTIF_LIEN_DIRECT` ajoutes**

- **Found during:** Taches 2 et 3 (lecture des criteres d'acceptation)
- **Issue:** les criteres d'acceptation exigent que la rubrique « Calcul long » **cite `--time-limit`** et que la rubrique « clavier » **renvoie vers `docs/installation.md`** ; aucun controle du module ne le prouvait (le controle de page ne distingue pas la rubrique qui porte le budget, et aucun lecteur de liens n'existait).
- **Fix:** deux fonctions pures de plus (`problemes_budget`, `problemes_renvois`), deux constantes de plus (`OPTION_BUDGET`, `RENVOIS_RUBRIQUES`), un motif de plus (`MOTIF_BUDGET`) et un lecteur de cibles de liens (`MOTIF_LIEN_DIRECT`, cible lue nue, fragment admis). Les deux fonctions rendent des constats **nommes** et sont branchees dans les tests de leurs familles.
- **Files modified:** `tests/test_docs_depannage.py`
- **Verification:** les deux controles sont verts sur la page livree, et la morsure supplementaire (renvoi remplace par de la prose) les fait mordre.
- **Committed in:** `f0bfec4`, `0c672f7`

### Ecarts d'interpretation (documentes, jamais des affaiblissements)

- **`_texte_page` garde son nom de la phase 5, et non `_texte_rendu`.** L'inventaire d'artefacts du plan nomme trois « lecteurs locaux » : `_texte_rendu`, `_lignes_du_corps`, `_statut`. Le module reutilise `_texte_page` (le nom et le role epingles par la phase 5 : lire une page de `docs/`, ici `depannage.md`) et lit les rendus par `_lignes_du_corps` / `_statut` / `_sonde`. Creer un `_texte_rendu` n'aurait ajoute ni lecture ni constat, et aurait duplique un lecteur sous un second nom (D-12).
- **La comparaison de provenance est une appartenance de sous-chaine.** Un message declare qui serait contenu dans un autre message passerait : la limite est ecrite dans la docstring du module (AR-5, honnetete des limites) plutot que masquee, et le controle qui possede le pouvoir complementaire est la **bijection** rubrique <-> table, qui est une egalite de deux ensembles de chaines.
- **Le mode `source_literal` prouve une presence, pas une atteinte.** Il etablit que la chaine est un litteral du fichier nomme, jamais qu'un chemin d'execution l'imprime — c'est la limite honnete du mode pour les messages que seule `main()` imprimerait, et elle est ecrite dans la docstring.
- **L'assertion CRLF depend de `core.autocrlf` du poste et n'est pas presentee comme portable** (aucun `.gitattributes` dans le depot) : la limite est ecrite la ou elle vit (Pitfall 11, backstop du plan).
- **La page cite les libelles, jamais les lignes entieres de la base locale.** La sortie reelle de `_print_db_status` porte `Fichier : ` suivi d'un chemin de dossier temporaire : la page cite donc le libelle, et les deux messages de l'etat de la base sont exiges en **ligne de corps** du rendu (mesure), pas en ligne de statut.
- **Bookkeeping du ledger : la ligne de la phase 5 du `ROADMAP.md` a ete rendue coherente.** Elle portait `- [ ]` **et** `(completed 2026-09-11)` tout en annoncant `In Progress` dans la table de progression, alors que `.planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-VERIFICATION.md` existe et porte `status: passed` : la case est cochee et la table dit `4/4 | Complete | 2026-09-11`. Aucune autre ligne d'une autre phase n'a ete touchee, et le compte `completed_phases` de `STATE.md` suit cette correction (5/6, 83%). Les fichiers de ledger modifies par le commit de metadonnees (`.planning/STATE.md`, `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`) sont ceux que les plans des phases 2 a 5 modifient eux aussi a leur cloture.

---

**Total deviations:** 2 auto-fixed (le decoupage de livraison en trois taches, rendu impossible par les controles de la tache 1 elle-meme ; deux controles manquants pour des criteres d'acceptation nommes) et 6 ecarts d'interpretation documentes (dont la mise en coherence de la ligne de la phase 5 dans le ledger), tous plus stricts ou plus lisibles, aucun plus permissif. Aucun ecart de perimetre : trois fichiers livres (`git diff --stat 110951f..HEAD` : `docs/depannage.md` 96 insertions, `docs/sommaire.md` 1 insertion, `tests/test_docs_depannage.py` 1 253 insertions nettes), `dofus_stuff/**` et `pyproject.toml` inchanges, rien de publie, deploye, achete ou supprime.
**Impact on plan:** aucun affaiblissement d'un controle pour obtenir le vert ; la couverture du critere 1 et de `AIDE-01` est atteinte telle que le plan la decrit, et les deux controles ajoutes couvrent deux criteres d'acceptation qui n'etaient autrement pas prouves.

## Issues Encountered

- **La sonde etait muette pour le refus des elements, et le controle l'a dit.** A la premiere execution, `3 failed, 6 passed` avec le constat exact : `message non produit par le code : aucune des routes sondees (...) ne porte : « Exemple : feu, terre air, ou multi. » (famille saisie, mode web_render)`. Le parcours conduisait l'etape des elements avec une valeur **valide**, donc le refus de cette etape n'etait jamais rendu. Correction : le refus est sonde **avant** de conduire l'etape (`{"cmd": "zzz"}` puis `{"cmd": "feu"}`), ce qui laisse l'etape a remplir entre les deux. Le controle n'a pas ete adouci ; la sonde a ete corrigee, comme le prevoit le protocole.
- **La mutation `pagination_inconditionnelle` a d'abord ete un **no-op**, et la batterie a crie `MUTATION NON DETECTEE`.** `dofus_stuff/web/routes.py` est en CRLF sur ce poste (1 384 retours chariot pour 1 384 fins de ligne) : le motif de remplacement ecrit en LF ne correspondait a rien, l'assertion de comptage de ma batterie a leve, et la copie a ete rejouee **non mutee** (d'ou le `225 passed, 3 skipped` visible dans la sortie). Correction : toute mutation de cette batterie passe par `python -c` qui lit et reecrit avec `newline=\"\"` et un motif portant les `\r\n` — mutation appliquee une seule fois (garde d'unicite verifiee), puis morsure detectee. Aucun fichier du depot n'a ete touche par cette erreur (les mutations vivent dans `mktemp -d`).
- **Les copies de batterie n'emportent pas `.data/`, donc trois mesures sautent** (`225 passed, 3 skipped`, sauts **nommes** : base locale du depot absente). C'est voulu — la base du depot ne doit pas entrer dans une copie de travail des morsures — et les trois sauts sont des mesures d'empreinte, pas des controles de ce plan. La suite du poste, elle, ne saute aucun test : `228 passed`, 0 skipped.
- **Aucun fichier hors perimetre touche** : `git status --short` ne montre, pour les trois commits, que `docs/depannage.md`, `docs/sommaire.md` et `tests/test_docs_depannage.py` ; `.gsd-tmp/` (les trois batteries rejouables) et ce SUMMARY restent hors des commits de tache.
- **Aucune morsure n'a eu besoin d'etre corrigee pour mordre** : les huit morsures du plan ont ete discriminantes a leur premiere execution complete, et la neuvieme (renvoi D-17) a mordu du premier coup.

## Limites declarees, jamais revendiquees (D-85)

- **La prose libre de la page n'est pas verifiee** : l'invitation a chercher par le message, la clarte des renvois et la justesse redactionnelle restent hors de portee d'un test ; les controles portent sur les rubriques, les messages et les valeurs **cites** (`verification: backstop` du plan).
- **La portabilite de l'assertion CRLF hors d'un poste dont `core.autocrlf` vaut `true` reste non prouvee** (aucun `.gitattributes`).
- **Le mode `source_literal` est une lecture de fichier, pas une execution** : il prouve la presence d'un litteral, jamais qu'un chemin d'execution l'atteint.
- **L'execution du JavaScript n'est pas revendiquee** : `terminal.js` est lu pour ses jetons (`activeElement`, `preventDefault`), aucun navigateur, aucun DOM, aucune execution JS.
- **`main()` n'est jamais execute** : les messages que seule la ligne de commande imprime sont couverts par leur litteral de source, pas par une execution — la limite est ecrite dans la docstring du module.
- **L'absence de toute connexion reseau pendant la suite entiere n'est pas etablie par ce plan** : la garde `ast` du module dit ce que **ce** module importe et appelle, jamais ce qu'un autre chemin ferait ; le membre « aucune connexion reseau, `main()` jamais execute » du critere 5 est livre au plan 06-04 (greffon `.gsd-tmp/no_net.py`).

## Known Stubs

Aucun. Ce plan n'ajoute que deux pages et un module de test : aucun chemin de code produit, aucune valeur vide, aucun libelle de remplacement, aucun `TODO`/`FIXME`, aucun test desactive (0 occurrence de `skip` / `xfail` dans le module). La suite du poste ne compte aucun test saute : `228 passed`, 0 skipped.

## Threat Flags

Aucun. Les fichiers livres n'introduisent aucune surface nouvelle : pas d'endpoint, pas de chemin d'authentification, pas d'acces fichier nouveau (la lecture de `.data/dofus.sqlite3` pour l'empreinte est celle des registres `T-05-13`/`T-05-17`, et elle est faite en lecture d'octets, jamais par SQLite), aucune dependance ajoutee (`T-06-SC` : sans objet). Les sondes du module travaillent sur des bases construites sous `tmp_path` et le module ne poste qu'un niveau **hors bornes** : le refus precede le calcul, ce que la garde `ast` interdit de contourner.

## Self-Check

- **Fichiers livres** : `docs/depannage.md` — `FOUND` (96 lignes, `## Source de vérité` present) ; `docs/sommaire.md` — `FOUND` (24 lignes, `| [Dépannage](depannage.md) |` present) ; `tests/test_docs_depannage.py` — `FOUND` (1 253 lignes, `def test_messages_de_base_absente_ou_vide` present, 9 tests collectes).
- **Ledger** : `.planning/STATE.md` — `FOUND` (20/23 plans, 5/6 phases, 83%, `state_head` = `0c672f7`) ; `.planning/ROADMAP.md` — `FOUND` (06-01 coche, table de progression 1/4 pour la phase 6) ; `.planning/REQUIREMENTS.md` — `FOUND` (`AIDE-01` coche et `Complete`).
- **Commits** : `0f4cc45` — `FOUND` ; `f0bfec4` — `FOUND` ; `0c672f7` — `FOUND` (`git log --oneline`).
- **Compteur mesure, jamais narre** : `git rev-list --count 110951f83d9baff3805c0bcb464525bf51f93514..HEAD` = **4** au total — **3** commits de tache (mesure prise avant le commit de metadonnees, exactement comme le fait le SUMMARY 05-03, qui porte lui aussi 3 alors que le compte final est 4) plus le commit de metadonnees de ce plan (le dernier de la branche) ; le registre de plan (`.git/gsd-plan-head-before-6-01`) porte bien `110951f83d9baff3805c0bcb464525bf51f93514` comme base.
- **Compteurs de tests mesures** : `228 passed` (suite entiere), `219 passed` sans ce module, `9 passed` sur le module, `225 passed, 3 skipped` sur une copie sans `.data/`.
- **Morsures** : 9 jouees, 9 detectees (4 + 2 + 2 + 1), chacune sur copie verte avant mutation, chacune avec le motif nomme.
- **Empreinte `.data/dofus.sqlite3`** : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique a la valeur de reference des phases 5 et 6, mesuree avant le plan, apres chaque tache et apres la suite complete.

## Self-Check: PASSED
