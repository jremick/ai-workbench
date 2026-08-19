#!/usr/bin/env python3
"""Validate the public skill manifest and the repository's SKILL.md contract."""

from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "catalog" / "artifacts.json"
ALLOWED_FRONTMATTER = {"name", "description", "license"}
ALLOWED_PUBLICATION_CLASSES = {
    "current-snapshot",
    "curated-projection",
    "illustrative-only",
    "superseded",
}
ALLOWED_AUDIT_CLASSES = {
    "safe-as-is",
    "safe-after-abstraction-redaction",
    "illustrative-only",
    "obsolete-superseded",
}
ALLOWED_RELATIONSHIPS = {
    "dated-public-snapshot",
    "exact-at-last-comparison",
    "independent-public",
    "sanitized-projection",
    "superseded-concept",
}
CLASS_CONTRACT = {
    "current-snapshot": ("safe-as-is", {"dated-public-snapshot", "exact-at-last-comparison"}),
    "curated-projection": ("safe-after-abstraction-redaction", {"sanitized-projection"}),
    "illustrative-only": ("illustrative-only", {"independent-public"}),
    "superseded": ("obsolete-superseded", {"superseded-concept"}),
}
REQUIRED_ARTIFACT_FIELDS = {
    "id",
    "title",
    "kind",
    "path",
    "public_version",
    "publication_class",
    "audit_classification",
    "source_relationship",
    "ownership",
    "prompt_visibility",
    "last_compared",
    "last_reviewed",
    "validation",
    "replacement",
    "notes",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def parse_scalar(value: str, path: Path, key: str, errors: list[str]) -> str:
    value = value.strip()
    if not value:
        errors.append(f"{path}: {key} must not be empty")
        return ""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            errors.append(f"{path}: {key} has invalid double-quoted YAML scalar")
            return ""
        if not isinstance(parsed, str):
            errors.append(f"{path}: {key} must be a string")
            return ""
        return parsed
    if value.startswith("'"):
        if not value.endswith("'") or len(value) < 2:
            errors.append(f"{path}: {key} has invalid single-quoted YAML scalar")
            return ""
        return value[1:-1].replace("''", "'")
    if ": " in value or value.startswith(("[", "{", "|", ">", "&", "*", "!")):
        errors.append(f"{path}: {key} must use a simple or quoted scalar")
    return value


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        errors.append(f"{path}: missing or malformed YAML frontmatter")
        return {}

    result: dict[str, str] = {}
    for line_number, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace() or ":" not in line:
            errors.append(f"{path}:{line_number}: only top-level scalar metadata is allowed")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in result:
            errors.append(f"{path}:{line_number}: duplicate frontmatter key {key!r}")
            continue
        if key not in ALLOWED_FRONTMATTER:
            errors.append(
                f"{path}:{line_number}: unsupported frontmatter key {key!r}; "
                "lifecycle metadata belongs in catalog/artifacts.json"
            )
            continue
        result[key] = parse_scalar(value, path, key, errors)
    return result


def valid_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    # A review performed just after local midnight can still be "tomorrow" on
    # a UTC-hosted CI runner. Allow one calendar day of timezone skew while
    # rejecting materially future-dated metadata.
    return parsed <= date.today() + timedelta(days=1)


def main() -> int:
    errors: list[str] = []
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {MANIFEST}: {exc}")
        return 1

    if manifest.get("schema_version") != 1:
        errors.append("catalog/artifacts.json: schema_version must be 1")
    if manifest.get("repository_status") != "public-alpha":
        errors.append("catalog/artifacts.json: repository_status must be public-alpha")
    if manifest.get("release_posture") != "no-release":
        errors.append("catalog/artifacts.json: release_posture must be no-release")
    if not valid_iso_date(manifest.get("last_reviewed")):
        errors.append("catalog/artifacts.json: last_reviewed must be a non-future ISO date")
    if not isinstance(manifest.get("source_of_truth"), str) or not manifest.get("source_of_truth"):
        errors.append("catalog/artifacts.json: source_of_truth must be a non-empty string")
    if not isinstance(manifest.get("claim_limits"), list) or not manifest.get("claim_limits"):
        errors.append("catalog/artifacts.json: claim_limits must be a non-empty list")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("catalog/artifacts.json: artifacts must be a list")
        artifacts = []

    seen: set[str] = set()
    manifest_ids: set[str] = set()
    for index, artifact in enumerate(artifacts):
        location = f"catalog/artifacts.json:artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{location}: artifact must be an object")
            continue
        missing = REQUIRED_ARTIFACT_FIELDS - artifact.keys()
        extra = artifact.keys() - REQUIRED_ARTIFACT_FIELDS
        if missing:
            errors.append(f"{location}: missing fields {sorted(missing)}")
        if extra:
            errors.append(f"{location}: unexpected fields {sorted(extra)}")

        artifact_id = artifact.get("id")
        if not isinstance(artifact_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", artifact_id):
            errors.append(f"{location}: invalid id {artifact_id!r}")
            continue
        if artifact_id in seen:
            errors.append(f"{location}: duplicate id {artifact_id!r}")
            continue
        seen.add(artifact_id)
        manifest_ids.add(artifact_id)

        expected_path = f"skills/{artifact_id}"
        if artifact.get("kind") != "skill" or artifact.get("path") != expected_path:
            errors.append(f"{location}: kind/path must identify {expected_path}")
        if artifact.get("publication_class") not in ALLOWED_PUBLICATION_CLASSES:
            errors.append(f"{location}: invalid publication_class")
        if artifact.get("audit_classification") not in ALLOWED_AUDIT_CLASSES:
            errors.append(f"{location}: invalid audit_classification")
        if artifact.get("source_relationship") not in ALLOWED_RELATIONSHIPS:
            errors.append(f"{location}: invalid source_relationship")
        class_contract = CLASS_CONTRACT.get(artifact.get("publication_class"))
        if class_contract:
            expected_audit_class, expected_relationships = class_contract
            if artifact.get("audit_classification") != expected_audit_class:
                errors.append(f"{location}: audit_classification conflicts with publication_class")
            if artifact.get("source_relationship") not in expected_relationships:
                errors.append(f"{location}: source_relationship conflicts with publication_class")
        if artifact.get("ownership") != "public-curated":
            errors.append(f"{location}: ownership must be public-curated")
        if artifact.get("prompt_visibility") != "host-decided":
            errors.append(f"{location}: prompt_visibility must be host-decided")
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(artifact.get("public_version", ""))):
            errors.append(f"{location}: public_version must be semantic version x.y.z")
        for field in ("last_compared", "last_reviewed"):
            if not valid_iso_date(artifact.get(field)):
                errors.append(f"{location}: {field} must be a non-future ISO date")
        if not isinstance(artifact.get("title"), str) or not artifact.get("title"):
            errors.append(f"{location}: title must be a non-empty string")
        if not isinstance(artifact.get("notes"), str) or not artifact.get("notes"):
            errors.append(f"{location}: notes must be a non-empty string")
        if artifact.get("replacement") is not None and not isinstance(artifact.get("replacement"), str):
            errors.append(f"{location}: replacement must be a string or null")
        if (
            not isinstance(artifact.get("validation"), list)
            or not artifact.get("validation")
            or not all(isinstance(item, str) and item for item in artifact.get("validation", []))
        ):
            errors.append(f"{location}: validation must be a non-empty list")
        if artifact.get("publication_class") == "superseded" and not artifact.get("replacement"):
            errors.append(f"{location}: superseded artifacts require a replacement")

        skill_dir = ROOT / expected_path
        skill_md = skill_dir / "SKILL.md"
        readme = skill_dir / "README.md"
        if not skill_md.is_file():
            errors.append(f"{location}: missing {skill_md.relative_to(ROOT)}")
            continue
        if not readme.is_file():
            errors.append(f"{location}: missing {readme.relative_to(ROOT)}")

        metadata = parse_frontmatter(skill_md, errors)
        if metadata.get("name") != artifact_id:
            errors.append(f"{skill_md.relative_to(ROOT)}: name must match manifest id")
        description = metadata.get("description", "")
        if not description:
            errors.append(f"{skill_md.relative_to(ROOT)}: description is required")
        elif len(description) > 1024 or "<" in description or ">" in description:
            errors.append(f"{skill_md.relative_to(ROOT)}: description violates length or character limits")
        if metadata.get("license") != "Apache-2.0":
            errors.append(f"{skill_md.relative_to(ROOT)}: license must be Apache-2.0")

        skill_json = skill_dir / "skill.json"
        if skill_json.exists():
            try:
                package_metadata = json.loads(skill_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{skill_json.relative_to(ROOT)}: invalid JSON: {exc}")
            else:
                if package_metadata.get("version") != artifact.get("public_version"):
                    errors.append(f"{skill_json.relative_to(ROOT)}: version must match public manifest")
                if package_metadata.get("license") != "Apache-2.0":
                    errors.append(f"{skill_json.relative_to(ROOT)}: license must be Apache-2.0")

        readme_text = readme.read_text(encoding="utf-8")
        if artifact.get("publication_class") == "superseded":
            if "> **Status: Superseded public snapshot.**" not in readme_text:
                errors.append(f"{readme.relative_to(ROOT)}: missing superseded status banner")
        if artifact.get("publication_class") == "illustrative-only":
            if "> **Status: Illustrative public example.**" not in readme_text:
                errors.append(f"{readme.relative_to(ROOT)}: missing illustrative status banner")
        if artifact.get("publication_class") == "curated-projection":
            if "> **Status: Curated public projection.**" not in readme_text:
                errors.append(f"{readme.relative_to(ROOT)}: missing curated-projection status banner")
        if artifact.get("publication_class") == "current-snapshot":
            if "> **Status: Current public snapshot.**" not in readme_text:
                errors.append(f"{readme.relative_to(ROOT)}: missing current-snapshot status banner")

    skill_ids = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    missing_from_manifest = skill_ids - manifest_ids
    missing_from_tree = manifest_ids - skill_ids
    if missing_from_manifest:
        errors.append(f"skills missing from manifest: {sorted(missing_from_manifest)}")
    if missing_from_tree:
        errors.append(f"manifest skills missing from tree: {sorted(missing_from_tree)}")

    if errors:
        for error in errors:
            fail(error)
        print(f"Public catalog validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Public catalog validation passed for {len(artifacts)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
