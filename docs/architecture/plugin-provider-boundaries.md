# Plugin and provider boundaries

Skills, plugins, MCP servers, and provider caches have related but distinct roles.

## Current product boundary

OpenAI documents skills as the workflow authoring format and plugins as the installable distribution unit for reusable skills and connectors. See [Build skills](https://developers.openai.com/codex/skills) and [Build plugins](https://developers.openai.com/codex/build-plugins).

A standalone public skill can still be useful for local or repository authoring. Packaging several skills as a plugin adds a distribution and compatibility surface that needs its own tests and support boundaries.

## Cache boundary

Provider or plugin caches are installed implementation state. Their presence does not establish:

- ownership by the repository maintainer;
- permission to copy or relicense their contents;
- prompt visibility;
- profile availability;
- runtime activation;
- public compatibility.

Do not delete caches as a routing policy and do not publish cached bodies as locally authored skills. Resolve provider capabilities through supported host or plugin mechanisms.

## AI Workbench posture

AI Workbench currently publishes repository-reference skills only. It does not publish a plugin, marketplace entry, automatic update channel, or universal install promise. A future plugin should contain a small cohesive cohort, use only public-owned artifacts, and follow clean-environment testing.
