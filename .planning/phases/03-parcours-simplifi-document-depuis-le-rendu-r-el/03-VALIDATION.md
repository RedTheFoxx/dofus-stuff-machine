---
phase: "3"
slug: "parcours-simplifi-document-depuis-le-rendu-r-el"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
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
| **Measured runtime** | base hors phase : **169 tests** en 2,57 s (planification) puis 4,73 s (re-vérification, autre horloge machine) ; phase close : **186 tests** en 4,32–5,23 s ; module seul (`tests/test_docs_parcours.py`) : **17 tests en 0,88–1,10 s** |

**Interdit mesuré :** rendre le résultat sur la base réelle coûte ~9,5 s **et n'est pas déterministe** (deux exécutions → 6 puis 7 pages, deux méthodes). Tout ancrage sur `Méthode` ou sur le nombre de pages passe par la **fixture minimale** (déterministe, 0,29 s puis 0,02 s).

---

## Sampling Rate

- **After every task commit:** `.venv/Scripts/python.exe -m pytest -q`
- **After every plan wave:** `.venv/Scripts/python.exe -m pytest -q`
- **Before `/gsd:verify-work`:** suite entière verte (**186 tests**) **et** mesure de non-régression `.data/` rejouée (V15)
- **Max feedback latency:** ~5 s mesuré pour la suite entière sur cette machine (chiffre **mesuré**, pas budgété : voir RF-4 dans `03-REVIEW-FIX.md`)

---

## Truths → Falsifying Control

| # | Vérité à prouver (critère ROADMAP) | Contrôle | Falsifiable ? |
|---|-----------------------------------|----------|---------------|
| V1 | Les trois questions et `AVANCE : personnaliser les réglages` sont rendues telles quelles (critère 1) | Rendre `GET /optimize/quick/classe` puis deux `POST` valides ; exiger dans les **lignes du corps** (normalisées, D-11) `1/3 - Quelle est votre classe ?`, `2/3 - Quels éléments privilégier ?`, `3/3 - Quel est votre niveau ? (1 à 200)`, `AVANCE : personnaliser les réglages` | Oui — retirer la ligne `AVANCE` (`routes.py:1003`) ou renommer une question ⇒ rouge |
| V2 | Les entrées citées sont réellement acceptées (critère 1) | Pour chaque entrée citée (`Cra`, `crâ`, `1`, `19`, `terre air`, `terre,air`, `terre+air`, `1 3`, `multi`, `150`) : `POST` ⇒ `302` vers l'étape attendue | Oui — une entrée inventée ⇒ `200` + message d'erreur ⇒ rouge |
| V3 | Les refus réels le sont, avec le message exact (critère 1) | `POST` d'une valeur refusée ⇒ `200`, ligne de statut commençant par le message attendu (`Saisissez le nom ou le numéro de votre classe.`, `Exemple : feu, terre air, ou multi.`, `Saisissez un niveau entre 1 et 200.`) | Oui — reformuler un message ⇒ rouge |
| V4 | Couple numéro ↔ libellé des deux menus (critère 5) | Extraire les couples **du rendu** (classe : 19, éléments : 4), comparer **section par section** aux couples cités par la page | Oui, **prouvé** — 6 mutations mesurées ⇒ rouges, page non mutée verte |
| V5 | Carte de pagination, forme rendue (critère 2) | Sur l'écran de résultat : `PAGE 1/{total} — ENTREE=VALIDER` dans la ligne de statut, `data-body-total` cohérent, atteinte de `PAGE {total}/{total}` | Oui — retirer `indicators.append(f"PAGE {page}/{total}")` (`routes.py:145`) ⇒ rouge |
| V6 | Les trois diagnostics sont en **fin** de résultat (critère 2) | Concaténer les pages dans l'ordre : `Méthode : `, `Score : `, `Indice de recherche : ` après le dernier `Équipement :` et avant `Greedy: `, avec `Recherche sur une sélection du catalogue ; optimalité globale non garantie.` juste après | Oui — déplacer `lines.extend(diagnostics)` (`api.py:433`) ⇒ rouge |
| V7 | Libellés de slot et leur nom complet (critère 2, **reformulé** par ÉCR-1) | Pour chaque libellé rendu par `api.py:362-380` présent dans la table de la page : exiger le libellé **et** son nom complet ; exiger que `api.py` porte bien `display_slots` | Oui — retirer un slot ou une ligne de table ⇒ rouge |
| V8 | Écrans de sauvegarde/export et leurs libellés (critère 3) | `GET /saves` ⇒ `SAV-01`, corps `CHARGEMENT DES SAUVEGARDES LOCALES…`, statut `N OUVRIR \| DEL N \| PURGE OUI` ; écran de résultat ⇒ statut contenant `SAVE [NOM]`, `SAVES`, `DB` et `data-mode="result"` | Oui — changer une ligne de statut ⇒ rouge |
| V9 | `MAX_SAVES = 20` et la clé de stockage (critère 3) | Ancrage **source** : `terminal.js:15` (`MAX_SAVES = 20`) et `:14` (clé `dofus-stuff-machine.saves`) ; la page cite le `20` et la clé | Oui — passer `MAX_SAVES` à 50 ⇒ rouge. ⚠ **contrôle de présence de littéral, pas d'exécution** |
| V10 | Export Dofusbook : URL, 10 groupes, `prysma` exclu (critère 3) | `build_dofusbook_url` est publique et pure : URL pour un dict connu, décodée (`base64`+`msgpack`), exiger `counts`, l'ordre plat et l'**absence** de `prysma`. **Réutiliser** `tests/test_web.py:713-750` (D-12) | Oui — réordonner `_GROUP_SLOTS` ⇒ rouge (`test_web.py` le prouve déjà) |
| V11 | Capital `5 * (level - 1)` et paliers PA/PM (critère 4) | Lire les littéraux `recommend.py:24,35,36` et exiger que la page cite `5`, `40`, `100`, `150` avec les cibles `8/10/11` et `4/5/6` | Oui — décaler un seuil ⇒ rouge |
| V12 | Les heuristiques de classe existent et sont nommées (critère 4, **confirmé par ÉCR-3**) | Exiger dans `recommend.py` les ensembles distance/mêlée, `Portée` (2/4 selon le niveau), `Invocation` (base 1, cible 3) ; page cohérente | Oui — retirer un ensemble ⇒ rouge |
| V13 | « sans exo/parchemins » et « sélection du catalogue » (critère 4) | Littéraux `api.py:316` et `api.py:434` exigés (normalisés) dans la page | Oui — reformuler la phrase rendue ⇒ rouge |
| V14 | Le sommaire liste la page et reste exhaustif dans les deux sens | Tests de la phase 1 déjà en place : `test_sommaire_lists_every_document`, `test_h1_matches_sommaire_entry`, `test_pages_have_back_link`, `test_all_relative_links_resolve` | Oui — ajouter la page sans sa ligne d'index ⇒ rouge (aucune exception, D-39) |
| V15 | Aucune écriture sous `.data/`, aucun réseau, aucun `main()` | (a) `mtime_ns` + taille + SHA-256 de `.data/dofus.sqlite3` relevés **avant et après la suite entière** (vérification du plan 03-04 ; le test de module ne fait qu'une **re-mesure locale**, la fixture `app` construisant sa propre base SQLite sous `tmp_path/data`) ; (b) garde `ast` du module : ni `dofus_stuff.database`, ni racine base/processus/socket/réseau, ni `main()`, ni suppression de fichier — y compris dans la **clôture transitive** de ses imports produit | Oui — un test qui ouvrirait `.data/` ⇒ le SHA change ; un import de la base, direct ou transitif ⇒ la garde rougit |

### Vérités non falsifiables — assumées, pas maquillées

- **Comportement JS** de la sauvegarde (éviction silencieuse, compteur, statuts) : aucun moteur JS disponible. V9 est un contrôle de **littéral source** et doit être nommé comme tel — il prouve que la page et le code ne divergent pas sur la **constante**, pas le comportement.
- **Formulation du H1** : libre (Claude's Discretion) ; seule la correspondance H1 ↔ libellé d'index est testable.

---

## Per-Task Verification Map

Les identifiants de tâche sont posés par les plans ; chaque plan doit fournir un `<automated>` par tâche et un `<fails_when>` nommant le signal d'échec.

| Réf | Plan | Vague | Requirement | Test Type | Automated Command | File Exists | Status |
|-----|------|-------|-------------|-----------|-------------------|-------------|--------|
| V1–V4 | 03-01 — les trois questions et le menu réel | 1 | SIMP-01 | rendu (Flask `test_client`) + morsures | `.venv/Scripts/python.exe -m pytest tests/test_docs_parcours.py -q` | ✅ créé — 7 tests au terme du plan | ✅ green |
| V5–V7 | 03-02 — lire le résultat et la correspondance des libellés | 2 | SIMP-02 | rendu + injection de session | idem | ✅ étendu — 9 tests | ✅ green |
| V8–V10 | 03-03 — sauvegarder et exporter | 3 | SIMP-03 | rendu + lecture de source (`ast`) | idem | ✅ étendu — 12 tests | ✅ green |
| V11–V13 | 03-04 — hypothèses, limites, clôture de page | 4 | SIMP-04 | lecture de source ancrée | idem | ✅ étendu — **17 tests** | ✅ green |
| V14 | transverse | — | SOMM-02 / SOMM-03 (phase 1) | structure | `.venv/Scripts/python.exe -m pytest tests/test_docs_structure.py -q` | ✅ existant — resté vert | ✅ green |
| V15 | transverse | — | GARD-02 (phase 1) + critère 5 | structure, mesure et garde `ast` | `.venv/Scripts/python.exe -m pytest tests/test_docs_code_anchor.py -q` puis suite entière | ✅ existant | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

### Contrôles livrés, par vérité

| Vérité | Test(s) qui la porte(nt) |
|--------|--------------------------|
| V1 | `test_trois_questions_et_avance_rendus`, `test_lignes_du_corps_ne_sont_pas_la_reponse_entiere` |
| V2, V3 | `test_entrees_citees_acceptees_et_refusees` |
| V4 | `test_couples_numeros_libelles_par_section`, `test_parcours_cli_ne_pose_pas_les_trois_questions` |
| V5, V6 | `test_pagination_et_emplacement_du_calcul` |
| V7 | `test_correspondance_libelles_slots`, `test_source_de_verite_et_chemins_cites` |
| V8 | `test_ecrans_de_sauvegarde_et_export` |
| V9, V10 | `test_sauvegarde_navigateur_et_export_dofusbook`, `test_aucun_post_db_sans_patch` |
| V11, V12, V13 | `test_hypotheses_prouvees_par_balayage`, `test_limites_ancrees_sur_le_code` |
| V14 | `test_page_complete_et_sans_derive` (module) + les quatre tests de structure de la phase 1 |
| V15 | `test_data_locale_non_modifiee_autour_des_rendus` (re-mesure locale) **+** la mesure au périmètre de la suite (avant/après `pytest -q`) |
| garde `ast` | `test_garde_ni_base_ni_processus_ni_reseau` |
| En-tête d'écran | `test_entete_des_trois_ecrans_de_questions_cite` |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/test_docs_parcours.py` — 17 tests, couvre SIMP-01…SIMP-04 et le critère 5
- [x] `docs/parcours-simplifie.md` — la page elle-même (269 lignes, 9 sections de niveau 2, CRLF sans BOM)
- [x] `docs/sommaire.md` — une ligne d'index + le H1 correspondant (V14)
- [x] **Aucune** installation : `flask`, `pytest`, `ortools`, `msgpack` étaient déjà présents
- [x] **Aucune** promotion de helper vers `tests/conftest.py` : les helpers utiles y étaient déjà (`normalize`, scanner de blocs, `sections`, `ligne_de_code`, `_section(texte, titre, page)`) — les nouveaux (`_touches`, `_lignes_du_corps`, `_couples_de_section`, `_attribut`, `_entete`…) sont restés **locaux au module** (D-12)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| — | — | Aucune | — |

*Toutes les vérités de la phase ont un contrôle automatisé, ou sont explicitement listées comme non falsifiables ci-dessus. Aucune validation manuelle n'est requise — et aucune n'est revendiquée.*

### Non falsifiables — déclarées, jamais maquillées

| Élément | Pourquoi aucun contrôle ne peut le falsifier | Ce que le contrôle prouve à la place |
|---------|----------------------------------------------|--------------------------------------|
| Comportement JS de la sauvegarde (éviction silencieuse au 21ᵉ enregistrement, compteur, statuts) | Aucun moteur JS n'est disponible dans cet environnement (pas de `localStorage`, pas de `shift`) | V9 : la page et le codebase ne divergent pas sur la **constante** (`MAX_SAVES`, clé de stockage) et sur les **libellés** ; la limite est écrite dans le module et dans la page |
| Comparaison octet à octet des blocs cités de la page avec le rendu | Les blocs cités sont des extraits choisis, pas des transcriptions intégrales | Les valeurs citées sont rejouées **individuellement** sur le rendu (V1–V3, V5, V8) |
| Équivalence « libellé technique ↔ mot affiché dans le jeu » | Non prouvable depuis le dépôt | Le nom complet est recopié de sa source **et** re-vérifié sur la ligne qui le porte |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies — **32 blocs `<automated>`**, chacun apparié à un `<fails_when>` (probe `verify-failure-directions` : 32/32 `ok`)
- [x] Sampling continuity: no 3 consecutive tasks without automated verify — 3/2/2/3 tâches, chacune avec au moins un `<automated>`
- [x] Wave 0 covers all MISSING references — aucun `MISSING` restant
- [x] No watch-mode flags — aucune invocation `pytest` en mode watch
- [x] Feedback latency < 5s — mesuré : 4,32–5,23 s pour la suite entière, 0,88–1,10 s pour le module
- [x] `nyquist_compliant: true` set in frontmatter

---

## Validation Audit 2026-09-11

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

**Ce qui a été vérifié plutôt que cru.** La phase est déclarée `nyquist_compliant: true` sur la base de mesures exécutées, pas sur la lecture des `SUMMARY` :

- suite entière **186 passed** (base 169 + 17), module `tests/test_docs_parcours.py` **17 passed**, aucun `skip` — les contrôles de la phase ont un effet observable, aucun n'est vert à vide ;
- la **vérification de phase** a rejoué sa propre batterie de **22 mutations sur copies jetables → 22/22 détectées**, chaque copie vérifiée verte avant sa mutation — c'est la preuve que les contrôles mordent, pas seulement qu'ils passent ;
- `.data/dofus.sqlite3` : empreinte (taille / `mtime_ns` / SHA-256) **identique avant et après la suite entière**, mesurée indépendamment du module ;
- douze des quinze vérités (V1–V13 hors V9) sont falsifiables par mutation, et leur mutation a été exécutée ; V9, V14 et V15 sont portées par des contrôles dont la **portée** est écrite (littéral, structure, mesure d'empreinte) ;
- deux contrôles à **portée plus étroite que leur formulation** ont été identifiés et ne sont pas comptés à la force annoncée : la garde `ast` (clôture **statique des imports produit**, pas la clôture d'exécution — importer `dofus_stuff.web.dofusbook_export` exécute `dofus_stuff/web/__init__.py` et charge `sqlite3`) et l'assertion de fin de ligne (elle mesure l'arbre de travail, pas le blob). Les deux sont portés au registre de sécurité (`03-SECURITY.md` § Limites connues L-1 et L-3) et à la revue de code (`03-REVIEW.md` WR-01) — vérifiés, chiffrés, **non** maquillés, et non bloquants pour les critères du ROADMAP, que la mesure d'empreinte et les 22 morsures couvrent directement.

**Approval:** verified 2026-09-11
