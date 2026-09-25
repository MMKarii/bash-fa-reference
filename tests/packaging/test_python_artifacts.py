from pathlib import Path
import tarfile
import zipfile

from tools.verify_python_artifacts import verify_sdist, verify_wheel


def test_verifiers_reject_missing_payload(tmp_path: Path):
    wheel = tmp_path / "bashref-2.0.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as z:
        z.writestr("bashref/__init__.py", "")
    assert verify_wheel(wheel, "2.0.0")

    sdist = tmp_path / "bashref-2.0.0.tar.gz"
    with tarfile.open(sdist, "w:gz") as t:
        marker = tmp_path / "marker"
        marker.write_text("x", encoding="utf-8")
        t.add(marker, arcname="bashref-2.0.0/marker")
    assert verify_sdist(sdist, "2.0.0")
