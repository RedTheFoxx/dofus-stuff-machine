"""Ancrage de la page `docs/cli.md` sur la surface reelle du parseur (CLI-01, CLI-02).

Le contrat va de la page vers le parseur : chaque jeton epingle ci-dessous est cherche dans la
page, puis sonde sur `build_parser().parse_args` — et chaque option longue citee par les lignes
de tableau des sections « Options globales », « search », « list » et « optimize » est sondee de la
meme facon, de sorte qu'une option inventee par la page soit nommee par l'echec. La troisieme
colonne de ces tableaux (« Defaut ») est lue et comparee aux valeurs par defaut reellement rendues
par le parseur, et chaque jeton qui y est cite est exige parmi les options que le parseur declare
dans ses aides publiques (`format_help()` du parseur racine et aide de chaque sous-commande) : un
prefixe non ambigu accepte par `argparse` ne suffit donc plus a faire passer un jeton perime.

Limite honnete (D-26) : la completude inverse n'est pas revendiquee. Une sous-commande ou une
option ajoutee plus tard a `dofus_stuff/cli.py` et non documentee ne fera pas echouer cette
suite ; le contrat est « page -> parseur » plus les listes epinglees ci-dessous, jamais une
egalite d'ensembles avec la surface du parseur.

Rien n'est execute : `main()` n'est jamais appele, aucune base n'est ouverte, aucun sous-processus
et aucune socket ne sont crees, rien n'est ecrit sous `.data/` (D-15). `db clear` est *parse* pour
prouver que la page cite une commande reelle, jamais execute.

Limite de lecture mesuree, corrigee apres revue de code (WR-05) : `argparse` accepte le prefixe non
ambigu d'une option reelle (mesure : `--force-sync` reste accepte apres renommage en
`--force-synchronisation` dans une copie du parseur), donc la sonde `parse_args` seule ne prouve pas
la forme stricte d'un jeton. L'ensemble exact des jetons declares est pourtant accessible par API
publique — `format_help()` du parseur racine et l'aide de chaque sous-commande epinglee capturee sur
sa sortie standard — et c'est lui que compare le controle d'appartenance stricte du test des
tableaux d'options. La sonde par `parse_args` garde son role propre : « les exemples et les lignes de
tableau sont analysables » ; elle ne pretend pas etre le controle de forme. Aucune introspection
privee d'`argparse` n'est utilisee (D-14).
"""

from __future__ import annotations

import ast
import io
import re
import shlex
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from dofus_stuff.cli import build_parser as build_cli_parser

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "cli.md"
SOURCE_CLI = "dofus_stuff/cli.py"

TITRE_OPTIONS_GLOBALES = "## Options globales"
TITRE_OPTIMIZE = "## optimize"
TITRE_DB = "## db"
TITRE_CACHE = "## cache"
TITRE_SOURCE = "## Source de vérité"

JETON_BUILD_PARSER = "build_parser()"
JETON_AIDE = "--help"

OPTION_LONGUE = re.compile(r"--[a-z][a-z-]*")
CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml|md|js|json|sql))`")

# Les trois descriptions du groupe db, lues dans l'aide du parseur (dofus_stuff/cli.py:185, :187
# et :189). La section `cache` de la page ne doit en reproduire aucune (D-20) : c'est
# l'anti-duplication testable de l'alias.
DESCRIPTIONS_DB = (
    "Afficher l'état de la base",
    "Forcer la synchronisation complète",
    "Vider la base locale",
)

# Marqueurs d'equivalence de la section `cache`, compares apres normalisation : la page livree
# declare l'alias en prose (« `cache` est le second nom de `db` ... equivaut a `db <sous-commande> »)
# sans employer le mot « alias ». Au moins un marqueur doit etre present : le controle reste
# falsifiable, et il ne se reecrit pas a la place de la page.
JETONS_ALIAS = ("alias", "second nom", "equivaut")

# Liste epinglee des sous-commandes documentees : des argv complets, jamais un jeton nu
# (`parse_args(["db"])` et `parse_args(["cache"])` sortent en code 2, `db_command` etant requis).
SONDES_SOUS_COMMANDES = (
    ("version", ["version"]),
    ("self-test", ["self-test"]),
    ("search", ["search", "Atcham"]),
    ("item", ["item", "44"]),
    ("list", ["list"]),
    ("optimize", ["optimize", "--demo"]),
    ("db", ["db", "status"]),
    ("cache", ["cache", "status"]),
)

# Liste epinglee des options globales : declarees sur le parseur racine, donc ecrites avant la
# sous-commande, qui est requise (`parse_args(["--offline"])` sort en code 2).
SONDES_GLOBALES = (
    ("--timeout", ["--timeout", "5", "version"]),
    ("--data-dir", ["--data-dir", "x", "version"]),
    ("--force-sync", ["--force-sync", "version"]),
    ("--offline", ["--offline", "db", "status"]),
)

# Liste epinglee des 30 options d'optimize : (option, valeur d'essai ou None pour un drapeau).
# La valeur d'essai est obligatoire des qu'une option prend une valeur : la sonde tri-etat heritee
# de la phase 1 (`[opt]`, `[opt, "1"]`, `[opt, "x"]`) declare `--jet` inventee, ses trois essais
# etant refuses par les `choices` du parseur (seul `average` est accepte).
SONDES_OPTIMIZE = (
    ("--level", "123"),
    ("--max", "intelligence"),
    ("--base-int", "100"),
    ("--base-vit", "100"),
    ("--base-str", "100"),
    ("--base-cha", "100"),
    ("--base-agi", "100"),
    ("--base-wis", "100"),
    ("--scroll-int", "50"),
    ("--scroll-vit", "50"),
    ("--scroll-str", "50"),
    ("--scroll-cha", "50"),
    ("--scroll-agi", "50"),
    ("--scroll-wis", "50"),
    ("--jet", "average"),
    ("--top-k", "40"),
    ("--time-limit", "10"),
    ("--no-cpsat", None),
    ("--classic-only", None),
    ("--demo", None),
    ("--target", "intelligence=1200"),
    ("--weight", "intelligence=2"),
    ("--ban", "123"),
    ("--force", "44"),
    ("--seed", "7"),
    ("--stop-when-satisfied", None),
    ("--auto-points", None),
    ("--allow-power", None),
    ("--allow-damages", None),
    ("--allow-crit-damages", None),
)

# Sous-commandes de db dont l'alias `cache` doit produire le meme espace de noms (D-21).
SOUS_COMMANDES_DB = ("status", "stats", "sync", "fill", "clear")

# Valeurs d'essai des options d'`optimize` dont la valeur epinglee dans SONDES_OPTIMIZE est *egale*
# au defaut du parseur (`--jet average`) : la mesure d'un defaut se fait par difference des deux
# espaces de noms, donc la sonde de defaut a besoin d'une valeur qui differe du defaut. La valeur
# epinglee, elle, ne change pas : `_option_optimize_acceptee` doit continuer d'essayer une valeur
# acceptee par les `choices` du parseur.
VALEURS_ESSAI_DEFAUT = {"--jet": "min"}

# Appariement jeton de la page -> (argv *sans* l'option, argv *avec* l'option), pour les options
# globales et de sous-commande autres que les 30 d'`optimize` : celles-ci sont derivees de
# `SONDES_OPTIMIZE` par `_sondes_defauts()`, chaque entree y portant deja sa valeur d'essai.
#
# La clef de destination de chaque option n'est jamais lue dans le code (`argparse` ne l'expose que
# par introspection privee, interdite par D-14) : elle est mesuree par difference des deux espaces
# de noms, et la valeur par defaut est celle que l'argv sans l'option rend reellement (WR-01).
SONDES_DEFAUTS_FIXES: dict[str, tuple[list[str], list[str]]] = {
    # Options globales : declarees sur le parseur racine, donc ecrites avant la sous-commande.
    "--timeout": (["version"], ["--timeout", "120", "version"]),
    "--data-dir": (["version"], ["--data-dir", "x", "version"]),
    "--force-sync": (["version"], ["--force-sync", "version"]),
    "--offline": (["db", "status"], ["--offline", "db", "status"]),
    # Options propres a une sous-commande, ecrites apres elle.
    "--limit": (["search", "Atcham"], ["search", "Atcham", "--limit", "3"]),
    "--page": (["list"], ["list", "--page", "3"]),
    "--size": (["list"], ["list", "--size", "3"]),
}


# ---------------------------------------------------------------------------------------------
# Exemples marques de la page (CLI-03, D-24, D-25, D-27) et garde des commandes destructrices
# (D-22, D-23)
#
# Un exemple est une ligne d'un bloc de code dont la balise d'ouverture est `console`
# (`BALISE_EXEMPLE` de `tests/conftest.py`, D-24) : une commande citee en prose n'en est pas un, et
# seule la projection `lignes_exemple` les rend — jamais un second scanner de blocs (D-12).
#
# Chaque exemple est decoupe par `shlex.split` puis soumis a `build_parser().parse_args` (D-25,
# D-14 : parseur public seul). La commande est *parsee*, jamais executee : ni `main()`, ni
# sous-processus, ni base ouverte, ni socket (D-15) — `test_sans_execution_ni_base_locale` verifie
# cette propriete sur le texte de ce module.
#
# Quatre regles de redaction mesurees pour un exemple (02-RESEARCH.md, Pitfall 9) :
#   1. aucun commentaire en fin de ligne : il devient des arguments et le parseur sort en code 2 ;
#   2. aucune continuation par antislash : `shlex.split` leve `ValueError` avant le parseur ;
#   3. aucun metacaractere de shell : `*` et `$` ne sont pas etendus, mais sont acceptes, donc les
#      montrer enseignerait un comportement que le lecteur n'obtiendra pas ;
#   4. chemin portable ou guillemete pour `--data-dir` : `shlex` avale silencieusement un chemin
#      Windows non guillemete et le parseur l'accepte — le controle resterait alors aveugle.
#
# Limite honnete (D-26), ecrite ici et pas seulement dans le plan : la ligne etant *extraite* de la
# page, l'exigence « verbatim » de CLI-03 est une garantie de construction, pas une exigence de
# validation qui pourrait echouer seule ; la completude inverse (toute option du parseur
# documentee) n'est pas revendiquee — une option ajoutee plus tard au parseur sans etre documentee
# ne fera pas rougir cette suite. La qualite « hors parcours recommande » du critere 4b n'est pas
# decidable mecaniquement : elle n'est approchee que par la co-presence de l'avertissement sur la
# meme ligne et par l'absence de la commande destructrice dans tout bloc marque.

# Forme dont la page doit porter au moins un exemple : l'option globale *avant* sa sous-commande
# (`db status --offline` sort en code 2, `fetcher.py: error: unrecognized arguments: --offline`).
# Constante de module et non litteral dans le corps du test : la batterie de mutations cherche cette
# forme dans la sortie, et pytest imprime la source de l'assertion en echec — un litteral dans
# l'assertion ferait croire a la detection meme si le message ne portait pas la forme attendue.
FORME_ATTENDUE = ("--offline", "optimize")

# Options globales du parseur racine qui consomment le jeton suivant : la projection du nom de
# sous-commande saute leur valeur, sinon `--data-dir x` ferait lire `x` comme une sous-commande.
OPTIONS_GLOBALES_A_VALEUR = ("--timeout", "--data-dir")

# Commande destructrice : `db` ou `cache`, des espaces quelconques (`\s+`), puis `clear`, chaque mot
# delimite. Le motif doit couvrir `cache clear` autant que `db clear` — sinon il laisserait passer
# exactement la meme destruction sous l'autre nom (lecon WR-01). Il sert aux regles (a) et (b)
# ci-dessous, celles du classement « destructeur » et de son avertissement.
JETON_DESTRUCTEUR = re.compile(r"(?<![\w-])(?:db|cache)\s+clear(?![\w-])")

# Commandes qui vident la base **ou** la reecrivent avec le reseau : `clear`, mais aussi `sync` et
# `fill` (alias de `sync`), que D-23 classe comme destructrices — elles reecrivent la base locale et
# exigent le reseau. Ce motif n'est volontairement PAS utilise pour la co-presence de
# l'avertissement de la regle (b) : la page cite `db sync` et `cache fill` dans une phrase qui ne
# porte pas le mot « destruct », et une co-presence etendue a `sync`/`fill` rendrait la page livree
# faussement rouge (mesure de revue, WR-02). Seule la regle (c) — « jamais une commande a recopier »
# — en depend.
JETONS_RESEAU = re.compile(r"(?<![\w-])(?:db|cache)\s+(?:clear|sync|fill)(?![\w-])")

# Jeton d'avertissement, cherche sur la ligne normalisee (D-11) : couvre aussi bien « destructif »
# que « destructrice » ou « destruction ». Le classement « destructeur » de `db clear` et
# `cache clear` est un jugement derive du code (`dofus_stuff/database.py`, `Database.clear` supprime
# `items` et `meta` sans confirmation), pas une propriete declaree par le parseur : ce motif prouve
# que le classement retenu est applique, pas qu'il est complet.
JETON_AVERTISSEMENT = "destruct"

# Modules dont l'import, dans ce module d'ancrage, trahirait une execution ou un acces a la base
# locale (D-15) : `shlex` decoupe sans executer et `parse_args` ne construit rien.
INTERDITS_EXECUTION = ("subprocess", "socket", "sqlite3")

# Seul module du produit que ce module a le droit d'importer : le parseur public (D-14, D-15).
IMPORT_PRODUIT_AUTORISE = "dofus_stuff.cli"


def _texte_page(docs_dir: Path) -> str:
    """Texte de la page, lu en UTF-8 explicite ; page absente = AssertionError localisante (D-13).

    Jamais de FileNotFoundError brut (lecon IN-03) : l'echec nomme la page, le chemin attendu et
    le fichier de code dont elle decrit la surface. Toute lecture de la page passe par ici.
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page de reference de "
            f"{SOURCE_CLI} livree dans docs/"
        )
    return chemin.read_text(encoding="utf-8")


def _accepte(argv: list[str]) -> bool:
    """Vrai si `build_parser().parse_args(argv)` accepte cet argv complet (D-14 : API publique).

    Le `SystemExit` d'`argparse` ne traverse jamais : chaque refus devient un constat nomme, et les
    deux sorties du parseur sont capturees pour ne pas polluer le rapport pytest. Le succes se lit au
    code de sortie, jamais a la seule absence d'exception : `argparse` leve `SystemExit(0)` apres
    avoir imprime une aide, et `--help` est une option reelle du parseur (WR-03).
    """
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            build_cli_parser().parse_args(argv)
    except SystemExit as sortie:
        return sortie.code in (0, None)
    return True


def _aide_capturee(argv: list[str]) -> str:
    """Sortie standard d'un argv d'aide du parseur public, sans jamais l'executer (D-14, D-15).

    `format_help()` du parseur racine ne rend que les options globales : l'aide d'un sous-parseur
    s'obtient par `parse_args([... \"--help\"])`, qui leve `SystemExit(0)` apres avoir ecrit sur la
    sortie standard — d'ou la capture des deux flux, la sortie d'erreur ne portant rien ici.
    """
    tampon = io.StringIO()
    try:
        with redirect_stdout(tampon), redirect_stderr(io.StringIO()):
            build_cli_parser().parse_args(argv)
    except SystemExit:
        pass
    return tampon.getvalue()


def _options_declarees() -> set[str]:
    """Jetons d'option longue que le parseur declare, lus par API publique seule (WR-05, D-14).

    Chaque aide est une aide publique : `format_help()` du parseur racine pour la surface globale,
    puis l'aide capturee de chaque sous-commande epinglee (`<argv> --help`), dont les options
    propres ne figurent pas dans l'aide racine. Un prefixe non ambigu accepte par `parse_args` ne
    figure pas forcement dans cet ensemble : c'est precisement le controle d'appartenance stricte
    que la tolerance d'`argparse` rend necessaire. Aucune introspection privee n'est employee.
    """
    aides = [build_cli_parser().format_help()]
    aides.extend(_aide_capturee([*argv, "--help"]) for _, argv in SONDES_SOUS_COMMANDES)
    return {option for aide in aides for option in OPTION_LONGUE.findall(aide)}


def _sondes_defauts() -> dict[str, tuple[list[str], list[str]]]:
    """Appariement jeton de la page -> (argv sans l'option, argv avec l'option), `optimize` compris."""
    sondes = dict(SONDES_DEFAUTS_FIXES)
    for jeton, valeur in SONDES_OPTIMIZE:
        sondes[jeton] = (
            ["optimize"],
            _argv_optimize(jeton, VALEURS_ESSAI_DEFAUT.get(jeton, valeur)),
        )
    return sondes


def _clef_et_defaut(
    argv_base: list[str], argv_sonde: list[str]
) -> tuple[str | None, object, str | None]:
    """(clef de destination, defaut reel, constat) mesures par difference des espaces de noms.

    La clef de destination n'est jamais lue dans le code de `dofus_stuff/cli.py` (D-14) : c'est
    celle qui change entre l'argv sans l'option et l'argv sans elle. Une sonde qui ne fait changer
    aucune clef, ou plus d'une, est un defaut de la liste epinglee de ce module : elle le dit au
    lieu de laisser croire a un defaut de la page.
    """
    try:
        avant = dict(vars(build_cli_parser().parse_args(argv_base)))
        apres = dict(vars(build_cli_parser().parse_args(argv_sonde)))
    except SystemExit:
        return None, None, (
            f"la sonde de defaut « {' '.join(argv_sonde)} » est refusee par "
            f"{SOURCE_CLI}::build_parser().parse_args() ; attendu un argv epingle accepte"
        )
    changees = sorted(
        clef for clef in set(avant) | set(apres) if avant.get(clef) != apres.get(clef)
    )
    if len(changees) != 1:
        return None, None, (
            f"la sonde de defaut « {' '.join(argv_sonde)} » fait changer {len(changees)} clef(s) "
            f"({', '.join(changees) or 'aucune'}) par rapport a « {' '.join(argv_base)} » ; attendu "
            f"exactement la clef de l'option sondee"
        )
    return changees[0], avant[changees[0]], None


def _valeur_de_cellule(cellule: str) -> object:
    """Valeur d'une cellule « Defaut » de la page, ou son texte si elle n'est pas litterale.

    Les formes non litterales employees par la page sont traduites : `faux` -> `False`,
    `aucun`/`aucune` -> `None`, `0` -> `0.0` (nombre). Toute autre forme (prose, jeton inconnu) est
    rendue telle quelle : la comparaison la declare fautive en nommant la cellule, donc une cellule
    non analysable devient un constat nomme et jamais un saut silencieux (WR-01).
    """
    texte = cellule.strip()
    if len(texte) >= 2 and texte.startswith("`") and texte.endswith("`"):
        texte = texte[1:-1].strip()
    if texte in ("faux", "false"):
        return False
    if texte in ("aucun", "aucune", "none"):
        return None
    try:
        return float(texte)
    except ValueError:
        return texte


def _defaut_correspond(cellule: str, defaut: object) -> bool:
    """Vrai si la cellule de la page annonce le defaut reellement rendu par le parseur (WR-01)."""
    valeur = _valeur_de_cellule(cellule)
    if isinstance(defaut, Path):
        # Cellule en prose (« le dossier `.data/` a la racine du depot ») : la comparaison porte sur
        # le nom du dossier resolu, seule partie stable d'un chemin propre au poste (D-19).
        return bool(defaut.name) and defaut.name in cellule
    if isinstance(defaut, bool):
        return isinstance(valeur, bool) and valeur is defaut
    if defaut is None:
        return valeur is None
    if isinstance(defaut, (int, float)):
        return (
            isinstance(valeur, (int, float))
            and not isinstance(valeur, bool)
            and float(valeur) == float(defaut)
        )
    return isinstance(valeur, str) and valeur == defaut


def _lignes_option(texte: str) -> list[tuple[int, list[str], list[str]]]:
    """Lignes de tableau citant une option longue : (numero de ligne, jetons, cellules).

    Une ligne est une ligne d'option des que sa premiere cellule porte un jeton `--…` ; le numero de
    ligne permet au constat de nommer l'endroit fautif (D-13). Les en-tetes, les lignes de
    separation et les tables sans option (les cinq verbes de `## db`) n'en sont pas.
    """
    lignes: list[tuple[int, list[str], list[str]]] = []
    for numero, ligne in enumerate(texte.splitlines(), start=1):
        if not ligne.lstrip().startswith("|"):
            continue
        cellules = [cellule.strip() for cellule in ligne.strip().strip("|").split("|")]
        jetons = OPTION_LONGUE.findall(cellules[0]) if cellules else []
        if jetons:
            lignes.append((numero, jetons, cellules))
    return lignes


def _espace_de_noms_brut(argv: list[str]) -> dict:
    """Espace de noms brut rendu par le parseur, cle `command` comprise.

    Vue brute necessaire au constat « chaque espace porte bien `command` » : `_espace_de_noms`
    la retire pour comparer l'alias, elle ne peut donc pas servir aux deux constats (Pitfall 3).
    """
    try:
        with redirect_stderr(io.StringIO()):
            namespace = build_cli_parser().parse_args(argv)
    except SystemExit:
        raise AssertionError(
            f"{PAGE} : espace de noms illisible pour « {' '.join(argv)} » ; attendu un argv "
            f"accepte par {SOURCE_CLI}::build_parser().parse_args()"
        ) from None
    return dict(vars(namespace))


def _espace_de_noms(argv: list[str]) -> dict:
    """Espace de noms rendu par le parseur, prive de la cle `command` (D-21, Pitfall 3).

    L'egalite brute de `vars(db_ns)` et `vars(cache_ns)` est toujours fausse : le parseur ecrit le
    nom choisi dans `dest="command"`, il n'y a pas d'`aliases=` dans `dofus_stuff/cli.py`.
    """
    return {cle: valeur for cle, valeur in _espace_de_noms_brut(argv).items() if cle != "command"}


def _options_des_tables(texte_section: str) -> set[str]:
    """Options longues citees par les lignes de tableau d'une section (premier caractere `|`).

    L'extraction se limite aux lignes de tableau (Pitfall 10) : le texte de la section `optimize`
    cite aussi `--offline`, option globale que le sous-parseur `optimize` refuse, et une extraction
    sur tout le texte produirait un faux echec. Le `=valeur` eventuellement colle est ignore par le
    motif, donc `--limit=10` et `--limit` se comparent pareil (lecon WR-04).
    """
    return {
        option
        for ligne in texte_section.splitlines()
        if ligne.lstrip().startswith("|")
        for option in OPTION_LONGUE.findall(ligne)
    }


def _cite_token(texte: str, jeton: str) -> bool:
    """Vrai si `jeton` est cite comme un jeton autonome, et non comme le prefixe d'un autre.

    Mesure : la page cite `--force` (contrainte d'optimize) et `--force-sync` (option globale) ;
    une recherche de sous-chaine declarerait `--force` present meme si seule l'option globale
    l'etait. Le controle exige donc que le jeton ne soit ni precede ni suivi d'un caractere de mot
    ou d'un tiret.
    """
    return re.search(rf"(?<![\w-]){re.escape(jeton)}(?![\w-])", texte) is not None


def _option_globale_acceptee(option: str) -> bool:
    """Vrai si le parseur racine accepte `option` devant une sous-commande (D-14 : API publique).

    Trois formes sont necessaires et mesurees : la sous-commande est requise
    (`parse_args(["--offline"])` sort en code 2) et une option a valeur consomme le jeton suivant
    (`parse_args(["--timeout", "version"])` sort en code 2 alors que `["--timeout", "5", "version"]`
    est accepte) — une forme unique produirait un refus faux sur une page correcte.
    """
    for argv in ([option, "version"], [option, "5", "version"], [option, "x", "version"]):
        if _accepte(argv):
            return True
    return False


def _argv_optimize(option: str, valeur: str | None) -> list[str]:
    """Sonde complete d'une option d'`optimize` : la valeur d'essai epinglee quand elle existe."""
    return ["optimize", option] if valeur is None else ["optimize", option, valeur]


def _option_optimize_acceptee(option: str) -> bool:
    """Vrai si le sous-parseur `optimize` accepte `option` (D-14 : API publique).

    Une option epinglee rejoue sa valeur d'essai : une option a `choices` est refusee par les trois
    essais generiques alors qu'elle est reelle (`parse_args(["optimize", "--jet", "1"])` et
    `["optimize", "--jet", "x"]` sortent en code 2, seul `average` est accepte) — une sonde
    generique unique declarerait inventee une option reelle de la page. Une option absente de la
    liste epinglee essaie `[option]`, `[option, "1"]` puis `[option, "x"]` ; une option inventee
    reste refusee par les trois.
    """
    for jeton, valeur in SONDES_OPTIMIZE:
        if jeton == option:
            return _accepte(_argv_optimize(jeton, valeur))
    for argv in (["optimize", option], ["optimize", option, "1"], ["optimize", option, "x"]):
        if _accepte(argv):
            return True
    return False


def test_sous_commandes_documentees_et_acceptees(docs_dir: Path, sections) -> None:
    """Chaque sous-commande documentee est citee et acceptee, et ses sections suivent l'ordre du parseur."""
    texte = _texte_page(docs_dir)
    constats: list[str] = []
    for nom, argv in SONDES_SOUS_COMMANDES:
        if nom not in texte:
            constats.append(f"la sous-commande « {nom} » n'est pas citee par {PAGE}")
        if not _accepte(argv):
            constats.append(
                f"la sonde de sous-commande « {' '.join(argv)} » est refusee par "
                f"{SOURCE_CLI}::build_parser().parse_args()"
            )

    # Le nom d'une sous-commande etant de toute facon cite par son propre exemple (le test de
    # couverture le garantit), la recherche de sous-chaine ne peut plus etre le premier controle a
    # rougir : elle est completee ici par l'existence d'une *section* de niveau 2 par sous-commande,
    # dans l'ordre du parseur (D-16). Un renommage ou une suppression de section est ainsi nomme,
    # et une occurrence fortuite ne suffit plus (mesure de revue : `item` etait satisfait par le mot
    # `items`, `version` par la prose « synchronisation de version »).
    attendus = [nom for nom, _ in SONDES_SOUS_COMMANDES]
    titres = [titre for titre, _ in sections(texte) if titre is not None]
    trouves = [titre for titre in titres if titre in set(attendus)]
    if trouves != attendus:
        constats.append(
            f"les sections de niveau 2 de {PAGE} ne portent pas les huit sous-commandes epinglees "
            f"dans l'ordre du parseur : lues {trouves or ['aucune']} ; attendu {attendus} "
            f"(une section par sous-commande, dans l'ordre declare par {SOURCE_CLI}::build_parser())"
        )

    assert not constats, (
        f"{PAGE} : constats sur les sous-commandes : "
        + " ; ".join(constats)
        + f" ; attendu chaque sous-commande documentee citee par la page et acceptee par {SOURCE_CLI}"
    )


def test_options_globales_documentees_et_acceptees(docs_dir: Path, section) -> None:
    """Les options globales epinglees sont citees et acceptees ; toute option de leur table est sondee."""
    texte = _texte_page(docs_dir)
    constats: list[str] = []
    for option, argv in SONDES_GLOBALES:
        if not _cite_token(texte, option):
            constats.append(f"l'option globale « {option} » n'est pas citee par {PAGE}")
        if not _accepte(argv):
            constats.append(
                f"la sonde « {' '.join(argv)} » est refusee par "
                f"{SOURCE_CLI}::build_parser().parse_args() ; les options globales se declarent sur le "
                f"parseur racine, donc avant la sous-commande"
            )

    citees = _options_des_tables(section(texte, TITRE_OPTIONS_GLOBALES, PAGE)) - {JETON_AIDE}
    if not citees:
        constats.append(
            f"aucune option longue n'est citee par les lignes de tableau de « {TITRE_OPTIONS_GLOBALES} » ; "
            f"attendu la surface globale de {SOURCE_CLI}"
        )
    inventees = sorted(option for option in citees if not _option_globale_acceptee(option))
    if inventees:
        constats.append(
            f"option(s) citee(s) par la table de « {TITRE_OPTIONS_GLOBALES} » mais refusee(s) par le "
            f"parseur racine : {', '.join(inventees)} ; attendu chaque option citee acceptee par "
            f"{SOURCE_CLI}::build_parser().parse_args()"
        )

    assert not constats, (
        f"{PAGE} : constats sur les options globales : "
        + " ; ".join(constats)
        + f" ; attendu chaque option globale citee par la page et acceptee par {SOURCE_CLI}"
    )


def test_options_optimize_documentees_et_acceptees(docs_dir: Path, section) -> None:
    """Les 30 options epinglees d'optimize sont citees et acceptees ; toute option de leurs tables est sondee."""
    texte = _texte_page(docs_dir)
    constats: list[str] = []
    for option, valeur in SONDES_OPTIMIZE:
        if not _cite_token(texte, option):
            constats.append(f"l'option « {option} » n'est pas citee par {PAGE}")
        argv = _argv_optimize(option, valeur)
        if not _accepte(argv):
            constats.append(
                f"la sonde « {' '.join(argv)} » est refusee par "
                f"{SOURCE_CLI}::build_parser().parse_args()"
            )

    citees = _options_des_tables(section(texte, TITRE_OPTIMIZE, PAGE)) - {JETON_AIDE}
    if not citees:
        constats.append(
            f"aucune option longue n'est citee par les lignes de tableau de « {TITRE_OPTIMIZE} » ; "
            f"attendu les options du sous-parseur optimize de {SOURCE_CLI}"
        )
    inventees = sorted(option for option in citees if not _option_optimize_acceptee(option))
    if inventees:
        constats.append(
            f"option(s) citee(s) par les tables de « {TITRE_OPTIMIZE} » mais refusee(s) par le "
            f"sous-parseur optimize : {', '.join(inventees)} ; attendu chaque option citee acceptee "
            f"par {SOURCE_CLI}::build_parser().parse_args()"
        )

    assert not constats, (
        f"{PAGE} : constats sur les options d'optimize : "
        + " ; ".join(constats)
        + f" ; attendu chaque option d'optimize citee par la page et acceptee par {SOURCE_CLI}"
    )


def test_valeurs_par_defaut_des_tables_egales_a_celles_du_parseur(docs_dir: Path) -> None:
    """La colonne « Defaut » des tableaux d'options est celle du parseur, ligne par ligne (WR-01, WR-05).

    Deux proprietes distinctes, mesurees sur la meme passe :

    - chaque ligne de tableau qui cite une option longue est appariee a une sonde de defaut, et
      chaque sonde a sa ligne : une ligne ne peut donc etre ni sautee ni inventee, et la cellule
      « Defaut » est comparee a la valeur que le parseur rend reellement (WR-01). Les valeurs non
      litterales de la page sont traduites (`faux`, `aucun`/`aucune`, `0`, et pour `--data-dir` le
      nom du dossier resolu, seule partie stable d'un chemin propre au poste) ;
    - chaque jeton cite figure aussi dans les aides publiques du parseur, lu par `format_help()` et
      par l'aide capturee d'`optimize` (WR-05) : `argparse` accepte le prefixe non ambigu d'une
      option reelle, donc un renommage cote parseur resterait invisible a la seule sonde d'analyse
      — c'est exactement la « documentation perimee » que le projet doit empecher.
    """
    texte = _texte_page(docs_dir)
    sondes = _sondes_defauts()
    declarees = _options_declarees()
    constats: list[str] = []

    lignes = _lignes_option(texte)
    citees = sorted({jeton for _, jetons, _ in lignes for jeton in jetons})
    if not citees:
        constats.append(
            f"aucune ligne de tableau de {PAGE} ne cite d'option longue ; la colonne « Defaut » "
            f"serait alors vide, donc infalsifiable — attendu les options de "
            f"{SOURCE_CLI}::build_parser() en lignes de tableau"
        )

    inventees = sorted(jeton for jeton in citees if jeton not in sondes)
    if inventees:
        constats.append(
            f"option(s) citee(s) par les tableaux de {PAGE} sans sonde de defaut epinglee : "
            f"{', '.join(inventees)} ; attendu une sonde par option citee, aucune ligne n'etant ni "
            f"sautee ni inventee"
        )
    non_documentees = sorted(jeton for jeton in sondes if jeton not in citees)
    if non_documentees:
        constats.append(
            f"option(s) epinglee(s) sans ligne de tableau dans {PAGE} : "
            f"{', '.join(non_documentees)} ; attendu une ligne de tableau par option epinglee, la "
            f"colonne « Defaut » ne pouvant plus etre verifiee pour une option absente"
        )

    for numero, jetons, cellules in lignes:
        for jeton in jetons:
            if jeton not in sondes:
                continue
            if len(cellules) < 3:
                constats.append(
                    f"ligne {numero} de {PAGE} : la ligne de « {jeton} » ne porte pas de colonne "
                    f"« Defaut » ; attendu trois colonnes (option, role, defaut) pour que le defaut "
                    f"reel du parseur puisse etre compare"
                )
                continue
            argv_base, argv_sonde = sondes[jeton]
            clef, defaut, echec = _clef_et_defaut(argv_base, argv_sonde)
            if echec is not None:
                constats.append(f"ligne {numero} de {PAGE} : {echec}")
                continue
            cellule = cellules[2]
            if not _defaut_correspond(cellule, defaut):
                constats.append(
                    f"ligne {numero} de {PAGE} : la colonne « Defaut » de « {jeton} » annonce "
                    f"« {cellule} » ; attendu le defaut reel du parseur pour la clef « {clef} » : "
                    f"{defaut!r} (lu par {SOURCE_CLI}::build_parser().parse_args())"
                )

    perimees = sorted(jeton for jeton in citees if jeton not in declarees)
    if perimees:
        constats.append(
            f"option(s) citee(s) par les tableaux de {PAGE} mais absente(s) des aides publiques du "
            f"parseur ({SOURCE_CLI}) : {', '.join(perimees)} ; attendu chaque jeton parmi les "
            f"options reellement declarees, un prefixe non ambigu accepte par `parse_args` ne "
            f"suffisant pas"
        )

    assert not constats, (
        f"{PAGE} : constats sur les valeurs par defaut des tableaux d'options : "
        + " ; ".join(constats)
        + f" ; attendu la colonne « Defaut » de chaque ligne egale au defaut rendu par "
        f"{SOURCE_CLI}::build_parser().parse_args() et chaque jeton declare par ses aides publiques"
    )


def test_alias_cache_equivalent_a_db_dans_le_parseur(docs_dir: Path, section, normalize) -> None:
    """`cache` equivaut a `db` pour le parseur, modulo la cle `command`, et la page ne duplique pas."""
    constats: list[str] = []
    for sous_commande in SOUS_COMMANDES_DB:
        brut_db = _espace_de_noms_brut(["db", sous_commande])
        brut_cache = _espace_de_noms_brut(["cache", sous_commande])
        if _espace_de_noms(["db", sous_commande]) != _espace_de_noms(["cache", sous_commande]):
            constats.append(
                f"l'espace de noms de « db {sous_commande} » differe de celui de "
                f"« cache {sous_commande} » hors la cle command ; attendu l'egalite prouvee par "
                f"{SOURCE_CLI}::build_parser().parse_args()"
            )
        for nom, brut in (("db", brut_db), ("cache", brut_cache)):
            if brut.get("command") != nom:
                constats.append(
                    f"l'espace de noms de « {nom} {sous_commande} » ne porte pas command={nom} "
                    f"(lu : {brut.get('command')!r})"
                )

    texte = _texte_page(docs_dir)
    corps_db = section(texte, TITRE_DB, PAGE)
    normalise_db = normalize(corps_db)
    absentes = [
        description for description in DESCRIPTIONS_DB if normalize(description) not in normalise_db
    ]
    if absentes:
        # Le controle anti-duplication ci-dessous n'exige que l'*absence* dans `## cache` : a lui
        # seul, il est satisfait par une page qui ne decrit la table nulle part (mesure de revue :
        # la table entiere des cinq verbes pouvait disparaitre sans qu'aucun test ne rougisse,
        # WR-04). La presence dans `## db` est donc exigee ici, en regard de la meme promesse.
        constats.append(
            f"la section « {TITRE_DB} » de {PAGE} ne decrit pas : {', '.join(absentes)} ; attendu "
            f"ces trois descriptions une seule fois, dans la section « {TITRE_DB} » (D-20)"
        )

    corps_cache = section(texte, TITRE_CACHE, PAGE)
    if "db" not in corps_cache:
        constats.append(f"la section « {TITRE_CACHE} » de {PAGE} ne cite pas « db »")
    normalise = normalize(corps_cache)
    if not any(marqueur in normalise for marqueur in JETONS_ALIAS):
        constats.append(
            f"la section « {TITRE_CACHE} » de {PAGE} ne declare pas l'equivalence avec db ; attendu "
            f"l'un des marqueurs {', '.join(JETONS_ALIAS)} (comparaison normalisee, D-11)"
        )
    dupliquees = [description for description in DESCRIPTIONS_DB if normalize(description) in normalise]
    if dupliquees:
        constats.append(
            f"la section « {TITRE_CACHE} » de {PAGE} duplique la description de db : "
            f"{', '.join(dupliquees)} ; attendu ces trois descriptions une seule fois, dans la "
            f"section « {TITRE_DB} » (D-20)"
        )

    assert not constats, (
        f"{PAGE} : constats sur l'alias cache : "
        + " ; ".join(constats)
        + f" ; attendu l'alias prouve par {SOURCE_CLI}::build_parser().parse_args() et non duplique par la page"
    )


def test_source_de_verite_de_la_page_cli(docs_dir: Path, section) -> None:
    """Le bloc « Source de verite » nomme `build_parser()` et chaque chemin cite par la page existe."""
    texte = _texte_page(docs_dir)
    bloc = section(texte, TITRE_SOURCE, PAGE)
    constats: list[str] = []

    chemins_bloc = sorted(set(CHEMIN_CITE.findall(bloc)))
    if not chemins_bloc:
        constats.append(
            f"aucun chemin de code n'est cite par la section « {TITRE_SOURCE} » ; attendu au moins "
            f"un chemin reel du depot ({PAGE})"
        )
    if "fetcher.py" not in chemins_bloc:
        constats.append(
            f"« fetcher.py » ne figure pas parmi les chemins cites par « {TITRE_SOURCE} » ; attendu "
            f"le point d'entree de la ligne de commande decrite par {PAGE}"
        )
    if JETON_BUILD_PARSER not in bloc:
        constats.append(
            f"le jeton « {JETON_BUILD_PARSER} » n'est pas cite par « {TITRE_SOURCE} » ; attendu la "
            f"fonction de {SOURCE_CLI} qui declare la surface documentee par {PAGE}"
        )
    manquants = sorted(
        chemin for chemin in set(CHEMIN_CITE.findall(texte)) if not (RACINE_DEPOT / chemin).exists()
    )
    if manquants:
        constats.append(
            f"chemin(s) cite(s) par {PAGE} mais absent(s) du depot : {', '.join(manquants)} ; attendu "
            f"un chemin existant depuis la racine du depot"
        )

    assert not constats, (
        f"{PAGE} : constats sur « {TITRE_SOURCE} » : "
        + " ; ".join(constats)
        + f" ; attendu le bloc Source de verite nommant {JETON_BUILD_PARSER} et ne citant que des "
        f"chemins existants de {SOURCE_CLI}"
    )


def _jetons(ligne: str) -> list[str]:
    """Jetons d'un exemple, ou AssertionError citant la page et la ligne fautive (D-13).

    `shlex.split` leve `ValueError` sur un guillemet non ferme ou sur une continuation par
    antislash : ces deux formes de redaction n'ont pas leur place dans un exemple, l'une comme
    l'autre faisant echouer la ligne avant meme d'atteindre le parseur de `dofus_stuff/cli.py`.
    Aucun `ValueError` ne traverse : il devient un constat qui nomme la page, la ligne et la cause.
    """
    try:
        return shlex.split(ligne)
    except ValueError as erreur:
        raise AssertionError(
            f"{PAGE} : exemple « {ligne} » non decoupable par shlex.split ({erreur}) ; attendu un "
            f"exemple sans guillemet non ferme ni continuation par antislash, les deux formes de "
            f"redaction qui empechent la ligne d'atteindre "
            f"{SOURCE_CLI}::build_parser().parse_args()"
        ) from None


def _exemple_accepte(ligne: str) -> bool:
    """Vrai si l'exemple complet est accepte par le parseur, sans jamais l'executer (D-15, D-25).

    Le succes se lit au code de sortie et non a l'absence d'exception : `argparse` leve
    `SystemExit(0)` apres avoir imprime son aide, et `python fetcher.py --help` est une ligne de
    reference legitime pour une page qui documente une ligne de commande (WR-03) — la compter comme
    un refus produirait un faux positif sur une page correcte. La sortie standard est capturee avec
    la sortie d'erreur, sinon les 28 lignes d'aide pollueraient le rapport pytest.
    """
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            build_cli_parser().parse_args(_jetons(ligne)[2:])
    except SystemExit as sortie:
        return sortie.code in (0, None)
    return True


def _sous_commande_atteinte(ligne: str) -> str | None:
    """Premier jeton positionnel d'un exemple : le nom de la sous-commande atteinte, ou None.

    Les deux premiers jetons (`python fetcher.py`) sont ecartes, puis chaque option globale est
    sautee ; une option qui consomme le jeton suivant (`--timeout`, `--data-dir`) fait sauter sa
    valeur, sinon cette valeur serait lue comme un nom de sous-commande.
    """
    sauter = False
    for jeton in _jetons(ligne)[2:]:
        if sauter:
            sauter = False
            continue
        if jeton.startswith("-"):
            sauter = jeton in OPTIONS_GLOBALES_A_VALEUR
            continue
        return jeton
    return None


def test_exemples_marques_sont_analysables(docs_dir: Path, lignes_exemple) -> None:
    """Chaque ligne des blocs marques `console` de la page est analysee par le parseur reel (CLI-03)."""
    texte = _texte_page(docs_dir)
    exemples = lignes_exemple(texte)
    if not exemples:
        raise AssertionError(
            f"{PAGE} : aucun bloc marque « console » trouve ; attendu au moins un exemple de ligne "
            f"de commande dans un bloc de code balise de {PAGE} et sonde sur "
            f"{SOURCE_CLI}::build_parser().parse_args() — sans aucun exemple, ce controle serait "
            f"vide, donc infalsifiable"
        )
    for ligne in exemples:
        # La ligne est extraite de la page : cette comparaison est une garantie de construction
        # (limite D-26 en tete de module), pas une exigence de validation qui pourrait echouer seule.
        # Aucune normalisation ici (D-11 ne s'applique pas a une commande : accents et espaces se
        # comparent tels quels).
        if ligne not in texte:
            raise AssertionError(
                f"{PAGE} : exemple « {ligne} » absent du texte de la page ; attendu chaque exemple "
                f"present verbatim dans {PAGE}"
            )
        jetons = _jetons(ligne)
        # Test de prefixe plutot qu'un `argv.index("fetcher.py")` : une valeur d'option qui vaudrait
        # `fetcher.py` ferait croire a un point d'entree correct.
        if jetons[:2] != ["python", "fetcher.py"]:
            raise AssertionError(
                f"{PAGE} : exemple « {ligne} » ne commence pas par « python fetcher.py » "
                f"(lu : {' '.join(jetons[:2]) or 'aucun jeton'}) ; attendu la ligne de commande de "
                f"{SOURCE_CLI} lancee depuis la racine du depot"
            )
        if not _exemple_accepte(ligne):
            raise AssertionError(
                f"{PAGE} : exemple « {ligne} » refuse par "
                f"{SOURCE_CLI}::build_parser().parse_args() ; regles de redaction mesurees : aucun "
                f"commentaire en fin de ligne, aucune continuation par antislash, aucun "
                f"metacaractere de shell (`*`, `$`), chemin portable ou guillemete pour --data-dir, "
                f"et option globale ecrite avant la sous-commande"
            )


def test_chaque_sous_commande_a_un_exemple(docs_dir: Path, lignes_exemple) -> None:
    """Les sous-commandes atteintes par les exemples sont exactement les huit epinglees (CLI-03)."""
    documentees = {nom for nom, _ in SONDES_SOUS_COMMANDES}
    atteintes = {
        sous_commande
        for sous_commande in (
            _sous_commande_atteinte(ligne) for ligne in lignes_exemple(_texte_page(docs_dir))
        )
        if sous_commande is not None
    }
    constats: list[str] = []
    manquantes = sorted(documentees - atteintes)
    if manquantes:
        constats.append(
            f"sous-commande(s) documentee(s) sans exemple : {', '.join(manquantes)} ; attendu au "
            f"moins un bloc marque « console » par sous-commande documentee de {PAGE}"
        )
    inattendues = sorted(atteintes - documentees)
    if inattendues:
        constats.append(
            f"sous-commande(s) atteinte(s) par un exemple sans etre documentee(s) : "
            f"{', '.join(inattendues)} ; attendu les huit sous-commandes epinglees de {SOURCE_CLI}"
        )

    assert not constats, (
        f"{PAGE} : constats sur la couverture par sous-commande : "
        + " ; ".join(constats)
        + f" ; attendu les huit sous-commandes de {SOURCE_CLI} atteintes par un exemple marque"
    )


def test_exemple_hors_ligne_avec_option_globale_avant_sous_commande(
    docs_dir: Path, lignes_exemple
) -> None:
    """Au moins un exemple marque place l'option globale avant sa sous-commande (D-27, critere 4a)."""
    forme = " ".join(FORME_ATTENDUE)
    trouvee = False
    for ligne in lignes_exemple(_texte_page(docs_dir)):
        jetons = _jetons(ligne)
        for index in range(2, len(jetons) - len(FORME_ATTENDUE) + 1):
            if tuple(jetons[index : index + len(FORME_ATTENDUE)]) == FORME_ATTENDUE:
                trouvee = True
    constats: list[str] = []
    if not trouvee:
        constats.append(
            f"aucun exemple marque de {PAGE} ne porte la forme « {forme} » ; attendu au moins une "
            f"ligne de la forme « python fetcher.py {forme} ... », l'option globale etant declaree "
            f"sur le parseur racine de {SOURCE_CLI}, donc ecrite avant sa sous-commande"
        )

    assert not constats, (
        f"{PAGE} : constats sur l'ordre des options : "
        + " ; ".join(constats)
        + f" ; attendu un exemple hors-ligne enseignant l'ordre reel du parseur de {SOURCE_CLI}"
    )


def test_commande_destructrice_avertie_et_jamais_dans_un_exemple(
    docs_dir: Path, lignes_exemple, normalize
) -> None:
    """La commande destructrice porte son avertissement, et aucune commande de base locale n'est un exemple.

    Les regles (a) et (b) portent sur les commandes destructrices au sens strict — `db clear` et
    `cache clear`, lues dans le code (D-22) — tandis que la regle (c) refuse aussi `db sync` et
    `cache fill` comme commandes a recopier, D-23 les classant destructrices parce qu'elles
    reecrivent la base locale.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    # (a) Presence : sans ligne citant la commande, la regle suivante serait vide, donc infalsifiable.
    lignes_citantes = [
        (numero, ligne)
        for numero, ligne in enumerate(texte.splitlines(), start=1)
        if JETON_DESTRUCTEUR.search(ligne)
    ]
    if not lignes_citantes:
        constats.append(
            f"aucune ligne de {PAGE} ne cite la commande destructrice ; la regle de co-presence "
            f"serait alors vide, donc infalsifiable — attendu au moins une ligne citant "
            f"« db clear » ou « cache clear » avec son avertissement (D-22)"
        )

    # (b) Co-presence sur la meme ligne, comparaison normalisee (D-11). Le perimetre est le texte
    # entier, ligne a ligne, jamais une section : l'en-tete de page echapperait a une regle evaluee
    # par section (lecon WR-02).
    for numero, ligne in lignes_citantes:
        if JETON_AVERTISSEMENT not in normalize(ligne):
            constats.append(
                f"ligne {numero} de {PAGE} : « {ligne.strip()} » cite la commande destructrice sans "
                f"l'avertissement attendu (jeton « {JETON_AVERTISSEMENT} » : destructif, "
                f"destructrice, destruction) ; attendu l'avertissement sur la meme ligne (D-22)"
            )

    # (c) Jamais un exemple marque : ni la commande destructrice (`clear`) ni les deux commandes qui
    # reecrivent la base avec le reseau (`db sync`, `cache fill`) ne doivent apparaitre comme des
    # commandes a recopier (D-22, D-23). Le motif est volontairement plus large ici qu'en (a) et (b),
    # qui gardent le classement « destructeur » et son avertissement : etendre *celles-la* a
    # `sync`/`fill` rendrait la page livree faussement rouge, sa phrase sur les deux sous-commandes de
    # synchronisation ne portant pas le mot « destruct ». La commande est *parsee* dans les exemples
    # pour prouver que la page cite des commandes reelles, et jamais executee — cette distinction ne
    # doit pas se perdre a la lecture.
    for ligne in lignes_exemple(texte):
        if JETONS_RESEAU.search(ligne):
            constats.append(
                f"l'exemple « {ligne} » de {PAGE} cite une commande qui vide ou reecrit la base "
                f"locale (`db clear`, `db sync`, `cache fill`) ; aucune ne doit etre une commande a "
                f"recopier (D-22, D-23), aucun bloc marque n'en contenant — attendu ces mentions "
                f"hors de tout exemple"
            )

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


def test_sans_execution_ni_base_locale() -> None:
    """Le module d'ancrage n'importe du produit que le parseur et n'execute rien (D-15, critere 5).

    La propriete est verifiee sur le texte de ce module par `ast`, et non par une recherche de
    chaines : le module cite lui-meme les noms interdits (`subprocess`, `socket`, `sqlite3`,
    `dofus_stuff.database`), donc une recherche textuelle se detecterait elle-meme. Un echec nomme
    le module fautif, la propriete attendue et le fichier de code concernee.
    """
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    importes: set[str] = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            importes.update(alias.name for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom) and noeud.module is not None:
            importes.add(noeud.module)
    appeles = {
        noeud.func.attr
        if isinstance(noeud.func, ast.Attribute)
        else getattr(noeud.func, "id", "")
        for noeud in ast.walk(arbre)
        if isinstance(noeud, ast.Call)
    }
    ancrage_public = any(
        isinstance(noeud, ast.ImportFrom)
        and noeud.module == IMPORT_PRODUIT_AUTORISE
        and any(alias.name == "build_parser" for alias in noeud.names)
        for noeud in ast.walk(arbre)
    )

    constats: list[str] = []
    hors_parseur = sorted(
        module
        for module in importes
        if (module == "dofus_stuff" or module.startswith("dofus_stuff."))
        and module != IMPORT_PRODUIT_AUTORISE
    )
    if hors_parseur:
        constats.append(
            f"import(s) du produit hors du parseur public : {', '.join(hors_parseur)} ; attendu "
            f"{IMPORT_PRODUIT_AUTORISE} seul — un module de base ou de catalogue importe ici "
            f"ouvrirait la base locale (D-15)"
        )
    interdits = sorted(module for module in importes if module.split(".")[0] in INTERDITS_EXECUTION)
    if interdits:
        constats.append(
            f"import(s) d'execution ou d'acces local : {', '.join(interdits)} ; attendu ni "
            f"subprocess, ni socket, ni sqlite3 dans le module d'ancrage decrit par {PAGE} (D-15)"
        )
    if "main" in appeles:
        constats.append(
            f"appel a main() dans le module d'ancrage ; attendu l'ancrage par le parseur de "
            f"{SOURCE_CLI} seul, la commande n'etant jamais executee (D-15)"
        )
    if not ancrage_public:
        constats.append(
            f"import « from {IMPORT_PRODUIT_AUTORISE} import build_parser » absent ; attendu "
            f"l'ancrage sur le parseur public de {SOURCE_CLI} decrit par {PAGE}"
        )

    assert not constats, (
        f"{PAGE} : constats sur la propriete « aucun test n'execute rien » : "
        + " ; ".join(constats)
        + f" ; attendu un module d'ancrage qui n'importe du produit que {IMPORT_PRODUIT_AUTORISE} "
        f"et n'ouvre ni base ni connexion"
    )



