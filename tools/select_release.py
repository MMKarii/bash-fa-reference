from __future__ import annotations

import argparse
import json
from pathlib import Path


def select_release_by_tag(releases: list[dict], tag: str) -> dict:
    matches = [
        release
        for release in releases
        if isinstance(release, dict) and release.get("tag_name") == tag
    ]
    if not matches:
        raise LookupError(f"release not found for tag: {tag}")
    if len(matches) > 1:
        raise LookupError(f"multiple releases found for tag: {tag}")
    return matches[0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("releases_json", type=Path)
    parser.add_argument("tag")
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args(argv)

    releases = json.loads(args.releases_json.read_text(encoding="utf-8"))
    if not isinstance(releases, list):
        raise SystemExit("release list response must be a JSON array")
    try:
        release = select_release_by_tag(releases, args.tag)
    except LookupError as exc:
        raise SystemExit(str(exc)) from exc
    args.output_json.write_text(
        json.dumps(release, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
