import unittest

from agent.review_flags import generate_review_flags


class LiveReviewFlagsTests(unittest.TestCase):
    def test_detects_missing_live_evidence_categories(self):
        evidence = [
            {
                "source_type": "reputable_news",
                "inferred_source_type": "reputable_news",
                "publication_date": "2026-05-27",
                "summary": "News report about Strait of Hormuz disruption.",
            }
        ]
        pack = {
            "evidence": evidence,
            "fetch_failures": [],
            "fallback_demo_data_used": False,
        }

        flags = generate_review_flags(evidence, evidence_pack=pack)

        self.assertIn("Missing official source in live evidence.", flags)
        self.assertIn("Missing company update in live evidence.", flags)
        self.assertIn("Missing insurance evidence in live evidence.", flags)
        self.assertIn("Missing energy chokepoint evidence in live evidence.", flags)
        self.assertIn("Missing contrary evidence in live evidence.", flags)


if __name__ == "__main__":
    unittest.main()
