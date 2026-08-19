# Codex Operating Resources

Version: 0.1.0
Last updated: 2026-06-04

Cleaned-up Codex operating resources adapted from an earlier multi-machine setup.

> **Status: Historical public examples.** These files predate the current router, profile, and plugin architecture. Use [the public reference architecture](../../docs/architecture/README.md) for current concepts and treat the examples below as material to adapt, not current Codex defaults.

## What's Here

| Resource | Use It For |
| --- | --- |
| [AGENTS.example.md](AGENTS.example.md) | A dated global `AGENTS.md` example for pragmatic coding-agent defaults. |
| [codex-config-sync-workflow.md](codex-config-sync-workflow.md) | A dated portable example of separating live Codex config from a versioned mirror. |

These are meant to be adapted. The examples deliberately avoid private project names, machine-local paths, secrets, raw session state, and account-specific routing. They do not document current plugin cache resolution, profile generation, or router registry behavior.

## How To Use

Start with [AGENTS.example.md](AGENTS.example.md), remove sections that do not match your workflow, and add only project-agnostic defaults at the global level.

Use [codex-config-sync-workflow.md](codex-config-sync-workflow.md) if you work across multiple machines or Codex installs and want a repeatable way to move reusable instructions, skills, agents, config templates, and setup scripts without copying runtime state.
