#!/usr/bin/env python3
"""Create a starter self-contained HTML artifact from a bundled template."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import re
import sys
from string import Template


ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "assets" / "templates"

RAW_KEYS = {
    "content_html",
    "sections_html",
    "cards_html",
    "timeline_html",
    "slides_html",
    "diagram_html",
    "editor_body_html",
    "data_js",
    "export_js",
}

DEFAULTS = {
    "title": "Untitled HTML artifact",
    "eyebrow": "HTML artifact",
    "summary": "Replace this summary with the artifact's purpose, source, and decision context.",
    "source_note": "Source note: update with the files, live systems, or prompt this artifact reflects.",
    "content_html": '<section class="panel"><h2>Replace this section</h2><p>Add the real artifact content here.</p></section>',
    "sections_html": '<section class="panel"><h2>Section</h2><p>Add the real content here.</p></section>',
    "cards_html": '<article class="card"><h2>Option A</h2><p>Replace with comparable content.</p></article>',
    "timeline_html": '<li><time>00:00</time><div><strong>Event</strong><p>Replace with timeline detail.</p></div></li>',
    "slides_html": '<section class="slide active"><h1>Title slide</h1><p>Replace with the deck opening.</p></section>',
    "diagram_html": '<svg viewBox="0 0 640 220" role="img" aria-label="Placeholder diagram"><rect x="24" y="72" width="160" height="72" rx="8"/><text x="104" y="114" text-anchor="middle">Start</text><path d="M190 108h110"/><rect x="306" y="72" width="160" height="72" rx="8"/><text x="386" y="114" text-anchor="middle">System</text><path d="M472 108h110"/><rect x="586" y="72" width="32" height="72" rx="8"/></svg>',
    "editor_body_html": '<textarea id="editorInput">Replace this with task-local data.</textarea>',
    "data_js": "const initialState = {};",
    "export_js": "return document.getElementById('editorInput')?.value || '';",
}


def list_templates() -> list[str]:
    return sorted(path.stem for path in TEMPLATE_DIR.glob("*.html"))


def load_data(path: str | None) -> dict[str, object]:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_key_values(values: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"--set/--raw values must be key=value, got: {value}")
        key, item = value.split("=", 1)
        if not key:
            raise SystemExit(f"empty key in value: {value}")
        parsed[key] = item
    return parsed


def render_value(key: str, value: object) -> str:
    if isinstance(value, (dict, list)):
        text = json.dumps(value, indent=2, ensure_ascii=False)
    else:
        text = str(value)
    if key in RAW_KEYS or key.endswith("_html") or key.endswith("_js"):
        return text
    return html.escape(text, quote=True)


def build_context(args: argparse.Namespace) -> dict[str, str]:
    data = {**DEFAULTS, **load_data(args.data)}
    data.update(parse_key_values(args.set))
    data["generated_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    data["css"] = (TEMPLATE_DIR / "shared.css").read_text(encoding="utf-8")
    context = {key: render_value(key, value) for key, value in data.items()}
    context.update({key: str(value) for key, value in parse_key_values(args.raw).items()})
    return context


def render(template_name: str, context: dict[str, str]) -> str:
    template_path = TEMPLATE_DIR / f"{template_name}.html"
    if not template_path.exists():
        available = ", ".join(list_templates())
        raise SystemExit(f"unknown template '{template_name}'. Available: {available}")
    text = template_path.read_text(encoding="utf-8")
    rendered = Template(text).safe_substitute(context)
    unresolved = sorted(set(re.findall(r"\$[A-Za-z_][A-Za-z0-9_]*", rendered)))
    if unresolved:
        raise SystemExit(f"unresolved placeholders in output: {', '.join(unresolved)}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", "-t", choices=list_templates(), help="Template name")
    parser.add_argument("--out", "-o", help="Output .html path")
    parser.add_argument("--title", help="Artifact title")
    parser.add_argument("--summary", help="Short summary/framing copy")
    parser.add_argument("--data", help="JSON file with template values")
    parser.add_argument("--set", action="append", default=[], help="Escaped key=value value")
    parser.add_argument("--raw", action="append", default=[], help="Raw key=value HTML/JS value")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    args = parser.parse_args()

    if args.list_templates:
        print("\n".join(list_templates()))
        return 0
    if not args.template or not args.out:
        parser.error("--template and --out are required unless --list-templates is used")

    context = build_context(args)
    if args.title:
        context["title"] = render_value("title", args.title)
    if args.summary:
        context["summary"] = render_value("summary", args.summary)

    rendered = render(args.template, context)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
