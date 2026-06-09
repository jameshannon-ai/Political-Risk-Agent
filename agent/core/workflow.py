from pathlib import Path

from agent.brief_generator import generate_brief, save_brief
from agent.evidence_pack_builder import build_evidence_pack, save_evidence_pack
from agent.live_search import run_live_searches
from agent.source_audit import generate_source_audit, save_source_audit
from agent.source_fetcher import fetch_selected_sources
from agent.source_parser import parse_source_notes
from agent.source_ranker import rank_candidate_sources
from agent.source_strategy import SOURCE_CATEGORIES, create_source_strategy


def run_topic_workflow(
    topic,
    business_user,
    decision_context="",
    region="",
    time_horizon="",
    concerns=None,
    domain=None,
    output_dir="outputs",
    source_notes="",
    live=False,
):
    concerns = concerns or []
    output_dir = Path(output_dir)
    strategy = create_source_strategy(
        topic,
        region,
        time_horizon,
        business_user=business_user,
        concerns=concerns + ([decision_context] if decision_context else []),
        domain=domain,
    )

    if live:
        search_result = run_live_searches(strategy)
        ranking = rank_candidate_sources(
            search_result["candidate_sources"],
            topic=topic,
            categories=SOURCE_CATEGORIES,
            per_category=1,
        )
        selected_sources = ranking["selected_sources"]
        rejected_sources = ranking["rejected_sources"]
        fetched_result = fetch_selected_sources(
            selected_sources,
            fallback_demo_data_used=search_result["fallback_demo_data_used"],
        )
    else:
        selected_sources = _manual_sources(source_notes)
        rejected_sources = []
        search_result = _manual_search_result(selected_sources)
        ranking = {"duplicate_urls_removed": 0}
        fetched_result = {
            "fetched_sources": [
                {
                    **source,
                    "content": source.get("summary") or source.get("snippet", ""),
                    "fetch_status": "manual",
                    "manual_input": True,
                    "evidence_source_mode": "manual_input",
                }
                for source in selected_sources
            ],
            "fetch_failures": [],
        }

    evidence_pack = build_evidence_pack(
        topic=topic,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        source_strategy=strategy,
        search_result=search_result,
        selected_sources=selected_sources,
        rejected_sources=rejected_sources,
        fetched_result=fetched_result,
    )
    evidence_pack["decision_context"] = decision_context
    evidence_pack["duplicate_urls_removed"] = ranking.get("duplicate_urls_removed", 0)

    evidence_pack_path = save_evidence_pack(evidence_pack, output_dir)
    source_audit = generate_source_audit(evidence_pack)
    source_audit_path = save_source_audit(source_audit, output_dir, topic)
    brief = generate_brief(
        topic=topic,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        sources=evidence_pack["evidence"],
        evidence_pack=evidence_pack,
    )
    brief_path = save_brief(brief, output_dir)

    return {
        "evidence_pack": evidence_pack,
        "evidence_pack_path": evidence_pack_path,
        "source_audit_path": source_audit_path,
        "brief_path": brief_path,
    }


def _manual_sources(source_notes):
    if source_notes.strip():
        parsed = parse_source_notes(source_notes)
    else:
        parsed = [
            {
                "source_id": "M1",
                "title": "Manual context placeholder",
                "publisher": "Analyst input",
                "summary": "No source notes were supplied. Treat this run as a structure-only workflow requiring live source refresh before operational use.",
                "inferred_source_type": "unknown",
            }
        ]
    sources = []
    for index, source in enumerate(parsed, start=1):
        source_type = source.get("source_type") or source.get("inferred_source_type") or "unknown"
        sources.append(
            {
                "source_id": source.get("source_id") or f"M{index}",
                "title": source.get("title") or f"Manual source {index}",
                "publisher": source.get("publisher", "Analyst input"),
                "url": source.get("url", ""),
                "publication_date": source.get("publication_date") or source.get("date", ""),
                "source_type": source_type,
                "source_role": source.get("source_role") or "company_required_data" if source_type == "unknown" else source.get("source_role", ""),
                "snippet": source.get("summary", ""),
                "summary": source.get("summary", ""),
                "evidence_weight": source.get("evidence_weight", "low" if source_type == "unknown" else "medium"),
                "selection_reason": "Manual input supplied for fresh-topic workflow.",
                "decision_use": "Supports initial structuring only; requires source verification before operational use.",
                "source_value_explanation": "Manual or analyst-provided context.",
                "manual_input": True,
                "source_mode": "manual_input",
            }
        )
    return sources


def _manual_search_result(selected_sources):
    return {
        "provider": "manual_input",
        "fallback_demo_data_used": False,
        "evidence_mode": "Manual source input",
        "provider_error": "",
        "total_queries_run": 0,
        "candidate_sources": selected_sources,
        "candidates_by_query": {"manual_input": selected_sources},
        "search_failures": [],
    }

