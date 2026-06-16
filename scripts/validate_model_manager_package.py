#!/usr/bin/env python3
"""Validate the public Model Manager skill package."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "model-manager"
REQUIRED_FILES = [
    PACKAGE / "SKILL.md",
    PACKAGE / "README.md",
    PACKAGE / "skill.json",
    PACKAGE / "scripts" / "model_manager.py",
    PACKAGE / "tests" / "test_model_manager.py",
    PACKAGE / "data" / "model_catalog.json",
    PACKAGE / "data" / "model_system.json",
    PACKAGE / "data" / "eval_cases.json",
    PACKAGE / "data" / "recommendation_values.json",
    PACKAGE / "docs" / "architecture.md",
    PACKAGE / "docs" / "benchmark-sources.md",
    PACKAGE / "docs" / "evaluation.md",
]
LEGACY_PLUGIN_PATH = "plugins/" + "model-manager"
LEGACY_MANIFEST_PATH = ".codex-" + "plugin"
LEGACY_ORG_NAME = "A" + "xon"
FORBIDDEN_PATTERNS = [
    (re.compile(r"/Users/[A-Za-z0-9._-]+"), "local absolute user path"),
    (re.compile(r"~/.codex"), "machine-local Codex path in public docs"),
    (re.compile(re.escape(LEGACY_PLUGIN_PATH)), "private plugin-root path"),
    (re.compile(re.escape(LEGACY_MANIFEST_PATH)), "plugin manifest path"),
    (re.compile(re.escape(LEGACY_ORG_NAME), re.IGNORECASE), "private organization reference"),
    (re.compile(r"(?i)api[_-]?key\\s*[:=]\\s*['\\\"][A-Za-z0-9_\\-]{16,}"), "inline API key assignment"),
]
TEXT_SUFFIXES = {".md", ".json", ".py", ".toml"}


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run(args: list[str], cwd: Path = ROOT) -> tuple[int, str, str]:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    return result.returncode, result.stdout, result.stderr


def check_required_files(errors: list[str]) -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required file: {relative(path)}")


def check_json(errors: list[str]) -> None:
    for path in PACKAGE.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{relative(path)}: invalid JSON: {exc}")


def check_public_surface(errors: list[str]) -> None:
    blocked_files = [
        PACKAGE / "LICENSE.txt",
        PACKAGE / "SECURITY.md",
        PACKAGE / "CONTRIBUTING.md",
        PACKAGE / "data" / "artificial_analysis_models.cache.json",
    ]
    for path in blocked_files:
        if path.exists():
            errors.append(f"unexpected package-local file: {relative(path)}")

    for path in PACKAGE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{relative(path)} contains {label}")


def check_skill_metadata(errors: list[str]) -> None:
    metadata = json.loads((PACKAGE / "skill.json").read_text(encoding="utf-8"))
    if metadata.get("license") != "Apache-2.0":
        errors.append("skill.json license must match repo license: Apache-2.0")
    if metadata.get("status") != "public-alpha":
        errors.append("skill.json status must be public-alpha")

    skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
    if "status: public-alpha" not in skill:
        errors.append("SKILL.md must declare status: public-alpha")


def check_recommendation_values(errors: list[str]) -> None:
    values = json.loads((PACKAGE / "data" / "recommendation_values.json").read_text(encoding="utf-8"))
    if values.get("attribution_required") is not True:
        errors.append("recommendation_values.json must mark attribution_required=true")
    cache = values.get("artificial_analysis_cache", {})
    if cache.get("used") is not True:
        errors.append("recommendation_values.json should preserve refreshed Artificial Analysis influence")
    if "api_key" in json.dumps(values).lower() or "x-api-key" in json.dumps(values).lower():
        errors.append("recommendation_values.json contains secret-like key marker")


def check_commands(errors: list[str]) -> None:
    script = PACKAGE / "scripts" / "model_manager.py"
    commands = [
        ["python3", str(script), "validate-skill", "--skill-dir", str(PACKAGE), "--json"],
        ["python3", str(script), "eval", "--json"],
        ["python3", "-m", "unittest", "discover", "-s", str(PACKAGE / "tests")],
    ]
    for command in commands:
        code, stdout, stderr = run(command)
        if code != 0:
            errors.append(f"command failed: {' '.join(command)}\n{stdout}{stderr}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_json(errors)
    check_public_surface(errors)
    check_skill_metadata(errors)
    check_recommendation_values(errors)
    check_commands(errors)
    result = {"passed": not errors, "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
