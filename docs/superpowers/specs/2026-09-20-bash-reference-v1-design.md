# Bash Reference v1 Design

## Goal

Convert the supplied Bash Word-document set and banner into a maintainable, professional, bilingual Persian/English reference aligned with the established Nmap/Hydra repository pattern.

## Content policy

The supplied files are the editorial source set. Repeated filler and duplicated drafts are excluded. Bash-specific technical claims are verified against the GNU Bash Reference Manual. Security material is framed for owned systems, controlled labs, and defensive administration.

## Information architecture

- 14 mirrored chapters in `docs/fa` and `docs/en`
- start pages: index, learning path, cheat sheet, glossary
- references and disclaimer
- RTL Persian and LTR English MkDocs builds
- root language selector
- `latest` and `v1.0` publishing aliases

## Quality gates

- matching bilingual file structure
- internal links and anchors
- translation drift
- external link deterministic 404/410 failures
- strict MkDocs builds
- accessibility and metadata checks on built HTML
- complete published-output verification
