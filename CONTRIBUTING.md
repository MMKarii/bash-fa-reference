# Contributing

Contributions are welcome when they improve software quality, Bash accuracy, translation quality, packaging, accessibility, examples, tests, or documentation.

## Repository areas

- `src/bashref/`: CLI/runtime code
- `reference/en/` and `reference/fa/`: canonical structured reference records
- `docs/en/` and `docs/fa/`: Professional Guide and editorial documentation
- `tools/`: deterministic generators and release tooling
- `tests/`: software, reference, integration, and packaging tests
- `packaging/`: Linux packages, completions, standalone entry point, and Homebrew template
- `.github/workflows/`: CI, packaging, deployment, and release automation

Generated reference pages under `docs/*/reference/generated/` and packaged data under `src/bashref/data/` must be regenerated from canonical source rather than edited by hand.

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e .
```

On Windows PowerShell use the matching `.venv\Scripts\Activate.ps1`.

## Required validation

Run focused tests while developing, then the full gate before opening a PR:

```bash
VERSION="$(python -c 'import bashref; print(bashref.__version__)')"
python tools/validate_reference.py
python tools/build_reference.py --version "$VERSION"
python tools/build_search_index.py
python tools/build_completions.py
python tools/build_docs_reference.py
python tools/build_manpages.py
python -m pytest -q
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/check_docs.py
python scripts/check_external_links.py
mkdocs build --strict -f mkdocs.fa.yml
mkdocs build --strict -f mkdocs.en.yml
```

CI additionally builds Python distributions, DEB/RPM packages, and standalone executables on Linux, macOS, and Windows.

## Reference changes

1. Keep English and Persian record IDs synchronized.
2. Cite GNU Bash documentation for Bash-specific semantics.
3. Preserve literal shell syntax in synopsis and example fields.
4. Add/update tests when introducing required coverage.
5. Regenerate packaged data and generated documentation.

## Software changes

Use test-driven development for behavior changes: add a failing test, implement the smallest correct behavior, then run the affected test set. Keep documented exit codes and JSON output backward compatible within a major release.

## Safety and privacy

- Never commit passwords, tokens, private keys, cookies, production credentials, or private infrastructure.
- Use `example.test`, localhost, or documentation address ranges.
- Keep privileged or destructive commands explicit and defensive.
- Bashref must never execute reference examples.
