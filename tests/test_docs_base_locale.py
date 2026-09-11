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
TITRE_WEB = "## Le mode hors-ligne du web"
TITRE_CLI = "## Le mode hors-ligne de la ligne de commande"
TITRE_CHAMPS_CLI = "## L'état de la base en ligne de commande"
TITRE_CHAMPS_WEB = "## L'état de la base dans l'interface web"
TITRE_CREATION = "## Le premier contact crée la base"
TITRE_REFUS = "## La synchronisation refuse le mode hors-ligne"
TITRE_SYNCHRO_WEB = "## L'écran de synchronisation du web contacte l'API"
TITRE_DESTRUCTRICES = "## Les commandes destructrices"
TITRE_SOURCE = "## Source de vérité"

TITRES_SECTION_ATTENDUS = (
    TITRE_FICHIER,
    TITRE_CATEGORIES,
    TITRE_FENETRE,
    TITRE_WEB,
    TITRE_CLI,
    TITRE_CHAMPS_CLI,
    TITRE_CHAMPS_WEB,
    TITRE_CREATION,
    TITRE_REFUS,
    TITRE_SYNCHRO_WEB,
    TITRE_DESTRUCTRICES,
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

# Textes d'aide des deux parseurs, releves sur le rendu de leur API publique (D-14) et non recopies d'un
# souvenir : chaque phrase est exigee du parseur **et** de la section de sa surface, ce qui interdit de
# les echangees ou de les attribuer a la mauvaise surface (D-71, D-72). `argparse` coupant l'aide a la
# largeur du terminal, la comparaison passe par la fixture `normalize` (D-11) et jamais par un `==`
# (Pitfall 5).
AIDE_WEB_OFFLINE = "Ne pas contacter l'API au démarrage (défaut : oui)"
AIDE_CLI_OFFLINE = "Ne pas contacter l'API (échoue si la base locale est vide)"

# Marques exigees de chaque section, comparees normalisees : la section du web doit dire que le mode
# hors-ligne y est le **defaut**, celle de la ligne de commande qu'il y est **exige**. Une section qui
# citerait le drapeau sans dire dans quel sens il penche ne prouverait rien de sa surface.
MARQUES_DEFAUT_WEB = ("par defaut", "defaut", "actif sans rien preciser")
MARQUES_EXIGENCE_CLI = ("requis", "obligatoire", "necessaire", "exige")

# Marques de creation exigees de la section du premier contact, comparees normalisees : la section doit
# dire que le fichier est **cree** au premier contact, pas seulement qu'il est lu ou decrit (D-77).
MARQUES_CREATION = ("cree", "creation", "cree le fichier", "cree la base")

# Libelle de fichier de l'ecran d'etat du web, dans sa forme exacte (majuscules et « : » final, comme
# toute cette surface) : c'est lui qui prouve que l'ecran d'etat a bien ete rendu — sur une base
# fraichement creee comme sur une base peuplee — et non une page d'erreur ou un corps vide. Il est
# compare par l'ensemble des libelles produits (`_libelles_produits`), jamais par une recherche dans le
# corps entier, qui confondrait le libelle d'une ligne avec le nom d'un fichier cite en prose.
LIBELLE_FICHIER_RENDU = "FICHIER :"

# Marques du cas hors-ligne de l'ecran de synchronisation, comparees normalisees : la section doit dire
# ce cas **explicitement**, un lecteur pouvant conclure du mode hors-ligne du web que cet ecran ne
# contacte pas l'API (D-79).
MARQUES_HORS_LIGNE = (
    "meme hors-ligne",
    "y compris hors-ligne",
    "quel que soit le mode hors-ligne",
)

# Marques d'un code de retour non nul, comparees normalisees : la section du refus doit dire que la
# commande s'arrete, pas seulement qu'un message s'affiche (D-78).
MARQUES_CODE_RETOUR = ("code de retour 1", "code de retour", "code 1")

# Message de refus de `db sync --offline` et phrase du corps de confirmation de l'ecran de
# synchronisation : deux litteraux **releves sur le code** (`dofus_stuff/cli.py:346` et
# `dofus_stuff/web/routes.py:794` de la recherche), pins comme constantes du module et exiges des deux
# cotes — du code, lu par `ast`, et de la page ou du rendu (patron du plan 05-01, D-71/D-72). Une page
# qui les paraphraserait rougit, et un code qui les renommerait rougit aussi.
MESSAGE_REFUS = "Erreur : --offline incompatible avec db sync"
PHRASE_SYNCHRO = "CETTE OPERATION CONTACTE L'API DOFUSDUDE"
INVITE_CONFIRMATION = "CONFIRMER ? (O=OUI / N=NON)"

# Les deux commandes destructrices du critere 4. Le motif de `db clear` est celui deja employe par
# `tests/test_docs_structure.py:20` et `tests/test_docs_wizard.py:186` : le meme motif partout, pour que
# les pages qui le portent ne divergent pas. La seconde commande n'est pas une commande Python — son
# effet est du JavaScript —, elle est donc un **jeton** exige au rendu de l'ecran des sauvegardes et dans
# le fichier du terminal.
COMMANDE_DESTRUCTRICE = re.compile(r"\bdb\s+clear\b")
JETON_PURGE = "PURGE OUI"

# Balise du bloc de commandes de la console, deja epinglee par `tests/test_docs_parcours.py:1481` sous ce
# nom : aucune commande destructrice ne doit apparaitre dans un exemple recopiable (D-80).
BALISE_COMMANDE = BALISE_CONSOLE

# Marques du caractere destructeur, comparees normalisees : l'avertissement doit porter sur la **meme
# ligne** que la commande (D-80). La marque est exigee de **chaque** ligne porteuse, jamais d'une autre
# ligne de la page.
MARQUES_DESTRUCTRICES = ("destruct", "detruit", "irreversible", "danger", "attention")

# Cibles distinctes des deux commandes (Pitfall 7) : la premiere vide la base SQLite, la seconde supprime
# les sauvegardes du navigateur. Une page qui reprendrait la formulation « de la base » pour la seconde
# serait fausse, et le controle le dit.
MARQUES_BASE = ("base locale", "dofus.sqlite3", "sqlite")
MARQUES_SAUVEGARDES = ("sauvegardes", "navigateur")

# Marques du fait que ces commandes ne sont l'etape d'aucun parcours (D-80).
MARQUES_HORS_PARCOURS = ("aucun parcours", "aucune etape")

# Marques du fait que `clear` vide les tables sans supprimer le fichier (D-81) : la nuance est ce qui
# distingue « la base est vide » de « la base a disparu », et la page doit la porter.
MARQUES_FICHIER_CONSERVE = (
    "le fichier n'est pas supprime",
    "fichier conserve",
    "ne supprime pas le fichier",
)

# Les deux instructions de suppression de `Database.clear`, lues par `ast` dans le code (D-81).
SUPPRESSION_ITEMS = "DELETE FROM items"
SUPPRESSION_META = "DELETE FROM meta"

# Traitement de `PURGE OUI` dans le JavaScript de l'ecran des sauvegardes : la comparaison du libelle, et
# l'appel qui retire la cle des sauvegardes du navigateur. Litteraux du fichier, jamais executes — aucun
# navigateur n'est lance et aucun JavaScript n'est compile (A2 de la recherche, D-85).
COMPARAISON_PURGE = re.compile(r"""upper\s*===\s*["']PURGE OUI["']""")
RETRAIT_SAUVEGARDES = re.compile(r"localStorage\.removeItem\(\s*SAVES_KEY\s*\)")

# Perimetre du critere 4, ecrit noir sur blanc dans le module (D-87, Pitfall 8) : le controle porte sur la
# page de ce depot et sur ce module. L'occurrence de `README.md` ligne 80 — seule du depot ou une commande
# destructrice figure dans un bloc de commandes sans avertissement — est **hors du mandat de reecriture**
# de cette phase (D-87 limite le travail du README a la resolution de ses renvois) : elle est consignee
# pour la phase 6, proprietaire de la completude, et **aucun** constat de ce module ne rougit a cause
# d'elle. La docstring de `test_commandes_destructrices` cite cette constante, et le controle verifie cette
# citation.
LIMITE_PERIMETRE = (
    "Ce controle porte sur docs/base-locale.md et sur ce module. L'occurrence de README.md ligne 80, "
    "seule du depot ou une commande destructrice figure dans un bloc de commandes sans avertissement, "
    "est hors du mandat de reecriture de cette phase (D-87) : elle est consignee pour la phase 6, "
    "proprietaire de la completude, et aucun constat de ce controle ne la mentionne."
)

# Chemin d'ecran cite entre accents graves : un jeton qui commence par une barre oblique est un chemin de
# route, jamais un chemin de fichier du depot (ceux-ci passent par `CHEMIN_CITE`). Chaque chemin cite doit
# etre declare par un decorateur `get`/`post` de `dofus_stuff/web/routes.py` (D-76) : la page ne nomme
# aucun ecran que le code ne declare.
CHEMIN_ECRAN = re.compile(r"`(?P<chemin>/[\w./<>-]*)`")

# Un libelle d'etat, dans la section qui le cite, est ecrit entre accents graves et se termine par
# « : » (« | `Fichier :` | le chemin ... | »). Le motif est ancre en debut de ligne pour ignorer les
# citations en prose, et la classe `[^`]+` ne peut pas traverser un accent grave : il capture donc le
# contenu d'un seul intervalle, jamais celui de plusieurs.
MOTIF_LIBELLE_CITE = re.compile(r"^\|\s*`(?P<libelle>[^`]+ :)`", re.MULTILINE)

# Prefixe des lignes de categorie produites par la ligne de commande (`  - equipment : 2`) ; il les
# distingue des libelles de champ au moment de lire une sortie.
PREFIXE_LIGNE_CATEGORIE = "  - "

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
MOTIF_CREATION = "creation de la base par le premier contact"
MOTIF_ROUTE = "chemin d ecran cite par la page"
MOTIF_REFUS = "refus de la synchronisation hors-ligne"
MOTIF_SYNCHRO_WEB = "synchronisation web hors-ligne"
MOTIF_DESTRUCTRICES = "commandes destructrices"
MOTIF_EFFET = "effet de la commande destructrice"
MOTIF_EXEMPLE = "bloc de commandes"

# Motifs de morsure du plan 05-03 (vague 3), portes par des constantes du module comme les precedents :
# pytest reproduit la ligne source du `assert`, une valeur ecrite en clair y serait trouvee meme si
# aucun constat n'avait ete produit. Valeurs ASCII, sans apostrophe, chacune incluse dans le constat
# qui la concerne.
MOTIF_README = "renvoi du README"
MOTIF_LIEN_D63 = "renvoi en prose sans lien vers la page de la base locale"
MOTIF_SECTION = "section attendue de la page"
MOTIF_SOURCE = "chemin du bloc source de verite"
MOTIF_LIEN_EXTERNE = "lien externe"
MOTIF_BASE_ABSENTE = "base locale du depot absente"
MOTIF_EMPREINTE_CHANGEE = "empreinte de la base locale modifiee"

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

# Contenu et objets du plan 05-03 : le detecteur de renvois du `README.md` (D-87), la dette denouee de
# la page voisine (D-63/D-44), la cloture de la page (D-67, D-69, D-73) et la mesure d'empreinte de
# `.data/` (D-81, D-89). Le motif des liens Markdown est celui deja employe par
# `tests/test_docs_wizard.py:2475` : une cible lue entre parentheses, jamais une cible reecrite.
MOTIF_LIEN_MARKDOWN = re.compile(r"\[(?P<libelle>[^\]]*)\]\((?P<cible>[^)]+)\)")
CIBLES_EXTERNES = ("http://", "https://", "mailto:")
TITRE_SECTION_RENVOI = "### Ce que cette page ne décrit pas"
PAGE_PARCOURS = "parcours-simplifie.md"
# Ligne de retour de la page, deja epinglee par le plan 05-01 sous le nom `LIGNE_RETOUR` : le plan
# 05-03 la nomme `LIEN_RETOUR`, et le litteral n'est pas reecrit une seconde fois.
LIEN_RETOUR = LIGNE_RETOUR
TITRE_H1 = "# Base locale"
BASE_LOCALE = (".data", "dofus.sqlite3")
# Renvois attendus vers la page de la base locale dans `docs/parcours-simplifie.md` : deux, l'un dans la
# phrase d'introduction, l'autre dans la section des renvois (D-63, D-86).
RENVOIS_PAGE_VOISINE = 2
# Formulaire d'un jeton entre accents graves qui ressemble a un chemin de fichier (une barre oblique, ou
# un suffixe de fichier connu) : le bloc « Source de verite » de la page est lu par ce motif, et chaque
# chemin trouve est exige sur disque (D-03, D-69).
MOTIF_JETON_ACCENTS = re.compile(r"`(?P<jeton>[^`]+)`")
SUFFIXES_CHEMIN = (".py", ".md", ".js", ".json")
# Ecrans rendus par le module pour la mesure d'empreinte : l'etat de la base, l'ecran de
# synchronisation, l'ecran de vidage et les sauvegardes, tous en **lecture** (aucun `POST`, D-81).
ECRANS_RENDUS = ("/db/status", "/db/sync", "/db/clear", "/saves")


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


def _routes_declarees() -> set[str]:
    """Chemins d'ecran declares par les decorateurs `get`/`post` de `dofus_stuff/web/routes.py`.

    Lecture par `ast` sur les **decorateurs des fonctions**, jamais par expression reguliere du source ni
    par introspection privee de Flask : seuls comptent les appels dont la fonction est un attribut nomme
    `get` ou `post` et dont le premier argument est un litteral de chaine. `request.args.get("page", 1)`
    n'est donc pas un chemin — ce n'est pas un decorateur — et `@bp.route("/search", methods=[...])`,
    qui declare pourtant un ecran, n'entre pas dans cet ensemble : la page ne cite que des chemins
    d'ecran `get`/`post`, et la lecture reste celle que le plan 05-02 a epinglee.
    """
    arbre = ast.parse((RACINE_DEPOT / SOURCE_ROUTES).read_text(encoding="utf-8"))
    chemins: set[str] = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorateur in noeud.decorator_list:
            if not isinstance(decorateur, ast.Call):
                continue
            if not isinstance(decorateur.func, ast.Attribute):
                continue
            if decorateur.func.attr not in ("get", "post") or not decorateur.args:
                continue
            premier = decorateur.args[0]
            if isinstance(premier, ast.Constant) and isinstance(premier.value, str):
                chemins.add(premier.value)
    return chemins


def _litteraux_du_module(arbre: ast.AST) -> set[str]:
    """Litteraux de chaine d'un module produit, lus par `ast`.

    C'est le mecanisme le plus faible des trois employes par ce module — un litteral dit ce que le code
    **ecrit**, pas ce qu'il rend — mais la seule route possible ici : `main()` n'est jamais execute
    (D-15), le refus hors-ligne de la ligne de commande n'a donc aucun rendu observable. La docstring du
    test le dit, et le controle voisin lit en plus la **structure** du refus (l'appel reseau ne doit pas
    en descendre), pour que le litteral seul ne porte pas toute la preuve.
    """
    return {
        noeud.value
        for noeud in ast.walk(arbre)
        if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str)
    }


def _litteraux_de_fonction(arbre: ast.AST, nom: str) -> set[str]:
    """Litteraux de chaine d'une fonction nommee, lus par `ast` ; ensemble vide si elle est absente.

    Sert a lire l'ecran de synchronisation dans `dofus_stuff/web/routes.py` et non dans tout le fichier :
    un litteral retrouve ailleurs ne dirait pas que c'est **cet** ecran qui l'annonce.
    """
    for noeud in ast.walk(arbre):
        if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)) and noeud.name == nom:
            return {
                enfant.value
                for enfant in ast.walk(noeud)
                if isinstance(enfant, ast.Constant) and isinstance(enfant.value, str)
            }
    return set()


def _constats_bloc_refus(arbre: ast.AST) -> list[str]:
    """Constats sur le bloc de refus hors-ligne de `main` : present, sortant en 1, sans reseau.

    Le refus est lu **par structure**, jamais par texte : un `if` dont le test est l'attribut `offline`
    et dont le corps porte un `return` de valeur 1. Exiger en plus qu'aucun appel de synchronisation du
    produit ne soit descendant de ce corps encode la propriete qui compte — le refus **precede** l'appel
    reseau, il ne le suit pas — et c'est ce fait qui rend la synchronisation inatteignable quand
    l'option est donnee (D-78).
    """
    constats: list[str] = []
    fonctions = [
        noeud
        for noeud in ast.walk(arbre)
        if isinstance(noeud, ast.FunctionDef) and noeud.name == APPEL_PRODUIT
    ]
    if not fonctions:
        return [
            f"{MOTIF_REFUS} : la fonction {APPEL_PRODUIT} est introuvable dans {SOURCE_CLI} ; attendu "
            f"le point d'entree de la ligne de commande, ou le refus hors-ligne est ecrit ({SOURCE_CLI})"
        ]

    refus: list[tuple[int, list[str]]] = []
    for noeud in ast.walk(fonctions[0]):
        if not isinstance(noeud, ast.If):
            continue
        test = noeud.test
        if not (isinstance(test, ast.Attribute) and test.attr == "offline"):
            continue
        sorties = [
            enfant
            for enfant in ast.walk(noeud)
            if isinstance(enfant, ast.Return)
            and isinstance(enfant.value, ast.Constant)
            and enfant.value.value == 1
        ]
        if not sorties:
            continue
        appels = sorted(
            {_nom_appele(enfant) for enfant in ast.walk(noeud) if isinstance(enfant, ast.Call)}
            & set(APPELS_SYNCHRO_PRODUIT)
        )
        refus.append((noeud.lineno, appels))

    if not refus:
        constats.append(
            f"{MOTIF_REFUS} : aucun bloc `if <args>.offline:` portant un `return 1` dans "
            f"{APPEL_PRODUIT} ; attendu le refus hors-ligne de la synchronisation, ecrit avant l'appel "
            f"reseau ({SOURCE_CLI}, D-78)"
        )
        return constats
    for ligne, appels in refus:
        if appels:
            constats.append(
                f"{MOTIF_REFUS} : le bloc de refus ligne {ligne} porte l'appel reseau "
                f"{', '.join(appels)} ; attendu un refus qui precede l'appel reseau, la synchronisation "
                f"etant inatteignable quand l'option est donnee ({SOURCE_CLI}, D-78)"
            )
    return constats


def _constats_effet_clear(arbre: ast.AST) -> list[str]:
    """Effet de la commande destructrice, lu par `ast` dans `Database.clear` sans jamais l'executer.

    Les deux litteraux de suppression disent ce que la commande detruit, et l'absence de tout appel dont
    le nom figure dans `APPELS_SUPPRESSION` dit ce qu'elle **ne** detruit pas : le fichier de la base
    reste sur le disque. La distinction est exactement celle que Pitfall 7 signale comme confusion
    possible entre les deux commandes destructrices.
    """
    constats: list[str] = []
    fonctions = [
        noeud
        for noeud in ast.walk(arbre)
        if isinstance(noeud, ast.FunctionDef) and noeud.name == "clear"
    ]
    if not fonctions:
        return [
            f"{MOTIF_EFFET} : la methode `clear` est introuvable dans {SOURCE_DATABASE} ; attendu le "
            f"vidage des deux tables, lu par ast et jamais execute (D-81)"
        ]

    methode = fonctions[0]
    litteraux = {
        noeud.value
        for noeud in ast.walk(methode)
        if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str)
    }
    for attendu in (SUPPRESSION_ITEMS, SUPPRESSION_META):
        if attendu not in litteraux:
            constats.append(
                f"{MOTIF_EFFET} : la methode `clear` de {SOURCE_DATABASE} ne porte plus "
                f"« {attendu} » ; attendu les deux instructions de suppression des tables `items` puis "
                f"`meta`, le fichier de la base etant vide et non supprime (D-81)"
            )
    suppressions = sorted(
        {
            _nom_appele(noeud)
            for noeud in ast.walk(methode)
            if isinstance(noeud, ast.Call)
        }
        & set(APPELS_SUPPRESSION)
    )
    if suppressions:
        constats.append(
            f"{MOTIF_EFFET} : la methode `clear` de {SOURCE_DATABASE} appelle "
            f"{', '.join(suppressions)} ; attendu aucun appel de suppression, le fichier de la base "
            f"n'etant jamais efface par cette commande (D-81)"
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


def test_defauts_hors_ligne(docs_dir: Path, section, normalize) -> None:
    """Les deux defauts hors-ligne sont enonces separement, chacun dans la section de sa surface.

    C'est le risque de confusion central de la phase (D-71) : l'interface web demarre hors-ligne, la
    ligne de commande demarre en ligne, et une phrase qui fusionnerait les deux serait fausse sur au
    moins une surface. Les defauts sont donc **mesures** sur les parseurs publics (D-14) — jamais lus
    dans l'introspection privee d'`argparse` — et chaque phrase d'aide est exigee du parseur **et** de la
    section de sa propre surface : c'est ce qui prouve que chaque defaut est enonce la ou il s'applique,
    et pas seulement quelque part dans la page.

    Limite honnete : ce controle porte sur les deux defauts et sur les deux phrases d'aide qui les
    disent. Il ne revendique aucune exhaustivite sur ce que les surfaces font une fois l'outil lance :
    ces cas appartiennent au plan suivant (D-85).
    """
    texte = _texte_page(docs_dir)
    corps_web = section(texte, TITRE_WEB, PAGE)
    corps_cli = section(texte, TITRE_CLI, PAGE)
    constats: list[str] = []

    # 1. Les defauts, mesures sur les parseurs publics et jamais supposes.
    defaut_web = parseur_web().parse_args([]).offline
    if defaut_web is not True:
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface web — `build_parser().parse_args([]).offline` vaut "
            f"{defaut_web!r} ; attendu True, l'interface web demarrant hors-ligne et `--offline` y "
            f"etant actif sans rien preciser ({SOURCE_WEB_MAIN})"
        )
    sans_offline = parseur_web().parse_args(["--no-offline"]).offline
    if sans_offline is not False:
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface web — `parse_args([\"--no-offline\"]).offline` vaut "
            f"{sans_offline!r} ; attendu False, `--no-offline` etant le geste qui autorise le contact "
            f"de l'API au demarrage ({SOURCE_WEB_MAIN})"
        )
    en_ligne = parseur_web().parse_args(["--online"])
    if en_ligne.offline is not True or en_ligne.online is not True:
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface web — `parse_args([\"--online\"])` rend "
            f"`offline={en_ligne.offline!r}` et `online={en_ligne.online!r}` ; attendu `offline=True` "
            f"et `online=True`, le contact API etant arbitre au lancement par `main` ({SOURCE_WEB_MAIN})"
        )
    defaut_cli = parseur_cli().parse_args(["db", "status"]).offline
    if defaut_cli is not False:
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface ligne de commande — "
            f"`build_parser().parse_args([\"db\", \"status\"]).offline` vaut {defaut_cli!r} ; attendu "
            f"False, la ligne de commande partant en ligne et `--offline` y etant requis ({SOURCE_CLI})"
        )

    # 2. Les deux phrases d'aide, lues sur le rendu des parseurs, puis exigees de leur propre section.
    aide_web = re.sub(r"\s+", " ", parseur_web().format_help())
    if normalize(AIDE_WEB_OFFLINE) not in normalize(aide_web):
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface web — l'aide rendue par `parseur_web().format_help()` ne "
            f"porte pas « {AIDE_WEB_OFFLINE} » ; attendu le texte d'aide reel de l'option, lu sur le "
            f"parseur et non recopie ({SOURCE_WEB_MAIN})"
        )
    if normalize(AIDE_WEB_OFFLINE) not in normalize(corps_web):
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface web — la section « {TITRE_WEB} » ne cite pas la phrase "
            f"« {AIDE_WEB_OFFLINE} » ; attendu le texte d'aide rendu par {SOURCE_WEB_MAIN}, cite dans "
            f"la section de sa propre surface (D-71, D-72)"
        )

    tampon = io.StringIO()
    try:
        with redirect_stdout(tampon):
            parseur_cli().parse_args(["--help"])
    except SystemExit:
        pass
    aide_cli = re.sub(r"\s+", " ", tampon.getvalue())
    if normalize(AIDE_CLI_OFFLINE) not in normalize(aide_cli):
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface ligne de commande — l'aide rendue par "
            f"`parse_args([\"--help\"])` ne porte pas « {AIDE_CLI_OFFLINE} » ; attendu le texte d'aide "
            f"reel de l'option, lu sur le parseur et non recopie ({SOURCE_CLI})"
        )
    if normalize(AIDE_CLI_OFFLINE) not in normalize(corps_cli):
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface ligne de commande — la section « {TITRE_CLI} » ne cite pas "
            f"la phrase « {AIDE_CLI_OFFLINE} » ; attendu le texte d'aide rendu par {SOURCE_CLI}, cite "
            f"dans la section de sa propre surface (D-71, D-72)"
        )

    # 3. Les jetons de drapeau sur leur forme exacte, et la marque de sens de chaque section.
    for jeton in ("--offline", "--no-offline", "--online"):
        if jeton not in corps_web:
            constats.append(
                f"{MOTIF_DEFAUTS} : la surface web — la section « {TITRE_WEB} » ne cite pas "
                f"« {jeton} » ; attendu les trois jetons du parseur de l'interface, dont le defaut "
                f"hors-ligne et le geste qui le desactive ({SOURCE_WEB_MAIN})"
            )
    if not any(normalize(marque) in normalize(corps_web) for marque in MARQUES_DEFAUT_WEB):
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface web — la section « {TITRE_WEB} » ne dit pas que le mode "
            f"hors-ligne y est le defaut (attendu au moins une de : {', '.join(MARQUES_DEFAUT_WEB)}) ; "
            f"attendu le sens du drapeau sur cette surface ({SOURCE_WEB_MAIN})"
        )
    if "--offline" not in corps_cli:
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface ligne de commande — la section « {TITRE_CLI} » ne cite pas "
            f"« --offline » ; attendu le drapeau de cette surface ({SOURCE_CLI})"
        )
    if not any(normalize(marque) in normalize(corps_cli) for marque in MARQUES_EXIGENCE_CLI):
        constats.append(
            f"{MOTIF_DEFAUTS} : la surface ligne de commande — la section « {TITRE_CLI} » ne dit pas "
            f"que « --offline » y est exige (attendu au moins une de : "
            f"{', '.join(MARQUES_EXIGENCE_CLI)}) ; attendu le sens du drapeau sur cette surface, "
            f"oppose a celui du web ({SOURCE_CLI})"
        )

    assert not constats, (
        f"{PAGE} : constats sur les deux defauts hors-ligne : "
        + " ; ".join(constats)
        + f" ; attendu les deux defauts enonces separement, chacun dans la section de sa surface, avec "
        f"la phrase d'aide que son propre parseur rend ({SOURCE_WEB_MAIN}, {SOURCE_CLI})"
    )


def _libelles_produits(lignes: list[str]) -> set[str]:
    """Libelles de champ portes par des lignes de sortie ou de rendu : la partie avant « : ».

    Les lignes de categorie (`  - equipment : 3`) sont ecartees : elles suivent un libelle de champ et
    n'en sont pas un. Une ligne sans « : » n'en porte pas non plus.
    """
    libelles: set[str] = set()
    for ligne in lignes:
        if ligne.startswith(PREFIXE_LIGNE_CATEGORIE) or ligne.strip().startswith("- "):
            continue
        if " :" not in ligne:
            continue
        libelles.add(ligne.split(" :", 1)[0].strip() + " :")
    return libelles


def _libelles_cites(corps: str) -> set[str]:
    """Libelles que la section cite dans un tableau, lus sur la page elle-meme."""
    return {trouve.group("libelle") for trouve in MOTIF_LIBELLE_CITE.finditer(corps)}


def _constats_bijection(
    lignes: list[str], corps: str, titre: str, motif: str, source: str, surface: str
) -> list[str]:
    """Constats de la bijection entre les libelles produits et ceux que la section cite.

    La comparaison est **exacte** dans les deux sens. La faire passer par `normalize` effacerait l'ecart
    entre `Entrées :` (ligne de commande) et `ENTREES :` (web), qui est precisement ce que la page doit
    rendre observable (Pitfall 4, D-75).
    """
    produits = _libelles_produits(lignes)
    cites = _libelles_cites(corps)
    constats: list[str] = []
    for libelle in sorted(produits - cites):
        constats.append(
            f"{motif} : {surface} — le libelle « {libelle} » produit par {source} n'est pas cite par la "
            f"section « {titre} » ; attendu chaque libelle produit, dans sa forme exacte, accent et "
            f"casse compris ({source}, D-75)"
        )
    for libelle in sorted(cites - produits):
        constats.append(
            f"{motif} : {surface} — la section « {titre} » cite « {libelle} », que {source} ne produit "
            f"pas ; attendu un libelle reellement produit par cette surface, jamais un libelle deduit "
            f"de l'autre surface ({source}, D-75)"
        )
    return constats


def _constats_conditionnels(
    vide: list[str], peuplee: list[str], titre: str, motif: str, source: str, surface: str
) -> list[str]:
    """Constats du champ conditionnel : la ligne par categorie ne survit pas a une base vide.

    La conditionnalite est mesuree sur les **deux** etats, pas seulement affirmee (Pitfall 3) : si le
    rendu d'une base vide porte les memes libelles que celui d'une base peuplee, le champ a cesse d'etre
    conditionnel sans que rien d'autre ne le signale.
    """
    libelles_vide = _libelles_produits(vide)
    conditionnels = _libelles_produits(peuplee) - libelles_vide
    if conditionnels:
        return []
    return [
        f"{MOTIF_CONDITION} : {surface} — {source} rend la meme liste de libelles sur une base vide et "
        f"sur une base peuplee ({', '.join(sorted(libelles_vide)) or 'aucun libelle'}) ; attendu au "
        f"moins un champ conditionnel, la ligne par categorie n'etant ecrite que si des objets existent "
        f"({source}, {titre}, {motif})"
    ]


def _sortie_db_status(db: Database) -> str:
    """Sortie capturee de `_print_db_status`, la base etant refermee dans tous les cas.

    `_print_db_status` interroge `stats()`, qui ouvre la connexion et la laisse ouverte : sans
    `close()`, le nettoyage du dossier temporaire echoue sur Windows (`PermissionError [WinError 32]`,
    mesure de la phase de recherche). La fermeture est donc dans un `finally`, pas apres la capture.
    """
    tampon = io.StringIO()
    try:
        with redirect_stdout(tampon):
            _print_db_status(db)
    finally:
        db.close()
    return tampon.getvalue()


def test_champs_de_la_ligne_de_commande(docs_dir: Path, section, app, tmp_path) -> None:
    """Les libelles de `db status` sont lus sur la sortie reelle de la commande, jamais supposes.

    Les valeurs de cette sortie (chemin du fichier, nombres, version) sont produites a l'execution : la
    page ne les recopie pas et ce controle ne les compare pas. Les libelles de champ, eux, sont les
    invariants de la sortie, et c'est leur bijection avec les lignes du tableau de la section qui est
    verifiee, dans les deux sens — page vers code et code vers page (D-75). L'etat vide est mesure lui
    aussi : c'est ce qui prouve que la page ne presente pas comme toujours ecrites les deux lignes qui
    changent de forme, ni la ligne par categorie (Pitfall 3).
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_CHAMPS_CLI, PAGE)
    constats: list[str] = []

    vide = _sortie_db_status(Database(data_dir=tmp_path / "vide")).splitlines()
    peuplee = _sortie_db_status(
        Database(data_dir=app.extensions["web_config"]["data_dir"])
    ).splitlines()

    constats += _constats_bijection(
        lignes=peuplee,
        corps=corps,
        titre=TITRE_CHAMPS_CLI,
        motif=MOTIF_CHAMPS_CLI,
        source=SOURCE_CLI,
        surface="la surface ligne de commande",
    )
    constats += _constats_conditionnels(
        vide=vide,
        peuplee=peuplee,
        titre=TITRE_CHAMPS_CLI,
        motif=MOTIF_CHAMPS_CLI,
        source=SOURCE_CLI,
        surface="la surface ligne de commande",
    )

    for etat in ("Version jeu : (aucune)", "Dernier check : (aucun)"):
        if etat not in corps:
            constats.append(
                f"{MOTIF_CHAMPS_CLI} : la surface ligne de commande — la section « {TITRE_CHAMPS_CLI} » "
                f"ne cite pas l'etat vide « {etat} » ; attendu la forme exacte que la commande ecrit "
                f"sur une base vide ({SOURCE_CLI}, D-77, Pitfall 3)"
            )

    assert not constats, (
        f"{PAGE} : constats sur les champs de la ligne de commande : "
        + " ; ".join(constats)
        + f" ; attendu chaque libelle reellement produit par `db status` cite dans la section "
        f"« {TITRE_CHAMPS_CLI} », dans sa forme exacte, etat vide compris ({SOURCE_CLI})"
    )


def test_champs_de_la_surface_web(
    docs_dir: Path, section, client, app, catalog, normalize, tmp_path
) -> None:
    """Les libelles de l'ecran d'etat sont lus sur le rendu, et compares exactement.

    `normalize` n'y sert qu'a **diagnostiquer** : si un libelle rendu manque a la page alors que sa
    forme normalisee s'y trouve, c'est que la page a lisse l'ecart de casse ou d'accent entre les deux
    surfaces — exactement ce que ce controle interdit, `Entrées :` (ligne de commande) et `ENTREES :`
    (web) etant deux chaines distinctes du code (Pitfall 4, D-75). Le rendu est lu sur les lignes du
    corps, jamais sur la reponse entiere (D-11).
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_CHAMPS_WEB, PAGE)
    constats: list[str] = []

    reponse = client.get("/db/status")
    if reponse.status_code != 200:
        constats.append(
            f"{MOTIF_CHAMPS_WEB} : la surface web — `GET /db/status` rend le statut "
            f"{reponse.status_code} ; attendu 200, l'ecran d'etat de la base etant ce que cette section "
            f"decrit ({SOURCE_ROUTES})"
        )
    rendu = _lignes_du_corps(reponse) if reponse.status_code == 200 else []

    vide_app = create_app(
        data_dir=tmp_path / "web_vide",
        offline=True,
        catalog=catalog,
        load_catalog=False,
    )
    vide_app.config["TESTING"] = True
    reponse_vide = vide_app.test_client().get("/db/status")
    if reponse_vide.status_code != 200:
        constats.append(
            f"{MOTIF_CHAMPS_WEB} : la surface web — `GET /db/status` sur un dossier de donnees "
            f"inexistant rend le statut {reponse_vide.status_code} ; attendu 200, une base vide etant un "
            f"etat normal de cette surface ({SOURCE_ROUTES})"
        )
    rendu_vide = _lignes_du_corps(reponse_vide) if reponse_vide.status_code == 200 else []
    dossier_vide = tmp_path / "web_vide"
    crees = sorted(chemin.name for chemin in dossier_vide.glob("*")) if dossier_vide.exists() else []
    if not crees:
        constats.append(
            f"{MOTIF_CHAMPS_WEB} : la surface web — l'ecran d'etat sur un dossier de donnees inexistant "
            f"n'a rien cree dans ce dossier ; attendu la base ouverte et refermee a la volee, la page "
            f"decrit un etat vide et non un ecran d'erreur ({SOURCE_ROUTES})"
        )

    constats += _constats_bijection(
        lignes=rendu,
        corps=corps,
        titre=TITRE_CHAMPS_WEB,
        motif=MOTIF_CHAMPS_WEB,
        source=SOURCE_ROUTES,
        surface="la surface web",
    )
    constats += _constats_conditionnels(
        vide=rendu_vide,
        peuplee=rendu,
        titre=TITRE_CHAMPS_WEB,
        motif=MOTIF_CHAMPS_WEB,
        source=SOURCE_ROUTES,
        surface="la surface web",
    )

    # Diagnostic : un libelle rendu qui n'apparait dans la page que sous une forme normalisee signale
    # un ecart de casse, d'accent ou d'entite lisse par la page. La comparaison des libelles, elle,
    # reste exacte.
    for libelle in sorted(_libelles_produits(rendu) - _libelles_cites(corps)):
        if normalize(libelle) in normalize(corps):
            constats.append(
                f"{MOTIF_CHAMPS_WEB} : la surface web — le libelle rendu « {libelle} » n'est cite par la "
                f"section « {TITRE_CHAMPS_WEB} » que sous une forme que seule la normalisation "
                f"rapproche (casse, accents ou entites HTML) ; attendu la forme exacte du rendu, l'ecart "
                f"entre les deux surfaces etant un fait observable ({SOURCE_ROUTES}, D-75)"
            )

    for etat in ("VERSION JEU : (aucune)", "DERNIER CHECK : (AUCUN)"):
        if etat not in corps:
            constats.append(
                f"{MOTIF_CHAMPS_WEB} : la surface web — la section « {TITRE_CHAMPS_WEB} » ne cite pas "
                f"l'etat vide « {etat} » ; attendu la forme exacte que l'ecran rend sur une base vide "
                f"({SOURCE_ROUTES}, D-77, Pitfall 3)"
            )

    assert not constats, (
        f"{PAGE} : constats sur les champs de la surface web : "
        + " ; ".join(constats)
        + f" ; attendu chaque libelle reellement rendu par « /db/status » cite dans la section "
        f"« {TITRE_CHAMPS_WEB} », dans sa forme exacte — majuscules et absence d'accents comprises "
        f"({SOURCE_ROUTES})"
    )


def test_le_premier_contact_cree_la_base(
    docs_dir: Path, section, app, client, catalog, normalize, tmp_path
) -> None:
    """Le premier contact cree le dossier puis le fichier, sur les deux surfaces, hors de `.data/`.

    Tranche verticale du plan 05-02 : la page, la sortie capturee de la ligne de commande, le rendu de
    l'ecran web et les chemins d'ecran cites sont traverses par ce seul controle. `_print_db_status` est
    mesure sur un `Database(data_dir=dossier)` jamais ouvert, et l'ecran sur une application dont
    `data_dir` pointe un dossier absent : les deux dossiers viennent de `tmp_path`, jamais `.data/`
    (D-81).

    Les deux oracles sont **proteges**, et c'est le point du controle : quand la creation du dossier
    disparait du code, `sqlite3.connect` echoue cote ligne de commande (`OperationalError: unable to
    open database file`) et l'erreur remonte sous `TESTING = True` cote web. L'appel est donc enferme
    dans un `try` et l'exception devient un **constat** portant `MOTIF_CREATION` ; sans cette
    protection, la morsure `creation_retiree` rapporterait une erreur de collection au lieu du constat
    attendu, et le controle serait juge non discriminant sur un module correct. La base ouverte cote
    ligne de commande est refermee par `_sortie_db_status` (`db.close()` en `finally`), sans quoi le
    nettoyage du dossier temporaire echoue sur Windows (`PermissionError [WinError 32]`).

    Limite honnete : ce controle porte sur la creation du dossier et du fichier, sur les trois libelles
    de l'etat vide et sur le libelle `FICHIER :` du rendu. Il ne revendique rien sur la prose de la
    section, ni sur les valeurs produites a l'execution (D-85).
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_CREATION, PAGE)
    constats: list[str] = []

    # 1. Surface ligne de commande : dossier absent, puis dossier ET fichier crees.
    dossier = tmp_path / "absent_cli"
    if dossier.exists():
        constats.append(
            f"{MOTIF_CREATION} : la surface ligne de commande — le dossier de travail « "
            f"{dossier.name} » existe deja avant l'appel ; attendu un dossier absent sous `tmp_path`, "
            f"la creation etant ce que ce controle mesure ({SOURCE_DATABASE})"
        )
    db = Database(data_dir=dossier)
    try:
        sortie = _sortie_db_status(db)
    except Exception as exc:
        constats.append(
            f"{MOTIF_CREATION} : la surface ligne de commande — `_print_db_status` a leve "
            f"{type(exc).__name__} : {exc} ; attendu la creation du dossier puis du fichier par "
            f"`Database.open`, sans exception ({SOURCE_DATABASE})"
        )
    else:
        for chemin, libelle in ((dossier, "le dossier"), (dossier / DB_NAME, "le fichier")):
            if not chemin.exists():
                constats.append(
                    f"{MOTIF_CREATION} : la surface ligne de commande — {libelle} « {chemin.name} » "
                    f"n'existe pas apres l'appel ; attendu le dossier puis le fichier `{DB_NAME}` "
                    f"crees au premier contact ({SOURCE_DATABASE})"
                )
        for attendu in ("Version jeu : (aucune)", "Dernier check : (aucun)", "Entrées : 0"):
            if attendu not in sortie:
                constats.append(
                    f"{MOTIF_CREATION} : la surface ligne de commande — la sortie de "
                    f"`_print_db_status` ne porte pas « {attendu} » ; attendu l'etat d'une base "
                    f"fraichement creee, jamais un ecran d'erreur ({SOURCE_CLI})"
                )

    # 2. Surface web : dossier absent, puis dossier ET fichier crees, et l'ecran rendu.
    dossier_web = tmp_path / "absent_web"
    if dossier_web.exists():
        constats.append(
            f"{MOTIF_CREATION} : la surface web — le dossier de donnees « {dossier_web.name} » existe "
            f"deja avant l'appel ; attendu un dossier absent sous `tmp_path` ({SOURCE_DATABASE})"
        )
    application = create_app(
        data_dir=dossier_web,
        offline=True,
        catalog=catalog,
        load_catalog=False,
    )
    application.config["TESTING"] = True
    try:
        reponse = application.test_client().get("/db/status")
    except Exception as exc:
        constats.append(
            f"{MOTIF_CREATION} : la surface web — `GET /db/status` a leve {type(exc).__name__} : "
            f"{exc} ; attendu la creation du dossier puis du fichier par la route, et une reponse "
            f"rendue ({SOURCE_ROUTES})"
        )
    else:
        if reponse.status_code != 200:
            constats.append(
                f"{MOTIF_CREATION} : la surface web — `GET /db/status` rend le statut "
                f"{reponse.status_code} sur un dossier de donnees absent ; attendu 200, la creation "
                f"du fichier etant le comportement decrit ({SOURCE_ROUTES})"
            )
        elif LIBELLE_FICHIER_RENDU not in _libelles_produits(_lignes_du_corps(reponse)):
            constats.append(
                f"{MOTIF_CREATION} : la surface web — le corps rendu par `GET /db/status` ne porte pas "
                f"le libelle « {LIBELLE_FICHIER_RENDU} » ; attendu l'ecran d'etat rendu, la base "
                f"venant d'etre creee ({SOURCE_ROUTES})"
            )
        if not (dossier_web / DB_NAME).exists():
            constats.append(
                f"{MOTIF_CREATION} : la surface web — le fichier « {DB_NAME} » n'existe pas dans "
                f"« {dossier_web.name} » apres l'appel ; attendu la base creee puis refermee par la "
                f"route ({SOURCE_DATABASE})"
            )

    # Temoin : l'ecran d'etat de la base peuplee de la fixture rend le meme libelle de fichier. Le
    # libelle exige de l'ecran vide n'est donc pas un libelle fantome, et la section decrit bien le
    # libelle que les deux etats portent.
    reponse_peuplee = client.get("/db/status")
    if reponse_peuplee.status_code != 200 or LIBELLE_FICHIER_RENDU not in _libelles_produits(
        _lignes_du_corps(reponse_peuplee)
    ):
        constats.append(
            f"{MOTIF_CREATION} : la surface web — l'ecran d'etat de la base peuplee (fixture `app`, "
            f"dossier « {app.extensions['web_config']['data_dir'].name} ») rend le statut "
            f"{reponse_peuplee.status_code} ; attendu 200 et le libelle « {LIBELLE_FICHIER_RENDU} », "
            f"le libelle exige de l'ecran vide etant celui du rendu reel ({SOURCE_ROUTES})"
        )

    # 3. La section dit l'effet de creation et nomme les deux surfaces.
    for jeton, attendu in (
        ("db status", "la commande hors-ligne de la ligne de commande"),
        ("/db/status", "le chemin de l'ecran d'etat du web"),
        ("--offline", "l'option globale qui rend la commande hors-ligne"),
    ):
        if jeton not in corps:
            constats.append(
                f"{MOTIF_CREATION} : la section « {TITRE_CREATION} » ne cite pas « {jeton} » "
                f"({attendu}) ; attendu les deux surfaces nommees dans la section ({SOURCE_CLI}, "
                f"{SOURCE_ROUTES})"
            )
    if not any(normalize(marque) in normalize(corps) for marque in MARQUES_CREATION):
        constats.append(
            f"{MOTIF_CREATION} : la section « {TITRE_CREATION} » ne dit pas que le premier contact "
            f"**cree** la base (attendu au moins une de : {', '.join(MARQUES_CREATION)}) ; attendu "
            f"l'effet decrit, pas seulement la lecture de l'etat ({SOURCE_DATABASE})"
        )

    # 4. Chaque chemin d'ecran cite par la page est declare par un decorateur de routes.py.
    declarees = _routes_declarees()
    for trouve in sorted({trouve.group("chemin") for trouve in CHEMIN_ECRAN.finditer(texte)}):
        if trouve not in declarees:
            constats.append(
                f"{MOTIF_ROUTE} : la page cite « {trouve} », absent des chemins declares par les "
                f"decorateurs de {SOURCE_ROUTES} ({', '.join(sorted(declarees))}) ; attendu un chemin "
                f"d'ecran reellement declare, jamais un chemin deduit (D-76)"
            )

    assert not constats, (
        f"{PAGE} : constats sur la creation de la base par le premier contact : "
        + " ; ".join(constats)
        + f" ; attendu le dossier puis le fichier crees par le premier contact, mesures sous "
        f"`tmp_path` sur la ligne de commande et sur l'ecran web, et cites par la section "
        f"« {TITRE_CREATION} » ({SOURCE_DATABASE}, {SOURCE_CLI}, {SOURCE_ROUTES})"
    )


def test_le_refus_de_la_synchronisation(docs_dir: Path, section, normalize) -> None:
    """Le refus de `db sync` en mode hors-ligne est lu dans le code, jamais execute (D-78, D-15).

    Trois ancrages, du plus faible au plus fort : le **litteral** du message de refus, lu par `ast` dans
    `dofus_stuff/cli.py` (faible : il dit ce que le code ecrit) ; la **structure** du refus — un bloc
    `if args.offline:` portant un `return 1`, dont **aucun** appel de synchronisation ne descend, donc un
    refus qui precede l'appel reseau ; et la **sonde publique** du parseur, `parse_args(["--offline",
    "db", "sync"])`, qui prouve que la forme refusee est bien celle que le parseur analyse. `main()`
    n'est jamais execute : la synchronisation n'est jamais lancee, et aucune socket n'est ouverte.

    Limite honnete : le rendu du refus (sa sortie reelle sur `stderr` et son code de retour observe) n'est
    pas mesure ici — cela demanderait d'executer `main()`. Ce controle lit le litteral, la structure et
    l'analyse des arguments, et il ne revendique rien de plus (D-85).
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_REFUS, PAGE)
    constats: list[str] = []

    # 1. Le message de refus, produit par le code (lecture par `ast`, `main()` jamais execute).
    arbre = ast.parse((RACINE_DEPOT / SOURCE_CLI).read_text(encoding="utf-8"))
    if MESSAGE_REFUS not in _litteraux_du_module(arbre):
        constats.append(
            f"{MOTIF_REFUS} : le message « {MESSAGE_REFUS} » n'est plus produit par {SOURCE_CLI} ; "
            f"attendu le message reel du refus, lu par ast et jamais recopie de memoire (D-78)"
        )

    # 2. Le refus precede l'appel reseau, et il sort en 1.
    constats += _constats_bloc_refus(arbre)

    # 3. La forme refusee est analysee par le parseur public — la commande est analysee, jamais executee.
    analyse = parseur_cli().parse_args(["--offline", "db", "sync"])
    if analyse.offline is not True or analyse.db_command != "sync":
        constats.append(
            f"{MOTIF_REFUS} : la surface ligne de commande — "
            f"`parse_args([\"--offline\", \"db\", \"sync\"])` rend offline={analyse.offline!r} et "
            f"db_command={analyse.db_command!r} ; attendu offline=True et db_command='sync', la forme "
            f"refusee etant celle que le parseur public analyse ({SOURCE_CLI})"
        )

    # 4. La page cite le message verbatim et dit que la commande s'arrete.
    if MESSAGE_REFUS not in corps:
        constats.append(
            f"{MOTIF_REFUS} : la section « {TITRE_REFUS} » ne cite pas le message « {MESSAGE_REFUS} » ; "
            f"attendu le message reel du code, cite verbatim et jamais paraphrase ({SOURCE_CLI}, D-78)"
        )
    if not any(normalize(marque) in normalize(corps) for marque in MARQUES_CODE_RETOUR):
        constats.append(
            f"{MOTIF_REFUS} : la section « {TITRE_REFUS} » ne dit pas que la commande sort avec un code "
            f"de retour non nul (attendu au moins une de : {', '.join(MARQUES_CODE_RETOUR)}) ; attendu "
            f"l'arret de la commande, pas seulement l'affichage d'un message ({SOURCE_CLI})"
        )

    assert not constats, (
        f"{PAGE} : constats sur le refus de la synchronisation hors-ligne : "
        + " ; ".join(constats)
        + f" ; attendu le message reel de {SOURCE_CLI} cite verbatim par la section "
        f"« {TITRE_REFUS} », un bloc de refus qui precede l'appel reseau, et la forme "
        f"`--offline db sync` analysee par le parseur public, `main()` n'etant jamais execute"
    )


def test_la_synchronisation_web_contacte_l_api(docs_dir: Path, section, client, normalize) -> None:
    """L'ecran web de synchronisation contacte l'API, meme hors-ligne — lu sans jamais poster (D-79).

    Le fait est adosse a trois sources : le litteral `offline=False` de l'appel de synchronisation, lu
    par `ast` dans `dofus_stuff/web/routes.py` — c'est lui qui prouve que l'ecran ne suit pas le mode
    hors-ligne de l'interface ; la phrase d'annonce du corps de confirmation, retrouvee dans le **corps
    rendu** de `GET /db/sync`, comparee apres `normalize` (l'apostrophe sort en `&#39;` dans le HTML) ;
    et la citation de cette phrase par la section.

    L'ecran se lit en **`GET` seulement** : poster une confirmation sur `/db/sync` declenche
    `ensure_up_to_date(force=True, offline=False, ...)` — reseau **et** ecriture —, et poster sur
    `/db/clear` vide la base. Ce module ne poste jamais ; le controle le verifie sur son propre texte par
    `ast`, et la garde de cloture du module refuse deja toute paire de confirmation (`D-81`, Pitfall 6).

    Limite honnete : ce controle lit un appel et un rendu de confirmation. Il ne declenche aucune
    synchronisation et ne mesure donc pas le contact reseau lui-meme (D-85).
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_SYNCHRO_WEB, PAGE)
    constats: list[str] = []

    # 1. L'appel de synchronisation de l'ecran porte `offline=False` en dur.
    arbre = ast.parse((RACINE_DEPOT / SOURCE_ROUTES).read_text(encoding="utf-8"))
    appels = [
        noeud
        for noeud in ast.walk(arbre)
        if isinstance(noeud, ast.Call) and _nom_appele(noeud).endswith("ensure_up_to_date")
    ]
    if not appels:
        constats.append(
            f"{MOTIF_SYNCHRO_WEB} : aucun appel a `ensure_up_to_date` dans {SOURCE_ROUTES} ; attendu "
            f"l'appel de synchronisation de l'ecran, dont le mode hors-ligne ne s'applique pas (D-79)"
        )
    for noeud in appels:
        valeur: ast.expr | None = None
        for mot in noeud.keywords:
            if mot.arg == "offline":
                valeur = mot.value
        if isinstance(valeur, ast.Constant) and valeur.value is False:
            continue
        constats.append(
            f"{MOTIF_SYNCHRO_WEB} : l'appel `ensure_up_to_date` ligne {noeud.lineno} de {SOURCE_ROUTES} "
            f"ne porte pas `offline=False` "
            f"({ast.unparse(valeur) if valeur is not None else 'argument nomme offline absent'}) ; "
            f"attendu le litteral False, l'ecran de synchronisation contactant l'API quel que soit le "
            f"mode hors-ligne de l'interface (D-79)"
        )

    # 2. La phrase d'annonce et l'invite de confirmation : lues dans l'ecran, retrouvees dans le rendu.
    litteraux_ecran = _litteraux_de_fonction(arbre, "db_sync_confirm")
    reponse = client.get("/db/sync")
    if reponse.status_code != 200:
        constats.append(
            f"{MOTIF_SYNCHRO_WEB} : `GET /db/sync` rend le statut {reponse.status_code} ; attendu 200, "
            f"l'ecran de confirmation etant ce que cette section decrit ({SOURCE_ROUTES})"
        )
        rendu: list[str] = []
    else:
        rendu = [normalize(ligne) for ligne in _lignes_du_corps(reponse)]
    for phrase, nature in (
        (PHRASE_SYNCHRO, "la phrase d'annonce du corps de confirmation"),
        (INVITE_CONFIRMATION, "l'invite de confirmation"),
    ):
        if phrase not in litteraux_ecran:
            constats.append(
                f"{MOTIF_SYNCHRO_WEB} : {nature} « {phrase} » n'est plus portee par l'ecran de "
                f"synchronisation de {SOURCE_ROUTES} ; attendu le litteral que l'ecran rend (D-79)"
            )
        if not any(normalize(phrase) in ligne for ligne in rendu):
            constats.append(
                f"{MOTIF_SYNCHRO_WEB} : {nature} « {phrase} » n'apparait pas dans le corps rendu par "
                f"`GET /db/sync` ; attendu le rendu de l'ecran de confirmation, lu sur les lignes du "
                f"corps et compare apres normalisation ({SOURCE_ROUTES}, D-11)"
            )

    # 3. La page cite la phrase de l'ecran et dit explicitement le cas hors-ligne.
    if normalize(PHRASE_SYNCHRO) not in normalize(corps):
        constats.append(
            f"{MOTIF_SYNCHRO_WEB} : la section « {TITRE_SYNCHRO_WEB} » ne cite pas la phrase "
            f"« {PHRASE_SYNCHRO} » ; attendu la phrase du corps de confirmation telle que l'ecran la "
            f"rend ({SOURCE_ROUTES}, D-79)"
        )
    if not any(normalize(marque) in normalize(corps) for marque in MARQUES_HORS_LIGNE):
        constats.append(
            f"{MOTIF_SYNCHRO_WEB} : la section « {TITRE_SYNCHRO_WEB} » ne dit pas le cas hors-ligne "
            f"(attendu au moins une de : {', '.join(MARQUES_HORS_LIGNE)}) ; attendu le fait que le mode "
            f"hors-ligne de l'interface ne s'applique pas a cet ecran ({SOURCE_ROUTES}, D-79)"
        )

    # 4. Ce module ne poste jamais : l'ecran se lit en GET seulement.
    arbre_module = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for noeud in ast.walk(arbre_module):
        if isinstance(noeud, ast.Call) and _nom_appele(noeud) == "post":
            constats.append(
                f"{MOTIF_SYNCHRO_WEB} : le module d'ancrage appelle `post` ligne {noeud.lineno} ; attendu "
                f"des lectures en GET seulement, poster une confirmation sur /db/sync declenchant "
                f"`ensure_up_to_date(offline=False)` — reseau et ecriture ({SOURCE_ROUTES}, D-81)"
            )

    assert not constats, (
        f"{PAGE} : constats sur l'ecran de synchronisation du web : "
        + " ; ".join(constats)
        + f" ; attendu `offline=False` dans l'appel de {SOURCE_ROUTES}, la phrase d'annonce retrouvee "
        f"dans le rendu de `GET /db/sync` et citee par la section « {TITRE_SYNCHRO_WEB} », le cas "
        f"hors-ligne dit explicitement, et aucun POST emis par ce module"
    )


def test_commandes_destructrices(
    docs_dir: Path, section, client, normalize, lignes_exemple
) -> None:
    """Les deux commandes destructrices sont signalees sur leur ligne et hors de tout parcours.

    Perimetre declare : le controle porte sur la page de ce depot et sur ce module, et il est ecrit noir
    sur blanc dans la constante `LIMITE_PERIMETRE`, que cette docstring cite. L'occurrence de `README.md`
    ligne 80, seule du depot ou une commande destructrice figure dans un bloc de commandes sans
    avertissement, appartient a la phase 6 (D-87) et aucun constat d'ici ne la mentionne (Pitfall 8,
    A3).

    Trois lectures, aucune execution. La reconnaissance est faite **ligne a ligne** sur le texte entier
    de la page (D-80) : chaque ligne qui porte une commande doit avertir sur elle-meme, meme si une autre
    ligne de la page porte deja l'avertissement. Les cibles sont distinguees (Pitfall 7) : la premiere
    commande vide la base SQLite, la seconde supprime les sauvegardes du navigateur. Et l'effet de
    chacune est **lu** — les deux instructions de suppression de `Database.clear` par `ast`, le libelle
    de la seconde commande sur la ligne de statut rendue par `GET /saves`, et son traitement dans
    `dofus_stuff/web/static/js/terminal.js` — jamais execute.

    Limite honnete : l'execution JavaScript de la seconde commande n'est pas observable en processus.
    Aucun navigateur n'est lance et aucun JavaScript n'est compile : ce qui est verifie est le libelle
    rendu et le texte du fichier qui le traite, pas le retrait effectif de la cle (A2 de la recherche,
    D-85).
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_DESTRUCTRICES, PAGE)
    lignes = texte.splitlines()
    constats: list[str] = []

    # 1. Reconnaissance ligne a ligne (D-80) : chaque ligne porteuse porte son propre avertissement.
    porteuses = {
        "db clear": [
            numero
            for numero, ligne in enumerate(lignes, start=1)
            if COMMANDE_DESTRUCTRICE.search(ligne)
        ],
        JETON_PURGE: [
            numero for numero, ligne in enumerate(lignes, start=1) if JETON_PURGE in ligne
        ],
    }
    for jeton, numeros in porteuses.items():
        if not numeros:
            constats.append(
                f"{MOTIF_DESTRUCTRICES} : la page ne porte pas la commande « {jeton} » ; attendu la "
                f"commande signalee comme destructrice, chaque ligne porteuse avertissant sur elle-meme "
                f"({PAGE}, D-80)"
            )
            continue
        for numero in numeros:
            ligne = lignes[numero - 1]
            if not any(
                normalize(marque) in normalize(ligne) for marque in MARQUES_DESTRUCTRICES
            ):
                constats.append(
                    f"{MOTIF_DESTRUCTRICES} : la ligne {numero} de {PAGE} porte « {jeton} » sans "
                    f"avertissement : « {ligne.strip()} » ; attendu une marque de caractere destructeur "
                    f"sur la meme ligne que la commande (au moins une de : "
                    f"{', '.join(MARQUES_DESTRUCTRICES)}) (D-80)"
                )

    # 2. Cibles distinctes (Pitfall 7) : chaque ligne porteuse nomme ce que sa commande detruit.
    for jeton, marques, cible, source in (
        ("db clear", MARQUES_BASE, "la base locale", SOURCE_DATABASE),
        (JETON_PURGE, MARQUES_SAUVEGARDES, "les sauvegardes du navigateur", SOURCE_TERMINAL_JS),
    ):
        for numero in porteuses[jeton]:
            ligne = lignes[numero - 1]
            if not any(normalize(marque) in normalize(ligne) for marque in marques):
                constats.append(
                    f"{MOTIF_DESTRUCTRICES} : la ligne {numero} de {PAGE} porte « {jeton} » sans "
                    f"nommer {cible} (attendu au moins une de : {', '.join(marques)}) ; attendu la cible "
                    f"que cette commande detruit reellement ({source}, Pitfall 7)"
                )

    # 3. Hors de tout parcours, et hors de tout exemple recopiable (D-80).
    if not any(normalize(marque) in normalize(corps) for marque in MARQUES_HORS_PARCOURS):
        constats.append(
            f"{MOTIF_DESTRUCTRICES} : la section « {TITRE_DESTRUCTRICES} » ne dit pas que ces commandes "
            f"ne sont l'etape d'aucun parcours (attendu au moins une de : "
            f"{', '.join(MARQUES_HORS_PARCOURS)}) ; attendu la mise hors parcours des deux commandes "
            f"({PAGE}, D-80)"
        )
    if BALISE_COMMANDE in texte:
        constats.append(
            f"{MOTIF_EXEMPLE} : la page porte un bloc de commandes « {BALISE_COMMANDE} » ; attendu "
            f"aucun bloc de ce genre, une commande destructrice ne devant jamais figurer dans un exemple "
            f"recopiable ({PAGE}, D-80)"
        )
    for ligne in lignes_exemple(texte):
        for jeton in ("db clear", JETON_PURGE):
            porte = (
                COMMANDE_DESTRUCTRICE.search(ligne) is not None
                if jeton == "db clear"
                else JETON_PURGE in ligne
            )
            if porte:
                constats.append(
                    f"{MOTIF_EXEMPLE} : une ligne d'exemple de {PAGE} porte « {jeton} » "
                    f"(« {ligne} ») ; attendu aucune commande destructrice dans un bloc d'exemple, "
                    f"meme marque ({PAGE}, D-80)"
                )

    # 4. Effet de la premiere commande, lu par `ast` et jamais execute (D-81).
    arbre_base = ast.parse((RACINE_DEPOT / SOURCE_DATABASE).read_text(encoding="utf-8"))
    constats += _constats_effet_clear(arbre_base)
    for attendu in (SUPPRESSION_ITEMS, SUPPRESSION_META):
        if attendu not in corps:
            constats.append(
                f"{MOTIF_EFFET} : la section « {TITRE_DESTRUCTRICES} » ne cite pas « {attendu} » ; "
                f"attendu l'effet reel de la commande, tel que le code l'ecrit ({SOURCE_DATABASE}, "
                f"D-80)"
            )
    if not any(normalize(marque) in normalize(corps) for marque in MARQUES_FICHIER_CONSERVE):
        constats.append(
            f"{MOTIF_EFFET} : la section « {TITRE_DESTRUCTRICES} » ne dit pas que le fichier n'est pas "
            f"supprime (attendu au moins une de : {', '.join(MARQUES_FICHIER_CONSERVE)}) ; attendu "
            f"l'effet exact de `clear`, qui vide les tables sans effacer le fichier de la base "
            f"({SOURCE_DATABASE}, D-81)"
        )

    # 5. Effet de la seconde commande : le libelle au rendu, et son traitement dans le fichier JS.
    reponse = client.get("/saves")
    if reponse.status_code != 200:
        constats.append(
            f"{MOTIF_EFFET} : `GET /saves` rend le statut {reponse.status_code} ; attendu 200, l'ecran "
            f"des sauvegardes etant celui qui porte le libelle de la seconde commande ({SOURCE_ROUTES})"
        )
    elif normalize(JETON_PURGE) not in normalize(_statut(reponse)):
        constats.append(
            f"{MOTIF_EFFET} : la ligne de statut rendue par `GET /saves` ne porte pas « {JETON_PURGE} » "
            f"(« {_statut(reponse).strip()} ») ; attendu le libelle de la seconde commande au rendu de "
            f"l'ecran des sauvegardes ({SOURCE_ROUTES})"
        )
    script = (RACINE_DEPOT / SOURCE_TERMINAL_JS).read_text(encoding="utf-8")
    if COMPARAISON_PURGE.search(script) is None:
        constats.append(
            f"{MOTIF_EFFET} : le fichier {SOURCE_TERMINAL_JS} ne compare plus le libelle "
            f"« {JETON_PURGE} » ; attendu le traitement de la commande, lu dans le fichier et jamais "
            f"execute (D-85)"
        )
    if RETRAIT_SAUVEGARDES.search(script) is None:
        constats.append(
            f"{MOTIF_EFFET} : le fichier {SOURCE_TERMINAL_JS} ne retire plus la cle des sauvegardes du "
            f"navigateur (`localStorage.removeItem(SAVES_KEY)`) ; attendu l'effet reel de la commande, "
            f"lu dans la source et jamais execute (D-85)"
        )

    # 6. Le perimetre est declare, et ce controle ne rougit pas pour un fichier hors mandat (D-87).
    if "LIMITE_PERIMETRE" not in (test_commandes_destructrices.__doc__ or ""):
        constats.append(
            f"{MOTIF_DESTRUCTRICES} : la docstring de ce test ne cite pas la constante "
            f"`LIMITE_PERIMETRE` de ce module ; attendu le perimetre declare, ce controle portant sur "
            f"{PAGE} et sur ce module ({PAGE}, D-87)"
        )

    assert not constats, (
        f"{PAGE} : constats sur les commandes destructrices : "
        + " ; ".join(constats)
        + f" ; attendu chacune des deux commandes signalee sur sa propre ligne, avec la cible qu'elle "
        f"detruit, hors de tout parcours et de tout bloc d'exemple, et son effet lu dans "
        f"{SOURCE_DATABASE}, {SOURCE_ROUTES} et {SOURCE_TERMINAL_JS} sans jamais etre execute"
    )


# ------------------------------------------------------------------------------------------------
# Cloture de la phase (plan 05-03). Ces controles n'ajoutent aucun fait a la page : ils la ferment —
# chaque renvoi interne du `README.md` resout (D-87), la dette D-44 est denouee par un renvoi
# legitime (D-63), les octets et les valeurs de la page sont conformes (D-67, D-69, D-73) — et ils
# mesurent que rien de tout cela n'ecrit sous `.data/` (D-81, D-89).
# ------------------------------------------------------------------------------------------------


def _cibles_de_liens(texte: str) -> list[tuple[str, str]]:
    """Couples `(libelle, cible)` des liens Markdown d'un texte, dans l'ordre du document.

    Lecture du seul motif du depot (`MOTIF_LIEN_MARKDOWN`, repris de `tests/test_docs_wizard.py`) : la
    cible est celle qui est ecrite entre parentheses, jamais une cible reecrite.
    """
    return [
        (trouve.group("libelle"), trouve.group("cible"))
        for trouve in MOTIF_LIEN_MARKDOWN.finditer(texte)
    ]


def _cible_interne(cible: str) -> bool:
    """Vrai quand la cible est un renvoi de fichier interne, candidat a la resolution (D-87).

    Ecartees : les cibles externes (`CIBLES_EXTERNES`) et les formes que la garde de structure de
    `docs/` interdit deja — ancre, chemin absolu, antislash, schema `file://`. Ces formes ne sont pas
    signalees ici : les signaler dupliquerait un controle que `tests/test_docs_structure.py` possede
    (D-12), et ce module ne revendique que la resolution des renvois de fichier.
    """
    if cible.startswith(CIBLES_EXTERNES):
        return False
    if "#" in cible or cible.startswith("/") or "\\" in cible or cible.startswith("file://"):
        return False
    return True


def _corps_du_titre(texte: str, titre: str) -> str:
    """Texte ouvert par un titre, jusqu'au prochain titre de niveau 2 ; vide si le titre est absent.

    Le titre de la section des renvois de `docs/parcours-simplifie.md` est de **niveau 3** : le helper
    `section` de `tests/conftest.py` ne rend que des sections de niveau 2 et ne peut donc pas l'isoler.
    Ce lecteur local reste un motif du module, jamais un doublon du helper partage (D-12).
    """
    debut = texte.find(titre)
    if debut < 0:
        return ""
    suite = texte[debut + len(titre) :]
    suivant = re.search(r"^##\s", suite, re.MULTILINE)
    return suite[: suivant.start()] if suivant is not None else suite


def renvois_morts(texte: str, racine: Path, fichier: str = "") -> list[str]:
    """Renvois internes d'un texte dont la cible n'existe pas sous `racine`, un constat par cible.

    Fonction **pure** : elle ne lit aucun fichier, n'ouvre aucune connexion et n'ecrit rien. La seule
    operation sur le systeme de fichiers est le test d'existence d'une cible interne sous `racine` ; la
    mutation qui prouve sa morsure vit donc sur une **chaine**, jamais sur un fichier du depot (D-84).

    Le motif du resolveur est **local** a ce module, et non importe de `tests/test_docs_structure.py` :
    ce dernier resout les cibles **depuis `docs/`** (`problemes_liens` part de `page.parent`), alors que
    le mandat de D-87 est de resoudre les renvois du `README.md` **depuis la racine du depot**. La
    duplication porte sur ce motif, jamais sur un helper de `tests/conftest.py` (D-12 ne porte que sur
    ceux-la).

    Limite honnete : seules les cibles de liens Markdown sont vues. Un chemin cite en prose, ou un renvoi
    ecrit sous une autre forme, ne l'est pas — ce module ne revendique aucune exhaustivite (D-85).
    """
    constats: list[str] = []
    for _, cible in _cibles_de_liens(texte):
        if not _cible_interne(cible):
            continue
        if not (racine / cible).exists():
            constats.append(
                f"{fichier or 'texte controle'} : {MOTIF_README} — la cible interne « {cible} » n'existe "
                f"pas sous {racine} ; attendu un renvoi interne qui resout depuis la racine du depot "
                f"(D-87)"
            )
    return constats


def test_renvois_du_readme_resolus(docs_dir: Path, normalize) -> None:
    """Chaque renvoi interne du `README.md` resout, et ce controle est prouve mordant (D-87, D-84).

    Tranche verticale du plan : elle traverse le fichier de la racine, le detecteur et le disque. Le
    temoin est mesure **vert** sur le texte livre ; la morsure est ensuite mesuree dans le meme test, sur
    une **copie en memoire** ou la cible du premier renvoi interne est remplacee par un chemin absent —
    aucun fichier du depot n'est ecrit, et la mutation vit sur une chaine (D-84).

    La mesure doit avoir un objet : un `README.md` sans aucun renvoi interne rendrait le controle vert
    sans qu'il ait rien controle. C'est pourquoi l'absence de renvoi interne est un constat, et non un
    vert silencieux.

    Limite honnete : ce controle dit que les cibles de liens Markdown du fichier resolvent depuis la
    racine du depot. Il ne dit rien d'un renvoi ecrit en prose, et il ne reecrit rien du fichier : le
    bloc de commandes du `README.md` est hors du mandat de cette phase (D-87).
    """
    chemin = docs_dir.parent / README
    if not chemin.is_file():
        raise AssertionError(
            f"{README} : fichier introuvable ({chemin}) ; attendu le fichier de la racine du depot dont "
            f"chaque renvoi interne est controle (D-87)"
        )
    texte = chemin.read_text(encoding="utf-8")
    liens = _cibles_de_liens(texte)
    cibles = [cible for _, cible in liens if _cible_interne(cible)]
    constats: list[str] = []

    # 1. La mesure a un objet : au moins un renvoi interne dans le fichier.
    if not cibles:
        constats.append(
            f"{README} : {MOTIF_README} — la mesure n'a aucun objet : aucun renvoi interne n'a ete vu "
            f"dans {chemin} (cibles lues : {', '.join(normalize(cible) for _, cible in liens) or 'aucune'}) "
            f"; attendu au moins un renvoi interne, la garde de D-87 n'ayant rien a resoudre sur un "
            f"fichier sans renvoi"
        )

    # 2. Le temoin vert : le texte **livre** ne porte aucun renvoi mort.
    temoin = renvois_morts(texte, chemin.parent, fichier=README)
    if temoin:
        constats.append(
            f"{README} : {MOTIF_README} — le fichier livre est deja signale par le detecteur : "
            + " ; ".join(temoin)
        )

    # 3. La morsure, mesuree dans le meme test sur une copie en memoire (D-84).
    if cibles:
        cible = cibles[0]
        mute = texte.replace(f"({cible})", f"({cible}.absent)", 1)
        if mute == texte:
            constats.append(
                f"{README} : {MOTIF_README} — la copie en memoire n'a pas pu etre construite : la cible "
                f"« {cible} » n'a pas ete retrouvee telle quelle dans {chemin} ; attendu une cible ecrite "
                f"« ({cible}) », sans quoi la morsure ne mesurerait rien (D-84)"
            )
        elif not renvois_morts(mute, chemin.parent, fichier=README):
            constats.append(
                f"{README} : {MOTIF_README} — la copie en memoire ou la cible « {cible} » est remplacee "
                f"par « {cible}.absent » n'est signalee par aucun constat ; attendu au moins un constat, "
                f"sans quoi ce controle vert ne dirait rien de sa valeur (D-84)"
            )

    assert not constats, (
        f"{README} : constats sur la resolution des renvois : "
        + " ; ".join(constats)
        + f" ; attendu un fichier dont chaque renvoi interne resout depuis la racine du depot, et un "
        f"detecteur dont la morsure est mesuree sur une copie en memoire (D-87, D-84)"
    )


def test_renvoi_base_locale_legitime(docs_dir: Path, normalize) -> None:
    """La dette D-44 est **denouee** : deux renvois vers la base locale, dont un dans la section idoine.

    La dette D-44/D-63 n'est pas supprimee par un controle en moins : le renvoi en prose de
    `docs/parcours-simplifie.md` est devenu un **lien**, parce que la cible existe desormais, et ce
    controle exige les deux faits ensemble — le lien dans la section des renvois, et le sens conserve
    (la section nomme toujours la base locale en clair, la normalisation du depot absorbant casse,
    accents et entites, D-11).

    Limite honnete : ce controle dit ce que les deux renvois nommes sont devenus, et que la cible existe.
    Il ne dit rien de la prose du reste de la page (D-85).
    """
    chemin = docs_dir / PAGE_PARCOURS
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE_PARCOURS} : page introuvable ({chemin}) ; attendu la page du parcours simplifie, "
            f"celle dont les renvois vers « {PAGE} » sont controles (D-63)"
        )
    texte = chemin.read_text(encoding="utf-8")
    cibles = [cible for _, cible in _cibles_de_liens(texte) if cible.endswith(PAGE)]
    corps = _corps_du_titre(texte, TITRE_SECTION_RENVOI)
    constats: list[str] = []

    # 1. Les deux renvois de la page, dont un dans sa phrase d'introduction.
    if len(cibles) < RENVOIS_PAGE_VOISINE:
        constats.append(
            f"{PAGE_PARCOURS} : {MOTIF_LIEN_D63} — la page porte {len(cibles)} renvoi(s) vers « {PAGE} » "
            f"({', '.join(cibles) or 'aucun'}) ; attendu au moins {RENVOIS_PAGE_VOISINE} renvois, la dette "
            f"etant denouee par un renvoi legitime et non par la suppression d'un controle (D-44, D-63)"
        )

    # 2. Le renvoi de la section des renvois, et le sens qui y est conserve.
    if TITRE_SECTION_RENVOI not in texte:
        constats.append(
            f"{PAGE_PARCOURS} : {MOTIF_LIEN_D63} — la section « {TITRE_SECTION_RENVOI} » est introuvable "
            f"dans {chemin} ; attendu la section ouverte par ce titre de niveau 3, celle ou le renvoi en "
            f"prose est devenu un lien (D-63, D-86)"
        )
    else:
        if f"]({PAGE})" not in corps:
            constats.append(
                f"{PAGE_PARCOURS} : {MOTIF_LIEN_D63} — la section « {TITRE_SECTION_RENVOI} » ne porte "
                f"aucun lien vers « {PAGE} » ; attendu un renvoi en prose devenu lien, la cible existant "
                f"desormais (D-63, D-86)"
            )
        if normalize("base locale") not in normalize(corps):
            constats.append(
                f"{PAGE_PARCOURS} : {MOTIF_LIEN_D63} — la section « {TITRE_SECTION_RENVOI} » ne nomme "
                f"plus la base locale en clair ; attendu le sens conserve par le renvoi en prose devenu "
                f"lien (D-63)"
            )

    # 3. La cible existe sur disque : c'est ce qui rend le renvoi legitime, et non seulement present.
    if not (docs_dir / PAGE).is_file():
        constats.append(
            f"{PAGE_PARCOURS} : {MOTIF_LIEN_D63} — la cible « {PAGE} » n'existe pas sous {docs_dir} ; "
            f"attendu la page de la base locale, sans laquelle le renvoi resterait mort (D-63)"
        )

    assert not constats, (
        f"{PAGE_PARCOURS} : constats sur le renvoi vers la base locale : "
        + " ; ".join(constats)
        + f" ; attendu deux renvois vers « {PAGE} » dont un dans la section « {TITRE_SECTION_RENVOI} », "
        f"la section nommant toujours la base locale en clair, et la page cible presente sur disque "
        f"(D-44, D-63, D-86)"
    )


def test_page_close_et_sans_valeur_volatile(docs_dir: Path, section, normalize) -> None:
    """La page est close : sections epinglees dans les deux sens, octets CRLF, valeurs et chemins (D-69).

    Derniere ecriture de la page, donc seul moment ou les regles d'ensemble s'appliquent a l'objet fini :

    - la cloture est comparee **dans les deux sens** : aucun titre de `TITRES_SECTION_ATTENDUS` ne
      manque, aucun titre de niveau 2 de la page n'est hors de cette liste, et ceux qui y appartiennent y
      sont **dans l'ordre** — quel que soit le nombre d'entrees de la constante a ce stade ;
    - `## Source de verite` reste le dernier titre epingle, et la derniere ligne non vide reste la ligne
      de retour vers le sommaire ;
    - les octets sont lus **en binaire** (`read_bytes`), jamais sur un texte re-encode : aucun BOM,
      decodage UTF-8 strict, et autant de retours chariot que de fins de ligne (CRLF sur toutes les
      lignes). Cette assertion depend de la configuration Git du poste : `core.autocrlf=true` sur ce
      poste, et **aucun `.gitattributes`** dans le depot — elle **n'est pas portable** (AR-5). Elle est
      ecrite ici comme les phases 3 et 4 l'ont ecrite, sans etre presentee comme telle ;
    - aucune valeur volatile (compteur d'objets, version de jeu, horodatage, taille figee), aucune porte
      de sortie (aucun lien externe, aucune adresse en clair), et chaque chemin cite entre accents graves
      dans le bloc « Source de verite » existe depuis la racine du depot.

    Le texte vient du lecteur local `_texte_page` quand les octets se decodent ; quand ils ne se decodent
    pas, le constat est produit et les controles de texte sont ecrits sur une chaine vide, plutot que de
    laisser `read_text` lever avant tout constat.

    Limite honnete : ce controle ne verifie **pas** la prose libre de la page, la formulation des
    avertissements ni l'appreciation de lisibilite : ces trois points restent hors de portee d'un
    controle, et ce module ne revendique aucune exhaustivite de la redaction (D-85).
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page de la base locale, lue en binaire "
            f"pour la cloture de ses octets et de ses sections (D-67, D-69)"
        )
    octets = chemin.read_bytes()
    constats: list[str] = []

    # 1. Les octets, lus en binaire : BOM, UTF-8 strict, CRLF sur toutes les lignes.
    if octets.startswith(BOM_UTF8):
        constats.append(
            f"{PAGE} : {MOTIF_CRLF} — la page commence par un BOM ; attendu un fichier UTF-8 sans BOM, "
            f"lu en binaire (D-67)"
        )
    decode_refuse = False
    try:
        octets.decode("utf-8")
    except UnicodeDecodeError as erreur:
        decode_refuse = True
        constats.append(
            f"{PAGE} : {MOTIF_CRLF} — les octets de la page ne se decodent pas en UTF-8 strict "
            f"(« {erreur} ») ; attendu un fichier UTF-8 sans BOM, lu en binaire et jamais sur un texte "
            f"re-encode (D-67)"
        )
    fins = octets.count(b"\n")
    retours = octets.count(b"\r\n")
    if retours != fins:
        constats.append(
            f"{PAGE} : {MOTIF_CRLF} — la page porte {fins} fin(s) de ligne pour {retours} retour(s) "
            f"chariot ; attendu des fins de ligne CRLF sur toutes les lignes, comme le reste du depot "
            f"(D-67, D-69)"
        )
    texte = "" if decode_refuse else _texte_page(docs_dir)

    if texte:
        # 2. Un seul titre de niveau 1, et c'est celui de la page.
        h1 = [ligne.strip() for ligne in texte.splitlines() if ligne.startswith(FRAGMENT_H1)]
        if len(h1) != 1:
            constats.append(
                f"{PAGE} : {MOTIF_SECTION} — la page porte {len(h1)} titre(s) de niveau 1 "
                f"({', '.join(h1) or 'aucun'}) ; attendu un seul titre de niveau 1, « {TITRE_H1} » (D-69)"
            )
        elif h1[0] != TITRE_H1:
            lisse = normalize(h1[0]) == normalize(TITRE_H1)
            constats.append(
                f"{PAGE} : {MOTIF_SECTION} — le titre de niveau 1 vaut « {h1[0]} » ; attendu "
                f"« {TITRE_H1} »"
                + (
                    " (ecart de casse ou d'accent seulement : la forme ecrite au caractere pres est "
                    "exigee, la normalisation ne sert ici qu'au diagnostic)"
                    if lisse
                    else " (titre different de celui attendu)"
                )
                + f" ; attendu le titre de la page de la base locale (D-69)"
            )

        # 3. La cloture des sections, dans les deux sens : aucun titre attendu manquant, aucun titre de
        #    la page hors de la liste, et l'ordre de ceux qui appartiennent a la liste.
        titres = [ligne.strip() for ligne in texte.splitlines() if ligne.startswith("## ")]
        attendus = list(TITRES_SECTION_ATTENDUS)
        manquants = [titre for titre in attendus if titre not in titres]
        etrangers = [titre for titre in titres if titre not in attendus]
        presents = [titre for titre in titres if titre in attendus]
        if manquants:
            constats.append(
                f"{PAGE} : {MOTIF_SECTION} — {len(manquants)} section(s) attendue(s) absente(s) de la "
                f"page : {', '.join(manquants)} ; attendu les {len(attendus)} sections de "
                f"TITRES_SECTION_ATTENDUS, quelle que soit la longueur de cette constante (D-69)"
            )
        if presents != attendus:
            constats.append(
                f"{PAGE} : {MOTIF_SECTION} — les sections attendues ne se suivent pas dans l'ordre du "
                f"document : lu ({', '.join(presents) or 'aucune'}) ; attendu ({', '.join(attendus)}) "
                f"(D-69)"
            )
        if etrangers:
            constats.append(
                f"{PAGE} : {MOTIF_SECTION} — la page porte {len(etrangers)} titre(s) de niveau 2 hors de "
                f"TITRES_SECTION_ATTENDUS : {', '.join(etrangers)} ; attendu aucun titre de niveau 2 hors "
                f"de la liste epinglee, un titre inattendu etant une derive de structure et non une "
                f"liberte de redaction (D-69)"
            )
        if titres and titres[-1] != TITRE_SOURCE:
            constats.append(
                f"{PAGE} : {MOTIF_SECTION} — la derniere section de la page est « {titres[-1]} » ; attendu "
                f"« {TITRE_SOURCE} » comme dernier titre epingle (D-69)"
            )
        remplies = [ligne.strip() for ligne in texte.splitlines() if ligne.strip()]
        derniere = remplies[-1] if remplies else ""
        if derniere != LIEN_RETOUR:
            constats.append(
                f"{PAGE} : {MOTIF_SECTION} — la derniere ligne non vide vaut « {derniere} » ; attendu "
                f"« {LIEN_RETOUR} » comme derniere ligne de la page (D-69)"
            )

        # 4. Aucune valeur volatile epinglee (D-73, D-75).
        volatiles = sorted(set(MOTIF_VOLATILE.findall(texte)))
        if volatiles:
            constats.append(
                f"{PAGE} : {MOTIF_VOLATILES} — la page porte {', '.join(volatiles)} ; attendu aucun "
                f"nombre de quatre chiffres ou plus — ni compteur d'objets, ni version de jeu, ni "
                f"horodatage, ni taille de fichier (D-73, D-75)"
            )

        # 5. Aucune porte de sortie : ni lien externe, ni adresse en clair.
        sortants = sorted(
            {cible for _, cible in _cibles_de_liens(texte) if cible.startswith(CIBLES_EXTERNES)}
        )
        if sortants:
            constats.append(
                f"{PAGE} : {MOTIF_LIEN_EXTERNE} — la page porte {len(sortants)} lien(s) sortant(s) : "
                f"{', '.join(sortants)} ; attendu des liens internes seulement, la page decrivant le "
                f"produit de ce depot (D-01, D-03)"
            )
        for schema in CIBLES_EXTERNES:
            if schema in texte:
                constats.append(
                    f"{PAGE} : {MOTIF_LIEN_EXTERNE} — la page porte « {schema} » ; attendu aucune adresse "
                    f"externe, meme en clair, aucune porte de sortie n'etant ouverte par cette page "
                    f"(D-01, D-03)"
                )

        # 6. Le bloc « Source de verite » : chaque chemin cite existe depuis la racine du depot.
        corps_source = section(texte, TITRE_SOURCE, PAGE)
        jetons = sorted(
            {
                trouve.group("jeton")
                for trouve in MOTIF_JETON_ACCENTS.finditer(corps_source)
                if "/" in trouve.group("jeton")
                or trouve.group("jeton").endswith(SUFFIXES_CHEMIN)
            }
        )
        if not jetons:
            constats.append(
                f"{PAGE} : {MOTIF_SOURCE} — la section « {TITRE_SOURCE} » ne cite aucun chemin entre "
                f"accents graves ; attendu au moins un chemin, la page ancrant ses valeurs sur le code "
                f"de ce depot (D-03, D-69)"
            )
        for jeton in jetons:
            if not (RACINE_DEPOT / jeton).exists():
                constats.append(
                    f"{PAGE} : {MOTIF_SOURCE} — la section « {TITRE_SOURCE} » cite « {jeton} » et ce "
                    f"chemin n'existe pas sous {RACINE_DEPOT} ; attendu un chemin existant, un chemin "
                    f"disparu signalant une page desalignee (D-03, D-69)"
                )

    assert not constats, (
        f"{PAGE} : constats de cloture de la page : "
        + " ; ".join(constats)
        + f" ; attendu une page close — sections epinglees dans les deux sens, « {TITRE_SOURCE} » en "
        f"dernier titre, « {LIEN_RETOUR} » en derniere ligne, octets CRLF sans BOM, aucune valeur "
        f"volatile, aucun lien externe et chaque chemin du bloc source existant (D-67, D-69, D-73)"
    )
