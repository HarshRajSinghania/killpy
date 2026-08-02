"""Gating matrix for the post-cleanup star hint (killpy/hints.py)."""

from __future__ import annotations

import io
import sys

import pytest
from rich.console import Console

from killpy.files import format_size
from killpy.hints import maybe_star_hint


@pytest.fixture()
def interactive(monkeypatch: pytest.MonkeyPatch) -> None:
    """Simulate an interactive terminal with no CI/opt-out variables."""
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("KILLPY_NO_HINT", raising=False)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True, raising=False)


def _capture() -> tuple[Console, io.StringIO]:
    buffer = io.StringIO()
    return Console(file=buffer, force_terminal=False, width=200), buffer


def test_prints_freed_size_and_repo_url_on_interactive_tty(interactive) -> None:
    console, buffer = _capture()

    maybe_star_hint(18_400_000_000, console)

    out = buffer.getvalue()
    assert "github.com/Tlaloc-Es/killpy" in out
    assert f"Freed {format_size(18_400_000_000)}" in out
    assert out.count("\n") <= 2  # a single line (plus its leading newline)


def test_silent_when_nothing_was_freed(interactive) -> None:
    console, buffer = _capture()

    maybe_star_hint(0, console)
    maybe_star_hint(-1, console)

    assert buffer.getvalue() == ""


def test_silent_when_user_opted_out(
    interactive, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("KILLPY_NO_HINT", "1")
    console, buffer = _capture()

    maybe_star_hint(1_000_000, console)

    assert buffer.getvalue() == ""


def test_silent_in_ci_even_on_a_tty(
    interactive, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CI", "true")
    console, buffer = _capture()

    maybe_star_hint(1_000_000, console)

    assert buffer.getvalue() == ""


def test_silent_when_stdout_is_not_a_tty(
    interactive, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False, raising=False)
    console, buffer = _capture()

    maybe_star_hint(1_000_000, console)

    assert buffer.getvalue() == ""
