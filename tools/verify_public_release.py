from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Callable

RPM_RE = re.compile(r"^bashref-(?P<version>\d+\.\d+\.\d+)-1(?:\.[A-Za-z0-9_.+-]+)?\.noarch\.rpm$")


def required_exact_assets(version: str) -> set[str]:
    return {
        f"bashref-{version}-py3-none-any.whl",
        f"bashref-{version}.tar.gz",
        f"bashref_{version}_all.deb",
        f"bashref-{version}-portable.tar.gz",
        f"bashref-{version}-manpages.tar.gz",
        f"bashref-{version}-completions.tar.gz",
        f"bashref-{version}-docs.tar.gz",
        "bashref.rb",
        "SHA256SUMS",
    }


def parse_checksum_names(text: str) -> set[str]:
    names: set[str] = set()
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            continue
        names.add(parts[1].strip())
    return names


def verify_release(
    release: dict,
    checksums_text: str,
    fetch_text: Callable[[str], str],
    base_url: str = "https://mmkarii.github.io/bash-fa-reference",
) -> list[str]:
    issues: list[str] = []
    tag = str(release.get("tag_name", ""))
    if not tag.startswith("v"):
        return ["release tag is missing or invalid"]
    version = tag[1:]

    assets = {
        str(asset.get("name", ""))
        for asset in release.get("assets", [])
        if isinstance(asset, dict)
    }
    missing = required_exact_assets(version) - assets
    for name in sorted(missing):
        issues.append(f"missing release asset: {name}")

    rpms = [name for name in assets if RPM_RE.fullmatch(name)]
    if not any(RPM_RE.fullmatch(name).group("version") == version for name in rpms):
        issues.append(f"missing RPM asset for version {version}")

    checksum_names = parse_checksum_names(checksums_text)
    for name in sorted(assets - {"SHA256SUMS"}):
        if name not in checksum_names:
            issues.append(f"SHA256SUMS does not list asset: {name}")

    marker = f"Bashref {version}"
    parts = version.split(".")
    snapshot = f"v{parts[0]}.{parts[1]}"
    endpoints = [
        f"{base_url}/",
        f"{base_url}/en/",
        f"{base_url}/fa/",
        f"{base_url}/{snapshot}/en/",
        f"{base_url}/{snapshot}/fa/",
    ]
    for url in endpoints:
        try:
            text = fetch_text(url)
        except Exception as exc:
            issues.append(f"cannot fetch Pages endpoint {url}: {exc}")
            continue
        if marker not in text:
            issues.append(f"Pages endpoint lacks release marker {marker}: {url}")
    return issues


def _fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "bashref-release-verifier/2.1"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-json", type=Path, required=True)
    parser.add_argument("--checksums", type=Path, required=True)
    parser.add_argument(
        "--base-url",
        default="https://mmkarii.github.io/bash-fa-reference",
    )
    args = parser.parse_args(argv)
    release = json.loads(args.release_json.read_text(encoding="utf-8"))
    checksums = args.checksums.read_text(encoding="utf-8")
    issues = verify_release(release, checksums, _fetch_text, args.base_url)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    print(f"Verified public release {release.get('tag_name')}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
