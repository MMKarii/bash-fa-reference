from __future__ import annotations

import argparse
import os
import tarfile
import tempfile
from pathlib import Path

from tools.build_completions import build_completions
from tools.build_manpages import build_manpages


def _tar_filter(info: tarfile.TarInfo) -> tarfile.TarInfo:
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = int(os.environ.get("SOURCE_DATE_EPOCH", "0"))
    return info


def _add_existing(tf: tarfile.TarFile, source: Path, arcname: str) -> None:
    if source.exists():
        tf.add(source, arcname=arcname, recursive=True, filter=_tar_filter)


def _ensure_generated_assets(source_root: Path, temp_root: Path) -> tuple[Path, Path]:
    man_root = source_root / "man"
    if not (man_root / "bashref.1").exists():
        man_root = temp_root / "man"
        build_manpages(source_root / "reference", man_root)

    completions_root = source_root / "packaging/completions"
    expected = [
        completions_root / "bash/bashref",
        completions_root / "zsh/_bashref",
        completions_root / "fish/bashref.fish",
    ]
    if not all(path.exists() for path in expected):
        completions_root = temp_root / "packaging/completions"
        build_completions(
            {
                "bash": completions_root / "bash/bashref",
                "zsh": completions_root / "zsh/_bashref",
                "fish": completions_root / "fish/bashref.fish",
            }
        )
    return man_root, completions_root


def build_release_assets(version: str, out_dir: Path, source_root: Path = Path(".")) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"bashref-{version}"

    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        man_root, completions_root = _ensure_generated_assets(source_root, temp_root)

        portable = out_dir / f"bashref-{version}-portable.tar.gz"
        with tarfile.open(portable, "w:gz") as tf:
            for relative in [
                "src",
                "reference",
                "README.md",
                "README.fa.md",
                "pyproject.toml",
                "LICENSE",
                "LICENSES",
            ]:
                _add_existing(tf, source_root / relative, f"{prefix}/{relative}")
            _add_existing(tf, man_root, f"{prefix}/man")
            _add_existing(tf, completions_root, f"{prefix}/packaging/completions")

        manpages = out_dir / f"bashref-{version}-manpages.tar.gz"
        with tarfile.open(manpages, "w:gz") as tf:
            _add_existing(tf, man_root, f"{prefix}/man")

        completions = out_dir / f"bashref-{version}-completions.tar.gz"
        with tarfile.open(completions, "w:gz") as tf:
            _add_existing(tf, completions_root, f"{prefix}/packaging/completions")

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
