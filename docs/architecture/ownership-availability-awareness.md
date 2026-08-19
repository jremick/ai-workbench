# Ownership, availability, awareness, and activation

These dimensions answer different questions and should not be collapsed into a single “installed” flag.

| Dimension | Question | Example values |
| --- | --- | --- |
| Ownership | Which environment is accountable for the workflow? | shared, personal, work, public-curated |
| Installed or cached | Does source exist somewhere the host can access? | present, absent |
| Profile availability | May the active environment resolve or use it? | enabled, disabled, unavailable |
| Prompt awareness | How can it be discovered before activation? | direct-visible, router-aware, direct-call-aware, not-aware |
| Activation | Has the full workflow been loaded for this task? | inactive, active |

A skill can be shared in ownership yet remain off the initial prompt. A cached provider skill can exist without being approved, visible, or safe to republish. A router can be visible while one of its targets is unavailable to the current profile.

The [synthetic profile resolution](../../architecture/examples/profile-resolution.json) demonstrates this: all six routers remain discoverable, four shared targets are enabled, and two differently owned targets are unavailable.

This terminology is AI Workbench's reference model. OpenAI's official documentation supports progressive skill disclosure, but does not define this complete ownership/awareness taxonomy. See [Official behavior versus this reference architecture](official-vs-reference.md).
