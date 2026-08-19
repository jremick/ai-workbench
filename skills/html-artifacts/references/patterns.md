# HTML Artifact Patterns

Use this reference after `html-artifacts` has triggered and before drafting a file. Start from a bundled template when one fits, then customize the content and layout.

## Universal Checks

- Single file: one `.html`, inline CSS and JS, no build step.
- Portable by default: no required runtime network calls; use inline SVG or plain CSS for visuals unless the task needs a real asset.
- Responsive: include `<meta name="viewport" content="width=device-width, initial-scale=1">` and test narrow layouts for text overflow.
- Scannable: title, short framing/TLDR, visible sections, navigation for long artifacts, and clear status/severity labels when relevant.
- Source aware: say what data, files, or live systems the artifact reflects, and when it was generated if freshness matters.
- Accessible: semantic headings, readable font sizes, sufficient contrast, keyboard-friendly controls for interactive pieces.
- Round-trip capable for editors: include copy/export actions and visible export text so the user can paste the result back into Codex, a repo, or another tool.

## Category Patterns

### Exploration and Planning

Use for: implementation options, design directions, roadmap slices, migration plans, research synthesis.

Shape:

- Option cards or columns with the same fields across options.
- A decision row with recommendation, tradeoffs, and proof needed.
- Timeline or milestone lane when sequence matters.
- Risk table with owner/mitigation only when the plan needs it.

Avoid: a long linear plan that could have been markdown.

### Code Review and Understanding

Use for: annotated PRs, diffs, file tours, module maps, unfamiliar code walkthroughs.

Shape:

- File/module navigation.
- Annotated diff or call graph when structure matters.
- Severity and confidence labels.
- "Where to focus review" section for PR writeups.

Avoid: replacing a concise code-review final response when the user asked for direct findings in chat.

### Design and Prototyping

Use for: visual directions, component variants, design-system token sheets, mockups, motion tuning, clickable flows.

Shape:

- Token swatches and component state sheets.
- Side-by-side design variants.
- Real controls for animation duration/easing or state transitions.
- Responsive layouts that show the actual first screen or component surface.

Avoid: decorative cards, generic gradients, fake product states, or style that conflicts with the repo's design system.

### Diagrams and Maps

Use for: architecture maps, workflow diagrams, data flow, deploy pipelines, process maps.

Shape:

- Inline SVG, CSS grid diagrams, or Mermaid-rendered output only if it works offline or the dependency is acceptable.
- Clickable or expandable nodes when details would clutter the visual.
- Clear legend for status, ownership, or risk.

Avoid: diagram screenshots that cannot be inspected or edited when inline SVG would do.

### Reports and Explainers

Use for: weekly status, incident timeline, post-mortems, concept explainers, feature deep-dives, learning material.

Shape:

- Summary band with current status and key numbers.
- Timeline for incidents or delivery status.
- Collapsible sections/tabs for reference detail.
- Glossary or side notes when terminology is load-bearing.

Avoid: over-designed reports where a short markdown summary is enough.

### Decks

Use for: short presentations, meeting walkthroughs, decision narratives.

Shape:

- One file with sections/slides.
- Keyboard navigation when practical.
- Presenter-friendly typography and a visible slide count.

Avoid: trying to replace a polished PPTX deliverable when the user needs Office-native editing.

### Temporary Editors

Use for: ticket triage, feature-flag toggling, prompt tuning, prioritization boards, simple data cleanup.

Shape:

- Direct manipulation UI: drag, toggle, edit, reorder, filter, or annotate.
- Persistent in-memory state for the current browser session.
- Copy/export button with markdown, JSON, prompt text, or patch-ready output.
- Reset/import controls when useful.

Avoid: editors without export. The export path is the point.

## Adding More Patterns

If a pattern is useful once, make the artifact directly. If the same shape repeats at least three times, propose a reusable template or generator improvement. Ask the user for confirmation before editing the reusable skill, then add the smallest deterministic template/script change that removes repeated boilerplate.

## Verification

- For static artifacts, inspect the rendered file or at least run a quick browser/screenshot pass when layout quality matters.
- For interactive artifacts, test the primary controls and export action.
- For mobile-sensitive artifacts, check a narrow viewport or use responsive CSS constraints that make overflow unlikely.
- Report any skipped visual or interaction verification in the closeout.
