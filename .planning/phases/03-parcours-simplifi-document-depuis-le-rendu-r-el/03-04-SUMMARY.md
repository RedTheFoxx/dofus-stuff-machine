---
phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
plan: 04
subsystem: documentation
tags: [markdown, pytest, flask-test-client, ast, balayage-surface-publique, solveur-paliers, empreinte-sha256, sqlite-lecture-seule, crlf-sans-bom, documentation-francaise]

# Dependency graph
requires:
  - phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
    provides: "docs/parcours-simplifie.md (les sept sections precedentes, le bloc Source de verite et la ligne de retour) et tests/test_docs_parcours.py (helpers _lignes_du_corps, _statut, _touches, _entete, _client_etape, _sous_section, _valeurs_tableau, constantes de titres dont TITRE_SUPPOSE / TITRE_LIMITES / TITRE_CORRESPONDANCE, garde ast auto-referente), suite verte a 181 tests"
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "harnais documentaire partage (docs_dir, section, sections, normalize) et invariants de docs/ (liens, sommaire, H1, encodage, comptage des couples)"
provides:
  - "docs/parcours-simplifie.md : les sections « Ce que l'outil suppose » et « Ce que l'outil ne fait pas », inserees avant « Source de verite » — la page porte desormais ses neuf sections de niveau 2, un seul H1 et la ligne de retour, en CRLF sans BOM (269 lignes)"
  - "tests/test_docs_parcours.py : NIVEAUX_BALAYES, NIVEAUX_PALIERS, CIBLES_PA_MESUREES, CIBLES_PM_MESUREES, PALIERS_PAGE, ENSEMBLES_CLASSES_ATTENDUS, MODES_COMPATIBILITE, TITRES_PAGE, MOTIF_SECTION, MOTIF_CRLF, BASE_LOCALE, les helpers _ensembles_de_classes, _tableau_paliers, _valeur_cols, _empreinte, _cite_en_mot_entier et cinq tests : test_hypotheses_prouvees_par_balayage (V11, V12, V13), test_limites_ancrees_sur_le_code, test_page_complete_et_sans_derive (V14), test_data_locale_non_modifiee_autour_des_rendus (V15), test_entete_des_trois_ecrans_de_questions_cite (RF-2)"
affects: []

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
actuals:
  tokens: 13765    # chars/4 sur le diff realise (55 059 caracteres, +71/-1 page, +856/-1 module)
  tasks: 3
  commits: 3       # MESURE : git rev-list --count 33a877df769d8e5169db8bddfcfbc67c45fc2fca..HEAD
  plan_head_before: 33a877df769d8e5169db8bddfcfbc67c45fc2fca

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (contrainte projet C1)
  patterns:
    - "Prise d'hypothese par balayage d'une surface publique pure : `recommendation_spec` ne resout rien, donc capital, paliers PA/PM et ensembles de classes sont mesures sur les bornes des paliers (1, 39, 40, 99, 100, 149, 150, 200) sans lancer le solveur ni lire la base"
    - "Ensembles de classes extraits par `ast` a chaque execution (les quatre ensembles du code, plus `CLASSES`) : le nombre de classes sans objectif propre est CALCULE, jamais ecrit de memoire, et la page doit citer le nombre calcule"
    - "Controle bidirectionnel d'une ligne litterale : la ligne rendue est exigee de la page (normalisee) ET retrouvee dans la source du rendu par une expression reguliere dont le constat nomme le motif cherche — un echec dit ce qui a ete cherche, jamais seulement que le resultat differe"
    - "Composante de code citee par une page = valeur extraite de sa source a chaque execution (`COLS` depuis `screens.py:5`) et retiree du texte avant la recherche des valeurs volatiles, seule valeur numerique a trois chiffres admise dans la section des limites"
    - "Empreinte de fichier (taille, mtime_ns, sha256) pour comparer deux instants : la re-mesure locale est nommee pour ce qu'elle mesure, et la morsure de la mesure se demontre sur une COPIE dans un dossier temporaire, jamais sur la base du depot"

key-files:
  created: []
  modified:
    - docs/parcours-simplifie.md
    - tests/test_docs_parcours.py

key-decisions:
  - "Les hypotheses sont mesurees, pas recopiees (D-42) : le capital vient de `total_capital_for_level` et `capital_spent` sur la surface publique, les cibles PA/PM du tableau de la page sont balayees aux niveaux de bordure des paliers, les quatre ensembles de classes sont extraits par `ast`, et le nombre de classes sans objectif est calcule (`len(CLASSES)` moins l'union des ensembles extraits, valeur epinglee 9). Deplacer un seuil ou retirer une classe rougit sans que la page change."
  - "La provenance du nombre affiche est mesuree, pas supposee : l'ensemble des modes de compatibilite rendus entre crochets (`optimal_prouve`, `borne_solver`, `borne_heuristique`) est extrait de `dofus_stuff/optimize/score.py` et exige de la page, la tournure « n'est pas une qualite en combat » etant epinglee a cote — l'indice de recherche est une mesure interne au solveur, jamais une note de combat (T-19)."
  - "Les heuristiques de classe sont presentees comme telles (ECR-3) : la page porte la tournure « preferences de style de jeu » et le controle exige le commentaire du code (`# Broad playstyle preferences, not a simulation of class spells.`, `recommend.py:44`) — le module ne pretend ni qu'elles simulent les sorts, ni qu'elles n'existent pas."
  - "La limite « selection du catalogue » est adossee au code, sans nom d'option recopie (D-37) : le filtre de plausibilite (`candidates.py:56`), la profondeur par emplacement (`recommend.py:60`) et la coupe `url[:COLS]` (`routes.py:1336`) sont exiges de la SOURCE, la page decrivant le mecanisme ; la ligne rendue sur la selection du catalogue est exigee des deux cotes."
  - "RF-1 garde la forme choisie au plan et ecrit son residu dans le message du controle : la valeur extraite de `COLS` est retiree du texte **en mot entier** avant la recherche des nombres a trois chiffres ; un autre nombre a trois chiffres est attrape (mesure : `1219` injecte), mais une page correcte qui citerait legitimement un nombre egal a la valeur de `COLS` dans cette seule section pourrait rougir — le constat dit lequel des deux et pourquoi."
  - "La page renvoie aux reglages avances et a la base locale **en prose, sans lien** (D-44) : les cibles n'existent pas encore, et un lien serait une cible morte ; le controle de cloture verifie l'absence de `](wizard-avance.md)` et `](base-locale.md)` sur la page entiere."
  - "La cloture de la page est un controle de forme, jamais de fond (V14) : les neuf titres de niveau 2 epingles dans l'ordre, un seul H1, la derniere ligne non vide `[Retour au sommaire](sommaire.md)`, aucun bloc ```console, aucun lien externe, et des octets lus en BINAIRE (CRLF sans BOM) — un texte re-encode ne dirait rien de l'encodage."
  - "La re-mesure de `.data/dofus.sqlite3` est nommee pour ce qu'elle mesure : `tests/conftest.py` construit sa propre base sous `tmp_path/data` et aucun test de la suite n'ouvre `.data/`, donc cette re-mesure locale prouve que **ce module** n'y touche pas et **ne peut pas** detecter une ecriture faite par un autre module ; le controle qui possede ce pouvoir est la mesure avant/apres autour de la suite entiere (executee a la verification de la tache 3, resultat cite ci-dessous)."
  - "RF-2 est traite par la premiere branche proposee par `03-REVIEW-FIX.md` : la page cite l'en-tete rendu des trois ecrans de questions (`OPT-SIMPLE` et `** RECOMMANDATION DE STUFF **`) et un controle le relit par `_entete` a chaque execution — le code est exige comme MOT entier, sans quoi un code derive `OPT-SIMPL` serait satisfait par la citation de `OPT-SIMPLE`."
  - "Aucun geste interdit n'a ete approche : `.data/` est lu (empreinte), jamais ecrit ; aucune synchronisation Dofusdude, aucun `db clear`, aucune suppression ; la fixture `app` fournit la seule base utilisee par les rendus."

patterns-established:
  - "Pattern 1 : hypothese d'outil = balayage d'une surface publique pure aux bornes des paliers, jamais une constante ecrite de memoire ni un solveur lance pour rien"
  - "Pattern 2 : limite d'outil = fichier et ligne cites dans le constat, ce qui n'est adosse a rien etant presente comme une interpretation, jamais comme une verite de code"
  - "Pattern 3 : garde non scopee a cote d'une regle scopee, quand la morsure a montre que le titre porteur peut disparaitre (une regle scopee a un titre devient inoperante quand ce titre derive)"
  - "Pattern 4 : mesure d'empreinte = trois composantes nommees (taille, mtime_ns, sha256) et discrimination demontree sur une copie temporaire, jamais sur le fichier du depot"

requirements-completed: [SIMP-04]

coverage:
  - id: D1
    description: "La section « Ce que l'outil suppose » porte la formule du capital `5 * (niveau - 1)`, les tableaux des paliers 1-39 / 40-99 / 100-149 / 150-200 avec les cibles PA/PM mesurees aux niveaux de bordure, et la base de PA qui bascule au niveau 100"
    requirement: "SIMP-04"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_hypotheses_prouvees_par_balayage"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 1 : palier_pa et capital detectees (motifs « cible PA mesuree au niveau » et « capital »), copie verte verifiee avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D2
    description: "Les quatre ensembles de classes et l'objectif que chacun ajoute sont extraits par `ast` du code, le nombre de classes sans objectif propre est calcule (9), et la page exige ces ensembles, la tournure « preferences de style de jeu » et le commentaire du code : les heuristiques sont presentees comme telles, sans etre niees ni presentees comme une simulation"
    requirement: "SIMP-04"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_hypotheses_prouvees_par_balayage"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 1 : classe_retiree detectee (motif « Osamodas »), copie verte verifiee avant mutation"
        status: pass
    human_judgment: false
  - id: D3
    description: "L'ambiguite `base+parcho` est levee et les deux lignes litterales d'hypothese sont exigees des deux cotes (page et `dofus_stuff/optimize/api.py`), le constat nommant le motif cherche"
    requirement: "SIMP-04"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_hypotheses_prouvees_par_balayage"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 1 : ligne_hypothese detectee (motif « sans exo\\/parchemins »), copie verte verifiee avant mutation"
        status: pass
    human_judgment: false
  - id: D4
    description: "La section « Ce que l'outil ne fait pas » borne l'indice de recherche (trois modes de compatibilite lus dans `score.py`, tournure « n'est pas une qualite en combat »), decrit la selection du catalogue (filtre de plausibilite, profondeur par emplacement, ligne rendue) et ne cite aucun nombre de trois chiffres ou plus hors la valeur de `COLS` lue dans `screens.py`"
    requirement: "SIMP-04"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_limites_ancrees_sur_le_code"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 2 : mode_retire, plausibilite et chiffre_volatile detectees (motifs « borne_heuristique », « _is_plausible_equipment », « 1219 »), copie verte verifiee avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D5
    description: "La coupe de l'adresse quand l'ouverture du navigateur echoue est adossee au code (`url[:COLS]`, `routes.py:1336`) et la page cite la largeur reellement appliquee, lue dans `screens.py:5` ; les renvois aux reglages avances et a la base locale sont en prose, sans lien (D-44)"
    requirement: "SIMP-04"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_limites_ancrees_sur_le_code"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 2 : lien_interdit detectee (motif « wizard-avance.md »), copie verte verifiee avant mutation"
        status: pass
    human_judgment: false
  - id: D6
    description: "La page est complete et conforme : ses sections de niveau 2 sont exactement les neuf titres epingles dans l'ordre, un seul H1, la derniere ligne non vide est la ligne de retour, aucun bloc ```console, aucun lien externe, aucun lien vers une page inexistante, et les octets sont en CRLF sans BOM"
    requirement: "SIMP-04"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_page_complete_et_sans_derive"
        status: pass
      - kind: other
        ref: "batterie de morsures tache 3 : section_renommee, lien_externe et lf_converti detectees (motifs « section de niveau 2 manquante ou renommee », « lien externe », « CRLF »), copie verte verifiee avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D7
    description: "`.data/dofus.sqlite3` est intact (taille, mtime_ns, SHA-256) autour de la suite ENTIERE (185 puis 186 tests) et la mesure discrimine, demontre sur une copie modifiee dans un dossier temporaire ; la base absente produit un skip nomme, jamais un faux vert"
    requirement: "SIMP-04"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_data_locale_non_modifiee_autour_des_rendus"
        status: pass
      - kind: other
        ref: "mesure autour de la suite complete : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b avant et apres `pytest -q` (identique)"
        status: pass
      - kind: other
        ref: "discrimination de _empreinte : copie du dossier temporaire modifiee d'un octet -> empreinte differente (« mesure discriminante »), reference du depot inchangee (24989696, 1788730056843137500)"
        status: pass
    human_judgment: false
  - id: D8
    description: "L'en-tete rendu des trois ecrans de questions est cite par la page : le code de programme et le titre lus dans le rendu (`_entete`) sont exiges de la page, le code comme mot entier, pour les trois etapes et a l'identique (RF-2, DOCS-04)"
    requirement: "SIMP-04"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_entete_des_trois_ecrans_de_questions_cite"
        status: pass
      - kind: other
        ref: "deux morsures mesurees hors plan : page sans OPT-SIMPLE et pgm renomme (OPT-SIMPL) -> motif « en-tete rendu des trois questions non cite » dans les deux cas, copie verte verifiee avant mutation"
        status: pass
    human_judgment: false

# Metrics
duration: 17 min
completed: 2026-09-11
status: complete
---

# Phase 3 Plan 04: Ce que l'outil suppose, ce qu'il ne fait pas, et la cloture de la page Summary

**Le critere 4 est tenu par la mesure, pas par la prose : les hypotheses de l'outil (capital, paliers PA/PM, heuristiques de classe, ni exo ni parchemins) sont prouvees par balayage sur la surface publique pure et ses limites (indice de recherche borne au solveur, recherche sur une selection du catalogue, coupe de l'adresse) sont adossees a des fichiers et des lignes cites — puis la page est close sur ses neuf sections, en CRLF sans BOM, et `.data/dofus.sqlite3` est mesuree intacte de part et d'autre de la suite entiere.**

## Performance

- **Duration:** ~17 min pour les trois taches (mesure : commit de tete du plan `33a877d` a 19:03:55 → commit de la tache 3 `7561940` a 19:20:43), la cloture SUMMARY/STATE/ROADMAP suivant
- **Tasks:** 3
- **Files modified:** 2 (0 cree, 2 modifies)
- **Commits:** 3 (un par tache)

## Accomplishments

- `docs/parcours-simplifie.md` gagne les deux sections attendues, **avant** `## Source de vérité` : `## Ce que l'outil suppose` (formule du capital `5 * (niveau - 1)`, tableau des quatre paliers avec les cibles PA/PM, base de PA qui bascule au niveau 100, objectifs ajoutes par classe, nombre de classes sans objectif propre calcule — 9, tournure « préférences de style de jeu », libellé ajustable après calcul, ligne « sans exo/parchemins », levée de l'ambiguïté `base+parcho`) et `## Ce que l'outil ne fait pas` (les trois modes de compatibilité lus dans `score.py`, l'indice qui n'est pas une qualité en combat, la recherche sur une sélection du catalogue, la coupe de l'adresse à 100 caractères lue dans `screens.py`, les renvois en prose vers les réglages avancés et la base locale). La page porte désormais **neuf** sections de niveau 2, un seul H1 et la ligne de retour, en **CRLF sans BOM** (269 lignes, mesure octet par octet).
- `tests/test_docs_parcours.py` gagne les constantes de balayage et de paliers, les ensembles de classes, les modes de compatibilité, les neuf titres de page, les marqueurs de format, la base locale, les helpers `_ensembles_de_classes`, `_tableau_paliers`, `_valeur_cols`, `_empreinte`, `_cite_en_mot_entier` et **cinq tests** : `test_hypotheses_prouvees_par_balayage` (V11, V12, V13), `test_limites_ancrees_sur_le_code`, `test_page_complete_et_sans_derive` (V14), `test_data_locale_non_modifiee_autour_des_rendus` (V15) et `test_entete_des_trois_ecrans_de_questions_cite` (RF-2). Le module passe de 12 a **17 tests**.
- **Le capital est prouvé par balayage, pas récité :** pour chacun des huit niveaux de la liste (1, 39, 40, 99, 100, 149, 150, 200), `capital_spent(recommendation_spec("Cra", ["terre"], niveau).goals…, niveau)` est comparé à `total_capital_for_level(niveau)` et à `5 * (niveau - 1)` ; les cibles PA/PM du tableau de la page sont balayées aux niveaux de bordure des paliers et comparées aux valeurs **mesurées** (6/3, 8/4, 10/5, 11/6), jamais recopiées de la ligne conditionnelle qu'elles remplacent. Aucun solveur n'est lancé pour ces preuves : `recommendation_spec` construit une spécification sans rien résoudre.
- **Les ensembles de classes sont extraits par `ast` à chaque exécution :** les quatre ensembles du code sont lus au niveau du module (et non dans un corps de fonction), `len(CLASSES)` est lu sur le produit, et le nombre de classes sans objectif propre est **calculé** (`len(CLASSES)` moins l'union des ensembles extraits, valeur épinglée 9). Retirer `Osamodas` de l'ensemble des dommages distance rougit le module en nommant la classe.
- **Les deux lignes littérales d'hypothèse sont exigées des deux côtés** (page et `dofus_stuff/optimize/api.py`), la ligne du code étant cherchée par une expression régulière dont le constat **nomme le motif cherché** (`Points inclus ; sans exo\/parchemins\. …`) : l'échec dit ce qui a été cherché, jamais seulement que le résultat diffère.
- **La section des limites ne cite aucun nombre de catalogue :** la seule valeur numérique à trois chiffres admise est celle de `COLS`, extraite de `dofus_stuff/web/screens.py:5` à chaque exécution et retirée du texte en mot entier avant la recherche de `\d{3,}`. La garde non scopée ajoutée en cours de tâche (voir écarts) attrape en plus tout nombre à quatre chiffres ou plus où qu'il soit dans la page : mesuré, la page n'en porte aucun aujourd'hui, et la morsure qui injecte `1219` rougit en le nommant.
- **La mesure de `.data/` possède son pouvoir et le dit :** la re-mesure locale encadre un **rendu réel** du résultat (session injectée sous `recommendation_input`, `POST` de l'étape 3, solveur exécuté sur la base de la fixture `tmp_path/data`, diagnostics exigés sur les pages concaténées) ; sa limite est écrite dans le test — elle prouve que **ce module** ne touche pas à `.data/`, pas ce qu'un autre module ferait. Le contrôle qui a ce pouvoir est la mesure avant/après **suite entière** :
  - `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` **avant et après** `pytest -q` — identique (suite verte à 186 tests).
  - Discrimination démontrée sur une **copie** dans un dossier temporaire (un octet ajouté → empreinte différente, message « mesure discriminante »), la référence du dépôt restant `24989696` / `1788730056843137500` : `.data/` n'a jamais été écrit, ni par le test, ni par la démonstration.
- **Treize morsures détectées sur copie verte vérifiée avant chaque mutation** : les onze du plan (4 en tâche 1, 4 en tâche 2, 3 en tâche 3) **plus deux** pour le contrôle RF-2 ajouté (page sans le code de programme, `pgm` renommé en `OPT-SIMPL`). Toutes rapportent le motif attendu dans la sortie ; aucune ne doit sa détection à la ligne source de l'`assert`.
- Suite complète verte : **186 passed** (181 avant ce plan + 5), `.data/dofus.sqlite3` intact, `docs/` conforme, aucun fichier produit touché.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : les hypotheses de l'outil mesurees sur la surface publique et citees par la page** - `7a537f7` (feat)
2. **Tache 2 : les limites de l'outil adossees au code, sans chiffre de catalogue** - `c945037` (feat)
3. **Tache 3 : la cloture de la page et l'empreinte de la base locale** (+ RF-2) - `7561940` (feat)

**Plan metadata:** `HEAD` apres le commit de cloture de ce plan (docs: complete plan).

_Note: `TDD_MODE=false` pour cette phase — aucun cycle RED/GREEN/REFACTOR n'etait requis. `MVP_MODE=true`, `ISOLATION=none` : execution sequentielle sur l'arbre principal, les mises a jour STATE/ROADMAP/REQUIREMENTS sont faites par cet executeur._

## Files Created/Modified

- `docs/parcours-simplifie.md` (modifie, +71/-1, 269 lignes, CRLF, UTF-8 sans BOM) — les sections `## Ce que l'outil suppose` (quatre sous-sections) et `## Ce que l'outil ne fait pas` (quatre sous-sections), inserees entre `## Sauvegarder et exporter` et `## Source de vérité`, qui reste la derniere section avant la ligne de retour ; la phrase d'ouverture de `## Question 1/3 : la classe` nomme desormais le programme `OPT-SIMPLE` et son titre d'en-tete (RF-2).
- `tests/test_docs_parcours.py` (modifie, +856/-1, 2 734 lignes, CRLF, UTF-8 sans BOM, 17 tests) — imports (`hashlib`, `pytest`), le paragraphe de limite nommee (balayage, empreinte, en-tete cite) dans le docstring, les blocs `# --- Hypotheses … (plan 03-04, tache 1) ---`, `# --- Limites adossees au code … (plan 03-04, tache 2) ---`, `# --- Cloture de la page et empreinte de la base locale (plan 03-04, tache 3) ---` et `# --- En-tete rendu des trois ecrans de questions … (RF-2) ---`, leurs constantes, leurs helpers et leurs cinq tests.

## Decisions Made

- **Rien n'est écrit de mémoire (D-42).** Le capital et les paliers sont mesurés sur la surface publique, les ensembles de classes extraits par `ast`, le nombre de classes sans objectif calculé, la valeur de `COLS` relue dans `screens.py:5`, les modes de compatibilité lus dans `score.py`, la ligne du catalogue relue dans `api.py`, et l'en-tête lu dans le rendu. Chaque message d'échec nomme la page, la valeur attendue et le fichier ou la ligne de code.
- **Ce qui n'est adossé à rien est présenté comme une interprétation (D-41).** L'intérêt pratique de l'indice pour un joueur n'est pas asséné : la page écrit « l'indice de recherche n'est pas une qualité en combat » et rattache chaque mode de compatibilité à sa provenance, jamais l'inverse.
- **Les heuristiques de classe existent et sont dites comme telles (ÉCR-3).** Le contrôle exige le commentaire du code à côté de la tournure « préférences de style de jeu » : le module ne prétend ni qu'elles simulent les sorts, ni qu'elles n'existent pas.
- **RF-1 gardé, résidu écrit dans le contrôle.** L'exemption par la valeur de `COLS` reste telle que le plan la décrit (retrait des occurrences en mot entier, exemption non élargie) et le constat de valeur volatile énonce la règle complète, y compris sa fragilité possible si une prose citait légitimement un nombre égal à cette valeur dans cette seule section.
- **La morsure d'une règle scopée à un titre peut la rendre inopérante** (mesure de la tâche 2) : la règle scopée reste, et une garde non scopée la complète — la section reste exigée par son titre, mais un titre dérivé ne peut plus faire disparaître le contrôle des nombres volatiles.
- **La ligne de retour et les renvois sans lien sont contrôlés sur la page entière** (D-01, D-44) : les cibles `wizard-avance.md` et `base-locale.md` n'existent pas encore, un lien serait une cible morte, et le contrôle de clôture refuse toute occurrence de `](http` (lien externe).
- **Le harnais reste sûr.** Le module n'importe ni `webbrowser` ni `sqlite3` (garde `ast` de 03-01, toujours verte), ne poste jamais `DB` (garde de 03-03), ne lance le solveur que sur la base de la fixture, et lit `.data/` uniquement pour en prendre une empreinte.
- **RF-2 est traité, pas enregistré comme omission** (première branche de `03-REVIEW-FIX.md`) : la page cite l'en-tête rendu, le contrôle le relit par `_entete` et exige le code de programme **comme mot entier** — mesure : un `pgm` dérivé en `OPT-SIMPL` rougit au lieu d'être satisfait par la citation de `OPT-SIMPLE`.

## Deviations from Plan

### Auto-fixed Issues

1. **La morsure `chiffre_volatile` du plan renomme le titre de la section (mesuré, pas supposé).** La commande `sed` du plan écrit `## Ce que l.outil ne fait pas` en remplacement : dans le remplacement, le point est littéral, donc la copie mutée porte un titre dérivé (`## Ce que l.outil ne fait pas`) **en plus** du nombre injecté. Conséquence mesurée : le contrôle scopé à la section perd son objet (le helper partagé lève « section introuvable ») et le nombre injecté n'était jamais nommé — la morsure rapportait « MUTATION NON DETECTEE : motif `1219` absent de la sortie ».
   **Correction, dans le module uniquement (la commande du plan n'a pas été modifiée) :** une section introuvable reste un **constat** (précédent de 03-01, tâche 1), les vérifications scopées sont sautées, et une **garde non scopée** reste armée — aucun nombre de quatre chiffres ou plus où que ce soit dans la page (les chiffres de catalogue mesurés sont des milliers ; mesure : la page n'en porte aucun aujourd'hui). La morsure est discriminante après correction (motif `1219` présent) et les quatre morsures de la tâche 2 passent 4/4.
2. **Chemins MSYS et interpréteur Windows dans les batteries du plan (mesuré).** Deux commandes de vérification passent un chemin `$(mktemp -d)` a l'interpréteur Windows en argument (`lf_converti` en tâche 3, démonstration de discrimination) : `$T/...` est un chemin MSYS que Python résout en `\tmp\...` et la mutation échoue (`FileNotFoundError`) ou n'atteint pas le fichier. Aucune correction de code : les batteries ont été rejouées en passant le chemin Windows (`cd "$T" && pwd -W`). Le `cd` de bash, lui, traduit correctement — c'est pourquoi les morsures `sed` fonctionnent sans adaptation.
3. **RF-2 exécuté (décision de `03-REVIEW-FIX.md`, pas une règle 1-4).** La page cite l'en-tête rendu des trois écrans de questions et un nouveau test le relit par `_entete`, en exigeant le code comme mot entier ; deux morsures supplémentaires ont été mesurées sur ce contrôle.
4. **Le test d'empreinte compare les diagnostics sur les pages concaténées.** La signature du plan (`app` seul) est conservée : la comparaison est brute (les accents des lignes du corps sont rendus tels quels, seule la charge utile `data-stuff-payload` les échappe — patron de `test_pagination_et_emplacement_du_calcul`), et les pages du résultat sont lues de 1 à `total` parce que les diagnostics tombent en fin de résultat (mesuré : la première page ne les porte pas). Aucune fixture de normalisation n'a été ajoutée.
5. **SIMP-01 restait `Pending` dans `REQUIREMENTS.md`** alors que `03-01-SUMMARY.md` déclare `requirements-completed: [SIMP-01]` et que la tâche 3 de ce plan exige la cohérence de la traçabilité à la clôture : la case et la ligne de traçabilité ont été mises à `Complete`, **preuve** citée (`git show 55ec185 --stat` : ce commit de clôture n'a pas touché `REQUIREMENTS.md`, alors que ceux de 03-02 et 03-03 l'ont fait). Aucun autre contenu de `REQUIREMENTS.md` n'a été modifié.

### Non-deviations worth recording

- **RF-1 : la forme est gardée volontairement.** L'exemption par la valeur de `COLS` n'a pas été élargie et n'exempte aucun autre nombre ; sa fragilité résiduelle est écrite dans le message du contrôle et dans une décision de ce SUMMARY, comme le demande la cible de `03-REVIEW-FIX.md`.
- **Les neuf titres épinglés par le plan sont ceux de la page (mesuré) :** `## Question 2/3 : les éléments` (et non « les questions »), dans cet ordre exact, `## Source de vérité` en dernier.
- **La démonstration de discrimination de la tâche 3 est la commande du plan, adaptée au chemin Windows** (point 2 ci-dessus) ; la lecture finale y compare les deux premières composantes de l'empreinte du dépôt, sans y écrire.
- **Les fichiers de travail de l'exécution** (`.gsd-tmp/plan-p3/*.py`) ne sont pas suivis par git et n'ont pas été indexés : aucun `git add .` n'a été employé, chaque commit a listé ses chemins explicitement.

## Issues Encountered

- **Le titre de la section est le point faible d'une règle scopée** (écart 1) : la leçon est enregistrée en décision et appliquée — la règle scopée reste exigée par le titre, la garde non scopée est ce qui survit à sa disparition.
- **Un nombre légitime à trois chiffres existe ailleurs dans la page** (`995` dans `## Ce que l'outil suppose`) : une garde non scopée sur `\d{3,}` aurait donc produit un faux rouge ; c'est ce qui a motivé la borne à quatre chiffres, mesurée (0 nombre à quatre chiffres dans la page avant et après la tâche 3).
- **Ordre des sections et comptage des couples :** la page ajoutée ne porte aucun motif `numero. Libelle`, le comptage des 23 couples de la vague 1 reste exact (mesure : la suite complète est verte, le contrôle des couples compris).
- **Fins de ligne :** les deux fichiers modifiés sont restés 100 % CRLF, UTF-8 sans BOM après chaque écriture (mesure octet par octet) ; les mutations `sed` des batteries réécrivent la **copie** en LF, ce qui est sans effet sur l'arbre livré (mesure : la page du dépôt reste 269 CRLF pour 269 fins de ligne après les onze morsures).
- Aucun blocage : ce plan n'exige ni geste humain, ni secret, ni accès réseau, ni synchronisation Dofusdude. Aucune commande destructive n'a été approchée (ni `db clear`, ni drop, ni suppression sous `.data/`).

## Known Stubs

None — aucun stub, aucun `TODO`, aucun test en `skip` **sur l'arbre du dépôt** (les `skip` observés pendant les batteries venaient des copies temporaires, qui ne contiennent pas `.data/` : le test d'empreinte y saute en le disant, ce qui est son comportement nommé). Les cinq blocs `<automated>` du plan ont été exécutés, plus la mesure d'empreinte autour de la suite entière et la démonstration de discrimination.

## Threat Flags

Aucune surface nouvelle : ce plan n'ajoute ni endpoint, ni route, ni dépendance, ni secret ; il étend une page `docs/` et un module de test qui lisent le dépôt, rendent des écrans en processus sur la base de la fixture et lisent `.data/` **en lecture seule** pour en prendre une empreinte. Les menaces du `<threat_model>` sont couvertes : **T-17** (aucune écriture sous `.data/` : la morsure de la mesure est démontrée sur une copie temporaire, la référence du dépôt restant `24989696` / `1788730056843137500`), **T-18** (le rendu réel a lieu entre les deux empreintes de la mesure locale et la mesure large encadre la suite entière — la seconde empreinte n'est jamais prise à vide ; la base absente produit un `skip` nommé), **T-19** (chaque limite est adossée à un fichier cité ; l'intérêt de l'indice pour un joueur reste une lecture annoncée comme telle), **T-20** (aucun nombre de trois chiffres ou plus dans la section des limites hors la valeur de `COLS`, mesuré, et le message nomme la valeur trouvée), **T-21** (octets lus en binaire : BOM refusé, égalité `\r\n` ↔ `\n` exigée, la morsure `lf_converti` rougit en nommant `CRLF`).

## Next Phase Readiness

- **Phase 3 close par l'exécution** : la page porte ses neuf sections dans l'ordre, la suite est verte à **186 tests**, `.data/dofus.sqlite3` est intacte de part et d'autre de la suite entière. `03-VALIDATION.md` reste à mettre à jour par `/gsd:validate-phase`, pas par cet exécuteur ; `/gsd:verify-work` rejouera la suite, la mesure `.data/` et les critères 1 à 5.
- **Contraintes transmises aux phases suivantes** : la page est désormais **figée dans sa forme** par `test_page_complete_et_sans_derive` (toute section ajoutée, renommée ou déplacée rougit et doit être déclarée dans `TITRES_PAGE`) ; la section des limites n'accepte aucun nombre à quatre chiffres ou plus ; les renvois vers `wizard-avance.md` et `base-locale.md` devront passer en lien **dans la phase qui crée ces pages** (D-44), et la phase 4 est celle qui les crée.
- **Ce qui reste ouvert et assumé hors périmètre** : les écarts RF-3 (marqueur `(RESOLVED)` manquant dans `03-RESEARCH.md`), RF-4 (durées de la porte de validation non reproductibles), RF-5 (`03-PATTERNS.md:629`) et RF-6 (`.gsd-tmp/` non ignoré) sont des écarts d'artefacts de planification, hors du périmètre de ce plan d'exécution, et restent enregistrés dans `03-REVIEW-FIX.md`.
- **Aucun blocage.** Aucune action humaine n'est requise pour ce plan ; rien de ce qu'il livre ne dépend d'un geste physique, d'un secret ou du réseau.

## Self-Check: PASSED

- `docs/parcours-simplifie.md` : FOUND (269 lignes, 269 CRLF, UTF-8 sans BOM, neuf sections de niveau 2 dans l'ordre du plan, `## Ce que l'outil ne fait pas` avant `## Source de vérité`, derniere ligne `[Retour au sommaire](sommaire.md)`)
- `tests/test_docs_parcours.py` : FOUND (2 734 lignes, 2 734 CRLF, UTF-8 sans BOM, 17 tests verts dans le module)
- Commit `7a537f7` : FOUND — feat(03-04) prouve par balayage les hypotheses de l'outil et les cite dans la page
- Commit `c945037` : FOUND — feat(03-04) adosse les limites de l'outil au code dans la page
- Commit `7561940` : FOUND — feat(03-04) ferme la page (neuf sections, CRLF) et encadre la base locale
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_parcours.py -q` : 17 passed
- `./.venv/Scripts/python.exe -m pytest -q` : 186 passed (181 avant ce plan)
- Morsures du plan : 11/11 detectees, copie verte verifiee avant chaque mutation (4 tache 1, 4 tache 2, 3 tache 3)
- Morsures du controle RF-2 ajoute : 2/2 detectees (page sans le code de programme ; `pgm` derive en `OPT-SIMPL`)
- `.data/dofus.sqlite3` : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique avant et apres la suite complete, et reference inchangee apres la demonstration sur copie
- Commits mesures : `git rev-list --count 33a877df769d8e5169db8bddfcfbc67c45fc2fca..HEAD` = 3

---

*Phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el*
*Completed: 2026-09-11*
