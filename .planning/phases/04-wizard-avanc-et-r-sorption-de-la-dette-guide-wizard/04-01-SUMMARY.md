---
phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
plan: 01
subsystem: documentation
tags: [markdown, pytest, flask-test-client, ast, wizard-avance, ortools-ui, sqlite-hors-ligne, documentation-francaise]

# Dependency graph
requires:
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "harnais documentaire partage (docs_dir, normalize, section, sections) et invariants de docs/ (sommaire exhaustif, H1 egal au libelle d'index, retour au sommaire, encodage)"
  - phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
    provides: "patron d'ancrage « page lue au rendu », marqueurs HTML du gabarit screen.html et motifs de refus lus dans la ligne de statut"
provides:
  - "docs/wizard-avance.md : page unique du flux avance, 6 sections — les 9 etapes dans l'ordre du code, les slots et filtres, les 11 options du solveur, les quatre nombres d'une ligne, la syntaxe des items, le bloc Source de verite"
  - "docs/sommaire.md : la ligne d'index « Wizard avance » dans la table (une seule cible ajoutee)"
  - "tests/test_docs_wizard.py : 8 tests — garde ast de cloture, page et index, ordre des etapes, slots et filtres, options du solveur, formats d'edition, syntaxe des items, conformite de forme de la page"
affects: [04-02, 04-03, 04-04]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
actuals:
  tokens: 18071    # chars/4 sur le diff realise (72 287 caracteres ajoutes, 0 retire, 3 commits)
  tasks: 3
  commits: 3       # MESURE : git rev-list --count c2afc42177c39a3ba1afa1c94a9ae9a3ed5becf1..e4214703ff79e27767984077276202cc4e257c20
  plan_head_before: c2afc42177c39a3ba1afa1c94a9ae9a3ed5becf1

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee
  patterns:
    - "Compte d'une liste sans constante publique : le nombre d'options et le nombre d'emplacements sont derives du corps rendu, jamais d'une table locale privee"
    - "Morsure prouvee sur copie jetable : la copy est verte avant mutation, la mutation est faite dans un dossier temporaire, jamais dans l'arbre de travail"
    - "Garde ast auto-referente : le module d'ancrage s'analyse lui-meme pour interdire un import de base, de processus, de socket ou de reseau, un appel de `main()` et la saisie `GO`"
    - "Motif de morsure porte par une constante du module et jamais ecrit en clair dans la ligne d'assertion : pytest reproduit la ligne source du assert, un motif en clair y serait trouve sans qu'aucun constat soit produit"

key-files:
  created:
    - docs/wizard-avance.md
    - tests/test_docs_wizard.py
  modified:
    - docs/sommaire.md

key-decisions:
  - "Chaque libelle, format et message cite par la page est lu au rendu par le client de test Flask puis exige, dans les deux sens : le rendu est la source, la page est le miroir, et aucun libelle n'est ecrit de memoire (D-19, D-32)."
  - "Les 11 options sont comptees au rendu, pas dans une table locale : `body_options` ecrit onze lignes litterales et la table d'application est locale a `apply_options_input`, donc le rendu est le seul ancrage possible (Pitfall 3, assumption enregistree du plan)."
  - "L'en-tete de chaque ecran est la seule source du titre rendu : la ligne de corps d'un ecran de statistiques porte le titre en majuscules pour sa pagination, mais l'ecran `recap` n'en porte aucun, et l'extraction du titre passe donc par la ligne d'en-tete du gabarit."
  - "Le sous-ecran d'edition est identifie par ce que le rendu porte vraiment (code de programme `OPT-WED`, libelle `VAL`, `maxlength` lu dans la balise du champ) et non par une supposition sur le numero saisi ; la longueur maximale est lue dans la balise du champ, car une recherche libre de `maxlength` trouverait d'abord une autre balise du document."
  - "Le refus de format est mesure sur les deux sous-ecrans : une saisie de trois valeurs rend le message de la forme affichee juste au-dessus, ce qui lie le message de refus a la forme de l'ecran au lieu de le comparer a un texte ecrit de memoire."
  - "La troncature des listes d'objets est mesuree sur onze ajouts : l'ellipse rendue (`… +N`) et le nombre d'entrees affichees doivent se sommer aux saisies postees, ce qui ancre la troncature sur un rapport de nombres plutot que sur un texte."
  - "L'etat vide est compare dans les deux sens et dans les deux etats (client neuf et apres `CLEAR`) : la page cite l'etat lu au rendu, et les deux listes rendues sont comparees a cet etat, jamais a un litteral ecrit dans le module de test."
  - "`+ID` est documente comme un verbe d'ajout et le test le prouve : la saisie `+12345` ne doit pas rendre le message de refus, alors que `12345` sans prefixe le rend — l'affirmation fausse de l'ancien guide est donc desamorcee par une mesure (D-19)."
  - "`TITRES_SECTION_ATTENDUS` compte les 6 sections de ce plan et reste en accord exact avec la page : le plan 04-02 la complete tache par tache, jamais un titre epingle sans sa section (la morsure du controle de forme reste alors discriminante)."

patterns-established:
  - "Pattern 1 : valeur de code citee par une page = lecture du rendu a chaque execution, avec un constat qui nomme la page, la valeur attendue et le fichier de code"
  - "Pattern 2 : helper local pour une sous-section de niveau 3, jamais promu dans `tests/conftest.py`, le helper partage ne connaissant que les titres de niveau 2 (D-12)"
  - "Pattern 3 : deux sources independantes pour un couple sensible (`F6`/`F7` lu au rendu et dans `TYPE_FILTER_KEYS`), pour qu'une permutation des deux libelles ne puisse pas passer"

requirements-completed: [WIZ-01]

coverage:
  - id: D1
    description: "docs/wizard-avance.md existe, est listee dans docs/sommaire.md, porte un H1 egal a son libelle d'index et cite les 9 titres d'etape lus dans la ligne d'en-tete des 9 ecrans rendus"
    requirement: "WIZ-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_page_et_index_du_wizard"
        status: pass
    human_judgment: false
  - id: D2
    description: "Les 9 titres d'etape sont cites dans la section des etapes, dans l'ordre exact de WIZARD_STEPS, chaque titre etant lu au rendu de l'ecran correspondant"
    requirement: "WIZ-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_etapes_dans_l_ordre_du_code"
        status: pass
    human_judgment: false
  - id: D3
    description: "Les 11 emplacements et les 10 filtres sont cites avec leur propre numero, lus au rendu des deux pages de l'ecran, avec F6 = ARMES DISTANCE et F7 = ARMES MELEE adosses a TYPE_FILTER_KEYS"
    requirement: "WIZ-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_slots_et_filtres_ancres_au_rendu"
        status: pass
    human_judgment: false
  - id: D4
    description: "Les deux formes d'edition (BASE POINTS CIBLE POIDS pour les caracteristiques, BASE EXO CIBLE POIDS pour PA / PM / PO) sont citees chacune avec son ecran, lues au sous-ecran reellement atteint, et le refus de format est celui de la forme affichee"
    requirement: "WIZ-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_formats_d_edition_et_refus_reels"
        status: pass
    human_judgment: false
  - id: D5
    description: "Les 11 options du solveur sont citees numero et libelle, et le nombre d'options est derive du rendu de l'ecran (aucune table locale)"
    requirement: "WIZ-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_options_solveur_ancres_au_rendu"
        status: pass
    human_judgment: false
  - id: D6
    description: "La syntaxe des items est citee telle que le code l'applique (couples prefixe/verbe apparies un a un), l'etat vide est celui du rendu dans les deux etats, et un identifiant sans prefixe est refusé alors que +ID ne l'est pas"
    requirement: "WIZ-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_syntaxe_d_items_et_etat_vide"
        status: pass
    human_judgment: false
  - id: D7
    description: "La page tient sa forme de bout en bout : 6 sections dans l'ordre, un seul H1, derniere ligne de retour au sommaire, fins de ligne CRLF sans BOM, aucun lien externe, aucun bloc de commandes, et chaque chemin de code cite existe sur le disque"
    requirement: "WIZ-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_page_sans_derive_ni_chemin_invente"
        status: pass
    human_judgment: false
  - id: D8
    description: "Le sommaire croit d'exactement une cible et les gardes documentaires existantes restent vertes (exhaustivite, H1, liens, encodage)"
    requirement: "WIZ-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_sommaire_lists_every_document"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_h1_matches_sommaire_entry"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_documents_are_utf8_and_not_drafts"
        status: pass
    human_judgment: false
  - id: D9
    description: "Le module d'ancrage n'ouvre ni la base locale, ni un processus, ni une socket, ni le reseau, n'appelle jamais main() et ne poste jamais la saisie GO qui lancerait le solveur"
    requirement: "WIZ-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_wizard.py#test_garde_de_cloture_du_harnais"
        status: pass
    human_judgment: false

# Metrics
duration: 10min
completed: 2026-09-11
status: complete
---

# Phase 4 : Wizard avance et resorption de la dette GUIDE_WIZARD — Plan 01 Summary

**`docs/wizard-avance.md` ancree sur le rendu reel : 9 etapes dans l'ordre du code, 11 emplacements et 10 filtres numerotes, 11 options comptees au rendu, deux formes d'edition jamais fusionnees et la syntaxe d'items avec son refus unique — tenues par 8 tests qui rougissent sur 10 derives epinglees.**

## Performance

- **Duration:** ~10 min entre le premier et le dernier commit de tache (mesure `git log --format=%cI` : 20:39:19 +02:00 → 20:48:39 +02:00) ; la sonde du rendu qui precede le premier commit n'est pas horodatee
- **Started:** 2026-09-11T20:39:19+02:00
- **Completed:** 2026-09-11T20:48:39+02:00
- **Tasks:** 3
- **Files modified:** 3 (`docs/wizard-avance.md` 147 lignes, `docs/sommaire.md` 22 lignes, `tests/test_docs_wizard.py` 1329 lignes)

## Accomplishments

- **Les 9 ecrans du wizard avance sont documentes depuis leur rendu** : chaque titre est lu dans la ligne d'en-tete de l'ecran reellement rendu par le client de test Flask, jamais de memoire, et l'ordre cite est celui de `WIZARD_STEPS`.
- **Les deux derives que le guide portait sont desamorcees par une mesure** : `F7` = `ARMES MELEE` et `F6` = `ARMES DISTANCE` (deux sources independantes), et `+ID` est un verbe d'ajout, pas une saisie interdite — le seul refus est `SYNTAXE : +ID | -ID | !ID | CLEAR`.
- **Les deux formes d'edition ne sont jamais fusionnees** : `FORMAT : BASE POINTS CIBLE POIDS` pour les caracteristiques, `FORMAT : BASE EXO CIBLE POIDS` pour PA / PM / PO, chacune lue sur le sous-ecran d'edition reellement atteint, et le refus de format est le message de la forme affichee.
- **Le nombre d'options est derive du rendu** : onze lignes numerotees extraites du corps de `GET /optimize/wizard/options`, egales une a une a ce que la page cite, sans aucune table locale privee.
- **La suite est passee de 186 a 194 tests, verte** (194 passed) et l'empreinte de `.data/dofus.sqlite3` est **byte-identique** avant et apres la suite complete : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`.
- **10 derives epinglees sont detectees** sur copie jetable verte avant mutation, les trois batteries ayant ete re-executees **apres** la tache 3 (la reecriture de la page aurait pu desarmer les morsures des taches 1 et 2) : 3/3 pour la tache 1 (`titre_etape` → "RESISTANCES ELEM", `index_retire` → "page non listee dans docs/sommaire.md", `h1_desaligne` → "different du libelle d'index"), 3/3 pour la tache 2 (`filtre_permute` → "ARMES MELEE", `slot_retire` → "PRYSMARADITE", `etapes_permutees` → "ordre de WIZARD_STEPS"), 4/4 pour la tache 3 (`formats_permutes` → "BASE EXO CIBLE POIDS", `items_verbe` → "AJOUTER INTERDIT", `etat_vide` → "aucun", `option_renommee` → "ALLOW DOM CRIT").

## Task Commits

Each task was committed atomically:

1. **Task 1 : tranche verticale (page, index, harnais, rendu)** — `b13e011` (feat)
2. **Task 2 : les 9 etapes dans l'ordre du code, les slots et les filtres** — `d6d537e` (feat)
3. **Task 3 : les options, les formats d'edition et la syntaxe d'items** — `e421470` (feat)

**Plan metadata:** aucun commit de metadonnees dans ce plan (le SUMMARY et la mise a jour de STATE/ROADMAP sont hors du perimetre des commits de tache).

## Files Created/Modified

- `docs/wizard-avance.md` — page unique du flux avance : les 9 etapes du wizard, les slots et filtres (11 emplacements, 10 filtres), les 11 options du solveur, les quatre nombres d'une ligne et les deux formes d'edition, la syntaxe des items (`+ID`/`-ID`/`!ID`/`CLEAR`), le bloc Source de verite et la ligne de retour au sommaire.
- `tests/test_docs_wizard.py` — module d'ancrage : marqueurs et lecteurs du rendu (`_lignes_du_corps`, `_statut`, `_entete`, `_touches`, `_champ_saisie`, `_sous_section`, lecteurs d'options, de syntaxe et de listes), garde de cloture par `ast`, et 8 tests.
- `docs/sommaire.md` — la ligne d'index « Wizard avance » dans la table, sans autre modification.

## Decisions Made

- **Aucun libelle ecrit de memoire** : chaque libelle, format et message cite par la page est lu au rendu par le client de test Flask puis exige dans les deux sens, avec des constats qui nomment la page, la valeur attendue et le fichier de code.
- **Le compte des options vient du rendu** : `body_options` ecrit onze lignes litterales et la table d'application est locale a `apply_options_input`, donc aucune constante publique de comptage n'existe et le rendu est le seul ancrage honnete.
- **L'en-tete est la seule source du titre rendu** : la ligne de corps d'un ecran de statistiques porte le titre en majuscules pour sa pagination, mais `recap` n'en porte aucun.
- **Le sous-ecran d'edition est reconnu a ce que le rendu porte** (code de programme `OPT-WED`, libelle `VAL`, `maxlength` lu dans la balise du champ) : `OPT-WED` est le code partage par tous les sous-ecrans d'edition, et la page ne pretend donc pas qu'il identifie les seules options.
- **Le refus de format est mesure sur les deux sous-ecrans** : une saisie de trois valeurs rend le message de la forme affichee juste au-dessus.
- **La troncature des listes est mesuree sur onze ajouts** : le nombre d'entrees affichees et le total annonce par l'ellipse rendue se somment aux saisies postees.
- **L'etat vide est compare au rendu dans les deux etats**, jamais a un litteral ecrit dans le module de test.
- **`TITRES_SECTION_ATTENDUS` compte les 6 sections de ce plan** : le plan 04-02 la complete tache par tache, jamais un titre epingle sans sa section, sinon la morsure du controle de forme serait indiscernable d'une derive.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocage : commande du plan non execitable] Le motif `different du libelle d'index` rompait le quoting shell**

- **Found during:** Task 1 (re-execution de la batterie de morsures apres la tache 3)
- **Issue:** la commande `<automated>` de la tache 1 porte `motif='different du libelle d'index'` : l'apostrophe de `d'index` ferme la chaine entre apostrophes, le fichier n'est plus un script valide (`syntax error near unexpected token '('`) et la batterie sort en erreur sans avoir rien mesure — le plan ne pouvait donc pas etre execute tel quel.
- **Fix:** seul le quoting de ce motif a ete corrige (`motif="different du libelle d'index"`) ; la mutation `h1_desaligne`, le motif et les trois morsures sont restes identiques au caractere pres.
- **Files modified:** aucun fichier du depot (script de batterie hors arbre, non committe)
- **Verification:** les trois mutations de la tache 1 sont detectees avec le motif inchange : `titre_etape` → "RESISTANCES ELEM", `index_retire` → "page non listee dans docs/sommaire.md", `h1_desaligne` → "different du libelle d'index", chacune sur une copie verte avant mutation.
- **Committed in:** aucun commit (correction d'execution, hors depot)

**3. [Rule 1 — Contrat de test ajuste] Le test de conformite de forme prend quatre fixtures au lieu de deux**

- **Found during:** Task 3 (options, formats et syntaxe d'items)
- **Issue:** le plan declare `test_page_sans_derive_ni_chemin_invente(docs_dir, normalize)` ; les controles reellement exiges par la tache (nombre et ordre des titres de niveau 2, bloc Source de verite) demandent le helper partage `sections` et le helper `section`, et recopier ces helpers dans le module aurait duplique la logique partagee (D-12).
- **Fix:** signature portee a `(docs_dir, normalize, sections, section)`, fixtures du harnais partage, sans aucun helper recopie.
- **Files modified:** tests/test_docs_wizard.py
- **Verification:** `./.venv/Scripts/python.exe -m pytest tests/test_docs_wizard.py -q` → 8 passed ; la morsure `h1_desaligne` de la tache 1 et la morsure de titre de la tache 3 restent detectees.
- **Committed in:** `e421470` (commit de la tache 3)

**3. [Rule 3 — Blocage : commentaire de constante faux] Le commentaire de `TITRES_SECTION_ATTENDUS` annoncait des titres de plans futurs deja epingles**

- **Found during:** Task 3 (revue du contrat apres lecture du plan 04-02)
- **Issue:** le commentaire herite de la tache 1 affirmait que les titres des plans 04-02 a 04-04 etaient « poses des maintenant, a leur position finale » ; le plan 04-02 exige au contraire que la constante soit completee tache par tache, en accord exact avec les sections reellement presentes dans la page, sinon la morsure du controle de forme n'est plus discriminante.
- **Fix:** commentaire reecrit pour dire ce que la constante contient (les 6 sections de ce plan) et qui la complete (le plan 04-02, tache par tache).
- **Files modified:** tests/test_docs_wizard.py
- **Verification:** lecture du plan 04-02 (`Output`, tache 1) et suite verte apres la correction (8 passed, puis 194 passed).
- **Committed in:** `e421470` (commit de la tache 3)

---

**Total deviations:** 3 auto-fixed (1 commande de plan non execitable, 1 contrat de test ajuste, 1 commentaire de constante faux). Aucun ecart de perimetre.
**Impact on plan:** les deux corrections rendent le controle de forme utilisable par le plan 04-02 sans faux positif ; aucune modification hors de `docs/` et `tests/`, aucun fichier de `dofus_stuff/**` touche.

## Issues Encountered

- **`OPT-WED` n'identifie pas les options** : la sonde du rendu montre que `OPT-WED` est le code de programme de **tous** les sous-ecrans d'edition (caracteristiques et PA / PM / PO compris). La page decrit donc le sous-ecran des options par `OPT-WED`, `VAL` et `maxlength=20` ensemble, et le controle des formats s'appuie sur la ligne `FORMAT : ...` lue au rendu, jamais sur le code de programme. Resolu en cours de tache, sans changement de perimetre.
- **La troncature des listes d'objets utilise une ellipse Unicode (`…`) et une ligne separee** : une premiere formulation cherchait `...` dans le contenu de la liste ; la mesure a montre que l'ellipse est une ligne a part et que le compte affiche reste le compte complet. Le controle porte desormais sur la ligne d'ellipse et sur la somme entrees affichees + total annonce. Resolu en cours de tache.
- **Le shell de l'hote resout `python` vers un interpreteur sans pytest** : toutes les commandes ont donc ete lancees avec le chemin explicite `./.venv/Scripts/python.exe` du projet, comme le plan l'ecrit.

## User Setup Required

None — no external service configuration required. Le plan travaille en mode hors ligne : la base locale `.data/dofus.sqlite3` n'est ni lue ni ecrite par le harnais, qui construit sa propre base dans un dossier temporaire.

## Next Phase Readiness

- **Pret pour le plan 04-02** : la page, sa ligne d'index et le module d'ancrage existent ; `TITRES_SECTION_ATTENDUS` est en accord exact avec les 6 sections presentes et n'attend que les sections que 04-02 creera (`## Arriver au wizard`, `## Exemple guide`, puis `## Touches et commandes`).
- **Contrat pose pour 04-02** : les helpers locaux (`_sous_section`, lecteurs de rendu, `_couples_texte`) sont reutilisables sans etre promus dans `tests/conftest.py` ; les marqueurs HTML du gabarit et l'extraction de la ligne d'en-tete sont deja en place.
- **Limite nommee, non un blocage** : la prose libre de la page n'est pas verifiee par un test — les controles portent sur les libelles, les nombres et les messages **cites**, et le plan ne revendique aucune exhaustivite de la redaction. Aucune action humaine n'est requise par ce plan.

---

*Phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard*
*Completed: 2026-09-11*
