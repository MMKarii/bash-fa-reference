import json
from pathlib import Path

ROOT = Path("reference")


def ids(language: str) -> set[str]:
    result = set()
    for path in (ROOT / language).rglob("*.json"):
        result.add(json.loads(path.read_text(encoding="utf-8"))["id"])
    return result


REQUIRED_OPTIONS = {
    "option.allexport", "option.braceexpand", "option.emacs", "option.errexit",
    "option.errtrace", "option.functrace", "option.hashall", "option.histexpand",
    "option.history", "option.ignoreeof", "option.interactive-comments",
    "option.keyword", "option.monitor", "option.noclobber", "option.noexec",
    "option.noglob", "option.notify", "option.nounset", "option.onecmd",
    "option.physical", "option.pipefail", "option.posix", "option.privileged",
    "option.verbose", "option.vi", "option.xtrace",
}

REQUIRED_SHOPT = {
    "shopt.array_expand_once", "shopt.assoc_expand_once", "shopt.autocd",
    "shopt.bash_source_fullpath", "shopt.cdable_vars", "shopt.cdspell",
    "shopt.checkhash", "shopt.checkjobs", "shopt.checkwinsize", "shopt.cmdhist",
    "shopt.direxpand", "shopt.dirspell", "shopt.dotglob", "shopt.execfail",
    "shopt.expand_aliases", "shopt.extdebug", "shopt.extglob", "shopt.failglob",
    "shopt.force_fignore", "shopt.globasciiranges", "shopt.globskipdots",
    "shopt.globstar", "shopt.gnu_errfmt", "shopt.histappend", "shopt.histreedit",
    "shopt.histverify", "shopt.hostcomplete", "shopt.huponexit",
    "shopt.inherit_errexit", "shopt.interactive_comments", "shopt.lastpipe",
    "shopt.lithist", "shopt.localvar_inherit", "shopt.localvar_unset",
    "shopt.mailwarn", "shopt.no_empty_cmd_completion", "shopt.nocaseglob",
    "shopt.nocasematch", "shopt.noexpand_translation", "shopt.nullglob",
    "shopt.patsub_replacement", "shopt.progcomp", "shopt.progcomp_alias",
    "shopt.promptvars", "shopt.restricted_shell", "shopt.shift_verbose",
    "shopt.sourcepath", "shopt.varredir_close", "shopt.xpg_echo",
}

REQUIRED_VARIABLES = {
    "variable.BASH", "variable.BASHOPTS", "variable.BASHPID",
    "variable.BASH_ALIASES", "variable.BASH_ARGC", "variable.BASH_ARGV",
    "variable.BASH_ARGV0", "variable.BASH_CMDS", "variable.BASH_COMMAND",
    "variable.BASH_COMPAT", "variable.BASH_ENV", "variable.BASH_LINENO",
    "variable.BASH_REMATCH", "variable.BASH_SOURCE", "variable.BASH_SUBSHELL",
    "variable.BASH_VERSINFO", "variable.BASH_VERSION", "variable.DIRSTACK",
    "variable.EPOCHREALTIME", "variable.EPOCHSECONDS", "variable.FUNCNAME",
    "variable.HISTCMD", "variable.HOSTNAME", "variable.LINENO",
    "variable.MACHTYPE", "variable.OLDPWD", "variable.OPTARG",
    "variable.OPTIND", "variable.OSTYPE", "variable.PIPESTATUS",
    "variable.PPID", "variable.PROMPT_COMMAND", "variable.PWD",
    "variable.RANDOM", "variable.REPLY", "variable.SECONDS",
    "variable.SHELLOPTS", "variable.SHLVL", "variable.SRANDOM",
}

REQUIRED_SYNTAX = {
    "syntax.quoting", "syntax.if", "syntax.case", "syntax.for", "syntax.while",
    "syntax.until", "syntax.select", "syntax.function", "syntax.arithmetic-command",
    "syntax.conditional-command", "syntax.group-command", "syntax.subshell",
}


def test_reference_maturity_coverage_is_bilingual():
    en = ids("en")
    fa = ids("fa")
    assert REQUIRED_OPTIONS <= en
    assert REQUIRED_OPTIONS <= fa
    assert REQUIRED_SHOPT <= en
    assert REQUIRED_SHOPT <= fa
    assert REQUIRED_VARIABLES <= en
    assert REQUIRED_VARIABLES <= fa
    assert REQUIRED_SYNTAX <= en
    assert REQUIRED_SYNTAX <= fa
