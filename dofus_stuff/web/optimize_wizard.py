"""Wizard multi-écrans pour configurer SolverSpec (UI terminal)."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from dofus_stuff.model.solver_spec import (
    EXO_STATS,
    MAIN_CARACS,
    SLOT_GROUPS,
    TYPE_FILTER_KEYS,
    SolverSpec,
    StatGoal,
    default_player_spec,
    spec_to_profile,
)
from dofus_stuff.optimize.profile_input import OptimizeRequest

SESSION_WIZARD = "optimize_wizard"
SESSION_WIZARD_EDIT = "optimize_wizard_edit"

WIZARD_STEPS: tuple[str, ...] = (
    "slots",
    "options",
    "caracs",
    "papmpo",
    "resistances",
    "damages",
    "misc",
    "items",
    "recap",
)

STEP_TITLES: dict[str, str] = {
    "slots": "SLOTS ET FILTRES",
    "options": "OPTIONS SOLVEUR",
    "caracs": "CARACTERISTIQUES",
    "papmpo": "PA / PM / PO",
    "resistances": "RESISTANCES",
    "damages": "DOMMAGES",
    "misc": "DIVERS",
    "items": "ITEMS INTERDITS / FORCES",
    "recap": "RECAPITULATIF",
}

RESISTANCE_STATS: tuple[str, ...] = (
    "% Résistance Neutre",
    "% Résistance Terre",
    "% Résistance Feu",
    "% Résistance Eau",
    "% Résistance Air",
    "Résistance Neutre",
    "Résistance Terre",
    "Résistance Feu",
    "Résistance Eau",
    "Résistance Air",
    "Résistance Critiques",
    "Résistance Poussée",
    "% Résistance distance",
    "% Résistance mêlée",
)

DAMAGE_STATS: tuple[str, ...] = (
    "Dommage",
    "Puissance",
    "Dommage Critiques",
    "Dommage Neutre",
    "Dommage Terre",
    "Dommage Feu",
    "Dommage Eau",
    "Dommage Air",
    "Dommage Pièges",
    "Puissance Pièges",
    "Dommage Poussée",
    "% Dommages aux sorts",
    "% Dommages d'armes",
    "% Dommages mêlée",
    "% Dommages distance",
)

MISC_STATS: tuple[str, ...] = (
    "Initiative",
    "Prospection",
    "Invocation",
    "Retrait PA",
    "Esquive PA",
    "Retrait PM",
    "Esquive PM",
    "% Critique",
    "Soin",
    "Tacle",
    "Fuite",
    "Pod",
)

SLOT_GROUP_LABELS: dict[str, str] = {
    "amulet": "AMULETTE",
    "rings": "ANNEAUX",
    "belt": "CEINTURE",
    "boots": "BOTTES",
    "hat": "COIFFE",
    "cape": "CAPE",
    "weapon": "ARME",
    "shield": "BOUCLIER",
    "dofus": "DOFUS/TROPHEES",
    "pet": "FAMILIER/MONTURE",
    "prysma": "PRYSMARADITE",
}

TYPE_FILTER_LABELS: dict[str, str] = {
    "familier": "FAMILIER",
    "montilier": "MONTILIER",
    "dragodinde": "DRAGODINDE",
    "muldo": "MULDO",
    "volkorne": "VOLKORNE",
    "arme_distance": "ARMES DISTANCE",
    "arme_melee": "ARMES MELEE",
    "dofus": "DOFUS",
    "trophee": "TROPHEE",
    "prysmaradite": "PRYSMARADITE",
}


def load_wizard_spec(session_obj: Any) -> SolverSpec:
    raw = session_obj.get(SESSION_WIZARD)
    if isinstance(raw, dict):
        return SolverSpec.from_dict(raw)
    return default_player_spec(level=200)


def save_wizard_spec(session_obj: Any, spec: SolverSpec) -> None:
    session_obj[SESSION_WIZARD] = spec.to_dict()


def reset_wizard(session_obj: Any) -> SolverSpec:
    spec = default_player_spec(level=200)
    save_wizard_spec(session_obj, spec)
    session_obj.pop(SESSION_WIZARD_EDIT, None)
    return spec


def next_step(step: str) -> str | None:
    try:
        idx = WIZARD_STEPS.index(step)
    except ValueError:
        return None
    if idx + 1 >= len(WIZARD_STEPS):
        return None
    return WIZARD_STEPS[idx + 1]


def prev_step(step: str) -> str | None:
    try:
        idx = WIZARD_STEPS.index(step)
    except ValueError:
        return None
    if idx <= 0:
        return None
    return WIZARD_STEPS[idx - 1]


def _on_off(flag: bool) -> str:
    return "ON " if flag else "OFF"


def _goal_line(name: str, goal: StatGoal, *, with_exo: bool = False) -> str:
    if with_exo:
        return (
            f"{name[:18]:18s} B={goal.base:g} E={goal.exo:g} "
            f"C={goal.target:g} W={goal.weight:g}"
        )
    return (
        f"{name[:18]:18s} B={goal.base:g} P={goal.points:g} "
        f"C={goal.target:g} W={goal.weight:g}"
    )


def body_slots(spec: SolverSpec) -> list[str]:
    lines = ["SLOTS (N=TOGGLE) :", ""]
    groups = list(SLOT_GROUPS.keys())
    enabled = set(spec.enabled_slot_groups)
    for i, group in enumerate(groups, start=1):
        flag = group in enabled
        label = SLOT_GROUP_LABELS.get(group, group.upper())
        lines.append(f"{i:2d}. [{_on_off(flag)}] {label}")
    lines.append("")
    lines.append("FILTRES TYPES (F+N) :")
    for i, key in enumerate(TYPE_FILTER_KEYS, start=1):
        flag = spec.type_filters.get(key, True)
        label = TYPE_FILTER_LABELS.get(key, key.upper())
        lines.append(f"F{i}. [{_on_off(flag)}] {label}")
    lines.append("")
    lines.append("ENTREE=SUIVANT  N=TOGGLE SLOT  FN=TOGGLE FILTRE")
    lines.append("F7=ECRAN PREC  F8=ECRAN SUIV (OU PAGE)")
    return lines


def body_options(spec: SolverSpec) -> list[str]:
    return [
        "OPTIONS (N=EDIT) :",
        "",
        f"1. NIVEAU          = {spec.level}",
        f"2. JET             = {spec.jet_mode}",
        f"3. DUREE (S)       = {spec.time_limit_s:g}",
        f"4. SEED            = {spec.seed if spec.seed is not None else '(aucun)'}",
        f"5. TOP-K           = {spec.top_k}",
        f"6. CP-SAT          = {_on_off(spec.use_cpsat).strip()}",
        f"7. STOP SI CIBLES  = {_on_off(spec.stop_when_satisfied).strip()}",
        f"8. AUTO POINTS     = {_on_off(spec.auto_distribute_points).strip()}",
        f"9. ALLOW POWER     = {_on_off(spec.allow_power_for_caracs).strip()}",
        f"10. ALLOW DOMMAGES = {_on_off(spec.allow_damages_for_elemental).strip()}",
        f"11. ALLOW DOM CRIT = {_on_off(spec.allow_crit_damages_for_elemental).strip()}",
        "",
        "ENTREE=SUIVANT  N=CHOISIR OPTION",
        "F7=ECRAN PREC  F8=ECRAN SUIV",
    ]


def body_stat_list(
    title: str,
    names: tuple[str, ...],
    spec: SolverSpec,
    *,
    with_exo: bool = False,
    page: int = 1,
    page_size: int = 12,
) -> tuple[list[str], int, int]:
    total_pages = max(1, (len(names) + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    chunk = names[start : start + page_size]
    lines = [f"{title} (N=EDIT)  PAGE {page}/{total_pages}", ""]
    for i, name in enumerate(chunk, start=start + 1):
        goal = spec.goals.get(name, StatGoal())
        lines.append(f"{i:2d}. {_goal_line(name, goal, with_exo=with_exo)}")
    lines.append("")
    lines.append("ENTREE=SUIVANT  N=EDIT  F7/F8=PAGE PUIS ECRAN")
    return lines, page, total_pages


def body_items(spec: SolverSpec) -> list[str]:
    bans = sorted(spec.blacklist_ids)
    forced = sorted(spec.forced_ids)
    lines = [
        "ITEMS — SYNTAXE :",
        "  +ID   AJOUTER INTERDIT",
        "  -ID   AJOUTER FORCE",
        "  !ID   RETIRER (BAN OU FORCE)",
        "  CLEAR VIDER LISTES",
        "",
        f"INTERDITS ({len(bans)}) : {', '.join(f'#{i}' for i in bans[:8]) or '(aucun)'}",
    ]
    if len(bans) > 8:
        lines.append(f"  … +{len(bans) - 8}")
    lines.append(
        f"FORCES ({len(forced)}) : {', '.join(f'#{i}' for i in forced[:8]) or '(aucun)'}"
    )
    if len(forced) > 8:
        lines.append(f"  … +{len(forced) - 8}")
    lines.append("")
    lines.append("ENTREE=SUIVANT")
    lines.append("F7=ECRAN PREC  F8=ECRAN SUIV")
    return lines


def body_recap(spec: SolverSpec) -> list[str]:
    weighted = {k: v.weight for k, v in spec.goals.items() if v.weight}
    targets = {k: v.target for k, v in spec.goals.items() if v.target > 0}
    lines = [
        f"NIVEAU {spec.level}  JET={spec.jet_mode}  DUREE={spec.time_limit_s:g}s",
        f"SLOTS : {', '.join(spec.enabled_slot_groups)}",
        f"POIDS : {weighted or '(aucun — defaut INT)'}",
        f"CIBLES : {targets or '(aucune)'}",
        f"BAN={len(spec.blacklist_ids)} FORCE={len(spec.forced_ids)}",
        f"STOP={spec.stop_when_satisfied} AUTO={spec.auto_distribute_points}",
        f"POWER={spec.allow_power_for_caracs} DMG={spec.allow_damages_for_elemental} "
        f"CRIT={spec.allow_crit_damages_for_elemental}",
        "",
        "GO = LANCER  RESET = REINITIALISER",
        "1-8 = RETOUR ECRAN  F7=ECRAN PREC",
    ]
    return lines


def apply_slots_input(spec: SolverSpec, raw: str) -> SolverSpec:
    text = raw.strip().casefold()
    if not text:
        return spec
    groups = list(SLOT_GROUPS.keys())
    if text.startswith("f") and text[1:].isdigit():
        idx = int(text[1:]) - 1
        if 0 <= idx < len(TYPE_FILTER_KEYS):
            key = TYPE_FILTER_KEYS[idx]
            filters = dict(spec.type_filters)
            filters[key] = not filters.get(key, True)
            return replace(spec, type_filters=filters)
        raise ValueError("Filtre invalide")
    if text.isdigit():
        idx = int(text) - 1
        if 0 <= idx < len(groups):
            group = groups[idx]
            enabled = list(spec.enabled_slot_groups)
            if group in enabled:
                enabled = [g for g in enabled if g != group]
            else:
                # garder un ordre stable
                enabled = [g for g in groups if g in enabled or g == group]
            if not enabled:
                raise ValueError("Au moins un slot requis")
            return replace(spec, enabled_slot_groups=tuple(enabled))
        raise ValueError("Slot invalide")
    raise ValueError("Saisie invalide")


def apply_options_input(spec: SolverSpec, raw: str) -> tuple[SolverSpec, str | None]:
    """Retourne (spec, clé à éditer) — clé non None => sous-écran édition."""
    text = raw.strip()
    if not text:
        return spec, None
    if not text.isdigit():
        raise ValueError("Saisir un numero d'option")
    n = int(text)
    keys = {
        1: "level",
        2: "jet_mode",
        3: "time_limit_s",
        4: "seed",
        5: "top_k",
        6: "use_cpsat",
        7: "stop_when_satisfied",
        8: "auto_distribute_points",
        9: "allow_power_for_caracs",
        10: "allow_damages_for_elemental",
        11: "allow_crit_damages_for_elemental",
    }
    if n not in keys:
        raise ValueError("Option invalide")
    key = keys[n]
    # Toggles booléens immédiats
    if key in {
        "use_cpsat",
        "stop_when_satisfied",
        "auto_distribute_points",
        "allow_power_for_caracs",
        "allow_damages_for_elemental",
        "allow_crit_damages_for_elemental",
    }:
        return replace(spec, **{key: not getattr(spec, key)}), None
    return spec, key


def apply_option_value(spec: SolverSpec, key: str, raw: str) -> SolverSpec:
    text = raw.strip()
    if key == "level":
        return replace(spec, level=int(text))
    if key == "jet_mode":
        mode = text.casefold()
        if mode not in {"min", "average", "max"}:
            raise ValueError("jet = min|average|max")
        return replace(spec, jet_mode=mode)  # type: ignore[arg-type]
    if key == "time_limit_s":
        return replace(spec, time_limit_s=float(text))
    if key == "seed":
        if not text or text in {"-", "none", "aucun"}:
            return replace(spec, seed=None)
        return replace(spec, seed=int(text))
    if key == "top_k":
        return replace(spec, top_k=max(1, int(text)))
    raise ValueError(f"Clé inconnue : {key}")


def apply_stat_edit(
    spec: SolverSpec,
    name: str,
    raw: str,
    *,
    with_exo: bool = False,
) -> SolverSpec:
    parts = raw.replace(",", " ").split()
    if with_exo:
        if len(parts) != 4:
            raise ValueError("Format : BASE EXO CIBLE POIDS")
        base, exo, target, weight = (float(p) for p in parts)
        points = 0.0
    else:
        if len(parts) != 4:
            raise ValueError("Format : BASE POINTS CIBLE POIDS")
        base, points, target, weight = (float(p) for p in parts)
        exo = 0.0
    goals = dict(spec.goals)
    prev = goals.get(name, StatGoal())
    goals[name] = StatGoal(
        base=base,
        points=points,
        target=target,
        weight=weight,
        exo=exo,
        scroll=prev.scroll,
    )
    return replace(spec, goals=goals)


def apply_items_input(spec: SolverSpec, raw: str) -> SolverSpec:
    text = raw.strip()
    if not text:
        return spec
    upper = text.casefold()
    if upper == "clear":
        return replace(spec, blacklist_ids=frozenset(), forced_ids=frozenset())
    if text[0] in {"+", "-", "!"} and text[1:].isdigit():
        aid = int(text[1:])
        bans = set(spec.blacklist_ids)
        forced = set(spec.forced_ids)
        if text[0] == "+":
            bans.add(aid)
            forced.discard(aid)
        elif text[0] == "-":
            forced.add(aid)
            bans.discard(aid)
        else:
            bans.discard(aid)
            forced.discard(aid)
        return replace(
            spec,
            blacklist_ids=frozenset(bans),
            forced_ids=frozenset(forced),
        )
    raise ValueError("Syntaxe : +ID | -ID | !ID | CLEAR")


def spec_to_request(spec: SolverSpec) -> OptimizeRequest:
    profile = spec_to_profile(spec)
    return OptimizeRequest(
        profile=profile,
        classic_only=False,
        top_k=spec.top_k,
        time_limit_s=spec.time_limit_s,
        use_cpsat=spec.use_cpsat,
        spec=spec,
    )


def stat_names_for_step(step: str) -> tuple[str, ...] | None:
    if step == "caracs":
        return MAIN_CARACS
    if step == "papmpo":
        return EXO_STATS
    if step == "resistances":
        return RESISTANCE_STATS
    if step == "damages":
        return DAMAGE_STATS
    if step == "misc":
        return MISC_STATS
    return None
