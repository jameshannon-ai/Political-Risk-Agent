import unittest
from pathlib import Path

from agent.source_planner import create_source_plan


class SourcePlannerTests(unittest.TestCase):
    def test_source_planner_module_exists(self):
        self.assertTrue(Path("agent/source_planner.py").exists())

    def test_planner_creates_different_domain_plans(self):
        maritime = create_source_plan(
            topic="Strait of Hormuz Transit Controls",
            domain="maritime_trade",
            business_user="shipping_operator",
            region="Persian Gulf",
            time_horizon="1-3 months",
            concerns=["transit controls"],
        )
        sanctions = create_source_plan(
            topic="Sanctions End-Use Controls affecting trade finance",
            domain="sanctions_trade_finance",
            business_user="trade_finance_lender",
            region="UK / EU",
            time_horizon="1-3 months",
            concerns=["sanctions exposure"],
        )

        self.assertNotEqual(maritime["required_source_mix"], sanctions["required_source_mix"])
        self.assertIn("official maritime/security advisory", maritime["required_source_mix"])
        self.assertIn("official sanctions guidance", sanctions["required_source_mix"])

    def test_sanctions_plan_includes_required_evidence(self):
        plan = create_source_plan(
            topic="Sanctions End-Use Controls affecting trade finance",
            domain="sanctions_trade_finance",
            business_user="trade_finance_lender",
            region="UK / EU",
            time_horizon="1-3 months",
            concerns=["sanctions exposure"],
        )
        mix = " ".join(plan["required_source_mix"])

        self.assertIn("official sanctions guidance", mix)
        self.assertIn("export-control", mix)
        self.assertIn("source_requirements", plan)
        self.assertIn("search_queries", plan)

    def test_maritime_plan_includes_official_and_insurance_evidence(self):
        plan = create_source_plan(
            topic="Strait of Hormuz Transit Controls",
            domain="maritime_trade",
            business_user="shipping_operator",
            region="Persian Gulf",
            time_horizon="1-3 months",
            concerns=["transit controls"],
        )
        mix = " ".join(plan["required_source_mix"])

        self.assertIn("official maritime/security", mix)
        self.assertIn("insurance and route-cost", mix)
        queries = " ".join(query for values in plan["search_queries"].values() for query in values)
        self.assertIn("OFAC FAQ 1249", queries)
        self.assertIn("Howden Re Strait of Hormuz war risk pricing", queries)


if __name__ == "__main__":
    unittest.main()
