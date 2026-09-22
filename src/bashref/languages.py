from __future__ import annotations

from collections.abc import Mapping

SUPPORTED_LANGUAGES = {"en", "fa"}


def _valid(value: str | None) -> str | None:
    return value if value in SUPPORTED_LANGUAGES else None


def resolve_language(
    explicit: str | None,
    configured: str | None,
    environ: Mapping[str, str],
) -> str:
    explicit_valid = _valid(explicit)
    if explicit_valid:
        return explicit_valid
    configured_valid = _valid(configured)
    if configured_valid:
        return configured_valid
    locale = (
        environ.get("LC_ALL")
        or environ.get("LC_MESSAGES")
        or environ.get("LANG")
        or ""
    ).casefold()
    if locale.startswith("fa"):
        return "fa"
    return "en"
