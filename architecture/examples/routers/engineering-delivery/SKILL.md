---
name: engineering-delivery
description: "Synthetic router for repositories, implementation, review, QA, security, and release readiness."
license: Apache-2.0
---

# Engineering Delivery Router

This is a synthetic reference router. It demonstrates routing structure without representing a real profile, plugin inventory, or private route table.

## Owns

- repository lifecycle, code changes, review, QA, security, and delivery evidence.

## Neighbor boundary

- Provider and infrastructure capability selection belongs to the tooling-platforms router.

## Route protocol

1. Read the current host and project instructions.
2. Confirm the requested action is available in the active profile.
3. Select the narrowest eligible workflow from the public registry.
4. Load that workflow's complete instructions and only the references needed for the task.
5. Preserve side-effect and authorization boundaries.
6. Verify the outcome with evidence that matches the claim.

For the included fixture, the example target is `repo-readiness`. See the [generated route map](../../generated-route-map.md).

## Stop conditions

Stop or ask when the target is unavailable, the profile resolution is stale, an external write lacks authority, or required evidence cannot be obtained.

## Claim limit

This file is illustrative. Installing it does not configure routing, profiles, plugins, or provider capabilities.
