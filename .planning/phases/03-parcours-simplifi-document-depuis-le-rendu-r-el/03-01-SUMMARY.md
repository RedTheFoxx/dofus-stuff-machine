---
phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
plan: 01
subsystem: documentation
tags: [markdown, pytest, flask-test-client, ast, crlf, documentation-francaise]

# Dependency graph
requires:
  - phase: 02-r-f-rence-cli-align-e-sur-le-parseur
    provides: "harnais documentaire partage (tests/conftest.py : fixtures app/client/docs_dir/normalize/section), docs/cli.md proprietaire de la surface de commandes (D-37), suite verte a 169 tests"
provides:
  - "docs/parcours-simplifie.md : les trois premieres sections du parcours simplifie (classe -> elements -> niveau), derivees du rendu reel, avec tables d'entrees acceptees et refusees, bloc Source de verite et ligne de retour"
  - "une ligne d'index ajoutee dans docs/sommaire.md : exhaustivite bidirectionnelle verte sans exception (D-39, V14)"
  - "tests/test_docs_parcours.py : module d'ancrage a 7 tests (rendu des trois ecrans, entrees rejouees, couples numero <-> libelle par section, garde ast sans base ni execution)"
  - "reutilisable par 03-02 a 03-04 : _lignes_du_corps, _statut, _touches, _libelle_saisie, _client_etape, _couples_de_section, _couples_du_rendu, ENTREES_MESUREES, et les constantes de titres TITRE_RESULTAT / TITRE_SAUVEGARDE / TITRE_SUPPOSE / TITRE_LIMITES"
affects: [03-02, 03-03, 03-04]

actuals:
  tokens: 11887    # chars/4 sur le diff realise (47 548 caracteres ajoutes)
  tasks: 3
  commits: 3       # MESURE : git rev-list --count 8f437bd03d6a266cdd474151b8c504da87b35776..HEAD
  plan_head_before: 8f437bd03d6a266cdd474151b8c504da87b35776

tech-stack:
  added: []          # aucune dependance ajoutee (contrainte projet C1)
  patterns:
    - "Rendu Flask en processus via la fixture app : la page est derivee du rendu reel, jamais du code lu a l'oeil (D-32)"
    - "Extraction des lignes du corps et de la ligne de statut : seule source d'assertion d'un ecran, jamais la reponse HTTP entiere (Pitfall 2)"
    - "Couples numero <-> libelle compares section par section, jamais par un dictionnaire global (Pitfall 1)"
    - "Garde ast ancree sur le risque reel (base, processus, socket, reseau, suppression) avec cloture transitive des imports produit, et non sur une liste blanche de modules"
    - "Constat accumules joints a une seule assertion, message citant la page, l'attendu et le fichier de code (D-13)"

key-files:
  created:
    - docs/parcours-simplifie.md
    - tests/test_docs_parcours.py
  modified:
    - docs/sommaire.md
    - .planning/config.json

key-decisions:
  - "La tranche verticale est livree en tete de plan (tache 1, type tracer) : page, ligne d'index et module d'ancrage touches de bout en bout avant toute expansion."
  - "L'etat de session de chaque etape est ecrit sous `recommendation_input`, la cle lue par la vue (dofus_stuff/web/routes.py:940) : c'est la seule forme qui produit les verdicts mesures. Injecter les memes cles a la racine de la session fait repondre 302 -> /optimize a tous les POST d'elements et de niveau."
  - "La comparaison des couples est scopee par section : les menus des classes (1-19) et des elements (1-4) partagent les numeros 1 a 4, un dictionnaire global rapporte quatre constats sur une page correcte."
  - "La garde statique porte sur le risque reel (ouvrir la base, lancer un processus, ouvrir une socket, joindre le reseau, supprimer un fichier) et non sur une liste blanche de modules produit : un import public pur ajoute plus tard passe sans revision, un import qui tirerait la base rougit. Un import produit non resolu est un echec nomme, et la cloture doit compter au moins 3 modules atteints."
  - "`_client_etape` rend un client neuf par entree rejouee : un POST accepte reecrit l'etat de session et fausserait le verdict suivant."
  - "L'etape 3 acceptee est eprouvee avec le solveur court-circuite (patch de `_run_optimize_and_redirect`, patron de tests/test_recommend.py:75) : aucun solveur lance, module sous 0,35 s."

patterns-established:
  - "Pattern 1 : un module d'ancrage par page, helpers locaux au module, jamais de promotion vers tests/conftest.py quand un helper equivalent existe (D-12, M15)"
  - "Pattern 2 : une table epinglee de couples (etape, valeur, attendu) rejouee sur le rendu, verifiee dans les deux sens contre les tables de la page"
  - "Pattern 3 : sous-section de niveau 3 extraite localement (`### Entrees acceptees`, `### Erreurs et refus`), seules les cellules entre accents graves etant des valeurs"

requirements-completed: [SIMP-01]

coverage:
  - id: D1
    description: "docs/parcours-simplifie.md : les trois questions du parcours simplifie et la ligne `AVANCE : personnaliser les reglages` cites tels qu'ils sont rendus"
    requirement: "SIMP-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_trois_questions_et_avance_rendus"
        status: pass
    human_judgment: false
  - id: D2
    description: "Chaque entree citee par la page est acceptee ou refusee par le rendu, avec les trois messages de refus attendus au debut de la ligne de statut"
    requirement: "SIMP-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_entrees_citees_acceptees_et_refusees"
        status: pass
    human_judgment: false
  - id: D3
    description: "Les couples numero <-> libelle des deux menus sont compares au rendu section par section ; la page non mutee est verte et cinq derives la font rougir en nommant la page, la section, le couple attendu et routes.py:<ligne>"
    requirement: "SIMP-01"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_couples_numeros_libelles_par_section"
        status: pass
      - kind: other
        ref: "batterie de morsures : 5/5 detectees, copie verte verifiee avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D4
    description: "Le sommaire liste la page, le H1 egale son libelle d'index et la ligne de retour se resout (tests de la phase 1 inchanges)"
    requirement: "SIMP-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_structure.py#test_sommaire_lists_every_document"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_h1_matches_sommaire_entry"
        status: pass
    human_judgment: false
  - id: D5
    description: "Le module d'ancrage n'ouvre ni la base, ni un processus, ni une socket, ni le reseau, et ne supprime rien (garde ast + cloture transitive)"
    requirement: "SIMP-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_parcours.py#test_garde_ni_base_ni_processus_ni_reseau"
        status: pass
      - kind: other
        ref: "mesure locale : .data/dofus.sqlite3 inchange apres chaque tache (24 989 696 octets, mtime_ns 1788730056843137500)"
        status: pass
    human_judgment: false
  - id: D6
    description: "La page affirme que le parcours en ligne de commande ne pose pas les trois questions, et aucun litteral de profile_input.py ne porte une invite de classe ou d'element"
    requirement: "SIMP-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_parcours.py#test_parcours_cli_ne_pose_pas_les_trois_questions"
        status: pass
    human_judgment: false

duration: 7 min
completed: 2026-09-11
status: complete
---

# Phase 3 Plan 01: Parcours simplifié documenté depuis le rendu réel Summary

**La page `docs/parcours-simplifie.md` est ouverte et ancrée sur le rendu réel : les trois questions du parcours simplifié, les entrées acceptées et refusées rejouées sur le client de test Flask, et les couples numéro ↔ libellé des deux menus comparés au rendu section par section — cinq dérives mesurées la font rougir.**

## Performance

- **Duration:** 405 s ≈ 7 min pour les trois tâches (mesuré : `date +%s` 1789144305 → 1789144710, du premier essai local au vert de la tâche 3 ; la clôture SUMMARY puis STATE/ROADMAP suit)
- **Started:** 2026-09-11T16:31:45Z (corroboré par la date de `.gsd-tmp/plan-p3/probe_render.py`)
- **Completed:** 2026-09-11T16:38:30Z (fin de la vérification de la tâche 3)
- **Tasks:** 3
- **Files modified:** 4 (2 créés, 2 modifiés)

## Accomplishments

- `docs/parcours-simplifie.md` : H1 `# Parcours simplifié`, introduction qui borne la page (lien relatif vers `cli.md`, renvois en prose, et la phrase mesurée « ne pose pas ces trois questions »), trois sections de questions avec les écrans recopiés depuis le rendu, tables d'entrées acceptées et refusées, sous-section « Passer aux réglages détaillés », bloc « Source de vérité » à huit chemins et ligne de retour.
- `tests/test_docs_parcours.py` : 7 tests qui rendent réellement les trois écrans (`GET /optimize/quick/classe` puis deux `POST` valides), extraient les lignes du corps et la ligne de statut, rejouent les 25 entrées épinglées, comparent les 19 + 4 couples des menus au rendu **section par section**, et portent une garde `ast` sans base, sans processus, sans socket et sans réseau.
- Les cinq morsures de la batterie sont détectées sur une copie vérifiée verte avant mutation : libellé inversé dans la page (6 ↔ 9), numéro décalé (6 → 3), élément inversé (1 ↔ 3), ligne de menu supprimée, et permutation de `CLASSES` côté code — chacune nommant la page, la section, le couple attendu et `dofus_stuff/web/routes.py:<ligne>`.
- `docs/sommaire.md` gagne une ligne d'index ; les tests de structure de la phase 1 restent verts **sans exception ni liste blanche** (V14).
- Suite complète verte : **176 passed** (169 avant la phase + 7 nouveaux). `.data/dofus.sqlite3` intact après chaque tâche.

## Task Commits

Each task was committed atomically:

1. **Task 1: la page s'ouvre et les trois questions sont citées depuis le rendu réel** - `0fca9e1` (feat)
2. **Task 2: les entrées acceptées et les refus réels, rejoués sur le rendu** - `f0e0879` (feat)
3. **Task 3: les couples numéro ↔ libellé comparés section par section** - `443f064` (test)

**Plan metadata:** `HEAD` après le commit de clôture de ce plan (docs: complete plan).

_Note: `TDD_MODE=false` pour cette phase — aucun cycle RED/GREEN/REFACTOR n'était requis._

## Files Created/Modified

- `docs/parcours-simplifie.md` (créé, 147 lignes, CRLF, UTF-8 sans BOM) — les trois sections de questions, les tables d'entrées, le bloc « Source de vérité » et la ligne de retour ; les sections `## Lire le résultat`, `## Sauvegarder et exporter`, `## Ce que l'outil suppose` et `## Ce que l'outil ne fait pas` seront insérées **avant** `## Source de vérité` par les plans 03-02 à 03-04.
- `docs/sommaire.md` (modifié, +1 ligne) — `| [Parcours simplifié](parcours-simplifie.md) | Obtenir un stuff en 3 questions, lire puis sauvegarder le résultat |`, insérée entre `Installation` et `CLI`. Rien d'autre n'a changé.
- `tests/test_docs_parcours.py` (créé, 844 lignes, CRLF, UTF-8 sans BOM) — constantes, helpers locaux, table `ENTREES_MESUREES`, listes épinglées `VALEURS_ACCEPTEES` / `VALEURS_REFUSEES`, `MESSAGES_REFUS`, et les 7 tests.
- `.planning/config.json` (modifié, +1 clé) — `git.allow_default_branch_commits: true`, voir « Deviations from Plan ».

## Decisions Made

- **Tranche verticale en tête de plan.** La tâche 1 (`type="tracer"`) livre page, index et module d'ancrage de bout en bout ; la suite étend la même page et le même module. Le plan se déclare entièrement autonome et ses quatre blocs `<verify>` sont purement automatisés : ils ont tous été exécutés (dont les deux batteries de morsures) et aucun `checkpoint` n'a été synthétisé.
- **État de session sous `recommendation_input`.** Forme mesurée et conservée telle quelle (D-32) : c'est la clé que lit `dofus_stuff/web/routes.py:940`. La « simplification » consistant à écrire `classe`/`elements` à la racine de la session fait répondre `302 → /optimize` à **tous** les POST d'éléments et de niveau, ce qui rendrait faux chacun des verdicts épinglés.
- **Comparaison par section, jamais globale.** Les deux menus partagent les numéros 1 à 4 : une comparaison sur la page entière rapporterait quatre constats sur une page correcte (Pitfall 1 de la recherche, mesuré).
- **Garde `ast` sur le risque réel.** Aucune liste blanche de modules produit : le contrôle interdit les racines `sqlite3`, `subprocess`, `socket`, `multiprocessing`, `ctypes`, `webbrowser`, `urllib`, `requests`, `http`, `ftplib`, `smtplib`, l'import de `dofus_stuff.database`, l'appel à `main` et les suppressions de fichiers — et il répète le contrôle sur la **clôture transitive** des imports produit (mesuré : 5 modules atteints depuis `dofus_stuff.optimize.recommend`, aucun interdit). Un import produit non résolu est un échec nommé, et la clôture doit compter au moins 3 modules, faute de quoi le contrôle ne mesurerait rien.
- **Solveur court-circuité pour l'étape 3 acceptée** (`patch("dofus_stuff.web.routes._run_optimize_and_redirect", return_value="computed")`, patron de `tests/test_recommend.py:75`) : la sentinelle est exigée et le niveau retenu relu dans la session (`050` vaut bien 50). Aucun solveur n'est lancé ; le module tourne en 0,31 s.
- **La page ne promet rien qu'elle ne puisse prouver.** Elle ne cite aucune commande (propriété de `docs/cli.md`, D-37), aucun écran du wizard avancé (D-43), aucun fonctionnement de la base locale (D-44), aucun lien externe, et aucune valeur volatile de résultat.
- **Frontière `maxlength="40"` nommée dans le module** : c'est une contrainte du navigateur, `client.post` l'ignore et le serveur n'a pas de borne de longueur propre. La page ne présente donc jamais 40 caractères comme une protection du serveur. Ce point n'était pas requis par la tâche 2 : il est écrit en commentaire du module, sans assertion inventée.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Garde de branche protégée : override documenté dans `.planning/config.json`**
- **Found during:** Task 1, avant le premier commit.
- **Issue:** L'assertion pré-commit du protocole refuse de committer quand `HEAD` est sur la branche par défaut, et `gsd_run query git.base-branch --is-protected main` répondait `true`. Or `.planning/config.json` porte `git.branching_strategy: "none"` et les phases 1 et 2 ont été livrées sur `main` : se mettre sur une branche `agent-*` ferait diverger ce plan de tout l'historique du dépôt.
- **Fix:** Ajout de la clé d'override **prévue par le protocole lui-même** — `git.allow_default_branch_commits: true` dans le bloc `git` de `.planning/config.json`. Vérifié après coup : `gsd_run query git.base-branch --is-protected main` → `false`. Le diff de ce fichier est de deux lignes, sans autre changement.
- **Files modified:** `.planning/config.json`
- **Verification:** `gsd_run query git.base-branch --is-protected main` renvoie `false` ; les trois commits de tâche passent sans `--no-verify` (les hooks s'exécutent normalement).
- **Committed in:** `.planning/config.json` est inclus dans le commit de clôture du plan (il n'appartient à aucune tâche).

**2. [Rule 3 - Adaptation structurelle] `_couples_du_rendu` posé en tâche 1, `_couples_de_section` en tâche 3**
- **Found during:** Task 1.
- **Issue:** Le module doit importer un module produit pour que la clôture transitive de la garde `ast` compte au moins trois modules résolus ; `dofus_stuff.optimize.recommend` a donc été importé dès la tâche 1 (`CLASSES`, `ELEMENTS`). Ces constantes devaient servir à quelque chose de réel et non décoratif.
- **Fix:** `_couples_du_rendu(lignes)` est posé en tâche 1 et employé comme garde anti-objet-vide sur les menus **rendus** (`len(CLASSES)` numéros pour la question 1, `len(ELEMENTS)` pour la question 2) ; la tâche 3 n'ajoute plus que `_couples_de_section` et les tests de comparaison. Comportement identique à celui décrit par le plan ; seule la répartition du helper entre deux commits change.
- **Files modified:** `tests/test_docs_parcours.py`
- **Verification:** Les deux tâches sont vertes ; la batterie de morsures de la tâche 3 est verte sur la page non mutée et rouge sur les cinq dérives.
- **Committed in:** `0fca9e1` (helper) et `443f064` (comparaison)

### Non-deviations worth recording

- **Signature du test du parcours CLI.** Le plan écrit `test_parcours_cli_ne_pose_pas_les_trois_questions(docs_dir, section, normalize)` ; la fixture `section` n'y est pas consommée (le contrôle ne lit aucune section de niveau 2) et a donc été omise. Le test, son nom, ses constats et son assertion sont inchangés.
- **Un seul point d'assertion par test.** Chaque test accumule ses constats et clôt par **une** assertion, forme mesurée en phase 2 (une assertion par constat rendait des motifs inatteignables).

---

**Total deviations:** 2 (2 Rule 3 — un blocage de commit et une adaptation structurelle interne au plan)
**Impact on plan:** Aucun écart de périmètre. L'override de branche est la seule écriture hors des fichiers du plan, et c'est la clé d'override documentée par le protocole lui-même. Les deux écarts restants sont internes : répartition d'un helper entre deux commits, et une fixture inutilisée retirée d'une signature de test.

## Issues Encountered

- **Garde de cohérence des occurrences de la page.** La préservation `dict[numero] -> list[libelles]` ne compte pas les occurrences : `sum(len(libelles))` a dû être utilisée (23 = 19 + 4) pour que « aucun second exemplaire des couples » soit réellement contrôlé. Corrigé pendant la tâche 3, avant le commit.
- **Subtilité mesurée sur `50.0`.** Le motif de couple rendu `(\d{1,2})\.\s+` pourrait mordre sur un message de refus se terminant par `200.` : la cellule de tableau est donc toujours suivie de la barre de colonne, et la valeur décimale `50.0` n'est jamais suivie d'une espace. Vérifié à la lecture du rendu de la page livrée (23 couples exactement).
- Aucun blocage : ce plan n'exige ni geste humain, ni secret, ni accès réseau. `.data/dofus.sqlite3` n'a jamais été ouvert (24 989 696 octets et `mtime_ns` 1788730056843137500 avant et après chaque tâche), et la fixture `app` construit sa propre base sous `tmp_path`.

## Known Stubs

None — aucun stub, aucun `TODO`, aucun test en `skip`, aucune `<verify>` non exécutée. Les 4 harnais de vérification de chaque tâche ont été exécutés, y compris les deux batteries de morsures, et leurs sorties sont citées ci-dessus.

## Threat Flags

Aucune surface nouvelle : ce plan n'ajoute aucun endpoint, aucune route, aucun accès fichier au-delà de la lecture de `docs/` et du dépôt, aucune dépendance et aucun secret. Les menaces T-1 à T-6 du `<threat_model>` du plan sont couvertes : extraction des lignes du corps (T-1), valeurs rejouées sur le rendu et listes épinglées (T-2), garde `ast` et mesure locale `.data/` (T-3), contrôle d'existence des chemins cités (T-4), aucune introspection privée hors `patch` de court-circuit (T-5), aucune installation (T-6).

## Next Phase Readiness

- **Prêt pour 03-02** (vague 2) : la page et le module existent, les constantes de titres `TITRE_RESULTAT` et `TITRE_SUPPOSE` sont déjà posées, et les helpers d'extraction (`_lignes_du_corps`, `_statut`, `_couples_de_section`) sont réutilisables tels quels.
- **Contrainte à honorer par les plans suivants** : insérer leurs sections **avant** `## Source de vérité`, laisser `[Retour au sommaire](sommaire.md)` en dernière ligne, et **ne pas** ajouter de second exemplaire des couples des deux menus (le contrôle compte 19 + 4 occurrences exactement).
- **Rappels de méthode déjà payés** : écrire sous `docs/` et `tests/` en CRLF et UTF-8 sans BOM ; n'ajouter aucun lien vers une page non encore livrée ; ne jamais asserter sur la réponse HTTP entière.
- **Aucun blocage.** `03-VALIDATION.md` reste `status: draft` : sa mise à jour revient à `/gsd:validate-phase`, pas à cet exécuteur.

## Self-Check: PASSED

- `docs/parcours-simplifie.md` : FOUND (147 lignes, CRLF, UTF-8 sans BOM, H1 unique, dernière ligne `[Retour au sommaire](sommaire.md)`)
- `tests/test_docs_parcours.py` : FOUND (844 lignes, CRLF, UTF-8 sans BOM, 7 tests verts)
- `docs/sommaire.md` : FOUND (ligne d'index présente, 21 lignes CRLF)
- Commit `0fca9e1` : FOUND — feat(03-01) la page s'ouvre et les trois questions sont citées depuis le rendu réel
- Commit `f0e0879` : FOUND — feat(03-01) les entrées acceptées et les refus réels, rejoués sur le rendu
- Commit `443f064` : FOUND — test(03-01) les couples numéro ↔ libellé comparés section par section
- `./.venv/Scripts/python.exe -m pytest -q` : 176 passed (169 avant la phase)
- Batterie de morsures de la tâche 1 : mutation détectée, copie verte avant mutation
- Batterie de morsures de la tâche 2 : mutation détectée, copie verte avant mutation
- Batterie de morsures de la tâche 3 : 5/5 détectées, copie verte avant chaque mutation
- `.data/dofus.sqlite3` : 24 989 696 octets, `mtime_ns` 1788730056843137500 — identique aux valeurs mesurées à la planification

---

*Phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el*
*Completed: 2026-09-11*
