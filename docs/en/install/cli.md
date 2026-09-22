# Bashref CLI installation

Bashref v2 provides an offline command-line interface for the bilingual Bash reference.

## Development installation

Until the v2 package release is published, install from a checked-out repository:

```bash
python -m pip install -e .
bashref --version
```

Core examples:

```bash
bashref search printf
bashref builtin printf
bashref --lang fa builtin printf
bashref --format json builtin printf
bashref completion bash
```

Core lookup and search do not require network access and never execute examples stored in the reference data.
