#!/usr/bin/env python3
"""Run deterministic smoke checks for the newly published portable skill packages."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        [*args],
        cwd=cwd or ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(args)}\n{message}")
    return result.stdout


def validate_html_artifacts(temp_root: Path) -> int:
    package = ROOT / "skills" / "html-artifacts"
    templates = run(PYTHON, "scripts/create_html_artifact.py", "--list-templates", cwd=package).splitlines()
    expected = {"comparison", "deck", "diagram", "editor", "report", "review"}
    if set(templates) != expected:
        raise RuntimeError(f"unexpected HTML templates: {templates}")
    outputs: list[str] = []
    for template in templates:
        output = temp_root / f"{template}.html"
        run(
            PYTHON,
            "scripts/create_html_artifact.py",
            "--template",
            template,
            "--out",
            str(output),
            "--title",
            f"Synthetic {template}",
            "--summary",
            "Public fixture smoke test.",
            cwd=package,
        )
        outputs.append(str(output))
    run(PYTHON, "scripts/check_html_artifact.py", *outputs, cwd=package)
    return len(outputs)


def validate_html_print_pdf() -> int:
    path = ROOT / "skills" / "html-print-pdf" / "evals" / "evals.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("evals")
    if payload.get("skill_name") != "html-print-pdf" or not isinstance(cases, list) or len(cases) != 3:
        raise RuntimeError("html-print-pdf eval fixture must contain three cases")
    for case in cases:
        if not case.get("prompt") or not case.get("expected_output"):
            raise RuntimeError("html-print-pdf eval case is incomplete")
    return len(cases)


def validate_peek_context_map(temp_root: Path) -> int:
    package = ROOT / "skills" / "peek-context-map"
    source = temp_root / "synthetic-source"
    source.mkdir()
    (source / "README.md").write_text("# Synthetic source\n", encoding="utf-8")
    map_path = temp_root / "map.json"
    ops_path = temp_root / "ops.json"
    ops_path.write_text(
        json.dumps(
            {
                "reasoning": "Synthetic smoke fixture.",
                "operations": [
                    {
                        "type": "ADD",
                        "section": "context_roadmap",
                        "content": "The synthetic source contains one README.",
                        "source_refs": ["README.md:1"],
                        "confidence": 1.0,
                        "priority": 50,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    run(
        PYTHON,
        "scripts/context_map.py",
        "init",
        "--context-id",
        "example:synthetic",
        "--source",
        str(source),
        "--map",
        str(map_path),
        cwd=package,
    )
    run(PYTHON, "scripts/context_map.py", "validate", "--map", str(map_path), cwd=package)
    run(
        PYTHON,
        "scripts/context_map.py",
        "apply-ops",
        "--map",
        str(map_path),
        "--ops",
        str(ops_path),
        "--dry-run",
        cwd=package,
    )
    run(
        PYTHON,
        "scripts/context_map.py",
        "apply-ops",
        "--map",
        str(map_path),
        "--ops",
        str(ops_path),
        cwd=package,
    )
    rendered = run(PYTHON, "scripts/context_map.py", "render", "--map", str(map_path), cwd=package)
    if "The synthetic source contains one README." not in rendered:
        raise RuntimeError("PEEK rendered map omitted the applied fixture")
    run(PYTHON, "scripts/context_map.py", "validate", "--map", str(map_path), cwd=package)
    return 1


def validate_product_review_generator(temp_root: Path) -> int:
    package = ROOT / "skills" / "product-ia-ux-redesign"
    output = temp_root / "review"
    run(
        PYTHON,
        "scripts/init-review-artifacts.py",
        "--out",
        str(output),
        "--product",
        "Synthetic Console",
        "--routes",
        "#home,#objects,#settings",
        "--review-mode",
        "prompt-only",
        cwd=package,
    )
    required = {
        "README.md",
        "00-executive-brief.md",
        "01-source-register.md",
        "03-current-ia-inventory.md",
        "04-role-task-page-purpose-map.md",
        "06-audit-findings.md",
        "07-proposed-ia-route-architecture.md",
        "08-implementation-lanes.md",
        "11-acceptance-browser-verification.md",
        "evidence/README.md",
        "evidence/browser-notes.md",
    }
    missing = sorted(item for item in required if not (output / item).is_file())
    if missing:
        raise RuntimeError(f"review generator omitted required files: {missing}")
    inventory = (output / "03-current-ia-inventory.md").read_text(encoding="utf-8")
    for route in ("#home", "#objects", "#settings"):
        if route not in inventory:
            raise RuntimeError(f"review generator omitted route: {route}")
    return len(required)


def main() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="ai-workbench-skill-smoke-") as raw:
            temp_root = Path(raw)
            html_count = validate_html_artifacts(temp_root)
            eval_count = validate_html_print_pdf()
            map_count = validate_peek_context_map(temp_root)
            artifact_count = validate_product_review_generator(temp_root)
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        "Portable skill package validation passed: "
        f"{html_count} HTML templates, {eval_count} print eval cases, "
        f"{map_count} context-map workflow, {artifact_count} generated review artifacts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
