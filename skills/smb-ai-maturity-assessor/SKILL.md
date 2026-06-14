---
name: smb-ai-maturity-assessor
description: Assess an SMB team, function, or workflow against the SMB AI Maturity Model and recommend the next capability move. Use when the user asks where a business, team, function, or workflow sits in AI maturity, what is blocking the next level, or what to do next.
version: 0.1.0
last_updated: 2026-06-04
status: public-ready
---

# SMB AI Maturity Assessor

Assess AI maturity from evidence, not ambition.

## Source Framework

Use the companion framework in `frameworks/smb-ai-maturity-model/`:

- `model.md`
- `self-assessment.md`
- `transformation-model.md`
- `starter-roadmap.md`

If this skill is installed outside the repository, use the level, dimension, spine, and transformation summaries below as the minimum working model.

## Level Summary

| Level | Name | Meaning |
| --- | --- | --- |
| 1 | Exploring | Individuals experiment with AI, but usage is ad hoc and not measured. |
| 2 | Assisted | Common tools are available, used routinely, and reviewed by humans. |
| 3 | Embedded | Priority workflows include AI as a documented, repeatable step. |
| 4 | Orchestrated | Connected AI workflows or agents run multi-step processes with approval gates. |
| 5 | AI-native | Selected functions are designed AI-first, with governance, measurement, and continuous improvement. |

## Assessment Dimensions

| Dimension | What To Check |
| --- | --- |
| Direction & Use Cases | Whether the right AI opportunities are being chosen and prioritised. |
| Workflow & Adoption | Whether AI is part of real recurring work, not just experiments. |
| Data & Context | Whether AI has useful source material, examples, constraints, and context. |
| Tools & Integration | Whether AI tools are connected to the workflow and systems where work happens. |

## Cross-Cutting Spines

| Spine | What To Check |
| --- | --- |
| People & Accountability | Whether people can delegate, verify, own, and improve AI-assisted work. |
| Governance & Evidence | Whether review, risk, value, quality, cost, and auditability are managed visibly. |

## Transformation Capabilities

| Capability | What To Check |
| --- | --- |
| AI Working Skill | Whether people can use AI effectively in real work. |
| Work Design Depth | Whether people are redesigning work at the right level. |
| Reliable AI Operations | Whether AI-assisted work can run safely and reliably. |
| Organizational Adaptability | Whether the organization can adapt roles, workflows, context, and controls as technology changes. |

## When To Use

Use this skill when the user asks:

- "What AI maturity level are we at?"
- "Are we ready for AI agents?"
- "What should we do next with AI?"
- "How mature is this team or workflow?"
- "What is blocking us from moving up a level?"

## Required Inputs

Collect or infer:

- assessment scope: company, team, function, or workflow
- company size and business context, if available
- current AI tools and where they are used
- recent examples of AI-assisted work
- workflow documentation, review gates, or measurement evidence
- known constraints: data quality, skills, tooling, risk, budget, or time

If evidence is thin, say so and lower confidence.

## Workflow

1. **Narrow the scope.** Prefer one team or workflow over broad company-wide claims.
2. **Extract evidence.** Separate observed behavior from intent, demos, licenses, or aspiration.
3. **Score four dimensions.**
   - Direction & Use Cases
   - Workflow & Adoption
   - Data & Context
   - Tools & Integration
4. **Score two cross-cutting spines.**
   - People & Accountability
   - Governance & Evidence
5. **Determine the dimension level.** Use the highest level where at least three of four dimensions meet that level and no dimension is more than one level behind.
6. **Apply the spine cap.** The working level cannot exceed the lower of the two spine scores.
7. **Create a transformation profile.** Score AI Working Skill, Work Design Depth, Reliable AI Operations, and Organizational Adaptability when the user needs a leadership or roadmap answer.
8. **Name the binding constraint.** Identify the lowest-scoring material dimension, spine, or transformation capability that blocks the target workflow.
9. **Recommend the next move.** Prefer the smallest action that raises the binding constraint by one level.
10. **Flag unsafe jumps.** If the user wants Level 4 or Level 5 behavior before Level 3 controls exist, say what must be in place first.

## Output Format

Return:

- `Scope`
- `Assessed working level`
- `Dimension scores`
- `Spine scores`
- `Transformation profile`
- `Evidence used`
- `Binding constraint`
- `Next level conditions`
- `Recommended next three actions`
- `Confidence`
- `What not to do yet`

## Guardrails

- Do not treat tool access as maturity.
- Do not average scores into a misleading high level.
- Do not let strong dimensions override weak accountability or governance spines.
- Do not recommend transformation programs when one workflow-level improvement would solve the current problem.
- Do not recommend autonomous agents without workflow documentation, review gates, and escalation paths.
- Do not use vendor claims as evidence of the user's maturity.
- Keep recommendations suitable for SMB constraints.
- Avoid prescribing enterprise governance unless the workflow risk justifies it.

## Verification

Before finalizing an assessment, confirm:

- the assessed scope is narrow enough to support the conclusion
- level claims are tied to observed evidence, not ambition or tool access
- dimension scores and spine scores are shown separately
- the working level respects the spine cap
- the binding constraint is named
- recommended actions are small enough for the assessed organization to execute
- confidence is lowered when evidence is thin
