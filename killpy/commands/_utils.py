"""Shared helpers for ``killpy`` commands."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import click
from rich.console import Console

from killpy.models import Environment

# Maps user-facing type names (detector names) to the concrete ``Environment.type``
# values those detectors produce.  Two detectors use sub-type tags instead of
# their own name: VenvDetector (tags: ".venv", "pyvenv.cfg") and CacheDetector
# (tags: "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
# "pip-cache", "uv-cache").  Without this mapping, ``--type venv`` and
# ``--type cache`` would never match anything.
_TYPE_ALIASES: dict[str, frozenset[str]] = {
    "venv": frozenset({".venv", "pyvenv.cfg"}),
    "cache": frozenset(
        {
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            "pip-cache",
            "uv-cache",
        }
    ),
}

_SIZE_UNITS = {
    "b": 1,
    "kb": 1 << 10,
    "kib": 1 << 10,
    "mb": 1 << 20,
    "mib": 1 << 20,
    "gb": 1 << 30,
    "gib": 1 << 30,
    "tb": 1 << 40,
    "tib": 1 << 40,
}
# ASCII digits only: \d is Unicode-aware and would accept values such as ٥MB.
# IEC prefixes (KiB/MiB/GiB/TiB) are aliases for the same binary units.
_SIZE_PATTERN = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s*([kmgt]?i?b)", re.IGNORECASE)


class SizeParamType(click.ParamType):
    """Convert human-readable byte sizes such as ``500MB`` or ``1.5GB``."""

    name = "SIZE"

    def convert(self, value, param, ctx):  # type: ignore[no-untyped-def]
        if isinstance(value, int):
            return value
        match = _SIZE_PATTERN.fullmatch(value.strip())
        if match is None:
            self.fail(
                "must be a size with a unit, such as 500MB, 1.5GB, or 200KB",
                param,
                ctx,
            )
        amount, unit = match.groups()
        factor = _SIZE_UNITS.get(unit.lower())
        if factor is None:
            self.fail(
                "must be a size with a unit, such as 500MB, 1.5GB, or 200KB",
                param,
                ctx,
            )
        # Decimal rather than float: a mantissa of 309+ digits overflows a
        # float to infinity, and int() then raises instead of failing cleanly.
        return int(Decimal(amount) * factor)


SIZE = SizeParamType()
