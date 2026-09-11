# Phase 1: Socle documentaire, installation et harnais vérifiable - Research

**Researched:** 2026-09-11
**Domain:** Documentation produit Markdown vérifiée par `pytest` (ancrage au code, zéro dépendance nouvelle)
**Confidence:** HIGH — chaque affirmation technique de ce document est vérifiée soit par lecture des lignes citées, soit par exécution réelle dans le dépôt avec l'interpréteur épinglé `.venv/Scripts/python.exe`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Gabarit de page
- **D-01:** Gabarit **léger** pour chaque page `docs/` : un `H1` unique, une phrase d'introduction, des sections courtes, un bloc **« Source de vérité »** listant les chemins réels du code (ex. `dofus_stuff/cli.py`, `dofus_stuff/web/routes.py`, `pyproject.toml`), et une ligne de retour vers le sommaire. Pas de front-matter, pas de bloc de métadonnées d'en-tête.
- **D-02:** Les encadrés « erreur fréquente » ne sont ajoutés que là où l'erreur est **réellement rencontrée** (attendu dans `installation.md`), jamais systématiquement sur toutes les pages.
- **D-03:** Le bloc « Source de vérité » crée un contrat vérifiable : chaque chemin `.py` qui y figure doit exister sur disque — c'est le premier ancrage au code que `tests/test_docs_code_anchor.py` vérifie.

#### Parcours & sommaire
- **D-04:** `docs/sommaire.md` est le **point d'entrée unique** : un parcours guidé ordonné (Installation → Parcours simplifié → Wizard avancé → CLI → Base locale → Dépannage → Glossaire) suivi d'un tableau d'index thématique, **sur la même page**. Pas de sommaire secondaire, pas de page annexe.
- **D-05:** Le sommaire **croît par phase** : il ne liste que les pages réellement livrées (donc uniquement `installation.md` en phase 1) et gagne une entrée à chaque phase. La liste épinglée des 8 pages n'arrive qu'en phase 6, quand toutes les cibles existent.
- **D-06:** Conséquence directe : le test d'exhaustivité bidirectionnelle (toute page listée existe / aucune page non listée) reste **vert à tout moment**, sans exception ni tolérance pour cible absente.

#### Détail installation
- **D-07:** `docs/installation.md` suit un **chemin minimal pas-à-pas d'abord** : Python 3.11+, environnement virtuel, `pip install -e ".[dev]"`, vérification, lancement CLI (`python fetcher.py version`) et web (`python -m dofus_stuff.web`, adresse par défaut), puis une courte section « erreurs fréquentes ».
- **D-08:** **Ni `uv` ni aucun autre gestionnaire de paquets ne sera documenté.** `pyproject.toml` déclare `setuptools` + `pip` et l'extra `dev` ; documenter un outil non utilisé serait inventer une procédure.
- **D-09:** Le pilotage clavier de l'interface web (champ de saisie, `F7`, `F8`, `ESC`, `PageUp`, `PageDown`) est décrit **avant** de lancer l'interface, pas après.
- **D-10:** La section « Documentation utilisateur » du `README.md` contient un **lien unique** vers `docs/sommaire.md`. Aucun lien direct vers les pages individuelles : la même information ne vit qu'à un endroit.

#### Tests : ancrage
- **D-11:** Les comparaisons de libellés, de touches et de chemins se font **après normalisation** : minuscules, accents insensibles, espaces et fins de ligne CRLF/LF unifiés, balises HTML retirées.
  — **Reversibility:** costly — Si la normalisation s'avère trop permissive (un test qui passe alors que la doc diverge), la corriger impose de reprendre les helpers de `tests/conftest.py` et de re-valider chaque assertion déjà écrite dans les phases 2 à 6, qui s'appuient dessus.
- **D-12:** Les helpers de test vivent dans le `tests/conftest.py` **existant** (fixtures `docs_dir`, fonction de normalisation testée), pas dans un module d'aide dédié.
- **D-13:** Chaque échec de test doit citer la page concernée, le libellé attendu et le fichier de code où il n'a pas été trouvé — un échec sans ces trois éléments est considéré comme un défaut du harnais.
- **D-14:** Interdits d'introspection acquis du cadrage : pas d'API privée d'`argparse`, pas de lecture d'attributs internes ; l'ancrage passe par le parseur public (`build_parser().parse_args`) et par le client de test Flask.
- **D-15:** Exécution de référence du harnais : `.venv/Scripts/python.exe -m pytest -q`, **sans** exécuter `main()`, **sans** écrire sous `.data/`, **sans** ouvrir de connexion réseau.

### Claude's Discretion
- Nom exact des fixtures et des fonctions de helper dans `tests/conftest.py` (seule contrainte : le comportement de normalisation de D-11 est testé).
- Découpage interne de `tests/test_docs_structure.py` en classes ou en fonctions.
- Formulation exacte du parcours guidé et de l'index dans `docs/sommaire.md` (seule contrainte : ordre de lecture et exhaustivité vérifiables).
- Choix de la ligne de retour au sommaire (libellé et forme du lien relatif), tant qu'un H1 unique et un lien résolu restent vérifiables par test.

### Deferred Ideas (OUT OF SCOPE)
- Page dédiée « lire le résultat » et « sauvegardes / export » → déjà prévu en phase 3 (SIMP-02, SIMP-03) ; noté en v2 (`DOC2-04`) comme pages séparées, hors roadmap actuel.
- Captures d'écran / illustrations du terminal → `DOC2-03`, hors roadmap.
- Génération d'un site statique depuis `docs/` (MkDocs/Sphinx) → `OUT2-01`, explicitement hors périmètre : la recherche recommande le Markdown nu.
- Vérificateur de liens **externes** → `OUT2-02`, hors roadmap ; cette phase ne contrôle que les liens internes.
- Intégration continue exécutant pytest à chaque changement → `OUT2-03`, hors roadmap (aucune plateforme distante autorisée).
- Guide de contribution et documentation d'architecture interne → hors périmètre du milestone (public « Utilisateur + dev », pas « Développeur »).

### Phase boundary (verbatim)
- **Livré :** section « Documentation utilisateur » dans `README.md` pointant vers `docs/sommaire.md` ; `docs/sommaire.md` ; `docs/installation.md` ; `tests/test_docs_structure.py` ; `tests/test_docs_code_anchor.py` (première moitié : chemins des blocs « Source de vérité » existants, options d'entrée web acceptées par le parseur réel).
- **Non livré :** `docs/cli.md` (phase 2), `docs/parcours-simplifie.md` (phase 3), `docs/wizard-avance.md` + résorption de `GUIDE_WIZARD.md` (phase 4), `docs/base-locale.md` (phase 5), `docs/depannage.md` + `docs/glossaire.md` + liste épinglée (phase 6) ; contrôle des renvois obsolètes (phase 4) ; complétude épinglée et test de mutation formel (phase 6).
- **Hors périmètre, sans exception :** toute modification de `dofus_stuff/**`, tout générateur de site statique, toute nouvelle dépendance, toute écriture sous `.data/`, tout réseau, toute publication.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (verbatim de `.planning/REQUIREMENTS.md`) | Research Support |
|----|--------------------------------------------------------|------------------|
| SOMM-01 | Un lecteur trouve le sommaire de la documentation depuis le `README.md` racine — dérivé de DOCS-01, DOCS-02 | « Common Pitfalls » Pitfall 1 et « Références réelles pour `docs/installation.md` » : point d'insertion exact (`README.md:3` → avant `## Base locale Dofus` en `README.md:5`) ; résolution du lien depuis la racine vérifiée par prototype |
| SOMM-02 | Chaque page livrée sous `docs/` est listée dans `docs/sommaire.md`, et réciproquement — dérivé de DOCS-01 | « Pattern 1 » : égalité d'ensembles `cibles_du_sommaire(docs_dir) == {p.name for p in docs_dir.rglob("*.md")} - {"sommaire.md"}` ; les 3 dérives injectées sont détectées et localisées (prototype exécuté) |
| SOMM-03 | Chaque page `docs/` porte un unique titre H1 égal à son libellé d'index et une ligne de retour vers le sommaire — dérivé de DOCS-01 | « Code Examples » et « Open Questions » : H1 unique, comparaison normalisée H1 ↔ libellé d'index, lien de retour dont la **cible** est `sommaire.md` ; tension D-04/D-05 arbitrée en §10 (question 1) |
| INST-01 | Un lecteur peut installer l'outil (Python 3.11+, `pip install -e ".[dev]"`) puis vérifier son installation sans lire le code — dérivé de DOCS-03 | « Références réelles — INST-01 » : valeurs à ancrer (`requires-python = ">=3.11"` en `pyproject.toml:10`, extra `dev` en `pyproject.toml:18-21`) ; **la commande de vérification issue de D-07 échoue sur une installation neuve** → arbitrage mesuré dans « Common Pitfalls » Pitfall 1 |
| INST-02 | Un lecteur peut démarrer l'interface web et sait dans quel mode elle démarre (hors-ligne par défaut) et sur quelle adresse — dérivé de DOCS-03 | « Références réelles — INST-02 » : adresse dérivée du parseur public (`dofus_stuff/web/__main__.py:33-34`) ; hors-ligne par défaut vérifié (`__main__.py:22-26`, `web/__init__.py:44`) ; premier lancement observé sur base vide, `GET /` → 200, sans réseau |
| INST-03 | Un lecteur comprend que l'interface web se pilote au clavier (champ de saisie, F7/F8/ESC/PageUp/PageDown) avant de la lancer — dérivé de DOCS-03 | « Références réelles — INST-03 » : touches réellement actives dans `dofus_stuff/web/static/js/terminal.js:548-600`, libellé `ESC` dans `dofus_stuff/web/routes.py:66-69` ; contrainte d'ordre encodable mécaniquement (« Code Examples ») |
| GARD-01 | La suite pytest échoue si un lien interne de `docs/` ne se résout pas, si le sommaire diverge de l'ensemble des pages, ou si un renvoi obsolète réapparaît — dérivé de DOCS-11 | « Pattern 1 », « Pattern 2 » et « Code Examples » : fonctions d'invariant **pures** paramétrées par `docs_dir` (sinon le test de mutation est inécrivable) ; liens morts, divergence d'index et H1 divergent détectés dès la phase 1 (prototype exécuté) ; le renvoi obsolète reste en phase 4 |
| GARD-02 | La suite pytest échoue si un libellé de flux ou d'étape du wizard cité dans la documentation n'est plus produit par le code — dérivé de DOCS-12 | « Pattern 3 » et « Pattern 4 » : mécanisme retenu = `build_parser().parse_args(<argv complet>)` + contenance dans `format_help()` (les deux vérifiés) ; le même mécanisme servira aux libellés CLI (phase 2) et web (phases 3-5) |

### Success Criteria (verbatim de `.planning/ROADMAP.md` § Phase 1)

1. `README.md` porte une section « Documentation utilisateur » dont la cible `docs/sommaire.md` existe sur disque (le lien est résolu par un test).
2. `docs/sommaire.md` liste exactement les pages `docs/**/*.md` présentes, et chaque page porte un unique H1 égal à son libellé d'index, plus une ligne de retour vers le sommaire (contrôle bidirectionnel).
3. `docs/installation.md` mène de Python 3.11+ au premier lancement CLI **et** web (`pip install -e ".[dev]"`, `.venv/Scripts/python.exe -m pytest -q`, `python -m dofus_stuff.web`, adresse par défaut) et décrit le pilotage clavier (`F7`, `F8`, `ESC`, `PageUp`, `PageDown`, champ de saisie) avant de lancer l'interface.
4. Chaque option d'entrée web citée par la documentation est acceptée par le parseur réel, et chaque chemin `.py` d'un bloc « Source de vérité » existe sur disque (contrôles d'ancrage).
5. Une dérive injectée dans une copie de travail de `docs/` (lien interne mort, page non listée, H1 divergent) fait échouer la suite, qui reste verte sur l'état livré — exécutée par `.venv/Scripts/python.exe -m pytest -q`, sans exécuter `main()`, sans écrire sous `.data/` et sans ouvrir de connexion réseau.
</phase_requirements>

## Summary

La phase 1 n'ajoute **aucune technologie** : elle ajoute un contrat exécutable autour de deux fichiers Markdown. Le produit est figé (`dofus_stuff/**` intouchable), la vérification est `pytest` + bibliothèque standard, et le seul risque réel est celui déjà mesuré par la recherche amont : un harnais **trop permissif** qui laisse passer une doc fausse, ou **trop rigide** qui échoue sur des différences typographiques légitimes (accents, CRLF, entités HTML). Les deux modules de test de cette phase sont la charpente que les phases 2 à 6 vont remplir : leurs invariants doivent donc être des **fonctions pures paramétrées par `docs_dir`**, sinon le test de mutation du critère 5 (et celui de la phase 6) est inécrivable.

Le travail de recherche a produit trois résultats qui changent le plan :

1. **Le mécanisme d'ancrage des options web est vérifié et non ambigu.** `dofus_stuff/web/__main__.py::build_parser()` expose les 8 options (`--data-dir`, `--offline`, `--no-offline`, `--online`, `--timeout`, `--host`, `--port`, `--debug`) dans sa surface **publique** `format_help()`, et `parse_args(<argv complet>)` les accepte. Mais en cas d'argv invalide, `argparse` lève **`SystemExit(2)`**, que `pytest` rapporte comme un `FAILED` accompagné de la trace d'`argparse` — donc **la lecture D-13 impose un `try/except SystemExit` converti en `AssertionError`** citant page + libellé attendu + fichier source.
2. **La vérification d'installation issue de D-07 est fausse sur une installation neuve.** Mesuré : `python fetcher.py --offline version` échoue (`Erreur : Base locale vide et --offline : impossible de synchroniser`, code retour 1, source `dofus_stuff/sync.py:43`) ; et sans `--offline` la CLI est **en ligne par défaut** (`dofus_stuff/cli.py:47-51`) donc `Catalog.load(…)` peut déclencher une resynchronisation Dofusdude, ce que la phase interdit. En revanche `python fetcher.py --offline db status` réussit, **crée** la base si elle est absente et n'ouvre aucune connexion : c'est la commande de premier contact CLI à documenter.
3. **Le test de mutation du critère 5 est démontré exécutable.** Un prototype (module de test jetable, écrit puis supprimé, jamais commité) a détecté les **trois** dérives exigées avec des messages localisants (`installation.md : lien mort vers sommaire.mrd`, `page non listée dans docs/sommaire.md : glossaire.md`, `installation.md : H1 « … » ≠ libellé d'index « … »`), tout en laissant l'état livré vert, via `shutil.copytree(docs_dir, tmp_path / "docs")`.

**Primary recommendation:** implémenter les invariants comme des **fonctions pures** `(docs_dir) -> list[str]` (liste vide = conforme) définies au niveau module de `tests/test_docs_structure.py`, exposées aux tests par les fixtures de `tests/conftest.py` (`docs_dir`, `normalize`), et ancrer les options web par **sondes d'argv complets + `format_help()`**, jamais par introspection privée d'`argparse` (D-14).

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Index unique et exhaustivité bidirectionnelle (`sommaire.md` ↔ `docs/**/*.md`) | Documentation (`docs/`) | Harnais (`tests/`) | La doc porte la vérité éditoriale, le test porte la garantie ; aucun recouvrement possible si le test lit les fichiers réels |
| Gabarit de page (H1 unique, ligne de retour, bloc « Source de vérité ») | Documentation (`docs/`) | Harnais (`tests/`) | Le gabarit est une décision de contenu (D-01), sa conformité est un invariant (SOMM-03, D-03) |
| Point d'entrée lecteur (`README.md` → `docs/sommaire.md`) | Dépôt (racine) | Harnais (`tests/`) | `README.md` est aussi le `readme` du paquet (`pyproject.toml`) : son lien est un contrat de packaging autant que de doc |
| Options d'entrée web documentées | Code produit (`dofus_stuff/web/__main__.py`) | Harnais (`tests/`) | Source unique de vérité = le parseur réel ; la doc le reflète, le test compare les deux |
| Touches du pilotage clavier | Code produit (`dofus_stuff/web/static/js/terminal.js`, `dofus_stuff/web/routes.py`) | Harnais (`tests/`) | Les touches sont définies côté navigateur (`keydown`) et côté gabarit (`fkeys`) : les deux sources doivent être lues, aucune n'est modifiable |
| Preuve d'échec (mutation) | Harnais (`tests/`) | — | Seul le harnais peut prouver qu'il mord ; la doc ne peut pas se tester elle-même |
| Lecture de fichier, encodage, normalisation | Harnais (`tests/conftest.py`) | — | Un seul point de lecture (`encoding="utf-8"`) évite les divergences de plateforme (CRLF observé) |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `pytest` | 9.1.1 (installé, observé via `.venv/Scripts/python.exe -m pytest --version`) | Seule capacité de vérification de la phase | Déjà déclaré dans l'extra `dev` (`pyproject.toml:18-21`, `pytest>=8.0`) et déjà configuré (`pyproject.toml:38-39` : `testpaths = ["tests"]`, `pythonpath = ["."]`) ; aucune installation nouvelle, conforme à GARD-04 |
| Bibliothèque standard Python (`pathlib`, `re`, `unicodedata`, `html`, `shlex`, `tomllib`) | Python 3.14.7 dans `.venv` (plancher déclaré `>=3.11`) | Lecture disque, extraction de liens, normalisation, décodage d'entités HTML, découpage de commandes, lecture de `pyproject.toml` | Couvre 100 % du besoin du harnais ; `tomllib` existe depuis 3.11 (plancher du projet), donc ancrer le plancher documenté sur `pyproject.toml` ne coûte aucune dépendance |
| Markdown « nu » (aucune bibliothèque) | — | Format des pages `docs/` | Décision amont (STACK/SUMMARY) : lisibilité immédiate sur GitHub, aucune chaîne de build, zéro dépendance nouvelle |

**Installation:** aucune. `pip install -e ".[dev]"` est le geste **documenté** dans `docs/installation.md`, pas un geste de cette phase.

**Version verification:** `./.venv/Scripts/python.exe -m pytest --version` → `pytest 9.1.1` ; `./.venv/Scripts/python.exe -c "import sys; print(sys.version)"` → `3.14.7 (main, Aug 7 2026, ...)` ; `./.venv/Scripts/python.exe -c "import flask; print(flask.__version__)"` → `flask 3.1.3` ; `git --version` → `2.55.0.windows.4`. Toutes observées le 2026-09-11.

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `argparse` (stdlib) | — | Surface publique du parseur web (`build_parser()`, `parse_args`, `format_help`) | Pour l'ancrage des options d'entrée web (critère 4) et, en phase 2, des sous-commandes CLI |
| Client de test Flask (`app.test_client()`) | Flask 3.1.3 | Rendu réel des écrans, nécessaire pour ancrer les libellés d'interface | **Pas en phase 1** (aucun libellé d'écran n'est ancré ici) ; les phases 3 à 5 réutilisent la fixture `client` déjà existante (`tests/conftest.py:108-110`) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `re` + `pathlib` pour valider les liens | `markdown`, `mistune`, `linkchecker` | Ajoute une dépendance interdite ; un parseur complet rouvre la question des cibles `#ancre` qu'on refuse par décision, sans gagner de garantie |
| `unicodedata.normalize("NFKD")` + suppression des diacritiques | Comparaison stricte octet à octet | Échoue sur des différences typographiques légitimes (accents de la prose, CRLF) et produit des faux positifs pendant cinq phases (D-11, réversibilité coûteuse) |
| Sondes d'argv complets + `format_help()` | `parser._subparsers._group_actions[...]` | API privée explicitement interdite par D-14 ; aucune garantie de stabilité sur Python 3.14 |
| `shlex.split` sur une ligne d'exemple | `subprocess` exécutant la commande | Exécuter serait destructif (`db clear`) et ouvrirait le réseau ; `shlex` découpe sans exécuter |

## Package Legitimacy Audit

> **Non applicable.** Cette phase n'installe **aucun** paquet : `pytest` est déjà déclaré (`pyproject.toml:18-21`) et déjà présent dans `.venv` (9.1.1 vérifié). Aucune ligne de `docs/installation.md` ne doit recommander un autre gestionnaire de paquets (D-08 : ni `uv`, ni `poetry`, ni `pipx`).

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| (aucun) | — | — | — | — | — | Aucune installation dans cette phase |

**Packages removed due to [SLOP] verdict:** none — aucune détection n'a été tentée, le seam de recherche externe étant indisponible dans cet hôte (voir §Sources) ; aucun verdict n'est inventé.
**Packages flagged as suspicious [SUS]:** none.

## Architecture Patterns

### System Architecture Diagram

```
                       (lecteur, hors dépôt)
                              |  ouvre
                              v
  +--------------+   lien unique   +--------------------+
  |  README.md   | --------------->| docs/sommaire.md   |
  | (racine)     |  docs/sommaire  | parcours + index   |
  +--------------+                 +---------+----------+
        ^                                    | liens relatifs
        | "inverser le flux"                 | (1 seule cible livrée en phase 1)
        |                                    v
        |                          +--------------------+
        |                          | docs/installation  |
        |                          | .md (H1 + gabarit) |
        |                          +---------+----------+
        |                                    | bloc « Source de vérité » + commandes
        |                                    v
        |                    +----------------------------------------+
        |                    |  CODE PRODUIT (FIGÉ, jamais modifié)   |
        |                    |  pyproject.toml        (requires-python)|
        |                    |  web/__main__.py       (parseur web)   |
        |                    |  dofus_stuff/cli.py    (sous-commandes)|
        |                    |  static/js/terminal.js (clavier)       |
        |                    |  web/routes.py         (libellés)      |
        |                    +------------------+---------------------+
        |                                       | lu, jamais exécuté
        |                                       v
        |            +------------------------------------------------------+
        +------------+  HARNAIS pytest (le juge)                           |
     échoue si      |  tests/test_docs_structure.py   (invariants internes) |
     la doc ment <--|  tests/test_docs_code_anchor.py (ancrage, 1re moitié) |
                    |        ^                                             |
                    |        | copie jetable + dérive injectée             |
                    |  tmp_path/docs   (critère 5 : preuve d'échec)        |
                    +------------------------------------------------------+
                       ni main(), ni écriture sous .data/, ni socket
```

Points de décision du flux : « le fichier est-il listé ? » (index), « la cible existe-t-elle ? » (liens), « le H1 est-il identique au libellé d'index ? » (gabarit), « l'option citée est-elle acceptée par le parseur ? » (ancrage), « la dérive injectée est-elle détectée ? » (mutation).

### Recommended Project Structure

```
dofus-stuff-machine/
├── README.md                       # + section « Documentation utilisateur » (lien unique, D-10)
├── docs/
│   ├── sommaire.md                 # H1 = # Documentation dofus-stuff-machine ; parcours + index
│   └── installation.md             # H1 = libellé d'index ; gabarit D-01 ; clavier AVANT lancement (D-09)
└── tests/
    ├── conftest.py                 # + fixture docs_dir, + normalisation testée (D-12)
    ├── test_docs_structure.py      # invariants : liens, index, H1, retour, UTF-8, mutation (critère 5)
    └── test_docs_code_anchor.py    # ancrage : chemins « Source de vérité », options d'entrée web
```

Règles de nommage inchangées et fermes : ASCII minuscule, `kebab-case`, `.md` (`parcours-simplifie.md`, jamais `Parcours-Simplifié.md`) ; le contenu reste intégralement accentué. Un fichier = un thème = une exigence `DOCS` ; aucun sous-dossier sous `docs/` (le contrôle d'exhaustivité est récursif, donc un sous-dossier ajouterait une page à l'index sans bénéfice).

### Pattern 1 : helper pur + fixture mince (condition de testabilité du critère 5)

**What:** les invariants documentaires sont des **fonctions pures** au niveau module, prenant `docs_dir: Path` et renvoyant `list[str]` de problèmes formatés D-13 (liste vide = conforme). Les fixtures de `tests/conftest.py` ne portent que la racine et la normalisation.
**When to use:** dès qu'un invariant doit s'exécuter deux fois — contre l'état livré **et** contre une copie dérivée (`tmp_path`).

```python
# tests/conftest.py (additions prévues, D-12)
from pathlib import Path
import html
import re
import unicodedata

import pytest


def _normalize(text: str) -> str:
    """Normalise un libellé pour comparaison (D-11) : entités HTML, accents, casse, espaces."""
    text = html.unescape(text)                                    # &amp; -> & , &#39; -> '
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().lower()


@pytest.fixture(scope="session")
def docs_dir() -> Path:
    """Racine du dossier docs/ du dépôt, indépendante du répertoire courant."""
    return Path(__file__).resolve().parents[1] / "docs"


@pytest.fixture(scope="session")
def normalize():
    """Expose _normalize aux modules de test sans import inter-modules (robuste en tout import-mode)."""
    return _normalize
```

```python
# tests/test_docs_structure.py (extrait ; même logique que le prototype exécuté)
import re
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)\)")
H1 = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.MULTILINE)


def _pages(docs_dir: Path) -> list[Path]:
    return sorted(docs_dir.rglob("*.md"))


def problemes_liens(docs_dir: Path) -> list[str]:
    """Liens relatifs non résolus ; chaque problème cite la page et la cible."""
    problemes: list[str] = []
    for page in _pages(docs_dir):
        for cible in LINK.findall(page.read_text(encoding="utf-8")):
            if cible.startswith(("http://", "https://", "mailto:")) or cible.startswith("#"):
                continue
            if not (page.parent / cible).resolve().exists():
                problemes.append(f"{page.name} : lien mort vers {cible}")
    return problemes


def test_all_relative_links_resolve(docs_dir: Path) -> None:
    """Chaque lien relatif de docs/ doit se résoudre sur disque."""
    problemes = problemes_liens(docs_dir)
    assert problemes == [], "\n".join(problemes)
```

Observé avec le prototype (avant suppression, aucune trace laissée dans le dépôt) : `clean tree == OK (aucun problème)` ; avec les trois dérives injectées, `['installation.md : lien mort vers sommaire.mrd']`, `['page non listée dans docs/sommaire.md : glossaire.md']`, `["installation.md : H1 « … » ≠ libellé d'index « … »"]`, et `2 passed` pour le module de mutation.

### Pattern 2 : comparaison normalisée, jamais textuelle

**What:** toute comparaison de libellé, de touche ou de chemin passe par la normalisation (D-11) : entités HTML décodées, accents réduits, casse aplatie, espaces (dont `\r\n`) unifiés ; lecture toujours avec `encoding="utf-8"` explicite.
**When to use:** H1 ↔ libellé d'index, libellé d'écran cité par la doc, chemins du bloc « Source de vérité ».
**Preuve d'exécution réelle :** le rendu HTML du menu échappe l'apostrophe — `GET /` renvoie `1. RECHERCHE D&#39;OBJETS` — donc `html.unescape` **avant** comparaison est nécessaire, pas théorique.

### Pattern 3 : ancrage par surface publique

**What:** pour prouver qu'une option est réelle, interroger le **parseur public** : `build_parser().parse_args(<argv complet>)` (ne doit pas lever) puis `build_parser().format_help()` (doit contenir le jeton). Les échecs sont convertis en `AssertionError` lisibles (Pattern 4).
**When to use:** critère 4 (options d'entrée web) ; en phase 2, sous-commandes et exemples CLI.
**Preuve d'exécution réelle :** les 8 options sont présentes dans `format_help()` (`--data-dir`, `--offline`, `--no-offline`, `--online`, `--timeout`, `--host`, `--port`, `--debug` : `True` pour les huit).

### Pattern 4 : `SystemExit` converti en assertion localisante (D-13)

**What:** `argparse` ne lève pas une exception ordinaire mais `SystemExit(2)` ; non intercepté, il produit `FAILED … SystemExit: 2` avec la trace d'`argparse` (observé), donc **aucune** page, libellé ou fichier source — exactement le « défaut du harnais » que D-13 interdit.
**When to use:** chaque sonde d'argv (phase 1 et phases suivantes).

```python
# tests/test_docs_code_anchor.py (extrait)
from dofus_stuff.web.__main__ import build_parser

SONDES_WEB = [
    ["--data-dir", "x"],
    ["--offline"],
    ["--no-offline"],
    ["--online"],
    ["--timeout", "5"],
    ["--host", "127.0.0.1"],
    ["--port", "5000"],
    ["--debug"],
]


def test_documented_entry_options_parse() -> None:
    """Chaque option d'entrée web citée par la doc est acceptée par le parseur réel."""
    parser = build_parser()
    aide = parser.format_help()
    for argv in SONDES_WEB:
        try:
            parser.parse_args(argv)
        except SystemExit:  # argparse sort par SystemExit, jamais par une exception ordinaire
            raise AssertionError(
                "installation.md : option "
                f"« {argv[0]} » refusée par dofus_stuff/web/__main__.py::build_parser()"
            ) from None
        assert argv[0] in aide, (
            "installation.md : option "
            f"« {argv[0]} » absente de la surface publique du parseur "
            "(source : dofus_stuff/web/__main__.py)"
        )
```

### Anti-Patterns to Avoid

- **Asserter sur les octets de fin de ligne** : `README.md`, `fetcher.py`, `tests/conftest.py` sont en CRLF et `dofus_stuff/cli.py` en LF (observé) ; `read_text(encoding="utf-8")` neutralise la différence, une lecture de `read_bytes()` ne le fait pas.
- **Cible de lien contenant `#`** : impose de réimplémenter l'algorithme de slug de GitHub (faux négatifs garantis). Les cibles `#ancre` sont **refusées**, pas résolues.
- **Écrire dans `docs/` pour le test de mutation** : la mutation s'exécute sur `shutil.copytree(docs_dir, tmp_path / "docs")`, jamais sur l'arbre réel.
- **Test dépendant du répertoire courant** : `Path(__file__).resolve().parents[1]`, jamais `Path("docs")`.
- **Fixture portant la logique d'invariant** : rend le test de mutation inécrivable sans duplication.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Résolution d'ancre `#titre` pour valider les liens | Un port de `github-slugger` | Interdire la cible `#…` (décision actée) | Chaque détail (accents, ponctuation, doublons) est une source de faux négatif silencieux |
| Parsing Markdown | Un mini-parseur de blocs et de listes | Deux expressions régulières (`[…](…)`, `^# …`) | Le gabarit est volontairement pauvre (D-01) : seules deux structures sont nécessaires |
| Introspection d'`argparse` | `parser._subparsers._group_actions[…].choices` | `build_parser()`, `parse_args(<argv>)`, `format_help()` | D-14 interdit l'API privée ; mesuré : la surface publique suffit intégralement |
| Découpage de commandes documentées | `subprocess.run(exemple)` | `shlex.split` | Exécuter `db clear` détruirait des données et ouvrirait le réseau |
| Vérification de liens externes | `requests` / `linkchecker` | Laisser les URL en texte, sans test | Hors périmètre (`OUT2-02`) et réseau interdit |
| Normalisation maison par `.lower()` seul | — | `unicodedata` (`NFKD` + combinaison) + `html.unescape` | `.lower()` laisse `é` ≠ `e` et `&#39;` ≠ `'` : deux faux positifs mesurés |
| Rejouer l'encodage de la console Windows | `subprocess` + `chcp` | `read_text(encoding="utf-8")` | Les sorties accentuées de la console varient selon la page de code (observé : `Entr�es` en sortie de `db status`) |

**Key insight:** dans ce domaine, tout ce qui est écrit à la main et qui n'est pas une **fonction pure paramétrée** finit par ne plus pouvoir être testé (mutation, réutilisation en phases 2-6) ; tout ce qui réimplémente une norme externe (slugs, Markdown, HTTP) finit par diverger silencieusement.

## Common Pitfalls

### Pitfall 1 : documenter `python fetcher.py version` comme vérification d'installation

**What goes wrong:** sur une installation neuve (`.data/` absent — `.data/` est ignoré par git), la commande échoue. Mesure exacte : `python fetcher.py --offline version` → `Erreur : Base locale vide et --offline : impossible de synchroniser`, code retour 1, message levé par la garde `if offline:` de `ensure_up_to_date` (`dofus_stuff/sync.py:43`) et affiché par `dofus_stuff/cli.py`. Et **sans** `--offline`, la commande n'atteint pas cette garde : la CLI est en ligne par défaut (`dofus_stuff/cli.py:44-51`, `version` charge le catalogue avec `offline=args.offline` : `dofus_stuff/cli.py:203-212` puis `dofus_stuff/sync.py:50-53`) donc `Catalog.load(…)` peut déclencher `ensure_up_to_date`, c'est-à-dire une resynchronisation Dofusdude que la phase interdit explicitement — la forme sans drapeau n'échoue donc pas comme la page le prétendrait.
**Why it happens:** D-07 a été écrit « chemin minimal » en supposant que `version` est une vérification inerte ; la commande dépend en réalité d'une base peuplée.
**How to avoid:** documenter `python fetcher.py --offline db status` comme premier contact CLI — mesuré : code retour 0, **crée** `dofus.sqlite3` si absent, n'ouvre aucune connexion, affiche `Fichier : …`, `Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0` — et ne citer la commande `version` que sous sa forme hors-ligne `python fetcher.py --offline version` (message d'erreur reproduit tel quel sur base vide, fichier source cité) ; `db sync`, décrit comme réseau en phase 5, est la seule façon d'obtenir une base peuplée.
**Warning signs:** une phrase « lancez `python fetcher.py version` pour vérifier l'installation » dans `docs/installation.md`.

### Pitfall 2 : placer une option globale après la sous-commande

**What goes wrong:** mesuré : `python fetcher.py --data-dir X db status --offline` → `fetcher.py: error: unrecognized arguments: --offline`, code retour 2. `--offline`, `--data-dir`, `--timeout` et `--force-sync` n'existent que sur le parseur **racine**.
**Why it happens:** la forme habituelle `git status --porcelain` (option APRÈS la sous-commande) induit en erreur.
**How to avoid:** tous les exemples de `docs/installation.md` placent les options **avant** la sous-commande ; le contrôle de la phase 2 (CLI-03) généralise la vérification (`--offline optimize …`).
**Warning signs:** un exemple recopié tel quel renvoie un code 2 chez le lecteur.

### Pitfall 3 : laisser `SystemExit` traverser un test d'ancrage

**What goes wrong:** mesuré : un test qui appelle `parser.parse_args(["--host"])` échoue avec `FAILED … - SystemExit: 2` et une trace `argparse`, sans page, sans libellé, sans fichier source (violation de D-13) ; le diagnostic ressemble à un bug du harnais plutôt qu'à une divergence doc/code.
**Why it happens:** `argparse` termine par `sys.exit(2)` ; `pytest` capture le `SystemExit` comme échec du test (le reste de la session continue, vérifié).
**How to avoid:** encapsuler chaque sonde dans `try/except SystemExit` → `raise AssertionError(<message D-13>) from None` (Pattern 4) ; c'est le seul endroit où l'on intercepte une sortie du produit, sans l'exécuter (`parse_args` ne fait que lire les arguments).
**Warning signs:** un `FAILED` dont le corps est une trace `argparse.py` et non une phrase française citant la page.

### Pitfall 4 : sommaire qui annonce des pages non livrées

**What goes wrong:** D-04 demande un parcours guidé ordonné sur 7 thèmes ; D-05/D-06 n'autorisent qu'une seule cible en phase 1. Un parcours écrit en liens Markdown produirait 6 liens morts → contrôle rouge, et la tentation de « tolérer les cibles absentes » détruirait la valeur du contrôle pour les phases 2 à 6.
**Why it happens:** tension réelle entre deux décisions actées (arbitrage en « Open Questions » n° 1).
**How to avoid:** en phase 1, le parcours guidé est en **texte simple numéroté** (sans `[…](…)`) ou ne fait un lien que vers la page livrée ; les liens apparaissent à mesure que les pages sont livrées. `TODO`/`À COMPLÉTER` étant interdits par les conventions de vérifiabilité, le parcours doit contenir de vrais libellés dès maintenant.
**Warning signs:** un `docs/sommaire.md` dont les cibles ne résolvent pas, ou un test assoupli par une liste blanche.

### Pitfall 5 : recopier des valeurs volatiles

**What goes wrong:** la base locale expose un nombre d'entrées, une version de jeu et un `Dernier check` variables ; l'en-tête d'écran contient une horloge (observé au rendu réel : `2026-09-11 00:56:34`). Toute valeur recopiée est périmée au premier `db sync` ou au premier rendu.
**Why it happens:** les valeurs observées sont le matériau naturel d'un exemple.
**How to avoid:** décrire le **format** des sorties (`Fichier :`, `Version jeu :`, `Dernier check : il y a Xh` ou `(aucun)`, `Entrées :`, `Par catégorie :`) sans aucune valeur ; ne jamais citer l'horloge de l'en-tête ; les tests de doc ne lisent **pas** `.data/dofus.sqlite3`.
**Warning signs:** un test de doc qu'il faudrait mettre à jour après une synchronisation.

### Pitfall 6 : présenter une barre de raccourcis fixe

**What goes wrong:** la barre est construite dynamiquement : `keys = list(fkeys or DEFAULT_FKEYS)`, puis remplacée par `F7`/`F8` (avec conservation de `F3`/`ESC`) **seulement** si `total > 1 or f7_url or f8_url` (`dofus_stuff/web/routes.py:137-141`). Le menu principal n'affiche donc que `F3 = Quitter` (`routes.py:206-208`, confirmé au rendu réel), tandis que `F7`, `F8`, `ESC`, `PageUp`, `PageDown` existent bel et bien comme gestionnaires de touches **globaux** (`dofus_stuff/web/static/js/terminal.js:548-600`).
**Why it happens:** « la barre affichée » et « les touches actives » sont deux choses différentes.
**How to avoid:** `docs/installation.md` décrit les **touches actives** et n'affirme jamais que `F7`/`F8` sont visibles partout.
**Warning signs:** une phrase « la barre affiche toujours F7, F8, ESC, Entrée ».

### Pitfall 7 : lire un fichier de doc sans encodage explicite

**What goes wrong:** le dépôt mélange CRLF (`README.md`, `fetcher.py`, `tests/conftest.py`) et LF (`dofus_stuff/cli.py`) ; une lecture dépendant de la locale (cp1252 sous Windows) ou une comparaison d'octets de fin de ligne diverge selon la machine.
**Why it happens:** `Path.read_text()` sans argument utilise l'encodage par défaut de la plateforme.
**How to avoid:** `read_text(encoding="utf-8")` partout ; l'invariant « pas de fichier non UTF-8 » s'implémente en laissant remonter `UnicodeDecodeError` sur des octets cp1252 ; ne jamais asserter sur les fins de ligne.
**Warning signs:** un test vert en local et rouge ailleurs (ou l'inverse).

### Pitfall 8 : toucher `.data/` ou le dépôt pendant les tests

**What goes wrong:** `DEFAULT_DATA_DIR` est **absolu et calculé à l'import** (`dofus_stuff/database.py:13` : racine du paquet + `.data`) et une base réelle existe (`.data/dofus.sqlite3`, 24 989 696 octets, mesuré). Un test qui laisse le défaut s'appliquer écrit dans la base de développement.
**Why it happens:** les défauts du produit sont conçus pour l'utilisateur, pas pour le harnais.
**How to avoid:** aucun chemin de test ne touche `.data/` : la phase 1 n'ouvre ni base ni catalogue ; les fixtures existantes passent déjà `data_dir=tmp_path / "data"` avec `offline=True` et `load_catalog=False` (`tests/conftest.py:78-105`).
**Warning signs:** un horodatage d'`.data/` modifié après un run de tests.

### Pitfall 9 : mutation qui ne prouve rien

**What goes wrong:** un test de mutation qui vérifie seulement « ça a échoué » accepte un harnais cassé pour une mauvaise raison (import cassé, mauvais chemin). À l'inverse, une mutation appliquée à l'arbre réel laisse le dépôt corrompu si le test échoue avant restauration.
**Why it happens:** la valeur d'une mutation est locale (quel invariant, quelle page), pas globale.
**How to avoid:** copier via `shutil.copytree(docs_dir, tmp_path / "docs")` (vérifié : la copie fonctionne et le nettoyage est automatique), asserter que la liste de problèmes est **non vide** et contient la cible injectée, et vérifier **dans le même test** que l'arbre livré reste sain.
**Warning signs:** un test de mutation qui passe même quand la fonction d'invariant renvoie toujours `[]`.

## Code Examples

### Vérification d'invariants et injection de dérive (prototype exécuté, puis supprimé)

```python
# Source : prototype exécuté avec ./.venv/Scripts/python.exe (fichier jetable, supprimé, jamais commité)
import re
from pathlib import Path

ENTRY = re.compile(r"\[(?P<label>[^\]]+)\]\((?P<target>[^)\s]+)\)")


def problemes_index(docs_dir: Path) -> list[str]:
    """Exhaustivité bidirectionnelle sommaire <-> docs/**/*.md (SOMM-02 / critère 2)."""
    problemes: list[str] = []
    sommaire = docs_dir / "sommaire.md"
    listees = {m.group("target") for m in ENTRY.finditer(sommaire.read_text(encoding="utf-8"))}
    presentes = {p.name for p in docs_dir.rglob("*.md")} - {"sommaire.md"}
    for absente in sorted(listees - presentes):
        problemes.append(f"docs/sommaire.md : cible listée absente sur disque : {absente}")
    for orpheline in sorted(presentes - listees):
        problemes.append(f"{orpheline} : page non listée dans docs/sommaire.md")
    return problemes


def test_mutation_detecte_les_trois_derives(tmp_path: Path, docs_dir: Path) -> None:
    """Une dérive injectée dans une copie de docs/ fait échouer les invariants (critère 5)."""
    import shutil

    copie = tmp_path / "docs"
    shutil.copytree(docs_dir, copie)
    assert problemes_liens(docs_dir) == []          # l'état livré reste sain
    page = copie / "installation.md"
    page.write_text(
        page.read_text(encoding="utf-8").replace("(sommaire.md)", "(sommaire.mrd)"),
        encoding="utf-8",
    )
    problemes = problemes_liens(copie)
    assert problemes, "aucune dérive détectée : le harnais ne mord pas"
    assert "sommaire.mrd" in problemes[0]
```

### Contrôle d'ordre « clavier avant lancement » (D-09 / critère 3)

```python
# Source : dérivé des décisions de phase — à écrire dans l'un des deux modules
TOUCHES = ["F3", "F7", "F8", "ESC", "PageUp", "PageDown"]
LANCEMENT_WEB = "python -m dofus_stuff.web"


def test_pilotage_clavier_avant_lancement(docs_dir: Path) -> None:
    """Les touches sont décrites avant la commande de lancement web (D-09)."""
    texte = (docs_dir / "installation.md").read_text(encoding="utf-8")
    position_lancement = texte.find(LANCEMENT_WEB)
    assert position_lancement != -1, (
        "installation.md : commande de lancement « python -m dofus_stuff.web » absente "
        "(source : dofus_stuff/web/__main__.py)"
    )
    for touche in TOUCHES:
        position = texte.find(touche)
        assert position != -1, (
            f"installation.md : touche « {touche} » non documentée "
            "(source : dofus_stuff/web/static/js/terminal.js)"
        )
        assert position < position_lancement, (
            f"installation.md : la touche « {touche} » doit être décrite AVANT le lancement web "
            "(source : dofus_stuff/web/static/js/terminal.js)"
        )
```

### Adresse par défaut dérivée du parseur (critère 3, « adresse par défaut »)

```python
# Source : dofus_stuff/web/__main__.py:33-34 (défauts vérifiés : 127.0.0.1 / 5000)
from dofus_stuff.web.__main__ import build_parser


def test_adresse_par_defaut_documentee(docs_dir: Path) -> None:
    """L'adresse citée par la doc est celle que le parseur réel applique par défaut."""
    args = build_parser().parse_args([])
    attendu = f"http://{args.host}:{args.port}"
    texte = (docs_dir / "installation.md").read_text(encoding="utf-8")
    assert attendu in texte, (
        f"installation.md : adresse par défaut « {attendu} » absente "
        "(source : dofus_stuff/web/__main__.py)"
    )
```

### Premier lancement web sur base vide (observation réelle, aucune connexion)

Sortie observée de `GET /` sur un `data_dir` neuf avec `offline=True` (défaut du produit) : code `200`, en-tête `** STUFF-MACHINE - MENU PRINCIPAL **`, corps `1. RECHERCHE D&#39;OBJETS … 4. OPTIMISATION DE STUFF … 5. SYSTEME`, barre `F3 = Quitter`, `catalog.version = None`, et création de `dofus.sqlite3` dans le `data_dir` demandé — `.data/` non modifié (horodatage inchangé).

## Références réelles pour `docs/installation.md` (INST-01, INST-02, INST-03)

### INST-01 — installation et vérification

| Affirmation de la page | Valeur réelle (source vérifiée) | Ancrage possible |
|------------------------|--------------------------------|------------------|
| Python 3.11+ | `pyproject.toml:10` : `requires-python = ">=3.11"` | Lire `pyproject.toml` avec `tomllib` et comparer au plancher cité par la doc |
| Extra `dev` | `pyproject.toml:18-21` : `dev = ["pytest>=8.0"]` | Le nom `dev` et la commande `pip install -e ".[dev]"` doivent apparaître tels quels |
| Vérification | `.venv/Scripts/python.exe -m pytest -q` (critère 3) ; re-mesuré le 2026-09-11 pendant cette recherche : `136 passed in 1.61s` | Le compteur ne doit **jamais** être cité par la doc : il change à chaque phase |
| Premier contact CLI | `python fetcher.py --offline db status` (mesuré : code 0, base créée, actes de sortie `Fichier : …`, `Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0`) | Découper avec `shlex` et valider par `dofus_stuff.cli.build_parser().parse_args` |
| Piège à documenter | `python fetcher.py --offline version` sans base échoue : `Base locale vide et --offline : impossible de synchroniser`, levé par la garde `if offline:` de `ensure_up_to_date` (`dofus_stuff/sync.py:43`), affiché par `dofus_stuff/cli.py` sous la forme `Erreur : <message>` (code retour 1). La même commande **sans** `--offline` n'atteint pas cette garde et peut contacter l'API (CLI en ligne par défaut, `dofus_stuff/cli.py:47-51`) | Bloc « erreur fréquente » (D-02) — c'est l'erreur réellement rencontrée, reproduite par la forme hors-ligne seulement ; le plan 01-04 exige `--offline` sur chaque commande `fetcher.py` des blocs de code de la page |

Le nom de l'interpréteur `.venv/Scripts/python.exe` est la forme **observée sur ce poste Windows** et celle citée par le critère 3 ; une mention POSIX (`.venv/bin/python`) reste optionnelle et ne doit pas remplacer la forme vérifiable.

### INST-02 — lancement web, mode, adresse

- Adresse par défaut : `--host` `127.0.0.1`, `--port` `5000` (`dofus_stuff/web/__main__.py:33-34`) → `http://127.0.0.1:5000`.
- Hors-ligne par défaut : `--offline` avec `default=True` et `--no-offline` via `BooleanOptionalAction` (`dofus_stuff/web/__main__.py:22-26`) ; `DOFUS_OFFLINE` a pour défaut `True` (`dofus_stuff/web/__init__.py:44`).
- Premier lancement sans base : observé `200` sur `GET /`, `catalog.version = None`, base SQLite créée dans le `data_dir`, aucun contact API (`skip_sync` forcé quand `offline` est vrai : `dofus_stuff/web/__init__.py:109-119`).
- Variables d'environnement : `DOFUS_DATA_DIR`, `DOFUS_OFFLINE`, `DOFUS_TIMEOUT`, `DOFUS_SECRET_KEY` existent dans le code. La doc peut **nommer** ces variables, jamais recopier leur valeur — en particulier `DOFUS_SECRET_KEY` a un défaut de développement (`dofus_stuff/web/__init__.py:40`, `"stuff-machine-dev-secret"`) qui ne doit pas apparaître dans la documentation.
- `--debug` active le serveur Flask de débogage : la page ne doit pas le recommander dans le chemin minimal (D-07), tout au plus le signaler comme réservé au développement.

### INST-03 — pilotage clavier réel

| Touche citée par le critère 3 | Réalité du code | Remarque de rédaction |
|-------------------------------|-----------------|------------------------|
| `F7` | `terminal.js:567-571` (`navigateF7()`) ; libellés `Precedent` / `Page prec` (`routes.py:137-141`) | Touche globale, barre visible seulement si pagination ou étapes |
| `F8` | `terminal.js:573-577` (`navigateF8()`) ; libellés `Suivant` / `Page suiv` | idem |
| `ESC` | libellé produit : `DEFAULT_FKEYS` contient `("ESC", "Retour")` (`routes.py:66-69`) ; événement : `e.key === "Escape"` (`terminal.js:558-561`) | Citer le libellé `ESC` et mentionner `Escape` comme nom d'événement |
| `PageUp` | `terminal.js:579-587` | Pagination de la page précédente |
| `PageDown` | `terminal.js:589-593` | Pagination de la page suivante |
| champ de saisie | `terminal.js:595-597` : `Enter` n'est pas intercepté quand le champ a le focus ; `terminal.js:599-603` : l'espace n'est bloqué que hors du champ | Expliquer que l'on tape dans le champ et que l'on valide par `Entrée` |
| `F3` (non exigée) | `terminal.js:551-555` (quitter) ; **seule** touche visible sur le menu (`routes.py:206-208`) | Recommandé : documenter la sortie de l'interface |

Contrainte d'ordre (D-09) : la section clavier précède la commande de lancement web ; encodable mécaniquement par comparaison de positions (`texte.find(touche) < texte.find("python -m dofus_stuff.web")`, code de démonstration ci-dessus). Attention à ne pas comparer la première occurrence de `F7` si la page cite `F7` dans un exemple de barre avant la section clavier : le contrôle doit être basé sur la section, pas sur la première lettre trouvée — prévoir un repère de section (titre `## … clavier …`) pour être robuste.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Doc écrite puis relue à la main | Doc comme **contrat exécutable** (tests rouges quand la doc dérive) | Décisions du milestone (`workflow.verifier: true`, `human_verify_mode: end-of-phase`, vérification par pytest) | Les 136 tests actuels ne lisent aucun fichier de documentation (mesuré) : la phase 1 comble ce trou |
| Générateur de site (MkDocs/Sphinx) pour la structure | Markdown nu + `docs/sommaire.md` + tests de structure | Décision amont (`OUT2-01` hors périmètre) | Structure plus simple à vérifier qu'à générer |
| `F12` comme touche de sortie | `ESC` (`Escape`) pour revenir, `F7`/`F8` pour naviguer, `F3` pour quitter | Historique du dépôt (`b3aa6f2`, `7e78b00`) | Toute doc citant `F12` est obsolète — contrôle des renvois obsolètes en phase 4 |
| Menu à quatre entrées | **Cinq** entrées (`1. RECHERCHE D'OBJETS` … `5. SYSTEME`) | `ab1eb38` (menu modifié sans mise à jour documentaire) | Les documents qui annoncent « quatre » ou `3. OPTIMISATION DE STUFF` sont faux ; `README.md` et `GUIDE_WIZARD.md` sont concernés (phases 1 et 4) |

**Deprecated/outdated :**
- `GUIDE_WIZARD.md` : périmé depuis `1d475f9` ; la phase 1 ne fait que rediriger `README.md` (ligne 59, `**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)`), la résorption complète reste en phase 4.
- Toute mention de `F12` : remplacée par `ESC` (`b3aa6f2`).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Le lecteur ouvre la doc depuis GitHub ou un éditeur de texte : un fichier non listé est invisible plutôt que nuisible | Pattern 1, Pitfall 4 | Faible : le contrôle d'exhaustivité protège dans tous les cas |
| A2 | `Ctrl+C` arrête le serveur Flask de développement (comportement du serveur, non du produit) | Références INST-02 | Faible : une phrase à retirer si le planner préfère ne rien dire de l'arrêt |
| A3 | Un parcours guidé rédigé en texte simple satisfait D-04 (ordre de lecture vérifiable sans liens) | Pitfall 4, Open Questions 1 | Moyen : sinon il faut soit livrer les 7 pages, soit tolérer des liens morts — ce que D-06 refuse |
| A4 | `.venv/Scripts/python.exe` est la forme de référence à documenter (poste Windows observé, citée par le critère 3) | Références INST-01 | Faible : une mention POSIX reste possible en complément |
| A5 | Le seuil minimal de la suite après cette phase est `136 + N` tests (compteur réel non cité par la doc) | Validation Architecture | Faible, mais tout compteur cité dans un rapport doit être re-mesuré avant publication |

**If this table is empty:** elle ne l'est pas — A3 a été confirmée explicitement par le planner (voir Open Question 1, RESOLVED ci-dessous), ce qui fixe le contenu de `docs/sommaire.md`.

## Open Questions (RESOLVED)

**Statut : les cinq questions sont RESOLVED par le planner de la phase 1.** Chaque resolution est
reportee inline ci-dessous, sous la forme `**Resolution:**` ; les plans 01-01 a 01-04 appliquent
ces resolutions telles quelles, et le plan 01-04 en controle une partie executable.

1. **Parcours guidé de `docs/sommaire.md` : liens ou texte ?**
   - What we know: D-04 impose un parcours ordonné sur 7 thèmes ; D-05/D-06 n'autorisent qu'une cible livrée en phase 1 ; `test_sommaire_links_resolve` doit rester vert sans liste blanche.
   - What's unclear: l'ordre de lecture peut-il s'exprimer sans lien (texte numéroté), ou faut-il un contrôle d'ordre tolérant sur la forme ?
   - Recommendation: **parcours en texte simple numéroté** (Installation → Parcours simplifié → Wizard avancé → CLI → Base locale → Dépannage → Glossaire), chaque thème devenant un lien dans la phase qui le livre ; l'index thématique contient alors une seule ligne (`installation.md`). Le contrôle bidirectionnel restant une égalité d'ensembles, la duplication d'une même cible (parcours + index) est sans effet.
   - **Resolution:** adoptée telle quelle. `docs/sommaire.md` est écrit par le plan 01-01 avec le parcours guidé en texte simple numéroté et un index thématique à une seule entrée (`installation.md`) ; aucun lien mort n'est introduit pour un thème non livré (D-06), et le contrôle d'égalité d'ensembles du plan 01-01 reste la garde opposable. La demande de confirmation explicite de l'hypothèse A3 est satisfaite par cette adoption.
2. **Quelle commande de vérification dans `docs/installation.md` ?**
   - What we know: mesuré — `--offline version` échoue sans base, `version` sans `--offline` peut déclencher une resynchronisation, `--offline db status` réussit et crée la base.
   - What's unclear: D-07 cite `python fetcher.py version`, alors que le critère 3 (opposable) n'exige que `pip install -e ".[dev]"`, la commande `pytest`, le lancement web et l'adresse par défaut.
   - Recommendation: vérification = `.venv/Scripts/python.exe -m pytest -q` (aucun réseau, aucune base, tests sur `tmp_path`), puis premier contact CLI = `python fetcher.py --offline db status`, et `version` présenté comme nécessitant une base peuplée. À acter dans le plan 01-02.
   - **Resolution:** adoptée, et précisée par la mesure : la forme `python fetcher.py version` **sans** `--offline` n'est pas seulement « nécessitant une base peuplée », elle atteint l'API Dofusdude sur une base vide (`version` charge le catalogue avec `offline=args.offline`, `dofus_stuff/cli.py:203-212` → `Catalog.load`, puis `fetch_version()` : `dofus_stuff/sync.py:50-53`). La page ne cite donc la commande `version` que sous la forme hors-ligne `python fetcher.py --offline version`, qui atteint réellement la garde `if offline:` et lève le message cité ; le plan 01-02 écrit cette forme et attribue le message à `dofus_stuff/sync.py`, le plan 01-04 exige le drapeau hors-ligne sur chaque commande `fetcher.py` des blocs de code de la page. Le message n'est jamais présenté comme le résultat de la forme sans drapeau.
3. **Faut-il ancrer aussi la commande CLI citée par `installation.md` ?**
   - What we know: le critère 4 n'exige l'ancrage que des options d'**entrée web** ; la phase 2 (CLI-01/CLI-03) couvrira `docs/cli.md`.
   - What's unclear: coût/bénéfice d'un contrôle minimal supplémentaire sur les exemples CLI de la page d'installation.
   - Recommendation: oui, version minimale — toute commande `fetcher.py …` de `docs/installation.md` doit se découper (`shlex.split`) et passer `dofus_stuff.cli.build_parser().parse_args`, sinon la page enseigne une commande fausse ; le contrôle exhaustif reste en phase 2.
   - **Resolution:** adoptée et renforcée en deux exigences dans le plan 01-04 : (i) chaque commande `fetcher.py` des blocs de code se découpe et passe le parseur réel (un `SystemExit` devient une assertion localisante) ; (ii) elle porte le drapeau hors-ligne avant la sous-commande, ce qui ferme la porte à une commande documentée qui atteindrait l'API. L'exemple d'ordre fautif de la page est décrit en prose, hors bloc de code, pour que l'exigence (i) reste sans exception.
4. **`ESC` ou `Escape` comme jeton ancré ?**
   - What we know: le code produit le libellé `ESC` (`routes.py:66-69`) et le nom d'événement `Escape` (`terminal.js:558`).
   - What's unclear: lequel doit être vérifié en priorité.
   - Recommendation: ancrer `ESC` (libellé produit par le code, forme du critère 3) et mentionner `Escape` dans la même ligne ; le test exige `ESC`, l'autre forme restant informative.
   - **Resolution:** adoptée. La page cite le libellé `ESC` et mentionne `Escape` comme nom d'événement (plan 01-02) ; le plan 01-04 va plus loin pour GARD-02 et ancre aussi les autres libellés produits que la page cite — `Quitter`, `Retour`, `Precedent`, `Page prec`, `Suivant`, `Page suiv` sur `dofus_stuff/web/routes.py` — ainsi que le message d'erreur hors-ligne sur `dofus_stuff/sync.py`.
5. **`F3` doit-il entrer dans la liste obligatoire du test ?**
   - What we know: `terminal.js:551-555` traite `F3` ; `F3 = Quitter` est la seule touche visible sur le menu (`routes.py:206-208`) ; le critère 3 n'exige que cinq touches.
   - What's unclear: étendre ou non la liste obligatoire.
   - Recommendation: documenter `F3` (un lecteur bloqué doit pouvoir sortir) et l'inclure dans les touches vérifiées, les cinq du critère restant le minimum opposable.
   - **Resolution:** adoptée. `docs/installation.md` documente `F3` avec son libellé `Quitter`, et le test `test_pilotage_clavier_avant_lancement` du plan 01-02 exige `F3`, `F7`, `F8`, `ESC`, `PageUp` et `PageDown` dans la section clavier, qui précède la commande de lancement web (D-09).

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `.venv/Scripts/python.exe` | Toutes les exigences (D-15) | oui | 3.14.7 (plancher déclaré `>=3.11`) | — |
| `pytest` dans `.venv` | GARD-01/02 et tous les contrôles | oui | 9.1.1 | — |
| Interpréteur ambiant (`python` → venv GSD) | — | non pour `pytest` | `No module named pytest` (observé) | Utiliser `.venv/Scripts/python.exe` (obligatoire) |
| `flask` (import du parseur web) | Critère 4 | oui | 3.1.3 | — |
| `ortools` (import transitif de `dofus_stuff.web`) | Critère 4 | oui | import vérifié | — |
| `git` | Commits locaux, `git status` | oui | 2.55.0.windows.4 | — |
| Base locale `.data/dofus.sqlite3` | Aucune exigence de la phase 1 (lecture interdite en test) | oui, présente | 24 989 696 octets | Les contrôles n'en dépendent pas |
| Recherche externe (context7 / websearch) | Aucune (sources locales décidées en amont) | non | `websearch` → `{"available": false, "reason": "BRAVE_API_KEY not set"}` ; aucun outil context7 dans cet hôte | Constats internes au dépôt, vérifiés par exécution ou lecture |
| Réseau | Interdit par la phase | non (politique) | — | Aucun contrôle de la phase n'ouvre de connexion |

**Missing dependencies with no fallback:** aucune — toutes les dépendances d'exécution sont présentes dans `.venv`.

**Missing dependencies with fallback:** fournisseurs de recherche externes indisponibles ; remplacés par la lecture et l'exécution locales (voir §Sources), sans aucun digest inventé et sans écriture de cache.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest` 9.1.1, exécuté par `.venv/Scripts/python.exe` (Python 3.14.7) |
| Config file | `pyproject.toml` — `[tool.pytest.ini_options]` : `testpaths = ["tests"]`, `pythonpath = ["."]` (lignes 38-39) |
| Quick run command | `./.venv/Scripts/python.exe -m pytest tests/test_docs_structure.py tests/test_docs_code_anchor.py -q` |
| Full suite command | `./.venv/Scripts/python.exe -m pytest -q` (re-mesuré le 2026-09-11 : `136 passed in 1.61s`) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SOMM-01 | La section « Documentation utilisateur » du `README.md` contient un lien unique résolu vers `docs/sommaire.md` | structure | `pytest tests/test_docs_structure.py::test_readme_links_to_sommaire -q` | non — Wave 0 |
| SOMM-02 | Les cibles du sommaire et les pages présentes forment le même ensemble | structure | `pytest tests/test_docs_structure.py::test_sommaire_lists_every_document tests/test_docs_structure.py::test_sommaire_links_resolve -q` | non — Wave 0 |
| SOMM-03 | H1 unique par page, égal au libellé d'index, plus ligne de retour vers `sommaire.md` | structure | `pytest tests/test_docs_structure.py::test_h1_matches_sommaire_entry tests/test_docs_structure.py::test_pages_have_back_link -q` | non — Wave 0 |
| INST-01 | `docs/installation.md` porte `pip install -e ".[dev]"`, le plancher `3.11` conforme à `pyproject.toml`, la commande de vérification et un premier contact CLI analysable | structure + ancrage | `pytest tests/test_docs_structure.py tests/test_docs_code_anchor.py -q` | non — Wave 0 |
| INST-02 | L'adresse par défaut citée vient des défauts réels du parseur (`127.0.0.1:5000`) et le mode hors-ligne par défaut est annoncé | ancrage | `pytest tests/test_docs_code_anchor.py::test_adresse_par_defaut_documentee -q` | non — Wave 0 |
| INST-03 | Les touches `F7`, `F8`, `ESC`, `PageUp`, `PageDown` sont citées avant la commande de lancement web | structure | `pytest tests/test_docs_structure.py::test_pilotage_clavier_avant_lancement -q` | non — Wave 0 |
| GARD-01 | Une dérive (lien mort, page non listée, H1 divergent) fait échouer la suite ; l'état livré reste vert | structure (mutation) | `pytest tests/test_docs_structure.py::test_mutation_detecte_les_trois_derives -q` | non — Wave 0 |
| GARD-02 | Les options d'entrée web citées sont acceptées par le parseur réel et présentes dans `format_help()` ; les chemins `.py` cités existent | ancrage | `pytest tests/test_docs_code_anchor.py -q` | non — Wave 0 |

### Inventaire de tests proposé (nommage anglais, docstrings françaises — convention du dépôt)

`tests/test_docs_structure.py` (module **sans import du produit** — stdlib + fixtures uniquement) :

1. `test_docs_directory_has_sommaire` — `docs/sommaire.md` existe.
2. `test_sommaire_lists_every_document` — égalité d'ensembles (SOMM-02).
3. `test_sommaire_links_resolve` — chaque cible du sommaire existe.
4. `test_all_relative_links_resolve` — tous les fichiers de `docs/`.
5. `test_no_anchor_or_absolute_links` — refus des cibles `#`, `/…`, `C:\…`, `file://`, et des antislashs.
6. `test_readme_links_to_sommaire` — lien unique + cible résolue (SOMM-01, D-10).
7. `test_h1_matches_sommaire_entry` — H1 unique, égal au libellé d'index (normalisé).
8. `test_pages_have_back_link` — ligne de retour ciblant `sommaire.md` (SOMM-03).
9. `test_pilotage_clavier_avant_lancement` — ordre clavier < lancement web (D-09, INST-03).
10. `test_documents_are_utf8_and_not_drafts` — décodage strict, absence de `TODO` / `À COMPLÉTER` / `Lorem`, longueur minimale.
11. `test_normalisation_insensible_aux_accents_et_casse` — la normalisation de D-11 est elle-même testée (obligation explicite de D-12) : `Éléments` ≡ `elements`, `&#39;` ≡ `'`, `A  B` ≡ `A B`, CRLF ≡ LF.
12. `test_mutation_detecte_les_trois_derives` — critère 5 (copie `tmp_path` + 3 dérives, message localisant exigé).

`tests/test_docs_code_anchor.py` (module qui **importe le produit**, jamais `main()`) :

1. `test_sources_de_verite_exist` — chaque chemin `.py` cité dans `docs/installation.md` existe sur disque (D-03).
2. `test_documented_entry_options_parse` — sondes d'argv complets acceptées par `build_parser()` (critère 4), `SystemExit` converti (Pattern 4).
3. `test_documented_entry_options_appear_in_help` — contenance dans `format_help()`.
4. `test_documented_entry_options_are_documented` — sens inverse : chaque option réelle de la surface publique apparaît dans `docs/installation.md` (empêche la doc d'en inventer une et de passer sous silence les autres).
5. `test_adresse_par_defaut_documentee` — `http://127.0.0.1:5000` dérivé du parseur.
6. `test_cli_examples_of_installation_page_parse` — optionnel recommandé (Open Question 3).

Réservé aux phases suivantes (ne pas ouvrir maintenant) : sous-commandes et exemples de `docs/cli.md` (phase 2), libellés de rendu et identifiants d'écrans (phase 3-4), noms de champs de `db status` (phase 5), liste épinglée des 8 pages et mutation formelle (phase 6).

### Sampling Rate

- **Per task commit :** `./.venv/Scripts/python.exe -m pytest tests/test_docs_structure.py tests/test_docs_code_anchor.py -q`
- **Per wave merge :** `./.venv/Scripts/python.exe -m pytest -q`
- **Phase gate :** suite complète verte **et** test de mutation vert avant `/gsd:verify-work` ; compteur et durée **re-mesurés** au moment de la citation, jamais recopiés depuis ce document.

### Wave 0 Gaps

- [ ] `docs/sommaire.md` — index unique + parcours (SOMM-01, SOMM-02)
- [ ] `docs/installation.md` — gabarit D-01, chemin d'installation, clavier avant lancement (INST-01 à INST-03)
- [ ] `README.md` — section « Documentation utilisateur » (SOMM-01, D-10)
- [ ] `tests/conftest.py` — fixture `docs_dir`, normalisation testée (D-11, D-12)
- [ ] `tests/test_docs_structure.py` — 12 tests ci-dessus (GARD-01)
- [ ] `tests/test_docs_code_anchor.py` — 5 tests ci-dessus (GARD-02)
- [ ] Framework : **aucun** (`pytest` 9.1.1 déjà installé, configuration déjà présente)

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | non | Aucune authentification dans le périmètre : interface locale mono-utilisateur ; la doc ne doit pas suggérer d'exposition réseau |
| V3 Session Management | non | Aucune session applicative documentée dans cette phase |
| V4 Access Control | non | Idem V2 ; le seul contrôle d'accès pertinent est l'écoute par défaut sur `127.0.0.1` (`dofus_stuff/web/__main__.py:33`) |
| V5 Input Validation | oui | Validation des **cibles de liens** dans le harnais : refus des schémas non relatifs, des ancres `#`, des antislashs et des cibles sortant de la racine du dépôt ; refus de tout fichier non décodable en `utf-8` strict ; validation des argv documentés par le parseur réel |
| V6 Cryptography | non | Aucune cryptographie dans le périmètre ; aucun secret ne doit être copié dans la doc (`DOFUS_SECRET_KEY` : nom seulement) |

### Known Threat Patterns for {documentation vérifiée par tests + Flask local}

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Secret de développement recopié dans la doc (`DOFUS_SECRET_KEY`, `stuff-machine-dev-secret` en `dofus_stuff/web/__init__.py:40`) | Information Disclosure | La doc nomme les variables d'environnement, jamais leur valeur ; le contrôle peut asserter l'absence de la chaîne `dev-secret` dans `docs/` |
| Doc recommandant `--host 0.0.0.0` (exposition d'un serveur de développement sans authentification) | Information Disclosure / Elevation of Privilege | Ne documenter que le défaut `127.0.0.1` ; toute recommandation d'exposition est un constat de sévérité **haute** (bloquant selon `security_block_on: "high"`) |
| Doc recommandant `--debug` dans le chemin normal (débogueur Werkzeug = exécution de code) | Elevation of Privilege | Ne pas l'inscrire dans le chemin minimal (D-07) ; au plus une mention « réservé au développement » |
| Commande destructrice présentée dans un parcours (`db clear`, `PURGE`) | Tampering / Denial of Service | Phase 1 : ces commandes n'apparaissent dans aucune des deux pages (`docs/installation.md` ne doit enseigner que `--offline db status`) ; la règle « jamais dans un parcours » et son contrôle arrivent en phase 5 |
| Cible de lien sortant du dépôt (`../../…`) ou absolue | Tampering | Le contrôle de liens résout la cible et exige qu'elle reste sous la racine du dépôt ; les cibles absolues et `file://` sont refusées |
| Harnais qui écrit sous `.data/` (perte de la base de développement) | Tampering | Aucune fixture de la phase n'ouvre la base ; les fixtures existantes utilisent `tmp_path` + `offline=True` + `load_catalog=False` |
| Contrôle qui ouvre une connexion réseau (fuite d'information, quotas Dofusdude) | Information Disclosure | `parse_args` n'exécute rien ; `main()` n'est jamais appelé ; aucun test ne charge le catalogue depuis un `data_dir` par défaut |
| Instruction d'installation qui déclenche une resynchronisation non voulue | Denial of Service (quota) | Le premier contact CLI documenté est hors-ligne (`--offline db status`) ; `db sync` n'est mentionné que comme action explicite (phase 5) |

Aucun secret, identifiant ou résultat de validation humaine n'est nécessaire à cette phase : il n'y a donc **aucun blocage d'exécution** de nature sécurité. Le niveau ASVS 1 est couvert par la validation d'entrées du harnais et par les interdits de rédaction ci-dessus.

## Sources

### Primary (HIGH confidence) — dépôt réel, lu ou exécuté

Fichiers lus (chemins relatifs à la racine du dépôt) :

- `pyproject.toml:10` (`requires-python = ">=3.11"`), `:18-21` (extra `dev`, `pytest>=8.0`), `:22-24` (`dofus-stuff`, `dofus-stuff-web`), `:38-39` (`testpaths`, `pythonpath`)
- `README.md:1-5` (titre, phrase d'intro, `## Base locale Dofus`), `:59` (`**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)`)
- `dofus_stuff/web/__main__.py:10-46` (parseur web : `--data-dir` défaut `DOFUS_DATA_DIR` ou `DEFAULT_DATA_DIR`, `--offline` défaut `True`, `--no-offline`, `--online`, `--timeout`, `--host 127.0.0.1`, `--port 5000`, `--debug`), `:49-60` (`main()` — jamais exécuté par les tests)
- `dofus_stuff/web/__init__.py:40` (`DOFUS_SECRET_KEY`, défaut de développement), `:44` (`DOFUS_OFFLINE` défaut `True`), `:92-121` (`reload_catalog`, `skip_sync` quand hors-ligne)
- `dofus_stuff/web/routes.py:66-69` (`DEFAULT_FKEYS = [("F3", "Quitter"), ("ESC", "Retour")]`), `:137-141` (barre `F7`/`F8` conditionnelle + libellés `Precedent`, `Page prec`, `Suivant`, `Page suiv`), `:189-208` (menu : 5 entrées, `PGM: MNU-01`, `fkeys=[("F3", "Quitter")]`), `:647` (message « AUCUNE VERSION EN BASE »)
- `dofus_stuff/web/static/js/terminal.js:547-604` (gestionnaire global `keydown` : `F3`, `Escape`, `F7`, `F8`, `PageUp`, `PageDown`, `Enter` dans le champ, espace hors champ)
- `dofus_stuff/web/static/js/terminal.js` (une seule feuille de style JS dans `static/js/`, `static/css/terminal.css` référencée par `templates/screen.html`)
- `dofus_stuff/cli.py:32-51` (parseur racine : `--timeout`, `--data-dir`, `--force-sync`, `--offline`), `:54-55` (`version`, `self-test`), `:180-189` (`db status|stats|sync|fill|clear`), `:203-212` (`_load_catalog` → `Catalog.load(offline=args.offline, …)`), `:214-232` (`_print_db_status` : libellés exacts `Fichier :`, `Version jeu :`, `Dernier check : il y a Xh` / `(aucun)`, `Entrées :`, `Par catégorie :`), `:329-407` (`main()` — jamais exécuté), `:24-31` (épilog d'exemples hors-ligne)
- `dofus_stuff/database.py:13` (`DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / ".data"`), `:12` (`DB_NAME = "dofus.sqlite3"`)
- `dofus_stuff/sync.py:43` (message « Base locale vide et --offline : impossible de synchroniser »)
- `tests/conftest.py:3-9` (imports), `:72-110` (fixtures `catalog`, `app` avec `data_dir=tmp_path`, `offline=True`, `load_catalog=False`, `client`)
- `fetcher.py:1-11` (shim CRLF vers `dofus_stuff.cli:main`)
- `.gitignore` (`.data/`, `.venv/`, `.gsd-auto/`)
- `.planning/ROADMAP.md` § Phase 1 (objectif, 5 critères, 4 plans), `.planning/REQUIREMENTS.md:16-24,58-61` (exigences verbatim), `.planning/phases/01-…/01-CONTEXT.md` (D-01 à D-15)

Commandes exécutées et résultats observés (2026-09-11, `.venv/Scripts/python.exe`) :

- `pytest --version` → `pytest 9.1.1` ; `-c "import sys; print(sys.version)"` → `3.14.7 …` ; `flask 3.1.3` ; `git --version` → `2.55.0.windows.4`
- `python -m pytest -q` → `136 passed in 1.61s` (état livré, re-mesuré le 2026-09-11 pendant cette recherche, avant tout ajout de cette phase)
- Prototype `_probe3.py` (écrit puis **exécuté**, puis supprimé ; jamais commité) → `format_help()` contient les 8 options web (`True` ×8) ; `parse_args(["--unknown-flag"])`, `(["--host"])`, `(["--port", "abc"])` → `SystemExit(2)` ; détection des 3 dérives avec messages localisants ; nettoyage OK ; arbre sain
- Prototype pytest jetable (`_probe_pytest/`, supprimé) → import inter-modules autorisé, `shutil.copytree(docs_dir, tmp_path / "docs")` fonctionnel, mutation détectée (`2 passed`), et `SystemExit` rapporté comme `FAILED … SystemExit: 2` avec trace `argparse`
- `fetcher.py --offline --data-dir <tmp> db status` → code 0, base créée, `Fichier : …`, `Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0`
- `fetcher.py --offline --data-dir <tmp> version` → code 1, `Erreur : Base locale vide et --offline : impossible de synchroniser` (stderr)
- `fetcher.py --data-dir <tmp> db status --offline` → code 2, `unrecognized arguments: --offline`
- `create_app(data_dir=<tmp neuf>, offline=True)` + `GET /` → `200`, menu à 5 entrées, `F3 = Quitter`, `catalog.version = None`, création de `dofus.sqlite3` ; `.data/` inchangée (horodatage constant)
- `git status --porcelain` → ` M .gitignore` (ajout de `.gsd-auto/`) + fichiers non suivis préexistants (`doc-agent.toml`, `gsd-auto.toml`, `gsd-auto-rules.toml`, `.doc-agent/`) : **ne jamais** utiliser `git add .`

### Secondary (MEDIUM confidence) — recherche amont du milestone (locale, `[CITED]`)

- `.planning/research/SUMMARY.md`, `STACK.md`, `ARCHITECTURE.md`, `PITFALLS.md`, `FEATURES.md` — cadrage déjà réalisé (structure `docs/`, conventions de vérifiabilité, pièges mesurés : 136 tests qui ne lisent aucune doc, menu modifié par `ab1eb38` sans mise à jour documentaire).

### Tertiary (LOW confidence)

- **Aucune.** Le seam de recherche externe a été sollicité : `gsd-tools query research-plan --input <…>` a produit 3 items (`context7` ×2 pour le domaine documentaire, `websearch` ×1) ; `gsd-tools query websearch "…"` a répondu `{"available": false, "reason": "BRAVE_API_KEY not set"}` et aucun outil `context7` n'existe dans cet hôte. Aucun digest n'a donc été écrit dans le cache de recherche, aucune source externe n'est citée, et rien n'a été inventé pour combler le manque.

## Metadata

**Confidence breakdown:**

- Standard stack : HIGH — aucune dépendance nouvelle ; `pytest` déjà installé et configuré, versions mesurées dans `.venv`.
- Architecture : HIGH — mécanismes d'invariant et de mutation **exécutés** sur le dépôt réel (prototypes supprimés après mesure).
- Pitfalls : HIGH — chaque piège est adossé à une observation (codes retour, messages d'erreur, lignes de code) ; la seule tension de conception non tranchée est explicitement listée en Open Questions.
- Ancrage version : HIGH pour le plancher Python (`pyproject.toml:10`) ; le compteur de tests (`136`) est un instantané daté, à re-mesurer avant toute citation.

**Research date:** 2026-09-11
**Valid until:** 2026-10-11 (30 jours — le produit est figé ; seules les décisions de contenu peuvent bouger)