#!/usr/bin/env python3
"""Validate and aggregate War Council persona reports."""

from __future__ import annotations

import argparse
import json
import math
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Option:
    id: str
    label: str


@dataclass(frozen=True)
class Dimension:
    id: str
    label: str
    weight: float


class WarCouncilError(ValueError):
    pass


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WarCouncilError(message)


def as_number(value: Any, label: str) -> float:
    require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} must be numeric")
    require(math.isfinite(float(value)), f"{label} must be finite")
    return float(value)


def parse_rubric(path: Path) -> tuple[str, list[Option], list[Dimension]]:
    rubric = load_json(path)
    require(isinstance(rubric, dict), "rubric must be an object")
    decision = str(rubric.get("decision", "")).strip()
    require(decision, "rubric.decision is required")

    raw_options = rubric.get("options")
    raw_dimensions = rubric.get("dimensions")
    require(isinstance(raw_options, list) and len(raw_options) >= 2, "rubric.options must contain at least two options")
    require(isinstance(raw_dimensions, list) and 1 <= len(raw_dimensions) <= 10, "rubric.dimensions must contain 1-10 dimensions")

    options: list[Option] = []
    seen_options: set[str] = set()
    for idx, item in enumerate(raw_options, start=1):
        require(isinstance(item, dict), f"option {idx} must be an object")
        option_id = str(item.get("id", "")).strip()
        label = str(item.get("label", "")).strip()
        require(option_id, f"option {idx} missing id")
        require(label, f"option {option_id} missing label")
        require(option_id not in seen_options, f"duplicate option id: {option_id}")
        seen_options.add(option_id)
        options.append(Option(option_id, label))

    dimensions: list[Dimension] = []
    seen_dimensions: set[str] = set()
    total_weight = 0.0
    for idx, item in enumerate(raw_dimensions, start=1):
        require(isinstance(item, dict), f"dimension {idx} must be an object")
        dimension_id = str(item.get("id", "")).strip()
        label = str(item.get("label", "")).strip()
        weight = as_number(item.get("weight"), f"dimension {dimension_id or idx} weight")
        require(dimension_id, f"dimension {idx} missing id")
        require(label, f"dimension {dimension_id} missing label")
        require(dimension_id not in seen_dimensions, f"duplicate dimension id: {dimension_id}")
        require(weight >= 0, f"dimension {dimension_id} weight must be non-negative")
        seen_dimensions.add(dimension_id)
        total_weight += weight
        dimensions.append(Dimension(dimension_id, label, weight))

    require(abs(total_weight - 100.0) < 1e-9, f"rubric weights must total exactly 100, got {total_weight:g}")
    return decision, options, dimensions


def load_reports(reports_dir: Path) -> list[dict[str, Any]]:
    paths = sorted(reports_dir.glob("*.json"))
    require(paths, f"no persona report JSON files found in {reports_dir}")
    reports = []
    seen: set[str] = set()
    for path in paths:
        report = load_json(path)
        require(isinstance(report, dict), f"{path.name} must contain an object")
        persona_id = str(report.get("persona_id", "")).strip()
        require(persona_id, f"{path.name} missing persona_id")
        require(persona_id not in seen, f"duplicate persona_id: {persona_id}")
        seen.add(persona_id)
        report["_path"] = str(path)
        reports.append(report)
    return reports


def validate_report(report: dict[str, Any], options: list[Option], dimensions: list[Dimension]) -> dict[str, float]:
    persona_id = str(report["persona_id"])
    option_ids = [option.id for option in options]
    dimension_ids = [dimension.id for dimension in dimensions]
    option_set = set(option_ids)
    dimension_set = set(dimension_ids)

    recommendation = str(report.get("recommendation", "")).strip()
    require(recommendation in option_set, f"{persona_id}: recommendation must be a known option id")

    confidence = report.get("confidence")
    if confidence is not None:
        confidence_value = as_number(confidence, f"{persona_id}: confidence")
        require(0 <= confidence_value <= 1, f"{persona_id}: confidence must be 0-1")

    scores = report.get("scores")
    require(isinstance(scores, dict), f"{persona_id}: scores must be an object")
    require(set(scores.keys()) == option_set, f"{persona_id}: scores must cover exactly these options: {', '.join(option_ids)}")

    weighted_scores: dict[str, float] = {}
    for option_id in option_ids:
        option_scores = scores.get(option_id)
        require(isinstance(option_scores, dict), f"{persona_id}: scores.{option_id} must be an object")
        require(set(option_scores.keys()) == dimension_set, f"{persona_id}: scores.{option_id} must cover dimensions: {', '.join(dimension_ids)}")
        total = 0.0
        for dimension in dimensions:
            score = as_number(option_scores[dimension.id], f"{persona_id}: {option_id}.{dimension.id}")
            require(0 <= score <= 100, f"{persona_id}: {option_id}.{dimension.id} score must be 0-100")
            total += score * dimension.weight / 100.0
        weighted_scores[option_id] = round(total, 4)

    war_chest = report.get("war_chest")
    require(isinstance(war_chest, dict), f"{persona_id}: war_chest must be an object")
    require(set(war_chest.keys()).issubset(option_set), f"{persona_id}: war_chest contains unknown option")
    allocation_total = 0.0
    for option_id, value in war_chest.items():
        amount = as_number(value, f"{persona_id}: war_chest.{option_id}")
        require(amount >= 0, f"{persona_id}: war_chest.{option_id} must be non-negative")
        allocation_total += amount
    require(abs(allocation_total - 100.0) < 1e-9, f"{persona_id}: war_chest must total exactly 100, got {allocation_total:g}")

    for field in ("agreements", "disagreements", "risks", "kill_criteria"):
        if field in report:
            require(isinstance(report[field], list), f"{persona_id}: {field} must be a list")

    return weighted_scores


def largest_remainder(values: dict[str, float], total: int = 100) -> dict[str, int]:
    floors = {key: int(math.floor(value)) for key, value in values.items()}
    remainder = total - sum(floors.values())
    ranked = sorted(values, key=lambda key: (values[key] - floors[key], key), reverse=True)
    result = dict(floors)
    for key in ranked[:remainder]:
        result[key] += 1
    return result


def tier_options(sorted_options: list[dict[str, Any]]) -> None:
    if not sorted_options:
        return
    top_score = sorted_options[0]["average_weighted_score"]
    for item in sorted_options:
        delta = top_score - item["average_weighted_score"]
        allocation = item["war_chest"]
        if item["rank"] == 1 and delta <= 0.0001:
            tier = "build_first"
        elif delta <= 5 or allocation >= 25:
            tier = "strong_candidate"
        elif allocation >= 10:
            tier = "nice_to_have"
        else:
            tier = "park_it"
        item["tier"] = tier


def aggregate(rubric_path: Path, reports_dir: Path) -> dict[str, Any]:
    decision, options, dimensions = parse_rubric(rubric_path)
    reports = load_reports(reports_dir)
    option_ids = [option.id for option in options]

    persona_summaries: list[dict[str, Any]] = []
    score_by_option: dict[str, list[float]] = {option_id: [] for option_id in option_ids}
    recommendation_votes: dict[str, int] = {option_id: 0 for option_id in option_ids}
    allocation_by_option: dict[str, list[float]] = {option_id: [] for option_id in option_ids}
    agreements: list[str] = []
    disagreements: list[str] = []
    risks: list[str] = []
    kill_criteria: list[str] = []

    for report in reports:
        weighted_scores = validate_report(report, options, dimensions)
        persona_id = str(report["persona_id"])
        recommendation = str(report["recommendation"])
        recommendation_votes[recommendation] += 1
        for option_id in option_ids:
            score_by_option[option_id].append(weighted_scores[option_id])
            allocation_by_option[option_id].append(float(report.get("war_chest", {}).get(option_id, 0)))
        agreements.extend(str(item) for item in report.get("agreements", []))
        disagreements.extend(str(item) for item in report.get("disagreements", []))
        risks.extend(str(item) for item in report.get("risks", []))
        kill_criteria.extend(str(item) for item in report.get("kill_criteria", []))
        persona_summaries.append(
            {
                "persona_id": persona_id,
                "persona_label": report.get("persona_label", persona_id),
                "recommendation": recommendation,
                "weighted_scores": weighted_scores,
                "confidence": report.get("confidence"),
                "source_path": report.get("_path"),
            }
        )

    average_allocations = {
        option_id: sum(values) / len(values)
        for option_id, values in allocation_by_option.items()
    }
    normalized_allocations = largest_remainder(average_allocations, total=100)

    option_rows: list[dict[str, Any]] = []
    option_lookup = {option.id: option.label for option in options}
    for option_id in option_ids:
        scores = score_by_option[option_id]
        average_score = sum(scores) / len(scores)
        score_spread = max(scores) - min(scores)
        option_rows.append(
            {
                "id": option_id,
                "label": option_lookup[option_id],
                "average_weighted_score": round(average_score, 4),
                "recommendation_votes": recommendation_votes[option_id],
                "score_spread": round(score_spread, 4),
                "war_chest": normalized_allocations[option_id],
            }
        )

    option_rows.sort(key=lambda row: (row["average_weighted_score"], row["war_chest"], row["recommendation_votes"]), reverse=True)
    for rank, row in enumerate(option_rows, start=1):
        row["rank"] = rank
    tier_options(option_rows)

    return {
        "decision": decision,
        "options": option_rows,
        "personas": persona_summaries,
        "agreements": sorted(set(item for item in agreements if item)),
        "disagreements": sorted(set(item for item in disagreements if item)),
        "risks": sorted(set(item for item in risks if item)),
        "kill_criteria": sorted(set(item for item in kill_criteria if item)),
    }


def ledger_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# War Council Decision Ledger",
        "",
        "## Decision",
        "",
        payload["decision"],
        "",
        "## Ranked Options",
        "",
    ]
    for option in payload["options"]:
        lines.append(
            f"{option['rank']}. {option['label']} ({option['id']}) - "
            f"score {option['average_weighted_score']:.2f}, "
            f"war chest ${option['war_chest']}, tier `{option['tier']}`"
        )
    lines.extend(["", "## Persona Recommendations", ""])
    for persona in payload["personas"]:
        lines.append(f"- {persona['persona_label']}: {persona['recommendation']}")

    for heading, key in (
        ("Agreements", "agreements"),
        ("Disagreements", "disagreements"),
        ("War Chest", "options"),
        ("Risks Accepted", "risks"),
        ("Kill Criteria", "kill_criteria"),
    ):
        lines.extend(["", f"## {heading}", ""])
        if key == "options":
            for option in payload["options"]:
                lines.append(f"- {option['label']}: ${option['war_chest']}")
        else:
            values = payload.get(key, [])
            if values:
                lines.extend(f"- {value}" for value in values)
            else:
                lines.append("- None recorded")

    lines.append("")
    return "\n".join(lines)


def cmd_aggregate(args: argparse.Namespace) -> int:
    payload = aggregate(args.rubric, args.reports_dir)
    write_json(args.out, payload)
    if args.ledger:
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        args.ledger.write_text(ledger_markdown(payload), encoding="utf-8")
    return 0


def cmd_self_test(_: argparse.Namespace) -> int:
    with tempfile.TemporaryDirectory(prefix="war-council-self-test-") as tmp:
        root = Path(tmp)
        rubric = root / "rubric.json"
        reports = root / "reports"
        reports.mkdir()
        write_json(
            rubric,
            {
                "decision": "Choose a launch path.",
                "options": [
                    {"id": "O1", "label": "Launch now with manual support"},
                    {"id": "O2", "label": "Delay for automation"},
                ],
                "dimensions": [
                    {"id": "D1", "label": "Mission fit", "weight": 40},
                    {"id": "D2", "label": "Economic quality", "weight": 20},
                    {"id": "D3", "label": "Execution realism", "weight": 20},
                    {"id": "D4", "label": "Customer impact", "weight": 20},
                ],
            },
        )
        base_report = {
            "persona_label": "Ruthless CFO",
            "recommendation": "O1",
            "thesis": "Manual launch creates faster learning at acceptable cost.",
            "scores": {
                "O1": {"D1": 90, "D2": 80, "D3": 70, "D4": 75},
                "O2": {"D1": 70, "D2": 65, "D3": 85, "D4": 70},
            },
            "war_chest": {"O1": 70, "O2": 30},
            "agreements": ["Both paths need a support plan."],
            "disagreements": ["Automation value depends on actual support load."],
            "evidence_ids": ["E1"],
            "claim_ids": ["C1"],
            "assumptions_challenged": ["A1"],
            "risks": ["Manual support may not scale."],
            "kill_criteria": ["Support tickets exceed capacity for two consecutive weeks."],
            "confidence": 0.7,
        }
        report_a = dict(base_report, persona_id="ruthless_cfo")
        report_b = dict(
            base_report,
            persona_id="wartime_operator",
            persona_label="Wartime Operator",
            recommendation="O1",
            war_chest={"O1": 60, "O2": 40},
        )
        write_json(reports / "ruthless_cfo.json", report_a)
        write_json(reports / "wartime_operator.json", report_b)
        out = root / "aggregate.json"
        ledger = root / "decision-ledger.md"
        payload = aggregate(rubric, reports)
        write_json(out, payload)
        ledger.write_text(ledger_markdown(payload), encoding="utf-8")
        require(payload["options"][0]["id"] == "O1", "self-test expected O1 to rank first")
        require(sum(option["war_chest"] for option in payload["options"]) == 100, "self-test allocation must total 100")
    print(json.dumps({"passed": True}, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    aggregate_parser = subparsers.add_parser("aggregate", help="validate reports and aggregate the council")
    aggregate_parser.add_argument("--rubric", type=Path, required=True)
    aggregate_parser.add_argument("--reports-dir", type=Path, required=True)
    aggregate_parser.add_argument("--out", type=Path, required=True)
    aggregate_parser.add_argument("--ledger", type=Path)
    aggregate_parser.set_defaults(func=cmd_aggregate)

    self_test = subparsers.add_parser("self-test", help="run a built-in validation fixture")
    self_test.set_defaults(func=cmd_self_test)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except WarCouncilError as exc:
        parser.exit(2, f"war-council: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
