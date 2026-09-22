# Bashref Core CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and package the first working `bashref` CLI with offline bilingual lookup/search, stable machine-readable output, safe rendering, and shell completion generation.

**Architecture:** Canonical JSON records live under `reference/{en,fa}` and are compiled into package data under `src/bashref/data`. The runtime uses only Python standard-library modules. CLI parsing is separated from reference loading, search, rendering, language selection, config, and completion generation so each responsibility is independently testable.

**Tech Stack:** Python 3.10+, `argparse`, `json`, `importlib.resources`, `difflib`, `pathlib`, `tomllib` where needed, pytest, setuptools build backend.

**Spec:** `docs/superpowers/specs/2026-09-22-bashref-product-design.md`

## Global Constraints

- Installed command: `bashref`.
- Distribution name: `bashref`.
- Python baseline: `>=3.10`.
- Core runtime dependency count: zero third-party packages.
- Search/lookup works without network access.
- Reference examples are data and are never executed.
- Stable exit codes: 0 success, 1 internal, 2 usage, 3 missing entry, 4 corrupt data.
- Text and JSON output are supported.
- Explicit `--lang` overrides config and locale.
- ANSI is disabled for non-TTY output or `--no-color`.

## Review Focus

1. Malformed JSON/manifest returns a structured corrupt-data error with exit code 4.
2. `--lang en` wins even when `LANG=fa_IR.UTF-8`.
3. Control characters embedded in record content are escaped/removed before terminal rendering.
4. Empty search returns exit code 0 with an empty list in JSON mode.
5. Alias lookup and canonical ID lookup resolve to the same record without duplicate results.

---

### Task 1: Package skeleton and versioned console entry point

**Files:**
- Create: `pyproject.toml`
- Create: `src/bashref/__init__.py`
- Create: `src/bashref/__main__.py`
- Create: `src/bashref/cli.py`
- Create: `tests/cli/test_entrypoint.py`

**Interfaces:**
- Produces: `bashref.cli.main(argv: list[str] | None = None) -> int`
- Produces: `bashref.__version__: str`

- [ ] **Step 1: Write the failing entry-point tests**

```python
from bashref import __version__
from bashref.cli import main

def test_version_constant_is_v2_development_line():
    assert __version__ == "2.0.0"

def test_main_version_prints_version(capsys):
    assert main(["--version"]) == 0
    assert capsys.readouterr().out.strip() == "bashref 2.0.0"
```

- [ ] **Step 2: Run the focused test and verify failure**

Run:
```bash
python -m pytest tests/cli/test_entrypoint.py -q
```

Expected: import failure because `bashref` does not yet exist.

- [ ] **Step 3: Add minimal package implementation**

`src/bashref/__init__.py`:
```python
__version__ = "2.0.0"
```

`src/bashref/__main__.py`:
```python
from .cli import main

raise SystemExit(main())
```

`src/bashref/cli.py`:
```python
from __future__ import annotations
import argparse
from . import __version__

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bashref")
    parser.add_argument("--version", action="version", version=f"bashref {__version__}")
    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0
```

`pyproject.toml` defines setuptools, `requires-python = ">=3.10"`, package discovery under `src`, and:
```toml
[project.scripts]
bashref = "bashref.cli:main"
```

- [ ] **Step 4: Install editable package and run tests**

Run:
```bash
python -m pip install -e .
python -m pytest tests/cli/test_entrypoint.py -q
bashref --version
```

Expected: tests pass and command prints `bashref 2.0.0`.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/bashref tests/cli/test_entrypoint.py
git commit -m "feat: add bashref package and CLI entry point"
```

### Task 2: Reference schema, seed records, and validator

**Files:**
- Create: `reference/schema/record.schema.json`
- Create: `reference/en/builtins/printf.json`
- Create: `reference/fa/builtins/printf.json`
- Create: `tools/validate_reference.py`
- Create: `tests/reference/test_validation.py`

**Interfaces:**
- Produces: `validate_record(data: dict) -> list[str]`
- Produces: `validate_tree(root: Path) -> list[str]`
- Record identity: `id = "builtin.printf"`

- [ ] **Step 1: Write failing validator tests**

Tests must assert that a valid bilingual `printf` pair passes, a missing required field fails, mismatched Persian/English IDs fail parity, and a record whose `language` does not match its tree fails.

- [ ] **Step 2: Run validator tests**

Run:
```bash
python -m pytest tests/reference/test_validation.py -q
```

Expected: FAIL because validator/schema do not exist.

- [ ] **Step 3: Implement schema and validator**

The JSON schema file documents required fields:
`id`, `kind`, `name`, `language`, `summary`, `synopsis`, `description`, `examples`, `related`, `sources`.

`tools/validate_reference.py` performs validation using standard library only:
- parse all `*.json`
- required field/type checks
- allowed language `en|fa`
- allowed kind set
- ID pattern check
- duplicate ID check per language
- exact EN/FA ID parity
- related-ID existence check
- `https://` source URL requirement

- [ ] **Step 4: Run tests and direct validator**

Run:
```bash
python -m pytest tests/reference/test_validation.py -q
python tools/validate_reference.py
```

Expected: PASS and validator prints a success count.

- [ ] **Step 5: Commit**

```bash
git add reference tools/validate_reference.py tests/reference/test_validation.py
git commit -m "feat: define bilingual reference record contract"
```

### Task 3: Deterministic package-data compiler and manifest

**Files:**
- Create: `tools/build_reference.py`
- Create: `src/bashref/data/.gitkeep`
- Create: `tests/reference/test_build_reference.py`
- Modify: `pyproject.toml`

**Interfaces:**
- Produces: `build_reference(source_root: Path, output_root: Path, version: str) -> dict`
- Produces generated `manifest.json`
- Produces packaged records under `src/bashref/data/{en,fa}/...`

- [ ] **Step 1: Write failing reproducibility tests**

Build into two temporary directories and assert byte-for-byte identical manifests and record files, sorted record IDs, and no absolute filesystem paths in output.

- [ ] **Step 2: Verify failure**

Run:
```bash
python -m pytest tests/reference/test_build_reference.py -q
```

- [ ] **Step 3: Implement deterministic compiler**

Compiler:
- calls validation first
- canonicalizes JSON with UTF-8, sorted keys, `ensure_ascii=False`, newline termination
- stores manifest keys `format_version`, `product_version`, `languages`, `record_count`, `records`
- copies only validated fields
- writes in stable ID/path order

Update package-data configuration so `src/bashref/data/**/*.json` is included in wheel/sdist.

- [ ] **Step 4: Run build twice and compare**

Run:
```bash
python tools/build_reference.py
python -m pytest tests/reference/test_build_reference.py -q
git diff --exit-code -- src/bashref/data
```

Expected: PASS after committed generated seed output.

- [ ] **Step 5: Commit**

```bash
git add tools/build_reference.py src/bashref/data pyproject.toml tests/reference/test_build_reference.py
git commit -m "feat: compile deterministic packaged reference data"
```

### Task 4: Reference loader and stable domain errors

**Files:**
- Create: `src/bashref/errors.py`
- Create: `src/bashref/reference.py`
- Create: `tests/reference/test_loader.py`

**Interfaces:**
- Produces `ReferenceErrorBase`, `EntryNotFoundError`, `CorruptReferenceError`
- Produces `ReferenceStore.load() -> ReferenceStore`
- Produces `ReferenceStore.get(query: str, language: str) -> dict`
- Produces `ReferenceStore.list(kind: str | None, language: str) -> list[dict]`

- [ ] **Step 1: Write failing loader tests**

Cover canonical ID, name, alias, missing entry, invalid manifest JSON, duplicate alias ambiguity, and no filesystem escape.

- [ ] **Step 2: Run tests and confirm failure**

```bash
python -m pytest tests/reference/test_loader.py -q
```

- [ ] **Step 3: Implement loader**

Use `importlib.resources.files("bashref.data")`; never accept a user-controlled path. Build in-memory indexes by ID, lower-cased name, and aliases. Raise `CorruptReferenceError` for invalid packaged data and `EntryNotFoundError` for direct lookup misses.

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/reference/test_loader.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/bashref/errors.py src/bashref/reference.py tests/reference/test_loader.py
git commit -m "feat: load and resolve packaged Bash reference records"
```

### Task 5: Language resolution and user config

**Files:**
- Create: `src/bashref/languages.py`
- Create: `src/bashref/config.py`
- Create: `tests/cli/test_languages.py`

**Interfaces:**
- Produces `resolve_language(explicit: str | None, configured: str | None, environ: Mapping[str,str]) -> str`
- Produces `load_config(path: Path | None = None) -> dict[str, str]`
- Produces `save_language(language: str, path: Path | None = None) -> None`

- [ ] **Step 1: Write precedence tests**

Assert explicit > config > Persian locale > English fallback. Assert `--lang en` wins against `LANG=fa_IR.UTF-8`. Assert malformed config is ignored with English fallback rather than crashing.

- [ ] **Step 2: Verify tests fail**

```bash
python -m pytest tests/cli/test_languages.py -q
```

- [ ] **Step 3: Implement language/config modules**

Use platform config roots:
- Windows: `APPDATA/bashref/config.json`
- Unix: `XDG_CONFIG_HOME/bashref/config.json` or `~/.config/bashref/config.json`

Only persist `{"language":"fa"}` or `{"language":"en"}`.

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/cli/test_languages.py -q
```

- [ ] **Step 5: Commit**

```bash
git add src/bashref/languages.py src/bashref/config.py tests/cli/test_languages.py
git commit -m "feat: add bilingual language preference resolution"
```

### Task 6: Safe text and JSON renderer

**Files:**
- Create: `src/bashref/renderer.py`
- Create: `tests/renderer/test_renderer.py`

**Interfaces:**
- Produces `render_record(record: dict, *, format: str, color: bool, width: int) -> str`
- Produces `render_records(records: list[dict], *, format: str, color: bool, width: int) -> str`
- Produces `render_error(code: int, message: str, suggestions: list[str], *, format: str) -> str`

- [ ] **Step 1: Write renderer tests**

Cover Persian UTF-8 preservation, deterministic JSON key order, terminal-control sanitization using `"bad\x1b[2Jtext"`, text wrapping, and structured error keys `error/code/message/suggestions`.

- [ ] **Step 2: Verify failure**

```bash
python -m pytest tests/renderer/test_renderer.py -q
```

- [ ] **Step 3: Implement renderer**

Sanitize C0 controls except newline/tab before terminal text rendering. JSON uses `json.dumps(..., ensure_ascii=False, sort_keys=True)`. Do not emit ANSI unless requested by caller.

- [ ] **Step 4: Run tests**

```bash
python -m pytest tests/renderer/test_renderer.py -q
```

- [ ] **Step 5: Commit**

```bash
git add src/bashref/renderer.py tests/renderer/test_renderer.py
git commit -m "feat: render safe text and JSON reference output"
```

### Task 7: Search index and offline ranking

**Files:**
- Create: `src/bashref/search.py`
- Create: `tools/build_search_index.py`
- Create: `tests/search/test_search.py`
- Modify: `tools/build_reference.py`

**Interfaces:**
- Produces `SearchEngine.search(query: str, language: str, limit: int = 20) -> list[dict]`
- Produces generated `search-index.json`

- [ ] **Step 1: Write ranking tests**

Test exact name above alias, alias above prefix, prefix above tag, empty query rejected as usage at CLI boundary, zero result list is valid, duplicate aliases do not duplicate a record, and typo `pritnf` suggests `printf`.

- [ ] **Step 2: Verify failure**

```bash
python -m pytest tests/search/test_search.py -q
```

- [ ] **Step 3: Implement deterministic index and ranking**

Normalize with Unicode `casefold()`. Score fields exactly:
- exact ID/name: 100
- exact alias: 90
- name/alias prefix: 70
- tag exact/prefix: 50
- summary token match: 30
- description token match: 10

Tie-break by canonical ID.

- [ ] **Step 4: Run search tests and determinism check**

```bash
python tools/build_search_index.py
python -m pytest tests/search/test_search.py -q
git diff --exit-code -- src/bashref/data/search-index.json
```

- [ ] **Step 5: Commit**

```bash
git add src/bashref/search.py tools/build_search_index.py tools/build_reference.py src/bashref/data/search-index.json tests/search/test_search.py
git commit -m "feat: add deterministic offline reference search"
```

### Task 8: Full CLI command surface and exit-code contract

**Files:**
- Modify: `src/bashref/cli.py`
- Create: `src/bashref/commands.py`
- Create: `tests/cli/test_commands.py`
- Create: `tests/cli/test_exit_codes.py`

**Interfaces:**
- Consumes: `ReferenceStore`, `SearchEngine`, language/config, renderer
- Produces subcommands: `search`, `show`, `builtin`, `syntax`, `expansion`, `option`, `shopt`, `variable`, `example`, `list`, `lang`

- [ ] **Step 1: Write CLI integration tests**

Use `main([...])` to pin:
- `search printf`
- `builtin printf`
- `--format json builtin printf`
- missing direct lookup returns 3
- malformed store returns 4
- unknown argparse command returns 2
- empty search result returns 0
- `lang fa` persists and prints confirmation

- [ ] **Step 2: Verify failure**

```bash
python -m pytest tests/cli/test_commands.py tests/cli/test_exit_codes.py -q
```

- [ ] **Step 3: Implement command dispatch**

Do not use `sys.exit` inside command handlers. `main()` catches domain errors and returns stable codes; `__main__` performs the final `SystemExit`.

- [ ] **Step 4: Run CLI tests and smoke commands**

```bash
python -m pytest tests/cli/test_commands.py tests/cli/test_exit_codes.py -q
bashref --lang en builtin printf
bashref --lang fa builtin printf
bashref --format json search printf
```

- [ ] **Step 5: Commit**

```bash
git add src/bashref/cli.py src/bashref/commands.py tests/cli
git commit -m "feat: expose Bash reference lookup and search commands"
```

### Task 9: docs/man URL resolution and shell completions

**Files:**
- Create: `src/bashref/completion.py`
- Create: `tests/cli/test_completion.py`
- Modify: `src/bashref/cli.py`
- Modify: `src/bashref/commands.py`

**Interfaces:**
- Produces `completion_script(shell: str) -> str`
- Produces `docs_url(record: dict | None, language: str) -> str`
- `bashref man [TOPIC]` invokes local `man` only when available; otherwise prints the man-page name and exits 0.
- `bashref docs [TOPIC]` prints the validated project URL; `--open` opens only URLs constructed from trusted IDs.

- [ ] **Step 1: Write completion and URL tests**

Pin output headers for Bash/Zsh/Fish; reject unknown shell; assert docs URL cannot be influenced by `../` in user input; assert record IDs map to fixed website paths.

- [ ] **Step 2: Verify failure**

```bash
python -m pytest tests/cli/test_completion.py -q
```

- [ ] **Step 3: Implement generation and URL mapping**

Completion scripts enumerate static subcommands and defer record names to `bashref list --format json` only when the user explicitly requests dynamic completion. Core generation itself requires no network.

- [ ] **Step 4: Run tests and smoke output**

```bash
python -m pytest tests/cli/test_completion.py -q
bashref completion bash | head
bashref completion zsh | head
bashref completion fish | head
```

- [ ] **Step 5: Commit**

```bash
git add src/bashref/completion.py src/bashref/cli.py src/bashref/commands.py tests/cli/test_completion.py
git commit -m "feat: add docs man routing and shell completions"
```

### Task 10: Build/install smoke test and core-phase documentation

**Files:**
- Create: `tests/integration/test_installed_cli.py`
- Create: `docs/en/install/cli.md`
- Create: `docs/fa/install/cli.md`
- Modify: `README.md`
- Modify: `README.fa.md`
- Modify: `CHANGELOG.md`
- Modify: `.github/workflows/docs.yml`

**Interfaces:**
- CI continues to publish status name `docs / build-and-deploy`.

- [ ] **Step 1: Add failing install smoke stage**

The integration test invokes the installed `bashref` executable with:
`--version`, `search printf`, `builtin printf`, `--format json builtin printf`.

- [ ] **Step 2: Run full suite locally/CI**

```bash
python -m pytest -q
python -m build
python -m pip install --force-reinstall dist/*.whl
python -m pytest tests/integration/test_installed_cli.py -q
```

Expected before workflow/dependency adjustment: build step fails if `build` is unavailable in CI.

- [ ] **Step 3: Add build/test dependencies and CI steps**

Use build-time dependencies only:
```text
pytest
build
```

Keep MkDocs dependencies in `requirements.txt`; add a separate `requirements-dev.txt` if needed so runtime package metadata remains dependency-free.

CI order before docs QA:
1. validate reference
2. build packaged data/index
3. pytest
4. build wheel/sdist
5. isolated wheel install smoke test

- [ ] **Step 4: Verify complete phase**

```bash
python tools/validate_reference.py
python tools/build_reference.py
python tools/build_search_index.py
python -m pytest -q
python -m build
```

Then verify `git diff --exit-code` after generation.

- [ ] **Step 5: Commit**

```bash
git add tests/integration docs/en/install docs/fa/install README.md README.fa.md CHANGELOG.md .github/workflows/docs.yml requirements-dev.txt
git commit -m "ci: validate installable bashref core product"
```
