import unittest
from pathlib import Path

from agent.source_requirements import generate_source_requirements


class SourceRequirementsTests(unittest.TestCase):
    def test_source_requirements_module_exists(self):
        self.assertTrue(Path("agent/source_requirements.py").exists())

    def test_hormuz_shipping_operator_has_expected_requirements(self):
        requirements = generate_source_requirements(
            topic="Strait of Hormuz Transit Controls",
            business_user="shipping_operator",
            region="Persian Gulf / UK shipping operators",
            time_horizon="1-3 months",
            concerns=["transit controls"],
        )

        self.assertGreaterEqual(len(requirements), 8)
        names = {item["requirement_name"] for item in requirements}
        self.assertIn("transit_control_or_constabulary_actions", names)
        self.assertIn("sanctions_and_safe_passage_payment_risk", names)
        self.assertIn("route_cost_and_arbitrage_inputs", names)
        for requirement in requirements:
            self.assertIn("why_required", requirement)
            self.assertTrue(requirement["why_required"])
            self.assertIn("decision_questions_supported", requirement)
            self.assertTrue(requirement["decision_questions_supported"])

    def test_sanctions_trade_finance_requirements_are_decision_led(self):
        requirements = generate_source_requirements(
            topic="Sanctions End-Use Controls affecting trade finance",
            business_user="trade_finance_lender",
            region="UK / EU",
            time_horizon="1-3 months",
            concerns=["sanctions exposure"],
        )

        self.assertGreaterEqual(len(requirements), 7)
        names = {item["requirement_name"] for item in requirements}
        self.assertIn("official_sanctions_guidance", names)
        self.assertIn("banking_and_payment_risk", names)
        for requirement in requirements:
            self.assertTrue(requirement["why_required"])
            self.assertTrue(requirement["decision_questions_supported"])


if __name__ == "__main__":
    unittest.main()
