from __future__ import annotations

import re
import sys

TAG_RE = re.compile(r"^v(\d+\.\d+\.\d+(?:[A-Za-z0-9.-]+)?)$")


def normalize_tag(tag: str) -> str:
    match = TAG_RE.fullmatch(tag)
    if not match:
        raise ValueError(f"invalid release tag: {tag}")
    return match.group(1)


def assert_release_version(tag: str, package_version: str) -> None:
    version = normalize_tag(tag)
    if version != package_version:
        raise ValueError(
            f"tag version {version} does not match package version {package_version}"
        )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print("usage: release_version.py TAG PACKAGE_VERSION", file=sys.stderr)
        return 2
    try:
        assert_release_version(args[0], args[1])
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"{args[0]} matches package version {args[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
