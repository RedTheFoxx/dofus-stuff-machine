"""Mapping type d'équipement → slots personnage."""

from __future__ import annotations

from enum import Enum
from typing import Any, Mapping


class EquipmentSlot(str, Enum):
    AMULET = "amulet"
    RING = "ring"
    BELT = "belt"
    BOOTS = "boots"
    HAT = "hat"
    CAPE = "cape"
    WEAPON = "weapon"
    SHIELD = "shield"
    # Dofus et Trophées partagent 6 emplacements.
    DOFUS = "dofus"
    # Familier / Montilier / montures (mutuellement exclusifs via 1 instance).
    PET = "pet"
    PRYSMA = "prysma"


DOFUS_INSTANCES: tuple[str, ...] = tuple(f"dofus_{i}" for i in range(1, 7))

# Slots classiques (anneaux ×2).
CLASSIC_SLOT_INSTANCES: tuple[str, ...] = (
    "amulet",
    "ring_a",
    "ring_b",
    "belt",
    "boots",
    "hat",
    "cape",
    "weapon",
)

# Périmètre optimiseur joueur : classiques + bouclier + dofus/trophées + familier/monture + prysma.
SLOT_INSTANCES: tuple[str, ...] = (
    *CLASSIC_SLOT_INSTANCES,
    "shield",
    *DOFUS_INSTANCES,
    "pet",
    "prysma",
)

# Alias historique.
V1_OPTIMIZE_SLOTS: tuple[str, ...] = CLASSIC_SLOT_INSTANCES
DEFAULT_OPTIMIZE_SLOTS: tuple[str, ...] = SLOT_INSTANCES

# Slots optionnels (peuvent rester vides).
OPTIONAL_SLOT_INSTANCES: frozenset[str] = frozenset(
    (*DOFUS_INSTANCES, "pet", "prysma", "shield")
)

_TYPE_NAME_TO_SLOT: dict[str, EquipmentSlot] = {
    "Amulette": EquipmentSlot.AMULET,
    "Anneau": EquipmentSlot.RING,
    "Ceinture": EquipmentSlot.BELT,
    "Bottes": EquipmentSlot.BOOTS,
    "Chapeau": EquipmentSlot.HAT,
    "Cape": EquipmentSlot.CAPE,
    "Bouclier": EquipmentSlot.SHIELD,
    "Dofus": EquipmentSlot.DOFUS,
    "Trophée": EquipmentSlot.DOFUS,
    "Familier": EquipmentSlot.PET,
    "Montilier": EquipmentSlot.PET,
    "Dragodinde": EquipmentSlot.PET,
    "Muldo": EquipmentSlot.PET,
    "Volkorne": EquipmentSlot.PET,
    "Prysmaradite": EquipmentSlot.PRYSMA,
    # Armes
    "Épée": EquipmentSlot.WEAPON,
    "Marteau": EquipmentSlot.WEAPON,
    "Bâton": EquipmentSlot.WEAPON,
    "Dague": EquipmentSlot.WEAPON,
    "Baguette": EquipmentSlot.WEAPON,
    "Arc": EquipmentSlot.WEAPON,
    "Hache": EquipmentSlot.WEAPON,
    "Pelle": EquipmentSlot.WEAPON,
    "Lance": EquipmentSlot.WEAPON,
    "Faux": EquipmentSlot.WEAPON,
    "Arme magique": EquipmentSlot.WEAPON,
    "Poignards": EquipmentSlot.WEAPON,
}

# Outils hors stuff combat classique
_EXCLUDED_WEAPON_TYPES = frozenset({"Outil", "Pioche"})


def slot_for_equipment(item: Mapping[str, Any]) -> EquipmentSlot | None:
    """Retourne le slot d'un équipement, ou None s'il est hors périmètre stuff."""
    type_info = item.get("type")
    if not isinstance(type_info, dict):
        return None
    type_name = type_info.get("name")
    if not isinstance(type_name, str):
        return None
    if type_name in _EXCLUDED_WEAPON_TYPES:
        return None
    slot = _TYPE_NAME_TO_SLOT.get(type_name)
    if slot is not None:
        return slot
    # Fallback armes marquées is_weapon
    if item.get("is_weapon"):
        return EquipmentSlot.WEAPON
    return None


def slot_instance_kind(slot_instance: str) -> EquipmentSlot:
    """Mappe une instance (ring_a, dofus_3) vers le slot logique."""
    if slot_instance in {"ring_a", "ring_b"}:
        return EquipmentSlot.RING
    if slot_instance.startswith("dofus_"):
        return EquipmentSlot.DOFUS
    return EquipmentSlot(slot_instance)


def instances_for_slot(slot: EquipmentSlot) -> tuple[str, ...]:
    if slot is EquipmentSlot.RING:
        return ("ring_a", "ring_b")
    if slot is EquipmentSlot.DOFUS:
        return DOFUS_INSTANCES
    if slot is EquipmentSlot.SHIELD:
        return ("shield",)
    if slot is EquipmentSlot.PET:
        return ("pet",)
    if slot is EquipmentSlot.PRYSMA:
        return ("prysma",)
    return (slot.value,)


def is_optional_slot(slot_instance: str) -> bool:
    return slot_instance in OPTIONAL_SLOT_INSTANCES
