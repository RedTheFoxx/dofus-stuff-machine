"""Client HTTP minimal vers l'API Dofusdude."""

from __future__ import annotations

import gzip
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://api.dofusdu.de/dofus3/v1"
DEFAULT_TIMEOUT = 15
SYNC_TIMEOUT = 120
MAX_RETRIES = 3

# (chemin /all, clé JSON des entrées, kind stocké en base)
SYNC_SOURCES: tuple[tuple[str, str, str], ...] = (
    ("/fr/items/equipment/all", "items", "equipment"),
    ("/fr/items/resources/all", "items", "resources"),
    ("/fr/items/consumables/all", "items", "consumables"),
    ("/fr/items/quest/all", "items", "quest"),
    ("/fr/items/cosmetics/all", "items", "cosmetics"),
    ("/fr/mounts/all", "mounts", "mounts"),
    ("/fr/sets/all", "sets", "sets"),
)


def api_get(
    path: str,
    params: dict[str, Any] | None = None,
    *,
    timeout: int | None = None,
) -> dict[str, Any] | list[Any]:
    effective_timeout = DEFAULT_TIMEOUT if timeout is None else timeout
    query = urllib.parse.urlencode(params or {}, doseq=True)
    url = f"{BASE_URL}{path}"
    if query:
        url = f"{url}?{query}"

    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "dofus-stuff-machine/0.2",
                },
            )
            with urllib.request.urlopen(request, timeout=effective_timeout) as response:
                raw = response.read()
                encoding = (response.headers.get("Content-Encoding") or "").lower()
                if encoding == "gzip" or raw[:2] == b"\x1f\x8b":
                    raw = gzip.decompress(raw)
                return json.loads(raw.decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < MAX_RETRIES - 1:
                time.sleep(0.5 * (attempt + 1))

    raise RuntimeError(f"Échec API après {MAX_RETRIES} tentatives: {url}") from last_error


def fetch_version(*, timeout: int | None = None) -> str:
    payload = api_get("/meta/version", timeout=timeout)
    if not isinstance(payload, dict):
        raise RuntimeError("Réponse version inattendue")
    version = payload.get("version")
    if not isinstance(version, str):
        raise RuntimeError("Champ version manquant")
    return version
