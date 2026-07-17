"""Application Flask — interface terminal rétro stuff-machine."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from flask import Flask

from dofus_stuff.catalog import Catalog
from dofus_stuff.database import DEFAULT_DATA_DIR


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def create_app(
    *,
    data_dir: Path | None = None,
    offline: bool | None = None,
    timeout: int | None = None,
    catalog: Catalog | None = None,
    load_catalog: bool = True,
) -> Flask:
    """
    Factory Flask.

    Si `catalog` est fourni (tests), il est utilisé tel quel.
    Sinon le catalogue est chargé depuis `data_dir` (offline par défaut).
    """
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.secret_key = os.environ.get("DOFUS_SECRET_KEY", "stuff-machine-dev-secret")

    resolved_data_dir = Path(
        data_dir
        if data_dir is not None
        else os.environ.get("DOFUS_DATA_DIR", DEFAULT_DATA_DIR)
    )
    resolved_offline = (
        offline if offline is not None else _env_bool("DOFUS_OFFLINE", True)
    )
    resolved_timeout = timeout
    if resolved_timeout is None:
        env_timeout = os.environ.get("DOFUS_TIMEOUT")
        resolved_timeout = int(env_timeout) if env_timeout else None

    app.config["DATA_DIR"] = resolved_data_dir
    app.config["OFFLINE"] = resolved_offline
    app.config["TIMEOUT"] = resolved_timeout

    app.extensions["catalog"] = catalog
    app.extensions["web_config"] = {
        "data_dir": resolved_data_dir,
        "offline": resolved_offline,
        "timeout": resolved_timeout,
    }

    if catalog is None and load_catalog:
        reload_catalog(app)

    from dofus_stuff.web.routes import bp

    app.register_blueprint(bp)

    @app.teardown_appcontext
    def _close_catalog(_exc: BaseException | None) -> None:
        # Connexion DB gardée ouverte pour la durée de vie du process.
        pass

    return app


def get_catalog(app: Flask | None = None) -> Catalog:
    from flask import current_app

    target = app or current_app
    catalog = target.extensions.get("catalog")
    if catalog is None:
        raise RuntimeError("Catalogue non initialisé")
    return catalog


def reload_catalog(
    app: Flask,
    *,
    force_sync: bool = False,
    skip_sync: bool | None = None,
) -> Catalog:
    """Ferme l'ancien catalogue et en charge un nouveau."""
    old: Catalog | None = app.extensions.get("catalog")
    if old is not None:
        try:
            old.close()
        except Exception:
            # Connexion SQLite éventuellement créée dans un autre thread.
            pass
        app.extensions["catalog"] = None

    cfg: dict[str, Any] = app.extensions["web_config"]
    if skip_sync is None:
        skip_sync = bool(cfg["offline"]) and not force_sync
    offline = bool(cfg["offline"]) and not force_sync
    catalog = Catalog.load(
        data_dir=Path(cfg["data_dir"]),
        force_sync=force_sync,
        offline=False if force_sync else offline,
        timeout=cfg.get("timeout"),
        quiet=True,
        skip_sync=skip_sync,
    )
    app.extensions["catalog"] = catalog
    return catalog


def set_catalog(app: Flask, catalog: Catalog) -> None:
    old: Catalog | None = app.extensions.get("catalog")
    if old is not None and old is not catalog:
        old.close()
    app.extensions["catalog"] = catalog
