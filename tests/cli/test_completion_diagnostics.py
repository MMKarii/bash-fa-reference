from bashref.completion import completion_script


def test_completions_include_diagnostic_commands():
    for shell in ("bash", "zsh", "fish"):
        text = completion_script(shell)
        assert "stats" in text
        assert "doctor" in text
