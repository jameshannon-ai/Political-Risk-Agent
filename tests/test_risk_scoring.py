import unittest

from agent.risk_scoring import score_risk


class RiskScoringTests(unittest.TestCase):
    def test_scores_are_between_one_and_five(self):
        scores = score_risk(
            topic="Strait of Hormuz disruption",
            concerns=["war-risk premiums", "energy tanker disruption", "claims aggregation"],
            region="Persian Gulf / UK marine insurance market",
            time_horizon="1-3 months",
        )

        for dimension in ["likelihood", "impact", "immediacy", "confidence"]:
            self.assertGreaterEqual(scores[dimension]["score"], 1)
            self.assertLessEqual(scores[dimension]["score"], 5)

    def test_high_risk_topic_increases_likelihood(self):
        baseline = score_risk(topic="General market uncertainty")
        elevated = score_risk(topic="Sanctions and port closure risk")

        self.assertGreater(
            elevated["likelihood"]["score"],
            baseline["likelihood"]["score"],
        )


if __name__ == "__main__":
    unittest.main()
