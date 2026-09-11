# Phase 3: Parcours simplifié documenté depuis le rendu réel - Research

**Researched:** 2026-09-11
**Domain:** Page Markdown `docs/parcours-simplifie.md` dérivée du **rendu réel** de l'interface Flask (client de test en processus), ancrée par `pytest` — zéro dépendance nouvelle, zéro écriture sous `.data/`
**Confidence:** HIGH pour toute la surface mesurée (libellés, entrées acceptées, messages d'erreur, constantes, pagination, export) ; **les mesures ont été obtenues en exécutant réellement le code produit en processus**, avec l'interpréteur épinglé `.venv/Scripts/python.exe` — jamais en inférant depuis une recherche textuelle. Deux points sont explicitement **non adossés** au code et sont signalés en section dédiée (§ « Écarts avec les critères du ROADMAP ») : la « table libellé tronqué → nom complet de slot » du critère 2 et la formulation « dernière page » du même critère.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Source du rendu réel
- **D-32:** Les **écrans web** sont lus au travers du **client de test Flask, en processus** — patron déjà présent dans `tests/test_recommend.py` (`client.post("/optimize/quick/niveau", ...)`). Aucun serveur lancé, aucun socket, aucune écriture sous `.data/`. Les libellés, l'ordre des écrans et la carte de pagination sont dérivés de cette sortie réelle.
  — **Reversibility:** costly — Si le harnais se révélait incapable de rendre un écran sans effet de bord (résolution, base absente), la dérivation devrait être reprise sur les autres modules de la phase et sur la page déjà rédigée.
- **D-33:** Les **libellés des questions guidées CLI** ne sont **pas** obtenus en exécutant `main()` (D-15) : ils sont lus dans leur **module source** et ancrés par test, exactement comme les sondes de la phase 2.
- **D-34:** L'**assertion négative** du critère 5 (un numéro de menu associé au mauvais libellé doit être détecté) est construite sur la **correspondance réellement rendue** numéro ↔ libellé, obtenue de la même source que les libellés positifs — sinon le test ne détecterait pas l'inversion.
- **D-35:** Rappel de D-19 : **aucune sémantique inventée**. Tout libellé cité est réellement lu ; ce qui n'est pas lisible dans le code n'est pas affirmé.

#### Périmètre de la page
- **D-36:** La page décrit **le parcours guidé tel que le lecteur le vit** ; les **écrans web sont la référence de rendu**, le parcours CLI est mentionné sans être redupliqué.
- **D-37:** La **surface de commandes reste propriété de `docs/cli.md`** (phase 2) : renvoi en prose, pas de recopie. C'est D-17 appliqué **entre deux pages** du même ensemble, pas seulement à l'intérieur d'une page.
- **D-38:** « **Lire le résultat** » et « **Sauvegarder et exporter** » (critère 3) sont des **sections de cette page**, rattachées à l'écran qui les expose — pas de page dédiée, pas de report : un report laisserait le critère 3 sans support.
- **D-39:** `docs/sommaire.md` gagne **l'entrée de cette page maintenant** (D-05) ; le test d'exhaustivité bidirectionnelle (D-06) reste vert sans exception ; `README.md` garde son **lien unique** vers le sommaire (D-10, D-29).

#### Hypothèses et limites (critère 4)
- **D-40:** Chaque hypothèse de l'outil (points par niveau, paliers PA/PM, heuristiques de classe, ni exo ni parchemins) est présentée **avec la valeur réellement présente dans le code**, et un contrôle vérifie que cette valeur y figure encore — même logique que le bloc « Source de vérité » de la phase 1 et les sondes de la phase 2.
- **D-41:** Une limite qui ne serait **adossée à rien de lisible** est soit retirée, soit explicitement présentée comme une **interprétation du parcours lecteur** — jamais comme une vérité de code. La différence est visible dans la page.
- **D-42:** Aucune constante n'est écrite de mémoire : elle est lue à la rédaction, et le message d'échec cite **la page, la valeur attendue et le fichier de code** (D-13).

#### Frontière avec les phases 4 et 5
- **D-43:** Cette page **ne re-décrit ni les écrans du wizard avancé (phase 4) ni le fonctionnement de la base locale (phase 5)** — D-17, une seule source par énoncé.
- **D-44:** Tant que `docs/wizard-avance.md` et `docs/base-locale.md` n'existent pas, le renvoi se fait **en prose, sans lien** (leçon mesurée en phase 2 : pas de lien mort). Le lien est **ajouté par la phase qui crée la page cible**, dans le même commit que la cible.

#### Conventions réappliquées
- **D-45:** Les conventions des phases 1 et 2 s'appliquent sans modification : comparaisons **après normalisation** accents/casse/CRLF/HTML (D-11), helpers dans le `tests/conftest.py` **existant** (D-12), message d'échec citant page + libellé attendu + fichier de code (D-13), ancrage par **API publique** — parseur public et client de test Flask, jamais d'introspection privée (D-14) — et exécution de référence `.venv/Scripts/python.exe -m pytest -q`, **sans** exécuter `main()`, **sans** écrire sous `.data/`, **sans** connexion réseau (D-15). Gabarit de page : D-01 (H1 unique, intro, sections courtes, bloc « Source de vérité » avec chemins réellement existants, ligne de retour au sommaire).

### Claude's Discretion
- Découpage des sections et leur ordre, la formulation des titres et de l'introduction.
- Nom du module de test ajouté (module dédié aux côtés de `tests/test_docs_cli.py`, ou extension d'un module existant) — seule contrainte : ne pas dupliquer les helpers de `tests/conftest.py` (D-12).
- Forme de la table « libellé tronqué → nom complet de slot » et de la carte de pagination.
- Découpage interne des tests (classes ou fonctions).

### Deferred Ideas (OUT OF SCOPE)
- Les écrans détaillés du **wizard avancé** (slots/filtres, options solveur, caractéristiques, PA/PM/PO, résistances, dommages, divers, items interdits/forcés, récapitulatif) et la résorption de la dette `GUIDE_WIZARD.md` → **phase 4**.
- Le fichier `.data/dofus.sqlite3`, les catégories d'objets et la **fenêtre de re-check de 24 h** → **phase 5** (dont le plan 05-01 rédigera `docs/base-locale.md`).
- La **FAQ / dépannage** et le **glossaire** → **phase 6**.
- La **liste épinglée des 8 pages** du sommaire → **phase 6**, quand toutes les cibles existent (D-05).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (verbatim de `.planning/REQUIREMENTS.md`) | Research Support |
|----|--------------------------------------------------------|------------------|
| SIMP-01 | « Un lecteur peut ouvrir l'optimisation depuis le menu réel et dérouler les trois questions (classe → éléments → niveau), avec les entrées acceptées et les messages d'erreur réels — dérivé de DOCS-04 » | § M1 (entrée `/optimize` → `/optimize/quick/classe`), § M2 (corps rendus verbatim), § M3 (matrice d'entrées mesurée), § M4 (trois messages d'erreur réels + `AVANCE`) |
| SIMP-02 | « Un lecteur peut lire son résultat : pagination, emplacement réel des informations de calcul, correspondance des libellés abrégés à l'écran — dérivé de DOCS-04 » | § M6 (écran `OPT-03`, carte `PAGE {page}/{total}` en ligne de statut, bloc de diagnostics en fin de résultat), § M7 (largeur et troncature mesurées — la table « libellé tronqué » n'est **pas** adossée, voir § Écarts) |
| SIMP-03 | « Un lecteur peut sauvegarder un stuff dans son navigateur et l'exporter vers Dofusbook — dérivé de DOCS-04 » | § M8 (`MAX_SAVES = 20`, clé `localStorage`, éviction du plus ancien, écran `SAV-01`), § M9 (URL d'import, 10 groupes, `prysma` non exporté, route `DB` et route JSON) |
| SIMP-04 | « Un lecteur sait ce que l'outil suppose (répartition des points, paliers, heuristiques) et ce qu'il ne fait pas — dérivé de DOCS-04 » | § M10 (capital `5 * (level - 1)`, paliers PA/PM mesurés 40/100/150, heuristiques de classe **existantes**, exo/parchemins à zéro, `compute_compatibility`, préfiltrage du catalogue) |

### Success Criteria (verbatim de `.planning/ROADMAP.md` § Phase 3)

  1. Les trois questions et le libellé `AVANCE : personnaliser les réglages` sont cités tels qu'ils sont rendus, avec les entrées acceptées (nom ou numéro de classe, éléments et alias, séparateurs) et les messages d'erreur réels.
  2. Le lecteur sait lire son résultat : carte de pagination, emplacement réel de `Méthode`, `Score` et `Indice de recherche` (dernière page), et table de correspondance libellé tronqué → nom complet de slot.
  3. La sauvegarde navigateur (20 sauvegardes maximum) et l'export Dofusbook sont décrits et rattachés à l'écran qui les expose.
  4. Les hypothèses de l'outil (points par niveau, paliers PA/PM 40/100/150, heuristiques de classe, ni exo ni parchemins) et ses limites (« indice de recherche » ≠ qualité en combat, recherche sur une sélection du catalogue) sont explicites.
  5. Le contrôle détecte un numéro de menu associé au mauvais libellé (assertion négative dérivée du rendu réel) et la suite reste verte.
</phase_requirements>

## Project Constraints (from CLAUDE.md)

Source : `./.claude/CLAUDE.md` (il n'existe pas de `CLAUDE.md` à la racine du dépôt — vérifié). Directives actionnables pour cette phase :

| # | Directive (citation) | Conséquence pour la phase 3 |
|---|----------------------|-----------------------------|
| C1 | « **Technique** : Python 3.11+, package `dofus_stuff`, pytest comme seul outillage de vérification — pas de nouvelle dépendance pour la documentation. » | Aucun paquet à installer ; l'audit de légitimité est vide (voir § Package Legitimacy Audit) |
| C2 | « **Langue** : documentation intégralement en français ; le code, les chemins et les identifiants techniques restent inchangés. » | La page et ses titres sont en français ; les libellés d'écran sont cités **tels quels**, accents compris (`RECOMMANDATION DE STUFF`, `AVANCE : personnaliser les réglages`) |
| C3 | « **Données** : lecture seule sur `.data/` — jamais de `db clear`, de drop SQLite ni de suppression sous `.data/`. » | Le harnais n'ouvre **pas** `.data/` (mesure M12) ; il utilise la fixture de catalogue |
| C4 | « **Réseau** : mode hors-ligne par défaut ; aucune resynchronisation Dofusdude sauf nécessité démontrée » | `create_app(..., offline=True)` ⇒ `Catalog.load(..., skip_sync=True)` : `ensure_up_to_date` n'est **pas** appelé (mesure M12) |
| C5 | « **Vérification** : les critères de “fait” doivent être prouvés par des tests pytest réellement exécutés — aucune validation manuelle ni résultat inventé. » | Toute la surface de la page est ancrée par des tests (§ Validation Architecture) |
| C6 | Ligne 80 de `.claude/CLAUDE.md`, ligne `cli.md` / **DOCS-06** : « Un tableau « commande → rôle → exemple » couvrant **toutes** les sous-commandes du parseur et **toutes** les options globales » | **Écart déjà assumé et consigné** (`.planning/WINDOWS.md`, entrée `2`, `open`). Cet écart porte sur `docs/cli.md` (phase 2) et **ne contraint pas** la page de cette phase : le critère 2 du ROADMAP **exige** au contraire une table de correspondance. Voir § « Tension DOCS-06 » |
| C7 | Ligne 80, ligne `parcours-simplifie.md` / **DOCS-04** : « Les 3 écrans réels (`OPT-SIMPLE`, « RECOMMANDATION DE STUFF »), les entrées acceptées (`Cra`, `1`, `terre air`, `1 3`, `multi`, niveau `1`–`200`), les messages d'erreur réels, le raccourci `AVANCE` » | C'est exactement le périmètre des critères 1 et 2 ; les cinq entrées d'exemple citées par DOCS-04 sont **toutes mesurées acceptées** (§ M3) |
| C8 | « GSD Workflow Enforcement » : passer par une commande GSD avant toute écriture | La page et ses tests sont produits dans le plan de phase 3, pas hors workflow |

### Tension DOCS-06 (à ne pas rouvrir, mais à ne pas subir)

`.claude/CLAUDE.md` §2 prescrit pour `cli.md` un tableau récapitulatif unique. La phase 2 a livré l'inverse (D-16/D-17 : une section par sous-commande, aucune table récapitulative), écart **consigné** dans `.planning/phases/02-.../02-01-SUMMARY.md:61,164,173-174` et **ouvert** dans `.planning/WINDOWS.md` (entrées `2` et `3`, `status: open`, `open_count: 4`).

Pour la phase 3, cette tension se manifeste sous une forme **inverse et favorable** : le critère 2 du ROADMAP exige littéralement une table de correspondance, et `.claude/CLAUDE.md` DOCS-04 décrit la page par une liste de libellés. La règle à retenir est donc **D-17 appliqué entre deux pages** (D-37) : la page peut porter **les tables qui sont son contenu propre** (menu des classes rendu, menu des éléments, correspondance libellé ↔ slot), mais **pas** recopier la surface de commandes, qui reste la propriété de `docs/cli.md` (D-37) — ni la re-décrire (D-43).

## Summary

Le parcours simplifié est un **flux Flask à état de session** servi par une seule vue, `optimize_quick(step)` (`dofus_stuff/web/routes.py:935-1011`), sur trois étapes `("classe", "elements", "niveau")`. Rien n'y est aléatoire : les trois écrans, les menus numérotés, la ligne `AVANCE : personnaliser les réglages`, les trois messages d'erreur et l'écran de résultat se **rendent hors-ligne, en processus**, avec `create_app(...).test_client()` et la fixture `client` de `tests/conftest.py`. Mesuré : `GET /optimize/quick/classe` **ne touche aucun catalogue** (rendu 200 même avec `catalog=None`) ; seule l'étape `niveau` réussie exige un catalogue (`RuntimeError: Catalogue non initialisé` sinon). Le harnais n'a donc **jamais besoin** d'ouvrir `.data/dofus.sqlite3`.

**Découverte décisive pour le harnais :** avec un catalogue **réel** (copie de `.data/`), le rendu du résultat **n'est pas déterministe** — deux exécutions successives ont produit 6 puis 7 pages et deux méthodes différentes (`cpsat_feasible+local (FEASIBLE)` puis `greedy (FEASIBLE)`), pour ~9,5–10,5 s par exécution. Avec la **fixture minimale**, le rendu est **déterministe** (trois exécutions, charge utile identique au SHA-256 près) et coûte **0,29 s puis 0,02 s**. Tous les contrôles de cette phase doivent donc s'ancrer sur la fixture, pas sur la base réelle.

**Deux écarts avec des critères du ROADMAP** sont à porter au plan (section dédiée en fin de document) : (1) la « table de correspondance **libellé tronqué** → nom complet de slot » n'a **aucun objet mesurable** dans ce flux — aucune ligne du résultat n'est tronquée (largeur max exactement 100 = `COLS`, zéro caractère `…` sur toutes les pages, en fixture comme sur la base réelle) ; (2) « `Méthode`, `Score`, `Indice de recherche` **dernière page** » est vrai sur une panoplie complète (6/6, 7/7 pages mesurées) mais **faux sur la fixture** (page 2/3), donc l'assertion doit porter sur la **position en fin de résultat**, pas sur l'indice de page.

**Primary recommendation:** livrer la page depuis un module d'ancrage qui **rend réellement** chaque écran avec la fixture `client`, compare **par section** (jamais sur toute la page) la correspondance rendue numéro ↔ libellé, et n'ouvre `.data/` à aucun moment.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|-----------|-------------|----------------|-----------|
| Questions guidées classe → éléments → niveau | **API / Backend (Flask)** | — | Une seule vue à état de session (`routes.py:935`) ; le formulaire ne fait que poster `cmd` (`screen.html:52-63`). La vérité des libellés est côté serveur : c'est elle que le test de rendu capture |
| Numérotation des menus de classe et d'éléments | **API / Backend** | — | Le numéro est la **position** dans `CLASSES`/`ELEMENTS` calculée au rendu (`routes.py:989` : `f"{j + 1:2}. {CLASSES[j]:12}"`), jamais une constante côté client |
| Progression d'étape et « retour » | **API / Backend** | Navigateur | Les gardes d'étape et la séquence vivent dans la vue (`routes.py:938-944`, `:983`) ; le navigateur ne connaît que `data-esc-url` (`screen.html:19`) |
| Pagination du résultat | **API / Backend** | Navigateur | Le découpage est serveur (`_result_screen`, `routes.py:1360-1364`, `paginate`) ; le navigateur charge `?page=N` (`terminal.js:104-133`). La carte `PAGE {page}/{total}` est écrite dans la **ligne de statut** (`routes.py:145,150`) |
| Bannière `AVANCE` | **API / Backend** | — | Ajoutée inconditionnellement aux trois corps rendus (`routes.py:1003`) |
| Sauvegardes navigateur (20 max) | **Navigateur** | — | `localStorage`, clé `dofus-stuff-machine.saves`, écriture et éviction entièrement en JS (`terminal.js:14,15,203-220,295-319`). **Non atteignable par pytest** — ancrage par lecture source |
| Export Dofusbook | **API / Backend** | Navigateur | `build_dofusbook_url` est pure et publique ; deux canaux : `POST cmd=DB` (ouvre le navigateur côté serveur, `routes.py:1326-1337`) et `POST /optimize/dofusbook-url` en JSON (`routes.py:1340-1357`, appelé par `terminal.js:413-432`) |
| Catalogue et solveur | **Database / Storage** → API | — | Les trois questions n'y touchent pas ; le résultat exige un catalogue, mais **n'importe lequel**, y compris la fixture à 3 objets |
## Standard Stack

### Core

| Bibliothèque | Version | Purpose | Why Standard |
|--------------|---------|---------|--------------|
| Markdown « nu » (CommonMark + GFM) | format, aucun paquet | Support de `docs/parcours-simplifie.md` | Convention déjà établie par les phases 1 et 2 (`docs/installation.md`, `docs/cli.md`) ; lisible tel quel et rendu par GitHub, aucun build |
| `pytest` | déclaré `>=8.0` ; **9.1.1 observé** dans `.venv` | Prouver les 5 critères | Déjà présent, déjà configuré (`testpaths`, `pythonpath`) ; 169 tests passent avant cette phase |
| `flask.Flask.test_client` (via `flask>=3.0`) | 3.x, déjà installé | Rendre réellement les écrans (D-32) | **Le** mécanisme de cette phase : c'est la seule façon d'obtenir « le rendu réel » en processus, sans serveur, sans socket |
| `dofus_stuff.web.create_app` / `dofus_stuff.web.dofusbook_export.build_dofusbook_url` / `dofus_stuff.optimize.recommend.recommendation_spec` | code du dépôt, inchangé | API publique sous laquelle la page est ancrée (D-14) | Aucune introspection privée ; les trois sont importables et pures (ou rendent un client) |

### Supporting

| Bibliothèque | Version | Purpose | When to Use |
|--------------|---------|---------|-------------|
| `re`, `html`, `unicodedata`, `pathlib`, `shlex` (stdlib) | 3.11+ | Extraire les couples rendus, normaliser, localiser les fichiers | Dans le module d'ancrage ; `html.unescape` est nécessaire : le rendu contient `&lt;` et `&#39;` (mesuré : `Objectif à vérifier : PA &lt; 11`, `POIDS : {&#39;% Critique&#39;: …}`) |
| `base64` + `msgpack` (déjà dépendance runtime du produit) | — | Décoder l'URL Dofusbook pour contrôler l'ordre des 10 groupes | Uniquement si le contrôle du critère 3 est étendu ; `tests/test_web.py:638-665` le fait déjà — **ne pas dupliquer**, voir § Don't Hand-Roll |
| `unittest.mock.patch` (stdlib) | — | Neutraliser `webbrowser.open_new_tab` | **Obligatoire** si un test poste `cmd=DB` sur l'écran de résultat (`tests/test_web.py:675`) — sinon le test ouvrirait un navigateur |
| Fixtures `client`, `docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple` de `tests/conftest.py` | existantes | Ne rien réécrire (D-12) | Dans le nouveau module d'ancrage |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Rendu par `client` (fixture minimale) | Rendu par `client` sur `.data/dofus.sqlite3` | **Écarté par la mesure** : non déterministe (6 puis 7 pages, deux méthodes), ~9,5 s par exécution, et oblige à ouvrir un fichier de données que C3 protège. Voir § M11 |
| Rendu par `client` | Appel direct de `format_optimize_result_lines(result, profile)` avec un `OptimizeResult` fabriqué | Déterministe et pur, mais ce n'est **plus le rendu** : la pagination, la carte `PAGE n/t` et la ligne de statut disparaissent. Convient au mieux comme contrôle **secondaire** de la fin de résultat |
| Comparaison par section | Comparaison d'un dictionnaire `numéro → libellé` sur toute la page | **Mesuré comme faux** : le menu des éléments (1–4) et le menu des classes (1–19) se recouvrent ; voir § Pitfall 1 et la preuve de morsure |
| Base64 + `msgpack` dans le nouveau module | Réutiliser les tests existants de `tests/test_web.py` | Le module d'ancrage de la page doit renvoyer à ces tests plutôt que les recopier (D-12, D-17) |

**Installation :**

```bash
# Rien à installer : aucune dépendance nouvelle (C1).
.venv/Scripts/python.exe -m pytest -q
```

**Version verification :** aucune version de paquet tiers n'entre dans le périmètre. Les seules versions qui comptent sont celles de l'outillage déjà présent, mesurées :

```bash
.venv/Scripts/python.exe -V                 # Python 3.14.7
.venv/Scripts/python.exe -m pytest -q       # 169 passed in 2.56s
```

## Package Legitimacy Audit

**Aucun paquet externe n'est installé par cette phase.** Aucun nom de paquet découvert par recherche web ou par mémoire de modèle n'apparaît dans ce document : la phase n'ajoute ni bibliothèque, ni outil, ni plugin (C1, PROJECT.md « Contraintes techniques »). Le « Package Legitimacy Gate » est donc **sans objet** — il n'y a rien à vérifier sur un registre, et rien à retirer.

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| *(aucun)* | — | — | — | — | — | Sans objet — zéro dépendance ajoutée |

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Mesures : la surface réelle du parcours simplifié (source de vérité de la page)

> **Méthode.** Chaque mesure ci-dessous provient d'une commande réellement exécutée dans cette session avec `.venv/Scripts/python.exe`, en processus, sans serveur, sans réseau, sans écriture sous `.data/`. Les sondes sont des fichiers jetables écrits dans `.gsd-tmp/research-p3/` (hors du dépôt livré, supprimés en fin de recherche) : `probe_render.py`, `probe_inputs.py`, `probe_result.py`, `probe_env.py`, `probe_assumptions.py`, `probe_determinism.py`, `probe_render2.py`, `proto_negative.py`. Les valeurs entre guillemets sont **verbatim** : elles sortent du rendu ou du fichier, jamais d'une paraphrase.

### M1 — Le flux est un automate d'étapes à état de session

`dofus_stuff/web/routes.py:929-944` (lu dans le fichier, verbatim) :

```python
@bp.get("/optimize")
def optimize_entry() -> Any:
    """Start the accessible recommendation flow."""
    return redirect(url_for("terminal.optimize_quick", step="classe"))


@bp.route("/optimize/quick/<step>", methods=["GET", "POST"])
def optimize_quick(step: str) -> Any:
    steps = ("classe", "elements", "niveau")
    if step not in steps:
        return redirect(url_for("terminal.optimize_entry"))
    state = dict(session.get("recommendation_input") or {})
    if step != "classe" and state.get("classe") not in CLASSES:
        return redirect(url_for("terminal.optimize_entry"))
    if step == "niveau" and not state.get("elements"):
        return redirect(url_for("terminal.optimize_quick", step="elements"))
```

| Sonde (client de test Flask) | Résultat mesuré |
|------------------------------|-----------------|
| `GET /optimize` | `302 → /optimize/quick/classe` |
| `GET /optimize/quick/classe` | `200` — rend `1/3` |
| `GET /optimize/quick/elements` (session vide) | `302 → /optimize` → chaîne → `200`, rend `1/3` |
| `GET /optimize/quick/niveau` (session vide) | idem : revient à `1/3` |
| `GET /optimize/quick/niveau` (classe posée, aucun élément) | `302 → /optimize/quick/elements` (garde `:943`) |
| `GET /optimize/quick/xyz` (étape inconnue) | `302 → /optimize` → chaîne → `200`, rend `1/3` — **pas** de message d'erreur d'étape inconnue dans ce flux |
| `POST /optimize/quick/classe` valide | `302 → /optimize/quick/elements` |
| `POST /optimize/quick/elements` valide | `302 → /optimize/quick/niveau` |
| `POST /optimize/quick/niveau` valide | `302 → /optimize/result` |
| `POST` invalide sur n'importe quelle étape | **`200` sur le même écran**, corps identique, message dans la **ligne de statut** |

**Décision de la machine d'état :** `session["recommendation_input"]` (clé littérale, `routes.py:940,980,982`) porte `classe`, `elements`, `niveau`. L'étape suivante est décidée par `steps[steps.index(step) + 1]` (`routes.py:983`). Le retour arrière n'est **pas** un bouton : c'est `data-esc-url` (`screen.html:19`) alimenté par `back_url` (`routes.py:1004,1009`).

### M2 — Corps rendus verbatim des trois questions

Les trois écrans portent le même `pgm="OPT-SIMPLE"` et le même titre `** RECOMMANDATION DE STUFF **` (`routes.py:1005-1006`). Corps mesurés (lignes non vides, `GET` puis deux `POST` successifs sur le même client) :

```
Écran 1/3 (GET /optimize/quick/classe)
|VOTRE STUFF EN 3 CHOIX
|1/3 - Quelle est votre classe ?
| 1. Cra              2. Ecaflip          3. Eliotrope
| 4. Eniripsa         5. Enutrof          6. Feca
| 7. Forgelance       8. Huppermage       9. Iop
|10. Osamodas        11. Ouginak         12. Pandawa
|13. Roublard        14. Sacrieur        15. Sadida
|16. Sram            17. Steamer         18. Xelor
|19. Zobal
|AVANCE : personnaliser les réglages

Écran 2/3 (POST classe=1, puis POST elements=arbre pour rester sur l'écran)
|VOTRE STUFF EN 3 CHOIX
|Classe : Cra
|2/3 - Quels éléments privilégier ?
|1. Terre    2. Feu    3. Eau    4. Air
|Un ou plusieurs : feu / terre air / 1 3 / multi
|Le multi valorise aussi votre élément le plus faible.
|AVANCE : personnaliser les réglages

Écran 3/3 (POST elements=terre puis POST niveau=201)
|VOTRE STUFF EN 3 CHOIX
|Cra - terre / air
|3/3 - Quel est votre niveau ? (1 à 200)
|ENTREE lance la recherche de votre équipement.
|PA/PM et vitalité sont pris en compte selon le niveau.
|Points répartis automatiquement, sans exo ni parchemins.
|Jets moyens ; préférences de classe ajustables après calcul.
|AVANCE : personnaliser les réglages
```

Points de rédaction vérifiés au rendu (et non déduits du source) :

- Le libellé `AVANCE : personnaliser les réglages` est rendu **sur les trois étapes**, sans condition (`routes.py:1003`) — il ne disparaît pas à l'étape `niveau`.
- La barre de touches des trois écrans est exactement `ESC=Retour` (mesuré : `fkeys=[('ESC', 'Retour')]`) ; le tableau de statut vaut `ENTREE=SUIVANT` aux étapes 1 et 2 et **`ENTREE=CALCULER`** à l'étape 3 (`routes.py:1010`, mesuré).
- Le champ de saisie est `<input name="cmd" maxlength="40">` avec le libellé `CHOIX` (`routes.py:1007`, mesuré sur les trois écrans) : **40 caractères**, pas 200.
- Les trois écrans tiennent sur **une seule page** (`data-body-total="1"`) : aucune carte `PAGE n/t` n'y apparaît. La pagination commence au résultat.
- Le titre contient des astérisques littérales : `** RECOMMANDATION DE STUFF **` (à citer tel quel).

### M3 — Entrées réellement acceptées et refusées (matrice mesurée)

**Question 1/3 — classe** (`routes.py:955-965`). Acceptée si `normalized(cmd)` égale `normalized(c)` pour un `c` de `CLASSES` (accents et casse ignorés), **ou** si `cmd.isdigit() and 1 <= int(cmd) <= len(CLASSES)`.

| `cmd` | Résultat mesuré | `cmd` | Résultat mesuré |
|-------|-----------------|-------|-----------------|
| `Cra`, `cra`, `CRA`, `Crâ`, `crâ` | accepté | `6.0` | refusé |
| `1`, `19`, `019`, `6`, ` 3 ` | accepté | `+1` | refusé |
| `Ecaflip ` (espace final), `ecaflip`, `Zobal`, `Eliotrope` | accepté | `eliotrop` | refusé (**pas** de tolérance de préfixe) |
| `0`, `20` | refusé | `truc`, `` (vide) | refusé |

Message d'erreur réel, mesuré dans la ligne de statut :

`Saisissez le nom ou le numéro de votre classe. — ENTREE=SUIVANT`

**Question 2/3 — éléments** (`routes.py:966-973`). Séparateurs mesurés acceptés : **espace**, **virgule**, **plus** (y compris collés et mélangés). Alias numériques `1 2 3 4` → `Terre Feu Eau Air` (`dict(zip("1234", ELEMENTS))`, `routes.py:968`) ; `multi` **seul** vaut les quatre ; les doublons sont dédupliqués (`dict.fromkeys`).

| `cmd` | Résultat mesuré | `cmd` | Résultat mesuré |
|-------|-----------------|-------|-----------------|
| `terre`, `feu`, `eau`, `air`, `TERRE`, `Terre` | accepté | `multi`, `MULTI` | accepté |
| `terre air`, `terre,air`, `terre, air`, `terre+air`, `terre + air` | accepté | `multi terre`, `terre multi`, `multi,tout` | refusé |
| `1`, `1 3`, `1,3`, `1+3`, `4`, `1 terre`, `2,2` | accepté | `0`, `5` | refusé |
| `terre  feu  eau  air`, `air eau feu terre`, `1 2 3 4` | accepté | `arbre`, `force`, `tous`, `` , `   ` | refusé |

Message d'erreur réel : `Exemple : feu, terre air, ou multi. — ENTREE=SUIVANT`

**Question 3/3 — niveau** (`routes.py:974-977`). `cmd.isdigit()` **et** `1 <= int(cmd) <= 200`.

| `cmd` | Résultat mesuré | `cmd` | Résultat mesuré |
|-------|-----------------|-------|-----------------|
| `1`, `200`, `050`, ` 50 ` | accepté → `/optimize/result` | `0`, `201`, `-1` | refusé |
| `AVANCE`, `avance`, ` Avance ` | accepté → `/optimize/wizard/recap` | `50.0`, `abc`, ``, `+50`, `1e2` | refusé |
| | | `2000000000000000000000` | refusé (`isdigit()` vrai, mais `int(cmd) > 200`) |

Message d'erreur réel : `Saisissez un niveau entre 1 et 200. — ENTREE=CALCULER`

### M4 — `AVANCE` : chemin réel, y compris depuis l'étape 3

`routes.py:948-954` (lu dans le fichier, verbatim) :

```python
if cmd.upper() == "AVANCE":
    if state.get("classe") and state.get("elements"):
        spec = recommendation_spec(state["classe"], state["elements"], state.get("niveau", 200))
        save_wizard_spec(session, spec)
    else:
        reset_wizard(session)
    return redirect(url_for("terminal.optimize_wizard", step="recap"))
```

Mesuré : cette branche est évaluée **avant** la validation de l'étape (elle précède le `if step == "classe"`), donc `AVANCE` fonctionne aux trois étapes, en minuscules et entouré d'espaces. Depuis l'étape 3 avec `classe` et `elements` en session, la redirection mène au récapitulatif du wizard, dont le corps rendu commence par :

```
|NIVEAU 200  JET=average  DUREE=8s
|SLOTS : amulet, rings, belt, boots, hat, cape, weapon, shield, dofus, pet, prysma
|POIDS : {&#39;% Critique&#39;: 2.0, &#39;% Dommages aux sorts&#39;: 12.0, …}
|GO = LANCER  RESET = REINITIALISER  1-8 = RETOUR ECRAN
|SAVES = STUFFS SAUVEGARDES
```

⚠️ Le wizard avancé est la **frontière de la phase 4** (D-43) : la page de cette phase cite `AVANCE` et dit qu'il ouvre les réglages détaillés, **sans** décrire les écrans du wizard ni recopier `NIVEAU 200 JET=average DUREE=8s`.

### M5 — Libellés du parcours CLI : mesurés, mais ce ne sont **pas** les trois questions

D-33 s'applique : les libellés CLI se lisent dans leur module source, jamais en exécutant `main()`. Mesure : `dofus_stuff/optimize/profile_input.py:324-391`, `prompt_optimize_interactive` (lu par `sed -n` avec numéros de ligne) — les invites réelles sont :

| Ligne | Invite verbatim |
|-------|-----------------|
| `:334` | `"Niveau [demo] : "` |
| `:336` | `"Classique seul (sans dofus/familier) [n] : "` |
| `:338` | `"Jets (min|average|max) [average] : "` |
| `:355` | `"Caractéristique(s) à maxer (ex: intelligence) : "` |
| `:370` | `f"Base hors stuff ({primary})"` — passé à `_ask_float`, qui rend l'invite `Base hors stuff (Force) [0] : ` |
| `:371` | `f"Parchemin ({primary})"` — idem : `Parchemin (Force) [0] : ` (gabarit réel en `:361` : `input_fn(f"{label} [{default:g}] : ")`) |

Occurrences réelles de `input_fn(` dans le module (mesuré : `grep -n 'input_fn(' dofus_stuff/optimize/profile_input.py`) : **7**, lignes `334, 336, 338, 355, 361, 387, 389` — `336`/`387` et `338`/`389` sont deux chemins alternatifs (profil « demo » vs profil par caractéristiques), et `361` est le gabarit de `_ask_float`. Aucune invite de **classe** ni d'**élément** n'existe dans ce module.

**Finding à porter au plan :** le parcours guidé CLI **ne pose pas** les trois questions classe → éléments → niveau. Il n'existe **aucune** invite de classe ni d'élément côté CLI (`grep -n "classe\|element"` sur `profile_input.py` ne renvoie aucune invite). La classe et les éléments n'existent que dans le flux web. La page doit donc dire cela **explicitement** (c'est une information utile au lecteur) plutôt que de laisser croire que le parcours CLI est le même : D-36 autorise cette mention en prose, sans recopie de la surface de commandes (D-37).

### M6 — L'écran de résultat : où vivent `Méthode`, `Score` et `Indice de recherche`

**Route :** `optimize_result` (`routes.py:1298-1323`), rendu par `_result_screen` (`routes.py:1360-1384`) :

```python
def _result_screen(lines: list[str]) -> Any:
    wrapped = wrap_lines(lines, COLS)
    page = max(1, int(request.args.get("page", 1)))
    slice_lines, page, total = paginate(wrapped, page=page, page_size=BODY_LINES)
    ...
    return _screen(
        pgm="OPT-03",
        title="** RESULTAT OPTIMISATION **",
        body_lines=slice_lines,
        input_label="",
        ...
        status="ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB",
        nav_base=url_for("terminal.optimize_result"),
        mode="result",
        stuff_payload=payload,
    )
```

**La carte de pagination est dans la ligne de statut**, pas dans le corps. `_screen` la compose (`routes.py:143-150`) :

```python
indicators: list[str] = []
if total > 1:
    indicators.append(f"PAGE {page}/{total}")
if input_label is not None:
    indicators.append(f"ENTREE={enter_hint}" if enter_hint else "ENTREE=VALIDER")
if status:
    indicators.insert(0, status)
status = " — ".join(indicators) if indicators else ""
```

Ligne de statut mesurée au rendu (verbatim) :

```
ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB — PAGE 1/6 — ENTREE=VALIDER
```

**Barre de touches mesurée** sur l'écran de résultat : `F7=Page prec`, `F8=Page suiv`, `ESC=Retour`. Attention : `Precedent`/`Suivant` (sans abréviation) ne sont produits que pour le **wizard** (qui passe `f7_url`/`f8_url`) ; le résultat, lui, passe par `f7_label = "Page prec"` / `f8_label = "Page suiv"` (`routes.py:137-141`). **Les deux libellés de la phase 4 et de la phase 3 ne sont donc pas les mêmes** — `tests/test_docs_code_anchor.py:64-67` épingle déjà les quatre.

**Où sont les diagnostics.** `dofus_stuff/optimize/api.py:327-341` construit le bloc, `:342-346` l'insère pour le flux non simplifié, et **`:433-434`** l'insère pour le flux simplifié — donc **en fin de résultat**, après l'équipement et les statistiques :

```python
    if simple:
        lines.extend(diagnostics)
        lines.append("Recherche sur une sélection du catalogue ; optimalité globale non garantie.")
    lines.append(f"Greedy: {result.greedy_score:.1f} | UB0: {result.ub0:.1f}")
```

Les trois libellés exacts (`api.py:329,338-340`) :

```python
        f"Méthode : {result.method}"
        + (f" ({result.cpsat_status})" if result.cpsat_status else "")
...
    diagnostics.append(
        f"Score : {result.evaluation.score:.1f}  |  "
        f"Indice de recherche : {result.compatibility.percent:.1f}% "
        f"[{result.compatibility.mode}]"
    )
```

Rendus mesurés (fixture puis base réelle) :

```
|Méthode : cpsat (OPTIMAL)
|Score : 1758.4  |  Indice de recherche : 100.0% [optimal_prouve]
|Recherche sur une sélection du catalogue ; optimalité globale non garantie.
|Greedy: 1758.4 | UB0: 1758.4
```

```
|Méthode : cpsat_feasible+local (FEASIBLE)
|Score : 6021.8  |  Indice de recherche : 84.6% [borne_solver]
```

**Ordre complet des lignes du résultat simplifié** (déduit du rendu, `api.py:305-436`) : `Niveau {n} — {éléments}` → `PA .. | PM .. | Portée ..` → `Éléments : …` → `Puissance .. | Vitalité ajoutée ..` → `Points inclus ; sans exo/parchemins. Jets moyens sauf réglage avancé.` → `Build valide : oui|non` → `Objectif à vérifier : …` (zéro ou plus) → `Équipement :` → 17 lignes de slot (`display_slots`, `api.py:362-380`) → `Panoplies actives : n` → `Stats totales (avec équipement) :` → `Stats gagnées (équipement + panoplies) :` → `Bonus de panoplie :` → `Détail {primary} — base+parcho: … | items: … | sets: …` → **le bloc de diagnostics** → `Recherche sur une sélection du catalogue ; optimalité globale non garantie.` → `Greedy: … | UB0: …`.

**Nombre de pages mesuré** (critère 2) :

| Catalogue | Niveau | Éléments | Pages | Où tombent `Méthode`/`Score` |
|-----------|--------|----------|-------|------------------------------|
| fixture minimale (3 objets) | 200 | `multi` | **3** | page **2**/3 |
| fixture minimale (3 objets) | 150 | `terre` | **2** | page 2/2 |
| base réelle (copie) | 200 | `1 3` | **6** | page **6/6** (dernière) |
| base réelle (copie) | 200 | `1 3` | **6** puis **7** (non déterministe) | dernière page dans les deux cas |

**Trap majeur mesuré : `data-stuff-payload` est présent sur *chaque* page du résultat** (vérifié page par page : `True` pour toutes). Cet attribut contient `{"lines": [...], "slots": ..., "level": ...}` — **le texte intégral du résultat**, sérialisé par `tojson` (`screen.html:21`), donc avec les accents échappés en `\uXXXX`. Conséquence : `assert "Méthode" in response.data` est **faux sur la page 1** (l'accent est échappé) mais `assert "Score" in response.data` est **vrai sur la page 1** alors que l'utilisateur ne le voit pas. Toute assertion sur `response.data` brut est donc invalide ; il faut extraire les **lignes du corps** (ou décoder la charge utile).

### M7 — Largeurs, troncature, et pourquoi la table « libellé tronqué » n'a pas d'objet

Règle de troncature réelle, `dofus_stuff/web/screens.py:14-20` (lu dans le fichier, verbatim) :

```python
def clip(text: str, width: int = COLS) -> str:
    """Tronque ou pad une ligne à exactement `width` caractères."""
    if len(text) > width:
        if width <= 1:
            return text[:width]
        return text[: width - 1] + "…"
    return text.ljust(width)
```

La même règle existe côté navigateur, `dofus_stuff/web/static/js/terminal.js:146-147` : `if (width <= 1) return text.slice(0, width); return text.slice(0, width - 1) + "…";`. `COLS = 100`, `BODY_LINES = 18` (`screens.py:5,10`).

Mesures :

```bash
.venv/Scripts/python.exe -c "from dofus_stuff.web.screens import clip; print(len(clip('x'*120)), clip('x'*120)[-3:])"
# 100 xx…   (99 'x' + '…')
```

| Mesure | Résultat |
|--------|----------|
| Nombre de lignes rendues contenant `…` sur **toutes** les pages du résultat (fixture, niveau 150) | **0** |
| Nombre de lignes rendues contenant `…` sur **toutes** les pages du résultat (copie de la base réelle, niveau 200) | **0** |
| Longueur maximale d'une ligne rendue (base réelle, toutes pages) | **100** exactement (= `COLS`) : les lignes sont **enveloppées** (`wrap_lines`) avant d'être passées à `pad_lines`, donc `clip` ne coupe rien |
| Longueur de tous les libellés de slot rendus (`f"  {slot:8s} : …"`, `api.py:392-395`) | au plus **7** (`dofus_1`…`dofus_6`, `ring_a`, `ring_b`) : le format `:8s` **complète** par des espaces, il ne tronque jamais |

Les 17 libellés de slot réellement rendus, dans l'ordre du rendu (`api.py:362-380`), et leur sens français (à confirmer par le lecteur) :

| Libellé rendu | Nom complet du slot | Libellé rendu | Nom complet du slot |
|---------------|---------------------|---------------|---------------------|
| `amulet` | amulette | `dofus_1`…`dofus_6` | les six emplacements Dofus |
| `ring_a`, `ring_b` | anneau A, anneau B | `pet` | familier / monture |
| `belt` | ceinture | `prysma` | prysmaradite |
| `boots` | bottes | `shield` | bouclier (masqué si non équipé) |
| `hat` | chapeau | `weapon` | arme |
| `cape` | cape | | |

⚠️ Les trois libellés `pet`, `prysma` et les `dofus_*` ne sont **rendus que s'ils sont équipés** (`api.py:384-385` : les slots vides ne sont affichés que s'ils ne sont pas Dofus/familier/prysma/bouclier). Sur une panoplie complète (base réelle), les 17 apparaissent — mesuré. Le premier libellé non vide de l'énumération `screen.html`/`terminal.js` (la chaîne `CHARGEMENT DES SAUVEGARDES LOCALES…`) **contient** un caractère `…`, sans rapport avec `clip` : une assertion « aucune ligne ne contient `…` » sur la page des sauvegardes serait fausse sur une implémentation correcte.

**Conclusion de M7 (finding, voir § Écarts) :** dans ce flux, **aucun libellé de slot n'est tronqué**. La correspondance utile au lecteur est **libellé technique court (`ring_a`, `dofus_3`, `prysma`) → nom complet en français**, et cette table est adossée au rendu (`api.py:362-380`) — mais elle ne dérive **pas** de `clip`/`slice(0, width-1)`, qui ne se déclenche jamais ici.

### M8 — Sauvegardes navigateur : 20 maximum, clé, écrans (JS non atteignable par pytest)

`dofus_stuff/web/static/js/terminal.js:14-15` (lu dans le fichier, verbatim) :

```javascript
  var SAVES_KEY = "dofus-stuff-machine.saves";
  var MAX_SAVES = 20;
```

Comportement **réel** de la limite (`terminal.js:294-318`, lu) :

```javascript
    var stuffs = loadSaves();
    while (stuffs.length >= MAX_SAVES) {
      stuffs.shift();
    }
    ...
    var msg = "STUFF SAUVEGARDE (" + stuffs.length + "/" + MAX_SAVES + ")";
```

⇒ **À la 21ᵉ sauvegarde, la plus ancienne est évincée silencieusement** (`shift`), puis la nouvelle est ajoutée (`push`) : la liste ne dépasse jamais 20, **aucun message d'éviction n'est produit** — le statut affiche seulement `STUFF SAUVEGARDE (20/20)`. C'est un point que la page doit dire honnêtement (« les plus anciennes sont remplacées »), car un lecteur s'attendrait à un refus.

Autres faits mesurés / lus :

| Élément | Valeur exacte | Source |
|---------|---------------|--------|
| Clé de stockage | `dofus-stuff-machine.saves` | `terminal.js:14` |
| Forme écrite | `{"version": 1, "stuffs": [...]}` | `terminal.js:215-220` |
| Champs d'une entrée | `id`, `savedAt`, `label`, `summary`, `lines`, et si présents `slots`/`level` | `terminal.js:298-309` |
| Résumé de liste | construit depuis les lignes : `Score … — niv.… — méthode` | `terminal.js:230-254` |
| Liste vide | `AUCUNE SAUVEGARDE LOCALE.` + `Apres un calcul, tapez SAVE [NOM] sur l'ecran resultat.` + `Les stuffs sont stockes dans ce navigateur uniquement.` | `terminal.js:323-328` |
| En-tête de liste | `N SAUVEGARDE(S) — MAX 20` | `terminal.js:331` |
| Statut de liste | `PAGE {page}/{total} — N OUVRIR \| DEL N \| PURGE OUI \| ESC` | `terminal.js:369-370` |
| Statut de détail | `PAGE {page}/{total} — BACK LISTE \| DB DOFUSBOOK \| ESC MENU` | `terminal.js:399-400` |
| Purge | `PURGE` → `CONFIRMER AVEC : PURGE OUI` → `SAUVEGARDES PURGEES` (retire la clé) | `terminal.js:459-471` |
| Commande de sauvegarde | saisie `SAVE` ou `SAVE <libellé>` interceptée sur `mode="result"` | `terminal.js:606-620` |

**Écrans qui les exposent** (les deux sont rendus côté serveur, donc **mesurables**) :

1. **Écran de résultat `OPT-03`** — sa ligne de statut annonce `ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB` (mesuré). C'est là que `SAVE [NOM]` et `DB` sont saisis ; `data-mode="result"` et la présence de `data-stuff-payload` sont mesurés sur ce rendu.
2. **Écran `SAV-01`, route `/saves`** (`routes.py:1280-1295`), mesuré : corps `CHARGEMENT DES SAUVEGARDES LOCALES…`, statut `N OUVRIR | DEL N | PURGE OUI — ENTREE=VALIDER`, champ `cmd` (maxlength 40), **pas** de libellé de champ. Le contenu de la liste est **remplacé par le navigateur** au chargement (`terminal.js:622-630` : `renderSavesList()` au `DOMContentLoaded` implicite du script).

**Ce que pytest ne peut pas exécuter :** ni `localStorage`, ni `shift`, ni `slice`, ni les assertions de statut JS. Il n'y a **aucun moteur JS** dans l'environnement (interdiction de `playwright`, C1). Le « 20 maximum » est donc ancrable par **lecture source ancrée** (patron `LIBELLES_SOURCE` de `tests/test_docs_code_anchor.py:61-74` : exiger le libellé côté page **et** le littéral + le porteur sur une même ligne du fichier JS), jamais par un test de comportement. Voir § Validation Architecture (critère 3) pour la forme exacte.

### M9 — Export Dofusbook

`dofus_stuff/web/dofusbook_export.py:21` (lu, verbatim) :

```python
DOFUSBOOK_IMPORT_URL = "https://www.dofusbook.net/fr/equipement/dofus-stuffer/objets"
```

Ordre des 10 groupes (`dofusbook_export.py:26-37`, lu, verbatim — commentaires d'origine compris) :

```python
_GROUP_SLOTS: tuple[tuple[str, ...], ...] = (
    ("cape",),  # 0 cape (ca)
    ("hat",),  # 1 coiffe (ch)
    ("belt",),  # 2 ceinture (ce)
    ("boots",),  # 3 bottes (bo)
    ("amulet",),  # 4 amulette (am)
    ("ring_a", "ring_b"),  # 5 anneaux (a1, a2)
    ("dofus_1", "dofus_2", "dofus_3", "dofus_4", "dofus_5", "dofus_6"),  # 6 dofus
    ("shield",),  # 7 bouclier (br)
    ("weapon",),  # 8 arme (ar)
    ("pet",),  # 9 familier/monture (fa)
)
```

Décodage mesuré (base64 + `msgpack`, valeurs réelles) : pour 14 slots fournis, la charge utile se décompose en `[caracs(51), points(51), niveau, flags, counts(10), ids]` et donne

```
counts = [1, 1, 0, 0, 0, 2, 6, 1, 1, 1] | niveau = 150 | flags = 0 | len(caracs) = 51 | len(ids) = 13
ids = [100, 44, 100, 101, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

**Finding (critère 3) : `prysma` n'est pas exporté.** Le slot `prysma` n'appartient à aucun des 10 groupes : l'ID fourni pour `prysma` (10) **n'apparaît pas** dans `ids` (mesuré : `10 not in ids` → `True`). L'export Dofusbook porte donc au plus 16 emplacements (cape, coiffe, ceinture, bottes, amulette, 2 anneaux, 6 Dofus, bouclier, arme, familier) — les trophées/Dofus passent par le groupe 6, la prysmaradite reste dehors. La page doit le dire, sinon le lecteur croira que « tout le stuff » part chez Dofusbook (D-35/D-41).

Canaux réels (les deux mesurés comme routes existantes, la seconde réellement appelée) :

| Canal | Déclencheur | Effet | Piège |
|-------|-------------|-------|-------|
| `POST /optimize/result` avec `cmd=DB` | saisie `DB` sur l'écran de résultat | `_open_dofusbook()` (`routes.py:1326-1337`) appelle **`webbrowser.open_new_tab(url)`** côté serveur, puis `flash("DOFUSBOOK OUVERT DANS LE NAVIGATEUR", "info")` | **Un test qui poste `DB` sans patcher `webbrowser.open_new_tab` lance un navigateur.** Le patron existe : `tests/test_web.py:675` |
| `POST /optimize/dofusbook-url` (JSON) | `terminal.js:413-432` au `DB` de l'écran de détail des sauvegardes | renvoie `{"url": …}` (ou 400 `{"error": "slots manquants"}`) | Déjà couvert par `tests/test_web.py:684,708` |
| Échec d'ouverture | `except Exception` dans `_open_dofusbook` | `flash(url[:COLS], "info")` — l'URL est **coupée à 100 caractères** | C'est ici que `[:COLS]` tronque réellement, sans `…` |

**Couverture déjà en place (à réutiliser, pas à dupliquer) :** `tests/test_web.py:638` (encodage), `:668` (ouverture navigateur, patché), `:684` (route JSON), `:713` (régression d'ordre cape-avant-chapeau, avec `counts == [1, 1, 1, 1, 1, 2, 6, 1, 1, 1]`). Ces tests **prouvent déjà** l'ordre des 10 groupes : la phase 3 doit s'y **renvoyer** et ancrer la **page** sur les libellés et la forme, pas réécrire ces assertions.

### M10 — Hypothèses et limites de l'outil (critère 4) : tout est mesuré

**Points par niveau.** `dofus_stuff/optimize/recommend.py:24` : `capital = 5 * (level - 1)` ; et `dofus_stuff/model/solver_spec.py:264-266` (lu, verbatim) :

```python
def total_capital_for_level(level: int) -> int:
    """Capital de points de caractéristiques disponible (approximation)."""
    return 5 * max(0, int(level) - 1)
```

Mesure de cohérence (balayage 1→200) : `capital_spent(spec.goals) == total_capital_for_level(level)` et `== 5 * (level - 1)` **pour tous les niveaux testés** (1, 39, 40, 99, 100, 149, 150, 200) — la répartition automatique consomme **tout** le capital. Le coût par point suit des paliers réels (`solver_spec.py:251-261` : 1 / 2 / 3 / 4 / 5 points selon `<100`, `<200`, `<300`, `<400`, sinon).

**Paliers PA/PM.** `recommend.py:35-36` (lu dans le fichier, verbatim) :

```python
    pa = 6 if level < 40 else 8 if level < 100 else 10 if level < 150 else 11
    pm = 3 if level < 40 else 4 if level < 100 else 5 if level < 150 else 6
```

Balayage mesuré 2→200 : la **cible PA change exactement en 40, 100 et 150** ; la **cible PM change exactement en 40, 100 et 150** ; la **base PA change exactement en 100** (`base=6 + int(level >= 100)`, `recommend.py:39`). Valeurs mesurées :

| Niveau | Capital | base PA | cible PA | base PM | cible PM |
|--------|---------|---------|----------|---------|----------|
| 1 | 0 | 6 | 6 | 3 | 3 |
| 39 | 190 | 6 | 6 | 3 | 3 |
| 40 | 195 | 6 | 8 | 3 | 4 |
| 99 | 490 | 6 | 8 | 3 | 4 |
| 100 | 495 | 7 | 10 | 3 | 5 |
| 149 | 740 | 7 | 10 | 3 | 5 |
| 150 | 745 | 7 | 11 | 3 | 6 |
| 200 | 995 | 7 | 11 | 3 | 6 |

**Heuristiques de classe : elles EXISTENT réellement.** Contrairement à l'hypothèse de recherche, `recommend.py:44-54` porte bien des heuristiques par classe, mesurées une par une :

| Classes | Objectif ajouté | Condition |
|---------|-----------------|-----------|
| Cra, Enutrof, Sadida, Eniripsa, Steamer, Osamodas | `% Dommages distance` (poids 12) | `character_class in {...}` (`recommend.py:45-46`) |
| Iop, Sacrieur, Ouginak, Zobal | `% Dommages mêlée` (poids 12) | `elif` (`recommend.py:47-48`) |
| Cra, Enutrof, Sadida | `Portée` cible **2** si niveau < 100, **4** sinon (poids 20) | `recommend.py:51-52` |
| Osamodas, Sadida | `Invocation` base 1, cible 3 (poids 35) | `recommend.py:53-54` |
| Ecaflip, Eliotrope, Feca, Forgelance, Huppermage, Pandawa, Roublard, Sram, Xelor | **aucun** objectif propre | mesuré classe par classe |

Le commentaire du code borne lui-même la portée (`recommend.py:44`) : `# Broad playstyle preferences, not a simulation of class spells.` La page doit citer cette limite telle quelle en substance (D-41) : ce sont des **préférences de style de jeu**, pas une simulation des sorts de la classe.

**Ni exo ni parchemins.** Ligne littérale du rendu, `api.py:316` (lu, verbatim) :

```python
        lines.append("Points inclus ; sans exo/parchemins. Jets moyens sauf réglage avancé.")
```

Et l'étape 3/3 le redit dans son corps (`routes.py:1001`, mesuré au rendu) : `Points répartis automatiquement, sans exo ni parchemins.` Enfin `routes.py:1002` : `Jets moyens ; préférences de classe ajustables après calcul.` Mesure de cohérence : `[(n, g.exo, g.scroll) for n, g in spec.goals.items() if g.exo or g.scroll] == []` — aucun exo ni parchemin dans le spec généré, pour toutes les classes et tous les niveaux testés. `tests/test_recommend.py:28` asserte déjà `all(g.exo == g.scroll == 0 …)`.

⚠️ **Nuance honnête à porter dans la page :** la ligne de détail rendue s'appelle `Détail {primary} — base+parcho: … | items: … | sets: …` (`api.py:429`). Le mot « parcho » apparaît donc à l'écran alors que **le parcours guidé suppose zéro parchemin** : le total `base+parcho` y est la somme de la base réelle **plus** les parchemins saisis (nuls ici). Ne pas présenter cette ligne comme un contredit de l'hypothèse ; ne pas la passer sous silence non plus.

**« Indice de recherche » ≠ qualité en combat.** Mécanisme réel : `dofus_stuff/optimize/score.py` (lu, verbatim) — `compute_compatibility` calcule `percent = 100 * score / score_ref` où `score_ref` vaut, dans l'ordre : le score lui-même si l'optimalité est **prouvée** (⇒ 100 %, mode `optimal_prouve`), sinon la borne CP-SAT (mode `borne_solver`), sinon `max(greedy, UB0, score)` (mode `borne_heuristique`). C'est donc un **rapport interne au solveur**, borné à `[0, 100]`, dont les trois modes sont rendus entre crochets : `[optimal_prouve]`, `[borne_solver]`, `[borne_heuristique]`. Aucun modèle de combat n'entre dans ce calcul — la limite du critère 4 est **adossée au code**.

**« Recherche sur une sélection du catalogue ».** Mécanisme réel : `dofus_stuff/optimize/candidates.py:298-341` (lu) — le pool est construit en filtrant `kind == "equipment"`, `level <= profile.level`, `_is_plausible_equipment` (écarte les objets MJ/aberrants, `:56-80`), les filtres de type, et les slots demandés ; puis, **par slot logique**, il garde `entries[:top_k]` **plus** les spécialistes de chaque objectif non nul, `max(2, top_k // 4)` par objectif (`candidates.py:328-336`). Le flux simplifié passe `top_k=40` (`recommend.py:59`), donc 40 par slot + jusqu'à 10 par objectif pondéré. Mesure quantitative (copie de la base réelle, `result.pool_stats["candidates_per_slot"]`) :

| Niveau | Éléments | Candidats retenus | Slots couverts | Panoplies indexées |
|--------|----------|-------------------|----------------|--------------------|
| 100 | terre | 1 219 | 17 | 929 |
| 100 | terre + air | 1 370 | 17 | 929 |
| 100 | 4 éléments | 1 636 | 17 | 929 |
| 200 | terre | 1 459 | 17 | 929 |
| 200 | terre + air | 1 618 | 17 | 929 |
| 200 | 4 éléments | 1 864 | 17 | 929 |

Contexte de lecture (mesuré en lecture seule, URI `file:…?mode=ro` sur `.data/dofus.sqlite3`) : `items` contient 4 356 lignes `kind='equipment'` et 929 `kind='sets'`. La recherche porte donc bien sur une **sélection** (le préfiltrage de plausibilité et le top-k par slot) et non sur tout le catalogue — **mais ces nombres ne doivent pas entrer dans la prose** (interdiction des valeurs volatiles, `PROJECT.md` « Out of Scope », réitérée par la phase 1) : la page décrit le **mécanisme** (filtre de plausibilité, niveau, `--top-k`), le lecteur qui veut un chiffre lance la commande.

**Rappel de la limite de rendu :** la phrase « Recherche sur une sélection du catalogue ; optimalité globale non garantie. » n'est rendue **que** pour le flux simplifié (`api.py:342` pour l'autre chemin, `:434` pour celui-ci) — c'est bien sur l'écran du parcours simplifié qu'elle apparaît, sur la **dernière page**.

### M11 — Déterminisme et coût : la mesure qui décide du harnais

| Configuration | Déterminisme | Coût mesuré |
|---------------|--------------|-------------|
| Fixture minimale (`tests/conftest.py::_sample_items`, 3 équipements) | **déterministe** : 3 exécutions → `pages=3`, empreinte SHA-256 de la charge utile **identique** (`a599bc333c48fba0`) | 0,288 s / 0,018 s / 0,021 s |
| Copie de `.data/dofus.sqlite3` (base réelle) | **non déterministe** : `pages=6` puis `pages=7`, méthode `cpsat_feasible+local (FEASIBLE)` puis `greedy (FEASIBLE)`, empreintes de charge utile différentes (`102b8e1ec64499c6` ≠ `4501c9510c3a92d4`) | 9,55 s puis ~10,5 s par exécution |

**Conséquence directe :** un test qui ancre `Méthode : …` ou le nombre de pages sur la base réelle est **flaky par construction** (la durée de `time_limit_s=8` et l'état de CP-SAT décident du chemin). Le harnais de la phase 3 doit utiliser la fixture.

### M12 — Effets de bord : `.data/` n'est pas touché, et pourquoi il ne faut pas y pointer le harnais

Deux mesures distinctes, toutes deux en processus :

1. **Avec la fixture** (`create_app(data_dir=tmp, catalog=catalog, load_catalog=False)`) : `.data/` n'est jamais ouvert ; le seul fichier créé est une base vide dans `tmp_path` (patron de `tests/conftest.py:78-95`). `.data/dofus.sqlite3` reste identique avant/après (taille 24 989 696, `mtime_ns` inchangé).
2. **En pointant volontairement l'application sur `.data/`** (`create_app(data_dir=ROOT/".data", offline=True, load_catalog=True)`) : le fichier reste **byte-identique** — `mtime_ns`, taille et SHA-256 (`e3793d64cb7939ad`) identiques avant/après le parcours complet (rendu des trois questions **et** du résultat), et `os.listdir(".data")` reste `['dofus.sqlite3']` (aucun `-journal`, aucun `-wal`). Explication : `offline=True` ⇒ `skip_sync=True` (dofus_stuff/web/__init__.py, `reload_catalog`), donc `ensure_up_to_date` **n'est pas appelé** ; les seules instructions exécutées sont les `CREATE TABLE/INDEX IF NOT EXISTS` de `Database.open()` (`database.py:38-62`), qui sont des **no-op de schéma** sur une base déjà complète.

**Pourquoi malgré cela ne pas pointer `.data/` :** la même sonde, exécutée sur un répertoire **vide**, montre que `Database.open()` **crée** `dofus.sqlite3` (`data_dir.mkdir(parents=True, exist_ok=True)` puis `sqlite3.connect` puis `CREATE TABLE`). L'ouverture est donc en **lecture-écriture** : sur un schéma absent ou modifié, elle écrirait sous `.data/` — ce que C3 interdit. Le harnais doit rester sur la fixture, et cette mesure est la justification.

**Bonus mesuré :** avec `create_app(catalog=None, load_catalog=False)`, les trois questions se rendent (`GET /optimize/quick/classe` → `200` avec `1/3 - Quelle est votre classe ?` ; les deux `POST` valides redirigent vers l'étape suivante), mais le `POST` réussi de l'étape 3 lève **`RuntimeError: Catalogue non initialisé`** (`dofus_stuff/web/__init__.py::get_catalog`). La frontière est donc nette : **SIMP-01 est sans catalogue ; SIMP-02/SIMP-03 exigent un catalogue, n'importe lequel.**

### M13 — Conventions de fichier mesurées (CRLF, UTF-8 sans BOM)

Comptage octet par octet (`\r\n`, `\n` seuls, BOM, décodage UTF-8 strict) sur les fichiers réellement écrits par les phases précédentes :

| Fichier | `\r\n` | `\n` seuls | BOM | UTF-8 strict |
|---------|--------|------------|-----|--------------|
| `docs/cli.md` | 195 | 0 | non | oui |
| `docs/installation.md` | 141 | 0 | non | oui |
| `docs/sommaire.md` | 20 | 0 | non | oui |
| `README.md` | 125 | 0 | non | oui |
| `tests/conftest.py` | 262 | 0 | non | oui |
| `tests/test_docs_cli.py` | 1 060 | 0 | non | oui |
| `tests/test_docs_code_anchor.py` | 255 | 0 | non | oui |
| `tests/test_docs_structure.py` | 603 | 0 | non | oui |
| `tests/test_web.py` | 758 | 0 | non | oui |

**Convention confirmée :** `docs/*.md` et `tests/*.py` sont **100 % CRLF**, sans BOM, en UTF-8 strict. Écrire la nouvelle page ou le nouveau module en LF ferait diverger le diff de tout le dépôt (leçon déjà coûteuse : « ce bit every prior executor »). Les comparaisons de contenu des tests doivent rester **tolérantes** (D-11 normalise déjà les espaces, donc les fins de ligne).

### M14 — Contraintes structurelles déjà actives sur une nouvelle page `docs/`

Relevé sur `tests/test_docs_structure.py` (lu) — la nouvelle page doit satisfaire, **sans qu'aucun test existant ne soit modifié** :

| Contrainte | Mécanisme | Valeurs mesurées aujourd'hui |
|------------|-----------|------------------------------|
| Une seule page d'index, exhaustive et **bidirectionnelle** | `problemes_index(docs_dir)` via `test_sommaire_lists_every_document` | `docs/` contient 3 `.md` ; l'index en liste 2 (`Installation`, `CLI`) + le sommaire se compte dans l'exhaustivité ⇒ ajouter la page **sans** sa ligne d'index fait échouer la suite |
| H1 unique **égal au libellé d'index** | `problemes_h1(docs_dir, normalize)` | normalisé (accents/casse/HTML) |
| Libellés d'index **uniques**, sommaire non auto-listé | `test_sommaire_index_labels_are_unique` | les libellés existants sont `Installation` et `CLI` |
| Ligne de retour vers `docs/sommaire.md` | `problemes_retour_sommaire(docs_dir)` | présent sur les 3 pages |
| Tous les liens relatifs résolvent, aucune ancre `#`, aucun chemin absolu | `problemes_liens(docs_dir)` | tout lien vers une page **inexistante** casse la suite (D-44) |
| UTF-8 strict, aucun jeton de brouillon (`todo`, `a completer`, `lorem`), longueur minimale | `problemes_encodage(docs_dir, normalize)`, `LONGUEUR_MINIMALE = 300` | 300 est un seuil de **page**, pas de section |
| `## Parcours conseillé` listé en texte numéroté, **sans liens** | contrainte de phase 1 (D-04) | déjà 7 entrées en prose, dont « 2. Parcours simplifié » : **aucun changement requis** |
| Pas de `db clear` sur `docs/installation.md` | `test_no_destructive_command_in_installation` | garde **locale** à `installation.md` ; la nouvelle page n'a aucune raison de citer une commande destructive |

### M15 — Le harnais existant : signatures réelles des helpers à réutiliser (D-12)

Relevé dans `tests/conftest.py` (lu intégralement) — **ne rien recopier, ne rien re-déclarer** :

| Fixture exposée | Ce qu'elle rend | Signature / contrat réel |
|-----------------|-----------------|--------------------------|
| `catalog` | un `Catalog(version="9.9.9.9", items=_sample_items())` : 3 équipements (Épée de Boisaille lvl 7, Cape d'Atcham lvl 40, Cape Rouge lvl 10), 1 ressource, 1 panoplie | fixture simple (fonction) |
| `app` | une application Flask avec **`load_catalog=False`** et le catalogue injecté, `TESTING = True`, sur un `data_dir=tmp_path/"data"` où une mini-base est créée puis fermée | dépend de `catalog`, `tmp_path` ; `yield` puis `catalog.close()` |
| `client` | `app.test_client()` | dépend de `app` |
| `docs_dir` | `Path(__file__).resolve().parents[1] / "docs"` | `scope="session"` |
| `normalize` | **rend le helper** `_normalize`, jamais une valeur normalisée | `html.unescape` → NFKD → suppression des diacritiques → espaces réduits → `strip().lower()` |
| `lignes_de_code` | rend le helper `_lignes_de_code(texte)` : **toutes** les lignes de blocs de code, toutes balises | `scope="session"` |
| `lignes_exemple` | rend le helper `_lignes_exemple(texte)` : seulement les blocs balisés `console` | `scope="session"` |
| `sections` | rend le helper `_sections(texte)` → `list[(titre_h2 | None, corps)]`, l'en-tête avant le premier `##` étant la section de titre `None` | `scope="session"` |
| `section` | rend le helper `_section(texte, titre, page)` → corps d'une section de niveau 2 ; **`page` est obligatoire, sans valeur par défaut** : un appel sans `page` lève `TypeError` (D-13, D-31) | `scope="session"` ; lève `AssertionError` nommant la page si la section est absente |

**Patrons existants à imiter** (relevés, pas supposés) :

- **Rendu Flask** : `tests/test_recommend.py:68-82` (`test_quick_flow_and_advanced`) — `client.post("/optimize/quick/classe", data={"cmd": "Crâ"}, follow_redirects=True)` puis `assert b"2/3" in response.data` ; et `patch("dofus_stuff.web.routes._run_optimize_and_redirect", return_value="computed")` pour tester l'étape 3 **sans** faire tourner le solveur. **C'est la façon la moins chère de tester SIMP-01** : elle est déjà verte et ne coûte rien.
- **Écran de résultat paginé** : `tests/test_web.py:522-585` (`test_optimize_result_pagination`) injecte `sess["optimize_result_lines"] = [...]` par `client.session_transaction()` puis lit les pages. **Patron déterministe et instantané** pour le critère 2 — il ne dépend ni du solveur, ni du catalogue.
- **Ancrage libellé → source** : `tests/test_docs_code_anchor.py:60-74` (`LIBELLES_SOURCE`) + `:240-255` (`test_libelles_cites_sont_produits_par_le_code`) — pour chaque libellé : présence côté page **et** `porteur` + littéral sur une **même ligne** du fichier source. C'est le patron exact à reprendre pour `MAX_SAVES`, `DOFUSBOOK_IMPORT_URL`, `PAGE {page}/{total}`, les trois questions et `AVANCE`.
- **Constats accumulés, une seule assertion** : `tests/test_docs_cli.py:985-990` clôt chaque test par `assert not constats, …` avec un message qui cite la page, l'attendu et la source.
- **Garde d'exécution** : `tests/test_docs_cli.py:993-1035` (`test_sans_execution_ni_base_locale`) analyse **son propre module** par `ast` avec `IMPORT_PRODUIT_AUTORISE = "dofus_stuff.cli"` et `INTERDITS_EXECUTION = ("subprocess", "socket", "sqlite3")`. ⚠️ **Cette garde est locale au module** : le nouveau module d'ancrage **doit** importer `dofus_stuff.web` (D-32) et ne peut donc pas reprendre cette liste. Si une garde analogue est souhaitée, son allow-list doit être **propre** au nouveau module (`dofus_stuff.web`, `dofus_stuff.optimize.recommend`, `dofus_stuff.web.dofusbook_export`) et jamais élargir celle de `test_docs_cli.py`.
- **Promotion vers `conftest.py`** : D-12 autorise la promotion **seulement** s'il n'existe pas d'équivalent. Relevé : `_texte_page(docs_dir)` (`test_docs_cli.py:233-245`) et la normalisation sont **déjà** partagées par fixture ; un helper « lire une page avec message localisant » n'existe **pas** dans `conftest.py` et serait le seul candidat légitime — mais il **dupliquerait** le rôle de `_texte_page`, donc il est **à ne pas promouvoir** (la promotion créerait deux exemplaires divergents, exactement ce que D-12 interdit). Conclusion : **aucune promotion nécessaire** ; les helpers utiles (`_section`, `_normalize`, `sections`) sont déjà exposés.

### M16 — Le patron de lecture des libellés CLI (D-33), transposé

`dofus_stuff/optimize/profile_input.py` est déjà sondé par `tests/test_profile_input.py`. Pour les invites, le patron de la phase 2 s'applique tel quel : lire le fichier, exiger que le libellé cité par la page et son porteur (`input_fn("…")`) soient sur la **même ligne**. Les invites mesurées en M5 sont les seules du module (7 occurrences de `input_fn(`, dont deux paires de chemins alternatifs) — la table de M5 les couvre toutes.

## Architecture Patterns

### System Architecture Diagram

```text
Lecteur (navigateur, clavier)
        │  saisit « cmd » dans <input name="cmd" maxlength="40">
        ▼
[POST /optimize/quick/<step>]  ── gardes d'étape (session["recommendation_input"])
        │
        ├─ cmd.upper() == "AVANCE" ─────────► /optimize/wizard/recap      (frontière phase 4)
        ├─ étape classe  : nombre 1..19 ou nom accent/casse-insensible
        ├─ étape elements: séparateurs « , + espace », 1..4, « multi » seul
        ├─ étape niveau  : entier 1..200
        │        └─ succès ─► recommendation_spec() ─► optimize_stuff(catalogue)
        │                              │
        │                              └─► session["optimize_result_lines"] + session["optimize_result_build"]
        │                                        └─ 302 ─► /optimize/result
        └─ saisie refusée ─► flash(message) ─► MÊME écran (200) : le message va dans la LIGNE DE STATUT
                                                │
                                                ▼
[GET /optimize/result?page=N]  ── wrap_lines(100) ─► paginate(18) ─► _screen(pgm="OPT-03")
        │                                    │
        │                                    └─ carte « PAGE {N}/{total} » insérée dans la ligne de statut
        ▼
Rendu HTML  « screen.html »
        ├─ lignes du corps visibles  ← la seule vérité lisible par le lecteur
        ├─ data-body-page / data-body-total / data-mode="result"
        └─ data-stuff-payload = {lines:[…], slots:{…}, level}   ⚠ contient TOUT le résultat sur CHAQUE page
                                                │
        ┌───────────────────────────────────────┼───────────────────────────────────────┐
        ▼                                       ▼                                       ▼
  « SAVE [NOM] » (JS)                    « DB » (POST)                        « SAVES » (POST)
  localStorage[SAVES_KEY]                _open_dofusbook()                    écran SAV-01 (/saves)
  évince la plus ancienne                webbrowser.open_new_tab(url)         liste rendue par JS
  au-delà de 20 (JS, non testable)       build_dofusbook_url(slots, level)    détail ─► « DB DOFUSBOOK »
                                         (10 groupes, prysma exclu)              └─► POST /optimize/dofusbook-url
```

### Recommended Project Structure

```text
docs/
├── sommaire.md              # gagne UNE ligne d'index vers la nouvelle page (D-39)
├── installation.md          # inchangée (phase 1)
├── cli.md                   # inchangée ; propriétaire de la surface de commandes (D-37)
└── parcours-simplifie.md    # ← LA page de cette phase
tests/
├── conftest.py              # helpers partagés : ne rien recopier, rien promouvoir (D-12)
├── test_docs_structure.py   # inchangé ; contraint la nouvelle page (M14)
├── test_docs_code_anchor.py # inchangé ; patron d'ancrage libellé → source
├── test_docs_cli.py         # inchangé ; patron « constats accumulés »
└── test_docs_parcours.py    # ← le nouveau module d'ancrage (nom au choix, Claude's Discretion)
```

### Pattern 1 : rendre, pas lire — la sonde de rendu qui extrait le corps visible

**What:** obtenir la vérité d'un écran en l'exécutant (client de test Flask) et en extrayant les **lignes du corps**, jamais le HTML brut.
**When to use:** pour chaque libellé, chaque menu et chaque message cité par la page (SIMP-01, SIMP-02).
**Example:**

```python
# Source : patron mesuré tests/test_recommend.py:68-82 + tests/conftest.py (fixture `client`)
BODY_ROW = re.compile(r'<div class="row">(.*?)</div>', re.S)

def lignes_du_corps(resp) -> list[str]:
    """Lignes visibles du corps (18 lignes), jamais le HTML entier."""
    texte = resp.get_data(as_text=True)
    corps = texte.split('id="body">', 1)[1].split('<div class="row status', 1)[0]
    return [ligne.rstrip() for ligne in BODY_ROW.findall(corps)]

def statut(resp) -> str:
    """Ligne de statut : c'est elle qui porte « PAGE {n}/{total} » et les messages d'erreur."""
    texte = resp.get_data(as_text=True)
    return texte.split('<div class="row status', 1)[1].split(">", 1)[1].split("</div>", 1)[0]
```

### Pattern 2 : correspondance numéro ↔ libellé **scopée par section** (critère 5, D-34)

**What:** lire la vérité dans le rendu, la comparer à la page **section par section**.
**When to use:** le menu des classes et le menu des éléments.
**Example — patron dont la morsure a été prouvée** (voir § Code Examples pour la preuve) :

```python
# Source : prototype exécuté .gsd-tmp/research-p3/proto_negative.py (vert sur page correcte, rouge sur 4 mutations)
def couples_section(texte: str, titre: str, page: str) -> list[tuple[int, str]]:
    """Couples (numéro, libellé) lus DANS la section — jamais sur toute la page."""
    corps = section(texte, titre, page)          # helper partagé de tests/conftest.py (D-12)
    return [(int(m.group("numero")), m.group("libelle").strip())
            for ligne in corps.splitlines() for m in COUPLE_TABLE.finditer(ligne)]
```

### Pattern 3 : ancrage libellé → porteur sur la même ligne (D-40, D-42)

**What:** chaque constante citée par la page est prouvée présente dans le code **et** sur la ligne qui la porte.
**When to use:** `MAX_SAVES`, `DOFUSBOOK_IMPORT_URL`, `PAGE {page}/{total}`, les trois questions, `AVANCE`, `capital = 5 * (level - 1)`, les deux expressions de paliers.
**Example:**

```python
# Source : tests/test_docs_code_anchor.py:61-74 et :246-255 (patron LIBELLES_SOURCE, déjà éprouvé)
CONSTANTES = [
    # (libellé cité par la page, fichier source, porteur sur la même ligne, section de la page)
    ("MAX_SAVES = 20", "dofus_stuff/web/static/js/terminal.js", "MAX_SAVES = 20", "## Sauvegarder"),
    ("PAGE {page}/{total}", "dofus_stuff/web/routes.py", 'f"PAGE {page}/{total}"', "## Lire le résultat"),
    ("5 * (level - 1)", "dofus_stuff/optimize/recommend.py", "5 * (level - 1)", "## Ce que l'outil suppose"),
]
```

### Pattern 4 : prouver l'entrée « acceptée » **et** l'entrée « refusée », avec le message

**What:** ne pas se contenter d'un `302` : le refus est un `200` sur le même écran, avec le message dans la ligne de statut.
**When to use:** SIMP-01 (critère 1).
**Example:**

```python
# Source : mesure M3 (matrice exécutée), messages lus dans le rendu
def refus(resp, message: str) -> bool:
    """Le refus n'est PAS un code d'erreur : c'est un 200 + message en ligne de statut."""
    return resp.status_code == 200 and statut(resp).startswith(message)
```

### Anti-Patterns to Avoid

- **Chercher un libellé dans `response.data`** : `data-stuff-payload` contient **tout** le résultat sur **chaque** page (M6) — l'assertion serait verte sur la mauvaise page. Toujours passer par les lignes du corps.
- **Un dictionnaire `numéro → libellé` global** : le menu des éléments (1–4) écrase le menu des classes (1–19). Mesuré : fait **échouer** le contrôle sur une page correcte (Pitfall 1).
- **Ancrer sur la base réelle** : non déterministe (6 puis 7 pages, deux méthodes) et ~9,5 s par exécution (M11).
- **Poster `cmd=DB` sans patcher `webbrowser.open_new_tab`** : le test ouvre un navigateur (M9).
- **Ouvrir `.data/` « pour avoir des données vraies »** : `Database.open()` écrit (`CREATE TABLE` sur un schéma absent) — la règle C3 protège ce fichier, et M12 montre que l'ouverture laisse le fichier intact **seulement** parce que le schéma existe déjà.
- **Recopier la surface de commandes** dans la page : elle appartient à `docs/cli.md` (D-37).
- **Décrire les écrans du wizard** depuis le rendu de `AVANCE` : frontière de la phase 4 (D-43).
- **Écrire la nouvelle page en LF** : tout `docs/` et tout `tests/` est en CRLF (M13).

## Don't Hand-Roll

| Problème | Ne pas construire | Utiliser | Pourquoi |
|----------|-------------------|----------|----------|
| Rendre un écran hors-ligne | Un serveur Flask de test, un `app.run()`, un port | `create_app(...).test_client()` (fixture `client`) | Déjà écrit, éprouvé, sans socket ; c'est la seule source du « rendu réel » (D-32) |
| Comparer des libellés accentués | Un `==` strict ou un `casefold()` maison | La fixture `normalize` (`html.unescape` + NFKD + diacritiques + espaces, D-11) | Le rendu contient `&lt;`, `&#39;` et des accents : un `==` strict produit des faux négatifs |
| Extraire des lignes de la page | Un parseur Markdown maison | Le scanner de blocs de `conftest.py` (`lignes_de_code`, `lignes_exemple`) et `section(texte, titre, page)` | Le scanner est unique et déjà exigé par les phases 1-2 (D-12) |
| Vérifier l'ordre des 10 groupes Dofusbook | Un nouveau décodage base64/msgpack | `tests/test_web.py:638-665` et `:713-750` | Déjà couvert et **plus précis** (régression cape-avant-chapeau) ; D-12/D-17 interdisent la duplication |
| Éprouver la limite de 20 sauvegardes | Un moteur JS, `playwright`, un navigateur piloté | Lecture source ancrée (littéral + porteur sur la même ligne, patron `LIBELLES_SOURCE`) | Aucun moteur JS dans l'environnement (C1) ; c'est une contrainte, pas un contournement — la nature du contrôle doit être dite dans la page/le test |
| Fabriquer un catalogue de test | Une fixture qui ouvre `.data/` | La fixture `catalog` (D-12) | C3 et M12 : l'ouverture est en écriture |

**Key insight :** dans ce domaine, tout ce qu'on serait tenté de « construire » (parseur de page, moteur de rendu, catalogue de test) **existe déjà** dans le dépôt, et les phases 1-2 ont payé pour les rendre uniques (D-12). La seule chose réellement nouvelle à écrire est le **couplage rendu ↔ page**, et il doit passer par le client de test de la fixture.

## Common Pitfalls

### Pitfall 1 : un dictionnaire `numéro → libellé` global — le contrôle rougit sur une page **correcte**

**What goes wrong:** le contrôle lit tous les couples de la page et les met dans un dict plat. Le menu des éléments (`1. Terre`, `2. Feu`, `3. Eau`, `4. Air`, `routes.py:993`) écrase les quatre premiers du menu des classes (`1. Cra`…`4. Eniripsa`). Le contrôle rapporte alors **quatre** constats sur une page parfaitement juste.
**Why it happens:** les deux menus partagent la même plage de numéros 1–4, et la page les cite tous les deux.
**How to avoid:** lire et comparer **section par section** (`section(texte, titre, page)`), jamais sur le texte entier.
**Warning signs:** quatre constats exactement, portant sur les numéros 1 à 4, avec des libellés d'éléments en face d'attendus de classes.
**Preuve mesurée (session de recherche) :** la première version du prototype, globale, a rapporté `[1 → Terre ; 2 → Feu ; 3 → Eau ; 4 → Air]` **sur la page correcte**. Corrigé par section : `constats == []` ⇒ `VERT`. C'est exactement la classe de défaut que la revue de la phase 2 a mesurée (« les trous étaient dans le harnais, pas dans la page »).

### Pitfall 2 : `data-stuff-payload` rend l'assertion sur `response.data` fausse sur la bonne page

**What goes wrong:** `assert "Score" in response.data` est **vrai sur la page 1** alors que le lecteur ne voit `Score` qu'à la fin. Inversement `assert "Méthode" in response.data` est **faux sur la page 1**, parce que `tojson` échappe l'accent en `\u00e9`.
**Why it happens:** `_result_screen` passe `stuff_payload={"lines": list(lines), …}` (`routes.py:1364`) et `screen.html:21` le sérialise en attribut **sur chaque page**.
**How to avoid:** extraire les lignes du corps (Pattern 1) ; si la charge utile doit servir, la décoder explicitement (`html.unescape` puis `json.loads`).
**Warning signs:** un constat vert alors que la ligne n'apparaît sur aucun écran, ou un constat rouge dont le libellé contient un accent.

### Pitfall 3 : ancrer sur la base réelle (non déterministe et coûteux)

**What goes wrong:** le test devient flaky (nombre de pages 6 ou 7, méthode `cpsat_feasible+local` ou `greedy`) et coûte ~9,5 s par exécution — pour deux assertions.
**Why it happens:** `time_limit_s=8` et l'issue de CP-SAT décident du chemin (`Méthode : {result.method} ({cpsat_status})`).
**How to avoid:** fixture minimale (déterministe, 0,02–0,29 s) ; pour l'écran de résultat, injecter les lignes par `client.session_transaction()` comme `tests/test_web.py:522`.
**Warning signs:** une assertion sur `Méthode : cpsat` ou sur un total de pages codé en dur.

### Pitfall 4 : croire que le refus d'entrée est un code d'erreur

**What goes wrong:** le test attend `400` et reçoit `200` (ou l'inverse : il asserte `200` et ne regarde pas le message).
**Why it happens:** `optimize_quick` **ne redirige pas** en cas de `ValueError` : il `flash` puis re-rend le même écran (`routes.py:984-985,1005`). Le message est dans la **ligne de statut**, concaténé avec `ENTREE=SUIVANT`/`ENTREE=CALCULER` (`routes.py:146-150`).
**How to avoid:** asserter sur le **début** de la ligne de statut, et vérifier que le corps est identique à celui du même écran sans erreur.
**Warning signs:** un `assert b"Saisissez" in response.data` qui passe aussi sur la page d'un autre écran (le message n'est jamais dans le corps).

### Pitfall 5 : oublier que l'étape 3 réussie exige un catalogue

**What goes wrong:** un test qui rend les trois questions avec `create_app(catalog=None, load_catalog=False)` réussit aux étapes 1 et 2 puis lève `RuntimeError: Catalogue non initialisé` à l'étape 3.
**Why it happens:** `_run_optimize_and_redirect` appelle `get_catalog()` (`routes.py:912`).
**How to avoid:** utiliser la fixture `client` (qui fournit un catalogue) dès qu'un scénario franchit l'étape 3, ou patcher `dofus_stuff.web.routes._run_optimize_and_redirect` (patron `tests/test_recommend.py:75`).
**Warning signs:** une exception `RuntimeError` en 500 au lieu d'une redirection.

### Pitfall 6 : fins de ligne et encodage (le piège qui a coûté un cycle à chaque exécuteur)

**What goes wrong:** la nouvelle page ou le nouveau module est écrit en LF (ou avec un BOM) ; le diff du dépôt devient mixte et les conventions mesurées (M13) sont rompues.
**Why it happens:** les outils Unix par défaut produisent LF ; `docs/` et `tests/` sont **100 % CRLF**, sans BOM.
**How to avoid:** écrire avec `newline="\r\n"` (ou vérifier après écriture) ; ne **jamais** asserter sur les octets de fin de ligne (D-11 normalise déjà, et le dépôt n'a pas de `.gitattributes`).
**Warning signs:** un `\n` seul compté dans `docs/parcours-simplifie.md` ou dans le nouveau module.

### Pitfall 7 : l'interpréteur ambiant n'a pas pytest

**What goes wrong:** `python -m pytest` échoue avec `No module named pytest`, ou pire : un test « passe » sous un autre interpréteur sans les mêmes dépendances.
**Why it happens:** l'hôte a un Python ambiant sans pytest ; le venv du projet (`Python 3.14.7`) porte pytest 9.1.1.
**How to avoid:** toujours `.venv/Scripts/python.exe -m pytest -q` depuis la racine.
**Warning signs:** un code de sortie différent de 0 sans sortie de test.

### Pitfall 8 : la tolérance de préfixe d'`argparse` — ne pas la transposer aux menus

**What goes wrong:** un contrôle écrit « le libellé accepté est-il un préfixe ? » pour les **menus** de classe, par analogie avec `argparse` (dont la leçon est écrite dans `tests/test_docs_cli.py:21-29` : `--force-sync` reste accepté après renommage en `--force-synchronisation`).
**Why it happens:** la phase 2 a montré que `parse_args` accepte un préfixe non ambigu ; on en déduit à tort que la saisie de classe l'accepte aussi.
**How to avoid:** mesurer — `eliotrop` est **refusé** (M3), la comparaison est une **égalité** après normalisation d'accents (`routes.py:960`), pas un `startswith`. La seule tolérance réelle est accents/casse/espaces autour, plus `int()` sur les chiffres.
**Warning signs:** une page affirmant que « le début du nom suffit ».

### Pitfall 9 : croire qu'un contrôle JS est exécutable

**What goes wrong:** on planifie un test « sauvegarde 21 fois, vérifie l'éviction » — impossible sans moteur JS.
**Why it happens:** `MAX_SAVES`, `localStorage`, `shift()` et les statuts vivent dans `terminal.js` (631 lignes), hors de portée de pytest.
**How to avoid:** assumer la frontière : ancrage **source** pour le comportement JS (littéral + porteur sur la même ligne), ancrage **rendu** pour ce que le serveur expose (`SAV-01`, la ligne de statut du résultat, `data-mode="result"`, la présence de `data-stuff-payload`). La page doit dire ce que le lecteur fait, pas promettre un refus poli qui n'existe pas (l'éviction est silencieuse, M8).
**Warning signs:** un plan qui prévoit `playwright` ou `node`.

## Code Examples

Tous les extraits ci-dessous viennent du **prototype réellement exécuté** dans cette session (`.gsd-tmp/research-p3/`), et leurs sorties sont celles mesurées.

### Preuve de morsure du contrôle du critère 5 (assertion négative, D-34)

Le prototype a été exécuté contre **cinq artefacts** : une page construite **depuis le rendu** (donc correcte par construction), trois pages mutées, et une exécution avec dérive **côté code**.

```text
$ .venv/Scripts/python.exe .gsd-tmp/research-p3/proto_negative.py page_correcte.md
couples rendus (elements) : [(1, 'Terre'), (2, 'Feu'), (3, 'Eau'), (4, 'Air')]
constats                  : aucun
VERT                                                             -> code de sortie 0

$ .venv/Scripts/python.exe .gsd-tmp/research-p3/proto_negative.py page_mutee.md   # 6 et 9 inversés
AssertionError: docs/parcours-simplifie.md : dans « ## Le menu des classes », le numero 6 est
associe au libelle « Iop » ; attendu « Feca » (couple « 6. Feca » tel que rendu par
dofus_stuff/web/routes.py:989)
docs/parcours-simplifie.md : dans « ## Le menu des classes », le numero 9 est associe au libelle
« Feca » ; attendu « Iop » (couple « 9. Iop » tel que rendu par dofus_stuff/web/routes.py:989)
                                                                 -> code de sortie 1

$ .venv/Scripts/python.exe .gsd-tmp/research-p3/proto_negative.py page_mutee_numero.md  # numero 6 -> 3
AssertionError: … le numero 3 est associe au libelle « Feca » ; attendu « Eliotrope » …
                … le numero 6 n'est associe a aucun libelle ; attendu le couple « 6. Feca » …
                                                                 -> code de sortie 1

$ .venv/Scripts/python.exe .gsd-tmp/research-p3/proto_negative.py page_mutee_element.md  # 1 <-> 3
AssertionError: … dans « ## Le menu des elements », le numero 1 est associe au libelle « Eau » ;
                attendu « Terre » (couple « 1. Terre » tel que rendu par dofus_stuff/web/routes.py:993)
                                                                 -> code de sortie 1

$ .venv/Scripts/python.exe .gsd-tmp/research-p3/proto_negative.py page_incomplete.md  # ligne 9. Iop supprimée
AssertionError: … le numero 9 n'est associe a aucun libelle ; attendu le couple « 9. Iop » …
                                                                 -> code de sortie 1

$ GSD_P3_DERIVE=1 .venv/Scripts/python.exe .gsd-tmp/research-p3/proto_negative.py page_correcte.md
derive injectee : CLASSES permute (6 <-> 9)
AssertionError: … le numero 6 est associe au libelle « Feca » ; attendu « Iop » (couple « 6. Iop »
                tel que rendu par dofus_stuff/web/routes.py:989) …
                                                                 -> code de sortie 1
```

Trois enseignements directement réutilisables par le plan :

1. **Le contrôle est vert sur l'artefact non muté** (critère 5 satisfait dans les deux sens) — condition indispensable, mesurée explicitement.
2. **Il mord sur une dérive de la page *et* sur une dérive du code** (la permutation `CLASSES` est injectée à chaud sur `dofus_stuff.web.routes`, sans toucher au dépôt) : le même contrôle attrape « la page s'est trompée » et « le code a bougé sous la page ».
3. **Le message d'échec cite la page, la section, le couple attendu et le fichier:ligne** (D-13, D-42) — le harnais est utilisable sans relire le code.

### Extraction des couples rendus (la vérité du critère 5)

```python
# Source : mesure — rendu de GET /optimize/quick/classe (fixture minimale)
# routes.py:989 : body += ["    ".join(f"{j + 1:2}. {CLASSES[j]:12}" for j in range(i, min(i + 3, len(CLASSES))))
#                         for i in range(0, len(CLASSES), 3)]
COUPLE_RENDU = re.compile(r"(?P<numero>\d{1,2})\.\s+(?P<libelle>[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ' -]*)")
# couples rendus mesurés :
# [(1, 'Cra'), (2, 'Ecaflip'), (3, 'Eliotrope'), (4, 'Eniripsa'), (5, 'Enutrof'), (6, 'Feca'),
#  (7, 'Forgelance'), (8, 'Huppermage'), (9, 'Iop'), (10, 'Osamodas'), (11, 'Ouginak'), (12, 'Pandawa'),
#  (13, 'Roublard'), (14, 'Sacrieur'), (15, 'Sadida'), (16, 'Sram'), (17, 'Steamer'), (18, 'Xelor'),
#  (19, 'Zobal')]
```

### Sonde d'acceptation d'une entrée, par différence de code de retour (SIMP-01)

```python
# Source : mesure M3 — le succès redirige (302), le refus re-rend l'écran (200 + message en statut)
def verdict(client, etape: str, valeur: str) -> str:
    r = client.post(f"/optimize/quick/{etape}", data={"cmd": valeur})
    if r.status_code == 302:
        return f"ACCEPTE -> {r.headers['Location']}"
    return f"REFUSE -> {statut(r).split(' — ')[0]!r}"
# mesuré : verdict(client, "classe", "019") == "ACCEPTE -> /optimize/quick/elements"
#           verdict(client, "elements", "multi terre") == "REFUSE -> 'Exemple : feu, terre air, ou multi.'"
```

### Atteindre l'écran de résultat sans solveur (critère 2, patron déjà présent)

```python
# Source : tests/test_web.py:522-527 (patron mesuré, 0 s, déterministe)
with client.session_transaction() as sess:
    sess["optimize_result_lines"] = [
        "Niveau 200 — Force / Agilité",
        "Points inclus ; sans exo/parchemins. Jets moyens sauf réglage avancé.",
        "Équipement :",
        "  hat      : Diadème (#20360, niv. 200)",
        "Méthode : cpsat (OPTIMAL)",
        "Score : 6021.8  |  Indice de recherche : 84.6% [borne_solver]",
        "Recherche sur une sélection du catalogue ; optimalité globale non garantie.",
        "Greedy: 5772.6 | UB0: 9343.0",
    ]
    sess["optimize_result_build"] = {"slots": {"hat": 20360}, "level": 200}
rv = client.get("/optimize/result")
# mesuré : la carte est dans la ligne de statut, jamais dans le corps
# statut(rv) == "ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB — PAGE 1/1 — ENTREE=VALIDER"
```

## Écarts avec les critères du ROADMAP (à porter au plan — section à lire en entier)

> Cette section existe parce que **deux affirmations d'un critère de succès ne sont pas adossées au code tel qu'il se rend**. D-35/D-41 exigent qu'elles soient soit retirées, soit explicitement présentées comme une interprétation du parcours lecteur — jamais présentées comme une vérité de code. Le plan doit trancher, pas contourner.

### ÉCR-1 — Critère 2, « table de correspondance libellé tronqué → nom complet de slot » : **la troncature n'existe pas dans ce flux**

**Mesuré :** zéro ligne rendue contient `…` (sur toutes les pages, en fixture **et** sur copie de la base réelle) ; la largeur maximale d'une ligne rendue est exactement `100 = COLS` (les lignes sont **enveloppées** avant le clip) ; tous les libellés de slot rendus font **au plus 7 caractères** (`ring_a`, `dofus_1`…) et sont **complétés** par `f"  {slot:8s} : "`, jamais coupés.

**Conséquence pour le plan :** la table du critère 2 ne peut pas être « libellé **tronqué** → nom complet ». Deux issues conformes à D-41 :

1. **Reformuler la table** en « libellé **technique court** → nom complet du slot » (le besoin réel du lecteur : que veut dire `ring_a`, `dofus_3`, `prysma` ?), adossée à `api.py:362-380` — **recommandé**, car c'est ce que le lecteur rencontre vraiment et c'est mesurable.
2. **Documenter la troncature comme un cas possible ailleurs** (écrans non couverts par cette phase) **et** dire que sur le parcours simplifié aucune ligne n'est coupée — à condition de nommer la règle réelle (`clip`, `screens.py:14-20`, largeur `COLS = 100`, remplacement du dernier caractère par `…`) et de **ne pas** prétendre qu'elle se déclenche ici.

Dans les deux cas : **ne pas** ancrer un test sur l'apparition de `…` — il serait rouge sur une implémentation correcte (leçon WR-01/02 de la phase 2, et `CHARGEMENT DES SAUVEGARDES LOCALES…` en M8 qui contient déjà un `…`).

### ÉCR-2 — Critère 2, « emplacement réel de `Méthode`, `Score`, `Indice de recherche` (**dernière page**) » : vrai sur une panoplie complète, **faux sur la fixture**

**Mesuré :** dernière page (6/6, 7/7) sur la copie de la base réelle ; page **2 sur 3** avec la fixture (niveau 200, `multi`), page 2 sur 2 (niveau 150, `terre`).

**Conséquence pour le plan :** l'assertion ne doit pas porter sur `page == total`. Elle doit porter sur ce qui est vrai **dans les deux cas** et qui décrit le lecteur :

- les trois libellés apparaissent **après** la section « Équipement : » et **avant** la ligne `Greedy: … | UB0: …`, dans la concaténation ordonnée des pages ;
- la dernière page est atteignable et son statut affiche `PAGE {total}/{total}` ;
- la ligne `Recherche sur une sélection du catalogue ; optimalité globale non garantie.` suit immédiatement le bloc de diagnostics.

**Recommandation de rédaction :** la page dit « en **fin de résultat** — naviguez jusqu'à `PAGE n/n` » plutôt que « dernière page » ; si le plan tient à la formule du ROADMAP, il doit alors la qualifier (« sur une panoplie complète, en fin de résultat, donc sur la dernière page ») **et** ne pas la transformer en assertion sur l'indice de page. Contrôle complémentaire possible, purement déterministe : la **queue** de `data-stuff-payload["lines"]` (décodée) doit être `[…, "Méthode : …", "Score : … | Indice de recherche : …", "Recherche sur une sélection…", "Greedy: …"]`.

### ÉCR-3 — Critère 4, « heuristiques de classe » : **confirmées par le code** (pas un écart, mais une correction de l'hypothèse de recherche)

L'hypothèse à réfuter était : « les heuristiques de classe ne sont peut-être adossées à rien ». **Réfutée par la mesure** : `recommend.py:44-54` ajoute des objectifs selon la classe (distance, mêlée, `Portée` 2/4 selon le niveau, `Invocation` base 1 cible 3) — mesuré classe par classe (M10). La seule prudence à garder : le code lui-même écrit `# Broad playstyle preferences, not a simulation of class spells.` ⇒ la page présente ces préférences comme des **hypothèses de style de jeu**, pas comme une simulation de classe, et signale que **9 des 19 classes n'ont aucun objectif propre** (mesuré).

### ÉCR-4 — Critère 4, « ni exo ni parchemins » : vrai dans les faits, mais l'écran affiche le mot « parcho »

**Mesuré :** aucun `exo`/`scroll` non nul dans le spec généré (M10) ; et la ligne de détail rendue s'appelle `Détail {primary} — base+parcho: … | items: … | sets: …` (`api.py:429`). Le lecteur voit donc « parcho » à l'écran. La page doit lever l'ambiguïté en une phrase (base + parchemins saisis = 0 ici), pas l'ignorer.

### ÉCR-5 — Critère 3, « la sauvegarde navigateur (**20 maximum**) » : vraie, mais l'éviction est **silencieuse**

Le code n'affiche pas « maximum atteint » : il fait `stuffs.shift()` tant que la liste est pleine (`terminal.js:295-297`). Écrire « 20 maximum » sans dire que **la plus ancienne est remplacée** serait exact mais trompeur. La page doit nommer le comportement observé dans le code (D-35).

## Non vérifié (liste explicite)

| Élément | Pourquoi je n'ai pas pu le vérifier | Conséquence pour le plan |
|---------|-------------------------------------|--------------------------|
| **Exécution du JavaScript** (`MAX_SAVES`, éviction, `localStorage`, statuts JS, `slice(0, width-1)`) | Aucun moteur JS dans l'environnement ; `playwright`/`node` interdits (C1). Je n'ai **pas** simulé le JS | Le critère 3 est ancré par **lecture source proposée au plan** (littéral + porteur sur la même ligne), pas par un test de comportement. À dire dans la page/le test |
| **Ordre de frappe réel dans un navigateur** (`SAVE [NOM]`, `N`, `DEL N`, `PURGE OUI`, `DB`) | Ces saisies sont interceptées par un écouteur `submit` JS (`terminal.js:606-630`) ; je n'ai pas exécuté de navigateur | Ancrage source uniquement |
| **Phrase exacte du message de statut après 21ᵉ sauvegarde** | Le code calcule `"STUFF SAUVEGARDE (" + stuffs.length + "/" + MAX_SAVES + ")"` ; après éviction `stuffs.length` vaut 20 **avant** le `push`, donc le statut peut annoncer une valeur différente du total réel affiché ensuite. Je n'ai **pas** exécuté le JS pour le confirmer | **Ne pas citer ce message dans la page**, ou l'annoncer comme non vérifié. Candidat à un `checkpoint:human-verify` **non requis** : la page n'a pas besoin de ce détail |
| **Valeurs numériques d'un résultat réel** (`Score`, `Indice de recherche`, nombre de pages, `Méthode`) | Volatiles par nature (M11 : deux exécutions, deux méthodes, deux totaux de pages) | La page décrit le **format** (`Score : {n.n}` , `Indice de recherche : {n.n}% [mode]`, `PAGE {n}/{t}`), jamais une valeur |
| **Contenu réel de `.data/dofus.sqlite3`** au-delà des comptes et de la version de schéma | Lecture seule volontaire ; les valeurs (4 356 équipements, 929 panoplies) sont des **preuves de travail**, pas du contenu de page | Aucune valeur de base dans la prose (interdiction des valeurs volatiles) |
| **Rendu de `docs/parcours-simplifie.md` sur GitHub** | Le rendu distant n'est pas vérifiable hors-ligne, et aucune publication n'est autorisée | Les conventions GFM suffisent (tableaux, blocs de code) ; aucun lien externe |
| **Comportement de l'étape `classe` avec un `cmd` de plus de 40 caractères** | Le `maxlength="40"` est une contrainte **du navigateur** ; `client.post` l'ignore. Le serveur accepterait `"Cra" + "x"*100` ? → refusé par égalité, mais **je n'ai pas mesuré** un nom de classe de plus de 40 caractères (aucun n'existe) | Sans objet : la page dit « 40 caractères » comme limite du champ, mesurée dans le HTML (`maxlength="40"`) |
| **`Méthode`/`Score` sur la **dernière** page pour tous les niveaux** | Je n'ai mesuré que quelques points (niveaux 150 et 200 en fixture ; 200 sur base réelle). Un balayage complet des 200 niveaux serait long et sans valeur : la position dépend du nombre de lignes, pas du niveau | Assertion **positionnelle** (ÉCR-2), jamais sur l'indice de page |

## State of the Art

| Approche ancienne | Approche retenue ici | Quand | Impact |
|-------------------|----------------------|-------|--------|
| `GUIDE_WIZARD.md` décrit le flux en prose libre, non vérifiée | Page dérivée du **rendu réel** + module d'ancrage pytest | Depuis la phase 1, réaffirmé par D-32 | Un libellé qui bouge fait rougir la suite au lieu de périmer silencieusement |
| Description du produit par le code lu à l'œil | Rendu **exécuté** en processus (`test_client`) | Cette phase | Le seul moyen d'attraper ce qui n'est écrit nulle part : une concaténation de statut, une garde de session, un refus qui reste en 200 |
| Un seul harnais de docs « fourre-tout » | Un module par page/surface, helpers **partagés** et jamais dupliqués | Depuis la phase 1 (D-12) | Les phases 1-2 ont payé le coût deux fois (WR-04 : un helper dupliqué finit par diverger) |

**Obsolète / à ne pas réintroduire :** une capture d'écran comme source de vérité (aucune image versionnée, et une capture ne se vérifie pas) ; `.doc-agent/`/`doc-agent.toml` comme générateur (état bloqué en `PLAN`, non suivi par git, interdit de relance par `PROJECT.md`).

## Assumptions Log

| # | Affirmation | Section | Risque si faux |
|---|-------------|---------|----------------|
| A1 | Le contenu de `.gsd-tmp/research-p3/` (sondes jetables) doit être supprimé avant la fin de la phase : ce sont mes mesures, pas un livrable, et `.gsd-tmp/` n'est **pas** dans `.gitignore` (vérifié : `git status` le montre en `?? .gsd-tmp/`) | § Validation Architecture | Un répertoire de sondes suivi par git polluerait le dépôt de la phase |
| A2 | Le nouveau module d'ancrage s'appellera `tests/test_docs_parcours.py` | § Recommended Project Structure | Aucun : le nom est explicitement du ressort de Claude (CONTEXT, *Claude's Discretion*) |
| A3 | La page s'appellera `docs/parcours-simplifie.md` avec un H1 à choisir, égal à sa ligne d'index (contrainte M14) | § M14 | Moyen : le nom de fichier est fixé par `.claude/CLAUDE.md` ligne 80 (`parcours-simplifie.md`) ; seul le **libellé** est libre |
| A4 | Les deux écrans du wizard (`recap`) atteints depuis `AVANCE` ne seront **pas** décrits (D-43) | § M4 | Faible : c'est une décision verrouillée, pas une hypothèse |
| A5 | Le libellé français des slots (`ring_a` → « anneau A ») proposé en M7 est une **traduction du vocabulaire du produit**, pas une valeur rendue | § M7 | Faible si la page présente la colonne comme « nom complet du slot » (vocabulaire du jeu), jamais comme un libellé d'écran. À ne pas citer entre guillemets de rendu |

**Si ce tableau ne contient que des éléments de forme** (A1-A5) : aucune hypothèse de **fond** ne reste à confirmer ; les affirmations de fond de ce document sont mesurées, et les deux qui ne le sont pas sont listées en § « Écarts » avec leur mesure contraire.

## Open Questions

1. **Faut-il trancher ÉCR-1 par reformulation (court → complet) ou par documentation de la règle de troncature ?**
   - Ce qu'on sait : aucune ligne du parcours simplifié n'est tronquée (mesuré) ; la règle `clip` existe et se déclencherait sur une ligne > 100 caractères non enveloppée, ce qui n'arrive pas dans ce flux.
   - Ce qui n'est pas clair : la formulation exacte du critère 2 du ROADMAP parle de « libellé tronqué » — soit le mot du rédacteur, soit une observation issue d'un autre écran.
   - Recommandation : **reformuler** en « libellé technique court → nom complet », adosser la table à `api.py:362-380`, et mentionner en une phrase la règle générale de largeur (`COLS = 100`) comme limite du terminal. Le plan doit **nommer cet écart** (comme la phase 2 l'a fait pour DOCS-06) plutôt que de le taire.

2. **`Méthode`/`Score`/`Indice de recherche` : « dernière page » ou « fin de résultat » ?**
   - Ce qu'on sait : dernière page sur la base réelle (6/6, 7/7), page 2/3 sur la fixture.
   - Ce qui n'est pas clair : la contrainte du test (fixture obligatoire pour le déterminisme) rend « dernière page » non testable littéralement.
   - Recommandation : assertion **positionnelle** + carte de pagination vérifiée ; la page dit « en fin de résultat (jusqu'à `PAGE n/n`) ».

3. **Le tableau des 17 slots doit-il lister les libellés « masqués si non équipés » ?**
   - Ce qu'on sait : `pet`, `prysma`, `shield` et les six `dofus_*` n'apparaissent **que s'ils sont équipés** (`api.py:384-385`) ; les autres affichent `(vide)`.
   - Recommandation : oui, une phrase — c'est exactement le genre de détail qui fait croire à un bug (« pourquoi `prysma` n'apparaît jamais ? »).

4. **La page doit-elle mentionner le canal `DB DOFUSBOOK` de l'écran des sauvegardes ?**
   - Ce qu'on sait : `SAV-01` liste les sauvegardes (JS) et son détail expose `DB DOFUSBOOK` (`terminal.js:399-400`), qui appelle `POST /optimize/dofusbook-url` (`terminal.js:413-432`).
   - Recommandation : oui, en une phrase, en rattachant l'export **aux deux écrans qui l'exposent** (critère 3 : « rattachés à l'écran qui les expose ») : `OPT-03` (`SAVE [NOM]`, `DB`) et `SAV-01` (détail puis `DB DOFUSBOOK`).

## Environment Availability

| Dépendance | Requise par | Disponible | Version | Repli |
|------------|-------------|------------|---------|-------|
| `.venv/Scripts/python.exe` | Toute la vérification | ✓ | Python 3.14.7 | aucun — **l'interpréteur ambiant n'a pas pytest** |
| `pytest` | Toute la vérification | ✓ | 9.1.1 observé (déclaré `>=8.0`) | aucun |
| `flask` | Rendu des écrans (D-32) | ✓ | 3.x (déclaré `>=3.0`) | aucun — c'est le seul moyen de rendre |
| `ortools` | Chemin solveur (`Méthode : cpsat…`) | ✓ | 9.10+ | Le code gère l'absence : `Méthode : … (UNAVAILABLE)` + `Attention : ortools indisponible, résultat = greedy seul` (`api.py:332-336`). Non sollicité si le test injecte ses lignes par session (patron `tests/test_web.py:522`) |
| `msgpack` | Décodage de l'URL Dofusbook | ✓ (dépendance runtime) | `>=1.0` | Les tests existants de `test_web.py` le font déjà |
| `git` (commits **locaux**) | Historisation de la page et du module | ✓ | — | aucun ; **aucun push** (règles projet) |
| Moteur JavaScript / navigateur | Rien dans cette phase | ✗ | — | **Ancrage par lecture source** pour `MAX_SAVES` et le comportement d'éviction (voir § Non vérifié) |
| Réseau (`api.dofusdu.de`, `dofusbook.net`) | Rien dans cette phase | ✗ (volontairement) | — | Aucun besoin : le rendu est hors-ligne ; l'URL Dofusbook est **construite**, jamais ouverte (et `webbrowser.open_new_tab` est patché si `cmd=DB` est posté) |
| `.data/dofus.sqlite3` | Rien dans cette phase | Disponible mais **volontairement non utilisé** | 24 989 696 octets, base complète | Fixture `catalog` (3 objets) — déterministe et 300× plus rapide |

**Missing dependencies with no fallback:** aucune.
**Missing dependencies with fallback:** le moteur JS (repli = lecture source ancrée, décision D-33 transposée) et `ortools` (repli = injection de lignes, patron déjà en place).

## Validation Architecture

> `workflow.nyquist_validation = true` dans `.planning/config.json` (vérifié) : cette section est **requise**.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest` 9.1.1 (déclaré `>=8.0`) |
| Config file | `pyproject.toml` § `[tool.pytest.ini_options]` : `testpaths = ["tests"]`, `pythonpath = ["."]`, un `filterwarnings` pour `ortools` |
| Quick run command | `.venv/Scripts/python.exe -m pytest -q` (suite entière : **2,56 s**, 169 tests — mesuré avant cette phase) |
| Full suite command | `.venv/Scripts/python.exe -m pytest -q` (identique : la suite est rapide, aucun marqueur de sélection n'existe dans le dépôt) |

**Budget mesuré à respecter :** le rendu du parcours complet en fixture coûte **0,29 s** la première fois puis **0,02 s** ; l'injection de lignes de résultat par session est **instantanée**. Un module d'ancrage qui reste sous **~1 s** est compatible avec la suite actuelle (2,56 s). **Interdit :** le rendu sur la base réelle (~9,5 s **et** non déterministe).

### Les vérités de la phase → contrôle qui peut les mettre en échec

| # | Vérité à prouver (critère) | Contrôle proposé | Peut la falsifier ? |
|---|----------------------------|------------------|---------------------|
| V1 | Les trois questions et `AVANCE : personnaliser les réglages` sont rendues **telles quelles** (critère 1) | Rendre `GET /optimize/quick/classe`, puis deux `POST` valides ; exiger dans les **lignes du corps** (normalisées, D-11) `1/3 - Quelle est votre classe ?`, `2/3 - Quels éléments privilégier ?`, `3/3 - Quel est votre niveau ? (1 à 200)`, `AVANCE : personnaliser les réglages` | **Oui** : retirer la ligne `AVANCE` de `routes.py:1003` (mutation citée dans le message), ou renommer une question ⇒ rouge |
| V2 | Les entrées acceptées le sont **réellement** (critère 1) | Pour chaque entrée citée par la page (`Cra`, `crâ`, `1`, `19`, `terre air`, `terre,air`, `terre+air`, `1 3`, `multi`, `150`) : `POST` ⇒ `302` vers l'étape attendue | **Oui** : une entrée inventée ⇒ `200` + message d'erreur ⇒ rouge |
| V3 | Les refus réels le sont, avec le **message exact** (critère 1) | `POST` d'une valeur refusée ⇒ `200`, corps identique, ligne de statut commençant par le message attendu (`Saisissez le nom ou le numéro de votre classe.`, `Exemple : feu, terre air, ou multi.`, `Saisissez un niveau entre 1 et 200.`) | **Oui** : reformuler un message dans `routes.py` ⇒ rouge |
| V4 | Le couple **numéro ↔ libellé** des deux menus (critère 5) | Extraire les couples du **rendu** (classe : 19 couples ; éléments : 4), les comparer **section par section** aux couples cités par la page | **Oui, prouvé** : 6 mutations mesurées (libellé inversé, numéro décalé, élément inversé, ligne supprimée, dérive `CLASSES`) ⇒ toutes rouges, page non mutée verte |
| V5 | La carte de pagination existe et a la forme rendue (critère 2) | Sur l'écran de résultat, exiger `PAGE 1/{total} — ENTREE=VALIDER` dans la **ligne de statut**, `data-body-total` cohérent, et l'atteinte de `PAGE {total}/{total}` | **Oui** : supprimer `indicators.append(f"PAGE {page}/{total}")` (`routes.py:145`) ⇒ rouge |
| V6 | Les trois diagnostics sont **en fin de résultat** (critère 2) | Concaténer les pages dans l'ordre : exiger `Méthode : `, `Score : ` **et** `Indice de recherche : ` après la dernière ligne `Équipement :` / les statistiques et avant `Greedy: `, avec `Recherche sur une sélection du catalogue ; optimalité globale non garantie.` juste après | **Oui** : déplacer `lines.extend(diagnostics)` (`api.py:433`) avant l'équipement ⇒ rouge |
| V7 | Les libellés de slot et leur nom complet (critère 2, reformulé par ÉCR-1) | Pour chaque libellé rendu par `api.py:362-380` et présent dans la table de la page : exiger le libellé **et** son nom complet dans la page ; exiger que `api.py` porte bien la liste (`display_slots`) | **Oui** : retirer un slot de `display_slots` ou de la table ⇒ rouge (patron `LIBELLES_SOURCE`) |
| V8 | Les deux écrans de sauvegarde/export et leurs libellés (critère 3) | `GET /saves` ⇒ `SAV-01`, corps `CHARGEMENT DES SAUVEGARDES LOCALES…`, statut `N OUVRIR \| DEL N \| PURGE OUI` ; écran de résultat ⇒ statut contenant `SAVE [NOM]`, `SAVES`, `DB` et `data-mode="result"` ; ces libellés doivent être cités par la page | **Oui** : changer une ligne de statut ⇒ rouge |
| V9 | `MAX_SAVES = 20` et la clé de stockage (critère 3) | Ancrage **source** : `dofus_stuff/web/static/js/terminal.js:15` porte `MAX_SAVES = 20` et `:14` la clé `dofus-stuff-machine.saves` ; la page cite le **20** et la clé | **Oui** : passer `MAX_SAVES` à 50 ⇒ rouge. ⚠️ C'est un contrôle de **présence de littéral**, pas d'exécution — à dire dans le test |
| V10 | L'export Dofusbook : URL, 10 groupes, `prysma` exclu (critère 3) | `build_dofusbook_url` est publique et pure : construire une URL pour un dict connu, décoder (`base64` + `msgpack`) et exiger `counts`, l'ordre plat, et l'**absence** de `prysma`. **Réutiliser** `tests/test_web.py:713-750` plutôt que le réécrire (D-12) | **Oui** : réordonner `_GROUP_SLOTS` ⇒ rouge (`test_web.py` le prouve déjà) |
| V11 | Le capital `5 * (level - 1)` et les paliers PA/PM (critère 4) | Lire les littéraux dans `recommend.py:24,35,36` (`5 * (level - 1)`, `pa = 6 if level < 40 …`, `pm = 3 if level < 40 …`) **et** exiger que la page cite les valeurs `5`, `40`, `100`, `150` avec les cibles `8/10/11` et `4/5/6` | **Oui** : décaler un seuil ⇒ rouge |
| V12 | Les heuristiques de classe existent et sont nommées (critère 4, ÉCR-3) | Exiger dans `recommend.py` les deux ensembles de classes distance/mêlée, `Portée` (2/4 selon le niveau) et `Invocation` (base 1, cible 3) ; page cohérente | **Oui** : retirer un ensemble ⇒ rouge |
| V13 | « sans exo/parchemins » et « sélection du catalogue » (critère 4) | Lire les littéraux `api.py:316` (`Points inclus ; sans exo/parchemins. Jets moyens sauf réglage avancé.`) et `api.py:434` (`Recherche sur une sélection du catalogue ; optimalité globale non garantie.`) ; exiger ces phrases (normalisées) dans la page | **Oui** : reformuler la phrase rendue ⇒ rouge |
| V14 | `docs/sommaire.md` liste la page et le sommaire reste exhaustif dans les deux sens | Les tests de la phase 1 (déjà en place) suffisent : `test_sommaire_lists_every_document`, `test_h1_matches_sommaire_entry`, `test_pages_have_back_link`, `test_all_relative_links_resolve` | **Oui** : ajouter la page sans sa ligne d'index ⇒ rouge (aucune exception, D-39) |
| V15 | Aucune écriture sous `.data/`, aucun réseau, aucun `main()` | (a) mesure de non-régression : `mtime_ns` + taille + SHA-256 du fichier avant/après la suite ; (b) la suite ne doit jamais pointer `.data/` (contrôle possible : le module n'importe pas `dofus_stuff.database`) | **Oui** : un test qui ouvre `.data/` ⇒ le SHA change (ou l'import est détecté) |

**Vérités non falsifiables par pytest (à assumer, pas à maquiller) :**

- Le **comportement JS** de la sauvegarde (éviction, compteur, statuts) : aucun moteur JS. Le contrôle de V9 est un contrôle de **littéral source**, et il faut le nommer ainsi — il ne prouve pas le comportement, il prouve que la page et le code n'ont pas divergé sur la **constante**.
- Le **libellé de la liste d'index** (H1 ↔ index) est falsifiable, mais **la formulation du H1** ne l'est pas : elle est libre (Claude's Discretion).

### Phase Requirements → Test Map

| Req ID | Comportement | Type | Commande d'exécution | Fichier existant ? |
|--------|--------------|------|----------------------|--------------------|
| SIMP-01 | Trois questions rendues + entrées acceptées/refusées + 3 messages | rendu (Flask `test_client`) | `.venv/Scripts/python.exe -m pytest tests/test_docs_parcours.py -q` | ❌ Wave 0 (nouveau module) — patrons dans `test_recommend.py:68-82` |
| SIMP-02 | Carte de pagination + position des diagnostics + libellés de slot | rendu + injection de session | idem | ❌ Wave 0 — patron dans `test_web.py:522-585` |
| SIMP-03 | Écrans `SAV-01` et `OPT-03` + constantes JS ancrées | rendu + lecture source | idem | ❌ Wave 0 — patron dans `test_web.py` + `test_docs_code_anchor.py:240-255` |
| SIMP-04 | Hypothèses et limites citées avec les littéraux du code | lecture source ancrée | idem | ❌ Wave 0 — patron `LIBELLES_SOURCE` |
| — (critère 5) | Couples numéro ↔ libellé, assertion négative | rendu + comparaison par section | idem | ❌ Wave 0 — **prototype prouvé** (ci-dessus) |
| SOMM-02 / SOMM-03 (phase 1) | Sommaire exhaustif, H1, retour | structure | `.venv/Scripts/python.exe -m pytest tests/test_docs_structure.py -q` | ✅ existant — **doit rester vert** |
| GARD-02 (phase 1) | Chemins du bloc « Source de vérité » existants | structure | `.venv/Scripts/python.exe -m pytest tests/test_docs_code_anchor.py -q` | ✅ existant — vert aussi sur la nouvelle page |

### Sampling Rate

- **Per task commit:** `.venv/Scripts/python.exe -m pytest -q` (2,6 s pour 169 tests : aucun besoin de sous-ensemble)
- **Per wave merge:** idem
- **Phase gate:** suite entière verte (**169 + les nouveaux tests**) avant `/gsd:verify-work`, avec la mesure de non-régression `.data/` (V15) rejouée

### Wave 0 Gaps

- [ ] `tests/test_docs_parcours.py` — couvre SIMP-01, SIMP-02, SIMP-03, SIMP-04 et le critère 5 (patrons : `test_recommend.py`, `test_web.py:522`, `test_docs_code_anchor.py:240`)
- [ ] `docs/parcours-simplifie.md` — la page elle-même (débloque V1-V14 : sans elle, la moitié des contrôles est rouge par construction)
- [ ] `docs/sommaire.md` — une ligne d'index + le libellé de H1 correspondant (V14)
- [ ] **Aucune** installation : `flask`, `pytest`, `ortools`, `msgpack` sont déjà là (M12, § Environment Availability)
- [ ] **Aucune** promotion de helper vers `tests/conftest.py` (M15 : les helpers utiles y sont déjà ; en promouvoir un nouveau créerait un doublon de `_texte_page`)

## Security Domain

`security_enforcement = true`, niveau ASVS 1 (`security_block_on: "high"`) — vérifié dans `.planning/config.json`.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | **no** | Le produit n'a aucune authentification ; le serveur web écoute en local (`docs/installation.md`) |
| V3 Session Management | **no** (pour cette phase) | Le flux utilise `session["recommendation_input"]`, mais la page 3 ne documente pas la session comme une frontière de sécurité ; le cookie et la clé de dev (`DOFUS_SECRET_KEY` avec défaut `stuff-machine-dev-secret`, `web/__init__.py`) appartiennent au produit, pas à cette phase |
| V4 Access Control | **no** | Aucune notion de rôle ou de ressource protégée |
| V5 Input Validation | **yes** | Validation **côté serveur** dans la vue : égalité normalisée pour la classe, liste blanche `ELEMENTS`, `isdigit()` + bornes pour le niveau (`routes.py:955-977`). La page **documente** ces règles ; elle n'en invente aucune. Le `maxlength="40"` est une garde **côté client** — la page ne doit pas la présenter comme une protection serveur |
| V6 Cryptography | **no** | Aucun secret, aucun chiffrement. L'URL Dofusbook est un encodage (base64 de MessagePack), **pas** une protection : ne jamais l'écrire dans la page comme « sécurisé » |

### Known Threat Patterns for {documentation ancrée sur une vue Flask locale}

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Documenter une règle de validation qui n'existe pas (« le préfixe suffit », « les majuscules sont converties ») | Tampering (de la vérité documentaire) | Mesurer chaque entrée (M3) ; contrôle V2/V3 ; D-35 |
| Ouvrir un navigateur pendant la vérification (`webbrowser.open_new_tab`) | Denial of Service (local, interactif) | `patch("dofus_stuff.web.routes.webbrowser.open_new_tab")` — patron `tests/test_web.py:675` |
| Faire écrire le harnais sous `.data/` (ouverture en lecture-écriture de `Database.open()`) | Tampering (données du joueur) | Fixture `catalog` ; jamais `.data/` ; mesure V15 (SHA-256 avant/après) |
| Une sonde qui déclenche une resynchronisation réseau | Information disclosure / hors-ligne | `offline=True` ⇒ `skip_sync=True` ⇒ `ensure_up_to_date` non appelé (M12) ; aucun test ne crée de socket |
| Publier/ouvrir une cible externe depuis la doc | — | Aucun lien externe ajouté ; l'URL Dofusbook est citée comme **chaîne construite**, jamais cliquée |

## Sources

### Primary (HIGH confidence — mesuré dans cette session)

- `.venv/Scripts/python.exe -m pytest -q` → `169 passed in 2.56s` ; `python -V` → `Python 3.14.7`
- `.venv/Scripts/python.exe .gsd-tmp/research-p3/probe_render.py` — corps rendus des trois questions, redirections, gardes d'étape (M1, M2)
- `.venv/Scripts/python.exe .gsd-tmp/research-p3/probe_inputs.py` — matrice d'entrées acceptées/refusées et les trois messages (M3, M4)
- `.venv/Scripts/python.exe .gsd-tmp/research-p3/probe_result.py mini|real` — écran `OPT-03`, carte `PAGE n/t`, position des diagnostics, présence de `data-stuff-payload` sur chaque page (M6)
- `.venv/Scripts/python.exe .gsd-tmp/research-p3/probe_env.py [a|b|c|d|e]` — lecture seule de la base, `mtime`/SHA avant-après, création de la base sur répertoire vide, attributs rendus, déterminisme (M11, M12)
- `.venv/Scripts/python.exe .gsd-tmp/research-p3/probe_assumptions.py` — capital, paliers (balayage 2→200), heuristiques classe par classe, exo/scroll, candidats par slot (M10)
- `.venv/Scripts/python.exe .gsd-tmp/research-p3/probe_determinism.py` — déterminisme de la fixture (M11)
- `.venv/Scripts/python.exe .gsd-tmp/research-p3/probe_render2.py [real]` — entrées du formulaire, écran `SAV-01`, troncature et largeurs, URL Dofusbook (M7, M8, M9)
- `.venv/Scripts/python.exe .gsd-tmp/research-p3/proto_negative.py <page>` (+ `make_pages.py`) — morsure du contrôle du critère 5 (5 artefacts + dérive code)
- `dofus_stuff/web/routes.py`, `dofus_stuff/web/screens.py`, `dofus_stuff/optimize/api.py`, `dofus_stuff/optimize/score.py`, `dofus_stuff/optimize/recommend.py`, `dofus_stuff/optimize/candidates.py`, `dofus_stuff/web/static/js/terminal.js`, `dofus_stuff/web/dofusbook_export.py`, `dofus_stuff/web/__init__.py`, `dofus_stuff/database.py`, `dofus_stuff/model/solver_spec.py`, `tests/conftest.py`, `tests/test_recommend.py`, `tests/test_web.py`, `tests/test_docs_structure.py`, `tests/test_docs_code_anchor.py`, `tests/test_docs_cli.py`, `pyproject.toml`, `docs/sommaire.md`, `docs/cli.md`, `docs/installation.md`, `README.md`, `.claude/CLAUDE.md`, `.planning/config.json`, `.planning/WINDOWS.md`

### Secondary (MEDIUM confidence)

- `.planning/phases/02-.../02-RESEARCH.md`, `02-REVIEW.md`, `02-01-SUMMARY.md`, `.planning/phases/01-.../01-RESEARCH.md` — formes de harnais et leçons déjà payées (WR-01…WR-05, D-12/D-13)
- `.planning/ROADMAP.md` § Phase 3, `.planning/REQUIREMENTS.md` (SIMP-01…04), `.planning/STATE.md` — cadrage

### Tertiary (LOW confidence)

- Aucune source web n'a été consultée : la phase est entièrement locale (produit figé, hors-ligne par défaut). Aucune affirmation de ce document ne provient d'une recherche en ligne ou de la mémoire de modèle.

## Metadata

**Confidence breakdown:**

- **Surface rendue (libellés, entrées, messages, pagination, export)** : **HIGH** — chaque valeur est sortie d'une exécution réelle, et les messages sont cités verbatim.
- **Hypothèses de l'outil (critère 4)** : **HIGH** — capital, paliers (balayage complet), heuristiques (classe par classe), exo/scroll, compatibilité et préfiltrage sont tous adossés à des mesures ou à des littéraux lus.
- **Harnais (critère 5)** : **HIGH** — le patron a été exécuté et sa morsure prouvée sur 5 artefacts + une dérive de code, avec la page non mutée verte.
- **Architecture** : **HIGH** pour le flux et la propriété des couches (lu + rendu) ; **MEDIUM** pour la formulation de ce que la page *doit dire* des écrans du wizard (frontière D-43, non démontrée ici).
- **Pitfalls** : **HIGH** — les deux pièges majeurs (charge utile sur chaque page, collision des numéros 1–4) sont **mesurés**, pas supposés.

**Note de provenance des lectures de source :** les plages de lignes citées (`fichier:ligne`) proviennent de dumps numérotés (`sed -n 'A,Bp' | nl -ba -vA`) et de lectures directes des fichiers réels dans cette session ; les extraits montrés en bloc de code sont **verbatim**, repris du fichier. Aucune valeur de code n'est citée de mémoire, et aucune n'est donnée d'après une recherche textuelle seule : chaque littéral cité est reproduit à côté de sa ligne.

**Research date:** 2026-09-11
**Valid until:** 2026-10-11 (produit figé, aucune dépendance externe : la péremption viendra d'une modification de `dofus_stuff/**`, que le périmètre de ce milestone interdit).


