# FAQ

## Does Bashref execute the examples it shows?

No. Reference records are data. Normal lookup/search never evaluates or executes stored shell examples.

## Does Bashref need internet access?

No for normal lookup, search, listing, diagnostics, language selection, or JSON output. `bashref docs --open` is the explicit feature that opens the published website.

## Do I need Bash installed?

Not to use the reference browser. Bash is only needed when you choose to run Bash commands/examples yourself.

## Which language is used by default?

An explicit `--lang` wins first, then the saved Bashref preference, then a Persian locale, with English as the fallback.

## What is the difference between the Reference Guide and Professional Guide?

The Reference Guide is a precise lookup manual generated from structured records. The Professional Guide is the longer tutorial and operations handbook.

## Which download should I use?

Use a standalone archive when you want one executable with no separate Python requirement. Use pipx/wheel when Python packaging fits your environment. Use DEB/RPM when you want Linux system integration including man pages and completions.

## How do I report a bug?

Run `bashref --format json doctor`, remove sensitive information, and include the output plus the exact command, installation method, OS, expected result, and actual result in a GitHub issue.
