# Official behavior versus this reference architecture

AI Workbench separates current OpenAI product behavior from Jarel Remick's public architecture recommendations.

## Current official behavior

| Topic | Current documented behavior | Source reviewed 2026-08-20 |
| --- | --- | --- |
| Skill loading | ChatGPT and Codex begin with skill name and description, then load the full `SKILL.md` when selected. | [Build skills](https://developers.openai.com/codex/skills) |
| Initial skill-list budget | Codex bounds the initial skill list and may shorten descriptions or omit skills when the list is large. | [Build skills](https://developers.openai.com/codex/skills) |
| Skill package | A skill is a directory containing `SKILL.md` plus optional scripts and references. | [Build skills](https://developers.openai.com/codex/skills) |
| Distribution | Skills author workflows; plugins package reusable skills and connectors for installation. | [Build plugins](https://developers.openai.com/codex/build-plugins) |
| Instruction discovery | Codex layers `AGENTS.md` instructions from user scope through the project path. | [AGENTS.md guidance](https://developers.openai.com/codex/guides/agents-md) |

Official behavior is time-sensitive. Follow the links before making operational or compatibility claims.

## AI Workbench recommendations

The following are local reference concepts, not official OpenAI taxonomy:

- six broad router domains;
- ownership separated from prompt awareness;
- installed or cached, profile-available, router-retrievable, and activated as separate states;
- a registry that generates public route maps and synthetic profile resolutions;
- structural smoke cases and negative mutation contracts;
- metadata-only drift review rather than automatic live-to-public copying.

The [synthetic registry](../../architecture/examples/minimal-registry.json) demonstrates these concepts without exposing a live environment.

## Claim rule

When a document combines both layers, label each claim as one of:

- **Official:** directly supported by current OpenAI documentation.
- **Reference:** an AI Workbench design recommendation.
- **Runtime-observed:** measured in a named environment and valid only for that observation.
- **Unverified:** proposed or not currently testable.

No reference artifact in this repository establishes the runtime state of another installation.
