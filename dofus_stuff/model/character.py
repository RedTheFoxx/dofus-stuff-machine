"""Profil personnage et objectif d'optimisation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping

from dofus_stuff.model.stats import JetMode, Stats, canonical_stat_name

if TYPE_CHECKING:
    from dofus_stuff.model.solver_spec import SolverSpec


@dataclass(frozen=True)
class Objective:
    """Poids par caractéristique (somme pondérée)."""

    weights: dict[str, float]

    @classmethod
    def maximize(cls, *stat_names: str) -> Objective:
        weights = {canonical_stat_name(name): 1.0 for name in stat_names}
        return cls(weights=weights)

    @classmethod
    def from_weights(cls, weights: Mapping[str, float]) -> Objective:
        return cls(weights={canonical_stat_name(k): float(v) for k, v in weights.items()})


@dataclass
class CharacterProfile:
    """Entrées utilisateur pour l'optimiseur (caracs hors stuff déclarées)."""

    level: int
    objective: Objective
    base_stats: Stats = field(default_factory=Stats)
    scrolls: Stats = field(default_factory=Stats)
    jet_mode: JetMode = "average"
    solver_spec: SolverSpec | None = None

    def stats_without_equipment(self) -> Stats:
        return self.base_stats + self.scrolls

    @classmethod
    def for_demo_int_123(cls) -> CharacterProfile:
        """Exemple du plan : niveau 123, max Intelligence, parcho 100, base 200 INT."""
        from dofus_stuff.model.solver_spec import StatGoal, SolverSpec, spec_to_profile

        spec = SolverSpec(
            level=123,
            goals={
                "Intelligence": StatGoal(base=200.0, scroll=100.0, weight=1.0),
                "Vitalité": StatGoal(base=0.0),
            },
            jet_mode="average",
        )
        return spec_to_profile(spec)
