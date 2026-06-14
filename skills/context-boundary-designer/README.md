# Context Boundary Designer

`context-boundary-designer` helps agents decide what context belongs in parent prompts, child agents, sidecar models, memory, docs, evals, and public artifacts.

It is useful when context is powerful but risky: nested agents, long-running tasks, public packaging, memory design, or any workflow that touches private source material.

## What It Does

This skill classifies context by sensitivity, stability, provenance, and destination. It decides what belongs with the parent, child agents, sidecar models, memory, docs, evals, public artifacts, and final answers.

## What It Does Not Do

It does not spawn agents, run sidecar models, write memory, publish artifacts, or verify final outputs. It defines boundaries that the parent agent must apply.

## Install

Copy this directory into your agent skill directory:

```text
skills/context-boundary-designer/
```

The minimum install is `SKILL.md`. Keep `evals/cases.json` for example prompts.

## Try It

```text
Use context-boundary-designer before delegating this task. Decide what the parent keeps, what child agents receive, what can be public, and what must stay out.
```

## What It Produces

- a context inventory
- sensitivity and stability classes
- destination rules for parent, child, sidecar, memory, docs, evals, and final answer
- redaction or transformation rules
- stop conditions before sharing or publishing

## Model Selection

This skill does not initiate model calls. If a sidecar model is used, send only the scoped delegation packet produced by this skill. The sidecar should not receive secrets, raw private logs, unrelated local details, or context that cannot be safely shared.

## Side Effects

Running this skill has no required side effects. Side effects occur only if the parent agent later stores memory, writes docs, creates evals, delegates work, or publishes artifacts using the boundary plan.

## Related Skills

- `harness-composer` uses the boundary plan when defining child harness inputs.
- `nested-agent-orchestrator` uses the delegation packet when spawning child agents.
- `verification-harness-router` checks whether context handling and public packaging claims are proven.

## Public Readiness

The public version focuses on reusable boundaries. It does not include private memory files, raw sessions, local paths, or private examples.
