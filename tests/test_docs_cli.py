"""Ancrage de la page `docs/cli.md` sur la surface reelle du parseur (CLI-01, CLI-02).

Le contrat va de la page vers le parseur : chaque jeton epingle ci-dessous est cherche dans la
page, puis sonde sur `build_parser().parse_args` — et chaque option longue citee par les lignes
de tableau des sections « Options globales » et « optimize » est sondee de la meme facon, de
sorte qu'une option inventee par la page soit nommee par l'echec.

Limite honnete (D-26) : la completude inverse n'est pas revendiquee. Une sous-commande ou une
option ajoutee plus tard a `dofus_stuff/cli.py` et non documentee ne fera pas echouer cette
suite ; le contrat est « page -> parseur » plus les listes epinglees ci-dessous, jamais une
egalite d'ensembles avec la surface du parseur.

Rien n'est execute : `main()` n'est jamais appele, aucune base n'est ouverte, aucun sous-processus
et aucune socket ne sont crees, rien n'est ecrit sous `.data/` (D-15). `db clear` est *parse* pour
prouver que la page cite une commande reelle, jamais execute.

Limite de lecture mesuree : `argparse` accepte le prefixe non ambigu d'une option reelle (mesure :
`--force-sync` reste accepte apres renommage en `--force-synchronisation` dans une copie du
parseur). Un jeton cite par la page qui serait un tel prefixe passerait donc ce controle, et
exiger la forme stricte demanderait l'introspection privee d'`argparse` interdite par D-14 ; les
mutations de ce plan choisissent pour cette raison des jetons qui ne sont le prefixe d'aucune
option reelle.
"""

from __future__ import annotations

import io
import re
import shlex
from contextlib import redirect_stderr
from pathlib import Path

from dofus_stuff.cli import build_parser as build_cli_parser

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "cli.md"
SOURCE_CLI = "dofus_stuff/cli.py"

TITRE_OPTIONS_GLOBALES = "## Options globales"
TITRE_OPTIMIZE = "## optimize"
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


# ---------------------------------------------------------------------------------------------
# Exemples marques de la page (CLI-03, D-24, D-25, D-27)
#
# Un exemple est une ligne d'un bloc de code dont la balise d'ouverture est `console`
# (`BALISE_EXEMPLE` de `tests/conftest.py`, D-24) : une commande citee en prose n'en est pas un, et
# seule la projection `lignes_exemple` les rend — jamais un second scanner de blocs (D-12).
#
# Chaque exemple est decoupe par `shlex.split` puis soumis a `build_parser().parse_args` (D-25,
# D-14 : parseur public seul). La commande est *parsee*, jamais executee : ni `main()`, ni
# sous-processus, ni base ouverte, ni socket (D-15).
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
# ne fera pas rougir cette suite.

# Forme dont la page doit porter au moins un exemple : l'option globale *avant* sa sous-commande
# (`db status --offline` sort en code 2, `fetcher.py: error: unrecognized arguments: --offline`).
# Constante de module et non litteral dans le corps du test : la batterie de mutations cherche cette
# forme dans la sortie, et pytest imprime la source de l'assertion en echec — un litteral dans
# l'assertion ferait croire a la detection meme si le message ne portait pas la forme attendue.
FORME_ATTENDUE = ("--offline", "optimize")

# Options globales du parseur racine qui consomment le jeton suivant : la projection du nom de
# sous-commande saute leur valeur, sinon `--data-dir x` ferait lire `x` comme une sous-commande.
OPTIONS_GLOBALES_A_VALEUR = ("--timeout", "--data-dir")


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

    Le `SystemExit` d'`argparse` ne traverse jamais : chaque refus devient un constat nomme, et
    la sortie d'erreur du parseur est capturee pour ne pas polluer le rapport pytest.
    """
    try:
        with redirect_stderr(io.StringIO()):
            build_cli_parser().parse_args(argv)
    except SystemExit:
        return False
    return True


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


def test_sous_commandes_documentees_et_acceptees(docs_dir: Path) -> None:
    """Chaque sous-commande documentee est citee par la page et acceptee par une sonde d'argv complet."""
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

    corps_cache = section(_texte_page(docs_dir), TITRE_CACHE, PAGE)
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
            f"section « ## db » (D-20)"
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
    """Vrai si l'exemple complet est accepte par le parseur, sans jamais l'executer (D-15, D-25)."""
    try:
        with redirect_stderr(io.StringIO()):
            build_cli_parser().parse_args(_jetons(ligne)[2:])
    except SystemExit:
        return False
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


