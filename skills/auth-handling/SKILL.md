---
name: auth-handling
description: Use when a task needs local authentication routing, API token loading, secret references, project environment files, password-manager CLI use, keychain-backed secret access, service account setup, or troubleshooting repeated auth prompts. Choose the least-exposure path by ownership: project-defined helpers first for project workflows, reusable local secret caches for repeated agent commands, and explicit user confirmation before creating new durable auth storage.
version: 1.1.0
last_updated: 2026-06-04
status: public-ready
---

# Auth Handling

Choose a safe local authentication path without exposing secrets.

This skill is about routing and boundaries, not about retrieving secret values. Never print, commit, log, paste, or store secret values in chat, repo files, shell startup files, issue trackers, docs, or durable notes.

## Operating Model

Use the smallest auth surface that can complete the task.

1. Identify the owner: project helper, local agent helper, deployment runtime, or CI system.
2. Identify the required variable names from docs, example files, or typed config, not from real secret files.
3. Prefer an already-exported environment variable for the current command.
4. For repeated local commands, prefer a strict keychain-backed helper that injects secrets only into child processes.
5. Use 1Password or another password-manager CLI for explicit warmup, one-time import, rotation, or single-command injection.
6. Verify auth by behavior, presence checks, or API status responses, not by printing values.
7. Document rotation, revocation, scope, and the non-secret names needed by operators.

## Routing Policy

Choose the auth path by ownership.

### Project-Owned Auth

Use this for a repo or external system with its own documented auth conventions.

Default order:

1. Follow project-defined helpers, docs, and local conventions.
2. Use `.env`, `.env.local`, or equivalent only when the project defines that as the local auth source.
3. Source or inject environment values into the target command without printing the file.
4. Use a project-specific keychain helper if one exists or if repeated commands need durable local reuse.
5. Ask the user before creating a new durable auth path, retrieving a new secret, or changing how the project stores credentials.

### Reusable Agent Auth

Use this for repeated local agent commands or shared helpers that need the same downstream API token across shell calls.

Default order:

1. Check an existing environment variable for the current command.
2. Use an existing keychain-backed helper when one exists.
3. Import a secret into a local secure store only when the user has approved that durable path.
4. Use a password-manager CLI only for explicit warmup, import, rotation, or one-off inspection.

Do not silently fall back from a missing local cache to direct password-manager secret reads.

## 1Password To Keychain Pattern

Use this pattern when a local agent needs the same downstream token across multiple shell calls.

1. Treat 1Password as the human-owned secret source of truth.
2. Treat the macOS Keychain, or the platform-equivalent secure store, as a local cache for repeated agent commands only after user approval.
3. Import or rotate the secret through a named helper that does not echo the value.
4. Have normal runtime helpers read from the current environment first, then the secure store.
5. On cache miss, fail with an import or rotation instruction. Do not automatically call 1Password.
6. Inject secrets into the child process environment and redact command output before logs, chat, or durable files.

Direct `op` commands are appropriate for:

- authenticating the CLI through its normal desktop, account, or service-account flow
- reading one field for a user-approved import or rotation
- running one command with secrets injected into its subprocess
- inspecting item metadata without revealing secret fields

Avoid direct `op` commands in loops. Repeated direct reads create prompt fatigue, make automation brittle, and increase the chance that a secret value or reference ends up in logs.

When multiple 1Password accounts may be available, pin the intended account through the CLI-supported account flag or environment variable. For non-interactive automation, use service accounts only when least-privilege access, storage, rotation, and revocation are clear.

## Non-Negotiables

- Do not dump `.env` files.
- Do not print secret values.
- Do not paste secret references or secret values into durable docs.
- Do not store session tokens in files, repo config, shell startup files, or notes.
- Do not create service account tokens unless the task is non-interactive automation or CI/CD and least-privilege scope is clear.
- Do not disable output masking unless the user explicitly asks to inspect a value and the channel is safe.
- Prefer least-privilege tokens and project helpers over ad hoc auth commands.

## Password Manager CLI Pattern

Use a password-manager CLI when it is the project or user-approved source of truth for secrets.

Safer uses:

- authenticate the CLI once through its normal desktop or service-account flow
- run a command with secrets injected only into a subprocess
- read one field only for import or rotation into a secure local store
- scope service accounts to only the required vaults, projects, or environments

Risky uses:

- repeated direct secret reads in every API request
- printing command output that may contain a secret
- storing session tokens in files
- checking `.env` files or generated secret files into git

## Project `.env` Handling

When a project uses `.env`:

- inspect variable names from `.env.example`, typed config, docs, or a presence-only helper
- prefer example files such as `.env.example` for docs
- source or inject the env file into the target command
- verify required variables by presence, not value
- never commit real `.env` files

Safe checks:

```bash
test -f .env && printf 'env file present\n'
python3 - <<'PY'
from pathlib import Path
for line in Path('.env.example').read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        print(line.split('=', 1)[0])
PY
```

If a real `.env` file is the only local source, do not read it into the model context. Use a deterministic helper that parses it locally and returns only approved facts such as `file_present`, `missing_names`, or `present_names`.

## Deterministic Auth Controls

Auth safety must not rely on prompt wording alone. Put controls in the harness, tool wrapper, validator, CI check, or project helper at the boundary where the secret could leak.

| Boundary | Control | Verification |
| --- | --- | --- |
| Agent file reads | Deny reads of real `.env` files and allow only documented sample env files by default. | Fixture requests for blocked real env paths and allowed sample paths. |
| Shell commands | Block or review commands that dump secret files, reveal password-manager values, or print auth headers. | Command-policy tests for `cat`, `sed`, `grep`, and script-based env reads. |
| Password-manager CLI | Require explicit approval or a named helper for direct secret reads. | Tests or hook logs showing direct reads are blocked unless bypass is approved. |
| Keychain helper | Return env injection or presence status, never secret text. | Unit tests for cache hit, cache miss, rotation, and redacted logs. |
| Public artifacts | Reject real env files, secret references, token patterns, and local machine paths. | Repository validator or secret-scan gate. |
| Auth-dependent claims | Verify by behavior or status, not by printing credentials. | Smoke test, API status response, or unauthorized/authorized route checks. |

### `.env` Read Gate Example

Use a deterministic pre-tool gate for file reads and shell commands:

```text
if request.operation == "read_file" and path_is_secret_env_file(request.path):
  deny("Real env files are secret-bearing. Read the sample env file or run a presence-only helper.")

if request.operation == "shell" and command_may_dump_secret_env_file(request.command):
  deny("This command could print env secrets. Use a scoped helper that returns presence-only status.")
```

The gate should default-deny `.env` and `.env.*` files, default-allow `.env.example` or equivalent sample files, and require an explicit exception for any project that intentionally keeps a public env-shaped file.

## Service Account Pattern

Use service accounts for automation only when:

- a human interactive account is not appropriate
- least-privilege scope is defined
- token storage is handled by the deployment platform or secure runtime
- rotation and revocation are documented
- logs redact auth headers and secret-bearing query parameters

## Troubleshooting

- Repeated prompts: use a project helper or approved local secure store instead of repeating direct secret reads.
- Wrong account: specify the account through the password-manager CLI's supported account flag or environment variable.
- Missing env var: verify presence and docs before retrieving a new secret.
- Project expects `.env`: source or inject it without printing values.
- Agent needs to know env names: read sample files or typed config, not real env values.
- CI secret missing: verify secret names and permission scopes, not secret values.

## Verification

Before claiming auth setup or auth-dependent work is ready:

- the selected route matches the ownership scope
- no secret values were printed, committed, pasted, logged, or stored durably
- repeated command paths use env variables, project helpers, or approved secure local storage rather than repeated direct secret reads
- `.env` files, when applicable, were sourced or inspected without dumping values
- deterministic controls block model-visible reads of real env files and block shell commands that would dump them
- any new durable auth storage path was explicitly requested or confirmed
- docs explain rotation, revocation, and least-privilege scope when automation is involved

## Official References

See `docs/references.md` for public references used to shape this package.
