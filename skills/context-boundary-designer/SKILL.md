---
name: context-boundary-designer
description: Use when an agentic task needs clear boundaries for what context belongs in the parent prompt, child agents, sidecar models, memory, docs, evals, public artifacts, or final answers. This skill prevents context bloat and private-context leakage by classifying sources, sensitivity, provenance, retention, and allowed use before work is delegated or published.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# Context Boundary Designer

Design what context goes where before an agent shares, stores, delegates, summarizes, or publishes it.

Context is not free. Too little context causes weak work. Too much context creates leakage, confusion, stale assumptions, and bloated prompts.

## Core Rule

Give each actor and artifact the minimum context needed to do its job, with clear provenance and sensitivity boundaries.

## Use When

Use this skill when:

- delegating to sub-agents or sidecar models
- preparing public artifacts from private or messy source work
- deciding what belongs in memory, docs, evals, examples, or final answers
- designing prompt packets for specialist agents
- handling raw logs, transcripts, local paths, private project details, or secrets
- reducing context bloat in a long-running task
- deciding whether a fact is stable enough to reuse without live verification

Do not use it for simple tasks where all context is already public, small, and directly relevant.

## Boundary Workflow

1. Inventory context classes.
   - User request
   - Source files or documents
   - Live system state
   - Prior decisions
   - Memory or notes
   - Tool outputs
   - Secrets or credentials
   - Private examples
   - Public examples

2. Classify sensitivity and stability.
   - Public, internal, private, secret, regulated, or unknown.
   - Stable, likely stale, live-only, or one-off.
   - Source-backed, inferred, user preference, or model-generated.

3. Assign context destinations.
   - Parent agent: source of truth, constraints, integration state, and verification obligations.
   - Child agent: only the scoped facts needed for its contract.
   - Sidecar model: minimal read-only context for critique, research, or comparison.
   - Memory: durable, source-backed lessons that should recur.
   - Docs: stable guidance and public-safe examples.
   - Evals: sanitized fixtures that can fail when behavior regresses.
   - Final answer: what the user needs to understand the outcome and remaining risk.

4. Redact or transform context.
   - Replace private names, local paths, hostnames, secrets, raw logs, and unpublished details with generic descriptions.
   - Keep behavior, constraints, and reasoning intact when sanitizing examples.
   - Preserve provenance for facts that affect decisions.

5. Define update and disposal behavior.
   - What should become durable?
   - What should stay in the current task only?
   - What must never be stored or published?
   - What should be rechecked before future reuse?

## Output Format

```markdown
## Context Boundary
Source of truth:
Public-safe goal:
Forbidden context:

## Context Allocation
| Context Class | Sensitivity | Destination | Transformation | Verification |
| --- | --- | --- | --- | --- |

## Delegation Packet
<what child or sidecar agents may receive>

## Durable Record
<what belongs in memory, docs, evals, or no durable record>

## Stop Conditions
<what should pause before sharing, storing, or publishing>
```

## Sidecar Model Rules

When using a sidecar model:

- state the sidecar's role before sending context
- use read-only context unless the user explicitly asks for edits
- omit secrets, private raw logs, and unrelated personal or internal details
- ask for bounded output: critique, risks, alternatives, or verification suggestions
- have the parent agent verify and integrate the result

If a sidecar needs sensitive context to be useful, pause and ask whether that route is appropriate.

## Public Artifact Rules

For public packages:

- publish the pattern, not the private incident
- use fake or sanitized examples
- remove local paths, hostnames, private names, raw transcripts, and secret references
- include a validator or review checklist for sensitive patterns
- state any proof summary without including raw private evidence

## Anti-Patterns

Flag these:

- sending full chat history to a child agent by default
- storing raw transcripts as memory
- using private examples in public evals
- dropping provenance while preserving claims
- assuming stale memory is current live state
- redacting so aggressively that the example no longer tests the real behavior

## Verification

Before sharing, storing, delegating, or publishing context:

- each context class has a destination or exclusion
- sensitive and stale context are marked
- child and sidecar packets are scoped
- public examples are sanitized but still meaningful
- durable records include only reusable, source-backed knowledge
- final answers disclose material uncertainty or skipped verification
