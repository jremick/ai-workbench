# Harness-First Review Rubric

Version: 1.1.2
Last updated: 2026-06-17

Score each item 0-2.

- 0: missing or actively harmful.
- 1: present but vague or partial.
- 2: clear and appropriate to the task size.

## Rubric

1. Q&A fit: asks focused questions when answers matter, or states safe assumptions when proceeding is reversible.
2. Altitude fit: reframes the goal at the right abstraction.
3. Source grounding: identifies and inspects the source of truth when available.
4. Boundary clarity: names constraints, non-goals, privacy, auth, reversibility, environment limits, and stop conditions.
5. Support-skill fit: chooses existing skills, workflows, or validators before proposing new reusable artifacts.
6. Harness fit: designs a minimum useful operating structure before implementation.
7. Context economy: keeps entrypoints small and loads detail progressively.
8. Evidence model: defines tests, evals, review gates, telemetry, screenshots, or live readbacks.
9. First lane: chooses one narrow next path.
10. Learning loop: says what should become reusable and what should remain one-off.

## Pass Target

Use 16/20 as the normal pass line.

Do not pass if any of these are zero:

- altitude fit,
- Q&A fit,
- source grounding,
- support-skill fit,
- harness fit,
- evidence model,
- first lane.
