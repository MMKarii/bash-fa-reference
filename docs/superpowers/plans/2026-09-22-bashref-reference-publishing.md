# Bashref Reference Publishing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the canonical bilingual reference to the v2 acceptance set and generate man pages plus MkDocs Reference Guide pages from the same source records.

**Architecture:** Reference records remain canonical. Generators transform validated records into roff man pages and generated Markdown while the existing 14-chapter Professional Guide remains editorial content. Generation is deterministic, bilingual IDs are paired, and authoritative-source metadata is retained in outputs.

**Tech Stack:** Python 3.10+ standard library, JSON, MkDocs Material, roff/mdoc-compatible output, mandoc lint in CI.

**Spec:** `docs/superpowers/specs/2026-09-22-bashref-product-design.md`

## Global Constraints

- Canonical reference source is `reference/{en,fa}`.
- Generated pages are never edited manually.
- EN/FA IDs must match exactly.
- Version-sensitive claims require authoritative primary-source URLs.
- Existing handbook pages and URLs remain intact.
- Required man pages: `bashref(1)`, `bashref-reference(5)`.
- Current site canonical roots remain `/en/` and `/fa/`.

## Review Focus

1. A record translated under the wrong ID must fail before docs generation.
2. Markdown special characters in synopsis/examples must be escaped without changing literal shell syntax.
3. Roff-leading dots/apostrophes in user-visible reference text must be escaped to prevent macro injection.
4. Two clean generation runs must be byte-identical.
5. A generated peer-language link must land on the same canonical record ID.

---

### Task 1: Expand record kinds and generation fixtures

**Files:**
- Modify: `reference/schema/record.schema.json`
- Create: `tests/reference/test_record_kinds.py`
- Create representative EN/FA fixtures under:
  - `reference/*/syntax/quoting.json`
  - `reference/*/expansions/parameter.json`
  - `reference/*/options/pipefail.json`
  - `reference/*/shopt/globstar.json`
  - `reference/*/variables/bash_source.json`
  - `reference/*/concepts/redirection.json`
  - `reference/*/examples/pipeline.json`

**Interfaces:**
- Supported kinds: `builtin`, `syntax`, `expansion`, `option`, `shopt`, `variable`, `concept`, `example`.

- [ ] Write tests asserting every kind validates and IDs use `kind.slug`.
- [ ] Run `pytest tests/reference/test_record_kinds.py -q` and confirm failure.
- [ ] Extend validator/schema and add paired authoritative-source fixtures.
- [ ] Run validator plus tests and confirm pass.
- [ ] Commit with `feat: support complete Bash reference record kinds`.

### Task 2: Required builtin corpus

**Files:**
- Create paired records under `reference/en/builtins/` and `reference/fa/builtins/`.
- Create: `tests/reference/test_required_builtins.py`.

**Interfaces:**
- `REQUIRED_BUILTINS: frozenset[str]` in validator/test helper.

- [ ] Write a failing coverage test containing the exact v2 required builtin set from the spec.
- [ ] Run the coverage test and record the missing IDs.
- [ ] Add paired records for every required builtin with summary, synopsis, description, exit status where meaningful, examples, related IDs, and authoritative sources.
- [ ] Run `python tools/validate_reference.py` and the coverage test.
- [ ] Commit in reviewer-sized alphabetical batches, each batch ending green. Final commit message: `docs: complete bilingual Bash builtin reference`.

### Task 3: Required language/concept corpus

**Files:**
- Create paired records under syntax, expansions, options, shopt, variables, concepts, examples.
- Create: `tests/reference/test_required_topics.py`.

**Interfaces:**
- Required topic IDs cover quoting, expansions, arrays, conditionals, loops, functions, pipelines, redirections, here-documents, here-strings, subshells, grouping, exit status, traps/signals, job control, shell options, shopt, startup files, environment, debugging, portability, defensive scripting.

- [ ] Write the failing required-topic ID test.
- [ ] Add records in coherent topic batches with authoritative GNU Bash citations for version-sensitive semantics.
- [ ] Validate related-ID integrity after each batch.
- [ ] Run search regression tests to ensure new records do not destabilize exact-match ranking.
- [ ] Commit final corpus with `docs: complete bilingual Bash language reference`.

### Task 4: Man-page renderer

**Files:**
- Create: `tools/build_manpages.py`
- Create: `tests/renderer/test_manpages.py`
- Create generated: `man/bashref.1`, `man/bashref-reference.5`, `man/generated/*.5`

**Interfaces:**
- Produces `escape_roff(text: str) -> str`
- Produces `render_cli_manpage(...) -> str`
- Produces `render_reference_manpage(record: dict) -> str`

- [ ] Write failing tests for roff escaping, section headers, synopsis preservation, UTF-8 Persian content, and deterministic ordering.
- [ ] Run focused tests.
- [ ] Implement renderer with explicit escaping for leading `.`, leading `'`, backslash, and hyphen where roff requires it.
- [ ] Generate pages twice and assert byte identity; run `mandoc -Tlint man/bashref.1 man/bashref-reference.5`.
- [ ] Commit with `feat: generate Bashref system man pages`.

### Task 5: Generated MkDocs Reference Guide pages

**Files:**
- Create: `tools/build_docs_reference.py`
- Create: `tests/renderer/test_docs_generation.py`
- Generate under `docs/en/reference/generated/` and `docs/fa/reference/generated/`
- Create curated landing pages `docs/en/reference/index.md`, `docs/fa/reference/index.md`

**Interfaces:**
- Produces `record_doc_path(record: dict) -> Path`
- Produces `render_markdown_record(record: dict) -> str`

- [ ] Write tests for deterministic paths, paired language paths, Markdown escaping, source links, related links, and generated-file header.
- [ ] Verify failure.
- [ ] Implement generator and create landing indexes grouped by kind.
- [ ] Generate twice and verify `git diff --exit-code`.
- [ ] Commit with `feat: generate bilingual web Reference Guide`.

### Task 6: Professional Guide separation and navigation

**Files:**
- Modify: `mkdocs.en.yml`
- Modify: `mkdocs.fa.yml`
- Modify: `docs/en/index.md`
- Modify: `docs/fa/index.md`
- Create: `docs/en/book/index.md`
- Create: `docs/fa/book/index.md`
- Modify existing handbook navigation only by grouping, not changing existing file URLs.

**Interfaces:**
- Website top navigation exposes Reference Guide and Professional Guide separately.

- [ ] Add a failing built-site test asserting both navigation labels exist.
- [ ] Run MkDocs strict builds and confirm test fails.
- [ ] Update navigation and landing copy while leaving chapter paths unchanged.
- [ ] Run both strict builds plus built-site QA.
- [ ] Commit with `docs: separate Reference Guide from Professional Guide`.

### Task 7: Same-record bilingual routing for generated reference pages

**Files:**
- Modify: `hooks/language_links.py`
- Modify: `scripts/test_language_links.py`
- Modify: generated page metadata as needed.

**Interfaces:**
- Generated pages expose stable `record_id` page metadata.
- Hook maps EN/FA peers by identical ID.

- [ ] Add failing test for `builtin.printf` mapping between `/en/reference/generated/builtins/printf/` and `/fa/reference/generated/builtins/printf/`.
- [ ] Implement metadata-aware mapping with existing path mapping as fallback for handbook pages.
- [ ] Build both languages and inspect generated hreflang links.
- [ ] Run language-link and built-site tests.
- [ ] Commit with `fix: keep bilingual reference switching on matching records`.

### Task 8: Reference generation in CI

**Files:**
- Modify: `.github/workflows/docs.yml`
- Modify: `requirements-dev.txt`
- Modify: `scripts/check_built_site.py` only if generated pages reveal legitimate new path forms.

**Interfaces:**
- Required check name remains exactly `docs / build-and-deploy`.

- [ ] Add a failing CI/local script check that generation produces no uncommitted diff.
- [ ] Insert validation/generation before MkDocs build.
- [ ] Add `mandoc` installation/lint on Ubuntu.
- [ ] Run full suite and both strict builds.
- [ ] Commit with `ci: verify generated reference and man pages`.

## Exact implementation skeletons

These signatures are normative for the tasks above.

~~~python
# tools/build_manpages.py
from pathlib import Path

def escape_roff(text: str) -> str:
    text = text.replace("\\", r"\e")
    out = []
    for line in text.splitlines():
        if line.startswith((".", "'")):
            line = r"\&" + line
        out.append(line.replace("-", r"\-"))
    return "\n".join(out)

def render_reference_manpage(record: dict) -> str:
    sections = [
        (".SH NAME", f"{record['name']} \\- {record['summary']}"),
        (".SH SYNOPSIS", record["synopsis"]),
        (".SH DESCRIPTION", "\n".join(record["description"])),
    ]
    return "\n".join(
        header + "\n" + escape_roff(body)
        for header, body in sections
    ) + "\n"
~~~

~~~python
# tools/build_docs_reference.py
from pathlib import Path

KIND_DIR = {
    "builtin": "builtins",
    "syntax": "syntax",
    "expansion": "expansions",
    "option": "options",
    "shopt": "shopt",
    "variable": "variables",
    "concept": "concepts",
    "example": "examples",
}

def record_doc_path(record: dict) -> Path:
    slug = record["id"].split(".", 1)[1]
    return Path(KIND_DIR[record["kind"]]) / f"{slug}.md"

def render_markdown_record(record: dict) -> str:
    header = (
        "---\n"
        "generated: true\n"
        f"record_id: {record['id']}\n"
        f"reference_kind: {record['kind']}\n"
        "---\n\n"
    )
    synopsis = f"~~~bash\n{record['synopsis']}\n~~~\n"
    description = "\n\n".join(record["description"])
    return header + f"# {record['name']}\n\n{record['summary']}\n\n## Synopsis\n\n{synopsis}\n## Description\n\n{description}\n"
~~~

~~~python
# tests/renderer/test_docs_generation.py
def test_generated_peer_uses_same_record_id(en_record, fa_record):
    assert en_record["id"] == fa_record["id"]

def test_generation_is_byte_stable(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    build_all(first)
    build_all(second)
    assert tree_bytes(first) == tree_bytes(second)
~~~

The corpus tasks use exact filename-to-ID mapping: a file named reference/en/builtins/read.json must contain id builtin.read, and its Persian peer must be reference/fa/builtins/read.json with the same id. The validator rejects any mismatch before generation.
