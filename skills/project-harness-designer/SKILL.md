---
name: project-harness-designer
description: Use whenever the user starts a new project, initiative, repo, app, tool, research effort, reusable skill, local integration, or other substantial build by giving a goal, desired outcome, constraints, requirements, success criteria, or what good looks like. Design the smallest effective project operating harness before execution: intent, success evidence, failure modes, work mode, structure, verification loop, and first execution path.
version: 0.4.0
last_updated: 2026-06-04
status: public-ready
---

# Project Harness Designer

Design the operating harness for a new project before executing inside it.

The user should only need to describe the project goal, desired outcome, constraints, or success criteria. The agent should then choose the smallest structure that makes success likely without turning the work into ceremony.

## Core Rule

When a substantial new project starts, design the project harness first, then execute.

A project harness is the practical operating structure that helps the work reach the right result. It can be a short plan, a repo scaffold, a research workflow, an eval harness, a build/test/deploy loop, project instructions, or the solution itself when no durable scaffold is needed.

Always ask:

> What is the minimum operating harness that makes success likely, and what would be overkill?

## Use When

Use this skill when the user:

- starts a new project or initiative
- describes a goal plus what good looks like
- asks to set up, bootstrap, scaffold, initialize, or prepare a project
- gives success criteria, required outcomes, constraints, or requirements for a new build
- wants a durable repo, skill, app, research project, integration, automation, or workflow
- asks the agent to understand what they are trying to achieve before building

Do not use it for a trivial command, a small edit, a narrow bug fix, or a one-off answer where the existing project harness is already clear.

## Harness Workflow

1. Model intent.
   - Restate what the user is trying to achieve.
   - Name the audience, user, or operating context when it matters.
   - Surface assumptions that affect the harness.

2. Translate success into evidence.
   - Separate what good looks like from proof that it is good.
   - Define acceptance checks, tests, evals, demos, read-backs, screenshots, live checks, or review gates.

3. Model likely failure modes.
   - Ask what would make the project look busy but fail.
   - Watch for unclear goals, wrong abstraction, over-scaffolding, weak validation, stale source of truth, hidden auth/deploy constraints, subjective quality bars, or context loss across sessions.

4. Choose the work mode.
   - Direct build: small, clear, low-risk.
   - Plan then build: moderate scope with known implementation path.
   - Research first: domain, vendor, or feasibility is uncertain.
   - Scaffold first: durable repo/workspace/lifecycle is needed.
   - Eval first: quality is subjective or model/output dependent.
   - Prototype first: product, UX, or technical feasibility is uncertain.
   - Ops harness first: auth, deployment, live systems, monitoring, or external writes dominate risk.

5. Design the minimum harness.
   - Include only structure that improves execution or verification.
   - Prefer existing repo conventions, helper scripts, validators, and local patterns.
   - Include continuity artifacts when work will span sessions, decisions, or reusable learning.
   - Include hooks when a repeated check, safety gate, or closeout reminder prevents drift.
   - Include right-sized documentation, with diagrams or screenshots when they make workflows, architecture, or evidence easier to understand.

6. Pick the first execution path.
   - Name the first milestone.
   - Identify what to build, research, verify, or scaffold first.
   - Define stop conditions before sensitive writes, destructive operations, external-system changes, or irreversible publication.

## Output Format

For normal projects, keep the harness compact:

```markdown
**Intent**
<what the user is really trying to achieve>

**Good Means**
<user-visible success criteria>

**Evidence**
<how success will be proven>

**Risks**
<ways the work could look busy but fail>

**Work Mode**
<direct build, research first, scaffold first, eval first, prototype first, ops harness first, or plan then build>

**Minimum Harness**
<the smallest useful structure or loop>

**First Path**
<next concrete step and stop conditions>
```

For tiny projects, compress this into a few sentences and proceed. For larger projects, expand only the parts that change execution quality.

## Harness Components

Use only what the project actually needs:

- Source of truth: repo, issue, live system, document, dataset, API, or user-provided prompt.
- Success evidence: tests, evals, screenshots, checks, review gates, examples, or user acceptance.
- Work mode: research, scaffold, prototype, eval, ops, or direct build.
- Continuity: README, decision log, learning notes, closeout note, or handoff summary.
- Hooks: preflight, pre-write, test, secret scan, build, deploy, sync, documentation, or closeout checks.
- Documentation: usage instructions, architecture notes, diagrams, examples, limitations, and maintenance notes.

## Anti-Patterns

Avoid:

- project-management ceremony for small work
- generic plans that do not define evidence
- scaffolding before the success criteria are clear
- running straight into implementation when domain, auth, data, deploy, or quality constraints are unknown
- treating subjective quality as verified without examples, screenshots, evals, or user review
- mixing private state, secrets, raw logs, or local runtime details into reusable artifacts

## Verification

Before moving from harness into execution, confirm:

- the source of truth is named
- the success evidence can actually be checked
- the main failure modes are visible
- the work mode fits the uncertainty and risk
- the harness is smaller than the work it supports
- the first execution path is concrete
- stop conditions are explicit for privacy, auth, destructive actions, live systems, and publication

## Proof Summary

The source skill was evaluated with a 33-case project-start suite before public packaging. The public package includes a proof summary in `docs/evaluation.md` rather than raw local run data.
