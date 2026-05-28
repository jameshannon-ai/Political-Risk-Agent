import unittest

from agent.evidence_pack_builder import build_evidence_pack
from agent.source_strategy import create_source_strategy


class EvidencePackBuilderTests(unittest.TestCase):
    def test_builds_expected_schema(self):
        strategy = create_source_strategy(
            "Strait of Hormuz disruption",
            "Persian Gulf",
            "1-3 months",
            business_user="marine_insurer",
        )
        selected_sources = [
            {
                "title": "Placeholder source",
                "publisher": "Reuters",
                "url": "https://www.reuters.com/example",
                "publication_date": "2026-05-27",
                "source_type": "reputable_news",
                "snippet": "Placeholder report on Strait of Hormuz disruption.",
            }
        ]
        search_result = {
            "provider": "fallback_demo_search",
            "fallback_demo_data_used": True,
            "evidence_mode": "Reproducible curated source pack",
            "provider_error": "",
            "total_queries_run": 1,
            "candidate_sources": selected_sources,
            "candidates_by_query": {"query": selected_sources},
            "search_failures": [],
        }
        fetched_result = {"fetched_sources": selected_sources, "fetch_failures": []}

        pack = build_evidence_pack(
            topic="Strait of Hormuz disruption",
            business_user="marine_insurer",
            region="Persian Gulf",
            time_horizon="1-3 months",
            concerns=["war-risk premiums"],
            source_strategy=strategy,
            search_result=search_result,
            selected_sources=selected_sources,
            rejected_sources=[{"title": "Rejected", "rejection_reason": "weak relevance"}],
            fetched_result=fetched_result,
        )

        for key in ["topic", "source_strategy", "selected_sources", "evidence", "fallback_demo_data_used"]:
            self.assertIn(key, pack)
        self.assertEqual(pack["evidence"][0]["source_id"], "L1")
        self.assertEqual(pack["selected_count"], 1)
        self.assertEqual(pack["rejected_count"], 1)
        self.assertIn("reputable_news", pack["source_categories_covered"])
        self.assertIn("official_primary", pack["source_categories_missing"])
        self.assertIn("requirement_coverage", pack)
        self.assertIn("requirements_missing", pack)
        self.assertIn("requirements_below_threshold", pack)
        self.assertIn("weighted_sources", pack)
        self.assertIn("source_plan", pack)
        self.assertIn("search_queries_by_requirement", pack)
        self.assertIn("candidates_by_query", pack)
        self.assertIn("selected_sources_by_requirement", pack)
        self.assertIn("rejected_sources_by_requirement", pack)
        self.assertIn("evidence_by_risk_driver", pack)
        self.assertIn("refresh_priorities", pack)
        self.assertTrue(pack["risk_drivers"])
        self.assertIn("highest_weight_sources", pack["risk_drivers"][0])
        self.assertIn("refresh_trigger", pack["risk_drivers"][0])
        self.assertEqual(pack["source_provider"], "fallback_demo_search")
        self.assertTrue(pack["fallback_used"])
        self.assertEqual(pack["evidence_mode"], "Reproducible curated source pack")


if __name__ == "__main__":
    unittest.main()
