from agent.search_providers import get_search_provider


def run_live_searches(source_strategy, provider=None, max_results_per_query=3):
    provider = provider or get_search_provider()
    candidate_sources = []
    failures = []
    total_queries_run = 0

    candidates_by_query = {}
    for category_plan in source_strategy["categories"]:
        category = category_plan["category"]
        requirement_id = category_plan.get("requirement_id", "")
        requirement_name = category_plan.get("requirement_name", "")
        for query in category_plan["queries"]:
            total_queries_run += 1
            try:
                results = provider.search(query, category, max_results=max_results_per_query)
                query_results = []
                for result in results:
                    result["query"] = query
                    result["query_used"] = query
                    result["source_requirement"] = requirement_name
                    result["requirement_id"] = result.get("requirement_id") or requirement_id
                    result["requirement_name"] = result.get("requirement_name") or requirement_name
                    result["decision_question_supported"] = category_plan.get("evidence_question", "")
                    candidate_sources.append(result)
                    query_results.append(result)
                candidates_by_query[query] = query_results
            except Exception as exc:
                failures.append({"query": query, "category": category, "requirement_id": requirement_id, "requirement_name": requirement_name, "error": str(exc)})

    return {
        "provider": provider.name,
        "fallback_demo_data_used": provider.uses_fallback,
        "evidence_mode": "Live source retrieval" if not provider.uses_fallback else "Reproducible curated source pack",
        "provider_error": "; ".join(item["error"] for item in failures) if failures else "",
        "total_queries_run": total_queries_run,
        "candidate_sources": candidate_sources,
        "candidates_by_query": candidates_by_query,
        "search_failures": failures,
    }
