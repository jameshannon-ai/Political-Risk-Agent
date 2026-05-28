import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


def main():
    if load_dotenv:
        load_dotenv()

    api_key = os.getenv("TAVILY_API_KEY")
    print(f"TAVILY_API_KEY loaded: {'yes' if api_key else 'no'}")
    if not api_key:
        print("Tavily request succeeded: no")
        print("Number of results returned: 0")
        print("Top result title: ")
        print("Top result URL: ")
        return

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=api_key)
        response = client.search(query="UK sanctions end-use controls GOV.UK", max_results=1)
        results = response.get("results", [])
        top = results[0] if results else {}
        print("Tavily request succeeded: yes")
        print(f"Number of results returned: {len(results)}")
        print(f"Top result title: {top.get('title', '')}")
        print(f"Top result URL: {top.get('url', '')}")
    except Exception as exc:
        print("Tavily request succeeded: no")
        print("Number of results returned: 0")
        print("Top result title: ")
        print("Top result URL: ")
        print(f"Error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
