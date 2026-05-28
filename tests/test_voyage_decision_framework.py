import unittest

from agent.route_cost_assessment import assess_route_cost
from agent.voyage_decision_framework import build_voyage_decision_framework


class VoyageDecisionFrameworkTests(unittest.TestCase):
    def test_route_cost_assessment_prefers_legal_hold_when_sanctions_flagged(self):
        result = assess_route_cost(
            route_name="Test route",
            direct_transit_allowed="uncertain",
            estimated_direct_voyage_days=14,
            estimated_reroute_days=24,
            daily_vessel_cost=45000,
            bunker_cost_per_day=28000,
            war_risk_premium_direct=750000,
            war_risk_premium_reroute=150000,
            demurrage_or_delay_cost_per_day=35000,
            sanctions_risk_flag=True,
            compliance_hold_days=5,
        )

        self.assertEqual(result["preferred_option"], "Escalate / legal hold")
        self.assertIn("Illustrative voyage assumptions", result["caveat"])

    def test_voyage_framework_sets_escalation_when_sanctions_evidence_present(self):
        evidence_pack = {
            "evidence": [
                {"source_id": "S1", "requirement_name": "sanctions_and_safe_passage_payment_risk"},
                {"source_id": "S2", "requirement_name": "official_maritime_security"},
            ]
        }
        route_cost = {"preferred_option": "Escalate / legal hold"}
        result = build_voyage_decision_framework(evidence_pack, route_cost)

        self.assertTrue(result["compliance_escalation_required"])
        self.assertEqual(result["insurance_cost_pressure"], "Moderate")
        self.assertIn("safe-passage payment demand", " ".join(result["sanctions_red_flags"]))


if __name__ == "__main__":
    unittest.main()
