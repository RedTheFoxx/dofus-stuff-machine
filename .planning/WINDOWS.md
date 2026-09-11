---
schema_version: 1
open_count: 6
waived_count: 0
fixed_count: 0
total_count: 6
last_updated: 2026-09-11T13:37:27.213Z
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
| 5 | 3 | deviation | .planning/ROADMAP.md | 1 | ECR-1 (critere de la phase 3) reformule, pas abandonne : la table 'libelle tronque -> nom complet' n'a pas d'objet dans ce flux (aucune ligne rendue ne porte de points de suspension, largeur maximale exactement COLS) ; la section Correspondance des libelles porte donc sur libelle technique -> nom complet et aucun controle n'asserte l'apparition d'une troncature (une telle assertion serait rouge sur une implementation correcte). Decision enregistree dans .planning/ROADMAP.md (bloc phase 3) et 03-04-PLAN.md (must_haves.assumptions). | open |  | 2026-09-11T13:37:24.258Z |  |
| 6 | 3 | deviation | .planning/ROADMAP.md | 1 | ECR-2 (critere de la phase 3) reformule, pas abandonne : 'Methode / Score / Indice de recherche sur la derniere page' est faux sur la fixture deterministe (page 2 sur 3) ; l'assertion du plan 03-02 est donc positionnelle (apres le dernier 'Equipement :' et avant 'Greedy: ', la page 3 et les suivantes etant structurellement identiques), et la page dit 'en fin de resultat'. Une assertion exigeant ces diagnostics sur la derniere page serait rouge sur une implementation correcte. Decision enregistree dans .planning/ROADMAP.md (bloc phase 3) et 03-02-PLAN.md (must_haves.assumptions). | open |  | 2026-09-11T13:37:27.213Z |  |

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
  },
  {
    "id": 5,
    "kind": "deviation",
    "phase": "3",
    "file": ".planning/ROADMAP.md",
    "line": 1,
    "description": "ECR-1 (critere de la phase 3) reformule, pas abandonne : la table 'libelle tronque -> nom complet' n'a pas d'objet dans ce flux (aucune ligne rendue ne porte de points de suspension, largeur maximale exactement COLS) ; la section Correspondance des libelles porte donc sur libelle technique -> nom complet et aucun controle n'asserte l'apparition d'une troncature (une telle assertion serait rouge sur une implementation correcte). Decision enregistree dans .planning/ROADMAP.md (bloc phase 3) et 03-04-PLAN.md (must_haves.assumptions).",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T13:37:24.258Z",
    "resolved_at": null
  },
  {
    "id": 6,
    "kind": "deviation",
    "phase": "3",
    "file": ".planning/ROADMAP.md",
    "line": 1,
    "description": "ECR-2 (critere de la phase 3) reformule, pas abandonne : 'Methode / Score / Indice de recherche sur la derniere page' est faux sur la fixture deterministe (page 2 sur 3) ; l'assertion du plan 03-02 est donc positionnelle (apres le dernier 'Equipement :' et avant 'Greedy: ', la page 3 et les suivantes etant structurellement identiques), et la page dit 'en fin de resultat'. Une assertion exigeant ces diagnostics sur la derniere page serait rouge sur une implementation correcte. Decision enregistree dans .planning/ROADMAP.md (bloc phase 3) et 03-02-PLAN.md (must_haves.assumptions).",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T13:37:27.213Z",
    "resolved_at": null
  }
]
````
