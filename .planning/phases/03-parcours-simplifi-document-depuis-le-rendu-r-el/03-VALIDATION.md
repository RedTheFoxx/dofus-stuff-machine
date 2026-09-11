---
phase: "3"
slug: "parcours-simplifi-document-depuis-le-rendu-r-el"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-11"
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest` 9.1.1 (déclaré `>=8.0`) — déjà installé, aucune dépendance à ajouter |
| **Config file** | `pyproject.toml` § `[tool.pytest.ini_options]` — `testpaths = ["tests"]`, `pythonpath = ["."]` |
| **Quick run command** | `.venv/Scripts/python.exe -m pytest -q` |
| **Full suite command** | `.venv/Scripts/python.exe -m pytest -q` (identique : aucun marqueur de sélection dans le dépôt) |
| **Estimated runtime** | ~2,6 s pour 169 tests ; budget du module ajouté : **< 1 s** |

**Interdit mesuré :** rendre le résultat sur la base réelle coûte ~9,5 s **et n'est pas déterministe** (deux exécutions → 6 puis 7 pages, deux méthodes). Tout ancrage sur `Méthode` ou sur le nombre de pages passe par la **fixture minimale** (déterministe, 0,29 s puis 0,02 s).

---

## Sampling Rate

- **After every task commit:** `.venv/Scripts/python.exe -m pytest -q`
- **After every plan wave:** `.venv/Scripts/python.exe -m pytest -q`
- **Before `/gsd:verify-work`:** suite entière verte (169 + les nouveaux tests) **et** mesure de non-régression `.data/` rejouée (V15)
- **Max feedback latency:** ~3 s

---

## Truths → Falsifying Control

| # | Vérité à prouver (critère ROADMAP) | Contrôle | Falsifiable ? |
|---|-----------------------------------|----------|---------------|
| V1 | Les trois questions et `AVANCE : personnaliser les réglages` sont rendues telles quelles (critère 1) | Rendre `GET /optimize/quick/classe` puis deux `POST` valides ; exiger dans les **lignes du corps** (normalisées, D-11) `1/3 - Quelle est votre classe ?`, `2/3 - Quels éléments privilégier ?`, `3/3 - Quel est votre niveau ? (1 à 200)`, `AVANCE : personnaliser les réglages` | Oui — retirer la ligne `AVANCE` (`routes.py:1003`) ou renommer une question ⇒ rouge |
| V2 | Les entrées citées sont réellement acceptées (critère 1) | Pour chaque entrée citée (`Cra`, `crâ`, `1`, `19`, `terre air`, `terre,air`, `terre+air`, `1 3`, `multi`, `150`) : `POST` ⇒ `302` vers l'étape attendue | Oui — une entrée inventée ⇒ `200` + message d'erreur ⇒ rouge |
| V3 | Les refus réels le sont, avec le message exact (critère 1) | `POST` d'une valeur refusée ⇒ `200`, ligne de statut commençant par le message attendu (`Saisissez le nom ou le numéro de votre classe.`, `Exemple : feu, terre air, ou multi.`, `Saisissez un niveau entre 1 et 200.`) | Oui — reformuler un message ⇒ rouge |
| V4 | Couple numéro ↔ libellé des deux menus (critère 5) | Extraire les couples **du rendu** (classe : 19, éléments : 4), comparer **section par section** aux couples cités par la page | Oui, **prouvé** — 6 mutations mesurées ⇒ rouges, page non mutée verte |
| V5 | Carte de pagination, forme rendue (critère 2) | Sur l'écran de résultat : `PAGE 1/{total} — ENTREE=VALIDER` dans la ligne de statut, `data-body-total` cohérent, atteinte de `PAGE {total}/{total}` | Oui — retirer `indicators.append(f"PAGE {page}/{total}")` (`routes.py:145`) ⇒ rouge |
| V6 | Les trois diagnostics sont en **fin** de résultat (critère 2) | Concaténer les pages dans l'ordre : `Méthode : `, `Score : `, `Indice de recherche : ` après le dernier `Équipement :` et avant `Greedy: `, avec `Recherche sur une sélection du catalogue ; optimalité globale non garantie.` juste après | Oui — déplacer `lines.extend(diagnostics)` (`api.py:432`) ⇒ rouge |
| V7 | Libellés de slot et leur nom complet (critère 2, **reformulé** par ÉCR-1) | Pour chaque libellé rendu par `api.py:362-380` présent dans la table de la page : exiger le libellé **et** son nom complet ; exiger que `api.py` porte bien `display_slots` | Oui — retirer un slot ou une ligne de table ⇒ rouge |
| V8 | Écrans de sauvegarde/export et leurs libellés (critère 3) | `GET /saves` ⇒ `SAV-01`, corps `CHARGEMENT DES SAUVEGARDES LOCALES…`, statut `N OUVRIR \| DEL N \| PURGE OUI` ; écran de résultat ⇒ statut contenant `SAVE [NOM]`, `SAVES`, `DB` et `data-mode="result"` | Oui — changer une ligne de statut ⇒ rouge |
| V9 | `MAX_SAVES = 20` et la clé de stockage (critère 3) | Ancrage **source** : `terminal.js:15` (`MAX_SAVES = 20`) et `:14` (clé `dofus-stuff-machine.saves`) ; la page cite le `20` et la clé | Oui — passer `MAX_SAVES` à 50 ⇒ rouge. ⚠ **contrôle de présence de littéral, pas d'exécution** |
| V10 | Export Dofusbook : URL, 10 groupes, `prysma` exclu (critère 3) | `build_dofusbook_url` est publique et pure : URL pour un dict connu, décodée (`base64`+`msgpack`), exiger `counts`, l'ordre plat et l'**absence** de `prysma`. **Réutiliser** `tests/test_web.py:713-750` (D-12) | Oui — réordonner `_GROUP_SLOTS` ⇒ rouge (`test_web.py` le prouve déjà) |
| V11 | Capital `5 * (level - 1)` et paliers PA/PM (critère 4) | Lire les littéraux `recommend.py:24,35,36` et exiger que la page cite `5`, `40`, `100`, `150` avec les cibles `8/10/11` et `4/5/6` | Oui — décaler un seuil ⇒ rouge |
| V12 | Les heuristiques de classe existent et sont nommées (critère 4, **confirmé par ÉCR-3**) | Exiger dans `recommend.py` les ensembles distance/mêlée, `Portée` (2/4 selon le niveau), `Invocation` (base 1, cible 3) ; page cohérente | Oui — retirer un ensemble ⇒ rouge |
| V13 | « sans exo/parchemins » et « sélection du catalogue » (critère 4) | Littéraux `api.py:316` et `api.py:434` exigés (normalisés) dans la page | Oui — reformuler la phrase rendue ⇒ rouge |
| V14 | Le sommaire liste la page et reste exhaustif dans les deux sens | Tests de la phase 1 déjà en place : `test_sommaire_lists_every_document`, `test_h1_matches_sommaire_entry`, `test_pages_have_back_link`, `test_all_relative_links_resolve` | Oui — ajouter la page sans sa ligne d'index ⇒ rouge (aucune exception, D-39) |
| V15 | Aucune écriture sous `.data/`, aucun réseau, aucun `main()` | (a) `mtime_ns` + taille + SHA-256 du fichier avant/après la suite ; (b) le module de test n'importe pas `dofus_stuff.database` | Oui — un test qui ouvre `.data/` ⇒ le SHA change ou l'import est détecté |

### Vérités non falsifiables — assumées, pas maquillées

- **Comportement JS** de la sauvegarde (éviction silencieuse, compteur, statuts) : aucun moteur JS disponible. V9 est un contrôle de **littéral source** et doit être nommé comme tel — il prouve que la page et le code ne divergent pas sur la **constante**, pas le comportement.
- **Formulation du H1** : libre (Claude's Discretion) ; seule la correspondance H1 ↔ libellé d'index est testable.

---

## Per-Task Verification Map

Les identifiants de tâche sont posés par les plans ; chaque plan doit fournir un `<automated>` par tâche et un `<fails_when>` nommant le signal d'échec.

| Réf | Plan (esquisse ROADMAP) | Vague | Requirement | Test Type | Automated Command | File Exists | Status |
|-----|------------------------|-------|-------------|-----------|-------------------|-------------|--------|
| V1–V4 | 03-01 les trois questions et le menu réel | 1 | SIMP-01 | rendu (Flask `test_client`) | `.venv/Scripts/python.exe -m pytest tests/test_docs_parcours.py -q` | ❌ Wave 0 | ⬜ pending |
| V5–V7 | 03-02 lire le résultat | 2 | SIMP-02 | rendu + injection de session | idem | ❌ Wave 0 | ⬜ pending |
| V8–V10 | 03-03 sauvegarder et exporter | 3 | SIMP-03 | rendu + lecture source | idem | ❌ Wave 0 | ⬜ pending |
| V11–V13 | 03-04 hypothèses, limites, contrôles de rendu | 4 | SIMP-04 | lecture source ancrée | idem | ❌ Wave 0 | ⬜ pending |
| V14 | transverse | — | SOMM-02 / SOMM-03 (phase 1) | structure | `.venv/Scripts/python.exe -m pytest tests/test_docs_structure.py -q` | ✅ existant — doit rester vert | ⬜ pending |
| V15 | transverse | — | GARD-02 (phase 1) | structure + mesure | `.venv/Scripts/python.exe -m pytest tests/test_docs_code_anchor.py -q` | ✅ existant | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_docs_parcours.py` — couvre SIMP-01…SIMP-04 et le critère 5
- [ ] `docs/parcours-simplifie.md` — la page elle-même (sans elle, la moitié des contrôles est rouge par construction)
- [ ] `docs/sommaire.md` — une ligne d'index + le H1 correspondant (V14)
- [ ] **Aucune** installation : `flask`, `pytest`, `ortools`, `msgpack` sont déjà présents
- [ ] **Aucune** promotion de helper vers `tests/conftest.py` : les helpers utiles y sont déjà (`normalize`, scanner de blocs, `sections`, `ligne_de_code`, `_section(texte, titre, page)`) ; en promouvoir un nouveau dupliquerait `_texte_page`

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| — | — | Aucune | — |

*Toutes les vérités de la phase ont un contrôle automatisé, ou sont explicitement listées comme non falsifiables ci-dessus. Aucune validation manuelle n'est requise — et aucune n'est revendiquée.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
