import json

from bashref.renderer import render_error, render_record, render_records


def sample_record(language="en"):
    return {
        "id": "builtin.printf",
        "kind": "builtin",
        "name": "printf",
        "language": language,
        "summary": "داده را چاپ می‌کند." if language == "fa" else "Format and print data.",
        "synopsis": "printf FORMAT [ARGUMENTS]",
        "description": ["A description with enough words to wrap in a narrow terminal width."],
        "examples": [{"title": "Example", "code": "printf '%s\\n' \"$value\""}],
        "related": [],
        "sources": ["https://example.test/manual"],
    }


def test_json_preserves_persian_and_is_deterministic():
    first = render_record(sample_record("fa"), format="json", color=False, width=80)
    second = render_record(sample_record("fa"), format="json", color=False, width=80)
    assert first == second
    assert "داده را چاپ می‌کند" in first
    assert json.loads(first)["id"] == "builtin.printf"


def test_text_sanitizes_terminal_control_characters():
    record = sample_record()
    record["summary"] = "bad\x1b[2Jtext"
    output = render_record(record, format="text", color=False, width=80)
    assert "\x1b" not in output
    assert "bad[2Jtext" in output


def test_text_removes_del_and_c1_terminal_controls():
    record = sample_record()
    record["summary"] = "safe\x7f\x9b31mtext"
    output = render_record(record, format="text", color=False, width=80)
    assert "\x7f" not in output
    assert "\x9b" not in output
    assert "safe31mtext" in output


def test_text_wraps_description_to_width():
    output = render_record(sample_record(), format="text", color=False, width=32)
    assert all(len(line) <= 32 for line in output.splitlines() if line)


def test_error_json_has_stable_contract():
    output = render_error(3, "missing", ["printf"], format="json")
    assert json.loads(output) == {
        "code": 3,
        "error": True,
        "message": "missing",
        "suggestions": ["printf"],
    }


def test_render_records_json_is_array():
    output = render_records([sample_record()], format="json", color=False, width=80)
    assert isinstance(json.loads(output), list)
