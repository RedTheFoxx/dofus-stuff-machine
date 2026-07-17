"""Tests SolverSpec / score Stuffer / filtres."""

from __future__ import annotations

import pytest

from dofus_stuff.model.solver_spec import (
    StatGoal,
    SolverSpec,
    auto_distribute_characteristic_points,
    effective_stat_value,
    item_passes_type_filters,
    spec_to_profile,
    stuffer_score,
    targets_satisfied,
)
from dofus_stuff.model.stats import Stats
from dofus_stuff.optimize.api import optimize_stuff
from dofus_stuff.optimize.profile_input import parse_optimize_request


def test_stuffer_score_caps_at_target():
    spec = SolverSpec(
        level=100,
        goals={"Intelligence": StatGoal(target=500, weight=2.0)},
    )
    stats = Stats({"Intelligence": 800.0})
    assert stuffer_score(stats, spec) == pytest.approx(1000.0)


def test_power_substitution():
    spec = SolverSpec(
        level=100,
        goals={"Intelligence": StatGoal(weight=1.0)},
        allow_power_for_caracs=True,
    )
    stats = Stats({"Intelligence": 100.0, "Puissance": 50.0})
    assert effective_stat_value(
        stats, "Intelligence", allow_power_for_caracs=True
    ) == pytest.approx(150.0)
    assert stuffer_score(stats, spec) == pytest.approx(150.0)


def test_targets_satisfied():
    spec = SolverSpec(
        level=100,
        goals={
            "PA": StatGoal(target=11, weight=1.0),
            "Intelligence": StatGoal(target=1000, weight=1.0),
        },
    )
    assert not targets_satisfied(Stats({"PA": 10, "Intelligence": 1000}), spec)
    assert targets_satisfied(Stats({"PA": 11, "Intelligence": 1000}), spec)


def test_type_filters_dofus():
    item = {"type": {"name": "Dofus"}}
    assert item_passes_type_filters(item, {"dofus": True})
    assert not item_passes_type_filters(item, {"dofus": False})


def test_type_filters_ranged_weapon():
    item = {"type": {"name": "Arc"}, "is_weapon": True}
    assert not item_passes_type_filters(item, {"arme_distance": False, "arme_melee": True})
    assert item_passes_type_filters(item, {"arme_distance": True, "arme_melee": False})


def test_auto_distribute_points():
    spec = SolverSpec(
        level=50,
        goals={"Intelligence": StatGoal(weight=1.0, target=200)},
        auto_distribute_points=True,
    )
    resolved = auto_distribute_characteristic_points(spec)
    assert resolved.goals["Intelligence"].points > 0


def test_spec_to_profile_weights():
    spec = SolverSpec(
        level=123,
        goals={
            "Intelligence": StatGoal(base=200, scroll=100, weight=2.0, target=1200),
            "Vitalité": StatGoal(weight=0.5),
        },
    )
    profile = spec_to_profile(spec)
    assert profile.level == 123
    assert profile.base_stats.get("Intelligence") == 200.0
    assert profile.scrolls.get("Intelligence") == 100.0
    assert profile.objective.weights["Intelligence"] == 2.0
    assert profile.solver_spec is not None


def test_cli_target_weight_flags():
    req = parse_optimize_request(
        level=100,
        max_stats=["intelligence"],
        base_int=100,
        targets=["intelligence=900"],
        weights=["intelligence=3"],
    )
    assert req.spec is not None
    goal = req.spec.goals["Intelligence"]
    assert goal.target == 900
    assert goal.weight == 3


def test_optimize_with_targets_and_weights(catalog):
    spec = SolverSpec(
        level=50,
        goals={
            "Intelligence": StatGoal(base=50, weight=1.0),
            "PA": StatGoal(base=6, target=8, weight=10.0),
        },
        enabled_slot_groups=(
            "amulet",
            "rings",
            "belt",
            "boots",
            "hat",
            "cape",
            "weapon",
        ),
        top_k=20,
        time_limit_s=2.0,
    )
    result = optimize_stuff(catalog, spec=spec)
    assert result.evaluation.score >= 0
    assert result.build.slots


def test_optimize_blacklist(catalog):
    # Trouver un item bas niveau
    sample = None
    for (kind, _), payload in catalog.items.items():
        if kind != "equipment":
            continue
        if int(payload.get("level") or 0) <= 20 and payload.get("ankama_id"):
            sample = payload
            break
    assert sample is not None
    aid = int(sample["ankama_id"])
    req = parse_optimize_request(
        level=50,
        max_stats=["intelligence"],
        ban_ids=[aid],
        classic_only=True,
        time_limit_s=2.0,
        top_k=15,
    )
    result = optimize_stuff(catalog, req.profile, spec=req.spec, classic_only=True)
    assert aid not in result.build.ankama_ids()
