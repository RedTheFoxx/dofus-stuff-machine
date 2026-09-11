---
phase: "2"
slug: "r-f-rence-cli-align-e-sur-le-parseur"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-11"
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Source: `02-RESEARCH.md` § Validation Architecture, `02-CONTEXT.md` D-16…D-31.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (already installed in the project virtualenv) |
| **Config file** | none — the existing suite at `tests/` is the harness; no new config |
| **Quick run command** | `./.venv/Scripts/python.exe -m pytest tests/test_docs_cli.py -q` |
| **Full suite command** | `./.venv/Scripts/python.exe -m pytest -q` |
| **Estimated runtime** | ~2 seconds (full suite measured at 1.6–2.5 s across phase 1) |

---

## Sampling Rate

- **After every task commit:** Run `./.venv/Scripts/python.exe -m pytest tests/test_docs_cli.py -q`
- **After every plan wave:** Run `./.venv/Scripts/python.exe -m pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** ~3 seconds

---

## Per-Task Verification Map

This table is the plan-time seed. `02-RESEARCH.md` § Validation Architecture is the authoritative statement of each predicate and of the mutation that must make it fail; the plan fills the Task ID / Wave / File Exists columns when the tasks are written.

| Criterion | Requirement | Predicate (must be machine-checkable) | Mutation that must make it fail | Test Type | Automated Command |
|-----------|-------------|----------------------------------------|--------------------------------|-----------|-------------------|
| 1 — every documented sub-command parses | CLI-01 | for each of the 8 pinned `(name, complete argv)` pairs: the name occurs in the page and `build_parser().parse_args(argv)` exits 0 — never a bare token, since bare `db`/`cache` exit 2 (`db_command` is required, measured) | rename a documented sub-command token on the page (`cache` → `alias-absent`) and, in a throwaway copy of `dofus_stuff/cli.py`, rename `self-test` → `selftest` | unit | `pytest tests/test_docs_cli.py -q` |
| 2 — every documented global and `optimize` option is accepted | CLI-02 | for each documented `(option, trial value)` pair, `parse_args` accepts it on the right parser level | add an invented option to a documented table | unit | `pytest tests/test_docs_cli.py -q` |
| 3 — every documented example is verbatim + `shlex`-parseable | CLI-03 | each marked example line occurs verbatim on the page AND `shlex.split(line)` → `parse_args` succeeds | edit an example in the page by one character | unit | `pytest tests/test_docs_cli.py -q` |
| 4a — global flag ordering illustrated | CLI-03 | at least one marked offline example has the global flag before the sub-command | move the global flag after the sub-command in every example | unit | `pytest tests/test_docs_cli.py -q` |
| 4b — destructive command never in a recommended path | CLI-03 | the destructive token appears only on a line that also carries its destructive warning, and never inside a recommended-path section | delete the warning from the destructive line | unit | `pytest tests/test_docs_cli.py -q` |
| 5 — suite green, no `main()`, no `.data/` write | CLI-01…03 | full suite exits 0 with the pinned interpreter, **and** the CLI module imports only `dofus_stuff.cli`, imports no `subprocess`/`socket`/`sqlite3` and calls no `main` (checked by AST on the module's own source, naming the offending module) | inject `from dofus_stuff.database import Database` into a throwaway copy of `tests/test_docs_cli.py` → the AST assertion must go red | unit | `./.venv/Scripts/python.exe -m pytest -q` |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Mutation Coverage (plan-time mapping)

> Le registre qui fait foi, assertion par assertion, est le tableau `## Mutation coverage` de
> `02-02-PLAN.md` et de `02-03-PLAN.md`. Le tableau ci-dessous en donne la vue par critere et par
> plan ; chaque mutation y est **programmee comme une commande executable** dans le `<verify>` de la
> tache concernee, jamais comme une intention.

| Where | Mutations scheduled | Class of assertion each one proves |
|-------|--------------------|------------------------------------|
| `02-02-PLAN.md` tache 1 | 2 | le scanner partage deplace mord encore (`--offline` retire de la copie de la page d'installation) et `_section(texte, titre, page)` nomme toujours la page (titre « Source de verite » renomme -> `introuvable` + page nommee) |
| `02-02-PLAN.md` tache 2 | 8 | jeton epingle renomme dans la page ; option inventee ajoutee a la table `## Options globales` ; toutes les lignes de tableau supprimees (gardes non vides) ; jeton de sous-commande renomme ; description de `db` dupliquee dans `## cache` ; derive cote parseur dans une copie de `dofus_stuff/cli.py` ; chemin cite absent du depot ; jeton `build_parser()` retire |
| `02-03-PLAN.md` tache 1 | 5 | marqueur `console` retire ; jeton d'option renomme dans un exemple ; guillemet non ferme ; seul exemple de `list` supprime ; ordre global/sous-commande inverse |
| `02-03-PLAN.md` tache 2 | 4 | avertissement destructeur retire ; mention destructrice glissee dans un bloc d'exemple ; toute ligne citant la commande supprimee ; import de `dofus_stuff.database` injecte dans une copie du module de test |

**Declared non-falsifiable for this phase** (written into the test module itself, D-26, and repeated
in the plans' `## Mutation coverage` tables):

| Item | Why it cannot be falsified here |
|------|--------------------------------|
| presence « verbatim » d'une ligne d'exemple | la ligne est extraite de la page : garantie de construction, pas exigence de validation |
| completude parser -> page | choix explicite D-26 : une sous-commande ou une option ajoutee plus tard et non documentee ne doit pas faire rougir la suite |
| un jeton cite qui serait le prefixe non ambigu d'une option reelle | `argparse` l'accepte (mesure : `--force-sync` reste accepte apres renommage en `--force-synchronisation`) ; le refuser exigerait l'introspection privee interdite par D-14 |
| « hors parcours recommande » comme qualite de section | non decidable mecaniquement ; approche par la co-presence ligne a ligne et l'absence dans tout bloc marque |
| le caractere « destructeur » lui-meme | aucun attribut du parseur ne le declare : classement humain derive du code (assumption A2) |
| « la suite est verte » | condition d'execution, falsifiable seulement par une regression du produit ; les parties falsifiables sont l'assertion statique par `ast` et l'horodatage inchange de `.data/dofus.sqlite3` |

**Resultat d'execution des mutations :** consigne mutation par mutation dans `02-03-SUMMARY.md`
(nom, mutation, sortie rouge, motif trouve). Les champs `status` et `nyquist_compliant` de
l'en-tete de ce fichier relevent de la porte de phase, pas de la planification.

---

## Wave 0 Requirements

- [ ] `tests/conftest.py` — a single shared code-block scanner (currently the block parsing lives inside `tests/test_docs_code_anchor.py`; D-12 requires the shared helper to move to `conftest.py` rather than be duplicated)
- [ ] `tests/test_docs_cli.py` — the new CLI-anchoring module (file created in wave 1 by plan 02-02/02-03)
- [ ] No framework install needed — pytest and the virtualenv already exist

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| « jamais dans un parcours recommandé » (criterion 4b, second half) | CLI-03 | Not fully decidable mechanically: whether a section is "a recommended path" is a reading of the page's structure, not a string. The test can only enforce the decidable part (the destructive token never shares a section with a recommended-path marker, and always carries its warning). | Inspect `docs/cli.md`: confirm `db clear` appears only in a section that is explicitly labelled as destructive/hors parcours, and that no recommended-path section mentions it. |
| Classifying which sub-commands are destructive (Assumption A2) | CLI-03 | The parser declares no "destructive" trait; the classification is a human judgement over the code. The plan must decide explicitly and carry its rationale rather than infer it silently. | Read `dofus_stuff/cli.py` + `dofus_stuff/database.py`; confirm the list the page's warning covers matches the commands that actually write/erase the local database. |

*Everything else in this phase has automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
