from pathlib import Path

from tools.build_reference import build_reference


def test_build_is_deterministic(tmp_path: Path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    m1 = build_reference(Path("reference"), first, "2.0.0")
    m2 = build_reference(Path("reference"), second, "2.0.0")
    assert m1 == m2
    files1 = {p.relative_to(first): p.read_bytes() for p in first.rglob("*") if p.is_file()}
    files2 = {p.relative_to(second): p.read_bytes() for p in second.rglob("*") if p.is_file()}
    assert files1 == files2


def test_manifest_has_sorted_records_and_no_absolute_paths(tmp_path: Path):
    output = tmp_path / "out"
    manifest = build_reference(Path("reference"), output, "2.0.0")
    assert manifest["records"] == sorted(manifest["records"])
    text = (output / "manifest.json").read_text(encoding="utf-8")
    assert str(Path.cwd()) not in text
    assert manifest["product_version"] == "2.0.0"
    assert manifest["languages"] == ["en", "fa"]
