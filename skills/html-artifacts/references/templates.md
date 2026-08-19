# HTML Artifact Templates

Read this before generating or extending a bundled HTML template.

## Generator

Use the standard-library generator to avoid rewriting page chrome:

```bash
python3 ~/.codex/skills/html-artifacts/scripts/create_html_artifact.py \
  --template comparison \
  --out artifacts/options.html \
  --title "Three implementation options" \
  --summary "Side-by-side comparison with recommendation."
```

Inspect available templates:

```bash
python3 ~/.codex/skills/html-artifacts/scripts/create_html_artifact.py --list-templates
```

Populate escaped values with `--set key=value`, raw HTML/JS values with `--raw key=value`, or a JSON object with `--data input.json`.

Common raw slots:

- `cards_html`
- `content_html`
- `sections_html`
- `timeline_html`
- `diagram_html`
- `slides_html`
- `editor_body_html`
- `data_js`
- `export_js`

## Template Selection

- `comparison`: Start here for option comparisons, design directions, implementation alternatives, tradeoffs, and recommendations. Based on the side-by-side comparison and implementation-plan examples.
- `report`: Start here for weekly status, incident reports, post-mortems, research summaries, and timeline-heavy updates.
- `review`: Start here for PR writeups, annotated review summaries, module understanding, and findings packages.
- `diagram`: Start here for architecture diagrams, flowcharts, process maps, and system sketches.
- `deck`: Start here for slide-like presentations that need keyboard navigation.
- `editor`: Start here for one-off tools where the user manipulates state and copies/export the result.

## Quality Rules

- Treat templates as scaffolds, not final artifacts. Replace placeholder content.
- Prefer project design tokens if available. Otherwise use `shared.css`.
- Keep one file, no build step, and no required network calls.
- Run `scripts/check_html_artifact.py <file>` before closeout when practical.
- For editors, verify the export action before closeout.
- For decks, verify keyboard navigation before closeout.
- For diagrams, prefer editable inline SVG over raster screenshots.

## Extending Templates

Do not add a new reusable template after a single occurrence. When a shape recurs at least three times:

1. Tell the user which repeated shape you noticed and what boilerplate the template would remove.
2. Ask for confirmation before changing this reusable skill.
3. Add or update the smallest template/generator behavior that helps.
4. Generate a sample artifact and inspect it.
5. Validate the skill and mirror through `codex-config-sync`.
