#!/usr/bin/env python3
"""Run narrow current-tree checks for obvious private paths and secret material."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_SUFFIXES = {".gif", ".jpeg", ".jpg", ".pdf", ".png", ".webp"}
BLOCKED_NAMES = {".env", ".env.local", ".env.production", "id_rsa", "id_ed25519"}
PATTERNS = {
    "macOS user home path": re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    "Linux user home path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
    "private key header": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "OpenAI-style secret": re.compile(r"(?<![A-Za-z0-9])" + "sk" + r"-[A-Za-z0-9_-]{20,}"),
    "GitHub personal token": re.compile("gh" + r"[ps]_[A-Za-z0-9]{20,}"),
    "Slack token": re.compile("xox" + r"[abprs]-[A-Za-z0-9-]{20,}"),
}


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
    for path in sorted(repository_files):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if path.name in BLOCKED_NAMES:
            errors.append(f"{relative}: blocked credential or environment filename")
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        checked += 1
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{relative}: matched {label}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Public-boundary check failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Public-boundary check passed for {checked} text files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
