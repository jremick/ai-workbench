# Deterministic Auth Controls

Version: 0.1.0
Last updated: 2026-06-04

Use these examples when auth safety needs enforcement in code, configuration, hooks, CI, or a tool wrapper. They are public-safe patterns only. They do not include real secret names, secret references, local paths, account identifiers, or private helper implementations.

## Control Goals

Auth handling should make these outcomes enforceable:

- agents cannot read real `.env` files into model context by default
- agents can still discover required variable names from sample files, docs, typed config, or presence-only helpers
- password-manager CLI use is explicit, scoped, and not repeated in every API call
- local secure-store helpers inject secrets into child commands instead of printing them
- public artifacts fail validation when they include real env files, secret references, token patterns, or local machine paths
- auth-dependent readiness claims are verified by behavior, not by showing credentials

## Example Policy

This is a policy shape, not a required implementation format.

```yaml
policy_version: auth-public-example-v1
file_read:
  default: allow
  deny:
    - .env
    - .env.*
  allow:
    - .env.example
    - .env.sample
    - .env.template
shell:
  deny_when:
    - command_may_print_secret_env_file
    - command_may_reveal_password_manager_secret
    - command_may_log_auth_header
password_manager:
  direct_secret_read: approval_required
  repeated_secret_read: deny
  service_account: least_privilege_required
secure_store:
  cache_miss: fail_with_import_instruction
  output_secret_values: deny
logging:
  redact_secret_values: required
  record_policy_decision: required
```

## Env File Gate

Block reads where the model would see raw env contents.

```text
function authorize_file_read(path):
  if is_real_env_file(path):
    return deny("Read a sample env file or use a presence-only helper.")
  return allow()

function is_real_env_file(path):
  name = basename(path)
  if name in [".env.example", ".env.sample", ".env.template"]:
    return false
  return name == ".env" or starts_with(name, ".env.")
```

This gate belongs in the file-read tool, command wrapper, or harness. A prompt that says "do not read env files" is useful guidance, but it is not sufficient control.

## Shell Command Gate

File-read controls are incomplete when the agent also has a shell. Shell policy should block commands that print secret-bearing env files through common tools or small scripts.

```text
function authorize_shell(command):
  if command_reads_real_env_file(command) and command_may_print_output(command):
    return deny("Use the env presence helper instead of dumping secret files.")
  if command_reveals_password_manager_secret(command):
    return deny("Use an approved import, rotation, or subprocess injection helper.")
  return allow()
```

The exact parser can be simple at first, but it should be deterministic and test-backed. Include fixtures for obvious commands, quoted paths, nested script calls, and allowed sample env reads.

## Presence-Only Helper

When an agent needs to verify auth setup, return only non-secret facts.

```json
{
  "file_present": true,
  "required_names": ["SERVICE_API_TOKEN", "SERVICE_BASE_URL"],
  "present_names": ["SERVICE_API_TOKEN", "SERVICE_BASE_URL"],
  "missing_names": []
}
```

The helper can parse a real env file locally, but it must not return values, line contents, comments containing secrets, or the full source text.

## 1Password And Keychain Gate

A safe repeated-command flow is:

1. User approves import or rotation from 1Password.
2. A helper reads one approved field and stores it in the platform secure store without printing it.
3. Runtime commands read from the current environment or secure store.
4. Runtime commands inject secrets into the child process only.
5. Cache misses fail loud instead of silently calling 1Password.

The deterministic rule is: normal runtime paths must not have a hidden password-manager fallback. Hidden fallbacks cause repeated prompts and blur the boundary between "secret import" and "ordinary command execution."

## Verification Cases

A useful test set should include:

- allowed read of `.env.example`
- denied read of `.env`
- denied read of `.env.local`
- denied shell command that prints `.env`
- allowed helper call that returns only variable presence
- denied repeated direct password-manager secret read
- allowed approved import or rotation path
- secure-store cache miss returns an instruction without revealing a value
- logs include policy version and decision reason without secret text

## Residual Judgment

The model can still decide which documented auth route fits the task, summarize missing setup, and explain tradeoffs. Deterministic code should decide whether secret-bearing files can be read, whether direct password-manager access is allowed, whether output is safe to log, and whether public artifacts pass the safety gate.
