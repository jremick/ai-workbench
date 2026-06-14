# Confidence Framework

Version: 1.0.0
Last updated: 2026-06-15

Use confidence labels to communicate evidence strength without overstating certainty.

| Label | Meaning |
| --- | --- |
| High | Primary sources agree, dates are current enough, and the claim is directly supported. |
| Medium | Evidence is credible but incomplete, indirect, or partially time-sensitive. |
| Low | Evidence is weak, old, conflicting, or relies on inference. |
| Unknown | The claim cannot be verified from available sources. |

## Good Confidence Notes

Good notes say why confidence is limited:

- "Medium: official docs confirm the API shape, but model availability should be checked at run time."
- "Low: only secondary reporting was available and no benchmark prompts were disclosed."
- "Unknown: pricing requires account-level access."

Avoid fake precision. A numeric confidence score is useful only when the workflow has a scoring rubric.
