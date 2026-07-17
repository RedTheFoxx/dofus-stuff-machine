"""Solver CP-SAT sur l'espace de candidats réduit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dofus_stuff.model.build import Build
from dofus_stuff.model.character import CharacterProfile
from dofus_stuff.model.set_bonus_limits import max_set_bonuses_allowed
from dofus_stuff.model.slots import is_optional_slot
from dofus_stuff.model.solver_spec import (
    ELEMENTAL_CARACS,
    ELEMENTAL_DAMAGES,
    SolverSpec,
    stuffer_score,
)
from dofus_stuff.model.stats import effects_to_stats, weighted_score
from dofus_stuff.optimize.candidates import CandidatePool, base_objective_score

# Échelle entière : on maximise 2 * score_average pour rester exact avec les demi-points.
SCALE = 2


@dataclass
class CpSatResult:
    build: Build
    score: float
    optimal: bool
    best_bound: float | None
    status_name: str


def _scaled_item_contrib(item: dict[str, Any], profile: CharacterProfile) -> int:
    stats = effects_to_stats(item.get("effects"), mode=profile.jet_mode)
    if profile.solver_spec is not None:
        raw = stuffer_score(stats, profile.solver_spec)
    else:
        raw = weighted_score(stats, profile.objective.weights)
    return int(round(raw * SCALE))


def _scaled_set_tier_contrib(
    set_payload: dict[str, Any],
    tier: int,
    profile: CharacterProfile,
) -> int:
    effects_map = set_payload.get("effects")
    if not isinstance(effects_map, dict):
        return 0
    tier_effects = effects_map.get(str(tier))
    if not isinstance(tier_effects, list):
        return 0
    stats = effects_to_stats(tier_effects, mode=profile.jet_mode)
    if profile.solver_spec is not None:
        raw = stuffer_score(stats, profile.solver_spec)
    else:
        raw = weighted_score(stats, profile.objective.weights)
    return int(round(raw * SCALE))


def _set_tiers(set_payload: dict[str, Any]) -> list[int]:
    effects_map = set_payload.get("effects")
    if not isinstance(effects_map, dict):
        return []
    tiers: list[int] = []
    for key, value in effects_map.items():
        if value is None:
            continue
        try:
            tiers.append(int(key))
        except (TypeError, ValueError):
            continue
    return sorted(set(tiers))


def _item_stat_value(item: dict[str, Any], stat: str, profile: CharacterProfile) -> int:
    stats = effects_to_stats(item.get("effects"), mode=profile.jet_mode)
    return int(round(stats.get(stat, 0.0) * SCALE))


def _add_target_constraints(
    model: Any,
    x: dict[tuple[str, int], Any],
    item_by_id: dict[int, dict[str, Any]],
    profile: CharacterProfile,
    spec: SolverSpec,
) -> None:
    """Contraintes dures valeur_effective >= cible (approximation linéaire items)."""
    base = profile.stats_without_equipment()
    for name, goal in spec.goals.items():
        if goal.target <= 0:
            continue
        terms: list[Any] = []
        for (slot, aid), var in x.items():
            contrib = _item_stat_value(item_by_id[aid], name, profile)
            # Substitutions approximatives au niveau item
            if spec.allow_power_for_caracs and name in ELEMENTAL_CARACS:
                contrib += _item_stat_value(item_by_id[aid], "Puissance", profile)
            if name in ELEMENTAL_DAMAGES:
                if spec.allow_damages_for_elemental:
                    contrib += _item_stat_value(item_by_id[aid], "Dommage", profile)
                if spec.allow_crit_damages_for_elemental:
                    contrib += _item_stat_value(
                        item_by_id[aid], "Dommage Critiques", profile
                    )
            if contrib:
                terms.append(contrib * var)
        base_part = int(round(base.get(name, 0.0) * SCALE))
        if spec.allow_power_for_caracs and name in ELEMENTAL_CARACS:
            base_part += int(round(base.get("Puissance", 0.0) * SCALE))
        if name in ELEMENTAL_DAMAGES:
            if spec.allow_damages_for_elemental:
                base_part += int(round(base.get("Dommage", 0.0) * SCALE))
            if spec.allow_crit_damages_for_elemental:
                base_part += int(round(base.get("Dommage Critiques", 0.0) * SCALE))
        target_scaled = int(round(goal.target * SCALE))
        model.Add(base_part + sum(terms) >= target_scaled)


def solve_cpsat(
    pool: CandidatePool,
    profile: CharacterProfile,
    *,
    time_limit_s: float = 5.0,
    hint_build: Build | None = None,
    stop_when_satisfied: bool = False,
) -> CpSatResult | None:
    """
    Résout le MIP stuff sur le pool.

    Retourne None si ortools n'est pas installé ou si aucun candidat.
    """
    try:
        from ortools.sat.python import cp_model
    except ImportError:
        return None

    slot_names = [s for s, items in pool.by_slot.items() if items]
    if not slot_names:
        return None

    model = cp_model.CpModel()
    forced_slots = set(pool.forced_build.slots)

    x: dict[tuple[str, int], Any] = {}
    item_by_id: dict[int, dict[str, Any]] = {}
    slots_of_item: dict[int, list[str]] = {}

    for slot in slot_names:
        for item in pool.by_slot[slot]:
            aid = item.get("ankama_id")
            if not isinstance(aid, int):
                continue
            item_by_id[aid] = item
            var = model.NewBoolVar(f"x_{slot}_{aid}")
            x[(slot, aid)] = var
            slots_of_item.setdefault(aid, []).append(slot)

    # Cardinalité par slot : ==1 si requis, <=1 si optionnel ; forcer les slots forcés
    for slot in slot_names:
        vars_in_slot = [
            x[(slot, item["ankama_id"])]
            for item in pool.by_slot[slot]
            if isinstance(item.get("ankama_id"), int) and (slot, item["ankama_id"]) in x
        ]
        if not vars_in_slot:
            continue
        if slot in forced_slots:
            forced_item = pool.forced_build.slots[slot]
            forced_aid = forced_item.get("ankama_id")
            if isinstance(forced_aid, int) and (slot, forced_aid) in x:
                model.Add(x[(slot, forced_aid)] == 1)
            continue
        if is_optional_slot(slot):
            model.Add(sum(vars_in_slot) <= 1)
        else:
            model.Add(sum(vars_in_slot) == 1)

    # Unicité globale d'ankama_id
    for aid, slots in slots_of_item.items():
        vars_for_item = [x[(slot, aid)] for slot in slots if (slot, aid) in x]
        if len(vars_for_item) > 1:
            model.Add(sum(vars_for_item) <= 1)

    # Index set_id → items candidats
    items_by_set: dict[int, list[int]] = {}
    for aid, item in item_by_id.items():
        parent = item.get("parent_set")
        if isinstance(parent, dict) and isinstance(parent.get("id"), int):
            items_by_set.setdefault(parent["id"], []).append(aid)

    set_bonus_terms: list[Any] = []
    active_set_vars: list[Any] = []

    for set_id, member_ids in items_by_set.items():
        set_payload = pool.sets_by_id.get(set_id)
        if set_payload is None:
            continue
        tiers = _set_tiers(set_payload)
        if not tiers:
            continue

        member_vars = []
        for aid in member_ids:
            for slot in slots_of_item.get(aid, []):
                if (slot, aid) in x:
                    member_vars.append(x[(slot, aid)])
        if not member_vars:
            continue
        count = model.NewIntVar(0, len(member_vars), f"set_count_{set_id}")
        model.Add(count == sum(member_vars))

        active = model.NewBoolVar(f"set_active_{set_id}")
        model.Add(count >= 2).OnlyEnforceIf(active)
        model.Add(count < 2).OnlyEnforceIf(active.Not())
        active_set_vars.append(active)

        z_vars: list[Any] = []
        for index, tier in enumerate(tiers):
            z = model.NewBoolVar(f"set_{set_id}_tier_{tier}")
            next_tier = tiers[index + 1] if index + 1 < len(tiers) else None
            model.Add(count >= tier).OnlyEnforceIf(z)
            if next_tier is not None:
                model.Add(count < next_tier).OnlyEnforceIf(z)
                ge = model.NewBoolVar(f"set_{set_id}_ge_{tier}")
                lt = model.NewBoolVar(f"set_{set_id}_lt_{next_tier}")
                model.Add(count >= tier).OnlyEnforceIf(ge)
                model.Add(count < tier).OnlyEnforceIf(ge.Not())
                model.Add(count < next_tier).OnlyEnforceIf(lt)
                model.Add(count >= next_tier).OnlyEnforceIf(lt.Not())
                model.AddBoolAnd([ge, lt]).OnlyEnforceIf(z)
                model.AddBoolOr([ge.Not(), lt.Not(), z])
            else:
                model.Add(count < tier).OnlyEnforceIf(z.Not())
            contrib = _scaled_set_tier_contrib(set_payload, tier, profile)
            if contrib:
                set_bonus_terms.append(contrib * z)
            z_vars.append(z)
        if z_vars:
            model.Add(sum(z_vars) <= 1)

    set_bonus_count = model.NewIntVar(0, max(len(active_set_vars), 1), "set_bonus_count")
    if active_set_vars:
        model.Add(set_bonus_count == sum(active_set_vars))
    else:
        model.Add(set_bonus_count == 0)

    for (slot, aid), var in x.items():
        item = item_by_id[aid]
        max_allowed = max_set_bonuses_allowed(item)
        if max_allowed is None:
            continue
        model.Add(set_bonus_count <= max_allowed).OnlyEnforceIf(var)

    if profile.solver_spec is not None and stop_when_satisfied:
        _add_target_constraints(
            model, x, item_by_id, profile, profile.solver_spec
        )

    item_terms: list[Any] = []
    for (slot, aid), var in x.items():
        contrib = _scaled_item_contrib(item_by_id[aid], profile)
        if contrib:
            item_terms.append(contrib * var)

    base_scaled = int(round(base_objective_score(profile) * SCALE))
    objective_expr = base_scaled + sum(item_terms) + sum(set_bonus_terms)
    model.Maximize(objective_expr)

    if hint_build is not None:
        for slot, item in hint_build.slots.items():
            aid = item.get("ankama_id")
            if isinstance(aid, int) and (slot, aid) in x:
                model.AddHint(x[(slot, aid)], 1)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit_s)
    solver.parameters.num_search_workers = 4
    if stop_when_satisfied:
        solver.parameters.stop_after_first_solution = True
    status = solver.Solve(model)

    status_name = solver.StatusName(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    build = Build()
    for (slot, aid), var in x.items():
        if solver.Value(var) == 1:
            build.slots[slot] = item_by_id[aid]

    # Respecter les slots forcés même si absents de la solution (ne devrait pas arriver)
    for slot, item in pool.forced_build.slots.items():
        build.slots[slot] = item

    objective_value = solver.ObjectiveValue() / SCALE
    best_bound: float | None = None
    try:
        best_bound = solver.BestObjectiveBound() / SCALE
    except Exception:
        best_bound = objective_value if status == cp_model.OPTIMAL else None

    return CpSatResult(
        build=build,
        score=objective_value,
        optimal=(status == cp_model.OPTIMAL),
        best_bound=best_bound,
        status_name=status_name,
    )
