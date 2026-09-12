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
epinglee du module confrontee au disque puis a l'index, le refus du vidage, l'**au plus une ligne par
cible** du tableau (que `problemes_index` ne peut pas voir, puisqu'il raisonne en ensembles) et le
**compte** des lignes d'index.

Les cinq constats de ce module forment le contrat `GARD-03` de la phase : deux pour la liste epinglee
confrontee au disque (page absente, page videe ou non indexee selon le cas) et pour le refus du vidage,
deux pour la couverture de l'index (page non indexee, cible hors de la liste) et un pour le compte. La
**couverture epinglee** de l'index est une **consequence** de l'egalite index <-> disque et de l'egalite
pages epinglees <-> disque : elle est gardee comme lecture de la **constante epinglee** (une seule source
de verite, `D-14`) plutot que comme seconde derivation du disque. Le module ne verifie ni le contenu
redactionnel des pages, ni leur rendu, ni le libelle des entrees d'index (`D-85`).

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

# Les deux pages livrees par cette phase, sujet du controle de la tache 3 : le controle verifie leur
# **appartenance** a `PAGES_EPINGLEES` et leur presence dans le tableau d'index, sans jamais recopier
# l'inventaire complet des pages — la liste epinglee reste la seule source de verite (`D-14`).
PAGES_DE_LA_PHASE = ("docs/depannage.md", "docs/glossaire.md")

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

# Motifs du controle de couverture de l'index (plan 06-03, tache 3) : les deux axes reellement neufs —
# la constante epinglee confrontee au tableau d'index, et le compte des lignes du tableau.
MOTIF_COUVERTURE_INDEX = "page livree non indexee"
MOTIF_INDEX_EN_TROP = "entree d index sans page epinglee"
MOTIF_NOMBRE_INDEX = "nombre de lignes d index"

# Familles de constat du controle du `README.md` (plan 06-03, tache 2) : trois constats distincts derives
# d'un meme motif de base (`MOTIF_README`), pour que la morsure chercher le motif et que le diagnostic
# nomme la famille — avertissement absent, renvoi absent, jeton de commande disparu.
FAMILLE_AVERTISSEMENT = "avertissement manquant"
FAMILLE_RENVOI = "renvoi non destructif manquant"
FAMILLE_DISPARITION = "commande de base disparue de la page"

# --- `README.md` : l'occurrence destructive, ce qui l'encadre et ce qui doit rester (D-100) ---
# Motif de morsure du controle du `README.md`, porte par une constante comme les precedents et inclus
# dans **chacun** des trois constats (avertissement, renvoi, jeton disparu).
MOTIF_README = "invitation a detruire les donnees"

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


# --- `README.md` : constats du controle D-100 (fonction pure, D-13) ---


def _blocs_contigus(texte: str) -> list[tuple[int, list[str]]]:
    """Blocs de lignes contigus d'un texte : `(numero de la premiere ligne, lignes)`, lignes vides exclues.

    Un bloc est une suite de lignes non vides : une commande et son avertissement restent donc dans le
    **meme** bloc tant qu'aucune ligne vide ne les separe, et une phrase posee trois paragraphes plus bas
    ne compte pas comme l'encadrement du bloc (D-100).
    """
    blocs: list[tuple[int, list[str]]] = []
    courant: list[str] = []
    debut = 1
    for numero, ligne in enumerate(texte.splitlines(), start=1):
        if ligne.strip():
            if not courant:
                debut = numero
            courant.append(ligne)
            continue
        if courant:
            blocs.append((debut, courant))
            courant = []
    if courant:
        blocs.append((debut, courant))
    return blocs


def problemes_readme(texte: str, invocation: str, renvoi: str = RENVOI_BASE_LOCALE) -> list[str]:
    """Constats du `README.md` : l'occurrence destructive est encadree, et rien n'a disparu (`D-100`).

    Fonction **pure** : elle recoit le texte (jamais le disque), ne lit aucun fichier, n'ecrit rien et
    n'execute aucune commande. Trois lectures, un constat par famille (`D-13`) :

    - pour **chaque** bloc de lignes contigues portant `invocation` — jamais seulement le premier — au
      moins un mot de `MOTS_AVERTISSEMENT` doit s'y trouver, sans quoi la famille est celle de
      l'avertissement manquant ;
    - le renvoi `renvoi` doit se trouver dans ce **meme** bloc : la commande perd sa forme d'invitation
      parce qu'elle voisine ce qui manquait, un renvoi pose ailleurs ne l'encadre pas ;
    - **chaque** jeton de `INVOCATIONS_CONSERVEES`, le jeton destructif compris, doit apparaitre au moins
      une fois dans le texte : la conservation des commandes de base est un controle, jamais une
      supposition, et le constat nomme le jeton disparu.

    Retirer l'occurrence destructive est donc un constat au meme titre que retirer son avertissement ou
    son renvoi : la ligne reste documentee, elle perd sa forme d'invitation (decision `D-100` ecrite dans
    la docstring du module). Ce controle ne teste jamais la commande, ne l'execute pas, et n'ouvre rien
    sous `.data/` : il porte sur le **texte** du `README.md` et rien d'autre (`D-104`).
    """
    constats: list[str] = []

    for debut, lignes in _blocs_contigus(texte):
        bloc = "\n".join(lignes)
        if invocation not in bloc:
            continue
        fin = debut + len(lignes) - 1
        if not any(mot in bloc for mot in MOTS_AVERTISSEMENT):
            constats.append(
                f"README.md : {MOTIF_README} — {FAMILLE_AVERTISSEMENT} : le bloc des lignes "
                f"{debut}..{fin} porte « {invocation} » sans aucun mot d'avertissement ; attendu l'un de "
                f"{', '.join(MOTS_AVERTISSEMENT)}, la commande detruisant la base locale (D-100)"
            )
        if renvoi not in bloc:
            constats.append(
                f"README.md : {MOTIF_README} — {FAMILLE_RENVOI} : le bloc des lignes {debut}..{fin} ne "
                f"renvoie pas vers « {renvoi} » ; attendu ce renvoi dans le meme bloc que "
                f"« {invocation} », la page documentant la base locale et ses gestes non destructifs "
                f"(D-100)"
            )

    for jeton in (invocation, *INVOCATIONS_CONSERVEES):
        if jeton not in texte:
            constats.append(
                f"README.md : {MOTIF_README} — {FAMILLE_DISPARITION} : le jeton « {jeton} » n'apparait "
                f"plus dans la page ; attendu que chaque commande de base reste documentee, la ligne "
                f"etant encadree et jamais supprimee (D-100)"
            )

    return constats


# --- Couverture de l'index : la constante epinglee et le compte (fonction pure de constats, D-13) ---


def _pages_contenu_epinglees() -> set[str]:
    """Cibles attendues du tableau d'index : les pages epinglees de `docs/`, sans le sommaire lui-meme.

    Le sommaire ne s'auto-liste pas et ne peut donc pas etre sa propre cible : la cible attendue de
    chaque page epinglee est son chemin **relatif a `docs/`**, tel qu'ecrit dans le tableau.
    """
    return {
        Path(chemin).relative_to(DOSSIER_DOCS).as_posix()
        for chemin, _ in PAGES_EPINGLEES
        if Path(chemin).name != SOMMAIRE
    }


def _corps_index(texte: str) -> str:
    """Corps du tableau du titre `## Index`, jusqu'au titre de niveau 2 suivant (ou la fin du fichier).

    Lecteur **local** du module (motif de lecture, jamais un helper partage) : `D-12` ne porte que sur
    les helpers de `tests/conftest.py`, dont la fixture `section` reste la seule source au niveau des
    tests.
    """
    debut = texte.find(TITRE_INDEX)
    if debut == -1:
        return ""
    suite = texte[debut + len(TITRE_INDEX) :]
    suivant = re.search(r"^##\s", suite, re.MULTILINE)
    return suite if suivant is None else suite[: suivant.start()]


def problemes_couverture_index(docs_dir: Path) -> list[str]:
    """Constats de couverture du tableau d'index, sur les **deux axes neufs** (`GARD-03`, `D-95`, `D-96`).

    Non-duplication ecrite (`D-12`, `D-14`) : ce controle lit l'index pour la **couverture de la
    constante epinglee** et pour le **compte**, et laisse `tests/test_docs_structure.py` tenir l'egalite
    index <-> **disque** (dans les deux sens), le titre de niveau 1 et l'unicite des libelles. La
    couverture epinglee est une **consequence** de l'egalite index <-> disque et de l'egalite pages
    epinglees <-> disque (tache 1) : elle est gardee comme lecture de la **constante epinglee** (une seule
    source de verite) plutot que comme seconde derivation du disque, et ce controle ajoute donc les deux
    choses qu'aucune garde livree ne porte — **au plus une** ligne par cible (`problemes_index` raisonne
    en ensembles, donc une ligne dupliquee lui echappe) et le **compte** des lignes.

    Trois lectures, un constat par motif :

    - une page de contenu epinglee sans ligne d'index est un constat de `MOTIF_COUVERTURE_INDEX` ;
    - une cible du tableau qui n'est pas une page epinglee est un constat de `MOTIF_INDEX_EN_TROP` ;
    - une cible portee par plusieurs lignes est un constat de `MOTIF_COUVERTURE_INDEX` (elle et les
      autres cibles ne sont pas disjointes) ;
    - le nombre de lignes du tableau doit egaler le nombre de pages de contenu epinglees, sans quoi le
      constat de `MOTIF_NOMBRE_INDEX` **nomme les deux nombres**.

    Ce controle ne verifie ni le libelle des entrees, ni le titre de niveau 1 du sommaire, ni la prose de
    la page : ce sont les controles de la phase 1, et le module ne les reprend pas (`D-12`).
    """
    sommaire = docs_dir / SOMMAIRE
    if not sommaire.is_file():
        return [
            f"{DOSSIER_DOCS}/{SOMMAIRE} : {MOTIF_COUVERTURE_INDEX} : {sommaire.as_posix()} absent ; "
            f"attendu le sommaire portant le tableau « {TITRE_INDEX} », la couverture etant lue sur lui "
            f"(GARD-03, D-95)"
        ]
    try:
        texte = sommaire.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [
            f"{DOSSIER_DOCS}/{SOMMAIRE} : {MOTIF_COUVERTURE_INDEX} : {sommaire.as_posix()} non decodable "
            f"en UTF-8 strict ; attendu un sommaire lisible, la couverture etant lue sur son texte "
            f"(GARD-03, D-11)"
        ]

    corps = _corps_index(texte)
    if not corps.strip():
        return [
            f"{DOSSIER_DOCS}/{SOMMAIRE} : {MOTIF_COUVERTURE_INDEX} : le titre « {TITRE_INDEX} » est absent "
            f"de {sommaire.as_posix()} ; attendu le tableau d'index ou sont lues les cibles des pages "
            f"livrees (GARD-03, D-95)"
        ]

    lignes = [ligne for ligne in corps.splitlines() if MOTIF_LIGNE_INDEX.match(ligne)]
    cibles = [MOTIF_LIGNE_INDEX.match(ligne).group("cible") for ligne in lignes]
    uniques = set(cibles)
    attendues = _pages_contenu_epinglees()
    constats: list[str] = []

    for cible in sorted(attendues - uniques):
        constats.append(
            f"{DOSSIER_DOCS}/{SOMMAIRE} : {MOTIF_COUVERTURE_INDEX} : la page epinglee "
            f"{DOSSIER_DOCS}/{cible} n'est la cible d'aucune ligne du tableau « {TITRE_INDEX} » ; attendu "
            f"une ligne d'index pointant vers {cible} pour chaque page de contenu epinglee (D-95, D-96)"
        )
    for cible in sorted(uniques - attendues):
        constats.append(
            f"{DOSSIER_DOCS}/{SOMMAIRE} : {MOTIF_INDEX_EN_TROP} : la cible « {cible} » du tableau "
            f"« {TITRE_INDEX} » n'est pas une page epinglee ; attendu chaque cible du tableau presente "
            f"dans PAGES_EPINGLEES, la constante etant la source unique du contrat (D-95, D-14)"
        )
    for cible in sorted({cible for cible in cibles if cibles.count(cible) > 1}):
        constats.append(
            f"{DOSSIER_DOCS}/{SOMMAIRE} : {MOTIF_COUVERTURE_INDEX} : la cible « {cible} » est portee par "
            f"{cibles.count(cible)} lignes du tableau « {TITRE_INDEX} » ; attendu au plus une ligne par "
            f"cible, l'egalite d'ensembles de la phase 1 ne voyant pas une ligne dupliquee (D-95, D-96)"
        )
    if len(lignes) != len(attendues):
        constats.append(
            f"{DOSSIER_DOCS}/{SOMMAIRE} : {MOTIF_NOMBRE_INDEX} : le tableau « {TITRE_INDEX} » porte "
            f"{len(lignes)} ligne(s) ; attendu {len(attendues)} pages de contenu epinglees, autant de "
            f"lignes que de pages livrees (D-95, D-96)"
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


# --- Controle du `README.md` (plan 06-03, tache 2 : D-100) ---


def test_readme_n_invite_pas_a_detruire(docs_dir: Path) -> None:
    """Le bloc qui porte la commande de nettoyage avertit sur elle et renvoie vers la page de la base.

    Une seule assertion, tous constats accumules (`D-13`) : le controle lit le `README.md` **livre** et
    ne le corrige pas (`T-06-03-05`). Trois lectures sont exercees ensemble — un mot d'avertissement et
    le renvoi `docs/base-locale.md` dans le bloc de **chaque** occurrence de `INVOCATION_DESTRUCTIVE`, et
    la presence de **chaque** jeton de `INVOCATIONS_CONSERVEES`, le jeton destructif compris : la
    conservation des commandes de base est un constat, jamais une supposition.

    Un fichier illisible est un constat nomme, jamais un vert silencieux : `read_text` est enferme, et
    l'echec de decodage produit un constat au lieu d'une exception. Le controle n'ouvre rien sous
    `.data/`, ne teste pas la commande et ne l'execute pas (`D-104`).
    """
    chemin = docs_dir.parent / "README.md"
    if not chemin.is_file():
        raise AssertionError(
            f"README.md : fichier introuvable ({chemin.as_posix()}) ; attendu le fichier de la racine du "
            f"depot dont le bloc des commandes de base est encadre (D-100)"
        )

    try:
        texte = chemin.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        constats = [
            f"README.md : {MOTIF_README} — fichier non decodable en UTF-8 strict : "
            f"{chemin.as_posix()} ; attendu un fichier de documentation lisible, le controle portant sur "
            f"son texte (D-100, D-11)"
        ]
    else:
        constats = problemes_readme(texte, INVOCATION_DESTRUCTIVE)

    assert not constats, (
        f"README.md : constats sur l'encadrement de la commande de nettoyage : " + " ; ".join(constats)
        + " ; attendu la commande de nettoyage de la base locale encadree, dans son bloc, par un mot "
        f"d'avertissement ({', '.join(MOTS_AVERTISSEMENT)}) et le renvoi vers {RENVOI_BASE_LOCALE}, "
        f"chaque jeton des commandes de base restant documente (D-100)"
    )


def test_le_controle_du_readme_mord_sur_un_texte_synthetique() -> None:
    """Les trois familles de constats sont exercees sur des textes synthetiques, hors du depot.

    La preuve de morsure est **hors du depot** et immediate : trois textes construits ici portent un meme
    inventaire de commandes, prive successivement de l'avertissement, du renvoi, puis de **tous** les
    jetons conserves. Le troisieme cas est celui qui interdit un faux temoin : un `README.md` qui ne
    porterait plus aucune occurrence de la commande destructive serait declare vert par un controle qui
    ne chercherait que des blocs — ici, le jeton manquant est un constat (`D-100`).

    La mesure a un objet : `INVOCATION_DESTRUCTIVE` non vide est exige avant l'application, sans quoi les
    textes construits ne mesureraient rien (`D-84`, lecon de la phase 5).
    """
    assert INVOCATION_DESTRUCTIVE, (
        f"README.md : {MOTIF_README} — la mesure n'a aucun objet : `INVOCATION_DESTRUCTIVE` est vide ; "
        f"attendu le jeton de la commande de nettoyage, lu dans le `README.md` a l'ecriture (D-19)"
    )

    avertissement = "ATTENTION : cette commande détruit la base locale, l'opération est irréversible."
    renvoi = f"Le mode hors-ligne et les gestes non destructifs sont dans {RENVOI_BASE_LOCALE}."
    inventaire = "\n".join((INVOCATION_DESTRUCTIVE, *INVOCATIONS_CONSERVEES))

    familles = (
        (FAMILLE_AVERTISSEMENT, f"{inventaire}\n{renvoi}\n"),
        (FAMILLE_RENVOI, f"{inventaire}\n{avertissement}\n"),
        (FAMILLE_DISPARITION, f"{avertissement}\n{renvoi}\n"),
    )
    absentes = [
        famille
        for famille, texte in familles
        if not any(
            famille in constat
            for constat in problemes_readme(texte, INVOCATION_DESTRUCTIVE)
        )
    ]
    assert not absentes, (
        f"README.md : {MOTIF_README} — famille(s) de constat absente(s) sur les textes synthetiques : "
        f"{', '.join(absentes) or 'aucune'} ; attendu les trois familles (avertissement manquant, renvoi "
        f"manquant, jeton disparu) sur trois textes prives successivement de l'avertissement, du renvoi "
        f"et de tous les jetons conserves (D-100, D-84)"
    )


# --- Cloture de completude : la couverture de l'index et son compte (plan 06-03, tache 3) ---


def test_couverture_de_l_index(docs_dir: Path, section) -> None:
    """Chaque page epinglee est une cible du tableau d'index, et aucune cible n'est hors de la liste.

    Une seule assertion, tous constats accumules (`D-13`) : les deux axes neufs du controle sont exerces
    ensemble — l'egalite d'ensembles **dans les deux sens** entre les cibles du tableau `## Index` et les
    pages de contenu de `PAGES_EPINGLEES`, avec au plus une ligne par cible. La fixture partagee `section`
    localise d'abord le tableau : la mesure a donc un objet, et le helper n'est jamais recopie (`D-12`).
    """
    texte = (docs_dir / SOMMAIRE).read_text(encoding="utf-8")
    section(texte, TITRE_INDEX, SOMMAIRE)
    constats = problemes_couverture_index(docs_dir)

    assert not constats, (
        f"{MOTIF_COUVERTURE_INDEX} — constats de couverture du tableau « {TITRE_INDEX} » : "
        + " ; ".join(constats)
        + f" ; attendu chaque page de contenu epinglee atteignable par une ligne d'index unique, et "
        f"aucune cible hors de PAGES_EPINGLEES (GARD-03, D-95, D-96)"
    )


def test_les_deux_pages_de_la_phase_sont_epinglees_et_indexees(docs_dir: Path, section) -> None:
    """Les deux pages de la phase sont epinglees **et** indexees, sans seconde enumeration de l'inventaire.

    Les chemins viennent de `PAGES_DE_LA_PHASE`, et leur appartenance est derivee de `PAGES_EPINGLEES` :
    aucune liste de pages n'est recopiee, donc aucune seconde source de verite (`D-14`). Le controle
    exerce exactement ce que le plan ferme — la page livree par cette phase est du contrat **et** de
    l'index — sans rejouer l'egalite index <-> disque de la phase 1 (`D-12`).
    """
    texte = (docs_dir / SOMMAIRE).read_text(encoding="utf-8")
    corps = section(texte, TITRE_INDEX, SOMMAIRE)
    cibles = {
        trouve.group("cible")
        for ligne in corps.splitlines()
        if (trouve := MOTIF_LIGNE_INDEX.match(ligne)) is not None
    }
    declarees = {chemin for chemin, _ in PAGES_EPINGLEES}

    constats: list[str] = []
    for chemin in PAGES_DE_LA_PHASE:
        cible = Path(chemin).relative_to(DOSSIER_DOCS).as_posix()
        if chemin not in declarees:
            constats.append(
                f"{chemin} : {MOTIF_COUVERTURE_INDEX} : la page livree par cette phase n'est pas une page "
                f"epinglee ; attendu une entree dans PAGES_EPINGLEES, la constante etant la source unique "
                f"du contrat (GARD-03, D-95, D-14)"
            )
        if cible not in cibles:
            constats.append(
                f"{chemin} : {MOTIF_COUVERTURE_INDEX} : la page livree par cette phase n'est la cible "
                f"d'aucune ligne du tableau « {TITRE_INDEX} » ; attendu une ligne d'index pointant vers "
                f"{cible} (GARD-03, D-95, D-96)"
            )

    assert not constats, (
        f"{MOTIF_COUVERTURE_INDEX} — constats sur les pages de la phase : " + " ; ".join(constats)
        + f" ; attendu {', '.join(PAGES_DE_LA_PHASE)} epinglees et atteignables depuis "
        f"« {TITRE_INDEX} » du sommaire, les chemins etant derives des constantes du module "
        f"(GARD-03, D-95)"
    )


def test_le_nombre_d_entrees_d_index_est_le_nombre_de_pages(docs_dir: Path, section) -> None:
    """Le tableau d'index porte autant de lignes que de pages de contenu epinglees.

    Le point (b) est exerce **seul**, isole de l'egalite d'ensembles : le constat de compte est donc
    diagnosticable sans lire les autres, et il nomme les deux nombres. Le tableau est d'abord localise
    par la fixture partagee `section`, sans quoi la mesure n'aurait pas d'objet (`D-12`).
    """
    texte = (docs_dir / SOMMAIRE).read_text(encoding="utf-8")
    section(texte, TITRE_INDEX, SOMMAIRE)
    constats = [
        constat
        for constat in problemes_couverture_index(docs_dir)
        if MOTIF_NOMBRE_INDEX in constat
    ]

    assert not constats, (
        f"{MOTIF_NOMBRE_INDEX} — constats de compte du tableau « {TITRE_INDEX} » : " + " ; ".join(constats)
        + f" ; attendu autant de lignes d'index que de pages de contenu epinglees (GARD-03, D-95)"
    )
