import os
import subprocess
import sys
from pathlib import Path


def run_tool(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, script, *args],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_build_reference_runs_as_direct_script(tmp_path: Path):
    result = run_tool("tools/build_reference.py", "--output", str(tmp_path / "data"))
    assert result.returncode == 0, result.stderr


def test_build_search_index_runs_as_direct_script(tmp_path: Path):
    result = run_tool("tools/build_search_index.py", "--output", str(tmp_path / "index.json"))
    assert result.returncode == 0, result.stderr
