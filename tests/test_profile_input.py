"""Tests du parsing d'entrée optimiseur."""

from __future__ import annotations

import pytest

from dofus_stuff.optimize.profile_input import (
    OptimizeInputError,
    parse_compact_line,
    parse_optimize_request,
    prompt_optimize_interactive,
)


def test_parse_demo():
    req = parse_compact_line("demo")
    assert req.profile.level == 123
    assert req.profile.stats_without_equipment().get("Intelligence") == 300.0
    assert req.classic_only is False


def test_parse_demo_classic_jet_max():
    req = parse_compact_line("demo classic jet=max")
    assert req.classic_only is True
    assert req.profile.jet_mode == "max"


def test_parse_compact_int_profile():
    req = parse_compact_line("123 intelligence 200 100")
    assert req.profile.level == 123
    assert req.profile.base_stats.get("Intelligence") == 200.0
    assert req.profile.scrolls.get("Intelligence") == 100.0
    assert "Intelligence" in req.profile.objective.weights


def test_parse_compact_multi_stat():
    req = parse_compact_line("100 int,vit 200,50 100,0")
    assert req.profile.base_stats.get("Intelligence") == 200.0
    assert req.profile.base_stats.get("Vitalité") == 50.0
    assert req.profile.scrolls.get("Intelligence") == 100.0
    assert req.profile.scrolls.get("Vitalité") == 0.0


def test_parse_compact_errors():
    with pytest.raises(OptimizeInputError):
        parse_compact_line("")
    with pytest.raises(OptimizeInputError):
        parse_compact_line("abc intelligence")
    with pytest.raises(OptimizeInputError):
        parse_compact_line("123")
    with pytest.raises(OptimizeInputError):
        parse_compact_line("123 intelligence 200 100 jet=foo")


def test_parse_optimize_request_flags():
    req = parse_optimize_request(
        level=50,
        max_stats=["force"],
        base_str=100,
        scroll_str=50,
        classic_only=True,
    )
    assert req.profile.level == 50
    assert req.profile.base_stats.get("Force") == 100.0
    assert req.classic_only is True


def test_parse_optimize_request_requires_level():
    with pytest.raises(OptimizeInputError):
        parse_optimize_request(max_stats=["intelligence"])


def test_interactive_demo(monkeypatch):
    answers = iter(["demo", "o", "average"])
    req = prompt_optimize_interactive(input_fn=lambda _prompt: next(answers))
    assert req.profile.level == 123
    assert req.classic_only is True


def test_interactive_level(monkeypatch):
    answers = iter(["123", "intelligence", "200", "100", "n", ""])
    req = prompt_optimize_interactive(input_fn=lambda _prompt: next(answers))
    assert req.profile.level == 123
    assert req.profile.base_stats.get("Intelligence") == 200.0
    assert req.profile.scrolls.get("Intelligence") == 100.0
    assert req.classic_only is False
    assert req.profile.jet_mode == "average"
