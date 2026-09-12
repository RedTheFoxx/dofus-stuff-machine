---
phase: 06-depannage-glossaire-completude-et-preuve-finale
plan: 02
subsystem: documentation
tags: [markdown, pytest, glossaire, vocabulaire-du-produit, employeur-confrontation, renvoi-de-definition, d17-une-seule-source, permutation-des-libelles, parcours-conseille-en-texte-simple, morsures, copie-verte-avant-mutation, documentation-francaise]

# Dependency graph
requires:
  - phase: 06-01
    provides: "docs/depannage.md et sa ligne d'index (l'index porte alors six pages de contenu) ; tests/test_docs_depannage.py comme patron du module, de la garde de cloture auto-analysee et des morsures sur copie verte ; les motifs de constat ASCII et la regle « jamais un motif en clair dans une ligne d'assertion »"
  - phase: 05-base-locale-hors-ligne-et-resynchronisation
    provides: "les pages livrees que le glossaire renvoie au lieu de les redefinir (base-locale.md, parcours-simplifie.md, wizard-avance.md, cli.md, installation.md, sommaire.md) et les fixtures partagees docs_dir / normalize / section / sections"
provides:
  - "docs/glossaire.md : la page unique du vocabulaire (56 lignes, 56 fins de ligne pour 56 retours chariot, sans BOM) — 27 termes tries apres normalisation, une seule section de tableau `## Les termes` a quatre colonnes, le bloc `## Source de vérité` en derniere section et `[Retour au sommaire](sommaire.md)` en derniere ligne non vide ; 22 termes renvoient vers la page qui les definit deja, 5 sont definis par le glossaire lui-meme (index, parcours conseillé, sommaire, source de vérité, stuff)"
  - "docs/sommaire.md : exactement une ligne de plus, `| [Glossaire](glossaire.md) | Le vocabulaire du produit et de la documentation, adossé à son employeur |`, ajoutee en fin de table `## Index` (25 lignes mesurees, >= 25 exigees) ; l'index porte desormais les sept pages de contenu et le parcours conseille reste du texte simple"
  - "tests/test_docs_glossaire.py : le module d'ancrage du vocabulaire (769 lignes, 7 tests) — docstring de contrat et de limites, garde de cloture auto-analysee par `ast` (reecrite pour ce module), constantes TERMES_GLOSSAIRE (27 entrees) et TERMES_INTERDITS, les vingt-deux motifs MOTIF_* et les lecteurs locaux, fonctions pures problemes_glossaire, problemes_page_glossaire et problemes_parcours"
  - "la couverture du critere 2 du ROADMAP et de AIDE-02 : le vocabulaire du produit **et** de la documentation, chaque entree adossee a un employeur reellement employeur, triee, unique, et renvoyee vers la page qui la definit deja quand elle existe (D-17, D-19, D-94)"
  - "le **parcours conseille final** du sommaire rendu verifiable (D-95) : la section que trois gardes vertes lisaient deja comme de l'index n'etait lue par **aucune** garde avant ce plan (mesure `grep \"Parcours\" tests/*.py` -> 0 occurrence)"
affects: [06-03, 06-04, verification-phase-6]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (80 000) est consigne tel quel : il mesure le pessimisme de l'estimate,
# pas un travail non fait (les trois taches sont livrees, 7/7 morsures du plan detectees).
actuals:
  tokens: 11937     # chars/4 sur le diff realise (47 746 caracteres de patch, 3 fichiers, 826 insertions)
  tasks: 3
  commits: 3        # MESURE : git rev-list --count 030ba01..67f7bb4 = 3 ; le compte final est 4 avec le commit de metadonnees de ce plan (le dernier de la branche)
  plan_head_before: 030ba014164cf4c19bc3a18044521e7fa08f1d2a

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; stdlib seulement (ast, re, pathlib)
  patterns:
    - "Morsure sur copie verte avant mutation (D-84) : chaque derive est jouee dans un repertoire temporaire (`mktemp -d`), la copie est mesuree VERTE sur `tests/test_docs_glossaire.py` avant mutation, puis la suite complete est rejouee apres — le script du plan refuse explicitement une copie rouge (« COPIE ROUGE AVANT MUTATION »), aucun de ces messages n'est apparu"
    - "Mutation ecrite par `python -c` qui lit et reecrit avec `newline=\"\"` : les CR des fichiers CRLF du depot (`docs/sommaire.md`, `docs/glossaire.md`) sont preserves ; le `sed -i` de ce poste les retire (lecon de 06-01, deja payee une fois)"
    - "Motif de morsure porte par une constante ASCII du module, jamais ecrit en clair dans une ligne d'assertion : pytest reproduit la ligne source de l'assert, une valeur en clair y serait trouvee meme sans constat produit (regle du plan 03-03, tenue ici sur les 7 tests)"
    - "Le contrat est une **constante** et la page en est le reflet : `TERMES_GLOSSAIRE` porte (terme, employeur, page qui definit deja) et l'egalite d'ensembles va **dans les deux sens** — un terme de la page non declare porte `terme cite non declare`, un terme declare absent de la page porte `terme declare absent de la page`. La source unique du contrat est le module (D-14), jamais la page"
    - "Un employeur est **confronte au fichier** : le chemin declare existe depuis la racine du depot et le terme y est present apres normalisation `D-11` ; la ligne de la page doit citer ce meme chemin, faute de quoi le constat nomme les deux. Un renvoi de definition est confronte a sa **cible**, resolue depuis `docs/` (D-17)"
    - "Un controle de prose est declare en **limite** et jamais en vert silencieux (D-85) : la qualite redactionnelle, le rendu Markdown hors GitHub et l'ordre de lecture du parcours sont ecrits dans la docstring du module et dans ce SUMMARY, sans qu'aucune validation humaine ne soit revendiquee"

key-files:
  created:
    - docs/glossaire.md
    - tests/test_docs_glossaire.py
  modified:
    - docs/sommaire.md

key-decisions:
  - "Le glossaire **renvoie** au lieu de redefinir (D-17) : sept pages livrees definissent deja le reste du vocabulaire, et chaque ligne renvoyee porte une phrase courte de renvoi — jamais la definition complete de la page cible. Seuls cinq termes sont definis par le glossaire, parce qu'aucune page livree ne les definit (mesure `06-RESEARCH.md` § B et lecture des six pages)."
  - "L'employeur de chaque terme est **le fichier ou la page qui l'emploie reellement**, verifie par lecture `fichier:ligne` avant d'ecrire la ligne (D-19), jamais repris de memoire. Repartition mesuree des 27 entrees : `dofus_stuff/cli.py` 9 (base locale, catégorie, cible, ID Ankama, jet, poids, prysmaradite, stuff, synchronisation), `dofus_stuff/model/slots.py` 3 (bouclier, familier, trophée), `docs/sommaire.md` 3 (index, parcours conseillé, sommaire), `dofus_stuff/model/solver_spec.py` 2 (exo, palier), `dofus_stuff/optimize/score.py` 2 (heuristique, score), `docs/base-locale.md` 2 (mode hors-ligne, source de vérité), `dofus_stuff/web/optimize_wizard.py` 2 (slot, wizard), `docs/parcours-simplifie.md` 1 (ligne de statut), `dofus_stuff/catalog.py` 1 (panoplie), `dofus_stuff/web/static/js/terminal.js` 1 (sauvegarde locale), `dofus_stuff/optimize/cpsat.py` 1 (solveur)."
  - "Decision de mesure : `trophée` ne renvoie **pas** a `docs/parcours-simplifie.md` — mesure de ce plan, cette page ne contient pas le mot (elle nomme le familier, la prysmaradite et le bouclier, jamais le trophee dont elle decrit pourtant les six Dofus). La page qui le nomme est `docs/wizard-avance.md` (`DOFUS/TROPHÉES`, `F9 TROPHEE`), et c'est elle qui est declaree comme page de definition ; l'employeur, lui, reste `dofus_stuff/model/slots.py`, qui l'emploie en clair."
  - "Decision de mesure : l'employeur de `sauvegarde locale` est `dofus_stuff/web/static/js/terminal.js` — la recherche pointait `parcours-simplifie.md` et `terminal.js`, et la forme exacte au singulier n'existe que dans le second (mesure : `terminal.js:324`, `AUCUNE SAUVEGARDE LOCALE.` ; `parcours-simplifie.md:174` ecrit `CHARGEMENT DES SAUVEGARDES LOCALES…`, ou « sauvegarde locale » n'est pas une sous-chaine). La page de definition reste `docs/parcours-simplifie.md`, qui decrit la liste et sa limite."
  - "Le glossaire **n'ouvre rien** : aucune base, aucun client, aucune sonde, aucun ecran (c'est une page de renvois et de lecture de fichiers). La garde de cloture, **reecrite** pour ce module, ne porte donc pas le resserrement `data_dir` de la phase 5 — une garde qui controlerait un risque inexistant serait du bruit — et refuse en revanche l'execution de `main`, les appels `optimize_stuff` / `_run_optimize_and_redirect`, les imports de base/processus/socket/reseau et les suppressions de fichier."
  - "`TERMES_INTERDITS` porte les trois termes de harnais mesures comme absents des pages livrees et de `dofus_stuff/**` (`page épinglée`, `renvoi`, `ancrage`) et son test exige la liste **non vide** avant de l'appliquer : un refus sans liste serait un vert trompeur. Le controle porte sur la **premiere cellule** du tableau, jamais sur le texte entier de la page — les phrases de renvoi emploient legitimement les mots de la documentation."
  - "`problemes_parcours` est une fonction **pure** : elle prend le texte du sommaire, jamais le disque (D-13, D-14), et elle exige une **permutation** des libelles d'index, pas un ordre donne. L'ordre de lecture reste celui deja livre (le wizard avant la reference CLI), et cette liberte est ecrite dans la docstring : la divergence d'ordre entre le parcours et l'index est une discretion assumee, pas une derive (D-85)."

patterns-established:
  - "Pattern 20 : une page de renvois se controle **de la page vers le depot** — chaque entree est confrontee a un employeur (chemin existant, terme present apres normalisation) et chaque renvoi a sa cible resolue ; c'est l'inverse du patron de provenance de 06-01 (produit vers page) et les deux se completent"
  - "Pattern 21 : un contrat de vocabulaire se declare en **constante** et se verifie par egalite d'ensembles **dans les deux sens**, avec un motif distinct par sens de l'erreur (non declare / absent de la page) — un controle a sens unique laisserait passer une entree citee sans contrat"
  - "Pattern 22 : une ligne de tableau est la forme extractible d'un terme (premiere cellule entre accents graves), et la tracabilite s'ecrit en deux colonnes de la meme ligne : l'employeur (ou le mot vit) et la page qui definit deja (a lire pour le detail) — la definition du glossaire n'est jamais une seconde source"
  - "Pattern 23 : un texte que trois gardes vertes lisent deja comme autre chose (ici le parcours conseille, lu comme de l'index par `problemes_index`, `problemes_h1` et `test_sommaire_index_labels_are_unique`) se protege par un controle **de forme** (aucun lien Markdown) avant qu'un controle de fond ne le compare : la prohibition devient executable au lieu d'etre declarative"

requirements-completed: [AIDE-02]

coverage:
  - id: D1
    description: "Le glossaire est un contrat extractible : `## Les termes` porte un seul tableau dont la premiere cellule de chaque ligne est un terme entre accents graves, les libelles lus et `TERMES_GLOSSAIRE` sont en egalite d'ensembles **dans les deux sens** (27 termes de chaque cote), la suite des libelles normalises est strictement croissante et aucun libelle ne se repete — la qualite de la prose n'est pas verifiee (limite declaree, D-85)"
    requirement: "AIDE-02"
    verification:
      - kind: unit
        ref: "`.venv/Scripts/python.exe -m pytest tests/test_docs_glossaire.py -q` -> `7 passed in 0.08s` ; `python -m pytest tests/test_docs_glossaire.py tests/test_docs_structure.py -q` -> `19 passed in 0.20s`"
        status: pass
      - kind: integration
        ref: "morsure `terme_retire` (la ligne de `stuff` retiree de la copie) -> « terme declare absent de la page » ; morsure `ordre_inverse` (les deux premieres lignes du tableau inversees) -> « ordre des termes »"
        status: pass
    human_judgment: false
  - id: D2
    description: "Chaque terme est employe par le fichier qu'il declare : les 27 employeurs sont confrontees au fichier cite, qui existe depuis la racine du depot et contient le terme apres normalisation D-11 — le constat nomme le terme, l'employeur declare et l'employeur cite quand l'un des trois manque (D-19)"
    requirement: "AIDE-02"
    verification:
      - kind: unit
        ref: "`problemes_glossaire` branchee dans `test_entrees_du_glossaire` et dans `test_renvois_de_definition` ; lecture `fichier:ligne` de chaque employeur faite avant ecriture de la ligne (mesure : les 27 chemins existent et portent le terme)"
        status: pass
      - kind: integration
        ref: "morsure `employeur_faux` (`` `dofus_stuff/cli.py` `` -> `` `dofus_stuff/database.py` `` dans la premiere ligne du tableau) -> « terme non employe par le fichier cite » : le constat nomme la ligne, l'employeur declare et l'employeur cite ; la suite entiere est rouge avec ce motif"
        status: pass
    human_judgment: false
  - id: D3
    description: "Le glossaire ne redefinit pas ce qu'une page livree definit deja (D-17) : les 22 termes concernes portent un lien vers **cette** page, dont la cible resout depuis `docs/` ; les 5 termes que le glossaire est seul a definir portent un tiret, et un lien sur l'un de ces cinq est un constat"
    requirement: "AIDE-02"
    verification:
      - kind: unit
        ref: "`test_renvois_de_definition` : le contrat est d'abord exerce lui-meme (au moins un terme declare une page de definition, et chaque page declaree existe sous `docs/`), puis `problemes_glossaire` accumule les constats de renvoi ; mesure : 22 entrees portent une page de definition, 5 portent `-` ; mesure avant la page complete : `1 failed, 4 passed in 0.08s` avec « TERMES_GLOSSAIRE ne declare aucune page de definition » (le contrat vide etait refuse)"
        status: pass
      - kind: integration
        ref: "morsure `renvoi_retire` (le premier renvoi d'une ligne portant `base-locale.md` remplace par un `-`, sur la copie) -> « renvoi de definition manquant »"
        status: pass
    human_judgment: false
  - id: D4
    description: "Le vocabulaire de harnais est refuse (D-19) : les trois libelles de `TERMES_INTERDITS` ne peuvent pas etre des entrees, la liste est exigee non vide, et le controle porte sur la premiere cellule du tableau"
    requirement: "AIDE-02"
    verification:
      - kind: unit
        ref: "`test_le_vocabulaire_du_harnais_est_absent` vert sur la page livree (aucune entree de `TERMES_INTERDITS`, liste non vide)"
        status: pass
      - kind: integration
        ref: "morsure `terme_interdit_ajoute` (une ligne `page épinglée` inseree juste apres le titre `## Les termes` de la copie) -> « terme hors du vocabulaire du produit »"
        status: pass
    human_judgment: false
  - id: D5
    description: "Le parcours conseille final du sommaire est verifiable (D-95) : la liste numerotee de `## Parcours conseillé` est une **permutation** des libelles d'index (egalite d'ensembles dans les deux sens apres normalisation), chaque libelle numerote apparie un libelle d'index exact, aucun libelle numerote ne porte de lien Markdown, la liste n'est pas plus courte que l'index, et les deux pages livrees par cette phase y sont nommees — libelles derives de l'index, jamais recopies"
    requirement: "AIDE-02"
    verification:
      - kind: unit
        ref: "`.venv/Scripts/python.exe -m pytest tests/test_docs_glossaire.py -q -k \"parcours\"` -> `2 passed, 5 deselected in 0.01s` ; `python -m pytest -q` -> `235 passed in 4.59s`"
        status: pass
      - kind: integration
        ref: "morsure `parcours_libelle_faux` (`7. Glossaire` -> `7. Glossaire des termes` dans la copie) -> « parcours conseille » ; morsure `parcours_en_liens` (`7. Glossaire` -> `7. [Glossaire](glossaire.md)`) -> « parcours conseille en liens »"
        status: pass
      - kind: integration
        ref: "mesure de discrimination : la fonction pure appliquee au `docs/sommaire.md` d'**avant** la phase (`git show 110951f:docs/sommaire.md`, 23 lignes) rend deux constats — « le libelle « Dépannage » du parcours conseille ne reprend aucun libelle d'index » et le meme pour « Glossaire » ; appliquee au sommaire livre (25 lignes), elle ne rend aucun constat"
        status: pass
    human_judgment: false
  - id: D6
    description: "La page respecte le gabarit et ne fige aucune valeur de poste : un seul titre de niveau 1, le bloc `## Source de vérité` en derniere section, `[Retour au sommaire](sommaire.md)` en derniere ligne non vide, octets CRLF sans BOM, aucun nombre de quatre chiffres ou plus, aucun chemin de poste, chaque chemin cite du bloc de provenance existant depuis la racine du depot ; et la garde de cloture du harnais est auto-analysee par `ast` (aucun import de base, de processus, de socket ou de reseau, aucun appel a `main`, a `optimize_stuff` ou a `_run_optimize_and_redirect`, aucun appel de suppression), sans aucun `skip` ni `xfail` dans le module"
    requirement: "AIDE-02"
    verification:
      - kind: unit
        ref: "`test_page_glossaire_close_et_sans_valeur_volatile` et `test_garde_de_cloture_du_harnais` verts ; mesure du fichier : `docs/glossaire.md` 56 lignes, 56 fins de ligne pour 56 retours chariot, BOM absent ; comptage : 0 occurrence de `skip` et 0 de `xfail` sur les 769 lignes du module"
        status: pass
      - kind: unit
        ref: "`python -m pytest tests/test_docs_glossaire.py tests/test_docs_structure.py -q` -> `19 passed` : les gardes existantes du gabarit (H1 unique et egal au libelle d'index, index <-> disque, ligne de retour, encodage) restent vertes avec la page neuve et sa ligne d'index"
        status: pass
    human_judgment: false
  - id: D7
    description: "La suite entiere est verte avec l'interpreteur epingle et son compteur releve tel qu'observe, et `.data/dofus.sqlite3` garde taille, mtime_ns et SHA-256 — y compris autour des trois batteries de morsures, qui ne touchent que des copies sous `mktemp -d`"
    requirement: "AIDE-02"
    verification:
      - kind: integration
        ref: "`.venv/Scripts/python.exe -m pytest -q` -> `231 passed in 4.38s` (apres la tache 1, 228 avant ce plan), `233 passed in 4.35s` (apres la tache 2), `235 passed in 4.59s` (apres la tache 3)"
        status: pass
      - kind: integration
        ref: "empreinte `.data/dofus.sqlite3` : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique avant le plan, apres chaque tache, apres chaque batterie et apres la suite complete"
        status: pass
    human_judgment: false

# Metrics
duration: 5min
completed: 2026-09-12
status: complete
---

# Phase 6 : Depannage, glossaire, completude et preuve finale — Plan 06-02 Summary

**Le glossaire existe et il renvoie au lieu de redefinir : 27 termes tries, chacun adosse a un employeur reellement employeur (27 chemins confrontes au fichier, terme cherche apres normalisation) et renvoye vers la page qui le definit deja quand elle existe (22 renvois, 5 definitions propres), plus le parcours conseille final du sommaire rendu verifiable par une permutation des libelles d'index qui refuse tout lien Markdown — la section que trois gardes vertes lisaient deja comme de l'index et qu'aucune garde ne lisait. Les sept derives du plan ont toutes ete detectees sur une copie verte avant mutation, avec le motif exact que la batterie cherche, et la suite entiere est verte : 235 passed (228 avant ce plan) avec la base du depot intacte.**

## Performance

- **Duration:** ~5 min (mesure : du fichier de preparation de la tache 1, `2026-09-12 02:02:37 +02:00`, au dernier releve avant cette synthese, `02:07:24 +02:00`, soit **4 min 47 s** ; l'intervalle entre le premier et le dernier commit de tache est de **3 min 33 s**, de `02:03:24` a `02:06:57`).
- **Started:** 2026-09-12T02:02:37+02:00 (horodatage du fichier de preparation, ecrit apres la lecture du plan, de la recherche et des pages)
- **Completed:** 2026-09-12T02:07:24+02:00
- **Tasks:** 3
- **Files:** 3 — une page creee (`docs/glossaire.md`, 56 lignes), une page modifiee d'une ligne (`docs/sommaire.md`, 25 lignes) et un module cree (`tests/test_docs_glossaire.py`, 769 lignes).
- **Commits:** 3, **zero fichier supprime** (`git diff --diff-filter=D --name-only 030ba01..67f7bb4` : vide) ; diff cumule : `3 files changed, 826 insertions(+)` (47 746 caracteres de patch).
- **Estimate vs actuals :** estimate `80 000` tokens, mesure `11 937` (chars/4 du diff realise) — l'estimate etait pessimiste d'un facteur ~6,7 comme les phases 5 et 06-01 l'ont consigne ; aucune tache n'a ete sautee pour autant (les trois taches sont livrees, 7/7 morsures du plan detectees).

## Accomplishments

- **Le glossaire est un contrat extractible, pas une page libre (D-94).** `docs/glossaire.md` porte un unique `## Les termes`, un tableau a quatre colonnes (`Terme`, `Définition`, `Employé par`, `Déjà défini dans`) dont la premiere cellule est le terme entre accents graves, le bloc `## Source de vérité` en derniere section et `[Retour au sommaire](sommaire.md)` en derniere ligne non vide — 56 lignes, 56 fins de ligne pour 56 retours chariot, sans BOM. Une mutation qui retire une ligne, inverse deux lignes, cite un mauvais employeur ou retire un renvoi fait rougir le module, chacune avec son motif.
- **L'egalite d'ensembles va dans les deux sens, avec un motif par sens (D-14).** `TERMES_GLOSSAIRE` porte 27 entrees `(terme, employeur, page qui definit deja)` et le controle exige que les libelles lus dans la page et les termes declares soient egaux : un libelle non declare porte `terme cite non declare`, un terme declare absent de la page porte `terme declare absent de la page`. Une seule assertion par test, constats accumules (D-13), chaque constat nommant la page, ce qui est faux, la valeur attendue et le fichier concerne.
- **Chaque terme est employe par le fichier qu'il declare (D-19).** Les 27 employeurs ont ete lus `fichier:ligne` **avant** d'ecrire la ligne, puis confrontes au fichier : chemin existant depuis la racine du depot et terme present apres normalisation `D-11`. Repartition mesuree des 27 entrees : `dofus_stuff/cli.py` 9, `dofus_stuff/model/slots.py` 3, `docs/sommaire.md` 3, `dofus_stuff/model/solver_spec.py` 2, `dofus_stuff/optimize/score.py` 2, `docs/base-locale.md` 2, `dofus_stuff/web/optimize_wizard.py` 2, `docs/parcours-simplifie.md` 1, `dofus_stuff/catalog.py` 1, `dofus_stuff/web/static/js/terminal.js` 1, `dofus_stuff/optimize/cpsat.py` 1. La ligne de la page doit citer ce meme chemin : la morsure `employeur_faux` produit le constat nomme.
- **Le glossaire renvoie au lieu de redefinir (D-17).** 22 termes portent un lien vers la page qui les definit deja (`base-locale.md`, `wizard-avance.md`, `parcours-simplifie.md`, `cli.md`) dont la cible resout depuis `docs/`, avec une phrase de renvoi courte — jamais la definition complete de la page cible ; les 5 termes qu'aucune page livree ne definit (`index`, `parcours conseillé`, `sommaire`, `source de vérité`, `stuff`) portent un `-`, et un lien sur l'un de ces cinq est un constat. Repartition mesuree des 22 renvois : `docs/parcours-simplifie.md` 9, `docs/wizard-avance.md` 7, `docs/base-locale.md` 5, `docs/cli.md` 1. `test_renvois_de_definition` exerce d'abord le contrat lui-meme : un contrat de renvoi vide est refuse (mesure avant la page complete : `1 failed, 4 passed`, « TERMES_GLOSSAIRE ne declare aucune page de definition »).
- **Le vocabulaire de harnais est refuse, et la liste n'est pas vide (D-19).** `TERMES_INTERDITS` porte les trois termes mesures comme absents des pages livrees et de `dofus_stuff/**` (`page épinglée`, `renvoi`, `ancrage`) ; `test_le_vocabulaire_du_harnais_est_absent` exige la constante non vide — un refus sans liste est un vert trompeur — puis refuse tout libelle de la liste en **premiere cellule** du tableau, jamais dans le texte entier : les phrases de renvoi emploient legitimement les mots de la documentation. La morsure `terme_interdit_ajoute` produit le motif nomme.
- **Le parcours conseille final devient verifiable (D-95).** La mesure de la recherche est confirmee : `grep "Parcours" tests/*.py` rend 0 occurrence avant ce plan — la section qui annoncait deja les deux pages de la phase n'etait lue par aucune garde. `problemes_parcours` (fonction **pure**, elle prend le texte, pas le disque) exige une **permutation** des libelles d'index apres normalisation, un appariement exact par libelle, la presence des deux pages de la phase — libelles derives de l'index, jamais recopies — et **aucun lien Markdown** dans la liste : c'est la mesure de la recherche qui rend cette prohibition executable (`problemes_index`, `problemes_h1` et `test_sommaire_index_labels_are_unique` lisent tout lien de `sommaire.md` comme une entree d'index, donc convertir le parcours en liens re-emettrait les libelles de l'index et ferait rougir trois gardes vertes).
- **Le controle du parcours est discrimine sur l'etat qui l'a motive.** Applique au `docs/sommaire.md` d'**avant** la phase (`git show 110951f`, 23 lignes), il rend deux constats en nommant « Dépannage » et « Glossaire » ; applique au sommaire livre (25 lignes), il n'en rend aucun. C'est la preuve que le controle est nouveau et qu'il distingue l'etat d'avant de l'etat d'apres.
- **La garde de cloture du harnais est reecrite, pas recopiee.** Ce module n'ouvre aucune base et n'instancie aucune application : la garde ne reprend donc pas le resserrement `data_dir` de la phase 5 (controle d'un risque inexistant) et refuse ce qui est le risque reel d'un module documentaire — les imports de `sqlite3`, `subprocess`, `socket`, `multiprocessing`, `ctypes`, `webbrowser`, `urllib`, `requests`, `http`, `ftplib`, `smtplib`, l'appel a `main`, les appels `optimize_stuff` / `_run_optimize_and_redirect` et les suppressions de fichier. Elle s'auto-analyse par `ast.parse(Path(__file__).read_text())`, jamais par une recherche de chaines : 0 occurrence de `skip` et de `xfail` sur les 769 lignes, donc aucun saut ne peut masquer un controle.
- **La base du depot n'est jamais approchee.** Aucune commande de base n'est lancee, `.data/dofus.sqlite3` est lu en octets pour son empreinte seulement, et l'empreinte (taille, mtime_ns, SHA-256) est identique avant le plan, apres chaque tache, apres chaque batterie et apres la suite complete.
- **Sept derives du plan, toutes detectees** (voir § Verification). Aucune n'a eu besoin d'etre corrigee pour mordre, aucune n'a ete rendue plus permissive.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : tranche verticale — la page, sa ligne d'index et son harnais (`type="tracer"`)** — `014b2c9` (feat) : `docs/glossaire.md` (28 insertions), `docs/sommaire.md` (1 insertion), `tests/test_docs_glossaire.py` (505 insertions) — `3 files changed, 534 insertions(+)`.
2. **Tache 2 : l'inventaire complet des termes, ses renvois et le refus du vocabulaire de harnais** — `d8c36dd` (test) : `docs/glossaire.md` porte alors les 27 termes (56 lignes mesurees), `tests/test_docs_glossaire.py` recoit `TERMES_GLOSSAIRE` complete, `test_renvois_de_definition` et `test_le_vocabulaire_du_harnais_est_absent` — `2 files changed, 129 insertions(+), 2 deletions(-)`.
3. **Tache 3 : le parcours conseille final devient verifiable, en texte simple** — `67f7bb4` (test) : `problemes_parcours`, `PAGES_DE_LA_PHASE`, `test_parcours_conseille_final`, `test_les_deux_pages_de_la_phase_sont_dans_le_parcours` — `1 file changed, 166 insertions(+), 1 deletion(-)`.

**Plan metadata:** le commit de metadonnees de ce plan — `docs(06-02): complete le glossaire du vocabulaire et le parcours conseille final` (le dernier de la branche, `git log -1`) : il porte ce SUMMARY, la position de `STATE.md`, la progression de `ROADMAP.md` et `AIDE-02` dans `REQUIREMENTS.md`.

`git rev-list --count 030ba01..67f7bb4` = **3** : trois commits de tache, aucun commit intermediaire de correction, **aucun fichier supprime** (`--diff-filter=D` vide sur tout l'intervalle).

## Files Created/Modified

- `docs/glossaire.md` — **cree** (28 insertions en tache 1, 56 lignes a la fin de la tache 2 ; 56 fins de ligne pour 56 retours chariot, BOM absent ; >= 55 lignes exigees). Un titre H1 (`# Glossaire`, egal au libelle d'index), une introduction sur la regle du renvoi, un unique `## Les termes` portant un tableau de 27 lignes a quatre colonnes, trois paragraphes de lecture apres le tableau (ce que les deux sortes de lignes signifient, ce que dit la colonne « Employé par », ce que la page ne juge pas), `## Source de vérité` (derniere section) et `[Retour au sommaire](sommaire.md)` (derniere ligne non vide).
- `docs/sommaire.md` — **modifie d'une ligne, en tache 1** : `| [Glossaire](glossaire.md) | Le vocabulaire du produit et de la documentation, adossé à son employeur |`, ajoutee en fin de table `## Index` (25 lignes mesurees, >= 25 exigees). La liste « Parcours conseillé » n'est **pas** convertie en liens : elle reste du texte simple, desormais gardee.
- `tests/test_docs_glossaire.py` — **cree** (505 insertions en tache 1, 769 lignes a la fin de la tache 3 ; 769 fins de ligne pour 769 retours chariot, BOM absent ; >= 210 lignes exigees). Docstring de contrat et de limites ; garde de cloture auto-analysee par `ast` ; constantes `TERMES_GLOSSAIRE` (27 entrees), `TERMES_INTERDITS`, `PAGES_DE_LA_PHASE`, `TITRE_TERMES`, `TITRE_INDEX`, `TITRE_PARCOURS`, `TITRE_SOURCE`, `SOMMAIRE`, `LIEN_RETOUR`, `BOM`, `RACINES_INTERDITES`, `APPELS_CALCUL_PRODUIT`, `APPELS_SUPPRESSION` ; **22** constantes `MOTIF_*` ; lecteurs locaux `MOTIF_LIGNE_TERME`, `MOTIF_LIEN_MARKDOWN`, `MOTIF_CHEMIN_CITE`, `MOTIF_ENTREE_NUMEROTEE`, `MOTIF_LIGNE_INDEX`, `MOTIF_VOLATILE`, `MOTIF_CHEMIN_POSTE` ; helpers `_texte_page`, `_lignes_de_termes`, `_cellules`, `_chemin_cite`, `_lignes_index`, `_entrees_numerotees`, `_imports_du_module`, `_appels_du_module` ; fonctions pures `problemes_glossaire`, `problemes_page_glossaire`, `problemes_parcours`. Les fixtures partagees de `tests/conftest.py` (`docs_dir`, `normalize`, `section`) sont **reutilisees telles quelles**, jamais recopiees (D-12) : le module ne definit ni normalisation, ni lecteur de section, ni fixture locale.
- `dofus_stuff/**` — **aucun octet modifie** (mesure : `git status --short -- dofus_stuff` vide entre les trois commits ; le code est le referentiel et la page s'y conforme — D-103). `pyproject.toml` inchange, aucune dependance ajoutee.

## Verification

Toutes les commandes ont ete executees avec l'interpreteur epingle `./.venv/Scripts/python.exe` (D-15), jamais un `python` nu. Les batteries sont celles **du plan**, reprises dans `.gsd-tmp/batterie-06-02-auto{2,5,8}.sh` (non suivies par git) : chacune copie l'arbre dans `mktemp -d`, mesure la copie **verte** avant de muter (une copie rouge fait crier le script avant la mutation), mute la copie seule par `python -c` avec `newline=""` (les CR sont preserves), rejoue la suite complete, puis exige un compteur d'echec **et** le motif nomme.

### Tache 1 — `014b2c9`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_glossaire.py tests/test_docs_structure.py -q` | `17 passed in 0.20s` — les 3 tests neufs et les 14 gardes de `docs/` inchangees |
| batterie du plan, morsure `terme_retire` | `mutation detectee (terme_retire), motif "terme declare absent de la page"` |
| batterie du plan, morsure `ordre_inverse` | `mutation detectee (ordre_inverse), motif "ordre des termes"` |
| batterie du plan, morsure `employeur_faux` | `mutation detectee (employeur_faux), motif "terme non employe par le fichier cite"` |
| **synthese de la batterie de la tache 1** | **`morsures 06-02 tache 1 : 3/3 detectees (copie verte avant chaque mutation)`** — aucun message « COPIE ROUGE AVANT MUTATION » |
| `python -m pytest -q` | `231 passed in 4.38s` (228 avant ce plan + 3 tests) |

**Porte de retroaction du `type="tracer"`** (mode standard, `<verify>` entierement automatise) : apres la tache 1, les trois blocs automatises ont ete rejoues — module et gardes de structure verts (`17 passed`), batterie de la tache rejouee (`3/3`), suite entiere verte (`231 passed`) — et aucun echec n'a ete observe. L'execution s'est donc poursuivie sans point d'arret.

### Tache 2 — `d8c36dd`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_glossaire.py -q` (ROUGE, les deux tests ecrits avant la page complete) | `1 failed, 4 passed in 0.08s` — `test_renvois_de_definition` : « TERMES_GLOSSAIRE ne declare aucune page de definition » (le contrat de renvoi vide etait refuse) |
| `python -m pytest tests/test_docs_glossaire.py -q` (VERT apres la page a 27 termes et la constante complete) | `5 passed in 0.08s` |
| `python -m pytest tests/test_docs_glossaire.py tests/test_docs_structure.py -q` | `19 passed in 0.20s` |
| batterie du plan, morsure `renvoi_retire` | `mutation detectee (renvoi_retire), motif "renvoi de definition manquant"` |
| batterie du plan, morsure `terme_interdit_ajoute` | `mutation detectee (terme_interdit_ajoute), motif "terme hors du vocabulaire du produit"` |
| **synthese de la batterie de la tache 2** | **`morsures 06-02 tache 2 : 2/2 detectees (copie verte avant chaque mutation)`** |
| `python -m pytest -q` | `233 passed in 4.35s` (231 + 2 tests) |

### Tache 3 — `67f7bb4`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_glossaire.py -q` | `7 passed in 0.08s` |
| `python -m pytest tests/test_docs_glossaire.py -q -k "parcours"` | `2 passed, 5 deselected in 0.01s` (aucun « no tests ran ») |
| controle applique au sommaire **d'avant** la phase (`git show 110951f:docs/sommaire.md`, 23 lignes) | 2 constats : « le libelle « Dépannage » du parcours conseille ne reprend aucun libelle d'index » et le meme pour « Glossaire » |
| controle applique au sommaire **livre** (25 lignes) | aucun constat ; entrees numerotees lues : `['Installation', 'Parcours simplifié', 'Wizard avancé', 'CLI', 'Base locale', 'Dépannage', 'Glossaire']` |
| batterie du plan, morsure `parcours_libelle_faux` | `mutation detectee (parcours_libelle_faux), motif "parcours conseille"` |
| batterie du plan, morsure `parcours_en_liens` | `mutation detectee (parcours_en_liens), motif "parcours conseille en liens"` |
| **synthese de la batterie de la tache 3** | **`morsures 06-02 tache 3 : 2/2 detectees (copie verte avant chaque mutation)`** |
| `python -m pytest -q` | `235 passed in 4.59s` (233 + 2 tests) |

### Mesures de cloture

| Mesure | Resultat observe |
|---|---|
| empreinte `.data/dofus.sqlite3` (taille: mtime_ns: SHA-256) | `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — **identique** avant le plan, apres chaque tache, apres chaque batterie et apres la suite complete |
| `docs/glossaire.md` | 56 lignes, 56 CRLF, BOM absent (>= 55 exigees) |
| `docs/sommaire.md` | 25 lignes (>= 25 exigees), contenant `[Glossaire](glossaire.md)` ; index a sept pages de contenu |
| `tests/test_docs_glossaire.py` | 769 lignes (>= 210 exigees), 7 tests, 0 `skip`, 0 `xfail` |
| `git diff --diff-filter=D --name-only 030ba01..67f7bb4` | vide — aucun fichier supprime |
| `git diff --stat 030ba01..67f7bb4` | `3 files changed, 826 insertions(+)` (47 746 caracteres de patch) |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — signature des fonctions pures] `normalize` en second parametre de `problemes_glossaire` et de `test_le_vocabulaire_du_harnais_est_absent`**

- **Found during:** Tache 1 (tranche verticale).
- **Issue:** le plan declare `problemes_glossaire(docs_dir) -> list[str]` et `test_le_vocabulaire_du_harnais_est_absent(docs_dir)`, mais l'egalite d'ensembles exigee est une egalite **apres normalisation `D-11`** (c'est elle qui fait passer `catégorie` pour `categorie` et `trophée` pour `trophee`), et `D-12` interdit de recopier le helper partage de `tests/conftest.py`.
- **Fix:** les deux fonctions recoivent la fixture `normalize` en second parametre, exactement comme `problemes_h1(docs_dir, normalize)` et `problemes_encodage(docs_dir, normalize)` de `tests/test_docs_structure.py`.
- **Files modified:** `tests/test_docs_glossaire.py`
- **Verification:** `problemes_glossaire` est appelee avec la fixture dans les deux tests qui la portent, et la suite est verte (`5 passed`, puis `19 passed`, puis `235 passed`) ; la normalisation est bien celle du depot et aucun helper n'est duplique (`grep -c "_normalize" tests/test_docs_glossaire.py` -> 0 : le module ne connait que la fixture partagee).
- **Committed in:** `014b2c9` (tache 1) et `d8c36dd` (tache 2, test qui consomme la constante).

**2. [Rule 2 — motif manquant] Ajout de `MOTIF_FERMETURE = "ligne de fermeture de la page"`**

- **Found during:** Tache 1.
- **Issue:** le plan exige le controle « la derniere ligne non vide egale a `LIEN_RETOUR` » dans `problemes_page_glossaire`, mais la liste des quatorze motifs qu'il fixe n'en nomme aucun pour cette constatation : `MOTIF_CRLF` ne parle que des fins de ligne, `MOTIF_SOURCE` que des chemins du bloc de provenance.
- **Fix:** un motif de plus que les quatorze du plan est porte par le module pour ce controle (le module en compte **22** au total, mesures — les autres viennent des taches 2 et 3), ASCII et sans apostrophe comme les autres, jamais ecrit en clair dans une ligne d'assertion. Precedent : `MOTIF_BUDGET`, ajoute au plan 06-01 pour le controle que son critere d'acceptation nommait et qu'aucun motif existant ne couvrait.
- **Files modified:** `tests/test_docs_glossaire.py`
- **Verification:** le motif apparait dans le constat de `test_page_glossaire_close_et_sans_valeur_volatile` quand la derniere ligne non vide derive, et dans aucun autre constat ; les 7 tests restent verts.
- **Committed in:** `014b2c9`

**3. [Rule 2 — motif partage assume] L'absence de BOM est controlee sous `MOTIF_CRLF`**

- **Found during:** Tache 1.
- **Issue:** le plan demande de controler « CRLF **et** absence de BOM » dans `problemes_page_glossaire`, sans motif dedie au BOM.
- **Fix:** les deux constats de forme du fichier portent `MOTIF_CRLF` (« fins de ligne »), et la phrase du constat dit exactement ce qui est faux (BOM present, ou nombre de CRLF different du nombre de sauts de ligne). Un motif de plus n'aurait servi qu'une seule famille de constats, pour un controle que le plan nomme deja.
- **Files modified:** `tests/test_docs_glossaire.py`
- **Verification:** `problemes_page_glossaire` vert sur la page livree (BOM absent, 56 CRLF pour 56 sauts de ligne) ; le controle mord si le fichier perd ses CR.
- **Committed in:** `014b2c9`

**4. [Rule 3 — l'artefact exigeait 55 lignes] Trois paragraphes ajoutes a la page apres mesure**

- **Found during:** Tache 2.
- **Issue:** la premiere redaction de la page avec les 27 termes mesurait **50 lignes**, sous le `min_lines: 55` que l'artefact du plan exige pour `docs/glossaire.md`.
- **Fix:** trois paragraphes utiles ont ete ajoutes — la consequence de la regle du renvoi (pourquoi les lignes a `-` sont les plus courtes), ce que dit la colonne « Employé par » pour le lecteur, et ce que la page ne juge pas (la redaction releve de la lecture, pas d'un controle). Aucune section de niveau 2 ajoutee, aucune ligne de tableau ajoutee, aucun remplissage.
- **Files modified:** `docs/glossaire.md`
- **Verification:** 56 lignes mesurees apres correction (>= 55), suite verte (`19 passed`, puis `235 passed`), et le bloc `## Source de vérité` reste la derniere section avec la ligne de retour juste apres.
- **Committed in:** `d8c36dd`

**5. [Rule 1 — mesure corrigee] `trophée` renvoie a `docs/wizard-avance.md`, pas a `docs/parcours-simplifie.md`**

- **Found during:** Tache 2, lecture `fichier:ligne` de chaque employeur et de chaque page de definition (D-19).
- **Issue:** la recherche groupe `trophée` avec `familier`, `prysmaradite` et `bouclier` et pointe `docs/parcours-simplifie.md` pour les quatre. Mesure de ce plan : `parcours-simplifie.md` ne contient **pas** le mot (il nomme le familier, la prysmaradite et le bouclier) ; ce sont `docs/wizard-avance.md` (`DOFUS/TROPHÉES`, `F9 TROPHEE`) et `docs/cli.md:112` (« ignorer Dofus, trophées, familier et prysmaradite ») qui le nomment.
- **Fix:** la page de definition declaree pour `trophée` est `docs/wizard-avance.md` (celle qui decrit l'ecran qui les bascule) ; l'employeur reste `dofus_stuff/model/slots.py`, qui l'emploie en clair. Les trois autres termes de ce groupe gardent `parcours-simplifie.md`, mesure a l'appui.
- **Files modified:** `docs/glossaire.md`, `tests/test_docs_glossaire.py`
- **Verification:** les 27 renvois pointent vers une page existante sous `docs/` (22 renvois repartis sur `parcours-simplifie.md` 9, `wizard-avance.md` 7, `base-locale.md` 5, `cli.md` 1) et chaque cible a ete lue `fichier:ligne` avant d'etre ecrite ; `test_renvois_de_definition` et `problemes_glossaire` verts.
- **Committed in:** `d8c36dd`

**6. [Rule 1 — mesure corrigee] L'employeur de `sauvegarde locale` est `terminal.js`, pas la page**

- **Found during:** Tache 2.
- **Issue:** la forme exacte au singulier n'existe dans aucune page livree : `docs/parcours-simplifie.md:174` ecrit `CHARGEMENT DES SAUVEGARDES LOCALES…`, ou « sauvegarde locale » n'est pas une sous-chaine, et c'est `dofus_stuff/web/static/js/terminal.js:324` (`AUCUNE SAUVEGARDE LOCALE.`) qui la porte.
- **Fix:** l'employeur declare est `dofus_stuff/web/static/js/terminal.js` ; la page de definition reste `docs/parcours-simplifie.md`, qui decrit la liste des sauvegardes et sa limite — c'est `D-17` (renvoyer, ne pas redefinir) et `D-19` (employeur mesure) appliquees ensemble.
- **Files modified:** `docs/glossaire.md`, `tests/test_docs_glossaire.py`
- **Verification:** la ligne porte un lien vers `parcours-simplifie.md` (cible resolue) et l'employeur contient le terme apres normalisation — exige par `problemes_glossaire`.
- **Committed in:** `d8c36dd`

---

**Total deviations:** 6 auto-corrigees (1 Rule 3 de signature, 2 Rule 2 de motif, 1 Rule 3 de forme de page, 2 Rule 1 de mesure corrigee apres lecture).
**Impact on plan:** aucun ecart de perimetre, aucune cible affaiblie, aucune semantique inventee. Les deux mesures corrigees (deviations 5 et 6) sont exactement ce que `D-19` demande : la page de definition et l'employeur sont lus avant d'etre ecrits, et une liste de recherche du plan ne remplace pas une mesure. Les motifs et les signatures suivent les patrons deja poses par les phases 3 a 5.

## Issues Encountered

- **Edition d'un module CRLF avec un outil qui ecrit en LF.** Le depot est integralement en CRLF dans l'arbre de travail (`git ls-files --eol` : `i/lf w/crlf` pour `docs/` comme pour `tests/`) et `sed -i` retire les CR sur ce poste (piege paye par 06-01). Chaque grappe d'editions a donc ete suivie d'une passe de conversion explicite en lecture/ecriture **binaire** (`newline=""`) : mesure finale, `docs/glossaire.md` 56 CRLF pour 56 LF et `tests/test_docs_glossaire.py` 769 pour 769. Aucun contenu perdu, aucun double converti.
- **Un helper `ast` supprime par une substitution ciblee.** En inserant `problemes_parcours` (tache 3), la ligne de definition de `_imports_du_module` a ete absorbee par la substitution. Le controle `grep "^def "` qui suit chaque edition l'a montre immediatement et le helper a ete restaure **avant** toute execution : la garde de cloture n'a jamais ete affaiblie, et la premiere execution suivante a rendu `5 passed`, puis `7 passed`.
- **`import pytest` declare par le plan et non employe.** Comme dans `tests/test_docs_depannage.py` (plan 06-01), le module importe `pytest` sans s'en servir : aucun `skip`, aucun `xfail`, aucun marqueur n'est pose dans ce harnais (mesure : 0 occurrence de `skip` et de `xfail` sur ses 769 lignes). L'import a ete laisse tel quel — le retirer aurait modifie le texte du plan sans rien prouver.

## User Setup Required

None — aucune variable d'environnement, aucun secret, aucun service. Toutes les commandes du plan sont hors-ligne (`.venv/Scripts/python.exe -m pytest -q`), aucune resynchronisation Dofusdude n'a ete lancee, `main()` n'a jamais ete execute et aucun POST de confirmation n'a ete emis.

## Known Stubs

None — aucune valeur en dur laissee en place, aucune branche morte : les 27 entrees de `TERMES_GLOSSAIRE` sont confrontees a la page, les 22 motifs servent au moins un constat, `PAGES_DE_LA_PHASE` est consomme par le controle du parcours, et chaque constante du module ci-dessus est lue par au moins une fonction ou un test.

## Threat Flags

None — ce plan ne touche aucun chemin reseau, aucune entree utilisateur, aucune surface d'authentification et aucune ecriture de fichier du produit ; les seules ecritures sont les copies de mutation sous `mktemp -d`, supprimees par le script de batterie lui-meme. `.data/` n'a jamais ete ouverte par SQLite, seulement lue en octets pour son empreinte.

## Declared Limits (not verified, no human check claimed)

- **Qualite redactionnelle du glossaire** : la justesse, l'utilite et le ton des 27 definitions ne sont pas verifiables automatiquement. Aucune relecture humaine n'a eu lieu et aucune n'est revendiquee (D-85). Ce que le harnais prouve est plus etroit et exact : le vocabulaire est complet par rapport au contrat, trie, unique, non redefini (D-17), employe par le fichier declare (D-19) et exempt du vocabulaire de harnais.
- **Rendu Markdown hors GitHub** : le tableau a quatre colonnes est rendu par le moteur de GitHub ; un autre moteur (rendu du depot local, editeur tier) n'est pas mesure.
- **Ordre de lecture du parcours conseille** : il est **libre** par decision de plan. Le controle exige une permutation des libelles d'index, jamais un ordre donne : un parcours qui listerait les sept pages dans un ordre different serait vert, et c'est voulu.
- **Discrimination par un humain du vocabulaire « du produit » et « de la documentation »** : l'ensemble des 27 termes est un choix edite, mesure contre les pages et le code, non une verite extractible du depot. Ce qui est garanti, c'est que tout terme cite ou declare est adosse a un employeur reel et a une page qui le definit deja — pas que la liste soit la seule liste possible.

## Self-Check: PASSED

- Fichiers crees : `docs/glossaire.md` (existe, 56 lignes) et `tests/test_docs_glossaire.py` (existe, 769 lignes) — verifie.
- Fichier modifie : `docs/sommaire.md` (existe, 25 lignes, contient la ligne de glossaire) — verifie.
- Commits : `014b2c9`, `d8c36dd`, `67f7bb4` presents dans `git log` sur `main` — verifie (`git rev-list --count 030ba01..67f7bb4` = 3).
- Compteurs de suite releves tels qu'observes : `231 passed in 4.38s`, `233 passed in 4.35s`, `235 passed in 4.59s` — aucun compteur attendu n'a ete pre-rempli avant l'execution.
