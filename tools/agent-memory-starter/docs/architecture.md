# Architecture

Version: 1.0.0
Last updated: 2026-06-04

## Purpose

Agent Memory Starter is a small reference architecture for durable AI agent memory.

It is designed for memory that should survive a session and help future agents act with better context. It is not designed for raw transcript storage, user tracking, or unrestricted model-writeable state.

## Data Model

| Table | Role |
| --- | --- |
| `sources` | Pointer-based provenance for curated summaries, docs, tickets, decisions, or imports. |
| `pages` | Durable concepts with current compiled truth. |
| `timeline_entries` | Dated evidence and changes attached to pages. |
| `chunks` | Searchable units derived from pages, timeline entries, or source notes. |
| `memory_update_proposals` | Review queue for proposed changes. |

## Retrieval Flow

1. The agent asks a question.
2. The client calls the Edge Function with `text_search` or `query`.
3. `text_search` uses Postgres full-text search and trigram similarity.
4. `query` creates a query embedding and blends vector similarity with text score.
5. Results return page slug, title, scope, sensitivity, chunk type, content, source pointer, and score.
6. The agent opens the page bundle when it needs more evidence before answering or acting.

## Write Flow

Default to proposals:

1. Search first to avoid duplicate memory.
2. Submit `propose_update` with target slug, change type, source URI, sensitivity, and reason.
3. A reviewer or trusted workflow promotes the proposal into page, timeline, and chunk updates.
4. Run embedding backfill.
5. Run retrieval evals.

Direct writes are intentionally not included in the public Edge Function. Add them only after defining approval, audit, and rollback rules.

## Trust Boundaries

| Boundary | Control |
| --- | --- |
| Function caller | `x-agent-memory-token` shared secret or a stronger deployment-specific auth layer. |
| Database access | Service-role calls stay inside the Edge Function. |
| Model output | Durable writes go through proposals by default. |
| Public examples | Fixture corpus is fake and sanitized. |
| Search quality | Fixture evals run without live credentials. |
| Secrets | Secrets are read from runtime environment variables and are never written to repo files. |

## Operational Notes

- Use text-only search as a fallback when embeddings are delayed.
- Keep a sensitivity field even for private deployments.
- Keep source pointers short. Store the source elsewhere, not inside memory rows.
- Store current truth separately from dated evidence so stale decisions can be corrected without erasing history.
- Evaluate ranking on realistic queries before trusting memory in an autonomous workflow.

## Production Hardening

Before production use, add:

- deployment-specific authentication and authorization
- row-level access policies if more than one trust group uses the same database
- proposal review UI or review automation
- deletion and archive workflow
- backup and export workflow
- structured logs with redaction
- rate limits and request size limits
- monitoring for embedding failures and stale chunks
- CI checks for schema migrations, function type checks, and fixture evals

## Known Limits

- The starter uses one embedding model and dimension by default.
- Fixture evals use deterministic lexical scoring, not live semantic embeddings.
- The Edge Function is a compact reference implementation, not a full admin API.
- The schema grants service-role access for server-side use. Adjust grants and exposed schemas for your deployment model.
