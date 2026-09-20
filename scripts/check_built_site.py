from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


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

    def handle_starttag(self, tag, attrs):
        values = {n.lower(): v or "" for n, v in attrs}
        tag = tag.lower()
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

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)


def check_html_file(path: Path) -> list[str]:
    parser = _PageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
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


def check_site(site_root: Path) -> list[str]:
    issues = []
    for path in sorted(site_root.rglob("*.html")):
        issues.extend(f"{path.relative_to(site_root).as_posix()}: {issue}" for issue in check_html_file(path))
    return issues


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "site"
    if not root.exists():
        print("Built site directory does not exist: site/")
        return 1
    issues = check_site(root)
    if issues:
        print("Built-site accessibility/metadata issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("Built-site accessibility and metadata checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
