#!/usr/bin/env python3
"""Run lightweight checks against a generated HTML artifact."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


PLACEHOLDER_PATTERNS = [
    re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*"),
    re.compile(r"\{\{[^}]+\}\}"),
    re.compile(r"\bTODO\b", re.IGNORECASE),
]

REQUIRED_PATTERNS = {
    "doctype": re.compile(r"^\s*<!doctype html>", re.IGNORECASE),
    "html lang": re.compile(r"<html[^>]+lang=", re.IGNORECASE),
    "charset": re.compile(r"<meta[^>]+charset=", re.IGNORECASE),
    "viewport": re.compile(r"<meta[^>]+name=[\"']viewport[\"']", re.IGNORECASE),
    "title": re.compile(r"<title>[^<]+</title>", re.IGNORECASE),
}

EXTERNAL_REQUIRED = re.compile(
    r"<(?:script|link|img|iframe)\b[^>]+(?:src|href)=[\"']https?://",
    re.IGNORECASE,
)


def check_file(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []

    for name, pattern in REQUIRED_PATTERNS.items():
        if not pattern.search(text):
            failures.append(f"missing {name}")

    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            failures.append(f"unresolved placeholder-like text: {match.group(0)}")
            break

    if EXTERNAL_REQUIRED.search(text):
        failures.append("required external script/link/img/iframe reference found")

    if len(text.encode("utf-8")) < 1200:
        failures.append("file is suspiciously small for a rendered artifact")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="HTML files to check")
    args = parser.parse_args()

    failed = False
    for raw in args.paths:
        path = pathlib.Path(raw)
        if not path.exists():
            print(f"{path}: missing file", file=sys.stderr)
            failed = True
            continue
        failures = check_file(path)
        if failures:
            failed = True
            print(f"{path}: FAIL", file=sys.stderr)
            for failure in failures:
                print(f"  - {failure}", file=sys.stderr)
        else:
            print(f"{path}: OK")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
