# What's The Point

`whats-the-point` is a skill for turning dense source material into decision-ready signal.

It is not a generic summarizer. It is optimized for finding the claim, ask, risk, tradeoff, uncertainty, and next action inside noisy text.

## Install

Copy this directory into your agent skill directory:

```text
skills/whats-the-point/
```

The minimum install is `SKILL.md`. Keep `evals/cases.json` when you want example test prompts.

## Try It

```text
Use whats-the-point on this update. I need the actual decision, the evidence, and what is still unclear.

<paste source material>
```

## Good Outputs

A good answer:

- names the point in the first line
- preserves dates, numbers, ownership, risks, and uncertainty
- separates what the source says from what the source implies
- avoids making weak evidence sound stronger than it is
- gives a clear next action

## Public Readiness

The public version was rewritten from a live internal skill and reviewed to remove local paths, private workspace references, raw internal eval outputs, and personal context. The included eval cases are sanitized examples.
