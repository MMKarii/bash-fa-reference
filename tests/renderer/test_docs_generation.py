from pathlib import Path

from tools.build_docs_reference import record_doc_path, render_markdown_record


def sample_record():
    return {
        "id": "builtin.printf",
        "kind": "builtin",
        "name": "printf",
        "language": "en",
        "summary": "Format and print data.",
        "synopsis": "printf [-v var] format [arguments]",
        "description": ["Print formatted output."],
        "examples": [],
        "related": [],
        "sources": ["https://www.gnu.org/software/bash/manual/bash.html#Bash-Builtins"],
    }


def test_record_doc_path_is_stable():
    assert record_doc_path(sample_record()) == Path("builtins/printf.md")


def test_generated_page_declares_record_id():
    text = render_markdown_record(sample_record())
    assert "record_id: builtin.printf" in text
    assert "reference_kind: builtin" in text


def test_literal_synopsis_is_fenced():
    text = render_markdown_record(sample_record())
    assert "```bash\nprintf [-v var] format [arguments]\n```" in text
