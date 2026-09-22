# Bashref v2 Implementation Roadmap

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement these plans task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the approved Bashref v2 architecture as four independently testable implementation phases, ending in an installable bilingual Bash reference product with CLI, man pages, packaging, website integration, and release automation.

**Architecture:** Work proceeds additively so the current documentation site remains deployable at every merge. Each phase has its own plan and produces a working increment that can be reviewed and released independently.

**Tech Stack:** Python 3.10+, standard-library runtime, pytest for new software tests, JSON reference data, MkDocs Material, GitHub Actions, Linux packaging tools, mandoc, shell completion scripts.

**Spec:** `docs/superpowers/specs/2026-09-22-bashref-product-design.md`

## Global Constraints

- Installed command: `bashref`.
- Python distribution name: `bashref`.
- Repository remains `MMKarii/bash-fa-reference`.
- Website remains `https://mmkarii.github.io/bash-fa-reference/`.
- Python baseline: `Python >= 3.10`.
- Runtime dependency policy: standard library only for the core CLI.
- Core lookup/search must work offline.
- CLI must never execute Bash examples.
- Existing `v1.0.0` release and published v1 URLs remain valid.
- Existing `/fa/`, `/en/`, `/latest/fa/`, and `/latest/en/` URLs remain valid.
- Software code uses MIT; documentation remains CC BY 4.0.
- Protected status context remains exactly `docs / build-and-deploy`.
- First integrated software release is `v2.0.0`.

## Review Focus

1. A malformed packaged record must produce exit code 4 instead of a traceback.
2. Persian locale detection must not override an explicit `--lang en`.
3. Search queries containing terminal control characters must never emit untrusted control sequences.
4. Generated website/man/reference outputs must be deterministic across two consecutive clean builds.
5. Existing documentation URLs must remain valid after generated reference pages are introduced.

---

## Phase order

1. **Core product foundation**  
   Plan: `docs/superpowers/plans/2026-09-22-bashref-core-cli.md`  
   Deliverable: installable `bashref` wheel/sdist with reference loader, lookup, list, search, bilingual language handling, text/JSON rendering, stable exit codes, and completion generation.

2. **Reference corpus, man pages, and generated web reference**  
   Plan: `docs/superpowers/plans/2026-09-22-bashref-reference-publishing.md`  
   Deliverable: validated bilingual canonical reference source, required Bash builtin/concept coverage, generated man pages, generated MkDocs reference pages, and Reference/Professional Guide separation.

3. **Packaging and platform distribution**  
   Plan: `docs/superpowers/plans/2026-09-22-bashref-packaging.md`  
   Deliverable: reproducible wheel/sdist, Debian package, RPM package, completions, portable archive, checksums, installation smoke tests, and Homebrew formula template.

4. **CI, release, website portal, and v2.0.0 release**  
   Plan: `docs/superpowers/plans/2026-09-22-bashref-release-system.md`  
   Deliverable: expanded required CI, current/v2 versioned website, download/install/release pages, tag-driven artifacts, GitHub Release publication, changelog/release notes, and post-deploy verification.

## Merge discipline

- One implementation branch per phase.
- TDD for every production behavior change.
- Each task ends with a focused commit.
- A phase merges only after its own full validation passes.
- The next phase starts from the updated `main`.
- No release tag is created before Phase 4 passes end-to-end verification.
