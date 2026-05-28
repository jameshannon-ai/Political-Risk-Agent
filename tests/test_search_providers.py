import os
import unittest
from unittest.mock import Mock, patch

from agent.search_providers import FallbackDemoSearchProvider, TavilySearchProvider, get_search_provider


class SearchProviderTests(unittest.TestCase):
    def test_fallback_provider_works_without_api_keys(self):
        with patch.dict(os.environ, {}, clear=True):
            provider = get_search_provider()

        self.assertIsInstance(provider, FallbackDemoSearchProvider)
        results = provider.search("Strait of Hormuz", "official_primary")

        self.assertTrue(results)
        self.assertTrue(provider.uses_fallback)

    def test_tavily_provider_selected_when_key_exists(self):
        with patch.dict(os.environ, {"TAVILY_API_KEY": "placeholder-key"}, clear=True):
            provider = get_search_provider()

        self.assertIsInstance(provider, TavilySearchProvider)

    @patch("agent.search_providers.TavilySearchProvider.search")
    def test_mocked_tavily_provider_can_succeed(self, mock_search):
        mock_search.return_value = [{"title": "Gov", "url": "https://gov.uk", "snippet": "Test", "source_type": "official_primary"}]
        provider = TavilySearchProvider("placeholder-key")

        results = provider.search("query", "official_primary")

        self.assertEqual(len(results), 1)
        self.assertFalse(provider.uses_fallback)


if __name__ == "__main__":
    unittest.main()
