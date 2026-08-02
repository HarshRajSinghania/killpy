# Security Policy

## Supported Versions

| Version | Supported |
| ------- | ------------------ |
| 1.0.x | :white_check_mark: |
| < 1.0 | :x: |

## Reporting a Vulnerability

Please **do not open a public issue** for security problems — killpy deletes
files, so a public report could put users at risk before a fix exists.

Instead, use GitHub's private vulnerability reporting: open the
[Security tab](https://github.com/Tlaloc-Es/killpy/security) and click
**"Report a vulnerability"**, or go directly to
<https://github.com/Tlaloc-Es/killpy/security/advisories/new>.

I will do my best to respond within **14 days**.

## What counts as a security issue

killpy is a destructive-deletion tool, so anything that can make it delete
paths it should not is in scope. For example:

- Path traversal or symlink tricks that redirect a deletion outside the
  selected environment or cache
- Bypasses of the `is_system_critical` guards (root, home, top-level
  directories)
- Any way the contents of a scanned directory can trick killpy into removing
  unrelated data

Crashes, wrong size reporting, or TUI glitches are regular bugs — please open
a normal issue for those.
