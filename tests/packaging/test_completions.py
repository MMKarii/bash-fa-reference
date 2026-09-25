from pathlib import Path

from bashref.completion import completion_script
from tools.build_completions import OUTPUTS, build_completions


def test_generated_completion_assets_match_runtime(tmp_path: Path):
    outputs = {shell: tmp_path / path.name for shell, path in OUTPUTS.items()}
    build_completions(outputs)
    for shell, path in outputs.items():
        assert path.read_text(encoding="utf-8") == completion_script(shell)
