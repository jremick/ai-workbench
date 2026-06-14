---
name: deterministic-controls
description: Identify when agent, harness, skill, workflow, or AI system behavior needs deterministic controls instead of model judgment, and recommend production-grade implementation approaches. Use when designing, reviewing, or hardening agentic workflows, tool harnesses, skills, evals, routing, parsing, validation, permissions, retries, state machines, audit logs, CI gates, policy enforcement, or AI reliability controls.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# Deterministic Controls

Use this skill to decide which parts of an agentic system should be implemented as code, configuration, schemas, tests, or runtime guardrails instead of prompt guidance.

The goal is not to remove model judgment. The goal is to put deterministic controls around the boundaries where correctness, safety, repeatability, auditability, or cost control must hold.

## Core Rule

Implement deterministic controls when a failure would be materially worse than an imperfect answer, a retry, or a clarifying question.

Let the model handle semantic judgment, synthesis, ranking, and explanation. Make code handle exact parsing, routing, validation, permissions, state transitions, side effects, retry policy, and pass/fail evaluation.

Use a hybrid pattern:

- The model proposes, summarizes, or chooses among ambiguous options.
- Deterministic code validates the proposal before action.
- A harness or policy gate decides whether to execute, ask, retry, redact, escalate, or stop.
- Tests and evals prove the control still works as prompts, tools, and models change.

## Decision Workflow

1. Identify the boundary: user input, model output, tool call, file write, network call, approval, state change, eval result, or final answer.
2. Classify the risk: correctness, security, privacy, cost, compliance, availability, reproducibility, user trust, or operational burden.
3. Decide whether deterministic enforcement is required:
   - Required: exact format, irreversible or external side effects, secrets, auth, money, legal/compliance, production state, durable records, safety policy, concurrency, routing, or eval pass/fail.
   - Recommended: repeated workflow, brittle prompt-only instruction, handoff between systems, noisy model output, user-visible quality gate, or expensive retry loop.
   - Usually unnecessary: low-risk brainstorming, drafting, summarization, exploratory analysis, design alternatives, or tasks where a human will review before action.
4. Choose the narrowest control that can enforce the invariant at the right boundary.
5. Define the verification: unit tests, schema tests, golden cases, property checks, dry runs, audit-log assertions, or eval cases.
6. Document the residual model judgment that remains and the stop condition when the control cannot decide.

## Control Selection

| Need | Best Practice Approach |
| --- | --- |
| Exact structured output | JSON Schema, Zod, Pydantic, TypeScript types, protobuf, or typed dataclasses with parse-and-repair limits |
| Routing between tools or workflows | Explicit router table, allowlist, priority order, confidence threshold, and fallback-to-ask behavior |
| Permissions and side effects | Capability allowlist, approval gate, dry-run mode, path sandbox, command wrapper, and deny-by-default policy |
| Multi-step agent state | Explicit state machine, durable checkpoint, idempotency key, resumable transaction, and invalid-transition tests |
| Retries and rate limits | Bounded retry policy, exponential backoff, jitter, timeout, circuit breaker, and classified error handling |
| Data extraction or transformation | Real parser or API, canonical schema, deterministic normalization, provenance fields, and fixture tests |
| Tool or API calls | Typed adapter, request/response validation, timeout, retry budget, error taxonomy, and contract tests |
| Evals and quality gates | Versioned eval cases, deterministic scorer, threshold, regression report, and CI or release gate |
| Auditability | Structured logs, event IDs, actor/source attribution, redaction, retention policy, and replayable traces |
| Policy enforcement | Central policy config, explicit ownership, exception workflow, monitoring, change control, and periodic review |

For additional patterns and examples, load `references/control-catalog.md`.

## Recommendation Format

When asked to review or design a workflow, return concise recommendations in this shape:

```markdown
## Deterministic Control Recommendations

1. Boundary: <where model/tool/user/system behavior crosses a reliability or safety boundary>
   Risk: <what fails and why it matters>
   Control: <schema, state machine, policy gate, parser, test, wrapper, etc.>
   Implementation: <specific local approach and owner module/file when known>
   Verification: <tests, eval cases, dry run, logs, or CI gate>
   Residual judgment: <what remains appropriate for the model or human>
```

If the answer is "do not add a deterministic control," say why the surface is low risk and what lightweight observation, prompt guidance, or human review is enough.

## Quality Gate

A production-grade recommendation should:

- enforce at the boundary where failure occurs, not only in a prompt
- prefer existing local frameworks, harness APIs, and policy systems over new infrastructure
- log the decision, input class, output class, policy version, and failure reason without leaking secrets
- be testable without a live model whenever practical
- fail closed for security, privacy, payments, destructive changes, production state, and compliance gates
- fail loud for ambiguous handoffs, missing context, stale credentials, partial parsing, or unverifiable claims
- include an owner, rollout path, and regression check when the control will affect repeated workflows

## Anti-Patterns

Flag these for correction:

- prompt-only enforcement for exact formats, security, permissions, or side effects
- free-form text parsing where a real parser, schema, or structured API exists
- regex as the only parser for nested, adversarial, or compliance-critical formats
- hidden model retries without a retry budget, timeout, or stop condition
- multiple sources of truth for the same policy or route table
- eval scores that require subjective manual interpretation but still gate releases
- silent best-effort behavior for secrets, production writes, external messages, or destructive commands

## Validation

Run the included documentation coverage eval:

```bash
python3 scripts/run_evals.py
```

To score model answers against the same cases, write JSONL records with `id` and `answer` fields and run:

```bash
python3 scripts/run_evals.py --answers path/to/answers.jsonl
```

Passing the evals does not prove the skill is perfect. It proves the current guidance covers the required control surfaces and that future answers can be regression-tested deterministically.
