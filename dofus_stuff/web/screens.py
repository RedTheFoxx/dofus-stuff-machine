"""Helpers de mise en page texte pour l'interface terminal 100x24."""

from __future__ import annotations

COLS = 100
ROWS = 24
HEADER_ROWS = 3
BODY_START = 4  # 1-indexed line
BODY_END = 21
BODY_LINES = BODY_END - BODY_START + 1  # 18
FOOTER_START = 22


def clip(text: str, width: int = COLS) -> str:
    """Tronque ou pad une ligne à exactement `width` caractères."""
    if len(text) > width:
        if width <= 1:
            return text[:width]
        return text[: width - 1] + "…"
    return text.ljust(width)


def wrap_line(text: str, width: int = COLS) -> list[str]:
    """Découpe une ligne trop longue en plusieurs lignes (coupure sur les espaces)."""
    if width < 1:
        return [text]
    if len(text) <= width:
        return [text]

    lines: list[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= width:
            lines.append(remaining)
            break
        split = remaining.rfind(" ", 0, width)
        if split <= 0:
            lines.append(remaining[:width])
            remaining = remaining[width:]
            continue
        lines.append(remaining[:split])
        remaining = remaining[split + 1 :]
    return lines


def wrap_lines(lines: list[str], width: int = COLS) -> list[str]:
    """Applique wrap_line à chaque ligne d'une liste."""
    out: list[str] = []
    for line in lines:
        out.extend(wrap_line(line, width))
    return out


def pad_lines(lines: list[str], count: int = BODY_LINES, width: int = COLS) -> list[str]:
    """Normalise une liste de lignes de corps à exactement `count` lignes de `width`."""
    out = [clip(line, width) for line in lines[:count]]
    while len(out) < count:
        out.append(" " * width)
    return out


def paginate(lines: list[str], page: int = 1, page_size: int = BODY_LINES) -> tuple[list[str], int, int]:
    """
    Paginate des lignes de corps.

    Retourne (slice, page_courante, total_pages).
    """
    if page_size < 1:
        page_size = 1
    total = max(1, (len(lines) + page_size - 1) // page_size) if lines else 1
    page = max(1, min(page, total))
    start = (page - 1) * page_size
    end = start + page_size
    return lines[start:end], page, total


def header_line(
    pgm: str,
    title: str,
    clock: str = "YYYY-MM-DD HH:MM:SS",
    width: int = COLS,
) -> str:
    """Construit la ligne d'en-tête : PGM | TITRE | HORLOGE."""
    left = f"PGM: {pgm}"
    right = clock
    center = title
    # left + spaces + center + spaces + right == width
    gap = width - len(left) - len(right) - len(center)
    if gap < 2:
        # titre trop long : on tronque le centre
        available = width - len(left) - len(right) - 2
        center = clip(center, max(0, available)).rstrip()
        gap = width - len(left) - len(right) - len(center)
    left_pad = gap // 2
    right_pad = gap - left_pad
    return left + (" " * left_pad) + center + (" " * right_pad) + right


def separator(width: int = COLS, char: str = "-") -> str:
    return char * width


def format_fkey_bar(keys: list[tuple[str, str]], width: int = COLS) -> str:
    """
    Formate la barre F-keys : [(F3, Quitter), ...].

    Le rendu HTML colore séparément ; ici on produit le texte brut.
    """
    parts = [f"{key}={label}" for key, label in keys]
    text = "   ".join(parts)
    return clip(text, width)


def table_row(columns: list[tuple[str, int]], width: int = COLS) -> str:
    """Aligne des colonnes (texte, largeur) par espaces."""
    parts: list[str] = []
    for text, col_w in columns:
        parts.append(clip(text, col_w) if len(text) > col_w else text.ljust(col_w))
    return clip("".join(parts), width)
