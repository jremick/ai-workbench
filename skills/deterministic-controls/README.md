# Deterministic Controls

`deterministic-controls` helps decide what should be enforced by code, schemas, state machines, policy gates, tests, and evals instead of model wording.

It is for serious agent and AI workflow design: tool permissions, routing, structured output, retries, side effects, auditability, release gates, and safety boundaries.

## Install

Copy this directory into your agent skill directory:

```text
skills/deterministic-controls/
```

Keep the `scripts/`, `evals/`, and `references/` folders if you want the validation harness.

## Try It

```text
Use deterministic-controls to review this agent workflow. It parses model JSON, writes files, and can call external APIs. Which controls belong in code or tests?
```

## Run The Eval

```bash
cd skills/deterministic-controls
python3 scripts/run_evals.py
```

Expected result:

```json
{
  "passed": true
}
```

## Public Readiness

This public package includes the portable eval runner, public-safe eval cases, and a control catalog. It does not include private logs, customer examples, or local environment assumptions.
