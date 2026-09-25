from pathlib import Path
import tarfile

from tools.write_checksums import write_checksums
from tools.build_release_assets import build_release_assets


def test_checksum_lines_are_sorted(tmp_path: Path):
    a = tmp_path / "a.bin"; b = tmp_path / "b.bin"
    a.write_bytes(b"a"); b.write_bytes(b"b")
    out = tmp_path / "SHA256SUMS"
    write_checksums([b, a], out)
    names = [line.split("  ", 1)[1] for line in out.read_text().splitlines()]
    assert names == ["a.bin", "b.bin"]


def test_release_archives_have_expected_names(tmp_path: Path):
    paths = build_release_assets("2.0.0", tmp_path, source_root=Path("."))
    names = {p.name for p in paths}
    assert {
        "bashref-2.0.0-portable.tar.gz",
        "bashref-2.0.0-manpages.tar.gz",
        "bashref-2.0.0-completions.tar.gz",
    } <= names
    man = tmp_path / "bashref-2.0.0-manpages.tar.gz"
    with tarfile.open(man, "r:gz") as tf:
        members = tf.getnames()
    assert any(name.endswith("bashref.1") for name in members)
