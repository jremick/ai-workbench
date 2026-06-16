# Evaluation Plan

Version: 0.2.0
Last updated: 2026-06-16

## Goals

The first eval layer checks route policy, not model answer quality.

It should catch:

- accidental over-delegation of trivial work
- failure to route live research toward Perplexity/Sonar
- failure to weight DeepSWE for long-horizon coding
- failure to prefer local models for private/local-only work
- unsafe cost-only routing on high-risk tasks
- incorrect model-system complexity and review-tier routing
- missing security-review routing for auth, secrets, tokens, dependencies, data, or infrastructure risk
- schema regressions in route-plan JSON

## Commands

```bash
python3 scripts/model_manager.py eval --json
python3 -m unittest discover -s tests
python3 scripts/model_manager.py validate-skill --json
python3 scripts/model_manager.py model-system-template --json
python3 scripts/model_manager.py write-recommendation-values --json
```

## Promotion Bar

A production-ready skill release should have:

- all deterministic eval cases passing
- standalone skill validation passing
- route plans with source notes and explicit fallback behavior
- role-stack routes with deterministic complexity, review tier, and security-review fields
- no live API keys or generated account caches committed
- sanitized recommendation values generated from the latest approved benchmark cache
- a documented benchmark refresh workflow
- public-safety checks for license, security guidance, benchmark attribution, and install documentation
- at least one real-world bake-off before changing global Codex defaults

## Future Evals

The next layer should use historical Codex tasks and compare:

- route chosen by current human judgment
- route chosen by Model Manager
- actual cost and latency where available
- output acceptance/rework
- missed requirements
- cases where delegation added overhead without value
