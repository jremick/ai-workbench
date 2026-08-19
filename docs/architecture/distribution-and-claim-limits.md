# Distribution, governance, and claim limits

AI Workbench uses three publication lanes.

## Publication lanes

1. **Maintained skills** — current public snapshots and curated projections under `skills/`.
2. **Synthetic reference architecture** — schemas, fake registries, templates, fixtures, and validators under `architecture/`.
3. **Historical material** — superseded standalone patterns retained with a successor direction.

The canonical records are [catalog/artifacts.json](../../catalog/artifacts.json) for skills and [catalog/architecture-artifacts.json](../../catalog/architecture-artifacts.json) for architecture.

## Distribution status

Architecture artifacts are `repo-reference` only. Public skills are readable and copyable as standalone packages, but no plugin or clean-environment compatibility guarantee is currently published.

A future distribution field may distinguish:

- `repo-reference`;
- `standalone-skill`;
- `plugin-candidate`;
- `plugin-tested`.

Promotion must be based on corresponding evidence, not intent.

## Review and governance

For each proposed artifact:

1. Identify provenance, license, upstream source, and source revision when applicable.
2. Classify it as a current snapshot, curated projection, illustrative example, or superseded pattern.
3. Review names, paths, examples, references, scripts, assets, and generated output for private coupling.
4. Use synthetic fixtures.
5. Record validation evidence and explicit claim limits.
6. Run boundary, link, catalog, generated-file, and package checks.
7. Review the complete disclosure diff before committing.
8. Keep the repository at public alpha until clean-environment and support evidence justifies a higher stage.

Quarterly review is a useful default, with earlier review when an official product dependency, package validator, or public issue changes the evidence.

## Non-shareable boundary

Do not publish raw profiles, resolutions, registries, route inventories, account or plugin state, provider caches, auth material, hooks, memory, sessions, transcripts, telemetry, private logs, machine identifiers, customer or employer context, or exact private-to-public mappings.

## Claim limits

- Structural validation is not behavioral acceptance.
- Package-authored evals are not independent evidence.
- Runtime observation is environment- and date-specific.
- Official product behavior can change.
- The six-router model and ownership/awareness taxonomy are public reference concepts, not official OpenAI architecture.
