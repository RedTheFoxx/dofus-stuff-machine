# Phase 3 : Parcours simplifié documenté depuis le rendu réel — Pattern Map

**Mapped:** 2026-09-11
**Padded phase:** 03
**Fichiers analysés:** 3 créés/modifiés (1 page, 1 index, 1 module de test) + 1 candidat **écarté par la mesure** (`tests/conftest.py`)
**Analogs trouvés:** 3 / 3 familles (`docs/`, `tests/ docs`, `tests/ rendu`) — mais **2 contrôles sans analog** (nommés § Gaps)

## Méthode et provenance

Ce document **ne re-mesure rien** : la surface rendue (libellés, entrées acceptées, messages, pagination, export, non-déterminisme) est celle mesurée par `03-RESEARCH.md` (§ M1–M16), et ce document s'y réfère par renvoi (`§ M…`, `§ ÉCR-…`). Ce qui a été **lu** ici, en lecture seule, ce sont les **fichiers analogs** eux-mêmes, pour en extraire la forme exacte à répliquer — chaque extrait porte son `fichier:ligne` réel.

Fichiers lus pour cette cartographie (tous **git-tracked**, vérifié par `git ls-files --`) :

| Fichier | Lignes | Rôle dans cette carte |
|---------|--------|------------------------|
| `docs/installation.md` | 141 | gabarit de page (H1, intro, sections, bloc d'erreur `text`, « Source de vérité », ligne de retour) |
| `docs/cli.md` | 195 | seconde page livrée (frontière de propriété, `console` vs `text`, bloc source) |
| `docs/sommaire.md` | 20 | index (table + parcours conseillé en prose) — **modifié** par la phase |
| `tests/conftest.py` | 262 | **signatures réelles** des helpers à consommer (D-12) |
| `tests/test_docs_structure.py` | 603 | contraintes déjà actives sur toute nouvelle page `docs/` |
| `tests/test_docs_code_anchor.py` | 255 | patron `LIBELLES_SOURCE` (libellé → porteur sur la même ligne) |
| `tests/test_docs_cli.py` | 1060 | `_texte_page`, accumulation des constats, garde d'exécution |
| `tests/test_recommend.py` | 107 | patron du **client de test Flask** sur `/optimize/quick/<step>` |
| `tests/test_web.py` | 758 | patron d'écrans (`/saves`), injection de session, charge utile, Dofusbook |
| `dofus_stuff/web/routes.py` | — | **source de vérité** citée par la page (libellés, messages, `PAGE`, `SAV-01`) |
| `dofus_stuff/optimize/api.py` | — | **source de vérité** du résultat (`Méthode`, `Score`, `Indice`, `display_slots`) |
| `dofus_stuff/optimize/recommend.py` | — | **source de vérité** des hypothèses (capital, paliers, heuristiques) |
| `dofus_stuff/web/static/js/terminal.js` | — | **source de vérité** des sauvegardes (`SAVES_KEY`, `MAX_SAVES`) |
| `dofus_stuff/web/dofusbook_export.py` | — | **source de vérité** de l'export (`DOFUSBOOK_IMPORT_URL`, `_GROUP_SLOTS`) |
| `dofus_stuff/web/templates/screen.html` | 79 | structure HTML sur laquelle les sondes de rendu s'appuient |
| `dofus_stuff/web/screens.py` | — | `COLS = 100`, `BODY_LINES = 18`, `clip` (largeurs et troncature) |

`dofus_stuff/**` est cité en **lecture seule** : la phase ne modifie aucun fichier du produit (périmètre CONTEXT.md `<domain>`), et **aucun** fichier de `.data/` n'a été ouvert.

---

## File Classification

| Fichier créé/modifié | Rôle | Data Flow | Analog le plus proche | Qualité de correspondance |
|----------------------|------|-----------|------------------------|---------------------------|
| `docs/parcours-simplifie.md` (nouveau) | `documentation` (page utilisateur) | `transform` (prose dérivée d'un rendu, contenu statique) | `docs/installation.md` (gabarit) + `docs/cli.md` (frontière de propriété) | **role-match** — exact pour H1/intro/sections/bloc source/retour ; **partiel** pour les blocs d'écran rendu (aucune page n'en contient, voir § Gaps) |
| `docs/sommaire.md` (modifié) | `documentation` (index) | `transform` (table GFM, une ligne) | lui-même, `docs/sommaire.md:15-20` | **exact** (auto-analog : on ajoute une ligne au motif existant) |
| `tests/test_docs_parcours.py` (nouveau) | `test` (module d'ancrage) | **mixte** : `request-response` (rendu Flask) **et** `file-I/O` (lecture source ancrée) | composite : `tests/test_recommend.py:68-82` (rendu) + `tests/test_web.py:553-566` (session) + `tests/test_docs_code_anchor.py:240-255` (ancrage) + `tests/test_docs_cli.py:980-990` (accumulation) | **role-match composite** — chaque sous-patron a un analog exact, aucun module n'existe qui combine les deux flux |
| `tests/conftest.py` | `test` (config/fixtures) | — | lui-même | **aucun changement** — M15 : « aucune promotion nécessaire » ; un helper neuf dupliquerait `_texte_page` (`tests/test_docs_cli.py:233-245`) |

**Note de classification :** le module de test est classé `request-response` **et** `file-I/O` — c'est cette dualité qui interdit de reprendre tel quel la garde d'exécution de `tests/test_docs_cli.py:993` (dont l'allow-list d'imports est `dofus_stuff.cli` seul ; le nouveau module **doit** importer `dofus_stuff.web`, D-32). Voir § Pattern 3.6.

---

## Pattern Assignments

### 1. `docs/parcours-simplifie.md` (documentation, transform)

**Analogs :** `docs/installation.md` (gabarit D-01) et `docs/cli.md` (page voisine, frontière D-37/D-44).

#### 1.1 H1 unique + introduction (le contrat de `problemes_h1`)

`docs/installation.md:1-5` (verbatim) :

```markdown
# Installation

Cette page décrit l'installation de dofus-stuff-machine, du prérequis Python au premier lancement en ligne de commande.

Le pilotage clavier de l'interface, puis son lancement dans le navigateur, sont décrits plus bas dans la même page.
```

`docs/cli.md:1-5` (verbatim) :

```markdown
# CLI

Cette page décrit la ligne de commande de dofus-stuff-machine : les sous-commandes de `fetcher.py`, les options qu'elles acceptent, les valeurs par défaut relevées dans le parseur et un exemple analysable par commande.

Le point d'entrée est `fetcher.py`, à la racine du dépôt : les commandes de cette page s'écrivent depuis cette racine. Le parseur de la ligne de commande ne connaît que les options déclarées dans `dofus_stuff/cli.py` : cette page n'en présente donc aucune qui ne soit définie dans le produit.
```

**Forme à répliquer :** `# <Libellé>` **puis une ligne vide**, puis **un** paragraphe d'introduction en français (une à deux phrases, « Cette page … »), puis **un second** paragraphe qui borne la page (ce qu'elle n'est pas / d'où viennent ses affirmations). L'introduction est la **section de titre `None`** au sens de `tests/conftest.py:198-211` — les règles « chaque section » s'y appliquent aussi (`tests/test_docs_code_anchor.py:199-213` le montre : la boucle `for titre, corps in sections(texte)` traite `titre is None` comme « l'entête de {PAGE}, avant le premier titre de niveau 2 »).

**Contrainte dure :** le H1 doit être **égal au libellé d'index** du sommaire **après normalisation** (accents/casse/HTML), et **unique** — `tests/test_docs_structure.py:337` (`problemes_h1`), testé par `test_h1_matches_sommaire_entry` (`:450-453`). La formulation exacte du H1 est laissée libre (Claude's Discretion, `03-VALIDATION.md` § « Vérités non falsifiables »), **mais elle engage la ligne d'index** : c'est le libellé retenu qui doit apparaître dans `docs/sommaire.md`.

#### 1.2 Sections courtes de niveau 2

`docs/installation.md` : `## Prérequis` (`:7`), `## Installation` (`:13`), `## Vérification` (`:29`), `## Premier lancement` (`:39`), `## Pilotage clavier` (`:53`), `## Erreurs fréquentes` (`:99`), `## Source de vérité` (`:131`).
`docs/cli.md` : `## Options globales` (`:7`), puis **une section par sous-commande** (`## version` `:32`, `## self-test` `:40`, … `## cache` `:180`), `## Source de vérité` (`:188`).

**Forme à répliquer :** sections **courtes**, chacune autonome, titres **en français**, `##` uniquement (le scanner `_sections` de `tests/conftest.py:143,198-211` ne découpe que sur `##`) ; `###` réservé à une sous-partie d'une section (`docs/installation.md:101`, `:119`, `:123`, `:127` ; `docs/cli.md:94`, `:106`, `:117`, `:136`, `:174`).

#### 1.3 Bloc de sortie verbatim (`text`) — l'analog le plus proche d'un « écran »

`docs/installation.md:109-115` (verbatim, **fin de ligne `text` critique**) :

````markdown
Elle se termine avec le code de retour 1 et la sortie d'erreur :

```text
Erreur : Base locale vide et --offline : impossible de synchroniser
```

Le message est levé par la garde hors-ligne `if offline:` de `ensure_up_to_date` dans `dofus_stuff/sync.py`, et `dofus_stuff/cli.py` l'affiche sous la forme `Erreur : <message>`.
````

Deuxième exemple, `docs/cli.md:168-172` (verbatim) :

````markdown
... elles sont incompatibles avec `--offline`, et une telle commande sort avec le code de retour 1 et le message suivant. Ce sont les seules commandes de cette page qui ne s'emploient pas hors-ligne.

```text
Erreur : --offline incompatible avec db sync
```
````

**Forme à répliquer pour les écrans rendus** (critère 1 : `1/3 - Quelle est votre classe ?`, le menu, `AVANCE : personnaliser les réglages`) : un bloc **```text** introduit par une phrase, contenant les **lignes telles que rendues** (§ M2, verbatim mesuré par la recherche). Le choix de la balise suit une règle observable : **```bash** pour une commande à recopier (`docs/installation.md:17,23,31,41,75,105`), **```console** pour un exemple de ligne de commande dans la page CLI (`docs/cli.md:36,44,57,69,82,146,154,184`), **```text** pour une **sortie** ou un **message** (`docs/installation.md:111`, `docs/cli.md:22,28,170`). Un écran du parcours simplifié est une **sortie de l'interface**, pas une commande à recopier ⇒ `text`.

**Interdit par D-37 :** ne **pas** mettre la surface de commandes (options, sous-commandes) dans cette page, ni en `console` ni en tableau — elle appartient à `docs/cli.md` (`## Options globales` `docs/cli.md:7-30`, une section par sous-commande). Le renvoi se fait **en prose**, sans recopie.

#### 1.4 Tableaux GFM (menus rendus, correspondance libellé ↔ slot)

Motif réel le plus proche — `docs/installation.md:57-66` (verbatim) :

```markdown
Les touches actives, quel que soit l'écran :

| Touche | Effet | Libellé affiché |
|--------|-------|-----------------|
| `F3` | quitter l'interface | « Quitter » |
| `F7` | écran ou page précédente | « Precedent » ou « Page prec » |
```

Et `docs/cli.md:11-16` (tableau à trois colonnes avec défauts, tous recopiés du parseur) :

```markdown
| Option | Rôle | Défaut |
|--------|------|--------|
| `--timeout` | délai HTTP en secondes | `15` |
| `--data-dir` | répertoire de la base locale | le dossier `.data/` à la racine du dépôt |
```

**Forme à répliquer :** tableau GFM à en-tête **en français**, libellés rendus **entre accents graves ou entre guillemets français** (`« Precedent »`), et **aucune valeur écrite de mémoire** : chaque cellule chiffrée doit exister dans le code cité (D-42). Pour les deux tables « contenu propre » que la phase doit porter (§ `03-RESEARCH.md` § « Tension DOCS-06 ») : **table du menu des classes** (19 couples, § M2) et **table des éléments** (4 couples, § M3), puis **table libellé technique → nom complet de slot** (§ M7, reformulée par ÉCR-1).

⚠️ **La comparaison des couples se fait par section** (Pitfall 1 de la recherche) : les deux menus partagent les numéros 1–4 ⇒ chaque menu doit vivre dans **sa propre section `##`**, sinon le contrôle du critère 5 rougit sur une page correcte.

#### 1.5 Bloc « Source de vérité » (exigé, non négociable)

`docs/installation.md:131-139` (verbatim) :

```markdown
## Source de vérité

- `pyproject.toml` : dépendances, extra `dev` et configuration de pytest.
- `fetcher.py` : point d'entrée de la ligne de commande.
- `dofus_stuff/cli.py` : parseur et commandes réellement disponibles.
- `dofus_stuff/sync.py` : synchronisation de la base locale et garde du mode hors-ligne.
- `dofus_stuff/web/__main__.py` : options et valeurs par défaut de l'interface web.
- `dofus_stuff/web/routes.py` : écrans et libellés affichés par l'interface web.
- `dofus_stuff/web/static/js/terminal.js` : gestion des touches du clavier.
```

`docs/cli.md:188-193` (verbatim, forme identique) :

```markdown
## Source de vérité

- `fetcher.py` : point d'entrée de la ligne de commande.
- `dofus_stuff/cli.py` : parseur et commandes réellement disponibles ; la fonction `build_parser()` y déclare la surface documentée ici.
```

**Contrat réel appliqué par les tests existants** (`tests/test_docs_code_anchor.py:23-25` puis `:98-112`) :

```python
TITRE_SOURCE = "## Source de vérité"
CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml|js|md|json|sql))`")
```

```python
    bloc = section(texte, TITRE_SOURCE, PAGE)
    assert sorted(set(CHEMIN_CITE.findall(bloc))), (
        f"{PAGE} : aucun chemin de code trouvé dans la section « {TITRE_SOURCE} » ; "
        f"attendu au moins un chemin réel du code ({PAGE})"
    )
    chemins = sorted(set(CHEMIN_CITE.findall(texte)))
    manquants = [chemin for chemin in chemins if not (RACINE_DEPOT / chemin).exists()]
```

⇒ **Double contrainte réelle**, à respecter dès la rédaction : (a) la section doit citer **au moins un chemin** de la forme `` `…\.(py|toml|js|md|json|sql)` `` ; (b) **tout** chemin ainsi écrit **n'importe où dans la page** doit **exister sur disque** — le motif est global (`CHEMIN_CITE.findall(texte)`, `:106`), pas limité au bloc source. `tests/test_docs_code_anchor.py:98-112` s'exécute aujourd'hui sur `installation.md` : il s'appliquera à `parcours-simplifie.md` **dès que le module l'aura paramétré** (voir Pattern 3.5), et la forme du bloc doit donc être identique.

#### 1.6 Ligne de retour au sommaire (dernière ligne)

`docs/installation.md:141` et `docs/cli.md:195`, tous deux **verbatim** :

```markdown
[Retour au sommaire](sommaire.md)
```

Contrôlé par `tests/test_docs_structure.py:383-400` (`problemes_retour_sommaire`) : la cible **résolue** doit être `docs/sommaire.md`. Un lien relatif `(sommaire.md)` suffit, et **aucun lien mort** n'est toléré (D-44 ; `problemes_liens`, `tests/test_docs_structure.py:39`, testé par `test_all_relative_links_resolve` `:151`).

#### 1.7 Ce qu'il faut réutiliser vs ne pas toucher

| À réutiliser | Source |
|--------------|--------|
| H1 unique + intro en deux paragraphes | `docs/installation.md:1-5`, `docs/cli.md:1-5` |
| Sections `##` courtes, `###` pour une sous-partie | `docs/installation.md:99-129` |
| Bloc de sortie verbatim en `text` | `docs/installation.md:109-115`, `docs/cli.md:168-172` |
| Tableaux GFM en français, valeurs adossées au code | `docs/installation.md:57-66`, `docs/cli.md:11-16` |
| Bloc « Source de vérité » + ligne de retour | `docs/installation.md:131-141`, `docs/cli.md:188-195` |
| Libellés d'écran cités **tels quels**, accents compris | `docs/installation.md:61-64` (`« Precedent »`, `« Page prec »`) |

| À ne **pas** toucher / pas recopier | Pourquoi |
|-------------------------------------|----------|
| `docs/cli.md` (contenu) | propriétaire de la surface de commandes (D-37) ; cette phase n'y écrit pas |
| `docs/installation.md` | livrée en phase 1, hors périmètre |
| La liste `## Parcours conseillé` du sommaire (`docs/sommaire.md:5-13`) | elle cite déjà « 2. Parcours simplifié » **en prose, sans lien** : « aucun changement requis » (§ M14) |
| `README.md` | garde son **lien unique** vers le sommaire (D-10, D-29) |
| Les écrans du wizard avancé / de la base locale | frontière des phases 4 et 5 (D-43, D-44) : renvoi **en prose, sans lien** tant que la cible n'existe pas |
| Un moteur de recherche/repli, un bloc « FAQ », un glossaire | phases 6 (hors périmètre) |

---

### 2. `docs/sommaire.md` (documentation/index, transform) — une ligne d'index

**Analog :** le fichier lui-même, `docs/sommaire.md:15-20` (verbatim, **intégralité de la table**) :

```markdown
## Index

| Page | Sujet |
|------|-------|
| [Installation](installation.md) | Installer l'outil, vérifier, lancer CLI et web |
| [CLI](cli.md) | Commandes, options et exemples de fetcher.py |
```

(Le fichier se termine par un `\r\n` après cette dernière ligne — vérifié à l'octet : `| [CLI](cli.md) | … |\r\n`. La nouvelle ligne s'insère **dans la table**, pas après la liste numérotée.)

#### 2.1 Contrat appliqué par les tests de la phase 1 (inchangés, D-39)

`tests/test_docs_structure.py:92-118` (verbatim, extrait) :

```python
    cibles = set(LINK.findall(sommaire.read_text(encoding="utf-8")))
    pages = {
        page.relative_to(docs_dir).as_posix()
        for page in _pages(docs_dir)
        if page.name != "sommaire.md"
    }
```

```python
    for page in sorted(pages - cibles):
        problemes.append(
            f"{page} : page non listee dans docs/sommaire.md ; attendu une ligne d'index "
            f"pointant vers {page} (SOMM-02, D-06)"
        )
```

Et la correspondance libellé ↔ H1, `tests/test_docs_structure.py:309` + `:326-334` :

```python
LIEN_LIBELLE = re.compile(r"\[(?P<libelle>[^\]]*)\]\((?P<cible>[^)\s]+)\)")
```

```python
def pages_listees(docs_dir: Path) -> list[tuple[str, str]]:
    """Couples (libelle d'index, cible) des entrees de docs/sommaire.md, dans l'ordre du fichier (SOMM-02)."""
```

**Conséquence directe :** la ligne à ajouter est `| [<Libellé>](parcours-simplifie.md) | <sujet court en français> |`, où `<Libellé>` **normalisé** (accents/casse/HTML) égale le **H1** de la nouvelle page, et où **aucun autre libellé d'index ne porte le même texte normalisé** (`test_sommaire_index_labels_are_unique`, `tests/test_docs_structure.py:468`). Libellés existants : `Installation`, `CLI`.

#### 2.2 Ce qu'il faut réutiliser vs ne pas toucher

- **Réutiliser :** l'ordre et la forme des deux colonnes (`Page` / `Sujet`), la ponctuation de la table (`|------|-------|`), un `Sujet` court et sans verbe conjugué, sans lien.
- **Ne pas toucher :** l'en-tête `# Sommaire de la documentation` (`:1`) et l'introduction (`:3`) ; la liste `## Parcours conseillé` (`:5-13`), déjà conforme (§ M14) ; le `| [CLI](cli.md) | … |` existant ; la fin de ligne CRLF (§ M13).
- **Gap :** la validation de la phrase `Sujet` est **libre** (aucun test ne la contraint) — ne pas inventer de contrainte, mais ne pas y écrire non plus de valeur volatile.

---

### 3. `tests/test_docs_parcours.py` (test, request-response **et** file-I/O) — module d'ancrage

Nom du module : laissé à la discrétion de Claude (CONTEXT.md, « Claude's Discretion »), à côté de `tests/test_docs_cli.py`. Le nom `tests/test_docs_parcours.py` est celui employé par `03-VALIDATION.md` (Wave 0) et `03-RESEARCH.md` (§ Validation Architecture) : garder ce nom évite de diverger des commandes de vérification déjà écrites.

#### 3.0 Ossature de module (patron commun aux trois modules d'ancrage)

`tests/test_docs_code_anchor.py:1-21` (verbatim, extrait) — en-tête, `from __future__ import annotations`, constantes de module :

```python
"""Ancrage de la documentation utilisateur sur le code réel du produit (critère de succès 4).

Aucune introspection privée d'argparse (D-14), aucune exécution de commande, aucune base
ouverte : les contrôles passent par les parseurs publics et par la lecture des fichiers.
"""

from __future__ import annotations

import io
import re
import shlex
from contextlib import redirect_stderr
from pathlib import Path

from dofus_stuff.cli import build_parser as build_cli_parser
from dofus_stuff.web.__main__ import build_parser

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "installation.md"
```

`tests/test_docs_cli.py:43-51` (verbatim) — mêmes constantes, préfixe `TITRE_` par section :

```python
RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "cli.md"
SOURCE_CLI = "dofus_stuff/cli.py"

TITRE_OPTIONS_GLOBALES = "## Options globales"
TITRE_OPTIMIZE = "## optimize"
TITRE_DB = "## db"
TITRE_CACHE = "## cache"
TITRE_SOURCE = "## Source de vérité"
```

**À répliquer :** module d'ancrage = **docstring de tête** qui dit ce qui est **exclu** (pas d'exécution, pas de base, pas d'introspection privée), `from __future__ import annotations`, `RACINE_DEPOT`, `PAGE = "parcours-simplifie.md"`, puis des constantes **`TITRE_*`** nommant les sections de la page **en français** (elles serviront d'argument à `section(texte, titre, page)` — le titre doit correspondre **exactement** au `##` de la page, `tests/conftest.py:221` fait `titre.strip().lstrip("#").strip()` puis compare la chaîne du `##`). Les **identifiants du code** restent en anglais/sans accent (`RACINE_DEPOT` est la seule exception historique), les commentaires et messages d'échec sont **en français**, sans accents dans le code de test (convention observée dans `tests/test_docs_cli.py` et `tests/test_docs_code_anchor.py` : messages accentués pour `test_docs_code_anchor.py`, non accentués pour `test_docs_cli.py` — **les deux existent**, choisir l'un des deux et s'y tenir).

#### 3.1 Le client de test Flask : rendre, pas lire (D-32, SIMP-01)

**Analog :** `tests/test_recommend.py:68-87` (verbatim, intégral) :

```python
def test_quick_flow_and_advanced(client):
    response = client.post("/optimize/quick/classe", data={"cmd": "Crâ"}, follow_redirects=True)
    assert b"2/3" in response.data
    response = client.post("/optimize/quick/elements", data={"cmd": "terre + air"}, follow_redirects=True)
    assert b"3/3" in response.data
    response = client.post("/optimize/quick/niveau", data={"cmd": "201"}, follow_redirects=True)
    assert b"1 et 200" in response.data
    with patch("dofus_stuff.web.routes._run_optimize_and_redirect", return_value="computed") as run:
        response = client.post("/optimize/quick/niveau", data={"cmd": "123"})
        assert response.data == b"computed"
        spec = run.call_args.args[0].spec
        assert spec.level == 123
        assert spec.balanced_elements == ("Force", "Agilité")
    response = client.post("/optimize/quick/niveau", data={"cmd": "AVANCE"}, follow_redirects=True)
    assert b"RECAPITULATIF" in response.data


def test_quick_deep_link_requires_profile(client):
    response = client.get("/optimize/quick/niveau", follow_redirects=True)
    assert b"1/3" in response.data
```

**Ce que cet analog porte déjà (mesuré en le lisant) :**
- la fixture **`client`** est consommée nue (pas de construction locale, pas de `create_app`) ;
- le scénario complet se rejoue **sur le même client** (session conservée entre les requêtes) ;
- l'étape 3 est testable **sans solveur** par `patch("dofus_stuff.web.routes._run_optimize_and_redirect", return_value="computed")` (`:75`) — patron à réutiliser si un test veut prouver la redirection réussie de l'étape 3 sans catalogue (cf. Pitfall 5) ;
- `AVANCE` mène au **récapitulatif du wizard** (`:81-82` : `b"RECAPITULATIF"`) : **frontière phase 4** ⇒ dans le nouveau module, `AVANCE` s'ancre par le fait qu'il est **rendu** (`routes.py:1003`) et non par une description de l'écran du wizard (D-43).

**Signature réelle de la fixture** (`tests/conftest.py:114-116`) :

```python
@pytest.fixture
def client(app):
    return app.test_client()
```

**Gap vis-à-vis de l'analog :** `tests/test_recommend.py` asserte sur `response.data` brut (`b"2/3" in response.data`). Ce réflexe **ne se transpose pas** à l'écran de résultat : `data-stuff-payload` y contient tout le texte à **chaque** page (§ M6) ⇒ l'assertion serait verte sur la mauvaise page. Le nouveau module doit extraire les **lignes du corps** (Pattern 3.2).

#### 3.2 Extraire les lignes du corps et la ligne de statut (le geste structurant)

**Gap d'analog nommé :** aucun module du dépôt n'extrait les lignes du corps d'un rendu. Le patron a été **prototypé et prouvé par la recherche** (`03-RESEARCH.md` § Architecture Patterns, Pattern 1), et les marqueurs HTML qu'il utilise ont été **vérifiés dans le gabarit réel** :

`dofus_stuff/web/templates/screen.html:31-35` (verbatim) :

```html
        <div class="body" id="body">
          {% for line in body_lines %}
          <div class="row">{{ line }}</div>
          {% endfor %}
        </div>
```

`dofus_stuff/web/templates/screen.html:49` (verbatim) :

```html
        <div class="row status {{ status_kind }}">{% if status %}{{ status }}{% else %}&nbsp;{% endif %}</div>
```

⇒ la découpe `texte.split('id="body">', 1)[1].split('<div class="row status', 1)[0]` puis `re.findall(r'<div class="row">(.*?)</div>', corps, re.S)` (patron de la recherche) est **adossée à du HTML réel** : `id="body"` et `<div class="row status` sont uniques dans la page, et les lignes du corps sont exactement des `<div class="row">…</div>` **sans attribut** (les autres lignes ont `class="row header"`, `row sep meta`, `row blank`, `row fkeys`, `row item-visual-title meta` — elles ne matchent pas `<div class="row">`).

**Exigence de forme (D-11) :** ces deux sondes (`lignes_du_corps`, `statut`) sont des **helpers locaux au module** ; elles ne se promeuvent **pas** dans `tests/conftest.py` (M15). Toute comparaison de libellé passe ensuite par la fixture `normalize` (jamais un `==` strict : le rendu contient `&lt;` et `&#39;`, § M6/Pitfall 2).

**Forme de la sonde d'acceptation** (`03-RESEARCH.md` § Code Examples, verbatim de la recherche) :

```python
def verdict(client, etape: str, valeur: str) -> str:
    r = client.post(f"/optimize/quick/{etape}", data={"cmd": valeur})
    if r.status_code == 302:
        return f"ACCEPTE -> {r.headers['Location']}"
    return f"REFUSE -> {statut(r).split(' — ')[0]!r}"
```

**Rappel mesuré qui décide du design (Pitfall 4) :** un refus n'est **pas** un code d'erreur — `optimize_quick` fait `flash` puis **re-rend le même écran en `200`** (`routes.py:984-985`), et le message est dans la **ligne de statut**, concaténé avec `ENTREE=SUIVANT`/`ENTREE=CALCULER` (`routes.py:146-150`). Sources verbatim des trois messages (`dofus_stuff/web/routes.py`) :

```python
   963	                if chosen is None:
   964	                    raise ValueError("Saisissez le nom ou le numéro de votre classe.")
```
```python
   971	                if not values or any(v not in ELEMENTS for v in values):
   972	                    raise ValueError("Exemple : feu, terre air, ou multi.")
```
```python
   975	                if not cmd.isdigit() or not 1 <= int(cmd) <= 200:
   976	                    raise ValueError("Saisissez un niveau entre 1 et 200.")
```

⇒ l'assertion de refus doit porter sur le **début** de la ligne de statut (`statut(rv).startswith(message)`), jamais sur `response.data` (le message n'est **jamais** dans le corps, Pitfall 4).

#### 3.3 L'écran de résultat sans solveur : injection de session

**Analog :** `tests/test_web.py:553-579` (verbatim, extrait ; le test complet est `test_optimize_result_pagination`, `:522-579`) :

```python
    with client.session_transaction() as sess:
        sess["optimize_result_lines"] = lines

    rv = client.get("/optimize/result")
    assert rv.status_code == 200
    body = rv.data.decode()
    assert 'data-body-total="' in body
    # Plus d'une page
    assert 'data-body-total="1"' not in body or "dofus_5" in body
    assert "data-nav-base=" in body
    assert "/optimize/result" in body
    assert 'data-mode="result"' in body
    assert "data-stuff-payload=" in body
    assert "SAVE" in body
```

et la lecture de `data-body-total` (`tests/test_web.py:569-574`, verbatim) :

```python
    total_attr = None
    for part in body.split("data-body-total=\"")[1:]:
        total_attr = part.split('"', 1)[0]
        break
```

**Ce que l'analog donne, prêt à réutiliser pour SIMP-02 :** le patron **déterministe et instantané** (0 s, § Wave 0 Gaps de la recherche) pour atteindre l'écran de résultat : `sess["optimize_result_lines"] = [...]` (+ `optimize_result_build` si `DB` est posté, `tests/test_web.py:671-674`), puis `client.get("/optimize/result")`. Pour la carte de pagination, la source réelle est `dofus_stuff/web/routes.py:143-150` :

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

⇒ la carte est **dans la ligne de statut**, séparateur exact `" — "` (tiret cadratin entouré d'espaces), et `PAGE {page}/{total}` n'apparaît **que si `total > 1`** (sur un écran à une seule page, aucune carte : ne pas l'exiger).

**Complément « position des diagnostics » (SIMP-02, item V6) :** la rotation correcte est prouvée par `dofus_stuff/optimize/api.py:432-435` (verbatim) :

```python
    if simple:
        lines.extend(diagnostics)
        lines.append("Recherche sur une sélection du catalogue ; optimalité globale non garantie.")
    lines.append(f"Greedy: {result.greedy_score:.1f} | UB0: {result.ub0:.1f}")
```

et par la composition de `diagnostics`, `dofus_stuff/optimize/api.py:327-341` (verbatim, extrait) :

```python
    diagnostics: list[str] = []
    diagnostics.append(
        f"Méthode : {result.method}"
        + (f" ({result.cpsat_status})" if result.cpsat_status else "")
    )
```

```python
    diagnostics.append(
        f"Score : {result.evaluation.score:.1f}  |  "
        f"Indice de recherche : {result.compatibility.percent:.1f}% "
        f"[{result.compatibility.mode}]"
    )
```

⚠️ **`Score : ` et `Indice de recherche : ` sont sur la MÊME ligne rendue** (deux f-strings concaténées, `api.py:337-341`), séparés par `"  |  "` (deux espaces, barre, deux espaces). Une assertion qui cherche `"Score : "` et `"Indice de recherche : "` **sur deux lignes distinctes** serait fausse sur une implémentation correcte.

#### 3.4 Les écrans de sauvegarde/export (SIMP-03)

**Analog écran `SAV-01` :** `tests/test_web.py:107-112` (verbatim, intégral) :

```python
def test_saves_screen(client):
    rv = client.get("/saves")
    assert rv.status_code == 200
    assert b"SAV-01" in rv.data or b"STUFFS SAUVEGARDES" in rv.data
    assert b'data-mode="saves"' in rv.data
    assert b"PURGE OUI" in rv.data
```

et la source réelle `dofus_stuff/web/routes.py:1280-1295` (verbatim, extrait) :

```python
@bp.get("/saves")
@bp.post("/saves")
def saves() -> Any:
    """Liste / consultation des stuffs sauvegardés (hydraté côté navigateur)."""
    return _screen(
        pgm="SAV-01",
        title="** STUFFS SAUVEGARDES **",
        body_lines=["CHARGEMENT DES SAUVEGARDES LOCALES…"],
```

**Analog « ne pas ouvrir de navigateur » :** `tests/test_web.py:675` (verbatim, extrait de `test_optimize_result_db_opens_browser:668-681`) :

```python
    with patch("dofus_stuff.web.routes.webbrowser.open_new_tab") as open_mock:
        rv = client.post("/optimize/result", data={"cmd": "DB"}, follow_redirects=False)
```

⇒ **obligatoire** dès qu'un test poste `cmd=DB` (§ M9, ligne « Piège »). Sans ce patch, le test **ouvre un vrai navigateur**.

**Analog export Dofusbook — à RENVOYER, pas à réécrire** : `tests/test_web.py:638-665` (`test_build_dofusbook_url_encodes_slots`) et `tests/test_web.py:713-757` (`test_build_dofusbook_url_124test_hat_cape_order`, qui asserte l'ordre plat des 10 groupes `counts == [1, 1, 1, 1, 1, 2, 6, 1, 1, 1]`). La recherche est explicite (§ Don't Hand-Roll : « Vérifier l'ordre des 10 groupes Dofusbook — Ne pas construire un nouveau décodage base64/msgpack »), et D-12/D-17 l'interdisent. Sources citées par la page : `dofus_stuff/web/dofusbook_export.py:21` (`DOFUSBOOK_IMPORT_URL`) et `:26-37` (`_GROUP_SLOTS`, **10 groupes**, le commentaire d'origine compris).

**Analog « constante JS ancrée par lecture source » :** c'est le patron `LIBELLES_SOURCE`, voir 3.5 — **avec une divergence de forme mesurée** (voir § Gaps).

#### 3.5 Ancrage libellé → porteur sur la même ligne (SIMP-03/SIMP-04, D-40/D-42)

**Analog :** `tests/test_docs_code_anchor.py:60-74` (verbatim, extrait de la table) :

```python
# Libellés d'écran cités par la page : (libellé, fichier source, jeton porteur, section de la page).
LIBELLES_SOURCE = [
    ("Quitter", "dofus_stuff/web/routes.py", "F3", "## Pilotage clavier"),
    ("Retour", "dofus_stuff/web/routes.py", "ESC", "## Pilotage clavier"),
    ("Precedent", "dofus_stuff/web/routes.py", "f7_label", "## Pilotage clavier"),
    ("Page prec", "dofus_stuff/web/routes.py", "f7_label", "## Pilotage clavier"),
```

et le contrôle lui-même, `tests/test_docs_code_anchor.py:240-255` (verbatim, intégral) :

```python
def test_libelles_cites_sont_produits_par_le_code(docs_dir: Path, section) -> None:
    """Chaque libellé cité par la page est encore produit par la ligne du code qui le porte."""
    texte = (docs_dir / PAGE).read_text(encoding="utf-8")
    for libelle, chemin_source, porteur, section_page in LIBELLES_SOURCE:
        corps = section(texte, section_page, PAGE) if section_page else texte
        perimetre = f"la section « {section_page} »" if section_page else "la page entière"
        assert libelle in corps, (
            f"{PAGE} : libellé « {libelle} » absent de {perimetre} ; attendu ce libellé dans "
            f"{perimetre}, parce que {chemin_source} le produit"
        )
        lignes = (RACINE_DEPOT / chemin_source).read_text(encoding="utf-8").splitlines()
        attendu = f'« {porteur} » et le littéral "{libelle}" sur une même ligne'
        assert any(porteur in ligne and f'"{libelle}"' in ligne for ligne in lignes), (
            f"{PAGE} : libellé « {libelle} » cité par la page n'est plus produit par "
            f"{chemin_source} ; attendu {attendu}"
        )
```

**Ce que l'analog apporte exactement :** une table `(libellé cité, fichier source, porteur, section de la page)`, une lecture de la page **une fois**, puis, par entrée, **deux** constats : (a) le libellé est dans **le périmètre désigné** (section nommée, ou page entière si `None`) ; (b) le littéral `"<libellé>"` (entre **guillemets droits**) et le **porteur** sont sur une **même ligne** du fichier source.

**Table à instancier pour cette phase** (les couples proviennent du patron `LIBELLES_SOURCE` et des sources vérifiées ci-dessous ; la page doit citer chaque libellé **dans la section indiquée**) :

| Libellé cité par la page | Fichier source | Porteur sur la même ligne | Section de la page |
|--------------------------|----------------|----------------------------|---------------------|
| `1/3 - Quelle est votre classe ?` | `dofus_stuff/web/routes.py` (`:988`) | `body +=` | section « question 1 » de la page |
| `2/3 - Quels éléments privilégier ?` | `dofus_stuff/web/routes.py` (`:992`) | `body +=` | idem |
| `3/3 - Quel est votre niveau ? (1 à 200)` | `dofus_stuff/web/routes.py` (`:998`) | `body +=` | idem |
| `AVANCE : personnaliser les réglages` | `dofus_stuff/web/routes.py` (`:1003`) | `body +=` | idem |
| `Saisissez le nom ou le numéro de votre classe.` | `dofus_stuff/web/routes.py` (`:964`) | `ValueError` | section « refus » |
| `Exemple : feu, terre air, ou multi.` | `dofus_stuff/web/routes.py` (`:972`) | `ValueError` | section « refus » |
| `Saisissez un niveau entre 1 et 200.` | `dofus_stuff/web/routes.py` (`:976`) | `ValueError` | section « refus » |
| `PAGE {page}/{total}` | `dofus_stuff/web/routes.py` (`:145`) | `indicators.append` | section « lire le résultat » |
| `ID DETAIL \| SAVE [NOM] \| SAVES \| EDIT \| DB` | `dofus_stuff/web/routes.py` (`:1380`) | `status=` | section « sauvegarder et exporter » |
| `N OUVRIR \| DEL N \| PURGE OUI` | `dofus_stuff/web/routes.py` (`:1293`) | `status=` | section « sauvegarder et exporter » |
| `CHARGEMENT DES SAUVEGARDES LOCALES…` | `dofus_stuff/web/routes.py` (`:1287`) | `body_lines=` | section « sauvegarder et exporter » |
| `dofus-stuff-machine.saves` | `dofus_stuff/web/static/js/terminal.js` (`:14`) | `SAVES_KEY =` | section « sauvegarder et exporter » |
| `MAX_SAVES = 20` | `dofus_stuff/web/static/js/terminal.js` (`:15`) | `MAX_SAVES =` | section « sauvegarder et exporter » |
| `Points inclus ; sans exo/parchemins. Jets moyens sauf réglage avancé.` | `dofus_stuff/optimize/api.py` (`:316`) | `lines.append` | section « ce que l'outil suppose » |
| `Recherche sur une sélection du catalogue ; optimalité globale non garantie.` | `dofus_stuff/optimize/api.py` (`:434`) | `lines.append` | section « ce que l'outil ne fait pas » |
| `Méthode : ` | `dofus_stuff/optimize/api.py` (`:329`) | `f"` / `diagnostics.append` | section « lire le résultat » |
| `Score : ` | `dofus_stuff/optimize/api.py` (`:338`) | `f"` / `diagnostics.append` | section « lire le résultat » |
| `Indice de recherche : ` | `dofus_stuff/optimize/api.py` (`:339`) | `f"` | section « lire le résultat » |
| `DOFUSBOOK_IMPORT_URL` | `dofus_stuff/web/dofusbook_export.py` (`:21`) | `DOFUSBOOK_IMPORT_URL =` | section « sauvegarder et exporter » |
| `5 * (level - 1)` | `dofus_stuff/optimize/recommend.py` (`:24`) | `capital =` | section « ce que l'outil suppose » |
| `pa = 6 if level < 40 else 8 if level < 100 else 10 if level < 150 else 11` | `dofus_stuff/optimize/recommend.py` (`:35`) | `pa =` | section « ce que l'outil suppose » |
| `pm = 3 if level < 40 else 4 if level < 100 else 5 if level < 150 else 6` | `dofus_stuff/optimize/recommend.py` (`:36`) | `pm =` | section « ce que l'outil suppose » |
| `% Dommages distance` | `dofus_stuff/optimize/recommend.py` (`:46`) | `goals[` | section « ce que l'outil suppose » (heuristiques) |
| `% Dommages mêlée` | `dofus_stuff/optimize/recommend.py` (`:48`) | `goals[` | idem |
| `Invocation` | `dofus_stuff/optimize/recommend.py` (`:54`) | `goals[` | idem |
| `Broad playstyle preferences, not a simulation of class spells.` | `dofus_stuff/optimize/recommend.py` (`:44`) | `#` (commentaire) | section « ce que l'outil suppose » |

⚠️ **Cette table est un mode d'emploi, pas du code copiable** : elle est dérivée des lignes **réellement lues**, et l'entrée `MAX_SAVES = 20` **ne peut pas** passer par la garde littérale de `test_docs_code_anchor.py:252` (voir § Gaps 3). De même, les libellés contenant `|` (lignes de statut) obligent à **échapper la barre dans la table Markdown de la page** (`\|`) : le motif `LIBELLES_SOURCE` compare le libellé **tel qu'il doit apparaître dans la page**, donc les deux formes (source Python et page Markdown) diffèrent — le rédacteur doit choisir et le test doit comparer au texte **normalisé** de la page, ou à la forme échappée.

#### 3.6 La garde « aucun accès à `.data/`, ni réseau, ni `main()` » (V15)

**Analog :** `tests/test_docs_cli.py:993-1057` (verbatim, extrait ; en-tête de la garde `:225-230`) :

```python
def test_sans_execution_ni_base_locale() -> None:
    """Le module d'ancrage n'importe du produit que le parseur et n'execute rien (D-15, critere 5).
```

```python
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
```

```python
    hors_parseur = sorted(
        module
        for module in importes
        if (module == "dofus_stuff" or module.startswith("dofus_stuff."))
        and module != IMPORT_PRODUIT_AUTORISE
    )
```

```python
INTERDITS_EXECUTION = ("subprocess", "socket", "sqlite3")

# Seul module du produit que ce module a le droit d'importer : le parseur public (D-14, D-15).
IMPORT_PRODUIT_AUTORISE = "dofus_stuff.cli"
```

**Ce que l'analog apporte :** la propriété est vérifiée **sur le texte de son propre module par `ast`** — jamais par une recherche de chaînes (le module cite lui-même les noms interdits, la recherche textuelle se détecterait elle-même : `tests/test_docs_cli.py:996-998`).

**Divergence obligatoire (M15) :** l'allow-list `IMPORT_PRODUIT_AUTORISE = "dofus_stuff.cli"` est **locale à `test_docs_cli.py`** ; le nouveau module **doit** importer `dofus_stuff.web` (D-32) et ne peut donc pas la reprendre. Si la garde est reprise, son allow-list est **propre au nouveau module** (p. ex. `{"dofus_stuff.web", "dofus_stuff.optimize.recommend", "dofus_stuff.web.dofusbook_export"}`) et **n'élargit jamais** celle de `test_docs_cli.py`. Le prédicat « pas d'import de `dofus_stuff.database` » demandé par `03-VALIDATION.md` (V15(b)) s'écrit dans la même boucle `ast.walk`.

#### 3.7 Accumuler les constats, une seule assertion par test

**Analog :** `tests/test_docs_cli.py:980-990` (verbatim, intégral) :

```python
    # Les trois constats sont accumules et joints a *une seule* assertion : les regles (b) et (c)
    # portent souvent sur la meme ligne, et une assertion par constat rendrait le motif « recopier »
    # inatteignable des que la co-presence manque aussi (mesure : une assertion par constat
    # rapportait cette mutation « non detectee » sur une page pourtant correcte, la premiere
    # assertion levant avant d'atteindre la seconde).
    assert not constats, (
        f"{PAGE} : constats sur la garde de la commande destructrice : "
        + " ; ".join(constats)
        + f" ; attendu chaque mention de la commande destructive citee avec son avertissement sur "
        f"la meme ligne et hors de tout exemple marque (D-22, critere de succes 4b)"
    )
```

**Forme exacte à répliquer :** `constats: list[str] = []` alimenté dans la boucle, puis **une seule** assertion finale `assert not constats, f"{PAGE} : … " + " ; ".join(constats) + f" ; attendu …"`. C'est la forme retenue par la phase 2 après mesure (CONTEXT.md : « une assertion par constat rendait des motifs inatteignables ») ; elle est **obligatoire** pour le contrôle des couples numéro ↔ libellé (19 + 4 constats possibles).

#### 3.8 Ce qu'il faut réutiliser vs ne pas toucher

| À consommer (jamais réécrire) | Signature réelle (`tests/conftest.py`) | Ce qu'elle rend |
|-------------------------------|-----------------------------------------|-----------------|
| `client` | `:114-116` `def client(app)` | `app.test_client()` — la **seule** source du rendu (D-32) |
| `app`, `catalog` | `:78-80`, `:83-111` | app Flask avec `load_catalog=False`, catalogue injecté (`version="9.9.9.9"`, 3 équipements), `TESTING = True`, `data_dir=tmp_path/"data"` |
| `docs_dir` | `:127-130` (`scope="session"`) | `Path(__file__).resolve().parents[1] / "docs"` |
| `normalize` | `:119-124` + `:133-136` | **le helper** `_normalize` (`html.unescape` → NFKD → diacritiques retirés → espaces réduits → `strip().lower()`) — rendu **jamais une valeur normalisée** |
| `lignes_de_code` | `:176-178` + `:231-234` | **le helper** `_lignes_de_code(texte)` : toutes les lignes de tous les blocs, toutes balises |
| `lignes_exemple` | `:181-195` + `:237-246` | **le helper** `_lignes_exemple(texte)` : seules les lignes des blocs balisés `console` (`BALISE_EXEMPLE = "console"`, `:151`) — ⚠️ la fixture rend le **helper**, itérer la fixture elle-même lève `TypeError: 'function' object is not iterable` (contrat écrit en `:241-244`) |
| `sections` | `:198-211` + `:249-252` | `list[(titre_h2 | None, corps)]`, **l'en-tête avant le premier `##` est la section de titre `None`** |
| `section` | `:214-228` + `:255-262` | `_section(texte, titre, page)` → corps d'une section de niveau 2 ; **`page` est obligatoire et sans valeur par défaut** ; lève `AssertionError` nommant la page si la section est absente |

**Snippet exact du contrat `page` obligatoire** (`tests/conftest.py:214-228`, verbatim) :

```python
def _section(texte: str, titre: str, page: str) -> str:
    """Corps d'une section de niveau 2, du titre jusqu'au titre de niveau 2 suivant.

    `page` est obligatoire et sans valeur par defaut (D-13, D-31) : le helper partage ne peut
    plus lire la constante de page du module appelant, et un appel sans page leve `TypeError`
    des l'execution au lieu de perdre silencieusement le nom de la page dans le message.
    """
    attendu = titre.strip().lstrip("#").strip()
    for titre_trouve, corps in _sections(texte):
        if titre_trouve is not None and titre_trouve.strip() == attendu:
            return corps
    raise AssertionError(
        f"{page} : section « {titre} » introuvable ; attendu un titre de niveau 2 "
        f"« ## {attendu} » dans la page ({page})"
    )
```

⇒ **tout** appel dans le nouveau module est de la forme `section(texte, TITRE_X, PAGE)`. Un appel à deux arguments lève `TypeError` **à l'exécution** (c'est voulu, D-13/D-31).

| À ne pas toucher | Pourquoi |
|------------------|----------|
| `tests/conftest.py` | **aucune promotion de helper** (M15) : les helpers utiles y sont déjà ; un helper « lire la page avec message localisant » **dupliquerait** le rôle de `_texte_page` (`tests/test_docs_cli.py:233-245`), donc il **n'y a rien à promouvoir**. Un changement ici est une **découverte à justifier**, pas un défaut |
| `tests/test_docs_structure.py` (dont sa `_section` **privée à 2 arguments**, `:223-230`) | module de la phase 1, à laisser **vert** (V14) ; sa `_section` locale n'est **pas** le helper partagé et **ne s'importe pas** — utiliser la fixture `section` (3 arguments) |
| `tests/test_docs_code_anchor.py` | à laisser vert (V15) ; il cible `PAGE = "installation.md"` (`:19`) — **ne pas** le paramétrer : le nouveau module porte ses propres contrôles |
| `tests/test_docs_cli.py` | à laisser vert ; sa garde d'exécution est **locale** et son allow-list **ne s'élargit pas** |
| `tests/test_web.py`, `tests/test_recommend.py` | analogs à **imiter**, jamais à réécrire ni à étendre pour la doc |
| `dofus_stuff/**` | hors périmètre : aucune modification |

**Lecture d'une page dans le nouveau module — l'analog réel** (le nouveau module n'a **pas** de `_texte_page`, et ne doit pas en promouvoir un) : `tests/test_docs_code_anchor.py:100` / `:106` / `:250` font la lecture inline :

```python
    texte = (docs_dir / PAGE).read_text(encoding="utf-8")
```

⚠️ Le `docs_dir / PAGE` brut lève `FileNotFoundError` si la page manque : `tests/test_docs_cli.py:233-245` existe précisément pour éviter « un `FileNotFoundError` brut (leçon IN-03) ». Le nouveau module doit donc soit **reprendre ce contrôle localement** (message citant la page et le chemin attendu, sans le mettre dans `conftest.py`), soit assumer le `FileNotFoundError` et le documenter. **Décision à porter au plan** — c'est le seul endroit où la forme est ambiguë.

### 4. `tests/conftest.py` (test/config) — **aucune modification attendue**

**Analog :** le fichier lui-même, `tests/conftest.py:139-141` (verbatim, le commentaire qui porte la règle) :

```python
# Scanner de blocs de code et helpers de section : un seul exemplaire, partage par fixtures (D-12).
# Un helper duplique finit par diverger (lecon WR-04) : ces fonctions ne sont donc jamais
# recopiees dans un module de test, elles y sont exposees comme l'est deja la normalisation.
```

**Verdict de la mesure (M15), qui est une contrainte de plan :** « **Aucune** promotion de helper vers `tests/conftest.py` : les helpers utiles y sont déjà (`normalize`, scanner de blocs, `sections`, `ligne_de_code`, `_section(texte, titre, page)`) ; en promouvoir un nouveau dupliquerait `_texte_page`. »

⇒ si le plan envisage d'écrire dans `tests/conftest.py`, c'est un **finding à justifier explicitement** contre M15 (nom du helper, ce qu'il apporterait que `_section`/`normalize`/`_texte_page` n'apportent pas, et pourquoi il ne duplique pas `_texte_page`). Le défaut est **de ne pas y toucher**.

---

## Gaps — là où aucun analog n'existe

Trois contrôles de cette phase n'ont **aucun précédent** dans le dépôt. Un analog étiré serait plus coûteux qu'un trou nommé :

### Gap 1 — Comparer un **numéro de menu rendu** à son **libellé** (critère 5)

**Aucun test existant ne le fait.** Vérifié par recherche : `grep -rn "1\. Cra\|CLASSES\|Ecaflip\|Eliotrope" tests/*.py` ⇒ **zéro résultat**. Les couples ne sont aujourd'hui asservis par **rien** : `dofus_stuff/optimize/recommend.py:5-9` définit `CLASSES` et `dofus_stuff/web/routes.py:989-990` la rend numérotée, mais aucun test ne relie les deux.

**Ce qui existe à la place :** le patron **prouvé** de la recherche — `03-RESEARCH.md` § Code Examples, exécuté sur **5 artefacts + une dérive de code** (vert sur la page non mutée, rouge sur 6 mutations, messages citant page + section + couple attendu + `fichier:ligne`). Le plan doit **reprendre ce patron**, pas chercher un analog.

**Forme du motif à conserver (verbatim de la recherche)** :

```python
COUPLE_RENDU = re.compile(r"(?P<numero>\d{1,2})\.\s+(?P<libelle>[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ' -]*)")
```

```python
def couples_section(texte: str, titre: str, page: str) -> list[tuple[int, str]]:
    """Couples (numéro, libellé) lus DANS la section — jamais sur toute la page."""
    corps = section(texte, titre, page)          # helper partagé de tests/conftest.py (D-12)
```

**Découverte de forme associée :** `dofus_stuff/web/routes.py:987-990` rend le menu des classes **par paquets de 3 sur une même ligne** (`"    ".join(...)`), donc un `match` doit être **itératif sur la ligne** (`finditer`), pas un `match` unique par ligne. Le libellé est **complété à 12 caractères** (`{CLASSES[j]:12}`) et le numéro **aligné sur 2** (`{j + 1:2}`) — les espaces multiples sont donc **normaux** dans le rendu ; la comparaison doit passer par `normalize` (D-11), jamais par une égalité de ligne brute.

⚠️ **Le message d'échec doit rester celui du prototype** (page + section + couple attendu + `routes.py:989`) : c'est ce qui rend le harnais utilisable sans relire le code (D-13, D-42).

### Gap 2 — Prouver une **constante JavaScript** (`MAX_SAVES = 20`, clé de stockage)

Le patron le plus proche est `LIBELLES_SOURCE` (§ 3.5), **mais sa garde littérale ne se transpose pas telle quelle**. `tests/test_docs_code_anchor.py:252` exige **le littéral entre guillemets droits** :

```python
        assert any(porteur in ligne and f'"{libelle}"' in ligne for ligne in lignes), (
```

Or la source réelle (`dofus_stuff/web/static/js/terminal.js:14-15`, verbatim) est :

```javascript
  var SAVES_KEY = "dofus-stuff-machine.saves";
  var MAX_SAVES = 20;
```

- pour `dofus-stuff-machine.saves` : la clé est **entre guillemets droits** ⇒ la garde de l'analog fonctionne **telle quelle** (porteur `SAVES_KEY =`) ;
- pour `MAX_SAVES = 20` : `20` est **nu** ⇒ la garde `f'"{libelle}"' in ligne` serait **toujours fausse**. Il faut un prédicat propre au nouveau module, du type `porteur in ligne and littéral in ligne` avec `porteur = "MAX_SAVES"` et `littéral = "= 20"` (ou la ligne entière), et **le message d'échec doit nommer la nature du contrôle** : `03-VALIDATION.md` (V9) l'impose — « ⚠ contrôle de présence de littéral, pas d'exécution ». Le test doit le **dire** (aucun moteur JS dans l'environnement, C1 ; § M8, Pitfall 9).

**Aucun analog d'ancrage JS n'existe** — vérifié : les ancrages source du dépôt visent des fichiers Python/TOML (`tests/test_docs_code_anchor.py`, `PAGE = "installation.md"`), et `terminal.js` n'y est atteint que de deux façons qui **ne sont pas** des ancrages de littéral :

- **cité comme chaîne** dans les messages d'échec de `tests/test_docs_structure.py:244-246,266-267,271-273` (« source `dofus_stuff/web/static/js/terminal.js` (INST-03, D-09) ») : le fichier est **nommé**, jamais **lu** ;
- **servi comme asset statique** par `tests/test_web.py:426-432` (`js = client.get("/static/js/terminal.js")`, `assert b"F3" in js.data`) : cela prouve que le fichier est servi, pas qu'un littéral y est présent.

⇒ la forme « porteur + littéral sur la même ligne, dans un fichier `.js` » est **nouvelle** dans ce dépôt. Le plan doit l'assumer et **nommer dans le test** que c'est un contrôle de présence de littéral (V9).

### Gap 3 — La « table libellé tronqué → nom complet de slot » du critère 2 (ÉCR-1)

**Il n'y a rien à analoguer, parce qu'il n'y a rien à mesurer** : § M7 / ÉCR-1 — **zéro** ligne rendue ne contient `…` (fixture **et** copie de la base réelle), largeur maximale **exactement 100 = `COLS`** (les lignes sont **enveloppées** avant d'être passées au clip), et les libellés de slot sont **complétés** par `f"  {slot:8s} : "` (jamais coupés). La règle de troncature existe pourtant, `dofus_stuff/web/screens.py:14-20` (verbatim) :

```python
def clip(text: str, width: int = COLS) -> str:
    """Tronque ou pad une ligne à exactement `width` caractères."""
    if len(text) > width:
        if width <= 1:
            return text[:width]
        return text[: width - 1] + "…"
    return text.ljust(width)
```

**Conséquence de plan (recommandation de la recherche, reprise telle quelle) :** reformuler la table en « **libellé technique court → nom complet du slot** » (`ring_a`, `dofus_3`, `prysma`…), adossée à `dofus_stuff/optimize/api.py:362-380` (`display_slots`), **et ne jamais** écrire un test qui exige l'apparition de `…` — il serait rouge sur une implémentation correcte (`CHARGEMENT DES SAUVEGARDES LOCALES…`, `dofus_stuff/web/routes.py:1287`, contient déjà un `…`).

**Analog de forme pour la table elle-même :** `docs/installation.md:59-66` (tableau GFM 3 colonnes) — c'est un analog de **forme Markdown**, pas de contenu.

---

## Shared Patterns — conventions transverses (à appliquer à tous les fichiers de la phase)

### S1. Fins de ligne CRLF, UTF-8 sans BOM (M13, Pitfall 6)

Mesure de la recherche (`§ M13`) : `docs/cli.md` 195/195, `docs/installation.md` 141/141, `docs/sommaire.md` 20/20, `tests/conftest.py` 262/262, `tests/test_docs_cli.py` 1 060/1 060, `tests/test_docs_code_anchor.py` 255/255, `tests/test_docs_structure.py` 603/603, `tests/test_web.py` 758/758 — **100 % `\r\n`**, BOM absent, UTF-8 strict. Contrôle indépendant fait ici sur `docs/sommaire.md` (`od -c` : la dernière ligne se termine par `\r \n`). Le répertoire `.planning/phases/03-…/` est lui aussi **100 % CRLF** (mesuré : `03-CONTEXT.md` 143/143, `03-RESEARCH.md` 1259/1259, `03-VALIDATION.md` 114/114).

⇒ **appliqué à :** `docs/parcours-simplifie.md`, la ligne ajoutée à `docs/sommaire.md`, `tests/test_docs_parcours.py`. **Aucun test ne doit asserter sur les octets de fin de ligne** (D-11 normalise déjà les espaces, donc les fins de ligne) ; la convention est à **respecter à l'écriture**, pas à **vérifier par assertion**.

### S2. Comparaison après normalisation, jamais un `==` strict (D-11)

Source unique : la fixture `normalize` (`tests/conftest.py:119-124`, exposée `:133-136`). Motif d'usage réel : `tests/test_docs_code_anchor.py:191-193` (`normalise = normalize(texte)` puis `option not in normalise`). Le rendu contient `&lt;`, `&#39;` et des accents (§ M6, Pitfall 2) : un `==` strict produit des faux **négatifs**.

### S3. Message d'échec : page + attendu + fichier de code (D-13, D-42)

Trois formes réelles à imiter :

- `tests/test_docs_code_anchor.py:246-249` : nomme la page, le libellé, le périmètre (« la section « ## … » » ou « la page entière ») **et** le fichier qui le produit ;
- `tests/test_docs_code_anchor.py:252-254` : nomme le fichier source **et** la forme attendue (« `« porteur »` et le littéral "libellé" sur une même ligne ») ;
- `tests/test_docs_cli.py:985-989` : page + la liste des constats joints + « attendu … » avec les références de décision (`D-22`) et le critère de succès.

### S4. Accumuler les constats, une seule assertion (voir § 3.7)

Forme de clôture obligatoire pour tout contrôle qui peut produire **plusieurs** constats (couples numéro ↔ libellé : 19 + 4 ; libellés cités : ~25 ; tableaux : 4 lignes de slots).

### S5. Ancrage par API publique, aucune introspection privée (D-14)

Analog : `tests/test_docs_code_anchor.py:2-5` (docstring) + `:94-95` (`build_parser().format_help()` est **public**). Pour cette phase : `create_app(...).test_client()` (fixture `client`), `build_dofusbook_url` (publique et pure), `recommendation_spec`. Les sondes internes (`_result_screen`, `_run_optimize_and_redirect`) ne sont utilisées que **via `patch`** pour **court-circuiter** un effet (patron `tests/test_recommend.py:75`), jamais pour **lire** un état.

### S6. Exécution de référence : `.venv/Scripts/python.exe -m pytest -q` (D-15, Pitfall 7)

Depuis la racine du dépôt. Jamais `main()`, jamais de serveur, jamais de socket, jamais d'écriture sous `.data/`, jamais de resynchronisation (§ M12). La suite passait **169 tests en 2,56 s** avant la phase (§ Validation Architecture) ; le budget du module ajouté est **< 1 s**.

### S7. Langue

Documentation, titres, tableaux et messages de test **en français** ; le code, les chemins et les identifiants techniques **inchangés** (C2 ; les libellés d'écran sont cités **tels quels**, accents compris : `** RECOMMANDATION DE STUFF **`, `AVANCE : personnaliser les réglages`).

---

## Traps — les mesures de `03-RESEARCH.md` qui changent le design

| # | Piège | Source (à citer, ne pas re-mesurer) | Effet sur le plan |
|---|-------|-------------------------------------|--------------------|
| T1 | `data-stuff-payload` porte **tout** le résultat, sur **chaque** page (accents échappés en `\uXXXX`) | § M6 ; Pitfall 2 ; `dofus_stuff/web/templates/screen.html:21` (attribut **à guillemets simples**) ; `tests/test_web.py:605-607` (décodage existant) | **Interdit** : `assert "Score" in response.data`. Obligatoire : extraire les **lignes du corps** (§ 3.2) ou décoder la charge utile explicitement (`html.unescape` puis `json.loads`) |
| T2 | Le nombre de pages et la `Méthode :` sur la **base réelle** sont **non déterministes** (6 puis 7 pages ; `cpsat_feasible+local` puis `greedy`) et coûtent ~9,5 s | § M11 ; Pitfall 3 | Ancrer sur la **fixture** (`client`) ou sur les **lignes injectées en session** ; jamais de total de pages codé en dur, jamais `Méthode : cpsat` en littéral |
| T3 | Les numéros 1–4 existent dans **les deux** menus ⇒ un dictionnaire global rougit sur une page **correcte** (4 constats mesurés) | Pitfall 1 ; § Code Examples (preuve de morsure) | Comparaison **section par section** (`section(texte, titre, page)`) ; chaque menu dans **sa propre section `##`** de la page |
| T4 | « `Méthode`/`Score`/`Indice` **dernière page** » est **faux sur la fixture** (page 2/3) | ÉCR-2 | Asserter la **position en fin de résultat** (après le dernier `Équipement :`, avant `Greedy: `, suivi de la phrase « sélection du catalogue »), **pas** `page == total`. La page dit « en fin de résultat — jusqu'à `PAGE n/n` » |
| T5 | La **troncature n'existe pas** dans ce flux (zéro `…`, largeur max = 100) | ÉCR-1 ; § M7 | Reformuler la table en « libellé technique → nom complet » ; **ne jamais** tester l'apparition de `…` |
| T6 | Les **heuristiques de classe existent** (elles étaient l'hypothèse à réfuter) et **9 des 19 classes n'ont aucun objectif propre** | ÉCR-3 ; § M10 | La page les présente comme des **préférences de style de jeu** (le code le dit lui-même : `recommend.py:44`) et dit qu'elles sont **ajustables après calcul** — jamais comme une simulation de classe |
| T7 | L'écran affiche le mot **« parcho »** (`Détail {primary} — base+parcho: …`) alors que le parcours suppose **zéro parchemin** | ÉCR-4 ; `dofus_stuff/optimize/api.py:429` | Une phrase lève l'ambiguïté (base + parchemins saisis = 0 ici) ; ni contradiction affirmée, ni silence |
| T8 | La **21ᵉ sauvegarde évince la plus ancienne silencieusement** (aucun message « maximum atteint ») | ÉCR-5 ; § M8 (`terminal.js:294-318` **selon la mesure de la recherche** — non relu pour cette carte) | La page dit « les plus anciennes sont remplacées », pas « 20 maximum » tout court |
| T9 | Les **paliers PA/PM** changent exactement en **40 / 100 / 150** ; la **base PA** change en **100** | § M10 ; `dofus_stuff/optimize/recommend.py:35-36` (+ `:38` pour `base=6 + int(level >= 100)`) | Citer `40`, `100`, `150`, les cibles `8/10/11` (PA) et `4/5/6` (PM) — **et** ne pas confondre cible et base |
| T10 | L'étape 3 réussie **exige un catalogue** (`RuntimeError: Catalogue non initialisé` sinon) ; les étapes 1–2 non | § M12 ; Pitfall 5 | Toute assertion qui **franchit** l'étape 3 utilise la fixture `client` ou patche `_run_optimize_and_redirect` |
| T11 | Poster `cmd=DB` **sans** patcher `webbrowser.open_new_tab` **ouvre un navigateur** | § M9 | `patch("dofus_stuff.web.routes.webbrowser.open_new_tab")`, patron `tests/test_web.py:675` |
| T12 | L'ouverture de la base sous `.data/` est en **lecture-écriture** (`CREATE TABLE IF NOT EXISTS`) — le fichier n'est intact que parce que le schéma existe déjà | § M12 ; C3 | **Aucun** test ne pointe `.data/` ; la justification de la fixture est cette mesure, pas une préférence |
| T13 | Le JavaScript (`MAX_SAVES`, `localStorage`, `shift`, statuts JS) **n'est pas exécutable** ici (aucun moteur, C1) | § M8 ; Pitfall 9 | Le contrôle V9 est un contrôle de **littéral source**, et le test comme la page doivent le **nommer** comme tel (Gap 2) |
| T14 | Aucun **lien mort** : un lien vers une page non livrée casse la suite | D-44 ; `tests/test_docs_structure.py:39`, testé `:151` | `docs/wizard-avance.md` et `docs/base-locale.md` se citent **en prose, sans lien**, tant que la phase qui les livre n'a pas écrit son propre lien |
| T15 | `README.md` garde **un seul** lien (vers le sommaire) | D-10, D-29 ; `tests/test_docs_structure.py:190` | Ne pas ajouter de lien direct vers la nouvelle page depuis `README.md` |

---

## Metadata

**Analog search scope :** `docs/*.md` (3 fichiers — tous lus), `tests/*.py` (10 fichiers ; 6 lus, dont 3 en entier), `dofus_stuff/web/{routes.py,screens.py}`, `dofus_stuff/web/templates/screen.html`, `dofus_stuff/web/static/js/terminal.js`, `dofus_stuff/optimize/{api.py,recommend.py}`, `dofus_stuff/web/dofusbook_export.py`, `.planning/phases/03-*/` (contexte et fins de ligne).
**Files scanned :** 16 fichiers du dépôt (tous **git-tracked**, vérifié par `git ls-files --`) — **3 familles d'analogs** trouvées (pages `docs/`, modules d'ancrage documentaire, modules de rendu Flask) ; **2 contrôles sans analog** (Gaps 1 et 2) et **1 critère sans objet mesurable** (Gap 3 / ÉCR-1).
**Non re-mesuré :** toute la surface rendue (libellés, entrées, messages, pagination, export, non-déterminisme) — citée depuis `03-RESEARCH.md` (§ M1–M16, § ÉCR-1…ÉCR-5, § Pitfalls).
**Pattern extraction date :** 2026-09-11


