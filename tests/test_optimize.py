"""Tests unitaires du modèle stuff et de l'optimiseur."""

from __future__ import annotations

import pytest

from dofus_stuff.catalog import Catalog
from dofus_stuff.model.build import Build, evaluate_build
from dofus_stuff.model.character import CharacterProfile, Objective
from dofus_stuff.model.conditions import evaluate_condition_node, item_conditions_satisfied
from dofus_stuff.model.slots import EquipmentSlot, slot_for_equipment
from dofus_stuff.model.stats import Stats, effects_to_stats, weighted_score
from dofus_stuff.optimize.candidates import build_candidate_pool
from dofus_stuff.optimize.greedy import greedy_build
from dofus_stuff.optimize.score import compute_compatibility
from dofus_stuff.optimize import optimize_stuff


def _effect(name: str, type_id: int, lo: int, hi: int, *, fixed: bool = False) -> dict:
    return {
        "int_minimum": lo,
        "int_maximum": 0 if fixed else hi,
        "ignore_int_max": fixed,
        "ignore_int_min": False,
        "type": {"name": name, "id": type_id, "is_meta": False, "is_active": False},
        "formatted": f"{lo} {name}" if fixed else f"{lo} à {hi} {name}",
    }


@pytest.fixture
def mini_catalog() -> Catalog:
    hat = {
        "ankama_id": 1,
        "name": "Chapeau INT",
        "level": 100,
        "type": {"name": "Chapeau", "id": 27},
        "is_weapon": False,
        "effects": [_effect("Intelligence", 13, 40, 50)],
        "parent_set": {"id": 10, "name": "Set Test"},
    }
    cape = {
        "ankama_id": 2,
        "name": "Cape INT",
        "level": 100,
        "type": {"name": "Cape", "id": 43},
        "is_weapon": False,
        "effects": [_effect("Intelligence", 13, 30, 40)],
        "parent_set": {"id": 10, "name": "Set Test"},
    }
    amulet = {
        "ankama_id": 3,
        "name": "Amulette INT",
        "level": 100,
        "type": {"name": "Amulette", "id": 33},
        "is_weapon": False,
        "effects": [_effect("Intelligence", 13, 20, 30)],
    }
    ring_a = {
        "ankama_id": 4,
        "name": "Anneau A",
        "level": 90,
        "type": {"name": "Anneau", "id": 17},
        "is_weapon": False,
        "effects": [_effect("Intelligence", 13, 10, 20)],
    }
    ring_b = {
        "ankama_id": 5,
        "name": "Anneau B",
        "level": 90,
        "type": {"name": "Anneau", "id": 17},
        "is_weapon": False,
        "effects": [_effect("Intelligence", 13, 15, 25)],
    }
    belt = {
        "ankama_id": 6,
        "name": "Ceinture",
        "level": 80,
        "type": {"name": "Ceinture", "id": 58},
        "is_weapon": False,
        "effects": [_effect("Intelligence", 13, 5, 15)],
    }
    boots = {
        "ankama_id": 7,
        "name": "Bottes",
        "level": 80,
        "type": {"name": "Bottes", "id": 45},
        "is_weapon": False,
        "effects": [_effect("Intelligence", 13, 5, 15)],
    }
    weapon = {
        "ankama_id": 8,
        "name": "Bâton",
        "level": 100,
        "type": {"name": "Bâton", "id": 4},
        "is_weapon": True,
        "effects": [
            _effect("Intelligence", 13, 20, 30),
            {
                "int_minimum": 10,
                "int_maximum": 15,
                "ignore_int_max": False,
                "type": {
                    "name": "dommages Feu",
                    "id": 99,
                    "is_meta": False,
                    "is_active": True,
                },
            },
        ],
    }
    weak_hat = {
        "ankama_id": 9,
        "name": "Chapeau faible",
        "level": 50,
        "type": {"name": "Chapeau", "id": 27},
        "is_weapon": False,
        "effects": [_effect("Intelligence", 13, 1, 2)],
    }
    set_payload = {
        "ankama_id": 10,
        "name": "Set Test",
        "level": 100,
        "items": 2,
        "equipment_ids": [1, 2],
        "effects": {
            "1": None,
            "2": [_effect("Intelligence", 13, 50, 50, fixed=True)],
        },
    }
    items = {
        ("equipment", 1): hat,
        ("equipment", 2): cape,
        ("equipment", 3): amulet,
        ("equipment", 4): ring_a,
        ("equipment", 5): ring_b,
        ("equipment", 6): belt,
        ("equipment", 7): boots,
        ("equipment", 8): weapon,
        ("equipment", 9): weak_hat,
        ("sets", 10): set_payload,
    }
    return Catalog(version="test", items=items)


def test_effects_to_stats_average_and_active_ignored():
    effects = [
        _effect("Intelligence", 13, 10, 20),
        {
            "int_minimum": 5,
            "int_maximum": 10,
            "type": {"name": "dommages Feu", "id": 99, "is_meta": False, "is_active": True},
        },
    ]
    stats = effects_to_stats(effects, mode="average")
    assert stats.get("Intelligence") == 15.0


def test_slot_mapping():
    assert slot_for_equipment({"type": {"name": "Chapeau"}, "is_weapon": False}) is EquipmentSlot.HAT
    assert slot_for_equipment({"type": {"name": "Épée"}, "is_weapon": True}) is EquipmentSlot.WEAPON
    assert slot_for_equipment({"type": {"name": "Outil"}, "is_weapon": True}) is None
    assert slot_for_equipment({"type": {"name": "Dofus"}}) is EquipmentSlot.DOFUS
    assert slot_for_equipment({"type": {"name": "Trophée"}}) is EquipmentSlot.DOFUS
    assert slot_for_equipment({"type": {"name": "Familier"}}) is EquipmentSlot.PET
    assert slot_for_equipment({"type": {"name": "Montilier"}}) is EquipmentSlot.PET
    assert slot_for_equipment({"type": {"name": "Prysmaradite"}}) is EquipmentSlot.PRYSMA


def test_max_set_bonuses_allowed():
    from dofus_stuff.model.set_bonus_limits import max_set_bonuses_allowed

    trophy = {
        "conditions": {
            "is_operand": True,
            "condition": {
                "operator": "<",
                "int_value": 3,
                "element": {"name": "Bonus de panoplies", "id": 72},
            },
        }
    }
    assert max_set_bonuses_allowed(trophy) == 2
    assert max_set_bonuses_allowed({"conditions": None}) is None


def test_set_bonus_applied(mini_catalog: Catalog):
    profile = CharacterProfile(
        level=120,
        objective=Objective.maximize("Intelligence"),
        base_stats=Stats({"Intelligence": 100}),
        scrolls=Stats({"Intelligence": 100}),
    )
    build = Build(
        slots={
            "hat": mini_catalog.get_equipment(1),
            "cape": mini_catalog.get_equipment(2),
        }
    )
    sets = {10: mini_catalog.get("sets", 10)}  # type: ignore[arg-type]
    evaluation = evaluate_build(build, profile, sets_by_id=sets, check_conditions=False)
    # base 200 + hat 45 + cape 35 + set 50 = 330
    assert evaluation.total_stats.get("Intelligence") == pytest.approx(330.0)
    assert len(evaluation.set_bonuses) == 1
    assert evaluation.set_bonuses[0].tier == 2


def test_conditions_stat_threshold():
    stats = Stats({"Intelligence": 250})
    node = {
        "is_operand": True,
        "condition": {
            "operator": ">",
            "int_value": 199,
            "element": {"name": "Intelligence", "id": 13},
        },
    }
    assert evaluate_condition_node(node, character_level=120, stats=stats) is True
    stats_low = Stats({"Intelligence": 100})
    assert evaluate_condition_node(node, character_level=120, stats=stats_low) is False


def test_item_level_condition():
    item = {"level": 150, "conditions": None}
    assert (
        item_conditions_satisfied(
            item,
            character_level=123,
            stats=Stats(),
        )
        is False
    )


def test_compatibility_optimal():
    compat = compute_compatibility(
        score=800,
        optimal=True,
        best_bound=800,
        ub0=900,
    )
    assert compat.percent == 100.0
    assert compat.mode == "optimal_prouve"


def test_compatibility_heuristic_bound():
    compat = compute_compatibility(
        score=700,
        optimal=False,
        best_bound=None,
        ub0=1000,
        greedy_score=650,
    )
    assert compat.mode == "borne_heuristique"
    assert compat.percent == pytest.approx(70.0)


def test_greedy_and_optimize_mini(mini_catalog: Catalog):
    profile = CharacterProfile(
        level=120,
        objective=Objective.maximize("Intelligence"),
        base_stats=Stats({"Intelligence": 200}),
        scrolls=Stats({"Intelligence": 100}),
    )
    pool = build_candidate_pool(mini_catalog, profile, top_k=10, set_expand_m=4)
    assert pool.by_slot["hat"]
    greedy = greedy_build(pool, profile)
    assert "hat" in greedy.slots
    # Doit préférer le chapeau INT au faible
    assert greedy.slots["hat"]["ankama_id"] == 1

    result = optimize_stuff(
        mini_catalog,
        profile,
        top_k=10,
        time_limit_s=2.0,
        use_cpsat=True,
    )
    assert result.evaluation.score >= 300
    assert result.evaluation.total_stats.get("Intelligence") >= 300
    assert result.compatibility.percent > 0
    # Hat + cape du set pour le bonus +50
    ids = result.build.ankama_ids()
    assert 1 in ids and 2 in ids


def test_weighted_score():
    stats = Stats({"Intelligence": 100, "Vitalité": 50})
    assert weighted_score(stats, {"Intelligence": 1.0, "Vitalité": 0.2}) == pytest.approx(110.0)


def test_demo_profile():
    profile = CharacterProfile.for_demo_int_123()
    assert profile.level == 123
    assert profile.stats_without_equipment().get("Intelligence") == 300.0


def test_plausible_filter_rejects_mj_ring():
    from dofus_stuff.optimize.candidates import _is_plausible_equipment

    bad = {
        "name": "Annobusé de Maître Jarbo",
        "level": 1,
        "effects": [_effect("Intelligence", 13, 300, 300, fixed=True)],
    }
    good = {
        "name": "Dora Bora",
        "level": 120,
        "effects": [_effect("Intelligence", 13, 61, 80)],
    }
    assert _is_plausible_equipment(bad) is False
    assert _is_plausible_equipment(good) is True
