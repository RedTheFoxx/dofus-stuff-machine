"""Normalisation et agrégation des effets numériques."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Literal, Mapping

JetMode = Literal["min", "average", "max"]

# IDs Dofusdude (effects[].type.id) — parité Stuffer Joueur.
STAT_IDS: dict[str, int] = {
    # Caracs principales
    "Vitalité": 9,
    "Sagesse": 10,
    "Intelligence": 13,
    "Chance": 22,
    "Agilité": 36,
    "Force": 45,
    # PA / PM / PO
    "PA": 12,
    "PM": 8,
    "Portée": 31,
    # Résistances %
    "% Résistance Neutre": 34,
    "% Résistance Terre": 63,
    "% Résistance Feu": 37,
    "% Résistance Eau": 17,
    "% Résistance Air": 16,
    # Résistances fixes
    "Résistance Neutre": 33,
    "Résistance Terre": 15,
    "Résistance Feu": 14,
    "Résistance Eau": 82,
    "Résistance Air": 60,
    "Résistance Critiques": 46,
    "Résistance Poussée": 70,
    "% Résistance distance": 108,
    "% Résistance mêlée": 65,
    # Dommages
    "Dommage": 30,
    "Puissance": 32,
    "Dommage Critiques": 38,
    "Dommage Neutre": 49,
    "Dommage Terre": 48,
    "Dommage Feu": 61,
    "Dommage Eau": 27,
    "Dommage Air": 47,
    "Dommage Pièges": 112,
    "Puissance Pièges": 106,
    "Dommage Poussée": 62,
    "% Dommages aux sorts": 93,
    "% Dommages d'armes": 41,
    "% Dommages mêlée": 40,
    "% Dommages distance": 71,
    # Divers
    "Initiative": 24,
    "Prospection": 25,
    "Invocation": 28,
    "Retrait PA": 64,
    "Esquive PA": 75,
    "Retrait PM": 50,
    "Esquive PM": 39,
    "% Critique": 29,
    "Soin": 121,
    "Tacle": 26,
    "Fuite": 59,
    "Pod": 220,
}

# Corriger % Résistance armes si présent sous un autre id en DB — on garde le nom.
STAT_NAMES: dict[int, str] = {stat_id: name for name, stat_id in STAT_IDS.items()}

# Alias de noms d'objectif / saisie utilisateur → nom canonique.
STAT_ALIASES: dict[str, str] = {
    "vit": "Vitalité",
    "vitalite": "Vitalité",
    "vitalité": "Vitalité",
    "sage": "Sagesse",
    "sagesse": "Sagesse",
    "int": "Intelligence",
    "intel": "Intelligence",
    "intelligence": "Intelligence",
    "cha": "Chance",
    "chance": "Chance",
    "agi": "Agilité",
    "agilite": "Agilité",
    "agilité": "Agilité",
    "fo": "Force",
    "force": "Force",
    "pa": "PA",
    "pm": "PM",
    "po": "Portée",
    "portee": "Portée",
    "portée": "Portée",
    "crit": "% Critique",
    "%crit": "% Critique",
    "puissance": "Puissance",
    "power": "Puissance",
    "dommage": "Dommage",
    "dommages": "Dommage",
    "dmg": "Dommage",
    "dommage_critiques": "Dommage Critiques",
    "dommages_critiques": "Dommage Critiques",
    "initiative": "Initiative",
    "prospection": "Prospection",
    "pp": "Prospection",
    "invocation": "Invocation",
    "invoc": "Invocation",
    "soin": "Soin",
    "soins": "Soin",
    "tacle": "Tacle",
    "fuite": "Fuite",
    "pod": "Pod",
    "pods": "Pod",
}


def canonical_stat_name(name: str) -> str:
    """Résout un libellé libre vers le nom d'effet canonique."""
    stripped = name.strip()
    if stripped in STAT_IDS:
        return stripped
    key = stripped.casefold()
    if key in STAT_ALIASES:
        return STAT_ALIASES[key]
    # Match insensible à la casse sur les noms connus
    for known in STAT_IDS:
        if known.casefold() == key:
            return known
    raise KeyError(f"Caractéristique inconnue : {name!r}")


@dataclass
class Stats:
    """Map nom de carac → valeur (float pour les jets moyens)."""

    values: dict[str, float] = field(default_factory=dict)

    def get(self, name: str, default: float = 0.0) -> float:
        return self.values.get(name, default)

    def add_inplace(self, other: Mapping[str, float] | Stats) -> None:
        src = other.values if isinstance(other, Stats) else other
        for key, value in src.items():
            self.values[key] = self.values.get(key, 0.0) + float(value)

    def __add__(self, other: Stats) -> Stats:
        result = Stats(dict(self.values))
        result.add_inplace(other)
        return result

    def copy(self) -> Stats:
        return Stats(dict(self.values))

    def as_int_dict(self) -> dict[str, int]:
        return {k: int(round(v)) for k, v in self.values.items()}


def effect_numeric_value(effect: Mapping[str, Any], mode: JetMode = "average") -> float | None:
    """Extrait la valeur numérique d'un effet passif, ou None si non agrégable."""
    effect_type = effect.get("type")
    if not isinstance(effect_type, dict):
        return None
    if effect_type.get("is_active") or effect_type.get("is_meta"):
        return None

    type_id = effect_type.get("id")
    type_name = effect_type.get("name")
    if type_id not in STAT_NAMES and type_name not in STAT_IDS:
        return None

    lo = int(effect.get("int_minimum") or 0)
    hi = int(effect.get("int_maximum") or 0)
    if effect.get("ignore_int_max"):
        return float(lo)
    if mode == "min":
        return float(lo)
    if mode == "max":
        return float(hi if hi else lo)
    # average
    if hi:
        return (lo + hi) / 2.0
    return float(lo)


def effect_stat_name(effect: Mapping[str, Any]) -> str | None:
    effect_type = effect.get("type")
    if not isinstance(effect_type, dict):
        return None
    type_id = effect_type.get("id")
    if isinstance(type_id, int) and type_id in STAT_NAMES:
        return STAT_NAMES[type_id]
    name = effect_type.get("name")
    if isinstance(name, str) and name in STAT_IDS:
        return name
    return None


def effects_to_stats(
    effects: Iterable[Mapping[str, Any]] | None,
    *,
    mode: JetMode = "average",
) -> Stats:
    """Agrège une liste d'effets en Stats (passifs reconnus uniquement)."""
    result = Stats()
    if not effects:
        return result
    for effect in effects:
        name = effect_stat_name(effect)
        if name is None:
            continue
        value = effect_numeric_value(effect, mode)
        if value is None:
            continue
        result.values[name] = result.values.get(name, 0.0) + value
    return result


def weighted_score(stats: Stats, weights: Mapping[str, float]) -> float:
    """Score scalaire Σ w_stat * valeur_stat."""
    total = 0.0
    for name, weight in weights.items():
        if weight == 0:
            continue
        total += float(weight) * stats.get(name, 0.0)
    return total
