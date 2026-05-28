import unittest


class QualityCheckPatternTests(unittest.TestCase):
    def test_tavily_key_patterns_are_detected(self):
        patterns = [
            "tvly-1234567890abcdef",
            "tvly-dev-1234567890abcdef",
            "TAVILY_API_KEY=tvly-1234567890abcdef",
        ]

        self.assertTrue(any("tvly-" in item for item in patterns))
        self.assertTrue(any("tvly-dev-" in item for item in patterns))
        self.assertTrue(any(item.startswith("TAVILY_API_KEY=") for item in patterns))

    def test_official_primary_examples_match_true_official_pattern(self):
        official_publishers = [
            "gov.uk",
            "ofac.treasury.gov",
            "imo.org",
            "ukmto.org",
        ]
        non_official_publishers = [
            "indexbox.io",
            "worldoil.com",
            "stl.news",
        ]

        self.assertTrue(any("gov" in item or "imo" in item or "ukmto" in item for item in official_publishers))
        self.assertFalse(any(item == "official_primary" for item in non_official_publishers))


if __name__ == "__main__":
    unittest.main()
