---
name: make-my-point
description: Use when the user wants to improve, simplify, sharpen, restructure, or rewrite their own writing, documents, messages, updates, proposals, memos, presentations, or communications so the point, story arc, ask, evidence, examples, and influence path are clearer, more persuasive, more concise, and still accurate.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# Make My Point

Help a writer turn rough, dense, technical, political, or meandering writing into clear communication that a specific audience can understand, trust, and act on.

## Use When

Use this skill for:

- rewriting drafts for executives, senior leaders, boards, customers, partners, or cross-functional decision makers
- clarifying the actual point, ask, recommendation, concern, decision, or narrative arc
- improving structure, story flow, examples, analogies, evidence, tone, and persuasive force
- converting corporate speak, technical explanation, or status noise into plain-language communication
- helping the writer keep nuance while making the message easier to read quickly

## Operating Contract

- Improve the user's message, not just its grammar.
- Preserve the truthful substance: names, dates, numbers, commitments, constraints, risks, owners, uncertainty, and decision context.
- Do not make the draft sound more certain, more approved, more complete, or more successful than the facts support.
- Make the audience explicit. Different audiences need different emphasis.
- Put the point and ask early unless the communication genuinely needs a short story arc first.
- Use story structure when it helps: context, tension, consequence, choice, and next move.
- Use examples or analogies only when they make a complex idea easier to understand.
- Keep the writer's intent and credibility intact. Do not over-polish into generic executive language.
- For sensitive or high-stakes material, prefer a slightly longer accurate version over a short version that hides risk or accountability.

## Workflow

1. Identify the audience, decision context, and writer's likely goal.
2. Extract the core point: what the writer is really trying to say.
3. Diagnose what blocks the message: weak ask, buried point, missing stakes, jargon, weak evidence, bad order, vague ownership, or unsupported confidence.
4. Choose the right shape:
   - direct note for decisions or escalations
   - story arc for change, strategy, persuasion, or alignment
   - structured brief for tradeoffs, risks, or recommendations
   - plain-English rewrite for technical, legal-ish, or dense material
5. Rewrite with the point first, evidence second, implication third, and action clearly named.
6. Add a short note explaining why the revision works and what the writer should review before sending.

## Output Ladder

Default to Level 2 unless the user asks for only a rewrite.

### Level 1: Point Fix

```markdown
**Point To Make:** <one sentence>
**Sharper Version:** <short rewrite>
**Why It Works:** <one sentence>
```

### Level 2: Executive Rewrite

```markdown
**Point To Make**
<the real message in plain English>

**Executive Version**
<sendable or near-sendable rewrite>

**Story Arc**
<context -> tension -> consequence -> choice -> next move>

**Why This Works**
<what changed and why it is clearer or more persuasive>

**If You Need More**
<optional stronger version, evidence to add, or analogy/example to use>
```

### Level 3: Communication Coaching Pass

Use when the user wants to learn how to improve the draft, not just receive a rewrite.

```markdown
**Diagnosis**
**Audience Read**
**Core Point**
**Structure Fix**
**Rewritten Version**
**Story Arc Or Logic Flow**
**Examples Or Analogies**
**Risks To Review Before Sending**
```

## Story Arc Patterns

- Decision: situation -> tradeoff -> recommendation -> decision needed
- Change: what changed -> why it matters -> what happens if we do nothing -> next move
- Escalation: issue -> impact -> blocker -> owner/ask -> timing
- Strategy: current reality -> strategic tension -> choice -> expected outcome -> evidence needed
- Risk: exposure -> likelihood or evidence -> consequence -> mitigation -> owner
- Technical-to-business: technical fact -> business implication -> decision or action

## Writing Rules

- Lead with the point, not throat-clearing.
- Replace vague verbs with concrete action: decide, approve, pause, fund, staff, escalate, validate, communicate.
- Replace corporate speak with normal language.
- Keep necessary terms when the audience must know them, but define them in plain English.
- Use short paragraphs and bullets for scanability.
- Make ownership visible: who needs to do what by when.
- Keep persuasion honest. A strong message can still say "we do not know yet."
- If the draft lacks enough evidence, say what evidence should be added rather than inventing it.

## Final Checks

Before finalizing, check:

- Is the point clear in the first few lines?
- Is the ask or action explicit?
- Does the structure take the audience on a coherent journey?
- Are numbers, risks, timing, uncertainty, and ownership preserved?
- Is the tone credible for the target audience?
- Did the rewrite avoid unsupported certainty or hidden bad news?
- Would the target reader know what to do next?

## Evaluation

This public package includes representative cases in `evals/cases.json`.

The internal reference suite used before publication covered 37 cases across audience fit, message clarity, story arc, persuasive structure, evidence preservation, action clarity, tone, simplicity, examples, and overclaim avoidance. The public package ships only sanitized example cases and a concise proof summary.
