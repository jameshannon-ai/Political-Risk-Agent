import unittest

from agent.source_ranker import rank_candidate_sources


class SourceRankerTests(unittest.TestCase):
    def test_prioritises_trusted_domains(self):
        candidates = [
            {
                "title": "Forum comment about shipping",
                "url": "https://example.com/hormuz",
                "snippet": "Strait of Hormuz shipping risk",
                "source_type": "reputable_news",
            },
            {
                "title": "Reuters Strait of Hormuz shipping risk",
                "url": "https://www.reuters.com/world/hormuz-shipping-risk",
                "snippet": "Strait of Hormuz tanker disruption and insurance concern",
                "source_type": "reputable_news",
            },
        ]

        ranked = rank_candidate_sources(candidates, topic="Strait of Hormuz disruption")

        self.assertEqual(ranked["selected_sources"][0]["url"], "https://www.reuters.com/world/hormuz-shipping-risk")
        self.assertIn("selection_reason", ranked["selected_sources"][0])
        for key in [
            "reliability_score",
            "relevance_score",
            "recency_score",
            "specificity_score",
            "decision_value_score",
            "independence_score",
            "total_score",
            "evidence_weight",
            "decision_use",
        ]:
            self.assertIn(key, ranked["selected_sources"][0])
        self.assertIn(ranked["selected_sources"][0]["evidence_weight"], {"high", "medium", "low"})

    def test_rejected_sources_include_rejection_reason(self):
        candidates = [
            {
                "title": "Reuters Strait of Hormuz shipping risk",
                "url": "https://www.reuters.com/world/hormuz-shipping-risk",
                "snippet": "Strait of Hormuz tanker disruption",
                "source_type": "reputable_news",
            },
            {
                "title": "Blog Strait of Hormuz shipping risk",
                "url": "https://unknown.example/hormuz",
                "snippet": "Strait of Hormuz tanker disruption",
                "source_type": "reputable_news",
            },
        ]

        ranked = rank_candidate_sources(
            candidates,
            topic="Strait of Hormuz disruption",
            categories=["reputable_news"],
        )

        self.assertTrue(ranked["rejected_sources"])
        self.assertIn("rejection_reason", ranked["rejected_sources"][0])
        self.assertIn("lowest_scoring_dimension", ranked["rejected_sources"][0])
        self.assertIn("total_score", ranked["rejected_sources"][0])


if __name__ == "__main__":
    unittest.main()
