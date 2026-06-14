# Model Council DRACO Benchmark

Version: 1.0.0
Last updated: 2026-06-15

This benchmark package prepares DRACO samples for evaluating the `model-council` skill.

DRACO is useful as a base-level benchmark for a council because it is designed around difficult prompts with grading criteria. The benchmark harness keeps answer generation separate from rubric-based grading.

Dataset:

```text
https://huggingface.co/datasets/perplexity-ai/draco
```

Raw JSONL:

```text
https://huggingface.co/datasets/perplexity-ai/draco/resolve/main/test.jsonl
```

## Benchmark Shape

1. Fetch the dataset.
2. Sample cases deterministically by seed.
3. Write generation tasks without rubric fields.
4. Write withheld grading rubrics separately.
5. Run the base council on generation tasks.
6. Grade outputs with rubrics after generation.
7. Report exact config, sample seed, dataset hash, model routes, and failures.

## Leakage Rules

Do not include rubric fields in worker prompts.

Do not include rubric fields in synthesizer prompts during answer generation.

Do not tune the council prompt against the test sample and then report that same sample as an unbiased score.

## Prep Script

Use the benchmark prep script:

```bash
python3 benchmarks/model-council-draco/scripts/draco_benchmark.py fetch \
  --output /tmp/draco-test.jsonl

python3 benchmarks/model-council-draco/scripts/draco_benchmark.py sample \
  --input /tmp/draco-test.jsonl \
  --out-dir /tmp/draco-base-sample \
  --count 20 \
  --seed 42
```

Use the first N source rows instead of a random sample:

```bash
python3 benchmarks/model-council-draco/scripts/draco_benchmark.py sample \
  --input /tmp/draco-test.jsonl \
  --out-dir /tmp/draco-first-10 \
  --count 10 \
  --strategy first
```

The script creates:

- `generation-tasks/*.json`: safe inputs for the council.
- `grading-rubrics/*.json`: withheld grader inputs.
- `sample-manifest.json`: selected IDs, source hash, seed, and paths.

For the current public DRACO `test.jsonl`, the task prompt is stored in `problem` and the grading rubric is stored as JSON in `answer`. The prep script keeps `answer` out of generation tasks.

## Base-Level Report Fields

Include these fields in a benchmark report:

```json
{
  "benchmark": "draco",
  "dataset_sha256": "sha256 of fetched jsonl",
  "sample_seed": 42,
  "sample_count": 20,
  "council_level": "base",
  "config_path": "tools/model-council-runner/configs/local-cli.base.json",
  "run_manifest_paths": [],
  "grading_method": "rubric withheld until after generation",
  "notes": []
}
```
