from pathlib import Path

from packaging.deb.build_deb import stage_deb

EXPECTED = {
    "usr/bin/bashref",
    "usr/share/man/man1/bashref.1.gz",
    "usr/share/man/man5/bashref-reference.5.gz",
    "usr/share/bash-completion/completions/bashref",
    "usr/share/zsh/vendor-completions/_bashref",
    "usr/share/fish/vendor_completions.d/bashref.fish",
    "usr/share/doc/bashref/LICENSE-MIT",
    "usr/share/doc/bashref/LICENSE-CC-BY-4.0",
}


def test_deb_stage_contains_required_system_paths(tmp_path: Path):
    root = stage_deb(tmp_path / "root", Path("dist/fake.whl"), "2.0.0", dry_run=True)
    paths = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    assert EXPECTED <= paths
    assert not any(".config/bashref" in p for p in paths)
