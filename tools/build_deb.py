from __future__ import annotations

import argparse
import gzip
import shutil
import subprocess
import sys
from pathlib import Path


def _copy_or_placeholder(source: Path, destination: Path, content: bytes = b"") -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.exists():
        shutil.copy2(source, destination)
    else:
        destination.write_bytes(content)


def _gzip_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes() if source.exists() else b".TH BASHREF 1\n"
    with destination.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as handle:
            handle.write(data)


def stage_deb(root: Path, wheel: Path, version: str, dry_run: bool = False) -> Path:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)

    launcher = root / "usr/bin/bashref"
    launcher.parent.mkdir(parents=True, exist_ok=True)
    launcher.write_text(
        "#!/bin/sh\nexec python3 -m bashref \"$@\"\n",
        encoding="utf-8",
    )
    launcher.chmod(0o755)

    payload = root / f"opt/bashref/{version}"
    payload.mkdir(parents=True, exist_ok=True)
    if wheel.exists():
        shutil.copy2(wheel, payload / wheel.name)
    elif dry_run:
        (payload / f"bashref-{version}-py3-none-any.whl").write_bytes(b"")
    else:
        raise FileNotFoundError(wheel)

    _gzip_copy(Path("man/bashref.1"), root / "usr/share/man/man1/bashref.1.gz")
    _gzip_copy(Path("man/bashref-reference.5"), root / "usr/share/man/man5/bashref-reference.5.gz")

    _copy_or_placeholder(
        Path("packaging/completions/bash/bashref"),
        root / "usr/share/bash-completion/completions/bashref",
    )
    _copy_or_placeholder(
        Path("packaging/completions/zsh/_bashref"),
        root / "usr/share/zsh/vendor-completions/_bashref",
    )
    _copy_or_placeholder(
        Path("packaging/completions/fish/bashref.fish"),
        root / "usr/share/fish/vendor_completions.d/bashref.fish",
    )
    _copy_or_placeholder(Path("LICENSES/MIT.txt"), root / "usr/share/doc/bashref/LICENSE-MIT")
    _copy_or_placeholder(Path("LICENSES/CC-BY-4.0.txt"), root / "usr/share/doc/bashref/LICENSE-CC-BY-4.0")

    control = root / "DEBIAN/control"
    control.parent.mkdir(parents=True, exist_ok=True)
    control.write_text(
        "\n".join(
            [
                "Package: bashref",
                f"Version: {version}",
                "Section: utils",
                "Priority: optional",
                "Architecture: all",
                "Depends: python3 (>= 3.10)",
                "Maintainer: MMKarii",
                "Description: Offline bilingual Bash reference CLI",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return root


def build_deb(wheel: Path, version: str, out_dir: Path = Path("dist")) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stage = out_dir / f".deb-root-{version}"
    root = stage_deb(stage, wheel, version)
    target = out_dir / f"bashref_{version}_all.deb"
    try:
        subprocess.run(["dpkg-deb", "--build", str(root), str(target)], check=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    parser.add_argument("--version", default="2.0.0")
    parser.add_argument("--out-dir", type=Path, default=Path("dist"))
    args = parser.parse_args(argv)
    path = build_deb(args.wheel, args.version, args.out_dir)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
