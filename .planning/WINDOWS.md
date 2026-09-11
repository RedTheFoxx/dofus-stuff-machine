---
schema_version: 1
open_count: 4
waived_count: 0
fixed_count: 0
total_count: 4
last_updated: 2026-09-11T12:26:15.224Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | stub | docs/installation.md | 1 | Squelette D-01 volontairement partiel : contenu complet livre par le plan 01-02 | open |  | 2026-09-11T10:24:55.610Z |  |
| 2 | 2 | deviation | docs/cli.md | 1 | Ecart assume avec .claude/CLAUDE.md DOCS-06 (tableau unique commande->role->exemple) : la page suit D-16/D-17/D-18 (une section par sous-commande, tables d'options par section, aucune table recapitulative unique) | open |  | 2026-09-11T12:19:29.230Z |  |
| 3 | 2 | deviation | tests/test_docs_cli.py | 1 | Marqueurs d'alias adaptes a la page livree : la section cache declare l'equivalence par « cache est le second nom de db ... equivaut a db <sous-commande> », sans le mot « alias » attendu par 02-RESEARCH.md Pattern 5 ; le controle exige donc l'un des marqueurs normalises alias/second nom/equivaut, et la page livree n'a pas ete modifiee pour faire passer le test | open |  | 2026-09-11T12:26:14.917Z |  |
| 4 | 2 | deviation | tests/test_docs_cli.py | 1 | Limite de lecture de la mutation « build_parser() retire » : dans une copie sans arbre produit le module est rouge par construction (controle d'existence des chemins) et la sortie cite deja build_parser ; la morsure discriminante a donc ete re-mesuree sur une copie incluant l'arbre produit (5 passed avant mutation, 1 failed apres, message nommant build_parser()) | open |  | 2026-09-11T12:26:15.224Z |  |

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
  },
  {
    "id": 2,
    "kind": "deviation",
    "phase": "2",
    "file": "docs/cli.md",
    "line": 1,
    "description": "Ecart assume avec .claude/CLAUDE.md DOCS-06 (tableau unique commande->role->exemple) : la page suit D-16/D-17/D-18 (une section par sous-commande, tables d'options par section, aucune table recapitulative unique)",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T12:19:29.230Z",
    "resolved_at": null
  },
  {
    "id": 3,
    "kind": "deviation",
    "phase": "2",
    "file": "tests/test_docs_cli.py",
    "line": 1,
    "description": "Marqueurs d'alias adaptes a la page livree : la section cache declare l'equivalence par « cache est le second nom de db ... equivaut a db <sous-commande> », sans le mot « alias » attendu par 02-RESEARCH.md Pattern 5 ; le controle exige donc l'un des marqueurs normalises alias/second nom/equivaut, et la page livree n'a pas ete modifiee pour faire passer le test",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T12:26:14.917Z",
    "resolved_at": null
  },
  {
    "id": 4,
    "kind": "deviation",
    "phase": "2",
    "file": "tests/test_docs_cli.py",
    "line": 1,
    "description": "Limite de lecture de la mutation « build_parser() retire » : dans une copie sans arbre produit le module est rouge par construction (controle d'existence des chemins) et la sortie cite deja build_parser ; la morsure discriminante a donc ete re-mesuree sur une copie incluant l'arbre produit (5 passed avant mutation, 1 failed apres, message nommant build_parser())",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T12:26:15.224Z",
    "resolved_at": null
  }
]
````
