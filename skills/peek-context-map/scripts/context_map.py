#!/usr/bin/env python3
"""Manage PEEK-style context maps without model calls."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


VERSION = "0.1"
DEFAULT_BUDGET = 1024
SECTION_ORDER = [
    "context_roadmap",
    "context_understanding",
    "domain_constants",
    "parsing_schema",
    "reusable_results",
    "known_failure_patterns",
]
SECTION_TITLES = {
    "context_roadmap": "CONTEXT ROADMAP",
    "context_understanding": "CONTEXT UNDERSTANDING",
    "domain_constants": "DOMAIN CONSTANTS",
    "parsing_schema": "PARSING SCHEMA",
    "reusable_results": "REUSABLE RESULTS",
    "known_failure_patterns": "KNOWN FAILURE PATTERNS",
}
SECTION_PREFIXES = {
    "context_roadmap": "cr",
    "context_understanding": "cu",
    "domain_constants": "dc",
    "parsing_schema": "ps",
    "reusable_results": "rr",
    "known_failure_patterns": "kf",
}
EVICTION_SECTION_ORDER = {
    "known_failure_patterns": 0,
    "parsing_schema": 1,
    "reusable_results": 2,
    "context_roadmap": 3,
    "domain_constants": 4,
    "context_understanding": 5,
}
EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
    ".next",
    ".turbo",
}


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_map_dir() -> Path:
    return Path.home() / ".codex" / "context-maps"


def read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")
    tmp.replace(path)


def run_git(args: list[str], cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return result.stdout.strip() or None


def git_root(path: Path) -> Path | None:
    probe = path if path.is_dir() else path.parent
    out = run_git(["rev-parse", "--show-toplevel"], probe)
    return Path(out).resolve() if out else None


def slugify(value: str, limit: int = 64) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return (slug or "context")[:limit].strip("-") or "context"


def map_filename(context_id: str) -> str:
    digest = hashlib.sha256(context_id.encode("utf-8")).hexdigest()[:12]
    return f"{slugify(context_id, 48)}-{digest}.json"


def resolve_context_id(sources: list[Path], explicit: str | None = None) -> str:
    if explicit:
        return explicit
    first = sources[0].resolve() if sources else Path.cwd().resolve()
    root = git_root(first)
    if root:
        remote = run_git(["config", "--get", "remote.origin.url"], root) or str(root)
        rel = "."
        try:
            rel = str(first.relative_to(root))
        except ValueError:
            pass
        head = run_git(["rev-parse", "--short", "HEAD"], root) or "unknown"
        return f"git:{remote}#{rel}@{head}"
    return f"path:{first}"


def resolve_map_path(context_id: str, map_dir: Path | None = None) -> Path:
    return (map_dir or default_map_dir()) / map_filename(context_id)


def estimate_tokens(text: str) -> int:
    return len(re.findall(r"\w+|[^\s\w]", text, flags=re.UNICODE))


def hash_file(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    stat = path.stat()
    return {
        "path": str(path.resolve()),
        "sha256": digest.hexdigest(),
        "bytes": stat.st_size,
    }


def iter_fingerprint_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)
        current = Path(dirpath)
        if current.name == "context-maps" and current.parent.name == ".codex":
            dirnames[:] = []
            continue
        for name in sorted(filenames):
            if name.startswith(".DS_Store"):
                continue
            files.append(current / name)
            if len(files) >= max_files:
                return files
    return files


def fingerprint_sources(sources: list[Path], max_files: int = 1000) -> dict[str, Any]:
    source_entries: list[dict[str, Any]] = []
    for source in sources:
        source = source.expanduser().resolve()
        if source.is_file():
            source_entries.append({"kind": "file", **hash_file(source)})
        elif source.is_dir():
            files = iter_fingerprint_files(source, max_files)
            digest = hashlib.sha256()
            file_entries = []
            for file_path in files:
                file_hash = hash_file(file_path)
                rel = str(file_path.relative_to(source))
                digest.update(rel.encode("utf-8"))
                digest.update(file_hash["sha256"].encode("utf-8"))
                file_entries.append({"path": rel, "sha256": file_hash["sha256"], "bytes": file_hash["bytes"]})
            source_entries.append(
                {
                    "kind": "directory",
                    "path": str(source),
                    "sha256": digest.hexdigest(),
                    "file_count": len(file_entries),
                    "truncated": len(file_entries) >= max_files,
                    "files": file_entries,
                }
            )
        else:
            source_entries.append({"kind": "missing", "path": str(source)})

    first = sources[0].expanduser().resolve() if sources else Path.cwd().resolve()
    root = git_root(first)
    fingerprint: dict[str, Any] = {
        "generated_at": now_iso(),
        "sources": source_entries,
    }
    if root:
        fingerprint.update(
            {
                "kind": "git",
                "git_root": str(root),
                "git_remote": run_git(["config", "--get", "remote.origin.url"], root),
                "git_head": run_git(["rev-parse", "HEAD"], root),
                "git_status_short": run_git(["status", "--short"], root) or "",
            }
        )
    else:
        fingerprint["kind"] = "path"
    return fingerprint


def empty_sections() -> dict[str, list[dict[str, Any]]]:
    return {section: [] for section in SECTION_ORDER}


def new_map(context_id: str, name: str | None, budget: int, sources: list[Path]) -> dict[str, Any]:
    timestamp = now_iso()
    return {
        "version": VERSION,
        "context_id": context_id,
        "name": name or context_id,
        "budget_tokens": budget,
        "created_at": timestamp,
        "updated_at": timestamp,
        "fingerprint": fingerprint_sources(sources),
        "sections": empty_sections(),
    }


def render_map(data: dict[str, Any], include_stale: bool = False) -> str:
    lines = [
        "## PEEK CONTEXT MAP",
        f"Context: {data.get('name') or data.get('context_id')}",
        f"Budget: {data.get('budget_tokens', DEFAULT_BUDGET)} approximate tokens",
        "",
    ]
    sections = data.get("sections", {})
    for section in SECTION_ORDER:
        lines.append(f"### {SECTION_TITLES[section]}")
        items = sections.get(section, [])
        rendered = 0
        for item in items:
            status = item.get("status", "active")
            if status != "active" and not include_stale:
                continue
            srcs = item.get("source_refs") or []
            src_text = f" (src: {'; '.join(srcs[:2])})" if srcs else ""
            status_text = f" [{status}]" if status != "active" else ""
            lines.append(f"- [{item.get('id')}] {item.get('content', '').strip()}{status_text}{src_text}")
            rendered += 1
        if rendered == 0:
            lines.append("- (empty)")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def map_token_count(data: dict[str, Any]) -> int:
    return estimate_tokens(render_map(data))


def validate_map(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["map must be a JSON object"]
    for key in ["version", "context_id", "budget_tokens", "sections"]:
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if not isinstance(data.get("budget_tokens"), int) or data.get("budget_tokens", 0) <= 0:
        errors.append("budget_tokens must be a positive integer")
    sections = data.get("sections")
    if not isinstance(sections, dict):
        errors.append("sections must be an object")
        return errors
    for section in SECTION_ORDER:
        if section not in sections:
            errors.append(f"missing section: {section}")
        elif not isinstance(sections[section], list):
            errors.append(f"section must be a list: {section}")
    seen: set[str] = set()
    for section, items in sections.items():
        if section not in SECTION_ORDER:
            errors.append(f"unknown section: {section}")
            continue
        if not isinstance(items, list):
            continue
        prefix = SECTION_PREFIXES[section]
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{section}[{idx}] must be an object")
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not re.fullmatch(r"[a-z]{2}-\d{5}", item_id):
                errors.append(f"{section}[{idx}] has invalid id: {item_id}")
            elif not item_id.startswith(prefix + "-"):
                errors.append(f"{item_id} has wrong prefix for section {section}")
            elif item_id in seen:
                errors.append(f"duplicate item id: {item_id}")
            else:
                seen.add(item_id)
            if not isinstance(item.get("content"), str) or not item["content"].strip():
                errors.append(f"{item_id or section + '[' + str(idx) + ']'} content must be non-empty")
            if item.get("status", "active") not in {"active", "stale", "superseded"}:
                errors.append(f"{item_id} has invalid status: {item.get('status')}")
            if not isinstance(item.get("source_refs", []), list):
                errors.append(f"{item_id} source_refs must be a list")
            for numeric in ["confidence", "priority"]:
                value = item.get(numeric)
                if value is not None and not isinstance(value, (int, float)):
                    errors.append(f"{item_id} {numeric} must be numeric")
            confidence = item.get("confidence")
            if isinstance(confidence, (int, float)) and not 0 <= confidence <= 1:
                errors.append(f"{item_id} confidence must be between 0 and 1")
    return errors


def next_id(data: dict[str, Any], section: str) -> str:
    prefix = SECTION_PREFIXES[section]
    highest = 0
    for item in data.get("sections", {}).get(section, []):
        item_id = item.get("id", "")
        match = re.fullmatch(prefix + r"-(\d{5})", item_id)
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{prefix}-{highest + 1:05d}"


def find_item(data: dict[str, Any], item_id: str) -> tuple[str, int, dict[str, Any]] | None:
    for section in SECTION_ORDER:
        for idx, item in enumerate(data.get("sections", {}).get(section, [])):
            if item.get("id") == item_id:
                return section, idx, item
    return None


def normalize_item(data: dict[str, Any], section: str, op: dict[str, Any]) -> dict[str, Any]:
    timestamp = now_iso()
    return {
        "id": next_id(data, section),
        "content": str(op["content"]).strip(),
        "source_refs": list(op.get("source_refs") or []),
        "confidence": float(op.get("confidence", 0.7)),
        "priority": int(op.get("priority", 50)),
        "status": op.get("status", "active"),
        "created_at": timestamp,
        "updated_at": timestamp,
        "last_verified": op.get("last_verified", timestamp),
    }


def apply_operations(data: dict[str, Any], ops_payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    result = copy.deepcopy(data)
    messages: list[str] = []
    operations = ops_payload.get("operations")
    if not isinstance(operations, list):
        raise SystemExit("ops JSON must contain an operations list")

    for op in operations:
        if not isinstance(op, dict):
            raise SystemExit("each operation must be an object")
        op_type = op.get("type")
        if op_type == "ADD":
            section = op.get("section")
            if section not in SECTION_ORDER:
                raise SystemExit(f"ADD has invalid section: {section}")
            if not str(op.get("content", "")).strip():
                raise SystemExit("ADD requires non-empty content")
            item = normalize_item(result, section, op)
            result["sections"][section].append(item)
            messages.append(f"ADD {item['id']}")
        elif op_type == "DELETE":
            item_id = op.get("item_id")
            found = find_item(result, item_id)
            if not found:
                raise SystemExit(f"DELETE item not found: {item_id}")
            section, idx, _ = found
            del result["sections"][section][idx]
            messages.append(f"DELETE {item_id}")
        elif op_type == "REPLACE":
            item_id = op.get("item_id")
            found = find_item(result, item_id)
            if not found:
                raise SystemExit(f"REPLACE item not found: {item_id}")
            section, idx, item = found
            if not str(op.get("content", "")).strip():
                raise SystemExit("REPLACE requires non-empty content")
            updated = copy.deepcopy(item)
            updated["content"] = str(op["content"]).strip()
            if "source_refs" in op:
                updated["source_refs"] = list(op.get("source_refs") or [])
            if "confidence" in op:
                updated["confidence"] = float(op["confidence"])
            if "priority" in op:
                updated["priority"] = int(op["priority"])
            if "status" in op:
                updated["status"] = op["status"]
            updated["updated_at"] = now_iso()
            updated["last_verified"] = op.get("last_verified", updated.get("last_verified", updated["updated_at"]))
            result["sections"][section][idx] = updated
            messages.append(f"REPLACE {item_id}")
        else:
            raise SystemExit(f"unknown operation type: {op_type}")

    result["updated_at"] = now_iso()
    return result, messages


def evict_to_budget(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    result = copy.deepcopy(data)
    budget = int(result.get("budget_tokens", DEFAULT_BUDGET))
    removed: list[str] = []

    def candidates() -> list[tuple[tuple[Any, ...], str, int, dict[str, Any]]]:
        values = []
        for section in SECTION_ORDER:
            for idx, item in enumerate(result.get("sections", {}).get(section, [])):
                status_rank = 0 if item.get("status") in {"stale", "superseded"} else 1
                key = (
                    status_rank,
                    EVICTION_SECTION_ORDER[section],
                    float(item.get("priority", 50)),
                    float(item.get("confidence", 0.7)),
                    item.get("updated_at", ""),
                )
                values.append((key, section, idx, item))
        values.sort(key=lambda row: row[0])
        return values

    while map_token_count(result) > budget:
        options = candidates()
        if not options:
            break
        _, section, idx, item = options[0]
        removed.append(item.get("id", "<unknown>"))
        del result["sections"][section][idx]

    if removed:
        result["updated_at"] = now_iso()
    return result, removed


def unified_render_diff(before: dict[str, Any], after: dict[str, Any]) -> str:
    return "".join(
        difflib.unified_diff(
            render_map(before).splitlines(keepends=True),
            render_map(after).splitlines(keepends=True),
            fromfile="before.md",
            tofile="after.md",
        )
    )


def command_resolve(args: argparse.Namespace) -> int:
    sources = [Path(p) for p in args.source] if args.source else [Path.cwd()]
    context_id = resolve_context_id(sources, args.context_id)
    path = Path(args.map) if args.map else resolve_map_path(context_id, Path(args.map_dir) if args.map_dir else None)
    payload = {
        "context_id": context_id,
        "map_path": str(path.expanduser()),
        "exists": path.expanduser().exists(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def command_init(args: argparse.Namespace) -> int:
    sources = [Path(p) for p in args.source] if args.source else [Path.cwd()]
    context_id = resolve_context_id(sources, args.context_id)
    path = Path(args.map).expanduser() if args.map else resolve_map_path(context_id, Path(args.map_dir).expanduser() if args.map_dir else None)
    if path.exists() and not args.force:
        raise SystemExit(f"map already exists: {path} (use --force to replace)")
    data = new_map(context_id, args.name, args.budget, sources)
    write_json(path, data)
    print(f"created {path}")
    return 0


def command_render(args: argparse.Namespace) -> int:
    data = read_json(Path(args.map).expanduser())
    print(render_map(data, include_stale=args.include_stale), end="")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    path = Path(args.map).expanduser()
    data = read_json(path)
    errors = validate_map(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK {path}")
    print(f"tokens={map_token_count(data)} budget={data.get('budget_tokens')}")
    return 0


def command_diff_ops(args: argparse.Namespace) -> int:
    data = read_json(Path(args.map).expanduser())
    ops = read_json(Path(args.ops).expanduser())
    after, messages = apply_operations(data, ops)
    after, removed = evict_to_budget(after)
    diff = unified_render_diff(data, after)
    print(diff if diff else "(no rendered changes)")
    if messages:
        print("operations:", ", ".join(messages), file=sys.stderr)
    if removed:
        print("evicted:", ", ".join(removed), file=sys.stderr)
    return 0


def command_apply_ops(args: argparse.Namespace) -> int:
    path = Path(args.map).expanduser()
    data = read_json(path)
    ops = read_json(Path(args.ops).expanduser())
    after, messages = apply_operations(data, ops)
    after, removed = evict_to_budget(after)
    errors = validate_map(after)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(unified_render_diff(data, after) or "(no rendered changes)")
        return 0
    write_json(path, after)
    print(f"updated {path}")
    if messages:
        print("operations:", ", ".join(messages))
    if removed:
        print("evicted:", ", ".join(removed))
    print(f"tokens={map_token_count(after)} budget={after.get('budget_tokens')}")
    return 0


def fingerprint_equal(a: dict[str, Any], b: dict[str, Any]) -> bool:
    a_clean = copy.deepcopy(a)
    b_clean = copy.deepcopy(b)
    a_clean.pop("generated_at", None)
    b_clean.pop("generated_at", None)
    return a_clean == b_clean


def command_stale_check(args: argparse.Namespace) -> int:
    path = Path(args.map).expanduser()
    data = read_json(path)
    if args.source:
        sources = [Path(p) for p in args.source]
    else:
        old_sources = data.get("fingerprint", {}).get("sources", [])
        paths = [entry.get("path") for entry in old_sources if entry.get("path")]
        sources = [Path(p) for p in paths] if paths else [Path.cwd()]
    current = fingerprint_sources(sources)
    old = data.get("fingerprint", {})
    if fingerprint_equal(old, current):
        print("OK fingerprint unchanged")
        return 0
    print("STALE fingerprint changed")
    print(json.dumps({"old": old, "current": current}, indent=2, sort_keys=True))
    if args.update_fingerprint:
        data["fingerprint"] = current
        data["updated_at"] = now_iso()
        write_json(path, data)
        print(f"updated fingerprint in {path}")
    return 2


def command_evict(args: argparse.Namespace) -> int:
    path = Path(args.map).expanduser()
    data = read_json(path)
    after, removed = evict_to_budget(data)
    if args.dry_run:
        print(unified_render_diff(data, after) or "(no rendered changes)")
        if removed:
            print("would evict:", ", ".join(removed), file=sys.stderr)
        return 0
    write_json(path, after)
    print(f"tokens={map_token_count(after)} budget={after.get('budget_tokens')}")
    if removed:
        print("evicted:", ", ".join(removed))
    else:
        print("nothing evicted")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage PEEK-style context maps.")
    sub = parser.add_subparsers(dest="command", required=True)

    common_resolve = argparse.ArgumentParser(add_help=False)
    common_resolve.add_argument("--context-id")
    common_resolve.add_argument("--source", action="append", default=[])
    common_resolve.add_argument("--map-dir")
    common_resolve.add_argument("--map")

    p = sub.add_parser("resolve", parents=[common_resolve], help="Resolve context id and default map path.")
    p.set_defaults(func=command_resolve)

    p = sub.add_parser("init", parents=[common_resolve], help="Create a new empty context map.")
    p.add_argument("--name")
    p.add_argument("--budget", type=int, default=DEFAULT_BUDGET)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=command_init)

    p = sub.add_parser("render", help="Render a map as prompt-ready Markdown.")
    p.add_argument("--map", required=True)
    p.add_argument("--include-stale", action="store_true")
    p.set_defaults(func=command_render)

    p = sub.add_parser("show", help="Alias for render.")
    p.add_argument("--map", required=True)
    p.add_argument("--include-stale", action="store_true")
    p.set_defaults(func=command_render)

    p = sub.add_parser("validate", help="Validate map schema and budget.")
    p.add_argument("--map", required=True)
    p.set_defaults(func=command_validate)

    p = sub.add_parser("diff-ops", help="Preview operations as a rendered Markdown diff.")
    p.add_argument("--map", required=True)
    p.add_argument("--ops", required=True)
    p.set_defaults(func=command_diff_ops)

    p = sub.add_parser("apply-ops", help="Apply operations and enforce the token budget.")
    p.add_argument("--map", required=True)
    p.add_argument("--ops", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=command_apply_ops)

    p = sub.add_parser("stale-check", help="Compare stored source fingerprint with current sources.")
    p.add_argument("--map", required=True)
    p.add_argument("--source", action="append", default=[])
    p.add_argument("--update-fingerprint", action="store_true")
    p.set_defaults(func=command_stale_check)

    p = sub.add_parser("evict", help="Enforce the current budget.")
    p.add_argument("--map", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=command_evict)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
