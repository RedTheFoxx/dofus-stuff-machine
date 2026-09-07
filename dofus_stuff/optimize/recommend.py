"""Opinionated, editable defaults for the three-question recommendation flow."""

from dofus_stuff.model.solver_spec import SolverSpec, StatGoal, characteristic_point_cost

CLASSES = (
    "Cra", "Ecaflip", "Eliotrope", "Eniripsa", "Enutrof", "Feca",
    "Forgelance", "Huppermage", "Iop", "Osamodas", "Ouginak", "Pandawa",
    "Roublard", "Sacrieur", "Sadida", "Sram", "Steamer", "Xelor", "Zobal",
)
ELEMENTS = {"terre": "Force", "feu": "Intelligence", "eau": "Chance", "air": "Agilité"}


def recommendation_spec(character_class: str, elements: list[str], level: int) -> SolverSpec:
    if character_class not in CLASSES:
        raise ValueError("Choisissez une classe de la liste.")
    if not 1 <= level <= 200:
        raise ValueError("Le niveau doit être compris entre 1 et 200.")
    if not elements or any(e not in ELEMENTS for e in elements):
        raise ValueError("Choisissez terre, feu, eau et/ou air.")
    elements = list(dict.fromkeys(elements))
    names = [ELEMENTS[e] for e in elements]
    # Equal investment, with the actual cost of each next characteristic point.
    points = dict.fromkeys(names, 0)
    capital = 5 * (level - 1)
    while capital:
        name = min(names, key=lambda n: points[n])
        cost = characteristic_point_cost(points[name])
        if cost > capital:
            break
        points[name] += 1
        capital -= cost
    goals = {n: StatGoal(points=points[n], weight=1 / len(names)) for n in names}
    for element in elements:
        goals[f"Dommage {element.title()}"] = StatGoal(weight=3 / len(names))
    pa = 6 if level < 40 else 8 if level < 100 else 10 if level < 150 else 11
    pm = 3 if level < 40 else 4 if level < 100 else 5 if level < 150 else 6
    goals.update({
        "PA": StatGoal(base=6 + int(level >= 100), target=pa, weight=150),
        "PM": StatGoal(base=3, target=pm, weight=120),
        "Vitalité": StatGoal(points=capital, target=level * 12, weight=0.15),
        "% Dommages aux sorts": StatGoal(weight=12),
        "% Critique": StatGoal(target=35, weight=2),
    })
    # Broad playstyle preferences, not a simulation of class spells.
    if character_class in {"Cra", "Enutrof", "Sadida", "Eniripsa", "Steamer", "Osamodas"}:
        goals["% Dommages distance"] = StatGoal(weight=12)
    elif character_class in {"Iop", "Sacrieur", "Ouginak", "Zobal"}:
        goals["% Dommages mêlée"] = StatGoal(weight=12)
    for element in ELEMENTS:
        goals[f"% Résistance {element.title()}"] = StatGoal(target=25, weight=2)
    if character_class in {"Cra", "Enutrof", "Sadida"}:
        goals["Portée"] = StatGoal(target=2 if level < 100 else 4, weight=20)
    if character_class in {"Osamodas", "Sadida"}:
        goals["Invocation"] = StatGoal(base=1, target=3, weight=35)
    return SolverSpec(
        level=level, goals=goals, allow_power_for_caracs=True,
        allow_damages_for_elemental=True, balanced_elements=tuple(names),
        enabled_slot_groups=("amulet", "rings", "belt", "boots", "hat", "cape",
                             "weapon", "shield", "dofus", "pet", "prysma"),
        top_k=40, time_limit_s=8,
    )
