# Bashref Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce reproducible installation artifacts for Python, Debian, RPM, portable use, man pages, and shell completions, with smoke tests and explicit split licensing.

**Architecture:** The wheel/sdist are canonical Python artifacts. Linux packages wrap the built wheel and install man/completion assets. All artifacts derive from the same version and generated reference output, and checksums are produced only after artifact verification.

**Tech Stack:** Python build, setuptools, dpkg-deb, rpmbuild, shell scripts, GitHub Actions Ubuntu runners.

**Spec:** `docs/superpowers/specs/2026-09-22-bashref-product-design.md`

## Global Constraints

- Runtime Python >=3.10.
- Wheel must be `py3-none-any`.
- Core runtime has no third-party dependencies.
- Software license MIT; docs CC BY 4.0.
- Packages include man pages, completions, licenses, and reference data.
- Build artifacts are versioned from one source of truth.

## Review Focus

1. Wheel installation in a clean environment must include reference JSON, not only Python modules.
2. Debian/RPM uninstall must not remove unrelated user config files.
3. Artifact version must fail the build if tag/package/version metadata disagree.
4. Completion files must be installed under distro-appropriate paths without executing the CLI at package install time.
5. Checksums must be generated after all artifacts are final and verify successfully.

---

### Task 1: Split-license repository layout

**Files:**
- Create: `LICENSES/MIT.txt`
- Create: `LICENSES/CC-BY-4.0.txt`
- Modify: `LICENSE`
- Modify: `pyproject.toml`
- Modify: `README.md`
- Modify: `README.fa.md`

**Interfaces:**
- Root license explains path scopes: software vs documentation.

- [ ] Add a failing packaging metadata test asserting project license expression/reference is MIT for software and both license files ship in sdist.
- [ ] Add exact standard MIT text and existing CC BY 4.0 legal reference text.
- [ ] Update metadata/readmes.
- [ ] Build sdist and inspect archive contents.
- [ ] Commit with `legal: define software and documentation license scopes`.

### Task 2: Reproducible wheel and sdist verification

**Files:**
- Create: `tests/packaging/test_python_artifacts.py`
- Create: `tools/verify_python_artifacts.py`
- Modify: `pyproject.toml`

**Interfaces:**
- `verify_wheel(path: Path, expected_version: str) -> list[str]`
- `verify_sdist(path: Path, expected_version: str) -> list[str]`

- [ ] Write tests asserting console entry point, package data, license files, Python floor, version, and wheel tag.
- [ ] Build artifacts and verify failing assertions until metadata is complete.
- [ ] Implement verifier using `zipfile`/`tarfile` and metadata parsing.
- [ ] Build twice in clean dirs and compare logical archive content manifests.
- [ ] Commit with `build: verify Python distribution artifacts`.

### Task 3: Versioned shell-completion assets

**Files:**
- Create: `packaging/completions/bash/bashref`
- Create: `packaging/completions/zsh/_bashref`
- Create: `packaging/completions/fish/bashref.fish`
- Create: `tools/build_completions.py`
- Create: `tests/packaging/test_completions.py`

**Interfaces:**
- Generation delegates to `bashref.completion.completion_script`.

- [ ] Write tests comparing generated assets to runtime completion output.
- [ ] Generate all three committed assets deterministically.
- [ ] Verify shell syntax with available `bash -n`; keep zsh/fish checks in CI on environments providing those shells.
- [ ] Run generation twice and assert no diff.
- [ ] Commit with `build: package Bash Zsh and Fish completions`.

### Task 4: Debian package

**Files:**
- Create: `packaging/deb/build_deb.py`
- Create: `tests/packaging/test_deb_layout.py`
- Create: `packaging/deb/README.md`

**Interfaces:**
- Produces `dist/bashref_<version>_all.deb`.

- [ ] Write layout test for `/usr/bin/bashref` wrapper/entry, Python payload under distro-neutral app location, `/usr/share/man/man1/bashref.1.gz`, `/usr/share/man/man5/bashref-reference.5.gz`, completions, copyright/license.
- [ ] Implement package-root assembly and `dpkg-deb --build`.
- [ ] Install into a disposable Ubuntu container/runner and run `bashref --version`, `bashref builtin printf`, `man -w bashref`.
- [ ] Remove package and assert project-installed files are removed while `~/.config/bashref` remains untouched.
- [ ] Commit with `build: add Debian package generation`.

### Task 5: RPM package

**Files:**
- Create: `packaging/rpm/bashref.spec.in`
- Create: `packaging/rpm/build_rpm.py`
- Create: `tests/packaging/test_rpm_spec.py`

**Interfaces:**
- Produces `dist/bashref-<version>-1.noarch.rpm`.

- [ ] Write spec-rendering tests for version, license, files, man pages, and completions.
- [ ] Implement spec rendering and `rpmbuild` source staging.
- [ ] Build and query package contents with `rpm -qlp`.
- [ ] Smoke-install on an RPM-capable CI job/container and run core commands.
- [ ] Commit with `build: add RPM package generation`.

### Task 6: Homebrew formula template

**Files:**
- Create: `packaging/homebrew/bashref.rb.in`
- Create: `tools/render_homebrew_formula.py`
- Create: `tests/packaging/test_homebrew_formula.py`

**Interfaces:**
- Renderer accepts release version, sdist URL, SHA256 and emits formula.

- [ ] Write exact render test for version/url/hash and `virtualenv_install_with_resources`-free installation because runtime has no third-party resources.
- [ ] Implement deterministic formula renderer.
- [ ] Run Ruby syntax check when `ruby` exists.
- [ ] Commit with `build: add Homebrew release formula template`.

### Task 7: Portable archive, man archive, completion archive, SHA256SUMS

**Files:**
- Create: `tools/build_release_assets.py`
- Create: `tools/write_checksums.py`
- Create: `tests/packaging/test_release_assets.py`

**Interfaces:**
- Produces:
  - `bashref-<version>-portable.tar.gz`
  - `bashref-<version>-manpages.tar.gz`
  - `bashref-<version>-completions.tar.gz`
  - `SHA256SUMS`

- [ ] Write tests pinning archive members and sorted checksum line order.
- [ ] Implement archive creation with normalized timestamps/ownership metadata where Python tar APIs allow it.
- [ ] Verify every checksum using a Python verifier and `sha256sum -c` on Linux.
- [ ] Build twice and compare logical manifests/checksums.
- [ ] Commit with `build: assemble portable release assets and checksums`.

### Task 8: Packaging matrix workflow

**Files:**
- Create: `.github/workflows/package.yml`
- Modify: `.github/workflows/docs.yml` to call or replicate the required smoke gate while preserving its status context.

**Interfaces:**
- PR must not merge unless the protected `docs / build-and-deploy` context includes package smoke validation or depends on a successful packaging job.

- [ ] Add workflow jobs for Python artifacts, Debian, RPM, and cross-platform Python smoke tests.
- [ ] Run Python matrix for supported versions and OS-relevant smoke tests on Ubuntu/macOS/Windows.
- [ ] Upload artifacts for CI inspection without publishing releases.
- [ ] Ensure final protected job fails if any required packaging job fails.
- [ ] Commit with `ci: test Bashref packaging across supported platforms`.

## Exact implementation skeletons

These signatures and layouts are normative for the packaging tasks above.

~~~python
# tools/verify_python_artifacts.py
from pathlib import Path
from zipfile import ZipFile
import tarfile

def verify_wheel(path: Path, expected_version: str) -> list[str]:
    issues = []
    with ZipFile(path) as archive:
        names = set(archive.namelist())
        if not any(name.endswith("bashref/data/manifest.json") for name in names):
            issues.append("wheel missing packaged reference manifest")
        if not any("/bashref/data/en/" in "/" + name for name in names):
            issues.append("wheel missing English reference data")
        if not any("/bashref/data/fa/" in "/" + name for name in names):
            issues.append("wheel missing Persian reference data")
    return issues

def verify_sdist(path: Path, expected_version: str) -> list[str]:
    issues = []
    with tarfile.open(path, "r:gz") as archive:
        names = set(archive.getnames())
        if not any(name.endswith("/LICENSES/MIT.txt") for name in names):
            issues.append("sdist missing MIT license")
        if not any(name.endswith("/LICENSES/CC-BY-4.0.txt") for name in names):
            issues.append("sdist missing CC BY 4.0 license")
    return issues
~~~

~~~python
# tools/write_checksums.py
from hashlib import sha256
from pathlib import Path

def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def write_checksums(paths: list[Path], output: Path) -> None:
    lines = [f"{digest(path)}  {path.name}" for path in sorted(paths, key=lambda p: p.name)]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
~~~

~~~text
Debian package-owned paths
/usr/bin/bashref
/opt/bashref/2.0.0/
/usr/share/man/man1/bashref.1.gz
/usr/share/man/man5/bashref-reference.5.gz
/usr/share/bash-completion/completions/bashref
/usr/share/zsh/vendor-completions/_bashref
/usr/share/fish/vendor_completions.d/bashref.fish
/usr/share/doc/bashref/LICENSE-MIT
/usr/share/doc/bashref/LICENSE-CC-BY-4.0
~~~

RPM uses the equivalent system paths. Neither DEB nor RPM package scripts read, create, or remove files under a user's home directory.
