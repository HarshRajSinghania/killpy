"""Regression tests for --min-size parsing and stats --history conflicts."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import click
import pytest
from click.testing import CliRunner

from killpy.__main__ import cli
from killpy.commands._utils import SIZE
from killpy.intelligence.tracker import UsageTracker


def test_iec_units_match_si_binary_aliases() -> None:
    assert SIZE.convert("2KiB", None, None) == SIZE.convert("2KB", None, None) == 2 << 10
    assert SIZE.convert("3MiB", None, None) == SIZE.convert("3MB", None, None) == 3 << 20
    assert SIZE.convert("1.5GiB", None, None) == SIZE.convert("1.5GB", None, None)
    assert SIZE.convert("1TiB", None, None) == SIZE.convert("1TB", None, None) == 1 << 40


@pytest.mark.parametrize("value", ["ib", "\u0665MB", "lots", "1000"])
def test_rejects_non_ascii_digits_and_invalid_units(value: str) -> None:
    with pytest.raises(click.UsageError):
        SIZE.convert(value, None, None)


def test_stats_history_rejects_min_size(tmp_path: Path) -> None:
    tracker = UsageTracker(tmp_path / "history.json")
    runner = CliRunner()
    with patch("killpy.commands.stats.UsageTracker", return_value=tracker):
        result = runner.invoke(cli, ["stats", "--history", "--min-size", "1MB"])
    assert result.exit_code != 0
    assert "--history" in result.output
    assert "--min-size" in result.output


def test_stats_history_rejects_explicit_path(tmp_path: Path) -> None:
    tracker = UsageTracker(tmp_path / "history.json")
    runner = CliRunner()
    with patch("killpy.commands.stats.UsageTracker", return_value=tracker):
        result = runner.invoke(cli, ["stats", "--history", "--path", str(tmp_path)])
    assert result.exit_code != 0
    assert "--history" in result.output
    assert "--path" in result.output
