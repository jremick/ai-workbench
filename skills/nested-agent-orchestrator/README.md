# Nested Agent Orchestrator

`nested-agent-orchestrator` helps decide when to use sub-agents or sidecar models, and how to keep them bounded.

It is for agentic work where parallel exploration, independent review, or delegated implementation could help, but only if the parent agent keeps ownership of integration and verification.

## What It Does

This skill creates delegation contracts: which agents should run, what each may see, what tools or write permissions they have, what they must return, and how the parent will verify their output.

## What It Does Not Do

It does not require delegation. It does not make child agents authoritative. It does not replace context design, harness composition, or final verification.

## Install

Copy this directory into your agent skill directory:

```text
skills/nested-agent-orchestrator/
```

The minimum install is `SKILL.md`. Keep `evals/cases.json` for example prompts.

## Try It

```text
Use nested-agent-orchestrator to decide whether this repo audit should be split across sub-agents. Define the child contracts and how the parent should verify them.
```

## What It Produces

- a go or no-go decision for delegation
- child agent contracts
- context and permission boundaries
- model-role choices for sidecar work
- integration and verification gates

## Model Selection

This skill does not initiate model calls by itself. When the caller has a model router or sidecar capability, use it explicitly: name the role, context, tool mode, cost or auth boundary if known, and expected output. Read-only sidecars are the default.

## Side Effects

Running this skill has no required side effects. Side effects only occur if the parent agent actually spawns agents, grants tools, or applies edits under the produced delegation plan.

## Related Skills

- `context-boundary-designer` should run first when context is sensitive or easy to over-share.
- `harness-composer` should run first when delegation is part of a larger parent/child harness structure.
- `verification-harness-router` should run after child outputs are available.

## Public Readiness

The public version avoids private tool names and local routing assumptions. It keeps the reusable pattern: explicit model route, read-only sidecars by default, parent-owned integration, and evidence-backed final claims.
