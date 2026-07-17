"""Tests unitaires des helpers de mise en page."""

from dofus_stuff.web.screens import (
    BODY_LINES,
    COLS,
    clip,
    format_fkey_bar,
    header_line,
    pad_lines,
    paginate,
    table_row,
    wrap_line,
    wrap_lines,
)


def test_clip_pads_and_truncates():
    assert len(clip("ABC", 5)) == 5
    assert clip("ABC", 5) == "ABC  "
    assert len(clip("ABCDEFGHIJ", 5)) == 5
    assert clip("ABCDEFGHIJ", 5).endswith("…")


def test_wrap_line_breaks_on_spaces():
    text = "Description : " + ("mot " * 40)
    lines = wrap_line(text.strip(), width=40)
    assert len(lines) > 1
    assert all(len(line) <= 40 for line in lines)
    assert all("…" not in line for line in lines)
    joined = " ".join(lines)
    assert "Description :" in joined
    assert "mot" in joined


def test_wrap_line_hard_breaks_long_token():
    lines = wrap_line("x" * 25, width=10)
    assert lines == ["x" * 10, "x" * 10, "x" * 5]


def test_wrap_lines_expands_list():
    wrapped = wrap_lines(["court", "a " * 60], width=20)
    assert wrapped[0] == "court"
    assert len(wrapped) > 2
    assert all(len(line) <= 20 for line in wrapped)


def test_pad_lines_fixed_count():
    lines = pad_lines(["a", "b"], count=4, width=10)
    assert len(lines) == 4
    assert all(len(line) == 10 for line in lines)


def test_paginate():
    lines = [str(i) for i in range(40)]
    page1, p, total = paginate(lines, page=1, page_size=18)
    assert p == 1
    assert total == 3
    assert len(page1) == 18
    page3, p3, _ = paginate(lines, page=3, page_size=18)
    assert p3 == 3
    assert len(page3) == 4


def test_header_line_width():
    line = header_line("MNU-01", "** TITLE **", "2026-07-17 12:00:00")
    assert len(line) == COLS
    assert line.startswith("PGM: MNU-01")
    assert line.endswith("2026-07-17 12:00:00")


def test_format_fkey_bar():
    bar = format_fkey_bar([("F3", "Quitter"), ("F12", "Retour")])
    assert "F3=Quitter" in bar
    assert "F12=Retour" in bar
    assert len(bar) == COLS


def test_table_row():
    row = table_row([("44", 8), ("7", 5), ("Epee", 20)])
    assert len(row) == COLS
    assert row.startswith("44")


def test_body_lines_constant():
    assert BODY_LINES == 18
