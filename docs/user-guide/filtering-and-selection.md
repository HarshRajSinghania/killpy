---
title: Filtering and selection \u2014 target exactly what to delete
description: Exclude paths, filter by age with --older-than or by size with --min-size, and use the TUI's live filter and multi-select to delete exactly the rows you intend.
---

# Filtering and Selection

## Excluding paths

The top-level command accepts comma-separated exclusion patterns:

```bash
killpy --path ~ --exclude "archive,backups,legacy"
```

Those exclusions are applied by substring matching against discovered paths.

## Filtering by age

The `list` and `delete` commands support `--older-than`:

```bash
killpy list --older-than 90
killpy delete --older-than 180 --dry-run
```

This filter is based on the recorded last-modified timestamp (`st_mtime`) stored in each `Environment` object.

## Filtering by size

The `list`, `find`, `delete`, `stats` and `doctor` commands support `--min-size`, which keeps only environments at least that large:

```bash
killpy list --min-size 500MB             # only what is worth reclaiming
killpy delete --min-size 1GB --dry-run   # preview the big ones
```

Sizes take a unit (`B`, `KB`/`KiB`, `MB`/`MiB`, `GB`/`GiB` or `TB`/`TiB`, case-insensitive) and accept decimals such as `1.5GB`. Units are binary \u2014 `1KB` and `1KiB` are both 1024 bytes \u2014 so a threshold matches exactly what the tool prints in its `Size` column. A value without a unit is a usage error. Only ASCII digits `0-9` are accepted.

`killpy stats --history` reports stored totals rather than a fresh scan, so `--min-size` and `--path` cannot be combined with it.

## Sorting output

The `list` command supports `--sort` (`size`, `date`, `name`) and `--reverse`:

```bash
killpy list --sort date                  # newest modified first
killpy list --sort size --reverse        # smallest size first
killpy list --sort name                  # alphabetical A-Z
```
