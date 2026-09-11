---
schema_version: 1
open_count: 1
waived_count: 0
fixed_count: 0
total_count: 1
last_updated: 2026-09-11T10:24:55.610Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | stub | docs/installation.md | 1 | Squelette D-01 volontairement partiel : contenu complet livre par le plan 01-02 | open |  | 2026-09-11T10:24:55.610Z |  |

````json
[
  {
    "id": 1,
    "kind": "stub",
    "phase": "01",
    "file": "docs/installation.md",
    "line": 1,
    "description": "Squelette D-01 volontairement partiel : contenu complet livre par le plan 01-02",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T10:24:55.610Z",
    "resolved_at": null
  }
]
````
