"""Ancrage de la page `docs/wizard-avance.md` sur le rendu reel du wizard avance.

Le contrat va du rendu vers la page : les neuf ecrans du wizard avance sont rendus par le client de
test Flask, en processus, sur la fixture `app` de `tests/conftest.py` (D-32), puis les titres, les
libelles, les formats et les messages lus dans le corps, dans la ligne de statut et dans la ligne
d'en-tete sont compares a ceux que la page cite. Aucun serveur n'est lance, aucun socket n'est
ouvert, le programme du produit n'est jamais execute et rien n'est ecrit sous `.data/` : la fixture
`app` construit sa propre base dans un dossier temporaire.

Limite nommee : la garde `ast` de ce module est une demonstration statique et indirecte. Elle dit ce
que ce module importe et appelle, pas ce qu'un autre chemin ferait. En particulier, poster `GO` sur
le recapitulatif **execute le solveur** (`dofus_stuff/web/routes.py:1114-1116`) : la garde refuse
cette paire dans le module, et aucun controle de ce module ne poste `GO`.

Limite nommee : la prose libre de la page (les phrases d'explication) n'est pas verifiee par un
test. Les controles portent sur les libelles, les nombres et les messages **cites**, et ce module ne
revendique aucune exhaustivite de la redaction.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from dofus_stuff.model.solver_spec import SLOT_GROUPS, TYPE_FILTER_KEYS
from dofus_stuff.web.optimize_wizard import (
    STEP_TITLES,
    TYPE_FILTER_LABELS,
    WIZARD_STEPS,
)

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "wizard-avance.md"
SOMMAIRE = "sommaire.md"
GUIDE_WIZARD = "GUIDE_WIZARD.md"
README = "README.md"
SOURCE_ROUTES = "dofus_stuff/web/routes.py"
SOURCE_WIZARD = "dofus_stuff/web/optimize_wizard.py"
SOURCE_SPEC = "dofus_stuff/model/solver_spec.py"
SOURCE_SCREENS = "dofus_stuff/web/screens.py"
SOURCE_TEMPLATE = "dofus_stuff/web/templates/screen.html"

# Contrat de titres de la page : chaque titre est ecrit au caractere pres, le helper `section` de
# `tests/conftest.py` ne normalisant pas un titre. La constante compte les sections de ce plan et
# reste en accord exact avec la page a la fin de chaque tache : le plan 04-02 la complete, tache par
# tache, avec les sections qu'il cree — jamais un titre epingle sans sa section, sinon la morsure du
# controle de forme serait indiscernable d'une derive. Les titres sont nommes un a un, puis rassembles
# dans l'ordre du document : l'insertion d'une section ne peut donc pas decaler silencieusement la
# constante d'une autre.
TITRE_ARRIVEE = "## Arriver au wizard"
TITRE_ETAPES = "## Les 9 étapes du wizard"
TITRE_SLOTS = "## Slots et filtres"
TITRE_OPTIONS = "## Les 11 options du solveur"
TITRE_NOMBRES = "## Les quatre nombres d'une ligne"
TITRE_ITEMS = "## Interdire, forcer, retirer un objet"
TITRE_EXEMPLE = "## Exemple guidé"
TITRE_SOURCE = "## Source de vérité"

TITRES_SECTION_ATTENDUS = (
    TITRE_ARRIVEE,
    TITRE_ETAPES,
    TITRE_SLOTS,
    TITRE_OPTIONS,
    TITRE_NOMBRES,
    TITRE_ITEMS,
    TITRE_EXEMPLE,
    TITRE_SOURCE,
)

# Sous-titres de niveau 3 de la section des slots et des filtres.
SOUS_TITRE_EMPLACEMENTS = "### Les 11 emplacements"
SOUS_TITRE_FILTRES = "### Les 10 filtres de type"

# Marqueurs du gabarit reel (`dofus_stuff/web/templates/screen.html`) : le corps visible est encadre
# par `id="body"` et par la seule ligne de statut, qui porte les messages de refus ; la ligne
# d'en-tete porte le code de programme et le titre de l'ecran.
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'
MARQUEUR_ENTETE = '<div class="row header" id="header-row">'
LIGNE_CORPS = re.compile(r'<div class="row">(.*?)</div>', re.S)
LIBELLE_SAISIE = re.compile(r'<label class="input-label meta">(.*?)</label>', re.S)
TOUCHE_BARRE = re.compile(
    r'<span class="fkey-key meta">([^<]*)</span>'
    r'<span class="fkey-eq meta">=</span>'
    r'<span class="fkey-label">([^<]*)</span>'
)

# Lignes rendues des emplacements et des filtres (`optimize_wizard.py:189-215`) : le numero, l'etat
# entre crochets produit par `_on_off` (espace finale comprise) et le libelle. Le motif est applique
# ligne par ligne, une ligne rendue ne portant jamais deux entrees.
MOTIF_EMPLACEMENT_RENDU = re.compile(
    r"^\s*(?P<numero>\d{1,2})\.\s+\[\s*(?:ON|OFF)\s*\]\s*(?P<libelle>.+?)\s*$"
)
MOTIF_FILTRE_RENDU = re.compile(
    r"^F(?P<numero>\d{1,2})\.\s+\[\s*(?:ON|OFF)\s*\]\s*(?P<libelle>.+?)\s*$"
)

# Lignes de tableau de la page : `| 1 | `AMULETTE` |` et `| `F1` | `FAMILIER` |`.
MOTIF_LIGNE_EMPLACEMENT = re.compile(
    r"^\|\s*(?P<numero>\d{1,2})\s*\|\s*`(?P<libelle>[^`]+)`\s*\|\s*$"
)
MOTIF_LIGNE_FILTRE = re.compile(
    r"^\|\s*`F(?P<numero>\d{1,2})`\s*\|\s*`(?P<libelle>[^`]+)`\s*\|\s*$"
)

# Invites et rappel de l'ecran des slots et des filtres, lus au rendu et jamais ecrits de memoire.
MOTIF_INVITE_EMPLACEMENTS = re.compile(r"^SLOTS \(N=TOGGLE\) :$")
MOTIF_INVITE_FILTRES = re.compile(r"^FILTRES TYPES \(F\+N\) :$")
MOTIF_RAPPEL_TOUCHES = re.compile(r"^N=TOGGLE SLOT\s+FN=TOGGLE FILTRE$")

# Lignes rendues des onze options du solveur (`optimize_wizard.py`) : numero, libelle, valeur.
MOTIF_OPTION_RENDUE = re.compile(
    r"^(?P<numero>\d{1,2})\.\s+(?P<libelle>.+?)\s*=\s*(?P<valeur>.*)$"
)

# Lignes rendues des listes d'objets : les quatre lignes de syntaxe et les deux listes, avec leur
# compte d'entrees et leur contenu.
MOTIF_SYNTAXE_RENDUE = re.compile(r"^\s*(?P<prefixe>\+ID|-ID|!ID|CLEAR)\s+(?P<verbe>.+?)\s*$")
MOTIF_LISTE_RENDUE = re.compile(
    r"^(?P<nom>INTERDITS|FORCES)\s*\((?P<compte>\d+)\)\s*:\s*(?P<contenu>.*)$"
)

# Invites et rappels des ecrans des options et des items, lus au rendu et jamais ecrits de memoire.
MOTIF_INVITE_OPTIONS = re.compile(r"^OPTIONS \(N=EDIT\) :$")
MOTIF_RAPPEL_OPTIONS = re.compile(r"^N=CHOISIR OPTION$")

# Ligne de tableau de la page citant une option : meme forme que celle d'un emplacement, un numero
# puis un libelle backtique.
MOTIF_LIGNE_OPTION = MOTIF_LIGNE_EMPLACEMENT

# Ligne de tableau de la page citant un ecran et sa forme d'edition, ou une saisie d'items et son
# verbe : la cle n'est pas un numero, elle est donc lue comme texte backtique.
MOTIF_LIGNE_FORMAT = re.compile(
    r"^\|\s*`(?P<cle>[^`]+)`\s*\|\s*`(?P<libelle>[^`]+)`\s*\|\s*$"
)
MOTIF_LIGNE_SYNTAXE_ITEMS = MOTIF_LIGNE_FORMAT

# Ligne de tableau de la page associant une etape a l'identifiant de son ecran :
# `| 1. `slots` | `OPT-W1` |`, tel que la ligne d'en-tete le rend (`dofus_stuff/web/routes.py`).
MOTIF_LIGNE_IDENTIFIANT = re.compile(
    r"^\|\s*(?P<numero>\d{1,2})\.\s*`(?P<etape>[a-z]+)`\s*"
    r"\|\s*`(?P<identifiant>OPT-W[A-Z0-9]+)`\s*\|\s*$"
)

# Lignes du parcours d'arrivee, lues au rendu et jamais ecrites de memoire : la ligne du menu
# principal qui ouvre l'optimisation, la ligne `AVANCE` proposee par les trois questions, et les
# trois questions elles-memes (`1/3`, `2/3`, `3/3`).
MOTIF_LIGNE_MENU = re.compile(r"^\s*(?P<numero>\d)\.\s+(?P<libelle>OPTIMISATION.*?)\s*$")
MOTIF_LIGNE_AVANCE = re.compile(r"^(?P<mot>AVANCE)\s*:\s*(?P<libelle>.+?)\s*$")
MOTIF_LIGNE_QUESTION = re.compile(r"^(?P<rang>[1-3])/3\s*-\s*(?P<question>.+?)\s*$")

# Commandes annoncees par le corps du recapitulatif (`GO = LANCER`, `RESET = REINITIALISER`,
# `1-8 = RETOUR ECRAN`, `SAVES = STUFFS SAUVEGARDES`) et la forme sous laquelle la page les cite.
# Les couples d'une meme ligne rendue sont separes par au moins deux espaces
# (`dofus_stuff/web/optimize_wizard.py`, `body_recap`) : la decoupe suit ce separateur mesure, jamais
# une position fixe.
MOTIF_COMMANDE_RENDUE = re.compile(r"^(?P<cle>\S+)\s=\s(?P<verbe>.+)$")
MOTIF_COMMANDE_CITEE = re.compile(r"`(?P<cle>[A-Z0-9-]+) = (?P<verbe>[^`]+)`")
SEPARATEUR_COMMANDES = re.compile(r"\s{2,}")

# Jeton d'une commande destructrice, interdit dans un parcours recommande (D-22/D-23, D-61) : l'exemple
# guide migre n'en contient aucun. Le motif est celui deja employe par la garde de la page
# d'installation (`tests/test_docs_structure.py`), repris ici pour la seule section de l'exemple.
COMMANDE_DESTRUCTRICE = re.compile(r"\bdb\s+clear\b")

# Etat vide cite par la page, lu a cote de la phrase qui le porte.
MOTIF_ETAT_VIDE_CITE = re.compile(r"l'état vide `(?P<etat>\([^`]+\))`")

# Champ de saisie de la coquille, lu **dans la balise du champ** : une recherche libre de
# `maxlength="..."` trouverait d'abord une autre balise du document.
MOTIF_CHAMP_SAISIE = re.compile(r'<input class="field"(?P<attributs>[^>]*)>', re.S)
MOTIF_ATTRIBUT_CHAMP = re.compile(r'(?P<nom>[a-z-]+)="(?P<valeur>[^"]*)"')

# Chemin de code cite entre accents graves, et forme du document entier, reprises du patron de la
# phase 3 : une page qui cite un chemin doit citer un chemin qui existe.
CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml|js|md|json|sql))`")
BOM_UTF8 = b"\xef\xbb\xbf"
FRAGMENT_H1 = "# "
FRAGMENT_LIEN_EXTERNE = "](http"
LIGNE_RETOUR = "[Retour au sommaire](sommaire.md)"
BALISE_COMMANDE = "```console"

# Motif de morsure porte par une constante de module et jamais ecrit en clair dans la ligne
# d'assertion (regle posee au plan 03-03, tache 2) : pytest reproduit cette ligne dans sa sortie, et
# une valeur ecrite en clair y serait trouvee sans qu'aucun message n'ait ete produit.
MOTIF_ORDRE_ETAPES = "ordre de WIZARD_STEPS"
MOTIF_ARRIVEE = "arrivee du wizard"
MOTIF_IDENTIFIANT_ECRAN = "identifiant d'ecran"
MOTIF_EXEMPLE = "exemple guide"

# Racines dont un import signalerait un risque reel : ouvrir la base, lancer un processus, ouvrir une
# socket, joindre le reseau. Le controle porte sur le risque, jamais sur une liste blanche de modules
# produit a tenir a jour.
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

# Nom produit dont l'import signalerait que le module d'ancrage tire la base locale.
MODULE_BASE_INTERDIT = "dofus_stuff.database"

# Noms d'appel dont la presence signalerait une action destructive ou l'execution du produit.
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"


def _texte_page(docs_dir: Path) -> str:
    """Texte de la page, lu en UTF-8 explicite ; page absente = AssertionError localisante (D-13).

    Jamais de `FileNotFoundError` brut : l'echec nomme la page, le chemin attendu et le fichier de
    code dont elle decrit la surface. Toute lecture de la page passe par ici.
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page du wizard avance "
            f"decrite par {SOURCE_WIZARD}, livree dans docs/"
        )
    return chemin.read_text(encoding="utf-8")


def _lignes_du_corps(reponse) -> list[str]:
    """Lignes visibles du corps de l'ecran, jamais la reponse entiere.

    La charge utile `data-stuff-payload` porte tout le resultat sur chaque page et `tojson` y
    echappe les accents : une assertion sur la reponse entiere serait fausse sur une page correcte.
    """
    texte = reponse.get_data(as_text=True)
    corps = texte.split(MARQUEUR_CORPS, 1)[1].split(MARQUEUR_STATUT, 1)[0]
    return [ligne.rstrip() for ligne in LIGNE_CORPS.findall(corps)]


def _entete(reponse) -> str:
    """Texte de la ligne d'en-tete de la coquille, ou "" si le marqueur est absent du rendu.

    Le titre de l'etape n'est rendu nulle part ailleurs : la ligne de corps d'un ecran de
    statistiques porte le titre en majuscules pour sa pagination, mais l'ecran `recap` n'en porte
    aucun. L'en-tete est donc la seule source du titre rendu.
    """
    texte = reponse.get_data(as_text=True)
    if MARQUEUR_ENTETE not in texte:
        return ""
    return texte.split(MARQUEUR_ENTETE, 1)[1].split("</div>", 1)[0]


def _statut(reponse) -> str:
    """Texte de la ligne de statut : la seule source des messages de refus."""
    texte = reponse.get_data(as_text=True)
    return texte.split(MARQUEUR_STATUT, 1)[1].split(">", 1)[1].split("</div>", 1)[0]


def _touches(reponse) -> list[tuple[str, str]]:
    """Couples touche <-> libelle de la barre de raccourcis, tels qu'ils sont rendus.

    Chaque touche est un `span` distinct : la chaine `ESC=Retour` n'existe nulle part dans le HTML
    rendu, c'est donc le couple extrait qui est exige, jamais la concatenation.
    """
    return TOUCHE_BARRE.findall(reponse.get_data(as_text=True))


def _sous_section(corps: str, titre: str) -> str:
    """Corps d'une sous-section de niveau 3, du titre jusqu'au titre `###` suivant.

    Le helper partage `section` de `tests/conftest.py` ne connait que les titres de niveau 2 : les
    listes vivant sous un titre de niveau 3, leur extraction reste locale a ce module et n'est
    promue nulle part (D-12).
    """
    lignes = corps.splitlines()
    debut: int | None = None
    for index, ligne in enumerate(lignes):
        if debut is not None and ligne.startswith("### "):
            return "\n".join(lignes[debut:index])
        if ligne.strip() == titre.strip():
            debut = index + 1
    if debut is None:
        raise AssertionError(
            f"{PAGE} : sous-section « {titre} » introuvable ; attendu ce titre de niveau 3, qui "
            f"porte la liste mesuree du wizard avance, rendue par {SOURCE_WIZARD}"
        )
    return "\n".join(lignes[debut:])


def _emplacements_du_rendu(lignes: list[str]) -> dict[int, str]:
    """Couples numero -> libelle des emplacements, lus dans les lignes rendues du corps."""
    couples: dict[int, str] = {}
    for ligne in lignes:
        trouve = MOTIF_EMPLACEMENT_RENDU.match(ligne)
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _filtres_du_rendu(lignes: list[str]) -> dict[int, str]:
    """Couples numero -> libelle des filtres de type, lus dans les lignes rendues du corps."""
    couples: dict[int, str] = {}
    for ligne in lignes:
        trouve = MOTIF_FILTRE_RENDU.match(ligne)
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _couples_de_table(sous_texte: str, motif: re.Pattern[str]) -> dict[int, str]:
    """Couples numero -> libelle cites par une table de la page, une ligne de tableau par couple."""
    couples: dict[int, str] = {}
    for ligne in sous_texte.splitlines():
        trouve = motif.match(ligne)
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _couples_texte(sous_texte: str, motif: re.Pattern[str]) -> dict[str, str]:
    """Couples cle -> libelle cites par une table dont la cle n'est pas un numero de ligne."""
    couples: dict[str, str] = {}
    for ligne in sous_texte.splitlines():
        trouve = motif.match(ligne)
        if trouve is not None:
            couples[trouve.group("cle").strip()] = trouve.group("libelle").strip()
    return couples


def _identifiants_cites(corps: str) -> dict[str, str]:
    """Couples etape -> identifiant d'ecran cites par la table de la section d'arrivee.

    La cle est le mot-cle de l'etape (`slots`, `options`, ...) : la comparaison se fait donc sur le
    nom que `WIZARD_STEPS` emploie, jamais sur le numero de la ligne de tableau.
    """
    cites: dict[str, str] = {}
    for ligne in corps.splitlines():
        trouve = MOTIF_LIGNE_IDENTIFIANT.match(ligne)
        if trouve is not None:
            cites[trouve.group("etape")] = trouve.group("identifiant")
    return cites


def _couples_de_commandes(lignes: list[str]) -> dict[str, str]:
    """Couples cle -> verbe annonces par le corps du recapitulatif, lus au rendu.

    Une meme ligne rendue porte plusieurs couples separes par au moins deux espaces
    (`GO = LANCER  RESET = REINITIALISER  1-8 = RETOUR ECRAN`) : la decoupe suit ce separateur
    mesure, jamais une position fixe. Les autres lignes du corps (`BAN=0 FORCE=0`, `JET=average`)
    ne portent pas la forme `CLE = VERBE` et ne produisent donc aucun couple.
    """
    couples: dict[str, str] = {}
    for ligne in lignes:
        for morceau in SEPARATEUR_COMMANDES.split(ligne.strip()):
            trouve = MOTIF_COMMANDE_RENDUE.match(morceau)
            if trouve is not None:
                couples[trouve.group("cle")] = trouve.group("verbe").strip()
    return couples


def _options_du_rendu(lignes: list[str]) -> dict[int, str]:
    """Couples numero -> libelle des options, lus dans les lignes rendues du corps.

    Le compte des options vient du rendu, jamais d'une table locale : la liste des onze options
    n'expose aucune constante publique (`dofus_stuff/web/optimize_wizard.py`), le rendu est donc le
    seul ancrage autorise.
    """
    couples: dict[int, str] = {}
    for ligne in lignes:
        trouve = MOTIF_OPTION_RENDUE.match(ligne.strip())
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _syntaxe_du_rendu(lignes: list[str]) -> dict[str, str]:
    """Couples prefixe -> verbe des quatre lignes de syntaxe, lus dans le corps rendu."""
    couples: dict[str, str] = {}
    for ligne in lignes:
        trouve = MOTIF_SYNTAXE_RENDUE.match(ligne)
        if trouve is not None:
            couples[trouve.group("prefixe")] = trouve.group("verbe").strip()
    return couples


def _listes_du_rendu(lignes: list[str]) -> dict[str, str]:
    """Contenu rendu des deux listes d'objets, par nom de liste."""
    listes: dict[str, str] = {}
    for ligne in lignes:
        trouve = MOTIF_LISTE_RENDUE.match(ligne.strip())
        if trouve is not None:
            listes[trouve.group("nom")] = trouve.group("contenu").strip()
    return listes


def _forme_d_edition(lignes: list[str]) -> str:
    """Ligne `FORMAT : ...` du sous-ecran d'edition, ou "" si l'ecran n'en porte pas."""
    return next((ligne.strip() for ligne in lignes if ligne.strip().startswith("FORMAT : ")), "")


def _message_de_statut(statut: str) -> str:
    """Premier segment de la ligne de statut : le message, avant les indicateurs de l'ecran.

    La coquille joint le message et les indicateurs par ` — ` (`dofus_stuff/web/routes.py`) : le
    message seul est ce qui se compare au libelle ecrit par le code, sans la pagination ni l'invite
    d'entree.
    """
    return statut.split(" — ", 1)[0].strip()


def _libelle_saisie(reponse) -> str:
    """Texte interieur du libelle du champ de saisie, tel qu'il est rendu."""
    trouve = LIBELLE_SAISIE.search(reponse.get_data(as_text=True))
    return "" if trouve is None else trouve.group(1)


def _champ_saisie(reponse) -> dict[str, str]:
    """Attributs de la balise du champ de saisie, lus dans cette balise et nulle part ailleurs."""
    trouve = MOTIF_CHAMP_SAISIE.search(reponse.get_data(as_text=True))
    if trouve is None:
        return {}
    return {
        attribut.group("nom"): attribut.group("valeur")
        for attribut in MOTIF_ATTRIBUT_CHAMP.finditer(trouve.group("attributs"))
    }


def _imports_du_module(arbre: ast.AST) -> set[str]:
    """Modules importes par le module d'ancrage, imports imbattables compris dans les fonctions."""
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
    """Le module n'ouvre ni la base, ni un processus, ni une socket, et ne poste jamais `GO` (T-04-03).

    La propriete est verifiee sur le texte de ce module par `ast`, et jamais par une recherche de
    chaines : le module cite lui-meme les noms interdits dans ses messages, une recherche textuelle
    se detecterait elle-meme. Le controle porte sur le risque reel — ouvrir la base, lancer un
    processus, ouvrir une socket, joindre le reseau, supprimer un fichier, executer le produit — donc
    un import public pur ajoute plus tard passe sans revision, alors qu'un import qui tirerait la
    base rougit. Poster `GO` au recapitulatif execute le solveur : c'est la saisie interdite ici.
    """
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    importes = _imports_du_module(arbre)
    appeles = _appels_du_module(arbre)
    constats: list[str] = []

    racines = sorted(module for module in importes if module.split(".")[0] in RACINES_INTERDITES)
    if racines:
        constats.append(
            f"import(s) de base, de processus, de socket ou de reseau : {', '.join(racines)} ; "
            f"attendu aucun de ces imports dans le module d'ancrage decrit par {PAGE} "
            f"({SOURCE_ROUTES}, wizard avance)"
        )
    if MODULE_BASE_INTERDIT in importes or any(
        module.startswith(MODULE_BASE_INTERDIT + ".") for module in importes
    ):
        constats.append(
            f"import de « {MODULE_BASE_INTERDIT} » ; attendu aucun import de la base locale, la "
            f"fixture `app` construisant sa propre base temporaire ({SOURCE_WIZARD})"
        )
    if APPEL_PRODUIT in appeles:
        constats.append(
            f"appel a {APPEL_PRODUIT}() dans le module d'ancrage ; attendu un ancrage par le client "
            f"de test Flask de {SOURCE_ROUTES}, le produit n'etant jamais execute"
        )
    suppressions = sorted(set(APPELS_SUPPRESSION) & appeles)
    if suppressions:
        constats.append(
            f"appel(s) de suppression de fichier : {', '.join(suppressions)} ; attendu aucun appel "
            f"destructif dans le module d'ancrage decrit par {PAGE}"
        )

    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        for mot in noeud.keywords:
            if mot.arg != "data" or not isinstance(mot.value, ast.Dict):
                continue
            paires: dict[str, str] = {}
            for cle, valeur in zip(mot.value.keys, mot.value.values):
                if (
                    isinstance(cle, ast.Constant)
                    and isinstance(cle.value, str)
                    and isinstance(valeur, ast.Constant)
                    and isinstance(valeur.value, str)
                ):
                    paires[cle.value] = valeur.value
            if paires.get("cmd", "").strip().casefold() == "go":
                constats.append(
                    f"saisie `cmd` = « GO » postee ligne {noeud.lineno} ; attendu aucune saisie "
                    f"`GO` : elle lance le solveur par `_run_optimize_and_redirect` "
                    f"({SOURCE_ROUTES}:1114-1116) et redirige vers le resultat"
                )

    assert not constats, (
        f"{PAGE} : constats sur la garde de cloture du harnais : "
        + " ; ".join(constats)
        + f" ; attendu un module d'ancrage qui rend les ecrans de {SOURCE_ROUTES} en processus, sans "
        f"ouvrir la base locale, sans joindre le reseau et sans jamais executer le solveur"
    )


def test_page_et_index_du_wizard(docs_dir: Path, app, normalize) -> None:
    """La page existe, son index est coherent, et les 9 titres rendus y sont cites (WIZ-01).

    Tranche verticale du plan : la page, sa ligne d'index, le harnais et le rendu sont traverses
    d'un bout a l'autre par ce seul controle. Les neuf ecrans repondent 200 sur un client neuf
    (`load_wizard_spec` retombe sur `default_player_spec(level=200)`), donc aucun etat de session
    n'est rejoue : un client neuf rend l'ecran, et la ligne d'en-tete porte le titre de l'etape.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    # 1. La ligne d'index de la page, lue dans la table du sommaire : le libelle cite sert de
    #    reference au H1, il n'est jamais ecrit deux fois de memoire.
    sommaire = (docs_dir / SOMMAIRE).read_text(encoding="utf-8")
    entree = re.search(rf"\|\s*\[(?P<libelle>[^\]]+)\]\({re.escape(PAGE)}\)", sommaire)
    if entree is None:
        constats.append(
            f"{PAGE} : page non listee dans docs/sommaire.md ; attendu une ligne de la table "
            f"« ## Index » de {SOMMAIRE} pointant vers {PAGE} (D-05, D-57)"
        )
    libelle = entree.group("libelle") if entree is not None else ""

    # 2. Un seul titre de niveau 1, egal au libelle d'index apres normalisation (D-11, D-56).
    titres = [ligne for ligne in texte.splitlines() if ligne.startswith("# ")]
    if len(titres) != 1:
        constats.append(
            f"{PAGE} : la page porte {len(titres)} titre(s) de niveau 1 ({', '.join(titres)}) ; "
            f"attendu un seul titre de niveau 1, celui de la page (D-56)"
        )
    elif libelle:
        h1 = titres[0][len("# ") :].strip()
        if normalize(h1) != normalize(libelle):
            constats.append(
                f"{PAGE} : H1 « {h1} » different du libelle d'index « {libelle} » ; attendu le "
                f"libelle d'index de {SOMMAIRE} pour {PAGE} (D-11)"
            )

    # 3. Les neuf titres rendus, lus dans la ligne d'en-tete de chaque ecran, puis exiges de la page.
    client = app.test_client()
    for numero, etape in enumerate(WIZARD_STEPS, start=1):
        rendu = client.get(f"/optimize/wizard/{etape}")
        attendu = STEP_TITLES.get(etape, "")
        entete = _entete(rendu)
        if rendu.status_code != 200 or normalize(attendu) not in normalize(entete):
            constats.append(
                f"l'ecran « {etape} » (etape {numero}) repond {rendu.status_code} et son en-tete "
                f"vaut « {entete} » ; attendu le titre « {attendu} » rendu par la ligne d'en-tete "
                f"de /optimize/wizard/{etape}, construit par {SOURCE_ROUTES}"
            )
        if normalize(attendu) not in normalize(texte):
            constats.append(
                f"{PAGE} : le titre rendu de l'etape {numero} vaut « {attendu} » et n'est pas cite "
                f"par la page ; attendu ce titre, lu au rendu de /optimize/wizard/{etape} et produit "
                f"par {SOURCE_WIZARD} (STEP_TITLES)"
            )

    assert not constats, (
        f"{PAGE} : constats sur la page et son index : "
        + " ; ".join(constats)
        + f" ; attendu la page de {SOURCE_WIZARD} listee dans {SOMMAIRE}, ouverte par un H1 egal a "
        f"son libelle d'index et citant les {len(WIZARD_STEPS)} titres rendus par les ecrans"
    )


def test_etapes_dans_l_ordre_du_code(docs_dir: Path, app, normalize, section) -> None:
    """Les 9 titres rendus sont cites par la page dans l'ordre de `WIZARD_STEPS` (D-50).

    L'ordre attendu n'est jamais ecrit dans ce module : il est relu dans `WIZARD_STEPS` et les
    titres dans `STEP_TITLES` (`dofus_stuff/web/optimize_wizard.py:23-45`), puis confronte a la ligne
    d'en-tete que le rendu produit reellement pour chacun des neuf ecrans. La comparaison d'ordre se
    fait dans la seule section des etapes, jamais sur la page entiere : la page cite ailleurs des
    mots qui reprennent un titre d'etape, et une position globale mesurerait alors autre chose.
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_ETAPES, PAGE)
    corps_normalise = normalize(corps)
    constats: list[str] = []

    client = app.test_client()
    titres: list[tuple[int, str, str]] = []
    for numero, etape in enumerate(WIZARD_STEPS, start=1):
        rendu = client.get(f"/optimize/wizard/{etape}")
        attendu = STEP_TITLES.get(etape, "")
        entete = _entete(rendu)
        if rendu.status_code != 200 or normalize(attendu) not in normalize(entete):
            constats.append(
                f"l'ecran « {etape} » (etape {numero}) repond {rendu.status_code} et son en-tete "
                f"vaut « {entete} » ; attendu le titre « {attendu} » rendu par la ligne d'en-tete de "
                f"/optimize/wizard/{etape}, construit par {SOURCE_ROUTES}"
            )
        titres.append((numero, etape, attendu))

    numerotees = [
        ligne for ligne in corps.splitlines() if re.match(r"^\d+\.\s", ligne.strip())
    ]
    if len(numerotees) != len(WIZARD_STEPS):
        constats.append(
            f"{PAGE} : la section « {TITRE_ETAPES} » porte {len(numerotees)} ligne(s) numerotee(s) "
            f"pour {len(WIZARD_STEPS)} etape(s) listee(s) par {SOURCE_WIZARD} (WIZARD_STEPS) ; "
            f"attendu {MOTIF_ORDRE_ETAPES}"
        )

    position = -1
    for numero, etape, attendu in titres:
        index = corps_normalise.find(normalize(attendu))
        if index < 0:
            constats.append(
                f"{PAGE} : le titre rendu de l'etape {numero} (« {attendu} ») de "
                f"/optimize/wizard/{etape} n'est pas cite par la section « {TITRE_ETAPES} » ; attendu "
                f"ce titre, lu au rendu et produit par {SOURCE_WIZARD} (STEP_TITLES), dans "
                f"l'{MOTIF_ORDRE_ETAPES}"
            )
            continue
        if index < position:
            constats.append(
                f"{PAGE} : le titre « {attendu} » de l'etape {numero} ({etape}) apparait avant le "
                f"titre de l'etape precedente ; attendu l'{MOTIF_ORDRE_ETAPES} — les "
                f"{len(WIZARD_STEPS)} titres cites dans l'ordre du code ({SOURCE_WIZARD}, "
                f"WIZARD_STEPS) et rendus par {SOURCE_ROUTES}"
            )
            continue
        position = index

    assert not constats, (
        f"{PAGE} : constats sur l'ordre des etapes : "
        + " ; ".join(constats)
        + f" ; attendu les {len(WIZARD_STEPS)} titres rendus cites dans l'{MOTIF_ORDRE_ETAPES}, "
        f"relu dans {SOURCE_WIZARD} et confronte au rendu de {SOURCE_ROUTES}"
    )


def test_slots_et_filtres_ancres_au_rendu(docs_dir: Path, app, normalize, section) -> None:
    """Les emplacements et les filtres cites par la page sont ceux du rendu, numerotes (D-53).

    L'ecran `slots` est rendu sur ses **deux** pages : son corps compte plus de 18 lignes
    (`BODY_LINES`, `dofus_stuff/web/screens.py:10`), les onze emplacements tiennent en page 1 mais
    les derniers filtres ne sont lisibles qu'en page 2. Les couples `(numero, libelle)` et
    `(F<n>, libelle)` sont extraits du corps rendu, puis exiges de la page a l'identique. Le couple
    `F6`/`F7` est en plus adosse a ses deux sources publiques — `TYPE_FILTER_KEYS[5]`/`[6]`
    (`dofus_stuff/model/solver_spec.py:42-53`) apparies a `TYPE_FILTER_LABELS`
    (`dofus_stuff/web/optimize_wizard.py:111-121`) — pour que la permutation des deux libelles ne
    puisse pas passer.
    """
    texte = _texte_page(docs_dir)
    corps_page = section(texte, TITRE_SLOTS, PAGE)
    constats: list[str] = []

    client = app.test_client()
    ecran = client.get("/optimize/wizard/slots")
    ecran_page2 = client.get("/optimize/wizard/slots?page=2")
    lignes = _lignes_du_corps(ecran) + _lignes_du_corps(ecran_page2)
    rendus_slots = _emplacements_du_rendu(lignes)
    rendus_filtres = _filtres_du_rendu(lignes)

    if ecran.status_code != 200 or ecran_page2.status_code != 200:
        constats.append(
            f"l'ecran /optimize/wizard/slots repond {ecran.status_code} en page 1 et "
            f"{ecran_page2.status_code} en page 2 ; attendu 200 sur les deux, cet ecran etant rendu "
            f"par {SOURCE_ROUTES}"
        )
    if len(rendus_slots) != len(SLOT_GROUPS):
        constats.append(
            f"le rendu de /optimize/wizard/slots porte {len(rendus_slots)} emplacement(s) numerote(s) "
            f"pour {len(SLOT_GROUPS)} groupe(s) de {SOURCE_SPEC} (SLOT_GROUPS) ; attendu autant "
            f"d'emplacements rendus que de groupes, le corps etant lu sur ses deux pages"
        )
    if len(rendus_filtres) != len(TYPE_FILTER_KEYS):
        constats.append(
            f"le rendu de /optimize/wizard/slots porte {len(rendus_filtres)} filtre(s) numerote(s) "
            f"pour {len(TYPE_FILTER_KEYS)} touche(s) de {SOURCE_SPEC} (TYPE_FILTER_KEYS) ; attendu "
            f"autant de filtres rendus que de touches, le corps etant lu sur ses deux pages"
        )

    # 1. Les invites et le rappel de touches, lus au rendu puis exiges de la page.
    for motif, invite in (
        (MOTIF_INVITE_EMPLACEMENTS, "SLOTS (N=TOGGLE) :"),
        (MOTIF_INVITE_FILTRES, "FILTRES TYPES (F+N) :"),
        (MOTIF_RAPPEL_TOUCHES, "N=TOGGLE SLOT  FN=TOGGLE FILTRE"),
    ):
        ligne_rendue = next((ligne.strip() for ligne in lignes if motif.match(ligne.strip())), "")
        if not ligne_rendue:
            constats.append(
                f"la ligne « {invite} » est absente du rendu de /optimize/wizard/slots ; attendu "
                f"cet intitule, ecrit par {SOURCE_WIZARD} (body_slots)"
            )
            continue
        if normalize(ligne_rendue) not in normalize(texte):
            constats.append(
                f"{PAGE} : l'intitule rendu « {ligne_rendue} » n'est pas cite par la page ; attendu "
                f"cet intitule, lu au rendu et ecrit par {SOURCE_WIZARD} (body_slots)"
            )

    # 2. Les onze emplacements, numero par numero.
    cites_slots = _couples_de_table(_sous_section(corps_page, SOUS_TITRE_EMPLACEMENTS), MOTIF_LIGNE_EMPLACEMENT)
    for numero in sorted(set(rendus_slots) | set(cites_slots)):
        rendu = rendus_slots.get(numero, "")
        cite = cites_slots.get(numero, "")
        if normalize(rendu) != normalize(cite):
            constats.append(
                f"{PAGE} : emplacement {numero} — la section cite « {cite} » et le rendu associe le "
                f"numero {numero} a « {rendu} » ; attendu le libelle rendu par {SOURCE_WIZARD} "
                f"(SLOT_GROUP_LABELS), sur l'ordre de {SOURCE_SPEC} (SLOT_GROUPS)"
            )

    # 3. Les dix filtres, touche par touche.
    cites_filtres = _couples_de_table(_sous_section(corps_page, SOUS_TITRE_FILTRES), MOTIF_LIGNE_FILTRE)
    for numero in sorted(set(rendus_filtres) | set(cites_filtres)):
        rendu = rendus_filtres.get(numero, "")
        cite = cites_filtres.get(numero, "")
        if normalize(rendu) != normalize(cite):
            constats.append(
                f"{PAGE} : filtre F{numero} — la section cite « {cite} » et le rendu associe F{numero} "
                f"a « {rendu} » ; attendu le couple (F{numero}, libelle) rendu par {SOURCE_WIZARD} "
                f"(TYPE_FILTER_LABELS)"
            )

    # 4. Seconde source du couple F6/F7, lue au code et jamais ecrite de memoire.
    for index in (5, 6):
        cle = TYPE_FILTER_KEYS[index]
        numero = index + 1
        attendu = TYPE_FILTER_LABELS.get(cle, cle.upper())
        cite = cites_filtres.get(numero, "")
        if normalize(cite) != normalize(attendu):
            constats.append(
                f"{PAGE} : F{numero} — {SOURCE_SPEC} donne TYPE_FILTER_KEYS[{index}] = « {cle} » et "
                f"{SOURCE_WIZARD} associe cette cle a « {attendu} » dans TYPE_FILTER_LABELS, alors "
                f"que la section cite « {cite} » ; attendu le couple lu au rendu et au code"
            )

    # 5. Les refus mesures, exiges de la page : le message rendu est la seule source.
    refus = (
        (("abc",), "SAISIE INVALIDE"),
        (("F11",), "FILTRE INVALIDE"),
    )
    for saisies, message_attendu in refus:
        client_refus = app.test_client()
        statut = ""
        for saisie in saisies:
            reponse = client_refus.post(
                "/optimize/wizard/slots", data={"cmd": saisie}, follow_redirects=True
            )
            statut = _statut(reponse)
        if normalize(message_attendu) not in normalize(statut):
            constats.append(
                f"la saisie « {saisies[-1]} » rend « {statut} » ; attendu le message "
                f"« {message_attendu} » dans la ligne de statut, ecrit par {SOURCE_ROUTES} "
                f"(apply_slots_input)"
            )
        if normalize(message_attendu) not in normalize(texte):
            constats.append(
                f"{PAGE} : le message de refus rendu « {message_attendu} » n'est pas cite par la "
                f"page ; attendu ce message, lu au rendu et ecrit par {SOURCE_WIZARD} "
                f"(apply_slots_input)"
            )

    # 6. Le dernier emplacement actif ne peut pas etre desactive : les onze numeros sont bascules,
    #    puis le dernier emplacement encore actif est bascule a son tour.
    client_dernier = app.test_client()
    statut = ""
    for numero in range(1, len(rendus_slots) + 1):
        reponse = client_dernier.post(
            "/optimize/wizard/slots", data={"cmd": str(numero)}, follow_redirects=True
        )
        statut = _statut(reponse)
    reponse = client_dernier.post("/optimize/wizard/slots", data={"cmd": "8"}, follow_redirects=True)
    statut = _statut(reponse)
    if normalize("AU MOINS UN SLOT REQUIS") not in normalize(statut):
        constats.append(
            f"desactiver le dernier emplacement actif rend « {statut} » (apres {len(rendus_slots)} "
            f"bascule(s) et une derniere) ; attendu le message « AU MOINS UN SLOT REQUIS », ecrit par "
            f"{SOURCE_WIZARD} (apply_slots_input)"
        )
    if normalize("AU MOINS UN SLOT REQUIS") not in normalize(texte):
        constats.append(
            f"{PAGE} : le message rendu « AU MOINS UN SLOT REQUIS » n'est pas cite par la page ; "
            f"attendu ce message, lu au rendu et ecrit par {SOURCE_WIZARD} (apply_slots_input)"
        )

    assert not constats, (
        f"{PAGE} : constats sur les slots et les filtres : "
        + " ; ".join(constats)
        + f" ; attendu les {len(SLOT_GROUPS)} emplacements et les {len(TYPE_FILTER_KEYS)} filtres "
        f"cites avec le numero et le libelle rendus par {SOURCE_WIZARD} et {SOURCE_SPEC}"
    )


def test_options_solveur_ancres_au_rendu(docs_dir: Path, app, normalize, section) -> None:
    """Les options citees par la page sont celles du rendu, et leurs refus ceux du code (D-19).

    Le compte des options est lu **au rendu**, jamais dans une table locale : la liste des options
    n'expose aucune constante publique (`dofus_stuff/web/optimize_wizard.py`). Le sous-ecran
    d'edition est reconnu a ce que le rendu porte vraiment — code de programme de l'en-tete, libelle
    de saisie, longueur maximale **lue dans la balise du champ** — et les deux comportements de
    numeros sont mesures : ouvrir une option d'edition passe par ce sous-ecran, basculer une option a
    valeur immediate rend un autre message. Aucune saisie `GO` : elle lancerait le solveur.
    """
    texte = _texte_page(docs_dir)
    texte_normalise = normalize(texte)
    corps_page = section(texte, TITRE_OPTIONS, PAGE)
    constats: list[str] = []

    client = app.test_client()
    ecran = client.get("/optimize/wizard/options")
    if ecran.status_code != 200:
        constats.append(
            f"/optimize/wizard/options repond {ecran.status_code} ; attendu 200, cet ecran etant "
            f"rendu par {SOURCE_ROUTES}"
        )
    lignes = _lignes_du_corps(ecran)
    rendues = _options_du_rendu(lignes)
    if not rendues:
        constats.append(
            f"aucune option numerotee n'est lisible dans le corps rendu de "
            f"/optimize/wizard/options ; attendu les options numerotees rendues par {SOURCE_WIZARD}"
        )
    else:
        numeros = sorted(rendues)
        if numeros != list(range(1, len(numeros) + 1)):
            constats.append(
                f"le rendu de /optimize/wizard/options porte les numeros {numeros} ; attendu des "
                f"options numerotees de 1 a {len(numeros)} sans trou, telles que {SOURCE_WIZARD} "
                f"les ecrit"
            )

    cites = _couples_de_table(corps_page, MOTIF_LIGNE_OPTION)
    if len(cites) != len(rendues):
        constats.append(
            f"{PAGE} : la section « {TITRE_OPTIONS} » cite {len(cites)} option(s) pour "
            f"{len(rendues)} rendue(s) par /optimize/wizard/options ; attendu autant d'options "
            f"citees que rendues, le compte etant lu au rendu ({SOURCE_WIZARD})"
        )
    for numero in sorted(set(rendues) | set(cites)):
        rendu = rendues.get(numero, "")
        cite = cites.get(numero, "")
        if normalize(rendu) != normalize(cite):
            constats.append(
                f"{PAGE} : option {numero} — la section cite « {cite} » et le rendu associe le "
                f"numero {numero} a « {rendu} » ; attendu le libelle rendu par {SOURCE_WIZARD}"
            )

    for motif, invite in (
        (MOTIF_INVITE_OPTIONS, "OPTIONS (N=EDIT) :"),
        (MOTIF_RAPPEL_OPTIONS, "N=CHOISIR OPTION"),
    ):
        ligne_rendue = next((ligne.strip() for ligne in lignes if motif.match(ligne.strip())), "")
        if not ligne_rendue:
            constats.append(
                f"la ligne « {invite} » est absente du rendu de /optimize/wizard/options ; attendu "
                f"cet intitule, ecrit par {SOURCE_WIZARD}"
            )
        elif normalize(invite) not in texte_normalise:
            constats.append(
                f"{PAGE} : l'intitule rendu « {invite} » n'est pas cite par la page ; attendu cet "
                f"intitule, lu au rendu et ecrit par {SOURCE_WIZARD}"
            )

    # Le sous-ecran d'edition, atteint par le rendu : ouvrir la premiere option d'edition.
    sous_ecran = app.test_client()
    sous_ecran.post("/optimize/wizard/options", data={"cmd": "1"}, follow_redirects=True)
    ecran_sous = sous_ecran.get("/optimize/wizard/options")
    lignes_sous = _lignes_du_corps(ecran_sous)
    entete_sous = _entete(ecran_sous)
    if normalize("OPT-WED") not in normalize(entete_sous):
        constats.append(
            f"l'en-tete du sous-ecran d'edition ouvert par la saisie « 1 » vaut « {entete_sous} » ; "
            f"attendu le code de programme « OPT-WED » rendu par {SOURCE_ROUTES}"
        )
    if normalize("OPT-WED") not in texte_normalise:
        constats.append(
            f"{PAGE} : le sous-ecran d'edition est annonce par « OPT-WED » et ce code n'est pas "
            f"cite par la page ; attendu le code rendu par {SOURCE_ROUTES}"
        )
    libelle = _libelle_saisie(ecran_sous)
    if normalize("VAL") not in normalize(libelle):
        constats.append(
            f"le libelle du champ de saisie du sous-ecran vaut « {libelle} » ; attendu un libelle "
            f"portant « VAL », ecrit par {SOURCE_ROUTES}"
        )
    if "VAL" not in texte:
        constats.append(
            f"{PAGE} : le libelle de saisie rendu « {libelle} » n'est pas cite par la page ; attendu "
            f"le libelle du champ, ecrit par {SOURCE_ROUTES}"
        )
    champ = _champ_saisie(ecran_sous)
    longueur = champ.get("maxlength", "")
    if longueur != "20":
        constats.append(
            f"la balise du champ du sous-ecran porte maxlength=« {longueur} » ; attendu la longueur "
            f"maximale rendue par {SOURCE_ROUTES}, lue dans la balise du champ"
        )
    if "maxlength=20" not in texte:
        constats.append(
            f"{PAGE} : le champ du sous-ecran est limite a maxlength={longueur} et cette limite "
            f"n'est pas citee par la page ; attendu la limite rendue par {SOURCE_ROUTES}"
        )

    reponse = sous_ecran.post("/optimize/wizard/options", data={"value": "300"}, follow_redirects=True)
    statut = _statut(reponse)
    if normalize("VALEUR ENREGISTREE") not in normalize(statut):
        constats.append(
            f"enregistrer une valeur dans le sous-ecran d'edition rend « {statut} » ; attendu le "
            f"message « VALEUR ENREGISTREE », ecrit par {SOURCE_ROUTES}"
        )
    if normalize("VALEUR ENREGISTREE") not in texte_normalise:
        constats.append(
            f"{PAGE} : le message rendu « VALEUR ENREGISTREE » n'est pas cite par la page ; attendu "
            f"ce message, ecrit par {SOURCE_ROUTES}"
        )

    for numero in (6, 11):
        bascule = app.test_client()
        reponse = bascule.post(
            "/optimize/wizard/options", data={"cmd": str(numero)}, follow_redirects=True
        )
        statut = _statut(reponse)
        if normalize("OPTION MISE A JOUR") not in normalize(statut):
            constats.append(
                f"la saisie « {numero} » sur /optimize/wizard/options rend « {statut} » ; attendu le "
                f"message « OPTION MISE A JOUR » d'une bascule immediate, ecrit par {SOURCE_WIZARD}"
            )
    if normalize("OPTION MISE A JOUR") not in texte_normalise:
        constats.append(
            f"{PAGE} : le message rendu « OPTION MISE A JOUR » n'est pas cite par la page ; attendu "
            f"ce message, lu au rendu et ecrit par {SOURCE_WIZARD}"
        )

    for saisie, message in (("12", "OPTION INVALIDE"), ("abc", "SAISIR UN NUMERO D'OPTION")):
        refus = app.test_client()
        reponse = refus.post("/optimize/wizard/options", data={"cmd": saisie}, follow_redirects=True)
        statut = _statut(reponse)
        if normalize(message) not in normalize(statut):
            constats.append(
                f"la saisie « {saisie} » rend « {statut} » ; attendu le message « {message} » dans la "
                f"ligne de statut, ecrit par {SOURCE_WIZARD}"
            )
        if normalize(message) not in texte_normalise:
            constats.append(
                f"{PAGE} : le message de refus rendu « {message} » n'est pas cite par la page ; "
                f"attendu ce message, lu au rendu et ecrit par {SOURCE_WIZARD}"
            )

    assert not constats, (
        f"{PAGE} : constats sur les options du solveur : "
        + " ; ".join(constats)
        + f" ; attendu les options rendues par {SOURCE_WIZARD} citees par la section "
        f"« {TITRE_OPTIONS} », avec le sous-ecran d'edition et les refus rendus par {SOURCE_ROUTES}"
    )


def test_formats_d_edition_et_refus_reels(docs_dir: Path, app, normalize, section) -> None:
    """La page cite chaque forme d'edition avec son ecran, et le refus de format est celui du rendu.

    Deux ecrans d'edition seulement portent une forme differente : les caracteristiques et les
    objectifs de PA / PM / PO. Le controle atteint **les deux** sous-ecrans par le rendu, lit leur
    ligne de forme et l'associe a l'ecran qui la porte, puis verifie que les deux formes marquees ne
    sont pas la meme : deux formes echangees ne peuvent donc pas passer. Le refus de format est
    mesure, pas deduit : une saisie qui ne porte pas quatre nombres rend le message de la forme de
    l'ecran, et ce message est celui de la forme affichee juste au-dessus.
    """
    texte = _texte_page(docs_dir)
    texte_normalise = normalize(texte)
    corps_page = section(texte, TITRE_NOMBRES, PAGE)
    constats: list[str] = []

    formes_citees = _couples_texte(corps_page, MOTIF_LIGNE_FORMAT)
    if not formes_citees:
        constats.append(
            f"{PAGE} : la section « {TITRE_NOMBRES} » ne cite aucune forme d'edition ; attendu une "
            f"ligne de tableau par forme, avec l'ecran qui la porte ({SOURCE_WIZARD})"
        )

    mesures: dict[str, tuple[object, str]] = {}
    for etape in ("caracs", "papmpo"):
        client = app.test_client()
        client.post(f"/optimize/wizard/{etape}", data={"cmd": "1"}, follow_redirects=True)
        ecran = client.get(f"/optimize/wizard/{etape}")
        if ecran.status_code != 200:
            constats.append(
                f"/optimize/wizard/{etape} repond {ecran.status_code} apres la saisie « 1 » ; attendu "
                f"200, cet ecran etant rendu par {SOURCE_ROUTES}"
            )
        forme = _forme_d_edition(_lignes_du_corps(ecran))
        mesures[etape] = (client, forme)
        titre = STEP_TITLES.get(etape, "")
        if not forme:
            constats.append(
                f"le sous-ecran d'edition de /optimize/wizard/{etape} ne porte aucune ligne de forme ; "
                f"attendu la forme rendue par {SOURCE_WIZARD}, lue apres la saisie « 1 »"
            )
            continue
        if normalize(forme) not in texte_normalise:
            constats.append(
                f"{PAGE} : la forme rendue par le sous-ecran de {etape} vaut « {forme} » et n'est pas "
                f"citee par la page ; attendu cette forme, lue au rendu ({SOURCE_WIZARD})"
            )
        cite = formes_citees.get(titre, "")
        if normalize(cite) != normalize(forme):
            constats.append(
                f"{PAGE} : l'ecran « {titre} » — la section cite « {cite} » et le sous-ecran atteint "
                f"par {etape} rend « {forme} » ; attendu chaque forme avec l'ecran qui la porte, "
                f"jamais deux formes echangees ({SOURCE_WIZARD})"
            )

    formes = {normalize(forme) for _, forme in mesures.values() if forme}
    if len(formes) != len(mesures):
        constats.append(
            f"{PAGE} : les {len(mesures)} sous-ecrans mesures rendent {len(formes)} forme(s) "
            f"distincte(s) ({', '.join(sorted(formes))}) ; attendu une forme par ecran, les deux "
            f"formes n'etant jamais fusionnees ({SOURCE_WIZARD})"
        )

    for etape, (client, forme) in mesures.items():
        reponse = client.post(
            f"/optimize/wizard/{etape}", data={"value": "1 2 3"}, follow_redirects=True
        )
        message = _message_de_statut(_statut(reponse))
        if normalize(forme) not in normalize(message):
            constats.append(
                f"{PAGE} : sur {etape}, une saisie de trois valeurs rend « {message} » et la forme du "
                f"sous-ecran vaut « {forme} » ; attendu le message de refus du format, identique a la "
                f"forme affichee juste au-dessus ({SOURCE_ROUTES})"
            )

    lignes_liste = _lignes_du_corps(app.test_client().get("/optimize/wizard/caracs"))
    if not any(ligne.strip().startswith("N=EDIT") for ligne in lignes_liste):
        constats.append(
            "la ligne « N=EDIT » est absente du rendu de /optimize/wizard/caracs ; attendu cet "
            f"intitule, ecrit par {SOURCE_WIZARD}"
        )
    if "N=EDIT" not in texte:
        constats.append(
            f"{PAGE} : l'intitule rendu « N=EDIT » n'est pas cite par la page ; attendu cet intitule, "
            f"ecrit par {SOURCE_WIZARD}"
        )

    for saisie, message in (("abc", "SAISIR LE NUMERO DE LA LIGNE"), ("99", "NUMERO INVALIDE")):
        refus = app.test_client()
        reponse = refus.post("/optimize/wizard/caracs", data={"cmd": saisie}, follow_redirects=True)
        statut = _statut(reponse)
        if normalize(message) not in normalize(statut):
            constats.append(
                f"la saisie « {saisie} » sur /optimize/wizard/caracs rend « {statut} » ; attendu le "
                f"message « {message} » dans la ligne de statut, ecrit par {SOURCE_WIZARD}"
            )
        if normalize(message) not in texte_normalise:
            constats.append(
                f"{PAGE} : le message rendu « {message} » n'est pas cite par la page ; attendu ce "
                f"message, lu au rendu et ecrit par {SOURCE_WIZARD}"
            )

    for separateur in (" ", ","):
        valeur = separateur.join(("1", "2", "3", "4"))
        valide = app.test_client()
        valide.post("/optimize/wizard/caracs", data={"cmd": "4"}, follow_redirects=True)
        reponse = valide.post(
            "/optimize/wizard/caracs", data={"value": valeur}, follow_redirects=True
        )
        statut = _statut(reponse)
        if normalize("CARAC ENREGISTREE") not in normalize(statut):
            constats.append(
                f"enregistrer la valeur « {valeur} » rend « {statut} » ; attendu le message "
                f"« CARAC ENREGISTREE » d'une saisie de quatre nombres, ecrit par {SOURCE_ROUTES}"
            )
    if normalize("CARAC ENREGISTREE") not in texte_normalise:
        constats.append(
            f"{PAGE} : le message rendu « CARAC ENREGISTREE » n'est pas cite par la page ; attendu ce "
            f"message, lu au rendu et ecrit par {SOURCE_WIZARD}"
        )

    assert not constats, (
        f"{PAGE} : constats sur les formes d'edition : "
        + " ; ".join(constats)
        + f" ; attendu chaque forme d'edition citee avec son ecran par la section "
        f"« {TITRE_NOMBRES} », les deux formes jamais fusionnees, et les messages d'edition rendus par "
        f"{SOURCE_ROUTES}"
    )


def test_syntaxe_d_items_et_etat_vide(docs_dir: Path, app, normalize, section) -> None:
    """La syntaxe des items citee par la page est celle du rendu, et l'etat vide est celui du code.

    Les quatre lignes de syntaxe sont appariees **prefixe par prefixe** : la page les cite sous forme
    de tableau, la comparaison porte donc sur le couple et jamais sur une ligne entiere — c'est ce qui
    rend une permutation de verbes visible. Le seul refus est mesure : une saisie sans prefixe est
    refusee, alors que `+ID` ne l'est pas. L'etat vide est lu au rendu puis confronte a la phrase qui
    le cite, sur un client neuf comme apres vidage, et la troncature annoncee est mesuree sur une
    liste de plus de huit entrees.
    """
    texte = _texte_page(docs_dir)
    texte_normalise = normalize(texte)
    corps_page = section(texte, TITRE_ITEMS, PAGE)
    constats: list[str] = []

    client = app.test_client()
    ecran = client.get("/optimize/wizard/items")
    if ecran.status_code != 200:
        constats.append(
            f"/optimize/wizard/items repond {ecran.status_code} ; attendu 200, cet ecran etant rendu "
            f"par {SOURCE_ROUTES}"
        )
    lignes = _lignes_du_corps(ecran)
    rendues = _syntaxe_du_rendu(lignes)
    attendues = ("+ID", "-ID", "!ID", "CLEAR")
    if sorted(rendues) != sorted(attendues):
        constats.append(
            f"le rendu de /optimize/wizard/items porte les saisies {sorted(rendues)} ; attendu les "
            f"quatre saisies {sorted(attendues)} ecrites par {SOURCE_WIZARD}"
        )

    cites = _couples_texte(corps_page, MOTIF_LIGNE_SYNTAXE_ITEMS)
    if len(cites) != len(rendues):
        constats.append(
            f"{PAGE} : la section « {TITRE_ITEMS} » cite {len(cites)} saisie(s) pour {len(rendues)} "
            f"ligne(s) de syntaxe rendue(s) ; attendu autant de saisies citees que de lignes rendues "
            f"({SOURCE_WIZARD})"
        )
    for prefixe in sorted(set(rendues) | set(cites)):
        verbe_rendu = rendues.get(prefixe, "")
        verbe_cite = cites.get(prefixe, "")
        if normalize(verbe_rendu) != normalize(verbe_cite):
            constats.append(
                f"{PAGE} : la saisie « {prefixe} » — la page annonce « {verbe_cite} » et l'ecran rend "
                f"« {verbe_rendu} » ; attendu le verbe rendu par {SOURCE_WIZARD}"
            )

    trouve = MOTIF_ETAT_VIDE_CITE.search(corps_page)
    etat_cite = trouve.group("etat") if trouve is not None else ""
    if not etat_cite:
        constats.append(
            f"{PAGE} : la section « {TITRE_ITEMS} » ne cite aucun etat vide ; attendu l'etat rendu par "
            f"{SOURCE_WIZARD} pour une liste sans entree"
        )
    etats_neuf = _listes_du_rendu(lignes)
    for nom in ("INTERDITS", "FORCES"):
        if nom not in etats_neuf:
            constats.append(
                f"la liste {nom} n'est pas lisible dans le rendu de /optimize/wizard/items ; attendu "
                f"les deux listes rendues par {SOURCE_WIZARD}"
            )
            continue
        if normalize(etats_neuf[nom]) != normalize(etat_cite):
            constats.append(
                f"{PAGE} : la section cite l'etat vide « {etat_cite} » et le rendu rend "
                f"« {etats_neuf[nom]} » pour la liste {nom} sur un client neuf ; attendu l'etat vide "
                f"ecrit par {SOURCE_WIZARD}"
            )
    vide_interdits = etats_neuf.get("INTERDITS", "")
    vide_forces = etats_neuf.get("FORCES", "")

    ajout = app.test_client()
    reponse = ajout.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
    etats = _listes_du_rendu(_lignes_du_corps(reponse))
    if "#12345" not in etats.get("INTERDITS", ""):
        constats.append(
            f"la saisie « +12345 » rend la liste INTERDITS « {etats.get('INTERDITS', '')} » ; attendu "
            f"l'objet ajoute aux interdits, comme l'annonce {SOURCE_WIZARD}"
        )
    if normalize(etats.get("FORCES", "")) != normalize(vide_forces):
        constats.append(
            f"la saisie « +12345 » rend la liste FORCES « {etats.get('FORCES', '')} » ; attendu une "
            f"liste de forces vide « {vide_forces} », l'objet n'etant jamais dans les deux listes "
            f"({SOURCE_WIZARD})"
        )

    deplace = app.test_client()
    deplace.post("/optimize/wizard/items", data={"cmd": "-12345"}, follow_redirects=True)
    reponse = deplace.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
    etats = _listes_du_rendu(_lignes_du_corps(reponse))
    if "#12345" not in etats.get("INTERDITS", "") or normalize(
        etats.get("FORCES", "")
    ) != normalize(vide_forces):
        constats.append(
            f"apres « -12345 » puis « +12345 », le rendu porte INTERDITS "
            f"« {etats.get('INTERDITS', '')} » et FORCES « {etats.get('FORCES', '')} » ; attendu "
            f"l'objet deplace d'une liste a l'autre, un objet n'etant jamais interdit et force en "
            f"meme temps ({SOURCE_WIZARD})"
        )

    retrait = app.test_client()
    retrait.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
    reponse = retrait.post("/optimize/wizard/items", data={"cmd": "!12345"}, follow_redirects=True)
    etats = _listes_du_rendu(_lignes_du_corps(reponse))
    if normalize(etats.get("INTERDITS", "")) != normalize(vide_interdits):
        constats.append(
            f"apres « !12345 », le rendu porte INTERDITS « {etats.get('INTERDITS', '')} » ; attendu "
            f"une liste d'interdits vide « {vide_interdits} », l'objet etant retire des deux listes "
            f"({SOURCE_WIZARD})"
        )

    for saisie in ("CLEAR", "clear"):
        vidage = app.test_client()
        vidage.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
        vidage.post("/optimize/wizard/items", data={"cmd": "-12345"}, follow_redirects=True)
        reponse = vidage.post("/optimize/wizard/items", data={"cmd": saisie}, follow_redirects=True)
        etats = _listes_du_rendu(_lignes_du_corps(reponse))
        for nom, reference in (("INTERDITS", vide_interdits), ("FORCES", vide_forces)):
            if normalize(etats.get(nom, "")) != normalize(reference):
                constats.append(
                    f"apres « {saisie} », le rendu porte {nom} « {etats.get(nom, '')} » ; attendu une "
                    f"liste vide « {reference} », la saisie vidant les deux listes ({SOURCE_WIZARD})"
                )

    espace = app.test_client()
    reponse = espace.post("/optimize/wizard/items", data={"cmd": "  +12345  "}, follow_redirects=True)
    etats = _listes_du_rendu(_lignes_du_corps(reponse))
    if "#12345" not in etats.get("INTERDITS", ""):
        constats.append(
            f"la saisie «   +12345   » rend INTERDITS « {etats.get('INTERDITS', '')} » ; attendu "
            f"l'objet ajoute comme pour une saisie sans espaces, les espaces etant ignores "
            f"({SOURCE_ROUTES})"
        )

    ajoutes = [f"+{identifiant}" for identifiant in range(20001, 20011)]
    troncature = app.test_client()
    for saisie in ajoutes:
        reponse = troncature.post(
            "/optimize/wizard/items", data={"cmd": saisie}, follow_redirects=True
        )
    lignes_tronquees = _lignes_du_corps(reponse)
    etats = _listes_du_rendu(lignes_tronquees)
    affichees = [entree for entree in etats.get("INTERDITS", "").split(",") if entree.strip()]
    ellipses = [ligne.strip() for ligne in lignes_tronquees if "…" in ligne]
    if not ellipses:
        constats.append(
            f"apres {len(ajoutes)} ajouts, aucune ligne d'ellipse n'est rendue pour INTERDITS "
            f"(contenu affiche « {etats.get('INTERDITS', '')} ») ; attendu la troncature de "
            f"l'affichage au-dela de huit entrees, ecrite par {SOURCE_WIZARD}"
        )
    elif len(affichees) >= len(ajoutes):
        constats.append(
            f"apres {len(ajoutes)} ajouts, le rendu affiche {len(affichees)} entree(s) d'INTERDITS et "
            f"la ligne d'ellipse « {ellipses[0]} » ; attendu une liste affichee plus courte que la "
            f"liste complete, la suite etant resumees par l'ellipse ({SOURCE_WIZARD})"
        )
    else:
        cache = re.search(r"\+(\d+)", ellipses[0])
        if cache is None or len(affichees) + int(cache.group(1)) != len(ajoutes):
            constats.append(
                f"apres {len(ajoutes)} ajouts, le rendu affiche {len(affichees)} entree(s) et la ligne "
                f"« {ellipses[0]} » ; attendu le nombre d'entrees cachees annonce, la somme devant "
                f"donner les {len(ajoutes)} saisies ajoutees ({SOURCE_WIZARD})"
            )

    refus = app.test_client()
    reponse = refus.post("/optimize/wizard/items", data={"cmd": "12345"}, follow_redirects=True)
    message = _message_de_statut(_statut(reponse))
    if not message:
        constats.append(
            "la saisie « 12345 » sur /optimize/wizard/items ne rend aucun message dans la ligne de "
            f"statut ; attendu le message de syntaxe ecrit par {SOURCE_WIZARD}"
        )
    elif normalize(message) not in texte_normalise:
        constats.append(
            f"{PAGE} : le refus rendu « {message} » n'est pas cite par la page ; attendu le message de "
            f"syntaxe ecrit par {SOURCE_WIZARD}"
        )
    plus = app.test_client()
    reponse = plus.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
    if message and normalize(message) in normalize(_statut(reponse)):
        constats.append(
            f"la saisie « +12345 » rend « {_statut(reponse)} » ; attendu un ajout et non le refus "
            f"« {message} », la saisie prefixee etant un verbe d'ajout et non une saisie interdite "
            f"({SOURCE_WIZARD})"
        )

    assert not constats, (
        f"{PAGE} : constats sur la syntaxe des items : "
        + " ; ".join(constats)
        + f" ; attendu les quatre saisies rendues par {SOURCE_WIZARD} citees avec leur verbe par la "
        f"section « {TITRE_ITEMS} », avec le seul refus et l'etat vide rendus par {SOURCE_ROUTES}"
    )


def test_page_sans_derive_ni_chemin_invente(
    docs_dir: Path, normalize, sections, section
) -> None:
    """La page tient sa forme de bout en bout : titres, H1, retour au sommaire, encodage, chemins.

    Le controle des chemins est le plus utile : tout chemin de code cite entre accents graves doit
    exister sur le disque. Une page qui nomme un fichier disparu (renommage, deplacement) fait donc
    rougir la suite, ce qu'aucune relecture ne garantit. Les titres sont exiges dans l'ordre et leur
    nombre est fixe : une section ajoutee sans controle se voit ici, et non au prochain plan.
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page du wizard avance, decrite par "
            f"{SOURCE_WIZARD}"
        )
    octets = chemin.read_bytes()
    texte = octets.decode("utf-8")
    constats: list[str] = []

    titres = [titre for titre, _ in sections(texte) if titre is not None]
    if len(titres) != len(TITRES_SECTION_ATTENDUS):
        constats.append(
            f"{PAGE} : la page porte {len(titres)} section(s) de niveau 2 ({', '.join(titres)}) ; "
            f"attendu exactement {len(TITRES_SECTION_ATTENDUS)} sections, dans cet ordre : "
            f"{', '.join(TITRES_SECTION_ATTENDUS)}"
        )
    for index, attendu in enumerate(TITRES_SECTION_ATTENDUS):
        trouve = titres[index] if index < len(titres) else ""
        if normalize(attendu.lstrip("#").strip()) != normalize(trouve):
            constats.append(
                f"{PAGE} : section {index + 1} attendue « {attendu.lstrip('#').strip()} », section "
                f"trouvee « {trouve} » ; attendu les {len(TITRES_SECTION_ATTENDUS)} sections de la "
                f"page, dans l'ordre du document"
            )

    h1 = [ligne for ligne in texte.splitlines() if ligne.startswith(FRAGMENT_H1)]
    if len(h1) != 1:
        constats.append(
            f"{PAGE} : la page porte {len(h1)} titre(s) de niveau 1 ({', '.join(h1)}) ; attendu un "
            f"seul titre de niveau 1 (D-56)"
        )

    remplies = [ligne.strip() for ligne in texte.splitlines() if ligne.strip()]
    derniere = remplies[-1] if remplies else ""
    if derniere != LIGNE_RETOUR:
        constats.append(
            f"{PAGE} : la derniere ligne non vide vaut « {derniere} » ; attendu « {LIGNE_RETOUR} » "
            f"comme derniere ligne de la page"
        )

    if BALISE_COMMANDE in texte:
        constats.append(
            f"{PAGE} : la page porte un bloc de commandes ; attendu aucun bloc de commandes, le "
            f"wizard avance n'exposant aucune commande en ligne de commande ({SOURCE_ROUTES})"
        )
    if FRAGMENT_LIEN_EXTERNE in texte:
        constats.append(
            f"{PAGE} : la page porte un lien externe ; attendu des liens internes seulement, la page "
            f"decrit le produit de ce depot"
        )

    fins = octets.count(b"\n")
    retours = octets.count(b"\r\n")
    if octets.startswith(BOM_UTF8):
        constats.append(f"{PAGE} : la page commence par un BOM ; attendu un fichier UTF-8 sans BOM")
    if retours != fins:
        constats.append(
            f"{PAGE} : la page porte {fins} fin(s) de ligne pour {retours} retour(s) chariot ; attendu "
            f"des fins de ligne CRLF sur toutes les lignes, comme les autres pages de docs/"
        )

    corps_source = section(texte, TITRE_SOURCE, PAGE)
    for source in (SOURCE_ROUTES, SOURCE_WIZARD, SOURCE_SPEC):
        if source not in corps_source:
            constats.append(
                f"{PAGE} : la section « {TITRE_SOURCE} » ne cite pas « {source} » ; attendu le bloc "
                f"« Source de verite », qui nomme les fichiers dont la page decrit la surface"
            )

    chemins = sorted(set(CHEMIN_CITE.findall(texte)))
    if not chemins:
        constats.append(
            f"{PAGE} : la page ne cite aucun chemin de code ; attendu au moins un chemin, la page "
            f"ancrant ses libelles sur le code de ce depot"
        )
    for cite in chemins:
        if not (RACINE_DEPOT / cite).exists():
            constats.append(
                f"{PAGE} : la page cite « {cite} » et ce chemin n'existe pas ; attendu un chemin "
                f"existant, un chemin disparu signalant une page desalignee"
            )

    assert not constats, (
        f"{PAGE} : constats sur la forme de la page : "
        + " ; ".join(constats)
        + f" ; attendu {len(TITRES_SECTION_ATTENDUS)} sections, un H1, la ligne de retour au sommaire, "
        f"des fins de ligne CRLF, aucun lien externe et des chemins de code existants"
    )


def test_ecrans_et_arrivee_du_wizard(docs_dir: Path, app, normalize, section) -> None:
    """Les identifiants d'ecrans et le chemin d'arrivee sont lus au rendu, puis exiges (D-51, WIZ-02).

    Le chemin d'arrivee est rejoue pas a pas sur **un seul** client : le menu poste `selection=4`,
    `/optimize` redirige vers les trois questions, et `AVANCE` ouvre le wizard. La ou l'on atterrit
    est mesure, jamais suppose : l'ecran d'arrivee est le recapitulatif, et la page le dit — c'est
    l'affirmation fausse que cette phase resorbe.

    Limite nommee (sonde d'aretes WIZ-02, ligne `unclassified`, qui reste `unresolved`) : ce controle
    porte sur les neuf couples identifiant/titre lus dans la ligne d'en-tete et sur la chaine
    d'arrivee. Il ne revendique aucune exhaustivite de la surface des touches, des messages ou des
    commandes du wizard : ce qu'il prouve est nomme, rien de plus.
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_ARRIVEE, PAGE)
    constats: list[str] = []

    # 1. Les neuf ecrans : identifiant et titre rendus dans la ligne d'en-tete, cites par la page.
    client = app.test_client()
    cites = _identifiants_cites(corps)
    for numero, etape in enumerate(WIZARD_STEPS, start=1):
        identifiant = f"OPT-W{numero}"
        rendu = client.get(f"/optimize/wizard/{etape}")
        entete = _entete(rendu)
        titre = STEP_TITLES.get(etape, "")
        if rendu.status_code != 200 or identifiant not in entete:
            constats.append(
                f"l'ecran « {etape} » (etape {numero}) repond {rendu.status_code} et sa ligne "
                f"d'en-tete vaut « {entete} » ; attendu l'{MOTIF_IDENTIFIANT_ECRAN} "
                f"« {identifiant} » dans la ligne d'en-tete rendue par {SOURCE_ROUTES}"
            )
        if normalize(titre) not in normalize(entete):
            constats.append(
                f"l'ecran « {etape} » repond {rendu.status_code} et sa ligne d'en-tete vaut "
                f"« {entete} » ; attendu le titre « {titre} » rendu par {SOURCE_WIZARD} (STEP_TITLES)"
            )
        if cites.get(etape, "") != identifiant:
            constats.append(
                f"{PAGE} : la section « {TITRE_ARRIVEE} » associe l'etape {numero} ({etape}) a "
                f"« {cites.get(etape, '')} » ; attendu l'{MOTIF_IDENTIFIANT_ECRAN} "
                f"« {identifiant} », lu dans la ligne d'en-tete rendue par {SOURCE_ROUTES}"
            )
        if normalize(titre) not in normalize(texte):
            constats.append(
                f"{PAGE} : le titre rendu de l'etape {numero} vaut « {titre} » et n'est pas cite "
                f"par la page ; attendu ce titre, lu au rendu de /optimize/wizard/{etape} et produit "
                f"par {SOURCE_WIZARD} (STEP_TITLES)"
            )

    # 2. Un ecran qui n'existe pas : le message du code, rendu sur l'ecran suivant (le menu).
    inconnu = app.test_client()
    reponse = inconnu.get("/optimize/wizard/inconnu")
    cible = reponse.headers.get("Location", "")
    if reponse.status_code != 302 or cible != "/":
        constats.append(
            f"l'ecran inconnu « inconnu » repond {reponse.status_code} vers « {cible} » ; attendu une "
            f"redirection vers le menu principal, posee par {SOURCE_ROUTES}"
        )
    message = "ECRAN WIZARD INCONNU"
    if message not in _statut(inconnu.get("/")):
        constats.append(
            f"{PAGE} : le message « {message} » n'est pas rendu sur l'ecran suivant ; attendu le refus "
            f"de {SOURCE_ROUTES} pour une etape hors de WIZARD_STEPS"
        )
    if normalize(message) not in normalize(texte):
        constats.append(
            f"{PAGE} : le message rendu « {message} » n'est pas cite par la page ; attendu ce message, "
            f"lu au rendu et produit par {SOURCE_ROUTES}"
        )

    # 3. La chaine d'arrivee, rejouee pas a pas sur un seul client.
    parcours = app.test_client()
    for methode, adresse, donnees, attendue in (
        ("POST", "/", {"selection": "4"}, "/optimize"),
        ("GET", "/optimize", None, "/optimize/quick/classe"),
        ("POST", "/optimize/quick/classe", {"cmd": "Cra"}, "/optimize/quick/elements"),
        ("POST", "/optimize/quick/elements", {"cmd": "terre"}, "/optimize/quick/niveau"),
        ("POST", "/optimize/quick/niveau", {"cmd": "avance"}, "/optimize/wizard/recap"),
    ):
        reponse = parcours.get(adresse) if methode == "GET" else parcours.post(adresse, data=donnees)
        cible = reponse.headers.get("Location", "")
        if reponse.status_code != 302 or cible != attendue:
            constats.append(
                f"{methode} {adresse} repond {reponse.status_code} vers « {cible} » ; attendu "
                f"l'{MOTIF_ARRIVEE} vers « {attendue} », construit par {SOURCE_ROUTES}"
            )
    titre_recap = STEP_TITLES.get("recap", "")
    arrivee = parcours.get("/optimize/wizard/recap")
    if arrivee.status_code != 200 or normalize(titre_recap) not in normalize(_entete(arrivee)):
        constats.append(
            f"l'ecran d'arrivee « /optimize/wizard/recap » repond {arrivee.status_code} et sa ligne "
            f"d'en-tete vaut « {_entete(arrivee)} » ; attendu le titre « {titre_recap} » — c'est lui "
            f"que l'{MOTIF_ARRIVEE} atteint, pas les emplacements ({SOURCE_ROUTES})"
        )

    # 4. Les quatre reperes du chemin, cites par la page depuis le rendu.
    entree_menu = next(
        (
            ligne.strip()
            for ligne in _lignes_du_corps(app.test_client().get("/"))
            if MOTIF_LIGNE_MENU.match(ligne)
        ),
        "",
    )
    if not entree_menu or normalize(entree_menu) not in normalize(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_ARRIVEE} » ne cite pas « {entree_menu} » ; attendu la ligne "
            f"du menu principal qui ouvre le parcours, lue au rendu de GET / et construite par "
            f"{SOURCE_ROUTES} ({MOTIF_ARRIVEE})"
        )

    questions_client = app.test_client()
    vues = [questions_client.get("/optimize/quick/classe")]
    questions_client.post("/optimize/quick/classe", data={"cmd": "Cra"})
    vues.append(questions_client.get("/optimize/quick/elements"))
    questions_client.post("/optimize/quick/elements", data={"cmd": "terre"})
    vues.append(questions_client.get("/optimize/quick/niveau"))

    questions: list[str] = []
    ligne_avance = ""
    for vue in vues:
        for ligne in _lignes_du_corps(vue):
            texte_ligne = ligne.strip()
            if MOTIF_LIGNE_QUESTION.match(texte_ligne) is not None:
                questions.append(texte_ligne)
            if MOTIF_LIGNE_AVANCE.match(texte_ligne) is not None:
                ligne_avance = texte_ligne
    if len(questions) != 3:
        constats.append(
            f"les trois questions du parcours repondent {len(questions)} ligne(s) de la forme "
            f"« N/3 - ... » ; attendu les trois questions posees par {SOURCE_ROUTES} avant le wizard "
            f"({MOTIF_ARRIVEE})"
        )
    for question in questions:
        if normalize(question) not in normalize(corps):
            constats.append(
                f"{PAGE} : la section « {TITRE_ARRIVEE} » ne cite pas la question « {question} » ; "
                f"attendu cette question, lue au rendu de /optimize/quick/<etape> par {SOURCE_ROUTES} "
                f"({MOTIF_ARRIVEE})"
            )
    if not ligne_avance or normalize(ligne_avance) not in normalize(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_ARRIVEE} » ne cite pas « {ligne_avance} » ; attendu la "
            f"ligne qui ouvre le wizard, lue au rendu des trois questions et construite par "
            f"{SOURCE_ROUTES} ({MOTIF_ARRIVEE})"
        )

    assert not constats, (
        f"{PAGE} : constats sur les ecrans et le chemin d'arrivee : "
        + " ; ".join(constats)
        + f" ; attendu les identifiants d'ecrans et l'{MOTIF_ARRIVEE} lus au rendu de {SOURCE_ROUTES}, "
        f"cites par la section « {TITRE_ARRIVEE} »"
    )


def test_exemple_guide_ancre_au_rendu(docs_dir: Path, app, normalize, section) -> None:
    """L'exemple guide migre est rejoue sur le rendu, edition par edition (D-55, WIZ-02).

    Les trois editions de l'exemple partent chacune d'un **client neuf** : un `POST` accepte reecrit
    l'etat de session, donc rejouer deux editions sur le meme client mesurerait autre chose. La ligne
    rendue apres chaque edition doit etre citee par la section de l'exemple : c'est cet ancrage qui
    fait rougir la suite si le code cesse de porter une ligne que l'exemple promet — la variante
    « cible PA » survit parce que le code la porte, jamais parce que l'ancien guide l'ecrivait.

    Aucune saisie `GO` n'est postee : elle lancerait le solveur (`{SOURCE_ROUTES}`). Seules sa
    citation, lue dans le corps du recapitulatif, et l'action des trois editions sont controlees.
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_EXEMPLE, PAGE)
    constats: list[str] = []

    # 1. Les trois editions de l'exemple : navigation depuis le recapitulatif, numero de ligne, valeur.
    for etape, chiffre, numero_ligne, valeur in (
        ("options", "2", "1", "123"),
        ("caracs", "3", "4", "300 0 0 1"),
        ("papmpo", "4", "1", "6 0 11 5"),
    ):
        adresse = f"/optimize/wizard/{etape}"
        client = app.test_client()
        client.get("/optimize/wizard/recap")
        saut = client.post("/optimize/wizard/recap", data={"cmd": chiffre})
        cible = saut.headers.get("Location", "")
        if saut.status_code != 302 or cible != adresse:
            constats.append(
                f"{PAGE} : {MOTIF_EXEMPLE} — le chiffre « {chiffre} » du recapitulatif repond "
                f"{saut.status_code} vers « {cible} » ; attendu l'ecran « {adresse} », lu dans le "
                f"rendu du recapitulatif ({SOURCE_ROUTES})"
            )
        ouverture = client.post(adresse, data={"cmd": numero_ligne})
        cible = ouverture.headers.get("Location", "")
        if ouverture.status_code != 302 or cible != adresse:
            constats.append(
                f"{PAGE} : {MOTIF_EXEMPLE} — le numero de ligne « {numero_ligne} » repond "
                f"{ouverture.status_code} vers « {cible} » ; attendu l'ouverture du sous-ecran "
                f"d'edition de « {adresse} » ({SOURCE_ROUTES})"
            )
        client.get(adresse)
        client.post(adresse, data={"value": valeur})
        rendues = [
            ligne.strip()
            for ligne in _lignes_du_corps(client.get(adresse))
            if ligne.strip().startswith(f"{numero_ligne}.")
        ]
        if not rendues:
            constats.append(
                f"{PAGE} : {MOTIF_EXEMPLE} — aucune ligne rendue ne commence par « {numero_ligne}. » "
                f"apres l'edition « {valeur} » sur « {adresse} » ; attendu la ligne editee, rendue "
                f"par {SOURCE_WIZARD}"
            )
        for ligne in rendues:
            if normalize(ligne) not in normalize(corps):
                constats.append(
                    f"{PAGE} : la section « {TITRE_EXEMPLE} » ne cite pas la ligne rendue « {ligne} » ; "
                    f"attendu cette ligne, lue apres l'edition « {valeur} » sur « {adresse} » "
                    f"({SOURCE_WIZARD})"
                )

    # 2. Le chemin d'arrivee, l'ecran d'arrivee et le libelle de lancement, cites depuis le rendu.
    ligne_avance = ""
    for ligne in _lignes_du_corps(app.test_client().get("/optimize/quick/classe")):
        if MOTIF_LIGNE_AVANCE.match(ligne.strip()) is not None:
            ligne_avance = ligne.strip()
    if not ligne_avance or normalize(ligne_avance) not in normalize(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_EXEMPLE} » ne cite pas « {ligne_avance} » ; attendu la "
            f"ligne qui ouvre le wizard, lue au rendu des trois questions ({SOURCE_ROUTES})"
        )

    recap = app.test_client().get("/optimize/wizard/recap")
    titre_recap = STEP_TITLES.get("recap", "")
    if recap.status_code != 200 or normalize(titre_recap) not in normalize(_entete(recap)):
        constats.append(
            f"l'ecran d'arrivee « /optimize/wizard/recap » repond {recap.status_code} ; attendu le "
            f"titre « {titre_recap} » — c'est l'ecran que l'exemple annonce ({SOURCE_ROUTES})"
        )
    if normalize(titre_recap) not in normalize(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_EXEMPLE} » ne cite pas l'ecran d'arrivee « {titre_recap} » ; "
            f"attendu cet ecran, rendu par {SOURCE_ROUTES} et produit par {SOURCE_WIZARD} (STEP_TITLES)"
        )

    commandes = _couples_de_commandes(_lignes_du_corps(recap))
    if "GO" not in commandes:
        constats.append(
            f"{PAGE} : {MOTIF_EXEMPLE} — le corps du recapitulatif n'annonce pas la commande « GO » ; "
            f"attendu le libelle de lancement rendu par {SOURCE_WIZARD} (body_recap)"
        )
    else:
        lancement = f"GO = {commandes['GO']}"
        if normalize(lancement) not in normalize(corps):
            constats.append(
                f"{PAGE} : la section « {TITRE_EXEMPLE} » ne cite pas « {lancement} » ; attendu le "
                f"libelle de lancement, lu dans le corps du recapitulatif ({SOURCE_WIZARD})"
            )

    # 3. Le refus de format de la ligne editee : c'est le message du code, pas un texte de memoire.
    edition = app.test_client()
    edition.get("/optimize/wizard/caracs")
    edition.post("/optimize/wizard/caracs", data={"cmd": "4"})
    forme = _forme_d_edition(_lignes_du_corps(edition.get("/optimize/wizard/caracs")))
    edition.post("/optimize/wizard/caracs", data={"value": "1 2 3"})
    refus = _message_de_statut(_statut(edition.get("/optimize/wizard/caracs")))
    if not forme or refus != forme:
        constats.append(
            f"{PAGE} : {MOTIF_EXEMPLE} — le refus d'une saisie de trois nombres vaut « {refus} » ; "
            f"attendu « {forme} », la forme de l'ecran edite, affichee juste au-dessus du refus par "
            f"{SOURCE_ROUTES}"
        )
    if normalize(forme) not in normalize(texte):
        constats.append(
            f"{PAGE} : {MOTIF_EXEMPLE} — la forme « {forme} » rendue par le sous-ecran n'est citee "
            f"nulle part dans la page ; attendu la forme de la ligne editee, lue au rendu "
            f"({SOURCE_ROUTES})"
        )

    # 4. Aucune commande destructrice dans un parcours recommande (D-22/D-23, D-61).
    if COMMANDE_DESTRUCTRICE.search(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_EXEMPLE} » porte une commande destructrice ; attendu un "
            f"parcours recommande sans aucune commande de destruction de donnees ({MOTIF_EXEMPLE})"
        )

    assert not constats, (
        f"{PAGE} : constats sur l'exemple guide : "
        + " ; ".join(constats)
        + f" ; attendu les trois editions de l'{MOTIF_EXEMPLE} rejouees sur le rendu de {SOURCE_WIZARD}, "
        f"leurs lignes rendues citees par la section « {TITRE_EXEMPLE} », et le libelle de lancement lu "
        f"dans le corps du recapitulatif"
    )
