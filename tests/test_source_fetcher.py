import unittest

from agent.source_fetcher import fetch_selected_sources


class SourceFetcherTests(unittest.TestCase):
    def test_pdf_url_fallback_mode_is_handled_gracefully(self):
        source = {
            "title": "PDF source",
            "url": "https://example.com/report.pdf",
            "snippet": "PDF snippet",
            "source_type": "insurance_market_evidence",
        }

        result = fetch_selected_sources([source], fallback_demo_data_used=True)

        self.assertEqual(result["fetched_sources"][0]["fetch_status"], "demo")
        self.assertEqual(result["fetch_failures"], [])


if __name__ == "__main__":
    unittest.main()
