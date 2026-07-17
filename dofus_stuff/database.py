"""Stockage SQLite de la copie locale de la DB Dofus."""

from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

DB_NAME = "dofus.sqlite3"
DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / ".data"

META_GAME_VERSION = "game_version"
META_LAST_CHECKED_AT = "last_checked_at"

ITEM_KINDS = (
    "equipment",
    "resources",
    "consumables",
    "quest",
    "cosmetics",
    "mounts",
    "sets",
)


@dataclass
class Database:
    data_dir: Path
    _conn: sqlite3.Connection | None = field(default=None, init=False, repr=False)

    @property
    def path(self) -> Path:
        return self.data_dir / DB_NAME

    def open(self) -> None:
        if self._conn is not None:
            return
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                kind TEXT NOT NULL,
                ankama_id INTEGER NOT NULL,
                payload TEXT NOT NULL,
                PRIMARY KEY (kind, ankama_id)
            )
            """
        )
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_items_kind ON items (kind)")
        self._conn.commit()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _require_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self.open()
        assert self._conn is not None
        return self._conn

    def get_meta(self, key: str) -> str | None:
        conn = self._require_conn()
        row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        conn = self._require_conn()
        conn.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
            (key, value),
        )
        conn.commit()

    def game_version(self) -> str | None:
        return self.get_meta(META_GAME_VERSION)

    def last_checked_at(self) -> float | None:
        raw = self.get_meta(META_LAST_CHECKED_AT)
        if raw is None:
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    def touch_checked_at(self, when: float | None = None) -> None:
        self.set_meta(META_LAST_CHECKED_AT, str(when if when is not None else time.time()))

    def item_count(self) -> int:
        conn = self._require_conn()
        return int(conn.execute("SELECT COUNT(*) FROM items").fetchone()[0])

    def counts_by_kind(self) -> dict[str, int]:
        conn = self._require_conn()
        rows = conn.execute(
            "SELECT kind, COUNT(*) FROM items GROUP BY kind ORDER BY kind"
        ).fetchall()
        return {kind: count for kind, count in rows}

    def is_empty(self) -> bool:
        return self.item_count() == 0

    def replace_kind(self, kind: str, entries: list[dict[str, Any]]) -> int:
        """Remplace toutes les lignes d'un kind. Retourne le nombre d'entrées écrites."""
        conn = self._require_conn()
        rows: list[tuple[str, int, str]] = []
        for entry in entries:
            ankama_id = entry.get("ankama_id")
            if not isinstance(ankama_id, int):
                continue
            rows.append((kind, ankama_id, json.dumps(entry, ensure_ascii=False)))

        conn.execute("DELETE FROM items WHERE kind = ?", (kind,))
        conn.executemany(
            "INSERT INTO items (kind, ankama_id, payload) VALUES (?, ?, ?)",
            rows,
        )
        conn.commit()
        return len(rows)

    def iter_items(self) -> Iterator[tuple[str, int, dict[str, Any]]]:
        conn = self._require_conn()
        rows = conn.execute("SELECT kind, ankama_id, payload FROM items").fetchall()
        for kind, ankama_id, payload in rows:
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict):
                yield kind, int(ankama_id), data

    def clear(self) -> int:
        """Vide items + meta. Retourne le nombre d'items supprimés."""
        conn = self._require_conn()
        cur = conn.execute("DELETE FROM items")
        conn.execute("DELETE FROM meta")
        conn.commit()
        return cur.rowcount

    def stats(self) -> dict[str, Any]:
        last_checked = self.last_checked_at()
        return {
            "path": str(self.path),
            "game_version": self.game_version(),
            "last_checked_at": last_checked,
            "total_items": self.item_count(),
            "by_kind": self.counts_by_kind(),
        }
