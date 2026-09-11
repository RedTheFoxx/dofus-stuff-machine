---
phase: "4"
slug: "wizard-avanc-et-r-sorption-de-la-dette-guide-wizard"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: true) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
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
| WIZ-01 | 01 | 1 | Les 9 étapes | Les 9 titres/étapes de `STEP_TITLES` apparaissent dans la page, dans l'ordre de `WIZARD_STEPS`, et le nombre d'étapes est relu au code | unit (rendu + constantes) | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_wizard.py -k etapes` | ✅ W0 | ✅ green |
| WIZ-01 | 01 | 1 | Slots et filtres | Les 11 slots et les 10 filtres `F1`…`F10` cités par la page existent au rendu ; `F6` = `ARMES DISTANCE`, `F7` = `ARMES MELEE` | unit (rendu page 1 + page 2) | `… -k filtres` | ✅ W0 | ✅ green |
| WIZ-01 | 01 | 1 | Les 11 options | Les 11 options de l'écran `OPTIONS SOLVEUR` sont citées (numéro + libellé lus au rendu) | unit | `… -k options` | ✅ W0 | ✅ green |
| WIZ-01 | 01 | 1 | Formats d'édition | Les formats `BASE POINTS CIBLE POIDS` / `BASE EXO CIBLE POIDS` sont décrits tels que le code les applique, avec les messages de refus réels | unit (rendu du sous-écran `OPT-WED` + POST de valeurs invalides) | `… -k formats` | ✅ W0 | ✅ green |
| WIZ-01 | 01 | 1 | Syntaxe d'items | La syntaxe d'items (`+ID` → INTERDITS, `-ID` → FORCES, `!ID`, `CLEAR`) et l'unique message de refus sont cités | unit (POST par cas + rendu) | `… -k items` | ✅ W0 | ✅ green |
| WIZ-02 | 02 | 2 | Touches actives | Les couples `F7`/`F8`/`ESC` **par étape** (extrémités incluses) et les commandes `GO`, `RESET`, `SAVES`, `1`–`8` sont cités | unit (rendu + POST `RESET`/`SAVES`/`1`/`8`, solveur jamais lancé) | `… -k touches` | ✅ W0 | ✅ green |
| WIZ-02 | 02 | 2 | Chemin d'arrivée | Le chemin réel (menu `4` → `/optimize` → `/optimize/quick/classe` → `AVANCE` → `/optimize/wizard/recap`) est décrit et mesuré | unit (chaîne de redirections) | `… -k arrivee` | ✅ W0 | ✅ green |
| WIZ-03 | 04 | 3 | Renvois obsolètes | `GUIDE_WIZARD.md` livré ne contient aucun des trois renvois obsolètes (fonction pure, attentes lues au rendu) | unit (détecteur) | `… -k renvoi_obsolete` | ✅ W0 | ✅ green |
| WIZ-03 | 04 | 3 | Preuve rouge durable | La **copie figée** sous `tests/` est signalée par le **même** détecteur (au moins trois constats nommés) | unit (détecteur) | `… -k copie_figee` | ✅ W0 | ✅ green |
| WIZ-03 | 03 | 2 | Aiguillage et README | Les deux liens de l'aiguillage résolvent et `README.md` ne contient plus `](GUIDE_WIZARD.md)` | unit (disque) | `… -k aiguillage` | ✅ W0 | ✅ green |
| WIZ-03 | 03 | 2 | Sommaire | Le nouvel index du sommaire reste cohérent : `problemes_index`/`problemes_h1`/`problemes_retour_sommaire` verts | unit (garde existante) | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_structure.py` | ✅ `tests/test_docs_structure.py` | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/test_docs_wizard.py` — module d'ancrage (étapes, filtres, options, formats, items, touches, arrivée)
- [x] `tests/test_docs_wizard.py` — détecteur `renvois_obsoletes` + test de la copie figée
- [x] `tests/fixtures/guide-wizard-obsolete.md` — copie figée de l'état antérieur (preuve rouge durable, D-59)
- [x] `tests/test_docs_parcours.py` — constante `PAGES_INEXISTANTES` réduite à (`base-locale.md`) + assertion symétrique du lien désormais légitime (**Pitfall 1 de la recherche : deux tests existants interdisent aujourd'hui le lien que D-63 impose**)

**Aucune installation de framework requise** : `pytest` 9.1.1 est déjà présent et configuré dans
`pyproject.toml`. Wave 0 ne crée que des fichiers de test et une fixture.

---

## Correctif de contrat (unique ecart trouve, clos)

Une seule ligne du tableau ci-dessus n'etait pas verte a la validation : celle du **Sommaire**
(WIZ-03), dont la commande automatisee s'ecrivait `pytest -m docs_structure`. Ce marqueur **n'est pas
declare** dans `pyproject.toml` : la commande selectionnait **0 test (205 deselectionnes)** au lieu du
garde-fou reel. Une ligne dont la commande ne selectionne rien est un **faux vert de contrat**, donc
elle a ete corrigee pour cibler le fichier qui existe, et la correction a ete **prouvee en l'executant** :

- `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_structure.py` -> **14 passed**.
- Les 10 autres lignes du tableau se sont averees couvertes et vertes, chacune selectionnant au moins
  un test : `etapes`, `filtres`, `options`, `formats`, `items`, `touches` et `arrivee` et
  `renvoi_obsolete` et `copie_figee` (1 passed chacune) et `aiguillage` (**3 passed**).
- Aucun marqueur n'a ete ajoute a `pyproject.toml` : la cible est le fichier, pas une configuration
  partagee, ce qui aurait depasse le perimetre de la phase.

Limite honnete : ce correctif rend la commande **fidele au garde-fou existant**, il ne l'etend pas et
ne revendique aucune couverture au-dela des gardes listes.

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

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-09-11
