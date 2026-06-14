# Harness Composer

`harness-composer` helps an agent turn a broad project into a parent harness and a small set of child harnesses.

It is useful when a normal plan would hide too much complexity: public artifact packaging, multi-agent work, research plus implementation, eval-heavy projects, or nested agentic workflows.

## What It Does

This skill produces a parent harness and child harness map: purpose, inputs, outputs, evidence, dependencies, model roles, and the first execution path.

## What It Does Not Do

It does not execute the child harnesses, spawn agents, run tests, or publish artifacts. The calling agent still owns execution, integration, and final verification.

## Install

Copy this directory into your agent skill directory:

```text
skills/harness-composer/
```

The minimum install is `SKILL.md`. Keep `evals/cases.json` when you want example test prompts.

## Try It

```text
Use harness-composer to break this agentic project into child harnesses. I want reusable public artifacts, not private process notes.
```

## What It Produces

A good output names:

- the parent outcome
- child harnesses with independent proof paths
- dependencies and integration gates
- which model or agent roles are useful
- what context each sidecar may receive
- the first execution path

## What It Prevents

- treating a large project as one vague task
- splitting work into sub-agents without clear acceptance checks
- publishing disconnected artifacts that do not serve a parent goal
- letting a sidecar model become the hidden source of truth

## Model Selection

This skill does not initiate model calls. If a caller uses a sidecar model to critique or compare the harness, the sidecar should receive only bounded public-safe context and return review input. The parent agent decides what to accept.

## Side Effects

Running this skill has no required filesystem, network, or external model side effects. Outputs are advisory unless the parent agent writes them into a project artifact.

## Related Skills

- `context-boundary-designer` decides what context child harnesses or sidecars may receive.
- `nested-agent-orchestrator` applies the harness when sub-agents are actually used.
- `verification-harness-router` chooses proof paths for parent and child claims.

## Public Readiness

The public version is vendor-neutral. It uses the public pattern of explicit model roles, bounded sidecar context, parent-owned integration, and deterministic validation without shipping private router scripts or local environment assumptions.
