import json
import unittest
from pathlib import Path

from agent.brief_generator import generate_brief, select_report_template


class ProjectPositioningTests(unittest.TestCase):
    def test_domain_packs_include_reusable_cases(self):
        path = Path("config/domain_packs.json")
        self.assertTrue(path.exists())

        packs = json.loads(path.read_text(encoding="utf-8"))

        self.assertGreaterEqual(len(packs), 5)
        for pack in packs.values():
            self.assertIn("default_source_categories", pack)
            self.assertIn("default_risk_drivers", pack)
            self.assertIn("likely_business_users", pack)
            self.assertIn("example_watchlist_indicators", pack)

    def test_generic_non_marine_insurer_path_has_no_marine_insurance_implications(self):
        brief = generate_brief(
            topic="Election risk",
            business_user="consultant",
            region="Emerging market",
            time_horizon="six months",
            concerns=["policy uncertainty"],
            sources=[],
        )

        self.assertNotIn("Marine Insurance Implications", brief)
        self.assertNotIn("Marine Insurer Exposure Assessment", brief)
        self.assertNotIn("Exposure Pressure Map", brief)

    def test_hormuz_shipping_operator_path_keeps_specialist_sections(self):
        brief = generate_brief(
            topic="Strait of Hormuz Transit Controls",
            business_user="shipping_operator",
            region="Persian Gulf / UK shipping operators",
            time_horizon="1-3 months",
            concerns=["transit controls"],
            sources=[],
        )

        self.assertIn("Decision Recommendation", brief)
        self.assertIn("Route Decision Optimiser", brief)
        self.assertIn("Sanctions Red-Flag Assessment", brief)
        self.assertEqual(
            select_report_template("Strait of Hormuz Transit Controls", "shipping_operator"),
            "hormuz_shipping_operator_showcase",
        )

    def test_critical_minerals_path_is_non_shipping_and_decision_led(self):
        brief = generate_brief(
            topic="Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers",
            business_user="advanced_manufacturer",
            region="UK advanced manufacturer exposed to global rare earth magnet supply chains",
            time_horizon="1-6 months",
            concerns=["production continuity"],
            sources=[],
        )

        self.assertIn("Controlled Input Assessment", brief)
        self.assertIn("Mitigation Options", brief)
        self.assertNotIn("Route Decision Optimiser", brief)
        self.assertEqual(
            select_report_template(
                "Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers",
                "advanced_manufacturer",
                "critical_minerals_supply_chain",
            ),
            "critical_minerals_advanced_manufacturer_showcase",
        )

    def test_readme_identifies_engine_domain_layer_and_showcase(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("Reusable political risk engine", readme)
        self.assertIn("Domain-specific layer", readme)
        self.assertIn("Showcase case", readme)
        self.assertIn("UK ETS Maritime Expansion", readme)


if __name__ == "__main__":
    unittest.main()
