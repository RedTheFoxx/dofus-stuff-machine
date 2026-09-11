---
gsd_state_version: "1.0"
current_phase: 2
current_phase_name: Référence CLI alignée sur le parseur
status: executing
stopped_at: Phase 2 context gathered
last_updated: "2026-09-11T12:13:46.334Z"
last_activity: 2026-09-11
last_activity_desc: Phase 1 complete, transitioned to Phase 2
state_head: 2f876e90c387164125d4732342b384e2ab162aa6
progress:
  total_phases: 6
  completed_phases: 1
  total_plans: 7
  completed_plans: 4
  percent: 17
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-10)

**Core value:** Un utilisateur qui n'a jamais vu le projet peut installer l'outil, lancer le flux simplifié classe → éléments → niveau, lire son résultat et retrouver chaque commande/menu cité dans le code réel — sans lire le code et sans rencontrer de documentation périmée.
**Current focus:** Phase 1 — Socle documentaire, installation et harnais vérifiable

## Current Position

Phase: 2 (Référence CLI alignée sur le parseur) — READY TO EXECUTE
Plan: Not started
Status: Ready to execute
Last activity: 2026-09-11 — Phase 1 complete, transitioned to Phase 2

Progress: [██░░░░░░░░] 17%

## Performance Metrics

**Velocity:**

- Total plans completed: 4
- Average duration: -
- Total execution time: -

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 | 4 | - | - |

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

Last session: 2026-09-11T11:03:05.437Z
Stopped at: Phase 2 context gathered
Resume file: .planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-CONTEXT.md
