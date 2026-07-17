#!/usr/bin/env python3
"""Shim CLI — délègue à dofus_stuff.cli (rétrocompatibilité)."""

from __future__ import annotations

from dofus_stuff.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
