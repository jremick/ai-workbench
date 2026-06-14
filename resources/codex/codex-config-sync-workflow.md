# Codex Config Sync Workflow

Version: 0.1.0
Last updated: 2026-06-04

## Purpose

Use a versioned sync repo to carry reusable Codex setup across machines without copying runtime state.

The core split is:

- Live Codex home: `$HOME/.codex`
- Versioned sync repo: `$HOME/projects/codex-config-sync`

The live home is the working runtime. The sync repo is the portable source bundle.

## What Belongs In The Sync Repo

Include reusable artifacts:

- global `AGENTS.md` profiles
- shared skills
- shared agent definitions
- config templates
- prompt templates
- setup scripts
- install or refresh docs
- decision logs or learning notes that are intentionally portable

Exclude runtime and machine-local state:

- auth files
- session history
- logs
- caches
- local databases
- memory exports
- shell snapshots
- generated temp files
- raw private project context

## Suggested Repo Shape

```text
codex-config-sync/
  .codex/
    AGENTS.md
    AGENTS.personal.md
    AGENTS.work.md
    DECISIONS.md
    agents/
    skills/
    config.toml.template
    config-snippets/
    rules/
  prompts/
  scripts/
    install.sh
    record-sync-status.sh
  sync/
    devices/
```

Use templates for machine-specific config. Render `$HOME`, optional tokens, and local paths during install rather than committing rendered config.

## New-Machine Install Flow

1. Clone the sync repo.
2. Sign in to the tools needed by your setup, such as GitHub CLI.
3. Run Codex once and complete product sign-in if needed.
4. Export optional environment variables used only to render templates.
5. Run the installer with the intended profile.
6. Review generated config before using it for real work.
7. Record the machine and tool sync status.

Example:

```bash
git clone git@github.com:ORG/codex-config-sync.git "$HOME/projects/codex-config-sync"
cd "$HOME/projects/codex-config-sync"

CODEX_PROFILE=personal ./scripts/install.sh
./scripts/record-sync-status.sh
```

## Installer Responsibilities

A practical installer can:

- create expected directories under `$HOME/.codex`
- install the selected `AGENTS.md` profile
- copy shared skills and agents
- render config templates with local placeholders
- install wrapper scripts into `$HOME/.local/bin`
- leave existing local-only files alone
- print explicit next steps instead of silently modifying auth state

It should not:

- overwrite auth files
- delete sessions, caches, logs, or local databases
- print secrets
- assume every machine has the same trusted project paths
- install work-specific context into personal machines unless explicitly requested

## Pull Remote To Live

Use this when a machine needs the latest shared setup.

```bash
SYNC_REPO="${SYNC_REPO:-$HOME/projects/codex-config-sync}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

git -C "$SYNC_REPO" fetch origin main
git -C "$SYNC_REPO" status --short --branch
git -C "$SYNC_REPO" log --date=iso-strict --left-right --cherry-pick --pretty=format:'%h %ad %s' main...origin/main
git -C "$SYNC_REPO" pull --ff-only origin main
```

Apply targeted updates when possible:

```bash
rsync -a --delete "$SYNC_REPO/.codex/skills/example-skill/" \
  "$CODEX_HOME/skills/example-skill/"

diff -qr "$SYNC_REPO/.codex/skills/example-skill" \
  "$CODEX_HOME/skills/example-skill"
```

Use the full installer only for new-machine setup or a deliberate profile refresh.

## Push Live To Sync Repo

Use this after changing reusable live artifacts.

```bash
SYNC_REPO="${SYNC_REPO:-$HOME/projects/codex-config-sync}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

git -C "$SYNC_REPO" fetch origin main
git -C "$SYNC_REPO" status --short --branch
```

Copy only intended reusable paths:

```bash
cp "$CODEX_HOME/AGENTS.md" "$SYNC_REPO/.codex/AGENTS.md"

rsync -a --delete "$CODEX_HOME/skills/example-skill/" \
  "$SYNC_REPO/.codex/skills/example-skill/"
```

Verify exact matches:

```bash
diff -q "$CODEX_HOME/AGENTS.md" "$SYNC_REPO/.codex/AGENTS.md"
diff -qr "$CODEX_HOME/skills/example-skill" "$SYNC_REPO/.codex/skills/example-skill"
```

Inspect, commit, and push:

```bash
git -C "$SYNC_REPO" diff --stat
git -C "$SYNC_REPO" status --short
git -C "$SYNC_REPO" add .codex/AGENTS.md .codex/skills/example-skill
git -C "$SYNC_REPO" commit -m "Update shared Codex artifacts"
git -C "$SYNC_REPO" push origin main
```

## Device Sync Records

Device records are small JSON files that say which system and tool last installed or checked the shared config. They complement Git history; they do not replace it.

Example:

```bash
SYSTEM_ID=dev-laptop \
SYSTEM_LABEL="Dev Laptop" \
AI_TOOL_ID=codex \
AI_TOOL_LABEL="Codex" \
./scripts/record-sync-status.sh
```

Suggested output path:

```text
sync/devices/dev-laptop/codex.json
```

Useful fields:

- system id and label
- tool id and label
- recorded timestamp
- sync repo branch and commit
- live `AGENTS.md` version
- whether the sync repo was dirty

## Safety Checks

Before committing sync repo changes, check:

- only intended paths changed
- no auth files or sessions were added
- no local absolute paths were committed
- no secrets or secret references were committed
- rendered config is not committed if it contains machine-specific values
- direct `diff` checks passed for mirrored live and sync paths

Before claiming sync is complete, report:

- the live paths changed
- the sync repo paths changed
- the direct comparison checks that passed
- the pushed commit id, if a push happened

## Common Failure Modes

| Failure Mode | Prevention |
| --- | --- |
| Treating `$HOME/.codex` as a git repo | Keep Git operations inside the sync repo. |
| Committing runtime state | Maintain an explicit exclude list and scan before commit. |
| Overwriting local decisions | Preserve or review decision logs before full install. |
| Pulling a dirty or diverged checkout blindly | Fetch, inspect status, and use fast-forward pulls only. |
| Copying rendered secrets into the mirror | Commit templates, not rendered secret-bearing config. |
| Assuming all machines are identical | Use profiles and placeholders for machine-specific paths. |

## Minimal Public Template

If you do not need a full installer, start with:

```text
codex-config-sync/
  .codex/
    AGENTS.md
    skills/
  scripts/
    install.sh
```

Keep the first version small. Add agents, config snippets, device status, and profile-specific instructions only when they solve a real multi-machine problem.
