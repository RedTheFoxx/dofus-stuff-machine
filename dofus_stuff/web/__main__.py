"""Point d'entrée : python -m dofus_stuff.web"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dofus_stuff.database import DEFAULT_DATA_DIR
from dofus_stuff.web import create_app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stuff-machine — interface terminal web")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(os.environ.get("DOFUS_DATA_DIR", DEFAULT_DATA_DIR)),
        help="Répertoire de la base locale",
    )
    parser.add_argument(
        "--offline",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Ne pas contacter l'API au démarrage (défaut : oui)",
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="Autoriser le contact API (équivalent --no-offline)",
    )
    parser.add_argument("--timeout", type=int, default=None, help="Timeout HTTP (s)")
    parser.add_argument("--host", default="127.0.0.1", help="Adresse d'écoute")
    parser.add_argument("--port", type=int, default=5000, help="Port HTTP")
    parser.add_argument("--debug", action="store_true", help="Mode debug Flask")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    offline = False if args.online else args.offline
    app = create_app(
        data_dir=args.data_dir,
        offline=offline,
        timeout=args.timeout,
    )
    app.run(host=args.host, port=args.port, debug=args.debug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
