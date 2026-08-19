# Contributing

AI Workbench is a curated public-alpha collection. Contributions should improve reusable patterns, public-safe examples, documentation clarity, lifecycle accuracy, or verification coverage.

## Good Contributions

- Fix broken links, unclear setup steps, or stale references.
- Improve an existing skill, harness, pattern, or example without changing its scope.
- Add sanitized examples, fixtures, or evals that make a workflow easier to test.
- Propose small documentation improvements that help readers adapt an artifact.

## Public Boundary

Do not include:

- real secrets, tokens, private keys, or `.env` files
- local absolute paths or machine-specific setup
- raw chat transcripts, session logs, or memory exports
- employer, customer, client, or private workspace details
- copied proprietary docs or examples without clear reuse rights

Use fake fixture data and generic names when an example needs realism.

## Pull Requests

Keep pull requests narrow:

1. Explain the artifact or workflow you are changing.
2. State whether the change affects publication class, public safety, structural compatibility, or verification.
3. Update `catalog/artifacts.json` when lifecycle, version, relationship, or validation evidence changes.
4. Update `catalog/architecture-artifacts.json` when a synthetic architecture artifact changes.
5. Regenerate `docs/skills.md` and the synthetic route map.
6. Run the default checks and the relevant package-specific checks.
7. Include before/after context for documentation rewrites.

Run the default public-repository checks:

```bash
python3 scripts/validate_public_catalog.py
python3 scripts/render_public_catalog.py --check
python3 scripts/validate_reference.py
python3 scripts/render_route_maps.py --check
python3 scripts/validate_portable_skill_packages.py
python3 scripts/check_markdown_links.py
python3 scripts/check_public_boundaries.py
```

For the model-council package, run:

```bash
python3 scripts/validate_model_council_package.py
```

For the model-manager package, run:

```bash
python3 scripts/validate_model_manager_package.py
```

The deterministic-controls, agent-memory, and war-council packages also have focused checks documented in their READMEs.

Validation has bounded claims. Structural checks do not prove usefulness, security, output quality, or compatibility with every host. If no behavioral or independent check exists for the changed area, say that in the pull request.
