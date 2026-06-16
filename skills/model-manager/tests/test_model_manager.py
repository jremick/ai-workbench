from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PACKAGE_DIR / "scripts" / "model_manager.py"
CATALOG_PATH = PACKAGE_DIR / "data" / "model_catalog.json"
EVAL_PATH = PACKAGE_DIR / "data" / "eval_cases.json"
MODEL_SYSTEM_PATH = PACKAGE_DIR / "data" / "model_system.json"

spec = importlib.util.spec_from_file_location("model_manager", SCRIPT_PATH)
assert spec and spec.loader
model_manager = importlib.util.module_from_spec(spec)
sys.modules["model_manager"] = model_manager
spec.loader.exec_module(model_manager)


class ModelManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = model_manager.load_json(CATALOG_PATH)
        self.model_system = model_manager.load_json(MODEL_SYSTEM_PATH)

    def context(self, task: str, **overrides):
        defaults = {
            "risk": "normal",
            "privacy": "standard",
            "needs_live_research": False,
            "long_horizon": False,
            "cost_policy": "balanced",
            "available_backends": {"codex", "claude_subscription", "perplexity", "lmstudio"},
            "max_routes": 3,
        }
        defaults.update(overrides)
        work_type = defaults.pop("work_type", None) or model_manager.infer_work_type(
            task,
            risk=defaults["risk"],
            privacy=defaults["privacy"],
            needs_live_research=defaults["needs_live_research"],
            long_horizon=defaults["long_horizon"],
        )
        return model_manager.TaskContext(task=task, work_type=work_type, **defaults)

    def test_trivial_task_stays_with_parent_codex(self) -> None:
        plan = model_manager.recommend(self.context("What is 2 + 2?"), self.catalog)
        self.assertFalse(plan["delegate"])
        self.assertEqual(plan["recommended_routes"][0]["model"], "parent/codex-default")

    def test_research_prefers_perplexity(self) -> None:
        plan = model_manager.recommend(
            self.context("Research the latest Artificial Analysis leaderboard changes."),
            self.catalog,
        )
        self.assertTrue(plan["delegate"])
        self.assertEqual(plan["work_type"], "research")
        self.assertEqual(plan["recommended_routes"][0]["backend"], "perplexity")

    def test_local_only_filters_external_models(self) -> None:
        plan = model_manager.recommend(
            self.context("Analyze this private local document offline.", privacy="local_only"),
            self.catalog,
        )
        self.assertTrue(plan["delegate"])
        self.assertEqual(plan["work_type"], "local_private")
        self.assertEqual(plan["recommended_routes"][0]["backend"], "lmstudio")
        for route in plan["recommended_routes"]:
            self.assertEqual(route["backend"], "lmstudio")

    def test_long_horizon_uses_deepswe_weight(self) -> None:
        plan = model_manager.recommend(
            self.context("Implement a multi-file repository migration with tests."),
            self.catalog,
        )
        self.assertEqual(plan["work_type"], "long_horizon_coding")
        self.assertIn(plan["recommended_routes"][0]["model"], {"openai/gpt-5.4", "openai/gpt-5.5"})
        self.assertTrue(
            any("deepswe_bonus" in reason for reason in plan["recommended_routes"][0]["reasons"]),
            json.dumps(plan, indent=2),
        )

    def test_model_system_routes_complexity_roles(self) -> None:
        plan = model_manager.recommend(
            self.context("Implement a multi-file repository migration with tests."),
            self.catalog,
            model_system=self.model_system,
        )
        route = plan["model_system_route"]
        self.assertEqual(route["complexity"], "high")
        self.assertEqual(route["review_tier"], "production")
        self.assertEqual(route["coder"]["role"], "coder_high")
        self.assertEqual(route["coder"]["model"], "openai/gpt-5.5")

    def test_model_system_flags_security_review(self) -> None:
        plan = model_manager.recommend(
            self.context("Implement OAuth login and API token storage for production."),
            self.catalog,
            model_system=self.model_system,
        )
        route = plan["model_system_route"]
        self.assertTrue(route["security_review"])
        self.assertEqual(route["security_reviewer"]["model"], "claude/opus")

    def test_model_system_blocks_external_route_for_local_only(self) -> None:
        stack = {
            "model_system": {
                "enabled": True,
                "coders": {
                    "medium": "openai/gpt-5.4"
                }
            }
        }
        plan = model_manager.recommend(
            self.context("Analyze this private local document offline.", privacy="local_only"),
            self.catalog,
            model_system=stack,
        )
        coder = plan["model_system_route"]["coder"]
        self.assertFalse(coder["available"])
        self.assertEqual(coder["blocked_reason"], "privacy constraint blocks external model")

    def test_high_risk_does_not_select_mini(self) -> None:
        plan = model_manager.recommend(
            self.context(
                "Stress test this irreversible production migration plan.",
                risk="high",
            ),
            self.catalog,
        )
        self.assertEqual(plan["work_type"], "high_risk_analysis")
        self.assertNotEqual(plan["recommended_routes"][0]["model"], "openai/gpt-5.4-mini")

    def test_eval_cases_pass(self) -> None:
        cases = model_manager.load_json(EVAL_PATH)
        result = model_manager.run_eval(cases, self.catalog, self.model_system)
        self.assertTrue(result["ok"], json.dumps(result, indent=2))

    def test_artificial_analysis_cache_can_influence_scoring(self) -> None:
        catalog = json.loads(json.dumps(self.catalog))
        matched = model_manager.apply_artificial_analysis_cache(
            catalog,
            {
                "status": 200,
                "data": [
                    {
                        "id": "aa-test-sonar",
                        "name": "Sonar",
                        "slug": "sonar",
                        "evaluations": {
                            "artificial_analysis_intelligence_index": 80,
                            "artificial_analysis_coding_index": 40,
                        },
                        "pricing": {
                            "price_1m_blended_3_to_1": 1.5
                        },
                        "median_output_tokens_per_second": 100,
                        "median_time_to_first_token_seconds": 1.2,
                    }
                ],
            },
        )
        self.assertEqual(matched["matched_models"], 1)
        self.assertEqual(matched["proxy_models"], 0)
        plan = model_manager.recommend(
            self.context("Research current benchmark changes."),
            catalog,
            {
                "artificial_analysis_cache": {
                    "used": True,
                    "matched_models": matched["matched_models"],
                    "proxy_models": matched["proxy_models"],
                }
            },
        )
        self.assertIn("artificial_analysis_intelligence", plan["recommended_routes"][0]["reasons"])
        self.assertTrue(plan["source_versions"]["source_status"]["artificial_analysis_cache"]["used"])

    def test_recommendation_values_snapshot_is_sanitized(self) -> None:
        catalog = json.loads(json.dumps(self.catalog))
        matched = model_manager.apply_artificial_analysis_cache(
            catalog,
            {
                "status": 200,
                "data": [
                    {
                        "id": "aa-test-gpt",
                        "name": "GPT-5.5 (xhigh)",
                        "slug": "gpt-5-5",
                        "evaluations": {
                            "artificial_analysis_intelligence_index": 90,
                            "artificial_analysis_coding_index": 85,
                        },
                        "pricing": {
                            "price_1m_blended_3_to_1": 12.0
                        },
                        "median_output_tokens_per_second": 80,
                        "median_time_to_first_token_seconds": 12,
                    }
                ],
            },
        )
        values = model_manager.build_recommendation_values(
            catalog,
            {
                "artificial_analysis_cache": {
                    "path": str(PACKAGE_DIR / "data" / "artificial_analysis_models.cache.json"),
                    "used": True,
                    "matched_models": matched["matched_models"],
                    "proxy_models": matched["proxy_models"],
                    "attribution_required": True,
                }
            },
            {
                "cases": [
                    {
                        "name": "trivial",
                        "task": "What is 2 + 2?",
                        "expect": {},
                    }
                ]
            },
        )
        rendered = json.dumps(values)
        self.assertIn("recommendation_profiles", values)
        self.assertIn("model_values", values)
        self.assertNotIn("api_key", rendered.lower())
        self.assertNotIn("artificial_analysis_api_key", rendered.lower())
        self.assertEqual(values["recommendation_profiles"][0]["top_model"], "parent/codex-default")

    def test_artificial_analysis_previous_model_proxy_is_labelled(self) -> None:
        catalog = json.loads(json.dumps(self.catalog))
        opus = next(model for model in catalog["models"] if model["id"] == "claude/opus")
        opus["artificial_analysis"]["previous_proxy"] = "claude-opus-4-7"
        matched = model_manager.apply_artificial_analysis_cache(
            catalog,
            {
                "status": 200,
                "data": [
                    {
                        "id": "aa-test-opus-47",
                        "name": "Claude Opus 4.7",
                        "slug": "claude-opus-4-7",
                        "evaluations": {
                            "artificial_analysis_intelligence_index": 57.3,
                            "artificial_analysis_coding_index": 52.5,
                        },
                        "pricing": {
                            "price_1m_blended_3_to_1": 10.938
                        },
                    }
                ],
            },
        )
        self.assertEqual(matched["matched_models"], 0)
        self.assertEqual(matched["proxy_models"], 1)
        self.assertEqual(opus["artificial_analysis_live"]["match_requested"], "claude-opus-4-8")
        self.assertEqual(opus["artificial_analysis_live"]["proxy_status"], "previous_model_proxy")


if __name__ == "__main__":
    unittest.main()
