"""Parsing d'entrée utilisateur pour l'optimiseur (CLI + web)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from dofus_stuff.model.character import CharacterProfile
from dofus_stuff.model.solver_spec import (
    SolverSpec,
    StatGoal,
    profile_from_legacy,
    spec_to_profile,
)
from dofus_stuff.model.stats import JetMode, Stats, canonical_stat_name

COMPACT_HELP_LINES: tuple[str, ...] = (
    "SYNTAXE : demo | demo classic",
    "         NIVEAU CARAC[,CARAC] [BASE[,…]] [SCROLL[,…]] [classic] [jet=…]",
    "EXEMPLES : demo",
    "           123 intelligence 200 100",
    "           123 int,vit 200,50 100,0 classic jet=max",
)


class OptimizeInputError(ValueError):
    """Erreur de saisie utilisateur (message affichable)."""


@dataclass(frozen=True)
class OptimizeRequest:
    profile: CharacterProfile
    classic_only: bool = False
    top_k: int = 30
    time_limit_s: float = 5.0
    use_cpsat: bool = True
    spec: SolverSpec | None = None

    @property
    def resolved_spec(self) -> SolverSpec | None:
        if self.spec is not None:
            return self.spec
        return self.profile.solver_spec


def _parse_float_list(token: str, expected: int, label: str) -> list[float]:
    parts = [p.strip() for p in token.split(",") if p.strip() != ""]
    if len(parts) == 1 and expected > 1:
        values = [float(parts[0])] + [0.0] * (expected - 1)
        return values
    if len(parts) != expected:
        raise OptimizeInputError(
            f"{label} : {expected} valeur(s) attendue(s) pour {expected} carac(s), "
            f"reçu {len(parts)}"
        )
    try:
        return [float(p) for p in parts]
    except ValueError as exc:
        raise OptimizeInputError(f"{label} invalide : {token!r}") from exc


def _stats_for_names(names: Sequence[str], values: Sequence[float]) -> Stats:
    return Stats({name: float(values[i]) for i, name in enumerate(names)})


def _parse_kv_pairs(values: Sequence[str] | None, label: str) -> dict[str, float]:
    """Parse STAT=valeur (ex: INT=1200 intelligence=2)."""
    result: dict[str, float] = {}
    if not values:
        return result
    for token in values:
        if "=" not in token:
            raise OptimizeInputError(f"{label} invalide : {token!r} (attendu STAT=valeur)")
        key, raw = token.split("=", 1)
        try:
            name = canonical_stat_name(key)
            result[name] = float(raw)
        except (KeyError, ValueError) as exc:
            raise OptimizeInputError(f"{label} invalide : {token!r}") from exc
    return result


def parse_optimize_request(
    *,
    demo: bool = False,
    level: int | None = None,
    max_stats: Sequence[str] | None = None,
    base_int: float = 0.0,
    base_vit: float = 0.0,
    base_str: float = 0.0,
    base_cha: float = 0.0,
    base_agi: float = 0.0,
    base_wis: float = 0.0,
    scroll_int: float = 0.0,
    scroll_vit: float = 0.0,
    scroll_str: float = 0.0,
    scroll_cha: float = 0.0,
    scroll_agi: float = 0.0,
    scroll_wis: float = 0.0,
    jet: JetMode = "average",
    classic_only: bool = False,
    top_k: int = 30,
    time_limit_s: float = 5.0,
    use_cpsat: bool = True,
    targets: Sequence[str] | None = None,
    weights: Sequence[str] | None = None,
    ban_ids: Sequence[int] | None = None,
    force_ids: Sequence[int] | None = None,
    seed: int | None = None,
    stop_when_satisfied: bool = False,
    auto_distribute_points: bool = False,
    allow_power_for_caracs: bool = False,
    allow_damages_for_elemental: bool = False,
    allow_crit_damages_for_elemental: bool = False,
) -> OptimizeRequest:
    """Construit une requête depuis des champs structurés (flags CLI)."""
    if demo:
        profile = CharacterProfile.for_demo_int_123()
        spec = profile.solver_spec
        assert spec is not None
        from dataclasses import replace

        spec = replace(
            spec,
            jet_mode=jet,
            top_k=top_k,
            time_limit_s=time_limit_s,
            use_cpsat=use_cpsat,
            seed=seed,
            stop_when_satisfied=stop_when_satisfied,
            auto_distribute_points=auto_distribute_points,
            allow_power_for_caracs=allow_power_for_caracs,
            allow_damages_for_elemental=allow_damages_for_elemental,
            allow_crit_damages_for_elemental=allow_crit_damages_for_elemental,
            blacklist_ids=frozenset(int(x) for x in (ban_ids or [])),
            forced_ids=frozenset(int(x) for x in (force_ids or [])),
        )
        if classic_only:
            spec = spec.with_classic_only()
        profile = spec_to_profile(spec)
        return OptimizeRequest(
            profile=profile,
            classic_only=classic_only,
            top_k=top_k,
            time_limit_s=time_limit_s,
            use_cpsat=use_cpsat,
            spec=spec,
        )

    if level is None or not max_stats:
        raise OptimizeInputError("--level et --max sont requis (ou utilisez --demo)")

    names = [canonical_stat_name(s) for s in max_stats]
    base = Stats(
        {
            "Intelligence": float(base_int),
            "Vitalité": float(base_vit),
            "Force": float(base_str),
            "Chance": float(base_cha),
            "Agilité": float(base_agi),
            "Sagesse": float(base_wis),
        }
    )
    scrolls = Stats(
        {
            "Intelligence": float(scroll_int),
            "Vitalité": float(scroll_vit),
            "Force": float(scroll_str),
            "Chance": float(scroll_cha),
            "Agilité": float(scroll_agi),
            "Sagesse": float(scroll_wis),
        }
    )
    spec = profile_from_legacy(
        level=int(level),
        max_stats=names,
        base_stats=base,
        scrolls=scrolls,
        jet_mode=jet,
        classic_only=classic_only,
        top_k=top_k,
        time_limit_s=time_limit_s,
        use_cpsat=use_cpsat,
    )

    goals = dict(spec.goals)
    for name, target in _parse_kv_pairs(targets, "--target").items():
        g = goals.get(name, StatGoal())
        goals[name] = StatGoal(
            base=g.base, points=g.points, target=target, weight=g.weight or 1.0, exo=g.exo, scroll=g.scroll
        )
    for name, weight in _parse_kv_pairs(weights, "--weight").items():
        g = goals.get(name, StatGoal())
        goals[name] = StatGoal(
            base=g.base, points=g.points, target=g.target, weight=weight, exo=g.exo, scroll=g.scroll
        )

    from dataclasses import replace

    spec = replace(
        spec,
        goals=goals,
        blacklist_ids=frozenset(int(x) for x in (ban_ids or [])),
        forced_ids=frozenset(int(x) for x in (force_ids or [])),
        seed=seed,
        stop_when_satisfied=stop_when_satisfied,
        auto_distribute_points=auto_distribute_points,
        allow_power_for_caracs=allow_power_for_caracs,
        allow_damages_for_elemental=allow_damages_for_elemental,
        allow_crit_damages_for_elemental=allow_crit_damages_for_elemental,
    )
    profile = spec_to_profile(spec)
    return OptimizeRequest(
        profile=profile,
        classic_only=classic_only,
        top_k=top_k,
        time_limit_s=time_limit_s,
        use_cpsat=use_cpsat,
        spec=spec,
    )


def parse_compact_line(
    line: str,
    *,
    top_k: int = 30,
    time_limit_s: float = 5.0,
    use_cpsat: bool = True,
) -> OptimizeRequest:
    """
    Parse une ligne compacte :

      demo
      demo classic
      123 intelligence 200 100
      123 int,vit 200,50 100,0 classic jet=max
    """
    raw = (line or "").strip()
    if not raw:
        raise OptimizeInputError("Saisie vide")

    tokens = raw.split()
    classic_only = False
    jet: JetMode = "average"
    positional: list[str] = []

    for token in tokens:
        lower = token.casefold()
        if lower == "classic":
            classic_only = True
            continue
        if lower.startswith("jet="):
            mode = token.split("=", 1)[1].strip().casefold()
            if mode not in {"min", "average", "max"}:
                raise OptimizeInputError(f"jet invalide : {mode!r} (min|average|max)")
            jet = mode  # type: ignore[assignment]
            continue
        positional.append(token)

    if not positional:
        raise OptimizeInputError("Saisie invalide — voir aide syntaxe")

    if positional[0].casefold() == "demo":
        if len(positional) > 1:
            raise OptimizeInputError("Après 'demo', seuls 'classic' et jet=… sont autorisés")
        return parse_optimize_request(
            demo=True,
            jet=jet,
            classic_only=classic_only,
            top_k=top_k,
            time_limit_s=time_limit_s,
            use_cpsat=use_cpsat,
        )

    try:
        level = int(positional[0])
    except ValueError as exc:
        raise OptimizeInputError(f"Niveau invalide : {positional[0]!r}") from exc

    if len(positional) < 2:
        raise OptimizeInputError("Indiquer au moins une caractéristique après le niveau")

    stat_names = [canonical_stat_name(s) for s in positional[1].split(",") if s.strip()]
    if not stat_names:
        raise OptimizeInputError("Aucune caractéristique valide")

    n = len(stat_names)
    base_values = [0.0] * n
    scroll_values = [0.0] * n

    if len(positional) >= 3:
        base_values = _parse_float_list(positional[2], n, "Bases")
    if len(positional) >= 4:
        scroll_values = _parse_float_list(positional[3], n, "Parchemins")
    if len(positional) > 4:
        raise OptimizeInputError(
            "Trop d'arguments — format : NIVEAU CARAC [BASE] [SCROLL] [classic] [jet=…]"
        )

    base = _stats_for_names(stat_names, base_values)
    scrolls = _stats_for_names(stat_names, scroll_values)
    spec = profile_from_legacy(
        level=level,
        max_stats=stat_names,
        base_stats=base,
        scrolls=scrolls,
        jet_mode=jet,
        classic_only=classic_only,
        top_k=top_k,
        time_limit_s=time_limit_s,
        use_cpsat=use_cpsat,
    )
    profile = spec_to_profile(spec)
    return OptimizeRequest(
        profile=profile,
        classic_only=classic_only,
        top_k=top_k,
        time_limit_s=time_limit_s,
        use_cpsat=use_cpsat,
        spec=spec,
    )


def prompt_optimize_interactive(
    *,
    input_fn=input,
    top_k: int = 30,
    time_limit_s: float = 5.0,
    use_cpsat: bool = True,
) -> OptimizeRequest:
    """Mode interactif CLI (prompts stdin)."""
    print("Optimiseur de stuff — mode interactif (Entrée = valeurs par défaut)")
    print("Astuce : saisissez 'demo' au niveau pour le profil exemple.")
    level_raw = input_fn("Niveau [demo] : ").strip()
    if not level_raw or level_raw.casefold() == "demo":
        classic_raw = input_fn("Classique seul (sans dofus/familier) [n] : ").strip().casefold()
        classic_only = classic_raw in {"o", "oui", "y", "yes", "1"}
        jet_raw = input_fn("Jets (min|average|max) [average] : ").strip().casefold() or "average"
        if jet_raw not in {"min", "average", "max"}:
            raise OptimizeInputError(f"jet invalide : {jet_raw!r}")
        return parse_optimize_request(
            demo=True,
            jet=jet_raw,  # type: ignore[arg-type]
            classic_only=classic_only,
            top_k=top_k,
            time_limit_s=time_limit_s,
            use_cpsat=use_cpsat,
        )

    try:
        level = int(level_raw)
    except ValueError as exc:
        raise OptimizeInputError(f"Niveau invalide : {level_raw!r}") from exc

    stats_raw = input_fn("Caractéristique(s) à maxer (ex: intelligence) : ").strip()
    if not stats_raw:
        raise OptimizeInputError("Au moins une caractéristique est requise")
    max_stats = [s.strip() for s in stats_raw.replace(";", ",").split(",") if s.strip()]

    def _ask_float(label: str, default: float = 0.0) -> float:
        raw = input_fn(f"{label} [{default:g}] : ").strip()
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError as exc:
            raise OptimizeInputError(f"Nombre invalide pour {label} : {raw!r}") from exc

    primary = canonical_stat_name(max_stats[0])
    base_primary = _ask_float(f"Base hors stuff ({primary})", 0.0)
    scroll_primary = _ask_float(f"Parchemin ({primary})", 0.0)

    kwargs: dict[str, float] = {}
    alias = {
        "Intelligence": ("base_int", "scroll_int"),
        "Vitalité": ("base_vit", "scroll_vit"),
        "Force": ("base_str", "scroll_str"),
        "Chance": ("base_cha", "scroll_cha"),
        "Agilité": ("base_agi", "scroll_agi"),
        "Sagesse": ("base_wis", "scroll_wis"),
    }
    if primary in alias:
        bkey, skey = alias[primary]
        kwargs[bkey] = base_primary
        kwargs[skey] = scroll_primary

    classic_raw = input_fn("Classique seul (sans dofus/familier) [n] : ").strip().casefold()
    classic_only = classic_raw in {"o", "oui", "y", "yes", "1"}
    jet_raw = input_fn("Jets (min|average|max) [average] : ").strip().casefold() or "average"
    if jet_raw not in {"min", "average", "max"}:
        raise OptimizeInputError(f"jet invalide : {jet_raw!r}")

    return parse_optimize_request(
        level=level,
        max_stats=max_stats,
        jet=jet_raw,  # type: ignore[arg-type]
        classic_only=classic_only,
        top_k=top_k,
        time_limit_s=time_limit_s,
        use_cpsat=use_cpsat,
        **kwargs,
    )


def needs_interactive_optimize(args) -> bool:
    """True si aucun profil n'est fourni via flags."""
    if getattr(args, "demo", False):
        return False
    if getattr(args, "level", None) is not None:
        return False
    if getattr(args, "max_stats", None):
        return False
    return True
