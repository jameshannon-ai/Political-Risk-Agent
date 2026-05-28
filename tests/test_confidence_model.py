import unittest

from agent.confidence_model import calculate_confidence


class ConfidenceModelTests(unittest.TestCase):
    def test_confidence_increases_with_source_diversity(self):
        narrow_sources = [
            {"inferred_source_type": "unknown", "summary": "Unclear disruption note."},
        ]
        diverse_sources = [
            {"inferred_source_type": "official_primary", "summary": "Advisory reports vessel incident."},
            {"inferred_source_type": "company_update", "summary": "Carrier avoids route."},
            {"inferred_source_type": "market_indicator", "summary": "Freight and premium indicators are elevated."},
            {"inferred_source_type": "specialist_analysis", "summary": "Stabilising evidence says some port operations remain normal."},
        ]

        self.assertGreater(
            calculate_confidence(diverse_sources)["confidence_score"],
            calculate_confidence(narrow_sources)["confidence_score"],
        )


if __name__ == "__main__":
    unittest.main()
