"""Représentation et évaluation d'un stuff (items + bonus de panoplie)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from dofus_stuff.model.character import CharacterProfile
from dofus_stuff.model.conditions import item_conditions_satisfied
from dofus_stuff.model.slots import SLOT_INSTANCES, slot_for_equipment, slot_instance_kind
from dofus_stuff.model.stats import JetMode, Stats, effects_to_stats, weighted_score


@dataclass
class Build:
    """Association slot_instance → équipement (payload brut)."""

    slots: dict[str, dict[str, Any]] = field(default_factory=dict)

    def equipped_items(self) -> list[dict[str, Any]]:
        return list(self.slots.values())

    def copy(self) -> Build:
        return Build(slots=dict(self.slots))

    def ankama_ids(self) -> set[int]:
        ids: set[int] = set()
        for item in self.slots.values():
            aid = item.get("ankama_id")
            if isinstance(aid, int):
                ids.add(aid)
        return ids


@dataclass
class SetBonusApplied:
    set_id: int
    set_name: str
    pieces: int
    tier: int
    stats: Stats


@dataclass
class BuildEvaluation:
    total_stats: Stats
    item_stats: Stats
    set_stats: Stats
    base_stats: Stats
    score: float
    set_bonuses: list[SetBonusApplied]
    valid: bool
    invalid_items: list[int] = field(default_factory=list)

    @property
    def set_bonus_count(self) -> int:
        """Nombre de panoplies actives (≥ 2 pièces) — pour conditions trophées."""
        return sum(1 for bonus in self.set_bonuses if bonus.pieces >= 2)


def _set_id_of(item: Mapping[str, Any]) -> int | None:
    parent = item.get("parent_set")
    if isinstance(parent, dict):
        set_id = parent.get("id")
        if isinstance(set_id, int):
            return set_id
    return None


def _highest_set_tier(effects: Mapping[str, Any] | None, piece_count: int) -> int | None:
    if not effects or piece_count < 2:
        return None
    best: int | None = None
    for key, value in effects.items():
        if value is None:
            continue
        try:
            tier = int(key)
        except (TypeError, ValueError):
            continue
        if tier <= piece_count and (best is None or tier > best):
            best = tier
    return best


def collect_set_bonuses(
    items: list[Mapping[str, Any]],
    sets_by_id: Mapping[int, Mapping[str, Any]],
    *,
    mode: JetMode = "average",
) -> list[SetBonusApplied]:
    counts: dict[int, list[Mapping[str, Any]]] = {}
    for item in items:
        set_id = _set_id_of(item)
        if set_id is None:
            continue
        counts.setdefault(set_id, []).append(item)

    bonuses: list[SetBonusApplied] = []
    for set_id, members in counts.items():
        piece_count = len(members)
        set_payload = sets_by_id.get(set_id)
        if set_payload is None:
            continue
        effects_map = set_payload.get("effects")
        if not isinstance(effects_map, dict):
            continue
        tier = _highest_set_tier(effects_map, piece_count)
        if tier is None:
            continue
        tier_effects = effects_map.get(str(tier))
        stats = effects_to_stats(tier_effects if isinstance(tier_effects, list) else None, mode=mode)
        bonuses.append(
            SetBonusApplied(
                set_id=set_id,
                set_name=str(set_payload.get("name") or f"Set #{set_id}"),
                pieces=piece_count,
                tier=tier,
                stats=stats,
            )
        )
    return bonuses


def evaluate_build(
    build: Build,
    profile: CharacterProfile,
    *,
    sets_by_id: Mapping[int, Mapping[str, Any]] | None = None,
    check_conditions: bool = True,
) -> BuildEvaluation:
    """Agrège base + items + sets et optionnellement valide les conditions."""
    sets_by_id = sets_by_id or {}
    mode = profile.jet_mode
    base = profile.stats_without_equipment()
    item_stats = Stats()
    for item in build.equipped_items():
        item_stats.add_inplace(effects_to_stats(item.get("effects"), mode=mode))

    set_bonuses = collect_set_bonuses(build.equipped_items(), sets_by_id, mode=mode)
    set_stats = Stats()
    for bonus in set_bonuses:
        set_stats.add_inplace(bonus.stats)

    total = base + item_stats + set_stats
    score = weighted_score(total, profile.objective.weights)

    invalid: list[int] = []
    valid = True
    if check_conditions:
        set_bonus_count = sum(1 for b in set_bonuses if b.pieces >= 2)
        for item in build.equipped_items():
            ok = item_conditions_satisfied(
                item,
                character_level=profile.level,
                stats=total,
                set_bonus_count=set_bonus_count,
            )
            if not ok:
                valid = False
                aid = item.get("ankama_id")
                if isinstance(aid, int):
                    invalid.append(aid)

    return BuildEvaluation(
        total_stats=total,
        item_stats=item_stats,
        set_stats=set_stats,
        base_stats=base,
        score=score,
        set_bonuses=set_bonuses,
        valid=valid,
        invalid_items=invalid,
    )


def validate_build_slots(build: Build) -> list[str]:
    """Vérifie cohérence slots / unicité ; renvoie la liste d'erreurs."""
    errors: list[str] = []
    seen_ids: set[int] = set()
    known_slots = set(SLOT_INSTANCES) | {"shield"}
    for slot_name, item in build.slots.items():
        if slot_name not in known_slots:
            errors.append(f"Slot inconnu : {slot_name}")
            continue
        logical = slot_for_equipment(item)
        if logical is None:
            errors.append(f"Item non équipable en stuff : {item.get('name')}")
            continue
        expected = slot_instance_kind(slot_name)
        if logical is not expected:
            errors.append(
                f"Item {item.get('name')} ({logical.value}) placé dans {slot_name}"
            )
        aid = item.get("ankama_id")
        if isinstance(aid, int):
            if aid in seen_ids:
                errors.append(f"Item dupliqué : #{aid}")
            seen_ids.add(aid)
    return errors
