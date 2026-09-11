---
phase: "5"
slug: "base-locale-hors-ligne-et-resynchronisation"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-11"
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
>
> **Autorité de détail :** `05-RESEARCH.md` § `Validation Architecture` porte le tableau complet
> « comportement → commande automatisée → fichier existant ou Wave 0 » (17 lignes) et l'inventaire de
> ce qui est **déjà couvert** par une garde existante. Les lignes ci-dessous sont la projection de ce
> tableau au niveau des exigences de la phase ; elles sont renseignées au fil de l'exécution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest **9.1.1** (déclaré `>=8.0`), Python 3.14.7 (`.venv`) |
| **Config file** | `pyproject.toml` → `[tool.pytest.ini_options]` (`testpaths = ["tests"]`, `pythonpath = ["."]`, `filterwarnings`) — **aucune configuration à ajouter** |
| **Quick run command** | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_base_locale.py` |
| **Full suite command** | `./.venv/Scripts/python.exe -m pytest -q` |
| **Estimated runtime** | ~4 secondes (baseline mesurée : **205 passed**) |

**Shared fixtures** (`tests/conftest.py`, D-12 — à réutiliser, jamais recopier) : `app`, `client`,
`docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple`. La fixture `app`
construit sa **propre** base sous `tmp_path` : aucun test ne touche `.data/dofus.sqlite3`.

**Reference interpreter** : `./.venv/Scripts/python.exe` (D-15). Sans exécuter `main()`, sans écrire
sous `.data/`, sans lancer de synchronisation, sans connexion réseau.

---

## Sampling Rate

- **After every task commit:** Run `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_base_locale.py`
- **After every plan wave:** Run `./.venv/Scripts/python.exe -m pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** ~4 secondes (suite entière)

---

## Per-Task Verification Map

Projection des 5 critères de succès et de BASE-01→BASE-03 sur les 3 plans du ROADMAP.
Au moment du seed, `tests/test_docs_base_locale.py` **n'existe pas encore** (d'où ❌ W0) : c'est le
module que la phase crée. Les deux dernières lignes s'appuient sur des gardes **existantes**.

| Req ID | Plan | Wave | Requirement | Behavior | Test Type | Automated Command | File Exists | Status |
|--------|------|------|-------------|----------|-----------|-------------------|-------------|--------|
| BASE-01 | 01 | 1 | Fichier et catégories | Le nom du fichier et les catégories cités par la page sont produits par le code (nom du fichier depuis sa constante, catégories depuis le schéma/les écrivains) | unit (constantes + schéma) | `… -m pytest -q tests/test_docs_base_locale.py -k fichier_categories` | ❌ W0 | ⬜ pending |
| BASE-01 | 01 | 1 | Fenêtre de re-check 24 h | La fenêtre est citée depuis sa constante nommée, sans aucune valeur volatile | unit (constante) | `… -k fenetre_24h` | ❌ W0 | ⬜ pending |
| BASE-02 | 01 | 1 | Les deux défauts hors-ligne | Web hors-ligne par défaut **et** CLI en ligne par défaut (`--offline` requis) : les deux sont énoncés séparément, chacun avec le défaut réel du parseur | unit (défauts des parseurs) | `… -k hors_ligne` | ❌ W0 | ⬜ pending |
| BASE-02 | 01 | 1 | Champs de l'état de la base | Les noms de champs cités sont produits par le code, sans aucune valeur volatile (date, taille, compteur) | unit (constantes publiques / rendu) | `… -k champs_etat` | ❌ W0 | ⬜ pending |
| BASE-03 | 02 | 2 | `db status` crée le fichier | Le comportement est décrit tel quel et prouvé **hors `.data/`** (répertoire temporaire) | unit (chemin temporaire) | `… -k db_status` | ❌ W0 | ⬜ pending |
| BASE-03 | 02 | 2 | `db sync` refuse `--offline` | Le refus est cité avec son **message réel** lu dans le code | unit (message du code) | `… -k db_sync_offline` | ❌ W0 | ⬜ pending |
| BASE-03 | 02 | 2 | Synchro web hors-ligne | Le fait que l'écran web contacte l'API **même hors-ligne** est dit, et adossé au code | unit (chemin de code) | `… -k synchro_web` | ❌ W0 | ⬜ pending |
| BASE-03 | 02 | 2 | Commandes destructrices | `db clear` et `PURGE OUI` sont signalées destructrices **sur la même ligne** et n'apparaissent dans aucun parcours | unit (analyse de la page) | `… -k destructrices` | ❌ W0 | ⬜ pending |
| BASE-03 | 03 | 3 | Ancrage des noms | Chaque nom cité par la page est retrouvé dans le code (constante publique ou rendu) | unit (ancrage) | `… -k ancrage` | ❌ W0 | ⬜ pending |
| BASE-03 | 03 | 3 | Intégrité et réseau | Les contrôles n'écrivent pas sous `.data/`, n'exécutent aucune synchronisation et n'ouvrent aucune connexion réseau ; empreinte de `.data/dofus.sqlite3` identique autour de la suite entière | unit + mesure d'empreinte | `… -k integrite` puis suite entière | ❌ W0 | ⬜ pending |
| BASE-03 | 03 | 3 | Renvois de `README.md` | Les renvois de `README.md` pointent vers des fichiers qui existent (D-87) | unit (disque) | `… -k readme` | ❌ W0 | ⬜ pending |
| BASE-01 | 01 | 1 | Sommaire et structure | L'index gagne une seule ligne, `H1` = libellé d'index, ligne de retour, encodage CRLF/UTF-8 sans BOM | unit (garde existante) | `… -m pytest -q tests/test_docs_structure.py` | ✅ `tests/test_docs_structure.py` | ⬜ pending |
| BASE-01 | 01 | 1 | Lien légitime vers la nouvelle page | La réserve de pages inexistantes est réduite : le lien vers la page désormais créée est **légitime** et contrôlé | unit (garde existante) | `… -m pytest -q tests/test_docs_parcours.py` | ✅ `tests/test_docs_parcours.py` | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_docs_base_locale.py` — module d'ancrage de la page (fichier et catégories, fenêtre 24 h, deux défauts hors-ligne, champs d'état, cas non évidents, commandes destructrices, ancrage des noms, intégrité et réseau, renvois du `README.md`)
- [ ] `tests/test_docs_parcours.py` — **modification obligatoire hors du module neuf** : la réserve `PAGES_INEXISTANTES` (aujourd'hui `("base-locale.md",)`) doit être réduite **dans le même commit** que la création de la page, sinon le contrôle du lien légitime rougit dès que `docs/base-locale.md` existe (patron posé en phase 4 pour `wizard-avance.md`)
- [ ] **Garde `ast` à réécrire, pas à recopier** : celle de la phase 4 interdit l'import de `dofus_stuff.database` — précisément la source de cette page. Le risque est **déplacé**, pas supprimé : aucune confirmation destructive (`"confirm"` ∈ {`O`,`Y`,`OUI`,`YES`}), jamais le répertoire de données par défaut en argument
- [ ] `docs/base-locale.md` + sa ligne d'index dans `docs/sommaire.md` (livrables de la phase, pas des tests)

**Aucune installation de framework requise** : `pytest` 9.1.1 est déjà présent et configuré dans
`pyproject.toml`. Wave 0 ne crée que des fichiers de documentation et de test.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Exécution JavaScript de `PURGE OUI` dans un navigateur réel | BASE-03 | La confirmation vit dans le `localStorage` du navigateur : son exécution n'est pas observable en processus. **Ce n'est pas un critère de succès** — le critère 4 porte sur l'**avertissement sur la même ligne**, qui est, lui, automatisé | Aucune : hors surface automatisée, déclaré comme tel dans `05-RESEARCH.md` (`## Claims non vérifiées`), **aucune validation humaine revendiquée** |

*Le critère 4 est prouvé automatiquement (avertissement sur la même ligne, hors parcours). Aucune
vérification humaine n'est revendiquée pour cette phase.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
