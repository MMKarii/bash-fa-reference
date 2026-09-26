from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from collections import Counter

from . import __version__
from .config import load_config
from .languages import resolve_language
from .reference import ReferenceStore


def reference_stats(store: ReferenceStore) -> dict:
    records = store.list(None, "en")
    counts = Counter(str(record.get("kind", "unknown")) for record in records)
    return {
        "product_version": __version__,
        "languages": ["en", "fa"],
        "record_count": len(records),
        "kinds": dict(sorted(counts.items())),
    }


def _bash_info() -> dict | None:
    path = shutil.which("bash")
    if path is None:
        return None
    try:
        result = subprocess.run(
            [path, "--version"],
            check=False,
            text=True,
            capture_output=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return {"path": path, "version": None}
    first = result.stdout.splitlines()[0].strip() if result.stdout else None
    return {"path": path, "version": first}


def doctor_report(store: ReferenceStore) -> dict:
    configured = load_config().get("language")
    language = resolve_language(None, configured, os.environ)
    stats = reference_stats(store)
    return {
        "bashref_version": __version__,
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "default_language": language,
        "reference_records": stats["record_count"],
        "reference_kinds": stats["kinds"],
        "bash": _bash_info(),
        "network_required": False,
    }
