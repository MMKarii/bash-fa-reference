import json
import shutil
import subprocess


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    exe = shutil.which("bashref")
    assert exe is not None, "bashref console script is not installed"
    return subprocess.run([exe, *args], check=False, text=True, capture_output=True)


def test_installed_version():
    result = run_cli("--version")
    assert result.returncode == 0
    assert result.stdout.strip() == "bashref 2.0.0"


def test_installed_search_and_lookup():
    search = run_cli("--lang", "en", "search", "printf")
    assert search.returncode == 0
    assert "printf" in search.stdout
    lookup = run_cli("--lang", "en", "--format", "json", "builtin", "printf")
    assert lookup.returncode == 0
    assert json.loads(lookup.stdout)["id"] == "builtin.printf"
