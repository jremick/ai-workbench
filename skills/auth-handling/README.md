# Auth Handling

`auth-handling` is a safety skill for local credentials, secret references, project env files, 1Password or other password-manager CLIs, keychain-backed caches, and service accounts.

It is intentionally pattern-focused. It does not ship private helper scripts, secret names, local keychain services, or machine-specific hooks.

## Install

Copy this directory into your agent skill directory:

```text
skills/auth-handling/
```

The minimum install is `SKILL.md`. Keep `docs/references.md` for source links and `docs/deterministic-controls.md` for policy-gate examples.

## Try It

```text
Use auth-handling to decide how this project should load its API token for repeated local smoke tests without printing secrets.
```

```text
Use auth-handling to design a deterministic policy that prevents agents from reading real .env files while still allowing .env.example and presence-only checks.
```

## What It Catches

- repeated direct secret reads
- full `.env` dumps
- unclear project-owned versus reusable-agent auth paths
- hidden password-manager fallbacks after keychain cache misses
- prompt-only controls for secret-bearing file reads
- service accounts without least-privilege scope
- secret values leaking into logs, docs, commits, or chat

## Included Patterns

- 1Password as the human-owned secret source of truth.
- Keychain or platform secure-store cache for approved repeated local agent commands.
- Strict runtime helpers that read environment variables or secure store entries, then fail loud on cache miss.
- Deterministic gates that block model-visible reads of real `.env` files and commands that would dump them.
- Presence-only auth checks that return required names, present names, and missing names without values.

## Public Readiness

The public version removes private helper implementation, local hook paths, personal cache names, and machine-specific examples. It keeps the reusable routing policy, safety checks, and deterministic control examples.
