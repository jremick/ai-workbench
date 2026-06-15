# Persona Brief Template

Copy this for each council member into `briefs/<persona_id>.md`.

```markdown
# War Council Persona Brief: <Persona Label>

## Mission

Read:

- `mission.md`
- `evidence-register.json`
- `rubric.json`

Do not read other persona reports before writing yours.

## Persona Mandate

<Persona-specific mandate from personas.md>

## Task

Evaluate every option in `rubric.json`.

Return JSON only, matching the persona report schema in `references/output-schema.md`.

## Required Analysis

1. State your recommendation as one known option ID.
2. Score every option against every rubric dimension from 0 to 100.
3. Allocate exactly $100 across the known options in `war_chest`.
4. Cite relevant evidence IDs, claim IDs, and assumptions challenged.
5. Name the strongest objection to your own recommendation.
6. Name at least one kill criterion that would reverse or pause your recommendation.
7. State confidence as a number from 0 to 1.

## Output Contract

Write:

`reports/<persona_id>.json`

Do not include Markdown outside the JSON file.
```
