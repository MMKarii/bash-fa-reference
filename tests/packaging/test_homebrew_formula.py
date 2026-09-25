from tools.render_homebrew_formula import render_formula


def test_formula_contains_release_coordinates():
    digest = "a" * 64
    text = render_formula("2.0.0", "https://example.test/bashref-2.0.0.tar.gz", digest)
    assert 'version "2.0.0"' in text
    assert 'url "https://example.test/bashref-2.0.0.tar.gz"' in text
    assert f'sha256 "{digest}"' in text
    assert "virtualenv_install_with_resources" not in text
