---
name: agent-memory-starter
description: Use when designing, reviewing, or bootstrapping a source-backed memory layer for AI agents. Focus on durable facts, provenance, retrieval quality, privacy boundaries, update proposals, and eval-backed search rather than raw transcript storage.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# Agent Memory Starter

Use this skill to design or operate a durable memory layer for AI agents.

The goal is not to remember everything. The goal is to preserve reusable, source-backed knowledge that helps future agents answer and act with less guesswork.

## Core Model

A practical agent memory system has four layers:

- Pages: durable concepts such as projects, systems, people, preferences, decisions, runbooks, and workflows.
- Timeline entries: dated evidence, decisions, reversals, and meaningful changes.
- Chunks: searchable text derived from pages, timeline entries, and source-backed notes.
- Proposals: pending memory updates that need review before becoming durable truth.

Keep these separate. Compiled truth should be concise and current. Timeline entries should preserve what changed and why. Search chunks should optimize retrieval without becoming raw log storage.

## Source Boundary

Use memory for stable knowledge:

- project status that will matter in future work
- system architecture and operational boundaries
- user preferences that should carry across sessions
- decisions, reversals, and lessons with source evidence
- reusable workflow patterns and verification contracts

Do not store:

- secrets, tokens, private keys, or credential references
- raw chat logs, raw transcripts, or full session dumps
- private browsing history or unrelated personal details
- customer, employer, or regulated material without a specific public-safe process
- transient task state that will not matter after the current session

When in doubt, create a proposal instead of writing durable memory.

## Design Workflow

1. Name the memory purpose: personal assistant memory, product support memory, team knowledge memory, or agent operations memory.
2. Define the allowed source classes and the classes that are explicitly forbidden.
3. Choose the storage model: pages, timeline entries, chunks, sources, and proposals.
4. Add provenance fields before adding embeddings.
5. Add retrieval over both text and vectors.
6. Add a deterministic search-quality eval with fake or sanitized fixtures.
7. Add an update workflow that can be reviewed, rejected, or corrected.
8. Add export and deletion paths before relying on the system.

## Retrieval Rules

Good retrieval should be:

- source-backed: every returned memory can point to a source or curated summary
- scoped: queries can include or exclude personal, team, shared, or public memory
- auditable: timeline evidence and source metadata are inspectable
- evaluated: search has fixture cases that fail when ranking regresses
- privacy-aware: sensitive memories do not leak into public examples or generic docs

Prefer hybrid retrieval. Text search catches exact names and paths. Vector search helps with paraphrases and conceptual questions. Keep a text-only fallback so the system can still work when embeddings are delayed or disabled.

## Update Rules

Do not let the model silently rewrite durable memory.

Use this sequence:

1. Search first to avoid duplicate pages.
2. Identify the target page slug and scope.
3. Classify sensitivity.
4. Propose the update with source evidence.
5. Review the proposal before changing compiled truth.
6. Add or refresh chunks.
7. Backfill embeddings.
8. Run retrieval evals and a targeted read-back.

For low-risk solo systems, an agent may apply approved update types directly. For team or public systems, keep review explicit.

## Starter Kit

This repo includes a public-safe starter kit at:

```text
tools/agent-memory-starter/
```

Use it as a reference implementation for:

- a Postgres schema with pages, sources, timeline entries, chunks, and proposals
- a Supabase Edge Function that performs auth, embedding, search, stats, page reads, and proposal writes
- a small CLI wrapper for calling the function
- fake fixture memory and deterministic search evals

Treat the starter as a base, not a complete product. Production systems still need deployment-specific auth, retention, redaction, access control, observability, and deletion workflows.

## Verification

Before claiming an agent memory system is ready:

- the source boundary and forbidden data classes are documented
- fixture evals pass without live secrets
- search returns source-backed results for exact and paraphrased queries
- failed auth returns a clear unauthorized response
- update proposals can be inspected before promotion
- sensitive fields are redacted from logs and errors
- public examples contain only fake or sanitized data
- a deletion or archive path exists for mistaken memories

For this public package, run:

```bash
python3 tools/agent-memory-starter/scripts/run_fixture_eval.py
```
