from __future__ import annotations

import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit, urlunsplit
from urllib.request import Request, urlopen

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\((https?://[^)\s]+)\)")
HTML_LINK_RE = re.compile(r"(?:href|src)=[\"'](https?://[^\"']+)[\"']", re.IGNORECASE)
PLAIN_URL_RE = re.compile(r"https?://[^\s<>'\"`]+")

WARNING_ONLY_HOSTS = {"github.com", "raw.githubusercontent.com", "img.shields.io"}


def classify_http_status(status: int) -> str:
    if 200 <= status < 400:
        return "ok"
    if status in {404, 410}:
        return "error"
    return "warning"


def is_warning_only_url(url: str) -> bool:
    host = urlsplit(url).hostname or ""
    return host in WARNING_ONLY_HOSTS


def _ascii_url(url: str) -> str:
    parsed = urlsplit(url)
    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            quote(parsed.path, safe="/%:@-._~!$&'()*+,;="),
            quote(parsed.query, safe="=&?/:;+,%@-._~!$'()*"),
            quote(parsed.fragment, safe="=&?/:;+,%@-._~!$'()*"),
        )
    )


def check_url(url: str, opener=urlopen, retries: int = 1, timeout: int = 8) -> tuple[str, str]:
    request = Request(
        _ascii_url(url),
        headers={
            "User-Agent": "bash-fa-reference-link-checker/1.0",
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Range": "bytes=0-1023",
        },
        method="GET",
    )
    last_message = "unknown failure"
    for attempt in range(retries + 1):
        try:
            with opener(request, timeout=timeout) as response:
                status = getattr(response, "status", 200)
            return classify_http_status(status), f"HTTP {status}"
        except HTTPError as exc:
            state = classify_http_status(exc.code)
            last_message = f"HTTP {exc.code} {exc.reason}"
            if state == "error" or exc.code in {401, 403}:
                return state, last_message
        except URLError as exc:
            last_message = str(exc.reason)
        except TimeoutError as exc:
            last_message = str(exc) or "timeout"
        if attempt < retries:
            time.sleep(0.25 * (attempt + 1))
    return "warning", last_message


def collect_external_links(repo_root: Path) -> set[str]:
    files: list[Path] = []
    for directory in (repo_root / "docs" / "fa", repo_root / "docs" / "en"):
        if directory.exists():
            files.extend(directory.rglob("*.md"))
    files.extend(repo_root.glob("*.md"))
    for extra in (
        repo_root / "site-root" / "index.html",
        repo_root / "mkdocs.fa.yml",
        repo_root / "mkdocs.en.yml",
        repo_root / "overrides" / "main.html",
        repo_root / ".github" / "repository-metadata.md",
    ):
        if extra.exists():
            files.append(extra)

    urls: set[str] = set()
    for path in files:
        text = path.read_text(encoding="utf-8")
        urls.update(m.group(1).rstrip(".,") for m in MARKDOWN_LINK_RE.finditer(text))
        urls.update(m.group(1).rstrip(".,") for m in HTML_LINK_RE.finditer(text))
        urls.update(m.group(0).rstrip(".,);]}>") for m in PLAIN_URL_RE.finditer(text))
    return urls


def _check_one(url: str) -> tuple[str, str, str]:
    state, message = check_url(url)
    return url, state, message


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    urls = sorted(collect_external_links(repo_root))
    errors, warnings = [], []

    print(f"Checking {len(urls)} unique external link(s) with bounded concurrency...")
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(urls)))) as pool:
        results = list(pool.map(_check_one, urls))

    for url, state, message in results:
        warning_only = is_warning_only_url(url)
        if state == "error" and not warning_only:
            errors.append(f"{url}: {message}")
        elif state in {"warning", "error"}:
            suffix = " (rate-limited host allowlist)" if warning_only else ""
            warnings.append(f"{url}: {message}{suffix}")

    if warnings:
        print("External link warnings:")
        for item in warnings:
            print(f"  - {item}")

    if errors:
        print("Deterministically broken external links:")
        for item in errors:
            print(f"  - {item}")
        return 1

    print("External link check completed without non-allowlisted deterministic 404/410 failures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
