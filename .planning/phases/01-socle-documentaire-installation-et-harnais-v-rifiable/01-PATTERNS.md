# Phase 1 : Socle documentaire, installation et harnais vérifiable — Carte de patrons

**Cartographié :** 2026-09-11
**Fichiers analysés :** 6 (1 modifié en profondeur, 5 créés/modifiés)
**Analogues trouvés :** 6 / 6 (dont 2 partiels : aucune norme externe réimplémentée n'existe dans le dépôt)

**Portée de la recherche d'analogues :** racine du dépôt, `tests/`, `dofus_stuff/cli.py`, `dofus_stuff/web/__main__.py`.
**Gate source suivi (#3645) :** chaque analogue nommé ci-dessous est vérifié suivi par git — `git ls-files -- README.md GUIDE_WIZARD.md pyproject.toml tests/conftest.py tests/test_web.py tests/test_screens.py dofus_stuff/cli.py dofus_stuff/web/__main__.py` renvoie les 8 chemins (non vide = suivi). Aucun chemin de miroir ignoré par git (`.gsd-auto/`, `.doc-agent/`, `.data/`) n'est utilisé comme analogue.

---

## Classification des fichiers

| Fichier créé/modifié | Rôle | Flux de données | Analogue le plus proche | Qualité du rapprochement |
|----------------------|------|-----------------|-------------------------|--------------------------|
| `README.md` | documentation (page d'entrée dépôt, aussi `readme` du paquet) | contenu statique (Markdown rendu par GitHub) | `README.md` lui-même (§ `### Installation` l. 15-19, `### Usage CLI` l. 21-45, `### Interface web` l. 92-100) | exact (même fichier, sections existantes) |
| `docs/sommaire.md` | documentation (page d'index unique) | contenu statique + liens relatifs résolus | `GUIDE_WIZARD.md` (H1 l. 7 + sections `## N.` l. 13-19) ; liens `[libellé](cible)` : `README.md:59` | correspondance de rôle |
| `docs/installation.md` | documentation (page de procédure pas-à-pas) | contenu statique + blocs de code `bash` | `README.md` § `### Installation` / `### Usage CLI` / `### Interface web` (l. 15-45, 74-100) | correspondance de rôle |
| `tests/conftest.py` | fixture + helper de test | entrée/sortie fichier (lecture disque `utf-8`) | `tests/conftest.py:72-110` (fixtures `catalog`/`app`/`client` déjà en place) | exact (même fichier, mêmes fixtures) |
| `tests/test_docs_structure.py` | test (invariants purs, sans import du produit) | entrée/sortie fichier + transformation | `tests/test_screens.py:1-20` (module court de fonctions pures, docstring française) | correspondance de rôle |
| `tests/test_docs_code_anchor.py` | test (ancrage sur le code réel) | requête/réponse (parseur `argparse`) + entrée/sortie fichier | `tests/test_web.py:1-20` (import direct du produit + fixtures `conftest`) ; `tests/test_recommend.py:1-14` (style d'import du produit) | correspondance de rôle |

Le répertoire `docs/` **n'existe pas encore** (`ls docs` → `No such file or directory`, mesuré le 2026-09-11) : les deux pages sont de vraies créations, et le module de test doit donc tolérer un `docs/` absent sans erreur de collecte (voir « Aucun analogue trouvé »).

---

## Affectations de patrons

### `README.md` (documentation, contenu statique)

**Analogue :** `README.md` — patron de section existant, à reproduire sans toucher au reste.

**Structure actuelle et point d'insertion réel** (mesuré : `README.md` compte 121 lignes, `# dofus-stuff-machine` en l. 1, `## Base locale Dofus` en l. 5) :

```markdown
# dofus-stuff-machine                              <!-- l. 1 -->

Outils pour travailler avec les objets et ressources de Dofus : …   <!-- l. 3 -->

## Base locale Dofus                                <!-- l. 5 -->
```

**Patron de lien interne déjà employé** (l. 59) — c'est le seul précédent de renvoi documentaire du fichier, et celui que D-10 remplace :

```markdown
**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)
```

**Patron de renvoi vers un fichier du dépôt, forme attendue par D-10** (une seule cible, aucun lien vers les pages individuelles) :

```markdown
## Documentation utilisateur

… [Sommaire de la documentation](docs/sommaire.md)
```

**Section « Tests » à ne pas déformer** (l. 105-109) : elle ne cite qu'un compteur implicite (`pytest` nu). Le patron de vérification de la phase est `.venv/Scripts/python.exe -m pytest -q` — la mention peut être ajoutée là, mais **aucun compteur de tests ne doit être recopié** (il change à chaque phase, cf. RESEARCH « Pitfall 5 »).

**Contraintes de style observées :** prose française accentuée, `##`/`###`/`####` hiérarchisés, tableaux Markdown `| Option | Description |` (l. 85-90), blocs ``` ```bash ``` ``` avec commentaires `#`. Fins de ligne CRLF sur ce poste (mesuré) — aucun test ne doit asserter dessus.

---

### `docs/sommaire.md` (documentation, contenu statique + liens relatifs)

**Analogues :** `GUIDE_WIZARD.md` (forme d'une page de documentation française du dépôt) + `README.md:59` (forme du lien relatif).

**En-tête de page conforme à D-01** (adapté de `GUIDE_WIZARD.md:7-9`, H1 unique + une phrase d'introduction, sans front-matter) :

```markdown
# Guide du Wizard d’optimisation de stuff        <!-- GUIDE_WIZARD.md:7 -->

Ce guide explique comment utiliser le **wizard** de stuff-machine pour générer automatiquement un équipement Dofus, même si vous n’avez jamais utilisé l’outil.   <!-- GUIDE_WIZARD.md:9 -->
```

**Découpage par sections numérotées + séparateurs** (`GUIDE_WIZARD.md:11-19`) — patron réutilisable pour « parcours guidé » puis « index thématique » sur la même page (D-04) :

```markdown
---                                     <!-- GUIDE_WIZARD.md:11 -->

## 1. À quoi sert le wizard ?            <!-- GUIDE_WIZARD.md:13 -->

…                                       <!-- GUIDE_WIZARD.md:15-17 -->
```

**Forme des entrées d'index** (seul patron de lien interne du dépôt, `README.md:59`) :

```markdown
[libellé lisible](cible-relative.md)
```

**Invariant structurel qui gouverne cette page** (D-05/D-06, RESEARCH §Open Questions 1) : en phase 1, une **seule** entrée d'index (`installation.md`). Le parcours guidé des 7 thèmes est en **texte simple numéroté, sans `[…](…)`** — toute entrée en lien produirait une cible absente et ferait rougir `test_sommaire_links_resolve`, sans liste blanche possible. Le test d'exhaustivité bidirectionnel ne porte que sur les liens : une cible citée par le parcours et par l'index est sans effet sur l'égalité d'ensembles.

**Interdits vérifiés par test :** cible `#ancre`, cible absolue (`/…`, `C:\…`), `file://`, antislash, cible sortant du dépôt (`../../…`).

---

### `docs/installation.md` (documentation, page de procédure)

**Analogue :** `README.md` § `### Installation` (l. 15-19), `### Usage CLI` (l. 21-45), `#### Base locale` (l. 74-81), `### Interface web (terminal rétro)` (l. 92-100).

**Bloc d'installation déjà rédigé — à reprendre tel quel** (l. 15-19) :

````markdown
### Installation

```bash
pip install -e ".[dev]"
```
````

**Formulation de l'adresse par défaut déjà présente** (l. 99) — c'est exactement l'affirmation que `test_adresse_par_defaut_documentee` ancre :

```markdown
Par défaut : mode offline (base locale uniquement), écoute sur `http://127.0.0.1:5000`.
```

**Bloc de commandes CLI (l. 75-79)** — patron de bloc `bash` avec commentaire en fin de ligne ; **attention** : la l. 78 (`db clear`) est une commande destructrice qui n'a **rien** à faire dans `docs/installation.md` (chemin minimal D-07 : `--offline db status` uniquement, cf. RESEARCH §Security Domain).

**Tableau d'options (l. 85-90)** — patron réutilisable pour les options d'entrée web si la page en dresse la liste :

```markdown
| Option | Description |
|--------|-------------|
| `--timeout N` | Timeout HTTP en secondes (défaut : 15) |
```

**Valeurs à ancrer, telles que le code les produit (jamais recopiées d'un run) :**

| Affirmation de la page | Source réelle (suivie par git) | Contrôle |
|------------------------|-------------------------------|----------|
| Python 3.11+ | `pyproject.toml:10` `requires-python = ">=3.11"` | lecture `tomllib` possible (stdlib 3.11+) |
| `pip install -e ".[dev]"` | `pyproject.toml:18-21` extra `dev = ["pytest>=8.0"]` | présence verbatim dans la page |
| Adresse par défaut `http://127.0.0.1:5000` | `dofus_stuff/web/__main__.py:33-34` (`--host` défaut `127.0.0.1`, `--port` défaut `5000`) | `build_parser().parse_args([])` → `f"http://{args.host}:{args.port}"` |
| Mode hors-ligne par défaut | `dofus_stuff/web/__main__.py:22-26` (`--offline` `default=True`, `BooleanOptionalAction`) | mention de `--offline` / `--no-offline` |
| Premier contact CLI `python fetcher.py --offline db status` | `dofus_stuff/cli.py:32-51` (options racine `--timeout`, `--data-dir`, `--force-sync`, `--offline`) + l. 180-189 (`db status|stats|sync|fill|clear`) | `shlex.split` + `dofus_stuff.cli.build_parser().parse_args` |
| Libellés de sortie `Fichier :`, `Version jeu :`, `Dernier check :`, `Entrées :`, `Par catégorie :` | `dofus_stuff/cli.py:214-229` (`_print_db_status`) | présence des libellés seuls, **jamais** de valeur |
| Touches `F3`, `F7`, `F8`, `ESC`, `PageUp`, `PageDown` | `dofus_stuff/web/static/js/terminal.js:547-604` ; `ESC` aussi dans `dofus_stuff/web/routes.py:66-69` (`DEFAULT_FKEYS`) | présence + position **avant** `python -m dofus_stuff.web` |

**Contrainte d'ordre D-09 (clavier avant lancement)** — le contrôle doit viser la **section** clavier, pas la première occurrence de la lettre trouvée dans la page : un repère de section (titre `## … clavier …`) est nécessaire, sinon un exemple de barre de touches cité plus haut fera passer ou échouer le test au hasard.

**Interdits de rédaction à ne pas réintroduire :** `uv`/`poetry`/`pipx` (D-08), `--host 0.0.0.0`, `--debug` dans le chemin minimal, toute valeur de `DOFUS_SECRET_KEY`, `db clear`, `db sync` présenté comme une étape d'installation, tout compteur d'objets ou de tests.

---

### `tests/conftest.py` (fixture + helper, lecture disque)

**Analogue :** `tests/conftest.py:72-110` — fixtures déjà présentes, à **compléter** sans modifier les fixtures existantes (D-12).

**En-tête du module à conserver** (l. 1-9) : docstring française d'une ligne, `from __future__ import annotations`, import de `pytest` en premier bloc puis imports du produit. Les ajouts se placent **après** la l. 110 (fin de `client`), pour ne rien déranger au-dessus.

**Patron de fixture existant** (l. 72-78 et 108-110) : décorateur nu `@pytest.fixture`, annotation de type de retour, `yield` quand il y a une ressource à libérer.

```python
@pytest.fixture
def catalog() -> Catalog:
    return Catalog(version="9.9.9.9", items=_sample_items())


@pytest.fixture
def app(catalog: Catalog, tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    …
    yield application
    catalog.close()


@pytest.fixture
def client(app):
    return app.test_client()
```

**Ajouts attendus pour cette phase (calqués sur ce patron) :**

```python
# à placer après la fixture client (l. 110), imports en tête de fichier
import html
import re
import unicodedata
from pathlib import Path


def _normalize(text: str) -> str:
    """Normalise un libellé pour comparaison (D-11) : entités HTML, accents, casse, espaces."""
    text = html.unescape(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().lower()


@pytest.fixture(scope="session")
def docs_dir() -> Path:
    """Racine du dossier docs/ du dépôt, indépendante du répertoire courant."""
    return Path(__file__).resolve().parents[1] / "docs"


@pytest.fixture(scope="session")
def normalize():
    """Expose _normalize aux modules de test sans import inter-modules."""
    return _normalize
```

**Écarts assumés par rapport à l'analogue :** les fixtures existantes sont de portée *fonction* et dépendent de `tmp_path` ; `docs_dir` / `normalize` sont de portée **session** (lecture seule d'un arbre figé, aucun état mutable) — c'est le seul endroit du fichier où `scope="session"` apparaît. Un module d'aide séparé est **interdit** (D-12) : le helper doit rester dans ce fichier, et son comportement est testé (D-11, test n° 11 de l'inventaire RESEARCH).

---

### `tests/test_docs_structure.py` (test, lecture fichier + transformation)

**Analogue :** `tests/test_screens.py:1-20` — module court, docstring française, un test = une fonction, noms de fonctions en anglais, aucune classe.

**En-tête du module (structure exacte à reproduire) :**

```python
"""Tests unitaires des helpers de mise en page."""      # tests/test_screens.py:1

from dofus_stuff.web.screens import (                    # tests/test_screens.py:3 — ici : stdlib seulement
    BODY_LINES,
    …
)


def test_clip_pads_and_truncates():                      # tests/test_screens.py:19
    assert len(clip("ABC", 5)) == 5
```

**Écart structurant, imposé par la recherche :** ce module **n'importe pas le produit** (stdlib + fixtures uniquement) — c'est ce qui autorise le test de mutation et l'exécution sans base ni réseau. Il porte en revanche des **fonctions pures au niveau module**, paramétrées par `docs_dir: Path` et renvoyant `list[str]` (liste vide = conforme), que les tests appellent deux fois : contre l'arbre livré **et** contre une copie `tmp_path` (RESEARCH §Pattern 1, critère 5).

**Patron de fonction d'invariant + test mince (squelette du prototype exécuté) :**

```python
import re
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)\)")
H1 = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.MULTILINE)


def _pages(docs_dir: Path) -> list[Path]:
    return sorted(docs_dir.rglob("*.md"))


def problemes_liens(docs_dir: Path) -> list[str]:
    """Liens relatifs non résolus ; chaque problème cite la page et la cible (D-13)."""
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

**Messages d'échec — écart assumé par rapport à l'analogue :** les assertions de `tests/test_web.py` / `tests/test_screens.py` sont **nues** (`assert b"MENU PRINCIPAL" in rv.data`) ; D-13 impose ici le message à trois éléments (page + libellé attendu + fichier source). C'est une déviation volontaire du style existant, pas une incohérence.

**Patron du test de mutation (critère 5)** — copie jetable, jamais l'arbre réel :

```python
def test_mutation_detecte_les_trois_derives(tmp_path: Path, docs_dir: Path) -> None:
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

Le précédent `tmp_path` du dépôt est `tests/test_web.py:389` (`def test_catalog_load_releases_db(tmp_path):`) — même mécanique de bac à sable, portée par pytest.

**Contrôle d'ordre clavier (INST-03 / D-09)** — à repérer par section, jamais par première occurrence :

```python
TOUCHES = ["F3", "F7", "F8", "ESC", "PageUp", "PageDown"]
LANCEMENT_WEB = "python -m dofus_stuff.web"
```

**Contraintes D-15 respectées par construction :** aucune fixture du module n'ouvre la base ni le catalogue, aucun `subprocess`, aucune socket, `main()` jamais appelé. `docs/` peut être absent au premier commit : la fonction d'invariant doit alors renvoyer un problème lisible plutôt que lever (`docs/sommaire.md : absent`) — un `FileNotFoundError` non converti violerait D-13.

---

### `tests/test_docs_code_anchor.py` (test, requête/réponse + lecture fichier)

**Analogues :** `tests/test_web.py:1-20` (import du produit + fixtures implicites de `conftest`) ; `tests/test_recommend.py:1-14` (import direct de modules internes, sans `sys.path`).

**En-tête du module, forme observée :**

```python
"""Tests d'intégration Flask — parité CLI."""            # tests/test_web.py:1

from __future__ import annotations                       # tests/test_web.py:3

from unittest.mock import patch                          # tests/test_web.py:5

from dofus_stuff.catalog import Catalog                  # tests/test_web.py:7


def test_menu_get(client):                               # tests/test_web.py:10
    rv = client.get("/")
    assert rv.status_code == 200
```

Le module d'ancrage suit ce patron : docstring française, `from __future__ import annotations`, puis **import du produit en surface publique uniquement** :

```python
from dofus_stuff.web.__main__ import build_parser
```

`dofus_stuff.cli.build_parser` est utilisé dans les mêmes conditions pour les commandes `fetcher.py` citées par la page (option recommandée par l'Open Question 3 de la recherche).

**Patron de sonde d'argv : `SystemExit` converti en assertion localisante (D-13 / Pitfall 3)** — c'est l'écart décisif par rapport à l'analogue `test_web.py`, où aucun `SystemExit` n'est intercepté :

```python
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

**Patron d'adresse par défaut dérivée du parseur (INST-02) :** `parse_args([])` puis recomposition `f"http://{args.host}:{args.port}"` — jamais les littéraux `127.0.0.1` / `5000` écrits en dur dans le test.

**Patron « Source de vérité » (D-03) :** chaque chemin `` `…py` `` cité par la page est vérifié par `(racine_du_depot / chemin).exists()`, la racine étant dérivée de `Path(__file__).resolve().parents[1]` (même patron que la fixture `docs_dir`) — jamais `Path(".")` ni le répertoire courant.

**Sûreté de la sonde CLI :** `shlex.split(exemple)` puis `parse_args` uniquement — `parse_args` ne fait que lire les arguments ; `db clear` et `db sync` sont **parsés**, jamais exécutés (pas de `subprocess`), conformément à la contrainte « ne jamais exécuter `main()` ».

---

## Patrons transverses

### Lecture de fichier avec encodage explicite
**Source :** aucun précédent dans le dépôt — `grep -rn "read_text\|unicodedata\|html.unescape" tests/` ne renvoie **rien** (mesuré le 2026-09-11). Patron neuf, fixé par RESEARCH §Pattern 2 et Pitfall 7.
**S'applique à :** `tests/conftest.py`, `tests/test_docs_structure.py`, `tests/test_docs_code_anchor.py`.

```python
page.read_text(encoding="utf-8")     # jamais read_text() nu, jamais read_bytes() pour comparer
page.write_text(texte, encoding="utf-8")   # y compris dans la copie de mutation
```

Fins de ligne mesurées sur ce poste : `README.md`, `GUIDE_WIZARD.md`, `pyproject.toml`, `tests/conftest.py`, `tests/test_web.py`, `dofus_stuff/cli.py` sont **tous en CRLF** ; la recherche amont signale un mélange CRLF/LF. Conclusion identique dans les deux cas : **aucune assertion sur les octets de fin de ligne**, la normalisation `\s+ → " "` couvre CRLF et LF.

### Normalisation des libellés (D-11)
**Source :** portée par `tests/conftest.py`, exposée par la fixture `normalize`.
**S'applique à :** comparaison H1 ↔ libellé d'index, libellé d'écran cité par la doc, chemins du bloc « Source de vérité », touches.

```python
html.unescape(text)                       # nécessaire : GET / renvoie « 1. RECHERCHE D&#39;OBJETS »
unicodedata.normalize("NFKD", text)       # « Épée » ≡ « Epee »
"".join(ch for ch in text if not unicodedata.combining(ch))
re.sub(r"\s+", " ", text).strip().lower() # CRLF ≡ LF, espaces multiples ≡ un
```

Chaîne observée le 2026-09-11 par la recherche : `tests/test_web.py:16` asserte `b"MENU PRINCIPAL"` en octets bruts — ce style reste valable pour l'ancrage de libellés **non accentués**, mais toute comparaison avec la prose accentuée doit passer par `normalize`.

### Messages d'échec localisants (D-13)
**Source :** aucun analogue — les assertions existantes sont nues.
**S'applique à :** les deux modules de test de la phase.

Trois éléments obligatoires dans chaque message : **la page concernée**, **le libellé attendu**, **le fichier de code où il n'a pas été trouvé**. Un `FAILED` dont le corps est une trace `argparse.py` est un défaut du harnais (Pitfall 3), pas une divergence doc/code.

### Conventions de nommage des tests
**Source :** `tests/test_web.py`, `tests/test_screens.py`, `tests/test_optimize.py`, `tests/test_recommend.py`, `tests/test_profile_input.py` — **noms de fonctions en anglais, docstrings en français** (observé sur les 6 modules, seule `test_web.py:22` porte une docstring, en français).
**S'applique à :** les 12 + 5 fonctions de test de l'inventaire RESEARCH.

### Interdits de sûreté communs aux deux modules
**Source :** `tests/conftest.py:78-105` — les fixtures existantes passent déjà `data_dir=tmp_path / "data"`, `offline=True`, `load_catalog=False` : c'est le patron à ne pas défaire.
**S'applique à :** tout le harnais.

- jamais `main()`, jamais `subprocess`, jamais de socket ;
- jamais de lecture ni d'écriture sous `.data/` (`.data/dofus.sqlite3` reste intact) ;
- jamais d'API privée d'`argparse` (D-14) : `build_parser()`, `parse_args`, `format_help()` suffisent ;
- la mutation s'exécute sur `shutil.copytree(docs_dir, tmp_path / "docs")`, jamais sur l'arbre livré.

### Commandes d'exécution de référence (D-15)
**Source :** `pyproject.toml:38-39` (`testpaths = ["tests"]`, `pythonpath = ["."]`).

```bash
./.venv/Scripts/python.exe -m pytest tests/test_docs_structure.py tests/test_docs_code_anchor.py -q
./.venv/Scripts/python.exe -m pytest -q
```

Aucune configuration pytest à ajouter : les deux nouveaux modules sont détectés par `testpaths` sans modification de `pyproject.toml` (`pytest>=8.0` déjà dans l'extra `dev`, l. 18-21 ; aucun `conftest` racine supplémentaire à créer).

---

## Aucun analogue trouvé

| Fichier / patron | Rôle | Flux de données | Raison |
|------------------|------|-----------------|--------|
| Normalisation `unicodedata` + `html.unescape` (`_normalize`) | utilitaire | transformation | Aucun helper de normalisation n'existe dans `tests/` (grep vide) ; aucun module ne lit de fichier de documentation aujourd'hui — 136 tests verts, aucun ne lit `docs/` (mesure de la recherche amont). Patron à créer d'après RESEARCH §Pattern 2. |
| Harnais de mutation (`shutil.copytree` + injection de dérive) | test | entrée/sortie fichier | Aucun test du dépôt ne copie un arbre de fichiers ; seul précédent partiel : `tests/test_web.py:389` (`tmp_path` comme bac à sable). Patron fixé par RESEARCH §Pattern 1 et §Code Examples. |
| Pages `docs/*.md` | documentation | contenu statique | Le répertoire `docs/` **n'existe pas** (`ls docs` → erreur, mesuré). Analogues de forme les plus proches (H1, prose française, sections numérotées) : `GUIDE_WIZARD.md` et `README.md` ; le gabarit lui-même vient de D-01. |
| Suffixe d'index / ligne de retour vers le sommaire | documentation | contenu statique | Aucun renvoi « retour à l'index » n'existe dans le dépôt (`GUIDE_WIZARD.md` ne contient **aucun** lien Markdown ; `README.md` n'en contient qu'un, l. 59). Forme laissée à la discrétion du plan, seule la **cible** `sommaire.md` est vérifiée. |

---

## Métadonnées

**Portée de la recherche d'analogues :** racine du dépôt, `tests/`, `dofus_stuff/` (lecture seule), `pyproject.toml`, `.gitignore`.
**Fichiers lus pour extraction :** `tests/conftest.py`, `tests/test_web.py`, `tests/test_screens.py`, `tests/test_recommend.py`, `tests/test_optimize.py`, `tests/test_profile_input.py`, `README.md`, `GUIDE_WIZARD.md`, `pyproject.toml`, `dofus_stuff/cli.py`, `dofus_stuff/web/__main__.py`, `.claude/CLAUDE.md`.
**Fichiers suivis vérifiés (`git ls-files`) :** `README.md`, `GUIDE_WIZARD.md`, `pyproject.toml`, `tests/conftest.py`, `tests/test_web.py`, `tests/test_screens.py`, `dofus_stuff/cli.py`, `dofus_stuff/web/__main__.py`, `dofus_stuff/web/routes.py`, `dofus_stuff/web/static/js/terminal.js` — tous suivis, aucun miroir ignoré.
**Fichiers non suivis (jamais utilisés comme analogue) :** `doc-agent.toml`, `gsd-auto.toml`, `gsd-auto-rules.toml`, `.doc-agent/`, `.gsd-auto/`.
**Date d'extraction :** 2026-09-11.
**Contraintes dures rappelées au planificateur :** aucune dépendance nouvelle ; `dofus_stuff/**` jamais modifié ; aucune écriture sous `.data/` ; aucun réseau ; `main()` jamais exécuté ; helpers dans le `tests/conftest.py` existant ; interpréteur de référence `.venv/Scripts/python.exe -m pytest -q`.
