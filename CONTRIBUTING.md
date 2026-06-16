# Contributing

AI Workbench is a public working collection. Contributions should improve reusable patterns, public-safe examples, docs clarity, or verification coverage.

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
2. State whether the change affects public safety, installability, or verification.
3. Run the relevant local check when one exists.
4. Include before/after context for docs rewrites.

For the model-council package, run:

```bash
python3 scripts/validate_model_council_package.py
```

For the model-manager package, run:

```bash
python3 scripts/validate_model_manager_package.py
```

If no check exists for the changed area, say that in the PR.
