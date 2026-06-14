# MCP Build

`mcp-build` is a practical skill for building and reviewing Model Context Protocol servers.

It focuses on the surfaces that most often break in real MCP projects: SDK/version drift, transport choice, schemas, tool boundaries, auth, direct route protection, smoke tests, and documentation.

## Install

Copy this directory into your agent skill directory:

```text
skills/mcp-build/
```

The minimum install is `SKILL.md`. Keep `docs/references.md` for source links and version-check context.

## Try It

```text
Use mcp-build to review this MCP server before I expose it to a remote client. Focus on schemas, auth, tool risk classes, and smoke tests.
```

## What It Catches

- stale SDK import paths
- prompt-only validation
- stdout noise in stdio servers
- generic API proxy tools
- missing direct-route auth for remote servers
- write/admin tools without risk classification
- missing negative tests and smoke checks

## Public Readiness

The public version was refreshed against current public MCP and Cloudflare documentation on 2026-06-04. It deliberately avoids hard-coding one SDK generation's imports as universal truth.
