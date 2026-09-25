# Contributing

Contributions are welcome when they improve software behavior, technical accuracy, translation quality, accessibility, examples, packaging, or documentation tooling.

## Contribution paths

- **Software:** edit `src/bashref/` and add or update tests under `tests/`.
- **Reference records:** edit canonical JSON under `reference/en/` and `reference/fa/`. Keep record IDs paired across languages.
- **Professional Guide:** edit the mirrored long-form chapters under `docs/en/` and `docs/fa/`.
- **Packaging/release tooling:** edit `packaging/`, `tools/`, and workflow files.
- **Generated output:** do not hand-edit generated reference pages, packaged reference data, search indexes, man pages, or completion assets. Run the generators instead.

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e .
```

On Windows PowerShell, activate the virtual environment with `.venv\Scripts\Activate.ps1`.

## Required checks

Run before opening a pull request:

```bash
python tools/validate_reference.py
python tools/build_reference.py
python tools/build_search_index.py
python tools/build_docs_reference.py
python tools/build_manpages.py
python tools/build_completions.py
python -m pytest -q
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/check_docs.py
python scripts/check_external_links.py
mkdocs build --strict -f mkdocs.fa.yml -d site/fa
mkdocs build --strict -f mkdocs.en.yml -d site/en
git diff --exit-code
```

## Reference rules

1. Use GNU Bash documentation as the primary source for Bash semantics.
2. A bilingual record uses the same stable `id` in English and Persian.
3. Version-sensitive behavior must include an authoritative source URL.
4. Keep examples deterministic, reviewable, and safe on owned systems.
5. Never add real credentials, private infrastructure, or third-party production targets.
6. Do not execute example content from reference data inside the Bashref runtime.

## Pull requests

Keep changes focused. Add regression tests for software defects and update generated outputs in the same PR when canonical reference data changes. The protected `docs / build-and-deploy` check must pass before merge.
