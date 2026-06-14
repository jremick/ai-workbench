# Project Harness Designer

`project-harness-designer` helps an agent start substantial projects with the right operating structure before execution.

It is useful when a user gives a goal like "set up this repo", "build a tool", "create a framework", "research this deeply", or "make this public-ready" and the agent needs to define success evidence, risks, and the first execution path.

## Install

Copy this directory into your agent skill directory:

```text
skills/project-harness-designer/
```

The minimum install is `SKILL.md`. Keep `docs/evaluation.md` when you want the public proof summary.

## Try It

```text
I want to create a small public repo for evaluated AI skills. It should be useful, safe to share, and easy for people to navigate. Set up the project.
```

The skill should respond with intent, success evidence, failure modes, work mode, minimum harness, and first path before starting implementation.

## What It Prevents

- building before success criteria are clear
- creating heavy scaffolding for small work
- skipping verification because the task sounds subjective
- losing context across a longer project
- mixing private runtime state into reusable artifacts

## Public Readiness

The public version removes local sync mechanics, private repo paths, personal workspace assumptions, and raw eval run data. It keeps the operating pattern and a short proof summary.
