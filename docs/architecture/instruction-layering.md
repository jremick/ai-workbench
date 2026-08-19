# Instruction layering

Instruction layering answers a different question from skill routing: which durable instructions apply before a task-specific workflow is selected?

## Official Codex layer

OpenAI documents `AGENTS.md` discovery from user scope through the active project path. More specific project instructions can refine broader defaults. See [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md).

A public repository should include only contributor-relevant instructions. Personal preferences, private integrations, account state, machine paths, and work-only policy do not belong in a public `AGENTS.md`.

## Reference architecture layer

AI Workbench recommends this separation:

```text
host and organization policy
        ↓
user-level durable instructions
        ↓
repository and directory instructions
        ↓
small domain router metadata
        ↓
one activated skill and its necessary references
```

Durable instructions should carry stable invariants such as safety, source-of-truth, authorization, and verification expectations. Fast-changing provider syntax, plugin paths, route tables, examples, and workflow detail should live in their owning skills, registries, profiles, or references.

## Conflict rule

Resolve conflicts through the host's documented precedence rules. Do not merge incompatible instructions into a new hybrid policy. If the effective instruction set is unclear, stop before an external or destructive action and obtain the missing authority.
