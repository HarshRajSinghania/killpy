---
title: Find and delete unused Python virtual environments and free disk space
description: killpy scans your machine for forgotten venv, Conda, Poetry, pipx, pyenv and uv environments, shows what each one costs in disk space, and deletes them safely.
---

# killpy

<div align="center">
	<img src="assets/images/logo.png" alt="killpy logo" width="420">
</div>

**killpy** finds every Python environment on your machine — `.venv` folders, Conda and Poetry environments, pipx packages, pyenv versions, Pipenv, Hatch, tox and uv environments, plus caches and build artifacts — shows what each one costs in disk space, and lets you delete the ones you no longer need.

```bash
uvx killpy --path ~        # instant run, no install needed
```

![killpy in action](https://raw.githubusercontent.com/Tlaloc-Es/killpy/master/docs/gifs/demo.gif)

A typical development machine accumulates **10–40 GB** of forgotten environments over a few years. killpy is [npkill](https://github.com/voidcosmos/npkill) for Python: the same idea, but it understands every environment manager instead of matching folders by name.

## Why killpy exists

Python tooling tends to scatter disk usage across many locations:

- local `.venv` folders inside projects
- directories containing `pyvenv.cfg`
- Poetry-managed environments in cache directories
- Conda environments outside your repo tree
- `pipx` package environments
- `pyenv` versions
- tox, Hatch, Pipenv, and uv environments
- stale caches and Python build artifacts

For many developers, these directories grow for months or years and turn into hidden disk usage. Instead of jumping between `conda`, Poetry cache directories, `pipx`, `pyenv`, and ad hoc shell commands, `killpy` gives you one scanner and one cleanup workflow that makes that usage visible, measurable, and removable.

## Interfaces

`killpy` has two primary surfaces:

- An interactive Textual TUI launched by the top-level `killpy` command
- Scriptable CLI subcommands for listing, deleting, stats, and cache cleanup

The TUI is optimized for inspection and explicit deletion. The scanner and non-interactive commands expose the broader detection model.

## Important behavior notes

- The TUI currently shows environment results plus a dedicated `pipx` tab.
- Cache and artifact detection exists in the scanner and CLI flows, but those do not have separate TUI tables today.
- `killpy clean` removes `__pycache__` directories recursively under the target path.
- Environments managed by external tools are deleted through those tools when possible, such as `conda env remove` and `pipx uninstall`.

## Where to go next

Continue with the [Quickstart](getting-started/quickstart.md) for the main workflows, browse the [use cases](user-guide/use-cases.md) for complete, copy-pasteable recipes, or jump to the [CLI reference](user-guide/cli.md).

If `killpy` saves you time or disk space, the GitHub repository is here: [Tlaloc-Es/killpy](https://github.com/Tlaloc-Es/killpy).
