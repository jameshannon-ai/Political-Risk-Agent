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

        self.assertGreaterEqual(len(requirements), 9)
        names = {item["requirement_name"] for item in requirements}
        self.assertIn("uk_sanctions_ofsi_official_guidance", names)
        self.assertIn("sanctions_end_use_controls_and_controlled_goods_risk", names)
        self.assertIn("counterparty_and_ownership_exposure", names)
        self.assertIn("jurisdiction_route_and_diversion_exposure", names)
        self.assertIn("documentation_and_transaction_quality_evidence", names)
        self.assertIn("sanctions_company_data_requirements_and_anti_overclaiming_controls", names)
        for requirement in requirements:
            self.assertTrue(requirement["why_required"])
            self.assertTrue(requirement["decision_questions_supported"])

    def test_critical_minerals_advanced_manufacturer_requirements_exist(self):
        requirements = generate_source_requirements(
            topic="Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers",
            business_user="advanced_manufacturer",
            region="UK advanced manufacturer exposed to global rare earth magnet supply chains",
            time_horizon="1-6 months",
            concerns=["production continuity"],
            domain_pack={"domain": "critical_minerals_supply_chain"},
        )

        names = {item["requirement_name"] for item in requirements}
        self.assertIn("uk_critical_minerals_policy_and_manufacturing_resilience", names)
        self.assertIn("supply_concentration_and_dependency_data", names)
        self.assertIn("company_data_requirements_and_anti_overclaiming_controls", names)
        self.assertGreaterEqual(len(requirements), 9)


if __name__ == "__main__":
    unittest.main()
