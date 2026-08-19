# Frameworks And Sources

Use this reference when grounding IA/UX/UI findings.

## Source Quality Ladder

1. Direct product behavior: live UI, local build, browser screenshots, API responses, telemetry, route state.
2. Product source of truth: product goals, architecture docs, decisions, design system, code, tests, issue/roadmap records.
3. Primary UX/accessibility/framework sources: W3C/WCAG, Nielsen Norman Group, GOV.UK Service Manual, Material Design, IBM Carbon, Apple HIG, Microsoft Fluent, Atlassian Design System, official vendor docs.
4. Comparable product evidence: official docs, live app behavior, official screenshots/videos, public help centers.
5. Secondary research or commentary: useful only when primary evidence is unavailable or to add interpretation.

Record trust level and access date. Do not cite a product pattern unless you inspected the source during the task or clearly mark it as prior memory.

## Core Review Frameworks

- Nielsen Norman Group heuristic evaluation: visibility of system status, match with real world, user control, consistency, error prevention, recognition over recall, flexibility, minimalist design, error recovery, help/documentation. Rank severity by frequency, impact, and persistence.
- W3C WCAG 2.2: keyboard access, focus visibility, headings/labels, target size, contrast, status messages, names/roles/values, consistent navigation, multiple ways where applicable.
- GOV.UK Service Manual and Design Principles: start with user needs, design the whole service, make simple and accessible paths, make security/reliability visible where users need it.
- Material Design navigation: navigation should reflect hierarchy, support task completion, show location, and avoid ambiguous destinations.
- IBM Carbon enterprise/product guidance: data-heavy workflows need tables/lists with search, filters, sorting, display settings, row actions, progressive disclosure, batch actions, empty/loading/error states.
- Atlassian, Microsoft Fluent, and cloud-console patterns: separate resources, work queues, logs/activity, health, integrations, and settings; use object-scoped actions and breadcrumbs.

## Comparable Product Matrix Guidance

For each comparable product, capture:

- why it is comparable
- official source URLs
- screenshot or evidence reference if available
- pattern to borrow
- pattern not to borrow
- confidence level

Useful comparison families:

- content/knowledge systems: Notion, Confluence, Guru, GitBook, ReadMe
- developer/cloud consoles: Vercel, AWS, Azure, Google Cloud, Postman
- observability/log systems: Datadog, Grafana, Honeycomb
- workflow/approval systems: Linear, LaunchDarkly, GitHub, Retool
- design systems: Carbon, Fluent, Atlassian, Material, Apple HIG

Do not copy IA wholesale from a product with a different category. Use comparable products to validate patterns, not to replace product strategy.

## Operator Versus Reader Heuristics

Operator/control interfaces should emphasize:

- status, health, recency, errors, and pending work
- filters, tables, bulk actions, row actions, side panels, and drill-down
- auditability, permissions, rollback, and safety
- compact layout, stable navigation, object context, and low visual drama
- clear distinction between configuration, activity, work queues, and resources

Reader/consumer interfaces should emphasize:

- content clarity, reading comfort, search, browse structure, citations, and related references
- trust/provenance state only where it helps comprehension or action
- fewer controls, less operational noise, and clear next reading paths

Mixed products need an explicit boundary. A reader page can surface trust state; it should not become an admin settings panel. An operator page can include previews; it should not pretend to be a public reading experience.

## Overclaim Checks

Before finalizing findings, ask:

- Did I inspect the current rendered UI, or only source files?
- Did I verify the route/state I am describing?
- Is this a true blocker or a preference?
- Does this recommendation preserve API/CLI/MCP or other non-UI consumers?
- Did I separate product strategy from implementation debt?
- Did I record uncertainty and review triggers?
- Would a future implementer know exactly what to change and how to prove it worked?
