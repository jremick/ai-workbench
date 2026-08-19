# Artifact System

Use this reference when creating or reviewing the IA/UX/UI redesign artifact package.

## Directory Structure

Create a task-local folder, usually `work/ia-ux-review/` or `work/<date>-ia-ux-review/`:

```text
work/ia-ux-review/
  README.md
  00-executive-brief.md
  01-source-register.md
  02-comparable-products-prior-art.md
  03-current-ia-inventory.md
  04-role-task-page-purpose-map.md
  05-page-element-purpose-ledger.md
  06-audit-findings.md
  07-proposed-ia-route-architecture.md
  08-implementation-lanes.md
  09-agent-task-briefs.md
  10-decisions.md
  11-acceptance-browser-verification.md
  evidence/
    README.md
    browser-notes.md
    screenshots/
```

## Artifact Purposes

- `README.md`: archive index. Explain what each artifact is for, what source state it reflects, and how to use it later.
- `00-executive-brief.md`: short human brief: product frame, top risks, target direction, first lane, verification posture.
- `01-source-register.md`: source-backed evidence log with files, routes, screenshots, live URLs, comparable sources, and access dates.
- `02-comparable-products-prior-art.md`: matrix of comparable products, source links, screenshots, borrowed patterns, and non-transferable patterns.
- `03-current-ia-inventory.md`: current route/page taxonomy, visible sections, owners, actions, loading behavior, and evidence.
- `04-role-task-page-purpose-map.md`: roles, jobs, tasks, expected destination, current destination, friction, and proposed destination.
- `05-page-element-purpose-ledger.md`: page-by-page element inventory: purpose, owner, user, state, action target, and whether it is implementation plumbing.
- `06-audit-findings.md`: prioritized findings with severity, evidence, framework mapping, human impact, fix direction, acceptance check, and uncertainty.
- `07-proposed-ia-route-architecture.md`: target taxonomy, route model, aliases, object pages, page purposes, and migration notes.
- `08-implementation-lanes.md`: safe lanes with scope, files, risks, tests, browser checks, rollback path, and stop rules.
- `09-agent-task-briefs.md`: copyable task packets for implementation agents and sub-agents.
- `10-decisions.md`: decision log with rationale, alternatives, uncertainty, review triggers, and owner/date.
- `11-acceptance-browser-verification.md`: verification matrix for role walkthroughs, browser viewports, a11y, route truth, data states, and evidence.
- `evidence/README.md`: index for screenshots, browser notes, command output summaries, and artifacts.

## Review Modes And Evidence Labels

Use these labels consistently:

- `browser-verified`: rendered UI or live product behavior was inspected directly.
- `file-grounded`: source files, product docs, design artifacts, or tests were inspected, but the UI was not run.
- `prompt-provided`: the user supplied a scenario without repo files or live UI.
- `inferred`: the finding follows from prompt/source structure but was not directly observed.
- `planned`: a browser/accessibility check that should be run later.

Prompt-only packages should still be useful, but their findings must be framed as hypotheses and implementation plans, not verified observations.

## Minimum Fill Levels

For small or prompt-only reviews, fill at least:

- `00-executive-brief.md`
- `01-source-register.md`
- `03-current-ia-inventory.md`
- `04-role-task-page-purpose-map.md`
- `06-audit-findings.md`
- `07-proposed-ia-route-architecture.md`
- `08-implementation-lanes.md`
- `11-acceptance-browser-verification.md`

For full repo or live-product reviews, also fill `02-comparable-products-prior-art.md`, `05-page-element-purpose-ledger.md`, `09-agent-task-briefs.md`, `10-decisions.md`, and the evidence index. If any artifact stays skeletal, note why in `README.md`.

## Required Tables

### Source Register

| ID | Type | Source | Date accessed | Evidence captured | Trust level | Notes |
| --- | --- | --- | --- | --- | --- | --- |

### Current IA Inventory

| Route/Page | Zone | Intended job | Visible contents | Primary actions | Loading/data behavior | Evidence | Friction |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Role Task Page Purpose Map

| Role | Job/task | Expected destination | Current destination | Works? | Friction | Proposed destination |
| --- | --- | --- | --- | --- | --- | --- |

### Element Purpose Ledger

| Page | Element/control | Purpose | Acts on | Target user | State dependency | Keep/move/remove | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Audit Findings

| Severity | Finding | Evidence | Framework/source | Human impact | Fix direction | Acceptance check | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Implementation Lanes

| Lane | Scope | User value | Files/areas | Risk | Tests | Browser checks | Rollback |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Browser Verification Matrix

| Scenario | Role | Route/page | Viewport | Expected evidence | Status | Screenshot/log |
| --- | --- | --- | --- | --- | --- | --- |

## AI-Agent Task Brief Template

```markdown
## Task: <brief title>

### Goal
<One concrete behavioral or IA outcome.>

### Source Of Truth
- <docs/files/routes/screenshots>

### Scope
- In: <files/surfaces>
- Out: <explicit non-goals>

### Required Behavior
- <acceptance bullets>

### Constraints
- <privacy/auth/design-system/source-boundary rules>

### Verification
- <commands>
- <browser walkthroughs>
- <screenshots/evidence>

### Stop Rules
- <when to ask or halt>
```

## Decision Template

```markdown
## YYYY-MM-DD: <decision>

Decision: <chosen path>

Rationale: <why this best serves users/product/constraints>

Alternatives considered:
- <option and why not>

Uncertainty: <what may be wrong>

Review trigger: <when to revisit>
```
