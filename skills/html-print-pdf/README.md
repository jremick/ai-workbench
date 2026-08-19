# HTML Print PDF

> **Status: Current public snapshot.**

A focused workflow for making an existing HTML report, dashboard, or slide deck print cleanly through the browser and save as PDF.

## Package contents

- `SKILL.md` — artifact inspection, print-page selection, selector adaptation, and verification.
- `references/print-patterns.md` — adaptable CSS and browser-PDF smoke-test patterns.
- `evals/evals.json` — three documented prompt/expectation cases.

## Use it

Read the HTML before applying any pattern. Selectors in the reference are examples, not universal rules. The intended verification path is a browser print preview or generated PDF followed by page-count, text, and visual inspection.

## Claim limits

The included eval cases are package-authored expectations, not independent behavioral acceptance. PDF rendering varies by browser, font availability, page size, and the source artifact's CSS. No supported-browser matrix is published.
