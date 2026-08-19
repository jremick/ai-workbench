#!/usr/bin/env python3
"""Check local Markdown links and images without making network requests."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    checked = 0
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    repository_files = [ROOT / item.decode() for item in result.stdout.split(b"\0") if item]
    for markdown in sorted(path for path in repository_files if path.suffix.lower() == ".md"):
        text = markdown.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip()
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            target = raw.split(maxsplit=1)[0].strip("'\"")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            if target.startswith("/"):
                errors.append(f"{markdown.relative_to(ROOT)}: absolute local link is not public-safe")
                continue
            local = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not local:
                continue
            checked += 1
            resolved = (markdown.parent / local).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{markdown.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{markdown.relative_to(ROOT)}: missing local target: {target}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Markdown link check failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Markdown link check passed for {checked} local targets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
