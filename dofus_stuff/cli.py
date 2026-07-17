"""Interface en ligne de commande."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from dofus_stuff.api import DEFAULT_TIMEOUT
from dofus_stuff.catalog import Catalog, format_item_summary
from dofus_stuff.database import DEFAULT_DATA_DIR, Database
from dofus_stuff.optimize import format_optimize_result, optimize_stuff
from dofus_stuff.optimize.profile_input import (
    OptimizeInputError,
    needs_interactive_optimize,
    parse_optimize_request,
    prompt_optimize_interactive,
)
from dofus_stuff.sync import ensure_up_to_date


_OPTIMIZE_EPILOG = """\
exemples :
  %(prog)s --offline optimize --demo
  %(prog)s --offline optimize --level 123 --max intelligence --base-int 200 --scroll-int 100
  %(prog)s --offline optimize
      (mode interactif : questions guidées)
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="API Dofus — base locale Dofusdude")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout HTTP (s)")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help=f"Répertoire de la base locale (défaut : {DEFAULT_DATA_DIR})",
    )
    parser.add_argument(
        "--force-sync",
        action="store_true",
        help="Ignorer la fenêtre 24h et forcer une vérif / sync version",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Ne pas contacter l'API (échoue si la base locale est vide)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Afficher la version Dofus de la base locale")
    subparsers.add_parser("self-test", help="Vérifier la base locale et des objets connus")

    search_parser = subparsers.add_parser("search", help="Rechercher des objets (local)")
    search_parser.add_argument("query", help="Terme de recherche (sensible à la casse)")
    search_parser.add_argument("--limit", type=int, default=10, help="Nombre max de résultats")

    item_parser = subparsers.add_parser("item", help="Détail d'un équipement par ID Ankama")
    item_parser.add_argument("ankama_id", type=int, help="ID Ankama de l'objet")

    list_parser = subparsers.add_parser("list", help="Lister une page d'équipements")
    list_parser.add_argument("--page", type=int, default=1, help="Numéro de page")
    list_parser.add_argument("--size", type=int, default=5, help="Taille de page")

    optimize_parser = subparsers.add_parser(
        "optimize",
        help="Optimiser un stuff pour un niveau et une/des caractéristiques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_OPTIMIZE_EPILOG,
    )
    optimize_parser.add_argument("--level", type=int, help="Niveau du personnage")
    optimize_parser.add_argument(
        "--max",
        dest="max_stats",
        nargs="+",
        help="Caractéristique(s) à maximiser (ex: intelligence)",
    )
    optimize_parser.add_argument(
        "--base-int",
        type=float,
        default=0.0,
        help="Intelligence hors stuff (capital déjà converti)",
    )
    optimize_parser.add_argument("--base-vit", type=float, default=0.0)
    optimize_parser.add_argument("--base-str", type=float, default=0.0)
    optimize_parser.add_argument("--base-cha", type=float, default=0.0)
    optimize_parser.add_argument("--base-agi", type=float, default=0.0)
    optimize_parser.add_argument("--base-wis", type=float, default=0.0)
    optimize_parser.add_argument("--scroll-int", type=float, default=0.0)
    optimize_parser.add_argument("--scroll-vit", type=float, default=0.0)
    optimize_parser.add_argument("--scroll-str", type=float, default=0.0)
    optimize_parser.add_argument("--scroll-cha", type=float, default=0.0)
    optimize_parser.add_argument("--scroll-agi", type=float, default=0.0)
    optimize_parser.add_argument("--scroll-wis", type=float, default=0.0)
    optimize_parser.add_argument(
        "--jet",
        choices=("min", "average", "max"),
        default="average",
        help="Mode de jets d'objets (défaut: average)",
    )
    optimize_parser.add_argument("--top-k", type=int, default=30, help="Candidats top-K par slot")
    optimize_parser.add_argument(
        "--time-limit",
        type=float,
        default=5.0,
        help="Timeout CP-SAT en secondes",
    )
    optimize_parser.add_argument(
        "--no-cpsat",
        action="store_true",
        help="Désactiver CP-SAT (greedy + local uniquement)",
    )
    optimize_parser.add_argument(
        "--classic-only",
        action="store_true",
        help="Ignorer Dofus/Trophées, familier et prysmaradite",
    )
    optimize_parser.add_argument(
        "--demo",
        action="store_true",
        help="Profil démo niveau 123 / max INT (ignore --level/--max/bases)",
    )
    optimize_parser.add_argument(
        "--target",
        nargs="+",
        default=None,
        help="Cibles STAT=valeur (ex: intelligence=1200 pa=11)",
    )
    optimize_parser.add_argument(
        "--weight",
        nargs="+",
        default=None,
        help="Poids STAT=valeur (ex: intelligence=2 vitalite=0.5)",
    )
    optimize_parser.add_argument(
        "--ban",
        nargs="+",
        type=int,
        default=None,
        help="Ankama IDs interdits",
    )
    optimize_parser.add_argument(
        "--force",
        nargs="+",
        type=int,
        default=None,
        help="Ankama IDs obligatoires",
    )
    optimize_parser.add_argument("--seed", type=int, default=None, help="Seed RNG")
    optimize_parser.add_argument(
        "--stop-when-satisfied",
        action="store_true",
        help="Arrêter dès que les cibles sont atteintes",
    )
    optimize_parser.add_argument(
        "--auto-points",
        action="store_true",
        help="Répartir automatiquement les points de caracs",
    )
    optimize_parser.add_argument(
        "--allow-power",
        action="store_true",
        help="Autoriser la puissance à la place des caracs",
    )
    optimize_parser.add_argument(
        "--allow-damages",
        action="store_true",
        help="Autoriser les dommages à la place des dommages élémentaires",
    )
    optimize_parser.add_argument(
        "--allow-crit-damages",
        action="store_true",
        help="Autoriser les dommages critiques à la place des dommages élémentaires",
    )

    for db_name in ("db", "cache"):
        db_parser = subparsers.add_parser(
            db_name,
            help="Gérer la base locale" if db_name == "db" else argparse.SUPPRESS,
        )
        db_sub = db_parser.add_subparsers(dest="db_command", required=True)
        db_sub.add_parser("status", help="Afficher l'état de la base")
        db_sub.add_parser("stats", help=argparse.SUPPRESS)  # alias cache stats
        db_sub.add_parser("sync", help="Forcer la synchronisation complète")
        db_sub.add_parser("fill", help=argparse.SUPPRESS)  # alias cache fill
        clear_parser = db_sub.add_parser("clear", help="Vider la base locale")
        clear_parser.add_argument(
            "--all",
            action="store_true",
            help=argparse.SUPPRESS,
        )

    return parser


def _data_dir_from_args(args: argparse.Namespace) -> Path:
    return args.data_dir


def _load_catalog(args: argparse.Namespace, *, quiet: bool = False, skip_sync: bool = False) -> Catalog:
    return Catalog.load(
        data_dir=_data_dir_from_args(args),
        force_sync=args.force_sync,
        offline=args.offline,
        timeout=args.timeout,
        quiet=quiet,
        skip_sync=skip_sync,
    )


def _print_db_status(db: Database) -> None:
    stats = db.stats()
    print(f"Fichier : {stats['path']}")
    print(f"Version jeu : {stats['game_version'] or '(aucune)'}")
    last_checked = stats["last_checked_at"]
    if isinstance(last_checked, float):
        age_h = (time.time() - last_checked) / 3600
        print(f"Dernier check : il y a {age_h:.1f}h")
    else:
        print("Dernier check : (aucun)")
    print(f"Entrées : {stats['total_items']}")
    by_kind = stats["by_kind"]
    if isinstance(by_kind, dict) and by_kind:
        print("Par catégorie :")
        for kind, count in by_kind.items():
            print(f"  - {kind} : {count}")


def collect_self_test_checks(catalog: Catalog) -> list[tuple[str, bool]]:
    """Exécute les contrôles self-test et renvoie (libellé, ok)."""
    checks: list[tuple[str, bool]] = []

    checks.append((f"version locale : {catalog.version}", bool(catalog.version)))
    checks.append(("catalogue non vide", len(catalog.items) > 0))

    try:
        item = catalog.get_equipment(44)
        checks.append(("objet 44 nom", item.get("name") == "Épée de Boisaille"))
        checks.append(("objet 44 niveau", item.get("level") == 7))
        recipe = item.get("recipe")
        if isinstance(recipe, list) and recipe and isinstance(recipe[0], dict):
            name = catalog.resolve_recipe_ingredient_name(recipe[0])
            checks.append(
                (
                    "recette nom ressource",
                    name != f"#{recipe[0].get('item_ankama_id')}" and bool(name),
                )
            )
        else:
            checks.append(("recette nom ressource", False))
    except Exception as exc:
        checks.append((f"objet 44 : {exc}", False))
        return checks

    try:
        results = catalog.search_items("Atcham", limit=5)
        checks.append(("recherche Atcham", len(results) >= 1))
    except Exception as exc:
        checks.append((f"recherche : {exc}", False))
        return checks

    before = len(catalog.items)
    catalog.get_equipment(44)
    catalog.search_items("Atcham", limit=5)
    checks.append(("lecture mémoire stable", len(catalog.items) == before and before >= 1))
    return checks


def run_self_test(catalog: Catalog) -> int:
    checks = collect_self_test_checks(catalog)
    failed = 0
    for label, ok in checks:
        status = "OK" if ok else "ÉCHEC"
        print(f"[{status}] {label}")
        if not ok:
            failed += 1
    return 1 if failed else 0


def _normalize_db_command(command: str) -> str:
    aliases = {"stats": "status", "fill": "sync"}
    return aliases.get(command, command)


def _request_from_optimize_args(args: argparse.Namespace):
    if needs_interactive_optimize(args):
        return prompt_optimize_interactive(
            top_k=args.top_k,
            time_limit_s=args.time_limit,
            use_cpsat=not args.no_cpsat,
        )
    return parse_optimize_request(
        demo=bool(args.demo),
        level=args.level,
        max_stats=args.max_stats,
        base_int=args.base_int,
        base_vit=args.base_vit,
        base_str=args.base_str,
        base_cha=args.base_cha,
        base_agi=args.base_agi,
        base_wis=args.base_wis,
        scroll_int=args.scroll_int,
        scroll_vit=args.scroll_vit,
        scroll_str=args.scroll_str,
        scroll_cha=args.scroll_cha,
        scroll_agi=args.scroll_agi,
        scroll_wis=args.scroll_wis,
        jet=args.jet,
        classic_only=bool(args.classic_only),
        top_k=args.top_k,
        time_limit_s=args.time_limit,
        use_cpsat=not args.no_cpsat,
        targets=args.target,
        weights=args.weight,
        ban_ids=args.ban,
        force_ids=args.force,
        seed=args.seed,
        stop_when_satisfied=bool(args.stop_when_satisfied),
        auto_distribute_points=bool(args.auto_points),
        allow_power_for_caracs=bool(args.allow_power),
        allow_damages_for_elemental=bool(args.allow_damages),
        allow_crit_damages_for_elemental=bool(args.allow_crit_damages),
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    catalog: Catalog | None = None

    try:
        if args.command in {"db", "cache"}:
            db_command = _normalize_db_command(args.db_command)
            db = Database(data_dir=_data_dir_from_args(args))
            db.open()
            try:
                if db_command == "status":
                    _print_db_status(db)
                    return 0

                if db_command == "sync":
                    if args.offline:
                        print("Erreur : --offline incompatible avec db sync", file=sys.stderr)
                        return 1
                    ensure_up_to_date(
                        db,
                        force=True,
                        offline=False,
                        timeout=args.timeout,
                        quiet=False,
                    )
                    return 0

                if db_command == "clear":
                    deleted = db.clear()
                    print(f"Base vidée : {deleted} entrée(s) supprimée(s).")
                    return 0

                raise AssertionError(f"Sous-commande db non gérée : {args.db_command}")
            finally:
                db.close()

        # Commandes qui s'appuient sur le catalogue mémoire.
        catalog = _load_catalog(args, quiet=False)

        if args.command == "version":
            version = catalog.version
            if version is None:
                print("Erreur : aucune version en base", file=sys.stderr)
                return 1
            print(f"Version Dofus (locale) : {version}")
            return 0

        if args.command == "self-test":
            return run_self_test(catalog)

        if args.command == "search":
            results = catalog.search_items(args.query, limit=args.limit)
            if not results:
                print("Aucun résultat.")
                return 0
            for item in results:
                print(format_item_summary(item, catalog=catalog))
                print()
            return 0

        if args.command == "item":
            item = catalog.get_equipment(args.ankama_id)
            print(format_item_summary(item, detailed=True, catalog=catalog))
            return 0

        if args.command == "list":
            page_data = catalog.list_equipment_page(page=args.page, page_size=args.size)
            items = page_data.get("items", [])
            if not isinstance(items, list) or not items:
                print("Aucun objet sur cette page.")
                return 0
            for item in items:
                if isinstance(item, dict):
                    print(format_item_summary(item, catalog=catalog))
                    print()
            links = page_data.get("_links")
            if isinstance(links, dict) and links.get("next"):
                print(f"Page suivante disponible : {links['next']}")
            return 0

        if args.command == "optimize":
            try:
                req = _request_from_optimize_args(args)
            except OptimizeInputError as exc:
                print(f"Erreur : {exc}", file=sys.stderr)
                return 1
            print("Calcul en cours (CP-SAT)…", flush=True)
            result = optimize_stuff(
                catalog,
                req.profile,
                spec=req.spec,
                top_k=req.top_k,
                time_limit_s=req.time_limit_s,
                use_cpsat=req.use_cpsat,
                classic_only=req.classic_only,
            )
            print(format_optimize_result(result, req.profile))
            return 0

    except OptimizeInputError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    finally:
        if catalog is not None:
            catalog.close()

    raise AssertionError(f"Commande non gérée : {args.command}")


# Réexport utile pour tests / scripts
__all__ = ["main", "build_parser", "collect_self_test_checks", "run_self_test"]
