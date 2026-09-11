---
phase: "4"
slug: "wizard-avanc-et-r-sorption-de-la-dette-guide-wizard"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-11"
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest **9.1.1** (déclaré `>=8.0`), Python 3.14.7 (`.venv`) |
| **Config file** | `pyproject.toml` → `[tool.pytest.ini_options]` (`testpaths = ["tests"]`, `pythonpath = ["."]`, `filterwarnings`) — **aucune configuration à ajouter** |
| **Quick run command** | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_wizard.py` |
| **Full suite command** | `./.venv/Scripts/python.exe -m pytest -q` |
| **Estimated runtime** | ~4 seconds (baseline mesurée : 186 passed in 3.65s) |

**Shared fixtures** (`tests/conftest.py`, D-12 — à réutiliser, jamais recopier) : `app`, `client`,
`docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple`.

**Reference interpreter** : `./.venv/Scripts/python.exe` (D-15). Sans exécuter `main()`, sans écrire
sous `.data/`, sans connexion réseau.

---

## Sampling Rate

- **After every task commit:** Run `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_wizard.py`
- **After every plan wave:** Run `./.venv/Scripts/python.exe -m pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** ~4 seconds (full suite)

---

## Per-Task Verification Map

Renseigné au fil de l'exécution par `/gsd:validate-phase` à partir des `<automated>` des plans.
Le contrat de phase ci-dessous fixe ce que chaque exigence doit prouver.

| Req ID | Plan | Wave | Requirement | Behavior | Test Type | Automated Command | File Exists | Status |
|--------|------|------|-------------|----------|-----------|-------------------|-------------|--------|
| WIZ-01 | 01 | 1 | Les 9 étapes | Les 9 titres/étapes de `STEP_TITLES` apparaissent dans la page, dans l'ordre de `WIZARD_STEPS`, et le nombre d'étapes est relu au code | unit (rendu + constantes) | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_wizard.py -k etapes` | ❌ W0 | ⬜ pending |
| WIZ-01 | 01 | 1 | Slots et filtres | Les 11 slots et les 10 filtres `F1`…`F10` cités par la page existent au rendu ; `F6` = `ARMES DISTANCE`, `F7` = `ARMES MELEE` | unit (rendu page 1 + page 2) | `… -k filtres` | ❌ W0 | ⬜ pending |
| WIZ-01 | 01 | 1 | Les 11 options | Les 11 options de l'écran `OPTIONS SOLVEUR` sont citées (numéro + libellé lus au rendu) | unit | `… -k options` | ❌ W0 | ⬜ pending |
| WIZ-01 | 01 | 1 | Formats d'édition | Les formats `BASE POINTS CIBLE POIDS` / `BASE EXO CIBLE POIDS` sont décrits tels que le code les applique, avec les messages de refus réels | unit (rendu du sous-écran `OPT-WED` + POST de valeurs invalides) | `… -k formats` | ❌ W0 | ⬜ pending |
| WIZ-01 | 01 | 1 | Syntaxe d'items | La syntaxe d'items (`+ID` → INTERDITS, `-ID` → FORCES, `!ID`, `CLEAR`) et l'unique message de refus sont cités | unit (POST par cas + rendu) | `… -k items` | ❌ W0 | ⬜ pending |
| WIZ-02 | 02 | 2 | Touches actives | Les couples `F7`/`F8`/`ESC` **par étape** (extrémités incluses) et les commandes `GO`, `RESET`, `SAVES`, `1`–`8` sont cités | unit (rendu + POST `RESET`/`SAVES`/`1`/`8`, solveur jamais lancé) | `… -k touches` | ❌ W0 | ⬜ pending |
| WIZ-02 | 02 | 2 | Chemin d'arrivée | Le chemin réel (menu `4` → `/optimize` → `/optimize/quick/classe` → `AVANCE` → `/optimize/wizard/recap`) est décrit et mesuré | unit (chaîne de redirections) | `… -k arrivee` | ❌ W0 | ⬜ pending |
| WIZ-03 | 04 | 3 | Renvois obsolètes | `GUIDE_WIZARD.md` livré ne contient aucun des trois renvois obsolètes (fonction pure, attentes lues au rendu) | unit (détecteur) | `… -k renvoi_obsolete` | ❌ W0 | ⬜ pending |
| WIZ-03 | 04 | 3 | Preuve rouge durable | La **copie figée** sous `tests/` est signalée par le **même** détecteur (au moins trois constats nommés) | unit (détecteur) | `… -k copie_figee` | ❌ W0 | ⬜ pending |
| WIZ-03 | 03 | 2 | Aiguillage et README | Les deux liens de l'aiguillage résolvent et `README.md` ne contient plus `](GUIDE_WIZARD.md)` | unit (disque) | `… -k aiguillage` | ❌ W0 | ⬜ pending |
| WIZ-03 | 03 | 2 | Sommaire | Le nouvel index du sommaire reste cohérent : `problemes_index`/`problemes_h1`/`problemes_retour_sommaire` verts | unit (garde existante) | `… -m docs_structure` puis suite entière | ✅ `tests/test_docs_structure.py` | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_docs_wizard.py` — module d'ancrage (étapes, filtres, options, formats, items, touches, arrivée)
- [ ] `tests/test_docs_wizard.py` — détecteur `renvois_obsoletes` + test de la copie figée
- [ ] `tests/fixtures/guide-wizard-obsolete.md` — copie figée de l'état antérieur (preuve rouge durable, D-59)
- [ ] `tests/test_docs_parcours.py` — constante `PAGES_INEXISTANTES` réduite à (`base-locale.md`) + assertion symétrique du lien désormais légitime (**Pitfall 1 de la recherche : deux tests existants interdisent aujourd'hui le lien que D-63 impose**)

**Aucune installation de framework requise** : `pytest` 9.1.1 est déjà présent et configuré dans
`pyproject.toml`. Wave 0 ne crée que des fichiers de test et une fixture.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|

*All phase behaviors have automated verification.* — le critère 5 du ROADMAP (« rouge puis vert »)
est ramené à un contrôle automatique par la double preuve D-59 : observation réelle en ordre TDD
**et** copie figée signalée par le même détecteur, donc relançable à tout moment. Aucune validation
humaine n'est revendiquée pour cette phase.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
