#!/usr/bin/env python3
"""Deterministic model delegation and cost-routing recommendations for Codex."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = SCRIPT_DIR.parent
DATA_DIR = PACKAGE_DIR / "data"
DEFAULT_CATALOG_PATH = DATA_DIR / "model_catalog.json"
DEFAULT_EVAL_PATH = DATA_DIR / "eval_cases.json"
DEFAULT_AA_CACHE_PATH = DATA_DIR / "artificial_analysis_models.cache.json"
DEFAULT_RECOMMENDATION_VALUES_PATH = DATA_DIR / "recommendation_values.json"
DEFAULT_MODEL_SYSTEM_PATH = DATA_DIR / "model_system.json"
AA_ENDPOINT = "https://artificialanalysis.ai/api/v2/data/llms/models"

WORK_TYPES = {
    "trivial",
    "implementation",
    "code_review",
    "long_horizon_coding",
    "research",
    "docs_writing",
    "high_risk_analysis",
    "local_private",
    "frontend_qa",
}

COST_POLICY_WEIGHT = {
    "cheap": 1.4,
    "balanced": 0.9,
    "quality": 0.35,
}

QUALITY_POLICY_WEIGHT = {
    "cheap": 0.8,
    "balanced": 1.0,
    "quality": 1.25,
}

WORK_TYPE_DELEGATION = {
    "trivial": False,
    "implementation": False,
    "code_review": True,
    "long_horizon_coding": True,
    "research": True,
    "docs_writing": False,
    "high_risk_analysis": True,
    "local_private": True,
    "frontend_qa": False,
}

SECURITY_TERMS = [
    "api key",
    "auth",
    "credential",
    "crypto",
    "dependency",
    "env var",
    "injection",
    "jwt",
    "oauth",
    "password",
    "permission",
    "pii",
    "privacy",
    "secret",
    "session",
    "sso",
    "supply chain",
    "token",
]


class ModelManagerError(Exception):
    """Expected CLI error."""


@dataclass(frozen=True)
class TaskContext:
    task: str
    work_type: str
    risk: str
    privacy: str
    needs_live_research: bool
    long_horizon: bool
    cost_policy: str
    available_backends: set[str]
    max_routes: int


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_optional_json(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    return load_json(path)


def display_path(path: Path | str | None) -> str | None:
    if path is None:
        return None
    candidate = Path(path)
    try:
        return str(candidate.resolve().relative_to(PACKAGE_DIR.resolve()))
    except ValueError:
        return str(candidate)


def normalize_key(value: str | None) -> str:
    if not value:
        return ""
    return "".join(char.lower() for char in value if char.isalnum())


def load_catalog(catalog_path: Path, aa_cache_path: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    catalog = load_json(catalog_path)
    source_status: dict[str, Any] = {
        "artificial_analysis_cache": {
            "path": str(aa_cache_path) if aa_cache_path else None,
            "used": False,
            "matched_models": 0,
            "proxy_models": 0,
        }
    }
    if aa_cache_path and aa_cache_path.exists():
        cache = load_json(aa_cache_path)
        match_counts = apply_artificial_analysis_cache(catalog, cache)
        source_status["artificial_analysis_cache"].update(
            {
                "used": True,
                "matched_models": match_counts["matched_models"],
                "proxy_models": match_counts["proxy_models"],
                "attribution_required": True,
            }
        )
    return catalog, source_status


def apply_artificial_analysis_cache(catalog: dict[str, Any], cache: dict[str, Any]) -> dict[str, int]:
    by_key: dict[str, dict[str, Any]] = {}
    for item in cache.get("data", []):
        for key in (item.get("id"), item.get("name"), item.get("slug")):
            normalized = normalize_key(key)
            if normalized:
                by_key[normalized] = item

    matched = 0
    proxy_matched = 0
    for model in catalog.get("models", []):
        aa_config = model.get("artificial_analysis", {})
        match_value = aa_config.get("match")
        aa_item = by_key.get(normalize_key(match_value))
        proxy_status = None
        if not aa_item and aa_config.get("previous_proxy"):
            aa_item = by_key.get(normalize_key(aa_config.get("previous_proxy")))
            proxy_status = "previous_model_proxy"
        if not aa_item:
            continue
        model["artificial_analysis_live"] = {
            "id": aa_item.get("id"),
            "name": aa_item.get("name"),
            "slug": aa_item.get("slug"),
            "match_requested": match_value,
            "proxy_status": proxy_status,
            "evaluations": aa_item.get("evaluations", {}),
            "pricing": aa_item.get("pricing", {}),
            "median_output_tokens_per_second": aa_item.get("median_output_tokens_per_second"),
            "median_time_to_first_token_seconds": aa_item.get("median_time_to_first_token_seconds"),
        }
        if proxy_status:
            proxy_matched += 1
        else:
            matched += 1
    return {"matched_models": matched, "proxy_models": proxy_matched}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def infer_work_type(task: str, *, risk: str, privacy: str, needs_live_research: bool, long_horizon: bool) -> str:
    text = task.lower()
    if privacy == "local_only" or any(term in text for term in ["offline", "local only", "do not send", "private local"]):
        return "local_private"
    if risk == "high" or any(term in text for term in ["irreversible", "production migration", "failure mode", "stress test"]):
        return "high_risk_analysis"
    if needs_live_research or any(term in text for term in ["latest", "current", "research", "leaderboard", "market scan", "source"]):
        return "research"
    if long_horizon or any(
        term in text
        for term in [
            "multi-file",
            "long-horizon",
            "repository migration",
            "unfamiliar modules",
            "large codebase",
            "end-to-end implementation",
        ]
    ):
        return "long_horizon_coding"
    if any(term in text for term in ["review this pr", "code review", "pull request", "hidden regression", "missing tests"]):
        return "code_review"
    if any(term in text for term in ["browser", "screenshot", "responsive", "playwright", "frontend qa", "local app"]):
        return "frontend_qa"
    if any(term in text for term in ["write", "draft", "rewrite", "summarize", "document", "docs"]):
        return "docs_writing"
    if any(term in text for term in ["implement", "fix", "refactor", "test", "build"]):
        return "implementation"
    if len(task.split()) <= 8:
        return "trivial"
    return "implementation"


def build_context(args: argparse.Namespace) -> TaskContext:
    work_type = args.work_type
    if work_type == "auto":
        work_type = infer_work_type(
            args.task,
            risk=args.risk,
            privacy=args.privacy,
            needs_live_research=args.needs_live_research,
            long_horizon=args.long_horizon,
        )
    if work_type not in WORK_TYPES:
        raise ModelManagerError(f"unknown work type: {work_type}")

    available = {item.strip() for item in args.available_backends.split(",") if item.strip()}
    return TaskContext(
        task=args.task,
        work_type=work_type,
        risk=args.risk,
        privacy=args.privacy,
        needs_live_research=args.needs_live_research,
        long_horizon=args.long_horizon,
        cost_policy=args.cost_policy,
        available_backends=available,
        max_routes=args.max_routes,
    )


def model_index(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(model["id"]): model for model in catalog.get("models", [])}


def model_available(model: dict[str, Any], context: TaskContext) -> bool:
    if context.work_type == "trivial" and model["id"] != "parent/codex-default":
        return False
    backend = str(model["backend"])
    if backend not in context.available_backends:
        return False
    if context.privacy == "local_only" and model.get("privacy_level") != "local":
        return False
    if context.needs_live_research and not model.get("supports_live_research", False) and backend != "codex":
        return False
    return True


def route_command(model: dict[str, Any], mode: str) -> str | None:
    backend = model["backend"]
    target = model["route_target"]
    if target == "parent":
        return None
    if backend == "claude_subscription":
        return f"codex-model exec {target} --mode {mode}"
    if backend == "perplexity":
        return f"codex-model exec {target} --mode {mode}"
    if backend == "lmstudio":
        return f"codex-model exec {target} --mode {mode}"
    if backend == "codex":
        return None
    return None


def security_review_needed(task: str) -> bool:
    text = task.lower()
    return any(term in text for term in SECURITY_TERMS)


def route_complexity(context: TaskContext) -> str:
    text = context.task.lower()
    if context.risk == "high" or context.work_type in {"high_risk_analysis", "long_horizon_coding"}:
        return "high"
    if any(term in text for term in ["architecture", "migration", "production", "release", "reliability"]):
        return "high"
    if context.work_type in {"trivial", "docs_writing"}:
        return "low"
    if context.work_type == "implementation" and len(context.task.split()) <= 12:
        return "low"
    if context.work_type in {"research", "implementation", "code_review", "frontend_qa", "local_private"}:
        return "medium"
    return "medium"


def review_tier(context: TaskContext, complexity: str) -> str | None:
    text = context.task.lower()
    if context.work_type in {"trivial", "docs_writing", "research", "local_private", "frontend_qa"}:
        return None
    if context.risk == "high" or complexity == "high" or context.work_type in {"code_review", "long_horizon_coding"}:
        return "production"
    if any(term in text for term in ["production", "release", "ship", "customer", "migration"]):
        return "production"
    if any(term in text for term in ["prototype", "mvp", "demo", "experiment", "play"]):
        return "play"
    if context.work_type == "implementation":
        return "play" if complexity == "low" else "production"
    return None


def model_system_payload(model_system: dict[str, Any] | None) -> dict[str, Any] | None:
    if not model_system:
        return None
    payload = model_system.get("model_system") or model_system.get("modelSystem") or model_system
    if not isinstance(payload, dict) or payload.get("enabled", True) is False:
        return None
    return payload


def model_ref_id(ref: Any) -> str | None:
    if ref is None:
        return None
    if isinstance(ref, str):
        return ref
    if isinstance(ref, dict):
        value = ref.get("model") or ref.get("id")
        return str(value) if value else None
    return None


def tier_ref(section: dict[str, Any], tier: str) -> str | None:
    return model_ref_id(section.get(tier))


def recommended_mode(context: TaskContext) -> str:
    if context.work_type in {"trivial", "docs_writing"}:
        return "none"
    if context.work_type == "implementation":
        return "read"
    return "read"


def deepswe_bonus(model: dict[str, Any], context: TaskContext) -> float:
    if context.work_type != "long_horizon_coding":
        return 0.0
    score = model.get("benchmark_scores", {}).get("deepswe", {}).get("score")
    if not isinstance(score, (int, float)):
        return 0.0
    return float(score) / 10.0


def score_model(model: dict[str, Any], context: TaskContext) -> tuple[float, list[str]]:
    reasons: list[str] = []
    work_score = float(model.get("work_type_scores", {}).get(context.work_type, 0))
    score = work_score * 2.0
    reasons.append(f"work_type_fit={work_score:g}")

    quality = float(model.get("quality_tier", 0))
    quality_weight = QUALITY_POLICY_WEIGHT[context.cost_policy]
    score += quality * quality_weight
    reasons.append(f"quality_tier={quality:g}")

    cost = float(model.get("cost_tier", 0))
    cost_weight = COST_POLICY_WEIGHT[context.cost_policy]
    score -= cost * cost_weight
    reasons.append(f"cost_tier={cost:g}")

    latency = float(model.get("latency_tier", 0))
    score -= latency * 0.2

    if context.risk == "high":
        score += quality * 0.8
        if cost <= 1 and quality < 4:
            score -= 8
            reasons.append("penalized_cheap_for_high_risk")

    if context.work_type == "research" and model.get("supports_live_research"):
        score += 6
        reasons.append("live_research_support")

    if context.work_type in {"implementation", "frontend_qa"} and model.get("supports_tools"):
        score += 3
        reasons.append("tool_support")

    if context.work_type == "code_review" and model["backend"] == "claude_subscription":
        score += 4
        reasons.append("subscription_second_opinion")

    if context.work_type == "local_private" and model.get("privacy_level") == "local":
        score += 10
        reasons.append("local_privacy_match")

    bonus = deepswe_bonus(model, context)
    if bonus:
        score += bonus
        reasons.append(f"deepswe_bonus={bonus:.1f}")

    if model["id"] == "parent/codex-default" and context.work_type in {"trivial", "implementation", "frontend_qa"}:
        score += 4
        reasons.append("parent_codex_default")

    aa = model.get("artificial_analysis_live")
    if isinstance(aa, dict):
        if aa.get("proxy_status"):
            reasons.append(f"artificial_analysis_proxy={aa['proxy_status']}")
        evaluations = aa.get("evaluations", {})
        pricing = aa.get("pricing", {})
        intelligence = evaluations.get("artificial_analysis_intelligence_index")
        coding = evaluations.get("artificial_analysis_coding_index")
        if isinstance(intelligence, (int, float)):
            score += min(float(intelligence) / 20.0, 5.0)
            reasons.append("artificial_analysis_intelligence")
        if context.work_type in {"implementation", "code_review", "long_horizon_coding"} and isinstance(coding, (int, float)):
            score += min(float(coding) / 20.0, 5.0)
            reasons.append("artificial_analysis_coding")
        blended = pricing.get("price_1m_blended_3_to_1")
        if isinstance(blended, (int, float)):
            score -= min(float(blended) / 5.0, 6.0) * COST_POLICY_WEIGHT[context.cost_policy]
            reasons.append("artificial_analysis_price")

    return round(score, 3), reasons


def configured_route(
    model_id: str | None,
    role: str,
    context: TaskContext,
    catalog_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    if not model_id:
        return None
    model = catalog_by_id.get(model_id)
    if not model:
        return {
            "role": role,
            "model": model_id,
            "available": False,
            "blocked_reason": "model is not present in model_catalog.json",
        }
    available = model_available(model, context)
    if available:
        score, reasons = score_model(model, context)
    else:
        score, reasons = 0.0, []
    route = build_route(model, score, reasons, context)
    route["role"] = role
    route["available"] = available
    if not available:
        if context.privacy == "local_only" and model.get("privacy_level") != "local":
            route["blocked_reason"] = "privacy constraint blocks external model"
        elif str(model["backend"]) not in context.available_backends:
            route["blocked_reason"] = f"backend {model['backend']} is not in available_backends"
        else:
            route["blocked_reason"] = "model is not available for this context"
    return route


def should_delegate(context: TaskContext, top_model: dict[str, Any]) -> bool:
    if context.work_type == "frontend_qa":
        return False
    if context.work_type == "implementation" and top_model["backend"] == "codex":
        return False
    return WORK_TYPE_DELEGATION.get(context.work_type, True)


def build_route(model: dict[str, Any], score: float, reasons: list[str], context: TaskContext) -> dict[str, Any]:
    mode = recommended_mode(context)
    settings = dict(model.get("default_settings", {}))
    if context.work_type == "long_horizon_coding" and "benchmark_scores" in model:
        deep = model["benchmark_scores"].get("deepswe", {})
        if "setting" in deep:
            settings.setdefault("benchmark_setting", deep["setting"])
    if context.risk == "high" and model["backend"] == "codex":
        settings["reasoning_effort"] = "high"

    return {
        "role": role_for_work_type(context.work_type, model),
        "model": model["id"],
        "display_name": model["display_name"],
        "backend": model["backend"],
        "provider": model["provider"],
        "route_target": model["route_target"],
        "mode": mode,
        "settings": settings,
        "score": score,
        "reasons": reasons,
        "route_command": route_command(model, mode),
    }


def role_for_work_type(work_type: str, model: dict[str, Any]) -> str:
    if work_type == "research":
        return "research_scout"
    if work_type == "code_review":
        return "code_review_second_opinion"
    if work_type == "long_horizon_coding":
        return "coding_agent_candidate"
    if work_type == "high_risk_analysis":
        return "risk_critic"
    if work_type == "local_private":
        return "local_private_reader"
    if model["id"] == "parent/codex-default":
        return "parent_executor"
    return "assistant"


def build_model_system_route(
    context: TaskContext,
    catalog: dict[str, Any],
    model_system: dict[str, Any] | None,
) -> dict[str, Any] | None:
    stack = model_system_payload(model_system)
    if not stack:
        return None

    catalog_by_id = model_index(catalog)
    complexity = route_complexity(context)
    review = review_tier(context, complexity)
    needs_security = security_review_needed(context.task)

    orchestrators = stack.get("orchestrators", {})
    coders = stack.get("coders", {})
    reviewers = stack.get("reviewers", {})

    selector = configured_route(model_ref_id(stack.get("selector")), "selector", context, catalog_by_id)
    orchestrator = configured_route(tier_ref(orchestrators, complexity), f"orchestrator_{complexity}", context, catalog_by_id)
    coder = configured_route(tier_ref(coders, complexity), f"coder_{complexity}", context, catalog_by_id)
    reviewer = configured_route(tier_ref(reviewers, review), f"reviewer_{review}", context, catalog_by_id) if review else None
    security = configured_route(
        model_ref_id(stack.get("security_reviewer") or stack.get("securityReviewer")),
        "security_reviewer",
        context,
        catalog_by_id,
    ) if needs_security else None

    notes = [
        "Model-system routing is deterministic: complexity, review tier, and security review are derived from task metadata.",
        "The active executor remains parent Codex unless the operator explicitly runs a returned route command.",
    ]
    if coder and not coder.get("available", True):
        notes.append("Configured coder route is blocked; fall back to the ranked recommendation list.")
    if needs_security and not security:
        notes.append("Security-sensitive task detected, but no security reviewer is configured.")

    return {
        "schema_version": "0.1.0",
        "enabled": True,
        "complexity": complexity,
        "review_tier": review,
        "security_review": needs_security,
        "selector": selector,
        "orchestrator": orchestrator,
        "coder": coder,
        "reviewer": reviewer,
        "security_reviewer": security,
        "notes": notes,
    }


def recommend(
    context: TaskContext,
    catalog: dict[str, Any],
    source_status: dict[str, Any] | None = None,
    model_system: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidates = []
    unavailable = []
    for model in catalog["models"]:
        if model_available(model, context):
            score, reasons = score_model(model, context)
            candidates.append((score, model, reasons))
        else:
            unavailable.append(model["id"])

    if not candidates:
        raise ModelManagerError("no candidate models available for this context")

    candidates.sort(key=lambda item: item[0], reverse=True)
    top_model = candidates[0][1]
    delegate = should_delegate(context, top_model)
    routes = [
        build_route(model, score, reasons, context)
        for score, model, reasons in candidates[: context.max_routes]
    ]

    notes = []
    if context.privacy == "local_only":
        notes.append("Privacy constraint forces local-only routing.")
    if context.work_type == "long_horizon_coding":
        notes.append("DeepSWE score is weighted because the task is long-horizon software engineering.")
    if context.work_type in {"implementation", "frontend_qa"} and top_model["backend"] == "codex":
        notes.append("Parent Codex remains owner because integrated tools, edits, and verification matter.")
    if context.work_type == "research":
        notes.append("Perplexity/Sonar is preferred for live source discovery.")

    result = {
        "schema_version": "0.1.0",
        "delegate": delegate,
        "work_type": context.work_type,
        "risk": context.risk,
        "privacy": context.privacy,
        "cost_policy": context.cost_policy,
        "primary_owner": "parent_codex",
        "recommended_routes": routes,
        "unavailable_models": unavailable,
        "source_versions": {
            "catalog_version": catalog.get("version"),
            "catalog_last_updated": catalog.get("last_updated"),
            "sources": catalog.get("sources", {}),
            "source_status": source_status or {},
        },
        "notes": notes,
    }
    model_system_route = build_model_system_route(context, catalog, model_system)
    if model_system_route:
        result["model_system_route"] = model_system_route
    return result


def run_eval(cases: dict[str, Any], catalog: dict[str, Any], model_system: dict[str, Any] | None = None) -> dict[str, Any]:
    results = []
    passed = 0
    for case in cases["cases"]:
        flags = case.get("flags", {})
        context = TaskContext(
            task=case["task"],
            work_type=infer_work_type(
                case["task"],
                risk=flags.get("risk", "normal"),
                privacy=flags.get("privacy", "standard"),
                needs_live_research=flags.get("needs_live_research", False),
                long_horizon=flags.get("long_horizon", False),
            ),
            risk=flags.get("risk", "normal"),
            privacy=flags.get("privacy", "standard"),
            needs_live_research=flags.get("needs_live_research", False),
            long_horizon=flags.get("long_horizon", False),
            cost_policy=flags.get("cost_policy", "balanced"),
            available_backends=set(flags.get("available_backends", ["codex", "claude_subscription", "perplexity", "lmstudio"])),
            max_routes=3,
        )
        plan = recommend(context, catalog, model_system=model_system)
        top = plan["recommended_routes"][0]
        system_route = plan.get("model_system_route")
        failures = []
        expect = case["expect"]
        if "work_type" in expect and plan["work_type"] != expect["work_type"]:
            failures.append(f"work_type expected {expect['work_type']} got {plan['work_type']}")
        if "delegate" in expect and plan["delegate"] != expect["delegate"]:
            failures.append(f"delegate expected {expect['delegate']} got {plan['delegate']}")
        if "top_backend" in expect and top["backend"] != expect["top_backend"]:
            failures.append(f"top_backend expected {expect['top_backend']} got {top['backend']}")
        if "top_model_any_of" in expect and top["model"] not in expect["top_model_any_of"]:
            failures.append(f"top_model expected one of {expect['top_model_any_of']} got {top['model']}")
        if "not_top_model" in expect and top["model"] == expect["not_top_model"]:
            failures.append(f"top_model should not be {top['model']}")
        if "complexity" in expect:
            actual = system_route.get("complexity") if system_route else None
            if actual != expect["complexity"]:
                failures.append(f"complexity expected {expect['complexity']} got {actual}")
        if "review_tier" in expect:
            actual = system_route.get("review_tier") if system_route else None
            if actual != expect["review_tier"]:
                failures.append(f"review_tier expected {expect['review_tier']} got {actual}")
        if "security_review" in expect:
            actual = system_route.get("security_review") if system_route else None
            if actual != expect["security_review"]:
                failures.append(f"security_review expected {expect['security_review']} got {actual}")

        ok = not failures
        passed += 1 if ok else 0
        results.append(
            {
                "name": case["name"],
                "passed": ok,
                "failures": failures,
                "work_type": plan["work_type"],
                "delegate": plan["delegate"],
                "top_model": top["model"],
                "top_backend": top["backend"],
                "complexity": system_route.get("complexity") if system_route else None,
                "review_tier": system_route.get("review_tier") if system_route else None,
                "security_review": system_route.get("security_review") if system_route else None,
            }
        )

    return {
        "schema_version": "0.1.0",
        "passed": passed,
        "total": len(cases["cases"]),
        "ok": passed == len(cases["cases"]),
        "results": results,
    }


def selected_artificial_analysis_values(model: dict[str, Any]) -> dict[str, Any] | None:
    aa = model.get("artificial_analysis_live")
    if not isinstance(aa, dict):
        return None

    evaluations = aa.get("evaluations", {})
    pricing = aa.get("pricing", {})
    return {
        "id": aa.get("id"),
        "name": aa.get("name"),
        "slug": aa.get("slug"),
        "match_requested": aa.get("match_requested"),
        "proxy_status": aa.get("proxy_status"),
        "evaluations": {
            "artificial_analysis_intelligence_index": evaluations.get("artificial_analysis_intelligence_index"),
            "artificial_analysis_coding_index": evaluations.get("artificial_analysis_coding_index"),
        },
        "pricing": {
            "price_1m_blended_3_to_1": pricing.get("price_1m_blended_3_to_1"),
        },
        "speed": {
            "median_output_tokens_per_second": aa.get("median_output_tokens_per_second"),
            "median_time_to_first_token_seconds": aa.get("median_time_to_first_token_seconds"),
        },
    }


def build_recommendation_values(
    catalog: dict[str, Any],
    source_status: dict[str, Any],
    cases: dict[str, Any],
    model_system: dict[str, Any] | None = None,
) -> dict[str, Any]:
    aa_status = dict(source_status.get("artificial_analysis_cache", {}))
    aa_status["path"] = display_path(aa_status.get("path"))

    model_values = []
    for model in catalog.get("models", []):
        aa_values = selected_artificial_analysis_values(model)
        if not aa_values:
            continue
        model_values.append(
            {
                "model": model["id"],
                "display_name": model["display_name"],
                "provider": model["provider"],
                "backend": model["backend"],
                "artificial_analysis": aa_values,
            }
        )

    profiles = []
    for case in cases["cases"]:
        flags = case.get("flags", {})
        context = TaskContext(
            task=case["task"],
            work_type=infer_work_type(
                case["task"],
                risk=flags.get("risk", "normal"),
                privacy=flags.get("privacy", "standard"),
                needs_live_research=flags.get("needs_live_research", False),
                long_horizon=flags.get("long_horizon", False),
            ),
            risk=flags.get("risk", "normal"),
            privacy=flags.get("privacy", "standard"),
            needs_live_research=flags.get("needs_live_research", False),
            long_horizon=flags.get("long_horizon", False),
            cost_policy=flags.get("cost_policy", "balanced"),
            available_backends=set(flags.get("available_backends", ["codex", "claude_subscription", "perplexity", "lmstudio"])),
            max_routes=3,
        )
        plan = recommend(context, catalog, source_status, model_system)
        top = plan["recommended_routes"][0]
        profiles.append(
            {
                "name": case["name"],
                "task": case["task"],
                "flags": flags,
                "work_type": plan["work_type"],
                "delegate": plan["delegate"],
                "top_model": top["model"],
                "top_backend": top["backend"],
                "recommended_routes": plan["recommended_routes"],
                "model_system_route": plan.get("model_system_route"),
            }
        )

    return {
        "schema_version": "0.1.0",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": "Artificial Analysis + committed catalog policy",
        "attribution_required": bool(aa_status.get("attribution_required")),
        "artificial_analysis_cache": aa_status,
        "model_values": model_values,
        "recommendation_profiles": profiles,
        "notes": [
            "This file intentionally stores only non-secret benchmark-derived values and route recommendations.",
            "The Artificial Analysis API key is supplied at runtime and is not stored here.",
            "Raw Artificial Analysis cache data remains ignored by git.",
            "Models with proxy_status use a labelled previous-model proxy only until the requested model appears in Artificial Analysis.",
        ],
    }


def write_recommendation_values(output_path: Path, data: dict[str, Any]) -> dict[str, Any]:
    write_json(output_path, data)
    return {
        "ok": True,
        "output": str(output_path),
        "model_values": len(data.get("model_values", [])),
        "recommendation_profiles": len(data.get("recommendation_profiles", [])),
        "attribution_required": data.get("attribution_required", False),
    }


def model_system_template() -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "model_system": {
            "enabled": True,
            "selector": {
                "model": "parent/codex-default",
                "notes": "Deterministic policy selector; replace with a stronger model id only if your executor supports it.",
            },
            "orchestrators": {
                "low": "parent/codex-default",
                "medium": "openai/gpt-5.4",
                "high": "openai/gpt-5.5",
            },
            "coders": {
                "low": "parent/codex-default",
                "medium": "openai/gpt-5.4",
                "high": "openai/gpt-5.5",
            },
            "reviewers": {
                "play": "claude/sonnet",
                "production": "claude/opus",
            },
            "security_reviewer": "claude/opus",
        },
        "notes": [
            "Use model ids from data/model_catalog.json.",
            "This config chooses role routes; Model Manager still returns ranked alternatives and does not execute them automatically.",
        ],
    }


def refresh_artificial_analysis(output_path: Path) -> dict[str, Any]:
    api_key = os.environ.get("ARTIFICIAL_ANALYSIS_API_KEY")
    if not api_key:
        raise ModelManagerError("ARTIFICIAL_ANALYSIS_API_KEY is not set")
    request = urllib.request.Request(AA_ENDPOINT, headers={"x-api-key": api_key}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ModelManagerError(f"Artificial Analysis API returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise ModelManagerError(f"Artificial Analysis API request failed: {exc}") from exc

    if payload.get("status") != 200:
        raise ModelManagerError(f"Artificial Analysis API returned status {payload.get('status')}")
    write_json(output_path, payload)
    return {
        "ok": True,
        "output": str(output_path),
        "models": len(payload.get("data", [])),
        "source": "Artificial Analysis",
        "attribution_required": True,
    }


def validate_skill(skill_dir: Path) -> dict[str, Any]:
    failures: list[str] = []
    required_files = [
        "SKILL.md",
        "README.md",
        "scripts/model_manager.py",
        "data/model_catalog.json",
        "data/model_system.json",
        "data/eval_cases.json",
        "data/recommendation_values.json",
        "tests/test_model_manager.py",
        "docs/benchmark-sources.md",
    ]
    for rel_path in required_files:
        if not (skill_dir / rel_path).exists():
            failures.append(f"missing required file: {rel_path}")

    if (skill_dir / "data/artificial_analysis_models.cache.json").exists():
        failures.append("raw Artificial Analysis cache must not be committed")

    legacy_plugin_path = "plugins/" + "model-manager"
    for rel_path in ["SKILL.md", "README.md"]:
        path = skill_dir / rel_path
        if path.exists() and legacy_plugin_path in path.read_text(encoding="utf-8"):
            failures.append(f"{rel_path} still contains old plugin-root command paths")

    try:
        catalog = load_json(skill_dir / "data/model_catalog.json")
        model_system = load_json(skill_dir / "data/model_system.json")
        catalog_ids = {str(model["id"]) for model in catalog.get("models", [])}
        stack = model_system_payload(model_system) or {}
        configured_ids: list[str] = []
        for value in [
            stack.get("selector"),
            *(stack.get("orchestrators", {}) or {}).values(),
            *(stack.get("coders", {}) or {}).values(),
            *(stack.get("reviewers", {}) or {}).values(),
            stack.get("security_reviewer"),
        ]:
            if isinstance(value, dict):
                value = value.get("model")
            if value:
                configured_ids.append(str(value))
        for model_id in configured_ids:
            if model_id and model_id not in catalog_ids:
                failures.append(f"model_system references missing catalog model: {model_id}")
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        failures.append(f"could not validate catalog/model_system: {exc}")

    recommendation_values = skill_dir / "data/recommendation_values.json"
    if recommendation_values.exists():
        rendered = recommendation_values.read_text(encoding="utf-8").lower()
        for marker in ["api_key", "artificial_analysis_api_key", "x-api-key"]:
            if marker in rendered:
                failures.append(f"recommendation_values contains secret-like marker: {marker}")

    return {
        "ok": not failures,
        "skill_dir": str(skill_dir),
        "failures": failures,
    }


def print_result(data: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2))
    else:
        if isinstance(data, dict) and "recommended_routes" in data:
            print(f"work_type: {data['work_type']}")
            print(f"delegate: {str(data['delegate']).lower()}")
            model_system_route = data.get("model_system_route")
            if model_system_route:
                print(
                    "model_system: "
                    f"complexity={model_system_route['complexity']} "
                    f"review={model_system_route['review_tier'] or 'none'} "
                    f"security={str(model_system_route['security_review']).lower()}"
                )
                coder = model_system_route.get("coder")
                if coder:
                    status = "available" if coder.get("available", True) else f"blocked: {coder.get('blocked_reason')}"
                    print(f"coder: {coder['model']} via {coder['backend']} ({status})")
            for route in data["recommended_routes"]:
                print(f"- {route['model']} via {route['backend']} score={route['score']}")
        else:
            print(json.dumps(data, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recommend model delegation and routing policy for Codex tasks.")
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG_PATH), help="Path to model catalog JSON.")
    parser.add_argument("--aa-cache", default=str(DEFAULT_AA_CACHE_PATH), help="Optional Artificial Analysis cache JSON.")
    parser.add_argument("--model-system", default=str(DEFAULT_MODEL_SYSTEM_PATH), help="Optional model-system role-stack JSON.")
    parser.add_argument("--no-model-system", action="store_true", help="Disable model-system role-stack routing.")
    sub = parser.add_subparsers(dest="command", required=True)

    recommend_cmd = sub.add_parser("recommend", help="Recommend a route plan for a task.")
    recommend_cmd.add_argument("--task", required=True)
    recommend_cmd.add_argument("--work-type", choices=["auto", *sorted(WORK_TYPES)], default="auto")
    recommend_cmd.add_argument("--risk", choices=["normal", "high"], default="normal")
    recommend_cmd.add_argument("--privacy", choices=["standard", "local_only"], default="standard")
    recommend_cmd.add_argument("--needs-live-research", action="store_true")
    recommend_cmd.add_argument("--long-horizon", action="store_true")
    recommend_cmd.add_argument("--cost-policy", choices=["cheap", "balanced", "quality"], default="balanced")
    recommend_cmd.add_argument(
        "--available-backends",
        default="codex,claude_subscription,perplexity,lmstudio",
        help="Comma-separated backends available in the current environment.",
    )
    recommend_cmd.add_argument("--max-routes", type=int, default=3)
    recommend_cmd.add_argument("--json", action="store_true")

    eval_cmd = sub.add_parser("eval", help="Run deterministic routing evals.")
    eval_cmd.add_argument("--cases", default=str(DEFAULT_EVAL_PATH))
    eval_cmd.add_argument("--json", action="store_true")

    template_cmd = sub.add_parser("model-system-template", help="Print a public-friendly model-system config template.")
    template_cmd.add_argument("--output", help="Optional output path. Defaults to stdout.")
    template_cmd.add_argument("--json", action="store_true")

    values_cmd = sub.add_parser("write-recommendation-values", help="Write sanitized recommendation values from the current catalog/cache.")
    values_cmd.add_argument("--cases", default=str(DEFAULT_EVAL_PATH))
    values_cmd.add_argument("--output", default=str(DEFAULT_RECOMMENDATION_VALUES_PATH))
    values_cmd.add_argument("--json", action="store_true")

    refresh_cmd = sub.add_parser("refresh-artificial-analysis", help="Fetch Artificial Analysis model data into a local cache.")
    refresh_cmd.add_argument("--output", default=str(DATA_DIR / "artificial_analysis_models.cache.json"))
    refresh_cmd.add_argument("--json", action="store_true")

    validate_skill_cmd = sub.add_parser("validate-skill", help="Validate the standalone skill package.")
    validate_skill_cmd.add_argument("--skill-dir", default=str(PACKAGE_DIR))
    validate_skill_cmd.add_argument("--json", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "refresh-artificial-analysis":
            result = refresh_artificial_analysis(Path(args.output))
            print_result(result, args.json)
            return 0

        if args.command == "validate-skill":
            result = validate_skill(Path(args.skill_dir))
            print_result(result, args.json)
            return 0 if result["ok"] else 1

        if args.command == "model-system-template":
            result = model_system_template()
            if args.output:
                write_json(Path(args.output), result)
                print_result({"ok": True, "output": args.output}, args.json)
            else:
                print_result(result, True)
            return 0

        catalog, source_status = load_catalog(Path(args.catalog), Path(args.aa_cache))
        model_system = None if args.no_model_system else load_optional_json(Path(args.model_system))
        if args.command == "write-recommendation-values":
            cases = load_json(Path(args.cases))
            values = build_recommendation_values(catalog, source_status, cases, model_system)
            result = write_recommendation_values(Path(args.output), values)
            print_result(result, args.json)
            return 0

        if args.command == "recommend":
            context = build_context(args)
            result = recommend(context, catalog, source_status, model_system)
            print_result(result, args.json)
            return 0

        if args.command == "eval":
            cases = load_json(Path(args.cases))
            result = run_eval(cases, catalog, model_system)
            print_result(result, args.json)
            return 0 if result["ok"] else 1

        raise ModelManagerError(f"unsupported command: {args.command}")
    except ModelManagerError as exc:
        print(f"model-manager: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
