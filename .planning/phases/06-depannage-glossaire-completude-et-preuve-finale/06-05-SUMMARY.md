---
phase: 06-depannage-glossaire-completude-et-preuve-finale
plan: 05
subsystem: documentation
tags: [markdown, crlf, pytest, controle-de-portee, absolu-de-portee, pagination, oracle-du-produit, preuve-de-morsure, documentation-francaise]

# Dependency graph
requires:
  - phase: 06-01
    provides: "docs/depannage.md et tests/test_docs_depannage.py : la page livree (96 lignes, 13354 octets, CRLF) dont la rubrique « Resultat pagine » portait l'absolu de portee signale par le defaut T3 de 06-VERIFICATION.md, et le module d'ancrage (1253 lignes, 9 tests) ou le nouveau controle a ete ajoute"
  - phase: 06-04
    provides: "Le patron de la preuve de morsure sur copie mesuree verte avant mutation (tests/test_docs_mutation.py, 14 morsures declarees), l'empreinte en lecture seule de .data/dofus.sqlite3 (24989696, 1788730056843137500, e3793d64...) et le greffon de refus reseau .gsd-tmp/no_net.py (6 pieges armes avant la collecte)"
provides:
  - "docs/depannage.md : la rubrique « Resultat pagine » bornee a ses deux producteurs mesures — la surface servie par l'application (dofus_stuff/web/routes.py, statut garde par « plus d'une page », corps « porte toujours ») et les deux ecrans de sauvegardes (dofus_stuff/web/static/js/terminal.js, statut sur « une seule page » et « aucune ligne de pagination » dans le corps) — et la rubrique « Saisie invalide » desambiguee, AUCUN RESULTAT. n'etant plus range parmi les refus qui tombent avant tout travail"
  - "tests/test_docs_depannage.py : la fonction problemes_pagination et son test test_pagination_bornee_a_ses_deux_producteurs (10e test du module), lies aux deux comportements mesures dans les fichiers producteurs, avec les trois motifs formes de la pagination, surface de pagination non declaree et absolu de pagination non borne"
  - "La preuve que le controle peut rougir, mesuree : 5 constats sur la page livree par 06-01 (3 de surface, 2 d'absolu), 0 sur la page corrigee, et 3/3 morsures sur copies mesurees vertes avant mutation (absolu 2 constats, jeton de condition 1, procede du script 1)"
affects: [verification-phase-6, milestone-documentation]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart est consigne tel quel : il mesure le pessimisme de l'estimate, pas un travail non fait.
actuals:
  tokens: 2962      # chars/4 sur le diff realise (11 850 caracteres sur 186 lignes modifiees, 2 fichiers)
  tasks: 2
  commits: 2        # MESURE : git rev-list --count c47a7df4931c6d1fa19d6105b905c402aa77cb50..HEAD = 2
  plan_head_before: c47a7df4931c6d1fa19d6105b905c402aa77cb50

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (aucun paquet installe, pyproject.toml inchange)
  patterns:
    - "Le controle s'ancre au **procede mesure** de chaque fichier producteur, avec son nombre d'occurrences : la garde elle-meme pour la surface servie par l'application (routes.py:144-145, 1 occurrence), la ligne de corps toujours composee (:477 et :543, 2 occurrences), et la composition inconditionnelle du script adossee a `setStatus(` (terminal.js:370 et :400, 2 occurrences) — un procede deplace ou une occurrence perdue est un constat, jamais un vert silencieux"
    - "L'asymetrie est verifiee dans les deux sens : la surface servie par l'application doit garder sa garde (`total > 1` : 3 occurrences du fichier bornees a la navigation, :133 et :137, plus celle du statut) et la surface des sauvegardes ne doit en porter **aucune** (`total > 1` : 0 occurrence mesuree dans terminal.js, `total` etant borne par `Math.max(1, ...)`)"
    - "Un **absolu de portee** est un constat nomme : la liste des marques est finie, declaree (`ABSOLUS_PAGINATION`, 8 marques) et ecrite en constantes, jamais dans une ligne d'assertion — pytest reproduisant la ligne source de l'`assert`, une marque ecrite en clair y serait trouvee meme si aucun constat n'avait ete produit (regle du plan 03-03)"
    - "L'ecriture de la page et du module se fait **au niveau des octets** (`read_bytes()` / `write_bytes()`, paragraphes joints par la sequence CRLF explicite) : `read_text`/`write_text` rameneraient le CRLF a du LF et `sed -i` retire le CR sur cette plateforme ; la page reste a 99 CRLF pour 99 lignes, sans BOM"

key-files:
  created: []
  modified:
    - docs/depannage.md
    - tests/test_docs_depannage.py

key-decisions:
  - "La page se conforme au code, jamais l'inverse (`D-88`, `D-103`) : les deux oracles (`dofus_stuff/web/routes.py`, `dofus_stuff/web/static/js/terminal.js`) ont ete lus en octets et **jamais ecrits** ; `git status --porcelain -- dofus_stuff` rend 0 avant et apres chaque tache."
  - "La phrase corrigee dit exactement ce que le code fait, sans « seulement », sans « jamais » et sans « quel que soit l'ecran » que le produit ne soutient pas : la rubrique nomme desormais le **fichier producteur** de chaque ligne de statut et la condition de chacun, au lieu de la regle unique que portait la page livree."
  - "Le controle **presuppose** le controle comportemental deja livre (`test_pagination_a_deux_formes`) et ne le reecrit pas : c'est lui qui rend les deux ecrans servis par l'application et mesure statut et corps ; `problemes_pagination` est statique, lit les deux fichiers producteurs, n'execute pas le JavaScript et ne rend pas les deux ecrans de sauvegardes — cette limite est ecrite dans sa docstring et dans ce rapport."
  - "La preuve que le controle peut rougir est portee par deux mesures et non par une relecture : 5 constats sur une copie de la **page livree** (3 de surface — les deux surfaces non nommees et le jeton « aucune ligne de pagination » absent — et 2 d'absolu : « aucun motif a son statut », « n'ajoute aucun motif »), et 3/3 morsures sur des copies mesurees vertes avant mutation (`absolu_sans_surface` 2 constats, `condition_effacee` 1, `procede_js_efface` 1)."
  - "Aucun controle existant n'a ete affaibli pour obtenir le vert : la garde de cloture du harnais reste telle quelle (`ast`, aucun import de base/processus/socket/reseau, aucun appel de suppression, aucune racine interdite en moins), `problemes_page`, `test_pagination_a_deux_formes` et les 14 morsures declarees de `tests/test_docs_mutation.py` ne sont pas touches, et le nouveau test est collecte par son nom (aucune enumeration de tests modifiee)."

requirements-completed: [AIDE-01]

# Coverage metadata (#1602) — une entree par livrable de ce plan.
coverage:
  - id: D1
    description: "docs/depannage.md : rubrique « Resultat pagine » bornee a ses deux producteurs mesures (routes.py garde par plus d'une page et corps toujours pagine ; terminal.js sans garde, une seule page, corps sans ligne de pagination) et rubrique « Saisie invalide » desambiguee (AUCUN RESULTAT. ecrit apres la recherche)"
    requirement: "AIDE-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_depannage.py::test_pagination_bornee_a_ses_deux_producteurs (0 constat sur la page corrigee ; 5 constats sur une copie de la page livree par 06-01)"
        status: pass
      - kind: unit
        ref: "pytest tests/test_docs_depannage.py tests/test_docs_structure.py tests/test_docs_completude.py tests/test_docs_code_anchor.py -q -> 39 passed"
        status: pass
    human_judgment: false
  - id: D2
    description: "tests/test_docs_depannage.py : problemes_pagination, ses deux motifs de surface, ses 8 marques d'absolu et test_pagination_bornee_a_ses_deux_producteurs, lies aux deux comportements mesures des fichiers producteurs"
    requirement: "AIDE-01"
    verification:
      - kind: unit
        ref: "pytest tests/test_docs_depannage.py -q -> 10 passed"
        status: pass
      - kind: integration
        ref: "3 morsures sur copies sous mktemp -d (absolu_sans_surface / condition_effacee / procede_js_efface), copie verte avant chaque mutation, motif nomme present -> 3/3 detectees"
        status: pass
    human_judgment: false

# Metrics
duration: 7min
completed: 2026-09-12
status: complete
---

# Phase 6 Plan 05 : portee de la pagination bornee a ses deux producteurs, et controle qui peut la voir

**`docs/depannage.md` ne dit plus que « un ecran qui n'a qu'une seule page n'ajoute aucun motif a son statut » : la rubrique nomme les deux producteurs mesures de la ligne de statut — `dofus_stuff/web/routes.py` (composition gardee, corps toujours pagine) et `dofus_stuff/web/static/js/terminal.js` (motif des la premiere page, corps sans ligne de pagination) — et `problemes_pagination` rougit des qu'un absolu de portee, une surface non nommee ou un jeton de condition disparait.**

## Performance

- **Duration:** ~7 min (encadree par deux horodatages mesures : `2026-09-12T03:44:52+02:00`, premier artefact ecrit par la session, et `2026-09-12T03:52:07+02:00`, fin du dernier controle rejoue — soit **7 min 15 s** ; l'intervalle entre le premier et le dernier commit de tache est de **2 min 43 s**, de `03:45:36` a `03:48:19`, et le commit de metadonnees est a `03:51:44`).
- **Started:** 2026-09-12T01:44:52Z (horodatage pris a l'ecriture du premier script d'execution, apres la lecture du plan, de `06-VERIFICATION.md` et des deux oracles)
- **Completed:** 2026-09-12T01:51:44Z (commit de metadonnees de ce plan ; le dernier controle — suite entiere `250 passed in 5.71s` — est rejoue juste apres)
- **Tasks:** 2
- **Files:** 2 modifies, aucun fichier cree, aucun fichier supprime — `docs/depannage.md` (96 -> 99 lignes, 13354 -> 14258 octets) et `tests/test_docs_depannage.py` (1253 -> 1430 lignes, 9 -> 10 tests).
- **Commits:** 2 commits de tache + le commit de metadonnees de ce plan ; `git diff --diff-filter=D --name-only` vide sur l'intervalle. Diff cumule : `docs/depannage.md | 6 insertions(+), 3 deletions(-)` et `tests/test_docs_depannage.py | 177 insertions(+)`.
- **Estimate vs actuals :** estimate `45 000` tokens, mesure `**2 962**` (chars/4 sur 11 850 caracteres de diff realise) — l'estimate etait pessimiste d'un facteur ~15, comme les phases precedentes de ce milestone l'ont consigne ; les deux taches sont livrees et les deux mesures de rouge mordent.

## Accomplishments

- **L'absolu de portee du defaut `T3` a disparu, remplace par les deux comportements mesures (`D-19`).** La page livree affirmait que « la ligne de **statut** ne porte le motif de page que lorsque l'ecran est reellement pagine — un ecran qui n'a qu'une seule page n'ajoute aucun motif a son statut ». C'est vrai des ecrans que l'application sert elle-meme (`dofus_stuff/web/routes.py:144-145`, ou la composition est sous la garde `if total > 1:`) et **faux** des deux ecrans de sauvegardes, ou le script compose `"PAGE " + page + "/" + total` sans aucune garde (`terminal.js:370` et `:400`, `total` borne par `Math.max(1, ...)`), si bien que `PAGE 1/1` est ecrit des la premiere page. La rubrique porte desormais quatre paragraphes bornes a chaque surface — la troisieme ligne affirme l'inverse de la regle livree, parce que c'est ce que le code fait — et le corps de la ligne de tableau du message `PAGE {page}/{total}` porte les deux conditions (premiere cellule inchangee).
- **La rubrique « Saisie invalide » ne range plus `AUCUN RESULTAT.` parmi les refus qui tombent avant tout travail.** Le message est ecrit par `dofus_stuff/web/routes.py:351` **apres** la recherche de `:334-335` : la phrase d'ouverture nomme maintenant l'exception (« Une ligne de cette rubrique fait exception et le dit elle-meme »), le message reste cite dans sa ligne de tableau et n'est donc plus confondu avec un refus ni avec une panne.
- **Le nouveau controle est lie aux deux comportements mesures, pas a une seule source.** `problemes_pagination` lit les deux fichiers producteurs depuis `RACINE_DEPOT` en `read_bytes()` et exige, dans l'ordre et surface par surface : le nombre d'occurrences mesure du procede de statut (garde pour `routes.py`, composition inconditionnelle pour `terminal.js`), la ligne de corps de la surface servie par l'application (2 occurrences de `f"PAGE {page}/{total_pages}"`), l'**absence** de toute garde `total > 1` dans le script, l'adossement de chaque composition du script a `setStatus(` dans les 80 caracteres qui precedent (le script portant les seules compositions lues par la page), le nom du fichier producteur dans le corps normalise de la rubrique, et les quatre jetons de condition. Un procede deplace, une occurrence perdue ou une troisieme composition hors de la ligne de statut rougit avec `formes de la pagination` : jamais un vert silencieux.
- **Le rouge est mesure avant d'etre cru, sur la page livree (backstop `D-85` comble par une mesure).** Sur une copie de la **page livree par 06-01** (96 lignes, 96 CRLF, 13354 octets — identique a l'octet a la version d'avant correction), le module rend `1 failed, 9 passed` avec **5 constats**, exactement ceux annonces par le planificateur : `surface de pagination non declaree` x3 (les deux surfaces non nommees, puis le jeton « aucune ligne de pagination » absent pour la surface des sauvegardes) et `absolu de pagination non borne` x2 (« aucun motif a son statut », « n'ajoute aucun motif »). Sur la page **corrigee**, il rend **0 constat** (`10 passed in 0.40s`). Le rouge tient donc a ce que la phrase dit du produit, jamais a la presence d'un fichier ni a une exception.
- **La copie est mesuree verte avant chaque mutation, et les trois derivees mordent avec leur motif nomme.** Mesure d'executeur (outil hors livrable, `.gsd-tmp/06-05-*`) : aucune ligne `COPIE ROUGE AVANT MUTATION`, puis `mutation detectee (absolu_sans_surface)` avec `absolu de pagination non borne` (**2** constats dans le message d'echec), `mutation detectee (condition_effacee)` avec `surface de pagination non declaree` (**1** constat) et `mutation detectee (procede_js_efface)` avec `formes de la pagination` (**1** constat) — soit `morsures 06-05 tache 2 : 3/3 detectees`, aucune `MUTATION NON DETECTEE`. La mutation `absolu_sans_surface` reintroduit **exactement** le defaut `T3` sur une copie corrigee : c'est cette mesure qui remplace la relecture humaine du rouge.
- **Le gabarit de la page tient, et les modules qui l'ancrent restent verts (`D-102`, `D-69`).** Mesure : 99 lignes pour 99 CRLF, aucun BOM, un seul H1 egal au libelle d'index, les cinq rubriques de `RUBRIQUES` dans l'ordre, `## Source de verite` en derniere section, `[Retour au sommaire](sommaire.md)` en derniere ligne non vide, aucun nombre de quatre chiffres ou plus, aucun chemin de poste, aucun lien externe. Les quatre modules qui ancrent la page rendent `39 passed in 0.36s`.
- **La base du depot est intacte, mesuree en lecture seule (`GARD-03`, `D-104`).** Empreinte `(taille, mtime_ns, sha256)` lue en octets avant **et** apres la suite complete : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`, identique, et identique a la valeur de reference donnee par l'affectation. Aucune commande du plan n'approche `.data/` en ecriture : jamais de `db clear`, de `db sync`, de `db status`, de drop ni de suppression.
- **Les deux executions finales sont citees, jamais estimees.** Suite entiere : `250 passed in 5.78s` (249 avant ce plan) ; suite sous le greffon de refus reseau et de piege `main()` : `250 passed in 5.73s`, precedee de la ligne `greffon de preuve 06-04 : 6 pieges armes avant la collecte -> socket.socket, socket.create_connection, socket.socketpair, urllib.request.urlopen, dofus_stuff.cli.main, dofus_stuff.web.__main__.main`. La seconde execution n'est pas un doublon : c'est elle qui satisfait le membre « aucun acces reseau, `main()` jamais execute, aucun serveur » du critere 4 de la phase.

## Task Commits

Chaque tache a ete commitee atomiquement, par chemin explicite (jamais `git add .`, `D-91`/`D-105`) :

1. **Tache 1 : borner la portee de la pagination a ses deux producteurs, et desambiguer la phrase de la saisie invalide** — `b791063` (docs) : `docs/depannage.md` (3 remplacements de ligne au niveau des octets) — `1 file changed, 6 insertions(+), 3 deletions(-)`.
2. **Tache 2 : le controle qui tient la portee de la pagination, et sa preuve de morsure** — `d2a5dab` (test) : `tests/test_docs_depannage.py` (+177 lignes : 2 motifs, 5 constantes de procede, `SURFACES_PAGINATION`, `ABSOLUS_PAGINATION`, `problemes_pagination`, `test_pagination_bornee_a_ses_deux_producteurs`) — `1 file changed, 177 insertions(+)`. **Aucun fichier supprime** (`git diff --diff-filter=D --name-only` vide apres chaque commit).

**Plan metadata:** le commit de metadonnees de ce plan porte ce SUMMARY, `STATE.md`, `ROADMAP.md` et `REQUIREMENTS.md`. `git rev-list --count c47a7df..HEAD` = **2** : deux commits de tache, aucun commit intermediaire de correction.

## Files Created/Modified

- `docs/depannage.md` — **modifie** (96 -> 99 lignes, 13354 -> 14258 octets, 99 CRLF, aucun BOM) : rubrique « Saisie invalide » (l'ouverture nomme l'exception `AUCUN RESULTAT.`), rubrique « Resultat pagine » (quatre paragraphes, un par surface et un par conclusion, chacun ancre a son fichier producteur) et ligne de tableau du message `PAGE {page}/{total}` (troisieme cellule portant les deux conditions). Aucune autre page de `docs/` n'est touchee : les 8 pages epinglees et l'index ne bougent pas (`D-102`).
- `tests/test_docs_depannage.py` — **modifie** (1253 -> 1430 lignes, 9 -> 10 tests) : `MOTIF_PAGINATION_SURFACE`, `MOTIF_PAGINATION_ABSOLU` a cote de `MOTIF_PAGINATION` ; `MOTIF_GARDE_STATUT_ROUTES`, `MOTIF_CORPS_ROUTES`, `MOTIF_STATUT_JS`, `MOTIF_ECRITURE_STATUT_JS`, `MOTIF_GARDE_PAGINATION`, `SURFACES_PAGINATION` (2 surfaces, avec leurs occurrences attendues et leurs jetons de condition) et `ABSOLUS_PAGINATION` (8 marques) apres `MOTIF_PAGE_COMPOSE` ; la fonction `problemes_pagination(docs_dir, sections, normalize) -> list[str]` apres `problemes_page` ; le test `test_pagination_bornee_a_ses_deux_producteurs(docs_dir, sections, normalize)` apres `test_pagination_a_deux_formes`. Aucun import nouveau (`re`, `Path` et les fixtures existantes suffisent), aucune enumeration de tests modifiee.
- `dofus_stuff/web/routes.py` et `dofus_stuff/web/static/js/terminal.js` — **aucun octet modifie** : les deux oracles sont lus en octets par le controle et conformes a ce que la page affirme (`D-88`, `D-103`). `git status --porcelain -- dofus_stuff` rend `0` (`git diff --name-only HEAD -- dofus_stuff` : `0`).
- `.data/dofus.sqlite3` — **aucun octet modifie** : lu en octets pour l'empreinte avant et apres la suite, `sha256` et `mtime_ns` identiques.
- `.gsd-tmp/` (hors livrable, non suivi par git) — l'outillage d'executeur : `06-05-t1-apply.py` et `06-05-t2-apply.py` (les deux ecritures, au niveau des octets, la seconde extrayant les blocs de code du `PLAN.md` ligne a ligne), `06-05-page-livree-avant.md` (copie d'octets de la page livree par 06-01, support de la mesure de rouge) et `06-05-module-avant.py`.

## Decisions Made

- **La page se conforme au code, jamais l'inverse.** Les deux oracles (`routes.py`, `terminal.js`) ont ete lus avant d'ecrire, et chaque affirmation de la rubrique est adossee a une ligne mesuree : `routes.py:144-145` (garde du statut), `:477` et `:543` (lignes de corps toujours composees), `:334-335` puis `:351` (recherche puis `AUCUN RESULTAT.`), `terminal.js:370` et `:400` (compositions inconditionnelles, adossees a `setStatus(`), `terminal.js:11` (l'element `.row.status`). Aucun fichier de `dofus_stuff/**` n'a ete ecrit.
- **Le controle est statique et le dit.** `problemes_pagination` lit les deux fichiers producteurs ; il n'execute pas le JavaScript, ne rend pas les deux ecrans de sauvegardes et ne remplace ni ne reecrit `test_pagination_a_deux_formes` (le controle comportemental livre par 06-01, qui rend les deux ecrans de liste et mesure statut et corps). Cette separation est ecrite dans la docstring de la fonction et dans les limites de ce rapport.
- **Le rouge est mesure sur la page livree, pas raconte.** Une copie d'octets de la page d'avant correction a servi de support : 5 constats, exactement les deux surfaces non nommees, le jeton de condition absent et les deux marques d'absolu. C'est la mesure qui remplace la relecture humaine, et c'est aussi ce qui prouve que le nouveau test n'est pas un test qui passe par construction.
- **Aucun controle existant n'a ete affaibli pour obtenir le vert.** Le nouveau test est collecte par son nom ; la garde de cloture du harnais (auto-analyse par `ast`) reste verte sans modification, `problemes_page` et `test_pagination_a_deux_formes` sont intacts, et `tests/test_docs_mutation.py` garde ses 14 morsures declarees (fichier non touche).
- **Les ecritures se font en octets, jamais par `read_text`/`write_text` ni `sed -i`.** La page reste a 99 CRLF pour 99 lignes sans BOM, et le module a 1430 lignes pour 1430 CRLF : la mesure est verifiee apres chaque ecriture, pas supposee.

## Deviations from Plan

**None — le plan a ete execute exactement tel qu'ecrit**, et ses trois mesures annoncees ont ete retrouvees a l'identique :

- page corrigee : 99 lignes / 99 CRLF / 13354 -> 14258 octets (mesure du planificateur : identique) ;
- page livree sous le nouveau controle : **5 constats** (mesure du planificateur : identique : 3 de surface, 2 d'absolu) ;
- morsures : **2**, **1** et **1** constats portant leur motif nomme (mesure du planificateur : identique) ;
- les quatre modules de la page : `39 passed` (mesure du planificateur : identique).

Aucune regle de deviation (1 a 4) n'a ete declenchee : aucun bogue, aucune fonctionnalite critique manquante, aucun blocage, aucun choix d'architecture. Aucun point d'arret (`checkpoint`) n'etait pose par le plan.

## Verification

Les blocs `<automated>` des deux taches ont ete joues dans l'ordre, chacun avec son resultat **reel** :

| Tache | Commande | Resultat observe |
|-------|----------|------------------|
| 1 | controle de fragments de la rubrique (les deux producteurs, les quatre jetons de condition, `PAGE 1/1`) et de la desambiguisation de la saisie invalide | `page : les deux producteurs sont nommes, leurs deux conditions sont portees, et la rubrique de la saisie invalide est desambiguee` (exit 0) |
| 1 | controle d'octets de la page | `page : 99 lignes, 99 CR, aucun BOM` |
| 1 | `pytest tests/test_docs_depannage.py tests/test_docs_structure.py tests/test_docs_completude.py tests/test_docs_code_anchor.py -q` puis `pytest -q` | `39 passed in 0.36s` puis `249 passed in 5.81s` (avant ce plan : 249) |
| 1 | `git status --porcelain -- dofus_stuff \| wc -l` | `0` |
| 2 | `pytest tests/test_docs_depannage.py -q` | `10 passed in 0.40s` |
| 2 | `pytest tests/test_docs_depannage.py::test_garde_de_cloture_du_harnais tests/test_docs_structure.py tests/test_docs_completude.py tests/test_docs_code_anchor.py -q` | `31 passed in 0.17s` |
| 2 | morsures sur copies sous `mktemp -d` (copie verte avant mutation, mutation par octets, motif nomme exige) | `mutation detectee (absolu_sans_surface), motif « absolu de pagination non borne »` (2 constats) ; `mutation detectee (condition_effacee), motif « surface de pagination non declaree »` (1 constat) ; `mutation detectee (procede_js_efface), motif « formes de la pagination »` (1 constat) ; `morsures 06-05 tache 2 : 3/3 detectees` ; aucune `MUTATION NON DETECTEE`, aucune `COPIE ROUGE AVANT MUTATION` |
| 2 | suite complete, empreinte de `.data/` avant/apres, perimetre | `250 passed in 5.78s` ; `suite complete verte, empreinte .data/ identique : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` ; `git diff --name-only HEAD -- dofus_stuff \| wc -l` = `0` ; `git status --porcelain -- dofus_stuff \| wc -l` = `0` |
| 2 | suite complete sous le greffon de refus reseau (critere 4 de la phase) | `greffon de preuve 06-04 : 6 pieges armes avant la collecte -> ...` puis `250 passed in 5.73s` |

**La paire rouge / vert mesuree (tache 2), sur deux copies distinctes :**

- **rouge sur la page livree par 06-01** — copie sous `mktemp -d` portant la page d'avant correction (96 lignes, 96 CRLF, 13354 octets, verifiee a l'octet) : `1 failed, 9 passed in 0.35s`, message d'echec portant **5** constats, dans cet ordre : `surface de pagination non declaree` ne nomme pas la surface « application » (`dofus_stuff/web/routes.py`) ; ne nomme pas la surface « sauvegardes » (`dofus_stuff/web/static/js/terminal.js`) ; ne porte pas « aucune ligne de pagination » pour la surface « sauvegardes » ; `absolu de pagination non borne` porte « aucun motif a son statut » ; `absolu de pagination non borne` porte « n'ajoute aucun motif » ;
- **vert sur la page corrigee** — le depot, apres la tache 1 : `10 passed in 0.40s`, soit 0 constat.


**Rejeu final, apres le commit de metadonnees :** `.venv/Scripts/python.exe -m pytest -q` -> **`250 passed in 5.71s`** ; empreinte de `.data/dofus.sqlite3` identique avant et apres (`24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`) ; `git status --porcelain -- dofus_stuff` = `0` et `git status --porcelain -- docs tests` = `0` ; `git diff --diff-filter=D --name-only c47a7df..HEAD` vide (aucun fichier supprime).
**Limites nommees de cette verification, recopiees du bloc `<verification>` du plan :** le rendu Markdown hors GitHub, l'execution du JavaScript et le comportement du DOM ne sont pas observes (le controle lit `terminal.js`, il ne l'execute pas) ; la copie de morsure n'embarque pas `.data/`, donc la morsure est mesuree **module par module** (`tests/test_docs_depannage.py`, qui ne depend pas de `.data/`) et la suite entiere y serait rouge pour une raison etrangere a la mutation ; et une reecriture du produit ou du script invaliderait la mesure, le controle lisant ces deux fichiers.

## Issues Encountered

- **Aucun echec de controle.** Les deux taches sont vertes a la premiere execution, les deux mesures de rouge (page livree, trois derivees) sont conformes aux mesures du planificateur, et aucune assertion n'a ete affaiblie. Aucun aller-retour de mise au point n'a ete necessaire sur les livrables.
- **Un seul point d'outillage, hors livrable** : `mktemp -d` rend un chemin POSIX que le Python natif de Windows ne resout pas lorsqu'il est **interpole dans une chaine** (`Path('/tmp/...')` -> `\tmp\...`). Les blocs `<automated>` du plan ne sont pas concernes (ils passent par `cd "$T"` et des chemins relatifs) ; pour ma mesure supplementaire du rouge sur la page livree, le chemin a ete converti par `cygpath -w` avant d'etre interpole. Aucun fichier du depot n'en depend.

## User Setup Required

None : aucun paquet installe, aucune dependance ajoutee (`re`, `pathlib`, `hashlib` et les fixtures existantes suffisent), aucune variable d'environnement, aucun service externe, aucun appel reseau, aucune resynchronisation Dofusdude, aucune action manuelle.

## Threat Flags

Aucun drapeau nouveau : les menaces `mitigate` du plan sont couvertes par des mesures, et aucune surface nouvelle n'est introduite.

- **T-06-05-01 (La page reste fausse d'un autre cote)** : les deux affirmations de la rubrique sont mesurees (`routes.py:144-145` avec sa garde ; `terminal.js:370` et `:400` sans garde), et le controle exige un **nombre d'occurrences**, pas une presence. La morsure `procede_js_efface` rejoue cette mesure sur une copie.
- **T-06-05-02 (La reponse du refus)** : le controle ne refuse qu'une surface non nommee, un jeton de condition absent ou une marque d'absolu declaree ; une reformulation bornee passe (mesure : 0 constat sur la page corrigee).
- **T-06-05-03 (Un absolu formule autrement)** : limite nommee, ecrite ici et dans la docstring de la fonction — huit marques sont couvertes, une generalisation formulee autrement reste hors d'atteinte.
- **T-06-05-04 (La mesure ne prouve pas la page)** : le controle exige que **toutes** les compositions du script soient adossees a `setStatus(`, donc une troisieme composition (corps ou en-tete) rougit avec `formes de la pagination`.
- **T-06-05-05 (La derive destructrice)** : aucune commande n'approche `.data/` en ecriture ; l'empreinte en lecture seule (`24989696`, `1788730056843137500`, `e3793d64...`) est identique avant et apres la suite complete.
- **T-06-05-06 (La mutation qui n'ecrit rien)** : les mutations sont des remplacements d'octets sur des copies sous `mktemp -d`, chacune precedee d'une assertion d'ancre et mesuree **verte avant** sa mutation (`COPIE ROUGE AVANT MUTATION` sinon) ; aucun `sed -i`, aucun `read_text`/`write_text`.
- **T-06-05-07 (Le perimetre qui deborde)** : `git status --porcelain -- dofus_stuff` = `0`, `git status --porcelain -- docs` vide (la seule page touchee est celle de ce plan, commitee), `tests/test_docs_mutation.py` non touche (14 morsures declarees), aucune page epinglee modifiee.

## Self-Check: PASSED

- `docs/depannage.md` existe, porte la rubrique corrigee (99 lignes, 99 CRLF, aucun BOM, 14258 octets) et `dofus_stuff/**` n'a pas bouge (`git status --porcelain -- dofus_stuff` = `0`).
- `tests/test_docs_depannage.py` existe, porte `problemes_pagination` (ligne 908) et `test_pagination_bornee_a_ses_deux_producteurs` (ligne 1324), et `pytest tests/test_docs_depannage.py -q` rend `10 passed`.
- `git log --oneline c47a7df..HEAD` contient les deux commits de tache : `b791063`, `d2a5dab` ; `git rev-list --count c47a7df..HEAD` = `2` (mesure, egale au champ `actuals.commits`).
- `git diff --diff-filter=D --name-only` vide sur l'intervalle : aucun fichier supprime.
- La paire rouge/vert est mesuree : **5** constats sur la page livree par 06-01, **0** sur la page corrigee ; les trois derivees mordent avec leur motif nomme (2, 1, 1).
- Les deux suites finales sont vertes et citees : `250 passed in 5.78s` et `250 passed in 5.73s` (sous le greffon de refus reseau).
- `.data/dofus.sqlite3` : empreinte `(taille, mtime_ns, sha256)` identique avant et apres la suite complete.

## Limites declarees

Recopiees du bloc `<verification>` du plan, aucune n'est presentee comme resolue :

1. **Le rendu Markdown hors GitHub n'est pas observe** (aucun moteur de rendu installe, aucune publication distante).
2. **L'execution du JavaScript et le comportement du DOM ne sont pas observes** : le controle lit `terminal.js` en octets, il ne l'execute pas. La phrase « Leur corps ne porte aucune ligne de pagination » est bornee par les deux seules compositions du fichier, toutes deux adossees a `setStatus(` — c'est une lecture, pas un rendu.
3. **La morsure est mesuree module par module** : la copie sous `mktemp -d` n'embarque pas `.data/`, donc la suite complete y serait rouge pour une raison etrangere a la mutation ; seule `tests/test_docs_depannage.py` (qui ne depend pas de `.data/`) est rejouee.
4. **Une reformulation de la rubrique, du produit ou du script est une nouvelle mesure a faire** : le controle lit deux fichiers producteurs, et une reecriture de l'un d'eux invaliderait la mesure.
5. **Une generalisation de la page formulee autrement que par les jetons et les marques declares reste hors d'atteinte** (`D-85`, backstop du plan) : la liste des marques d'absolu est finie (8) et declaree.
6. **Le controle est invisible pour `tests/test_docs_mutation.py`**, qui garde ses 14 morsures declarees et n'est pas modifie : la preuve de morsure de ce controle vit dans la tache 2, sur des copies.
7. **La garde de cloture du harnais est une demonstration statique et indirecte** : elle dit ce que le module importe et appelle, pas ce qu'un autre chemin ferait.

## Next Phase Readiness

- **Ce plan est le plan de fermeture de la phase 6** : le defaut `T3` de `06-VERIFICATION.md` (critere 1 du ROADMAP) et son observation secondaire sur la ligne 28 sont traites, et le controle qui les tient est livre avec sa preuve de morsure. `AIDE-01` est complete.
- **Ce qui reste ouvert et n'est pas du ressort de ce plan** : la **re-verification de phase** sur le critere 1, qui relira la rubrique corrigee, la paire rouge/vert et les executions citees ; aucune verification humaine n'est revendiquee ici, et aucune validation manuelle n'a eu lieu.
- **Reserve heritee, nommee et non corrigee** : la derive `windows_ledger_table_drift` (registre `.planning/WINDOWS.md`, `id=5`) reste declaree telle quelle, comme les plans precedents l'ont consignee. Aucune ligne de ce plan ne la presente comme resolue, et aucune ligne n'y a ete ajoutee (aucun stub, aucun test saute, aucun `<verify>` non joue).
- **Aucun nouveau milestone** n'est ouvert par ce plan : le besoin initial (une documentation utilisateur en francais, livree et gardee) est couvert par les phases 1 a 6.

---
*Phase: 06-depannage-glossaire-completude-et-preuve-finale*
*Completed: 2026-09-12*
