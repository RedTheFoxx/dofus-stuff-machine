---
phase: "6"
slug: "depannage-glossaire-completude-et-preuve-finale"
# status lifecycle: draft (seeded by plan-phase) -> validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-11"
---

# Phase 6 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> **Autorite de detail :** `06-RESEARCH.md` § `Validation Architecture` porte le tableau complet
> « comportement -> commande automatisee -> fichier existant ou Wave 0 », ainsi que l'inventaire de ce qui
> est **deja couvert** par une garde existante (l'egalite index<->disque et l'egalite H1<->libelle sont
> deja tenues : mesure, page manquante -> 14 failed, page en trop -> echecs index + H1).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.1.1, Python 3.14.7 (`.venv`) |
| **Config file** | `pyproject.toml` -> `[tool.pytest.ini_options]` - **aucune configuration a ajouter** |
| **Quick run command** | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_<module>.py` |
| **Full suite command** | `./.venv/Scripts/python.exe -m pytest -q` |
| **Estimated runtime** | ~4 a 8 secondes (baseline mesuree : **219 passed in 4.31s**) |

Fixtures partagees (`tests/conftest.py`, D-12) : `app`, `client`, `docs_dir`, `normalize`, `section`,
`sections`, `lignes_de_code`, `lignes_exemple`. Interpreteur epingle (D-15) ; aucune ecriture sous
`.data/`, aucune synchronisation, aucune connexion reseau, `main()` jamais execute.

---

## Sampling Rate

- **After every task commit:** `./.venv/Scripts/python.exe -m pytest -q` (le module vise d'abord)
- **After every plan wave:** `./.venv/Scripts/python.exe -m pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** les batteries de morsures rejouent la suite sur des copies : compter 20 a 45 s par batterie (cout assume, D-97)

---

## Per-Task Verification Map

Projection des 5 criteres et de AIDE-01, AIDE-02, GARD-03, GARD-04 sur les 4 plans du ROADMAP.
Les selecteurs `-k` seront remplaces par les noms reels des tests a la validation de phase (lecon des
phases 3 a 5 : un selecteur provisoire qui ne selectionne rien est un faux temoin).

| Req ID | Plan | Wave | Requirement | Behavior | Test Type | Automated Command | File Exists | Status |
|--------|------|------|-------------|----------|-----------|-------------------|-------------|--------|
| AIDE-01 | 06-01 | 1 | Message -> rubrique | Chaque rubrique de `docs/depannage.md` s'adosse a un message **reellement produit** (les 5 familles du critere 1), et les cas sans message (clavier inactif) sont dits pour ce qu'ils sont | unit (correspondance message -> rubrique) | `... -m pytest -q tests/test_docs_depannage.py` | ❌ W0 | ⬜ pending |
| AIDE-01 | 06-01 | 1 | Index et gabarit | La page est listee dans `docs/sommaire.md`, H1 = libelle d'index, ligne de retour, CRLF/UTF-8 sans BOM | unit (gardes existantes) | `... -m pytest -q tests/test_docs_structure.py` | ✅ | ⬜ pending |
| AIDE-02 | 06-02 | 2 | Entrees du glossaire | Chaque entree citee est **reellement presente** et les entrees sont **triees** | unit (existence + ordre) | `... -m pytest -q tests/test_docs_glossaire.py` | ❌ W0 | ⬜ pending |
| AIDE-02 | 06-02 | 2 | Parcours conseille final | Le sommaire propose le parcours final, coherent avec les pages reellement livrees | unit (coherence sommaire <-> disque) | `... -k parcours` | ❌ W0 | ⬜ pending |
| GARD-03 | 06-03 | 3 | Liste epinglee des 8 pages | Les 8 pages epinglees sont livrees et **l'ensemble exact** des fichiers de `docs/` est verifie : **toute page en trop fait echouer la suite** | unit (egalite d'ensembles) | `... -k completude` | ❌ W0 | ⬜ pending |
| GARD-03 | 06-03 | 3 | Non-duplication | Le controle ne duplique pas les gardes existantes (egalite index<->disque, H1<->libelle) | unit (inventaire) | `... -m pytest -q tests/test_docs_structure.py` | ✅ | ⬜ pending |
| GARD-04 | 06-04 | 4 | Preuve du harnais | Une copie de `docs/` sous `tmp_path` avec **derive injectee** fait **echouer reellement** le harnais : page manquante, libelle derive, renvoi obsolete. La copie est **verte avant mutation** et chaque morsure exige un **motif nomme** | integration (mutation sur copie) | `... -k mutation` | ❌ W0 | ⬜ pending |
| GARD-04 | 06-04 | 4 | Integrite de `.data/` | Empreinte de `.data/dofus.sqlite3` identique autour de la suite complete ; aucune connexion reseau ; `main()` jamais execute | unit + mesure d'empreinte | suite entiere encadree par deux empreintes | ❌ W0 | ⬜ pending |
| GARD-04 | 06-04 | 4 | Audit de perimetre | `git status` est consigne **avec sa portee reelle** (la recherche a mesure que `.gitignore` et `.planning/config.json` sont deja modifies avant la phase) - divergence declaree, jamais masquee | unit (lecture de `git status`) | suite entiere + `git status --porcelain` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_docs_depannage.py` - controle message -> rubrique (06-01)
- [ ] `tests/test_docs_glossaire.py` - controle des entrees et du tri (06-02)
- [ ] controle de completude : liste epinglee des 8 pages + ensemble exact des fichiers de `docs/` (06-03)
- [ ] test de mutation du harnais sur copie `tmp_path` (06-04)
- [ ] `docs/depannage.md`, `docs/glossaire.md` + leurs lignes d'index (livrables, pas des tests)

**Aucune installation requise** : pytest 9.1.1 est deja present et configure.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Rendu Markdown hors GitHub | AIDE-01, AIDE-02 | Le rendu d'un autre moteur Markdown n'est pas observable en processus | Aucune : declare comme limite non verifiee dans `06-RESEARCH.md`, **aucune validation humaine revendiquee** |
| Comportement DOM/navigateur (clavier inactif) | AIDE-01 | Aucun navigateur n'est disponible | Le mecanisme est **mesure dans le code** (`autofocus`, refocus, garde sur `activeElement`) : la rubrique s'adosse au mecanisme reel, pas a un message inexistant |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s (batteries de morsures incluses)
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
