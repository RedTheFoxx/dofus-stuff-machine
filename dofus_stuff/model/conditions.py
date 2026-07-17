"""Évaluation d'un arbre de conditions d'équipement."""

from __future__ import annotations

from typing import Any, Mapping

from dofus_stuff.model.stats import Stats, canonical_stat_name

# Éléments non liés aux caracs numériques du stuff.
_LEVEL_ELEMENT = "Être niveau {0} ou plus"
_SUBSCRIBER_ELEMENT = "Être abonné"
_SET_BONUS_ELEMENT = "Bonus de panoplies"
_ALIGNMENT_ELEMENT = "Niveau d'alignement"
_KAMAS_ELEMENT = "Kamas"


def _compare(left: float, operator: str, right: float) -> bool:
    if operator == ">":
        return left > right
    if operator == "<":
        return left < right
    if operator == "=":
        return left == right
    if operator == ">=":
        return left >= right
    if operator == "<=":
        return left <= right
    if operator == "!=":
        return left != right
    raise ValueError(f"Opérateur de condition inconnu : {operator!r}")


def _element_value(
    element_name: str,
    *,
    character_level: int,
    stats: Stats,
    set_bonus_count: int,
    assume_subscribed: bool,
) -> float | None:
    """Valeur de l'élément pour évaluation ; None = non évaluable (considéré vrai)."""
    if element_name == _LEVEL_ELEMENT:
        return float(character_level)
    if element_name == _SUBSCRIBER_ELEMENT:
        return 1.0 if assume_subscribed else 0.0
    if element_name == _SET_BONUS_ELEMENT:
        return float(set_bonus_count)
    if element_name in {_ALIGNMENT_ELEMENT, _KAMAS_ELEMENT}:
        # Hors scope v1 : on ne bloque pas.
        return None
    try:
        stat_name = canonical_stat_name(element_name)
    except KeyError:
        return None
    return stats.get(stat_name, 0.0)


def evaluate_condition_node(
    node: Mapping[str, Any] | None,
    *,
    character_level: int,
    stats: Stats,
    set_bonus_count: int = 0,
    assume_subscribed: bool = True,
) -> bool:
    """Évalue un nœud de conditions (and/or/operand). Absent → True."""
    if not node:
        return True

    if node.get("is_operand"):
        condition = node.get("condition") or {}
        operator = condition.get("operator")
        int_value = condition.get("int_value")
        element = condition.get("element") or {}
        element_name = element.get("name")
        if not isinstance(operator, str) or not isinstance(element_name, str):
            return True
        if not isinstance(int_value, (int, float)):
            return True
        left = _element_value(
            element_name,
            character_level=character_level,
            stats=stats,
            set_bonus_count=set_bonus_count,
            assume_subscribed=assume_subscribed,
        )
        if left is None:
            return True
        return _compare(left, operator, float(int_value))

    relation = node.get("relation")
    children = node.get("children") or []
    if not children:
        return True
    results = [
        evaluate_condition_node(
            child,
            character_level=character_level,
            stats=stats,
            set_bonus_count=set_bonus_count,
            assume_subscribed=assume_subscribed,
        )
        for child in children
        if isinstance(child, dict)
    ]
    if relation == "or":
        return any(results) if results else True
    # default and
    return all(results) if results else True


def item_conditions_satisfied(
    item: Mapping[str, Any],
    *,
    character_level: int,
    stats: Stats,
    set_bonus_count: int = 0,
    assume_subscribed: bool = True,
) -> bool:
    if int(item.get("level") or 0) > character_level:
        return False
    conditions = item.get("conditions")
    if not isinstance(conditions, dict):
        return True
    return evaluate_condition_node(
        conditions,
        character_level=character_level,
        stats=stats,
        set_bonus_count=set_bonus_count,
        assume_subscribed=assume_subscribed,
    )
