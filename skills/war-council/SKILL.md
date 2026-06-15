---
name: war-council
description: "Use for high-stakes or uncomfortable decisions that need structured advisor personas, adversarial challenge, weighted tradeoff scoring, forced budget allocation, agreement/disagreement tracking, and an auditable decision ledger. Trigger when the user asks for a war council, advisor council, ruthless CFO/operator/customer-rep review, decision debate, forced prioritization, tradeoff call, uncomfortable recommendation, or a $100/$1000-style allocation across options. Do not use for ordinary brainstorming, simple summaries, copyediting, or low-stakes preference lists."
---

# War Council

Version: 1.0.0
Last updated: 2026-06-16

War Council is a decision harness for moments where the easy answer may be rationalized and the useful answer is uncomfortable. It turns advisor personas into a traceable workflow: evidence first, independent opinions, weighted scoring, forced allocation, synthesis, and an audit trail.

The council does not replace the user's judgment. It makes assumptions, disagreements, tradeoffs, and reversal triggers visible.

## Operating Rules

1. Read the real files, live systems, or user-provided context before advising.
2. Create a run directory under `work/war-council/<topic-slug>-<timestamp>/` for non-trivial runs.
3. Keep first-pass persona opinions independent. Do not let one persona see another persona's report before aggregation.
4. Use fixed personas plus dynamic personas selected by the decision type.
5. Build a weighted rubric totaling exactly 100 before scoring options.
6. Require each persona to score every option, cite evidence IDs, state assumptions challenged, and force a $100 allocation across options or action batches.
7. Use `scripts/war_council.py` for score and allocation math. Do not hand-compute the final ranking.
8. Preserve disagreements. A lone dissent can be the most useful output.
9. End with a decision ledger: decision, rationale, agreements, disagreements, allocation, risks accepted, kill criteria, and questions only the user can answer.

## Workflow

### 1. Scope The Mission

Capture the decision frame in `mission.md`:

- decision to make
- options under consideration
- goal and non-goals
- constraints, deadline, budget, risk tolerance, and reversibility
- stakeholders affected
- what would make the decision wrong
- evidence mode: user-provided, internal-only, live-verified, or web-augmented

Ask only if a missing answer materially changes the decision or creates an unsafe guess. Otherwise state assumptions and continue.

### 2. Build The Evidence Register

Create `evidence-register.json` with:

- claims: `C1`, `C2`, ...
- evidence: `E1`, `E2`, ...
- assumptions: `A1`, `A2`, ...
- constraints: `K1`, `K2`, ...

Use direct files, tests, telemetry, docs, source systems, or user-provided facts as evidence. Model agreement is not evidence.

Read `references/output-schema.md` before creating the register or persona report files.

### 3. Assemble The Council

Always include:

- `ruthless_cfo`: economics, opportunity cost, runway, ROI, downside protection
- `wartime_operator`: execution reality, speed, sequencing, failure modes, ownership
- `compassionate_customer_rep`: customer/user harm, trust, support burden, communication
- `judge`: neutral synthesis only, no first-pass recommendation

Add 1-2 dynamic personas using `references/personas.md`. Pick personas by decision type, not preference. Examples:

- technical architecture -> Principal Engineer, Security Skeptic
- product strategy -> Product Strategist, Growth Skeptic
- hiring/org -> Talent Operator, Culture Carrier
- public communication -> Reputation Counsel, Skeptical Reader
- investment/spend -> Market Analyst, Procurement Skeptic

### 4. Build The Rubric

Create `rubric.json` before persona scoring. Use 5-7 dimensions with integer weights totaling 100. The highest-weight dimension should represent the actual mission goal unless the user explicitly says otherwise.

Use `references/rubrics.md` for default dimensions and weighting patterns.

### 5. Run Independent Persona Passes

For each persona, create a brief from `references/brief-template.md` and save it under `briefs/<persona_id>.md`.

If the user explicitly asks to run subagents or parallel agents, spawn independent subagents with `fork_context:false` and give each one only the mission, evidence register, rubric, and that persona's brief. If subagents are unavailable or not explicitly authorized, run the persona passes sequentially and label the run `single-agent-simulated`.

Each persona must write `reports/<persona_id>.json` using the schema in `references/output-schema.md`.

### 6. Aggregate Deterministically

Run:

```bash
python3 /path/to/war-council/scripts/war_council.py aggregate \
  --rubric work/war-council/<run>/rubric.json \
  --reports-dir work/war-council/<run>/reports \
  --out work/war-council/<run>/aggregate.json \
  --ledger work/war-council/<run>/decision-ledger.md
```

The script validates:

- rubric weights total exactly 100
- persona reports cover all options and dimensions
- scores are numeric and 0-100
- forced allocations total exactly 100 per persona
- recommendation IDs match known options

It computes:

- weighted score by option and persona
- average weighted score by option
- recommendation votes
- disagreement spread
- normalized final war-chest allocation
- ranked option tiers

### 7. Judge Synthesis

The judge reads `mission.md`, `evidence-register.json`, all persona reports, and `aggregate.json`. The judge produces:

- decision made, decision deferred, or human-gated decision
- strongest case for the top option
- strongest case against it
- agreements
- material disagreements
- uncomfortable truth
- allocation and first actions
- risks accepted
- kill criteria and reversal triggers
- questions only the user can answer

Save the final answer to `final.md` when the run is substantial.

## Output Format

Return a concise decision memo:

```markdown
**Decision**
<recommended option or human-gated decision>

**Why**
<short rationale tied to evidence IDs and rubric results>

**Council View**
- Agreement: <where personas converged>
- Disagreement: <what still splits the council>
- Lone dissent: <important minority view, if any>

**War Chest**
<forced $100 allocation across options or action batches>

**Risks Accepted**
<what this choice knowingly tolerates>

**Kill Criteria**
<signals that should reverse or pause the decision>

**Only You Can Answer**
<3-5 questions requiring human judgment>
```

## Reference Files

| File | Use |
| --- | --- |
| `references/output-schema.md` | JSON schemas for mission, evidence, rubric, persona reports, aggregate, and decision ledger |
| `references/personas.md` | Fixed and dynamic persona definitions plus routing table |
| `references/rubrics.md` | Weighted rubric patterns and tiering rules |
| `references/brief-template.md` | Persona brief template for subagents or sequential passes |

## Verification

Before claiming a War Council is complete:

- mission, evidence register, council roster, rubric, reports, aggregate, and ledger exist for non-trivial runs
- first-pass persona reports were isolated
- all persona reports cite evidence or assumptions by ID
- `war_council.py aggregate` completed successfully
- disagreements and lone dissents are visible in the final memo
- the final recommendation states what would change the decision
