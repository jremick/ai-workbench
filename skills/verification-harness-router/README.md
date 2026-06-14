# Verification Harness Router

`verification-harness-router` helps agents choose the right proof path for a claim.

It is useful when "looks good" is not enough: public artifact packaging, launch readiness, skill evals, UI verification, code changes, live-system checks, and sub-agent review.

## What It Does

This skill routes a claim to the smallest credible evidence path: tests, evals, smoke checks, screenshots, read-backs, scans, sidecar critique, user review, or a combination when needed.

## What It Does Not Do

It does not implement every verifier, replace test code, or treat model review as proof. It names the route and the minimum evidence needed before a completion claim is credible.

## Install

Copy this directory into your agent skill directory:

```text
skills/verification-harness-router/
```

The minimum install is `SKILL.md`. Keep `evals/cases.json` for example prompts.

## Try It

```text
Use verification-harness-router to decide what checks prove this skill package is public-ready.
```

## What It Produces

- the exact claim being verified
- the smallest credible evidence route
- required versus optional checks
- failure behavior
- residual risk

## Model Selection

This skill does not initiate model calls. Sidecar model review can help critique a plan, eval case, or public-facing claim, but it is not enough proof for code behavior, public safety, secret handling, or live system health.

## Side Effects

Running this skill has no required side effects. The checks it recommends may run commands, inspect files, call services, or request human review depending on the claim and the caller's environment.

## Related Skills

- `harness-composer` defines parent and child harness claims that need evidence.
- `nested-agent-orchestrator` produces child outputs that still require parent verification.
- `context-boundary-designer` defines what evidence can be shared, stored, or published.

## Public Readiness

The public version treats sidecar model review as useful critique, not proof. It asks for deterministic checks, read-backs, evals, screenshots, or user review depending on the claim.
