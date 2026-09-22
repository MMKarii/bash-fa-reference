from pathlib import Path


def test_split_license_files_exist_and_root_explains_scope():
    mit = Path("LICENSES/MIT.txt")
    cc = Path("LICENSES/CC-BY-4.0.txt")
    root = Path("LICENSE").read_text(encoding="utf-8")
    assert mit.is_file()
    assert cc.is_file()
    assert "Software source code" in root
    assert "Documentation and reference prose" in root
    assert "LICENSES/MIT.txt" in root
    assert "LICENSES/CC-BY-4.0.txt" in root
