---
phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
plan: 02
subsystem: documentation
tags: [markdown, pytest, flask-test-client, ancrage-au-rendu, wizard-avance, touches-clavier, commandes-recapitulatif, exemple-guide, sqlite-hors-ligne, documentation-francaise]

# Dependency graph
requires:
  - phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
    plan: 01
    provides: "docs/wizard-avance.md (page et ligne d'index), tests/test_docs_wizard.py (marqueurs du gabarit, lecteurs du rendu, garde ast, controle de forme) et la constante TITRES_SECTION_ATTENDUS a completer tache par tache"
provides:
  - "docs/wizard-avance.md : section « Arriver au wizard » (menu `4. OPTIMISATION DE STUFF`, les trois questions, `AVANCE`, atterrissage mesure sur le recap, identifiants `OPT-W1` a `OPT-W9`, `OPT-WED`, `ECRAN WIZARD INCONNU`)"
  - "docs/wizard-avance.md : section « Touches et commandes » (couples `F7`/`F8`/`ESC` par etape, particularite mesuree du recap qui rend `Page suiv` sans pagination, quatre commandes du corps, liste de refus `GO | RESET | SAVES | 1-8`)"
  - "docs/wizard-avance.md : section « Exemple guide » (exemple du guide migre et reancre : niveau `123`, ligne 4 des caracteristiques `300 0 0 1`, variante cible PA `6 0 11 5` conservee parce que le code la porte)"
  - "tests/test_docs_wizard.py : 4 tests de plus (12 au total) — ecrans et arrivee, exemple guide, touches et commandes par etape, empreinte de la base locale"
affects: [04-03, 04-04, verification-phase-4]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (72 000) est consigne tel quel : il mesure le pessimisme de l'estimate, pas
# un travail non fait (les deux taches sont livrees et leurs six morsures sont detectees).
actuals:
  tokens: 9223     # chars/4 sur le diff realise (36 389 caracteres ajoutes, 504 retires, 2 commits)
  tasks: 2
  commits: 2       # MESURE : git rev-list --count c588a98dcd7f6c0bc9e19db36a8d5d0cf416805c..HEAD
  plan_head_before: c588a98dcd7f6c0bc9e19db36a8d5d0cf416805c

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange)
  patterns:
    - "Verite par etape : un libelle qui change aux extremites du parcours (barre de touches) est controle par etape, jamais par une affirmation generale qui serait fausse aux deux bords"
    - "Le motif de morsure porte par une constante du module (MOTIF_ARRIVEE, MOTIF_IDENTIFIANT_ECRAN, MOTIF_EXEMPLE, MOTIF_TOUCHE, MOTIF_COMMANDE_RECAP, MOTIF_COMMANDE_NUMERIQUE), jamais ecrit en clair dans la ligne d'assertion : pytest reproduit la ligne source du assert"
    - "Table de la page lue comme source structuree : une ligne de tableau par etape (numero, mot-cle, couples de touches / identifiant d'ecran), mise en correspondance avec le rendu, jamais avec une liste recopiee"
    - "Commande prouvee par l'action quand elle est sans effet de bord (RESET, SAVES, chiffres 1-8) et seulement citee quand elle execute le solveur (GO) — la garde ast du plan 04-01 continue de refuser toute paire `\"cmd\": \"GO\"` dans le module"
    - "Empreinte (taille, mtime_ns, sha256) de `.data/dofus.sqlite3` relevee avant et apres les rendus, avec saut explicite nomme si la base est absente : le chemin degrade est mesure, jamais un faux vert"

key-files:
  created: []
  modified:
    - docs/wizard-avance.md
    - tests/test_docs_wizard.py

key-decisions:
  - "Le chemin d'arrivee est rejoue pas a pas sur un seul client de test, `AVANCE` poste en minuscules (`avance`) : la casse ignoree, que la page annonce, est ainsi mesuree au lieu d'etre affirmee."
  - "L'ecran d'arrivee est nomme par le titre rendu lu dans la ligne d'en-tete du recap (`RECAPITULATIF`), jamais par une supposition sur le premier ecran du wizard : c'est la correction du point que le guide se trompait."
  - "Les identifiants d'ecrans sont associes aux mots-cles de `WIZARD_STEPS` dans une table de page et confrontes a la ligne d'en-tete rendue (`OPT-W<index>`), l'ecran d'edition gardant son identifiant partage `OPT-WED`."
  - "La table des touches exige les trois couples de chaque etape (F7, F8, ESC) : le controle est scopé par etape, donc aucune assertion ne demande `Precedent`/`Suivant` sur les neuf — ce qui contredirait le rendu des extremites et la ligne 140 de docs/parcours-simplifie.md."
  - "Les quatre libelles du corps du recapitulatif sont lus au rendu et compares a ceux que la section cite, dans les deux sens (un dictionnaire de la section compare au dictionnaire rendu) : renommer un libelle ou en ajouter un rougit sans que la page change."
  - "Les chiffres `1` a `8` ne sont pas recopies : la cible attendue est calculee par `WIZARD_STEPS[n - 1]`, la table des etapes etant lue dans le code (`dofus_stuff/optimize_wizard.py`)."
  - "`GO` n'est jamais poste : il execute le solveur. Sa citation est lue dans le corps rendu, et son execution reelle reste couverte, patchee, par tests/test_web.py — le module d'ancrage ne duplique pas ce controle (D-12)."
  - "L'exemple guide est reancre edition par edition sur des clients neufs : la ligne rendue apres chaque edition doit etre citee par la section, ce qui fait tomber la variante « cible PA » si le code cesse de la porter (mesure : `1. PA B=6 E=0 C=11 W=5`)."
  - "La justification « base 200 + parchemins 100 » du guide est presentee comme une decision du lecteur et non comme une contrainte de l'outil : le wizard n'edite pas les parchemins, il compte la base saisie."
  - "La re-mesure locale de la base est nommee pour ce qu'elle mesure (la fixture `app` construit sa propre base sous `tmp_path`) : le seul controle qui peut detecter une ecriture d'un autre module est la mesure avant/apres autour de la suite entiere, executee par la verification du plan."
  - "Aucun fichier de `dofus_stuff/**` ni `docs/parcours-simplifie.md` n'est modifie : le code et la ligne 140 sont le referentiel, la page s'y conforme (D-64, D-66)."

patterns-established:
  - "Pattern 4 : une affirmation qui n'est vraie que sur une plage d'ecrans est controlee sur cette plage, et la page dit la plage — jamais une generalisation qui serait fausse aux extremites"
  - "Pattern 5 : commande sans effet de bord prouvee par le POST et la redirection ; commande a effet de bord prouvee par sa seule citation, l'execution restant couverte par un test patche cite en commentaire"
  - "Pattern 6 : table de page lue comme donnee structuree (une ligne par entree) et comparee au rendu, dans les deux sens, plutot que par une recherche de sous-chaine dans le texte entier"

requirements-completed: [WIZ-02]

coverage:
  - id: D1
    description: "La page dit le chemin d'arrivee reel, mesure pas a pas : menu `4. OPTIMISATION DE STUFF` -> `/optimize` -> les trois questions -> `AVANCE` -> `/optimize/wizard/recap`, l'arrivee etant le recapitulatif, pas les emplacements"
    requirement: "WIZ-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_ecrans_et_arrivee_du_wizard"
        status: pass
    human_judgment: false
  - id: D2
    description: "Les neuf en-tetes d'ecran portent `OPT-W1` a `OPT-W9` dans l'ordre des etapes, l'ecran d'edition porte `OPT-WED`, un ecran inconnu rend `ECRAN WIZARD INCONNU`, et la page associe chaque etape a son identifiant"
    requirement: "WIZ-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_ecrans_et_arrivee_du_wizard"
        status: pass
    human_judgment: false
  - id: D3
    description: "L'exemple guide migre est reancre : les trois editions (niveau `123`, ligne 4 des caracteristiques `300 0 0 1`, variante PA `6 0 11 5`) sont rejouees sur des clients neufs et leurs lignes rendues sont citees par la page ; aucune commande destructrice n'apparait dans le parcours"
    requirement: "WIZ-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_exemple_guide_ancre_au_rendu"
        status: pass
    human_judgment: false
  - id: D4
    description: "Les couples touche/libelle sont cites par etape : `Page prec`/`Suivant` a l'etape 1, `Precedent`/`Suivant` aux etapes 2 a 8, `Precedent`/`Page suiv` a l'etape 9, `Retour` sur les neuf"
    requirement: "WIZ-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_touches_et_commandes_par_etape"
        status: pass
    human_judgment: false
  - id: D5
    description: "Les quatre commandes du recapitulatif sont citees depuis le corps rendu (`GO = LANCER`, `RESET = REINITIALISER`, `1-8 = RETOUR ECRAN`, `SAVES = STUFFS SAUVEGARDES`), `RESET` et `SAVES` et les chiffres `1` a `8` sont prouves par leur redirection, et la liste de refus `GO | RESET | SAVES | 1-8` est celle du rendu"
    requirement: "WIZ-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_touches_et_commandes_par_etape"
        status: pass
    human_judgment: false
  - id: D6
    description: "Aucun controle du module ne poste `GO` (le libelle est seulement cite, l'execution du solveur restant couverte par tests/test_web.py) et la garde ast refuse toujours cette saisie"
    requirement: "WIZ-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_wizard.py#test_garde_de_cloture_du_harnais"
        status: pass
    human_judgment: false
  - id: D7
    description: "L'empreinte (taille, mtime_ns, sha256) de `.data/dofus.sqlite3` est identique avant et apres les rendus de ce module, et le test saute explicitement, en nommant la raison, quand la base est absente"
    requirement: "WIZ-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_data_locale_non_modifiee_autour_des_rendus"
        status: pass
    human_judgment: false
  - id: D8
    description: "La page tient sa forme : neuf sections dans l'ordre (dont « Arriver au wizard » et « Touches et commandes »), un seul H1 egal au libelle d'index, la ligne de retour au sommaire en dernier, des octets CRLF sans BOM, aucun lien externe et des chemins de code qui existent"
    requirement: "WIZ-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_page_sans_derive_ni_chemin_invente"
        status: pass
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_page_et_index_du_wizard"
        status: pass
    human_judgment: false
  - id: D9
    description: "L'affirmation de docs/parcours-simplifie.md:140 (le wizard affiche `Precedent`/`Suivant`, le resultat `Page prec`/`Page suiv`) reste vraie : le controle du module est scopé par etape et la page dit la verite des extremites au lieu de generaliser"
    human_judgment: true
    rationale: "La verite de la phrase de la ligne 140 est un jugement de lecture sur une page qui appartient a un autre plan (04-03 la convertit en lien, la verification de phase la relit) : le module prouve seulement qu'aucune assertion ne la contredit (les couples sont lus et compares etape par etape). Laisser trancher un humain, plutot que declarer la phrase vraie au nom d'un controle qui ne la lit pas."
    verification: []

# Metrics
duration: 2min
completed: 2026-09-11
status: complete
---

# Phase 4 : Wizard avance et resorption de la dette GUIDE_WIZARD — Plan 02 Summary

**Le wizard avance est decrit par ce qu'il rend vraiment : le chemin d'arrivee reel (menu `4`, trois questions, `AVANCE`, atterrissage mesure sur le **recapitulatif**), les identifiants `OPT-W1` a `OPT-W9`, les couples de touches par etape, les quatre commandes du recapitulatif et l'exemple guide migre et reancre — tenus par 4 nouveaux tests qui rougissent sur 6 derives epinglees.**

## Performance

- **Duration:** 2 min entre le premier et le dernier commit de tache (mesure `git log --format=%cI` : 20:59:36 +02:00 -> 21:01:32 +02:00) ; la lecture du plan, de la recherche et la sonde du rendu qui precedent le premier commit ne sont pas horodatees
- **Started:** 2026-09-11T20:59:36+02:00
- **Completed:** 2026-09-11T21:01:32+02:00
- **Tasks:** 2
- **Files modified:** 2 (`docs/wizard-avance.md` 224 lignes, `tests/test_docs_wizard.py` 1906 lignes)

## Accomplishments

- **Le chemin d'arrivee est mesure, pas raconte** : `POST /` avec `selection=4` -> `/optimize` -> `/optimize/quick/classe` -> les trois questions -> `POST /optimize/quick/niveau` avec `avance` (casse ignoree, prouvee) -> `/optimize/wizard/recap`. La page dit que l'ecran d'arrivee est le **recapitulatif**, ce qui corrige les deux erreurs de l'ancien guide (arrivee « directe » et premier ecran « slots ») ; le mot « direct » n'apparait nulle part dans la page.
- **Les identifiants d'ecrans sont lus au rendu et cites** : chaque en-tete porte `OPT-W<index>` dans l'ordre de `WIZARD_STEPS`, l'ecran d'edition porte `OPT-WED`, et un ecran inconnu repond 302 vers le menu avec `ECRAN WIZARD INCONNU` rendu a l'ecran suivant.
- **Les couples de touches sont exiges par etape** : `Page prec`/`Suivant` a l'etape 1, `Precedent`/`Suivant` aux etapes 2 a 8, `Precedent`/`Page suiv` a l'etape 9, `Retour` sur les neuf — avec la particularite mesuree du recapitulatif qui rend `Page suiv` alors qu'il n'a aucune pagination.
- **Les commandes du recapitulatif sont prouvees des deux facons** : par le rendu (les quatre libelles du corps exiges dans la page, comparaison dans les deux sens) et par l'action (`RESET` -> `/optimize/wizard/slots`, `SAVES` -> `/saves`, chaque chiffre `n` -> `WIZARD_STEPS[n - 1]`, saisie hors liste refusee avec `GO | RESET | SAVES | 1-8`). `GO` n'est **jamais** poste : sa citation vient du corps rendu, son execution reste couverte par `tests/test_web.py`.
- **L'exemple guide est migre sans perte et reancre** : les trois editions sont rejouees sur des clients neufs et rendent `1. NIVEAU = 123`, ` 4. Intelligence B=300 P=0 C=0 W=1` et ` 1. PA B=6 E=0 C=11 W=5`. La variante « cible PA » **survit** parce que le code la porte (`with_exo`, forme `BASE EXO CIBLE POIDS`) ; la justification « base 200 + parchemins 100 » est presentee comme une decision du lecteur, et le refus de format est celui du code pour la ligne editee.
- **La suite est passee de 194 a 198 tests, verte** (12 dans le module) et l'empreinte de `.data/dofus.sqlite3` est **byte-identique** avant et apres la suite complete : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`.
- **6 derives epinglees sont detectees** sur copie jetable verte avant mutation : 3/3 pour la tache 1 (`AVANCE` casse -> « arrivee du wizard », index des identifiants decale -> « identifiant d'ecran », format d'edition deplace hors de PA / PM / PO -> « exemple guide »), 3/3 pour la tache 2 (libelle `Precedent` renomme -> « couple touche/libelle », libelle de `SAVES` renomme -> « commande du recapitulatif », table des chiffres decalee -> « commande numerique »). La batterie de la tache 1 a ete **rejouee apres la tache 2** (3/3 encore detectees) : l'ajout de section n'a pas desarme ses morsures.
- **Le chemin degrade de la mesure d'empreinte est mesure lui aussi** : sur une copie ou `.data/dofus.sqlite3` est absent, le test saute en nommant la raison (`base locale absente : la mesure d'empreinte n'a pas d'objet`), jamais un faux vert.

## Task Commits

Each task was committed atomically:

1. **Task 1 : le chemin d'arrivee reel, les identifiants d'ecrans et l'exemple guide migre** — `b5ed47e` (feat)
2. **Task 2 : les couples de touches par etape, les commandes du recapitulatif et la garde d'empreinte** — `f957649` (feat)

**Plan metadata:** `docs(04-02): complete ...` (voir le commit de metadonnees du plan, qui porte ce SUMMARY et la mise a jour de STATE/ROADMAP)

## Files Created/Modified

- `docs/wizard-avance.md` — deux sections nouvelles et une troisieme : `## Arriver au wizard` (menu, trois questions, `AVANCE`, atterrissage sur le recapitulatif, table des identifiants d'ecrans, `OPT-WED`, `ECRAN WIZARD INCONNU`), `## Touches et commandes` (table des couples par etape, particularite du recap, quatre commandes, liste de refus, renvoi vers le parcours simplifie) et `## Exemple guide` (exemple migre et reancre, variante PA conservee, aucun parcours destructeur). La page passe de 147 a 224 lignes.
- `tests/test_docs_wizard.py` — `TITRES_SECTION_ATTENDUS` completee tache par tache (8 titres a la fin de la tache 1, 9 a la fin de la tache 2), titres nommes un a un pour qu'une insertion ne decale plus la constante ; quatre tests nouveaux (`test_ecrans_et_arrivee_du_wizard`, `test_exemple_guide_ancre_au_rendu`, `test_touches_et_commandes_par_etape`, `test_data_locale_non_modifiee_autour_des_rendus`) et leurs lecteurs (`_identifiants_cites`, `_couples_de_commandes`, `_touches_citees`, `_empreinte`), sans recopier un seul helper de `tests/conftest.py` ni de `tests/test_docs_parcours.py`.

## Decisions Made

- **La casse ignoree d'`AVANCE` est mesuree, pas affirmee** : la chaine d'arrivee poste `avance` en minuscules, ce qui prouve la propriete que la page annonce et fait tomber la mutation `cmd.upper() == "AVANCER"`.
- **L'arrivee est nommee par le titre rendu** (`RECAPITULATIF`, lu dans la ligne d'en-tete du recap) et non par une supposition sur le premier ecran : c'est exactement le point que l'ancien guide se trompait.
- **Les identifiants d'ecrans sont mis en correspondance avec `WIZARD_STEPS`**, pas avec un numero de ligne de tableau : la table de la page porte le mot-cle de l'etape, donc un reordonnancement du code ne peut pas passer inapercu.
- **Le controle des touches est scopé par etape** (les trois couples de chaque etape sont lus dans la barre rendue) : aucune assertion n'exige `Precedent`/`Suivant` sur les neuf, ce qui contredirait le rendu des extremites et la phrase de `docs/parcours-simplifie.md:140`.
- **Les quatre libelles du recapitulatif sont compares dans les deux sens** (dictionnaire de la section = dictionnaire rendu) : un libelle renomme ou ajoute rougit sans que la page change.
- **Les chiffres ne sont pas recopies** : la cible attendue est `WIZARD_STEPS[n - 1]`, lue dans `dofus_stuff/web/optimize_wizard.py`.
- **`GO` reste cite et jamais poste** : le module d'ancrage ne duplique pas l'execution deja couverte, patchee, par `tests/test_web.py` (D-12) ; la garde `ast` du plan 04-01 continue de refuser la paire `"cmd": "GO"`.
- **L'exemple rejoue chaque edition sur un client neuf** : un POST accepte reecrit l'etat de session, donc deux editions sur le meme client mesureraient autre chose.
- **L'empreinte locale est nommee pour ce qu'elle mesure** (la fixture `app` construit sa base sous `tmp_path`) : le seul controle capable de detecter une ecriture d'un autre module est la mesure avant/apres autour de la suite entiere, executee par la verification du plan.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocage : commande du plan non execitable] Le motif `identifiant d'ecran` rompait le quoting shell**

- **Found during:** Tache 1 (batterie de morsures)
- **Issue:** la commande `<automated>` de la tache 1 porte `motif='identifiant d'ecran'` : l'apostrophe de `d'ecran` ferme la chaine entre apostrophes, le fichier n'est plus un script valide et la batterie sort en erreur (meme classe de defaut que celle corrigee au plan 04-01, deviation 1).
- **Fix:** seul le quoting de ce motif a ete corrige (`motif="identifiant d'ecran"`) ; la mutation `identifiant_ecran`, le motif et les trois morsures sont restes identiques au caractere pres. Le motif compare est bien la valeur de `MOTIF_IDENTIFIANT_ECRAN`.
- **Files modified:** aucun fichier du depot (script de batterie hors arbre, non committe)
- **Verification:** les trois mutations de la tache 1 sont detectees avec le motif inchange : `avance_casse` -> "arrivee du wizard", `identifiant_ecran` -> "identifiant d'ecran", `exemple_pa` -> "exemple guide", chacune sur une copie verte avant mutation.
- **Committed in:** aucun commit (correction d'execution, hors depot)

---

**Total deviations:** 1 auto-fixed (1 commande de plan non execitable). Aucun ecart de perimetre.
**Impact on plan:** la correction ne touche que le quoting du script de preuve ; aucune modification de `dofus_stuff/**`, de `docs/parcours-simplifie.md` ni d'un autre fichier de documentation.

## Issues Encountered

- **Le corps du recapitulatif laisse la ligne de barre de touches inchangee a l'etape 9** : le recap rend `Page suiv` alors qu'il n'a aucune pagination (`f8_url is None`), consequence directe de `dofus_stuff/web/routes.py:137-141`. Le fait est documente **tel quel** dans la page, avec la consequence pratique (quitter le recapitulatif passe par les commandes), au lieu d'etre lisse (D-19).
- **La ligne 140 de `docs/parcours-simplifie.md` n'est vraie que sur les etapes intermediaires** : les extremites du wizard rendent `Page prec` et `Page suiv`, comme le resultat. Le controle a donc ete scopé par etape et la page dit la verite des extremites ; la ligne 140 n'a **pas** ete modifiee (elle appartient a 04-03) et n'est pas contredite.
- **La page citait deja un couple `JET = MIN|AVERAGE|MAX`** dans la section des options : le dictionnaire des commandes citees est donc lu dans la seule section des touches et commandes, sinon la comparaison avec le corps du recapitulatif aurait melange deux surfaces. Resolu en cours de tache, sans changement de perimetre.
- **L'estimate du plan (72 000 tokens) surestime largement le travail realise** (mesure : 9 223 tokens sur la meme echelle, chars/4 du diff). L'ecart est consigne tel quel dans `actuals` : il calibre les prochains estimates, il n'est pas lisse pour paraitre plus juste.

## User Setup Required

None — no external service configuration required. Le plan travaille en mode hors ligne : la fixture `app` construit sa propre base SQLite sous `tmp_path`, aucun serveur n'est lance, aucun socket n'est ouvert et rien n'est ecrit sous `.data/`.

## Next Phase Readiness

- **Pret pour le plan 04-04 (vague 3)** : le module d'ancrage du wizard est complet (12 tests) ; le detecteur de renvois obsoletes porte donc sur un module fini, et son rouge initial est attendu sur `GUIDE_WIZARD.md` encore obsolete.
- **Contrat pose pour 04-03 (vague 4)** : la page porte la verite par etape des couples de touches et un renvoi en lien vers `docs/parcours-simplifie.md` ; la ligne 140 de cette page reste inchangee et vraie sur les etapes intermediaires, ce que 04-03 n'a pas a corriger.
- **Contrat pose pour la verification de phase** : les six morsures sont relancables telles quelles (aucune n'ecrit dans l'arbre de travail), la commande `./.venv/Scripts/python.exe -m pytest -q` passe a 198 tests, et la mesure d'empreinte de `.data/dofus.sqlite3` autour de la suite entiere est verte.
- **Limite nommee, non un blocage** : la prose libre de la page n'est pas verifiee par un test (les controles portent sur les libelles, les nombres et les messages **cites**), et aucune exhaustivite de la surface des touches n'est revendiquee — la sonde d'aretes WIZ-02 reste `unclassified`/`unresolved`, ce que le docstring des deux tests ecrit noir sur blanc. Aucune action humaine n'est requise par ce plan.

## Self-Check: PASSED

- `docs/wizard-avance.md` : FOUND
- `tests/test_docs_wizard.py` : FOUND
- Commit `b5ed47e` : FOUND
- Commit `f957649` : FOUND
- `tests/test_docs_wizard.py` : 12 passed
- Suite complete : 198 passed, empreinte `.data/dofus.sqlite3` identique

---

*Phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard*
*Completed: 2026-09-11*
