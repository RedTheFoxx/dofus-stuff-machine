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
