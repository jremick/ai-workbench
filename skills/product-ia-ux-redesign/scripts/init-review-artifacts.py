#!/usr/bin/env python3
"""Create a reusable IA/UX/UI review artifact skeleton."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

PLACEHOLDER_MARKERS = (
    "<",
    "|  |",
    "P0/P1",
    "Repo/live source:",
    "Browser/rendered baseline:",
    "not run",
)


FILES: dict[str, str] = {
    "README.md": """# {product} IA/UX/UI Review Archive

Date: {date}
Product: {product}
Review mode: {review_mode}

## Source State

- Repo/live source:
- Commit or local-state note:
- Browser/rendered baseline:
- Privacy/source boundary:

## Artifact Index

- `00-executive-brief.md`: human summary and recommendation.
- `01-source-register.md`: evidence and source quality log.
- `02-comparable-products-prior-art.md`: comparable product matrix.
- `03-current-ia-inventory.md`: route/page taxonomy and current structure.
- `04-role-task-page-purpose-map.md`: human roles, jobs, and expected destinations.
- `05-page-element-purpose-ledger.md`: purpose and ownership of visible elements.
- `06-audit-findings.md`: ranked IA/UX/UI findings.
- `07-proposed-ia-route-architecture.md`: target taxonomy and route architecture.
- `08-implementation-lanes.md`: safe implementation slices.
- `09-agent-task-briefs.md`: copyable AI-agent implementation packets.
- `10-decisions.md`: decisions, uncertainty, and review triggers.
- `11-acceptance-browser-verification.md`: acceptance and browser verification matrix.
- `evidence/`: screenshots, browser notes, logs, and supporting evidence.

## How To Use This Package

Start with `00-executive-brief.md`, inspect evidence in `01-source-register.md`, then use `08-implementation-lanes.md` and `09-agent-task-briefs.md` for implementation.
""",
    "00-executive-brief.md": """# Executive Brief

## Product Frame

- Product category:
- Primary human roles:
- Agent/system consumers:
- Operator/control surfaces:
- Reader/consumer surfaces:

## Top Findings

| Severity | Finding | Why it matters | First fix |
| --- | --- | --- | --- |
| P0/P1 |  |  |  |

## Target Direction

- IA model:
- First implementation lane:
- Verification posture:

## Open Questions

-
""",
    "01-source-register.md": """# Source Register

| ID | Type | Source | Date accessed | Evidence captured | Trust level | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | Product docs |  | {date} |  | high |  |

## Source Boundary

- Private sources allowed:
- Public/demo-only constraints:
- Secrets/auth handling:
- Unverified sources:
""",
    "02-comparable-products-prior-art.md": """# Comparable Products And Prior Art

| Product/source | Why comparable | Official evidence | Screenshot/evidence ID | Pattern to borrow | Pattern not to borrow | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Synthesis

- Patterns that generalize:
- Category-specific caveats:
- Sources needing refresh:
""",
    "03-current-ia-inventory.md": """# Current IA Inventory

| Route/Page | Zone | Intended job | Visible contents | Primary actions | Loading/data behavior | Evidence | Friction |
| --- | --- | --- | --- | --- | --- | --- | --- |
{route_rows}

## Route Aliases And Compatibility

-

## Object Model Observations

-
""",
    "04-role-task-page-purpose-map.md": """# Role Task Page Purpose Map

| Role | Job/task | Expected destination | Current destination | Works? | Friction | Proposed destination |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Operator Versus Reader Boundary

- Operator/control jobs:
- Reader/consumer jobs:
- Mixed-surface risks:
""",
    "05-page-element-purpose-ledger.md": """# Page Element Purpose Ledger

| Page | Element/control | Purpose | Acts on | Target user | State dependency | Keep/move/remove | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Implementation Plumbing Exposed To Users

-

## Controls That Should Move Closer To Objects

-
""",
    "06-audit-findings.md": """# Audit Findings

Severity guide: P0 blocks core work or creates safety risk; P1 causes major recurring confusion; P2 has workaround; P3 is polish or future fit.

| Severity | Finding | Evidence | Framework/source | Human impact | Fix direction | Acceptance check | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 |  |  |  |  |  |  |  |

## Findings Narrative

### P0

### P1

### P2

### P3
""",
    "07-proposed-ia-route-architecture.md": """# Proposed IA And Route Architecture

## Principles

-

## Target Taxonomy

| Zone | Route/page | Human purpose | Primary objects/actions | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Object Detail Model

- Overview:
- Content:
- Metadata:
- Permissions:
- Versions:
- Distribution:
- Activity:
- Settings:

## Aliases And Migration

-
""",
    "08-implementation-lanes.md": """# Implementation Lanes

| Lane | Scope | User value | Files/areas | Risk | Tests | Browser checks | Rollback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |

## Stop Rules

-

## First Safe Lane

- Goal:
- In scope:
- Out of scope:
- Acceptance:
""",
    "09-agent-task-briefs.md": """# AI-Agent Task Briefs

## Task: <title>

### Goal

### Source Of Truth

-

### Scope

- In:
- Out:

### Required Behavior

-

### Constraints

-

### Verification

- Commands:
- Browser walkthrough:
- Evidence:

### Stop Rules

-
""",
    "10-decisions.md": """# Decisions

## {date}: <decision>

Decision:

Rationale:

Alternatives considered:

-

Uncertainty:

Review trigger:
""",
    "11-acceptance-browser-verification.md": """# Acceptance And Browser Verification

## Acceptance Criteria

-

## Browser Verification Matrix

| Scenario | Role | Route/page | Viewport | Expected evidence | Status | Screenshot/log |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | not run |  |

## Accessibility Checks

- Keyboard navigation:
- Focus visibility:
- Headings and labels:
- Status messages:
- Contrast:
- Target size:

## Residual Risk

-
""",
    "evidence/README.md": """# Evidence Index

## Screenshots

| ID | File | Route/page | Viewport | Date | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | {date} |  |

## Command Or Browser Notes

- `browser-notes.md`
""",
    "evidence/browser-notes.md": """# Browser Notes

| Time | Route/page | Viewport | Action | Observation | Evidence |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
""",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output directory for the artifact package.")
    parser.add_argument("--product", default="Product", help="Product or interface name.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Review date, default: today.")
    parser.add_argument(
        "--review-mode",
        choices=("browser-verified", "file-grounded", "prompt-only"),
        default="file-grounded",
        help="Evidence mode to record in the archive README.",
    )
    parser.add_argument(
        "--routes",
        default="",
        help="Comma-separated route/page names to seed into the current IA inventory.",
    )
    parser.add_argument(
        "--check-placeholders",
        action="store_true",
        help="Print markdown lines that still look like placeholders after generation.",
    )
    parser.add_argument(
        "--fail-on-placeholders",
        action="store_true",
        help="Exit non-zero when placeholder-like lines remain. Implies --check-placeholders.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing skeleton files.")
    return parser.parse_args()


def split_routes(routes: str) -> list[str]:
    return [route.strip() for route in routes.split(",") if route.strip()]


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|")


def render_route_rows(routes: list[str]) -> str:
    if not routes:
        return "|  |  |  |  |  |  |  |  |"
    return "\n".join(
        f"| {escape_cell(route)} |  |  |  |  |  | prompt-provided |  |"
        for route in routes
    )


def scan_placeholders(root: Path) -> list[tuple[Path, int, str]]:
    matches: list[tuple[Path, int, str]] = []
    for path in sorted(root.rglob("*.md")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if any(marker in stripped for marker in PLACEHOLDER_MARKERS):
                matches.append((path, line_number, stripped))
    return matches


def main() -> int:
    args = parse_args()
    root = Path(args.out).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "evidence" / "screenshots").mkdir(parents=True, exist_ok=True)

    route_rows = render_route_rows(split_routes(args.routes))
    written: list[Path] = []
    skipped: list[Path] = []
    for relative, template in FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.force:
            skipped.append(path)
            continue
        path.write_text(
            template.format(
                product=args.product,
                date=args.date,
                review_mode=args.review_mode,
                route_rows=route_rows,
            ),
            encoding="utf-8",
        )
        written.append(path)

    print(f"artifact_root={root}")
    print(f"written={len(written)}")
    print(f"skipped={len(skipped)}")
    for path in written:
        print(f"+ {path.relative_to(root)}")
    for path in skipped:
        print(f"= {path.relative_to(root)}")
    if args.check_placeholders or args.fail_on_placeholders:
        matches = scan_placeholders(root)
        print(f"placeholder_like_lines={len(matches)}")
        for path, line_number, line in matches:
            print(f"! {path.relative_to(root)}:{line_number}: {line}")
        if matches and args.fail_on_placeholders:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
