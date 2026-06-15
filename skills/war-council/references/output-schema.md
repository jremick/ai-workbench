# War Council Output Schema

Use these contracts for auditable War Council runs. Keep IDs stable inside a run.

## Run Directory

```text
work/war-council/<topic-slug>-<timestamp>/
  mission.md
  evidence-register.json
  council-roster.json
  rubric.json
  briefs/
  reports/
  aggregate.json
  decision-ledger.md
  final.md
```

## Evidence Register

```json
{
  "claims": [
    {"id": "C1", "text": "Claim being relied on.", "source_ids": ["E1"]}
  ],
  "evidence": [
    {"id": "E1", "type": "file|test|telemetry|source-system|user-provided|web", "locator": "path, URL, command, or note", "summary": "What it supports."}
  ],
  "assumptions": [
    {"id": "A1", "text": "Assumption.", "why_it_matters": "Decision impact if false."}
  ],
  "constraints": [
    {"id": "K1", "text": "Constraint.", "hard": true}
  ]
}
```

## Rubric

`rubric.json`:

```json
{
  "decision": "Which option should we choose?",
  "options": [
    {"id": "O1", "label": "Option one"},
    {"id": "O2", "label": "Option two"}
  ],
  "dimensions": [
    {"id": "D1", "label": "Mission fit", "weight": 35},
    {"id": "D2", "label": "Economic quality", "weight": 20},
    {"id": "D3", "label": "Execution risk", "weight": 20},
    {"id": "D4", "label": "User/customer impact", "weight": 15},
    {"id": "D5", "label": "Reversibility", "weight": 10}
  ]
}
```

Rules:

- option IDs must be unique
- dimension IDs must be unique
- weights must be integers
- weights must total exactly 100
- use 5-7 dimensions unless the decision is intentionally simple

## Persona Report

Each report file under `reports/` must be valid JSON:

```json
{
  "persona_id": "ruthless_cfo",
  "persona_label": "Ruthless CFO",
  "recommendation": "O1",
  "thesis": "Short recommendation rationale.",
  "scores": {
    "O1": {"D1": 80, "D2": 90, "D3": 60, "D4": 70, "D5": 60},
    "O2": {"D1": 70, "D2": 65, "D3": 75, "D4": 80, "D5": 75}
  },
  "war_chest": {"O1": 70, "O2": 30},
  "agreements": ["Where this persona expects the council to converge."],
  "disagreements": ["Where this persona expects or creates dissent."],
  "evidence_ids": ["E1"],
  "claim_ids": ["C1"],
  "assumptions_challenged": ["A1"],
  "risks": ["Risk accepted if this recommendation is followed."],
  "kill_criteria": ["Signal that should reverse or pause the decision."],
  "confidence": 0.72
}
```

Rules:

- `recommendation` must be one known option ID
- `scores` must cover every option and every dimension
- score values must be numbers from 0 to 100
- `war_chest` must cover known option IDs and total exactly 100
- `confidence` must be 0 to 1 when present
- cite evidence, claims, and assumptions by ID instead of embedding long source text

## Aggregate

`scripts/war_council.py` writes:

```json
{
  "options": [
    {
      "id": "O1",
      "label": "Option one",
      "average_weighted_score": 78.25,
      "rank": 1,
      "tier": "build_first",
      "recommendation_votes": 3,
      "score_spread": 14.5,
      "war_chest": 62
    }
  ],
  "personas": [
    {
      "persona_id": "ruthless_cfo",
      "recommendation": "O1",
      "weighted_scores": {"O1": 79.0, "O2": 71.25}
    }
  ],
  "agreements": ["..."],
  "disagreements": ["..."]
}
```

Tier labels:

- `build_first`: top ranked and materially ahead
- `strong_candidate`: close to the lead or high allocation
- `nice_to_have`: useful but lower priority
- `park_it`: weak, blocked, or not worth near-term spend

## Decision Ledger

The ledger is Markdown. It should be short enough to read and complete enough to audit:

```markdown
# War Council Decision Ledger

## Decision
...

## Ranked Options
...

## Agreements
...

## Disagreements
...

## War Chest
...

## Risks Accepted
...

## Kill Criteria
...
```
