import unittest

from agent.live_search import run_live_searches


class StubProvider:
    name = "tavily"
    uses_fallback = False

    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def search(self, query, category, max_results=5):
        if self.should_fail:
            raise RuntimeError("provider failed")
        return [
            {
                "title": "Result",
                "url": "https://example.com",
                "snippet": "Snippet",
                "source_type": category,
            }
        ]


class LiveSearchTests(unittest.TestCase):
    def test_provider_status_and_query_fields_are_recorded(self):
        source_strategy = {
            "categories": [
                {
                    "category": "official_primary",
                    "requirement_id": "REQ-1",
                    "requirement_name": "official_policy_scope",
                    "evidence_question": "Question?",
                    "queries": ["query one"],
                }
            ]
        }

        result = run_live_searches(source_strategy, provider=StubProvider())

        self.assertEqual(result["provider"], "tavily")
        self.assertFalse(result["fallback_demo_data_used"])
        self.assertEqual(result["evidence_mode"], "Live source retrieval")
        self.assertEqual(result["total_queries_run"], 1)
        self.assertEqual(result["candidate_sources"][0]["query_used"], "query one")
        self.assertEqual(result["candidate_sources"][0]["requirement_id"], "REQ-1")

    def test_provider_errors_are_captured(self):
        source_strategy = {
            "categories": [
                {
                    "category": "official_primary",
                    "requirement_id": "REQ-1",
                    "requirement_name": "official_policy_scope",
                    "evidence_question": "Question?",
                    "queries": ["query one"],
                }
            ]
        }

        result = run_live_searches(source_strategy, provider=StubProvider(should_fail=True))

        self.assertIn("provider failed", result["provider_error"])
        self.assertEqual(len(result["search_failures"]), 1)


if __name__ == "__main__":
    unittest.main()
