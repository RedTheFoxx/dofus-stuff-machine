"""Façade d'optimisation de stuff."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dofus_stuff.catalog import Catalog
from dofus_stuff.model.build import Build, BuildEvaluation, evaluate_build, validate_build_slots
from dofus_stuff.model.character import CharacterProfile
from dofus_stuff.model.conditions import item_conditions_satisfied
from dofus_stuff.model.slots import CLASSIC_SLOT_INSTANCES, DEFAULT_OPTIMIZE_SLOTS
from dofus_stuff.model.solver_spec import SolverSpec, spec_to_profile, targets_satisfied
from dofus_stuff.model.stats import STAT_IDS, Stats
from dofus_stuff.optimize.candidates import (
    CandidatePool,
    base_objective_score,
    build_candidate_pool,
)
from dofus_stuff.optimize.cpsat import solve_cpsat
from dofus_stuff.optimize.greedy import greedy_build, local_search
from dofus_stuff.optimize.score import Compatibility, compute_compatibility


def _iter_nonzero_stats(stats: Stats) -> list[tuple[str, float]]:
    """Caracs non nulles, dans l'ordre canonique puis extras alphabetiques."""
    ordered: list[tuple[str, float]] = []
    seen: set[str] = set()
    for name in STAT_IDS:
        value = stats.get(name)
        if value:
            ordered.append((name, value))
            seen.add(name)
    for name in sorted(stats.values):
        if name in seen:
            continue
        value = stats.get(name)
        if value:
            ordered.append((name, value))
    return ordered


def _format_stat_lines(
    stats: Stats,
    *,
    targets: dict[str, float] | None = None,
) -> list[str]:
    lines: list[str] = []
    target_map = targets or {}
    for name, value in _iter_nonzero_stats(stats):
        target = target_map.get(name)
        if target is not None and target > 0:
            lines.append(f"  {name}: {value:.1f} (cible {target:g})")
        else:
            lines.append(f"  {name}: {value:.1f}")
    if not lines:
        lines.append("  (aucune)")
    return lines


@dataclass
class OptimizeResult:
    build: Build
    evaluation: BuildEvaluation
    compatibility: Compatibility
    method: str
    greedy_score: float
    ub0: float
    pool_stats: dict[str, Any] = field(default_factory=dict)
    cpsat_status: str | None = None


def _repair_invalid_conditions(
    build: Build,
    pool: CandidatePool,
    profile: CharacterProfile,
) -> Build:
    """Retire / remplace les items dont les conditions échouent après agrégation."""
    forced_slots = set(pool.forced_build.slots)
    current = build.copy()
    for _ in range(8):
        evaluation = evaluate_build(
            current,
            profile,
            sets_by_id=pool.sets_by_id,
            check_conditions=True,
        )
        if evaluation.valid:
            return current
        invalid = set(evaluation.invalid_items)
        repaired = False
        for slot, item in list(current.slots.items()):
            if slot in forced_slots:
                continue
            aid = item.get("ankama_id")
            if not isinstance(aid, int) or aid not in invalid:
                continue
            del current.slots[slot]
            occupied = current.ankama_ids()
            best: dict[str, Any] | None = None
            best_score = float("-inf")
            for candidate in pool.by_slot.get(slot) or []:
                cid = candidate.get("ankama_id")
                if isinstance(cid, int) and cid in occupied:
                    continue
                trial = current.copy()
                trial.slots[slot] = candidate
                trial_eval = evaluate_build(
                    trial,
                    profile,
                    sets_by_id=pool.sets_by_id,
                    check_conditions=False,
                )
                if not item_conditions_satisfied(
                    candidate,
                    character_level=profile.level,
                    stats=trial_eval.total_stats,
                    set_bonus_count=trial_eval.set_bonus_count,
                ):
                    continue
                if trial_eval.score > best_score:
                    best_score = trial_eval.score
                    best = candidate
            if best is not None:
                current.slots[slot] = best
            repaired = True
            break
        if not repaired:
            break
    return current


def optimize_stuff(
    catalog: Catalog,
    profile: CharacterProfile | None = None,
    *,
    spec: SolverSpec | None = None,
    top_k: int | None = None,
    set_expand_m: int = 6,
    time_limit_s: float | None = None,
    use_cpsat: bool | None = None,
    local_polish: bool = True,
    classic_only: bool = False,
) -> OptimizeResult:
    """Pipeline complet : candidats → greedy → CP-SAT → polish → compatibilité."""
    if spec is None and profile is not None and profile.solver_spec is not None:
        spec = profile.solver_spec
    if spec is not None:
        if classic_only:
            spec = spec.with_classic_only()
        profile = spec_to_profile(spec)
    elif profile is None:
        raise ValueError("profile ou spec requis")

    assert profile is not None
    resolved_top_k = top_k if top_k is not None else (spec.top_k if spec else 30)
    resolved_time = (
        time_limit_s
        if time_limit_s is not None
        else (spec.time_limit_s if spec else 5.0)
    )
    resolved_cpsat = (
        use_cpsat if use_cpsat is not None else (spec.use_cpsat if spec else True)
    )
    seed = spec.seed if spec else None
    stop_when = bool(spec.stop_when_satisfied) if spec else False

    if classic_only and spec is None:
        slot_instances = CLASSIC_SLOT_INSTANCES
    elif spec is not None:
        slot_instances = spec.slot_instances()
    else:
        slot_instances = DEFAULT_OPTIMIZE_SLOTS

    pool = build_candidate_pool(
        catalog,
        profile,
        top_k=resolved_top_k,
        set_expand_m=set_expand_m,
        slot_instances=slot_instances,
        spec=spec,
    )
    base_score = base_objective_score(profile)
    ub0 = base_score + pool.upper_bound_equipment

    greedy = greedy_build(pool, profile, seed=seed)
    greedy_eval = evaluate_build(
        greedy,
        profile,
        sets_by_id=pool.sets_by_id,
        check_conditions=True,
    )

    best_build = greedy
    best_score = greedy_eval.score
    method = "greedy"
    optimal = False
    best_bound: float | None = None
    cpsat_status: str | None = None

    already_satisfied = (
        stop_when
        and greedy_eval.valid
        and spec is not None
        and targets_satisfied(greedy_eval.total_stats, spec)
    )

    if resolved_cpsat and not already_satisfied:
        cpsat = solve_cpsat(
            pool,
            profile,
            time_limit_s=resolved_time,
            hint_build=greedy,
            stop_when_satisfied=stop_when,
        )
        if cpsat is not None:
            cpsat_status = cpsat.status_name
            best_bound = cpsat.best_bound
            optimal = cpsat.optimal
            cpsat_eval = evaluate_build(
                cpsat.build,
                profile,
                sets_by_id=pool.sets_by_id,
                check_conditions=False,
            )
            if cpsat_eval.score >= best_score - 1e-9:
                best_build = cpsat.build
                best_score = cpsat_eval.score
                method = "cpsat" if cpsat.optimal else "cpsat_feasible"

    skip_polish = False
    if stop_when and spec is not None:
        ev = evaluate_build(
            best_build, profile, sets_by_id=pool.sets_by_id, check_conditions=True
        )
        if ev.valid and targets_satisfied(ev.total_stats, spec):
            skip_polish = True

    if local_polish and not skip_polish:
        polished = local_search(best_build, pool, profile, seed=seed)
        polished_eval = evaluate_build(
            polished,
            profile,
            sets_by_id=pool.sets_by_id,
            check_conditions=False,
        )
        if polished_eval.score > best_score + 1e-9:
            best_build = polished
            best_score = polished_eval.score
            method = f"{method}+local"
            optimal = False

    best_build = _repair_invalid_conditions(best_build, pool, profile)
    evaluation = evaluate_build(
        best_build,
        profile,
        sets_by_id=pool.sets_by_id,
        check_conditions=True,
    )
    best_score = evaluation.score

    compatibility = compute_compatibility(
        score=best_score,
        optimal=optimal and evaluation.valid,
        best_bound=best_bound,
        ub0=ub0,
        greedy_score=greedy_eval.score,
    )

    slot_errors = validate_build_slots(best_build)
    pool_stats = {
        "candidates_per_slot": {s: len(items) for s, items in pool.by_slot.items()},
        "sets_indexed": len(pool.sets_by_id),
        "ub0": ub0,
        "slot_errors": slot_errors,
        "forced": sorted(pool.forced_build.ankama_ids()),
    }

    return OptimizeResult(
        build=best_build,
        evaluation=evaluation,
        compatibility=compatibility,
        method=method,
        greedy_score=greedy_eval.score,
        ub0=ub0,
        pool_stats=pool_stats,
        cpsat_status=cpsat_status,
    )


def format_optimize_result(result: OptimizeResult, profile: CharacterProfile) -> str:
    """Format texte CLI."""
    lines: list[str] = []
    lines.append(f"Niveau {profile.level} — objectif {dict(profile.objective.weights)}")
    if profile.solver_spec is not None:
        targets = {
            k: v.target
            for k, v in profile.solver_spec.goals.items()
            if v.target > 0
        }
        if targets:
            lines.append(f"Cibles : {targets}")
    lines.append(
        f"Méthode : {result.method}"
        + (f" ({result.cpsat_status})" if result.cpsat_status else "")
    )
    lines.append(
        f"Score : {result.evaluation.score:.1f}  |  "
        f"Compatibilité : {result.compatibility.percent:.1f}% "
        f"[{result.compatibility.mode}]"
    )
    lines.append(f"Build valide : {'oui' if result.evaluation.valid else 'non'}")
    if result.evaluation.invalid_items:
        lines.append(f"Items invalides : {result.evaluation.invalid_items}")
    lines.append("")
    lines.append("Équipement :")
    display_slots = (
        "amulet",
        "ring_a",
        "ring_b",
        "belt",
        "boots",
        "hat",
        "cape",
        "weapon",
        "shield",
        "dofus_1",
        "dofus_2",
        "dofus_3",
        "dofus_4",
        "dofus_5",
        "dofus_6",
        "pet",
        "prysma",
    )
    for slot in display_slots:
        item = result.build.slots.get(slot)
        if item is None:
            if slot.startswith("dofus_") or slot in {"pet", "prysma", "shield"}:
                continue
            lines.append(f"  {slot:8s} : (vide)")
            continue
        type_name = ""
        type_info = item.get("type")
        if isinstance(type_info, dict) and type_info.get("name"):
            type_name = f" [{type_info['name']}]"
        lines.append(
            f"  {slot:8s} : {item.get('name')}{type_name} "
            f"(#{item.get('ankama_id')}, niv. {item.get('level')})"
        )
    if result.evaluation.set_bonuses:
        lines.append("")
        lines.append(
            f"Panoplies actives : {result.evaluation.set_bonus_count}"
        )
    lines.append("")
    primary = next(iter(profile.objective.weights), None)
    targets: dict[str, float] = {}
    if profile.solver_spec is not None:
        targets = {
            name: goal.target
            for name, goal in profile.solver_spec.goals.items()
            if goal.target > 0
        }
    equipment_stats = result.evaluation.item_stats + result.evaluation.set_stats
    lines.append("Stats totales (avec équipement) :")
    lines.extend(_format_stat_lines(result.evaluation.total_stats, targets=targets))
    lines.append("")
    lines.append("Stats gagnées (équipement + panoplies) :")
    lines.extend(_format_stat_lines(equipment_stats))
    if result.evaluation.set_bonuses:
        lines.append("")
        lines.append("Bonus de panoplie :")
        for bonus in result.evaluation.set_bonuses:
            lines.append(
                f"  {bonus.set_name} — {bonus.pieces} pièces (palier {bonus.tier})"
            )
    if primary:
        base_v = result.evaluation.base_stats.get(primary)
        item_v = result.evaluation.item_stats.get(primary)
        set_v = result.evaluation.set_stats.get(primary)
        lines.append("")
        lines.append(
            f"Détail {primary} — base+parcho: {base_v:.1f} | "
            f"items: {item_v:.1f} | sets: {set_v:.1f}"
        )
    lines.append(f"Greedy: {result.greedy_score:.1f} | UB0: {result.ub0:.1f}")
    return "\n".join(lines)


def format_optimize_result_lines(
    result: OptimizeResult,
    profile: CharacterProfile,
) -> list[str]:
    """Lignes prêtes pour pagination terminal (IDs Ankama bien visibles)."""
    return format_optimize_result(result, profile).splitlines()
