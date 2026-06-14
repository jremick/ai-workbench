#!/usr/bin/env python3
"""Deterministic eval runner for the deterministic-controls skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "cases.json"
DEFAULT_THRESHOLD = 0.92


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def load_cases(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if "cases" not in data or not isinstance(data["cases"], list):
        raise ValueError(f"{path} must contain a top-level cases list")
    return data


def load_docs(root: Path) -> dict[str, str]:
    paths = [root / "SKILL.md"]
    paths.extend(sorted((root / "references").glob("*.md")))
    combined = []
    for path in paths:
        combined.append(path.read_text(encoding="utf-8"))
    return {"__docs__": "\n\n".join(combined)}


def load_answers(path: Path) -> dict[str, str]:
    if path.suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict) and "answers" in data:
            records = data["answers"]
        else:
            raise ValueError("JSON answers must be a list or an object with an answers list")
    else:
        records = []
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSONL at line {line_number}: {exc}") from exc

    answers: dict[str, str] = {}
    for record in records:
        case_id = str(record.get("id", "")).strip()
        answer = str(record.get("answer", "")).strip()
        if not case_id or not answer:
            raise ValueError("Each answer record must include non-empty id and answer fields")
        answers[case_id] = answer
    return answers


def phrase_present(text: str, phrase: str) -> bool:
    return normalize(phrase) in text


def score_case(case: dict[str, Any], text: str, include_avoid: bool) -> dict[str, Any]:
    normalized = normalize(text)
    checks = case.get("checks", [])
    avoid = case.get("avoid", []) if include_avoid else []
    passed = 0
    total = len(checks) + len(avoid)
    details = []

    for check in checks:
        phrases = check.get("any", [])
        name = check.get("name", "unnamed check")
        ok = any(phrase_present(normalized, phrase) for phrase in phrases)
        if ok:
            passed += 1
        details.append({"name": name, "passed": ok, "type": "required", "phrases": phrases})

    for phrase in avoid:
        ok = not phrase_present(normalized, phrase)
        if ok:
            passed += 1
        details.append({"name": f"avoid: {phrase}", "passed": ok, "type": "avoid", "phrases": [phrase]})

    score = 1.0 if total == 0 else passed / total
    return {
        "id": case["id"],
        "score": score,
        "passed": passed,
        "total": total,
        "details": details,
    }


def run(cases_path: Path, root: Path, answers_path: Path | None, threshold: float | None) -> int:
    data = load_cases(cases_path)
    threshold = threshold if threshold is not None else float(data.get("threshold", DEFAULT_THRESHOLD))
    cases = data["cases"]

    if answers_path is None:
        mode = "docs"
        targets = load_docs(root)
    else:
        mode = "answers"
        targets = load_answers(answers_path)

    results = []
    missing_answers = []
    for case in cases:
        case_id = case["id"]
        if mode == "docs":
            text = targets["__docs__"]
        else:
            text = targets.get(case_id)
            if text is None:
                missing_answers.append(case_id)
                continue
        results.append(score_case(case, text, include_avoid=mode == "answers"))

    if missing_answers:
        print("Missing answers for cases:", ", ".join(missing_answers), file=sys.stderr)
        return 2

    overall = sum(result["score"] for result in results) / len(results) if results else 0.0
    report = {
        "skill_name": data.get("skill_name"),
        "mode": mode,
        "threshold": threshold,
        "overall_score": round(overall, 4),
        "passed": overall >= threshold,
        "cases": [
            {
                "id": result["id"],
                "score": round(result["score"], 4),
                "passed": result["score"] >= threshold,
                "failed_checks": [
                    detail["name"] for detail in result["details"] if not detail["passed"]
                ],
            }
            for result in results
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--answers", type=Path, help="JSON or JSONL records with id and answer fields")
    parser.add_argument("--threshold", type=float)
    args = parser.parse_args()
    return run(args.cases, args.root, args.answers, args.threshold)


if __name__ == "__main__":
    raise SystemExit(main())
