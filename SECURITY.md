# Security Policy

## Reporting a documentation security issue

If an example could expose credentials, encourage unsafe privilege handling, cause destructive behavior, or create a security regression, open a private security report through GitHub's security reporting features when available. For ordinary technical corrections, use the issue templates.

## Documentation rules

- Never commit passwords, tokens, private keys, cookies, or real production credentials.
- Use `example.test`, localhost, or documentation IP ranges in examples.
- Prefer defensive and administrative examples over offensive automation.
- Keep privileged operations minimal and explicit.
- Test scripts before production use.
