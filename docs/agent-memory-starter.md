# Agent Memory Starter

Version: 1.0.0
Last updated: 2026-06-04

Agent Memory Starter is a public-safe reference package for building durable memory for AI agents.

It packages a source-backed memory pattern around pages, timeline entries, searchable chunks, update proposals, and retrieval evals. The point is to make memory auditable and testable instead of storing raw transcripts and hoping retrieval works.

## Public Angle

Most agent memory demos focus on "save everything and retrieve something similar." This package focuses on operational memory:

- current truth is compiled into pages
- dated evidence is preserved in timeline entries
- retrieval chunks are derived from curated memory
- updates are proposed before becoming durable truth
- search quality has fixture evals
- examples are fake and safe to share

## Package Contents

| Artifact | Link | Purpose |
| --- | --- | --- |
| Skill | [skills/agent-memory-starter](../skills/agent-memory-starter/README.md) | Agent-facing guidance for designing and operating memory. |
| Starter kit | [tools/agent-memory-starter](../tools/agent-memory-starter/README.md) | Schema, Edge Function, CLI, fixtures, and evals. |
| Architecture notes | [tools/agent-memory-starter/docs/architecture.md](../tools/agent-memory-starter/docs/architecture.md) | Data model, trust boundaries, and production hardening checklist. |
| Fixture eval | [tools/agent-memory-starter/scripts/run_fixture_eval.py](../tools/agent-memory-starter/scripts/run_fixture_eval.py) | Deterministic local retrieval test with fake data. |

## Quickstart

Run the public fixture eval:

```bash
python3 tools/agent-memory-starter/scripts/run_fixture_eval.py
```

Then inspect the starter kit:

```text
tools/agent-memory-starter/
```

The eval does not need Supabase, OpenAI, or any secrets.

## What Is Deliberately Excluded

This package does not include:

- private memory exports
- raw chat logs
- live database identifiers
- local machine paths
- secret references
- personal project data

The public version is a generalized implementation pattern with fake fixtures.

## Verification

Run the fixture eval:

```bash
python3 tools/agent-memory-starter/scripts/run_fixture_eval.py
```

This verifies the starter kit against fake data and does not need Supabase, OpenAI, or any secrets.
