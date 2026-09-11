---
gsd_state_version: "1.0"
current_phase: 3
current_phase_name: Parcours simplifié documenté depuis le rendu réel
status: planning
stopped_at: Phase 2 complete, ready to plan Phase 3
last_updated: "2026-09-11T12:59:16.918Z"
last_activity: 2026-09-11
last_activity_desc: Phase 2 complete, transitioned to Phase 3
state_head: 0a9e2821a524b1b52975fd1fc5ba3063f6a56340
progress:
  total_phases: 6
  completed_phases: 2
  total_plans: 7
  completed_plans: 7
  percent: 33
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-10)

**Core value:** Un utilisateur qui n'a jamais vu le projet peut installer l'outil, lancer le flux simplifié classe → éléments → niveau, lire son résultat et retrouver chaque commande/menu cité dans le code réel — sans lire le code et sans rencontrer de documentation périmée.
**Current focus:** Phase 2 — Référence CLI alignée sur le parseur

## Current Position

Phase: 3 (x) — READY TO EXECUTE
Plan: Not started
Status: planning
Last activity: 2026-09-11 — Phase 2 complete, transitioned to Phase 3

Progress: [███░░░░░░░] 33%

## Performance Metrics

**Velocity:**

- Total plans completed: 7
- Average duration: -
- Total execution time: -

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 | 4 | - | - |
| 2 | 3 | - | - |

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

Last session: 2026-09-11T12:34:39.558Z
Stopped at: Phase 2 complete, ready to plan Phase 3
Resume file: None
