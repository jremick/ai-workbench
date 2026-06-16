<h1 align="center">AI Workbench</h1>

<p align="center">
  <strong>Reusable skills, harnesses, agent patterns, frameworks, and resources for practical agentic AI work.</strong>
  <br/>
  A selective working collection for keeping agents scoped, verifiable, and useful outside one private workspace.
</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-Apache_2.0-blue.svg"/></a>
  <img alt="Status" src="https://img.shields.io/badge/status-public_working_collection-2f6f5f.svg"/>
  <a href="docs/skills.md"><img alt="Skills" src="https://img.shields.io/badge/skills-catalog-5964a8.svg"/></a>
  <a href="resources/README.md"><img alt="Resources" src="https://img.shields.io/badge/resources-available-8a6f2a.svg"/></a>
</p>

<p align="center">
  <img src="assets/workbench-map.svg" alt="AI Workbench artifact map" width="880"/>
</p>

> **Status:** AI Workbench is a public, evolving collection. The artifacts are usable and Apache-2.0-licensed, but this is not a packaged product; individual skills, tools, and examples may change as the patterns mature.

> Built and maintained by [Jarel Remick](https://github.com/jremick).

## What is AI Workbench?

AI Workbench collects reusable AI operating artifacts: agent skills, project harnesses, workflow patterns, model-council tools, adoption frameworks, starter kits, diagrams, fixtures, and public-safe examples.

Most of it came from repeated use: keeping agents scoped, designing project harnesses, managing context, choosing verification paths, and moving deterministic work out of prompts and into code or checks.

This is a selective working collection, not a prompt dump.

## Why this exists

- **Reusable agent work** - turn repeated operating patterns into skills, templates, checks, and small tools.
- **Public-safe examples** - keep the reusable pattern while removing private workspace details, secrets, local paths, and raw session history.
- **Verification-first habits** - pair agent workflows with the smallest credible proof path: evals, validators, read-backs, fixtures, screenshots, or documented manual checks.
- **Higher-level project harnesses** - make broad agentic work concrete enough to start, delegate, inspect, and finish.

## Quick start

Clone the repo and start from the catalog that matches what you want to adapt:

```bash
git clone https://github.com/jremick/ai-workbench.git
cd ai-workbench

# Optional sanity checks for the package families with validators.
python3 scripts/validate_model_council_package.py
python3 scripts/validate_model_manager_package.py
```

Then browse by category:

| Group | What's in it | Where to look |
| --- | --- | --- |
| Frameworks | Models and worksheets for thinking about AI adoption, maturity, and operating constraints. | [SMB AI Maturity Model](frameworks/smb-ai-maturity-model/README.md) |
| Patterns | Reusable workflow shapes for splitting, routing, verifying, and repeating agent work. | [Agent Workflow Patterns](patterns/agent-workflow-patterns/README.md) |
| Skills | Reusable instructions for recurring agent work: writing, triage, diagramming, auth handling, MCP work, model routing, model councils, research, and context boundaries. | [skills](skills/) and [docs/skills.md](docs/skills.md) |
| Harnesses | Operating patterns for starting projects, composing nested work, routing verification, and keeping larger agent tasks coherent. | [harness-first-project-coach](skills/harness-first-project-coach/README.md), [project-harness-designer](skills/project-harness-designer/README.md), [harness-composer](skills/harness-composer/README.md), [verification-harness-router](skills/verification-harness-router/README.md) |
| Agents and plugins | Patterns for delegation, sidecar agents, MCP servers, tool boundaries, and context packets. | [nested-agent-orchestrator](skills/nested-agent-orchestrator/README.md), [mcp-build](skills/mcp-build/README.md), [context-boundary-designer](skills/context-boundary-designer/README.md) |
| Benchmarks | Dataset prep and scoring harnesses for evaluating skills and agent workflows. | [Model Council DRACO Benchmark](benchmarks/model-council-draco/README.md) |
| Resources | Starter kits, examples, diagrams, eval fixtures, and reference docs that make the patterns easier to adapt. | [AGENTS example](resources/codex/AGENTS.example.md), [Codex sync workflow](resources/codex/codex-config-sync-workflow.md), [resources](resources/) |

Most artifacts have their own README with usage notes, examples, and the smallest useful check or fixture.

## Notable

### Project Harness Designer

[Project Harness Designer](skills/project-harness-designer/README.md) turns a fuzzy project start into a compact operating frame: intent, success evidence, risks, work mode, verification loop, and first path. It is the pattern I reach for when a request is bigger than a single edit but does not need heavyweight project planning.

### Harness-First Project Coach

[Harness-First Project Coach](skills/harness-first-project-coach/README.md) is the earlier coaching layer for substantial starts. It clarifies material questions, reframes the goal, maps support skills, defines context boundaries, and chooses the first evidence-backed lane before implementation.

### Agent Memory

[Agent Memory Starter](docs/agent-memory-starter.md) is a source-backed memory pattern for agents. It uses curated pages, timeline evidence, searchable chunks, update proposals, fake fixtures, and a retrieval eval so memory can be inspected and tested instead of becoming a transcript pile.

### Model Council and Deep Research

[Model Council](skills/model-council/README.md) runs independent model workers and a separate synthesis pass, with local CLI routes for Codex, Claude Code, Antigravity, and Grok Build plus a Vercel AI Gateway option. [Deep Research](skills/deep-research/README.md) keeps source-backed research disciplined and escalates difficult synthesis to the council pattern. The companion [runner](tools/model-council-runner/README.md) supports dry-run planning, manifests, and route validation. [Model Council DRACO Benchmark](benchmarks/model-council-draco/README.md) is a separate benchmark package for evaluating the council skill.

### Model Manager

[Model Manager](skills/model-manager/README.md) is a public-alpha skill and deterministic CLI for choosing when model delegation is worthwhile, selecting a role-stack route, and preserving parent-owned execution. It includes sanitized benchmark-derived recommendation values, Artificial Analysis attribution notes, DeepSWE-aware long-horizon coding policy, evals, tests, and a package validator.

### War Council

[War Council](skills/war-council/README.md) is a decision harness for uncomfortable tradeoffs. It uses advisor personas, weighted scoring, forced $100 allocation, and a deterministic aggregate script to preserve agreements, disagreements, risks, kill criteria, and the final decision ledger.

### Meta-Harnesses

The meta-harness pieces are for shaping larger agent workflows: [Harness Composer](skills/harness-composer/README.md) for parent and child workstreams, [Nested Agent Orchestrator](skills/nested-agent-orchestrator/README.md) for delegation, [Verification Harness Router](skills/verification-harness-router/README.md) for choosing checks, and [Context Boundary Designer](skills/context-boundary-designer/README.md) for deciding what context belongs where.

### Agent Workflow Patterns

[Agent Workflow Patterns](patterns/agent-workflow-patterns/README.md) is a diagram-backed catalog for choosing classify-and-act, fan-out-and-synthesize, adversarial verification, generate-and-filter, tournament, loop-until-done, and quarantine-and-act workflows.

### Deterministic Controls

[Deterministic Controls](skills/deterministic-controls/README.md) helps decide when model judgment is the wrong tool. It pushes exact formats, permission gates, routing, retries, release checks, and auditability into schemas, state machines, validators, tests, or other deterministic controls.

### Codex Operating Resources

[AGENTS example](resources/codex/AGENTS.example.md) is a cleaned-up global instruction template for pragmatic coding-agent defaults. [Codex sync workflow](resources/codex/codex-config-sync-workflow.md) covers the live-home versus versioned-mirror pattern for keeping reusable Codex instructions, skills, agents, config templates, and setup scripts aligned across machines.

## Documentation

- [Skills catalog](docs/skills.md) - installable public skills and starting points.
- [Patterns](patterns/README.md) - reusable workflow shapes.
- [Resources](resources/README.md) - starter kits, templates, and reference material.
- [Model Council and Deep Research](docs/model-council-and-deep-research.md) - council workflow, routing, and benchmark notes.
- [Model Manager](skills/model-manager/README.md) - role-based model routing, benchmark-aware policy, and validation commands.

## Community and support

- [Issues](https://github.com/jremick/ai-workbench/issues) - bugs, broken links, unclear docs, and concrete improvement ideas.
- [Contributing](CONTRIBUTING.md) - how to propose public-safe changes.
- [Security policy](SECURITY.md) - how to report private or sensitive findings.

## License

[Apache License 2.0](LICENSE) - Copyright 2026 Jarel Remick.
