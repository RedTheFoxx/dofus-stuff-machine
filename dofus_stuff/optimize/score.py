"""Score d'objectif et pourcentage de compatibilité."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CompatibilityMode = Literal["optimal_prouve", "borne_solver", "borne_heuristique"]


@dataclass
class Compatibility:
    percent: float
    mode: CompatibilityMode
    score: float
    reference: float


def compute_compatibility(
    *,
    score: float,
    optimal: bool,
    best_bound: float | None,
    ub0: float,
    greedy_score: float | None = None,
) -> Compatibility:
    """
    compatibilité = 100 * score / score_ref

    score_ref :
      1. si optimal prouvé → score (100 %)
      2. sinon best_bound CP-SAT si dispo
      3. sinon max(greedy, UB0)
    """
    if optimal:
        reference = score if score > 0 else 1.0
        return Compatibility(
            percent=100.0,
            mode="optimal_prouve",
            score=score,
            reference=reference,
        )

    if best_bound is not None and best_bound > 0:
        percent = 100.0 * score / best_bound
        return Compatibility(
            percent=min(100.0, max(0.0, percent)),
            mode="borne_solver",
            score=score,
            reference=best_bound,
        )

    floor = greedy_score if greedy_score is not None else score
    reference = max(floor, ub0, score, 1e-9)
    percent = 100.0 * score / reference
    return Compatibility(
        percent=min(100.0, max(0.0, percent)),
        mode="borne_heuristique",
        score=score,
        reference=reference,
    )
