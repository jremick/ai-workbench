---
name: html-print-pdf
description: "Use for HTML print/PDF support: print buttons, export to PDF, print CSS, preserved colors, all slides/sections, and browser PDF verification."
license: Apache-2.0
---

# HTML Print PDF

Version: 1.0.1
Last updated: 2026-05-28

Use this skill to make an existing HTML artifact export cleanly through the browser print dialog. The goal is a reliable user flow: open the page, click print or use the browser print command, choose Save as PDF, and get a complete, legible document without extra tooling.

## When To Use

Use this for HTML, single-page demos, static reports, dashboards, and browser-based slide decks.

Do not use this as the primary route for rich `.pptx`, `.docx`, or programmatically generated PDFs when the user needs editable source documents or precise print production. Use the relevant document skill for those formats.

## Working Method

1. Inspect the HTML structure before editing.
   - Identify the artifact type: slide deck, report/document, wide table/dashboard, or mixed app surface.
   - Find layout containers, hidden content, scroll containers, fixed navigation, buttons, counters, and theme classes.
   - Check whether the page already has `@media print`, `@page`, `window.print()`, or `.no-print`.
2. Choose the print page model.
   - Slide decks/presentations: `landscape`, margin `0`, one slide per page.
   - Reports/documents/plans: `A4 portrait`, margin around `1.5cm`.
   - Wide tables/dashboards: `landscape`, margin around `1cm`.
   - Preserve an existing page size if the artifact was clearly designed for another format.
3. Add print CSS after the existing screen styles so it wins in the cascade.
4. Adapt selectors to the actual page.
   - Do not paste generic `.nav`, `.toolbar`, `.slide`, or `.grid-3` rules without checking that those classes exist.
   - Prefer adding a reusable `.no-print` class to controls you introduce or can safely tag.
   - For app frameworks, avoid broad rules that hide all `button` elements if printed content legitimately includes button-like labels.
5. Make hidden content printable.
   - Slide decks often show one slide at a time; print mode should reveal every slide.
   - Scrollable report sections need `overflow: visible` in print.
   - Fixed or absolute containers usually need `position: static` or page-sized relative slide rules.
6. Preserve visual fidelity.
   - Set `print-color-adjust: exact` and `-webkit-print-color-adjust: exact` on `html, body`, and key themed containers.
   - Disable animations and transitions in print.
   - Keep dark-mode pages readable; if the PDF should be light, define explicit print colors instead of relying on theme toggles.
7. Add a print/PDF button only when useful.
   - If the page already has an export toolbar, add a button that calls `window.print()`.
   - If the artifact is a static handoff where browser shortcuts are acceptable, print CSS alone may be enough.
   - Style the button using the page's existing button system and mark it `.no-print`.
8. Verify the generated output.
   - Use a browser print preview or headless browser PDF generation when available.
   - Confirm every intended page/slide appears, interactive UI is hidden, colors render, content is not clipped, and page breaks are sensible.
   - Prefer a concrete PDF smoke test for slide decks and reports: generate a PDF, check page count, and inspect text or rendered pages.
   - If you cannot render the PDF in the environment, state the residual layout risk and provide exact local verification steps.

## Print Patterns

Load `references/print-patterns.md` when you need copyable CSS patterns for:

- base print reset
- page-size variants
- controls/toolbars hiding
- slide deck printing
- scrollable report printing
- grid preservation
- light/dark theme color handling
- print button markup
- command-line PDF smoke tests

Use those patterns as starting points, then adapt selectors to the actual HTML.

## Verification Checklist

Before calling the work done:

- The HTML contains one clear `@media print` block or an equivalent stylesheet.
- The `@page` rule matches the artifact type.
- Navigation, toolbars, counters, hints, and print buttons are hidden in print.
- Hidden slides/sections become visible in print.
- Scroll containers do not clip content.
- Page breaks occur at slide or section boundaries.
- Colors, backgrounds, and text remain legible in the generated PDF.
- No text overlaps, cropped edges, or blank pages appear in the rendered output.

## Common Failure Modes

- Only the currently visible slide prints because inactive slides stay `display: none`.
- A fixed full-screen app shell clips long content in print.
- Browser default margins change intended slide geometry.
- Dark theme backgrounds print without enough contrast or with missing background colors.
- Broad `button { display: none }` rules hide content that was styled as a button but should appear in the document.
- Grid layouts collapse to a single column because responsive mobile rules still apply in print.

## Example Requests

Use this skill for prompts like:

- "Add a Save as PDF button to this HTML deck."
- "The browser PDF only prints the first slide. Fix it."
- "Make this dashboard printable without the controls."
- "The printed PDF loses colors and cuts off the bottom of sections."
- "Turn this static HTML report into something I can print to PDF cleanly."
