#!/usr/bin/env python3
"""Validate the synthetic architecture catalog, fixtures, templates, and contracts."""

from __future__ import annotations

import copy
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from render_route_maps import render


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE_CATALOG = ROOT / "catalog" / "architecture-artifacts.json"
REGISTRY_PATH = ROOT / "architecture" / "examples" / "minimal-registry.json"
RESOLUTION_PATH = ROOT / "architecture" / "examples" / "profile-resolution.json"
SCHEMA_PATH = ROOT / "architecture" / "schema" / "router-registry-v1.schema.json"
SMOKE_PATH = ROOT / "architecture" / "evals" / "smoke-cases.json"
NEGATIVE_PATH = ROOT / "architecture" / "evals" / "negative-contracts.json"
GENERATED_PATH = ROOT / "architecture" / "examples" / "generated-route-map.md"
ROUTERS_PATH = ROOT / "architecture" / "examples" / "routers"
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OWNERSHIP = {"shared", "personal", "work"}
AWARENESS = {"direct-visible", "router-aware", "direct-call-aware", "not-aware"}
SIDE_EFFECTS = {"read-only", "reversible-write", "external-write"}


def load_json(path: Path, errors: list[str]) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: cannot load JSON: {exc}")
        return {}


def valid_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    return parsed <= date.today() + timedelta(days=1)


def duplicate_ids(items: object, label: str, errors: list[str]) -> set[str]:
    ids: set[str] = set()
    if not isinstance(items, list) or not items:
        errors.append(f"{label} must be a non-empty list")
        return ids
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}] must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not ID_RE.fullmatch(item_id):
            errors.append(f"{label}[{index}] has invalid id")
            continue
        if item_id in ids:
            errors.append(f"duplicate {label[:-1]} id: {item_id}")
        ids.add(item_id)
    return ids


def validate_registry(registry: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(registry, dict):
        return ["registry must be an object"]
    if registry.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if registry.get("reference_only") is not True:
        errors.append("reference_only must be true")

    routers = registry.get("routers")
    skills = registry.get("skills")
    profiles = registry.get("profiles")
    router_ids = duplicate_ids(routers, "routers", errors)
    skill_ids = duplicate_ids(skills, "skills", errors)
    duplicate_ids(profiles, "profiles", errors)

    if isinstance(skills, list):
        for index, skill in enumerate(skills):
            if not isinstance(skill, dict):
                continue
            skill_id = skill.get("id", f"skills[{index}]")
            if not isinstance(skill.get("title"), str) or not skill["title"].strip():
                errors.append(f"{skill_id}: skill title must be non-empty")
            if skill.get("ownership") not in OWNERSHIP:
                errors.append(f"{skill_id}: invalid ownership")
            if skill.get("awareness") not in AWARENESS:
                errors.append(f"{skill_id}: invalid awareness")

    if isinstance(routers, list):
        for index, router in enumerate(routers):
            if not isinstance(router, dict):
                continue
            router_id = router.get("id", f"routers[{index}]")
            if not isinstance(router.get("title"), str) or not router["title"].strip():
                errors.append(f"{router_id}: router title must be non-empty")
            if not isinstance(router.get("description"), str) or not router["description"].strip():
                errors.append(f"{router_id}: router description must be non-empty")
            routes = router.get("routes")
            if not isinstance(routes, list) or not routes:
                errors.append(f"{router_id}: routes must be a non-empty list")
                continue
            for route_index, route in enumerate(routes):
                if not isinstance(route, dict):
                    errors.append(f"{router_id}: route {route_index} must be an object")
                    continue
                if not isinstance(route.get("intent"), str) or not route["intent"].strip():
                    errors.append(f"{router_id}: route intent must be non-empty")
                if route.get("target") not in skill_ids:
                    errors.append(f"{router_id}: unknown target {route.get('target')}")
                if route.get("side_effect") not in SIDE_EFFECTS:
                    errors.append(f"{router_id}: invalid side effect")

    skill_by_id = {
        item["id"]: item
        for item in skills or []
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if isinstance(profiles, list):
        for index, profile in enumerate(profiles):
            if not isinstance(profile, dict):
                continue
            profile_id = profile.get("id", f"profiles[{index}]")
            owners = profile.get("allowed_ownership")
            if not isinstance(owners, list) or any(owner not in OWNERSHIP for owner in owners):
                errors.append(f"{profile_id}: invalid allowed ownership")
                owners = []
            enabled = profile.get("enabled_skills")
            if not isinstance(enabled, list):
                errors.append(f"{profile_id}: enabled_skills must be a list")
                continue
            if len(enabled) != len(set(enabled)):
                errors.append(f"{profile_id}: duplicate enabled skill")
            for skill_id in enabled:
                if skill_id not in skill_ids:
                    errors.append(f"{profile_id}: profile enables unknown skill {skill_id}")
                    continue
                if skill_by_id[skill_id].get("ownership") not in owners:
                    errors.append(f"{profile_id}: enabled skill ownership is not allowed: {skill_id}")

    if len(router_ids) != 6:
        errors.append("synthetic registry must contain exactly six routers")
    return errors


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        errors.append(f"{path.relative_to(ROOT)}: missing frontmatter")
        return {}
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line or line[:1].isspace():
            errors.append(f"{path.relative_to(ROOT)}: frontmatter must use top-level scalars")
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    if set(metadata) != {"name", "description", "license"}:
        errors.append(f"{path.relative_to(ROOT)}: frontmatter keys must be name, description, license")
    if metadata.get("license") != "Apache-2.0":
        errors.append(f"{path.relative_to(ROOT)}: license must be Apache-2.0")
    return metadata


def validate_catalog(catalog: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(catalog, dict):
        return ["architecture catalog must be an object"]
    if catalog.get("schema_version") != 1:
        errors.append("architecture catalog schema_version must be 1")
    if catalog.get("repository_status") != "public-alpha":
        errors.append("architecture catalog repository_status must be public-alpha")
    if catalog.get("reference_only") is not True:
        errors.append("architecture catalog reference_only must be true")
    if not valid_date(catalog.get("last_reviewed")):
        errors.append("architecture catalog last_reviewed must be a non-future ISO date")
    artifacts = catalog.get("artifacts")
    ids = duplicate_ids(artifacts, "artifacts", errors)
    if isinstance(artifacts, list):
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                continue
            artifact_id = artifact.get("id", "artifact")
            relative = artifact.get("path")
            if not isinstance(relative, str) or relative.startswith("/") or ".." in Path(relative).parts:
                errors.append(f"{artifact_id}: invalid public path")
            elif not (ROOT / relative).exists():
                errors.append(f"{artifact_id}: missing public path {relative}")
            if artifact.get("distribution_status") != "repo-reference":
                errors.append(f"{artifact_id}: distribution_status must be repo-reference")
            evidence = artifact.get("validation_evidence")
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"{artifact_id}: validation_evidence must be non-empty")
            provenance = artifact.get("provenance")
            if not isinstance(provenance, dict) or not provenance.get("relationship"):
                errors.append(f"{artifact_id}: provenance relationship is required")
            limits = artifact.get("claim_limits")
            if not isinstance(limits, list) or not limits:
                errors.append(f"{artifact_id}: claim_limits must be non-empty")
            if not valid_date(artifact.get("last_reviewed")):
                errors.append(f"{artifact_id}: last_reviewed must be a non-future ISO date")
    if len(ids) != 6:
        errors.append("architecture catalog must contain six artifacts")
    return errors


def set_path(document: object, path: str, value: object) -> None:
    parts = path.split(".")
    cursor = document
    for part in parts[:-1]:
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    final = parts[-1]
    if isinstance(cursor, list):
        cursor[int(final)] = value
    else:
        cursor[final] = value


def mutate(registry: dict[str, object], spec: dict[str, object]) -> dict[str, object]:
    changed = copy.deepcopy(registry)
    if spec.get("operation") == "set":
        set_path(changed, str(spec["path"]), spec.get("value"))
    elif spec.get("operation") == "duplicate":
        collection = changed[str(spec["collection"])]
        collection.append(copy.deepcopy(collection[int(spec["index"])]))
    else:
        raise ValueError(f"unsupported mutation operation: {spec.get('operation')}")
    return changed


def main() -> int:
    errors: list[str] = []
    catalog = load_json(ARCHITECTURE_CATALOG, errors)
    registry = load_json(REGISTRY_PATH, errors)
    resolution = load_json(RESOLUTION_PATH, errors)
    schema = load_json(SCHEMA_PATH, errors)
    smoke = load_json(SMOKE_PATH, errors)
    negative = load_json(NEGATIVE_PATH, errors)

    errors.extend(validate_catalog(catalog))
    registry_errors = validate_registry(registry)
    errors.extend(f"registry: {item}" for item in registry_errors)

    if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema: expected JSON Schema draft 2020-12")
    if schema.get("title") != "AI Workbench synthetic router registry":
        errors.append("schema: unexpected title")

    router_ids = {item["id"] for item in registry.get("routers", [])}
    skill_ids = {item["id"] for item in registry.get("skills", [])}
    profiles = {item["id"]: item for item in registry.get("profiles", [])}
    reviewer = profiles.get("reviewer", {})

    if not isinstance(resolution, dict) or resolution.get("reference_only") is not True:
        errors.append("profile resolution must be reference_only")
    if resolution.get("profile") != "reviewer":
        errors.append("profile resolution must use the reviewer fixture")
    if set(resolution.get("enabled_routers", [])) != router_ids:
        errors.append("profile resolution enabled_routers do not match registry")
    if set(resolution.get("enabled_skills", [])) != set(reviewer.get("enabled_skills", [])):
        errors.append("profile resolution enabled_skills do not match reviewer profile")
    unavailable = {item.get("id") for item in resolution.get("unavailable_skills", [])}
    if unavailable != skill_ids - set(reviewer.get("enabled_skills", [])):
        errors.append("profile resolution unavailable_skills do not match registry")

    route_pairs = {
        (router["id"], route["target"])
        for router in registry.get("routers", [])
        for route in router.get("routes", [])
    }
    cases = smoke.get("cases") if isinstance(smoke, dict) else None
    if not isinstance(cases, list) or len(cases) != 6:
        errors.append("smoke cases must contain exactly six cases")
        cases = []
    for case in cases:
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"smoke {case.get('id')}: prompt must be non-empty")
        pair = (case.get("expected_router"), case.get("expected_target"))
        if pair not in route_pairs:
            errors.append(f"smoke {case.get('id')}: expected route pair is absent")

    mutations = negative.get("mutations") if isinstance(negative, dict) else None
    if not isinstance(mutations, list) or len(mutations) != 9:
        errors.append("negative contracts must contain exactly nine mutations")
        mutations = []
    for spec in mutations:
        changed = mutate(registry, spec)
        observed = validate_registry(changed)
        expected = spec.get("expected_error")
        if not any(expected in item for item in observed):
            errors.append(f"negative {spec.get('id')}: expected error not observed: {expected}")

    for router_id in router_ids:
        path = ROUTERS_PATH / router_id / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing router template: {path.relative_to(ROOT)}")
            continue
        metadata = parse_frontmatter(path, errors)
        if metadata.get("name") != router_id:
            errors.append(f"{path.relative_to(ROOT)}: name must match router id")

    expected_generated = render(registry)
    current_generated = GENERATED_PATH.read_text(encoding="utf-8") if GENERATED_PATH.exists() else ""
    if current_generated != expected_generated:
        errors.append("generated route map is stale")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Reference architecture validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(
        "Reference architecture validation passed: "
        f"{len(router_ids)} routers, {len(skill_ids)} skills, "
        f"{len(cases)} smoke cases, {len(mutations)} negative contracts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
