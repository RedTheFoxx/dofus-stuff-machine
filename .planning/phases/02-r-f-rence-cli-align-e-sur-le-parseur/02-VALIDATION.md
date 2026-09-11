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
| 1 — every documented sub-command parses | CLI-01 | each documented sub-command token, run bare through `build_parser().parse_args([...])`, exits 0 and yields `command == <token>` | rename a documented sub-command token on the page | unit | `pytest tests/test_docs_cli.py -q` |
| 2 — every documented global and `optimize` option is accepted | CLI-02 | for each documented `(option, trial value)` pair, `parse_args` accepts it on the right parser level | add an invented option to a documented table | unit | `pytest tests/test_docs_cli.py -q` |
| 3 — every documented example is verbatim + `shlex`-parseable | CLI-03 | each marked example line occurs verbatim on the page AND `shlex.split(line)` → `parse_args` succeeds | edit an example in the page by one character | unit | `pytest tests/test_docs_cli.py -q` |
| 4a — global flag ordering illustrated | CLI-03 | at least one marked offline example has the global flag before the sub-command | move the global flag after the sub-command in every example | unit | `pytest tests/test_docs_cli.py -q` |
| 4b — destructive command never in a recommended path | CLI-03 | the destructive token appears only on a line that also carries its destructive warning, and never inside a recommended-path section | delete the warning from the destructive line | unit | `pytest tests/test_docs_cli.py -q` |
| 5 — suite green, no `main()`, no `.data/` write | CLI-01…03 | full suite exits 0 with the pinned interpreter | (guarded by construction: no test invokes `main()` or `--data-dir .data`) | unit | `./.venv/Scripts/python.exe -m pytest -q` |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

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
