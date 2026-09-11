"""Ancrage de la documentation utilisateur sur le code réel du produit (critère de succès 4).

Aucune introspection privée d'argparse (D-14), aucune exécution de commande, aucune base
ouverte : les contrôles passent par les parseurs publics et par la lecture des fichiers.
"""

from __future__ import annotations

import re
import shlex
from pathlib import Path

from dofus_stuff.cli import build_parser as build_cli_parser
from dofus_stuff.web.__main__ import build_parser

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "installation.md"
SOURCE_WEB = "dofus_stuff/web/__main__.py"
SOURCE_CLI = "dofus_stuff/cli.py"

# Bloc « Source de vérité » de la page d'installation (D-01, D-03).
TITRE_SOURCE = "## Source de vérité"
CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml))`")

TITRE_H2 = re.compile(r"^##\s+(?P<titre>.+?)\s*$", re.MULTILINE)
DELIMITEUR_CODE = re.compile(r"^\s*```")
ADRESSE_ECOUTE = re.compile(r"(?P<hote>(?:\d{1,3}\.){3}\d{1,3}):(?P<port>\d{1,5})")


def _sections(texte: str) -> list[tuple[str, str]]:
    """Couples (titre de niveau 2, corps) des sections de la page, dans l'ordre du fichier."""
    titres = list(TITRE_H2.finditer(texte))
    sections: list[tuple[str, str]] = []
    for index, trouve in enumerate(titres):
        fin = titres[index + 1].start() if index + 1 < len(titres) else len(texte)
        sections.append((trouve.group("titre"), texte[trouve.end() : fin]))
    return sections


def _section(texte: str, titre: str) -> str:
    """Corps d'une section de niveau 2, du titre jusqu'au titre de niveau 2 suivant."""
    attendu = titre.strip().lstrip("#").strip()
    for titre_trouve, corps in _sections(texte):
        if titre_trouve.strip() == attendu:
            return corps
    raise AssertionError(
        f"{PAGE} : section « {titre} » introuvable ; attendu un titre de niveau 2 "
        f"« ## {attendu} » dans la page ({PAGE})"
    )


def _lignes_de_code(texte: str) -> list[str]:
    """Lignes situées entre les délimiteurs de blocs de code Markdown (trois accents graves)."""
    lignes: list[str] = []
    dans_bloc = False
    for ligne in texte.splitlines():
        if DELIMITEUR_CODE.match(ligne):
            dans_bloc = not dans_bloc
            continue
        if dans_bloc:
            lignes.append(ligne)
    return lignes


def test_sources_de_verite_exist(docs_dir: Path) -> None:
    """Chaque chemin cité par le bloc « Source de vérité » de la page existe sur disque."""
    texte = (docs_dir / PAGE).read_text(encoding="utf-8")
    corps = _section(texte, TITRE_SOURCE)
    chemins = sorted(set(CHEMIN_CITE.findall(corps)))
    assert chemins, (
        f"{PAGE} : aucun chemin .py ni .toml trouvé dans la section « {TITRE_SOURCE} » ; "
        f"attendu au moins un chemin réel du code ({PAGE})"
    )
    manquants = [chemin for chemin in chemins if not (RACINE_DEPOT / chemin).exists()]
    assert not manquants, (
        f"{PAGE} : chemin(s) cité(s) comme source de vérité mais absent(s) du dépôt : "
        f"{', '.join(manquants)} ; attendu un chemin existant depuis la racine du dépôt "
        f"(section « {TITRE_SOURCE} »)"
    )


def test_cli_examples_of_installation_page_parse(docs_dir: Path) -> None:
    """Chaque commande fetcher.py des blocs de code est analysable et porte --offline."""
    texte = (docs_dir / PAGE).read_text(encoding="utf-8")
    commandes = [ligne.strip() for ligne in _lignes_de_code(texte) if "fetcher.py" in ligne]
    assert commandes, (
        f"{PAGE} : aucune commande fetcher.py dans les blocs de code de la page ; "
        f"attendu au moins le premier contact CLI ({SOURCE_CLI})"
    )
    parser = build_cli_parser()
    for commande in commandes:
        try:
            argv = shlex.split(commande)
        except ValueError:
            raise AssertionError(
                f"{PAGE} : commande « {commande} » non analysable ; attendu une commande "
                f"découpable par shlex (source : {SOURCE_CLI})"
            ) from None
        reste = argv[argv.index("fetcher.py") + 1 :]
        try:
            parser.parse_args(reste)
        except SystemExit:
            raise AssertionError(
                f"{PAGE} : commande « {commande} » refusée par le parseur réel ; "
                f"attendu une commande acceptée par {SOURCE_CLI}::build_parser().parse_args()"
            ) from None
        assert "--offline" in reste, (
            f"{PAGE} : commande « {commande} » sans drapeau hors-ligne placé avant sa "
            f"sous-commande ; attendu « --offline » sur chaque commande documentée "
            f"(source : {SOURCE_CLI})"
        )


def test_adresse_par_defaut_documentee(docs_dir: Path) -> None:
    """L'adresse citée par la page est celle que le parseur web applique par défaut."""
    args = build_parser().parse_args([])
    attendue = f"http://{args.host}:{args.port}"
    texte = (docs_dir / PAGE).read_text(encoding="utf-8")
    assert attendue in texte, (
        f"{PAGE} : adresse par défaut « {attendue} » absente de la page ; attendu l'adresse "
        f"construite depuis les défauts réels de {SOURCE_WEB}::build_parser()"
    )
    fautives = sorted(
        {f"http://{hote}:{port}" for hote, port in ADRESSE_ECOUTE.findall(texte)} - {attendue}
    )
    assert not fautives, (
        f"{PAGE} : adresse(s) d'écoute citée(s) en contradiction avec le parseur : "
        f"{', '.join(fautives)} ; attendu « {attendue} » ({SOURCE_WEB})"
    )
