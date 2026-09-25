from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_checksums(paths: list[Path], output: Path) -> None:
    unique = {path.resolve(): path for path in paths if path.resolve() != output.resolve()}
    ordered = sorted(unique.values(), key=lambda path: path.name)
    lines = [f"{digest(path)}  {path.name}" for path in ordered]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=Path("dist/SHA256SUMS"))
    args = parser.parse_args(argv)
    write_checksums(args.paths, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
