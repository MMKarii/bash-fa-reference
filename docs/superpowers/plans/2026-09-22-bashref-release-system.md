# Bashref Release System and Website v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the repository into a complete public product portal and ship the first integrated `v2.0.0` release with verified artifacts, versioned documentation, release notes, and post-deployment checks.

**Architecture:** The existing Pages workflow remains the source of current docs, while tag builds add immutable `v2.0` snapshots. Release automation consumes already-tested package builders, creates checksums, uploads GitHub Release assets, and then verifies the public site and release metadata.

**Tech Stack:** GitHub Actions, MkDocs Material, Python release tooling, GitHub Releases API/actions, existing QA scripts.

**Spec:** `docs/superpowers/specs/2026-09-22-bashref-product-design.md`

## Global Constraints

- Protected status remains `docs / build-and-deploy`.
- `v1.0.0` and `/v1.0/` remain immutable.
- Current canonical docs stay under `/en/` and `/fa/`.
- v2 snapshot paths: `/v2.0/en/`, `/v2.0/fa/`.
- Tag releases build only from exact tag checkout.
- Release artifacts include wheel, sdist, DEB, RPM, portable archive, man archive, completion archive, checksums, docs snapshot.
- No release is marked complete until public URLs and checksums are verified.

## Review Focus

1. A tag whose version differs from `bashref.__version__` must fail before publishing anything.
2. Re-running a release workflow must not silently replace v1 or another tag's immutable docs snapshot.
3. GitHub Pages aliases must not create canonical URLs pointing at `/latest/` or `/v2.0/`.
4. A partially uploaded release must remain draft/non-final until artifact verification completes.
5. Public verification must detect a missing artifact, broken checksum, or stale Pages deployment.

---

### Task 1: Product portal navigation and landing pages

**Files:**
- Modify: `site-root/index.html`
- Modify: `mkdocs.en.yml`
- Modify: `mkdocs.fa.yml`
- Create paired:
  - `docs/*/download/index.md`
  - `docs/*/install/index.md`
  - `docs/*/releases/index.md`
  - `docs/*/about/index.md`
- Modify: `docs/*/index.md`

**Interfaces:**
- Portal exposes Documentation/Reference Guide/Builtins/Syntax/Options/Examples/Download/Installation/Releases/Contributing/Security/About.

- [ ] Add built-site tests for required portal links in both languages.
- [ ] Update root landing page from language-only selector to product portal while preserving obvious Persian/English entry points.
- [ ] Add bilingual download/install/release/about pages and navigation.
- [ ] Run strict builds, accessibility, local-link and SEO checks.
- [ ] Commit with `docs: turn Pages landing site into Bashref product portal`.

### Task 2: Versioned v2 documentation snapshot

**Files:**
- Modify: `.github/workflows/docs.yml`
- Modify: `scripts/check_built_site.py`
- Modify: `scripts/test_check_built_site.py`

**Interfaces:**
- Current build copied to `site/v2.0/{fa,en}` only for v2 tag/release policy.
- Current canonical metadata remains `/fa/` and `/en/`.

- [ ] Write failing tests for resolving root-relative project paths inside `v2.0`.
- [ ] Extend edition-root resolver from fixed `v1.0` handling to version-pattern handling such as `v\d+\.\d+`.
- [ ] Add tag-aware v2 snapshot generation that never rewrites `site/v1.0`.
- [ ] Run full built-site link checks across current/latest/v1.0/v2.0 trees.
- [ ] Commit with `feat: publish immutable v2 documentation snapshots`.

### Task 3: Unified CI gate and Python/platform matrices

**Files:**
- Modify: `.github/workflows/docs.yml`
- Modify: `.github/workflows/package.yml`
- Create: `.github/workflows/quality.yml` only if decomposition keeps final protected context stable.

**Interfaces:**
- Final required check rendered by GitHub must be exactly `docs / build-and-deploy`.

- [ ] Add a workflow-level test/documented assertion for the exact final check name.
- [ ] Arrange jobs so reference validation, unit/integration tests, package builds, man lint, completions, docs QA, and package smoke tests all feed the protected final job.
- [ ] Confirm PR check UI exposes `docs / build-and-deploy`.
- [ ] Run a branch PR and verify ruleset accepts the check.
- [ ] Commit with `ci: gate main on complete Bashref product validation`.

### Task 4: Tag/version consistency and release staging

**Files:**
- Create: `tools/release_version.py`
- Create: `tests/packaging/test_release_version.py`
- Create: `.github/workflows/release.yml`

**Interfaces:**
- `assert_release_version(tag: str, package_version: str) -> None`
- Release starts as draft.

- [ ] Write tests for `v2.0.0 == 2.0.0`, mismatch rejection, malformed tag rejection, prerelease handling if used.
- [ ] Implement exact-tag checkout and version assertion.
- [ ] Build all release artifacts from the tag and run existing verifiers.
- [ ] Create/update a draft release associated with the same tag and upload verified assets.
- [ ] Commit with `ci: stage verified tag-driven Bashref releases`.

### Task 5: Release notes and v2 changelog

**Files:**
- Create: `.github/release-notes/v2.0.0.md`
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `README.fa.md`

**Interfaces:**
- Notes distinguish Reference Guide, Professional Guide, CLI, packaging, languages, security, compatibility.

- [ ] Add a check that release-note file exists for the tag version.
- [ ] Write v2.0.0 notes with install commands, major features, supported Python baseline, artifact list, checksum verification example, upgrade notes from docs-only v1.
- [ ] Update top-level README quick-start to prefer installed CLI plus live docs.
- [ ] Run local link checks.
- [ ] Commit with `docs: prepare Bashref v2.0.0 release notes`.

### Task 6: Public release verification script

**Files:**
- Create: `tools/verify_public_release.py`
- Create: `tests/integration/test_public_release_verifier.py`

**Interfaces:**
- Verifier accepts release JSON/asset listing plus base site URL via dependency-injected fetcher for tests.
- Validates expected artifact names, checksum membership, Pages markers, current/v2 docs endpoints.

- [ ] Write fake-fetcher tests for missing artifact, stale site marker, checksum mismatch, and successful release.
- [ ] Implement verifier without hard-coding credentials.
- [ ] Add final workflow step that runs only after Pages deployment and release upload.
- [ ] Keep release draft if verification fails.
- [ ] Commit with `test: verify published Bashref release and documentation`.

### Task 7: Create and publish v2.0.0

**Files:**
- No production code unless verification exposes a defect.
- Tag: `v2.0.0`.

**Interfaces:**
- Exact release artifact set defined by spec.

- [ ] On a clean `main`, run:
```bash
python tools/validate_reference.py
python tools/build_reference.py
python tools/build_search_index.py
python tools/build_docs_reference.py
python tools/build_manpages.py
python tools/build_completions.py
python -m pytest -q
python -m build
git diff --exit-code
```
- [ ] Verify current main CI success.
- [ ] Create annotated `v2.0.0` tag from the verified commit.
- [ ] Let release workflow build/upload draft artifacts and Pages snapshot.
- [ ] Run public verifier and checksum validation.
- [ ] Publish/finalize release only after successful verification.

### Task 8: Post-release repository verification

**Files:**
- Modify documentation only if actual published URLs differ from expected deployment configuration.

- [ ] Verify live root, Persian, English, Reference Guide, Professional Guide, install, download, `/v2.0/fa/`, `/v2.0/en/`, robots, sitemap.
- [ ] Verify GitHub release has all required assets and `SHA256SUMS` covers every downloadable artifact.
- [ ] Verify fresh wheel installation and core CLI commands from released artifact.
- [ ] Verify main branch ruleset still requires `docs / build-and-deploy`.
- [ ] Record release completion in changelog if any post-release metadata is required, without moving the v2 tag.
