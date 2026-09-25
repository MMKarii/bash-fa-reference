# Hacking on Bashref

This document describes the internal architecture and development workflow.

## Architecture

Bashref has three product layers:

1. `reference/{en,fa}/` is the canonical structured reference source.
2. `src/bashref/` is the offline CLI/runtime.
3. MkDocs, man pages, package data, completions, and release assets are generated from canonical sources.

The 14-chapter Professional Guide under `docs/{en,fa}/` remains editorial long-form content and is intentionally separate from generated Reference Guide pages.

## Runtime modules

- `cli.py`: argument parsing and exit-code contract
- `reference.py`: packaged-record loading and direct lookup
- `search.py`: deterministic offline search/ranking
- `renderer.py`: safe text and JSON output
- `languages.py` / `config.py`: language resolution and preferences
- `completion.py`: shell completion and trusted documentation URL mapping
- `diagnostics.py`: local runtime and corpus diagnostics

Core runtime code uses only the Python standard library.

## Generation pipeline

```text
reference/en + reference/fa
        |
        +-> validate_reference.py
        +-> build_reference.py -> src/bashref/data/
        +-> build_search_index.py
        +-> build_docs_reference.py -> generated Reference Guide
        +-> build_manpages.py -> man/
        +-> build_completions.py -> packaging/completions/
```

Generated output must be deterministic. CI regenerates it and fails on drift.

## Error contract

- 0: success
- 1: internal error
- 2: command-line usage error
- 3: named reference entry not found
- 4: corrupt packaged reference data

Do not casually change these codes; JSON clients may depend on them.

## Security invariants

- reference examples are data, never executable input
- core lookup/search performs no network requests
- user input is never converted into filesystem paths for packaged data
- generated documentation URLs derive from validated record IDs
- terminal text rendering strips unsafe control characters

## Testing

Use TDD for behavior changes. A defect fix should include a failing regression test before the production change whenever practical.

See `CONTRIBUTING.md` for the full validation command sequence.
