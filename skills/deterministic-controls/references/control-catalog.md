# Deterministic Control Catalog

Version: 1.0.0
Last updated: 2026-06-04

Use this reference when the main skill needs more detailed control patterns, implementation choices, or eval criteria.

## Control Classes

### Structured Contracts

Use for model output, tool arguments, API payloads, config files, task handoffs, and persisted records.

- Define a canonical schema with JSON Schema, Zod, Pydantic, TypeScript types, protobuf, OpenAPI, or a typed dataclass.
- Parse before acting; reject or repair within a bounded loop before any side effect.
- Keep one source of truth for field names, allowed values, defaults, and versioning.
- Add fixture tests for valid, missing, malformed, and extra-field inputs.
- Store provenance when extracting facts: source path, locator, timestamp, parser version, and confidence when semantic extraction is involved.

Avoid prompt-only JSON instructions for production workflows. A model can be asked to emit JSON, but deterministic parsing and validation must decide whether the JSON is usable.

### Routing And Classification

Use for skill selection, tool selection, escalation, queue assignment, approval paths, and feature flags.

- Use an explicit router table with ordered rules, allowed destinations, and fallback-to-ask behavior.
- Split deterministic facts from model judgment. Example: use code to detect file type and repo state, then let the model summarize intent.
- Require confidence thresholds only when calibrated and testable. Otherwise prefer explicit rule matches plus a safe fallback.
- Log the selected route, rule ID, input class, model version when relevant, and fallback reason.
- Add regression cases for near-misses, ambiguous requests, and forbidden destinations.

### Permission And Policy Gates

Use for file writes, shell commands, browser automation, emails, tickets, production data, secrets, deploys, purchases, and destructive actions.

- Fail closed by default. Allow only named capabilities, paths, hosts, scopes, or commands.
- Put the gate in the harness or tool wrapper, not only in a prompt.
- Separate read-only checks, dry runs, staging, approval, execution, and rollback.
- Redact secrets before logging and block secret values from durable files or chat.
- Track policy version, actor, approval source, and decision reason in structured logs.

### State Machines And Checkpoints

Use for multi-step agents, long-running tasks, resumable workflows, handoffs, transactions, and workflows with approvals.

- Model each durable state and allowed transition explicitly.
- Store checkpoints with enough context to resume safely without replaying unsafe side effects.
- Use idempotency keys for external writes, messages, uploads, deploys, and payments.
- Reject invalid transitions and duplicate side effects.
- Test interrupted, resumed, duplicate, stale, and out-of-order flows.

### Tool Harness Controls

Use for shell, browser, file, API, MCP, connector, and automation tools.

- Wrap tools with typed adapters and validate arguments before invocation.
- Prefer structured APIs over screen scraping or string parsing where available.
- Define timeouts, retry budgets, cancellation, output truncation, and error taxonomy.
- Capture command, working directory class, environment class, exit code, sanitized output, and elapsed time.
- Gate high-risk operations with dry-run previews and explicit approvals when required.

### Retry, Timeout, And Backoff

Use for network calls, flaky tools, external APIs, rate limits, model calls, and queue workers.

- Classify errors as retryable, fatal, user-actionable, or policy-blocked.
- Set max attempts, max elapsed time, per-attempt timeout, backoff, jitter, and circuit breaker behavior.
- Preserve the original failure and final failure reason.
- Avoid hidden infinite retries and silent fallbacks that change semantics.
- Test retry exhaustion and fatal-error short-circuiting.

### Evals And Release Gates

Use when a skill, prompt, agent, policy, parser, or workflow must stay reliable over time.

- Version eval cases with realistic prompts and expected control categories.
- Use deterministic scorers for pass/fail gates whenever practical.
- Separate model-quality evals from harness-control evals.
- Require a threshold, regression report, and explanation for any waived failure.
- Include adversarial and ambiguous cases, not only happy paths.

### Audit, Monitoring, And Incident Review

Use for production systems, regulated workflows, user-impacting actions, and repeated automation.

- Emit structured logs with event ID, actor, request ID, route, policy version, decision, and sanitized failure reason.
- Keep sensitive values out of logs while preserving enough metadata for debugging.
- Add counters for policy blocks, schema failures, retries, tool errors, approval denials, and fallback-to-human events.
- Make important decisions replayable from stored non-secret inputs and policy versions.
- Define retention and access controls for audit logs.

## Decision Rubric

Score each boundary from 0 to 2:

| Factor | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Exactness | Fuzzy output is acceptable | Some fields or choices must match | Exact parse, route, or state is required |
| Side effect | No external action | Reversible local change | External, destructive, costly, or durable action |
| Safety/security | Low sensitivity | Internal or moderate risk | Secrets, auth, privacy, production, compliance, or money |
| Repeatability | One-off exploration | Repeated manually | Automated, CI-gated, or reused by many agents |
| Observability | No audit need | Debug logs useful | Formal audit, incident review, or reporting needed |

If any factor is 2, add at least one deterministic control at that boundary. If the total is 4 or higher, use tests or evals before rollout. If the total is 7 or higher, add ownership, monitoring, and rollback or stop conditions.

## Best Practice Mapping

| Scenario | Recommended Controls | Verification |
| --- | --- | --- |
| Model emits task JSON for a harness | JSON Schema or typed model, bounded repair, reject on validation failure | Unit tests with valid, malformed, missing, and extra fields |
| Agent chooses which skill to invoke | Rule table, capability tags, route priority, fallback-to-ask | Golden routing cases and ambiguous-case tests |
| Agent runs shell commands | Command allowlist or denylist, working-directory constraints, dry-run support, approval gate | Fixture tests for allowed, blocked, and path traversal commands |
| Agent writes files | Path sandbox, diff preview, file-type validation, atomic write | Tests for allowed paths, blocked paths, and rollback behavior |
| Agent sends external messages | Recipient allowlist, content policy, preview, approval, audit log | Approval-flow tests and redaction checks |
| Workflow uses retries | Error taxonomy, bounded retries, backoff, timeout, circuit breaker | Retry exhaustion and fatal-error tests |
| Long-running agent resumes work | State machine, checkpoint schema, idempotency key, duplicate detection | Resume, duplicate, stale-state, and interrupted-flow tests |
| Skill claims production readiness | Structural validation, eval cases, deterministic scorer, threshold | Skill validation, eval harness, and regression report |
| Policy is enforced | Central policy config, versioned rules, deny-by-default gate, exception workflow | Policy unit tests and audit-log assertions |

## Recommendation Checklist

Before finalizing a recommendation, confirm:

- the boundary is named clearly
- the failure mode is concrete
- the control is enforceable by code, config, schema, tests, or a harness
- the model still has a defined role where semantic judgment is useful
- the implementation fits existing local conventions and avoids speculative infrastructure
- the verification can fail if the control is removed or weakened
- residual risk, owner, and stop condition are explicit when the system is production-facing
