import unittest

from agent.risk_driver_synthesis import synthesize_risk_drivers


class RiskDriverSynthesisTests(unittest.TestCase):
    def test_groups_evidence_into_drivers(self):
        drivers = synthesize_risk_drivers(
            [
                {
                    "source_id": "H1",
                    "risk_driver": "Insurance-market repricing",
                    "requirement_name": "insurance_pricing_reinsurance",
                    "evidence_weight": "high",
                    "decision_value_score": 5,
                    "extracted_claim": "War-risk premiums increased.",
                    "commercial_meaning": "Pricing and reinsurance markets repriced route risk.",
                    "business_user_implication": "Premium adequacy and reinsurance appetite.",
                    "decision_use": "Supports pricing review.",
                    "caveat": "Refresh broker quotes.",
                    "refresh_requirement": "Refresh before binding.",
                }
            ]
        )

        self.assertEqual(drivers[0]["driver_name"], "Insurance-market repricing")
        self.assertEqual(drivers[0]["highest_weight_sources"], ["H1"])
        self.assertIn("refresh_trigger", drivers[0])


if __name__ == "__main__":
    unittest.main()
