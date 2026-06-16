# Harness-First Project Design: Simple Guide

Version: 1.1.2
Last updated: 2026-06-17

## What It Is

Harness-First Project Design is a way to start substantial AI or software work.

Instead of asking an agent to start building immediately, ask it to design the working setup first:

- what the real goal is,
- what questions must be answered before a good start is possible,
- what source of truth matters,
- what existing skills or workflows should support the work,
- what context should and should not be loaded,
- what minimum project scaffold is needed,
- what the first execution lane is,
- what evidence will prove progress,
- what learning should be reused next time.

## When To Use It

Use it when work is:

- broad or ambiguous,
- likely to span multiple sessions,
- sensitive to privacy, auth, quality, or live systems,
- a new project, repo, app, workflow, skill, automation, or research effort,
- important enough that a wrong start would waste time.

Do not use the full method for tiny edits, one-off commands, or obvious local changes.

## How To Prompt It

```text
Use harness-first-project-coach before implementation.

Highest practical goal:
<one paragraph>

Context and source of truth:
<repo, document, live system, brief, or constraints>

Musts and must-nots:
<privacy, auth, time, style, quality, scope, non-goals>

Please:
1. Ask only the clarifying questions that materially change the harness.
2. Reframe the goal at the right altitude.
3. Identify the source of truth.
4. Choose any existing skills or workflows that should support this.
5. Design the minimum project harness.
6. Pick the first execution lane.
7. Define verification evidence and stop conditions.
```

## What Good Output Looks Like

```markdown
**Harness-First Goal**
- Intent:
- Good means:
- Evidence:
- Risks:
- Work mode:
- Clarifying Q&A:
- Support skills:
- Minimum harness:
- First lane:

**Plan**
1. ...

**Stop Conditions**
- ...
```

## Team Use Pattern

1. User gives the highest practical goal and constraints.
2. Agent asks focused Q&A or states safe assumptions.
3. Agent investigates the source of truth.
4. Agent maps the support skills or workflows that fit.
5. Agent reframes the work before implementation.
6. Human reviews the proposed harness and first lane.
7. Agent executes one lane.
8. Evidence decides whether to continue, revise, or stop.
9. Reusable lessons become docs, skills, tests, scripts, or decision records.

## Quick Test

The method is working if the answer makes the project easier to execute, easier to verify, and harder to drift.
