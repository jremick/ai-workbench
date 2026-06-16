# Benchmark Sources

Version: 0.1.3
Last updated: 2026-05-29

## Artificial Analysis

Artificial Analysis is the preferred source for general LLM quality, pricing, speed, and latency metadata.

The public API documentation says the free API exposes independent intelligence evaluations, speed benchmarks, and pricing. It also documents the LLM models endpoint at:

```text
GET https://artificialanalysis.ai/api/v2/data/llms/models
```

The documented response includes:

- stable model `id`
- model `name` and `slug`
- `evaluations`
- `pricing`
- median output tokens per second
- median time to first token

Attribution is required when using free API data. The skill documentation and generated route plans should attribute benchmark and pricing data to Artificial Analysis when live API data or cached Artificial Analysis data influenced the decision.

The refresh command requires `ARTIFICIAL_ANALYSIS_API_KEY` and writes to an ignored local cache:

```bash
ARTIFICIAL_ANALYSIS_API_KEY=... \
  python3 scripts/model_manager.py refresh-artificial-analysis \
  --output data/artificial_analysis_models.cache.json
```

Do not commit the generated cache unless the team explicitly decides that a sanitized snapshot is acceptable under the Artificial Analysis terms and attribution requirements.

Claude Opus routes target Opus 4.8 as of 2026-05-29. Artificial Analysis now publishes direct Opus 4.8 values, so model-manager recommendations should use `claude-opus-4-8` directly instead of the previous Opus 4.7 proxy.

After refreshing the cache, write the committed recommendation values separately:

```bash
python3 scripts/model_manager.py write-recommendation-values \
  --output data/recommendation_values.json \
  --json
```

`recommendation_values.json` must contain only selected benchmark-derived values, route scores, and recommendation profiles. It must not contain the Artificial Analysis API key or raw account-scoped cache payload.

## DeepSWE

DeepSWE is the preferred benchmark signal for long-horizon software engineering agents. Datacurve describes it as a benchmark for frontier coding agents on original, long-horizon software engineering tasks.

The current curated fixture records these public leaderboard entries:

| Model | Setting | DeepSWE score |
|---|---:|---:|
| GPT-5.5 | xhigh | 70 +/- 4 |
| GPT-5.4 | xhigh | 56 +/- 5 |
| Claude Opus 4.8 | max | pending; temporarily keep Claude Opus 4.7 proxy 54 +/- 5 for DeepSWE only |
| Claude Sonnet 4.6 | high | 32 +/- 4 |
| Gemini 3.5 Flash | medium | 28 +/- 4 |
| GPT-5.4 Mini | xhigh | 24 +/- 4 |

DeepSWE should not be treated as a universal model ranking. It is specifically weighted for repository exploration, multi-file changes, long-horizon coding, and behavior-verifier oriented software engineering work.

## Scoring Policy

Model Manager combines sources conservatively:

- Artificial Analysis: general quality, cost, latency, and speed.
- DeepSWE: long-horizon coding-agent reliability.
- Local policy: tool access, privacy constraints, subscription preference, provider availability, and parent-Codex ownership.

When live benchmark data is unavailable, the recommender must say it used the committed catalog snapshot.
