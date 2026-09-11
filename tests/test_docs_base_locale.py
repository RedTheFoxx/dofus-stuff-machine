"""Ancrage de la page `docs/base-locale.md` sur les constantes publiques et le rendu reel.

Le contrat va du code vers la page : le nom du fichier de la base, le dossier qui le porte, les sept
categories stockees et la fenetre de re-check sont lus a l'import des constantes publiques de
`dofus_stuff/database.py` et `dofus_stuff/sync.py` (D-14), puis confrontes a ce que la page cite ; les
surfaces sont rendues par le client de test Flask, en processus, sur la fixture `app` de
`tests/conftest.py` (D-32), et la sortie de l'etat de la base cote ligne de commande est capturee par
`redirect_stdout`. Aucun serveur n'est lance, aucune socket n'est ouverte, le programme du produit n'est
jamais execute et rien n'est ecrit sous `.data/` (D-15, D-81) : les bases que ce module ouvre sont
construites sous `tmp_path`, par la fixture `app` ou par `Database(data_dir=...)`.

Limite nommee : la garde `ast` de ce module est une demonstration statique et indirecte. Elle dit ce que
ce module importe et appelle, pas ce qu'un autre chemin ferait. En particulier, poster une confirmation
sur `/db/sync` declenche `ensure_up_to_date(force=True, offline=False, ...)` — reseau **et** ecriture — et
poster une confirmation sur `/db/clear` vide la base : la garde refuse cette paire dans le module, et
aucun controle de ce module ne poste de confirmation (D-79, D-81).

Limite nommee : la mesure d'empreinte locale de `.data/`, ecrite au plan 05-03, est vraie par
construction (L-2 de `04-SECURITY.md`) : la fixture construit sa base sous `tmp_path`, donc comparer la
base du depot a elle-meme ne peut pas detecter une ecriture faite par un autre module ; le controle qui
possede ce pouvoir est la mesure avant/apres autour de la suite entiere.

Limite nommee : la prose libre de la page (les phrases d'explication) n'est pas verifiee par un test. Les
controles portent sur les libelles, les valeurs et les messages **cites**, et ce module ne revendique
aucune exhaustivite de la redaction (D-85).

Limite nommee : l'execution JavaScript de `PURGE OUI` n'est pas observable en processus : le controle
s'arrete au libelle rendu par l'ecran `SAV-01` et a la lecture du fichier
`dofus_stuff/web/static/js/terminal.js` (A2 de la recherche, D-85).

Limite nommee : l'assertion de fins de ligne CRLF n'est pas portable hors d'un poste dont
`core.autocrlf` vaut `true` (AR-5) : elle est ecrite comme les phases 3 et 4 l'ont ecrite, sans etre
presentee comme portable.
"""

# Aucun `from __future__ import annotations` ici, contrairement aux autres modules de tests : la morsure
# `import_interdit` du plan insere un import interdit **en tete du fichier** pour prouver que la garde de
# cloture mord. Un import `__future__` place apres une autre instruction est une erreur de syntaxe
# (`from __future__ imports must occur at the beginning of the file`, verifie : `ast.parse` l'accepte mais
# `compile` la refuse, et c'est `compile` que la reecriture d'assertions de pytest utilise). Le module
# mourrait donc sur une erreur de collection au lieu de produire son constat, et la morsure ne serait pas
# discriminante. Les annotations de ce module (`ast.expr | None`, `list[tuple[int, str]]`) sont valides
# sans l'import differe.
import ast
import hashlib
import io
import re
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from dofus_stuff.api import SYNC_SOURCES
from dofus_stuff.cli import _print_db_status
from dofus_stuff.cli import build_parser as parseur_cli
from dofus_stuff.database import (
    DB_NAME,
    DEFAULT_DATA_DIR,
    ITEM_KINDS,
    META_GAME_VERSION,
    META_LAST_CHECKED_AT,
    Database,
)
from dofus_stuff.sync import CHECK_INTERVAL_SECONDS
from dofus_stuff.web import create_app
from dofus_stuff.web.__main__ import build_parser as parseur_web

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "base-locale.md"
SOMMAIRE = "sommaire.md"
README = "README.md"
SOURCE_DATABASE = "dofus_stuff/database.py"
SOURCE_SYNC = "dofus_stuff/sync.py"
SOURCE_API = "dofus_stuff/api.py"
SOURCE_CLI = "dofus_stuff/cli.py"
SOURCE_WEB_MAIN = "dofus_stuff/web/__main__.py"
SOURCE_ROUTES = "dofus_stuff/web/routes.py"
SOURCE_TERMINAL_JS = "dofus_stuff/web/static/js/terminal.js"

# Contrat de titres de la page : chaque titre est ecrit au caractere pres, le helper `section` de
# `tests/conftest.py` ne normalisant pas un titre. La constante compte les sections de ce plan et reste
# en accord exact avec la page a la fin de chaque tache : les taches 2 et 3, puis le plan 05-02,
# insererent leurs titres **juste avant** `## Source de vérité`, qui doit rester le dernier titre
# epingle. L'ordre relatif des titres deja crees ne bouge donc jamais, et la suite reste verte a chaque
# commit. Les titres sont nommes un a un, puis rassembles dans l'ordre du document : l'insertion d'une
# section ne peut pas decaler silencieusement la constante d'une autre.
TITRE_FICHIER = "## Le fichier de la base"
TITRE_CATEGORIES = "## Les catégories stockées"
TITRE_FENETRE = "## La fenêtre de re-check de 24 heures"
TITRE_SOURCE = "## Source de vérité"

TITRES_SECTION_ATTENDUS = (
    TITRE_FICHIER,
    TITRE_CATEGORIES,
    TITRE_FENETRE,
    TITRE_SOURCE,
)

# Marqueurs du gabarit reel (`dofus_stuff/web/templates/screen.html`) : le corps visible est encadre par
# `id="body"` et par la seule ligne de statut, qui porte les messages de refus.
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'
LIGNE_CORPS = re.compile(r'<div class="row">(.*?)</div>', re.S)

# Chemin de code cite entre accents graves, et forme du document entier, reprises du patron de la phase
# 4 : une page qui cite un chemin doit citer un chemin qui existe.
CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml|js|md|json|sql))`")
BOM_UTF8 = b"\xef\xbb\xbf"
FRAGMENT_H1 = "# "
FRAGMENT_LIEN_EXTERNE = "](http"
LIGNE_RETOUR = "[Retour au sommaire](sommaire.md)"
BALISE_CONSOLE = "```console"

# Categorie citee par la section des categories : une ligne de liste dont le premier jeton entre accents
# graves est un mot simple. La forme est exigee, jamais cherchee dans toute la section : un `kind` cite
# en prose (la colonne `kind`) n'est pas une categorie citee.
CATEGORIE_CITEE = re.compile(r"^-\s*`(?P<kind>[a-z]+)`", re.MULTILINE)

# Expression de la fenetre de re-check, telle que `dofus_stuff/sync.py:11` la declare.
EXPRESSION_FENETRE = "24 * 60 * 60"

# Motif de valeur volatile : un nombre de quatre chiffres ou plus est un compteur d'objets, une version
# de jeu, un horodatage ou une taille de fichier — jamais citable (D-73, D-75).
MOTIF_VOLATILE = re.compile(r"\d{4,}")

# Motifs de morsure portes par des constantes du module, jamais ecrits en clair dans la ligne
# d'assertion (regle posee au plan 03-03, tache 2) : pytest reproduit la ligne source du `assert`, une
# valeur en clair y serait trouvee meme si aucun constat n'avait ete produit. Valeurs ASCII, sans
# apostrophe, chacune incluse dans le constat qui la concerne.
MOTIF_FICHIER = "nom du fichier de la base"
MOTIF_CATEGORIES = "categories stockees"
MOTIF_FENETRE = "fenetre de re-check"
MOTIF_INDEX = "index du sommaire"
MOTIF_H1 = "titre de niveau 1"
MOTIF_DEFAUTS = "defauts hors-ligne"
MOTIF_CHAMPS_CLI = "champs de la ligne de commande"
MOTIF_CHAMPS_WEB = "champs de la surface web"
MOTIF_CONDITION = "champ conditionnel"
MOTIF_VOLATILES = "valeur volatile"
MOTIF_GARDE = "garde de cloture du harnais"
MOTIF_DATA_DIR = "repertoire de donnees non isole"
MOTIF_CONFIRMATION = "confirmation d une action destructive"
MOTIF_CRLF = "fins de ligne"

# Racines dont un import signalerait un risque reel : ouvrir la base, lancer un processus, ouvrir une
# socket, joindre le reseau. Le controle porte sur le risque, jamais sur une liste blanche de modules
# produit a tenir a jour — et **plus** sur l'import de `dofus_stuff.database`, qui est la matiere de
# cette page (constantes publiques et `Database`). Le risque de la phase 4 est donc deplace, pas
# supprime : ce que la garde refuse desormais, c'est un `data_dir` hors de `tmp_path` et une paire de
# confirmation.
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

# Noms d'appel dont la presence signalerait une action destructive, l'execution du produit ou une
# synchronisation. `ensure_up_to_date` et `pull_all` sont les deux points d'entree de synchronisation du
# produit (`dofus_stuff/sync.py:14` et `:74`) : par eux, un controle atteindrait le reseau au travers de
# `dofus_stuff.api`.
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"
APPELS_SYNCHRO_PRODUIT = ("ensure_up_to_date", "pull_all")

# Valeurs de confirmation acceptees par `dofus_stuff/web/routes.py:810` : les poster declenche la
# synchronisation web (`offline=False` en dur) ou le vidage de la base.
CONFIRMATIONS_INTERDITES = ("O", "Y", "OUI", "YES")

# Appels qui construisent une base, et formes de `data_dir` admises : une expression derivee de
# `tmp_path`, ou un nom lie dans le module a une telle expression (patron `dossier = tmp_path / "absent"`).
CIBLES_DATA_DIR = ("Database", "create_app")
REPERTOIRES_ISOLES = ("tmp_path", "web_config")


def _texte_page(docs_dir: Path) -> str:
    """Texte de la page, lu en UTF-8 explicite ; page absente = AssertionError localisante (D-13).

    Jamais de `FileNotFoundError` brut : l'echec nomme la page, le chemin attendu et les fichiers de
    code dont elle decrit la surface. Toute lecture de la page passe par ici.
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page de la base locale, decrite par "
            f"{SOURCE_DATABASE} et {SOURCE_SYNC}, livree dans docs/"
        )
    return chemin.read_text(encoding="utf-8")


def _lignes_du_corps(reponse) -> list[str]:
    """Lignes visibles du corps d'un ecran, jamais la reponse entiere.

    La reponse entiere porte la coquille, la ligne d'en-tete et la ligne de statut : une assertion
    ecrite sur elle serait vraie pour une raison etrangere a l'ecran controle.
    """
    texte = reponse.get_data(as_text=True)
    corps = texte.split(MARQUEUR_CORPS, 1)[1].split(MARQUEUR_STATUT, 1)[0]
    return [ligne.rstrip() for ligne in LIGNE_CORPS.findall(corps)]


def _statut(reponse) -> str:
    """Texte de la ligne de statut : la seule source des messages de refus."""
    texte = reponse.get_data(as_text=True)
    return texte.split(MARQUEUR_STATUT, 1)[1].split(">", 1)[1].split("</div>", 1)[0]


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
    """Noms lies dans le module a une expression derivee de `tmp_path`.

    Une base construite par `Database(data_dir=dossier)` ou `dossier = tmp_path / "absent"` est isolee
    autant qu'une expression ecrite en clair : sans cette lecture, la variable intermediaire serait
    signalee comme un dossier du depot et la garde deviendrait un faux rouge que les plans suivants
    devraient desactiver.
    """
    noms: set[str] = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Assign):
            continue
        if "tmp_path" not in ast.unparse(noeud.value):
            continue
        for cible in noeud.targets:
            if isinstance(cible, ast.Name):
                noms.add(cible.id)
    return noms


def _cibles_data_dir(arbre: ast.AST) -> list[tuple[int, str]]:
    """Appels qui construisent une base sur un dossier non isole : `(ligne, texte de data_dir)`.

    Le risque de cette phase n'est pas l'import de `dofus_stuff.database` — c'est la matiere de la page
    — mais un `data_dir` qui ne vient pas de `tmp_path` : `Database(data_dir=DEFAULT_DATA_DIR)` ouvrirait
    la base du depot, et `Database(data_dir=RACINE_DEPOT)` la construirait a la racine. Sont admis une
    expression derivee de `tmp_path`, un nom lie a une telle expression, et la base de la fixture `app`,
    que la fixture construit elle-meme sous `tmp_path`.
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


def test_garde_de_cloture_du_harnais() -> None:
    """Le module n'ouvre que des bases isolees, ne joint ni reseau ni processus, et ne poste rien.

    La propriete est verifiee sur le texte de ce module par `ast`, et jamais par une recherche de
    chaines : le module cite lui-meme les noms interdits dans ses messages, une recherche textuelle se
    detecterait elle-meme. Le controle porte sur le risque reel — ouvrir la base du depot, lancer un
    processus, ouvrir une socket, joindre le reseau, supprimer un fichier, executer le produit,
    synchroniser, poster une confirmation — donc un import public pur ajoute plus tard passe sans
    revision, alors qu'un import qui tirerait la base rougit.

    Limite nommee : l'import de `dofus_stuff.database` n'est **plus** refuse ici, contrairement au
    module de la phase 4 : c'est la source des constantes publiques que la page cite (Pitfall 2 de la
    recherche). Le risque est deplace sur les deux interdits qui ont un sens pour cette page — un
    `data_dir` hors de `tmp_path` et une paire de confirmation — jamais supprime.
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
            f"({SOURCE_DATABASE}, {SOURCE_ROUTES})"
        )
    if APPEL_PRODUIT in appeles:
        constats.append(
            f"appel a {APPEL_PRODUIT}() dans le module d'ancrage ; attendu un ancrage par les "
            f"parseurs publics et le client de test Flask, le produit n'etant jamais execute "
            f"({SOURCE_CLI}, {SOURCE_ROUTES})"
        )
    synchronisations = sorted(set(APPELS_SYNCHRO_PRODUIT) & appeles)
    if synchronisations:
        constats.append(
            f"appel(s) de synchronisation du produit : {', '.join(synchronisations)} ; attendu aucun "
            f"appel de synchronisation dans le module d'ancrage, ces deux points d'entree atteignant "
            f"le reseau au travers de {SOURCE_API}"
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
            f"« {texte_data_dir} » ; attendu un dossier derive de `tmp_path`, jamais la racine du "
            f"depot ni `DEFAULT_DATA_DIR` ({SOURCE_DATABASE})"
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
            confirmation = paires.get("confirm", "").strip().upper()
            if confirmation in CONFIRMATIONS_INTERDITES:
                constats.append(
                    f"{MOTIF_CONFIRMATION} : la confirmation « {confirmation} » est postee ligne "
                    f"{noeud.lineno} ; attendu aucune confirmation, `POST /db/sync` contactant l'API "
                    f"hors-ligne et `POST /db/clear` vidant la base ({SOURCE_ROUTES})"
                )

    assert not constats, (
        f"{PAGE} : {MOTIF_GARDE} — constats : "
        + " ; ".join(constats)
        + f" ; attendu un module d'ancrage qui n'ouvre que des bases construites sous `tmp_path`, "
        f"sans joindre le reseau, sans synchroniser, sans supprimer de fichier et sans poster de "
        f"confirmation ({SOURCE_DATABASE}, {SOURCE_ROUTES})"
    )


def test_page_et_index_de_la_base_locale(docs_dir: Path, normalize, section) -> None:
    """La page existe, son index est coherent, et ses valeurs fondatrices viennent du code (BASE-01).

    Tranche verticale du plan : la page, sa ligne d'index, le harnais et les constantes publiques sont
    traverses d'un bout a l'autre par ce seul controle. Le libelle d'index est lu dans le sommaire, il
    n'est jamais ecrit deux fois de memoire, et chaque valeur citee est confrontee a la constante
    importee : renommer le fichier de la base, retirer une categorie ou changer la fenetre de re-check
    dans le code fait rougir ce controle.

    Limite honnete : ce controle ne revendique aucune exhaustivite sur la prose de la page. Il porte sur
    les titres, le titre de niveau 1, la ligne de retour, les octets, les chemins cites et les valeurs
    fondatrices — rien de plus (D-85).
    """
    chemin = docs_dir / PAGE
    texte = _texte_page(docs_dir)
    octets = chemin.read_bytes()
    constats: list[str] = []

    # 1. La ligne d'index de la page, lue dans la table du sommaire : le libelle cite sert de reference
    #    au titre de niveau 1, il n'est jamais ecrit deux fois de memoire.
    sommaire = (docs_dir / SOMMAIRE).read_text(encoding="utf-8")
    entree = re.search(rf"\|\s*\[(?P<libelle>[^\]]+)\]\({re.escape(PAGE)}\)", sommaire)
    if entree is None:
        constats.append(
            f"{PAGE} : page non listee dans l'{MOTIF_INDEX} ; attendu une ligne de la table "
            f"« ## Index » de {SOMMAIRE} pointant vers {PAGE} (D-70, D-06)"
        )
    libelle = entree.group("libelle") if entree is not None else ""

    # 2. Le gabarit : les sections epinglees, dans l'ordre, puis un seul titre de niveau 1.
    titres = [ligne.strip() for ligne in texte.splitlines() if ligne.startswith("## ")]
    if len(titres) != len(TITRES_SECTION_ATTENDUS):
        constats.append(
            f"{PAGE} : la page porte {len(titres)} section(s) de niveau 2 ({', '.join(titres)}) ; "
            f"attendu exactement {len(TITRES_SECTION_ATTENDUS)} sections, dans cet ordre : "
            f"{', '.join(TITRES_SECTION_ATTENDUS)}"
        )
    for index, attendu in enumerate(TITRES_SECTION_ATTENDUS):
        trouve = titres[index] if index < len(titres) else ""
        if normalize(attendu) != normalize(trouve):
            constats.append(
                f"{PAGE} : section {index + 1} attendue « {attendu.lstrip('#').strip()} », section "
                f"trouvee « {trouve} » ; attendu les {len(TITRES_SECTION_ATTENDUS)} sections de la "
                f"page, dans l'ordre du document (D-69)"
            )

    h1 = [ligne.strip() for ligne in texte.splitlines() if ligne.startswith(FRAGMENT_H1)]
    if len(h1) != 1:
        constats.append(
            f"{PAGE} : la page porte {len(h1)} {MOTIF_H1} ({', '.join(h1)}) ; attendu un seul titre de "
            f"niveau 1, celui de la page (D-69)"
        )
    elif libelle:
        titre = h1[0][len(FRAGMENT_H1) :].strip()
        if normalize(titre) != normalize(libelle):
            constats.append(
                f"{PAGE} : H1 « {titre} » different du libelle d'index « {libelle} » ; attendu le "
                f"libelle d'index de {SOMMAIRE} pour {PAGE} (D-11, D-69)"
            )

    # 3. La ligne de retour, en derniere ligne non vide de la page.
    remplies = [ligne.strip() for ligne in texte.splitlines() if ligne.strip()]
    derniere = remplies[-1] if remplies else ""
    if derniere != LIGNE_RETOUR:
        constats.append(
            f"{PAGE} : la derniere ligne non vide vaut « {derniere} » ; attendu « {LIGNE_RETOUR} » "
            f"comme derniere ligne de la page (D-69)"
        )

    # 4. Les octets, lus en binaire : un texte re-encode ne dirait rien de l'encodage.
    fins = octets.count(b"\n")
    retours = octets.count(b"\r\n")
    if octets.startswith(BOM_UTF8):
        constats.append(
            f"{PAGE} : la page commence par un BOM ; attendu un fichier UTF-8 sans BOM (D-67)"
        )
    if retours != fins:
        constats.append(
            f"{PAGE} : {MOTIF_CRLF} — la page porte {fins} fin(s) de ligne pour {retours} retour(s) "
            f"chariot ; attendu des fins de ligne CRLF sur toutes les lignes, comme les autres pages "
            f"de docs/ (D-67)"
        )

    # 5. Aucun bloc de commandes, aucun lien sortant du depot.
    if BALISE_CONSOLE in texte:
        constats.append(
            f"{PAGE} : la page porte un bloc de commandes « {BALISE_CONSOLE} » ; attendu aucun bloc de "
            f"ce genre, un bloc d'exemple etant recopiable par le lecteur (D-80)"
        )
    if FRAGMENT_LIEN_EXTERNE in texte:
        constats.append(
            f"{PAGE} : la page porte « {FRAGMENT_LIEN_EXTERNE} », un lien sortant du depot ; attendu "
            f"des liens internes seulement, la page decrivant le produit de ce depot (D-01)"
        )

    # 6. Le bloc « Source de verite », et chaque chemin cite existe depuis la racine du depot.
    corps_source = section(texte, TITRE_SOURCE, PAGE)
    for attendu in (SOURCE_DATABASE, SOURCE_SYNC, SOURCE_API):
        if attendu not in corps_source:
            constats.append(
                f"{PAGE} : la section « {TITRE_SOURCE} » ne cite pas « {attendu} » ; attendu le bloc "
                f"qui nomme les fichiers dont la page decrit la surface (D-03, D-69)"
            )
    chemins = sorted(set(CHEMIN_CITE.findall(texte)))
    if not chemins:
        constats.append(
            f"{PAGE} : la page ne cite aucun chemin de code ; attendu au moins un chemin, la page "
            f"ancrant ses libelles sur le code de ce depot (D-69)"
        )
    for cite in chemins:
        if not (RACINE_DEPOT / cite).exists():
            constats.append(
                f"{PAGE} : la page cite « {cite} » et ce chemin n'existe pas ; attendu un chemin "
                f"existant, un chemin disparu signalant une page desalignee (D-69)"
            )

    # 7. Le fichier de la base : le nom et le dossier sont ceux des constantes publiques (D-74).
    corps_fichier = section(texte, TITRE_FICHIER, PAGE)
    if "DB_NAME" not in corps_fichier:
        constats.append(
            f"{MOTIF_FICHIER} : la section « {TITRE_FICHIER} » ne nomme pas la constante `DB_NAME` ; "
            f"attendu la constante publique que la page doit citer ({SOURCE_DATABASE}:12)"
        )
    if DB_NAME not in corps_fichier:
        constats.append(
            f"{MOTIF_FICHIER} : la section « {TITRE_FICHIER} » ne cite pas « {DB_NAME} » ; attendu le "
            f"nom du fichier de la base, egal a `DB_NAME` lu a l'import ({SOURCE_DATABASE}:12, D-74)"
        )
    if "DEFAULT_DATA_DIR" not in corps_fichier:
        constats.append(
            f"{MOTIF_FICHIER} : la section « {TITRE_FICHIER} » ne nomme pas la constante "
            f"`DEFAULT_DATA_DIR` ; attendu la constante publique que la page doit citer "
            f"({SOURCE_DATABASE}:13)"
        )
    if DEFAULT_DATA_DIR.name not in corps_fichier:
        constats.append(
            f"{MOTIF_FICHIER} : la section « {TITRE_FICHIER} » ne cite pas "
            f"« {DEFAULT_DATA_DIR.name} » ; attendu le dossier de la base, egal au nom de "
            f"`DEFAULT_DATA_DIR` lu a l'import ({SOURCE_DATABASE}:13, D-74)"
        )

    # 8. Les sept categories stockees : nommees, et aucune autre.
    corps_categories = section(texte, TITRE_CATEGORIES, PAGE)
    citees = set(CATEGORIE_CITEE.findall(corps_categories))
    for kind in ITEM_KINDS:
        if kind not in citees:
            constats.append(
                f"{MOTIF_CATEGORIES} : la section « {TITRE_CATEGORIES} » ne cite pas la categorie "
                f"« {kind} » ; attendu les {len(ITEM_KINDS)} categories stockees, lues dans "
                f"`ITEM_KINDS` ({SOURCE_DATABASE}:18-26, D-74)"
            )
    for kind in sorted(citees - set(ITEM_KINDS)):
        constats.append(
            f"{MOTIF_CATEGORIES} : la section « {TITRE_CATEGORIES} » cite la categorie "
            f"« {kind} », absente de `ITEM_KINDS` ; attendu aucune categorie que le code ne stocke "
            f"pas ({SOURCE_DATABASE}:18-26, D-74)"
        )
    kinds_synchro = tuple(kind for _, _, kind in SYNC_SOURCES)
    if kinds_synchro != ITEM_KINDS:
        constats.append(
            f"{MOTIF_CATEGORIES} : les kinds de `SYNC_SOURCES` ({', '.join(kinds_synchro)}) different "
            f"de `ITEM_KINDS` ({', '.join(ITEM_KINDS)}) ; attendu deux sources concordantes, la page "
            f"citant les categories que la synchronisation ecrit ({SOURCE_API}:19-28, D-14)"
        )

    # 9. La fenetre de re-check : la constante nommee, son expression citee, et la meme duree des deux
    #    cotes. Aucune duree calculee, aucun horodatage, aucune date (D-73).
    corps_fenetre = section(texte, TITRE_FENETRE, PAGE)
    if "CHECK_INTERVAL_SECONDS" not in corps_fenetre:
        constats.append(
            f"{MOTIF_FENETRE} : la section « {TITRE_FENETRE} » ne nomme pas la constante "
            f"`CHECK_INTERVAL_SECONDS` ; attendu la constante publique que la page doit citer "
            f"({SOURCE_SYNC}:11)"
        )
    if EXPRESSION_FENETRE not in corps_fenetre:
        constats.append(
            f"{MOTIF_FENETRE} : la section « {TITRE_FENETRE} » ne cite pas l'expression "
            f"« {EXPRESSION_FENETRE} » ; attendu l'expression de `CHECK_INTERVAL_SECONDS` lue dans le "
            f"code ({SOURCE_SYNC}:11, D-73)"
        )
    if CHECK_INTERVAL_SECONDS != 24 * 60 * 60:
        constats.append(
            f"{MOTIF_FENETRE} : `CHECK_INTERVAL_SECONDS` vaut {CHECK_INTERVAL_SECONDS} et la page "
            f"annonce une journee ({EXPRESSION_FENETRE}) ; attendu la meme fenetre des deux cotes "
            f"({SOURCE_SYNC}:11, D-73)"
        )

    # 10. Aucune valeur volatile epinglee dans la prose (D-73, D-75).
    volatiles = sorted(set(MOTIF_VOLATILE.findall(texte)))
    if volatiles:
        constats.append(
            f"{MOTIF_VOLATILES} : la page porte {', '.join(volatiles)} ; attendu aucun nombre de "
            f"quatre chiffres ou plus — ni compteur d'objets, ni version de jeu, ni horodatage, ni "
            f"taille de fichier (D-73, D-75)"
        )

    assert not constats, (
        f"{PAGE} : constats sur la page et son index : "
        + " ; ".join(constats)
        + f" ; attendu la page de la base locale listee dans {SOMMAIRE}, ouverte par un H1 egal a son "
        f"libelle d'index, portant ses sections dans l'ordre, la ligne de retour en dernier et des "
        f"octets CRLF, avec le fichier, les sept categories et la fenetre de re-check lus dans "
        f"{SOURCE_DATABASE} et {SOURCE_SYNC}"
    )
