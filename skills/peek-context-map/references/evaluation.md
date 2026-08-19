# Evaluation

Version: 0.1.0
Last updated: 2026-05-24

Use a lightweight replay before trusting a context map workflow.

## Test Shape

Pick one recurring context with 20-50 realistic tasks:

- a repo with repeated implementation, debugging, and explanation tasks
- a manual/document corpus with repeated lookup and synthesis tasks
- a dataset with repeated schema, aggregation, and interpretation tasks

Split tasks into:

- warm-up: first 3-5 tasks allow map updates
- evaluation: remaining tasks reuse the map and may update only after scoring

## Compare

Run at least two modes:

- baseline: no context map
- map: render the context map before each task

Optional modes:

- frozen map after warm-up
- auto-updating map
- human-approved updates only

## Metrics

Track:

- task correctness or human acceptance
- repeated orientation searches
- tool calls or iterations
- elapsed time
- token usage if available
- stale-map incidents
- hallucinated or unsourced map claims

## Pass Criteria

The map is useful only if it reduces repeated orientation work or improves task quality without adding false confidence. A map that grows but does not change agent behavior is not working.

## Stop Conditions

Pause rollout when:

- stale entries mislead tasks
- map entries become generic advice
- secrets or private raw excerpts appear
- the map duplicates project docs instead of pointing to them
- operation diffs are too noisy to review quickly
