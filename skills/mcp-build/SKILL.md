---
name: mcp-build
description: Use when building, reviewing, deploying, or extending Model Context Protocol servers, especially TypeScript MCP servers, stdio transports, Streamable HTTP transports, remote MCP servers, hosted agent platforms, or tools that expose external systems to AI clients. Emphasize schemas, narrow tools, auth boundaries, smoke tests, and direct-access risk review.
version: 1.0.0
last_updated: 2026-06-04
status: public-ready
---

# MCP Build

Use this skill for Model Context Protocol server design, implementation, review, deployment, and documentation.

MCP servers are execution boundaries. Treat them like productized APIs, not just prompt extensions.

## Core Defaults

- Check the current MCP SDK and hosting docs before copying import paths or transport boilerplate.
- Use explicit schemas for all tool inputs.
- Prefer narrow, intent-based tools over generic API proxy tools.
- Keep tool outputs concise and structured for client compatibility.
- Separate tool registration, integration clients, normalization, policy checks, and runtime entrypoints once a server has more than one tool or one upstream integration.
- Keep stdio servers stdout-clean. Send logs and diagnostics to stderr.
- For remote servers, prefer Streamable HTTP unless a specific client requires a legacy transport.
- Treat read-only, write, admin, and destructive actions as separate risk classes.

## Version Check

Before writing code, confirm:

- target SDK package and version
- server API used by that version
- transport package and import path
- runtime: Node.js, Bun, Deno, Worker, container, or serverless host
- client target: Claude Desktop, Cursor, Codex, custom client, hosted agent, or another MCP host

Do not mix snippets from different SDK generations. If docs disagree, prefer the versioned docs for the package actually installed in the project.

## Tool Design

Good MCP tools are:

- narrow enough to describe clearly
- schema-validated
- idempotent where practical
- explicit about read/write risk
- concise in output
- safe under repeated calls
- tested with representative valid and invalid inputs

Avoid:

- exposing raw upstream APIs as generic tools
- hiding large side effects behind innocent tool names
- returning huge unstructured blobs by default
- using the model's wording as the only approval gate
- treating MCP client authentication as proof the upstream direct URL is protected

## Security Defaults

- Authenticate remote MCP servers at the server boundary.
- Protect direct upstream MCP routes, not only proxy or portal routes.
- Add a central action-risk registry before write/admin tools.
- Unknown actions should fail closed.
- Require server-side confirmation, a server-validated approval token, or a clear human approval path for write/admin actions.
- Redact secrets in errors and logs, including raw and URL-encoded credentials.
- Keep health checks shallow by default. Put upstream/deep readiness behind auth.
- Rate-limit or quota sensitive write paths.

## Stdio Checklist

- Build before connecting from a client.
- Configure clients to run the built entrypoint directly.
- Keep stdout reserved for protocol messages.
- Send logs to stderr.
- Test initialize, list tools, and a simple tool call.
- Test malformed input and missing configuration.

## Remote Checklist

- Use the current standard remote transport for the target SDK/client.
- Authenticate the MCP endpoint.
- Verify unauthenticated requests fail as intended.
- Check that dev routes are not publicly exposed.
- Verify direct hostnames do not bypass the intended auth boundary.
- Test auth failure, expired credentials, malformed requests, and rate limits.
- Record expected status codes in docs.

## Verification

Run the checks that fit the project:

- type-check and lint
- unit tests for validation, normalization, policy gates, and error redaction
- negative tests for malformed IDs, path traversal, missing secrets, and unauthorized calls
- MCP smoke test that initializes, lists tools, calls at least one read-only tool, and validates expected output
- dependency audit or lockfile check
- deployment dry-run or bundle check
- post-deploy smoke test against the real endpoint when publishing a remote server

## Documentation Checklist

Update docs when behavior changes:

- runtime topology and trust boundaries
- required secrets and bindings
- MCP client connection method
- auth model and known direct-access risks
- tool list and risk class
- validation commands and expected outputs
- limitations and unsafe actions that are intentionally not exposed

## Official References

See `docs/references.md` for the public references used to shape this package.
