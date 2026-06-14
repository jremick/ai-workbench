---
name: deep-research
description: Use for source-backed research that needs current facts, citation discipline, uncertainty tracking, competing explanations, or a decision-ready synthesis. This skill structures research into source collection, evidence extraction, uncertainty handling, and model-council escalation when claims need independent model review.
version: 1.0.0
last_updated: 2026-06-15
---

# Deep Research

Use this skill when an answer should be grounded in sources instead of memory or a single model's prior knowledge.

The skill produces decision-ready research: scoped question, source plan, evidence table, synthesis, uncertainty, and next checks.

## Core Rule

Separate source collection from synthesis. Facts should trace back to sources, and uncertain claims should stay uncertain.

Use model judgment for interpretation. Use deterministic tools for fetching, parsing, deduping, sorting dates, extracting metadata, and checking citation coverage.

## Workflow

1. Define the research question.
   - Name the decision or output the research supports.
   - State assumptions and scope limits.
   - Identify current-state claims that require live verification.

2. Build a source plan.
   - Prefer primary sources, official docs, papers, code, datasets, filings, standards, or direct product docs.
   - Use secondary sources for context, not as the only proof of important claims.
   - Record source URLs, dates, authors or owners when available, and retrieval date for unstable topics.

3. Extract evidence.
   - Capture short paraphrased findings, not long copied passages.
   - Track conflicts between sources.
   - Keep exact quotes short and only when wording matters.

4. Synthesize.
   - Answer the research question directly.
   - Separate findings, implications, open questions, and confidence.
   - Include concrete dates for time-sensitive claims.

5. Escalate when needed.
   - Use `model-council` for hard synthesis, benchmark design, high-stakes conclusions, or cases with plausible competing interpretations.
   - Use a council after source extraction so workers reason over the same evidence packet.

## Output Shape

```markdown
## Research Question
<question and decision context>

## Sources Checked
| Source | Type | Date | Why It Matters |
| --- | --- | --- | --- |

## Findings
1. <finding with source link>

## Differences Or Conflicts
<material disagreements between sources>

## Implications
<what the evidence means for the decision>

## Confidence And Gaps
<confidence level, missing evidence, and next checks>
```

Use a shorter shape for small questions, but do not omit sources for claims that depend on current or external facts.

## Source Quality

Prefer:

- official docs and changelogs
- primary research papers and datasets
- standards and specifications
- source code and release tags
- direct API responses or CLI read-backs
- reputable reporting for events, with dates checked

Treat these carefully:

- marketing pages with vague claims
- unsourced blog summaries
- stale package tutorials
- benchmarks without disclosed prompts, models, sample IDs, or scoring
- social posts that are not primary announcements

## Reference Files

Load these only when needed:

- `references/research-depth-guide.md`: choose the right depth and source plan.
- `references/citation-standards.md`: citation handling and quote limits.
- `references/confidence-framework.md`: confidence labels and uncertainty handling.
- `references/model-council-integration.md`: when to escalate research into a council.

## Verification

Before claiming research is complete:

- current-state claims were checked against current sources
- important claims have source links
- source dates were compared where recency matters
- conflicts or weak evidence are visible
- model-council escalation was used or explicitly ruled out for hard synthesis
- source material was handled according to the task scope and citation requirements
