---
name: product-ia-ux-redesign
description: "Use for deep source-backed IA, UX, UI, and product-interface redesign reviews of complex apps, admin consoles, SaaS products, developer tools, agent/operator control planes, mixed reader/operator products, and large route/page architectures. Produces human-reviewable audit/redesign artifacts plus AI-agent implementation briefs, browser verification matrices, evidence indexes, and decision logs."
license: Apache-2.0
---

# Product IA UX Redesign

Version: 0.1.1
Last updated: 2026-06-20

## Purpose

Review and redesign complex product interfaces using source-backed IA, UX, and UI evidence. Treat the result as both a human review package and an implementation-ready agent plan.

Use this skill for products where page purpose, navigation, route taxonomy, workflow ownership, controls, data tables, reader views, operator consoles, settings, telemetry, approvals, or object detail pages need rigorous evaluation.

## Fast Start

1. Establish source of truth: repo, live URL, design artifacts, product docs, current screenshots, user goals, and known constraints.
2. Create the artifact skeleton:

```bash
python3 ~/.codex/skills/product-ia-ux-redesign/scripts/init-review-artifacts.py \
  --out work/ia-ux-review \
  --product "Product name" \
  --routes "#library,#review,#settings"
```

3. Read `references/artifact-system.md` for required artifacts and `references/frameworks-and-sources.md` for source quality rules.
4. Run the review in lanes: source/register, current IA inventory, task/page-purpose map, rendered/browser evidence, audit findings, proposed IA, implementation lanes, agent packets, decisions, verification.
5. Close with Changed / Verified / Open loops / Next safe action when artifacts were created or updated.

## Operating Rules

- Ground claims in files, rendered UI, direct product behavior, or reputable UX/product sources. Label inferred findings as inference.
- Use primary/high-quality sources first: official framework docs, W3C/WCAG, Nielsen Norman Group, GOV.UK Service Manual, design-system docs, vendor docs/screenshots, product source, telemetry, and direct browser evidence.
- Do not substitute taste for evidence. Every major recommendation should map to user jobs, product strategy, IA theory, accessibility, comparable products, operational risk, or implementation constraints.
- Separate operator/control interfaces from consumer/reader interfaces. Mixed products usually need both: dense operational control for admins/operators and quiet reading/browsing for readers.
- Preserve product category. Do not turn admin consoles into landing pages, agent tools into generic CMSs, or governed workflows into decorative dashboards.
- Keep private/customer/staff/source-system content out of public artifacts. Use synthetic examples unless the user explicitly authorizes private-context handling.
- Do not inspect secrets or dump `.env` files. Use project auth helpers and browser sessions without exposing tokens.
- Do not claim source freshness, visual behavior, accessibility, or browser results without verifying them in the current task.

## Review Modes

Use the strongest evidence mode available:

- `browser-verified`: runnable UI inspected in a browser with screenshots or browser notes.
- `file-grounded`: repo/design/source files inspected, but rendered behavior was not verified.
- `prompt-only`: user supplied a scenario without source files or runnable UI.

For prompt-only work, label sources as `prompt-provided` and findings as `inferred`. Produce architecture, risk, and verification plans, but do not describe current visual behavior as fact. In `11-acceptance-browser-verification.md`, mark browser checks as `planned`, not `passed`.

## Workflow

### 1. Frame The Product

Capture:

- product category and non-goals
- primary human roles and agent/system consumers
- operator/control surfaces versus reader/consumer surfaces
- critical jobs to be done
- source-of-truth hierarchy
- constraints: public/private boundary, auth, deployment, framework, design system, active work lanes, and forbidden changes

If this is an agent-native, developer-tool, security, operations, or admin product, default to quiet, dense, scan-friendly app patterns. Avoid marketing-page heuristics unless the surface is actually public acquisition or documentation.

### 2. Build The Source Register

Record every source used in `01-source-register.md`:

- repo/docs/design/code files with path and commit or local-state note
- live URLs or browser routes with timestamp
- screenshots and viewport
- official UX/accessibility/design-system sources
- comparable products and whether evidence came from official docs, live app, screenshots, or secondary commentary

Prefer official product docs and direct rendered screenshots for prior art. Use secondary articles only as supporting commentary.

### 3. Inventory Current IA

Map current routes/pages/sections into `03-current-ia-inventory.md`:

- route/hash/path/page title
- owning zone/group
- intended human job
- actual visible contents
- primary actions
- data/loading behavior
- empty/error states
- accessibility and responsive notes
- evidence link or screenshot id

Flag pages that are aliases, debug panels, mixed-purpose pages, empty-on-load routes, or implementation names exposed as human IA.

### 4. Map Roles, Tasks, Pages, And Elements

Use `04-role-task-page-purpose-map.md` and `05-page-element-purpose-ledger.md`.

Ask for each major role:

- What job is this person trying to finish?
- Which page should they naturally choose first?
- Which object is the action about?
- Is the action placed near the object or state it changes?
- Is the page a destination, a drawer/detail view, a settings surface, an activity/log explorer, a review workflow, or a reading surface?

For each visible element, record purpose, owner page, target user, state dependencies, and whether it is operator-facing workflow or implementation plumbing.

### 5. Audit With Severity

Use severity based on impact, frequency, persistence, reversibility, and risk:

- `P0`: blocks a core beta/production job, creates security/privacy risk, or makes state/action ownership misleading.
- `P1`: high-friction IA/workflow problem likely to confuse real users or cause repeated operator mistakes.
- `P2`: meaningful usability/accessibility/consistency issue with workaround.
- `P3`: polish, wording, or future enhancement.

Each finding should include:

- evidence: file/route/screenshot/source
- framework/source mapping
- who struggles and why
- concrete fix direction
- acceptance check
- uncertainty or test needed

### 6. Propose Target IA

Design from human jobs and domain objects, not implementation modules. For enterprise/operator products, common durable zones are:

- Home or Control Room: recent work, alerts, health, pinned destinations, only when real data exists
- Objects/Resources: browse, search, detail, metadata, permissions, versions, activity
- Work/Review: queues, approvals, publish/release work, diff/rollback
- Distribute/Publish/Deploy: packages, channels, exports, delivery history
- Activity/Observability: logs, telemetry, audit, runs, feedback, filters, detail panels
- Health: readiness, dependencies, provider status, maintenance posture
- Integrations: providers, connectors, identity, webhooks
- Settings/Admin: users, groups, API keys, policies, retention, secrets, tenant controls

For reader/consumer surfaces, common zones are:

- Browse/tree
- Search/query
- Reading/detail
- Related references
- Version or trust state when relevant

Do not blend reader pages and operator settings unless the product intentionally presents a power-user cockpit.

### 7. Split Implementation Into Safe Lanes

Prefer small lanes that reduce risk:

- labels, aliases, breadcrumbs, route ownership, and page-purpose copy
- route-owned loading, empty/error/loading states, and visible refresh behavior
- move controls to the page or object they act on
- object detail/tabs and side panels
- table/list upgrades with filters, sorting, row actions, saved views, and batch actions
- settings/integrations/policies separation
- component-system adoption
- route-module or architecture extraction only after behavior is stable

Each lane needs acceptance criteria, tests/browser checks, rollback path, and affected files.

### 8. Delegate When Useful

Use sub-agents for splittable work:

- Researcher: source-backed UX/IA frameworks and comparable products.
- Codebase mapper: routes, components, state, loaders, permissions, and page ownership.
- Browser QA: screenshots, responsive checks, keyboard/focus, empty/loading/error states.
- Synthesis reviewer: severity, contradictions, overclaim checks, and implementation-lane risk.

Parent agent owns source-of-truth decisions, artifact integration, final recommendations, and verification. Pass raw artifacts and bounded prompts. Do not leak intended conclusions when asking a sub-agent to validate the review.

### 9. Verify

Use current local/project verification rules. Typical checks:

- route/page inventory matches rendered UI
- each nav leaf lands on a distinct purposeful page or documented alias
- core role walkthroughs complete without hidden manual setup
- browser screenshots at desktop/tablet/mobile widths
- keyboard navigation, focus, labels, headings, status messages, and contrast
- text fits buttons/cards/tables/sidebar at target widths
- API/CLI/MCP or other non-UI consumers remain respected when the product is multi-surface
- restricted/private data does not appear in public screenshots or artifacts

If browser access, auth, build, or live data is unavailable, mark affected findings as file-grounded or partial.

## Minimum Fill For Small Reviews

For a lightweight or prompt-only review, fill at least:

- `00-executive-brief.md`: product frame, top findings, target direction, open questions.
- `01-source-register.md`: source boundary and evidence labels.
- `03-current-ia-inventory.md`: every known route/page, even if inferred from a prompt.
- `04-role-task-page-purpose-map.md`: primary roles and jobs.
- `06-audit-findings.md`: ranked findings with evidence mode.
- `07-proposed-ia-route-architecture.md`: target taxonomy and route migration.
- `08-implementation-lanes.md`: first safe lane and stop rules.
- `11-acceptance-browser-verification.md`: planned checks and residual risk.

Leave other artifacts skeletal only when they are not needed yet. If an artifact is intentionally skeletal, say why in `README.md`.

## Mixed Reader/Operator Example

For an admin console with `#library`, `#reader`, `#review`, `#exports`, `#operations`, `#providers`, and `#policies`:

- Treat `#library` and `#reader` as reader/resource surfaces unless they expose admin actions.
- Treat `#review` as governance work.
- Rename or alias `#exports` toward `Distribute` or `Package builder` when packages are for API/CLI/MCP/agent consumers.
- Split `#operations` into concrete operator jobs such as `Activity`, `Health`, `Approvals`, or `Maintenance`.
- Move provider setup to `Integrations`; move policy/user/key/retention controls to `Settings`.
- Hide persistent API URL/API key bars for normal signed-in users; move them to developer connection or settings.
- Replace manual `Load` pages with route-owned loading, refresh, empty, and error states unless cost/rate limits require explicit lazy loading.

## Stop Rules

Stop and ask or narrow scope when:

- source of truth conflicts and the choice affects implementation
- private data would enter a public artifact
- credentials, production writes, or paid external systems are required
- the task asks for implementation but the review uncovers security/privacy leakage
- the requested design direction contradicts the product category or established local design system
- browser evidence is required but no runnable or accessible UI exists

## Closeout

Report:

- artifact directory
- most important artifacts created or updated
- top findings and target IA in one short summary
- validation performed and what remains unverified
- implementation lanes and next safe action
- any decisions recorded with uncertainty/review triggers

Do not overclaim. State whether results are source-backed, browser-verified, code-grounded, or proposed.

## Reference Routing

- `references/artifact-system.md`: artifact set, directory structure, and templates.
- `references/frameworks-and-sources.md`: source quality rules, framework register, and comparable-product evidence guidance.
