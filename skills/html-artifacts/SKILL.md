---
name: html-artifacts
description: "Default to this skill for non-trivial human-facing output that the user is meant to read, review, share, inspect, present, compare, or manipulate: plans, specs, comparisons, design explorations, annotated reviews, PR writeups, module maps, architecture diagrams, timelines, dashboards, reports, incident reviews, explainers, slide-like decks, browser-inspectable mockups, animation or interaction prototypes, and temporary editors/tools that export back to text. Stay in markdown for simple text review, short conversational replies, code-only answers, terminal commands, canonical source files that need clean diffs, and brief notes that markdown handles well."
license: Apache-2.0
---

# HTML Artifacts

Version: 0.2.0
Last updated: 2026-06-19

## Purpose

Create self-contained HTML working artifacts for human-facing deliverables by default. Markdown remains right for simple text review and canonical/diff-heavy source records, but substantial plans, reviews, reports, explainers, comparisons, visual artifacts, and temporary tools should usually become HTML files.

Source context:

- Thariq Shihipar's examples: https://thariqs.github.io/html-effectiveness/
- Source skill reviewed: https://github.com/dogum/html-artifacts
- Example corpus repo: https://github.com/ThariqS/html-effectiveness

## Decision Rule

Use HTML by default when the user or task needs any of these:

- Side-by-side comparison, option exploration, or tradeoff review.
- Spatial information such as diffs, call graphs, timelines, architecture maps, flows, dashboards, or before/after states.
- Visual inspection of a design, prototype, component state sheet, motion, interaction, or browser-rendered artifact.
- A human-readable report, post-mortem, spec, review package, status update, explainer, or implementation plan that is more than simple text review.
- A temporary editor or control surface where the user changes state, then exports markdown, JSON, prompt text, config, or another pasteable representation.

Stay in markdown when the output is a short answer, simple text review, canonical record, repeated source input, code/config block, command sequence, or file expected to be hand-edited and reviewed in diffs. If both are useful, keep markdown or structured data as the source of truth and generate HTML as the review/view artifact.

## Workflow

1. Decide whether HTML earns its cost.
   - Default to yes for substantial human-facing output.
   - For routine template-backed artifacts, use the template list in this file and skip extra references.
   - Read `references/patterns.md` when category-specific layout guidance would improve the result.
   - Read `references/templates.md` when using advanced generator slots or extending templates.
   - If no, answer normally in markdown.
2. Start from a bundled template unless the artifact is too custom.
   - Run `scripts/create_html_artifact.py --list-templates`.
   - Generate a starter with `scripts/create_html_artifact.py --template <name> --out <file> --title "..." --summary "..."`.
   - Edit the generated file with task-specific content rather than hand-writing page chrome from scratch.
3. Choose the artifact home.
   - Use the current repo's established `artifacts/`, `docs/`, `work/`, or task folder conventions.
   - For one-off local review in this repo, prefer a task-local folder or `artifacts/`.
   - Do not commit generated HTML unless it is intentionally part of the deliverable.
4. Produce one portable `.html` file.
   - Inline CSS and JavaScript.
   - Avoid required network calls and build steps.
   - Include viewport metadata and responsive layout.
   - Use real structure: columns for comparisons, timelines for events, diagrams for flows, controls for editors.
5. Preserve round-trip paths.
   - Temporary editors must include an export or copy action that returns the user's edited state to markdown, JSON, prompt text, or another useful text format.
   - When the source of truth is markdown, JSON, repo code, or a live system, state that boundary in the artifact or closeout.
6. Verify what matters.
   - Run `scripts/check_html_artifact.py <file>` for generated files when practical.
   - Open or inspect the file in a browser when visual layout or interaction is material.
   - For complex or interactive artifacts, use Playwright/browser screenshot checks when available.
   - If verification is skipped, say so.

## Deterministic Template Path

Use the bundled generator when it can save time, reduce repeated boilerplate, or keep page quality consistent:

```bash
python3 ~/.codex/skills/html-artifacts/scripts/create_html_artifact.py \
  --template comparison \
  --out artifacts/options.html \
  --title "Three implementation options" \
  --summary "A side-by-side comparison with recommendation and risks."
```

Available starter templates:

- `comparison`: option comparisons, design directions, implementation tradeoffs.
- `report`: status reports, incident timelines, post-mortems, research summaries.
- `review`: annotated review packages, PR writeups, findings summaries.
- `diagram`: architecture maps, flowcharts, process maps.
- `deck`: keyboard-navigable slide-like presentations.
- `editor`: temporary editors or tools with copy/export output.

Use `--data input.json`, `--set key=value`, and `--raw key=value` for repeatable population. Keep generated HTML as a starting point; task-specific substance still needs judgment.

Run the lightweight checker before closeout:

```bash
python3 ~/.codex/skills/html-artifacts/scripts/check_html_artifact.py artifacts/options.html
```

## Template Improvement Loop

When the same HTML artifact shape recurs at least three times, propose adding or refining a bundled template or generator behavior. Ask the user for confirmation before changing the reusable skill. After approval, add the smallest template/script change that removes repeated boilerplate, validate it with a generated sample, then mirror through `codex-config-sync`.

## Output Rules

- In final chat, link the absolute local path to the generated HTML file and summarize what it contains.
- Do not paste the full HTML into chat unless the user explicitly requests inline source.
- For browser-visible artifacts, follow existing frontend/design instructions and project design systems before inventing a style.
- Avoid generic "AI dashboard" styling. Use restrained typography, clear hierarchy, accessible contrast, stable responsive dimensions, and only enough color to carry meaning.
- Use HTML as a working/view layer, not as a replacement for durable markdown, structured data, source code, decisions, or live-system records unless the user explicitly asks for that.

## Reference Routing

- `references/patterns.md`: read when category-specific layout guidance would improve the artifact.
- `references/templates.md`: read when using advanced generator slots or extending bundled templates.
- `references/source.md`: read only when provenance, upstream links, licensing, or source-skill comparison matters.
