"""Synchronisation de la base locale depuis l'API Dofusdude."""

from __future__ import annotations

import time
from typing import Any

from dofus_stuff.api import SYNC_SOURCES, SYNC_TIMEOUT, api_get, fetch_version
from dofus_stuff.database import META_GAME_VERSION, Database

CHECK_INTERVAL_SECONDS = 24 * 60 * 60


def ensure_up_to_date(
    db: Database,
    *,
    force: bool = False,
    offline: bool = False,
    timeout: int | None = None,
    quiet: bool = False,
) -> dict[str, Any]:
    """
    Vérifie la version API si le dernier check date de >24h (ou si force).
    Resynchronise toute la DB si la version a changé ou si la base est vide.
    """
    db.open()
    now = time.time()
    last_checked = db.last_checked_at()
    local_version = db.game_version()
    empty = db.is_empty()

    needs_check = force or empty or last_checked is None or (now - last_checked) >= CHECK_INTERVAL_SECONDS
    if not needs_check:
        return {
            "action": "skip",
            "reason": "within_24h",
            "game_version": local_version,
            "counts": db.counts_by_kind(),
        }

    if offline:
        if empty:
            raise RuntimeError("Base locale vide et --offline : impossible de synchroniser")
        return {
            "action": "skip",
            "reason": "offline",
            "game_version": local_version,
            "counts": db.counts_by_kind(),
        }

    remote_version = fetch_version(timeout=timeout)
    if (
        not force
        and not empty
        and local_version == remote_version
    ):
        db.touch_checked_at(now)
        if not quiet:
            print(f"Base à jour (version {remote_version}).")
        return {
            "action": "touch",
            "game_version": remote_version,
            "counts": db.counts_by_kind(),
        }

    counts = pull_all(db, version=remote_version, timeout=timeout, quiet=quiet)
    return {
        "action": "sync",
        "game_version": remote_version,
        "counts": counts,
    }


def pull_all(
    db: Database,
    *,
    version: str | None = None,
    timeout: int | None = None,
    quiet: bool = False,
) -> dict[str, int]:
    """Télécharge toutes les sources /all et remplace le contenu local."""
    db.open()
    if version is None:
        version = fetch_version(timeout=timeout)

    effective_timeout = SYNC_TIMEOUT if timeout is None else max(timeout, SYNC_TIMEOUT)
    started = time.time()
    counts: dict[str, int] = {}

    if not quiet:
        print(f"Synchronisation de la base locale (version {version})…")

    for list_path, collection_key, kind in SYNC_SOURCES:
        if not quiet:
            print(f"  → {kind}…", flush=True)
        payload = api_get(list_path, timeout=effective_timeout)
        if not isinstance(payload, dict):
            raise RuntimeError(f"Réponse liste inattendue pour {list_path}")
        entries = payload.get(collection_key)
        if not isinstance(entries, list):
            raise RuntimeError(f"Clé {collection_key!r} manquante pour {list_path}")

        typed_entries = [e for e in entries if isinstance(e, dict)]
        n = db.replace_kind(kind, typed_entries)
        counts[kind] = n
        if not quiet:
            print(f"    {n} entrée(s)", flush=True)

    db.set_meta(META_GAME_VERSION, version)
    db.touch_checked_at()
    if not quiet:
        total = sum(counts.values())
        elapsed = time.time() - started
        print(f"Base synchronisée : {total} entrée(s) en {elapsed:.1f}s.")
    return counts
