"""Modèle métier stuff : stats, slots, profil, build, conditions."""

from dofus_stuff.model.build import Build, BuildEvaluation, evaluate_build
from dofus_stuff.model.character import CharacterProfile, Objective
from dofus_stuff.model.slots import SLOT_INSTANCES, EquipmentSlot, slot_for_equipment
from dofus_stuff.model.solver_spec import SolverSpec, StatGoal, spec_to_profile
from dofus_stuff.model.stats import JetMode, STAT_IDS, STAT_NAMES, Stats, effects_to_stats

__all__ = [
    "Build",
    "BuildEvaluation",
    "CharacterProfile",
    "EquipmentSlot",
    "JetMode",
    "Objective",
    "SLOT_INSTANCES",
    "STAT_IDS",
    "STAT_NAMES",
    "SolverSpec",
    "StatGoal",
    "Stats",
    "effects_to_stats",
    "evaluate_build",
    "slot_for_equipment",
    "spec_to_profile",
]
