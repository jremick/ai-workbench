---
name: verification-harness-router
description: Use when an agent needs to prove a claim, choose tests or evals, verify a public artifact, validate a workflow, check launch readiness, or decide what evidence is enough. This skill routes work to the smallest credible verification harness: tests, evals, smoke checks, screenshots, read-backs, diff review, secret scan, sidecar critique, or user review.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# Verification Harness Router

Choose the smallest credible proof path for an agent claim or deliverable.

The goal is not to run every possible check. The goal is to match the claim to evidence that would actually fail if the claim were false.

## Core Rule

Every important completion claim needs evidence. The evidence must test the claim, not merely show activity.

## Use When

Use this skill when the user asks:

- is this ready, working, public-ready, safe, or complete?
- how should we test or evaluate this?
- what proof should a skill, tool, app, workflow, or artifact include?
- which checks belong in CI, a script, a smoke test, a manual review, or a model eval?
- how to verify work from sub-agents or sidecar models
- how to package proof for a public artifact

Do not use it for low-stakes brainstorming where no readiness claim is being made.

## Routing Workflow

1. Name the claim.
   - Example: "the app works", "the skill is public-ready", "the migration is safe", or "the summary is faithful".
   - Split broad claims into smaller claims that can be checked.

2. Classify the evidence type.
   - Code behavior: unit, integration, end-to-end, fixture, or smoke test.
   - Agent behavior: eval cases, deterministic scorer, transcript review, or regression report.
   - UI behavior: browser check, screenshot, interaction test, visual inspection, or accessibility check.
   - Public artifact: README review, example run, validator, license check, secret scan, and sanitized fixture check.
   - Live system: read-only health check, logs, API read-back, canary, or rollback proof.
   - Writing or synthesis: source citation check, contradiction scan, sidecar critique, or user review.

3. Pick the narrowest harness.
   - Prefer deterministic checks when exact pass/fail matters.
   - Use model or human review when quality is semantic or subjective.
   - Combine checks only when one evidence type cannot cover the claim.

4. Define failure behavior.
   - Stop, ask, retry, revise, roll back, mark partial, or document residual risk.
   - Fail closed for public safety, privacy, secrets, destructive actions, money, and live production writes.

5. Verify the verifier.
   - A useful test would fail if the behavior regressed.
   - A useful eval has cases that distinguish good from generic answers.
   - A useful screenshot or read-back proves the relevant surface, not just that something loaded.

## Model And Sidecar Review

Use sidecar models as review tools, not proof by themselves.

Good sidecar uses:

- critique a plan for missed risks
- compare two verification strategies
- independently inspect public-facing wording
- review whether eval cases are discriminating

Do not use a sidecar model as the only evidence for code correctness, secret safety, public readiness, or live-system health. Parent agents must still run deterministic checks or read-backs where possible.

## Output Format

```markdown
## Claim
<what needs to be proven>

## Verification Route
| Claim Part | Evidence | Command Or Check | Failure Behavior |
| --- | --- | --- | --- |

## Minimum Proof
<checks that must pass before claiming done>

## Useful But Optional
<checks that add confidence but are not required>

## Residual Risk
<what remains unproven and why>
```

## Anti-Patterns

Flag these:

- claiming readiness from code review alone when behavior can be run
- using screenshots for non-visual logic
- using unit tests as proof of an integration contract they do not cover
- treating a model critique as deterministic validation
- passing evals that only check for generic words
- saying "tests passed" without naming which tests ran
- hiding skipped checks or partial verification

## Verification

Before finalizing a verification plan or readiness answer:

- each material claim has an evidence route
- required and optional checks are separated
- commands, files, screenshots, read-backs, or review gates are concrete
- failure behavior is explicit
- skipped or unavailable checks are disclosed
- public artifacts include sanitization and secret-scan style checks
