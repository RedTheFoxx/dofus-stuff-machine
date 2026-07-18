"""Export d'un stuff vers Dofusbook (URL d'import Dofus-Stuffer).

Format reverse-engineered depuis le bundle Dofusbook :
l'URL ``/fr/equipement/dofus-stuffer/objets?stuff=<BASE64>`` attend un payload
MessagePack de la forme::

    [caracs_finales[51], points[51], niveau, flags, counts[10], ids_a_plat]

Les 10 groupes Dofusbook sont, dans l'ordre :
cape, coiffe, ceinture, bottes, amulette, anneaux (2), dofus (6), bouclier,
arme, familier. Les ``ids`` sont les IDs Ankama, a plat, ordonnés par groupe.
"""

from __future__ import annotations

import base64
from typing import Any, Mapping

import msgpack

DOFUSBOOK_IMPORT_URL = "https://www.dofusbook.net/fr/equipement/dofus-stuffer/objets"

# Ordre des 10 groupes de slots attendus par l'import Dofusbook
# (cf. ``gs=[[x.ca],[x.ch],[x.ce],...]`` dans le bundle : ca=cape, ch=chapeau).
# Pour chaque groupe, la liste ordonnée des slot_instances du solveur.
_GROUP_SLOTS: tuple[tuple[str, ...], ...] = (
    ("cape",),  # 0 cape (ca)
    ("hat",),  # 1 coiffe (ch)
    ("belt",),  # 2 ceinture (ce)
    ("boots",),  # 3 bottes (bo)
    ("amulet",),  # 4 amulette (am)
    ("ring_a", "ring_b"),  # 5 anneaux (a1, a2)
    ("dofus_1", "dofus_2", "dofus_3", "dofus_4", "dofus_5", "dofus_6"),  # 6 dofus
    ("shield",),  # 7 bouclier (br)
    ("weapon",),  # 8 arme (ar)
    ("pet",),  # 9 familier/monture (fa)
)

_CARAC_COUNT = 51


def _item_id(item: Any) -> int | None:
    if isinstance(item, Mapping):
        aid = item.get("ankama_id")
        if isinstance(aid, int):
            return aid
    return None


def build_dofusbook_url(
    slots_by_instance: Mapping[str, Any],
    level: int,
) -> str:
    """Construit l'URL Dofusbook pré-remplie pour un stuff.

    ``slots_by_instance`` mappe ``slot_instance -> payload item`` (dict avec
    ``ankama_id``) ou directement ``slot_instance -> ankama_id``.
    """
    counts: list[int] = []
    flat_ids: list[int] = []
    for group in _GROUP_SLOTS:
        n = 0
        for slot in group:
            raw = slots_by_instance.get(slot)
            aid = raw if isinstance(raw, int) else _item_id(raw)
            if aid is None:
                continue
            flat_ids.append(aid)
            n += 1
        counts.append(n)

    caracs = [0] * _CARAC_COUNT
    points = [0] * _CARAC_COUNT
    flags = 0
    payload = [caracs, points, int(level), flags, counts, flat_ids]
    packed = msgpack.packb(payload, use_bin_type=True)
    token = base64.b64encode(packed).decode("ascii")
    return f"{DOFUSBOOK_IMPORT_URL}?stuff={token}"
