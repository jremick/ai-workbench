#!/usr/bin/env python3
"""Call the Agent Memory Starter Edge Function."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError


FUNCTION_URL_ENV = "AGENT_MEMORY_FUNCTION_URL"
FUNCTION_TOKEN_ENV = "AGENT_MEMORY_FUNCTION_TOKEN"


class AgentMemoryError(RuntimeError):
    """Expected command failure."""


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise AgentMemoryError(f"Missing required environment variable: {name}")
    return value


def call_function(payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        require_env(FUNCTION_URL_ENV),
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-agent-memory-token": require_env(FUNCTION_TOKEN_ENV),
        },
    )

    try:
        with request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AgentMemoryError(f"function returned {exc.code}: {detail}") from exc
    except URLError as exc:
        raise AgentMemoryError(f"function request failed: {exc}") from exc


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def command_stats(_: argparse.Namespace) -> int:
    print_json(call_function({"mode": "stats"}))
    return 0


def command_search(args: argparse.Namespace) -> int:
    payload: dict[str, Any] = {
        "mode": "query" if args.semantic else "text_search",
        "query": args.query,
        "match_count": args.limit,
    }
    if args.scope:
        payload["include_scopes"] = args.scope
    print_json(call_function(payload))
    return 0


def command_page(args: argparse.Namespace) -> int:
    print_json(
        call_function(
            {
                "mode": "page",
                "slug": args.slug,
                "include_embeddings": args.include_embeddings,
            }
        )
    )
    return 0


def command_backfill(args: argparse.Namespace) -> int:
    print_json(call_function({"mode": "backfill", "batch_size": args.batch_size}))
    return 0


def command_propose(args: argparse.Namespace) -> int:
    print_json(
        call_function(
            {
                "mode": "propose_update",
                "proposed_by": args.proposed_by,
                "target_slug": args.target_slug,
                "change_type": args.change_type,
                "proposed_text": args.text,
                "reason": args.reason,
                "scope": args.scope,
                "sensitivity": args.sensitivity,
                "source_uri": args.source_uri,
            }
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    stats = subparsers.add_parser("stats", help="Show memory counts and embedding status.")
    stats.set_defaults(func=command_stats)

    search = subparsers.add_parser("search", aliases=["text-search"], help="Search memory.")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--scope", action="append", help="Limit to a scope. Repeatable.")
    search.add_argument("--semantic", action="store_true", help="Create a query embedding for hybrid search.")
    search.set_defaults(func=command_search)

    page = subparsers.add_parser("page", help="Read one page bundle by slug.")
    page.add_argument("slug")
    page.add_argument("--include-embeddings", action="store_true")
    page.set_defaults(func=command_page)

    backfill = subparsers.add_parser("backfill", help="Embed pending or stale chunks.")
    backfill.add_argument("--batch-size", type=int, default=25)
    backfill.set_defaults(func=command_backfill)

    propose = subparsers.add_parser("propose", help="Submit a reviewable memory update proposal.")
    propose.add_argument("--target-slug")
    propose.add_argument(
        "--change-type",
        required=True,
        choices=["create_page", "update_compiled_truth", "append_timeline", "add_chunk", "archive_page"],
    )
    propose.add_argument("--text", required=True)
    propose.add_argument("--reason", default="")
    propose.add_argument("--scope", default="shared", choices=["personal", "team", "shared", "public"])
    propose.add_argument(
        "--sensitivity",
        default="internal",
        choices=["public", "internal", "private", "restricted"],
    )
    propose.add_argument("--source-uri")
    propose.add_argument("--proposed-by", default="unknown-agent")
    propose.set_defaults(func=command_propose)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except AgentMemoryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
