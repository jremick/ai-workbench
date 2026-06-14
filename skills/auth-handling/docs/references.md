# Auth Handling References

Version: 0.2.0
Last updated: 2026-06-04

Use current official docs before implementing a password-manager or service-account flow.

## References Used For This Public Skill

- 1Password CLI app integration: <https://developer.1password.com/docs/cli/app-integration/>
- 1Password CLI environment variables: <https://developer.1password.com/docs/cli/environment-variables/>
- 1Password CLI `run`: <https://developer.1password.com/docs/cli/reference/commands/run/>
- 1Password CLI `read`: <https://developer.1password.com/docs/cli/reference/commands/read/>
- 1Password CLI multiple accounts: <https://developer.1password.com/docs/cli/use-multiple-accounts/>
- 1Password service accounts: <https://developer.1password.com/docs/service-accounts/use-with-1password-cli/>
- 1Password secrets automation security: <https://developer.1password.com/docs/secrets-automation/security/>
- macOS Keychain Services overview: <https://developer.apple.com/documentation/security/keychain-services>

## Current Notes

The exact command flags and environment features can change. As of this review, the public docs include:

- account selection through command flags or environment variables
- subprocess secret injection through CLI run commands
- output masking defaults for run-style secret injection
- service-account authentication for non-interactive automation
- environment variable features for developer environments

Do not include real secret references, vault names, item names, account IDs, or token values in examples.

See `deterministic-controls.md` for public-safe policy examples around env-file read gates, shell command gates, and keychain-backed runtime helpers.
