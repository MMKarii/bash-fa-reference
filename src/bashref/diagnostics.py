from __future__ import annotations

import json
import platform
import sys

from . import __version__
from .reference import ReferenceStore


def collect_diagnostics(store: ReferenceStore, language: str) -> dict[str, object]:
    en_records = store.list(None, "en")
    fa_records = store.list(None, "fa")
    paired = len(en_records) == len(fa_records)
    return {
        "status": "ok" if paired else "warning",
        "bashref_version": __version__,
        "runtime": "standalone" if getattr(sys, "frozen", False) else "python",
        "python_version": platform.python_version(),
        "platform": platform.system().lower() or "unknown",
        "machine": platform.machine() or "unknown",
        "language": language,
        "reference_records": len(en_records),
        "reference_languages": ["en", "fa"],
        "bilingual_parity": paired,
    }


def render_diagnostics(payload: dict[str, object], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n"
    if output_format != "text":
        raise ValueError(f"unsupported output format: {output_format}")
    lines = [
        f"Bashref: {payload['bashref_version']}",
        f"Status: {payload['status']}",
        f"Runtime: {payload['runtime']}",
        f"Python: {payload['python_version']}",
        f"Platform: {payload['platform']} ({payload['machine']})",
        f"Language: {payload['language']}",
        f"Reference records: {payload['reference_records']} per language",
        f"Bilingual parity: {'ok' if payload['bilingual_parity'] else 'mismatch'}",
    ]
    return "\n".join(lines) + "\n"
