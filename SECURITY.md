# Security Policy

## Supported versions

| Release line | Security/correctness support |
| --- | --- |
| 2.1.x | Current supported line after publication |
| 2.0.x | Critical correctness/security fixes while 2.1 is current |
| 1.0.x | Historical documentation snapshot |

## Reporting a security issue

If Bashref packaging, the CLI, generated artifacts, or a documentation example could expose credentials, cause destructive behavior, or create a security regression, use GitHub private security reporting when available. Do not publish sensitive exploit details or real credentials in a public issue.

For an ordinary technical correction without security impact, use the issue templates.

A useful private report includes the affected Bashref version, installation method, operating system, minimal reproduction, expected/observed behavior, and `bashref --format json doctor` output with sensitive details removed.

## Project security properties

- Bashref treats reference records and examples as data and never executes them during lookup/search.
- Core lookup/search is offline and does not send telemetry.
- No credentials are collected or stored.
- Documentation examples use `example.test`, localhost, or documentation address ranges instead of private production targets.
- Privileged/destructive examples must be minimal, explicit, and defensive.
- Release artifacts are accompanied by `SHA256SUMS` and are built/tested in GitHub Actions.
