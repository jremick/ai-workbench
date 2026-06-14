# Codex Workflow Harvest

`codex-workflow-harvest` is an improvement-loop skill for agent work.

It helps turn repeated failures, user corrections, and workflow friction into durable skills, instructions, helper scripts, automations, or follow-up work.

## Install

Copy this directory into your agent skill directory:

```text
skills/codex-workflow-harvest/
```

The minimum install is `SKILL.md`. Keep `examples/` for a simple harvest queue template.

## Try It

```text
Use codex-workflow-harvest to review the last few task summaries and suggest which patterns should become durable instructions or skills.
```

## What Makes It Useful

This skill prevents two common problems:

- repeating the same operating mistakes because the lesson stayed trapped in one conversation
- dumping too much one-off detail into global instructions

The useful middle path is to promote only recurring, high-value patterns into the narrowest durable surface.

## Included Example

- [Harvest queue](examples/harvest-queue.md)

## Public Readiness

The public version is a pattern-level skill. It does not include private memory files, rollout summaries, local helper scripts, or private workspace references.
