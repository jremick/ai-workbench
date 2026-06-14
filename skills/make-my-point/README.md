# Make My Point

`make-my-point` is a skill for sharpening rough writing into a clear, audience-aware message.

It pairs naturally with `whats-the-point`: use `whats-the-point` to understand source material, then use `make-my-point` to shape the outgoing message.

## Install

Copy this directory into your agent skill directory:

```text
skills/make-my-point/
```

The minimum install is `SKILL.md`. Keep `evals/cases.json` when you want example test prompts.

## Try It

```text
Use make-my-point on this draft for a product leader. I need the point, the ask, and a stronger version that does not overclaim.

<paste draft>
```

## Good Outputs

A good answer:

- names the point and audience
- preserves facts, risks, uncertainty, and ownership
- puts the ask near the top
- improves structure and story without making claims stronger than the evidence
- explains why the revision works

## Public Readiness

The public version was rewritten from a live internal skill and reviewed to remove local paths, private workspace references, raw internal eval outputs, and personal context. The included eval cases are sanitized examples.
