# HTML Artifacts

> **Status: Current public snapshot.**

A workflow and deterministic starter kit for choosing self-contained HTML when spatial layout, interaction, comparison, or browser inspection materially helps the reader.

## Package contents

- `SKILL.md` — selection rules, workflow, output boundaries, and verification.
- `assets/templates/` — offline starters for comparisons, reports, reviews, diagrams, decks, and temporary editors.
- `scripts/create_html_artifact.py` — standard-library template generator.
- `scripts/check_html_artifact.py` — lightweight structural and portability checks.
- `references/` — layout patterns, template guidance, and provenance notes.

## Try it

From this package directory:

```bash
python3 scripts/create_html_artifact.py --list-templates
python3 scripts/create_html_artifact.py \
  --template comparison \
  --out /tmp/ai-workbench-options.html \
  --title "Three options" \
  --summary "A synthetic comparison artifact."
python3 scripts/check_html_artifact.py /tmp/ai-workbench-options.html
```

The checker does not replace rendered browser inspection. Interactive controls, responsiveness, accessibility, and visual quality require appropriate browser verification.

## Provenance

This package was informed by [The Unreasonable Effectiveness of HTML](https://thariqs.github.io/html-effectiveness/), its [Apache-2.0 example repository](https://github.com/ThariqS/html-effectiveness), and the Apache-2.0 [dogum/html-artifacts](https://github.com/dogum/html-artifacts) skill. See `references/source.md` for the adaptation boundary.

## Compatibility

This is a dated public snapshot, not an automatic mirror of any private environment. It assumes Python 3 for the helpers and a browser for meaningful visual verification. No plugin or clean-environment compatibility guarantee is published.
