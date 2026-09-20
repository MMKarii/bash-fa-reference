# Bash Professional Reference — فارسی + English

![Bash Professional Reference](docs/en/assets/brand-banner.webp)

A structured bilingual Bash reference for shell fundamentals, scripting, automation, system administration, DevOps, defensive security, debugging, and portability.

**مطالعه فارسی:** [docs/fa/index.md](docs/fa/index.md)  
**English edition:** [docs/en/index.md](docs/en/index.md)

## Scope

This repository consolidates and professionally restructures the supplied Bash articles into parallel Persian and English documentation. It preserves the original emphasis on command-line fundamentals, text processing, automation, system administration, DevOps, security practices, Zsh/Fish comparison, debugging, glossary material, and practical examples.

Technical behavior that is easy to misstate—especially `set -e`, pipelines, quoting, exit status, and portability—is cross-checked against the GNU Bash Reference Manual. Shell scripts shown here are intended for owned systems, controlled labs, and routine administration.

## Documentation map

- 14 mirrored chapters in `docs/fa/` and `docs/en/`
- learning path, cheat sheet, glossary, references, and disclaimer
- strict MkDocs builds for RTL Persian and LTR English
- link, anchor, translation-drift, metadata, and accessibility QA
- version aliases: `latest` and stable `v1.0`
- deployable `gh-pages` output

## Quality

CI tests the documentation tooling, checks local links and anchors, checks external links for deterministic 404/410 failures, builds both languages with `--strict`, validates built-site metadata/accessibility, and verifies the full published output.

## License

Documentation is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code snippets are examples for education and administration; review them before production use.
