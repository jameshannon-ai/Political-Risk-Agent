import unittest
from datetime import date

from agent.review_flags import generate_review_flags


class ReviewFlagsTests(unittest.TestCase):
    def test_detects_missing_source_types(self):
        sources = [
            {
                "inferred_source_type": "reputable_news",
                "date": "2026-05-20",
                "summary": "News report discusses shipping disruption.",
            }
        ]

        flags = generate_review_flags(sources)

        self.assertIn("Missing official_primary source.", flags)
        self.assertIn("Missing company_update source.", flags)
        self.assertIn("Fewer than three sources supplied.", flags)

    def test_detects_stale_sources(self):
        sources = [
            {
                "inferred_source_type": "official_primary",
                "date": "2026-01-01",
                "summary": "Old advisory.",
            },
            {
                "inferred_source_type": "company_update",
                "date": "2026-05-20",
                "summary": "Stabilising update says operations remain normal.",
            },
            {
                "inferred_source_type": "market_indicator",
                "date": "2026-05-21",
                "summary": "Freight premium indicator.",
            },
        ]

        flags = generate_review_flags(sources, today=date(2026, 5, 27))

        self.assertIn("One or more sources appear older than 90 days.", flags)

    def test_uk_ets_flags_do_not_include_hormuz_insurance_flags(self):
        evidence_pack = {
            "source_strategy": {"domain": "regulatory_carbon_shipping"},
            "evidence": [],
            "fetch_failures": [],
        }

        flags = generate_review_flags([], evidence_pack=evidence_pack, today=date(2026, 5, 28))

        self.assertIn("Live UKA price feed is not embedded; manual price input should be refreshed.", flags)
        self.assertNotIn("Missing insurance evidence in live evidence.", flags)
        self.assertNotIn("Missing energy chokepoint evidence in live evidence.", flags)
        self.assertNotIn("Missing company_update source.", flags)


if __name__ == "__main__":
    unittest.main()
