---
name: harness-composer
description: Use when a user starts, reviews, or rescopes a complex agentic project that needs multiple nested harnesses, workstreams, sub-agents, eval loops, or public artifact tracks. This skill composes a parent harness and child harnesses with clear dependencies, success evidence, integration gates, model-role choices, and stop conditions before execution begins.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# Harness Composer

Compose a complex project into a parent harness plus smaller child harnesses that can be executed, verified, and integrated without losing the real goal.

Use this skill one level above ordinary planning. The output is not a long project plan. It is the operating shape that keeps nested work bounded and testable.

## Core Rule

Create a child harness only when it has its own purpose, owner, source of truth, success evidence, and integration point.

If a child harness cannot be verified independently, it is probably a task inside another harness, not a separate harness.

## Use When

Use this skill when the user asks to:

- break a large agentic project into workstreams
- design a meta-harness or nested harness
- coordinate multiple skills, agents, tools, repos, or deliverables
- turn a broad initiative into publishable or reusable artifacts
- separate research, prototype, implementation, verification, and packaging loops
- decide which parts should be delegated, evaluated, documented, or stopped

Do not use it for a small edit, a simple one-shot plan, or a single harness that is already clear.

## Composition Workflow

1. Name the parent outcome.
   - State what the overall project must make true.
   - Name the audience and source of truth.
   - Separate user-visible success from internal activity.

2. Identify the natural child boundaries.
   - Split by independent uncertainty, artifact, system, skill, owner, risk, or verification method.
   - Avoid splitting by arbitrary steps when the work needs one continuous judgment loop.

3. Define each child harness.
   - Intent: what the child is responsible for.
   - Inputs: sources and assumptions it may use.
   - Outputs: artifacts, decisions, patches, reports, evals, or proofs.
   - Evidence: what proves the child succeeded.
   - Stop condition: what should pause that child.

4. Map dependencies and integration gates.
   - Name which child outputs unblock other children.
   - Define how the parent accepts, rejects, or revises each child output.
   - Keep integration in the parent harness unless the child has an explicit integration contract.

5. Select model roles and delegation boundaries.
   - Use the default fully tooled parent model for orchestration, writes, integration, and final claims.
   - Use sidecar models only for bounded critique, research, alternative design, or independent verification.
   - Make every sidecar route explicit: role, context allowed, tool access, write permission, expected output, and verification.
   - Prefer read-only sidecars. Use edit-capable sidecars only when the user explicitly asks and the parent will review the diff.

6. Choose the smallest verification loop.
   - Each child gets proof appropriate to its output.
   - The parent gets integration proof that the child outputs still serve the parent outcome.

## Output Format

```markdown
## Parent Harness
Intent:
Good means:
Evidence:
Source of truth:
Stop conditions:

## Child Harnesses
| Child | Purpose | Inputs | Output | Evidence | Stop Condition |
| --- | --- | --- | --- | --- | --- |

## Dependencies
<dependency order, parallel work, and integration gates>

## Model And Agent Roles
<parent model role, sidecar roles if useful, and what context each may receive>

## First Execution Path
<the first child to execute, why it goes first, and what proof must exist before proceeding>
```

Compress the format when the project is small. Expand only when it changes execution quality.

## Public Artifact Guidance

When composing work for a public package:

- keep private staging, raw notes, and source inventories outside the public artifact
- require sanitized examples and explicit license decisions
- include a validation or smoke check for every reusable artifact
- treat sidecar model suggestions as review input, not as publication proof
- record why each child artifact deserves to exist instead of adding a generic skill or doc

## Anti-Patterns

Flag and correct:

- child harnesses that are just task lists
- delegation without independent success evidence
- sidecar models that receive unnecessary private context
- parent harnesses that never define an integration gate
- public packages that copy private workflow details instead of extracting the reusable pattern
- verification that proves a child artifact exists but not that it helps the parent outcome

## Verification

Before moving from composition into execution, confirm:

- the parent outcome is concrete enough to verify
- every child harness has a bounded output and proof path
- dependencies and parallelizable work are visible
- model and sidecar roles are explicit
- private, secret, and local-runtime context is outside public or delegated packets
- the first execution path is clear and reversible
