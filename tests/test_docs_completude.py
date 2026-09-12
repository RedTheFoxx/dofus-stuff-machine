"""Completude de la documentation livree : la liste epinglee confrontee au disque, dans les deux sens.

Contrat (`GARD-03`, `D-96`) : `PAGES_EPINGLEES` nomme les **huit** pages de `docs/` — les sept pages de
contenu et le sommaire — chacune avec le seuil de lignes non vides en dessous duquel elle est declaree
videe ; `PAGES_RACINE` nomme les deux fichiers de documentation de la racine du depot. La decouverte du
disque (`docs/*.md` et les deux fichiers de racine) est confrontee a cette liste **dans les deux sens** :
une page deplacee, renommee, ajoutee, supprimee ou videe est un constat nomme, jamais un silence. La
constante du module est la **seule source de verite** de ce qui est livre (`D-14`) : le disque ne fait que
la confirmer ou la contredire, il ne la remplace jamais.

Non-duplication ecrite (`D-12`) : l'egalite index <-> disque (dans les deux sens), le titre de niveau 1 de
chaque page et l'unicite des libelles d'index sont **deja** tenus par `tests/test_docs_structure.py`
(`problemes_index`, `problemes_h1`, `test_sommaire_index_labels_are_unique` ; mesures de la recherche,
`06-RESEARCH.md` § C.3). Ce module ne les rejoue pas : il ajoute les axes reellement neufs — la constante
epinglee du module confrontee au disque puis a l'index, le refus du vidage, et le compte des lignes du
tableau d'index.

Decision `D-100` : **encadrer la ligne de nettoyage de la base locale dans le `README.md`, jamais la
supprimer.** Cette decision est ecrite ici avant tout controle, avec sa justification :

- la ligne est un **contenu livre** (elle documente qu'une remise a zero existe), et `GARD-03` demande que
  la documentation n'**invite** pas a detruire les donnees tout en documentant les chemins de
  reconstruction : retirer la ligne perdrait l'information au lieu de proteger le lecteur ;
- une suppression **ne prouve rien** du besoin : aucune assertion ne saurait distinguer « information
  absente » de « information jamais livree » ;
- l'encadrement, lui, est **verifiable automatiquement** par deux constats distincts et nommes (mot
  d'avertissement manquant dans le bloc, renvoi vers la page de la base locale manquant) ;
- les regles de cette phase interdisent de supprimer de la documentation livree, comme elles interdisent
  toute action destructive sous `.data/` : on n'efface pas, on encadre.

La ligne de commande **reste** donc dans le `README.md`, et le controle exige en plus que l'information
soit **encore la** : une ligne de base disparue est un constat, au meme titre qu'une ligne privee de son
avertissement. Ce module **lit** le `README.md` et ne l'ecrit jamais (`T-06-03-05`) : la modification du
fichier est un acte de mise en oeuvre, pas une correction automatique d'un controle.

`MOTS_AVERTISSEMENT` est un **contrat de presence**, pas une exigence de style : les formes declarees sont
lues dans le `README.md` au moment de l'ecriture puis figees ici (`D-19`), et le controle exige au moins
l'une d'elles dans le bloc de chaque occurrence, jamais une tournure donnee.

Limites nommees (`D-85`), pour qu'aucun controle de ce module ne soit lu au-dela de ce qu'il mesure :

1. **Perimetre de decouverte** : `docs/*.md` (un seul niveau) et les deux fichiers de la racine. Une page
   rangee dans un **sous-dossier** de `docs/` ne serait pas vue — mesure de l'ecriture : `docs/` ne porte
   aucun sous-dossier. Un fichier suivi par `git` mais ignore par `.gitignore` est vu, puisque la
   decouverte passe par le disque ;
2. **Comparaison sur des chemins relatifs a la racine du depot**, construits par `Path` et normalises en
   chaines a barres obliques (`as_posix`) avant comparaison : l'ensemble est donc sensible a la maniere
   dont les separateurs sont ecrits, jamais au systeme de fichiers lui-meme ;
3. **Seuil de lignes non vides par page** = garde-fou **anti-vidage**, pas une mesure de qualite : il est
   declare une fois par page dans `PAGES_EPINGLEES`, sans pretention d'exhaustivite, et une page courte
   mais honnete reste possible ;
4. **Le controle lit le `README.md` sans le corriger** : il dit ce que le fichier porte, il ne reecrit
   rien et ne choisit pas la formulation de l'avertissement ;
5. **La qualite redactionnelle des avertissements n'est pas verifiee** : c'est un controle d'**occurrence
   et de renvoi**, pas de style, et l'effet reellement ressenti par un lecteur (comprend-il que la
   commande detruit sa base ?) n'est pas observable en processus — declare en `backstop`, aucune
   validation humaine n'est revendiquee ni simulee ;
6. **Une reformulation sans perte reste hors d'atteinte** : un avertissement deja present reecrit en
   d'autres termes, ou une ligne existante reecrite sans disparaitre, n'est vue ni par le controle des
   jetons conserves ni par la comparaison avec `git show HEAD:README.md`.

Ce module n'ouvre **aucune** base : il lit des fichiers texte du depot et rien d'autre. La garde de
cloture ne porte donc pas le resserrement `data_dir` de la phase 5 (un controle d'un risque inexistant
serait du bruit) ; elle refuse en revanche ce qui serait le risque reel d'un module documentaire — ouvrir
une base, lancer un processus, joindre le reseau, executer le produit, calculer un stuff ou supprimer un
fichier.
"""

# Aucun `from __future__ import annotations` ici, comme dans `tests/test_docs_base_locale.py` : une morsure
# du harnais qui insere un import interdit **en tete** du fichier produirait un module mort a la collecte
# (`from __future__ imports must occur at the beginning of the file` : `ast.parse` l'accepte, `compile` le
# refuse, et c'est `compile` que la reecriture d'assertions de pytest emploie) au lieu du constat attendu
# (Pitfall 5 de `06-RESEARCH.md`). Les annotations ecrites ici sont valides sans import differe.

import ast
import re
from pathlib import Path

import pytest

# --- Chemins et titres (constantes de lecture, jamais des chaines en clair dans un controle) ---

RACINE_DEPOT = Path(__file__).resolve().parents[1]
DOSSIER_DOCS = "docs"
SOMMAIRE = "sommaire.md"
TITRE_INDEX = "## Index"

# La liste epinglee : les **huit** pages de `docs/` avec leur seuil de lignes non vides, et les deux
# fichiers de documentation de la racine. Les seuils sont **lus sur le disque au moment de l'ecriture**
# puis declares ici (`D-14`, `D-19`) : mesure de l'ecriture, en lignes non vides — `docs/base-locale.md`
# 82, `docs/cli.md` 137, `docs/depannage.md` 71, `docs/glossaire.md` 44, `docs/installation.md` 91,
# `docs/parcours-simplifie.md` 174, `docs/sommaire.md` 20, `docs/wizard-avance.md` 162. Chaque seuil est
# une fraction de la mesure (trois quarts environ), jamais une exigence de qualite : il refuse le vidage
# et la troncature, pas la concision (limite 3). L'ordre des sept pages de contenu puis du sommaire est
# celui de `06-RESEARCH.md` § C.2.
PAGES_EPINGLEES = (
    ("docs/base-locale.md", 60),
    ("docs/cli.md", 100),
    ("docs/depannage.md", 50),
    ("docs/glossaire.md", 30),
    ("docs/installation.md", 65),
    ("docs/parcours-simplifie.md", 130),
    ("docs/sommaire.md", 15),
    ("docs/wizard-avance.md", 120),
)

# Les deux fichiers de documentation hors `docs/` : verifies existants, fichiers et non vides. Aucun seuil
# de lignes n'est declare pour eux : ce plan ne pretend pas les mesurer (limite 3).
PAGES_RACINE = ("README.md", "GUIDE_WIZARD.md")

# --- Motifs de morsure ---
# Portes par des constantes du module, jamais ecrits en clair dans une ligne d'assertion (regle du plan
# 03-03, tenue par les phases 3 a 5) : pytest reproduit la ligne source de l'`assert`, une valeur en clair
# y serait trouvee meme si aucun constat n'avait ete produit. Valeurs ASCII, sans apostrophe, chacune
# incluse dans le constat qui la concerne.
MOTIF_PAGES = "pages epinglees"
MOTIF_PAGE_ABSENTE = "page epinglee absente ou non fichier"
MOTIF_PAGE_NON_DECLAREE = "page du disque non epinglee"
MOTIF_PAGE_VIDE = "page videe ou tronquee"
MOTIF_PAGE_ILLISIBLE = "page non decodable en UTF-8"
MOTIF_H1 = "titre de niveau 1 absent"
MOTIF_GARDE = "garde de cloture du harnais"

# --- `README.md` : l'occurrence destructive, ce qui l'encadre et ce qui doit rester (D-100) ---
# Formes de l'avertissement, lues dans le `README.md` au moment de l'ecriture (`D-19`) : un contrat de
# presence, jamais une exigence de style.
MOTS_AVERTISSEMENT = ("détruit", "irréversible")

# Le jeton de la commande de nettoyage de la base locale et les jetons des deux autres commandes de base
# du meme bloc plus la mention des sous-commandes acceptees en alias, **copies du `README.md` au moment de
# l'ecriture** : l'executeur les lit sur le disque, il ne les compose pas de memoire (`D-19`). Ce sont
# eux qui mecanisent la clause « aucune ligne existante n'est retiree » : la conservation de chaque jeton
# est **controlee**, jamais supposee.
INVOCATION_DESTRUCTIVE = "python fetcher.py db clear"
INVOCATIONS_CONSERVEES = (
    "python fetcher.py db status",
    "python fetcher.py db sync",
    "cache stats|fill|clear",
)

# Le renvoi exige dans le bloc de l'occurrence : la page qui documente la base locale, son mode hors-ligne
# et les gestes non destructifs.
RENVOI_BASE_LOCALE = "docs/base-locale.md"

# --- Lecteurs locaux ---
# Motifs de **lecture** seulement (le titre de niveau 1 d'une page), jamais des helpers partages : `D-12`
# ne porte que sur les helpers de `tests/conftest.py`, qui restent la seule source des fixtures de
# section, de normalisation et de scan de blocs.
MOTIF_TITRE = re.compile(r"^#\s+(?P<titre>\S.*)$", re.MULTILINE)
MOTIF_LIGNE_INDEX = re.compile(r"^\|\s*\[(?P<libelle>[^\]]+)\]\((?P<cible>[^)\s]+)\)\s*\|")

# --- Garde de cloture du harnais ---
# Racines dont un import signalerait un risque reel pour un module qui ne lit que des fichiers texte :
# ouvrir une base, lancer un processus, ouvrir une socket, joindre le reseau. Le controle porte sur le
# risque, jamais sur une liste blanche de modules produit a tenir a jour.
RACINES_INTERDITES = (
    "sqlite3",
    "subprocess",
    "socket",
    "multiprocessing",
    "ctypes",
    "webbrowser",
    "urllib",
    "requests",
    "http",
    "ftplib",
    "smtplib",
)

# Noms d'appel dont la presence signalerait une action destructive, l'execution du produit ou un calcul :
# `main` est le point d'entree du produit, `optimize_stuff` et `_run_optimize_and_redirect` declenchent le
# solveur (et donc l'ouverture de la base du depot), et les quatre derniers effacent des fichiers. Un
# module de documentation n'appelle rien de tout cela, et n'ouvre jamais une base pour la vider.
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"
APPELS_CALCUL_PRODUIT = ("optimize_stuff", "_run_optimize_and_redirect")


def _imports_du_module(arbre: ast.AST) -> set[str]:
    """Modules importes par le module controle, imports imbriques compris dans les fonctions."""
    importes: set[str] = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            importes.update(alias.name for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom) and noeud.module is not None:
            importes.add(noeud.module)
    return importes


def _appels_du_module(arbre: ast.AST) -> set[str]:
    """Noms appeles par le module controle, sous forme `nom` ou `attribut` terminal."""
    appeles: set[str] = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        if isinstance(noeud.func, ast.Attribute):
            appeles.add(noeud.func.attr)
        else:
            appeles.add(getattr(noeud.func, "id", ""))
    return appeles


# --- Constats de completude (fonctions pures de constats, D-13) ---


def _non_vides(texte: str) -> int:
    """Nombre de lignes non vides d'un texte : ce que le seuil de chaque page mesure."""
    return len([ligne for ligne in texte.splitlines() if ligne.strip()])


def problemes_pages_epinglees(racine: Path) -> list[str]:
    """Constats de la liste epinglee confrontee au disque, dans les deux sens (`GARD-03`, `D-95`).

    Trois lectures, aucune ecriture et aucun acces a la base :

    - chaque page **declaree** est confrontee au disque : chemin existant, fichier, texte decodable en
      UTF-8, un titre de niveau 1, et un nombre de lignes non vides au moins egal au seuil declare ;
    - la **decouverte du disque** (`docs/*.md`) est comparee a la liste declaree dans les deux sens : une
      page du disque non declaree est un constat, une page declaree absente du disque aussi ;
    - les deux fichiers de la racine sont verifies existants, fichiers et non vides, sans seuil de lignes.

    La racine est recue en argument, jamais lue d'une constante du module : le controle reste donc
    exercable sur une copie construite sous `tmp_path`, sans toucher au depot.
    """
    constats: list[str] = []
    declarees = {chemin for chemin, _ in PAGES_EPINGLEES}

    for chemin, seuil in PAGES_EPINGLEES:
        page = racine / chemin
        if not page.is_file():
            constats.append(
                f"{chemin} : {MOTIF_PAGE_ABSENTE} : {page.as_posix()} ; attendu un fichier livre sous "
                f"{racine.as_posix()} ({seuil} lignes non vides exigees, D-95)"
            )
            continue
        try:
            texte = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            constats.append(
                f"{chemin} : {MOTIF_PAGE_ILLISIBLE} : {page.as_posix()} ; attendu une page livree "
                f"decodable en UTF-8 strict, la liste epinglee etant confrontee au disque (D-95, D-11)"
            )
            continue
        if MOTIF_TITRE.search(texte) is None:
            constats.append(
                f"{chemin} : {MOTIF_H1} : aucun titre de niveau 1 dans {page.as_posix()} ; attendu un "
                f"titre de niveau 1, la page restant livree et atteignable (D-95)"
            )
        non_vides = _non_vides(texte)
        if non_vides < seuil:
            constats.append(
                f"{chemin} : {MOTIF_PAGE_VIDE} : {non_vides} ligne(s) non vide(s) dans "
                f"{page.as_posix()} ; attendu au moins {seuil} lignes non vides, le seuil etant le refus "
                f"du vidage et non une mesure de qualite (D-95)"
            )

    disque = {
        page.relative_to(racine).as_posix()
        for page in sorted((racine / DOSSIER_DOCS).glob("*.md"))
        if page.is_file()
    }
    for chemin in sorted(disque - declarees):
        constats.append(
            f"{chemin} : {MOTIF_PAGE_NON_DECLAREE} : page presente sous "
            f"{(racine / DOSSIER_DOCS).as_posix()} et absente de la liste epinglee ; attendu une entree "
            f"dans PAGES_EPINGLEES pour chaque page livree (D-95, D-14)"
        )
    for chemin in sorted(declarees - disque):
        constats.append(
            f"{chemin} : {MOTIF_PAGE_ABSENTE} : page declaree epinglee et absente du disque sous "
            f"{(racine / DOSSIER_DOCS).as_posix()} ; attendu chaque page epinglee presente sur disque, "
            f"la liste etant la source unique du contrat (D-95, D-14)"
        )

    for nom in PAGES_RACINE:
        page = racine / nom
        if not page.is_file():
            constats.append(
                f"{nom} : {MOTIF_PAGE_ABSENTE} : {page.as_posix()} ; attendu un fichier de documentation "
                f"de la racine du depot, verifie sans seuil de lignes (D-95)"
            )
            continue
        try:
            texte = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            constats.append(
                f"{nom} : {MOTIF_PAGE_ILLISIBLE} : {page.as_posix()} ; attendu un fichier de "
                f"documentation decodable en UTF-8 strict (D-95, D-11)"
            )
            continue
        if not texte.strip():
            constats.append(
                f"{nom} : {MOTIF_PAGE_VIDE} : 0 ligne non vide dans {page.as_posix()} ; attendu un "
                f"fichier de documentation non vide de la racine du depot (D-95)"
            )

    return constats


# --- Tests de la tranche verticale ---


def test_garde_de_cloture_du_harnais() -> None:
    """Le module n'ouvre aucune base, ne joint ni processus ni reseau, et n'execute jamais le produit.

    La propriete est verifiee sur le texte de ce module par `ast`, et **jamais** par une recherche de
    chaines : le module cite lui-meme les noms interdits dans ses messages, une recherche textuelle se
    detecterait elle-meme. Le controle porte sur le risque **reel** de ce module — lire des fichiers texte
    du depot — donc ni `sqlite3`, ni `subprocess`, ni `socket`, ni le reseau, et jamais l'execution du
    produit ni une suppression de fichier.

    Limite nommee : la garde est une demonstration **statique et indirecte**. Elle dit ce que ce module
    importe et appelle, pas ce qu'un autre chemin ferait ; et elle ne remplace pas la mesure d'empreinte
    de `.data/dofus.sqlite3`, prise avant et apres la suite entiere par le plan 06-04 (D-85, T-06-03-04).
    """
    source = RACINE_DEPOT / "tests" / Path(__file__).name
    arbre = ast.parse(source.read_text(encoding="utf-8"))
    importes = _imports_du_module(arbre)
    appeles = _appels_du_module(arbre)
    constats: list[str] = []

    racines = sorted(module for module in importes if module.split(".")[0] in RACINES_INTERDITES)
    if racines:
        constats.append(
            f"import(s) de base, de processus, de socket ou de reseau : {', '.join(racines)} ; attendu "
            f"aucun de ces imports dans un module de completude qui ne lit que des fichiers texte "
            f"(T-06-03-04, T-06-03-05)"
        )
    if APPEL_PRODUIT in appeles:
        constats.append(
            f"appel a {APPEL_PRODUIT}() dans le module de completude ; attendu un module qui lit des "
            f"fichiers texte et n'execute jamais le point d'entree du produit (T-06-03-05)"
        )
    calculs = sorted(set(APPELS_CALCUL_PRODUIT) & appeles)
    if calculs:
        constats.append(
            f"appel(s) de calcul du produit : {', '.join(calculs)} ; attendu aucun appel de calcul, "
            f"ces points d'entree ouvrant la base du depot (T-06-03-04, T-06-03-05)"
        )
    suppressions = sorted(set(APPELS_SUPPRESSION) & appeles)
    if suppressions:
        constats.append(
            f"appel(s) de suppression de fichier : {', '.join(suppressions)} ; attendu aucun appel "
            f"destructif dans un module qui ne fait que lire (D-104)"
        )

    assert not constats, (
        f"{MOTIF_GARDE} — constats : " + " ; ".join(constats) + " ; attendu un module de completude qui "
        f"lit des fichiers texte du depot sans ouvrir de base, sans joindre le reseau et sans executer le "
        f"produit (D-103, D-104)"
    )


def test_pages_epinglees_completes(docs_dir: Path) -> None:
    """Les huit pages epinglees et les deux fichiers de racine existent, et le disque est en egalite.

    Une seule assertion, tous constats accumules (`D-13`) : le disque et la **liste epinglee** du module
    sont en egalite dans les deux sens, chaque page declaree porte un titre de niveau 1 et au moins son
    seuil de lignes non vides. Le controle est le meme sur l'arbre livre et sur une copie, la racine
    etant recue en argument plutot que lue d'une constante.
    """
    constats = problemes_pages_epinglees(docs_dir.parent)
    assert not constats, (
        f"{MOTIF_PAGES} — constats : " + " ; ".join(constats) + " ; attendu les huit pages de `docs/` "
        f"presentes, non videes et en egalite avec la liste epinglee, plus les deux fichiers de la racine "
        f"(GARD-03, D-95)"
    )


def test_aucune_page_ne_peut_etre_videe(tmp_path: Path) -> None:
    """Une copie minimale (page tronquee, page absente) porte les deux constats attendus, hors du depot.

    C'est la forme la **moins invasive** de la preuve de morsure : la copie vit sous `tmp_path`, le depot
    n'est pas touche, et les deux constats sont exiges ensemble — une page declaree absente et une page
    videe. La mesure a un objet : sans seuil ni liste, ce controle serait vert sans rien controler.
    """
    racine = tmp_path
    (racine / DOSSIER_DOCS).mkdir()
    (racine / DOSSIER_DOCS / "glossaire.md").write_text(
        "# Glossaire\r\n", encoding="utf-8", newline=""
    )
    for nom in PAGES_RACINE:
        (racine / nom).write_text(
            "# Fichier de racine\r\n\r\nContenu non vide.\r\n", encoding="utf-8", newline=""
        )

    constats = problemes_pages_epinglees(racine)
    absents = [
        motif
        for motif in (MOTIF_PAGE_ABSENTE, MOTIF_PAGE_VIDE)
        if not any(motif in constat for constat in constats)
    ]
    assert not absents, (
        f"{MOTIF_PAGES} : constat(s) attendu(s) absent(s) de la copie de mesure : "
        f"{', '.join(absents) or 'aucun'} ; constats produits : " + " ; ".join(constats) + " ; attendu "
        f"les deux constats attendus sur une copie minimale construite sous {racine.as_posix()} "
        f"(GARD-03, D-95)"
    )
