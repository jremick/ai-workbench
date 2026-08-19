---
name: adhd-helper
description: "Use for personal adult ADHD-friendly Codex workflows: broad, ambiguous, multi-step, interruptible, context-heavy, review-heavy, or parallel-agent coding tasks needing visible state, open-loop control, bounded exploration, verification, and restartable progress. Avoid for trivial one-file edits unless explicitly requested."
license: Apache-2.0
---

# ADHD Helper

Version: 1.0.0
Last updated: 2026-06-16

Purpose: reduce working-memory load, scope creep, open loops, and restart friction during Codex coding work.

This is a workflow scaffold, not medical advice.

## When to use

Use for tasks that are ambiguous, multi-step, interruption-prone, risky, review-heavy, context-heavy, or likely to touch multiple files.

## When not to use

Do not use for tiny obvious edits unless explicitly requested.

## Default stance

- Prefer one active implementation lane.
- Make small, reviewable changes.
- Define done before changing code.
- Verify with the narrowest relevant check.
- Leave a restart point if not fully complete.
- Do not spawn subagents unless explicitly requested.

## Task card

For non-trivial tasks, start or update:

```text
Goal:
Assumptions:
Non-goals:
Acceptance checks:
Active lane:
Next safe action:
```

## Session state

For medium/long tasks, maintain `.codex/adhd-helper/session.md`:

```text
Goal:
Current state:
Files inspected:
Files changed:
Decisions:
Active lane:
Parked lanes:
Open loops:
Acceptance checks:
Next safe action:
```

Keep this file local unless explicitly asked to commit it. If creating repo-local session state, ensure `.codex/adhd-helper/` is gitignored first.

## Work loop

1. Inspect only what is needed for the active lane.
2. State the next action briefly.
3. Make the smallest useful change.
4. Run the narrowest relevant verification.
5. Update session state when the task is medium/long.
6. Continue, close, or park.

## Exploration control

If new ideas appear, do not chase them immediately. Park them:

| Lane | Why parked | Resume condition | Kill condition |
|---|---|---|---|

Default limits:
- 1 active implementation lane.
- 1 active exploration lane.
- 3 parked lanes.

## Subagents

Do not use subagents unless explicitly requested.

If requested:
- cap at 3 unless explicitly overridden;
- give each one narrow scope;
- require finding, evidence, risk, recommended action;
- synthesize into one table;
- close or park all threads before final response.

## Verification

Before saying work is complete:
- run relevant tests/checks where practical;
- report exact commands;
- if checks are not run, say why;
- if checks fail, report the failure and next safe action.

## Final response contract

```text
Changed:
- ...

Verified:
- ...

Open loops:
- None

Next safe action:
- ...
```

If incomplete:

```text
Open loops:
- [risk] [next action]
```

## Avoid

- Large rewrites when a small patch works.
- Continuing exploration after enough evidence exists.
- Saying "done" without verification.
- Leaving context only in chat.
- Asking me to choose among many options without a recommendation.
- Adding process ceremony to tiny tasks.
