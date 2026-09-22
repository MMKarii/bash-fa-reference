from __future__ import annotations

SITE_ROOT = "https://mmkarii.github.io/bash-fa-reference"


def _published_url(language: str, page_url: str) -> str:
    relative = (page_url or "").lstrip("/")
    if relative in {".", "./"}:
        relative = ""
    return f"{SITE_ROOT}/{language}/{relative}"


def on_page_context(context, *, page, config, nav):
    """Point Material's language switcher and hreflang links at the matching page."""
    page_url = getattr(page, "url", "") or ""
    config.extra["alternate"] = [
        {"name": "فارسی", "link": _published_url("fa", page_url), "lang": "fa"},
        {"name": "English", "link": _published_url("en", page_url), "lang": "en"},
    ]
    return context
