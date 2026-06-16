# Skills

Version: 0.3.2
Last updated: 2026-06-17

This directory collects installable agent skills that are intended to be useful outside any private workspace.

Each public skill should include:

- `SKILL.md`: installable skill instructions with YAML frontmatter.
- `README.md`: human-facing usage notes, install guidance, and safety notes.
- examples, evals, scripts, or references only when they are sanitized and useful.

## Recommended Starting Points

| Skill | Use It For | Why It Is Here |
| --- | --- | --- |
| [What's The Point](../skills/whats-the-point/README.md) | Distilling dense material into decision-ready signal. | A practical, easy-to-test skill with evaluation coverage. |
| [Make My Point](../skills/make-my-point/README.md) | Sharpening rough writing for a specific audience and decision. | Pairs with What's The Point as an evaluated communication workflow. |
| [Harness-First Project Coach](../skills/harness-first-project-coach/README.md) | Clarifying substantial AI or software starts before implementation. | Adds Q&A, support-skill selection, context boundaries, and a first-lane evidence loop before building. |
| [Project Harness Designer](../skills/project-harness-designer/README.md) | Starting substantial projects with intent, proof, risks, and a first execution path. | A reusable operating pattern for agent-assisted project starts. |
| [Deterministic Controls](../skills/deterministic-controls/README.md) | Deciding which agent behavior belongs in code, schemas, gates, and tests. | A reliability skill with a portable eval harness. |
| [Model Council](../skills/model-council/README.md) | Running independent model workers and synthesizing their outputs with disagreement preserved. | Generalizes a multi-model council pattern with deterministic local CLI and hosted API routes. |
| [Model Manager](../skills/model-manager/README.md) | Choosing explicit role-stack routes, delegation policy, and model settings before provider execution. | Packages benchmark-aware routing policy with evals, tests, sanitized recommendation values, and public attribution notes. |
| [War Council](../skills/war-council/README.md) | Making uncomfortable decisions with advisor personas, weighted scoring, forced allocation, and an audit ledger. | Converts subjective advice into traceable tradeoffs, disagreement, and reversal criteria. |
| [Deep Research](../skills/deep-research/README.md) | Source-backed research with citation discipline, uncertainty tracking, and council escalation. | A reusable research workflow that pairs clean source handling with council escalation. |
| [Diagramming](../skills/diagramming/README.md) | Choosing and producing diagrams for docs, architecture, workflows, and presentations. | Converts diagram requests into a clear Mermaid-or-D2 workflow. |
| [Codex Workflow Harvest](../skills/codex-workflow-harvest/README.md) | Turning repeated agent workflow lessons into durable skills, helpers, or instructions. | Captures an improvement loop without publishing private memory. |
| [MCP Build](../skills/mcp-build/README.md) | Building and reviewing Model Context Protocol servers. | Encodes practical MCP server boundaries, testing, auth, and docs checks. |
| [Auth Handling](../skills/auth-handling/README.md) | Choosing safe local secret and credential handling patterns. | Documents least-exposure auth routing without shipping secrets or machine-local helpers. |
| [Agent Memory Starter](../skills/agent-memory-starter/README.md) | Designing source-backed, eval-checked memory for AI agents. | Packages a memory pattern with fake fixtures, schema, function, CLI, and retrieval evals. |
| [Harness Composer](../skills/harness-composer/README.md) | Composing complex projects into parent and child harnesses. | Makes nested harness work concrete, bounded, and independently verifiable. |
| [Nested Agent Orchestrator](../skills/nested-agent-orchestrator/README.md) | Deciding when and how to use sub-agents or sidecar models. | Keeps delegation explicit, scoped, and parent-verified. |
| [Verification Harness Router](../skills/verification-harness-router/README.md) | Choosing the smallest credible proof path for agent claims. | Routes readiness claims to tests, evals, screenshots, read-backs, scans, or review gates. |
| [Context Boundary Designer](../skills/context-boundary-designer/README.md) | Deciding what context belongs in parent, child, memory, docs, evals, and public artifacts. | Prevents context bloat and private-context leakage in nested workflows. |

## Installation Pattern

Most agent skill runtimes use a directory-per-skill layout:

```text
skills/
  skill-name/
    SKILL.md
    README.md
    references/
    scripts/
    evals/
```

Copy only the skill directory you need into your agent's configured skill directory. Keep examples and evals when you want to understand or test behavior; keep only `SKILL.md` when you need the lightest install.

## Public Boundary

Public skills in this repo avoid:

- private workspace names
- local absolute paths
- customer or employer material
- raw logs, transcripts, session exports, or memory dumps
- secrets, tokens, secret references, or credential values

When a live internal skill had private examples or local helpers, the public version was rewritten around a clean pattern instead of copied directly.
