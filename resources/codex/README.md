# Codex Operating Resources

Version: 0.1.0
Last updated: 2026-06-04

Cleaned-up Codex operating resources adapted from a working multi-machine setup.

## What's Here

| Resource | Use It For |
| --- | --- |
| [AGENTS.example.md](AGENTS.example.md) | A reusable global `AGENTS.md` template for pragmatic coding-agent defaults. |
| [codex-config-sync-workflow.md](codex-config-sync-workflow.md) | A portable workflow for keeping live Codex config and a versioned sync repo aligned. |

These are meant to be adapted. The examples deliberately avoid private project names, machine-local paths, secrets, raw session state, and account-specific routing.

## How To Use

Start with [AGENTS.example.md](AGENTS.example.md), remove sections that do not match your workflow, and add only project-agnostic defaults at the global level.

Use [codex-config-sync-workflow.md](codex-config-sync-workflow.md) if you work across multiple machines or Codex installs and want a repeatable way to move reusable instructions, skills, agents, config templates, and setup scripts without copying runtime state.
