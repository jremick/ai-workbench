---
name: peek-context-map
description: Use when a task asks to create, maintain, inspect, or apply a PEEK-style context map, orientation cache, reusable context map, or bounded memory for repeated work over the same large repo, document set, dataset, manual corpus, research corpus, or other recurring external context. Also use when repeated context-orientation work should be captured without carrying raw chat history.
license: Apache-2.0
---

# Peek Context Map

Version: 0.1.0
Last updated: 2026-05-24

## Purpose

Maintain a small, source-grounded orientation cache for recurring long contexts. The map captures reusable knowledge about a context: what it contains, how it is organized, exact constants and schemas, useful derived results, and known processing pitfalls.

The map is not chat memory, not a task strategy, and not an instruction layer. Treat it as a navigational aid that must be verified against source files when exactness matters.

## When To Use

Use this skill when:

- the user explicitly mentions PEEK, context maps, orientation cache, reusable context knowledge, or bounded memory for a corpus
- multiple tasks query the same large repo, docs corpus, manual set, dataset, paper collection, or external context
- an agent repeatedly rediscovers the same structure, schemas, constants, locations, or parsing rules
- the user asks to warm up, inspect, update, evaluate, or export a map for a recurring context

Do not use this skill for one-off tasks, short contexts that fit easily in one prompt, generic project memory, user preferences, secrets, or work that belongs in host instructions or project documentation.

## Source Of Truth

Store map data separately from the reusable skill:

- Default local maps: `~/.codex/context-maps/` when used with Codex
- Optional repo-local maps: `<repo>/.codex/context-maps/`
- Skill source: this public package directory

Do not bundle map data with the reusable skill or publish context-specific maps by default. Maps may contain private source structure even when they contain no secrets.

## Workflow

1. Resolve the active context.
   - Prefer an explicit user-provided context name or corpus path.
   - For repos, use the git root, remote URL, and current `HEAD` when available.
   - For document sets or datasets, use the directory path plus file fingerprints.
2. Load or initialize the map with `scripts/context_map.py`.
3. Render the map into the prompt only when it helps the current task.
4. Complete the user task normally, verifying exact claims against source files.
5. After the task, identify reusable orientation knowledge from the trajectory.
6. Use the Distiller reference prompt when LLM judgment is needed.
7. Use the Cartographer reference prompt to produce structured operations.
8. Apply operations with the helper script, inspect the diff, then save.
9. Run validation and stale checks before claiming the map is current.

## Helper Script

Use the bundled helper for deterministic operations:

```bash
python3 scripts/context_map.py resolve
python3 scripts/context_map.py init --context-id "repo:example" --source .
python3 scripts/context_map.py render --map ~/.codex/context-maps/<map>.json
python3 scripts/context_map.py validate --map ~/.codex/context-maps/<map>.json
python3 scripts/context_map.py diff-ops --map <map.json> --ops <ops.json>
python3 scripts/context_map.py apply-ops --map <map.json> --ops <ops.json>
python3 scripts/context_map.py stale-check --map <map.json> --source .
```

The helper never calls an LLM and never writes outside the requested map path. It uses approximate token counts for budget enforcement.

## Map Sections

- `context_roadmap`: what documents, folders, sections, tables, or subsystems exist and where to find them
- `context_understanding`: high-level orientation, key entities, concepts, relationships, and domain shape
- `domain_constants`: exact values, formulas, enum sets, output fields, reference ranges, or thresholds defined by the context
- `parsing_schema`: delimiters, record formats, field structures, file patterns, or reliable splitting rules
- `reusable_results`: derived counts, classifications, summaries, or computations likely to help multiple future tasks
- `known_failure_patterns`: factual pitfalls observed while processing this context

## Update Rules

Cache understanding, not answers.

Prefer:

- source-backed structure and locations
- exact constants and schemas
- compact reusable derived results with method notes
- factual pitfalls with source or command evidence

Reject:

- secrets, credentials, tokens, private keys, or personal data not needed for future tasks
- raw transcripts, raw chat history, or long copied excerpts
- generic behavior instructions like "always be careful"
- one-off answers that only solve the current request
- unverified guesses or model-only speculation

## References

Read only the reference needed for the current step:

- `references/schema.md`: map JSON format, operations, section priorities, and storage rules
- `references/distiller-prompt.md`: prompt for extracting reusable orientation candidates from a trajectory
- `references/cartographer-prompt.md`: prompt for converting candidates into `ADD`, `REPLACE`, and `DELETE` operations
- `references/evaluation.md`: lightweight harness for proving the map helps instead of just accumulating text

## Verification

Before claiming the skill was used successfully:

- `validate` passes for the map
- source fingerprints are current or stale entries are explicitly marked
- generated operations were inspected before save unless the user allowed auto-apply
- the rendered map is within budget
- exact claims that matter were verified against source files, not trusted from the map alone
