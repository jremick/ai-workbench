---
name: model-council
description: Use when a task needs multiple independent model perspectives, sidecar model review, adversarial synthesis, benchmarkable ensemble reasoning, or comparison against a Fusion-style multi-model answer. This skill defines a deterministic council workflow with explicit worker roles, isolated prompts, structured outputs, a separate synthesizer, and verifiable routing through local CLIs or Vercel AI Gateway.
version: 1.0.0
last_updated: 2026-06-15
---

# Model Council

Use a model council when one model's answer is not enough evidence for a decision, research synthesis, design choice, critique, or benchmark.

The council is not a vote. It is an independent evidence-gathering pattern followed by a synthesis pass that makes disagreements visible.

## Core Rule

Run council members independently before synthesis. The synthesizer may see the task, the rubric, and the worker outputs. Workers should not see each other's answers.

This keeps agreement meaningful and prevents the strongest or first answer from anchoring the rest of the council.

## Default Route Order

1. Local CLI routes first:
   - OpenAI models through Codex CLI.
   - Anthropic models through Claude Code CLI.
   - Google models through Antigravity CLI.
   - xAI models through Grok Build CLI.
2. Vercel AI Gateway as an API alternate option, when one endpoint is preferred over local CLI auth and sessions.

Do not silently substitute routes. If a configured CLI, model, or API credential is missing, stop or mark that route unavailable in the run manifest.

## Council Levels

| Level | Use For | Minimum Shape |
| --- | --- | --- |
| `base` | Normal hard questions, product decisions, research synthesis, and evaluation runs. | Three workers plus one synthesizer. |
| `adversarial` | High-risk claims, architecture choices, public or customer-facing conclusions. | Base plus an explicit critic or red-team worker. |
| `stress-test` | Claims that need failure-mode discovery. | Base plus test-case generation and verification recommendations. |
| `extended` | Large research or strategy work. | Multiple specialist workers, independent source review, synthesis, and a final verification pass. |

Use `base` unless the task has a clear reason to pay for more calls.

## Worker Roles

The base council should use distinct roles rather than indistinguishable "answer this" prompts:

| Role | Focus |
| --- | --- |
| Structural Analyst | Map the problem, constraints, hidden assumptions, and decision frame. |
| Empirical Analyst | Focus on facts, evidence, source quality, benchmarks, and falsifiable claims. |
| Contrarian Analyst | Look for failure modes, alternative explanations, and where the task framing may be wrong. |
| Optional Domain Analyst | Add narrow expertise only when the task needs it. |

The synthesizer is a separate role. It should identify consensus, disagreement, accepted claims, rejected claims, verification gaps, and the final answer.

## Output Contract

Ask each worker for structured output:

```json
{
  "role_id": "structural",
  "answer": "Worker answer.",
  "key_claims": ["Claim that matters."],
  "evidence": ["Evidence or reasoning used."],
  "uncertainties": ["What remains unknown."],
  "failure_modes": ["How this answer could be wrong."],
  "confidence": 0.72
}
```

Ask the synthesizer for:

```json
{
  "final_answer": "Decision-ready synthesis.",
  "consensus": "Where workers aligned.",
  "material_disagreements": ["Disagreement that affects the answer."],
  "accepted_claims": ["Claims used in the final answer."],
  "rejected_claims": ["Claims excluded and why."],
  "verification_gaps": ["Checks still needed."],
  "recommended_next_checks": ["Concrete verification step."],
  "confidence": 0.68
}
```

The runner stores raw outputs because model JSON can be imperfect. Treat parse failures as a quality signal, not as permission to discard the evidence silently.

## Deterministic Runner

Use the bundled runner when this skill is installed from the AI Workbench repo:

```bash
python3 tools/model-council-runner/scripts/council_runner.py validate \
  --config tools/model-council-runner/configs/local-cli.base.json \
  --task tools/model-council-runner/fixtures/smoke-task.json

python3 tools/model-council-runner/scripts/council_runner.py plan \
  --config tools/model-council-runner/configs/local-cli.base.json \
  --task tools/model-council-runner/fixtures/smoke-task.json \
  --run-dir /tmp/model-council-smoke \
  --force
```

`plan` creates prompts, command arrays, and a manifest without making model calls. `execute` must be run explicitly.

## Reference Files

Load these only when needed:

- `references/council-method.md`: detailed workflow, council levels, and synthesis rules.
- `references/provider-routing.md`: local CLI and Vercel AI Gateway routing notes.

## Verification

Before claiming a council run is complete:

- worker prompts were generated independently
- configured routes were named in the manifest
- unavailable routes were not silently replaced
- synthesis used worker outputs and preserved material disagreement
- raw prompts and outputs were saved under the run directory
