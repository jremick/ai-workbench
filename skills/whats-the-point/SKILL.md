---
name: whats-the-point
description: Use when the user wants to evaluate information, documents, proposals, updates, strategy notes, research, or jargon-heavy writing and distill the real point into plain-language, decision-ready signal while preserving accuracy, nuance, uncertainty, and the ability to expand detail incrementally.
version: 1.1.0
last_updated: 2026-06-04
status: public-ready
---

# What's The Point

Turn dense, overlong, or jargon-heavy material into plain-language signal that a busy reader can act on quickly without losing accuracy or important nuance.

## Use When

Use this skill for:

- executive summaries, board notes, status updates, strategy memos, research summaries, policy notes, proposals, postmortems, decision briefs, meeting notes, or pasted documents
- simplifying corporate speak, technical detail, legal-ish wording, or abstract strategy language
- finding the actual claim, decision, risk, ask, tradeoff, implication, or next action inside a noisy source
- producing an expandable brief where the user can start with the shortest useful answer and ask for deeper detail only when needed

## Operating Contract

- Be blunt about the point, but not careless.
- Preserve names, dates, numbers, commitments, ownership, constraints, risks, and stated uncertainty.
- Separate what the source directly says from what it suggests.
- Do not invent missing context. If the source is unclear, say what is unclear and why it matters.
- Do not overstate the source. A possible result stays possible, a pilot stays a pilot, a recommendation stays a recommendation, and missing evidence stays missing.
- Do not collapse contradictions. If two sources conflict, keep the conflict visible and name the reconciliation needed.
- Simplify jargon into normal language. Keep a term only when it is necessary, defined, or useful to the audience.
- For sensitive or high-stakes material, prefer a slightly longer accurate answer over a shorter answer that hides risk, uncertainty, or ownership.
- When summarizing source documents, cite source sections, pages, headings, or short snippets when available.

## Workflow

1. Identify the user goal: understand, decide, act, direct, challenge, approve, reject, or ask follow-up questions.
2. Find the central claim, ask, decision, tension, evidence, and stakes.
3. Remove noise: throat-clearing, duplicated rationale, status theater, buzzwords, vague optimism, and unsupported certainty.
4. Preserve nuance: constraints, caveats, open questions, dissent, conditionality, and facts that could change the decision.
5. Translate to plain language and organize from shortest to deepest.
6. End with the next useful move: decide, ask, verify, delegate, escalate, or read deeper.

## Output Ladder

Default to the shortest level that answers the request.

### Level 1: Fastest Read

Use for quick triage.

```markdown
**Point:** <one sentence>
**Why It Matters:** <one sentence>
**Decision Or Action:** <what the user should decide, ask, or do next>
**Nuance:** <the caveat, condition, or uncertainty that should not be lost>
```

### Level 2: Signal Brief

Use when the user needs enough context to act.

```markdown
**Fastest Read**
<2-4 bullets, no filler>

**What It Means**
<plain-language implication>

**Decision Needed**
<decision, owner, timing, or missing approval>

**Risks Or Watchouts**
<only decision-relevant risks>

**If You Need More**
<2-3 bullets with the next layer of detail>
```

### Level 3: Decision Brief

Use when the user needs to defend a decision, direct work, or challenge the source.

```markdown
**Bottom Line**
**Evidence**
**Tradeoffs**
**Assumptions**
**Open Questions**
**Recommended Next Move**
**Detail Available On Request**
```

## Translation Rules

- Replace abstraction with concrete meaning.
- Remove hedging that adds no meaning, but keep uncertainty that affects the decision.
- Convert passive phrasing into owner/action language when the source supports it.
- Keep the shortest wording that still preserves the real claim.
- If a source hides weak evidence behind confident language, say that the confidence is not yet supported.

## Final Checks

Before finalizing, check:

- Did the output keep the source's core point, not just a more convenient point?
- Did it preserve decision-relevant facts, constraints, and uncertainty?
- Did it avoid turning a possibility into a certainty?
- Did it separate facts from interpretation?
- Did it make the user's next action clearer?
- Is there a path to expand detail without making the first answer long?

## Evaluation

This public package includes representative cases in `evals/cases.json`.

The internal reference suite used before publication covered 33 cases across ambiguous sources, conflicting evidence, missing context, sensitive facts, high-stakes decisions, overconfident sources, and unsupported claims. The public package ships only sanitized example cases and a concise proof summary.
