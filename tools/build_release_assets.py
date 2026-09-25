from __future__ import annotations

import argparse
import os
import tarfile
from pathlib import Path


def _tar_filter(info: tarfile.TarInfo) -> tarfile.TarInfo:
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = int(os.environ.get("SOURCE_DATE_EPOCH", "0"))
    return info


def _add_existing(tf: tarfile.TarFile, source_root: Path, relative: str, arc_prefix: str) -> None:
    path = source_root / relative
    if path.exists():
        tf.add(path, arcname=f"{arc_prefix}/{relative}", recursive=True, filter=_tar_filter)


def _build_archive(target: Path, source_root: Path, version: str, members: list[str]) -> Path:
    prefix = f"bashref-{version}"
    with tarfile.open(target, "w:gz") as tf:
        for relative in members:
            _add_existing(tf, source_root, relative, prefix)
    return target


def build_release_assets(version: str, out_dir: Path, source_root: Path = Path(".")) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    portable = _build_archive(
        out_dir / f"bashref-{version}-portable.tar.gz",
        source_root,
        version,
        [
            "src",
            "reference",
            "README.md",
            "README.fa.md",
            "pyproject.toml",
            "LICENSE",
            "LICENSES",
            "man",
            "packaging/completions",
        ],
    )
    manpages = _build_archive(
        out_dir / f"bashref-{version}-manpages.tar.gz",
        source_root,
        version,
        ["man"],
    )
    completions = _build_archive(
        out_dir / f"bashref-{version}-completions.tar.gz",
        source_root,
        version,
        ["packaging/completions"],
    )
    return [portable, manpages, completions]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="2.0.0")
    parser.add_argument("--out-dir", type=Path, default=Path("dist"))
    parser.add_argument("--source-root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    for path in build_release_assets(args.version, args.out_dir, args.source_root):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
