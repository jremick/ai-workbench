---
name: model-manager
description: "Use when a non-trivial Codex task may benefit from explicit model delegation, role-stack routing, cost-aware model selection, benchmark-informed settings, or routing through Claude, Perplexity, LM Studio, Vercel AI Gateway, or another non-default provider."
version: 0.2.0
last_updated: 2026-06-16
status: public-alpha
---

# Model Manager

Use Model Manager as a policy layer before provider execution. It decides whether delegation is worthwhile, what role/model/settings should be used, and whether an explicit provider router such as `codex-model-router` should execute a non-default route.

Do not use this for trivial one-step questions where normal Codex can answer directly.

## Workflow

1. Classify the work:
   - trivial
   - implementation
   - code review
   - long-horizon coding
   - research
   - docs/writing
   - high-risk analysis
   - local/private
   - frontend QA
2. Decide whether delegation adds value.
3. Run the deterministic recommender when there is a real model choice:

```bash
python3 scripts/model_manager.py recommend \
  --task "Review this PR for architecture risks and missing tests" \
  --json
```

4. Inspect both returned surfaces:
   - `recommended_routes`: ranked model choices with scores and reasons.
   - `model_system_route`: selector/orchestrator/coder/reviewer/security-review role stack from `data/model_system.json`.
5. Follow the returned route plan.
6. Keep parent Codex responsible for integration, verification, final edits, and the final response.

## Model System

The public-friendly role stack lives in `data/model_system.json`.

It maps work to:

- `complexity`: `low`, `medium`, or `high`
- `review_tier`: `play`, `production`, or no review route
- `security_review`: true when auth, secrets, tokens, dependencies, permissions, data, privacy, or infrastructure risk appears

Generate a starter config:

```bash
python3 scripts/model_manager.py model-system-template --json
```

Use only model ids that exist in `data/model_catalog.json`.

## Source Rules

- Use Artificial Analysis for general model benchmark, price, speed, and latency data when a live cache is available.
- Use DeepSWE as the benchmark signal for long-horizon coding-agent work.
- Use the committed catalog as a fallback only when live benchmark refresh is unavailable.
- Current Claude Opus routing targets Opus 4.8. Artificial Analysis now publishes direct Opus 4.8 values; use previous-model proxy values only when a future catalog entry explicitly marks them.
- Store refreshed benchmark influence in `data/recommendation_values.json`; do not store API keys or raw account-scoped caches in the skill.
- Say when a recommendation is based on the committed fallback catalog.

## Execution Boundary

Model Manager recommends. It does not automatically spend external credits or run sidecars.

When a route requires Claude subscription, Perplexity, Vercel AI Gateway, or LM Studio, call `model-router` / `codex-model-router` with the explicit route returned by the recommender.

If a configured role route is marked unavailable, do not force it. Use the ranked fallback route list or update `data/model_system.json`.

## Verification

Before treating this skill as healthy:

```bash
python3 scripts/model_manager.py eval --json
python3 -m unittest discover -s tests
python3 scripts/model_manager.py validate-skill --json
python3 scripts/model_manager.py model-system-template --json
python3 scripts/model_manager.py write-recommendation-values --json
```
