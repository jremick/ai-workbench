# Synthetic reference architecture

This directory contains a self-contained public example of a six-router skill architecture. Every identifier, profile, target skill, and route is synthetic.

## Start here

- [Registry schema](schema/router-registry-v1.schema.json)
- [Minimal registry](examples/minimal-registry.json)
- [Generated route map](examples/generated-route-map.md)
- [Synthetic profile resolution](examples/profile-resolution.json)
- [Router templates](examples/routers/README.md)
- [Positive structural cases](evals/smoke-cases.json)
- [Negative mutation contracts](evals/negative-contracts.json)
- [Architecture documentation](../docs/architecture/README.md)

## Validate

```bash
python3 scripts/validate_reference.py
python3 scripts/render_route_maps.py --check
```

These checks establish public-fixture consistency only. They do not inspect a live Codex environment or prove runtime routing, activation, plugin compatibility, or clean-environment installation.
