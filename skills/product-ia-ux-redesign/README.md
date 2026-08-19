# Product IA UX Redesign

> **Status: Current public snapshot.**

A source-backed workflow for auditing and redesigning complex product information architecture, UX, and UI while producing implementation-ready artifacts and explicit browser-verification plans.

## Package contents

- `SKILL.md` — evidence modes, IA workflow, severity model, implementation lanes, and stop rules.
- `references/artifact-system.md` — the review archive contract and tables.
- `references/frameworks-and-sources.md` — source-quality ladder and comparison guidance.
- `scripts/init-review-artifacts.py` — a deterministic review-package generator.

## Try it

From this package directory:

```bash
tmp_dir="$(mktemp -d)"
python3 scripts/init-review-artifacts.py \
  --out "$tmp_dir/review" \
  --product "Synthetic Console" \
  --routes "#home,#objects,#settings" \
  --review-mode prompt-only
```

The generator creates a skeleton, not completed research or acceptance evidence.

## Claim limits

File-grounded review is not browser verification. Prompt-only findings must remain inferred, and package-authored templates do not establish usability, accessibility conformance, or implementation correctness. Current external UX guidance should be rechecked when it materially affects a recommendation.
