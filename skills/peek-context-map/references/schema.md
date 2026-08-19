# Peek Context Map Schema

Version: 0.1.0
Last updated: 2026-05-24

## Storage

Default map storage is `~/.codex/context-maps/<slug>-<hash>.json`. Repo-local maps may live at `<repo>/.codex/context-maps/<name>.json` when the repo should carry the map.

Do not store maps in reusable skill repos by default. Map data describes a specific context and may contain private structure.

## Top-Level Shape

```json
{
  "version": "0.1",
  "context_id": "repo:https://example/repo.git#subpath",
  "name": "Human label",
  "budget_tokens": 1024,
  "created_at": "2026-05-24T00:00:00Z",
  "updated_at": "2026-05-24T00:00:00Z",
  "fingerprint": {
    "kind": "git",
    "git_root": "/absolute/path",
    "git_head": "abcdef0",
    "sources": []
  },
  "sections": {
    "context_roadmap": [],
    "context_understanding": [],
    "domain_constants": [],
    "parsing_schema": [],
    "reusable_results": [],
    "known_failure_patterns": []
  }
}
```

## Item Shape

```json
{
  "id": "cr-00001",
  "content": "Short source-grounded orientation item.",
  "source_refs": ["/absolute/path/file.md:42"],
  "confidence": 0.8,
  "priority": 50,
  "status": "active",
  "created_at": "2026-05-24T00:00:00Z",
  "updated_at": "2026-05-24T00:00:00Z",
  "last_verified": "2026-05-24T00:00:00Z"
}
```

Allowed statuses: `active`, `stale`, `superseded`.

## Section Prefixes

- `context_roadmap`: `cr`
- `context_understanding`: `cu`
- `domain_constants`: `dc`
- `parsing_schema`: `ps`
- `reusable_results`: `rr`
- `known_failure_patterns`: `kf`

## Operations

The Cartographer should output a JSON object:

```json
{
  "reasoning": "Why these edits improve reusable orientation.",
  "operations": [
    {
      "type": "ADD",
      "section": "context_roadmap",
      "content": "Docs are organized by provider under docs/providers/.",
      "source_refs": ["/repo/docs/providers/README.md:1"],
      "confidence": 0.9,
      "priority": 60
    },
    {
      "type": "REPLACE",
      "item_id": "ps-00002",
      "content": "Records are newline-delimited JSON with fields id, title, status.",
      "source_refs": ["/repo/data/sample.ndjson:1"]
    },
    {
      "type": "DELETE",
      "item_id": "rr-00003"
    }
  ]
}
```

## Budget Priority

When the map exceeds `budget_tokens`, evict lower-value items first:

1. `known_failure_patterns`
2. `parsing_schema`
3. `reusable_results`
4. `context_roadmap`
5. `domain_constants`
6. `context_understanding`

Within a section, evict lower `priority`, lower `confidence`, older `updated_at`, and stale items first.

## Prompt Rendering

The rendered Markdown should fit in the map budget and include only active items unless stale items are explicitly requested. Each item should include its stable ID so later operations can update it.
