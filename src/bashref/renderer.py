from __future__ import annotations

import json
import textwrap


def _sanitize_text(value: str) -> str:
    return "".join(ch for ch in value if ch in "\n\t" or ord(ch) >= 32)


def _wrap(value: str, width: int) -> list[str]:
    value = _sanitize_text(value)
    if not value:
        return []
    result: list[str] = []
    for line in value.splitlines() or [value]:
        wrapped = textwrap.wrap(
            line,
            width=max(10, width),
            replace_whitespace=False,
            drop_whitespace=True,
            break_long_words=True,
            break_on_hyphens=False,
        )
        result.extend(wrapped or [""])
    return result


def _text_record(record: dict, width: int) -> str:
    lines: list[str] = []
    name = _sanitize_text(str(record.get("name", "")))
    kind = _sanitize_text(str(record.get("kind", "")))
    header = f"{name} ({kind})" if kind else name
    lines.extend(_wrap(header, width))
    lines.extend(_wrap(str(record.get("summary", "")), width))

    synopsis = str(record.get("synopsis", ""))
    if synopsis:
        lines.append("")
        lines.extend(_wrap("SYNOPSIS", width))
        lines.extend(_wrap(synopsis, width))

    description = record.get("description", [])
    if isinstance(description, list) and description:
        lines.append("")
        lines.extend(_wrap("DESCRIPTION", width))
        for paragraph in description:
            lines.extend(_wrap(str(paragraph), width))

    examples = record.get("examples", [])
    if isinstance(examples, list) and examples:
        lines.append("")
        lines.extend(_wrap("EXAMPLES", width))
        for example in examples:
            if isinstance(example, dict):
                title = str(example.get("title", ""))
                code = str(example.get("code", ""))
                if title:
                    lines.extend(_wrap(title, width))
                if code:
                    lines.extend(_wrap(code, width))
    return "\n".join(lines).rstrip() + "\n"


def render_record(record: dict, *, format: str, color: bool, width: int) -> str:
    if format == "json":
        return json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    if format != "text":
        raise ValueError(f"unsupported output format: {format}")
    return _text_record(record, width)


def render_records(records: list[dict], *, format: str, color: bool, width: int) -> str:
    if format == "json":
        return json.dumps(records, ensure_ascii=False, sort_keys=True) + "\n"
    if format != "text":
        raise ValueError(f"unsupported output format: {format}")
    return "\n".join(_text_record(record, width).rstrip() for record in records).rstrip() + ("\n" if records else "")


def render_error(code: int, message: str, suggestions: list[str], *, format: str) -> str:
    payload = {
        "error": True,
        "code": code,
        "message": _sanitize_text(message),
        "suggestions": [_sanitize_text(item) for item in suggestions],
    }
    if format == "json":
        return json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n"
    if format != "text":
        raise ValueError(f"unsupported output format: {format}")
    text = f"error: {payload['message']}"
    if payload["suggestions"]:
        text += "\nsuggestions: " + ", ".join(payload["suggestions"])
    return text + "\n"
