"""One-line, opt-out hints printed after a successful cleanup."""

from __future__ import annotations

import os
import sys

from rich.console import Console

from killpy.files import format_size

_REPO_URL = "github.com/Tlaloc-Es/killpy"


def maybe_star_hint(freed_bytes: int, console: Console | None = None) -> None:
    """Print a single, unobtrusive star hint after ``freed_bytes`` were reclaimed.

    Stays silent unless stdout is an interactive terminal, and never shows
    when the ``CI`` environment variable is present or when the user opted
    out with ``KILLPY_NO_HINT``.
    """
    if freed_bytes <= 0:
        return
    if os.environ.get("KILLPY_NO_HINT") or os.environ.get("CI"):
        return
    if not sys.stdout.isatty():
        return
    (console or Console()).print(
        f"\n[bold yellow]Freed {format_size(freed_bytes)}[/bold yellow]"
        f"[dim] · [/dim][yellow]★[/yellow] [dim]{_REPO_URL}[/dim]"
    )
