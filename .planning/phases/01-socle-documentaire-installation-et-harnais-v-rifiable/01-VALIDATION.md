---
phase: "01"
slug: "socle-documentaire-installation-et-harnais-v-rifiable"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-11"
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Source: `01-RESEARCH.md` § Validation Architecture (valeurs mesurées le 2026-09-11).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest` 9.1.1, exécuté par `.venv/Scripts/python.exe` (interpréteur épinglé, D-15) |
| **Config file** | `pyproject.toml` — `[tool.pytest.ini_options]` : `testpaths = ["tests"]`, `pythonpath = ["."]` |
| **Quick run command** | `./.venv/Scripts/python.exe -m pytest tests/test_docs_structure.py tests/test_docs_code_anchor.py -q` |
| **Full suite command** | `./.venv/Scripts/python.exe -m pytest -q` |
| **Estimated runtime** | ~2 secondes pour la suite complète (état de départ mesuré : `136 passed in 1.61s`) |

---

## Sampling Rate

- **After every task commit:** Run `./.venv/Scripts/python.exe -m pytest tests/test_docs_structure.py tests/test_docs_code_anchor.py -q`
- **After every plan wave:** Run `./.venv/Scripts/python.exe -m pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** ~5 seconds

---

## Per-Task Verification Map

Task IDs below are the ROADMAP plan IDs; individual `<automated>` commands live in each
PLAN.md and are the binding ones. Rows are keyed by requirement so the map stays valid
whatever internal task split the planner chooses (dimension 8 draws its test-type and
threat-ref columns from the plan file itself).

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01 | 01 | see PLAN.md | SOMM-01 | T-01-01 (secret non recopié) | `README.md` ne contient qu'un lien unique vers `docs/sommaire.md`, aucun secret | structure | `pytest tests/test_docs_structure.py::test_readme_links_to_sommaire -q` | ❌ W0 | ⬜ pending |
| 01-01 | 01 | see PLAN.md | SOMM-02 | T-01-04 (cible hors dépôt refusée) | Toute cible du sommaire reste sous la racine du dépôt et existe | structure | `pytest tests/test_docs_structure.py::test_sommaire_lists_every_document tests/test_docs_structure.py::test_sommaire_links_resolve -q` | ❌ W0 | ⬜ pending |
| 01-02 | 01 | see PLAN.md | INST-01 | T-01-05 (commande destructrice) | `docs/installation.md` n'enseigne que `--offline db status` — aucune commande destructrice | structure + ancrage | `pytest tests/test_docs_structure.py tests/test_docs_code_anchor.py -q` | ❌ W0 | ⬜ pending |
| 01-02 | 01 | see PLAN.md | INST-02 | T-01-02 (exposition réseau) | L'adresse par défaut citée est `127.0.0.1:5000` dérivée du parseur ; aucune recommandation `0.0.0.0` | ancrage | `pytest tests/test_docs_code_anchor.py::test_adresse_par_defaut_documentee -q` | ❌ W0 | ⬜ pending |
| 01-02 | 01 | see PLAN.md | INST-03 | — | Touches `F7`, `F8`, `ESC`, `PageUp`, `PageDown` citées avant la commande de lancement web | structure | `pytest tests/test_docs_structure.py::test_pilotage_clavier_avant_lancement -q` | ❌ W0 | ⬜ pending |
| 01-03 | 01 | see PLAN.md | SOMM-03 | T-01-04 (lien mort) | H1 unique par page, égal au libellé d'index ; ligne de retour résolue vers `sommaire.md` | structure | `pytest tests/test_docs_structure.py::test_h1_matches_sommaire_entry tests/test_docs_structure.py::test_pages_have_back_link -q` | ❌ W0 | ⬜ pending |
| 01-03 | 01 | see PLAN.md | GARD-01 | T-01-07 (écriture hors `tmp_path`) | Test de mutation sur copie `tmp_path` uniquement : aucune écriture sous `docs/` ni `.data/` | structure (mutation) | `pytest tests/test_docs_structure.py::test_mutation_detecte_les_trois_derives -q` | ❌ W0 | ⬜ pending |
| 01-04 | 01 | see PLAN.md | GARD-02 | T-01-03 (`--debug`/`main()`), T-01-08 (réseau) | Options d'entrée web acceptées par `build_parser().parse_args` ; chemins « Source de vérité » existants ; aucun `main()`, aucun réseau | ancrage | `pytest tests/test_docs_code_anchor.py -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `docs/sommaire.md` — index unique + parcours (SOMM-01, SOMM-02)
- [ ] `docs/installation.md` — gabarit D-01, chemin d'installation, clavier avant lancement (INST-01 à INST-03)
- [ ] `README.md` — section « Documentation utilisateur » (SOMM-01, D-10)
- [ ] `tests/conftest.py` — fixture `docs_dir`, normalisation testée (D-11, D-12)
- [ ] `tests/test_docs_structure.py` — 12 tests d'invariants documentaires (GARD-01)
- [ ] `tests/test_docs_code_anchor.py` — 5 tests d'ancrage au code (GARD-02)
- [ ] Framework : aucun (pytest déjà installé, `[tool.pytest.ini_options]` déjà configuré)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| *(aucune)* | — | Tous les critères de la phase sont automatisables : liens, exhaustivité, H1, ancrage parseur, mutation de dérive | — |

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
