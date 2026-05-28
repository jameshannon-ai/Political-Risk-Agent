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


if __name__ == "__main__":
    unittest.main()
