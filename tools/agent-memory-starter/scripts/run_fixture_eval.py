#!/usr/bin/env python3
"""Run deterministic fixture retrieval evals for Agent Memory Starter."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "fixtures" / "sample-corpus.json"
DEFAULT_EVALS = ROOT / "evals" / "search-quality.json"

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "be",
    "do",
    "does",
    "how",
    "is",
    "it",
    "of",
    "or",
    "should",
    "still",
    "the",
    "to",
    "what",
    "when",
    "with",
    "without",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2 and token not in STOP_WORDS
    ]


def page_text(page: dict[str, Any]) -> str:
    parts: list[str] = [
        page.get("slug", ""),
        page.get("title", ""),
        page.get("summary", ""),
        page.get("compiled_truth", ""),
        " ".join(page.get("tags", [])),
    ]

    for entry in page.get("timeline", []):
        parts.append(entry.get("event_text", ""))
    for chunk in page.get("chunks", []):
        parts.append(chunk.get("content", ""))

    return "\n".join(parts)


def score_page(query: str, page: dict[str, Any]) -> float:
    query_tokens = tokenize(query)
    if not query_tokens:
        return 0.0

    body_counts = Counter(tokenize(page_text(page)))
    title_counts = Counter(tokenize(page.get("title", "")))
    slug_counts = Counter(tokenize(page.get("slug", "").replace("/", " ")))

    score = 0.0
    for token in query_tokens:
        score += body_counts[token]
        score += 2.0 * title_counts[token]
        score += 1.5 * slug_counts[token]

    normalized_query = " ".join(query_tokens)
    normalized_body = " ".join(tokenize(page_text(page)))
    if normalized_query and normalized_query in normalized_body:
        score += 5.0

    return score


def rank_pages(query: str, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = [
        {
            "slug": page["slug"],
            "score": score_page(query, page),
        }
        for page in pages
    ]
    return sorted(ranked, key=lambda item: (-item["score"], item["slug"]))


def run_eval(corpus_path: Path, evals_path: Path) -> dict[str, Any]:
    corpus = load_json(corpus_path)
    evals = load_json(evals_path)
    pages = corpus["pages"]

    results = []
    for case in evals["cases"]:
        ranked = rank_pages(case["query"], pages)
        top_slug = ranked[0]["slug"] if ranked else None
        passed = top_slug == case["expected_top_slug"]
        results.append(
            {
                "id": case["id"],
                "passed": passed,
                "expected_top_slug": case["expected_top_slug"],
                "actual_top_slug": top_slug,
                "top_scores": ranked[:3],
            }
        )

    return {
        "name": evals["name"],
        "passed": all(result["passed"] for result in results),
        "cases": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--evals", type=Path, default=DEFAULT_EVALS)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_eval(args.corpus, args.evals)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
