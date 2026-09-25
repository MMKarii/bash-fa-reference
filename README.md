# Bash Professional Reference — فارسی + English

![Bash Professional Reference](docs/en/assets/brand-banner.webp)

Bashref is a bilingual Persian/English Bash reference product: an offline CLI, structured Reference Guide, generated man pages, cross-platform standalone executables, Linux packages, and a 14-chapter Professional Guide.

**Live documentation:** https://mmkarii.github.io/bash-fa-reference/  
**فارسی:** https://mmkarii.github.io/bash-fa-reference/fa/  
**English:** https://mmkarii.github.io/bash-fa-reference/en/

## Bashref CLI

Bashref 2.1.0 keeps normal lookup and search offline:

```bash
bashref
bashref search quoting
bashref builtin printf
bashref option pipefail
bashref --lang fa builtin read
bashref --format json builtin printf
bashref doctor
```

Running `bashref` with no arguments prints a concise command summary. `bashref doctor` reports the runtime, platform, selected language, reference record count, and bilingual parity.

## Installation

The release line supports several installation models:

- standalone Linux x86_64 executable
- standalone macOS arm64 and x86_64 executables
- standalone Windows x86_64 executable
- Python wheel / pipx for Python 3.10+
- Debian package
- RPM package
- Homebrew formula artifact

Standalone builds do not require a separate Python installation. See the [installation guide](https://mmkarii.github.io/bash-fa-reference/en/install/) for exact commands and uninstall instructions.

## Product architecture

- **Bashref CLI:** offline terminal lookup/search with text and JSON output
- **Reference Guide:** structured bilingual records for builtins, syntax, expansions, options, variables, concepts, and examples
- **Professional Guide:** 14 chapters covering shell fundamentals, scripting, automation, SysAdmin, DevOps, defensive security, debugging, and portability
- **Man pages:** generated from the same reference source
- **Packages:** wheel/sdist, DEB, RPM, completions, Homebrew formula, portable archives, and checksums
- **Standalone executables:** built and smoke-tested separately on Linux, macOS, and Windows
- **Website:** Persian RTL and English LTR editions with stable version snapshots

## Quality and release engineering

CI validates structured reference parity, generated outputs, unit/integration tests, installed-wheel behavior, man pages, links, anchors, metadata, accessibility, DEB/RPM installation, and standalone executables. Release assets are published with SHA-256 checksums.

The reference database is never executed as shell code. Bash-specific semantics cite the GNU Bash Reference Manual.

## Support

Start with:

```bash
bashref --format json doctor
```

Then see [SUPPORT.md](SUPPORT.md) for bug-reporting information. Sensitive security issues should follow [SECURITY.md](SECURITY.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Canonical reference records live under `reference/en/` and `reference/fa/`; generated reference pages should not be edited directly.

## License

Software is MIT licensed. Documentation/reference prose is CC BY 4.0. See the root `LICENSE` and `LICENSES/` directory for scope.
