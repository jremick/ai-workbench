# Example Output

Version: 0.1.0
Last updated: 2026-06-04

This is a fictional example response from the SMB AI Maturity Assessor.

## Scope

Customer support intake for a 60-person SaaS company.

## Assessed Working Level

**Level 2 - Assisted**

The team uses AI routinely for ticket summaries and draft replies, and humans review customer-facing output. It is not yet Level 3 because the workflow is not documented, context is manually pasted, and quality checks are informal.

## Dimension Scores

| Dimension | Score | Confidence |
| --- | --- | --- |
| Direction & Use Cases | 2 | Medium |
| Workflow & Adoption | 2 | High |
| Data & Context | 1 | High |
| Tools & Integration | 2 | High |

## Spine Scores

| Spine | Score | Confidence |
| --- | --- | --- |
| People & Accountability | 2 | Medium |
| Governance & Evidence | 2 | Medium |

## Transformation Profile

| Capability | Score | Confidence |
| --- | --- | --- |
| AI Working Skill | 2 | High |
| Work Design Depth | 2 | Medium |
| Reliable AI Operations | 2 | Medium |
| Organizational Adaptability | 1 | High |

## Evidence Used

- agents use AI for summaries and first-draft replies
- managers expect human review before customer responses are sent
- there is no shared support context pack
- prompt examples are owned by individuals, not the team
- response time is measured, but AI-assisted quality is not

## Binding Constraint

**Data & Context**

The maturity blocker is context quality. The transformation blocker is organizational adaptability: the team does not yet have a cadence for improving prompts, context, review criteria, roles, or measures as AI capability changes.

The support team cannot reliably move to Level 3 until AI has consistent access to approved support knowledge, tone examples, escalation rules, and response-quality criteria.

## Next Level Conditions

To reach Level 3, the team needs:

- a documented AI-assisted intake workflow
- reusable prompts and context for the top support categories
- a response review checklist
- examples of good and bad AI-assisted replies
- simple measures for response time, edit rate, escalation, and customer satisfaction

## Recommended Next Three Actions

1. Build a support context pack for the top 10 ticket categories.
2. Add a one-page review checklist for AI-assisted replies.
3. Run a 30-day pilot and compare response time, edit rate, escalation rate, and customer satisfaction.

## Confidence

Medium.

The team has enough evidence to assess current maturity, but the score would be stronger with reviewed examples of actual AI-assisted replies.

## What Not To Do Yet

Do not deploy an autonomous support agent yet. The workflow is not mature enough for Level 4 orchestration because context quality and quality measurement are still weak.
