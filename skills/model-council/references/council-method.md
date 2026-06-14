# Council Method

Version: 1.0.0
Last updated: 2026-06-15

## Intent

A model council is a controlled fan-out-and-synthesize workflow. It is designed to improve coverage, surface disagreement, and reduce single-model anchoring.

It is not designed to create the illusion of certainty. If workers disagree, the final answer should show the disagreement and name the checks that would resolve it.

## Workflow

1. Normalize the task.
   - Write the user goal, constraints, success criteria, and allowed sources.
   - Decide whether the task needs `base`, `adversarial`, `stress-test`, or `extended`.

2. Generate worker prompts.
   - Give every worker the same task frame.
   - Give each worker one role-specific lens.
   - Do not include other worker answers.
   - Ask for structured output.

3. Run workers independently.
   - Prefer parallel execution when the routes are available.
   - Save raw stdout, stderr, and extracted answer text.
   - Mark unavailable routes explicitly.

4. Synthesize.
   - Give the synthesizer the task frame, rubric if allowed, and worker outputs.
   - Require consensus, disagreement, accepted claims, rejected claims, verification gaps, and final answer.
   - Do not hide disagreement just to produce a smoother answer.

5. Verify.
   - Use deterministic checks where possible.
   - Use human or model review for semantic quality.
   - For benchmarks, isolate gold rubrics from generation.

## Role Design

Roles should create useful difference. A weak council uses four models with the same prompt. A stronger council asks each worker to optimize for a different failure mode.

Good role lenses:

- problem structure and assumptions
- evidence and source quality
- contrarian or red-team analysis
- domain-specific analysis
- implementation feasibility
- benchmark leakage or scoring risk

Avoid role lenses that only rename the same behavior.

## Synthesis Rules

The synthesizer should:

- prefer claims supported by multiple independent workers or strong evidence
- keep minority objections when they affect risk
- reject claims that are unsupported, stale, overconfident, or contradicted
- name what evidence would change the conclusion
- produce an answer that a human can act on

The synthesizer should not:

- use majority vote as the only decision rule
- merge incompatible answers into a vague compromise
- invent sources that workers did not provide
- conceal missing evidence

## Minimum Council Run Record

Save:

- task JSON
- config JSON
- worker prompt files
- worker command arrays or API route descriptors
- worker stdout and stderr logs
- worker output text
- synthesizer prompt
- synthesizer command or API route descriptor
- synthesizer output
- final manifest with status, timestamps, and paths
