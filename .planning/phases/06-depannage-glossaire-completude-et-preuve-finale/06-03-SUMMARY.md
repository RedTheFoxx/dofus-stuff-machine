---
phase: 06-depannage-glossaire-completude-et-preuve-finale
plan: 03
subsystem: documentation
tags: [markdown, pytest, completude, liste-epinglee, garde-anti-vidage, couverture-d-index, readme-d100, encadrement-d-une-ligne-destructrice, garde-de-cloture-ast, morsures, copie-verte-avant-mutation, documentation-francaise]

# Dependency graph
requires:
  - phase: 06-01
    provides: "docs/depannage.md et sa ligne d'index (l'index porte alors six pages de contenu), tests/test_docs_depannage.py comme patron de la garde de cloture auto-analysee et des morsures sur copie verte avant mutation, et la regle « un motif de morsure est porte par une constante ASCII du module »"
  - phase: 06-02
    provides: "docs/glossaire.md et sa ligne d'index (le tableau porte alors les sept pages de contenu, 7 lignes mesurees) : la liste epinglee des huit pages de docs/ ne peut etre ecrite qu'apres ces deux pages (depends_on du plan)"
  - phase: 05-base-locale-hors-ligne-et-resynchronisation
    provides: "docs/base-locale.md (la page vers laquelle le README renvoie desormais), l'occurrence de la commande de nettoyage relevee par le plan 05-03 (README.md:80, hors du mandat D-87, transmise a cette phase par D-100) et les fixtures partagees docs_dir / normalize / section / sections"
provides:
  - "tests/test_docs_completude.py : le module de completude (790 lignes, 8 tests) — docstring de contrat, de decision D-100 et de six limites nommees, garde de cloture auto-analysee par `ast` (reecrite pour ce module : aucune base, aucun processus, aucune socket, aucun reseau, aucun appel a `main` ni au solveur, aucune suppression de fichier), et les constantes PAGES_EPINGLEES (les huit pages de `docs/` avec leur seuil de lignes non vides, lus sur le disque), PAGES_RACINE, PAGES_DE_LA_PHASE, MOTS_AVERTISSEMENT, INVOCATION_DESTRUCTIVE, INVOCATIONS_CONSERVEES, RENVOI_BASE_LOCALE, dix motif de morsure ASCII et trois constantes de famille"
  - "Les trois fonctions pures de constats : `problemes_pages_epinglees` (une page epinglee = chemin existant, fichier, decodable, un titre de niveau 1, seuil de lignes non vides atteint ; puis egalite d'ensembles avec `docs/*.md` dans les deux sens, et les deux fichiers de racine verifies existants et non vides), `problemes_readme` (un constat par famille pour chaque occurrence : avertissement manquant, renvoi manquant, jeton de commande disparu) et `problemes_couverture_index` (constante epinglee contre le tableau `## Index` dans les deux sens, au plus une ligne par cible, et le compte des lignes)"
  - "README.md : la commande de nettoyage de la base locale **reste** documentee et perd sa forme d'invitation — deux lignes ajoutees dans le meme bloc que l'occurrence disent qu'elle detruit la base locale et que l'operation est irreversible, et renvoient vers `docs/base-locale.md` (D-100 : encadrer, jamais supprimer ; 2 insertions, 0 suppression, CRLF preserve)"
  - "La cloture de completude : les huit pages de `docs/` sont epinglees et confrontees au disque dans les deux sens, aucune ne peut etre supprimee ni videe en silence, chacune est atteignable depuis l'index, l'index ne promet aucune page hors de la liste, et le tableau porte autant de lignes que de pages de contenu epinglees (7 pour 7, mesure)"
affects: [06-04, verification-phase-6]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (70 000) est consigne tel quel : il mesure le pessimisme de l'estimate,
# pas un travail non fait (les trois taches sont livrees, 5/5 morsures du plan detectees).
actuals:
  tokens: 10792     # chars/4 sur le diff realise (43 171 caracteres de patch, 2 fichiers, 792 insertions)
  tasks: 3
  commits: 3        # MESURE : git rev-list --count aa4b82a..215c384 = 3 ; le compte final est 4 avec le commit de metadonnees de ce plan (le dernier de la branche)
  plan_head_before: aa4b82a7851e9e4a2b80ad68871ec2576157daf7

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; stdlib seulement (ast, re, pathlib)
  patterns:
    - "Morsure sur copie verte avant mutation (D-84) : chaque derive est jouee dans un repertoire temporaire (`mktemp -d`), la copie est mesuree VERTE sur `tests/test_docs_completude.py` avant mutation, puis la suite complete est rejouee apres — le script du plan refuse explicitement une copie rouge (« COPIE ROUGE AVANT MUTATION »), aucun de ces messages n'est apparu"
    - "Mutation ecrite par `python -c` qui lit et reecrit avec `newline=\"\"` : les CR des fichiers CRLF du depot (`README.md`, `docs/glossaire.md`, `docs/sommaire.md`) sont preserves ; le `sed -i` de ce poste les retire (lecon de 06-01, deja payee une fois)"
    - "Un motif de morsure est porte par une constante du module, jamais ecrit en clair dans une ligne d'assertion : pytest reproduit la ligne source de l'`assert`, une valeur en clair y serait trouvee meme sans constat produit (regle du plan 03-03, tenue ici sur les 8 tests et sur les 17 constantes de motif)"
    - "Une famille de constat est une constante distincte (`FAMILLE_AVERTISSEMENT`, `FAMILLE_RENVOI`, `FAMILLE_DISPARITION`) : un motif unique (`MOTIF_README`) permet a la batterie de chercher **une** chaine dans la sortie, et les trois familles restent diagnostiquables separement — un constat par famille, jamais un constat generique"
    - "Un controle d'encadrement raisonne par **bloc de lignes contigues** : une commande et son avertissement ne sont dans le meme bloc que s'ils ne sont pas separes par une ligne vide, donc une phrase posee deux paragraphes plus bas ne compte pas comme encadrante — la contiguite est la mesure, pas la proximite dans le fichier"
    - "L'egalite d'ensembles va **dans les deux sens** avec un motif distinct par sens (page livree non indexee / entree d'index sans page epinglee), et le controle ajoute ce qu'un raisonnement en ensembles ne peut pas voir : **au plus une** ligne par cible, et le **compte** des lignes"
    - "Un controle d'index qui ne veut pas doubler les gardes livrees ecrit sa non-duplication et declare la **transitivite** : la couverture epinglee est une consequence de l'egalite index <-> disque et de l'egalite pages epinglees <-> disque, et elle est gardee comme lecture de la **constante** (une seule source de verite, D-14) plutot que comme seconde derivation du disque"
    - "Une clause « aucune ligne existante n'est retiree » est **mecanisee**, jamais laissee au jugement : les jetons des commandes de base sont lus sur le disque a l'ecriture et figes en constante (`INVOCATIONS_CONSERVEES`, le jeton destructif compris), la disparition de l'un d'eux est un constat, et la comparaison `git show HEAD:README.md` <-> copie de travail tranche l'absence de retrait (mesure : 123 lignes avant, 125 apres, 0 disparue)"

key-files:
  created:
    - tests/test_docs_completude.py
  modified:
    - README.md

key-decisions:
  - "`D-100` tranchee par l'**encadrement**, jamais par la suppression : la ligne de nettoyage de la base locale reste dans le `README.md` (elle est un contenu livre : retirer l'information perdrait le lecteur au lieu de le proteger), et ce qui manquait — l'avertissement et le renvoi vers le geste non destructif — est ajoute **dans le meme bloc** que l'occurrence. La justification complete est ecrite dans la docstring du module, avant tout code : une suppression ne prouverait rien du besoin (aucune assertion ne distinguerait « information absente » de « information jamais livree »), alors que l'encadrement produit deux constats automatiques et nommes."
  - "La decision `D-100` est **verifiee dans les deux sens** : le controle exige que l'occurrence soit encadree (avertissement et renvoi), et il exige aussi que l'information soit **encore la** (chaque jeton de `INVOCATIONS_CONSERVEES`, le jeton destructif compris, doit apparaitre au moins une fois). Supprimer la ligne est donc un constat, au meme titre que retirer son avertissement : le controle ne peut pas etre satisfait par la disparition du contenu livre."
  - "Les seuils de `PAGES_EPINGLEES` sont des **garde-fous anti-vidage**, pas des exigences de qualite : ils sont lus sur le disque au moment de l'ecriture (mesure : `docs/base-locale.md` 82 lignes non vides, `cli.md` 137, `depannage.md` 71, `glossaire.md` 44, `installation.md` 91, `parcours-simplifie.md` 174, `sommaire.md` 20, `wizard-avance.md` 162) puis declares a environ trois quarts de la mesure (60, 100, 50, 30, 65, 130, 15, 120). Une page courte mais honnete reste donc possible ; une page tronquee ou videe rougit."
  - "Le controle de `README.md` traite **chaque** occurrence de la commande, pas seulement la premiere : la selection se fait par bloc de lignes contigues, donc une seconde occurrence ajoutee ailleurs dans la page devra porter son propre avertissement et son propre renvoi — la forme ne peut pas etre « achetee » par un encadrement pose une seule fois."
  - "Le renvoi vers `docs/base-locale.md` est ecrit en **prose dans le bloc de code** (le chemin lisible tel quel), et non en lien Markdown : dans un bloc cloture, `[texte](cible)` ne serait pas rendu comme un lien, et le controle exige le chemin du fichier, jamais une mise en forme. `docs/base-locale.md` reste donc aussi la cible du renvoi verifie, sans dependre d'un rendu."
  - "La garde de cloture est **reecrite, pas recopiee** : ce module n'ouvre aucune base et n'instancie aucune application, il ne reprend donc pas le resserrement `data_dir` de la phase 5 (controle d'un risque inexistant) et refuse le risque reel d'un module documentaire — les racines de base/processus/socket/reseau, l'appel a `main`, les appels `optimize_stuff` / `_run_optimize_and_redirect` et les suppressions de fichier. Elle s'auto-analyse par `ast.parse` du fichier lu (`RACINE_DEPOT / tests / <nom>`), jamais par une recherche de chaines : 0 occurrence de `skip` et de `xfail` sur les 790 lignes, donc aucun saut ne peut masquer un controle."
  - "Chaque page indecodable en UTF-8 stricte est un **constat** (`MOTIF_PAGE_ILLISIBLE`), jamais une exception : `read_text` est enferme, en tache 1 comme dans le controle du `README.md` (le bloc de verification du plan exige d'ailleurs qu'un `README.md` illisible soit un constat et jamais un vert). C'est un ajout de robustesse, pas un affaiblissement : sans lui, un fichier corrompu aurait fait echouer la collecte ou l'appel avant tout diagnostic."
  - "`PAGES_DE_LA_PHASE` nomme les deux pages livrees par cette phase comme **sujet** du controle, et leur appartenance est verifiee contre `PAGES_EPINGLEES` : aucune enumeration des pages n'est recopiee, donc aucune seconde source de verite (D-14, D-95)."
  - "Le module ne rejoue pas les gardes de la phase 1 (D-12) : l'egalite index <-> disque, le titre de niveau 1 et l'unicite des libelles restent ceux de `tests/test_docs_structure.py`, et la docstring du module le dit en toutes lettres, avec la transitivite de la couverture epinglee et les deux axes reellement neufs (au plus une ligne par cible, et le compte)."

patterns-established:
  - "Pattern 24 : une liste epinglee se declare avec un **seuil par element** et se confronte au disque **dans les deux sens** — le seuil n'est pas une exigence de qualite mais le refus du vidage, et la fonction de constats recoit la **racine en argument** plutot que de la lire d'une constante, ce qui rend la morsure possible sur une copie `tmp_path` sans toucher au depot"
  - "Pattern 25 : un encadrement se mesure par **bloc de lignes contigues**, avec un motif par famille de manque (avertissement, renvoi) et une verification symetrique de **conservation** des jetons de la page — une ligne ne peut donc ni rester non encadree ni disparaitre en silence, et la clause « aucune ligne existante n'est retiree » devient une constante puis une comparaison `git show HEAD:<fichier>` <-> copie de travail"
  - "Pattern 26 : une fonction de constats pure recoit le **texte** (jamais le disque) quand son objet est une prose, et la morsure est alors prouvee par des textes **synthetiques** prives successivement de chaque element attendu : la preuve de morsure est immediate et hors du depot, et le cas « aucun jeton » interdit un faux temoin (un controle qui ne chercherait que des blocs serait vert sur une page vidée)"
  - "Pattern 27 : un controle de couverture d'index se limite aux axes qu'aucune garde livree ne porte (au plus une ligne par cible, et le compte) et **declare** que le reste est deja tenu ailleurs, avec la transitivite qui le justifie — la duplication ecrite est ce qui permet a deux modules de rester verts sur le meme objet sans se neutraliser"

requirements-completed: [GARD-03]

coverage:
  - id: D1
    description: "La liste epinglee des huit pages de docs/ est declaree (avec son seuil de lignes non vides) et confrontee au disque **dans les deux sens** : une page deplacee, renommee, ajoutee, supprimee ou videe est un constat nomme, jamais un silence ; les deux fichiers de documentation de la racine sont verifies existants, fichiers et non vides"
    requirement: "GARD-03"
    verification:
      - kind: unit
        ref: "`tests/test_docs_completude.py::test_pages_epinglees_completes` ; `.venv/Scripts/python.exe -m pytest tests/test_docs_completude.py -q` -> `3 passed in 0.07s` (tache 1), `8 passed in 0.08s` (tache 3)"
        status: pass
      - kind: integration
        ref: "morsure `page_supprimee` (`rm docs/cli.md` sur la copie) -> motif « page epinglee absente ou non fichier » ; morsure `page_videe` (`# Glossaire` seul dans `docs/glossaire.md` de la copie) -> motif « page videe ou tronquee » — 2/2 detectees, copie verte avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D2
    description: "Une page livree ne peut plus etre **videe** en silence : chaque page epinglee porte un titre de niveau 1 et au moins son seuil declare de lignes non vides, et une page illisible est un constat plutot qu'une exception"
    requirement: "GARD-03"
    verification:
      - kind: unit
        ref: "`problemes_pages_epinglees` branchee dans `test_pages_epinglees_completes` ; la fonction rend un constat par page pour l'absence, le type, le decodage, le titre de niveau 1 et le seuil de lignes non vides"
        status: pass
      - kind: integration
        ref: "morsure `page_videe` : la page tronquee a 1 ligne non vide pour un seuil de 30, constat « page videe ou tronquee : 1 ligne(s) non vide(s) ... attendu au moins 30 »"
        status: pass
    human_judgment: false
  - id: D3
    description: "La morsure du controle de la liste epinglee est prouvee **hors du depot**, sur une copie minimale construite sous `tmp_path` (un dossier `docs` avec une page tronquee et une page absente, plus les deux fichiers de racine) : le controle est declare capable de mordre sans qu'aucun fichier du depot soit touche"
    requirement: "GARD-03"
    verification:
      - kind: unit
        ref: "`tests/test_docs_completude.py::test_aucune_page_ne_peut_etre_videe` (copie `tmp_path`, deux familles de constats exigees ensemble)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Le README.md n'invite plus a detruire les donnees locales : le bloc qui porte la commande de nettoyage porte aussi un mot d'avertissement declare et le renvoi `docs/base-locale.md`, la ligne de commande reste presente, et **chaque** occurrence est traitee"
    requirement: "GARD-03"
    verification:
      - kind: unit
        ref: "`tests/test_docs_completude.py::test_readme_n_invite_pas_a_detruire` ; mesure avant l'encadrement : `1 failed` avec les deux familles (avertissement manquant + renvoi manquant) sur le bloc des lignes 77..81 ; apres : `2 passed, 3 deselected in 0.01s`"
        status: pass
      - kind: integration
        ref: "morsure `renvoi_retire` (lignes contenant `base-locale.md` retirees du README de la copie) et morsure `avertissement_retire` (`détruit` -> `vide`, `irréversible` -> `simple`) -> 2/2 detectees avec le motif « invitation a detruire les donnees », copie verte avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D5
    description: "Aucune ligne existante du README.md n'est retiree : l'encadrement se fait par des lignes **ajoutees**, la conservation de chaque jeton de commande de base est exigee par le controle (`INVOCATIONS_CONSERVEES`, le jeton destructif compris), et la comparaison `git show HEAD:README.md` <-> copie de travail ne montre aucune ligne disparue"
    requirement: "GARD-03"
    verification:
      - kind: integration
        ref: "`git show HEAD:README.md` <-> copie de travail, pris avant le commit du plan : `code retour git show : 0 lignes avant : 123 lignes apres : 125 lignes disparues : 0` ; `git diff --numstat -- README.md` -> `2 0` (deux insertions, zero suppression) ; `git ls-files --eol README.md` reste `i/lf w/crlf`"
        status: pass
      - kind: unit
        ref: "`tests/test_docs_completude.py::test_le_controle_du_readme_mord_sur_un_texte_synthetique` : la famille « jeton disparu » est exigee sur un texte prive de **tous** les jetons conserves (le jeton destructif compris), donc une page qui n'aurait plus d'occurrence n'est pas declaree verte"
        status: pass
    human_judgment: false
  - id: D6
    description: "Chaque page livree est **atteignable** : chaque page de contenu epinglee est la cible d'exactement une ligne du tableau `## Index`, aucune cible du tableau n'est hors de la liste epinglee, et le nombre de lignes d'index egale le nombre de pages de contenu epinglees"
    requirement: "GARD-03"
    verification:
      - kind: unit
        ref: "`tests/test_docs_completude.py::test_couverture_de_l_index` et `test_le_nombre_d_entrees_d_index_est_le_nombre_de_pages` ; mesure de livraison : le tableau `## Index` porte **7** lignes (installation, parcours-simplifie, cli, wizard-avance, base-locale, depannage, glossaire) pour 7 pages de contenu epinglees"
        status: pass
      - kind: integration
        ref: "morsure `index_tronque` (les lignes contenant `glossaire.md` retirees de `docs/sommaire.md` de la copie) -> motif « page livree non indexee », constat nommant la page ; 1/1 detectee, copie verte avant mutation"
        status: pass
    human_judgment: false
  - id: D7
    description: "Les deux pages livrees par cette phase sont **epinglees et indexees**, et le controle le derive des constantes (appartenance a `PAGES_EPINGLEES` + cible du tableau d'index) plutot que d'une enumeration recopiee"
    requirement: "GARD-03"
    verification:
      - kind: unit
        ref: "`tests/test_docs_completude.py::test_les_deux_pages_de_la_phase_sont_epinglees_et_indexees` ; mesure : les deux cibles `depannage.md` et `glossaire.md` sont dans le tableau et leurs chemins sont dans `PAGES_EPINGLEES`"
        status: pass
    human_judgment: false
  - id: D8
    description: "Le module de completude ne duplique aucune garde livree et le dit, la garde de cloture du harnais est auto-analysee par `ast` (aucune base, aucun processus, aucune socket, aucun reseau, aucun appel a `main` ni au solveur, aucune suppression), aucun controle ne saute, et la suite entiere est verte avec la base du depot intacte"
    requirement: "GARD-03"
    verification:
      - kind: unit
        ref: "`tests/test_docs_completude.py::test_garde_de_cloture_du_harnais` ; `.venv/Scripts/python.exe -m pytest -q` -> `238 passed in 4.50s` (tache 1 ; 235 avant ce plan), `240 passed in 4.45s` (tache 2), `243 passed in 4.50s` (tache 3) ; 0 `skip` et 0 `xfail` sur les 790 lignes du module"
        status: pass
      - kind: integration
        ref: "empreinte `.data/dofus.sqlite3` : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique avant le plan, apres chaque tache, apres chaque batterie de morsures et apres la suite complete ; `dofus_stuff/**` non modifie, `pyproject.toml` inchange"
        status: pass
    human_judgment: false

# Metrics
duration: 5min
completed: 2026-09-12
status: complete
---

# Phase 6 : Depannage, glossaire, completude et preuve finale — Plan 06-03 Summary

**La documentation livree est prouvee complete et le README n'envoie plus personne detruire sa base : les huit pages de `docs/` sont epinglees dans une constante et confrontees au disque dans les deux sens (seuil de lignes non vides par page contre le vidage), chaque page de contenu est la cible d'exactement une ligne du tableau `## Index` et le tableau porte autant de lignes que de pages (7 pour 7), et la commande de nettoyage du `README.md` reste documentee mais gagne, dans son propre bloc, l'avertissement qui dit qu'elle detruit la base locale et le renvoi vers `docs/base-locale.md`. Les cinq derives du plan ont toutes ete detectees sur une copie verte avant mutation, et la suite entiere est verte : 243 passed (235 avant ce plan) avec la base du depot intacte.**

## Performance

- **Duration:** ~5 min (mesure : du premier horodatage de la passe, `2026-09-12T00:15:35Z`, au releve precedent cette synthese, `2026-09-12T00:20:13Z`, soit **4 min 38 s** ; l'intervalle entre le premier et le dernier commit de tache est de **3 min 06 s**, de `02:17:00` a `02:20:06` en heure locale).
- **Started:** 2026-09-12T00:15:35Z (horodatage pris avant la tache 1, apres la lecture du plan, de la recherche et des mesures du disque)
- **Completed:** 2026-09-12T00:20:13Z
- **Tasks:** 3
- **Files:** 2 — un module cree (`tests/test_docs_completude.py`, 790 lignes, 8 tests) et un fichier documentaire modifie par **ajout** (`README.md`, 123 -> 125 lignes, `2 0` en `--numstat`).
- **Commits:** 3, **aucun fichier supprime** (`git diff --diff-filter=D --name-only` vide sur l'intervalle et apres chaque commit) ; diff cumule : `2 files changed, 792 insertions(+)` (43 171 caracteres de patch).
- **Estimate vs actuals :** estimate `70 000` tokens, mesure `10 792` (chars/4 du diff realise) — l'estimate etait pessimiste d'un facteur ~6,5, comme les phases 5, 06-01 et 06-02 l'ont consigne ; aucune tache n'a ete sautee pour autant (les trois taches sont livrees, 5/5 morsures du plan detectees).

## Accomplishments

- **La liste epinglee est la source unique du contrat, et le disque la contredit ou la confirme (D-14, D-95).** `PAGES_EPINGLEES` nomme les huit pages de `docs/` — les sept pages de contenu et le sommaire — avec, pour chacune, un seuil de lignes non vides **lu sur le disque au moment de l'ecriture** puis declare (mesure : `base-locale.md` 82, `cli.md` 137, `depannage.md` 71, `glossaire.md` 44, `installation.md` 91, `parcours-simplifie.md` 174, `sommaire.md` 20, `wizard-avance.md` 162 lignes non vides ; seuils declares : 60, 100, 50, 30, 65, 130, 15, 120). `PAGES_RACINE` nomme les deux fichiers de la racine, verifies existants, fichiers et non vides. La comparaison de la liste au disque se fait **dans les deux sens** : une page du disque non epinglee et une page epinglee absente du disque sont deux constats de motifs distincts, donc une page ajoutee, deplacee ou renommee ne peut pas passer pour une page deja listee.
- **Une page ne peut plus etre videe en silence.** Chaque page epinglee doit porter un titre de niveau 1 et au moins son seuil de lignes non vides ; une page indécodable en UTF-8 stricte est un **constat** (`MOTIF_PAGE_ILLISIBLE`) plutot qu'une exception, `read_text` etant enferme. Le seuil est ecrit comme un **garde-fou anti-vidage**, jamais comme une mesure de qualite (limite 3 de la docstring) : il refuse la troncature et le vidage, il ne juge pas la concision.
- **La morsure du controle est prouvee sans toucher au depot.** `test_aucune_page_ne_peut_etre_videe` construit sous `tmp_path` une copie minimale — un dossier `docs` avec une seule page tronquee (`# Glossaire` et rien d'autre), les sept autres absentes, plus les deux fichiers de racine — et exige **les deux familles de constats ensemble** (`page epinglee absente ou non fichier` et `page videe ou tronquee`). C'est la forme la moins invasive de la preuve de morsure : la fonction recoit la racine en argument, jamais une constante du module, donc l'arbre livre ne peut pas etre modifie par la mesure.
- **Le `README.md` n'invite plus a detruire les donnees, et la ligne reste (D-100).** La decision est ecrite **avant tout code** dans la docstring du module, avec sa justification : la ligne de nettoyage est un contenu livre, `GARD-03` demande que la documentation n'invite pas a detruire les donnees **tout en documentant les chemins de reconstruction**, une suppression ne prouverait rien (aucune assertion ne distinguerait « information absente » de « information jamais livree »), et l'encadrement produit deux constats automatiques et nommes. La modification est un ajout de **deux lignes** dans le bloc des commandes de base, juste avant l'occurrence (ligne 80 du fichier d'origine) : elle dit que la commande detruit la base locale et que l'operation est irreversible, et renvoie vers `docs/base-locale.md`. Mesure : `2 0` en `--numstat`, CRLF preserve (`git ls-files --eol README.md` reste `i/lf w/crlf`), 90 -> 92 lignes non vides.
- **« Aucune ligne existante n'est retiree » est mecanise, jamais laisse au jugement.** Trois garanties independantes : (i) `problemes_readme` exige la presence, dans le texte, de **chaque** jeton de `INVOCATIONS_CONSERVEES` **et** du jeton destructif — la conservation des commandes de base est un constat, et le constat nomme le jeton disparu ; (ii) la comparaison `git show HEAD:README.md` <-> copie de travail, prise **avant** le commit du plan, rend `lignes avant : 123 lignes apres : 125 lignes disparues : 0` (la reference `git log -1 --numstat -- README.md` est explicitement rejetee par le plan, mesure : le dernier commit ayant touche le fichier porte `0 2`, qui conclurait a tort a un retrait) ; (iii) la morsure synthetique exige la famille « jeton disparu » sur un texte prive de tous les jetons, donc le controle ne peut pas etre satisfait par la disparition du contenu.
- **Le controle du `README.md` traite chaque occurrence, par bloc de lignes contigues.** La fonction est **pure** (elle recoit le texte, jamais le disque), un constat par famille avec un motif de base commun : `FAMILLE_AVERTISSEMENT` (aucun mot de `MOTS_AVERTISSEMENT` — `détruit`, `irréversible` — dans le bloc de l'occurrence), `FAMILLE_RENVOI` (le bloc ne renvoie pas vers `docs/base-locale.md`), `FAMILLE_DISPARITION` (un jeton de commande de base a disparu de la page). La contiguite est la mesure : une phrase posee deux paragraphes plus bas ne compte pas comme encadrante, et une seconde occurrence ajoutee ailleurs devra porter son propre encadrement.
- **La morsure du controle du `README.md` est prouvee sur trois textes synthetiques.** Trois textes construits dans le test portent le meme inventaire de commandes, prives successivement de l'avertissement, du renvoi, puis de **tous** les jetons conserves : les trois familles sont exigees ensemble, la preuve est immediate et hors du depot, et la mesure a un objet declaré (`INVOCATION_DESTRUCTIVE` non vide, sans quoi les textes construits ne mesureraient rien).
- **Chaque page livree est atteignable, et l'index ne promet rien de plus (D-95, D-96).** `problemes_couverture_index` confronte la **constante epinglee** au tableau `## Index` dans les deux sens (une page epinglee sans ligne, une cible hors de la liste), exige **au plus une** ligne par cible — l'axe qu'aucune garde livree ne voit, `problemes_index` raisonnant en ensembles — et exige que le nombre de lignes du tableau egale le nombre de pages de contenu epinglees, le constat nommant les deux nombres. Mesure de livraison : le tableau porte **7** lignes (`installation.md`, `parcours-simplifie.md`, `cli.md`, `wizard-avance.md`, `base-locale.md`, `depannage.md`, `glossaire.md`) pour **7** pages de contenu epinglees, les deux pages livrees par cette phase (celles de 06-01 et 06-02) comprises.
- **La non-duplication est ecrite, et la transitivite aussi (D-12).** L'egalite index <-> disque (dans les deux sens), le titre de niveau 1 et l'unicite des libelles restent ceux de `tests/test_docs_structure.py` : le module ne les rejoue pas, et sa docstring declare que la couverture epinglee est une **consequence** de cette egalite et de l'egalite pages epinglees <-> disque, gardee comme lecture de la **constante** (une seule source de verite) plutot que comme seconde derivation du disque. Ce module ajoute donc exactement ce qui manquait : l'egalite de la constante avec le disque et avec l'index, le refus du vidage, l'unicite de la ligne d'index, et le compte.
- **La garde de cloture est reecrite pour le risque reel du module.** Ce module ne lit que des fichiers texte : il ne reprend donc pas le resserrement `data_dir` de la phase 5 (controle d'un risque inexistant) et refuse les racines de base, de processus, de socket et de reseau, l'appel a `main`, les appels `optimize_stuff` / `_run_optimize_and_redirect` et les suppressions de fichier. Auto-analyse par `ast.parse` du source du module (`RACINE_DEPOT / "tests" / <nom du fichier>`), jamais par une recherche de chaines : 0 occurrence de `skip` et de `xfail` sur les 790 lignes.
- **La base du depot n'est jamais approchee.** Aucune commande de base n'est lancee, `.data/dofus.sqlite3` est lu en octets pour son empreinte seulement, et l'empreinte (taille, `mtime_ns`, SHA-256) est identique avant le plan, apres chaque tache, apres chaque batterie et apres la suite complete.
- **Cinq derives du plan, toutes detectees** (voir § Verification). Aucune n'a eu besoin d'etre rendue plus permissive ; une correction a porte sur le **test** qui portait la morsure (voir § Deviations).

## Task Commits

Each task was committed atomically:

1. **Tache 1 : tranche verticale « la liste epinglee existe, elle est confrontee au disque, et une page ne peut plus disparaitre ni se vider » (`type="tracer"`)** — `e0a9c9a` (feat) : `tests/test_docs_completude.py` (398 insertions) — `1 file changed, 398 insertions(+)`.
2. **Tache 2 : le README n'invite plus a detruire les donnees — encadrer, jamais supprimer (D-100)** — `a7ffbdd` (feat) : `README.md` (2 insertions, 0 suppression), `tests/test_docs_completude.py` (+174) — `2 files changed, 176 insertions(+)`.
3. **Tache 3 : la cloture de completude — chaque page livree est indexee, et l'index ne promet aucune page** — `215c384` (test) : `tests/test_docs_completude.py` (+220, -2) — `1 file changed, 220 insertions(+), 2 deletions(-)`. Les deux lignes retirees sont une phrase de la docstring du module remplacee par la version qui declare la non-duplication et la transitivite ; **aucun fichier n'est supprime** (`--diff-filter=D` vide).

**Plan metadata:** le commit de metadonnees de ce plan — `docs(06-03): complete la completude, la garde du lecteur et la liste epinglee` (le dernier de la branche, `git log -1`) : il porte ce SUMMARY, la position de `STATE.md`, la progression de `ROADMAP.md` et `GARD-03` dans `REQUIREMENTS.md`.

`git rev-list --count aa4b82a..215c384` = **3** : trois commits de tache, aucun commit intermediaire de correction.

## Files Created/Modified

- `tests/test_docs_completude.py` — **cree** (398 insertions en tache 1, 790 lignes a la fin de la tache 3 ; >= 200 lignes exigees). Docstring de contrat, de decision `D-100` et de six limites nommees ; garde de cloture auto-analysee par `ast` ; constantes `RACINE_DEPOT`, `DOSSIER_DOCS`, `SOMMAIRE`, `TITRE_INDEX`, `PAGES_EPINGLEES` (8 entrees), `PAGES_RACINE`, `PAGES_DE_LA_PHASE`, `MOTS_AVERTISSEMENT`, `INVOCATION_DESTRUCTIVE`, `INVOCATIONS_CONSERVEES`, `RENVOI_BASE_LOCALE`, `RACINES_INTERDITES`, `APPELS_SUPPRESSION`, `APPEL_PRODUIT`, `APPELS_CALCUL_PRODUIT`, **dix** constantes `MOTIF_*` et **trois** constantes `FAMILLE_*` ; lecteurs locaux `MOTIF_TITRE`, `MOTIF_LIGNE_INDEX` ; helpers `_imports_du_module`, `_appels_du_module`, `_non_vides`, `_blocs_contigus`, `_pages_contenu_epinglees`, `_corps_index` ; fonctions pures `problemes_pages_epinglees`, `problemes_readme`, `problemes_couverture_index` ; **8 tests**. Les fixtures partagees de `tests/conftest.py` (`docs_dir`, `normalize`, `section`) sont **reutilisees telles quelles**, jamais recopiees (D-12) : le module ne definit ni normalisation, ni lecteur de section, ni fixture locale.
- `README.md` — **modifie par ajout en tache 2** : deux lignes inserees dans le bloc `bash` des commandes de base, avant l'occurrence de la commande de nettoyage (ligne 80 du fichier d'origine), `# ATTENTION : la commande ci-dessous détruit la base locale (l'opération est irréversible).` et `# Le mode hors-ligne et les gestes non destructifs sont documentés dans docs/base-locale.md`. 123 -> 125 lignes, 90 -> 92 lignes non vides, `2 0` en `--numstat`, CRLF preserve, aucun autre bloc touche (ni la ligne de resynchronisation, ni la ligne d'etat, ni la mention des sous-commandes acceptees en alias).
- `docs/**` — **aucun octet modifie** (aucune page touchee, le sommaire etant seulement **lu** par le controle de couverture).
- `dofus_stuff/**` — **aucun octet modifie** (D-103) ; `pyproject.toml` inchange (aucune dependance ajoutee) ; `.data/**` jamais approche.

## Decisions Made

- **`D-100` : encadrer, jamais supprimer** — la commande de nettoyage reste documentee, encadree dans son propre bloc par l'avertissement et le renvoi ; la justification complete (contenu livre, suppression non verifiable, encadrement verifiable par deux constats, interdiction de supprimer de la documentation livree) est ecrite dans la docstring du module avant tout code.
- **Les seuils de `PAGES_EPINGLEES` sont des garde-fous anti-vidage** (~trois quarts de la mesure de chaque page), declares une fois par page, sans pretention d'exhaustivite.
- **Le renvoi est ecrit en prose dans le bloc de code** (le chemin lisible tel quel) et non en lien Markdown : un lien dans un bloc cloture ne serait pas rendu, et le controle exige le chemin du fichier, jamais une mise en forme.
- **Le controle du `README.md` est une fonction pure qui traite chaque occurrence** par bloc de lignes contigues, avec un constat par famille ; il ne lit jamais `.data/`, ne teste pas la commande et ne l'execute pas.
- **La clause « aucune ligne retiree » est mecanisee** par les jetons conserves (constantes lues sur le disque) et par la comparaison `git show HEAD:README.md` <-> copie de travail — mesure : 123 lignes avant, 125 apres, 0 disparue ; la reference `git log -1 --numstat` est rejetee par le plan (mesure : `0 2` sur le dernier commit touchant le fichier).
- **Le controle de couverture se limite aux deux axes neufs** (au plus une ligne par cible, et le compte) et **declare** que le reste est tenu par la phase 1, avec la transitivite qui le justifie.
- **`PAGES_DE_LA_PHASE` est le sujet du controle, pas une seconde liste** : l'appartenance des deux pages de la phase est verifiee contre `PAGES_EPINGLEES`, donc aucune enumeration des pages n'est recopiee (D-14).
- **`PAGES_EPINGLEES`, `MOTS_AVERTISSEMENT`, `INVOCATION_DESTRUCTIVE` et `INVOCATIONS_CONSERVEES` sont lues sur le disque a l'ecriture** (D-19) : aucune page, aucun seuil et aucun avertissement n'est invente de memoire.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] La morsure « les deux pages de la phase » lisait le tableau d'index avec un motif ancre sans `re.MULTILINE`**
- **Found during:** Tache 3 (la cloture de completude), premiere execution du bloc `<automated>` de la tache.
- **Issue:** le test `test_les_deux_pages_de_la_phase_sont_epinglees_et_indexees` extrait les cibles du tableau avec `MOTIF_LIGNE_INDEX.finditer(corps)` ; le motif declare par le plan est ancre (`^\|\s*\[...\]\s*\|`) **sans** le drapeau `re.MULTILINE`, il ne peut donc matcher qu'au debut de la chaine. Resultat mesure : `1 failed, 7 passed`, deux constats « page livree non indexee » produits **sur un arbre correct** — le controle criait au loup parce que la lecture du test etait vide, pas parce que l'index etait en derive.
- **Fix:** la lecture se fait desormais **ligne a ligne** (`MOTIF_LIGNE_INDEX.match(ligne)` sur chaque ligne du corps de section), comme dans `problemes_couverture_index` — le motif du plan est conserve tel quel, aucune garde n'est affaiblie, et le corps de section vient toujours de la fixture partagee `section`.
- **Files modified:** `tests/test_docs_completude.py`
- **Verification:** `.venv/Scripts/python.exe -m pytest tests/test_docs_completude.py -q` -> `8 passed in 0.08s` ; la morsure `index_tronque` est detectee avec le motif « page livree non indexee », et la mesure de livraison compte 7 lignes de tableau pour 7 pages epinglees.
- **Committed in:** `215c384` (Tache 3).

### Ajouts de robustesse (Rule 2, signales comme tels)

**2. [Rule 2 - Missing Critical] Une page indecodable en UTF-8 stricte est un constat, jamais une exception**
- **Found during:** Tache 1 (la liste epinglee confrontee au disque).
- **Issue:** `Path.read_text(encoding="utf-8")` leve `UnicodeDecodeError` sur un fichier corrompu : le controle mourrait avant tout diagnostic, alors que le bloc de verification de la tache 2 exige explicitement qu'un `README.md` illisible soit un constat et jamais un vert.
- **Fix:** `read_text` est enferme dans les deux lectures (`problemes_pages_epinglees` pour les pages de `docs/` et pour les fichiers de racine, `test_readme_n_invite_pas_a_detruire` pour le `README.md`) et l'echec de decodage produit un constat nomme (`MOTIF_PAGE_ILLISIBLE`, ligne de fichier citee) au lieu d'une exception.
- **Files modified:** `tests/test_docs_completude.py`
- **Verification:** la suite entiere reste verte (243 passed) et aucun constat d'illisibilite n'est produit sur l'arbre livre ; la branche est exercee par lecture du code, sans mutation de fichier du depot.
- **Committed in:** `e0a9c9a` (Tache 1) et `a7ffbdd` (Tache 2).

### Autres ecarts (sans effet sur un controle)

**3. [Placement] `MOTIF_README` est declare en tache 2 plutot qu'en tache 1**
- Le plan listait `MOTIF_README` parmi les constantes de la tache 1 alors que la tache 1 ne l'utilise pas et que les criteres d'acceptation de la tache 1 ne le nomment pas. Il est declare avec les autres constantes du controle du `README.md`, la ou il sert. Aucun controle n'est modifie.
- **Committed in:** `a7ffbdd` (Tache 2).

**4. [Ajout] Trois constantes de famille et `PAGES_DE_LA_PHASE` s'ajoutent aux constantes declarees par le plan**
- `FAMILLE_AVERTISSEMENT`, `FAMILLE_RENVOI` et `FAMILLE_DISPARITION` rendent les trois familles de constats du `README.md` diagnosticables separement tout en portant le **meme** motif de base (`MOTIF_README`), sur lequel la batterie du plan fait son `grep` : c'est ce qui permet a la morsure de chercher une seule chaine sans rendre les constats generiques. `PAGES_DE_LA_PHASE` est le sujet du controle des deux pages de la phase, jamais une seconde liste de l'inventaire. Aucun seuil, aucun mot d'avertissement et aucun jeton n'est invente : les valeurs sont lues sur le disque a l'ecriture.

---

**Total deviations:** 1 auto-corrige (Rule 1 — bug de lecture dans un test neuf, corrige avant le commit de sa tache), 1 ajout de robustesse (Rule 2), 2 ecarts de placement/ajout sans effet sur un controle.
**Impact on plan:** aucun affaiblissement de controle, aucun elargissement de perimetre : les 5 morsures du plan sont detectees avec leurs motifs declares, la suite entiere est verte, et `dofus_stuff/**`, `docs/**`, `.data/**` et `pyproject.toml` sont inchanges.

## Preuves de verification (mesures reelles)

**Les cinq morsures du plan, jouees sur une copie verte avant mutation** (`mktemp -d`, copie de `docs tests dofus_stuff fetcher.py pyproject.toml GUIDE_WIZARD.md README.md`, copie mesuree VERTE sur le module avant chaque mutation, puis suite complete rejouee apres) :

| Tache | Morsure | Mutation reellement appliquee | Sorti du `grep -F` | Resultat |
|---|---|---|---|---|
| 1 | `page_supprimee` | `rm docs/cli.md` dans la copie | `page epinglee absente ou non fichier` | `mutation detectee (page_supprimee)` |
| 1 | `page_videe` | `docs/glossaire.md` ecrit en `# Glossaire\r\n` (1 ligne non vide pour un seuil de 30) | `page videe ou tronquee` | `mutation detectee (page_videe)` |
| 2 | `renvoi_retire` | les lignes contenant `base-locale.md` retirees du `README.md` de la copie | `invitation a detruire les donnees` | `mutation detectee (renvoi_retire)` |
| 2 | `avertissement_retire` | `détruit` -> `vide` et `irréversible` -> `simple` dans le `README.md` de la copie | `invitation a detruire les donnees` | `mutation detectee (avertissement_retire)` |
| 3 | `index_tronque` | les lignes contenant `glossaire.md` retirees de `docs/sommaire.md` de la copie | `page livree non indexee` | `mutation detectee (index_tronque)` |

Les trois batteries rendent `2/2`, `2/2` et `1/1` detectees, avec l'exit 0 et **aucun** message « COPIE ROUGE AVANT MUTATION », « MUTATION NON DETECTEE » ni « MORSURES DU PLAN 06-03 (TACHE n) EN ECHEC ».

**Controles automatises (resultats reels, interpreteur epingle `./.venv/Scripts/python.exe`) :**

| Commande | Resultat mesure |
|---|---|
| `-m pytest tests/test_docs_completude.py -q` | `3 passed in 0.07s` (tache 1), `8 passed in 0.08s` (tache 3) |
| `-m pytest tests/test_docs_completude.py -q -k "readme"` | `1 failed, 1 passed, 3 deselected in 0.06s` **avant** l'encadrement (familles avertissement + renvoi, motif « invitation a detruire les donnees », bloc des lignes 77..81), puis `2 passed, 3 deselected in 0.01s` **apres** |
| `-m pytest -q` | `238 passed in 4.50s` (tache 1 ; 235 avant ce plan), `240 passed in 4.45s` (tache 2), `243 passed in 4.50s` (tache 3) |
| comparaison `git show HEAD:README.md` <-> copie de travail | `code retour git show : 0 lignes avant : 123 lignes apres : 125 lignes disparues : 0` |
| lisibilite du `README.md` | `README.md relu : lignes non vides = 92` en UTF-8 |
| empreinte `.data/dofus.sqlite3` | `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — 4 mesures, toutes identiques (avant le plan, apres la tache 1, apres la tache 2, apres la tache 3) |

**Porte de retour de la tranche verticale (tache 1, `type="tracer"`)** : le mode automatique etant inactif (`workflow.auto_advance` et `_auto_chain_active` a `false`) et le mode de verification humaine etant `end-of-phase` avec un bloc `<verify>` purement automatise, les trois blocs de la tache ont ete **rejoues de bout en bout apres le commit** : `3 passed`, `2/2 morsures detectees` (copie verte avant chaque mutation), `238 passed in 4.62s`. Aucun point d'arret humain n'a donc ete pose pour cette tranche, et aucun n'aurait pu l'etre : rien dans ce plan ne depend d'un geste humain, d'un secret ou d'un reseau.

**Non automatisable, nomme comme tel (backstop/judgment, aucune validation humaine revendiquee ni simulee) :** l'effet reellement ressenti par un lecteur du `README.md` (comprend-il que la commande detruit sa base ?), la qualite redactionnelle des avertissements, une **reformulation sans perte** d'une ligne du `README.md` (les jetons conserves et la comparaison `git show` attrapent la disparition, pas la reecriture), et le fait qu'aucune page ne soit rangee dans un sous-dossier de `docs/` (mesure : il n'en existe aucun). Ces quatre points sont declares dans la docstring du module et ici ; la condition de `must_haves.truths` ecrite en `backstop` (l'effet ressenti) n'est donc **pas** presentee comme verifiee.

## Known Stubs

Aucun : aucun `TODO`, `FIXME`, `placeholder`, valeur vide ou composant non alimente n'a ete introduit par ce plan, et aucun controle du module ne saute (`0` occurrence de `skip` et de `xfail` sur les 790 lignes). Le seul fichier documentaire modifie l'est par **ajout** de deux lignes de commentaire, sans texte de remplacement laisse en attente.

## Threat Flags

Aucun : les trois menaces `mitigate` du plan (`T-06-03-01` perte silencieuse de contenu livre, `T-06-03-02` documentation qui invite a detruire, `T-06-03-05` execution du produit ou correction automatique d'un fichier livre) sont couvertes par le module et ses morsures, et aucune surface nouvelle n'est introduite — le module lit des fichiers texte du depot, n'ouvre aucune base, ne joint aucun reseau et n'ecrit rien. Aucun chemin de poste ni valeur volatile n'apparait dans un constat (les chemins sont relatifs a la racine du depot, `Path.as_posix`).

## Self-Check: PASSED

- `tests/test_docs_completude.py` existe (790 lignes, 8 tests, `pytest tests/test_docs_completude.py -q` -> `8 passed`).
- `git log --oneline aa4b82a..HEAD` contient les trois commits de tache : `e0a9c9a`, `a7ffbdd`, `215c384`.
- `git diff --diff-filter=D --name-only aa4b82a..215c384` est vide : aucun fichier supprime.
- `.data/dofus.sqlite3` : empreinte identique avant et apres (4 mesures).
- Aucun fichier de `dofus_stuff/**`, de `docs/**`, ni `pyproject.toml` modifie.

## Next Phase Readiness

- **Le plan 06-04 peut etre joue** : `tests/test_docs_completude.py` est en place et vert, et il fournit les deux controles que la preuve de mutation du harnais consommera (la fonction pure de la liste epinglee, exercable sur une copie `tmp_path`, et le controle du `README.md`), avec `GARD-03` marque complete.
- **La reserve de morsure du `README.md` est levee, pas deplacee** : l'occurrence consignee par le plan 05-03 (`README.md:80`, hors du mandat D-87) est desormais couverte par un controle qui mord, et la decision `D-100` est tranchee (encadrer, jamais supprimer) — le plan 06-04 n'a plus a la trancher.
- **Rappel de perimetre pour 06-04** : la preuve de mutation du harnais, l'empreinte de `.data/` et l'audit `git status` restent hors de ce plan ; `GARD-04` est toujours ouvert. Limite connue et non corrigee ici (D-101) : la derive preexistante du registre `.planning/WINDOWS.md` (`windows_ledger_table_drift`) reste declaree, hors perimetre.

---
*Phase: 06-depannage-glossaire-completude-et-preuve-finale*
*Completed: 2026-09-12*


