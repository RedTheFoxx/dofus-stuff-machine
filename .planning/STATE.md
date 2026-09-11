---
gsd_state_version: "1.0"
current_phase: 4
current_phase_name: Wizard avancé et résorption de la dette `GUIDE_WIZARD`
status: executing
stopped_at: Completed 04-01-PLAN.md
last_updated: "2026-09-11T18:52:44.289Z"
last_activity: 2026-09-11
last_activity_desc: Plan 04-01 terminé — page du wizard avancé, entrée d'index et module d'ancrage (194 tests verts)
state_head: e4214703ff79e27767984077276202cc4e257c20
progress:
  total_phases: 6
  completed_phases: 3
  total_plans: 15
  completed_plans: 12
  percent: 50
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-10)

**Core value:** Un utilisateur qui n'a jamais vu le projet peut installer l'outil, lancer le flux simplifié classe → éléments → niveau, lire son résultat et retrouver chaque commande/menu cité dans le code réel — sans lire le code et sans rencontrer de documentation périmée.
**Current focus:** Phase 4 — Wizard avancé et résorption de la dette `GUIDE_WIZARD`

## Current Position

Phase: 4 (Wizard avancé et résorption de la dette `GUIDE_WIZARD`) — EXECUTING
Plan: 2 of 4
Status: Ready to execute
Last activity: 2026-09-11 — Plan 04-01 terminé (page du wizard avancé, entrée d'index, module d'ancrage)

Progress: [█████░░░░░] 50%

## Performance Metrics

**Velocity:**

- Total plans completed: 12
- Average duration: -
- Total execution time: -

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 | 4 | - | - |
| 2 | 3 | - | - |
| 3 | 4 | - | - |
| 4 | 1 | 4 | - |

**Recent Trend:**

- Last 5 plans: -
- Trend: -

*Updated after each plan completion*
**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 01 P01 | 2min | 2 tasks | 5 files |
| Phase 1 P02 | 4min | 2 tasks | 2 files |
| Phase 01 P03 | 3min | 2 tasks | 1 files |
| Phase 1 P04 | 2 min | 2 tasks | 1 files |
| Phase 2 P01 | 3min | 3 tasks | 2 files |
| Phase 2 P02 | 7min | 2 tasks | 3 files |
| Phase 2 P03 | 5min | 2 tasks | 2 files |
| Phase 3 P01 | 7min | 3 tasks | 4 files |
| Phase 03 P02 | 6min | 2 tasks | 2 files |
| Phase 03 P03 | 4min | 2 tasks | 2 files |
| Phase 03 P04 | 17 min | 3 tasks | 2 files |
| Phase 4 P01 | 10min | 3 tasks | 3 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Roadmap]: Périmètre strictement documentaire sur un produit figé — aucune phase ne touche `dofus_stuff/**`, aucune resynchronisation Dofusdude n'est planifiée, `.data/` reste en lecture seule.
- [Roadmap]: Le harnais pytest est posé en phase 1, mais la liste épinglée des 8 pages n'arrive qu'en phase 6 (dernière phase) — une suite rouge pendant cinq phases perdrait sa valeur de signal.
- [Roadmap]: Le contrôle des renvois obsolètes doit être vu rouge sur l'état antérieur puis vert dans la phase 4, qui résorbe la dette `GUIDE_WIZARD.md` (source unique du flux avancé).
- [Roadmap]: `**UI hint**: no` explicite sur les 6 phases : la prose documentaire contient « interface » et « page », que les outils prendraient sinon pour un chantier frontend.
- [Phase 1]: Sommaire sans cible hors index : aucune ligne de retour vers ../README.md, aucun lien dans l'introduction ni dans le parcours conseille, pour que l'egalite d'ensembles sommaire <-> docs/**/*.md reste un vrai signal (SOMM-02, D-05, D-06)
- [Phase 1]: Parcours conseille des sept themes en texte numerote simple, sans lien markdown : une cible absente ferait rougir problemes_index sans liste blanche possible (D-04)
- [Phase 1]: Imports ajoutes en tete de tests/conftest.py, fixtures docs_dir/normalize et helper _normalize en fin de fichier ; fixtures existantes byte-identiques (25 insertions, 0 suppression)
- [Phase 1]: [Phase 1]: Le seul contact CLI enseigne par docs/installation.md est hors-ligne (python fetcher.py --offline db status) ; la synchronisation (db sync) n'est nommee qu'en prose, jamais en commande, pour qu'aucune lecture de la page ne declenche de resynchronisation Dofusdude (T-01-06)
- [Phase 1]: [Phase 1]: La forme fautive d'ordre des options (db status --offline) est citee en prose entre accents graves, jamais en ligne de commande : le controle d'ancrage du plan 01-04 analyse les blocs de code et exige une commande analysable et hors-ligne
- [Phase 1]: [Phase 1]: Les deux nouvelles gardes de docs/installation.md (ordre clavier avant lancement, absence de jeton destructeur) portent sur cette seule page : un controle d'absence de db clear sur tout docs/** ferait echouer la phase 2, qui doit au contraire avertir sur db clear dans cli.md (T-01-05)
- [Phase 1]: [Phase 1]: Le test de mutation verifie l'etat sain (problemes_liens, problemes_index, problemes_h1 tous vides) avant toute injection : une derive preexistante fait echouer le test en le disant, au lieu de prouver une detection sur un etat deja faux
- [Phase 1]: [Phase 1]: Chaque derive injectee doit etre nommee dans le message de l'invariant qui la refuse (any(cible injectee in probleme ...)) : un harnais casse pour une autre raison ne peut pas faire passer le test de mutation (critere de succes 5)
- [Phase 1]: [Phase 1]: Les quatre helpers de gabarit (pages_listees, problemes_h1, problemes_retour_sommaire, problemes_encodage) restent des fonctions pures parametrees par docs_dir, donc executables contre l'arbre livre et contre une copie tmp_path sans dupliquer la logique
- [Phase 1]: tests/test_docs_code_anchor.py ancré sur le produit : chemins source, commandes fetcher.py hors-ligne, adresse derivee du parseur, options web verifiees des deux cotes, libelles ancres sur la ligne porteuse
- [Phase 2]: [Phase 2]: docs/cli.md suit le gabarit de la phase 1 (H1 unique, phrase d'introduction, sections courtes, bloc Source de verite accentue, ligne de retour) ; Options globales precede ## version pour que la mutation option inventee de 02-02 tombe dans le perimetre de la garde non vide, et Source de verite reste la derniere section avant la ligne de retour
- [Phase 2]: [Phase 2]: Le mode interactif (python fetcher.py --offline optimize) est decrit en prose et dans aucun bloc console : le temoin marque de l'ordre global-avant-sous-commande reste unique (--offline optimize --demo) et la mutation d'ordre de 02-03 t1 garde son motif
- [Phase 2]: [Phase 2]: Les trois descriptions verbatim de l'aide (Afficher l'état de la base, Forcer la synchronisation complète, Vider la base locale) sont citees une seule fois, dans ## db ; ## cache declare l'alias et renvoie a cette section sans en reprendre aucune (D-20) ; db sync et cache fill reecrivent la base et exigent le reseau mais ne portent pas le jeton destructeur (classement A2)
- [Phase 2]: [Phase 2]: La regle de docs/installation.md « toutes les commandes portent --offline » n'est pas reconduite sur la page CLI (mesure M5 : --offline db sync sort en code 1) ; le renvoi vers la future page base-locale est fait en prose sans lien markdown, pour ne pas creer de cible morte sous problemes_liens
- [Phase 2]: Scanner de blocs et helpers de section deplaces (jamais recopies) dans tests/conftest.py, exposes par les fixtures lignes_de_code, sections et section ; _section(texte, titre, page) exige la page et un appel sans page leve TypeError (D-12, D-13, D-31)
- [Phase 2]: Section « ## cache » : controle d'alias sur les marqueurs normalises alias / second nom / equivaut, la page livree declarant l'equivalence sans le mot « alias » ; la page n'a pas ete modifiee pour faire passer un test
- [Phase 2]: Espace de noms d'alias lu en deux vues : brute pour exiger command == db ou cache, privee de command pour comparer l'alias — une vue unique aurait fait rougir un constat sur une page correcte
- [Phase 2]: Un seul point d'assertion par test (constats cumules) : avec une assertion par constat, les motifs --candidats-top et « aucune option » seraient inatteignables et la batterie rapporterait MUTATION NON DETECTEE sur une implementation correcte
- [Phase 2]: Morsure de la mutation « build_parser() retire » re-mesuree sur une copie incluant l'arbre produit (verte avant mutation, rouge apres) : la copie « sans » est rouge par construction et cite deja le jeton
- [Phase 2]: Options citees extraites des seules lignes de tableau des sections Options globales et optimize, jamais du texte entier : la section optimize cite --offline, option globale refusee par le sous-parseur optimize (Pitfall 10)
- [Phase 2]: [Phase 2]: Exemples marques de docs/cli.md extraits par la projection lignes_exemple du scanner unique, decoupes par shlex.split puis acceptes par build_parser().parse_args : la commande est analysee, jamais executee (CLI-03, D-24, D-25)
- [Phase 2]: [Phase 2]: Garde destructrice evaluee ligne a ligne sur le texte entier de la page (jamais par section, lecon WR-02) avec un motif (db|cache) + espaces + clear (lecon WR-01) ; ses trois constats sont joints a une seule assertion, mesure a l'appui : une assertion par constat rapportait la mutation « mention destructrice glissee dans un bloc d'exemple » non detectee sur une page correcte
- [Phase 2]: [Phase 2]: Le nom de sous-commande d'un exemple est projete comme premier jeton positionnel (options globales et leur valeur sautees) avant comparaison aux huit noms epingles : le constat « atteinte sans etre documentee » reste atteignable au lieu d'etre une branche morte infalsifiable (T-02-14) ; sur la page livree le resultat est identique au filtre du plan
- [Phase 2]: Revue de code de la phase 2 : les 5 constats Warning sont appliques au harnais d'ancrage CLI seulement (tests/test_docs_cli.py, tests/conftest.py) — la page docs/cli.md et dofus_stuff/** restent inchanges, les tests ne sont pas adoucis pour faire passer la page : WR-01 (colonne « Defaut » des 37 lignes de tableau lue et comparee au parseur, bijection ligne <-> sonde, aucune ligne ni sautee ni inventee), WR-02 (motif reseau reserve a la seule regle « jamais une commande a recopier »), WR-03 (`--help` n'est plus declare « refuse par le parseur »), WR-04 (presence des trois descriptions dans « ## db » et sections de niveau 2 exigees dans l'ordre du parseur), WR-05 (appartenance stricte des jetons aux aides publiques).
- [Phase 2]: WR-02 separe deux regles au lieu d'etendre un motif : `JETONS_RESEAU` ((db|cache) + (clear|sync|fill)) ne sert qu'au constat « exemple marque citant une commande qui vide ou reecrit la base » ; les regles de presence et de co-presence de l'avertissement gardent le motif `clear` seul, car la ligne 168 de la page cite `db sync` et `cache fill` sans le mot « destruct » — les etendre aurait rendu la page livree faussement rouge (D-22 vs D-23).
- [Phase 2]: WR-05 corrige une justification fausse ecrite dans le module : la forme stricte d'un jeton n'exige aucune introspection privee d'argparse (D-14), l'ensemble des options declarees s'obtient par `format_help()` du parseur racine et par l'aide capturee de chaque sous-commande epinglee. La sonde `parse_args` garde son role (« les exemples et les tableaux sont analysables ») mais ne prouve plus la forme : mesure de discrimination, un renommage cote parseur (--force-sync -> --force-synchronisation, --top-k -> --top-k-slot) laisse le test de sonde seul vert alors que le controle d'appartenance stricte rougit en nommant les deux jetons perimes.
- [Phase 2]: Valeurs d'essai des defauts mesurees par difference des deux espaces de noms du parseur (jamais par introspection privee) ; la valeur d'essai de `--jet` differe de sa valeur epinglee (`min` au lieu de `average`), la sonde de defaut ayant besoin d'une valeur qui ne soit pas le defaut lui-meme.
- [Phase 2]: Mesures de la passe qualite : `.venv/Scripts/python.exe -m pytest -q` -> 169 passed (168 + le nouveau test des tableaux) ; les 19 mutations des batteries de 02-02 et 02-03 rapportent toutes « mutation detectee » avec leurs blocs a l'exit 0 ; les cinq falsifications de defaut, l'exemple marque `python fetcher.py --offline db sync` et la suppression de la table de « ## db » passent au rouge, l'exemple `python fetcher.py --help` reste vert ; `docs/`, `dofus_stuff/` et `.data/` inchanges (horodatage de `.data/dofus.sqlite3` identique).

- [Phase 3 03-01]: La page docs/parcours-simplifie.md est derivee du rendu reel (client de test Flask en processus) : les trois premieres sections (question 1 classe, question 2 elements, question 3 niveau), la sous-section « Passer aux reglages detailles », le bloc Source de verite (huit chemins) et la ligne de retour sont en place ; les quatre sections de 03-02 a 03-04 s'inserent AVANT Source de verite, la ligne de retour restant la derniere ligne.
- [Phase 3 03-01]: Le module tests/test_docs_parcours.py porte les helpers reutilisables (_lignes_du_corps, _statut, _touches, _libelle_saisie, _client_etape, _couples_du_rendu, _couples_de_section), la table epinglee ENTREES_MESUREES (25 entrees) et les constantes de titres TITRE_RESULTAT / TITRE_SAUVEGARDE / TITRE_SUPPOSE / TITRE_LIMITES : 03-02 a 03-04 n'ont plus qu'a les consommer.
- [Phase 3 03-01]: Etat de session par etape ecrit sous `recommendation_input`, la cle lue par dofus_stuff/web/routes.py:940 : la « simplification » consistant a ecrire classe/elements a la racine de la session fait repondre 302 -> /optimize a TOUS les POST d'elements et de niveau, ce qui rendrait faux chacun des verdicts epingles (D-32).
- [Phase 3 03-01]: La comparaison des couples numero <-> libelle est scopee par section : les menus des classes (1-19) et des elements (1-4) partagent les numeros 1 a 4, un dictionnaire global rapporterait quatre constats sur une page correcte (Pitfall 1 de la recherche, mesure).
- [Phase 3 03-01]: Garde statique ancree sur le risque reel (sqlite3, subprocess, socket, multiprocessing, ctypes, webbrowser, http/urllib/requests, import de dofus_stuff.database, appel a main, suppression de fichier), repetee sur la cloture transitive des imports produit — mesuree a 5 modules atteints depuis dofus_stuff.optimize.recommend, aucun interdit. Pas de liste blanche de modules : un import public pur ajoute plus tard passe sans revision, un import qui tirerait la base rougit ; un import produit non resolu est un echec nomme et la cloture doit compter au moins 3 modules (T-03-03).
- [Phase 3 03-01]: Le controle des couples ne se contente pas des numeros distincts : `sum(len(libelles))` exige 23 occurrences (19 classes + 4 elements), faute de quoi un second exemplaire (table recapitulative des 19 classes) ne serait pas detecte — la preservation dict[numero] -> list[libelles] etant necessaire a la comparaison par section.
- [Phase 3 03-01]: Commits locaux sur main : la garde de branche protegee a ete levee par la cle d'override prevue par le protocole lui-meme (`git.allow_default_branch_commits: true` dans .planning/config.json, deux lignes de diff), coherente avec `git.branching_strategy = none` et les phases 1 et 2 livrees sur main ; aucun commit n'est passe par --no-verify.
- [Phase 3 03-01]: Mesures de la passe de tache : `.venv/Scripts/python.exe -m pytest -q` -> 176 passed (169 avant la phase + 7) ; les trois batteries de morsures (1 pour t1, 1 pour t2, 5 pour t3) rapportent toutes « mutation detectee » sur une copie verte verifiee avant mutation ; .data/dofus.sqlite3 identique (24 989 696 octets, mtime_ns 1788730056843137500) ; aucun ecart de perimetre.
- [Phase 3]: [Phase 3 03-02]: La carte de pagination est lue dans la ligne de statut du resultat rendu (PAGE 1/<total>) et confrontee aux attributs data-body-page/data-body-total de la coquille : la coherence statut <-> attributs est exigee, mais aucun total de pages n'est epingle (il depend du catalogue : 3 pages sur la fixture, 6 puis 7 sur la base reelle).
- [Phase 3]: [Phase 3 03-02]: La position des diagnostics est exigee sur les pages CONCATENEES du resultat, apres le dernier « Équipement : » et avant « Greedy: », la phrase du catalogue devant suivre immediatement le dernier diagnostic : aucune comparaison entre un numero de page et le total n'existe dans le module (reformulation enregistree ECR-2).
- [Phase 3]: [Phase 3 03-02]: La page ecrit « en fin de resultat — jusqu'a PAGE n/n » et non « derniere page » (tournure controlee absente, comparaison apres normalisation) ; les quatre motifs de valeur volatile (Score : \d, Indice de recherche : \d, Greedy: \d, Methode : [a-z]) sont controles absents de la section.
- [Phase 3]: [Phase 3 03-02]: Les libelles de la table viennent d'une extraction ast de display_slots (jamais d'une liste ecrite de memoire) ; SLOTS_MESURE porte pour chaque libelle une aiguille de ligne et le nom complet recopie de sa source (commentaires de _GROUP_SLOTS pour les seize emplacements exportes, solver_spec pour prysma), re-verifie sur la ligne qui les porte.
- [Phase 3]: [Phase 3 03-02]: Aucune troncature n'est promise ni assertee : la section « Correspondance des libelles » ne contient ni « libelle tronque » ni le caractere de points de suspension, et le module n'asserte nulle part ce caractere sur un rendu (reformulation enregistree ECR-1, mesure M7 : 0 ligne rendue du resultat n'en porte).
- [Phase 3]: [Phase 3 03-02]: Le resultat est rendu une seule fois par le solveur dans ce plan (fixture minimale deterministe : niveau 200, quatre elements -> 3 pages, diagnostics en page 2/3 ; module a 0,8 s) et le module reutilise _touches sans le redefinir (D-12).
- [Phase 3]: [Phase 3 03-02]: Mesures de la passe de tache : .venv/Scripts/python.exe -m pytest -q -> 177 passed apres la tache 1 puis 178 passed apres la tache 2 ; les deux batteries de morsures (2 pour t1, 4 pour t2) rapportent toutes « mutation detectee » sur une copie verte verifiee avant mutation ; .data/dofus.sqlite3 identique (24 989 696 octets, mtime_ns 1788730056843137500).
- [Phase 3]: [Phase 3 03-03]: La limite de sauvegarde du navigateur est ancree sur les litteraux du fichier JS (cle `dofus-stuff-machine.saves` et valeur de `MAX_SAVES` extraites a chaque execution par `_litteral_js`, motifs epingles sur terminal.js:14-15) : la page doit citer la valeur courante, donc passer `MAX_SAVES` a 50 rougit sans que la page change (D-42). Le controle est nomme comme un controle de LITTERAUX dans le docstring du module et dans le constat lui-meme : aucun moteur JS n'existe ici (ni `localStorage`, ni `shift`), l'eviction reelle reste non testee et le module ne pretend pas le contraire (T-13).
- [Phase 3]: [Phase 3 03-03]: L'eviction est dite honnetement (ECR-5, D-41) : la section porte « les plus anciennes sont remplacees » et l'assertion refuse la tournure « 20 maximum » seule, exacte mais trompeuse puisque la sauvegarde en trop remplace la plus ancienne sans message d'echec (terminal.js:294-318) ; les libelles `DB DOFUSBOOK`, `BACK LISTE` et `SAUVEGARDES PURGEES` sont exiges dans la page ET sur la ligne du fichier JS qui les porte (patron LIBELLES_SOURCE de tests/test_docs_code_anchor.py:61-74).
- [Phase 3]: [Phase 3 03-03]: L'export est prouve par la surface publique pure `build_dofusbook_url` : 17 emplacements fournis (les seize exportes plus la `prysma`), charge utile decodee de forme [caracs(51), points(51), niveau, flags, counts(10), ids], `sum(counts) == 16` et identifiant 999 absent des `ids`. L'ordre des dix groupes n'est PAS re-teste car deja prouve par tests/test_web.py:713-750 (D-12, cite en commentaire) ; le nombre cite par la page est celui du calcul, jamais un 16 ecrit de memoire, et l'URL d'import est lue sur l'attribut public du module par `importlib` puis exigee entre accents graves (D-01, adresse technique et non lien externe).
- [Phase 3]: [Phase 3 03-03]: Le rendu du resultat est obtenu sans poster la saisie `DB` (injection de `optimize_result_lines` dans la session, patron de tests/test_web.py:668-671) et le module porte sa propre garde `ast` (`test_aucun_post_db_sans_patch`) interdisant tout import de `webbrowser` et tout appel dont l'argument nomme `data` porte un dictionnaire litteral `cmd=DB` : la suite ne peut pas lancer de navigateur (T-12), et le comportement reste couvert, patche, par tests/test_web.py:668. Le motif de morsure est porte par une constante du module (`MOTIF_EMPREINTE_EXPORT`) et jamais ecrit en clair dans la ligne d'assertion : pytest reproduit la ligne source du `assert` dans sa sortie, un motif en clair y serait trouve meme sans qu'aucun constat soit produit.
- [Phase 3]: [Phase 3 03-03]: Mesures de la passe de tache : `.venv/Scripts/python.exe -m pytest -q` -> 181 passed (178 avant ce plan) ; les six morsures des deux batteries (2 pour t1, 4 pour t2) rapportent toutes « mutation detectee » sur une copie verte verifiee avant mutation, et la batterie de t1 a ete rejouee apres t2 (toujours 2/2) ; sur la mutation de l'export la sortie montre des constats reels (« 17 pour 17 emplacements fournis ; attendu 16 », identifiant 999 present) et non un echo de ligne source ; .data/dofus.sqlite3 identique (24 989 696 octets, mtime_ns 1788730056843137500) ; le module de test passe a 12 tests.
- [Phase 3]: [Phase 3 03-04]: Les hypotheses de loutil sont MESUREES par balayage sur la surface publique pure (capital 5 * (niveau - 1), cibles PA/PM aux niveaux de bordure 39/40, 99/100, 149/150, 200), les quatre ensembles de classes sont extraits par ast et le nombre de classes sans objectif (9) est calcule : deplacer un seuil ou retirer une classe rougit sans que la page change (D-42). Les heuristiques de classe sont presentees comme telles, avec le commentaire du code exige a cote de la tournure « preferences de style de jeu » (ECR-3). — docs/parcours-simplifie.md, tests/test_docs_parcours.py, plan 03-04 taches 1 et 2 ; mesure : 186 passed apres le plan, morsures 4/4 en tache 1 et 4/4 en tache 2
- [Phase 3]: [Phase 3 03-04]: La section des limites est adossee au code (modes de compatibilite de score.py, filtre de plausibilite de candidates.py, profondeur top_k=40, coupe url[:COLS] de routes.py:1336) et ne cite aucun nombre de trois chiffres ou plus hors la valeur de COLS lue dans screens.py:5 ; une morsure mesuree a montre quun titre derive rend la regle scopee inoperante, d ou une garde NON scopee conservee a cote (aucun nombre de quatre chiffres ou plus dans la page). RF-2 est traite : la page cite len-tete rendu (OPT-SIMPLE / RECOMMANDATION DE STUFF) et un controle le relit par _entete, le code exige comme mot entier. — mesure : morsure chiffre_volatile (le sed du plan renomme le titre) et deux morsures RF-2 (page sans OPT-SIMPLE, pgm derive en OPT-SIMPL) ; 0 nombre a quatre chiffres dans la page
- [Phase 3]: [Phase 3 03-04]: La page est close sur ses neuf sections (CRLF sans BOM, un seul H1, ligne de retour, aucun bloc console, aucun lien externe ni vers wizard-avance.md / base-locale.md) et lempreinte de .data/dofus.sqlite3 (taille, mtime_ns, sha256) est identique avant et apres la suite ENTIERE : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b. La re-mesure locale du module est nommee pour ce quelle mesure (conftest construit sa base sous tmp_path, donc elle ne peut pas detecter une ecriture dun autre module) et la morsure de la mesure est demontree sur une COPIE temporaire, jamais sur .data/ (T-17, T-18). — mesure : 186 passed, 11/11 morsures du plan + 2/2 RF-2, base du depot reference 24989696 / 1788730056843137500 inchangee
- [Phase 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard]: Le compte des listes documentees est lu au rendu, jamais dans une table locale : les 11 options du solveur sont extraites du corps de GET /optimize/wizard/options et comparees une a une a ce que la page cite, et les 11 emplacements et 10 filtres sont lus sur les deux pages de GET /optimize/wizard/slots. — La liste des options n'expose aucune constante publique (body_options ecrit onze lignes litterales, la table d'application est locale a apply_options_input) : le rendu est le seul ancrage honnete du compte, et il prouve que la page et l'ecran ne divergent pas sans pretendre a une constante de comptage.
- [Phase 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard]: Les deux formes d'edition des quatre nombres ne sont jamais fusionnees : FORMAT : BASE POINTS CIBLE POIDS est cite avec l'ecran des caracteristiques et FORMAT : BASE EXO CIBLE POIDS avec PA / PM / PO, chacun lu sur le sous-ecran d'edition reellement atteint par le rendu, et le refus de format est le message de la forme affichee juste au-dessus. — Une page qui melange les deux formes fait apprendre au lecteur un format que l'ecran n'affiche pas ; le controle atteint les deux sous-ecrans et exige que les deux formes marquees restent distinctes, si bien qu'une permutation des deux litteraux rougit la suite avec le litteral rendu dans le constat.

### Pending Todos

None yet.

### Blockers/Concerns

- Vérification obligatoire par `.venv/Scripts/python.exe -m pytest -q` : l'interpréteur ambiant de l'hôte n'a pas pytest (`No module named pytest`) — aucun résultat de test ne peut être cité sans exécution réelle par cet interpréteur.
- Outillage documentaire antérieur inactif (`doc-agent.toml`, `.doc-agent/`) ciblant `docs/` : ne jamais le lancer, ne rien supprimer, ne jamais utiliser `git add .` depuis la racine.

## Deferred Items

Items acknowledged and deferred at milestone close, most recent first:

| Category | Item | Status | Deferred At | Milestone |
|----------|------|--------|-------------|-----------|
| *(none)* | | | | |

## Session Continuity

Last session: 2026-09-11T18:52:44.246Z
Stopped at: Completed 04-01-PLAN.md
Resume file: None
