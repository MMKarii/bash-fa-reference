from __future__ import annotations

import email
import sys
import tarfile
import zipfile
from pathlib import Path


def _wheel_metadata(archive: zipfile.ZipFile) -> str:
    candidates = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
    if len(candidates) != 1:
        return ""
    return archive.read(candidates[0]).decode("utf-8", errors="replace")


def verify_wheel(path: Path, expected_version: str) -> list[str]:
    issues: list[str] = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if not any(name.endswith("bashref/data/manifest.json") for name in names):
                issues.append("wheel missing packaged reference manifest")
            if not any("/bashref/data/en/" in "/" + name for name in names):
                issues.append("wheel missing English reference data")
            if not any("/bashref/data/fa/" in "/" + name for name in names):
                issues.append("wheel missing Persian reference data")
            metadata_text = _wheel_metadata(archive)
            if not metadata_text:
                issues.append("wheel missing METADATA")
            else:
                metadata = email.message_from_string(metadata_text)
                if metadata.get("Version") != expected_version:
                    issues.append(
                        f"wheel version {metadata.get('Version')!r} does not match {expected_version!r}"
                    )
                requires = metadata.get_all("Requires-Dist") or []
                if requires:
                    issues.append(f"wheel declares runtime dependencies: {requires}")
    except (OSError, zipfile.BadZipFile) as exc:
        issues.append(f"invalid wheel: {exc}")
    return issues


def verify_sdist(path: Path, expected_version: str) -> list[str]:
    issues: list[str] = []
    try:
        with tarfile.open(path, "r:gz") as archive:
            names = set(archive.getnames())
            prefix = f"bashref-{expected_version}/"
            if not any(name.endswith("/LICENSES/MIT.txt") or name == prefix + "LICENSES/MIT.txt" for name in names):
                issues.append("sdist missing MIT license")
            if not any(name.endswith("/LICENSES/CC-BY-4.0.txt") or name == prefix + "LICENSES/CC-BY-4.0.txt" for name in names):
                issues.append("sdist missing CC BY 4.0 license")
            if not any(name.endswith("/reference/en/builtins/printf.json") for name in names):
                issues.append("sdist missing English reference source")
            if not any(name.endswith("/reference/fa/builtins/printf.json") for name in names):
                issues.append("sdist missing Persian reference source")
    except (OSError, tarfile.TarError) as exc:
        issues.append(f"invalid sdist: {exc}")
    return issues


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) < 2:
        print("usage: verify_python_artifacts VERSION ARTIFACT...", file=sys.stderr)
        return 2
    version, *artifacts = args
    issues: list[str] = []
    for raw in artifacts:
        path = Path(raw)
        current = verify_wheel(path, version) if path.suffix == ".whl" else verify_sdist(path, version)
        issues.extend(f"{path.name}: {issue}" for issue in current)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    print(f"Verified {len(artifacts)} Python artifact(s) for {version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
