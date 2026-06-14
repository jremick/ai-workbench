#!/usr/bin/env python3
"""Prepare DRACO benchmark samples for model-council skill evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import urllib.request
from pathlib import Path
from typing import Any


DRACO_TEST_URL = "https://huggingface.co/datasets/perplexity-ai/draco/resolve/main/test.jsonl"
PROMPT_KEYS = ("prompt", "question", "problem", "task", "input", "query")
RUBRIC_KEYS = ("rubric", "criteria", "grading_rubric", "evaluation", "judge", "scoring", "answer")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise SystemExit(f"{path}:{line_number}: expected object")
            rows.append(row)
    return rows


def first_value(row: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def row_id(row: dict[str, Any], index: int) -> str:
    for key in ("id", "uid", "example_id", "problem_id"):
        if row.get(key) not in (None, ""):
            return str(row[key])
    return f"draco-{index:05d}"


def normalize_rubric(value: Any) -> Any:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                return json.loads(stripped)
            except json.JSONDecodeError:
                return value
    return value


def split_row(row: dict[str, Any], index: int) -> tuple[dict[str, Any], dict[str, Any]]:
    rid = row_id(row, index)
    prompt = first_value(row, PROMPT_KEYS)
    rubric = first_value(row, RUBRIC_KEYS)
    generation = {
        "id": rid,
        "benchmark": "draco",
        "question": prompt if prompt is not None else row,
        "metadata": {
            key: row[key]
            for key in ("domain", "category", "source", "difficulty")
            if key in row
        },
    }
    rubric_payload = {
        "id": rid,
        "benchmark": "draco",
        "rubric": normalize_rubric(rubric),
        "withheld_fields": {
            key: row[key]
            for key in RUBRIC_KEYS
            if key in row
        },
    }
    return generation, rubric_payload


def cmd_fetch(args: argparse.Namespace) -> int:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(DRACO_TEST_URL, timeout=120) as response:
        args.output.write_bytes(response.read())
    print(json.dumps({"output": str(args.output), "sha256": sha256_file(args.output)}, indent=2))
    return 0


def cmd_sample(args: argparse.Namespace) -> int:
    rows = load_jsonl(args.input)
    if args.count > len(rows):
        raise SystemExit(f"count {args.count} exceeds dataset rows {len(rows)}")
    if args.strategy == "first":
        selected_indexes = list(range(args.count))
    else:
        rng = random.Random(args.seed)
        selected_indexes = sorted(rng.sample(range(len(rows)), args.count))
    generation_dir = args.out_dir / "generation-tasks"
    rubric_dir = args.out_dir / "grading-rubrics"
    generation_dir.mkdir(parents=True, exist_ok=True)
    rubric_dir.mkdir(parents=True, exist_ok=True)

    cases = []
    for index in selected_indexes:
        generation, rubric = split_row(rows[index], index)
        safe_id = "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in generation["id"])
        generation_path = generation_dir / f"{safe_id}.json"
        rubric_path = rubric_dir / f"{safe_id}.json"
        generation_path.write_text(json.dumps(generation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        rubric_path.write_text(json.dumps(rubric, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        cases.append(
            {
                "id": generation["id"],
                "source_index": index,
                "generation_task": str(generation_path),
                "grading_rubric": str(rubric_path),
            }
        )

    manifest = {
        "benchmark": "draco",
        "source": str(args.input),
        "source_sha256": sha256_file(args.input),
        "seed": args.seed,
        "count": args.count,
        "strategy": args.strategy,
        "rubric_policy": "Rubrics are withheld from generation tasks.",
        "cases": cases,
    }
    manifest_path = args.out_dir / "sample-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "count": args.count}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch = subparsers.add_parser("fetch", help="Download DRACO test JSONL.")
    fetch.add_argument("--output", type=Path, required=True)
    fetch.set_defaults(func=cmd_fetch)

    sample = subparsers.add_parser("sample", help="Create deterministic generation and rubric files.")
    sample.add_argument("--input", type=Path, required=True)
    sample.add_argument("--out-dir", type=Path, required=True)
    sample.add_argument("--count", type=int, default=20)
    sample.add_argument("--seed", type=int, default=42)
    sample.add_argument("--strategy", choices=["random", "first"], default="random")
    sample.set_defaults(func=cmd_sample)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
