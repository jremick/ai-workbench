# Security Policy

AI Workbench is a public collection of docs, skills, examples, and small tools. Most issues will be documentation or fixture problems, but private reporting is still appropriate for anything that could expose secrets, private data, unsafe auth guidance, or a vulnerable tool pattern.

## Reporting

Do not open a public issue for sensitive findings.

Use GitHub private vulnerability reporting when available:

https://github.com/jremick/ai-workbench/security/advisories/new

If that path is unavailable, open a minimal public issue asking for a private reporting channel and do not include exploit details, tokens, private data, or sensitive reproduction steps.

## Scope

Please report:

- committed secrets, credential values, private keys, or real `.env` files
- examples that leak private workspace details, local paths, or customer/employer data
- unsafe auth, MCP, agent, or tool patterns that could cause credential exposure or unintended writes
- scripts that mishandle secret values or write sensitive data to durable logs

## Out of Scope

- general documentation preferences
- non-sensitive broken links or typos
- vulnerabilities in third-party tools not introduced by this repo

Open a normal issue for non-sensitive docs and example improvements.
