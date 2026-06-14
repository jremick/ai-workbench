# Diagramming

`diagramming` helps choose and produce the right text-defined diagram for the destination.

It is intentionally neutral: no private brand theme, no work-specific palette, and no local rendering assumptions.

## Install

Copy this directory into your agent skill directory:

```text
skills/diagramming/
```

The minimum install is `SKILL.md`. Keep `examples/` for starter snippets.

## Try It

```text
Use diagramming to create a simple architecture diagram for this agent workflow. It will live in a README first, but may later become a slide.
```

The skill should start in Mermaid for the README version and suggest D2 only if the diagram becomes a polished reusable asset.

## Included Examples

- [Mermaid workflow](examples/workflow.mmd)
- [D2 workflow](examples/workflow.d2)

## Public Readiness

This public version was rewritten from a private diagramming skill to remove private brand names, private palettes, local render wrappers, and work-specific writing routes.
