# Ownership and visibility

Where a skill belongs and when a model sees it are different decisions.

## Four states to keep separate

| State | Question |
| --- | --- |
| Installed or cached | Does the skill source exist in a location the host or plugin system can access? |
| Prompt-visible | Is its name and description present in the current model context? |
| Router-retrievable | Can the active host, profile, or router resolve it when a matching task arrives? |
| Activated | Has the host loaded the complete workflow for this task? |

OpenAI's skill guidance describes progressive disclosure: the host starts with skill metadata and loads the complete instructions when the user invokes the skill or the request matches its description. See [Build skills](https://developers.openai.com/codex/skills).

This repository adds a public architectural recommendation: keep the prompt-visible set small, use domain routers for broad intent, and keep specialized leaves retrievable or explicit-use until activation.

## Ownership is independent

A reusable workflow may be:

- shared across environments;
- personal to one operator;
- owned by a work or team environment;
- public-curated for reuse outside the source environment.

None of those labels determines prompt visibility. A shared skill can remain off-prompt, and a personal skill can be directly visible when it is central to that profile.

AI Workbench records only `public-curated` ownership. It does not publish private personal/work assignments.

## Provider and plugin cache boundary

Plugin and provider packages can contribute many installed skill files. Installed cache content should not automatically become prompt-visible, canonical, or safe to copy.

Use profile or host controls to disable or de-prioritize unwanted surfaces. Do not delete provider caches as a substitute for routing policy, and never publish cached provider bodies as if they were locally owned artifacts.

Plugins are the current OpenAI distribution unit for reusable skills and optional connectors. A skill provides workflow instructions; an MCP server can provide live data, authentication, authorization, and controlled actions. See [Build skills](https://developers.openai.com/codex/skills) and [Build plugins](https://developers.openai.com/codex/build-plugins).

For the expanded five-dimension model, see [Ownership, availability, awareness, and activation](ownership-availability-awareness.md).

## Public claim boundary

AI Workbench can document this model and publish sanitized examples. It cannot establish the prompt-visible or activated state of a reader's host. Those states require runtime evidence from that environment.
