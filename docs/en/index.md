# Bashref: Bash from terminal to reference manual

**Bashref 2.1.0** is a free, open-source Bash reference project combining an offline CLI, a **214-record bilingual Reference Guide**, system man pages, installable packages, and a fourteen-chapter Professional Guide.

[Get Bashref 2.1.0](download/index.md){ .md-button }

## News

- **Bashref 2.1.0:** the structured Persian/English reference now contains 214 bilingual records, including broader `set -o`, `shopt`, Bash-variable, and compound-command coverage.
- **Offline diagnostics:** `bashref stats` reports corpus coverage and `bashref doctor` reports the local runtime without network access.
- **Versioned documentation:** immutable v2.1, v2.0, and v1.0 snapshots remain available.

## What Bashref provides

- **[Reference Guide](reference/):** precise lookup for builtins, syntax, expansions, shell options, `shopt`, variables, concepts, and examples.
- **[Professional Guide](book/):** fourteen chapters for learning, automation, SysAdmin, DevOps, security, and debugging.
- **[Installation](install/):** install the CLI from verified release artifacts.
- **[Download](download/):** wheel, source archive, DEB/RPM, portable archive, man pages, completions, Homebrew formula, and checksums.
- **[Releases](releases/):** release history and stable documentation snapshots.
- **[About](about/):** architecture, scope, licensing, and project boundaries.

## Quick start

```bash
bashref search quoting
bashref builtin printf
bashref option pipefail
bashref shopt extglob
bashref variable BASH_VERSION
bashref doctor
```

## Bashref is...

- **Comprehensive:** 214 paired English/Persian records plus the long-form Professional Guide.
- **Offline:** core reference lookup, search, diagnostics, JSON output, and completions need no network connection.
- **Portable:** Python wheel, source distribution, Debian/RPM packages, portable archive, man pages, and shell completions.
- **Well documented:** Reference Guide, Professional Guide, install documentation, contributor documentation, and system man pages.
- **Verifiable:** protected CI, release checksums, deterministic generated outputs, and immutable stable documentation snapshots.

Bash-specific behavior is cross-checked primarily against the [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html).

!!! warning "Run commands deliberately"
    Test deletion, permission/ownership changes, service operations, and system-level automation in a controlled environment before production use.
