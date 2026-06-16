# Support Skill Map

Version: 1.1.2
Last updated: 2026-06-17

Use this reference when a harness-first start needs supporting skills, workflows, validators, or docs.

## Decision Rule

Do not assume the first referenced skill is the right dependency.

Ask:

1. What capability does the goal actually need?
2. Does an existing skill or repo workflow already cover it?
3. Is the existing skill published, local-only, external, or missing?
4. Should the current task use it, link it, publish it, or create something new?
5. Is the need reusable enough to justify another skill, or is it only project-specific context?

## Preferred Order

1. Use an existing public or locally available skill when it fits.
2. Use a repo workflow or validator when it owns the evidence.
3. Link to external guidance only when this repo does not own the pattern.
4. Propose publishing a missing skill only when others will reuse it.
5. Propose creating a new skill only when no existing skill or lightweight project doc covers the repeatable work.

## Support Skills In AI Workbench

| Need | Skill | Repo path | Use when |
| --- | --- | --- | --- |
| Executable project-start harness | `project-harness-designer` | `skills/project-harness-designer/` | The next output should be the actual operating harness for a project, repo, research effort, app, automation, or reusable artifact. |
| Complex parent/child harness map | `harness-composer` | `skills/harness-composer/` | The work needs nested workstreams, sidecars, public artifacts, or integration gates. |
| Context boundary | `context-boundary-designer` | `skills/context-boundary-designer/` | The harness needs to decide what context belongs in parent, child, memory, docs, evals, or public artifacts. |
| Verification routing | `verification-harness-router` | `skills/verification-harness-router/` | The evidence path is unclear or multiple proof types are possible. |
| Deterministic controls | `deterministic-controls` | `skills/deterministic-controls/` | The harness needs schemas, policy gates, state machines, validators, tests, or auditability. |
| Diagram routing | `diagramming` | `skills/diagramming/` | The work needs a reusable visual diagram and the diagram type or format is not obvious. |
| Workflow harvesting | `codex-workflow-harvest` | `skills/codex-workflow-harvest/` | A repeated workflow should become a durable public-safe skill, helper, or instruction. |

## Output Pattern

When support skills matter, include:

```markdown
- Support skills: Use `<skill>` for `<reason>`; skip `<skill>` because `<reason>`; propose `<new skill>` only if `<reusable gap>`.
```

When no support skill is needed, say:

```markdown
- Support skills: None. A short plan plus verification check is enough.
```
