---
name: codex-workflow-harvest
description: Review recent agent work, memory summaries, rollout notes, repeated failures, and workflow friction to decide which lessons should become durable skills, instructions, helper scripts, automations, or follow-up work. Use when a team wants to convert repeated agent operating lessons into reusable workflow improvements without publishing private logs or bloating global instructions.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# Codex Workflow Harvest

Turn repeated agent workflow lessons into durable improvements.

Despite the name, the pattern applies to any coding-agent environment that has skills, instructions, memory notes, helper scripts, or recurring automations. Keep the public version focused on the workflow, not on any one private setup.

## Purpose

Use this skill for periodic improvement passes over recent agent work.

The goal is to promote recurring lessons into the right durable surface:

- a skill update
- a helper script
- a project instruction
- a global instruction
- a reusable checklist
- an automation
- a follow-up issue
- an explicit rejection because the lesson is too narrow or stale

## Inputs

Use only sources the user has approved for review.

Good inputs:

- curated memory summaries
- sanitized rollout summaries
- project closeout notes
- recurring failure notes
- skill files
- instruction files
- validation reports
- user-approved issue or task records

Avoid:

- raw private chat logs
- secrets or credentials
- customer or employer-confidential material
- personal memory exports
- local machine state that does not generalize
- stale facts that should be rechecked before reuse

## Harvest Criteria

Promote a pattern when at least one is true:

- the same failure mode appeared in multiple tasks
- the pattern saves setup, routing, authentication, or source-of-truth rediscovery time
- the pattern reduces risk around live writes, permissions, public surfaces, or budgets
- the user explicitly said to remember it for future work
- the pattern changes how future agents should choose tools, sources, or verification

Do not promote:

- one-off facts unlikely to recur
- stale live-state values that must be rechecked anyway
- project-specific details into global instructions when a project skill is a better fit
- secrets, token values, raw private exports, or unreviewed transcripts

## Workflow

1. Define the review window.
   - recent tasks, one repo, one workflow, one incident type, or one skill family
2. Collect only approved evidence.
   - prefer summaries and curated notes over raw logs
3. Extract repeated signals.
   - symptoms, fixes, routing mistakes, auth friction, verification gaps, and user corrections
4. Choose the durable target.
   - skill, helper script, project instruction, global instruction, automation, issue, or no action
5. Keep the edit small.
   - promote the rule where it will trigger, but avoid bloating broad instructions
6. Verify the artifact.
   - run validators, syntax checks, examples, or direct read-backs
7. Leave a harvest queue outcome.
   - implemented, follow-up, rejected, or deferred for live recheck

## Output Format

```markdown
**Harvest Scope**
<what was reviewed>

**Patterns Found**
<only recurring or high-value patterns>

**Promotions**
<target -> change -> why>

**Rejected Or Deferred**
<what was not promoted and why>

**Verification**
<checks or read-backs run>

**Next Review**
<optional follow-up window or trigger>
```

## Quality Gate

Before claiming a workflow harvest is done:

- every promoted pattern has a named target
- every material finding has an outcome: implemented, follow-up, rejected, or deferred
- broad instruction changes are minimal and reusable
- private raw source material was not copied into durable artifacts
- changed skills or instructions include visible version and date markers
- validation or direct read-back was run for touched artifacts
