# Bash Professional Reference — فارسی + English

![Bash Professional Reference](docs/en/assets/brand-banner.webp)

A structured bilingual Bash reference and offline CLI for shell fundamentals, scripting, automation, system administration, DevOps, defensive security, debugging, and portability.

**Live documentation:** https://mmkarii.github.io/bash-fa-reference/  
**مطالعه فارسی:** https://mmkarii.github.io/bash-fa-reference/fa/  
**English edition:** https://mmkarii.github.io/bash-fa-reference/en/

## Bashref CLI

Bashref 2.0.0 provides an installable offline CLI backed by the same bilingual reference data:

```bash
pipx install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.0.0/bashref-2.0.0-py3-none-any.whl
bashref --version
bashref search printf
bashref builtin printf
bashref --lang fa builtin printf
bashref --format json builtin printf
```

The CLI runtime uses only the Python standard library. Release artifacts are published on GitHub Releases, and the existing v1.0 documentation snapshot remains available unchanged.

## Scope

This repository consolidates and professionally restructures the supplied Bash articles into parallel Persian and English documentation. It preserves the original emphasis on command-line fundamentals, text processing, automation, system administration, DevOps, security practices, Zsh/Fish comparison, debugging, glossary material, and practical examples.

Technical behavior that is easy to misstate—especially `set -e`, pipelines, quoting, exit status, and portability—is cross-checked against the GNU Bash Reference Manual. Shell scripts shown here are intended for owned systems, controlled labs, and routine administration.

## Documentation map

- installable `bashref` CLI with offline bilingual lookup/search
- deterministic structured reference data under `reference/`
- 14 mirrored chapters in `docs/fa/` and `docs/en/`
- learning path, cheat sheet, glossary, references, and disclaimer
- strict MkDocs builds for RTL Persian and LTR English
- page-matched Persian/English language switching and hreflang metadata
- link, anchor, translation-drift, metadata, and accessibility QA
- version aliases: `latest`, stable `v1.0`, and stable `v2.0`
- GitHub Pages deployment from `gh-pages`

## Quality

CI tests the documentation tooling, checks local links and anchors, checks external links for deterministic 404/410 failures, builds both languages with `--strict`, validates built-site metadata/accessibility, and verifies the full published output.

## License

Documentation is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code snippets are examples for education and administration; review them before production use.
