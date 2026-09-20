# Contributing

Contributions are welcome when they improve technical accuracy, translation quality, accessibility, examples, or documentation tooling.

## Before opening a PR

1. Keep Persian and English file structure synchronized.
2. Do not add real credentials, private infrastructure, or third-party targets.
3. Prefer GNU Bash documentation for Bash semantics.
4. Run:
   - `python -m unittest discover -s scripts -p 'test_*.py'`
   - `python scripts/check_docs.py`
   - `python scripts/check_external_links.py`
   - `mkdocs build --strict -f mkdocs.fa.yml`
   - `mkdocs build --strict -f mkdocs.en.yml`
5. Keep examples small, reviewable, and safe to test in a lab.
