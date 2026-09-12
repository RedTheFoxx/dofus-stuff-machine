"""Ancrage de la page `docs/glossaire.md` et du parcours conseille de `docs/sommaire.md`.

Le contrat va de la page vers le depot (D-19, D-94) : le glossaire ne definit que ce qu'aucune page
livree ne definit, et **renvoie** vers la page qui definit deja le terme partout ailleurs (D-17). Chaque
entree est confrontee a son **employeur** — le fichier qui emploie reellement le terme — et chaque renvoi
de definition est confronte a sa **cible**, resolue depuis `docs/`. Le contrat vit dans la constante
`TERMES_GLOSSAIRE` (D-14) : les libelles lus dans la page et les termes declares y sont en **egalite
d'ensembles dans les deux sens**, un terme de la page non declare comme un terme declare absent de la
page etant un constat portant son propre motif.

Aucun serveur n'est lance, aucune socket n'est ouverte, `main()` n'est jamais execute, le solveur n'est
jamais lance et rien n'est ecrit sous `.data/` : ce module n'ouvre **aucune** base et n'instancie
**aucune** application, il ne lit que des fichiers texte de l'arbre du depot (D-103, D-104). La garde de
cloture ne porte donc **pas** le resserrement `data_dir` de la phase 5 : un module qui n'ouvre aucune base
n'a rien a y resserrer, et une garde qui controlerait un risque inexistant serait du bruit.

Limites nommees (D-85) :

- la prose des definitions n'est pas verifiee : les constats portent sur les libelles, leur ordre, leur
  employeur, leur renvoi et la forme de la page, jamais sur la clarte ou l'exactitude de la redaction ;
- la comparaison d'emploi est une **appartenance de sous-chaine** sur le texte normalise du fichier
  employeur : un terme qui serait contenu dans un autre mot passerait (mesure : `jet` est contenu dans
  `objets`). La limite est ecrite ici plutot que masquee, et c'est l'egalite d'ensembles libelles <->
  `TERMES_GLOSSAIRE` qui porte la fidelite du contrat ;
- le tri est celui de la normalisation `D-11` (accents, casse, entites, espaces), pas une collation
  linguistique : l'ordre de l'affichage accentue peut differer de l'ordre normalise, et c'est l'ordre
  normalise qui fait foi ;
- l'assertion de fins de ligne CRLF depend de `core.autocrlf` du poste et n'est presentee comme portable
  pour aucun autre reglage (AR-5) ;
- l'ordre de lecture du parcours conseille du sommaire est **libre par decision de plan** : le controle
  exige une permutation des libelles d'index, jamais un ordre donne ;
- le vocabulaire de harnais n'apparait ni dans les pages livrees ni dans `dofus_stuff/**` (mesure
  `06-RESEARCH.md` § B) : le definir exposerait au lecteur des mots qu'il ne rencontrera jamais a l'ecran,
  et cette absence est controlee par une liste, jamais par une relecture (D-19) ;
- ce module n'ouvre aucune base et ne rend aucun ecran : les modes de provenance du plan 06-01 n'ont pas
  d'equivalent ici, et cette absence est ecrite, jamais silencieuse.
"""

import ast
import re
from pathlib import Path

import pytest

RACINE_DEPOT = Path(__file__).resolve().parents[1]

PAGE = "glossaire.md"
SOMMAIRE = "sommaire.md"
TITRE_TERMES = "## Les termes"
TITRE_SOURCE = "## Source de vérité"
TITRE_PARCOURS = "## Parcours conseillé"
TITRE_INDEX = "## Index"
LIEN_RETOUR = "[Retour au sommaire](sommaire.md)"

# Le contrat du glossaire (D-14) : (terme, fichier employeur, page qui definit deja le terme ou None).
# `None` dit que le glossaire est le **premier** a definir le terme — aucune page livree ne le definit.
# L'ordre de cette constante est celui de la forme normalisee des libelles (D-11), comme la page.
TERMES_GLOSSAIRE: tuple[tuple[str, str, str | None], ...] = (
    ("base locale", "dofus_stuff/cli.py", "base-locale.md"),
    ("bouclier", "dofus_stuff/model/slots.py", "parcours-simplifie.md"),
    ("catégorie", "dofus_stuff/cli.py", "base-locale.md"),
    ("cible", "dofus_stuff/cli.py", "wizard-avance.md"),
    ("exo", "dofus_stuff/model/solver_spec.py", "parcours-simplifie.md"),
    ("familier", "dofus_stuff/model/slots.py", "parcours-simplifie.md"),
    ("heuristique", "dofus_stuff/optimize/score.py", "parcours-simplifie.md"),
    ("ID Ankama", "dofus_stuff/cli.py", "cli.md"),
    ("index", "docs/sommaire.md", None),
    ("jet", "dofus_stuff/cli.py", "wizard-avance.md"),
    ("ligne de statut", "docs/parcours-simplifie.md", "parcours-simplifie.md"),
    ("mode hors-ligne", "docs/base-locale.md", "base-locale.md"),
    ("palier", "dofus_stuff/model/solver_spec.py", "parcours-simplifie.md"),
    ("panoplie", "dofus_stuff/catalog.py", "base-locale.md"),
    ("parcours conseillé", "docs/sommaire.md", None),
    ("poids", "dofus_stuff/cli.py", "wizard-avance.md"),
    ("prysmaradite", "dofus_stuff/cli.py", "parcours-simplifie.md"),
    ("sauvegarde locale", "dofus_stuff/web/static/js/terminal.js", "parcours-simplifie.md"),
    ("score", "dofus_stuff/optimize/score.py", "parcours-simplifie.md"),
    ("slot", "dofus_stuff/web/optimize_wizard.py", "wizard-avance.md"),
    ("solveur", "dofus_stuff/optimize/cpsat.py", "wizard-avance.md"),
    ("sommaire", "docs/sommaire.md", None),
    ("source de vérité", "docs/base-locale.md", None),
    ("stuff", "dofus_stuff/cli.py", None),
    ("synchronisation", "dofus_stuff/cli.py", "base-locale.md"),
    ("trophée", "dofus_stuff/model/slots.py", "wizard-avance.md"),
    ("wizard", "dofus_stuff/web/optimize_wizard.py", "wizard-avance.md"),
)

# Vocabulaire de harnais et de planification : mesure (`06-RESEARCH.md` § B), zero occurrence dans les
# pages livrees comme dans `dofus_stuff/**`. Le definir exposerait au lecteur des mots qu'il ne
# rencontrera jamais a l'ecran (D-19) : ces libelles ne peuvent donc pas etre des entrees du glossaire.
TERMES_INTERDITS = ("page épinglée", "renvoi", "ancrage")

# Motifs de constat, portes par le module et **jamais** ecrits en clair dans une ligne d'assertion :
# pytest reproduit la ligne source de l'`assert`, une valeur en clair y serait trouvee meme sans constat
# produit (regle posee au plan 03-03, tenue ici sur tous les tests). Valeurs ASCII, sans apostrophe.
MOTIF_TERMES = "termes du glossaire"
MOTIF_TERME_NON_DECLARE = "terme cite non declare"
MOTIF_TERME_ABSENT = "terme declare absent de la page"
MOTIF_TRI = "ordre des termes"
MOTIF_DOUBLON = "terme duplique"
MOTIF_EMPLOYEUR = "terme non employe par le fichier cite"
MOTIF_RENVOI_MANQUANT = "renvoi de definition manquant"
MOTIF_TERME_INTERDIT = "terme hors du vocabulaire du produit"
MOTIF_PARCOURS = "parcours conseille"
MOTIF_PARCOURS_LIEN = "parcours conseille en liens"
MOTIF_VOLATILES = "valeur volatile"
MOTIF_CRLF = "fins de ligne"
MOTIF_SOURCE = "chemin de source absent"
MOTIF_FERMETURE = "ligne de fermeture de la page"
MOTIF_GARDE = "garde de cloture du harnais"

# Lecteurs locaux du module (motifs de lecture, jamais des helpers partages : D-12 ne porte que sur les
# helpers de `tests/conftest.py`). `MOTIF_LIGNE_TERME` lit la **premiere cellule** d'une ligne de
# tableau, c'est-a-dire la forme extractible du terme.
MOTIF_LIGNE_TERME = re.compile(r"^\|\s*`(?P<terme>[^`]+)`\s*\|(?P<reste>.*)\|\s*$")
MOTIF_LIEN_MARKDOWN = re.compile(r"\[[^\]]*\]\((?P<cible>[^)\s]+)\)")
MOTIF_CHEMIN_CITE = re.compile(r"`(?P<chemin>[^`]+)`")
MOTIF_ENTREE_NUMEROTEE = re.compile(r"^\s*\d+\.\s+(?P<libelle>.+?)\s*$", re.MULTILINE)
MOTIF_LIGNE_INDEX = re.compile(
    r"^\|\s*\[(?P<libelle>[^\]]*)\]\((?P<cible>[^)\s]+)\)\s*\|", re.MULTILINE
)

# Les deux refus de D-73 / D-75 : une valeur qui change d'un poste ou d'une execution a l'autre ne
# decrit pas le produit et ne doit pas etre epinglee dans la page.
MOTIF_VOLATILE = re.compile(r"\d{4,}")
MOTIF_CHEMIN_POSTE = re.compile(r"[A-Za-z]:[\\/]")

BOM = b"\xef\xbb\xbf"

# Garde de cloture du harnais, **reecrite** pour ce module (jamais recopiee d'un autre plan) : le risque
# d'ici n'est ni la base, ni la synchronisation, ni une confirmation postee — ce module n'ouvre aucune
# base et n'instancie aucune application — mais l'execution du produit, le lancement d'un processus, une
# socket, le reseau et la suppression d'un fichier.
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
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"
APPELS_CALCUL_PRODUIT = ("optimize_stuff", "_run_optimize_and_redirect")


def _texte_page(docs_dir: Path, nom: str) -> str | None:
    """Texte d'une page de `docs/`, ou None si elle est absente ou non decodable (D-13, D-11)."""
    chemin = docs_dir / nom
    if not chemin.is_file():
        return None
    try:
        return chemin.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def _lignes_de_termes(texte: str) -> list[tuple[str, str]]:
    """Couples (terme, reste de la ligne) des entrees du tableau de `TITRE_TERMES`.

    Le lecteur suit le seul titre de niveau 2 du glossaire et s'arrete au titre suivant : un tableau
    d'une autre section ne peut pas devenir une entree par accident. Un titre absent rend une liste
    vide, donc des constats nommes, jamais une exception (D-13).
    """
    entrees: list[tuple[str, str]] = []
    dans_section = False
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            dans_section = ligne.strip() == TITRE_TERMES
            continue
        if not dans_section:
            continue
        trouve = MOTIF_LIGNE_TERME.match(ligne)
        if trouve:
            entrees.append((trouve.group("terme"), trouve.group("reste")))
    return entrees


def _cellules(reste: str) -> list[str]:
    """Cellules suivant celle du terme : definition, employeur, page de definition."""
    return [cellule.strip() for cellule in reste.split("|")]


def _chemin_cite(cellule: str) -> str | None:
    """Premier chemin entre accents graves d'une cellule, ou None s'il n'y en a pas."""
    trouve = MOTIF_CHEMIN_CITE.search(cellule)
    return trouve.group("chemin") if trouve else None


def problemes_glossaire(docs_dir: Path, normalize) -> list[str]:
    """Constats sur les entrees du glossaire : libelles, ordre, employeur, renvoi, vocabulaire.

    Le controle va de la page vers le depot : il lit les libelles du tableau de `TITRE_TERMES` et les
    confronte a `TERMES_GLOSSAIRE` (D-14) **dans les deux sens**, puis, pour chaque terme declare, il
    exige que le fichier employeur existe depuis la racine du depot, que le terme y soit present apres
    normalisation (D-11, D-19) et que la ligne porte le renvoi exige quand une page livree definit deja
    le terme (D-17). Chaque constat nomme le terme, la valeur attendue et le fichier ou la page (D-13).
    """
    texte = _texte_page(docs_dir, PAGE)
    if texte is None:
        return [
            f"{PAGE} : {MOTIF_TERMES} — page absente : {(docs_dir / PAGE).as_posix()} ; attendu la page "
            f"unique du vocabulaire du produit et de la documentation (D-94)"
        ]

    constats: list[str] = []
    lignes = texte.splitlines()
    titres = [ligne.strip() for ligne in lignes if ligne.strip() == TITRE_TERMES]
    if len(titres) != 1:
        constats.append(
            f"{PAGE} : {MOTIF_TERMES} — {len(titres)} titre(s) « {TITRE_TERMES} » ; attendu un unique "
            f"titre de niveau 2 portant le tableau des termes (D-94)"
        )

    entrees = _lignes_de_termes(texte)
    declarees = {normalize(terme) for terme, _employeur, _page in TERMES_GLOSSAIRE}
    interdits = {normalize(terme) for terme in TERMES_INTERDITS}
    lues: set[str] = set()
    precedente_brute: str | None = None
    precedente_cle: str | None = None

    for terme, reste in entrees:
        cle = normalize(terme)

        if cle in lues:
            constats.append(
                f"{PAGE} : {MOTIF_DOUBLON} — « {terme} » ; attendu un libelle unique par terme, deux "
                f"termes egaux apres normalisation etant un constat (D-11, D-94)"
            )
        else:
            lues.add(cle)

        if precedente_cle is not None and cle <= precedente_cle:
            constats.append(
                f"{PAGE} : {MOTIF_TRI} — « {terme} » est place apres « {precedente_brute} » ; attendu la "
                f"suite des libelles normalises strictement croissante, la normalisation D-11 faisant foi "
                f"(D-94)"
            )
        precedente_brute, precedente_cle = terme, cle

        if cle in interdits:
            constats.append(
                f"{PAGE} : {MOTIF_TERME_INTERDIT} — « {terme} » appartient au vocabulaire de "
                f"planification, absent des pages livrees et de dofus_stuff/ ; attendu un terme du "
                f"produit ou de la documentation (D-19)"
            )

        declare = next(
            (entree for entree in TERMES_GLOSSAIRE if normalize(entree[0]) == cle), None
        )
        if declare is None:
            constats.append(
                f"{PAGE} : {MOTIF_TERME_NON_DECLARE} — « {terme} » ; attendu une entree de "
                f"TERMES_GLOSSAIRE ({len(TERMES_GLOSSAIRE)} termes declares) pour chaque ligne du "
                f"tableau (D-94)"
            )
            continue

        _libelle, employeur, page_definition = declare
        cellules = _cellules(reste)
        if len(cellules) != 3:
            constats.append(
                f"{PAGE} : {MOTIF_TERMES} — la ligne de « {terme} » porte {len(cellules) + 1} cellules ; "
                f"attendu quatre colonnes : terme, definition, employeur, page qui definit deja (D-94)"
            )
            continue

        cite = _chemin_cite(cellules[1])
        if cite != employeur:
            constats.append(
                f"{PAGE} : {MOTIF_EMPLOYEUR} — la ligne de « {terme} » cite « {cite} » ; attendu "
                f"l'employeur declare « {employeur} » (D-19)"
            )

        chemin = RACINE_DEPOT / employeur
        if not chemin.is_file():
            constats.append(
                f"{PAGE} : {MOTIF_EMPLOYEUR} — le fichier employeur « {employeur} » de « {terme} » est "
                f"absent de {RACINE_DEPOT.as_posix()} ; attendu un chemin existant depuis la racine du "
                f"depot (D-19)"
            )
        elif cle not in normalize(chemin.read_text(encoding="utf-8")):
            constats.append(
                f"{PAGE} : {MOTIF_EMPLOYEUR} — « {terme} » n'est pas employe par « {employeur} » ; "
                f"attendu le terme present dans le texte normalise de {employeur} (D-19)"
            )

        cibles = [trouve.group("cible") for trouve in MOTIF_LIEN_MARKDOWN.finditer(cellules[2])]
        if page_definition is None:
            if cibles:
                constats.append(
                    f"{PAGE} : {MOTIF_RENVOI_MANQUANT} — la ligne de « {terme} » renvoie vers "
                    f"« {', '.join(cibles)} » alors qu'aucune page livree ne definit ce terme ; attendu un "
                    f"tiret, le glossaire etant le premier a le definir (D-17)"
                )
        else:
            if page_definition not in cibles:
                constats.append(
                    f"{PAGE} : {MOTIF_RENVOI_MANQUANT} — la ligne de « {terme} » ne renvoie pas vers "
                    f"« {page_definition} » (cibles lues : {cibles}) ; attendu le renvoi vers la page qui "
                    f"definit deja le terme (D-17)"
                )
            for cible in cibles:
                if not (docs_dir / cible).is_file():
                    constats.append(
                        f"{PAGE} : {MOTIF_RENVOI_MANQUANT} — la cible « {cible} » de « {terme} » ne "
                        f"resout pas depuis {docs_dir.name}/ ; attendu une page de {docs_dir.name}/ qui "
                        f"definit deja le terme (D-17)"
                    )

    for terme, employeur, _page in TERMES_GLOSSAIRE:
        if normalize(terme) not in lues:
            constats.append(
                f"{PAGE} : {MOTIF_TERME_ABSENT} — « {terme} » (employeur declare : {employeur}) ; attendu "
                f"une ligne de tableau dont la premiere cellule porte le terme entre accents graves "
                f"(D-94)"
            )

    return constats


def problemes_page_glossaire(docs_dir: Path) -> list[str]:
    """Constats de forme de la page : octets, valeurs volatiles, sources citees, derniere ligne.

    Le controle porte sur le **fichier** : octets UTF-8 sans BOM, fins de ligne CRLF, aucune valeur
    volatile, chaque chemin entre accents graves du bloc `TITRE_SOURCE` existant depuis la racine du
    depot, ce bloc en derniere section, et `LIEN_RETOUR` en derniere ligne non vide (D-03, D-73, D-75,
    D-102).
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        return [
            f"{PAGE} : {MOTIF_TERMES} — page absente : {chemin.as_posix()} ; attendu la page unique du "
            f"vocabulaire du produit et de la documentation (D-94)"
        ]

    octets = chemin.read_bytes()
    texte = _texte_page(docs_dir, PAGE)
    if texte is None:
        return [
            f"{PAGE} : {MOTIF_CRLF} — fichier non decodable en UTF-8 strict ; attendu des octets UTF-8 "
            f"sans BOM (D-102)"
        ]

    constats: list[str] = []

    if octets.startswith(BOM):
        constats.append(
            f"{PAGE} : {MOTIF_CRLF} — le fichier commence par une marque d'ordre des octets ; attendu des "
            f"octets UTF-8 sans BOM (D-102)"
        )

    crlf = octets.count(b"\r\n")
    sauts = octets.count(b"\n")
    retours = octets.count(b"\r")
    if crlf != sauts or crlf != retours:
        constats.append(
            f"{PAGE} : {MOTIF_CRLF} — {crlf} fins de ligne CRLF, {sauts} sauts de ligne et {retours} "
            f"retours chariot ; attendu autant de CRLF que de sauts de ligne, comme les autres pages de "
            f"docs/ (D-102)"
        )

    for trouve in MOTIF_VOLATILE.finditer(texte):
        constats.append(
            f"{PAGE} : {MOTIF_VOLATILES} — le nombre « {trouve.group(0)} » ; attendu aucune valeur qui "
            f"change d'une installation ou d'une execution a l'autre (D-73, D-75)"
        )
    chemin_poste = MOTIF_CHEMIN_POSTE.search(texte)
    if chemin_poste:
        constats.append(
            f"{PAGE} : {MOTIF_VOLATILES} — « {chemin_poste.group(0)} » ; attendu aucun chemin de poste "
            f"dans la page (D-73)"
        )

    lignes = texte.splitlines()
    rangs = [
        rang for rang, ligne in enumerate(lignes) if ligne.strip() == TITRE_SOURCE
    ]
    if not rangs:
        constats.append(
            f"{PAGE} : {MOTIF_SOURCE} — la section « {TITRE_SOURCE} » est absente ; attendu ce bloc de "
            f"provenance, en derniere section de la page (D-03, D-69)"
        )
    else:
        rang_source = rangs[0]
        suivants = [
            ligne for ligne in lignes[rang_source + 1 :] if ligne.startswith("## ")
        ]
        if suivants:
            constats.append(
                f"{PAGE} : {MOTIF_SOURCE} — le bloc « {TITRE_SOURCE} » est suivi de {len(suivants)} "
                f"titre(s) de niveau 2 ; attendu ce bloc en derniere section, la ligne de retour apres "
                f"lui (D-102, D-69)"
            )
        for cite in MOTIF_CHEMIN_CITE.findall("\n".join(lignes[rang_source + 1 :])):
            if not (RACINE_DEPOT / cite).is_file():
                constats.append(
                    f"{PAGE} : {MOTIF_SOURCE} — « {cite} » ne resout pas depuis "
                    f"{RACINE_DEPOT.as_posix()} ; attendu un chemin existant, cite entre accents graves "
                    f"dans le bloc « {TITRE_SOURCE} » (D-03)"
                )

    non_vides = [ligne for ligne in lignes if ligne.strip()]
    derniere = non_vides[-1].strip() if non_vides else ""
    if derniere != LIEN_RETOUR:
        constats.append(
            f"{PAGE} : {MOTIF_FERMETURE} — la derniere ligne non vide vaut « {derniere} » ; attendu "
            f"« {LIEN_RETOUR} » comme derniere ligne du gabarit de page (D-102)"
        )

    return constats


def _imports_du_module(arbre: ast.AST) -> set[str]:
    """Modules importes par le module d'ancrage, imports imbriques compris dans les fonctions."""
    importes: set[str] = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            importes.update(alias.name for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom) and noeud.module is not None:
            importes.add(noeud.module)
    return importes


def _appels_du_module(arbre: ast.AST) -> set[str]:
    """Noms appeles par le module d'ancrage, sous forme `objet.attribut` ou `nom`."""
    appeles: set[str] = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        if isinstance(noeud.func, ast.Attribute):
            appeles.add(noeud.func.attr)
        else:
            appeles.add(getattr(noeud.func, "id", ""))
    return appeles


def test_garde_de_cloture_du_harnais() -> None:
    """Le module ne joint ni base, ni processus, ni socket, ni reseau, et n'execute pas le produit.

    La propriete est verifiee sur le texte de ce module par `ast`, et jamais par une recherche de
    chaines : le module cite lui-meme les noms interdits dans ses messages, une recherche textuelle se
    detecterait elle-meme. La garde est **reecrite** pour ce module : elle ne porte pas le resserrement
    `data_dir` de la phase 5 (ce module n'ouvre aucune base) et refuse en revanche le lancement du
    calcul du produit, qui reste le risque reel d'un module d'ancrage documentaire.

    Limite nommee : c'est une demonstration statique et indirecte. Elle dit ce que ce module importe et
    appelle, pas ce qu'un autre chemin ferait ; la preuve directe qu'aucune ecriture n'a lieu sous
    `.data/` est la mesure d'empreinte prise autour de la suite entiere.
    """
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    importes = _imports_du_module(arbre)
    appeles = _appels_du_module(arbre)
    constats: list[str] = []

    racines = sorted(module for module in importes if module.split(".")[0] in RACINES_INTERDITES)
    if racines:
        constats.append(
            f"import(s) de base, de processus, de socket ou de reseau : {', '.join(racines)} ; attendu "
            f"aucun de ces imports dans le module d'ancrage du vocabulaire ({PAGE})"
        )
    if APPEL_PRODUIT in appeles:
        constats.append(
            f"appel a {APPEL_PRODUIT}() dans le module d'ancrage ; attendu un ancrage par la lecture des "
            f"pages et des fichiers employeurs, le produit n'etant jamais execute ({PAGE})"
        )
    calculs = sorted(set(APPELS_CALCUL_PRODUIT) & appeles)
    if calculs:
        constats.append(
            f"appel(s) de calcul du produit : {', '.join(calculs)} ; attendu aucun lancement de calcul "
            f"dans le module d'ancrage, ces points d'entree lancant le solveur ({PAGE})"
        )
    suppressions = sorted(set(APPELS_SUPPRESSION) & appeles)
    if suppressions:
        constats.append(
            f"appel(s) de suppression de fichier : {', '.join(suppressions)} ; attendu aucun appel "
            f"destructif dans le module d'ancrage ({PAGE})"
        )

    assert not constats, (
        f"{PAGE} : {MOTIF_GARDE} — constats : "
        + " ; ".join(constats)
        + " ; attendu un module d'ancrage qui lit des fichiers, sans joindre le reseau, sans lancer de "
        "processus, sans executer le produit et sans supprimer de fichier (D-103, D-104)"
    )


def test_entrees_du_glossaire(docs_dir: Path, normalize) -> None:
    """Les entrees du glossaire sont declarees, uniques, triees, employees et renvoyees qui de droit.

    Tranche verticale du plan : la page, sa ligne d'index et son harnais sont traverses d'un bout a
    l'autre par ce seul controle, qui va de la page vers le depot — les libelles confrontes a la
    constante du module, les employeurs confrontes a l'arbre, les renvois a leur cible (D-19, D-94).

    Limite honnete : ce controle ne revendique aucune exhaustivite sur la prose des definitions. Il porte
    sur les libelles, leur ordre, leur employeur et leur renvoi — rien de plus (D-85).
    """
    constats = problemes_glossaire(docs_dir, normalize)
    assert not constats, (
        f"{PAGE} : {MOTIF_TERMES} — constats : "
        + " ; ".join(constats)
        + f" ; attendu une page dont chaque ligne de tableau porte un terme declare par TERMES_GLOSSAIRE, "
        f"trie apres normalisation, employe par le fichier qu'elle cite et renvoye vers la page qui le "
        f"definit deja quand elle existe (D-17, D-19, D-94)"
    )


def test_renvois_de_definition(docs_dir: Path, normalize) -> None:
    """Chaque terme que le glossaire renvoie au lieu de le definir porte un renvoi qui resout (D-17).

    Le test exerce d'abord le contrat lui-meme : si aucun terme ne declare de page de definition, le
    controle du renvoi serait un faux temoin — une fonction qui ne verifie rien passe toujours — et une
    page declaree qui ne serait pas un nom de page de `docs/` serait un renvoi impossible. Puis
    `problemes_glossaire` accumule le reste : cible absente de la ligne, cible qui ne resout pas.
    """
    constats: list[str] = []
    renvois = [
        (libelle, page) for libelle, _employeur, page in TERMES_GLOSSAIRE if page is not None
    ]

    if not renvois:
        constats.append(
            f"{PAGE} : {MOTIF_RENVOI_MANQUANT} — TERMES_GLOSSAIRE ne declare aucune page de definition ; "
            f"attendu au moins un terme qu'une page livree definit deja, sans quoi ce controle serait un "
            f"faux temoin (D-17)"
        )

    for libelle, page in renvois:
        if not (docs_dir / page).is_file():
            constats.append(
                f"{PAGE} : {MOTIF_RENVOI_MANQUANT} — la page de definition « {page} » declaree pour "
                f"« {libelle} » n'existe pas sous {docs_dir.name}/ ; attendu une page livree qui definit "
                f"deja le terme (D-17)"
            )

    constats.extend(problemes_glossaire(docs_dir, normalize))
    assert not constats, (
        f"{PAGE} : {MOTIF_RENVOI_MANQUANT} — constats : "
        + " ; ".join(constats)
        + f" ; attendu un renvoi vers la page qui definit deja chaque terme deja defini, et un renvoi "
        f"court — jamais la definition complete de la page cible — pour les autres (D-17)"
    )


def test_le_vocabulaire_du_harnais_est_absent(docs_dir: Path, normalize) -> None:
    """Aucun libelle d'entree n'appartient au vocabulaire de harnais, et la liste n'est pas vide.

    Un refus sans liste est un vert trompeur : la constante est donc exigee **non vide** avant d'etre
    appliquee. Le controle porte sur les libelles (la premiere cellule du tableau), jamais sur le texte
    entier de la page : les phrases de renvoi du glossaire emploient legitimement les mots de la
    documentation, ce sont les **entrees** qui ne doivent pas etre des mots de planification (D-19).
    """
    constats: list[str] = []

    if not TERMES_INTERDITS:
        constats.append(
            f"{PAGE} : {MOTIF_TERME_INTERDIT} — TERMES_INTERDITS est vide ; attendu le vocabulaire de "
            f"planification, mesure comme absent des pages livrees et de dofus_stuff/ (D-19)"
        )

    texte = _texte_page(docs_dir, PAGE)
    if texte is None:
        constats.append(
            f"{PAGE} : {MOTIF_TERMES} — page absente : {(docs_dir / PAGE).as_posix()} ; attendu la page "
            f"unique du vocabulaire du produit et de la documentation (D-94)"
        )
    else:
        interdits = {normalize(terme) for terme in TERMES_INTERDITS}
        for libelle, _reste in _lignes_de_termes(texte):
            if normalize(libelle) in interdits:
                constats.append(
                    f"{PAGE} : {MOTIF_TERME_INTERDIT} — « {libelle} » appartient au vocabulaire de "
                    f"planification, absent des pages livrees et de dofus_stuff/ ; attendu un terme du "
                    f"produit ou de la documentation (D-19)"
                )

    assert not constats, (
        f"{PAGE} : {MOTIF_TERME_INTERDIT} — constats : "
        + " ; ".join(constats)
        + f" ; attendu des libelles d'entree qui n'appartiennent pas au vocabulaire de planification, et "
        f"une liste de refus non vide (D-19)"
    )


def test_page_glossaire_close_et_sans_valeur_volatile(docs_dir: Path) -> None:
    """La page respecte le gabarit et ne fige aucune valeur de poste (D-102, D-73).

    Un seul titre de niveau 1, le bloc `TITRE_SOURCE` en derniere section, `LIEN_RETOUR` en derniere
    ligne non vide, octets CRLF sans BOM, aucun nombre de quatre chiffres ou plus, aucun chemin de
    poste, et chaque chemin cite du bloc de provenance existant depuis la racine du depot.
    """
    constats = problemes_page_glossaire(docs_dir)
    assert not constats, (
        f"{PAGE} : constats de forme : "
        + " ; ".join(constats)
        + f" ; attendu des octets CRLF sans BOM, aucune valeur volatile, un bloc « {TITRE_SOURCE} » en "
        f"derniere section dont chaque chemin existe, et « {LIEN_RETOUR} » en derniere ligne non vide "
        f"(D-03, D-73, D-102)"
    )
