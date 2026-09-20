from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
EXPLICIT_ID_RE = re.compile(r"\s*\{#([^}]+)\}\s*$")
HTML_TAG_RE = re.compile(r"<[^>]+>")
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}

FORBIDDEN_PUBLIC_STRINGS = {
    "cpanel.tikadentplus.ir",
    "ubuntu@1.2.3.4",
}
HIGH_RISK_PATTERNS = [
    re.compile(r"rm\s+-rf\s+/\s*(?:$|[#;&|])", re.IGNORECASE | re.MULTILINE),
    re.compile(r"curl\b[^\n|]*\|\s*(?:sudo\s+)?(?:bash|sh)\b", re.IGNORECASE),
    re.compile(r"wget\b[^\n|]*\|\s*(?:sudo\s+)?(?:bash|sh)\b", re.IGNORECASE),
]


def compare_language_structure(fa_dir: Path, en_dir: Path) -> tuple[list[str], list[str]]:
    fa_files = {p.relative_to(fa_dir).as_posix() for p in fa_dir.rglob("*.md")}
    en_files = {p.relative_to(en_dir).as_posix() for p in en_dir.rglob("*.md")}
    return sorted(en_files - fa_files), sorted(fa_files - en_files)


def _clean_link_target(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        return raw[1 : raw.index(">")]
    if ' "' in raw or " '" in raw:
        return raw.split(maxsplit=1)[0]
    return raw


def _extract_local_targets(text: str) -> set[str]:
    targets = {_clean_link_target(m.group(1)) for m in MARKDOWN_LINK_RE.finditer(text)}
    targets.update(m.group(1).strip() for m in HTML_LINK_RE.finditer(text))
    return targets


def slugify_heading(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).strip().lower()
    text = EXPLICIT_ID_RE.sub("", text)
    text = HTML_TAG_RE.sub("", text)
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = "".join(ch for ch in text if ch.isalnum() or ch in {"_", "-", "\u200c"} or ch.isspace())
    return re.sub(r"[\s-]+", "-", text).strip("-")


def _heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(stripped)
        if not match:
            continue
        heading = match.group(1).strip()
        explicit = EXPLICIT_ID_RE.search(heading)
        if explicit:
            anchor = explicit.group(1)
        else:
            base = slugify_heading(heading)
            if not base:
                continue
            occurrence = counts.get(base, 0)
            anchor = base if occurrence == 0 else f"{base}_{occurrence}"
            counts[base] = occurrence + 1
        anchors.add(anchor)
    return anchors


def _resolve_local_path(source_file: Path, path_part: str) -> Path | None:
    if not path_part:
        return source_file
    decoded = unquote(path_part)
    base = source_file.parent
    exact = (base / decoded).resolve()
    if exact.exists():
        if exact.is_dir():
            index = exact / "index.md"
            return index if index.exists() else None
        return exact
    if decoded.endswith("/"):
        without_slash = decoded.rstrip("/")
        md = (base / f"{without_slash}.md").resolve()
        if md.exists():
            return md
        index = (base / without_slash / "index.md").resolve()
        if index.exists():
            return index
    elif not Path(decoded).suffix:
        md = (base / f"{decoded}.md").resolve()
        if md.exists():
            return md
        index = (base / decoded / "index.md").resolve()
        if index.exists():
            return index
    return None


def _candidate_exists(source_file: Path, target: str) -> bool:
    if not target or target.startswith("#") or target.startswith("//"):
        return True
    parsed = urlsplit(target)
    if parsed.scheme.lower() in EXTERNAL_SCHEMES or parsed.netloc:
        return True
    return _resolve_local_path(source_file, parsed.path) is not None


def find_broken_local_links(root: Path) -> list[str]:
    broken = []
    for source_file in sorted(root.rglob("*.md")):
        text = source_file.read_text(encoding="utf-8")
        for target in sorted(_extract_local_targets(text)):
            if not _candidate_exists(source_file, target):
                broken.append(f"{source_file.relative_to(root).as_posix()}: {target}")
    return broken


def find_broken_local_anchors(root: Path) -> list[str]:
    broken = []
    anchor_cache: dict[Path, set[str]] = {}
    for source_file in sorted(root.rglob("*.md")):
        text = source_file.read_text(encoding="utf-8")
        for target in sorted(_extract_local_targets(text)):
            parsed = urlsplit(target)
            if parsed.scheme.lower() in EXTERNAL_SCHEMES or parsed.netloc or not parsed.fragment:
                continue
            target_file = _resolve_local_path(source_file, parsed.path)
            if target_file is None or target_file.suffix.lower() != ".md":
                continue
            target_file = target_file.resolve()
            if target_file not in anchor_cache:
                anchor_cache[target_file] = _heading_anchors(target_file.read_text(encoding="utf-8"))
            fragment = unquote(parsed.fragment)
            if fragment not in anchor_cache[target_file]:
                broken.append(f"{source_file.relative_to(root).as_posix()}: {target}")
    return broken


def evaluate_translation_drift(delta_days: int) -> str:
    delta_days = abs(delta_days)
    if delta_days > 90:
        return "error"
    if delta_days > 30:
        return "warning"
    return "ok"


def _git_last_modified(repo_root: Path, relative_path: Path) -> int | None:
    try:
        output = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", "--", relative_path.as_posix()],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return int(output) if output.isdigit() else None


def find_translation_drift(repo_root: Path, fa_dir: Path, en_dir: Path) -> tuple[list[str], list[str]]:
    warnings, errors = [], []
    fa_set = {p.relative_to(fa_dir) for p in fa_dir.rglob("*.md")}
    en_set = {p.relative_to(en_dir) for p in en_dir.rglob("*.md")}
    for relative in sorted(fa_set & en_set):
        fa_rel = (fa_dir / relative).relative_to(repo_root)
        en_rel = (en_dir / relative).relative_to(repo_root)
        fa_ts = _git_last_modified(repo_root, fa_rel)
        en_ts = _git_last_modified(repo_root, en_rel)
        if fa_ts is None or en_ts is None:
            continue
        delta_days = abs(fa_ts - en_ts) // 86400
        state = evaluate_translation_drift(delta_days)
        newer = "Persian" if fa_ts > en_ts else "English" if en_ts > fa_ts else "neither"
        message = f"{relative.as_posix()}: {delta_days} day(s) drift; newer side: {newer}"
        if state == "warning":
            warnings.append(message)
        elif state == "error":
            errors.append(message)
    return warnings, errors


def find_public_safety_issues(root: Path) -> list[str]:
    findings = []
    candidates = list(root.glob("README*.md")) + list((root / "docs").rglob("*.md"))
    for extra in (root / "CHANGELOG.md", root / "DISCLAIMER.md"):
        if extra.exists():
            candidates.append(extra)
    for path in candidates:
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        for forbidden in sorted(FORBIDDEN_PUBLIC_STRINGS):
            if forbidden in lower:
                findings.append(f"{path.relative_to(root).as_posix()}: contains forbidden target marker '{forbidden}'")
        for pattern in HIGH_RISK_PATTERNS:
            if pattern.search(text):
                findings.append(f"{path.relative_to(root).as_posix()}: contains high-risk destructive/piped-shell pattern '{pattern.pattern}'")
    return findings


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    fa_dir = repo_root / "docs" / "fa"
    en_dir = repo_root / "docs" / "en"

    missing_fa, missing_en = compare_language_structure(fa_dir, en_dir)
    broken_links = find_broken_local_links(repo_root)
    broken_anchors = find_broken_local_anchors(repo_root)
    drift_warnings, drift_errors = find_translation_drift(repo_root, fa_dir, en_dir)
    safety = find_public_safety_issues(repo_root)

    errors = 0
    for label, items in [
        ("Files missing from Persian edition", missing_fa),
        ("Files missing from English edition", missing_en),
        ("Broken local links", broken_links),
        ("Broken local anchors", broken_anchors),
        ("Public safety issues", safety),
    ]:
        if items:
            errors += len(items)
            print(label + ":")
            for item in items:
                print(f"  - {item}")

    if drift_warnings:
        print("Translation drift warnings:")
        for item in drift_warnings:
            print(f"  - {item}")
    if drift_errors:
        errors += len(drift_errors)
        print("Translation drift errors (>90 days):")
        for item in drift_errors:
            print(f"  - {item}")

    if errors:
        print(f"Documentation integrity check failed with {errors} issue(s).")
        return 1

    print("Documentation integrity check passed: language structure, local links, anchors, translation freshness, and public safety policy are within policy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
