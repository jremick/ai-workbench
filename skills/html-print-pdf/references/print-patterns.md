# Print Patterns

Copy only the patterns that match the artifact, then adapt selectors to the page. Place print CSS after screen CSS.

## Base Print Reset

```css
@media print {
  @page {
    size: A4 portrait;
    margin: 1.5cm;
  }

  html,
  body {
    height: auto !important;
    overflow: visible !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## Page Size Variants

```css
/* Slide decks / presentations */
@page {
  size: landscape;
  margin: 0;
}

/* Reports / documents / plans */
@page {
  size: A4 portrait;
  margin: 1.5cm;
}

/* Wide tables / dashboards */
@page {
  size: landscape;
  margin: 1cm;
}
```

## Hide Interactive UI

Prefer `.no-print` for controls you add. Add project-specific selectors only after confirming they exist.

```css
@media print {
  .no-print,
  .nav,
  .controls,
  .toolbar,
  .slide-counter,
  .key-hint,
  #notes-panel {
    display: none !important;
  }
}
```

Use broad `button { display: none !important; }` only when buttons are purely controls and never part of the printable document.

## Slide Deck Printing

Use when one slide is shown at a time on screen.

```css
@media print {
  .deck,
  .slides-container {
    position: static !important;
    width: 100% !important;
    height: auto !important;
    overflow: visible !important;
  }

  .slide {
    position: relative !important;
    display: flex !important;
    width: 100% !important;
    height: 100vh !important;
    overflow: hidden !important;
    page-break-after: always;
    break-after: page;
  }

  .slide:last-child {
    page-break-after: avoid;
    break-after: avoid;
  }
}
```

If inactive slides use attributes or framework state, override those too:

```css
@media print {
  .slide[hidden],
  .slide[aria-hidden="true"] {
    display: flex !important;
    visibility: visible !important;
  }
}
```

## Scrollable Reports

```css
@media print {
  body,
  main,
  .page,
  .report,
  .content {
    overflow: visible !important;
    height: auto !important;
  }

  .page-section,
  section.print-page {
    page-break-after: always;
    break-after: page;
  }

  .page-section:last-child,
  section.print-page:last-child {
    page-break-after: avoid;
    break-after: avoid;
  }
}
```

## Preserve Grid Layouts

Use the grid classes or data attributes that exist in the page.

```css
@media print {
  .grid-2 {
    grid-template-columns: 1fr 1fr !important;
  }

  .grid-3 {
    grid-template-columns: 1fr 1fr 1fr !important;
  }

  .grid-4 {
    grid-template-columns: 1fr 1fr !important;
  }
}
```

## Theme And Color Handling

```css
@media print {
  html,
  body,
  body.light,
  body.dark,
  body.light *,
  body.dark * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
}
```

For dark themes, decide whether the PDF should preserve the dark theme or force a print-specific light theme:

```css
@media print {
  body.print-light {
    background: #ffffff !important;
    color: #111111 !important;
  }
}
```

## Print Button

```html
<button class="no-print" type="button" onclick="window.print()" title="Print or save as PDF">
  PDF
</button>
```

If the app has event handlers or a component framework, wire the same `window.print()` behavior through the local component pattern instead of inline HTML.

## Command-Line Smoke Test

If Google Chrome is available, generate a browser-native PDF without adding new dependencies:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --disable-gpu \
  --no-first-run \
  --no-default-browser-check \
  --print-to-pdf="$PWD/print-smoke.pdf" \
  "file://$PWD/index.html"
```

Then check page count and extracted text when `pypdf` is available:

```bash
python3 - <<'PY'
from pypdf import PdfReader

pdf = PdfReader("print-smoke.pdf")
print("pages", len(pdf.pages))
for index, page in enumerate(pdf.pages, 1):
    text = (page.extract_text() or "").strip().replace("\n", " | ")
    print(index, text[:160])
PY
```

For visual layout checks, render the PDF to page images with Poppler when available:

```bash
pdftoppm -png print-smoke.pdf print-smoke-page
```

Passing text extraction is not enough for final delivery, but it quickly catches missing slides, missing report sections, and accidental blank pages.
