---
phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
plan: 04
subsystem: documentation
tags: [markdown, pytest, flask-test-client, detecteur-pur, renvois-obsoletes, copie-figee, morsures, etat-rouge-borne, sqlite-hors-ligne, documentation-francaise]

# Dependency graph
requires:
  - phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
    plan: 02
    provides: "tests/test_docs_wizard.py (12 tests, marqueurs du gabarit, lecteurs du rendu, garde ast) et docs/wizard-avance.md : le module complet sur lequel le detecteur s'ajoute, et le fichier encore obsolete qu'il doit juger"
provides:
  - "tests/test_docs_wizard.py : la fonction pure `renvois_obsoletes(texte, faits)` a trois predicats nommes, le lecteur d'attentes mesurees `_faits_du_rendu(app, normalize)`, le lecteur de copie figee `_lire_fixture()`, les constantes de motif des trois formes et de la limite honnete, quatre temoins legitimes, et trois tests nouveaux (15 au total dans le module)"
  - "tests/fixtures/guide-wizard-obsolete.md : la copie figee et partielle des extraits obsoletes du guide (39 lignes, CRLF, UTF-8 sans BOM), signalee par le meme detecteur, qui rend le rouge du critere 5 relancable apres la correction du fichier livre"
  - "L'observation ROUGE du critere 5 (WIZ-03) : `test_aiguillage_sans_renvoi_obsolete` echoue sur GUIDE_WIZARD.md encore obsolete avec les trois formes nommees et le libelle rendu du menu d'optimisation ; le plan 04-03 (vague 4) produira le vert"
affects: [04-03, verification-phase-4]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (66 000) est consigne tel quel : il mesure le pessimisme de l'estimate,
# pas un travail non fait (les deux taches sont livrees, 3/3 morsures detectees et le rouge borne
# est observe). Aucun lissage.
actuals:
  tokens: 6634     # chars/4 sur le diff realise (26 537 caracteres ajoutes, 0 retire, 2 commits)
  tasks: 2
  commits: 2       # MESURE : git rev-list --count fb8d59c066e7a00b4b68f89d6954e3be6c868706..HEAD
  plan_head_before: fb8d59c066e7a00b4b68f89d6954e3be6c868706

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; deux modules stdlib (html, unicodedata)
  patterns:
    - "Detecteur a deux entrees : le meme detecteur juge le fichier livre et une copie figee sous tests/, ce qui rend le rouge relancable apres la correction et protege le controle d'une regression (D-59b)"
    - "Attentes mesurees, jamais recopiees : les faits du detecteur sont lus au rendu (menu de GET /, numero branche sur /optimize decouvert par la redirection du POST /, couple F6/F7 sur les deux pages de slots et corrobore par TYPE_FILTER_KEYS[5]/[6], dernier segment de la chaine d'arrivee) — aucune valeur de produit n'est ecrite de memoire (D-58, T-04-12)"
    - "Constat complet : chaque constat porte sa forme, la valeur fautive, la valeur attendue lue au rendu ET le fichier de code producteur, transporte par `faits` pour que la fonction reste pure (D-13, D-65)"
    - "Regle d'appartenance et non d'egalite stricte pour les jetons de menu : sans elle, les formes abreges que D-47 exige (`4. OPTIMISATION`, `3. PANOPLIES`) seraient declarees fautives et le vert du critere 5 serait inatteignable"
    - "Fenetre de jugement par ligne : la forme (b) n'est evaluee que sur la ligne qui porte la touche, ce qui evite les faux positifs des autres phrases (resistance distance, F7 de navigation)"
    - "Motif de morsure porte par une constante du module (MOTIFS_RENVOI) : les tests de morsure cherchent la chaine du motif, jamais une phrase ecrite en clair dans la ligne d'assertion"

key-files:
  created:
    - tests/fixtures/guide-wizard-obsolete.md
  modified:
    - tests/test_docs_wizard.py

key-decisions:
  - "Le detecteur est une **fonction pure** `renvois_obsoletes(texte, faits)` : ses attentes lui arrivent par `faits` et chaque constat nomme le fichier de code qui les produit (D-13, D-58, D-65). Aucun acces fichier, aucune constante de projet dans son corps."
  - "Le numero du menu qui ouvre l'optimisation est **decouvert**, jamais suppose : chaque numero du menu rendu est poste sur un client neuf et le numero retenu est celui dont la redirection atteint /optimize puis les trois questions. Mesure : `4`."
  - "Le couple F6/F7 vient du rendu **et** est corrobore par TYPE_FILTER_KEYS[5]/[6] + TYPE_FILTER_LABELS (D-53) : une divergence entre les deux sources est signalee comme erreur de harnais, pas comme constat de documentation."
  - "Les libelles sont stockes **tels que le rendu les produit** (entites HTML resolues, espaces reduits) et la comparaison normalise a l'interieur du detecteur, qui doit rester pur : le constat peut ainsi citer `OPTIMISATION DE STUFF` et `ARMES MELEE` mot pour mot, ce qu'un libelle deja normalise ne permettrait pas."
  - "Les jetons `N. LIBELLE` sont cherches **n'importe ou dans la ligne** : les trois occurrences reelles du guide sont en tete de ligne, en gras et entre accents graves, donc une prise limitee au debut de ligne en manquerait deux sur trois."
  - "La regle de comparaison d'un jeton de menu est l'**appartenance de mots significatifs** (longueur >= 4, hors mots-outils LISTE/DES/DE/LA/LE/LES), et non l'egalite stricte ni la contenance de sous-chaine : c'est l'arbitrage de 04-RESEARCH.md, requis par les formes abreges de D-47."
  - "La forme (c) exige une marque d'immediatete **sans** marque de negation (`pas`, `jamais`, `ne`, `n'`) : la page corrigee peut ecrire « vous n'arrivez pas directement dans le wizard », et ce renvoi est legitime (D-60)."
  - "La copie figee est **partielle et annoncee comme telle** (commentaire HTML en tete : pièce de test, pas de la documentation, non citee par docs/) et suit la convention mesuree du depot : UTF-8 sans BOM, CRLF en arbre de travail (39/39), LF en blob git (`core.autocrlf=true`, comme GUIDE_WIZARD.md et docs/wizard-avance.md) — aucune seconde convention introduite."
  - "Le rouge est **consigne tel quel** et le fichier livre n'est pas touche : `git diff --quiet -- GUIDE_WIZARD.md` est vrai apres la tache 2, et le vert appartient au plan 04-03."
  - "Aucune validation humaine n'est revendiquee : le rouge est une sortie de commande, la limite d'inexhaustivite est ecrite dans le module, et rien ne depend d'un geste humain, d'un secret ou d'un reseau."

patterns-established:
  - "Pattern 7 : un controle dont le rouge est transitoire (ici jusqu'a la correction du fichier juge) se prouve sur une **copie figee** jugee par le meme code, sinon la preuve disparait avec la correction"
  - "Pattern 8 : une attente de controle se **mesure** au rendu (redirection suivie, page 2 lue, constante publique corroboree) et le constat en nomme la valeur, le producteur et le fichier de code"

requirements-completed: [WIZ-03]

coverage:
  - id: D1
    description: "`renvois_obsoletes(texte, faits)` est une fonction pure a trois predicats nommes, chaque constat prefixe de son motif ASCII et portant la valeur fautive, la valeur attendue et le fichier de code producteur transporte par `faits`"
    requirement: "WIZ-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_wizard.py#test_copie_figee_signalee_par_le_detecteur"
        status: pass
      - kind: unit
        ref: "tests/test_docs_wizard.py#test_renvois_legitimes_non_signales"
        status: pass
    human_judgment: false
  - id: D2
    description: "Les attentes sont mesurees au rendu : libelles de menu de GET /, numero branche sur /optimize decouvert par la redirection du POST /, couple F6/F7 lu sur les deux pages de slots et corrobore par TYPE_FILTER_KEYS[5]/[6], dernier segment de la chaine d'arrivee (`recap`)"
    requirement: "WIZ-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_copie_figee_signalee_par_le_detecteur"
        status: pass
    human_judgment: false
  - id: D3
    description: "La copie figee `tests/fixtures/guide-wizard-obsolete.md` est signalee par le meme detecteur : six constats couvrant les trois formes, dont un qui nomme le libelle rendu du menu d'optimisation (`OPTIMISATION DE STUFF`) et un qui nomme le libelle rendu de F7 (`ARMES MELEE`)"
    requirement: "WIZ-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_copie_figee_signalee_par_le_detecteur"
        status: pass
      - kind: integration
        ref: "batterie de morsures 04-04 tache 1 : 3/3 formes retirees de la copie figee sont detectees, sur copie verte avant mutation"
        status: pass
    human_judgment: false
  - id: D4
    description: "Aucun renvoi legitime n'est signale : texte corrige type aux formes de D-47, phrase portant F7 et son libelle rendu, phrase negative sur l'arrivee, renvoi en prose (D-60)"
    requirement: "WIZ-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_wizard.py#test_renvois_legitimes_non_signales"
        status: pass
    human_judgment: false
  - id: D5
    description: "GUIDE_WIZARD.md encore obsolete est observe **ROUGE** avec les trois formes nommees et le libelle rendu du menu d'optimisation, le fichier reste byte-identique (`git diff --quiet -- GUIDE_WIZARD.md`) et la fenetre rouge est bornee : le reste du module est vert et la suite complete ne compte qu'un seul echec, nommement celui-ci"
    requirement: "WIZ-03"
    verification:
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_aiguillage_sans_renvoi_obsolete (rouge attendu de cette vague ; vert produit par le plan 04-03)"
        status: fail-by-design
      - kind: integration
        ref: "./.venv/Scripts/python.exe -m pytest -q -> 1 failed, 200 passed (l'echec unique est test_aiguillage_sans_renvoi_obsolete)"
        status: pass
      - kind: integration
        ref: "git diff --quiet -- GUIDE_WIZARD.md -> vrai (le fichier livre n'est pas modifie)"
        status: pass
    human_judgment: false
  - id: D6
    description: "La limite honnete est ecrite dans le module **et** dans les messages : trois formes nommees, aucune exhaustivite revendiquee, l'enonce produit est « le detecteur ne signale rien sur l'aiguillage corrige » ; la limite de precision de la forme (a) borne les jetons juges aux libelles de premier niveau mesures au rendu de GET /"
    requirement: "WIZ-03"
    verification:
      - kind: unit
        ref: "docstring de `renvois_obsoletes` et de `test_aiguillage_sans_renvoi_obsolete`, constante LIMITE_HONNETE relayee par les messages d'echec"
        status: pass
    human_judgment: false
    rationale: "La couverture de formes de renvoi **non nommees** ne peut pas etre prouvee par un controle : elle est nommee dans le module et dans les messages plutot que deleguee a un jugement humain (D-58/D-26, sonde d'aretes WIZ-03 en `unclassified`/`unresolved`). Aucune validation humaine n'est requise ni revendiquee par ce plan."

# Metrics
duration: 1min
completed: 2026-09-11
status: complete
---

# Phase 4 : Wizard avance et resorption de la dette GUIDE_WIZARD — Plan 04 Summary

**Le detecteur de renvois obsoletes existe — une fonction pure a trois formes nommees, dont les attentes sont mesurees au rendu et qui rend, pour chaque constat, la valeur fautive, la valeur attendue et le fichier de code qui la produit — et il a ete lance contre `GUIDE_WIZARD.md` **encore obsolete** : le critere 5 est observe **ROUGE**, avec les trois formes nommees, sans qu'une seule ligne du fichier livre n'ait ete touchee. C'est un resultat attendu, borne a un seul test : le plan 04-03 produira le vert.**

## Performance

- **Duration:** 1 min entre le premier et le dernier commit de tache (mesure `git log --format=%cI` : 21:09:27 +02:00 -> 21:10:16 +02:00) ; le temps d'execution total de l'agent (lecture du plan, de la recherche et des patrons, puis probes de rendu avant le premier commit) represente environ 5 minutes, non horodatees dans les commits
- **Started:** 2026-09-11T21:09:27+02:00
- **Completed:** 2026-09-11T21:10:16+02:00
- **Tasks:** 2
- **Files modified:** 2 (`tests/test_docs_wizard.py` 2360 lignes, `tests/fixtures/guide-wizard-obsolete.md` 39 lignes)

## Accomplishments

- **Le detecteur est un outil, pas un chien de garde d'un seul fichier.** `renvois_obsoletes(texte, faits)` est **pure** : aucun acces fichier, aucun client, aucune constante de projet dans son corps. Ses attentes lui arrivent par `faits`, et chaque constat nomme la forme, la valeur fautive, la valeur attendue **et le fichier de code qui la produit** (D-13, repris par D-65) : `dofus_stuff/web/routes.py` pour le menu et l'arrivee, `dofus_stuff/model/solver_spec.py` pour le couple `F6`/`F7`.
- **Les attentes sont mesurees, jamais recopiees** (D-58, T-04-12). `_faits_du_rendu(app, normalize)` lit au rendu : les libelles du menu principal (`GET /`), le numero qui ouvre reellement l'optimisation en postant **chaque** numero sur un client neuf et en suivant sa redirection jusqu'aux trois questions (mesure : `4`), le couple `F6`/`F7` sur les **deux** pages de `/optimize/wizard/slots` corrobore par `TYPE_FILTER_KEYS[5]`/`[6]` + `TYPE_FILTER_LABELS` (D-53), et le dernier segment de la chaine d'arrivee (`recap`). Faits mesures dans cette session :
  `{'menus': {1: "RECHERCHE D'OBJETS", 2: 'LISTE DES EQUIPEMENTS', 3: 'LISTE DES PANOPLIES', 4: 'OPTIMISATION DE STUFF', 5: 'SYSTEME'}, 'menu_optimisation': 4, 'filtres': {6: 'ARMES DISTANCE', 7: 'ARMES MELEE'}, 'arrivee': 'recap', 'source_menu': 'dofus_stuff/web/routes.py', 'source_filtres': 'dofus_stuff/web/routes.py et dofus_stuff/model/solver_spec.py', 'source_arrivee': 'dofus_stuff/web/routes.py'}`.
- **Trois formes nommees, et rien d'autre.** (a) le renvoi au menu principal se juge par deux prises : une **invitation** (`tapez`/`saisissez` + un numero entre accents graves + l'optimisation) comparee au numero mesure, et un **jeton `N. LIBELLE`** cherche n'importe ou dans la ligne et juge par appartenance de mots significatifs contre le libelle rendu de ce numero ; (b) le renvoi de filtre inverse se juge sur **la ligne** qui porte `F6`/`F7` et un mot de distance sans le libelle rendu de la touche ; (c) l'arrivee « directe » exige une marque d'immediatete **sans** negation.
- **La copie figee garde la morsure.** `tests/fixtures/guide-wizard-obsolete.md` (39 lignes, CRLF, UTF-8 sans BOM, en-tete HTML qui l'annonce comme piece de test et non comme documentation) est signalee par le **meme** detecteur avec **six constats** couvrant les trois formes — dont un qui nomme `OPTIMISATION DE STUFF` (libelle rendu du menu d'optimisation) et un qui nomme `ARMES MELEE` (libelle rendu de `F7`). Retirer une forme de la copie fait rougir le test : **3/3 morsures detectees** sur copie verte avant mutation.
- **Aucun renvoi legitime n'est signale** (D-60) : les quatre temoins du module — texte corrige type aux formes **que D-47 exige** (`4. OPTIMISATION`, `3. PANOPLIES`, `5. SYSTEME`, avec l'invitation correcte a taper le numero mesure), phrase qui porte `F7` **et** `ARMES MELEE`, phrase negative sur l'arrivee, renvoi en prose — rendent **zero constat**. Le premier temoin est aussi la preuve que la forme (a) accepte les formes abreges de D-47.
- **Le critere 5 est observe ROUGE, borne a un seul test, et consigne ici.** Sorties reelles en fin de document (§ *Le rouge observe, verbatim*). `GUIDE_WIZARD.md` est **byte-identique** (`git diff --quiet -- GUIDE_WIZARD.md` est vrai), `README.md` et `docs/parcours-simplifie.md` n'ont pas ete touches, et la suite complete compte **exactement un** echec, nommement `test_aiguillage_sans_renvoi_obsolete`.
- **La limite honnete est ecrite, pas contournee** (D-58/D-26) : trois formes nommees, aucune exhaustivite revendiquee, enonce produit « le detecteur ne signale rien sur l'aiguillage corrige » ; et la limite de precision de la forme (a) est nommee — les jetons `N. LIBELLE` sont juges contre les libelles de **premier niveau** mesures au rendu de `GET /`, donc un renvoi vers un **sous-menu** du meme numero est hors de la surface comparee et serait rapporte comme forme (a).
- **Aucune ecriture hors de `tests/`, aucune execution du produit, aucun reseau** : la garde `ast` du module passe toujours, la collecte des faits se fait sur la fixture `app` (base sous `tmp_path`), et rien n'est ecrit sous `.data/` ni sous `.doc-agent/`. `GO` n'est jamais poste.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : le detecteur a trois formes, ses attentes mesurees et la copie figee qui le rend relancable** — `4ebc5c9` (feat)
2. **Tache 2 : appliquer le detecteur au fichier encore obsolete et consigner le rouge** — `d841500` (test)

**Plan metadata:** `docs(04-04): complete ...` (voir le commit de metadonnees du plan, qui porte ce SUMMARY et la mise a jour de STATE/ROADMAP)

## Files Created/Modified

- `tests/fixtures/guide-wizard-obsolete.md` — **nouveau** (dossier `tests/fixtures/` cree). Copie figee et **partielle** des extraits obsoletes couverts par le wizard avance, **copies verbatim** depuis `GUIDE_WIZARD.md` (verifie ligne par ligne contre le fichier source : la phrase d'invitation `Tapez \`3\` puis ... l'optimisation.`, l'arbre du menu avec `3. OPTIMISATION DE STUFF` et `4. SYSTEME`, la phrase d'arrivee « **directement** », la mention hors arbre `**4. SYSTEME**` + `self-test et gestion de la base.`, la ligne de table `F3`…`prysmaradite` et l'exemple `F7`). En-tete HTML : piece de test, **pas** de la documentation, non citee par `docs/`. Encodage : UTF-8 sans BOM, **CRLF** en arbre de travail (39/39), LF en blob git — exactement la convention mesuree du depot (`core.autocrlf=true`, comme `GUIDE_WIZARD.md` : 330 CRLF en arbre, 0 dans le blob).
- `tests/test_docs_wizard.py` — **modifie** (+492 lignes). Ajouts : `import html`, `import unicodedata` ; la ligne de docstring de module qui annonce l'etat **ROUGE attendu** pendant la phase ; les constantes du detecteur (`MOTIF_RENVOI_MENU`, `MOTIF_RENVOI_FILTRE`, `MOTIF_RENVOI_ARRIVEE`, `MOTIFS_RENVOI`, `FIXTURE_OBSOLETE`, `LIMITE_HONNETE`, `MOTIF_JETON_MENU`, `MOTIF_LIGNE_MENU_RENDU`, `MOTIF_INVITATION`, `MOTIF_NUMERO_CITE`, `RACINE_OPTIMISATION`, `MOTIF_TOUCHE_FILTRE`, `MOTIF_NEGATION`, `MOTS_OUTILS`, `RACINES_DISTANCE`, `RACINES_ARRIVEE`, `MARQUES_IMMEDIATETE`, les quatre temoins legitimes) ; les lecteurs `_sans_accents`, `_mots_significatifs`, `_libelle_rendu`, `_lire_fixture`, `_faits_du_rendu` ; les trois predicats prives `_renvois_au_menu`, `_renvois_de_filtre`, `_renvois_a_l_arrivee` ; la fonction publique `renvois_obsoletes` ; et les trois tests `test_copie_figee_signalee_par_le_detecteur`, `test_renvois_legitimes_non_signales`, `test_aiguillage_sans_renvoi_obsolete`. Le module passe de 12 a **15 tests**. Aucun helper de `tests/conftest.py` ni de `tests/test_docs_parcours.py` n'est recopie (D-12) : la normalisation du detecteur lui est **interne**, precisement parce qu'elle doit rester pure.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocage : commande du plan non discriminante] L'adresse `sed` de la morsure « arrivee retiree » ne matchait pas la ligne reelle**

- **Found during:** Tache 1 (batterie de morsures, premiere execution)
- **Issue:** le plan demande de retirer la forme (c) de la copie figee par `sed -i '/directement dans le wizard/d'`. Le texte reel du guide porte l'emphase : `Vous arrivez **directement** dans le wizard (...)`. Le motif `directement dans le wizard` n'existe donc **litteralement pas** dans le fichier, le `sed` ne supprime **rien**, la forme (c) reste dans la copie figee et la morsure sort en « MUTATION NON DETECTEE (fixture_sans_arrivee) » — un faux negatif de la batterie, pas du detecteur.
- **Fix:** seule l'**adresse** du `sed` a ete corrigee, au plus pres du fichier reel : `sed -i '/directement\*\* dans le wizard/d'`. La mutation (retirer la phrase d'arrivee), le motif cherche (`renvoi obsolete (c)`) et les trois morsures sont restes identiques — meme classe de defaut que la correction de quoting du plan 04-02 (deviation 1), enoncee ici telle quelle.
- **Files modified:** aucun fichier du depot (le script de batterie vit hors arbre, non committe)
- **Verification:** apres correction, `grep -c "arrivez"` sur la copie mutee vaut `0` et la sortie porte `1 failed` **et** la chaine `renvoi obsolete (c)` : `mutation detectee (fixture_sans_arrivee), motif "renvoi obsolete (c)"`. Batterie complete : **3/3** detectees.
- **Committed in:** aucun commit (correction d'execution, hors depot)

**2. [Rule 3 — Blocage : forme de la preuve] Les libelles de `faits["menus"]` sont conserves tels que le rendu les produit, et non deja normalises**

- **Found during:** Tache 1 (ecriture de `_faits_du_rendu`)
- **Issue:** le plan decrit `faits["menus"]` comme « numero → libelle normalise par la fixture `normalize` ». Or `renvois_obsoletes` doit rester **pure** : elle ne peut pas recevoir la fixture et doit donc normaliser elle-meme le texte juge. Stocker des libelles deja normalises aurait mis dans les constats une forme minuscule et sans accents (`optimisation de stuff`), alors que le critere d'acceptation demande qu'un constat **nomme le libelle reellement rendu du menu de l'optimisation** — une preuve qu'on peut relire et rechercher telle quelle.
- **Fix:** les libelles sont stockes **tels que le rendu les produit**, apres resolution des entites HTML et reduction des espaces (`_libelle_rendu`) : `RECHERCHE D'OBJETS`, `OPTIMISATION DE STUFF`, `ARMES MELEE`. La normalisation necessaire aux comparaisons est faite **a l'interieur** du detecteur (`_sans_accents`), qui reste pur. La fixture `normalize` reste utilisee par `_faits_du_rendu`, la ou elle est utile : la **corroboration** du couple `F6`/`F7` entre le rendu et `TYPE_FILTER_KEYS[5]`/`[6]` + `TYPE_FILTER_LABELS` (D-53).
- **Files modified:** `tests/test_docs_wizard.py` (meme commit que la tache 1)
- **Verification:** les constats citent mot pour mot les libelles rendus (`« OPTIMISATION DE STUFF »`, `« ARMES MELEE »`) ; `test_copie_figee_signalee_par_le_detecteur` exige que ces libelles apparaissent dans les constats et passe ; la batterie de morsures reste 3/3.
- **Committed in:** `4ebc5c9`

---

**Total deviations:** 2 auto-fixed (1 commande de plan non discriminante, 1 forme de preuve des attentes). Aucun ecart de perimetre.
**Impact on plan:** aucune modification de `dofus_stuff/**`, de `GUIDE_WIZARD.md`, de `README.md` ou de `docs/**` ; la tache 2 du plan est livree sans changement de fond, et le detecteur n'a ete ni elargi ni affaibli.

## Issues Encountered

- **La fenetre rouge est le resultat attendu de la vague, pas une regression.** `test_aiguillage_sans_renvoi_obsolete` est rouge parce que `GUIDE_WIZARD.md` est **encore** l'ancien guide (D-59a) ; la suite complete affiche `1 failed, 200 passed in 3.54s`. Le plan 04-03 corrige l'aiguillage et produit le vert ; aucun affaiblissement du controle n'est admissible pour l'obtenir, et ce plan n'a pas touche le fichier.
- **`GUIDE_WIZARD.md` porte une occurrence de plus que la recherche n'en annoncait**: en plus de `3. OPTIMISATION DE STUFF` et de la ligne d'invitation, les jetons `4. SYSTEME` apparaissent **trois** fois (l'arbre, la mention hors arbre, et le renvoi du § 12) et `4. GESTION DE LA BASE` une fois — **six** constats de forme (a) sur le fichier livre. Le fait est consigne tel quel : le detecteur juge le numero contre le libelle rendu, donc aucune de ces occurrences ne lui echappe.
- **La premiere redaction du message de commit de la tache 1 a ete abimee par le shell** : les accents graves de `` `renvois_obsoletes(texte, faits)` `` ont ete interpretes comme une substitution de commande et ont disparu du message. Le commit a ete **amende** dans la meme minute avec un message ecrit dans un fichier (`git commit --amend -F`), avant tout autre travail : le hash retenu pour la tache 1 est `4ebc5c9` (le hash intermediaire `dda4d74` n'existe plus dans l'historique). La meme precaution (message en fichier) a ete prise pour la tache 2.
- **L'estimate du plan (66 000 tokens) surestime largement le travail realise** (mesure : 6 634 tokens sur la meme echelle, chars/4 du diff). L'ecart est consigne tel quel dans `actuals` : il calibre les prochains estimates, il n'est pas lisse.

## Le rouge observe, verbatim

Commande et sortie reelles de la tache 2 (extrait, assertion complete en une ligne pour les huit constats) :

```
$ ./.venv/Scripts/python.exe -m pytest tests/test_docs_wizard.py -q -k "renvoi_obsolete"
...
E       AssertionError: GUIDE_WIZARD.md : renvois obsoletes signales sur la page controlee : renvoi obsolete (a) : la ligne « Tapez `3` puis **Entrée** pour ouvrir l’optimisation. » invite a taper `3` pour ouvrir l'optimisation ; le numero mesure qui ouvre l'optimisation est `4` (menu 4 = « OPTIMISATION DE STUFF »), verifie par la redirection de POST / construite par dofus_stuff/web/routes.py ; renvoi obsolete (a) : le jeton de menu « 3. OPTIMISATION DE STUFF » ne designe pas le menu 3 ; le rendu de GET / associe 3 au libelle « LISTE DES PANOPLIES », construit par dofus_stuff/web/routes.py ; renvoi obsolete (a) : le jeton de menu « 4. SYSTEME » ne designe pas le menu 4 ; le rendu de GET / associe 4 au libelle « OPTIMISATION DE STUFF », construit par dofus_stuff/web/routes.py ; [...] ; renvoi obsolete (b) : la ligne « Exemple : pour **interdire les armes à distance**, tapez `F7` (selon la liste affichée) jusqu’à voir `OFF`. » renvoie a une arme de distance par la touche F7 ; le libelle rendu de F7 est « ARMES MELEE », lu sur /optimize/wizard/slots et produit par dofus_stuff/web/routes.py et dofus_stuff/model/solver_spec.py ; renvoi obsolete (c) : la ligne « Vous arrivez **directement** dans le wizard (premier écran : slots et filtres). » affirme une arrivee directe dans le wizard ; la chaine d'arrivee mesuree atteint « recap » apres les trois questions, construit par dofus_stuff/web/routes.py ; [...] ; le vert de ce controle appartient au plan 04-03, qui corrige l'aiguillage, jamais a un affaiblissement du detecteur
1 failed, 14 deselected in 0.19s
```

Les trois autres controles de la vague, verbatim :

```
$ ... (verification de l'etat rouge) ...
ROUGE OBSERVE : les trois formes nommees sont signalees sur GUIDE_WIZARD.md encore obsolète
$ git diff --quiet -- GUIDE_WIZARD.md && echo ...
GUIDE_WIZARD.md inchange par le plan 04-04 : le rouge est reel
$ ./.venv/Scripts/python.exe -m pytest tests/test_docs_wizard.py -q -k "not renvoi_obsolete"
14 passed, 1 deselected in 0.48s
$ ./.venv/Scripts/python.exe -m pytest -q
1 failed, 200 passed in 3.54s
fenetre rouge bornee : exactement un echec, test_aiguillage_sans_renvoi_obsolete
```

La batterie de morsures de la tache 1, verbatim :

```
mutation detectee (fixture_sans_arrivee), motif "renvoi obsolete (c)"
mutation detectee (fixture_sans_filtre), motif "renvoi obsolete (b)"
mutation detectee (fixture_sans_menu), motif "renvoi obsolete (a)"
morsures 04-04 tache 1 : 3/3 detectees (copie verte avant chaque mutation)
```

Les six constats rendus sur la copie figee (mesure directe du detecteur, hors pytest) :

```
renvoi obsolete (a) : la ligne « Tapez `3` puis **Entrée** pour ouvrir l’optimisation. » invite a taper `3` ... le numero mesure qui ouvre l'optimisation est `4` (menu 4 = « OPTIMISATION DE STUFF »)
renvoi obsolete (a) : le jeton de menu « 3. OPTIMISATION DE STUFF » ne designe pas le menu 3 ; le rendu associe 3 au libelle « LISTE DES PANOPLIES »
renvoi obsolete (a) : le jeton de menu « 4. SYSTEME » ne designe pas le menu 4 ; le rendu associe 4 au libelle « OPTIMISATION DE STUFF »
renvoi obsolete (a) : le jeton de menu « 4. SYSTEME » ne designe pas le menu 4 ; le rendu associe 4 au libelle « OPTIMISATION DE STUFF »
renvoi obsolete (b) : la ligne « Exemple : pour **interdire les armes à distance**, tapez `F7` ... » renvoie a une arme de distance par la touche F7 ; le libelle rendu de F7 est « ARMES MELEE »
renvoi obsolete (c) : la ligne « Vous arrivez **directement** dans le wizard (...) » affirme une arrivee directe dans le wizard ; la chaine d'arrivee mesuree atteint « recap » apres les trois questions
```

## Known Stubs

Aucun. Le module ne contient ni valeur vide qui remonterait a l'affichage, ni texte de remplacement, ni `TODO`/`FIXME` : la seule chose qui n'est pas encore satisfaite est **l'etat du fichier juge**, qui appartient au plan 04-03, et elle est ecrite comme telle dans la docstring du module et du test.

## User Setup Required

None — no external service configuration required. Aucune dependance ajoutee (`pyproject.toml` inchange), aucun serveur lance, aucun socket ouvert, aucun reseau, rien d'ecrit sous `.data/` : la fixture `app` construit sa propre base sous `tmp_path` et les faits du detecteur se mesurent en processus sur le client de test Flask.

## Next Phase Readiness

- **Pret pour le plan 04-03 (vague 4)** : le controle est en place et **rouge** ; sa mise au vert se fait en corrigeant `GUIDE_WIZARD.md` (arbre de menu lu au code — `4. OPTIMISATION`, `3. PANOPLIES`, `5. SYSTEME` —, suppression de l'affirmation d'arrivee directe, et mention de la touche correcte pour les armes a distance), **jamais** en touchant au detecteur. Les quatre temoins legitimes du module decrivent deja le texte corrige type : une correction qui s'y conforme passera sans ajustement du controle.
- **Contrat pose pour la verification de phase** : trois morsures relancables (aucune n'ecrit dans l'arbre de travail), la copie figee qui garde le rouge apres la correction, et la limite honnete des trois formes nommee dans le module **et** dans les messages d'echec.
- **Limite nommee, non un blocage** : la couverture de formes de renvoi **non nommees** n'est pas controlee (le detecteur en couvre trois et le dit) ; la sonde d'aretes WIZ-03 reste `unclassified`/`unresolved`, ce que la docstring de `renvois_obsoletes` et celle de `test_aiguillage_sans_renvoi_obsolete` ecrivent noir sur blanc. Aucune action humaine n'est requise par ce plan, aucun secret, aucun reseau.

## Self-Check: PASSED

- `tests/fixtures/guide-wizard-obsolete.md` : FOUND (39 lignes, CRLF 39/39 en arbre de travail, UTF-8 sans BOM)
- `tests/test_docs_wizard.py` : FOUND (15 tests collectes)
- Commit `4ebc5c9` : FOUND
- Commit `d841500` : FOUND
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_wizard.py -q -k "copie_figee or renvois_legitimes"` : 2 passed
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_wizard.py -q -k "renvoi_obsolete"` : 1 failed (rouge attendu, trois motifs presents)
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_wizard.py -q -k "not renvoi_obsolete"` : 14 passed
- `./.venv/Scripts/python.exe -m pytest -q` : 1 failed, 200 passed (un seul echec : `test_aiguillage_sans_renvoi_obsolete`)
- `git diff --quiet -- GUIDE_WIZARD.md` : vrai ; `README.md` et `docs/parcours-simplifie.md` inchanges
- Batterie de morsures 04-04 tache 1 : 3/3 detectees (copie verte avant chaque mutation)

---

*Phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard*
*Completed: 2026-09-11*
