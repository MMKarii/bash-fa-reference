import json
from pathlib import Path

REQUIRED_IDS = {
    "syntax.quoting",
    "expansion.parameter",
    "expansion.command-substitution",
    "expansion.arithmetic",
    "expansion.process-substitution",
    "expansion.brace",
    "expansion.pathname",
    "concept.arrays",
    "concept.associative-arrays",
    "concept.conditionals",
    "concept.loops",
    "concept.functions",
    "concept.pipelines",
    "concept.redirections",
    "concept.here-documents",
    "concept.here-strings",
    "concept.subshells",
    "concept.grouping",
    "concept.exit-status",
    "concept.traps",
    "concept.signals",
    "concept.job-control",
    "concept.shell-options",
    "concept.shopt",
    "concept.startup-files",
    "concept.environment",
    "concept.debugging",
    "concept.portability",
    "concept.defensive-scripting",
    "option.errexit",
    "option.nounset",
    "option.pipefail",
    "option.xtrace",
    "shopt.globstar",
    "shopt.nullglob",
    "variable.BASH_SOURCE",
    "variable.PIPESTATUS",
    "example.pipeline",
    "example.trap",
}


def ids(lang: str) -> set[str]:
    root = Path("reference") / lang
    result = set()
    for path in root.rglob("*.json"):
        if "builtins" in path.parts:
            continue
        result.add(json.loads(path.read_text(encoding="utf-8"))["id"])
    return result


def test_required_topics_exist_in_both_languages():
    assert REQUIRED_IDS - ids("en") == set()
    assert REQUIRED_IDS - ids("fa") == set()
