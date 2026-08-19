# Validation, drift, and metrics

Validation should match the claim being made.

## Evidence levels

| Evidence | Supports | Does not support |
| --- | --- | --- |
| Structural | Required files, metadata, identifiers, and cross-references are coherent | Usefulness or runtime compatibility |
| Generated consistency | Derived public files match their committed public inputs | Live or private parity |
| Offline fixture | A deterministic helper handles synthetic cases | Real-user acceptance |
| Runtime observed | A named host performed the workflow at a point in time | Other hosts or future versions |
| Clean environment | A documented install and first-run path worked outside the maintainer environment | Universal compatibility |
| Independent evaluation | A separate evaluator exercised declared outcomes | All untested tasks |

The architecture validator runs six positive route-presence cases and nine negative mutation contracts. These are structural contracts, not semantic routing evals.

## Drift process

1. Compare only metadata such as names, versions, hashes, lifecycle state, and validation results.
2. Open a human review item when a public candidate changes.
3. Recheck provenance, private boundaries, current documentation, and claim limits.
4. Update the public source deliberately.
5. Regenerate derived public files.
6. Run the complete public validation suite.
7. Publish only the reviewed diff.

Never auto-copy from a live environment or private mirror.

## Privacy-safe metrics

Useful public maintenance metrics include artifact age, validator status, generated drift, broken links, fixture coverage, and review cadence. Do not publish raw prompts, transcripts, private inventories, user identities, account state, or a one-to-one map from private to public artifacts.
