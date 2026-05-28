import json
import os
from pathlib import Path


def get_search_provider():
    if os.getenv("TAVILY_API_KEY"):
        return TavilySearchProvider(os.getenv("TAVILY_API_KEY"))
    if os.getenv("SERPAPI_API_KEY"):
        return SerpApiSearchProvider(os.getenv("SERPAPI_API_KEY"))
    return FallbackDemoSearchProvider()


class TavilySearchProvider:
    name = "tavily"
    uses_fallback = False

    def __init__(self, api_key):
        self.api_key = api_key
        self.last_error = None

    def search(self, query, category, max_results=5):
        try:
            from tavily import TavilyClient
        except ImportError as exc:
            self.last_error = exc
            raise

        try:
            client = TavilyClient(api_key=self.api_key)
            data = client.search(query=query, max_results=max_results)
        except Exception as exc:
            self.last_error = exc
            raise
        return [
            _result(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("content", ""),
                category=category,
            )
            for item in data.get("results", [])
        ]


class SerpApiSearchProvider:
    name = "serpapi"
    uses_fallback = False

    def __init__(self, api_key):
        self.api_key = api_key
        self.last_error = None

    def search(self, query, category, max_results=5):
        import requests

        response = requests.get(
            "https://serpapi.com/search.json",
            params={"api_key": self.api_key, "q": query, "num": max_results},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return [
            _result(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                category=category,
            )
            for item in data.get("organic_results", [])
        ]


class FallbackDemoSearchProvider:
    name = "fallback_demo_search"
    uses_fallback = True

    def __init__(self, demo_case_path=None):
        self.demo_case_path = demo_case_path
        self.last_error = None

    def search(self, query, category, max_results=5):
        case_path = self.demo_case_path or _demo_case_path_for(query)
        case = json.loads(Path(case_path).read_text(encoding="utf-8"))
        results = [
            source for source in case["demo_search_results"]
            if source["source_type"] == category
        ]
        return [
            _result(
                title=item["title"],
                url=item["url"],
                snippet=item.get("claim_supported") or item.get("snippet", ""),
                category=category,
                publication_date=item.get("publication_date", ""),
                publisher=item.get("publisher", ""),
                extra=item,
            )
            for item in results[:max_results]
        ]


def _result(title, url, snippet, category, publication_date="", publisher="", extra=None):
    result = {
        "title": title,
        "url": url,
        "snippet": snippet,
        "source_type": category,
        "publication_date": publication_date,
        "publisher": publisher,
    }
    if extra:
        result.update(extra)
    return result


def _demo_case_path_for(query):
    lowered = query.lower()
    if "uk ets" in lowered or "emissions trading" in lowered or "carbon price" in lowered:
        return Path("examples/uk_ets_real_evidence_case.json")
    if "sanctions" in query.lower() and "end-use" in query.lower():
        return Path("examples/sanctions_real_evidence_case.json")
    return Path("examples/hormuz_real_evidence_case.json")
