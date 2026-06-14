# Provider Routing

Version: 1.0.0
Last updated: 2026-06-15

This reference documents the public routing assumptions for the companion runner.

## Route Priority

Use local CLIs first when the machine already has authenticated developer tools:

| Provider | Local Route | Purpose |
| --- | --- | --- |
| OpenAI | Codex CLI `codex exec` | OpenAI worker and synthesizer runs. |
| Anthropic | Claude Code CLI `claude -p` | Claude worker runs. |
| Google | Antigravity CLI `agy --print` | Gemini worker runs. |
| xAI | Grok Build CLI `grok -p` or `grok --prompt-file` | Grok worker runs. |

Use Vercel AI Gateway as an API alternate option when a single endpoint, centralized usage, or deployment environment is more important than local CLI behavior.

## Local CLI Command Shapes

The runner builds command arrays instead of shell strings.

Codex CLI:

```bash
codex exec --ephemeral --json -C "$PWD" -s read-only -o output.txt -
```

Claude Code CLI:

```bash
claude --bare -p "prompt" --output-format json --no-session-persistence --permission-mode plan
```

Antigravity CLI:

```bash
agy --print "prompt" --print-timeout 20m --sandbox
```

Grok Build CLI:

```bash
grok --no-auto-update --prompt-file prompt.md --output-format json --permission-mode plan --no-subagents --no-memory --cwd "$PWD"
```

Pin models in config only when the target environment has verified that the model aliases are available. Public sample configs prefer CLI defaults for local routes.

## xAI Notes

xAI documents Grok Build as a terminal coding agent with headless mode. The public docs show `grok -p "Your prompt here"`, `--model`, `--cwd`, `--output-format plain|json|streaming-json`, `--no-auto-update`, and API-key auth through `XAI_API_KEY` for non-browser environments.

Use `--permission-mode plan`, `--no-subagents`, and `--no-memory` for council workers so a worker behaves like a bounded analyst rather than spawning an uncontrolled nested workflow.

## Vercel AI Gateway

The sample Gateway config uses the OpenAI-compatible endpoint:

```text
https://ai-gateway.vercel.sh/v1/chat/completions
```

The runner reads auth from:

1. `AI_GATEWAY_API_KEY`
2. `VERCEL_OIDC_TOKEN`

Use provider-prefixed model IDs supported by your Vercel account. Verify currently available models before pinning a public benchmark configuration.

```bash
python3 tools/model-council-runner/scripts/council_runner.py models \
  --config tools/model-council-runner/configs/vercel-gateway.base.json
```

## Deterministic Controls

The route table is configuration, not prose. Treat these as required controls:

- explicit adapter per route
- explicit provider per route
- no silent fallback across providers
- per-route timeout
- raw logs saved to disk
- generated command arrays saved before execution
- API credentials read from environment only
- no secret values written to manifests
