# War Council Rubrics

Build the rubric before persona scoring. Use integer weights totaling exactly 100.

## Default Decision Rubric

Use this when the decision does not fit a more specific template:

| Dimension | Weight | Meaning |
| --- | ---: | --- |
| Mission fit | 30 | Directly advances the stated goal |
| Economic quality | 20 | ROI, opportunity cost, cash, time, and attention |
| Execution realism | 20 | Can be done with available people, systems, and time |
| User/customer impact | 15 | Trust, support burden, harm, or benefit to affected people |
| Reversibility | 10 | Easy to unwind, pause, or stage |
| Strategic optionality | 5 | Preserves or expands future choices |

## Product Or Roadmap Rubric

| Dimension | Weight |
| --- | ---: |
| Customer pull | 25 |
| Strategic differentiation | 20 |
| Learning velocity | 15 |
| Build and maintenance cost | 15 |
| Revenue or retention leverage | 15 |
| Reversibility | 10 |

## Technical Architecture Rubric

| Dimension | Weight |
| --- | ---: |
| Correctness and reliability | 25 |
| Simplicity and maintainability | 20 |
| Security and privacy | 20 |
| Migration and integration risk | 15 |
| Operating cost | 10 |
| Reversibility | 10 |

## Spend Or Vendor Rubric

| Dimension | Weight |
| --- | ---: |
| Expected value | 30 |
| Opportunity cost | 20 |
| Implementation effort | 15 |
| Lock-in and reversibility | 15 |
| Risk reduction | 10 |
| Time-to-value | 10 |

## Public Communication Rubric

| Dimension | Weight |
| --- | ---: |
| Truthfulness | 30 |
| Audience relevance | 20 |
| Reputation risk | 15 |
| Clarity | 15 |
| Strategic positioning | 10 |
| Reversibility | 10 |

## Weighting Rules

- The top dimension should usually be 25-35.
- Avoid equal weights unless the user explicitly wants a neutral comparison.
- If one constraint is hard, include it as a gate instead of a low-weight dimension.
- If the decision is irreversible, increase reversibility or downside protection.
- If the evidence is weak, add learning velocity or staged optionality.

## Tiering Guidance

Use the deterministic aggregate first, then judge the tiers:

- `build_first`: highest score and no unresolved fatal objection
- `strong_candidate`: close to the lead or worth a staged bet
- `nice_to_have`: useful but does not deserve near-term focus
- `park_it`: weak, blocked, too risky, or dominated by another option

Never hide a close race. If the top two options are within 5 points, treat the decision as contested unless the war chest strongly favors one.
