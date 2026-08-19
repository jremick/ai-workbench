---
name: decision-log
description: Capture and track decisions, rationale, and consequences. Use when a user asks to document decisions, alternatives, or to maintain a decision log.
license: Apache-2.0
---

# Decision Log

Version: 1.1.0
Last updated: 2026-05-28

Use this skill when the work makes, depends on, revisits, supersedes, or needs to report a material decision.

Resolve the decision-log path from the current project instructions. Prefer a repository-local `DECISIONS.md` when decisions belong with the project. For cross-project decisions, ask the user for the intended durable location instead of inventing or assuming one.

## Capture Criteria

Log a decision when it affects scope, source of truth, ownership, stakeholder communication, documentation, automation, tracking, security posture, architecture, spending, reusable instructions, or future operating behavior.

Do not log routine tactical choices, command attempts, or weak observations. Keep reusable lessons separate from individual decisions.

## Workflow

1. Identify the decision and whether it is proposed, accepted, superseded, or due for revisit.
2. Capture the context, owner, affected scope, and stakeholders.
3. List alternatives considered or rejected.
4. Record rationale, evidence, constraints, and tradeoffs.
5. Note consequences, follow-ups, reporting needs, documentation updates, notifications, tracking links, and review date or cadence.
6. Record `Accounted for` so later checks can tell whether the decision has been used in reports, communicated, documented, tracked, automated, or intentionally deferred.
7. Add a `Memory routing` note only when the host has an explicit, user-approved durable-memory workflow.

## Output Template

```markdown
### D-YYYYMMDD-NNN - Decision title

- `Date`: YYYY-MM-DD
- `Status`: Proposed | Accepted | Superseded | Revisit
- `Owner`: Person or system accountable for follow-through
- `Scope`: Global, project, work system, or artifact affected
- `Decision`: The choice made
- `Why`: Rationale, evidence, constraints, or tradeoffs
- `Alternatives`: Plausible options considered or rejected
- `Follow-ups`: Notifications, reports, docs, tracking items, automations, or checks needed
- `Accounted for`: Where the decision has already been used, reported, notified, documented, or tracked
- `Memory routing`: None | Added through approved memory workflow | Needs explicit user approval
```

## Scheduled Review

When asked to check the decision log, resolve the active log from project instructions and review it for:
- open follow-ups
- decisions with empty or stale `Accounted for`
- decisions that should be reflected in reports, notifications, documentation, tracking systems, automations, or approved memory
- decisions contradicted by newer live source-of-truth evidence

Report only actionable gaps unless the user asks for a full ledger summary.
