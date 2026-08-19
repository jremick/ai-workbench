# Peek Context Map

> **Status: Curated public projection.**

A bounded, source-grounded orientation cache for recurring work over a large repository, document collection, dataset, or other external context.

## Package contents

- `SKILL.md` — map purpose, update rules, storage boundary, and verification.
- `scripts/context_map.py` — deterministic initialization, rendering, validation, diff, apply, eviction, and staleness checks.
- `references/schema.md` — map and operation schema.
- `references/distiller-prompt.md` and `cartographer-prompt.md` — optional model-judgment stages.
- `references/evaluation.md` — a bounded comparison plan.

## Try it

From this package directory:

```bash
tmp_dir="$(mktemp -d)"
python3 scripts/context_map.py init \
  --context-id "example:synthetic" \
  --source references \
  --map "$tmp_dir/map.json"
python3 scripts/context_map.py validate --map "$tmp_dir/map.json"
python3 scripts/context_map.py render --map "$tmp_dir/map.json"
```

The helper does not call a model. It can fingerprint source paths and store source references, so generated maps may reveal private structure. Do not commit or publish real maps without a separate disclosure review.

## Projection boundary

This public edition removes assumptions about a maintainer's private memory, sync, and operating systems. It is not a snapshot of any context-map data and does not include private maps or source inventories.
