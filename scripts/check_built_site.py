from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}


class _PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = ""
        self.in_title = False
        self.title_parts = []
        self.description = ""
        self.viewport = ""
        self.canonical = ""
        self.og_title = ""
        self.local_images_without_alt = []
        self.local_targets: list[tuple[str, str]] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag, attrs):
        values = {n.lower(): v or "" for n, v in attrs}
        tag = tag.lower()

        element_id = values.get("id", "").strip()
        if element_id:
            self.anchors.add(element_id)
        if tag == "a":
            name = values.get("name", "").strip()
            if name:
                self.anchors.add(name)

        if tag == "html":
            self.html_lang = values.get("lang", "").strip()
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = values.get("name", "").lower()
            prop = values.get("property", "").lower()
            if name == "description":
                self.description = values.get("content", "").strip()
            elif name == "viewport":
                self.viewport = values.get("content", "").strip()
            elif prop == "og:title":
                self.og_title = values.get("content", "").strip()
        elif tag == "link" and values.get("rel", "").lower() == "canonical":
            self.canonical = values.get("href", "").strip()
        elif tag == "img":
            src = values.get("src", "").strip()
            parsed = urlsplit(src)
            is_local = bool(src) and not parsed.scheme and not parsed.netloc and not src.startswith("//")
            if is_local and not values.get("alt", "").strip():
                self.local_images_without_alt.append(src)

        for attr in ("href", "src"):
            target = values.get(attr, "").strip()
            if target:
                parsed = urlsplit(target)
                if (
                    not parsed.scheme
                    and not parsed.netloc
                    and not target.startswith("//")
                    and parsed.scheme.lower() not in EXTERNAL_SCHEMES
                ):
                    self.local_targets.append((attr, target))

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)


def parse_html(path: Path) -> _PageParser:
    parser = _PageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def check_html_file(path: Path) -> list[str]:
    parser = parse_html(path)
    issues = []
    if not parser.html_lang:
        issues.append("missing html lang attribute")
    if not "".join(parser.title_parts).strip():
        issues.append("missing page title")
    if not parser.description:
        issues.append("missing meta description")
    if not parser.viewport:
        issues.append("missing viewport metadata")
    if not parser.canonical:
        issues.append("missing canonical URL")
    if not parser.og_title:
        issues.append("missing Open Graph title")
    issues.extend(f"project-controlled img alt missing: {src}" for src in parser.local_images_without_alt)
    return issues


def _resolve_local_target(site_root: Path, source_file: Path, raw_target: str) -> tuple[Path | None, str]:
    parsed = urlsplit(raw_target)
    fragment = unquote(parsed.fragment)
    path_part = unquote(parsed.path)

    if not path_part:
        return source_file, fragment

    if path_part.startswith("/"):
        candidate = site_root / path_part.lstrip("/")
    else:
        candidate = source_file.parent / path_part

    candidate = candidate.resolve()
    site_root_resolved = site_root.resolve()
    try:
        candidate.relative_to(site_root_resolved)
    except ValueError:
        return None, fragment

    if candidate.is_dir():
        candidate = candidate / "index.html"
    elif path_part.endswith("/"):
        candidate = candidate / "index.html"
    elif not candidate.suffix:
        html_candidate = candidate.with_suffix(".html")
        index_candidate = candidate / "index.html"
        if html_candidate.exists():
            candidate = html_candidate
        elif index_candidate.exists():
            candidate = index_candidate

    return candidate, fragment


def check_built_links(site_root: Path) -> list[str]:
    issues: list[str] = []
    parser_cache: dict[Path, _PageParser] = {}

    for source_file in sorted(site_root.rglob("*.html")):
        parser = parser_cache.setdefault(source_file, parse_html(source_file))
        for attr, target in parser.local_targets:
            if target.startswith("#"):
                target_file = source_file
                fragment = unquote(urlsplit(target).fragment)
            else:
                target_file, fragment = _resolve_local_target(site_root, source_file, target)

            rel_source = source_file.relative_to(site_root).as_posix()
            if target_file is None or not target_file.exists():
                issues.append(f"{rel_source}: broken local {attr} target: {target}")
                continue

            if fragment and target_file.suffix.lower() == ".html":
                target_parser = parser_cache.setdefault(target_file, parse_html(target_file))
                if fragment not in target_parser.anchors:
                    issues.append(f"{rel_source}: missing local anchor: {target}")

    return issues


def check_site(site_root: Path) -> list[str]:
    issues = []
    for path in sorted(site_root.rglob("*.html")):
        issues.extend(f"{path.relative_to(site_root).as_posix()}: {issue}" for issue in check_html_file(path))
    issues.extend(check_built_links(site_root))
    return issues


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "site"
    if not root.exists():
        print("Built site directory does not exist: site/")
        return 1

    issues = check_site(root)
    if issues:
        print("Built-site accessibility, metadata, or local-link issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("Built-site accessibility, metadata, local-link, and anchor checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
