"""Spécification Stuffer Joueur pour l'optimiseur."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Mapping

from dofus_stuff.model.character import CharacterProfile, Objective
from dofus_stuff.model.slots import (
    DOFUS_INSTANCES,
)
from dofus_stuff.model.stats import JetMode, Stats, canonical_stat_name

# Groupes de slots activables (UI / filtres).
SLOT_GROUPS: dict[str, tuple[str, ...]] = {
    "amulet": ("amulet",),
    "rings": ("ring_a", "ring_b"),
    "belt": ("belt",),
    "boots": ("boots",),
    "hat": ("hat",),
    "cape": ("cape",),
    "weapon": ("weapon",),
    "shield": ("shield",),
    "dofus": DOFUS_INSTANCES,
    "pet": ("pet",),
    "prysma": ("prysma",),
}

DEFAULT_SLOT_GROUPS: tuple[str, ...] = (
    "amulet",
    "rings",
    "belt",
    "boots",
    "hat",
    "cape",
    "weapon",
    "dofus",
    "pet",
    "prysma",
)

# Filtres de types d'équipement (True = autorisé).
TYPE_FILTER_KEYS: tuple[str, ...] = (
    "familier",
    "montilier",
    "dragodinde",
    "muldo",
    "volkorne",
    "arme_distance",
    "arme_melee",
    "dofus",
    "trophee",
    "prysmaradite",
)

_RANGED_WEAPON_TYPES = frozenset({"Arc", "Baguette", "Arme magique"})
_MELEE_WEAPON_TYPES = frozenset(
    {
        "Épée",
        "Marteau",
        "Bâton",
        "Dague",
        "Hache",
        "Pelle",
        "Lance",
        "Faux",
        "Poignards",
    }
)

MAIN_CARACS: tuple[str, ...] = (
    "Vitalité",
    "Sagesse",
    "Force",
    "Intelligence",
    "Chance",
    "Agilité",
)

EXO_STATS: tuple[str, ...] = ("PA", "PM", "Portée")

ELEMENTAL_CARACS: frozenset[str] = frozenset(
    {"Force", "Intelligence", "Chance", "Agilité"}
)
ELEMENTAL_DAMAGES: frozenset[str] = frozenset(
    {
        "Dommage Neutre",
        "Dommage Terre",
        "Dommage Feu",
        "Dommage Eau",
        "Dommage Air",
    }
)


@dataclass(frozen=True)
class StatGoal:
    """Base / points / cible / poids (+ exo pour PA/PM/PO, scroll = parchemins)."""

    base: float = 0.0
    points: float = 0.0
    target: float = 0.0
    weight: float = 0.0
    exo: float = 0.0
    scroll: float = 0.0

    def contribution_without_equipment(self) -> float:
        return (
            float(self.base)
            + float(self.points)
            + float(self.scroll)
            + float(self.exo)
        )

    def to_dict(self) -> dict[str, float]:
        return {
            "base": self.base,
            "points": self.points,
            "target": self.target,
            "weight": self.weight,
            "exo": self.exo,
            "scroll": self.scroll,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> StatGoal:
        return cls(
            base=float(data.get("base") or 0.0),
            points=float(data.get("points") or 0.0),
            target=float(data.get("target") or 0.0),
            weight=float(data.get("weight") or 0.0),
            exo=float(data.get("exo") or 0.0),
            scroll=float(data.get("scroll") or 0.0),
        )


def default_type_filters() -> dict[str, bool]:
    return {key: True for key in TYPE_FILTER_KEYS}


@dataclass(frozen=True)
class SolverSpec:
    """Configuration complète de l'optimiseur (parité Stuffer Joueur)."""

    level: int = 200
    jet_mode: JetMode = "average"
    goals: dict[str, StatGoal] = field(default_factory=dict)
    enabled_slot_groups: tuple[str, ...] = DEFAULT_SLOT_GROUPS
    type_filters: dict[str, bool] = field(default_factory=default_type_filters)
    blacklist_ids: frozenset[int] = field(default_factory=frozenset)
    forced_ids: frozenset[int] = field(default_factory=frozenset)
    auto_distribute_points: bool = False
    allow_power_for_caracs: bool = False
    allow_damages_for_elemental: bool = False
    allow_crit_damages_for_elemental: bool = False
    stop_when_satisfied: bool = False
    time_limit_s: float = 5.0
    seed: int | None = None
    top_k: int = 30
    use_cpsat: bool = True

    def goal(self, name: str) -> StatGoal:
        try:
            canon = canonical_stat_name(name)
        except KeyError:
            canon = name
        return self.goals.get(canon, StatGoal())

    def slot_instances(self) -> tuple[str, ...]:
        slots: list[str] = []
        seen: set[str] = set()
        for group in self.enabled_slot_groups:
            for instance in SLOT_GROUPS.get(group, ()):
                if instance not in seen:
                    slots.append(instance)
                    seen.add(instance)
        return tuple(slots)

    def with_classic_only(self) -> SolverSpec:
        groups = tuple(g for g in self.enabled_slot_groups if g in {
            "amulet", "rings", "belt", "boots", "hat", "cape", "weapon",
        })
        return replace(self, enabled_slot_groups=groups or DEFAULT_SLOT_GROUPS[:7])

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "jet_mode": self.jet_mode,
            "goals": {k: v.to_dict() for k, v in self.goals.items()},
            "enabled_slot_groups": list(self.enabled_slot_groups),
            "type_filters": dict(self.type_filters),
            "blacklist_ids": sorted(self.blacklist_ids),
            "forced_ids": sorted(self.forced_ids),
            "auto_distribute_points": self.auto_distribute_points,
            "allow_power_for_caracs": self.allow_power_for_caracs,
            "allow_damages_for_elemental": self.allow_damages_for_elemental,
            "allow_crit_damages_for_elemental": self.allow_crit_damages_for_elemental,
            "stop_when_satisfied": self.stop_when_satisfied,
            "time_limit_s": self.time_limit_s,
            "seed": self.seed,
            "top_k": self.top_k,
            "use_cpsat": self.use_cpsat,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SolverSpec:
        goals_raw = data.get("goals") or {}
        goals = {
            canonical_stat_name(k) if _can_canon(k) else k: StatGoal.from_dict(v)
            for k, v in goals_raw.items()
        }
        filters = default_type_filters()
        filters.update({str(k): bool(v) for k, v in (data.get("type_filters") or {}).items()})
        groups = tuple(data.get("enabled_slot_groups") or DEFAULT_SLOT_GROUPS)
        jet = data.get("jet_mode") or "average"
        if jet not in {"min", "average", "max"}:
            jet = "average"
        return cls(
            level=int(data.get("level") or 200),
            jet_mode=jet,  # type: ignore[arg-type]
            goals=goals,
            enabled_slot_groups=groups,
            type_filters=filters,
            blacklist_ids=frozenset(int(x) for x in (data.get("blacklist_ids") or [])),
            forced_ids=frozenset(int(x) for x in (data.get("forced_ids") or [])),
            auto_distribute_points=bool(data.get("auto_distribute_points")),
            allow_power_for_caracs=bool(data.get("allow_power_for_caracs")),
            allow_damages_for_elemental=bool(data.get("allow_damages_for_elemental")),
            allow_crit_damages_for_elemental=bool(
                data.get("allow_crit_damages_for_elemental")
            ),
            stop_when_satisfied=bool(data.get("stop_when_satisfied")),
            time_limit_s=float(data.get("time_limit_s") or 5.0),
            seed=int(data["seed"]) if data.get("seed") is not None else None,
            top_k=int(data.get("top_k") or 30),
            use_cpsat=bool(data.get("use_cpsat", True)),
        )


def _can_canon(name: str) -> bool:
    try:
        canonical_stat_name(name)
        return True
    except KeyError:
        return False


def characteristic_point_cost(current_points: int) -> int:
    """Coût du prochain point de carac (hors Vitalité) selon paliers Dofus."""
    if current_points < 100:
        return 1
    if current_points < 200:
        return 2
    if current_points < 300:
        return 3
    if current_points < 400:
        return 4
    return 5


def total_capital_for_level(level: int) -> int:
    """Capital de points de caractéristiques disponible (approximation)."""
    return max(0, int(level) - 1)


def capital_spent(goals: Mapping[str, StatGoal]) -> int:
    """Capital consommé par les points déjà saisis (Vitalité 1:1, autres paliers)."""
    spent = 0
    for name, goal in goals.items():
        pts = int(max(0, round(goal.points)))
        if pts <= 0:
            continue
        if name == "Vitalité":
            spent += pts
            continue
        # Coût cumulé pour atteindre `pts` depuis 0
        for current in range(pts):
            spent += characteristic_point_cost(current)
    return spent


def auto_distribute_characteristic_points(spec: SolverSpec) -> SolverSpec:
    """Répartit le capital restant vers les caracs principales à poids/cible."""
    if not spec.auto_distribute_points:
        return spec

    goals = dict(spec.goals)
    remaining = total_capital_for_level(spec.level) - capital_spent(goals)
    if remaining <= 0:
        return spec

    # Priorité : poids décroissant, puis cible
    candidates = [
        name
        for name in MAIN_CARACS
        if goals.get(name, StatGoal()).weight > 0
        or goals.get(name, StatGoal()).target > 0
    ]
    if not candidates:
        candidates = list(MAIN_CARACS)

    candidates.sort(
        key=lambda n: (
            -(goals.get(n, StatGoal()).weight),
            -(goals.get(n, StatGoal()).target),
            n,
        )
    )

    # Répartition gloutonne point par point
    safety = remaining + 5
    while remaining > 0 and safety > 0:
        safety -= 1
        best_name: str | None = None
        best_cost = 0
        for name in candidates:
            goal = goals.get(name, StatGoal())
            pts = int(max(0, round(goal.points)))
            cost = 1 if name == "Vitalité" else characteristic_point_cost(pts)
            if cost > remaining:
                continue
            # Préférer les caracs encore sous cible
            deficit = max(0.0, goal.target - goal.contribution_without_equipment())
            if best_name is None:
                best_name = name
                best_cost = cost
                continue
            best_goal = goals.get(best_name, StatGoal())
            best_deficit = max(
                0.0, best_goal.target - best_goal.contribution_without_equipment()
            )
            if deficit > best_deficit + 1e-9:
                best_name = name
                best_cost = cost
            elif abs(deficit - best_deficit) < 1e-9 and goal.weight > best_goal.weight:
                best_name = name
                best_cost = cost
        if best_name is None:
            break
        g = goals.get(best_name, StatGoal())
        goals[best_name] = StatGoal(
            base=g.base,
            points=g.points + 1,
            target=g.target,
            weight=g.weight,
            exo=g.exo,
            scroll=g.scroll,
        )
        remaining -= best_cost

    return replace(spec, goals=goals)


def effective_stat_value(
    stats: Stats,
    name: str,
    *,
    allow_power_for_caracs: bool = False,
    allow_damages_for_elemental: bool = False,
    allow_crit_damages_for_elemental: bool = False,
) -> float:
    """Valeur d'une carac pour le score (avec substitutions optionnelles)."""
    value = stats.get(name, 0.0)
    if allow_power_for_caracs and name in ELEMENTAL_CARACS:
        value += stats.get("Puissance", 0.0)
    if name in ELEMENTAL_DAMAGES:
        if allow_damages_for_elemental:
            value += stats.get("Dommage", 0.0)
        if allow_crit_damages_for_elemental:
            value += stats.get("Dommage Critiques", 0.0)
    return value


def stuffer_score(
    stats: Stats,
    spec: SolverSpec,
) -> float:
    """
    Score Stuffer : Σ weight_i * contribution_i
    contribution = min(valeur_effective, target) si target > 0, sinon valeur.
    """
    total = 0.0
    for name, goal in spec.goals.items():
        if goal.weight == 0:
            continue
        value = effective_stat_value(
            stats,
            name,
            allow_power_for_caracs=spec.allow_power_for_caracs,
            allow_damages_for_elemental=spec.allow_damages_for_elemental,
            allow_crit_damages_for_elemental=spec.allow_crit_damages_for_elemental,
        )
        if goal.target > 0:
            value = min(value, goal.target)
        total += float(goal.weight) * value
    return total


def targets_satisfied(stats: Stats, spec: SolverSpec) -> bool:
    """True si toutes les cibles > 0 sont atteintes (avec substitutions)."""
    for name, goal in spec.goals.items():
        if goal.target <= 0:
            continue
        value = effective_stat_value(
            stats,
            name,
            allow_power_for_caracs=spec.allow_power_for_caracs,
            allow_damages_for_elemental=spec.allow_damages_for_elemental,
            allow_crit_damages_for_elemental=spec.allow_crit_damages_for_elemental,
        )
        if value + 1e-9 < goal.target:
            return False
    return True


def item_passes_type_filters(item: Mapping[str, Any], filters: Mapping[str, bool]) -> bool:
    """Applique les filtres de types Stuffer."""
    type_info = item.get("type")
    type_name = type_info.get("name") if isinstance(type_info, dict) else None
    if not isinstance(type_name, str):
        return True

    if type_name == "Familier" and not filters.get("familier", True):
        return False
    if type_name == "Montilier" and not filters.get("montilier", True):
        return False
    if type_name == "Dragodinde" and not filters.get("dragodinde", True):
        return False
    if type_name == "Muldo" and not filters.get("muldo", True):
        return False
    if type_name == "Volkorne" and not filters.get("volkorne", True):
        return False
    if type_name == "Dofus" and not filters.get("dofus", True):
        return False
    if type_name == "Trophée" and not filters.get("trophee", True):
        return False
    if type_name == "Prysmaradite" and not filters.get("prysmaradite", True):
        return False

    if type_name in _RANGED_WEAPON_TYPES and not filters.get("arme_distance", True):
        return False
    if type_name in _MELEE_WEAPON_TYPES and not filters.get("arme_melee", True):
        return False
    # Arme non classée : autorisée si au moins un mode arme est ON
    if item.get("is_weapon") and type_name not in _RANGED_WEAPON_TYPES | _MELEE_WEAPON_TYPES:
        if not (filters.get("arme_distance", True) or filters.get("arme_melee", True)):
            return False
    return True


def spec_to_profile(spec: SolverSpec) -> CharacterProfile:
    """Dérive un CharacterProfile (bases + poids) depuis un SolverSpec."""
    resolved = auto_distribute_characteristic_points(spec)
    base_values: dict[str, float] = {}
    scroll_values: dict[str, float] = {}
    weights: dict[str, float] = {}
    for name, goal in resolved.goals.items():
        base_part = float(goal.base) + float(goal.points) + float(goal.exo)
        if base_part:
            base_values[name] = base_part
        if goal.scroll:
            scroll_values[name] = float(goal.scroll)
        if goal.weight:
            weights[name] = float(goal.weight)
    if not weights:
        weights = {"Intelligence": 1.0}
    return CharacterProfile(
        level=resolved.level,
        objective=Objective.from_weights(weights),
        base_stats=Stats(base_values),
        scrolls=Stats(scroll_values),
        jet_mode=resolved.jet_mode,
        solver_spec=resolved,
    )


def profile_from_legacy(
    *,
    level: int,
    max_stats: list[str],
    base_stats: Stats,
    scrolls: Stats,
    jet_mode: JetMode = "average",
    classic_only: bool = False,
    top_k: int = 30,
    time_limit_s: float = 5.0,
    use_cpsat: bool = True,
) -> SolverSpec:
    """Construit un SolverSpec depuis l'ancienne API max-caracs."""
    goals: dict[str, StatGoal] = {}
    for name in max_stats:
        canon = canonical_stat_name(name)
        goals[canon] = StatGoal(
            base=base_stats.get(canon, 0.0),
            scroll=scrolls.get(canon, 0.0),
            weight=1.0,
        )

    for name in ("Intelligence", "Vitalité", "Force", "Chance", "Agilité", "Sagesse"):
        if name in goals:
            continue
        b = base_stats.get(name, 0.0)
        s = scrolls.get(name, 0.0)
        if b or s:
            goals[name] = StatGoal(base=b, scroll=s, weight=0.0)

    groups = (
        tuple(
            g
            for g in DEFAULT_SLOT_GROUPS
            if g in {"amulet", "rings", "belt", "boots", "hat", "cape", "weapon"}
        )
        if classic_only
        else DEFAULT_SLOT_GROUPS
    )
    return SolverSpec(
        level=level,
        jet_mode=jet_mode,
        goals=goals,
        enabled_slot_groups=groups,
        top_k=top_k,
        time_limit_s=time_limit_s,
        use_cpsat=use_cpsat,
    )


def default_player_spec(*, level: int = 200) -> SolverSpec:
    """Spec wizard par défaut (slots standards, aucun poids)."""
    return SolverSpec(level=level, enabled_slot_groups=DEFAULT_SLOT_GROUPS)
