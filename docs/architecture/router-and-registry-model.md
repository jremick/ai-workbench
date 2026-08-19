# Router and registry model

A registry gives a large skill library one reviewable source for ownership, awareness, routes, and profile eligibility. Router files remain small and task-oriented; generated maps make drift detectable.

## Public fixture flow

```text
minimal-registry.json
    ├── generated-route-map.md
    ├── six synthetic router templates
    ├── profile-resolution.json
    └── smoke and negative contracts
```

The canonical public fixture is [minimal-registry.json](../../architecture/examples/minimal-registry.json). [render_route_maps.py](../../scripts/render_route_maps.py) produces the readable route map. [validate_reference.py](../../scripts/validate_reference.py) checks structure, cross-references, templates, profiles, smoke cases, and negative mutations.

## Registry responsibilities

The public schema records:

- router identity, scope, and routes;
- target skill identity;
- ownership: shared, personal, or work;
- prompt awareness: direct-visible, router-aware, direct-call-aware, or not-aware;
- profile allowlists and enabled skills;
- side-effect class for each route.

A production registry may need more fields, but adding them should follow an evidenced requirement rather than reproduce private implementation detail.

## Generation rule

Generated route maps must come only from the committed public fixture. They must never read a live home directory, private mirror, provider cache, profile resolution, or secret store.

Run:

```bash
python3 scripts/render_route_maps.py
python3 scripts/render_route_maps.py --check
python3 scripts/validate_reference.py
```

Passing these checks proves internal consistency of the synthetic package. It does not prove runtime routing accuracy.
