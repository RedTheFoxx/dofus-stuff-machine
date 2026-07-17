"""Baseline greedy set-aware + passes de swap local."""

from __future__ import annotations

import random
from typing import Any

from dofus_stuff.model.build import Build, evaluate_build
from dofus_stuff.model.character import CharacterProfile
from dofus_stuff.model.slots import DOFUS_INSTANCES, CLASSIC_SLOT_INSTANCES, is_optional_slot
from dofus_stuff.model.solver_spec import targets_satisfied
from dofus_stuff.optimize.candidates import CandidatePool


_FILL_ORDER: tuple[str, ...] = (
    *CLASSIC_SLOT_INSTANCES,
    "shield",
    *DOFUS_INSTANCES,
    "pet",
    "prysma",
)


def _delta_score(
    build: Build,
    slot: str,
    item: dict[str, Any] | None,
    profile: CharacterProfile,
    pool: CandidatePool,
    *,
    require_valid: bool = True,
) -> float:
    trial = build.copy()
    if item is None:
        trial.slots.pop(slot, None)
    else:
        trial.slots[slot] = item
        aid = item.get("ankama_id")
        if isinstance(aid, int):
            for other_slot, other in list(trial.slots.items()):
                if other_slot != slot and other.get("ankama_id") == aid:
                    del trial.slots[other_slot]
    evaluation = evaluate_build(
        trial,
        profile,
        sets_by_id=pool.sets_by_id,
        check_conditions=require_valid,
    )
    if require_valid and not evaluation.valid:
        return float("-inf")
    return evaluation.score


def greedy_build(
    pool: CandidatePool,
    profile: CharacterProfile,
    *,
    swap_passes: int = 2,
    seed: int | None = None,
) -> Build:
    """Construit un stuff glouton puis améliore par swaps locaux."""
    rng = random.Random(seed)
    build = pool.forced_build.copy() if pool.forced_build.slots else Build()
    slot_order = [s for s in _FILL_ORDER if s in pool.by_slot]
    forced_slots = set(pool.forced_build.slots)

    for slot in slot_order:
        if slot in forced_slots:
            continue
        candidates = list(pool.by_slot.get(slot) or [])
        if seed is not None:
            rng.shuffle(candidates)
            candidates.sort(
                key=lambda it: _delta_score(build, slot, it, profile, pool),
                reverse=True,
            )
        best_item: dict[str, Any] | None = None
        best_score = float("-inf")
        if is_optional_slot(slot):
            empty_score = _delta_score(build, slot, None, profile, pool)
            if empty_score > best_score:
                best_score = empty_score
                best_item = None

        occupied_ids = build.ankama_ids()
        for item in candidates:
            aid = item.get("ankama_id")
            if isinstance(aid, int) and aid in occupied_ids:
                continue
            score = _delta_score(build, slot, item, profile, pool)
            if score > best_score:
                best_score = score
                best_item = item
        if best_item is not None:
            build.slots[slot] = best_item
        elif is_optional_slot(slot):
            build.slots.pop(slot, None)

        if (
            profile.solver_spec is not None
            and profile.solver_spec.stop_when_satisfied
        ):
            ev = evaluate_build(
                build, profile, sets_by_id=pool.sets_by_id, check_conditions=True
            )
            if ev.valid and targets_satisfied(ev.total_stats, profile.solver_spec):
                return build

    for _ in range(swap_passes):
        improved = False
        for slot in slot_order:
            if slot in forced_slots:
                continue
            current_eval = evaluate_build(
                build,
                profile,
                sets_by_id=pool.sets_by_id,
                check_conditions=True,
            )
            best_item: dict[str, Any] | None = build.slots.get(slot)
            best_score = current_eval.score if current_eval.valid else float("-inf")
            occupied = {
                other.get("ankama_id")
                for other_slot, other in build.slots.items()
                if other_slot != slot and isinstance(other.get("ankama_id"), int)
            }
            if is_optional_slot(slot):
                empty_score = _delta_score(build, slot, None, profile, pool)
                if empty_score > best_score + 1e-9:
                    best_score = empty_score
                    best_item = None
                    improved = True

            for item in pool.by_slot.get(slot) or []:
                aid = item.get("ankama_id")
                if isinstance(aid, int) and aid in occupied:
                    continue
                current = build.slots.get(slot)
                if current is not None and item.get("ankama_id") == current.get("ankama_id"):
                    continue
                score = _delta_score(build, slot, item, profile, pool)
                if score > best_score + 1e-9:
                    best_score = score
                    best_item = item
                    improved = True
            if best_item is not None:
                build.slots[slot] = best_item
            elif is_optional_slot(slot):
                build.slots.pop(slot, None)
        if not improved:
            break
        if (
            profile.solver_spec is not None
            and profile.solver_spec.stop_when_satisfied
        ):
            ev = evaluate_build(
                build, profile, sets_by_id=pool.sets_by_id, check_conditions=True
            )
            if ev.valid and targets_satisfied(ev.total_stats, profile.solver_spec):
                return build

    return build


def local_search(
    build: Build,
    pool: CandidatePool,
    profile: CharacterProfile,
    *,
    max_iterations: int = 400,
    seed: int | None = None,
) -> Build:
    """Recherche locale : remplace un item si le score augmente (build valide)."""
    rng = random.Random(seed)
    current = build.copy()
    current_eval = evaluate_build(
        current,
        profile,
        sets_by_id=pool.sets_by_id,
        check_conditions=True,
    )
    current_score = current_eval.score if current_eval.valid else float("-inf")
    forced_slots = set(pool.forced_build.slots)

    if (
        profile.solver_spec is not None
        and profile.solver_spec.stop_when_satisfied
        and current_eval.valid
        and targets_satisfied(current_eval.total_stats, profile.solver_spec)
    ):
        return current

    iterations = 0
    slot_order = [s for s in _FILL_ORDER if s in pool.by_slot and s not in forced_slots]
    if seed is not None:
        rng.shuffle(slot_order)

    while iterations < max_iterations:
        iterations += 1
        improved = False
        for slot in slot_order:
            occupied = {
                other.get("ankama_id")
                for other_slot, other in current.slots.items()
                if other_slot != slot and isinstance(other.get("ankama_id"), int)
            }
            if is_optional_slot(slot):
                score = _delta_score(current, slot, None, profile, pool)
                if score > current_score + 1e-9:
                    current.slots.pop(slot, None)
                    current_score = score
                    improved = True
                    break

            candidates = list(pool.by_slot.get(slot) or [])
            if seed is not None:
                rng.shuffle(candidates)
            for item in candidates:
                aid = item.get("ankama_id")
                if isinstance(aid, int) and aid in occupied:
                    continue
                if current.slots.get(slot) and current.slots[slot].get("ankama_id") == aid:
                    continue
                score = _delta_score(current, slot, item, profile, pool)
                if score > current_score + 1e-9:
                    current.slots[slot] = item
                    if isinstance(aid, int):
                        for other_slot, other in list(current.slots.items()):
                            if other_slot != slot and other.get("ankama_id") == aid:
                                del current.slots[other_slot]
                    current_score = score
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break
        if (
            profile.solver_spec is not None
            and profile.solver_spec.stop_when_satisfied
        ):
            ev = evaluate_build(
                current, profile, sets_by_id=pool.sets_by_id, check_conditions=True
            )
            if ev.valid and targets_satisfied(ev.total_stats, profile.solver_spec):
                return current

    return current
