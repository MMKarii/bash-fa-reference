# Bashref Product Architecture Design

Date: 2026-09-22
Status: Approved direction, design review
Target product release: v2.0.0

## 1. Purpose

Transform `MMKarii/bash-fa-reference` from a documentation-first repository into a complete, installable Bash reference product with the maturity pattern of established command-line projects such as Nmap: a real CLI, a canonical reference guide, system man pages, installable packages, release artifacts, a versioned website, bilingual documentation, contribution workflows, and strict automated quality gates.

The product remains Bash-focused. It does not copy Nmap source code, scanner functionality, prose, branding, or network-scanning behavior.

The repository remains the single project home and preserves all existing public documentation URLs.

## 2. Product identity

The installed command is:

```text
bashref
```

The Python distribution name is:

```text
bashref
```

The existing repository name remains:

```text
bash-fa-reference
```

The website remains:

```text
https://mmkarii.github.io/bash-fa-reference/
```

The existing documentation release `v1.0.0` remains immutable. The first integrated software + reference release is `v2.0.0`.

## 3. Product layers

The repository has three first-class product layers.

### 3.1 Bashref CLI

An offline-first command-line reference browser and search tool.

Primary commands:

```text
bashref
bashref --help
bashref --version
bashref search QUERY
bashref show TOPIC
bashref builtin NAME
bashref syntax NAME
bashref expansion NAME
bashref option NAME
bashref shopt NAME
bashref variable NAME
bashref example NAME
bashref list CATEGORY
bashref man [TOPIC]
bashref docs [TOPIC]
bashref lang {fa,en}
bashref completion {bash,zsh,fish}
```

Global output controls:

```text
--lang {fa,en}
--format {text,json}
--no-color
--width N
```

The CLI never executes Bash examples. Reference content is treated as data, not executable input.

### 3.2 Bash Reference Guide

A lookup-oriented, structured reference comparable in role to a mature command reference manual.

Top-level sections:

- NAME
- SYNOPSIS
- DESCRIPTION
- OPTIONS SUMMARY
- SHELL SYNTAX
- RESERVED WORDS
- BUILTINS
- VARIABLES
- PARAMETER EXPANSION
- COMMAND SUBSTITUTION
- ARITHMETIC EXPANSION
- PROCESS SUBSTITUTION
- QUOTING
- ARRAYS
- CONDITIONAL EXPRESSIONS
- LOOPS
- FUNCTIONS
- REDIRECTION
- PIPELINES
- JOB CONTROL
- SIGNALS
- TRAPS
- SHELL OPTIONS
- SHOPT OPTIONS
- STARTUP FILES
- ENVIRONMENT
- EXIT STATUS
- DEBUGGING
- PORTABILITY
- SECURITY
- EXAMPLES
- FILES
- BUGS
- AUTHORS
- LICENSE
- SEE ALSO

Each builtin, option, variable, syntax form, expansion, and major concept has an individual record and a generated web page.

### 3.3 Bash Professional Guide

The existing 14 bilingual chapters remain the tutorial and operational handbook. They are expanded over time but stay separate from the lookup-oriented Reference Guide.

The website presents both products clearly:

- Reference Guide: precise lookup
- Professional Guide: learning and applied usage

## 4. Repository architecture

```text
bash-fa-reference/
├── src/
│   └── bashref/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── commands.py
│       ├── search.py
│       ├── reference.py
│       ├── renderer.py
│       ├── config.py
│       ├── languages.py
│       ├── completion.py
│       ├── errors.py
│       └── data/
│           ├── manifest.json
│           ├── search-index.json
│           ├── en/
│           └── fa/
├── reference/
│   ├── schema/
│   │   └── record.schema.json
│   ├── en/
│   │   ├── builtins/
│   │   ├── syntax/
│   │   ├── expansions/
│   │   ├── options/
│   │   ├── shopt/
│   │   ├── variables/
│   │   ├── concepts/
│   │   └── examples/
│   └── fa/
│       └── same category layout
├── docs/
│   ├── en/
│   │   ├── reference/
│   │   ├── book/
│   │   ├── install/
│   │   ├── download/
│   │   └── examples/
│   └── fa/
│       └── mirrored layout
├── man/
│   ├── bashref.1
│   ├── bashref-reference.5
│   └── generated/
├── packaging/
│   ├── deb/
│   ├── rpm/
│   ├── homebrew/
│   └── completions/
├── tests/
│   ├── cli/
│   ├── reference/
│   ├── search/
│   ├── renderer/
│   ├── packaging/
│   └── integration/
├── tools/
│   ├── build_reference.py
│   ├── build_manpages.py
│   ├── build_search_index.py
│   └── validate_reference.py
├── scripts/
├── pyproject.toml
└── .github/workflows/
```

Generated files are reproducible from source records and are verified in CI.

## 5. Canonical reference data model

The source of truth for reference entries is `reference/{lang}/...`.

Records use JSON for deterministic parsing and zero runtime parser dependencies.

Every record follows a common schema.

Required fields:

```json
{
  "id": "builtin.printf",
  "kind": "builtin",
  "name": "printf",
  "language": "en",
  "summary": "Format and print data.",
  "synopsis": "printf [-v var] format [arguments]",
  "description": ["..."],
  "examples": [],
  "related": [],
  "sources": []
}
```

Supported fields include:

- `id`
- `kind`
- `name`
- `aliases`
- `language`
- `summary`
- `synopsis`
- `description`
- `syntax`
- `parameters`
- `exit_status`
- `examples`
- `pitfalls`
- `portability`
- `security`
- `related`
- `tags`
- `since`
- `sources`

The same `id` must exist in Persian and English for every bilingual record.

Reference data does not contain executable Python or shell snippets outside explicit text/example fields.

## 6. Reference coverage

The v2.0.0 acceptance set covers the Bash language and major Bash builtins, not only the current 14 handbook chapters.

Required builtin coverage includes at least:

`alias`, `bg`, `bind`, `break`, `builtin`, `caller`, `cd`, `command`, `compgen`, `complete`, `compopt`, `continue`, `declare`, `dirs`, `disown`, `echo`, `enable`, `eval`, `exec`, `exit`, `export`, `false`, `fc`, `fg`, `getopts`, `hash`, `help`, `history`, `jobs`, `kill`, `let`, `local`, `logout`, `mapfile`, `popd`, `printf`, `pushd`, `pwd`, `read`, `readarray`, `readonly`, `return`, `set`, `shift`, `shopt`, `source`, `suspend`, `test`, `times`, `trap`, `true`, `type`, `typeset`, `ulimit`, `umask`, `unalias`, `unset`, and `wait`.

Required language coverage includes:

- quoting
- parameter expansion
- command substitution
- arithmetic expansion
- process substitution
- brace expansion
- pathname expansion
- arrays and associative arrays
- conditionals
- loops
- functions
- pipelines
- redirections
- here documents
- here strings
- subshells
- grouping
- exit status
- traps and signals
- job control
- shell options
- `shopt`
- startup files
- environment variables
- debugging
- portability
- defensive scripting

Reference claims with version-sensitive behavior cite the GNU Bash manual or another authoritative primary source.

## 7. CLI architecture

The CLI uses Python's standard library `argparse` to keep runtime dependencies minimal.

Internal components:

### `cli.py`

Parses arguments, dispatches commands, maps exceptions to exit codes, and owns help output.

### `reference.py`

Loads packaged records using `importlib.resources`, resolves IDs, aliases, categories, and related entries.

### `search.py`

Uses a generated compact search index. Ranking weights:

1. exact ID/name match
2. alias match
3. title/name prefix
4. tags
5. summary
6. body text

Typo suggestions use deterministic standard-library matching.

### `renderer.py`

Produces terminal text and JSON. Text rendering respects terminal width and disables ANSI when stdout is not a TTY or `--no-color` is set.

### `languages.py`

Resolves default language in this order:

1. explicit `--lang`
2. saved user config
3. locale-derived Persian when locale begins with `fa`
4. English fallback

### `config.py`

Stores small user preferences under the platform-appropriate user config directory. No credentials or telemetry are stored.

### `completion.py`

Outputs static/deterministic completion scripts for Bash, Zsh, and Fish.

## 8. CLI behavior and exit codes

Exit codes are stable API:

- `0`: success
- `1`: unexpected internal error
- `2`: command-line usage error
- `3`: reference entry not found
- `4`: invalid/corrupt reference data

Human-readable errors go to stderr.

JSON mode returns machine-readable errors with:

- `error`
- `code`
- `message`
- `suggestions`

Search with zero results exits successfully and returns an empty result set. Direct lookup of a missing named entry exits with code `3`.

## 9. Man pages

The project installs real system manual pages.

Required pages for v2.0.0:

- `bashref(1)`: CLI command
- `bashref-reference(5)`: reference data/manual overview

Generated topic pages are stored under `man/generated/` and included in source/release archives.

The man-page generator consumes the same canonical reference records used by the CLI and website.

CI validates man pages with `mandoc -Tlint` on Linux.

## 10. Website architecture

The current bilingual MkDocs site remains the publishing engine.

Primary navigation becomes:

- Home
- Reference Guide
- Builtins
- Shell Syntax
- Expansions
- Options
- Variables
- Examples
- Professional Guide
- Installation
- Download
- Releases
- Contributing
- Security
- About

Generated reference pages are written into the MkDocs input tree during build and are not manually edited.

Existing URLs remain valid.

Current publication paths remain:

- `/fa/`
- `/en/`
- `/latest/fa/`
- `/latest/en/`
- `/v1.0/fa/`
- `/v1.0/en/`

v2 adds:

- `/v2.0/fa/`
- `/v2.0/en/`

Current pages use canonical URLs under `/fa/` and `/en/`. Archived version snapshots do not replace the current canonical edition.

Persian/English switchers keep users on the equivalent record/page when the paired translation exists.

## 11. Packaging

`pyproject.toml` is the canonical Python package definition.

Supported Python baseline:

```text
Python >= 3.10
```

Required install paths:

### PyPI-style package artifacts

- wheel
- source distribution

Primary user installation:

```text
pipx install bashref
```

Also supported:

```text
python -m pip install bashref
```

### Linux packages

Release automation produces:

- `.deb`
- `.rpm`

Packages install:

- `bashref`
- Python package/runtime files
- man pages
- shell completions
- license files

### Homebrew

A versioned Homebrew formula template is maintained under `packaging/homebrew/`.

### Portable archive

Each release includes a portable source/reference archive containing generated docs, man pages, completions, and install metadata.

## 12. Release artifacts

A v2.0.0 release produces at minimum:

- `bashref-2.0.0-py3-none-any.whl`
- `bashref-2.0.0.tar.gz`
- Debian package
- RPM package
- portable project archive
- man-page archive
- shell-completion archive
- `SHA256SUMS`
- generated release notes
- documentation snapshot

GitHub release artifacts are generated from the release tag, never from an untagged working tree.

Release checks fail if generated reference output differs from source records.

## 13. CI architecture

### PR validation

Required status check remains:

```text
docs / build-and-deploy
```

The workflow is expanded or decomposed while preserving this protected status name.

PR quality gates:

- Python unit tests
- CLI integration tests
- JSON/schema validation
- bilingual record parity
- duplicate ID detection
- broken related-record detection
- search index reproducibility
- generated output reproducibility
- packaging build
- wheel installation smoke test
- command smoke tests
- man-page lint
- shell completion generation
- existing docs structure tests
- local links and anchors
- external links
- strict Persian MkDocs build
- strict English MkDocs build
- built-site metadata
- accessibility
- SEO assertions
- public safety checks

### Python test matrix

Core package tests run against supported Python versions. Platform-specific smoke tests cover Linux, macOS, and Windows where the behavior is platform-relevant.

### Main deployment

Successful `main` builds publish the current website to `gh-pages`.

### Tag release

Tags matching `v*` run the release pipeline, produce artifacts, checksums, documentation snapshots, and GitHub Release assets.

## 14. Testing strategy

Tests are split by responsibility.

### Unit tests

Pure logic:

- record parsing
- language selection
- lookup
- alias resolution
- search ranking
- formatting
- errors
- completion rendering

### Contract tests

Validate:

- schema conformance
- stable exit codes
- JSON output shape
- paired bilingual IDs
- source citations for version-sensitive claims

### Integration tests

Run the installed CLI in a clean environment:

```text
bashref --version
bashref search quoting
bashref builtin printf
bashref option pipefail
bashref --format json builtin read
```

### Packaging tests

Build wheel/sdist, install the wheel into an isolated environment, confirm package metadata, entry points, packaged reference data, and man-page payload.

### Golden tests

Selected CLI text and generated man-page/reference output use reviewed golden fixtures to detect accidental formatting drift.

## 15. Security model

The program is a reference browser, not a shell executor.

Security requirements:

- never `eval` reference data
- never execute examples
- no implicit network requests for normal lookup/search
- no telemetry
- no credential collection
- no plugin loading from untrusted paths
- validate packaged record paths and IDs
- reject malformed reference manifests
- escape terminal control sequences from data fields
- keep defensive/public-safety documentation checks
- security reports use GitHub private reporting when available

The optional `bashref docs --open` action opens a fixed project URL or a URL derived only from validated internal record IDs.

## 16. Licensing

Existing documentation remains licensed under CC BY 4.0.

Software source code introduced for `bashref` uses the MIT License.

The repository moves to an explicit split-license layout:

- `LICENSES/CC-BY-4.0.txt`
- `LICENSES/MIT.txt`
- root `LICENSE` explains scope
- source files/package metadata identify the software license
- documentation pages identify the documentation license

No license or source text from Nmap is copied.

## 17. Migration from v1

The migration is additive.

Preserved:

- current GitHub repository
- existing v1.0.0 tag/release
- existing handbook content
- existing Persian/English URLs
- current Pages deployment
- existing contribution/security files
- current QA checks

Added:

- installable CLI
- structured reference database
- generated reference site
- generated man pages
- software packaging
- product release pipeline
- expanded CI
- download/install sections

The v1 handbook is not rewritten into generated data. It remains editorial long-form content.

## 18. Documentation generation flow

Build data flow:

```text
reference/en + reference/fa
          │
          ├── validate schema/parity/citations
          │
          ├── build packaged CLI data
          │       └── src/bashref/data/
          │
          ├── build search index
          │
          ├── generate MkDocs reference pages
          │       ├── docs/en/reference/
          │       └── docs/fa/reference/
          │
          └── generate man pages
                  └── man/generated/
```

All generated outputs contain a header identifying them as generated where the target format permits it.

CI regenerates outputs in a clean tree and compares them with committed/generated release expectations.

## 19. Versioning

Project versions follow semantic versioning.

- v1.0.0: documentation edition, retained
- v2.0.0: first integrated `bashref` product release

CLI reports the package version:

```text
bashref 2.0.0
```

Reference manifest records the Bash manual baseline used for technical verification separately from the `bashref` software version.

## 20. Contribution model

Contribution documentation gains separate paths for:

- software changes
- English reference records
- Persian translations
- handbook changes
- packaging
- generated-output changes

Contributors edit canonical source records, not generated reference pages.

PR templates require:

- tests
- paired translation impact
- source/citation impact
- generated-output update
- security impact

## 21. Non-goals

v2.0.0 does not:

- implement network scanning
- imitate Nmap CLI flags or behavior
- execute arbitrary Bash supplied by documentation
- replace the GNU Bash manual
- embed private credentials or production targets
- require internet access for core search/reference use
- remove the existing handbook or v1 archive

## 22. Definition of done for v2.0.0

v2.0.0 is complete only when all of the following are true:

1. `pipx install bashref` installs an operational CLI from a built package.
2. `bashref --help`, `search`, direct lookup, list, language, JSON, man, docs, and completion commands work.
3. Required Bash builtin coverage is present in both Persian and English.
4. Required language/reference categories are present in both languages.
5. Every bilingual reference pair shares a stable record ID.
6. Reference data passes schema and source-link validation.
7. CLI search works fully offline.
8. Real man pages build and pass lint.
9. Wheel and source distribution build and install in CI.
10. Debian and RPM packages are generated and smoke-tested.
11. Shell completions are generated for Bash, Zsh, and Fish.
12. The website exposes Reference Guide, Professional Guide, Installation, Download, Releases, Contributing, and Security sections.
13. Existing v1/current documentation URLs remain valid.
14. Current and versioned bilingual Pages builds pass local-link, anchor, metadata, accessibility, and SEO checks.
15. GitHub release automation produces versioned artifacts and SHA256 checksums.
16. Main remains protected by the required `docs / build-and-deploy` check.
17. All test and packaging workflows are green on the release commit.
18. Documentation/software split licensing is explicit.
19. CHANGELOG and release notes describe the product transition.
20. The published v2.0.0 release and live website are verified after deployment.

## 23. Implementation principle

Implementation is incremental and test-driven. The repository stays releasable throughout the migration. No step removes the currently working site before its replacement path is verified.

The product architecture favors a small dependency surface, deterministic generation, offline reference access, stable machine-readable output, and one canonical source of truth for reference facts.
