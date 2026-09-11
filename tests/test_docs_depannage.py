"""Ancrage de la page `docs/depannage.md` sur les messages **reellement produits** par le produit.

Le contrat va du produit vers la page : chaque message cite par la page est confronte a sa provenance
reelle, jamais a une memoire (D-19). Trois provenances sont employees, toutes en processus :

- `cli_status` : la sortie de la fonction de production `_print_db_status`, capturee par
  `redirect_stdout` sur une base construite sous `tmp_path` (base vide) et sur la base de la fixture
  `app` (base peuplee), avec `db.close()` dans un `finally` — sans quoi le nettoyage du dossier
  temporaire echoue sur Windows ;
- `web_render` : la ligne de statut et les lignes de corps rendues par le **client de test Flask**, en
  processus, sur une application a catalogue vide construite par `create_app` et sur la fixture `app` ;
- `source_literal` : le litteral lu dans le fichier producteur nomme, pour ce que seule l'execution de
  `main()` ou d'un POST de calcul imprimerait.

Aucun serveur n'est lance, aucune socket n'est ouverte, `main()` n'est jamais execute, le solveur n'est
jamais lance et rien n'est ecrit sous `.data/` : toute base construite par ce module l'est sous
`tmp_path`, ou par la fixture `app` qui construit la sienne au meme endroit (D-103, D-104).

Limites nommees (D-85) :

- l'execution JavaScript et le DOM ne sont pas observables : la rubrique du clavier s'adosse au
  mecanisme **lu** dans `screen.html` et `terminal.js` et au rendu des ecrans sans champ de saisie, elle
  ne revendique aucune execution ;
- le rendu Markdown des pages hors GitHub n'est pas observable (aucun moteur de rendu installe, aucune
  publication distante) ;
- la prose libre de la page (l'invitation a chercher par le message, la clarte des renvois) n'est pas
  verifiee : les constats portent sur les rubriques, les messages et les valeurs **cites** ;
- l'assertion de fins de ligne CRLF depend de `core.autocrlf` du poste et n'est pas presentee comme
  portable (AR-5) ;
- la comparaison de provenance est une **appartenance de sous-chaine** sur le texte produit : un message
  declare qui serait contenu dans un autre passerait. La limite est mesuree et ecrite ici plutot que
  masquee, et la bijection rubrique <-> table `MESSAGES` est, elle, une egalite de deux ensembles.

`source_literal` prouve que la chaine est un **litteral** du fichier nomme, pas qu'elle est atteinte a
l'execution : c'est la limite honnete du mode pour les messages que seul `main()` imprimerait.
"""

import ast
import contextlib
import io
import re
from pathlib import Path

import pytest

from dofus_stuff.catalog import Catalog
from dofus_stuff.cli import _print_db_status
from dofus_stuff.database import Database
from dofus_stuff.web import create_app

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "depannage.md"
SOMMAIRE = "sommaire.md"

# Un fichier de code par source citee par la page, jamais un chemin invente (D-03, D-69).
SOURCE_CLI = "dofus_stuff/cli.py"
SOURCE_SYNC = "dofus_stuff/sync.py"
SOURCE_ROUTES = "dofus_stuff/web/routes.py"
SOURCE_OPTIMIZE_WIZARD = "dofus_stuff/web/optimize_wizard.py"
SOURCE_PROFILE_INPUT = "dofus_stuff/optimize/profile_input.py"
SOURCE_TERMINAL_JS = "dofus_stuff/web/static/js/terminal.js"
SOURCE_ECRAN_HTML = "dofus_stuff/web/templates/screen.html"

# Les cinq familles du critere 1, dans son ordre : la **cle** est stable et ASCII, le titre est le
# libelle francais accentue du titre de niveau 2 de la page.
RUBRIQUES = (
    ("base", "Base absente ou vide"),
    ("saisie", "Saisie invalide"),
    ("calcul", "Calcul long"),
    ("clavier", "Clavier inactif"),
    ("pagination", "Résultat paginé"),
)

# La famille qui n'affiche **aucun** message : « clavier inactif » est un mecanisme, pas une chaine
# (D-76). `MESSAGES` ne doit porter aucune entree pour elle, et cette absence est controlee.
RUBRIQUES_MECANISME = ("clavier",)

TITRE_SOURCE = "Source de vérité"

# (message, cle de rubrique, mode de provenance, fichier producteur pour `source_literal`).
# Chaque ligne a ete mesuree sur le produit avant d'etre ecrite ici : la provenance est la fonction qui
# produit le message, jamais le nom d'un fichier a la ligne pres.
MESSAGES = (
    # Famille « base absente ou vide » : capture de la ligne de commande, rendu web, litteraux de refus.
    ("Version jeu : (aucune)", "base", "cli_status", None),
    ("Dernier check : (aucun)", "base", "cli_status", None),
    ("Entrées : 0", "base", "cli_status", None),
    ("Erreur : aucune version en base", "base", "source_literal", SOURCE_CLI),
    (
        "Base locale vide et --offline : impossible de synchroniser",
        "base",
        "source_literal",
        SOURCE_SYNC,
    ),
    ("AUCUNE VERSION EN BASE", "base", "web_render", None),
    ("ERREUR : AUCUNE VERSION EN BASE.", "base", "web_render", None),
    ("VERSION JEU : (aucune)", "base", "web_render", None),
    ("DERNIER CHECK : (AUCUN)", "base", "web_render", None),
    ("ENTREES : 0", "base", "web_render", None),
    # Famille « saisie invalide » : refus rendus par la ligne de statut, litteral du profil.
    ("SAISIE REQUISE", "saisie", "web_render", None),
    ("LIMITE INVALIDE", "saisie", "web_render", None),
    ("AUCUN RESULTAT.", "saisie", "web_render", None),
    ("ID INVALIDE — ENTIER ATTENDU", "saisie", "web_render", None),
    ("ÉQUIPEMENT INTROUVABLE", "saisie", "web_render", None),
    ("OPTION INVALIDE — SAISIR 1 A 5", "saisie", "web_render", None),
    ("OPTION INVALIDE — SAISIR 1 A 4", "saisie", "web_render", None),
    ("OPTION INVALIDE — SAISIR 1 A 3", "saisie", "web_render", None),
    ("Saisissez le nom ou le numéro de votre classe.", "saisie", "web_render", None),
    ("Exemple : feu, terre air, ou multi.", "saisie", "web_render", None),
    ("Saisissez un niveau entre 1 et 200.", "saisie", "web_render", None),
    ("SAISIE INVALIDE", "saisie", "web_render", None),
    ("Saisie invalide — voir aide syntaxe", "saisie", "source_literal", SOURCE_PROFILE_INPUT),
    # Famille « calcul long » : un seul message d'attente, un etat rendu, un budget, une fin de calcul.
    ("Calcul en cours (CP-SAT)…", "calcul", "source_literal", SOURCE_CLI),
    ("ENTREE=CALCULER", "calcul", "web_render", None),
    ("DUREE", "calcul", "web_render", None),
    ("CALCUL TERMINE", "calcul", "source_literal", SOURCE_ROUTES),
    # Famille « resultat pagine » : le motif du statut, l'indication de saisie, les deux touches de
    # navigation et le message de fin de page de la ligne de commande.
    ("PAGE {page}/{total}", "pagination", "source_literal", SOURCE_ROUTES),
    ("ENTREE=VALIDER", "pagination", "web_render", None),
    ("Page prec", "pagination", "source_literal", SOURCE_ROUTES),
    ("Page suiv", "pagination", "source_literal", SOURCE_ROUTES),
    ("Page suivante disponible :", "pagination", "source_literal", SOURCE_CLI),
)

# Jetons du mecanisme du clavier, avec le fichier qui les porte reellement : le champ de saisie est
# marque au gabarit, la refocalisation et la touche Entree vivent dans le script.
MECANISMES_CLAVIER = (
    ("autofocus", SOURCE_ECRAN_HTML),
    ("activeElement", SOURCE_TERMINAL_JS),
    ("preventDefault", SOURCE_TERMINAL_JS),
)

# Ecrans mesures sans champ de saisie : leur rendre un message serait une sonde muette par
# construction, c'est exactement ce que cette famille declare au lieu de l'inventer.
ECRANS_SANS_CHAMP = ("/version", "/db/status", "/quit")

# Motifs de morsure portes par des constantes du module, jamais ecrits en clair dans une ligne
# d'assertion (regle posee au plan 03-03) : pytest reproduit la ligne source du `assert`, une valeur en
# clair y serait trouvee meme si aucun constat n'avait ete produit. Valeurs ASCII, sans apostrophe,
# chacune incluse dans le constat qui la concerne.
MOTIF_RUBRIQUE_ABSENTE = "rubrique de depannage absente"
MOTIF_RUBRIQUE_VIDE = "rubrique de depannage sans message"
MOTIF_MESSAGE_ABSENT = "message non cite par sa rubrique"
MOTIF_MESSAGE_INVENTE = "message cite non declare"
MOTIF_MESSAGE_NON_PRODUIT = "message non produit par le code"
MOTIF_MECANISME = "mecanisme du clavier"
MOTIF_CHAMP_PRESENT = "champ de saisie inattendu"
MOTIF_PAGINATION = "formes de la pagination"
MOTIF_VOLATILES = "valeur volatile"
MOTIF_CHEMIN_ABSOLU = "chemin absolu"
MOTIF_PROMESSE_DUREE = "promesse de duree"
MOTIF_CRLF = "fins de ligne"
MOTIF_SOURCE = "chemin de source absent"
MOTIF_RETOUR = "ligne de retour de la page"
MOTIF_LIEN_EXTERNE = "lien externe"
MOTIF_BLOC_EXEMPLE = "bloc de commandes"
MOTIF_CHEMIN_DESTRUCTIF = "chemin destructif"
MOTIF_DATA_DIR = "repertoire de donnees non isole"
MOTIF_GARDE = "garde de cloture du harnais"
MOTIF_BUDGET = "budget de calcul non cite"

# Ce que le produit expose pour un calcul est un **budget** reglable — l'option lue sur l'aide du
# parseur — et un **etat**, jamais une duree d'attente promise (D-19, D-76). La rubrique du calcul long
# doit donc citer cette option, et ce controle est localise a la rubrique : le controle de page, lui, ne
# dit rien de la rubrique qui porte le budget.
OPTION_BUDGET = "--time-limit"

# Deux refus de valeur de la page : un nombre de quatre chiffres ou plus est un compteur, une version,
# un horodatage ou une taille de fichier (D-73) ; un chemin de poste commence par une lettre de lecteur
# (D-75). La sortie reellement capturee porte un chemin de dossier temporaire : la page cite donc les
# **libelles**, jamais la ligne entiere.
MOTIF_VOLATILE = re.compile(r"\d{4,}")
MOTIF_CHEMIN_POSTE = re.compile(r"[A-Za-z]:[\\/]")

# Formulations qui promettraient une duree d'attente. Aucune n'est un message du produit : elles vivent
# ici et nulle part dans la page (D-19), et leur absence est controlee.
JETONS_PROMESSE_DUREE = (
    "plusieurs minutes",
    "quelques minutes",
    "patientez",
    "cela peut prendre",
    "peut prendre du temps",
)

# Marqueurs du gabarit reel (`dofus_stuff/web/templates/screen.html`), repris a l'identique du module
# de la phase 5 : le corps visible est encadre par `id="body"` et par la seule ligne de statut, et le
# motif de ligne de corps ne capture que les lignes de la classe `row`. Les trois lecteurs ci-dessous
# sont locaux a ce module, comme la phase 5 l'a fait : un lecteur de rendu n'est pas un helper partage
# de `tests/conftest.py`, il n'est donc pas expose en fixture (D-12).
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'
LIGNE_CORPS = re.compile(r'<div class="row">(.*?)</div>', re.S)

# Une ligne de tableau dont la **premiere** cellule est un message entre accents graves : c'est la forme
# extractible de la page. Le motif est ancre en debut de ligne, et la classe `[^`]+` ne peut pas
# traverser un accent grave : il capture donc le contenu d'un seul intervalle.
MOTIF_MESSAGE_CITE = re.compile(r"^\|\s*`(?P<message>[^`]+)`\s*\|", re.MULTILINE)

# Un motif de pagination COMPOSE (`PAGE 3/3`), jamais une position : la ligne de corps de l'ecran de
# liste comme celle de l'ecran a page unique le portent.
MOTIF_PAGE_COMPOSE = re.compile(r"\bPAGE\s+\d+\s*/\s*\d+")

# Jeton entre accents graves du bloc « Source de verite » ; un jeton est lu comme un chemin s'il
# ressemble a un chemin de fichier, et il est alors exige sur disque depuis la racine du depot.
MOTIF_JETON_ACCENTS = re.compile(r"`(?P<jeton>[^`]+)`")
SUFFIXES_CHEMIN = (".py", ".md", ".js", ".json", ".html")

# Un bloc de code marque `console` porte des exemples a recopier (D-24) : cette page n'en a aucun. Les
# liens externes sont refuses par convention depuis la phase 1.
MOTIF_BALISE_CONSOLE = re.compile(r"^\s*```console", re.MULTILINE)
CIBLES_EXTERNES = ("http://", "https://", "mailto:")

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

# Noms d'appel dont la presence signalerait une action destructive, l'execution du produit ou le
# lancement du solveur. `optimize_stuff` et `_run_optimize_and_redirect` sont les deux points d'entree
# du calcul : poster un niveau **valide** sur l'ecran du niveau les declencherait, ce que ce module ne
# fait jamais (il ne poste qu'un niveau hors bornes, ce qui prouve aussi que le refus precede le calcul).
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"
APPELS_CALCUL_PRODUIT = ("optimize_stuff", "_run_optimize_and_redirect")

# Les deux seuls points d'entree de l'interface qui visent la base locale ou le reseau : poster l'un ou
# l'autre est interdit a ce module. L'ecran de sortie est en `GET` seulement et repond 405 sur `POST`,
# donc aucun controle ne l'appelle (mesure de la phase de recherche).
CHEMINS_DESTRUCTIFS = ("/db/clear", "/db/sync")

# Appels qui construisent une base, et formes de `data_dir` admises : une expression derivee de
# `tmp_path`, un nom lie dans le module a une telle expression, ou la base de la fixture `app`, que la
# fixture construit elle-meme sous `tmp_path`. `DEFAULT_DATA_DIR` n'est jamais passe a l'un d'eux.
CIBLES_DATA_DIR = ("Database", "create_app")
REPERTOIRES_ISOLES = ("tmp_path", "web_config")
NOM_DEFAUT_INTERDIT = "DEFAULT_DATA_DIR"

# Reperes du gabarit et de la page, nommes une seule fois : le champ de saisie du gabarit d'ecran, et
# la ligne de retour du gabarit de page (D-01, D-102).
MARQUEUR_SAISIE = 'id="main-input"'
LIEN_RETOUR = "[Retour au sommaire](sommaire.md)"


def _texte_page(docs_dir: Path) -> str:
    """Texte de la page, lu en UTF-8 explicite ; page absente = AssertionError localisante (D-13).

    Jamais de `FileNotFoundError` brut : l'echec nomme la page, le chemin attendu et les fichiers de
    code dont elle decrit les messages. Toute lecture de la page passe par ici.
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page de depannage indexee par le "
            f"message reellement produit, adossee a {SOURCE_CLI}, {SOURCE_SYNC} et {SOURCE_ROUTES}"
        )
    return chemin.read_text(encoding="utf-8")


def _corps_par_titre(texte: str, sections) -> dict[str, str]:
    """Corps des sections de niveau 2, par titre.

    Le decoupage vient du helper partage de `tests/conftest.py`, recu en parametre et jamais recopie
    (D-12) : un decoupage recopie finirait par diverger de celui des autres modules d'ancrage.
    """
    return {titre: corps for titre, corps in sections(texte) if titre is not None}


def _lignes_du_corps(reponse) -> list[str]:
    """Lignes visibles du corps d'un ecran, jamais la reponse entiere.

    La reponse entiere porte la coquille, la ligne d'en-tete et la ligne de statut : une assertion
    ecrite sur elle serait vraie pour une raison etrangere a l'ecran controle. Une reponse sans les
    marqueurs du gabarit leve un constat localisant plutot que de rendre une liste vide.
    """
    texte = reponse.get_data(as_text=True)
    if MARQUEUR_CORPS not in texte or MARQUEUR_STATUT not in texte:
        raise AssertionError(
            f"{MOTIF_MESSAGE_NON_PRODUIT} : la reponse sondee ne porte pas les marqueurs du gabarit "
            f"d'ecran ({MARQUEUR_CORPS}, {MARQUEUR_STATUT}) ; attendu une reponse rendue, redirections "
            f"suivies, par les ecrans de {SOURCE_ROUTES}"
        )
    corps = texte.split(MARQUEUR_CORPS, 1)[1].split(MARQUEUR_STATUT, 1)[0]
    return [ligne.rstrip() for ligne in LIGNE_CORPS.findall(corps)]


def _statut(reponse) -> str:
    """Texte de la ligne de statut : la seule source des messages de refus du produit."""
    texte = reponse.get_data(as_text=True)
    if MARQUEUR_STATUT not in texte:
        raise AssertionError(
            f"{MOTIF_MESSAGE_NON_PRODUIT} : la reponse sondee ne porte pas de ligne de statut "
            f"({MARQUEUR_STATUT}) ; attendu un ecran rendu par {SOURCE_ROUTES}, la ligne de statut "
            f"etant la source des messages de refus"
        )
    return texte.split(MARQUEUR_STATUT, 1)[1].split(">", 1)[1].split("</div>", 1)[0]


def _sonde(route: str, reponse) -> None:
    """Verifie la prise d'une sonde : l'ecran est rendu et sa coquille est presente.

    Une sonde qui ne prend rien est un constat, jamais un vert silencieux (T-06-01-05) : sans ce
    controle, une redirection non suivie ferait passer une famille entiere pour muette.
    """
    if reponse.status_code != 200:
        raise AssertionError(
            f"{MOTIF_MESSAGE_NON_PRODUIT} : la sonde de {route} n'a rien pris (statut HTTP "
            f"{reponse.status_code}) ; attendu un ecran rendu, redirections suivies, la route etant "
            f"celle des ecrans de {SOURCE_ROUTES}"
        )
    if MARQUEUR_CORPS not in reponse.get_data(as_text=True):
        raise AssertionError(
            f"{MOTIF_MESSAGE_NON_PRODUIT} : la reponse de {route} ne porte pas le corps d'ecran "
            f"({MARQUEUR_CORPS}) ; attendu un rendu du gabarit de {SOURCE_ROUTES}"
        )


def _ajouter(produites: dict[str, str], texte: str, provenance: str) -> None:
    """Enregistre une chaine produite avec sa provenance lisible, sans ecraser la premiere mesure."""
    texte = texte.strip()
    if texte:
        produites.setdefault(texte, provenance)


def _capture_cli(produites: dict[str, str], db: Database, provenance: str) -> None:
    """Capture la sortie de `_print_db_status`, la base etant refermee dans tous les cas.

    `_print_db_status` interroge `stats()`, qui ouvre la connexion et la laisse ouverte : sans
    `close()`, le nettoyage du dossier temporaire echoue sur Windows (`PermissionError [WinError 32]`,
    mesure de la phase de recherche). La fermeture est donc dans un `finally`.
    """
    tampon = io.StringIO()
    try:
        with contextlib.redirect_stdout(tampon):
            _print_db_status(db)
    finally:
        db.close()
    for ligne in tampon.getvalue().splitlines():
        _ajouter(produites, ligne, f"{provenance} ; capture de _print_db_status ({SOURCE_CLI})")


def _produire(client, tmp_path) -> dict[str, str]:
    """Sonde unique : l'ensemble des chaines **reellement produites**, associees a leur provenance.

    Elle capture la ligne de commande sur une base vide construite sous `tmp_path` et sur la base
    peuplee de la fixture `app`, rend les ecrans d'une application a catalogue vide (base absente, que
    le premier contact cree), sonde les refus par `client.post(..., follow_redirects=True)`, conduit le
    parcours simplifie **pas a pas** avant de sonder le refus de niveau, et lit les ecrans de calcul par
    des `GET` seulement.

    Le module ne poste **jamais** un niveau valide : ce POST est le calcul lui-meme. Seul un niveau hors
    bornes est poste, ce qui prouve aussi que le refus est rendu avant tout calcul. Chaque sonde verifie
    sa propre prise, et un message declare en mode `cli_status` ou `web_render` qui ne serait observe
    nulle part leve un constat nommant la route sondee : une sonde muette ne passe jamais pour un vert
    (T-06-01-05).
    """
    produites: dict[str, str] = {}
    routes_sondees: list[str] = []

    # (a) Ligne de commande : base vide sous tmp_path, puis base peuplee de la fixture `app`.
    _capture_cli(
        produites,
        Database(data_dir=tmp_path / "depannage-base-vide"),
        "etat de la base ligne de commande, base vide",
    )
    _capture_cli(
        produites,
        Database(data_dir=client.application.extensions["web_config"]["data_dir"]),
        "etat de la base ligne de commande, base peuplee",
    )

    # (b) Rendu web d'une application a catalogue vide : la base n'existe pas encore, le premier
    #     contact la cree — l'etat rendu est donc celui d'une base vide.
    vide = create_app(
        data_dir=tmp_path / "depannage-web-vide",
        offline=True,
        catalog=Catalog(version=None, items={}),
        load_catalog=False,
    )
    vide.config["TESTING"] = True
    client_vide = vide.test_client()
    for route in ("/version", "/db/status"):
        routes_sondees.append(f"GET {route}")
        reponse = client_vide.get(route)
        _sonde(route, reponse)
        _ajouter(
            produites,
            _statut(reponse),
            f"statut rendu par GET {route} sur une application a catalogue vide",
        )
        for ligne in _lignes_du_corps(reponse):
            _ajouter(
                produites,
                ligne,
                f"corps rendu par GET {route} sur une application a catalogue vide",
            )

    # (c) Refus rendus par la ligne de statut : les refus sont des flashs suivis d'une redirection.
    #     Aucun de ces POST ne lance de calcul (recherche, liste, fiche, menus, etape des emplacements).
    refus = (
        ("/search", {"query": ""}),
        ("/search", {"query": "Cape|abc"}),
        ("/search", {"query": "zzzz"}),
        ("/list", {"ankama_id": "x"}),
        ("/item", {"ankama_id": "x"}),
        ("/item", {"ankama_id": "999999"}),
        ("/", {"selection": "9"}),
        ("/system", {"selection": "9"}),
        ("/db", {"selection": "9"}),
        ("/optimize/quick/classe", {"cmd": "zzz"}),
        ("/optimize/wizard/slots", {"cmd": "zzz"}),
    )
    for route, donnees in refus:
        routes_sondees.append(f"POST {route}")
        reponse = client.post(route, data=donnees, follow_redirects=True)
        _sonde(route, reponse)
        _ajouter(produites, _statut(reponse), f"statut rendu par POST {route} sur la fixture app")
        for ligne in _lignes_du_corps(reponse):
            _ajouter(produites, ligne, f"corps rendu par POST {route} sur la fixture app")

    # (d) Parcours simplifie conduit pas a pas : le refus de l'etape du niveau n'est atteint que si la
    #     classe puis les elements ont ete renseignes. Seul un niveau hors bornes est poste ensuite.
    routes_sondees.append("POST /optimize/quick/classe")
    etape_classe = client.post(
        "/optimize/quick/classe", data={"cmd": "Cra"}, follow_redirects=True
    )
    _sonde("/optimize/quick/classe", etape_classe)
    _ajouter(
        produites,
        _statut(etape_classe),
        "statut rendu par POST /optimize/quick/classe, parcours conduit",
    )

    # Le refus des elements est sonde avant la conduite de l'etape : poster une valeur invalide ne
    # renseigne rien, l'etape reste a remplir.
    for donnees, provenance in (
        ({"cmd": "zzz"}, "refus rendu par POST /optimize/quick/elements, choix hors liste"),
        ({"cmd": "feu"}, "statut rendu par POST /optimize/quick/elements, parcours conduit"),
    ):
        routes_sondees.append("POST /optimize/quick/elements")
        reponse = client.post("/optimize/quick/elements", data=donnees, follow_redirects=True)
        _sonde("/optimize/quick/elements", reponse)
        _ajouter(produites, _statut(reponse), provenance)

    routes_sondees.append("GET /optimize/quick/niveau")
    ecran_niveau = client.get("/optimize/quick/niveau", follow_redirects=True)
    _sonde("/optimize/quick/niveau", ecran_niveau)
    _ajouter(
        produites,
        _statut(ecran_niveau),
        "statut rendu par GET /optimize/quick/niveau, parcours simplifie conduit",
    )

    routes_sondees.append("POST /optimize/quick/niveau")
    refus_niveau = client.post(
        "/optimize/quick/niveau", data={"cmd": "999"}, follow_redirects=True
    )
    _sonde("/optimize/quick/niveau", refus_niveau)
    _ajouter(
        produites,
        _statut(refus_niveau),
        "statut rendu par POST /optimize/quick/niveau avec un niveau hors bornes, aucun calcul lance",
    )

    # (e) Calcul long : le recapitulatif du wizard est lu par un GET seulement, il porte le budget.
    routes_sondees.append("GET /optimize/wizard/recap")
    recap = client.get("/optimize/wizard/recap", follow_redirects=True)
    _sonde("/optimize/wizard/recap", recap)
    _ajouter(
        produites,
        _statut(recap),
        "statut rendu par GET /optimize/wizard/recap sur la fixture app",
    )
    for ligne in _lignes_du_corps(recap):
        _ajouter(
            produites,
            ligne,
            "corps rendu par GET /optimize/wizard/recap sur la fixture app",
        )

    # (f) Prise des messages declares : aucun message en mode rendu ou capture ne doit manquer.
    manquants = [
        f"« {message} » (famille {cle}, mode {mode})"
        for message, cle, mode, _source in MESSAGES
        if mode != "source_literal" and not any(message in produit for produit in produites)
    ]
    if manquants:
        raise AssertionError(
            f"{MOTIF_MESSAGE_NON_PRODUIT} : aucune des routes sondees ({', '.join(routes_sondees)}) ne "
            f"porte : {' ; '.join(manquants)} ; attendu chaque message declare en mode `cli_status` ou "
            f"`web_render` observe sur la capture reelle ou sur le rendu ({SOURCE_CLI}, {SOURCE_ROUTES})"
        )
    return produites


def _rendus_sans_champ(client) -> dict[str, str]:
    """Rendu des ecrans declares sans champ de saisie, une prise verifiee par ecran.

    La mesure est faite sur la reponse entiere, jamais sur un fragment : c'est elle qui porte — ou ne
    porte pas — la balise du champ de saisie du gabarit.
    """
    rendus: dict[str, str] = {}
    for route in ECRANS_SANS_CHAMP:
        reponse = client.get(route, follow_redirects=True)
        _sonde(route, reponse)
        rendus[route] = reponse.get_data(as_text=True)
    return rendus


def problemes_rubriques(docs_dir: Path, sections) -> list[str]:
    """Chaque rubrique declaree existe, est non vide, dans l'ordre du critere 1, et porte ses messages.

    Une rubrique de `RUBRIQUES_MECANISME` ne porte **aucune** entree de `MESSAGES` — c'est sa
    declaration — et toute rubrique hors mecanisme en porte au moins une (D-93, D-76, critere 1).
    """
    texte = _texte_page(docs_dir)
    corps_par_titre = _corps_par_titre(texte, sections)
    titres = [titre for titre, _ in sections(texte) if titre is not None]
    constats: list[str] = []

    for cle, titre in RUBRIQUES:
        if titre not in corps_par_titre:
            constats.append(
                f"{MOTIF_RUBRIQUE_ABSENTE} : la rubrique « {titre} » de la famille « {cle} » n'existe "
                f"pas dans {PAGE} ; attendu un titre de niveau 2 « ## {titre} », dans l'ordre du "
                f"critere 1 (D-93, critere 1)"
            )
        elif not corps_par_titre[titre].strip():
            constats.append(
                f"{MOTIF_RUBRIQUE_VIDE} : la rubrique « {titre} » est vide dans {PAGE} ; attendu au "
                f"moins un message mesure de la famille « {cle} » ou sa declaration de mecanisme "
                f"(D-93, D-76)"
            )

    positions = [titres.index(titre) for _cle, titre in RUBRIQUES if titre in titres]
    if positions != sorted(positions):
        constats.append(
            f"{MOTIF_RUBRIQUE_ABSENTE} : les rubriques de {PAGE} ne sont pas dans l'ordre du critere 1 "
            f"({', '.join(titre for _cle, titre in RUBRIQUES)}) ; mesure : {', '.join(titres)} "
            f"(critere 1)"
        )

    for cle, titre in RUBRIQUES:
        declares = [
            message for message, cle_message, _mode, _source in MESSAGES if cle_message == cle
        ]
        if cle in RUBRIQUES_MECANISME and declares:
            constats.append(
                f"{MOTIF_MESSAGE_INVENTE} : la famille « {titre} » est declaree comme un mecanisme sans "
                f"message et porte pourtant {len(declares)} entree(s) de MESSAGES ; attendu aucune "
                f"entree pour elle (D-76, critere 1)"
            )
        if cle not in RUBRIQUES_MECANISME and not declares:
            constats.append(
                f"{MOTIF_RUBRIQUE_VIDE} : la famille « {titre} » ne porte aucun message declare ; "
                f"attendu au moins un message mesure, ou sa declaration de mecanisme (D-93, D-76)"
            )
    return constats


def problemes_messages(docs_dir: Path, produites: dict[str, str], sections) -> list[str]:
    """Chaque message declare est retrouve par sa provenance et cite dans la rubrique de sa famille.

    Deux confrontations distinctes : la **provenance** (presence dans `produites` pour les modes
    `cli_status` et `web_render`, presence du litteral dans le fichier nomme pour `source_literal`), et
    la **bijection** entre les lignes citees et la table declaree, dans les deux sens — message declare
    non cite et message cite non declare sont deux constats distincts (D-13, D-19, D-93).

    Limite nommee : la provenance est une appartenance de sous-chaine sur le texte produit, donc un
    message declare qui serait contenu dans un autre passerait ; la bijection, elle, est une egalite de
    deux ensembles et ne partage pas cette limite.
    """
    texte = _texte_page(docs_dir)
    corps_par_titre = _corps_par_titre(texte, sections)
    constats: list[str] = []

    for message, cle, mode, source in MESSAGES:
        if mode == "source_literal":
            chemin = RACINE_DEPOT / str(source)
            litteral = chemin.read_text(encoding="utf-8") if chemin.is_file() else ""
            if message not in litteral:
                constats.append(
                    f"{MOTIF_MESSAGE_NON_PRODUIT} : le message « {message} » declare pour la famille "
                    f"« {cle} » n'est pas un litteral de {source} ; attendu ce litteral dans le fichier "
                    f"producteur nomme, jamais une variante ecrite de memoire ({source}, D-19)"
                )
        elif not any(message in produit for produit in produites):
            constats.append(
                f"{MOTIF_MESSAGE_NON_PRODUIT} : le message « {message} » declare pour la famille "
                f"« {cle} » n'a ete produit par aucune sonde ; attendu un rendu ou une capture reelle "
                f"qui le porte ({SOURCE_CLI}, {SOURCE_ROUTES}, D-19)"
            )

    for cle, titre in RUBRIQUES:
        declares = {
            message for message, cle_message, _mode, _source in MESSAGES if cle_message == cle
        }
        corps = corps_par_titre.get(titre)
        cites = [message.strip() for message in MOTIF_MESSAGE_CITE.findall(corps)] if corps else []
        for message in sorted(declares - set(cites)):
            constats.append(
                f"{MOTIF_MESSAGE_ABSENT} : la rubrique « {titre} » de {PAGE} ne cite pas « {message} » "
                f"dans une ligne de tableau dont la premiere cellule est le message ; attendu une ligne "
                f"« | `{message}` | ... | » dans cette rubrique (D-93, critere 1)"
            )
        for message in sorted(set(cites) - declares):
            constats.append(
                f"{MOTIF_MESSAGE_INVENTE} : la rubrique « {titre} » de {PAGE} cite « {message} » ; "
                f"attendu un message declare dans MESSAGES avec sa provenance, ou son retrait de la "
                f"page : une chaine non produite par le code ne cree pas de ligne (D-19, D-93)"
            )
    return constats


def problemes_clavier(docs_dir: Path, rendus: dict[str, str], sections) -> list[str]:
    """La famille sans message est traitee comme un mecanisme, adosse au code et au rendu (D-76).

    Trois exigences : la rubrique existe et cite chaque jeton declare, chaque jeton est **reellement
    porte** par le fichier nomme, et `MESSAGES` ne porte aucune entree pour cette famille — un message
    invente pour elle serait exactement le defaut que le critere 1 interdit.
    """
    texte = _texte_page(docs_dir)
    corps_par_titre = _corps_par_titre(texte, sections)
    titre_clavier = dict(RUBRIQUES)["clavier"]
    corps = corps_par_titre.get(titre_clavier)
    constats: list[str] = []

    if corps is None:
        constats.append(
            f"{MOTIF_MECANISME} : la rubrique « {titre_clavier} » n'existe pas dans {PAGE} ; attendu la "
            f"rubrique du mecanisme du clavier, adossee a {SOURCE_ECRAN_HTML} et {SOURCE_TERMINAL_JS} "
            f"(D-76, critere 1)"
        )
    else:
        for jeton, source in MECANISMES_CLAVIER:
            if jeton not in corps:
                constats.append(
                    f"{MOTIF_MECANISME} : la rubrique « {titre_clavier} » de {PAGE} ne cite pas le jeton "
                    f"« {jeton} » ; attendu ce jeton du mecanisme, porte par {source} (D-76)"
                )
            chemin = RACINE_DEPOT / source
            porteur = chemin.read_text(encoding="utf-8") if chemin.is_file() else ""
            if jeton not in porteur:
                constats.append(
                    f"{MOTIF_MECANISME} : le jeton « {jeton} » n'est pas porte par {source} ; attendu ce "
                    f"jeton dans le fichier qui le porte, le mecanisme etant lu et jamais execute "
                    f"(D-76, D-85)"
                )

    if any(cle == "clavier" for _message, cle, _mode, _source in MESSAGES):
        constats.append(
            f"{MOTIF_MESSAGE_INVENTE} : MESSAGES porte une entree pour la famille « {titre_clavier} » ; "
            f"attendu aucune entree, cette famille n'ayant aucun message produit (D-76, D-93)"
        )

    for route in ECRANS_SANS_CHAMP:
        rendu = rendus.get(route)
        if rendu is None:
            raise AssertionError(
                f"{MOTIF_MECANISME} : l'ecran {route}, declare sans champ de saisie, n'a pas ete rendu ; "
                f"attendu une prise mesuree pour chaque ecran de ECRANS_SANS_CHAMP ({SOURCE_ROUTES})"
            )
        if MARQUEUR_SAISIE in rendu:
            constats.append(
                f"{MOTIF_CHAMP_PRESENT} : l'ecran {route} rend la balise {MARQUEUR_SAISIE} ; attendu "
                f"aucun champ de saisie sur cet ecran, qui n'en attend aucun ({SOURCE_ROUTES})"
            )
    return constats


def problemes_budget(docs_dir: Path, sections, normalize) -> list[str]:
    """La rubrique du calcul long cite le budget du produit, sans promettre de duree d'attente.

    Le produit regle un calcul par un budget (`OPTION_BUDGET`, lue sur l'aide du parseur) et l'expose par
    un etat ; il ne promet aucun delai (D-19). La rubrique doit donc citer l'option, et aucun jeton de
    `JETONS_PROMESSE_DUREE` ne doit apparaitre dans *cette* rubrique — controle localise, le controle de
    page ne distinguant pas la rubrique qui porte le budget des autres.
    """
    titre = dict(RUBRIQUES)["calcul"]
    corps = _corps_par_titre(_texte_page(docs_dir), sections).get(titre)
    constats: list[str] = []
    if corps is None:
        constats.append(
            f"{MOTIF_BUDGET} : la rubrique « {titre} » est absente de {PAGE} ; attendu la rubrique du "
            f"calcul long, qui cite le budget du produit ({SOURCE_CLI}, D-19)"
        )
        return constats
    if OPTION_BUDGET not in corps:
        constats.append(
            f"{MOTIF_BUDGET} : la rubrique « {titre} » de {PAGE} ne cite pas « {OPTION_BUDGET} » ; "
            f"attendu l'option de budget du produit, lue sur l'aide du parseur ({SOURCE_CLI}, D-19)"
        )
    normalise = normalize(corps)
    for jeton in JETONS_PROMESSE_DUREE:
        if jeton in normalise:
            constats.append(
                f"{MOTIF_PROMESSE_DUREE} : la rubrique « {titre} » de {PAGE} porte « {jeton} » ; attendu "
                f"un budget reglable et un etat rendu, jamais un delai d'attente annonce "
                f"({SOURCE_CLI}, D-19)"
            )
    return constats


def problemes_page(docs_dir: Path, sections, normalize) -> list[str]:
    """Cloture de la page et absence de valeur volatile : les gardes de structure ne les verifient pas.

    Sont controles ici les octets (CRLF sans BOM), les deux refus de valeur (`D-73`, `D-75`), l'absence
    de promesse de duree (`D-19`), l'absence de lien externe et de bloc d'exemples, la ligne de retour
    en derniere ligne non vide, et le bloc « Source de verite » dont chaque chemin existe reellement
    depuis la racine du depot (`D-03`, `D-69`).
    """
    chemin = docs_dir / PAGE
    texte = _texte_page(docs_dir)
    octets = chemin.read_bytes()
    corps_par_titre = _corps_par_titre(texte, sections)
    titres = [titre for titre, _ in sections(texte) if titre is not None]
    constats: list[str] = []

    sans_cr = octets.replace(b"\r\n", b"")
    lf_isoles = sans_cr.count(b"\n")
    bom = octets.startswith(b"\xef\xbb\xbf")
    if lf_isoles or bom:
        constats.append(
            f"{MOTIF_CRLF} : {PAGE} porte {lf_isoles} fin(s) de ligne LF isolee(s) et BOM={bom} ; "
            f"attendu des fins de ligne CRLF et un fichier UTF-8 sans BOM, comme les autres pages "
            f"livrees (D-102)"
        )

    volatile = MOTIF_VOLATILE.search(texte)
    if volatile:
        constats.append(
            f"{MOTIF_VOLATILES} : {PAGE} cite « {volatile.group(0)} » ; attendu aucun nombre de quatre "
            f"chiffres ou plus, ces valeurs changeant d'une installation a l'autre et n'etant pas des "
            f"messages du produit (D-73, D-75)"
        )

    absolu = MOTIF_CHEMIN_POSTE.search(texte)
    if absolu:
        constats.append(
            f"{MOTIF_CHEMIN_ABSOLU} : {PAGE} cite « {absolu.group(0)} » ; attendu aucun chemin de "
            f"poste, la page citant les libelles produits et jamais la ligne entiere de la sortie "
            f"capturee (D-75)"
        )

    normalise = normalize(texte)
    for jeton in JETONS_PROMESSE_DUREE:
        if jeton in normalise:
            constats.append(
                f"{MOTIF_PROMESSE_DUREE} : {PAGE} porte « {jeton} » ; attendu ce que le produit expose "
                f"— un budget et un etat — jamais une duree d'attente promise (D-19, D-76)"
            )

    for jeton in CIBLES_EXTERNES:
        if jeton in texte:
            constats.append(
                f"{MOTIF_LIEN_EXTERNE} : {PAGE} porte « {jeton} » ; attendu des liens internes "
                f"seulement, la documentation etant lue hors ligne (D-102)"
            )

    if MOTIF_BALISE_CONSOLE.search(texte):
        constats.append(
            f"{MOTIF_BLOC_EXEMPLE} : {PAGE} porte un bloc de code marque `console` ; attendu aucun "
            f"exemple a recopier sur cette page, qui cite des messages sans en recommander la frappe "
            f"(D-24)"
        )

    lignes = [ligne.strip() for ligne in texte.splitlines() if ligne.strip()]
    derniere = lignes[-1] if lignes else ""
    if derniere != LIEN_RETOUR:
        constats.append(
            f"{MOTIF_RETOUR} : la derniere ligne non vide de {PAGE} est « {derniere} » ; attendu "
            f"« {LIEN_RETOUR} » comme sur les autres pages livrees (D-102, D-01)"
        )

    if not titres or titres[-1] != TITRE_SOURCE:
        constats.append(
            f"{MOTIF_SOURCE} : le bloc « ## {TITRE_SOURCE} » n'est pas la derniere section de {PAGE} ; "
            f"attendu ce bloc en derniere section, la ligne de retour venant apres lui (D-102, D-69)"
        )

    corps_source = corps_par_titre.get(TITRE_SOURCE)
    if not corps_source or not corps_source.strip():
        constats.append(
            f"{MOTIF_SOURCE} : la section « {TITRE_SOURCE} » de {PAGE} est absente ou vide ; attendu un "
            f"chemin de source existant par ligne, entre accents graves (D-03, D-69)"
        )
    else:
        for jeton in MOTIF_JETON_ACCENTS.findall(corps_source):
            if not ("/" in jeton or jeton.endswith(SUFFIXES_CHEMIN)):
                continue
            if not (RACINE_DEPOT / jeton).exists():
                constats.append(
                    f"{MOTIF_SOURCE} : {PAGE} cite « {jeton} » dans son bloc « {TITRE_SOURCE} » ; "
                    f"attendu un chemin existant depuis la racine du depot, jamais un chemin invente "
                    f"(D-03, D-69)"
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


def _nom_appele(noeud: ast.Call) -> str:
    """Nom de la fonction appelee, terminal pour un attribut (`Database`, `create_app`, `get`)."""
    if isinstance(noeud.func, ast.Attribute):
        return noeud.func.attr
    return getattr(noeud.func, "id", "")


def _noms_isoles(arbre: ast.AST) -> set[str]:
    """Noms lies dans le module a une expression derivee de `tmp_path` ou de la configuration de test.

    Une base construite par `Database(data_dir=dossier)` avec `dossier = tmp_path / "vide"` est isolee
    autant qu'une expression ecrite en clair : sans cette lecture, la variable intermediaire serait
    signalee comme un dossier du depot et la garde deviendrait un faux rouge.
    """
    noms: set[str] = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Assign):
            continue
        texte = ast.unparse(noeud.value)
        if not any(isole in texte for isole in REPERTOIRES_ISOLES):
            continue
        for cible in noeud.targets:
            if isinstance(cible, ast.Name):
                noms.add(cible.id)
    return noms


def _cibles_data_dir(arbre: ast.AST) -> list[tuple[int, str]]:
    """Appels qui construisent une base sur un dossier non isole : `(ligne, texte de data_dir)`.

    Le risque de ce module n'est pas d'importer `Database` — c'est la matiere des messages de cette
    page — mais d'ouvrir ou de construire une base hors de `tmp_path` : `Database(data_dir=DEFAULT_DATA_DIR)`
    ouvrirait la base du depot. Sont admis une expression derivee de `tmp_path`, un nom lie a une telle
    expression, et la base de la fixture `app`, que la fixture construit elle-meme sous `tmp_path`.
    """
    isoles = _noms_isoles(arbre)
    fautifs: list[tuple[int, str]] = []
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call) or _nom_appele(noeud) not in CIBLES_DATA_DIR:
            continue
        valeur: ast.expr | None = None
        for mot in noeud.keywords:
            if mot.arg == "data_dir":
                valeur = mot.value
        if valeur is None and noeud.args:
            valeur = noeud.args[0]
        if valeur is None:
            continue
        if isinstance(valeur, ast.Name) and valeur.id in isoles:
            continue
        texte = ast.unparse(valeur)
        if any(isole in texte for isole in REPERTOIRES_ISOLES):
            continue
        fautifs.append((noeud.lineno, texte))
    return fautifs


def _litteraux_de_chemin_destructif(arbre: ast.AST) -> list[tuple[int, str]]:
    """Litteraux de chemin destructif du module, hors de la constante qui les declare.

    Les deux chemins de `CHEMINS_DESTRUCTIFS` sont eux-memes des litteraux du module : ils sont
    identifies par l'affectation de la constante et exclus de la recherche, sans quoi la garde
    s'accuserait elle-meme. Tout **autre** litteral qui commence par l'un de ces deux chemins est un
    constat — que l'appel soit ecrit en clair ou que le chemin soit range dans une table de routes, ce
    qu'une lecture des seuls arguments litteraux de `post(...)` laisserait passer.
    """
    declares: set[int] = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Assign):
            continue
        cibles = [cible for cible in noeud.targets if isinstance(cible, ast.Name)]
        if not any(cible.id == "CHEMINS_DESTRUCTIFS" for cible in cibles):
            continue
        declares.update(id(enfant) for enfant in ast.walk(noeud.value))
    fautifs: list[tuple[int, str]] = []
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Constant) or not isinstance(noeud.value, str):
            continue
        if id(noeud) in declares:
            continue
        if noeud.value.startswith(CHEMINS_DESTRUCTIFS):
            fautifs.append((noeud.lineno, noeud.value))
    return fautifs


def test_garde_de_cloture_du_harnais() -> None:
    """Le module n'ouvre que des bases isolees, ne joint ni reseau ni processus, et ne poste rien de destructif.

    La propriete est verifiee sur le texte de ce module par `ast`, et jamais par une recherche de
    chaines : le module cite lui-meme les noms interdits dans ses messages et dans ses constantes, une
    recherche textuelle se detecterait elle-meme. Le controle porte sur le risque reel — ouvrir la base
    du depot, construire une base hors de `tmp_path`, lancer un processus, ouvrir une socket, joindre le
    reseau, supprimer un fichier, executer le produit, lancer le solveur, poster un chemin destructif —
    donc un import public pur ajoute plus tard passe sans revision, alors qu'un import qui tirerait la
    base ou le reseau rougit.

    Limite nommee : cette garde est une demonstration statique et indirecte. Elle dit ce que ce module
    importe et appelle, pas ce qu'un autre chemin ferait. `DEFAULT_DATA_DIR` peut y etre **nomme** (la
    constante existe pour le refus), mais il n'est jamais passe a un appel qui construit une base.
    """
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    importes = _imports_du_module(arbre)
    appeles = _appels_du_module(arbre)
    constats: list[str] = []

    racines = sorted(module for module in importes if module.split(".")[0] in RACINES_INTERDITES)
    if racines:
        constats.append(
            f"import(s) de base, de processus, de socket ou de reseau : {', '.join(racines)} ; attendu "
            f"aucun de ces imports dans le module d'ancrage decrit par {PAGE} ({SOURCE_CLI}, "
            f"{SOURCE_ROUTES})"
        )
    if APPEL_PRODUIT in appeles:
        constats.append(
            f"appel a {APPEL_PRODUIT}() dans le module d'ancrage ; attendu un ancrage par la fonction "
            f"de production et le client de test Flask, le produit n'etant jamais execute "
            f"({SOURCE_CLI})"
        )
    calculs = sorted(set(APPELS_CALCUL_PRODUIT) & appeles)
    if calculs:
        constats.append(
            f"appel(s) de calcul du produit : {', '.join(calculs)} ; attendu aucun lancement de "
            f"solveur, seul un niveau hors bornes etant poste, ce qui laisse le refus precede tout "
            f"calcul ({SOURCE_ROUTES})"
        )
    suppressions = sorted(set(APPELS_SUPPRESSION) & appeles)
    if suppressions:
        constats.append(
            f"appel(s) de suppression de fichier : {', '.join(suppressions)} ; attendu aucun appel "
            f"destructif dans le module d'ancrage decrit par {PAGE}"
        )

    for ligne, texte_data_dir in _cibles_data_dir(arbre):
        constats.append(
            f"{MOTIF_DATA_DIR} : la ligne {ligne} construit une base avec `data_dir` = "
            f"« {texte_data_dir} » ; attendu un dossier derive de `tmp_path` ou la base de la fixture "
            f"`app`, jamais la racine du depot ni {NOM_DEFAUT_INTERDIT}"
        )

    for ligne, chemin in _litteraux_de_chemin_destructif(arbre):
        constats.append(
            f"{MOTIF_CHEMIN_DESTRUCTIF} : la ligne {ligne} porte le chemin « {chemin} » ; attendu aucun "
            f"appel vers ces deux points d'entree, qui vident la base locale ou joignent le reseau "
            f"({SOURCE_ROUTES})"
        )

    assert not constats, (
        f"{PAGE} : {MOTIF_GARDE} — constats : "
        + " ; ".join(constats)
        + f" ; attendu un module d'ancrage qui n'ouvre que des bases construites sous `tmp_path`, sans "
        f"joindre le reseau, sans lancer le produit ni le solveur et sans poster vers un point "
        f"d'entree destructif ({SOURCE_CLI}, {SOURCE_ROUTES})"
    )


def test_rubriques_de_depannage(docs_dir: Path, sections) -> None:
    """Les cinq rubriques du critere 1 existent, dans son ordre, et portent leurs messages (D-93).

    Une rubrique retiree, renommee, vide ou deplacee est un constat nomme. Le controle porte sur les
    rubriques **declarees** et sur la coherence entre la page et la table `MESSAGES` : une famille hors
    mecanisme doit porter au moins un message, et la famille sans message ne doit en porter aucun.
    """
    constats = problemes_rubriques(docs_dir, sections)
    assert not constats, (
        f"{PAGE} : constats sur les rubriques : "
        + " ; ".join(constats)
        + f" ; attendu les cinq rubriques du critere 1, dans son ordre, chacune adossee a sa capture, "
        f"son rendu ou son litteral de source ({SOURCE_CLI}, {SOURCE_ROUTES}, D-93)"
    )


def test_messages_de_base_absente_ou_vide(
    docs_dir: Path, client, tmp_path, sections
) -> None:
    """Chaque message declare est retrouve par sa provenance et cite dans la rubrique de sa famille.

    La famille « base absente ou vide » est mesuree sur les deux surfaces : la capture de
    `_print_db_status` sur une base vide et sur la base peuplee de la fixture `app`, le rendu de l'ecran
    de version et de l'ecran d'etat sur une application a catalogue vide, et les litteraux de refus que
    seule la ligne de commande imprime. La sonde est unique et verifie chacune de ses prises.
    """
    produites = _produire(client, tmp_path)
    constats = problemes_messages(docs_dir, produites, sections)
    assert not constats, (
        f"{PAGE} : constats sur les messages et leur provenance : "
        + " ; ".join(constats)
        + f" ; attendu chaque entree de MESSAGES trouvee par sa provenance et citee dans la ligne de "
        f"tableau de sa rubrique ({SOURCE_CLI}, {SOURCE_ROUTES}, D-19, D-93)"
    )


def test_messages_de_saisie_invalide(docs_dir: Path, client, tmp_path, sections) -> None:
    """Les refus de saisie sont lus sur la ligne de statut rendue, jamais sur une memoire du code.

    Trois bornes distinctes sont mesurees sur trois ecrans de menu differents, le message d'objet
    introuvable est lu sous sa forme rendue en majuscules, et le refus de niveau n'est atteint qu'apres
    avoir conduit le parcours simplifie par la classe puis les elements — sans jamais poster un niveau
    valide, ce POST etant le calcul lui-meme.
    """
    produites = _produire(client, tmp_path)
    constats = problemes_messages(docs_dir, produites, sections)
    assert not constats, (
        f"{PAGE} : constats sur les refus de saisie : "
        + " ; ".join(constats)
        + f" ; attendu chaque refus rendu cite dans la rubrique de sa famille avec sa provenance, le "
        f"parcours simplifie etant conduit pas a pas avant de sonder l'etape du niveau "
        f"({SOURCE_ROUTES}, {SOURCE_PROFILE_INPUT}, D-19)"
    )


def test_messages_de_calcul_long(
    docs_dir: Path, client, tmp_path, sections, normalize
) -> None:
    """Ce que le produit expose pour un calcul, ce sont un etat et un budget, jamais une duree.

    Le seul message d'attente et la fin de calcul sont des litteraux lus dans leurs fichiers
    producteurs, l'indication de saisie et le budget sont rendus par des `GET` seulement : aucun calcul
    n'est lance, et aucune duree d'attente n'est promise par la page.
    """
    produites = _produire(client, tmp_path)
    constats = problemes_messages(docs_dir, produites, sections) + problemes_budget(
        docs_dir, sections, normalize
    )
    assert not constats, (
        f"{PAGE} : constats sur la famille du calcul : "
        + " ; ".join(constats)
        + f" ; attendu l'etat et le budget rendus par des lectures seules, cites dans la rubrique de "
        f"leur famille avec leur provenance ({SOURCE_CLI}, {SOURCE_OPTIMIZE_WIZARD}, D-19, D-76)"
    )


def test_clavier_inactif_est_un_mecanisme(docs_dir: Path, client, sections) -> None:
    """La famille sans message est adossee au mecanisme lu et au rendu, jamais a une chaine inventee.

    Les trois jetons du mecanisme sont exiges dans la rubrique **et** dans le fichier qui les porte ;
    les trois ecrans sans champ de saisie sont rendus et ne doivent porter aucune balise de champ ; et
    `MESSAGES` ne doit porter aucune entree pour cette famille (D-76, critere 1).
    """
    rendus = _rendus_sans_champ(client)
    constats = problemes_clavier(docs_dir, rendus, sections)
    assert not constats, (
        f"{PAGE} : constats sur la famille sans message : "
        + " ; ".join(constats)
        + f" ; attendu la rubrique de cette famille adossee aux jetons reels de {SOURCE_ECRAN_HTML} et "
        f"{SOURCE_TERMINAL_JS}, au rendu des ecrans sans champ, et sans aucune entree de MESSAGES "
        f"pour elle (D-76, D-93)"
    )


def test_pagination_a_deux_formes(docs_dir: Path, client, sections) -> None:
    """Le motif du statut depend de l'ecran ; celui du corps n'en depend pas.

    Mesure : la ligne de statut ne compose `PAGE n/total` que si l'ecran compte plus d'une page, alors
    que la ligne de corps la porte toujours. Une assertion qui exigerait le motif dans le statut d'un
    ecran a page unique serait rouge sur un produit correct — c'est le piege deja paye par le jalon, et
    c'est cette asymetrie que ce controle tient.
    """
    constats: list[str] = []
    mesure = (
        ("/list?page=1&size=1", "la liste des equipements", True),
        ("/sets?page=1&size=1", "la liste des panoplies", False),
    )
    for route, surface, pagine in mesure:
        reponse = client.get(route)
        _sonde(route, reponse)
        statut = _statut(reponse)
        corps = " ".join(_lignes_du_corps(reponse))
        if bool(MOTIF_PAGE_COMPOSE.search(statut)) != pagine:
            constats.append(
                f"{MOTIF_PAGINATION} : le statut rendu par GET {route}, sur {surface}, est "
                f"« {statut} » ; attendu le motif de pagination "
                f"{'present' if pagine else 'absent'}, la ligne de statut ne le composant que lorsque "
                f"l'ecran compte plus d'une page ({SOURCE_ROUTES})"
            )
        if not MOTIF_PAGE_COMPOSE.search(corps):
            constats.append(
                f"{MOTIF_PAGINATION} : le corps rendu par GET {route}, sur {surface}, ne porte aucun "
                f"motif de pagination compose ; attendu une ligne de corps « PAGE n/total » sur les "
                f"deux ecrans, le corps etant pagine independamment du statut ({SOURCE_ROUTES})"
            )
    assert not constats, (
        f"{PAGE} : constats sur la pagination rendue : "
        + " ; ".join(constats)
        + f" ; attendu le motif du statut dependant de l'ecran et celui du corps ne dependant pas de "
        f"lui ({SOURCE_ROUTES}, D-19)"
    )


def test_page_close_et_sans_valeur_volatile(docs_dir: Path, sections, normalize) -> None:
    """La page est close selon le gabarit, sans valeur de poste et sans duree promise.

    Les gardes de structure ne verifient ni les octets (CRLF sans BOM) ni les deux refus de valeur, ni
    la promesse de duree : c'est ce controle qui les porte, avec le bloc « Source de verite » dont
    chaque chemin doit exister depuis la racine du depot (D-73, D-75, D-102).
    """
    constats = problemes_page(docs_dir, sections, normalize)
    assert not constats, (
        f"{PAGE} : constats sur la cloture de la page : "
        + " ; ".join(constats)
        + f" ; attendu une page CRLF sans BOM, sans nombre de quatre chiffres ou plus, sans chemin de "
        f"poste et sans duree promise, dont le bloc « {TITRE_SOURCE} » est le dernier et dont la "
        f"derniere ligne non vide renvoie au {SOMMAIRE} (D-73, D-75, D-102)"
    )


def test_les_cinq_familles_sont_couvertes(docs_dir: Path, sections) -> None:
    """Le balayage final : cinq familles, dans l'ordre du critere 1, avant le bloc Source de verite.

    Chaque famille porte soit au moins une entree de `MESSAGES`, soit sa declaration de mecanisme :
    aucune famille muette, aucune famille inventee. Le controle lit la page et la table declaree, jamais
    une liste ecrite pour l'occasion.
    """
    texte = _texte_page(docs_dir)
    titres = [titre for titre, _ in sections(texte) if titre is not None]
    constats: list[str] = []

    if TITRE_SOURCE not in titres:
        constats.append(
            f"{MOTIF_SOURCE} : la section « {TITRE_SOURCE} » de {PAGE} est absente ; attendu ce bloc "
            f"en derniere section, apres les cinq familles (D-102, D-69)"
        )
        rang_source = len(titres)
    else:
        rang_source = titres.index(TITRE_SOURCE)

    rangs: list[int] = []
    for cle, titre in RUBRIQUES:
        if titre not in titres:
            constats.append(
                f"{MOTIF_RUBRIQUE_ABSENTE} : la famille « {cle} » n'a pas de rubrique « {titre} » dans "
                f"{PAGE} ; attendu les cinq familles du critere 1, dans son ordre (D-93, critere 1)"
            )
            continue
        rang = titres.index(titre)
        if rang > rang_source:
            constats.append(
                f"{MOTIF_SOURCE} : la rubrique « {titre} » est placee apres le bloc « {TITRE_SOURCE} » "
                f"de {PAGE} ; attendu les cinq familles avant ce bloc (D-102, D-69)"
            )
        rangs.append(rang)
        declares = [
            message for message, cle_message, _mode, _source in MESSAGES if cle_message == cle
        ]
        if cle in RUBRIQUES_MECANISME and declares:
            constats.append(
                f"{MOTIF_MESSAGE_INVENTE} : la famille « {titre} » est declaree comme un mecanisme sans "
                f"message et porte pourtant des entrees de MESSAGES ; attendu aucune entree pour elle "
                f"(D-76)"
            )
        if cle not in RUBRIQUES_MECANISME and not declares:
            constats.append(
                f"{MOTIF_RUBRIQUE_VIDE} : la famille « {titre} » ne porte aucun message declare ; "
                f"attendu au moins un message mesure (D-93)"
            )

    if rangs != sorted(rangs):
        constats.append(
            f"{MOTIF_RUBRIQUE_ABSENTE} : les rubriques des cinq familles de {PAGE} ne sont pas dans "
            f"l'ordre du critere 1 ({', '.join(titre for _cle, titre in RUBRIQUES)}) ; mesure : "
            f"{', '.join(titres)} (critere 1)"
        )

    if tuple(RUBRIQUES_MECANISME) != ("clavier",):
        constats.append(
            f"{MOTIF_MECANISME} : RUBRIQUES_MECANISME vaut {RUBRIQUES_MECANISME} ; attendu la seule "
            f"famille dont le produit ne porte aucun message (D-76, critere 1)"
        )

    assert not constats, (
        f"{PAGE} : constats sur les cinq familles : "
        + " ; ".join(constats)
        + f" ; attendu les cinq familles du critere 1, chacune adossee a au moins une entree de "
        f"MESSAGES ou a sa declaration de mecanisme ({SOURCE_CLI}, {SOURCE_ROUTES}, D-93)"
    )
