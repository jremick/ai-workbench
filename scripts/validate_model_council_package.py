#!/usr/bin/env python3
"""Validate the model-council, deep-research, and DRACO benchmark packages."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PATHS = [
    ROOT / "skills" / "model-council",
    ROOT / "skills" / "deep-research",
    ROOT / "tools" / "model-council-runner",
    ROOT / "benchmarks" / "model-council-draco",
    ROOT / "docs" / "model-council-and-deep-research.md",
]
REQUIRED_FILES = [
    ROOT / "skills" / "model-council" / "SKILL.md",
    ROOT / "skills" / "model-council" / "README.md",
    ROOT / "skills" / "model-council" / "references" / "provider-routing.md",
    ROOT / "skills" / "deep-research" / "SKILL.md",
    ROOT / "skills" / "deep-research" / "README.md",
    ROOT / "tools" / "model-council-runner" / "scripts" / "council_runner.py",
    ROOT / "tools" / "model-council-runner" / "configs" / "local-cli.base.json",
    ROOT / "tools" / "model-council-runner" / "configs" / "vercel-gateway.base.json",
    ROOT / "tools" / "model-council-runner" / "fixtures" / "smoke-task.json",
    ROOT / "tools" / "model-council-runner" / "diagrams" / "skill-workflow-routing.mmd",
    ROOT / "tools" / "model-council-runner" / "diagrams" / "base-council-flow.mmd",
    ROOT / "tools" / "model-council-runner" / "diagrams" / "council-level-base.mmd",
    ROOT / "tools" / "model-council-runner" / "diagrams" / "council-level-adversarial.mmd",
    ROOT / "tools" / "model-council-runner" / "diagrams" / "council-level-stress-test.mmd",
    ROOT / "tools" / "model-council-runner" / "diagrams" / "council-level-extended.mmd",
    ROOT / "tools" / "model-council-runner" / "diagrams" / "provider-routing.mmd",
    ROOT / "tools" / "model-council-runner" / "diagrams" / "deep-research-council-escalation.mmd",
    ROOT / "benchmarks" / "README.md",
    ROOT / "benchmarks" / "model-council-draco" / "README.md",
    ROOT / "benchmarks" / "model-council-draco" / "scripts" / "draco_benchmark.py",
]
FORBIDDEN_PATTERNS = [
    (re.compile(r"/Users/[A-Za-z0-9._-]+"), "local absolute user path"),
    (re.compile(r"(?i)api[_-]?key\\s*[:=]\\s*['\\\"][A-Za-z0-9_\\-]{16,}"), "inline API key assignment"),
]


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    return result.returncode, result.stdout, result.stderr


def check_required_files(errors: list[str]) -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required file: {relative(path)}")


def check_json(errors: list[str]) -> None:
    for base in PUBLIC_PATHS:
        if base.is_file():
            candidates = [base] if base.suffix == ".json" else []
        else:
            candidates = list(base.rglob("*.json"))
        for path in candidates:
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{relative(path)}: invalid JSON: {exc}")


def check_forbidden_patterns(errors: list[str]) -> None:
    for base in PUBLIC_PATHS:
        candidates = [base] if base.is_file() else [path for path in base.rglob("*") if path.is_file()]
        for path in candidates:
            if path.suffix.lower() not in {".md", ".mmd", ".json", ".py"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern, label in FORBIDDEN_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{relative(path)} contains {label}")


def check_runner(errors: list[str]) -> None:
    runner = ROOT / "tools" / "model-council-runner" / "scripts" / "council_runner.py"
    task = ROOT / "tools" / "model-council-runner" / "fixtures" / "smoke-task.json"
    configs = [
        ROOT / "tools" / "model-council-runner" / "configs" / "local-cli.base.json",
        ROOT / "tools" / "model-council-runner" / "configs" / "vercel-gateway.base.json",
    ]
    for config in configs:
        code, stdout, stderr = run(["python3", str(runner), "validate", "--config", str(config), "--task", str(task)])
        if code != 0:
            errors.append(f"runner validate failed for {relative(config)}: {stdout}{stderr}")

    with tempfile.TemporaryDirectory(prefix="model-council-validate-") as tmp:
        run_dir = Path(tmp) / "plan"
        code, stdout, stderr = run(
            [
                "python3",
                str(runner),
                "plan",
                "--config",
                str(configs[0]),
                "--task",
                str(task),
                "--run-dir",
                str(run_dir),
                "--force",
            ]
        )
        if code != 0:
            errors.append(f"runner plan failed: {stdout}{stderr}")
            return
        manifest = run_dir / "manifest.json"
        code, stdout, stderr = run(["python3", str(runner), "validate", "--manifest", str(manifest)])
        if code != 0:
            errors.append(f"runner manifest validate failed: {stdout}{stderr}")


def check_draco_fixture(errors: list[str]) -> None:
    script = ROOT / "benchmarks" / "model-council-draco" / "scripts" / "draco_benchmark.py"
    rows = [
        {
            "id": "case-a",
            "prompt": "Explain whether a deterministic runner improves a model council.",
            "rubric": "Reward answers that mention isolation, repeatability, and saved evidence.",
            "domain": "evals",
        },
        {
            "id": "case-b",
            "question": "Compare local CLIs and an API gateway.",
            "criteria": ["route clarity", "auth boundary", "cost control"],
            "domain": "routing",
        },
    ]
    with tempfile.TemporaryDirectory(prefix="draco-fixture-") as tmp:
        tmp_path = Path(tmp)
        fixture = tmp_path / "fixture.jsonl"
        fixture.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
        out_dir = tmp_path / "sample"
        code, stdout, stderr = run(
            [
                "python3",
                str(script),
                "sample",
                "--input",
                str(fixture),
                "--out-dir",
                str(out_dir),
                "--count",
                "2",
                "--seed",
                "7",
            ]
        )
        if code != 0:
            errors.append(f"draco sample failed: {stdout}{stderr}")
            return
        manifest = out_dir / "sample-manifest.json"
        if not manifest.exists():
            errors.append("draco sample did not write sample-manifest.json")
            return
        for case in json.loads(manifest.read_text(encoding="utf-8"))["cases"]:
            generation = json.loads(Path(case["generation_task"]).read_text(encoding="utf-8"))
            if "rubric" in json.dumps(generation).lower() or "criteria" in json.dumps(generation).lower():
                errors.append(f"generation task leaked rubric fields: {case['generation_task']}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_json(errors)
    check_forbidden_patterns(errors)
    check_runner(errors)
    check_draco_fixture(errors)
    result = {"passed": not errors, "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
