"""Catalogue Dofus chargé en mémoire depuis la base locale."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dofus_stuff.database import DEFAULT_DATA_DIR, Database
from dofus_stuff.sync import ensure_up_to_date

SUBTYPE_TO_KIND = {
    "resources": "resources",
    "equipment": "equipment",
    "weapons": "equipment",
    "consumables": "consumables",
    "quest": "quest",
    "cosmetics": "cosmetics",
    "mounts": "mounts",
    "sets": "sets",
}


@dataclass
class Catalog:
    """Copie en mémoire de toute la DB locale."""

    version: str | None
    items: dict[tuple[str, int], dict[str, Any]] = field(default_factory=dict)
    _db: Database | None = field(default=None, repr=False)

    @classmethod
    def load(
        cls,
        data_dir: Path | None = None,
        *,
        force_sync: bool = False,
        offline: bool = False,
        timeout: int | None = None,
        quiet: bool = False,
        skip_sync: bool = False,
    ) -> Catalog:
        db = Database(data_dir=data_dir or DEFAULT_DATA_DIR)
        db.open()
        if not skip_sync:
            ensure_up_to_date(
                db,
                force=force_sync,
                offline=offline,
                timeout=timeout,
                quiet=quiet,
            )
        items: dict[tuple[str, int], dict[str, Any]] = {}
        for kind, ankama_id, payload in db.iter_items():
            items[(kind, ankama_id)] = payload
        version = db.game_version()
        # Fermer la connexion : le catalogue est autonome en mémoire
        # (évite les erreurs check_same_thread sous Flask multi-thread).
        db.close()
        return cls(version=version, items=items, _db=None)

    def close(self) -> None:
        if self._db is not None:
            self._db.close()
            self._db = None

    @property
    def db(self) -> Database | None:
        return self._db

    def get(self, kind: str, ankama_id: int) -> dict[str, Any] | None:
        return self.items.get((kind, ankama_id))

    def get_equipment(self, ankama_id: int) -> dict[str, Any]:
        item = self.get("equipment", ankama_id)
        if item is None:
            raise KeyError(f"Équipement introuvable : #{ankama_id}")
        return item

    def get_item_by_subtype(self, ankama_id: int, subtype: str) -> dict[str, Any]:
        kind = SUBTYPE_TO_KIND.get(subtype, subtype)
        item = self.get(kind, ankama_id)
        if item is None:
            raise KeyError(f"Item introuvable : {kind} #{ankama_id}")
        return item

    def resolve_recipe_ingredient_name(
        self,
        ingredient: dict[str, Any],
        *,
        name_cache: dict[tuple[str, int], str] | None = None,
    ) -> str:
        ankama_id = ingredient.get("item_ankama_id")
        subtype = ingredient.get("item_subtype") or "resources"
        if not isinstance(ankama_id, int):
            return f"#{ankama_id}"

        cache_key = (str(subtype), ankama_id)
        if name_cache is not None and cache_key in name_cache:
            return name_cache[cache_key]

        try:
            item = self.get_item_by_subtype(ankama_id, str(subtype))
            name = item.get("name")
            resolved = name if isinstance(name, str) and name else f"#{ankama_id}"
        except KeyError:
            resolved = f"#{ankama_id}"

        if name_cache is not None:
            name_cache[cache_key] = resolved
        return resolved

    def search_items(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Recherche locale par sous-chaîne dans le nom (sensible à la casse)."""
        if not query:
            return []
        results: list[dict[str, Any]] = []
        kind_order = (
            "equipment",
            "resources",
            "consumables",
            "cosmetics",
            "quest",
            "mounts",
            "sets",
        )
        for kind in kind_order:
            for (item_kind, _), item in self.items.items():
                if item_kind != kind:
                    continue
                name = item.get("name")
                if isinstance(name, str) and query in name:
                    results.append(item)
                    if len(results) >= limit:
                        return results
        return results

    def list_equipment_page(self, page: int = 1, page_size: int = 50) -> dict[str, Any]:
        equipment = [
            item
            for (kind, _), item in sorted(
                self.items.items(),
                key=lambda kv: kv[0][1],
            )
            if kind == "equipment"
        ]
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 1
        start = (page - 1) * page_size
        end = start + page_size
        slice_items = equipment[start:end]
        total_pages = max(1, (len(equipment) + page_size - 1) // page_size)
        links: dict[str, str | None] = {
            "first": f"page={1}",
            "prev": f"page={page - 1}" if page > 1 else None,
            "next": f"page={page + 1}" if page < total_pages else None,
            "last": f"page={total_pages}",
        }
        return {"items": slice_items, "_links": links, "total": len(equipment)}


def format_item_summary(
    item: dict[str, Any],
    *,
    detailed: bool = False,
    catalog: Catalog | None = None,
) -> str:
    lines = [
        f"ID {item.get('ankama_id')} — {item.get('name', '?')}",
        f"  Niveau : {item.get('level', '?')}",
    ]

    item_type = item.get("type")
    if isinstance(item_type, dict):
        lines.append(f"  Type : {item_type.get('name', '?')}")

    if detailed:
        description = item.get("description")
        if description:
            lines.append(f"  Description : {description}")

        effects = item.get("effects")
        if isinstance(effects, list) and effects:
            lines.append("  Effets :")
            for effect in effects:
                if isinstance(effect, dict):
                    formatted = effect.get("formatted")
                    if formatted:
                        lines.append(f"    - {formatted}")

        recipe = item.get("recipe")
        if isinstance(recipe, list) and recipe:
            lines.append("  Recette :")
            name_cache: dict[tuple[str, int], str] = {}
            for ingredient in recipe:
                if isinstance(ingredient, dict):
                    if catalog is not None:
                        name = catalog.resolve_recipe_ingredient_name(
                            ingredient,
                            name_cache=name_cache,
                        )
                    else:
                        ankama_id = ingredient.get("item_ankama_id")
                        name = f"#{ankama_id}"
                    lines.append(f"    - x{ingredient.get('quantity', '?')} {name}")

    return "\n".join(lines)
