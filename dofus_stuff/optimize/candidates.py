"""Préfiltre de candidats : top-K par slot + expansion panoplies."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from dofus_stuff.catalog import Catalog
from dofus_stuff.model.build import Build
from dofus_stuff.model.character import CharacterProfile
from dofus_stuff.model.slots import (
    DEFAULT_OPTIMIZE_SLOTS,
    DOFUS_INSTANCES,
    EquipmentSlot,
    instances_for_slot,
    slot_for_equipment,
)
from dofus_stuff.model.solver_spec import (
    SolverSpec,
    item_passes_type_filters,
    stuffer_score,
)
from dofus_stuff.model.stats import effects_to_stats, weighted_score

_ELEMENTAL_STATS = frozenset(
    {"Intelligence", "Force", "Chance", "Agilité", "Sagesse"}
)

# Familiers / montiliers / montures ont des caracs plates élevées légitimes.
_PET_SLOTS = frozenset({EquipmentSlot.PET})


@dataclass
class ScoredItem:
    item: dict[str, Any]
    slot: EquipmentSlot
    local_score: float


@dataclass
class CandidatePool:
    """Candidats par instance de slot + index sets."""

    by_slot: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    sets_by_id: dict[int, dict[str, Any]] = field(default_factory=dict)
    scored: list[ScoredItem] = field(default_factory=list)
    upper_bound_items: float = 0.0
    upper_bound_sets: float = 0.0
    forced_build: Build = field(default_factory=Build)

    @property
    def upper_bound_equipment(self) -> float:
        return self.upper_bound_items + self.upper_bound_sets


def _is_plausible_equipment(item: Mapping[str, Any]) -> bool:
    """Écarte les objets MJ / aberrants (ex. Annobusé 300 caracs niv. 1)."""
    level = int(item.get("level") or 0)
    name = str(item.get("name") or "")
    if "(MJ)" in name or "Maître Jarbo" in name:
        return False
    slot = slot_for_equipment(item)
    if slot in _PET_SLOTS:
        return True
    stats = effects_to_stats(item.get("effects"), mode="max")
    for stat_name in _ELEMENTAL_STATS:
        value = stats.get(stat_name, 0.0)
        if value <= 0:
            continue
        ceiling = max(100.0, 2.0 * level + 20.0)
        if value > ceiling:
            return False
    return True


def _item_objective_score(item: Mapping[str, Any], profile: CharacterProfile) -> float:
    stats = effects_to_stats(item.get("effects"), mode=profile.jet_mode)
    if profile.solver_spec is not None:
        # Score local approximatif : contribution de l'item seul vs base nulle
        return stuffer_score(stats, profile.solver_spec)
    return weighted_score(stats, profile.objective.weights)


def _set_tier_score(
    set_payload: Mapping[str, Any],
    tier: int,
    profile: CharacterProfile,
) -> float:
    effects_map = set_payload.get("effects")
    if not isinstance(effects_map, dict):
        return 0.0
    tier_effects = effects_map.get(str(tier))
    if not isinstance(tier_effects, list):
        return 0.0
    stats = effects_to_stats(tier_effects, mode=profile.jet_mode)
    if profile.solver_spec is not None:
        return stuffer_score(stats, profile.solver_spec)
    return weighted_score(stats, profile.objective.weights)


def _optimistic_set_upper_bound(
    candidate_items: list[dict[str, Any]],
    sets_by_id: Mapping[int, Mapping[str, Any]],
    profile: CharacterProfile,
) -> float:
    """Borne lâche : meilleurs bonus de set parmi les sets touchés."""
    best_by_set: dict[int, float] = {}
    touched: set[int] = set()
    for item in candidate_items:
        parent = item.get("parent_set")
        if isinstance(parent, dict) and isinstance(parent.get("id"), int):
            touched.add(parent["id"])

    for set_id in touched:
        set_payload = sets_by_id.get(set_id)
        if set_payload is None:
            continue
        effects_map = set_payload.get("effects")
        if not isinstance(effects_map, dict):
            continue
        best = 0.0
        for key, value in effects_map.items():
            if value is None:
                continue
            try:
                tier = int(key)
            except (TypeError, ValueError):
                continue
            best = max(best, _set_tier_score(set_payload, tier, profile))
        best_by_set[set_id] = best

    top = sorted(best_by_set.values(), reverse=True)[:4]
    return float(sum(top))


def build_sets_index(catalog: Catalog) -> dict[int, dict[str, Any]]:
    sets_by_id: dict[int, dict[str, Any]] = {}
    for (kind, ankama_id), payload in catalog.items.items():
        if kind != "sets":
            continue
        sets_by_id[ankama_id] = payload
    return sets_by_id


def _equipment_index_by_set(
    catalog: Catalog,
) -> dict[int, list[dict[str, Any]]]:
    by_set: dict[int, list[dict[str, Any]]] = {}
    for (kind, _), payload in catalog.items.items():
        if kind != "equipment":
            continue
        parent = payload.get("parent_set")
        if isinstance(parent, dict) and isinstance(parent.get("id"), int):
            by_set.setdefault(parent["id"], []).append(payload)
    return by_set


def _shared_pool_upper_bound(
    pool: list[dict[str, Any]],
    profile: CharacterProfile,
    cardinality: int,
) -> float:
    """Somme des `cardinality` meilleurs scores distincts d'un pool partagé."""
    if cardinality <= 0 or not pool:
        return 0.0
    scores = sorted(
        (_item_objective_score(it, profile) for it in pool),
        reverse=True,
    )
    return float(sum(scores[:cardinality]))


def _resolve_forced_build(
    catalog: Catalog,
    profile: CharacterProfile,
    spec: SolverSpec,
    slot_instances: tuple[str, ...],
) -> Build:
    """Place les items forcés dans leurs slots ; lève ValueError si conflit."""
    build = Build()
    for aid in sorted(spec.forced_ids):
        item = catalog.get("equipment", aid)
        if item is None:
            raise ValueError(f"Item forcé introuvable : #{aid}")
        if int(item.get("level") or 0) > profile.level:
            raise ValueError(f"Item forcé #{aid} trop haut niveau")
        if not item_passes_type_filters(item, spec.type_filters):
            raise ValueError(f"Item forcé #{aid} exclu par filtres de type")
        if aid in spec.blacklist_ids:
            raise ValueError(f"Item forcé #{aid} aussi en liste noire")
        slot = slot_for_equipment(item)
        if slot is None:
            raise ValueError(f"Item forcé #{aid} hors périmètre stuff")
        placed = False
        for instance in instances_for_slot(slot):
            if instance not in slot_instances:
                continue
            if instance in build.slots:
                continue
            build.slots[instance] = item
            placed = True
            break
        if not placed:
            raise ValueError(f"Aucun slot libre pour l'item forcé #{aid}")
    return build


def build_candidate_pool(
    catalog: Catalog,
    profile: CharacterProfile,
    *,
    top_k: int = 30,
    set_expand_m: int = 6,
    slot_instances: tuple[str, ...] | None = None,
    spec: SolverSpec | None = None,
) -> CandidatePool:
    """Construit le pool de candidats top-K + expansion des pièces de set."""
    spec = spec or profile.solver_spec
    if slot_instances is None:
        slot_instances = spec.slot_instances() if spec else DEFAULT_OPTIMIZE_SLOTS

    blacklist = spec.blacklist_ids if spec else frozenset()
    forced_ids = spec.forced_ids if spec else frozenset()
    type_filters = spec.type_filters if spec else None

    sets_by_id = build_sets_index(catalog)
    by_set = _equipment_index_by_set(catalog)

    forced_build = Build()
    if spec and forced_ids:
        forced_build = _resolve_forced_build(catalog, profile, spec, slot_instances)

    scored_by_logical: dict[EquipmentSlot, list[ScoredItem]] = {
        slot: [] for slot in EquipmentSlot
    }

    for (kind, _), payload in catalog.items.items():
        if kind != "equipment":
            continue
        aid = payload.get("ankama_id")
        if isinstance(aid, int) and aid in blacklist:
            continue
        level = int(payload.get("level") or 0)
        if level > profile.level:
            continue
        if not _is_plausible_equipment(payload):
            continue
        if type_filters is not None and not item_passes_type_filters(payload, type_filters):
            continue
        slot = slot_for_equipment(payload)
        if slot is None:
            continue
        if slot not in scored_by_logical:
            continue
        # Skip slots not requested
        if not any(inst in slot_instances for inst in instances_for_slot(slot)):
            continue
        local = _item_objective_score(payload, profile)
        scored_by_logical[slot].append(ScoredItem(item=payload, slot=slot, local_score=local))

    for slot, entries in scored_by_logical.items():
        entries.sort(key=lambda s: s.local_score, reverse=True)

    selected: dict[int, dict[str, Any]] = {}
    top_scored: list[ScoredItem] = []
    for slot, entries in scored_by_logical.items():
        for entry in entries[:top_k]:
            aid = entry.item.get("ankama_id")
            if isinstance(aid, int):
                selected[aid] = entry.item
                top_scored.append(entry)

    # Toujours inclure les items forcés dans le pool
    for item in forced_build.equipped_items():
        aid = item.get("ankama_id")
        if isinstance(aid, int):
            selected[aid] = item

    set_ids_touched: set[int] = set()
    for item in selected.values():
        parent = item.get("parent_set")
        if isinstance(parent, dict) and isinstance(parent.get("id"), int):
            set_ids_touched.add(parent["id"])

    for set_id in set_ids_touched:
        siblings = by_set.get(set_id, [])
        scored_siblings: list[tuple[float, dict[str, Any]]] = []
        for sibling in siblings:
            sid = sibling.get("ankama_id")
            if isinstance(sid, int) and sid in blacklist:
                continue
            if int(sibling.get("level") or 0) > profile.level:
                continue
            if not _is_plausible_equipment(sibling):
                continue
            if type_filters is not None and not item_passes_type_filters(sibling, type_filters):
                continue
            slot = slot_for_equipment(sibling)
            if slot is None:
                continue
            scored_siblings.append((_item_objective_score(sibling, profile), sibling))
        scored_siblings.sort(key=lambda t: t[0], reverse=True)
        for _, sibling in scored_siblings[:set_expand_m]:
            aid = sibling.get("ankama_id")
            if isinstance(aid, int):
                selected[aid] = sibling

    by_slot: dict[str, list[dict[str, Any]]] = {s: [] for s in slot_instances}
    for item in selected.values():
        slot = slot_for_equipment(item)
        if slot is None:
            continue
        for instance in instances_for_slot(slot):
            if instance in by_slot:
                by_slot[instance].append(item)

    # Retirer des pools libres les slots déjà forcés (sauf l'item forcé lui-même)
    forced_ids_set = forced_build.ankama_ids()
    for slot, forced_item in forced_build.slots.items():
        if slot not in by_slot:
            continue
        forced_aid = forced_item.get("ankama_id")
        by_slot[slot] = [
            it
            for it in by_slot[slot]
            if it.get("ankama_id") == forced_aid
            or (
                isinstance(it.get("ankama_id"), int)
                and it["ankama_id"] not in forced_ids_set
            )
        ]
        # Garantir que l'item forcé est dans la liste
        if forced_aid and not any(it.get("ankama_id") == forced_aid for it in by_slot[slot]):
            by_slot[slot].insert(0, forced_item)

    for instance, items in by_slot.items():
        items.sort(key=lambda it: _item_objective_score(it, profile), reverse=True)

    ub_items = 0.0
    accounted: set[str] = set()

    ring_pool = by_slot.get("ring_a") or by_slot.get("ring_b") or []
    ring_card = sum(1 for s in ("ring_a", "ring_b") if s in by_slot)
    if ring_card:
        ub_items += _shared_pool_upper_bound(ring_pool, profile, ring_card)
        accounted.update({"ring_a", "ring_b"})

    dofus_present = [s for s in DOFUS_INSTANCES if s in by_slot]
    if dofus_present:
        dofus_pool = by_slot.get(dofus_present[0]) or []
        ub_items += _shared_pool_upper_bound(dofus_pool, profile, len(dofus_present))
        accounted.update(dofus_present)

    for instance in slot_instances:
        if instance in accounted:
            continue
        pool = by_slot.get(instance) or []
        if pool:
            ub_items += _item_objective_score(pool[0], profile)

    ub_sets = _optimistic_set_upper_bound(list(selected.values()), sets_by_id, profile)

    return CandidatePool(
        by_slot=by_slot,
        sets_by_id=sets_by_id,
        scored=top_scored,
        upper_bound_items=ub_items,
        upper_bound_sets=ub_sets,
        forced_build=forced_build,
    )


def base_objective_score(profile: CharacterProfile) -> float:
    base = profile.stats_without_equipment()
    if profile.solver_spec is not None:
        return stuffer_score(base, profile.solver_spec)
    return weighted_score(base, profile.objective.weights)
