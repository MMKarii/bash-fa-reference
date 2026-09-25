from tools.build_manpages import escape_roff, render_reference_manpage


def sample_record(language="en"):
    return {
        "id": "builtin.printf",
        "kind": "builtin",
        "name": "printf",
        "language": language,
        "summary": "Format and print data." if language == "en" else "داده را چاپ می‌کند.",
        "synopsis": "printf [-v var] format [arguments]",
        "description": ["Print formatted output." if language == "en" else "خروجی قالب‌بندی‌شده چاپ می‌کند."],
        "examples": [],
        "related": [],
        "sources": ["https://www.gnu.org/software/bash/manual/bash.html#Bash-Builtins"],
    }


def test_roff_control_lines_are_escaped():
    assert escape_roff(".danger") == r"\&.danger"
    assert escape_roff("'danger") == r"\&'danger"


def test_reference_manpage_has_required_sections():
    text = render_reference_manpage(sample_record())
    for section in ("NAME", "SYNOPSIS", "DESCRIPTION", "SEE ALSO"):
        assert f".SH {section}" in text


def test_persian_text_is_preserved():
    assert "داده را چاپ می‌کند" in render_reference_manpage(sample_record("fa"))

def test_cli_manpage_uses_parseable_th_date():
    from tools.build_manpages import render_cli_manpage
    first = render_cli_manpage().splitlines()[0]
    assert '"September 25, 2026"' in first
    assert '"Bashref 2.0.0"' in first
