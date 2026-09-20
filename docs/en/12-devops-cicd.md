# 12. Bash in DevOps and CI/CD

The source material places Bash in build, test, deployment, Git, Docker, SSH, and file-transfer workflows. CI scripts should be **repeatable, observable, and explicit about failure**.

## A small CI wrapper

```bash
#!/usr/bin/env bash
set -u
set -o pipefail

run_tests() {
  printf '%s\n' "running tests"
  ./scripts/test.sh
}

main() {
  run_tests
}

main "$@"
```

## Git checks

```bash
git status --short
git diff --check
```

Automation should not blindly commit and push every workspace change.

## Containers

Use Bash as a thin orchestration layer. Move complex parsing and business logic to tools or languages designed for it.

## Secrets

- Do not store secrets in the repository.
- Do not echo CI secrets.
- Treat CI input as data.
- Retrieve credentials from the platform's secret store.
- Quote external values and validate constrained inputs.

## Idempotency

CI/CD jobs are easier to recover when rerunning them does not create inconsistent state.
