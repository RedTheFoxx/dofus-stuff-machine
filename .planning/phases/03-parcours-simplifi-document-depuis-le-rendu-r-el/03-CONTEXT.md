# Phase 3: Parcours simplifié documenté depuis le rendu réel - Context

**Gathered:** 2026-09-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Livrer `docs/parcours-simplifie.md` : la page qui permet à un lecteur de **dérouler le parcours guidé classe → éléments → niveau**, de **lire son résultat** et de **comprendre ce que l'outil suppose**. Chaque libellé, écran et message cité doit être **dérivé du rendu réel**, pas de la prose.

Dans le périmètre : la page `docs/parcours-simplifie.md`, son entrée dans `docs/sommaire.md`, et les contrôles pytest qui ancrent la page au rendu réel.

Hors périmètre : le wizard avancé (phase 4), la base locale et la fenêtre de 24 h (phase 5), le dépannage et le glossaire (phase 6), la correction de `GUIDE_WIZARD.md` (phase 4). Aucune modification de `dofus_stuff/**`, aucune dépendance nouvelle.

</domain>

<decisions>
## Implementation Decisions

### Source du rendu réel
- **D-32:** Les **écrans web** sont lus au travers du **client de test Flask, en processus** — patron déjà présent dans `tests/test_recommend.py` (`client.post("/optimize/quick/niveau", ...)`). Aucun serveur lancé, aucun socket, aucune écriture sous `.data/`. Les libellés, l'ordre des écrans et la carte de pagination sont dérivés de cette sortie réelle.
  — **Reversibility:** costly — Si le harnais se révélait incapable de rendre un écran sans effet de bord (résolution, base absente), la dérivation devrait être reprise sur les autres modules de la phase et sur la page déjà rédigée.
- **D-33:** Les **libellés des questions guidées CLI** ne sont **pas** obtenus en exécutant `main()` (D-15) : ils sont lus dans leur **module source** et ancrés par test, exactement comme les sondes de la phase 2.
- **D-34:** L'**assertion négative** du critère 5 (un numéro de menu associé au mauvais libellé doit être détecté) est construite sur la **correspondance réellement rendue** numéro ↔ libellé, obtenue de la même source que les libellés positifs — sinon le test ne détecterait pas l'inversion.
- **D-35:** Rappel de D-19 : **aucune sémantique inventée**. Tout libellé cité est réellement lu ; ce qui n'est pas lisible dans le code n'est pas affirmé.

### Périmètre de la page
- **D-36:** La page décrit **le parcours guidé tel que le lecteur le vit** ; les **écrans web sont la référence de rendu**, le parcours CLI est mentionné sans être redupliqué.
- **D-37:** La **surface de commandes reste propriété de `docs/cli.md`** (phase 2) : renvoi en prose, pas de recopie. C'est D-17 appliqué **entre deux pages** du même ensemble, pas seulement à l'intérieur d'une page.
- **D-38:** « **Lire le résultat** » et « **Sauvegarder et exporter** » (critère 3) sont des **sections de cette page**, rattachées à l'écran qui les expose — pas de page dédiée, pas de report : un report laisserait le critère 3 sans support.
- **D-39:** `docs/sommaire.md` gagne **l'entrée de cette page maintenant** (D-05) ; le test d'exhaustivité bidirectionnelle (D-06) reste vert sans exception ; `README.md` garde son **lien unique** vers le sommaire (D-10, D-29).

### Hypothèses et limites (critère 4)
- **D-40:** Chaque hypothèse de l'outil (points par niveau, paliers PA/PM, heuristiques de classe, ni exo ni parchemins) est présentée **avec la valeur réellement présente dans le code**, et un contrôle vérifie que cette valeur y figure encore — même logique que le bloc « Source de vérité » de la phase 1 et les sondes de la phase 2.
- **D-41:** Une limite qui ne serait **adossée à rien de lisible** est soit retirée, soit explicitement présentée comme une **interprétation du parcours lecteur** — jamais comme une vérité de code. La différence est visible dans la page.
- **D-42:** Aucune constante n'est écrite de mémoire : elle est lue à la rédaction, et le message d'échec cite **la page, la valeur attendue et le fichier de code** (D-13).

### Frontière avec les phases 4 et 5
- **D-43:** Cette page **ne re-décrit ni les écrans du wizard avancé (phase 4) ni le fonctionnement de la base locale (phase 5)** — D-17, une seule source par énoncé.
- **D-44:** Tant que `docs/wizard-avance.md` et `docs/base-locale.md` n'existent pas, le renvoi se fait **en prose, sans lien** (leçon mesurée en phase 2 : pas de lien mort). Le lien est **ajouté par la phase qui crée la page cible**, dans le même commit que la cible.

### Conventions réappliquées
- **D-45:** Les conventions des phases 1 et 2 s'appliquent sans modification : comparaisons **après normalisation** accents/casse/CRLF/HTML (D-11), helpers dans le `tests/conftest.py` **existant** (D-12), message d'échec citant page + libellé attendu + fichier de code (D-13), ancrage par **API publique** — parseur public et client de test Flask, jamais d'introspection privée (D-14) — et exécution de référence `.venv/Scripts/python.exe -m pytest -q`, **sans** exécuter `main()`, **sans** écrire sous `.data/`, **sans** connexion réseau (D-15). Gabarit de page : D-01 (H1 unique, intro, sections courtes, bloc « Source de vérité » avec chemins réellement existants, ligne de retour au sommaire).

### Claude's Discretion
- Découpage des sections et leur ordre, la formulation des titres et de l'introduction.
- Nom du module de test ajouté (module dédié aux côtés de `tests/test_docs_cli.py`, ou extension d'un module existant) — seule contrainte : ne pas dupliquer les helpers de `tests/conftest.py` (D-12).
- Forme de la table « libellé tronqué → nom complet de slot » et de la carte de pagination.
- Découpage interne des tests (classes ou fonctions).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Décisions de cadrage (antérieures, non négociables)
- `.planning/PROJECT.md` — core value, contraintes (français, lecture seule sous `.data/`, hors-ligne d'abord, aucun déploiement)
- `.planning/REQUIREMENTS.md` — SIMP-01, SIMP-02, SIMP-03, SIMP-04
- `.planning/ROADMAP.md` § `### Phase 3:` — objectif, 5 critères de succès, découpage indicatif en 4 plans
- `.planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-CONTEXT.md` — D-01 à D-15 (gabarit de page, sommaire qui croît par phase, conventions de test)
- `.planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-CONTEXT.md` — D-16 à D-31 (une seule source par énoncé, aucune sémantique inventée, conventions de test)
- `.claude/CLAUDE.md` — instructions projet (dont §2 / DOCS-06, écart déjà assumé et consigné en phase 2)

### Leçon de harnais mesurée en phase 2 (à ne pas reproduire)
- `.planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-REVIEW.md` — 5 avertissements corrigés (dont un **faux positif** et une **garde de sûreté manquante**) et 7 informations ouvertes ; la revue a montré que **les trous étaient dans le harnais, pas dans la page**

### Pages déjà livrées (formes à réutiliser, contenu à ne pas dupliquer)
- `docs/installation.md` — gabarit de référence : H1 unique, intro, section « erreurs fréquentes », bloc « Source de vérité »
- `docs/cli.md` — référence CLI : la surface de commandes y vit ; cette page y renvoie en prose (D-37)
- `docs/sommaire.md` — l'index qui gagne une entrée à cette phase

### Code source du rendu (source de vérité de cette phase)
- `dofus_stuff/web/routes.py` § `optimize_quick` (route `/optimize/quick/<step>`) — le parcours guidé côté web ; le libellé `AVANCE : personnaliser les réglages` y est rendu
- `dofus_stuff/web/optimize_wizard.py` — wizard avancé (frontière phase 4) et carte de pagination `PAGE {page}/{total_pages}`
- `dofus_stuff/web/dofusbook_export.py` — export Dofusbook (`build_dofusbook_url`, `DOFUSBOOK_IMPORT_URL`)
- `dofus_stuff/web/static/js/terminal.js` — sauvegardes navigateur (`MAX_SAVES = 20`, clé `localStorage`)
- `dofus_stuff/web/screens.py` — écrans du terminal
- `dofus_stuff/optimize/api.py` — rendu du résultat : `Méthode :`, `Score :`, `Indice de recherche :`, et la ligne d'hypothèse « Points inclus ; sans exo/parchemins. Jets moyens sauf réglage avancé. »
- `dofus_stuff/optimize/recommend.py` — paliers PA/PM (`pa = 6 if level < 40 else 8 if level < 100 else 10 if level < 150 else 11`, idem `pm`)
- `dofus_stuff/optimize/profile_input.py` — questions guidées du CLI (libellés lus, pas exécutés)
- `dofus_stuff/model/solver_spec.py` — `Score Stuffer`, groupes de buts, `exo` / `scroll`

### Tests existants à imiter (patrons mesurés)
- `tests/test_recommend.py` — **patron du client de test Flask** pour le parcours guidé ; `parametrize` sur les niveaux 1/39/40/99/100/149/150/200
- `tests/test_web.py` — patron de test d'écrans
- `tests/conftest.py` — fixtures partagées (`normalize`, scanner de blocs, helpers de section `_section(texte, titre, page)`)
- `tests/test_docs_structure.py` — invariants structurels du `docs/` (liens, sommaire, H1)
- `tests/test_docs_cli.py` — forme des contrôles d'ancrage page → code (sonde d'argv, `format_help()`, constats accumulés en une seule assertion)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Client de test Flask** : `tests/test_recommend.py` poste déjà `/optimize/quick/niveau` avec `cmd=AVANCE` et `follow_redirects=True` — le patron de rendu demandé par D-32 existe et est éprouvé.
- **Route du parcours guidé** : `@bp.route("/optimize/quick/<step>")` → `optimize_quick(step)` dans `dofus_stuff/web/routes.py` ; le libellé `AVANCE : personnaliser les réglages` est ajouté au corps rendu.
- **Rendu du résultat** : `dofus_stuff/optimize/api.py` produit déjà les trois lignes que le critère 2 exige de localiser (`Méthode :`, `Score :`, `Indice de recherche :`) et porte la ligne d'hypothèses du critère 4.
- **Paliers PA/PM** : `dofus_stuff/optimize/recommend.py` contient les seuils 40 / 100 / 150 et les valeurs 6/8/10/11 (PA) et 3/4/5/6 (PM) — lus, jamais recopiés de mémoire (D-40).
- **Sauvegardes navigateur** : `MAX_SAVES = 20` et la clé de stockage vivent dans `dofus_stuff/web/static/js/terminal.js`.
- **Export Dofusbook** : `dofus_stuff/web/dofusbook_export.py` expose l'URL d'import et l'ordre des 10 groupes de slots.

### Established Patterns
- **Une seule source par énoncé** (D-17) : la surface de commandes reste dans `docs/cli.md` ; cette page renvoie en prose.
- **Le sommaire croît par phase** (D-05) : une entrée par page livrée, exhaustivité bidirectionnelle testée.
- **Ancrage par API publique** (D-14) : parseur public et client de test Flask ; jamais d'API privée.
- **Constats accumulés, une seule assertion par test** : forme retenue en phase 2 parce qu'une assertion par constat rendait des motifs inatteignables et faisait échouer la batterie sur une implémentation correcte.
- **Pages `docs/` en CRLF, UTF-8 sans BOM** : convention mesurée, à préserver à l'écriture.

### Integration Points
- `docs/sommaire.md` — la nouvelle page s'y branche (parcours guidé ordonné + table d'index).
- `tests/conftest.py` — les helpers partagés s'y étendent, jamais dupliqués.
- `docs/cli.md` — frontière explicite : renvoi en prose, pas de recopie de la surface de commandes.
- Les phases 4 et 5 **lieront** cette page depuis `docs/wizard-avance.md` et `docs/base-locale.md` (D-44).

</code_context>

<specifics>
## Specific Ideas

- Le titre de la phase — « depuis le rendu réel » — est une **contrainte de méthode**, pas un slogan : ce qui est cité doit venir de ce qui est rendu, et le critère 5 exige une **assertion négative** dérivée de la même source.
- Le lecteur doit pouvoir **retrouver où vivent `Méthode`, `Score` et `Indice de recherche`** (dernière page) et savoir traduire un **libellé de slot tronqué** en nom complet — deux points où un lecteur se perd réellement.
- Les hypothèses doivent être **visibles comme telles** : le lecteur doit comprendre que l'indice de recherche n'est pas une qualité en combat et que la recherche porte sur une **sélection** du catalogue.
- L'ordre de lecture retenu pour la page : les trois questions d'abord, puis « lire le résultat », puis « sauvegarder et exporter », puis « ce que l'outil suppose » et « ce que l'outil ne fait pas ».

</specifics>

<deferred>
## Deferred Ideas

- Les écrans détaillés du **wizard avancé** (slots/filtres, options solveur, caractéristiques, PA/PM/PO, résistances, dommages, divers, items interdits/forcés, récapitulatif) et la résorption de la dette `GUIDE_WIZARD.md` → **phase 4**.
- Le fichier `.data/dofus.sqlite3`, les catégories d'objets et la **fenêtre de re-check de 24 h** → **phase 5** (dont le plan 05-01 rédigera `docs/base-locale.md`).
- La **FAQ / dépannage** et le **glossaire** → **phase 6**.
- La **liste épinglée des 8 pages** du sommaire → **phase 6**, quand toutes les cibles existent (D-05).

</deferred>

---

*Phase: 3-Parcours simplifié documenté depuis le rendu réel*
*Context gathered: 2026-09-11*
