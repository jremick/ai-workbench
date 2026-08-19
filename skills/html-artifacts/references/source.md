# Source And Adaptation Notes

This local Codex skill was created after reviewing:

- Thariq Shihipar's HTML effectiveness example gallery: https://thariqs.github.io/html-effectiveness/
- The example source repo: https://github.com/ThariqS/html-effectiveness
- `dogum/html-artifacts`, an Apache-2.0 Claude skill: https://github.com/dogum/html-artifacts

Public provenance review performed 2026-08-20:

- `ThariqS/html-effectiveness` commit `1787245d94aa680edf18b52027e3f859032776ba`, Apache-2.0.
- `dogum/html-artifacts` commit `c14a4ec2a5ad09fe24163f4430d46ee4bb8c1269`, Apache-2.0.

The public package adapts workflow ideas and category patterns. It does not copy the upstream example HTML corpus.

Useful upstream ideas adapted here:

- HTML should be chosen when the artifact benefits from spatial layout, hierarchy, color, interaction, or browser inspection.
- The right default is not "always answer in HTML"; the right default is "use the medium that best supports the human task."
- Temporary editors are only useful when they export back to a text representation the user can paste, commit, or feed into another agent.
- Existing design systems should win over generic artifact styling.
- Starter templates reduce repeated boilerplate but should not become rigid content schemas.

Local Codex adjustments:

- HTML is the default for substantial human-facing deliverables; markdown remains the right format for simple text review, decisions, repeated source inputs, and diff-heavy repo files unless the user asks otherwise.
- HTML artifacts are treated as working/view artifacts and should be saved to an appropriate local path, not pasted into chat by default.
- Verification follows Codex browser/frontend expectations: inspect rendered output when layout or interaction is material, and be explicit when verification is skipped.
