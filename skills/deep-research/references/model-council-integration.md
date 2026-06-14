# Model Council Integration

Version: 1.0.0
Last updated: 2026-06-15

Use `model-council` after research collection when the task needs independent interpretation.

## Escalate When

- sources conflict and a decision still has to be made
- benchmark design could be biased by prompt leakage or scoring choices
- the answer will become public documentation or a high-impact recommendation
- a single synthesis pass is likely to miss failure modes
- the task benefits from structural, empirical, and contrarian lenses

## Evidence Packet

Give every council worker the same evidence packet:

```markdown
## Question
<research question>

## Decision Context
<what the answer will be used for>

## Evidence
| Source | Date | Finding | Caveat |
| --- | --- | --- | --- |

## Known Conflicts
<conflicts or weak spots>

## Required Output
<worker output contract>
```

Do not include hidden grading rubrics, private notes, or unrelated raw source dumps.
