"""Helpers pour extraire les contraintes « Bonus de panoplies » des trophées."""

from __future__ import annotations

from typing import Any, Mapping

_SET_BONUS_ELEMENT = "Bonus de panoplies"


def _walk_set_bonus_bounds(node: Mapping[str, Any] | None, bounds: list[int]) -> None:
    if not node:
        return
    if node.get("is_operand"):
        condition = node.get("condition") or {}
        element = condition.get("element") or {}
        if element.get("name") != _SET_BONUS_ELEMENT:
            return
        operator = condition.get("operator")
        int_value = condition.get("int_value")
        if not isinstance(int_value, (int, float)):
            return
        value = int(int_value)
        # « Bonus de panoplies < 3 » ⇒ au plus 2 panoplies actives.
        if operator == "<":
            bounds.append(value - 1)
        elif operator == "<=":
            bounds.append(value)
        elif operator == "=":
            bounds.append(value)
        return
    for child in node.get("children") or []:
        if isinstance(child, dict):
            _walk_set_bonus_bounds(child, bounds)


def max_set_bonuses_allowed(item: Mapping[str, Any]) -> int | None:
    """
    Nombre max de panoplies actives (≥2 pièces) autorisé si l'item est équipé.

    None = aucune contrainte de ce type sur l'item.
    """
    conditions = item.get("conditions")
    if not isinstance(conditions, dict):
        return None
    bounds: list[int] = []
    _walk_set_bonus_bounds(conditions, bounds)
    if not bounds:
        return None
    return min(bounds)
