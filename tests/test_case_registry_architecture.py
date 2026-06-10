import json
import unittest
from pathlib import Path

from agent.cases.registry import CASE_REGISTRY, CaseConfig, match_case, normalize_business_user
from agent.exposure_mapping import VALID_BUSINESS_USERS
from agent.source_planner import infer_domain
from agent.source_ranker import TRUSTED_DOMAINS


class CaseRegistryArchitectureTests(unittest.TestCase):
    def test_registry_contains_active_cases(self):
        self.assertEqual(
            {"hormuz", "sanctions", "uk_ets", "critical_minerals", "cyber", "fiscal"},
            set(CASE_REGISTRY),
        )
        for config in CASE_REGISTRY.values():
            self.assertIsInstance(config, CaseConfig)
            self.assertTrue(config.case_id)
            self.assertTrue(config.display_name)
            self.assertTrue(config.domain)
            self.assertTrue(config.business_users)
            self.assertTrue(config.detect_keywords)
            self.assertTrue(callable(config.source_requirements_fn))
            self.assertTrue(callable(config.brief_generator_fn))
            self.assertTrue(config.scoring_profile)

    def test_business_user_aliases_normalise_to_canonical_ids(self):
        aliases = [
            "UK infrastructure contractor",
            "UK infrastructure contractor bidding for government-funded transport and energy projects",
            "uk_infrastructure_contractor",
        ]
        for alias in aliases:
            self.assertEqual(normalize_business_user(alias), "infrastructure_contractor")
        self.assertEqual(normalize_business_user("critical_services_operator"), "customer_facing_operator")
        self.assertEqual(normalize_business_user("uk_retailer"), "customer_facing_operator")

    def test_valid_business_users_match_config(self):
        config = json.loads(Path("config/business_users.json").read_text(encoding="utf-8"))
        configured_ids = tuple(item["id"] for item in config["business_users"])
        self.assertEqual(configured_ids, VALID_BUSINESS_USERS)

    def test_registry_drives_domain_inference(self):
        self.assertEqual(
            infer_domain("UK fiscal instability and public-sector procurement delay risk", "UK infrastructure contractor"),
            "uk_fiscal_procurement_risk",
        )
        self.assertEqual(
            match_case("Cyber Business Interruption Engine", "critical_services_operator").case_id,
            "cyber",
        )

    def test_brief_generator_is_thin_router(self):
        self.assertLess(Path("agent/brief_generator.py").read_text(encoding="utf-8").count("\n"), 150)
        for module in ["hormuz", "sanctions", "uk_ets", "critical_minerals", "cyber", "fiscal"]:
            text = Path(f"agent/briefs/{module}.py").read_text(encoding="utf-8")
            self.assertIn("def generate(evidence_pack)", text)

    def test_trusted_domains_are_configured_externally(self):
        config = json.loads(Path("config/trusted_domains.json").read_text(encoding="utf-8"))
        self.assertIn("gov.uk", config["trusted_domains"])
        self.assertEqual(config["trusted_domains"], TRUSTED_DOMAINS)


if __name__ == "__main__":
    unittest.main()

