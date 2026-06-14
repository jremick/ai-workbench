# MCP Build References

Version: 0.1.0
Last updated: 2026-06-04

Use current official docs before implementing a new MCP server because SDK imports, transports, and remote deployment patterns change.

## References Used For This Public Skill

- Model Context Protocol TypeScript SDK repository: <https://github.com/modelcontextprotocol/typescript-sdk>
- MCP build-server docs: <https://modelcontextprotocol.io/docs/develop/build-server>
- TypeScript SDK server docs: <https://ts.sdk.modelcontextprotocol.io/documents/server.html>
- Cloudflare Agents MCP docs: <https://developers.cloudflare.com/agents/model-context-protocol/>
- Cloudflare MCP transport docs: <https://developers.cloudflare.com/agents/model-context-protocol/transport/>
- Cloudflare MCP authorization docs: <https://developers.cloudflare.com/agents/model-context-protocol/authorization/>
- Cloudflare securing MCP servers guide: <https://developers.cloudflare.com/agents/guides/securing-mcp-server/>

## Current Caveat

As of this review, public MCP docs and the TypeScript SDK repository show an active version split:

- stable examples often use `@modelcontextprotocol/sdk/...` imports
- current SDK main branch documentation describes split packages such as `@modelcontextprotocol/server`

Do not cargo-cult snippets across that boundary. Inspect the target project's installed package and version before generating code.
