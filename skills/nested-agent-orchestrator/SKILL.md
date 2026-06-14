---
name: nested-agent-orchestrator
description: Use when a task may benefit from sub-agents, sidecar models, parallel reviewers, delegated implementation, independent verification, or nested agent workflows. This skill decides whether to delegate, defines each agent contract, limits context and permissions, and keeps the parent agent responsible for integration, verification, and final claims.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# Nested Agent Orchestrator

Use nested agents deliberately. Delegation helps when it creates independent progress, perspective, or verification. It hurts when it duplicates work, leaks context, or blurs responsibility.

## Core Rule

The parent agent owns the task. Child agents provide bounded outputs. They do not become the source of truth, the final integrator, or the final verifier unless the parent explicitly accepts and verifies their work.

## Use When

Use this skill when:

- a task has multiple independent questions or workstreams
- broad codebase or document exploration can happen in parallel
- one agent can implement while another reviews or tests
- a sidecar model can provide a bounded critique or alternative design
- independent verification would reduce risk
- context-heavy synthesis would benefit from scoped summaries

Do not delegate when the task is trivial, tightly coupled, blocked on one next decision, or too ambiguous to bound safely.

## Delegation Workflow

1. Decide whether delegation helps.
   - Name the speed, depth, verification, or context benefit.
   - If the next step depends on the result, delegation may not improve the critical path.

2. Define the parent contract.
   - Parent owns source of truth, final plan, writes, integration, verification, and final answer.
   - Parent decides which child outputs are accepted, revised, ignored, or escalated.

3. Create child agent contracts.
   - Task: one bounded objective.
   - Context: only what the child needs.
   - Tools: read-only, inspect, edit, browser, or no tools.
   - Write ownership: exact files or "no writes".
   - Output: expected format and evidence.
   - Stop condition: what the child must not guess through.

4. Select model roles.
   - Default to the fully tooled parent model for integration and user-facing claims.
   - Use sidecar models for critique, research, comparison, or isolated execution.
   - Prefer read-only mode for sidecars unless the user explicitly asks for edits.
   - If a model route is unavailable or ambiguous, do not silently substitute a different cost, tool, or auth path.

5. Run parent work in parallel where possible.
   - Do not wait if the parent can safely advance on non-overlapping work.
   - Do wait before decisions that genuinely depend on child output.

6. Integrate with evidence.
   - Review child output against the contract.
   - Check claims before using them.
   - Verify patches, docs, evals, or findings through local tests, diffs, screenshots, read-backs, or another appropriate proof path.

## Agent Contract Template

```markdown
## Delegation Plan
Parent source of truth:
Parent responsibilities:

| Agent | Objective | Context Allowed | Tool Mode | Write Ownership | Expected Output | Stop Condition |
| --- | --- | --- | --- | --- | --- | --- |

## Integration Gate
<how the parent will accept, reject, or revise each child output>

## Verification
<checks the parent will run before claiming completion>
```

## Output Rules For Child Agents

Ask child agents to return:

- findings first when reviewing
- changed files and verification when editing
- sources and dates when researching
- assumptions and uncertainty when synthesizing
- exact blockers instead of broad "needs clarification" language

For public or sensitive work, tell child agents explicitly not to include private names, secret references, local paths, raw logs, or unpublished internal details in outputs.

## Anti-Patterns

Flag these:

- delegating because "more agents" sounds better
- giving every child the full context by default
- allowing multiple agents to edit the same files without ownership
- accepting a child agent's claim without verification
- using an expensive or external sidecar route without making the route explicit
- hiding disagreement between child agents in the final answer

## Verification

Before claiming a nested-agent workflow is complete:

- every child had a bounded contract
- context and permissions were limited to the task
- any sidecar model route was explicit
- child outputs were reviewed before integration
- local deterministic checks were run where possible
- unresolved disagreement or uncertainty is visible
- final claims come from parent verification, not only child confidence
