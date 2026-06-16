# Model Manager

Version: 0.2.0
Last updated: 2026-06-16

Model Manager is a standalone Codex skill for role-based, benchmark-aware model delegation, cost optimization, and provider routing.

It is a policy layer above provider execution. It decides whether a task is worth delegating, chooses a model/settings route using task class plus benchmark and cost signals, and keeps non-default provider execution explicit through a router command.

## Status

Public alpha. The skill, deterministic recommender, route data, evals, and tests are usable, but model catalogs and benchmark-derived scores should be treated as policy fixtures rather than universal model rankings.

This package is distributed under the repository's Apache-2.0 license.

## What It Adds

- deterministic task classification and delegation decisions
- ranked model routes with score, backend, and rationale
- a `model_system` role stack for selector, orchestrator, coder, reviewer, and security-review routes
- Artificial Analysis refresh support without committing raw cache data
- DeepSWE-aware routing for long-horizon coding work
- evals, unit tests, and standalone package validation

## Quick Start

From this repository:

```bash
cd skills/model-manager
```

Run a recommendation:

```bash
python3 scripts/model_manager.py recommend \
  --task "Implement OAuth login, API token storage, and permission checks for production."
```

The output includes:

- `work_type`: task class such as `implementation`, `research`, or `long_horizon_coding`
- `delegate`: whether a sidecar route is worth considering
- `model_system`: complexity, review tier, and whether security review is needed
- ranked route alternatives with score and backend

Generate a model-system template:

```bash
python3 scripts/model_manager.py model-system-template --json
```

## Quick Checks

```bash
python3 scripts/model_manager.py recommend --task "Review this PR for architecture risks" --json
python3 scripts/model_manager.py eval --json
python3 -m unittest discover -s tests
python3 scripts/model_manager.py validate-skill --json
python3 scripts/model_manager.py model-system-template --json
```

## Live Benchmark Refresh

Artificial Analysis requires an API key. Do not commit live caches.

```bash
ARTIFICIAL_ANALYSIS_API_KEY=... \
  python3 scripts/model_manager.py refresh-artificial-analysis \
  --output data/artificial_analysis_models.cache.json

python3 scripts/model_manager.py write-recommendation-values \
  --output data/recommendation_values.json \
  --json
```

The raw cache must remain local and uncommitted. Commit only the sanitized recommendation values after checking that they contain no API key or raw account-scoped secret data.

Artificial Analysis attribution is required when its free API data influences recommendations. This package keeps attribution in the benchmark docs and source metadata returned by the CLI.

## Package Layout

| Path | Purpose |
|---|---|
| `SKILL.md` | Codex skill entrypoint. |
| `scripts/model_manager.py` | Deterministic recommendation, eval, refresh, and validation CLI. |
| `data/model_catalog.json` | Versioned benchmark-aware model catalog. |
| `data/model_system.json` | Role stack for selector, orchestrator, coder, reviewer, and security-review routes. |
| `data/recommendation_values.json` | Sanitized, non-secret recommendation values. |
| `data/eval_cases.json` | Deterministic routing eval cases. |
| `agents/` | Route-agent templates for bounded sidecar work. |
| `tests/` | Unit tests for classification, scoring, evals, and API behavior. |
| `docs/` | Architecture, benchmark source, and evaluation documentation. |

## Boundary

Model Manager recommends. It does not automatically spend external credits, call providers, edit files, or run sidecars. Parent Codex remains responsible for integration, verification, and final user-facing work.
