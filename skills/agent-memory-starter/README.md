# Agent Memory Starter

`agent-memory-starter` helps design a durable, source-backed memory layer for AI agents.

It is for teams and builders who want memory that is auditable and testable, not a private pile of raw chat logs.

## Install

Copy this directory into your agent skill directory:

```text
skills/agent-memory-starter/
```

Keep the companion starter kit when you want schema, function, CLI, and eval examples:

```text
tools/agent-memory-starter/
```

## Try It

```text
Use agent-memory-starter to design a memory layer for an AI coding assistant. It should remember durable project decisions, avoid raw chat logs, and support update proposals.
```

## Companion Kit

The companion kit includes:

- Postgres schema for pages, sources, timeline entries, chunks, and proposals
- Supabase Edge Function for private search, backfill, page reads, stats, and proposals
- CLI wrapper for calling the Edge Function
- fake fixture corpus and deterministic retrieval eval

Start at:

```text
tools/agent-memory-starter/README.md
```

## Run The Eval

From the repo root:

```bash
python3 tools/agent-memory-starter/scripts/run_fixture_eval.py
```

Expected result:

```json
{
  "passed": true
}
```

## Public Readiness

This public package uses fake fixture data. It does not include private memories, raw sessions, live project identifiers, local machine paths, secrets, or credential references.
