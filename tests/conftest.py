"""Fixtures pytest pour l'interface web."""

from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path

import pytest

from dofus_stuff.catalog import Catalog
from dofus_stuff.database import Database
from dofus_stuff.web import create_app


def _sample_items() -> dict[tuple[str, int], dict]:
    return {
        ("equipment", 44): {
            "ankama_id": 44,
            "name": "Épée de Boisaille",
            "level": 7,
            "type": {"name": "Épée"},
            "description": "Épée de simple facture.",
            "effects": [{"formatted": "8 à 10 dommages Neutre"}],
            "recipe": [
                {
                    "item_ankama_id": 1001,
                    "item_subtype": "resources",
                    "quantity": 3,
                }
            ],
            "image_urls": {
                "icon": "https://api.dofusdu.de/dofus3/v1/img/item/6007-64.png",
                "sd": "https://api.dofusdu.de/dofus3/v1/img/item/6007-128.png",
            },
            "parent_set": {"id": 1, "name": "Panoplie Test"},
        },
        ("equipment", 100): {
            "ankama_id": 100,
            "name": "Cape d'Atcham",
            "level": 40,
            "type": {"name": "Cape"},
            "description": "Une cape.",
            "effects": [],
            "recipe": [],
        },
        ("equipment", 101): {
            "ankama_id": 101,
            "name": "Cape Rouge",
            "level": 10,
            "type": {"name": "Cape"},
        },
        ("resources", 1001): {
            "ankama_id": 1001,
            "name": "Bois de Frêne",
            "level": 1,
            "type": {"name": "Bois"},
        },
        ("sets", 1): {
            "ankama_id": 1,
            "name": "Panoplie Test",
            "level": 20,
            "items": 3,
            "contains_cosmetics": False,
            "contains_cosmetics_only": False,
            "equipment_ids": [44, 100, 101],
            "effects": {
                "1": None,
                "2": [{"formatted": "10 Force"}],
                "3": [{"formatted": "20 Force"}, {"formatted": "1 PA"}],
            },
        },
    }


@pytest.fixture
def catalog() -> Catalog:
    return Catalog(version="9.9.9.9", items=_sample_items())


@pytest.fixture
def app(catalog: Catalog, tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    # Mini base pour db status / clear
    db = Database(data_dir=data_dir)
    db.open()
    db.set_meta("game_version", "9.9.9.9")
    db.replace_kind(
        "equipment",
        [
            catalog.items[("equipment", 44)],
            catalog.items[("equipment", 100)],
            catalog.items[("equipment", 101)],
        ],
    )
    db.replace_kind("resources", [catalog.items[("resources", 1001)]])
    db.close()

    application = create_app(
        data_dir=data_dir,
        offline=True,
        catalog=catalog,
        load_catalog=False,
    )
    application.config["TESTING"] = True
    application.extensions["web_config"]["data_dir"] = data_dir
    yield application
    catalog.close()


@pytest.fixture
def client(app):
    return app.test_client()


def _normalize(text: str) -> str:
    """Normalise un libellé pour comparaison (D-11) : entités HTML, accents, casse, espaces."""
    text = html.unescape(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().lower()


@pytest.fixture(scope="session")
def docs_dir() -> Path:
    """Racine du dossier docs/ du dépôt, indépendante du répertoire courant."""
    return Path(__file__).resolve().parents[1] / "docs"


@pytest.fixture(scope="session")
def normalize():
    """Expose _normalize aux modules de test sans import inter-modules."""
    return _normalize


# Scanner de blocs de code et helpers de section : un seul exemplaire, partage par fixtures (D-12).
# Un helper duplique finit par diverger (lecon WR-04) : ces fonctions ne sont donc jamais
# recopiees dans un module de test, elles y sont exposees comme l'est deja la normalisation.

TITRE_H2 = re.compile(r"^##\s+(?P<titre>.+?)\s*$", re.MULTILINE)
# Trois accents graves, suivis d'une balise alphanumerique optionnelle (tirets et soulignes admis),
# puis la fin de la ligne : plus strict que l'ancien motif de la phase 1, qui absorbait comme une
# balise toute ligne commencant par trois accents graves meme suivie de texte.
DELIMITEUR_BLOC = re.compile(r"^\s*```(?P<balise>[A-Za-z0-9_-]*)\s*$")

# Balise d'ouverture qui marque un bloc d'exemples de ligne de commande (D-24) : seules les lignes
# d'un bloc portant cette balise sont des exemples a recopier, jamais une commande citee en prose.
BALISE_EXEMPLE = "console"


def _blocs_de_code(texte: str) -> list[tuple[str, list[str]]]:
    """Blocs de code Markdown : (balise d'ouverture, lignes), dans l'ordre du fichier.

    La balise est conservee (elle vaut "" pour une cloture nue) : c'est ce qui permettra de
    distinguer les blocs marques des autres sans ajouter un second scanner (plan 02-03).
    """
    blocs: list[tuple[str, list[str]]] = []
    balise, lignes, dans_bloc = "", [], False
    for ligne in texte.splitlines():
        trouve = DELIMITEUR_BLOC.match(ligne)
        if trouve:
            if dans_bloc:
                blocs.append((balise, lignes))
            else:
                balise, lignes = trouve.group("balise"), []
            dans_bloc = not dans_bloc
            continue
        if dans_bloc:
            lignes.append(ligne)
    return blocs


def _lignes_de_code(texte: str) -> list[str]:
    """Lignes de tous les blocs de code, toutes balises confondues (comportement de la phase 1)."""
    return [ligne for _, lignes in _blocs_de_code(texte) for ligne in lignes]


def _lignes_exemple(texte: str) -> list[str]:
    """Lignes des seuls blocs de code dont la balise d'ouverture est `BALISE_EXEMPLE` (D-24).

    Projection marquee du scanner unique (D-12) : `_blocs_de_code` conserve deja la balise, cette
    vue ne fait que la filtrer, elle ne rescannne rien. Les bords sont rognes et les lignes vides
    ecartees, pour qu'une ligne blanche d'un bloc ne devienne pas un `argv` vide sonde sur le
    parseur. Une commande citee en prose n'est jamais un exemple (D-24).
    """
    return [
        ligne.strip()
        for balise, lignes in _blocs_de_code(texte)
        if balise == BALISE_EXEMPLE
        for ligne in lignes
        if ligne.strip()
    ]


def _sections(texte: str) -> list[tuple[str | None, str]]:
    """Couples (titre de niveau 2, corps) des sections, dans l'ordre du fichier.

    L'entete qui precede le premier titre de niveau 2 est la premiere section, de titre None :
    une regle portant sur « chaque section » couvre donc aussi l'entete de la page.
    """
    titres = list(TITRE_H2.finditer(texte))
    sections: list[tuple[str | None, str]] = [
        (None, texte[: titres[0].start()] if titres else texte)
    ]
    for index, trouve in enumerate(titres):
        fin = titres[index + 1].start() if index + 1 < len(titres) else len(texte)
        sections.append((trouve.group("titre"), texte[trouve.end() : fin]))
    return sections


def _section(texte: str, titre: str, page: str) -> str:
    """Corps d'une section de niveau 2, du titre jusqu'au titre de niveau 2 suivant.

    `page` est obligatoire et sans valeur par defaut (D-13, D-31) : le helper partage ne peut
    plus lire la constante de page du module appelant, et un appel sans page leve `TypeError`
    des l'execution au lieu de perdre silencieusement le nom de la page dans le message.
    """
    attendu = titre.strip().lstrip("#").strip()
    for titre_trouve, corps in _sections(texte):
        if titre_trouve is not None and titre_trouve.strip() == attendu:
            return corps
    raise AssertionError(
        f"{page} : section « {titre} » introuvable ; attendu un titre de niveau 2 "
        f"« ## {attendu} » dans la page ({page})"
    )


@pytest.fixture(scope="session")
def lignes_de_code():
    """Expose _lignes_de_code aux modules de test sans import inter-modules."""
    return _lignes_de_code


@pytest.fixture(scope="session")
def lignes_exemple():
    """Expose _lignes_exemple aux modules de test, comme les autres helpers (D-12).

    La fixture rend le *helper*, jamais les lignes d'une page : chaque test appelle
    `lignes_exemple(texte_de_la_page)`. Rendre directement des lignes obligerait la fixture a
    connaitre la page de l'appelant, et iterer la fixture elle-meme leve
    `TypeError: 'function' object is not iterable` — contrat ecrit ici pour ne pas etre redecouvert.
    """
    return _lignes_exemple


@pytest.fixture(scope="session")
def sections():
    """Expose _sections aux modules de test sans import inter-modules."""
    return _sections


@pytest.fixture(scope="session")
def section():
    """Expose _section aux modules de test, sans pre-lier de page.

    Chaque appel passe sa propre page (D-13) : un pre-lien imposerait la page d'un module aux
    autres, et un oubli de page serait alors invisible au lieu de lever des l'execution.
    """
    return _section
