from packaging.rpm.build_rpm import render_spec


def test_rpm_spec_contains_required_payload():
    text = render_spec("2.0.0", "bashref-2.0.0.tar.gz")
    assert "Version: 2.0.0" in text
    assert "BuildArch: noarch" in text
    assert "%{_bindir}/bashref" in text
    assert "%{_mandir}/man1/bashref.1*" in text
    assert "%{_datadir}/bash-completion/completions/bashref" in text
    assert "%post" not in text
