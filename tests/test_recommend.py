from unittest.mock import patch

import pytest

from dofus_stuff.model.build import evaluate_build
from dofus_stuff.model.solver_spec import (
    SolverSpec, StatGoal, capital_spent, spec_to_profile, stuffer_score,
    total_capital_for_level,
)
from dofus_stuff.model.stats import Stats
from dofus_stuff.optimize.candidates import CandidatePool
from dofus_stuff.optimize.cpsat import solve_cpsat
from dofus_stuff.optimize.recommend import recommendation_spec


def item(aid, kind, **stats):
    return {"ankama_id": aid, "level": 1, "name": str(aid), "type": {"name": kind},
            "effects": [{"type": {"name": n}, "int_minimum": v,
                         "int_maximum": v, "ignore_int_max": True} for n, v in stats.items()]}


@pytest.mark.parametrize("level", [1, 39, 40, 99, 100, 149, 150, 200])
@pytest.mark.parametrize("elements", [["feu"], ["terre", "air"], ["terre", "feu", "eau", "air"]])
def test_recommendation_investment(level, elements):
    spec = recommendation_spec("Cra", elements, level)
    assert total_capital_for_level(level) == 5 * (level - 1)
    assert capital_spent(spec.goals) == 5 * (level - 1)
    assert all(g.exo == g.scroll == 0 for g in spec.goals.values())
    assert spec.goal("PA").base == (7 if level >= 100 else 6)
    assert max(spec.goal(n).points for n in spec.balanced_elements) - min(
        spec.goal(n).points for n in spec.balanced_elements) <= 1
    assert SolverSpec.from_dict(spec.to_dict()) == spec


def test_multi_prefers_balance():
    spec = recommendation_spec("Iop", ["terre", "feu"], 100)
    assert stuffer_score(Stats({"Force": 90, "Intelligence": 90}), spec) > stuffer_score(
        Stats({"Force": 200}), spec)


def test_solver_caps_total_and_matches_evaluation():
    spec = SolverSpec(goals={"PA": StatGoal(base=6, target=8, weight=100),
                             "Intelligence": StatGoal(weight=1)})
    profile = spec_to_profile(spec)
    pa_hat = item(1, "Chapeau", PA=2)
    int_hat = item(2, "Chapeau", Intelligence=80)
    cape = item(3, "Cape", PA=2)
    pool = CandidatePool(by_slot={"hat": [pa_hat, int_hat], "cape": [cape]})
    result = solve_cpsat(pool, profile)
    assert result is not None
    assert result.build.slots["hat"]["ankama_id"] == 2
    assert result.score == evaluate_build(result.build, profile).score == 880


def test_set_bonus_counts_toward_target():
    spec = SolverSpec(goals={"PA": StatGoal(base=6, target=8, weight=100)})
    hat, cape = item(1, "Chapeau"), item(2, "Cape")
    for it in (hat, cape):
        it["parent_set"] = {"id": 10}
    pool = CandidatePool(by_slot={"hat": [hat], "cape": [cape]}, sets_by_id={
        10: {"name": "Test", "effects": {"2": item(9, "Cape", PA=2)["effects"]}}})
    profile = spec_to_profile(spec)
    result = solve_cpsat(pool, profile, stop_when_satisfied=True)
    assert result is not None
    assert result.score == evaluate_build(result.build, profile, sets_by_id=pool.sets_by_id).score == 800


def test_quick_flow_and_advanced(client):
    response = client.post("/optimize/quick/classe", data={"cmd": "Crâ"}, follow_redirects=True)
    assert b"2/3" in response.data
    response = client.post("/optimize/quick/elements", data={"cmd": "terre + air"}, follow_redirects=True)
    assert b"3/3" in response.data
    response = client.post("/optimize/quick/niveau", data={"cmd": "201"}, follow_redirects=True)
    assert b"1 et 200" in response.data
    with patch("dofus_stuff.web.routes._run_optimize_and_redirect", return_value="computed") as run:
        response = client.post("/optimize/quick/niveau", data={"cmd": "123"})
        assert response.data == b"computed"
        spec = run.call_args.args[0].spec
        assert spec.level == 123
        assert spec.balanced_elements == ("Force", "Agilité")
    response = client.post("/optimize/quick/niveau", data={"cmd": "AVANCE"}, follow_redirects=True)
    assert b"RECAPITULATIF" in response.data


def test_quick_deep_link_requires_profile(client):
    response = client.get("/optimize/quick/niveau", follow_redirects=True)
    assert b"1/3" in response.data


def test_event_equipment_is_filtered():
    from dofus_stuff.optimize.candidates import _is_plausible_equipment
    assert not _is_plausible_equipment(item(2155, "Amulette", PA=4, Vitalité=400))
    assert _is_plausible_equipment(item(1, "Amulette", PA=1))


def test_solver_multi_balances_aggregate():
    spec = SolverSpec(goals={"Force": StatGoal(weight=0.5), "Intelligence": StatGoal(weight=0.5)},
                      balanced_elements=("Force", "Intelligence"), allow_power_for_caracs=True)
    hat = item(1, "Chapeau", Force=150)
    complement = item(2, "Cape", Intelligence=140)
    redundant = item(3, "Cape", Force=160)
    pool = CandidatePool(by_slot={"hat": [hat], "cape": [complement, redundant]})
    profile = spec_to_profile(spec)
    result = solve_cpsat(pool, profile)
    assert result is not None
    assert result.build.slots["cape"]["ankama_id"] == 2
    assert result.score == evaluate_build(result.build, profile).score == 285
