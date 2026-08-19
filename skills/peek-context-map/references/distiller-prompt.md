# Distiller Prompt

Version: 0.1.0
Last updated: 2026-05-24

Use this prompt when an LLM should inspect a completed run and identify reusable context-map candidates.

```text
You are maintaining a PEEK-style context map for a recurring external context.

The context map is a small orientation cache. It should capture reusable knowledge about the context itself: structure, locations, schemas, exact constants, key entities, relationships, derived reusable results, and factual failure patterns.

It must NOT store current-task answers, chat history, secrets, generic behavioral advice, or instructions.

Inputs:
- Current context map:
<<<CONTEXT_MAP>>>
{context_map}
<<<CONTEXT_MAP>>>

- User task:
<<<TASK>>>
{task}
<<<TASK>>>

- Execution trajectory summary:
<<<TRAJECTORY>>>
{trajectory_summary}
<<<TRAJECTORY>>>

Produce JSON with exactly these fields:
{
  "diagnosis": "Briefly explain what orientation work was repeated or newly learned, and what was task-specific.",
  "item_tags": {
    "<item_id>": "helpful | harmful | neutral | stale"
  },
  "cache_candidates": [
    {
      "section": "context_roadmap | context_understanding | domain_constants | parsing_schema | reusable_results | known_failure_patterns",
      "value": "Compact reusable item. Preserve exact constants and schema names.",
      "source_refs": ["Optional source path or command evidence"],
      "confidence": 0.0,
      "priority": 50,
      "transferability": "What future question types this helps.",
      "rationale": "Why this is shared context understanding, not a one-off answer."
    }
  ]
}

Rules:
- Prefer abstractions over raw passages, but keep exact numeric constants, formulas, enum sets, field names, and thresholds.
- Mark an existing item stale only when it is outdated, superseded, or contradicted by source evidence.
- If a candidate would only answer the current task, omit it.
- If evidence is weak, lower confidence or omit the candidate.
- Never include secrets or private tokens.
```
