---
name: harness-first-project-coach
description: "Coach and critique Harness-First Project Design for substantial AI or software starts, ambiguous initiatives, team training, reusable skill or workflow design, and project bootstrap reviews. Use when the work should design the operating harness before implementation: goal altitude, source of truth, context boundary, minimum project scaffold, first execution lane, verification loop, and reusable learning."
license: Apache-2.0
---

# Harness-First Project Coach

Version: 1.1.2
Last updated: 2026-06-17
Status: public-alpha

Use this skill to start substantial work by designing the operating harness before building the solution.

The process name is `Harness-First Project Design`.
The visual teaching model is the `Nested Harness Model`.

## Core Rule

Design the smallest operating structure that makes the real goal clear, executable, verifiable, restartable, and improvable.

Do not use the full process for trivial tasks. If the work is small, local, and reversible, say that a full harness is overkill and act directly.

## Workflow

1. Run the material Q&A gate.
   - Clarify the goal, desired outcomes, success criteria, solution constraints, assumptions, environment constraints, source of truth, and stop conditions.
   - Ask focused questions only when the answer materially changes the harness or avoids a bad start.
   - If the first step is safe and reversible, state assumptions and proceed instead of blocking on broad questions.

2. Diagnose altitude.
   - Restate the highest practical goal.
   - Identify whether the user's framing is too low, too broad, or right-sized.
   - Name the real category of work, not only the surface tool, app, or document.

3. Ground the source of truth.
   - Identify the repo, document, live system, dataset, brief, or stakeholder input that owns current facts.
   - Inspect it before designing when it is available.
   - Separate evidence from inference.

4. Set boundaries.
   - Capture constraints, non-goals, privacy boundary, auth boundary, reversibility, and stop conditions.
   - Resolve or record material assumptions from the Q&A gate.

5. Map support skills.
   - Ask what existing skills, repo workflows, validators, or docs should support the goal.
   - Prefer using an existing published or locally available skill when it fits.
   - Propose publishing, mirroring, or creating another skill only when the current goal needs a missing reusable capability.

6. Design the minimum harness.
   - Include only structures that reduce execution risk or improve verification.
   - Consider project instructions, goal/backlog docs, decision records, tests, evals, scripts, diagrams, telemetry, live readbacks, or session state.
   - Avoid ceremony when a short plan and one verification check are enough.

7. Manage context.
   - Decide what to load now, what to point to, what to defer, and what to exclude.
   - Keep entrypoints small and load detail progressively.

8. Pick one lane.
   - Define the first narrow research or implementation path.
   - Use Plan-Execute-Verify for that lane.
   - Park adjacent ideas instead of expanding scope.

9. Close the loop.
   - Compare output against goal, constraints, failure modes, and evidence.
   - Capture only reusable learning in the right artifact.

## Output Contract

For a normal project-start coaching pass, return:

```markdown
**Harness-First Goal**
- Intent:
- Good means:
- Evidence:
- Risks:
- Work mode:
- Clarifying Q&A:
- Support skills:
- Minimum harness:
- First lane:

**Plan**
1. ...

**Stop Conditions**
- ...
```

For critique or review, lead with findings:

```markdown
**Findings**
- ...

**Recommended Adjustment**
- ...
```

For training work, include a short explanation of the Nested Harness Model and point to the simple guide.

## Reference Routing

- Read `references/simple-guide.md` when a teammate needs the plain-language guide or prompt pattern.
- Read `references/how-it-works.md` when explaining the workflow, teaching the diagram, or adapting the method.
- Read `references/support-skill-map.md` when deciding whether to use, publish, mirror, or create supporting skills.
- Read `references/review-rubric.md` when scoring a project-start prompt, plan, or bootstrap artifact.

## Relationship To Other Skills

- Use `project-harness-designer` when the next step is to produce the executable project harness.
- Use `harness-composer` when the work needs parent and child harnesses.
- Use `context-boundary-designer` when the main risk is loading too much, too little, or unsafe context.
- Use `verification-harness-router` when the proof path is unclear.
- Use `deterministic-controls` when the harness needs schemas, policy gates, state machines, validators, tests, or auditability.
- Treat named support skills as selectable dependencies, not mandatory steps. Select, skip, publish, mirror, or create skills based on the current goal and reusable value.

## Quality Bar

A good output:

- resolves material questions or states safe assumptions,
- reframes the work at the right altitude,
- identifies the source of truth,
- maps support skills without overfitting to the first obvious skill,
- designs a minimum useful harness,
- defines evidence before execution,
- keeps context economical,
- picks one first lane,
- avoids ceremony for small work,
- leaves the next session restartable.

## Stop Conditions

Pause or narrow scope when:

- the goal and success criteria conflict,
- the source of truth cannot be identified and guessing would change the plan,
- the next step would create, publish, sync, or mutate durable artifacts without approval,
- the proposed harness duplicates an existing workflow,
- verification cannot be made concrete enough to support a completion claim.
