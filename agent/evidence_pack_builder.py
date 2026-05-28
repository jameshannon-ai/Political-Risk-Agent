from datetime import datetime
from pathlib import Path
import json

from agent.live_evidence_extraction import extract_live_evidence
from agent.quantitative_assessment import build_evidence_to_score_bridge, build_quantified_evidence_readout
from agent.risk_driver_synthesis import synthesize_risk_drivers
from agent.risk_scoring import score_risk


def build_evidence_pack(
    topic,
    business_user,
    region,
    time_horizon,
    concerns,
    source_strategy,
    search_result,
    selected_sources,
    fetched_result,
    rejected_sources=None,
):
    rejected_sources = rejected_sources or []
    evidence = extract_live_evidence(fetched_result["fetched_sources"], business_user)
    evidence_index = _index_evidence(evidence)
    selected_sources = [_merge_source_identity(source, evidence_index) for source in selected_sources]
    rejected_sources = [_merge_source_identity(source, evidence_index) for source in rejected_sources]
    risk_drivers = synthesize_risk_drivers(evidence)
    source_categories = [item["category"] for item in source_strategy["categories"]]
    covered = sorted({source.get("source_type", "unknown") for source in selected_sources})
    missing = [category for category in source_categories if category not in covered]
    source_requirements = source_strategy.get("source_requirements", [])
    requirement_coverage = _requirement_coverage(source_requirements, evidence)
    retrieval_timestamp = datetime.now().isoformat(timespec="seconds")
    partial_pack = {
        "source_strategy": source_strategy,
        "selected_sources": selected_sources,
        "evidence": evidence,
        "requirement_coverage": requirement_coverage,
        "requirements_missing": [
            item["requirement_id"] for item in requirement_coverage
            if item["covered_by_count"] == 0
        ],
        "fallback_demo_data_used": search_result["fallback_demo_data_used"],
    }
    risk_scores = score_risk(topic=topic, concerns=concerns, region=region, time_horizon=time_horizon, sources=evidence)
    quantified_readout = build_quantified_evidence_readout(partial_pack)
    score_bridge = build_evidence_to_score_bridge(partial_pack, risk_scores)
    return {
        "topic": topic,
        "business_user": business_user,
        "region": region,
        "time_horizon": time_horizon,
        "concerns": concerns,
        "created_at": retrieval_timestamp,
        "retrieval_timestamp": retrieval_timestamp,
        "source_strategy": source_strategy,
        "source_plan": source_strategy.get("source_plan", {}),
        "source_requirements": source_requirements,
        "search_queries_by_requirement": _search_queries_by_requirement(source_strategy),
        "candidates_by_query": _candidate_ids_by_query(search_result.get("candidates_by_query", {})),
        "source_provider": search_result["provider"],
        "search_provider": search_result["provider"],
        "evidence_mode": search_result.get("evidence_mode", "Live source retrieval" if not search_result["fallback_demo_data_used"] else "Reproducible curated source pack"),
        "provider_error": search_result.get("provider_error", ""),
        "fallback_demo_data_used": search_result["fallback_demo_data_used"],
        "fallback_used": search_result["fallback_demo_data_used"],
        "total_queries_run": search_result.get("total_queries_run", 0),
        "candidate_count": len(search_result.get("candidate_sources", [])),
        "selected_count": len(selected_sources),
        "rejected_count": len(rejected_sources),
        "selected_sources": selected_sources,
        "rejected_sources": rejected_sources,
        "weighted_sources": selected_sources,
        "source_categories_covered": covered,
        "source_categories_missing": missing,
        "requirement_coverage": requirement_coverage,
        "evidence_by_requirement": _evidence_by_requirement(requirement_coverage),
        "selected_sources_by_requirement": _sources_by_requirement(selected_sources),
        "rejected_sources_by_requirement": _sources_by_requirement(rejected_sources),
        "evidence_by_risk_driver": _evidence_by_risk_driver(evidence),
        "risk_drivers": risk_drivers,
        "refresh_priorities": _refresh_priorities(risk_drivers),
        "quantified_evidence_readout": quantified_readout,
        "evidence_to_score_bridge": score_bridge,
        "quantified_facts_by_source": {
            item.get("source_id", ""): item.get("quantified_facts", [])
            for item in evidence
        },
        "confidence_cap_reason": quantified_readout["confidence_cap"],
        "requirements_missing": [
            item["requirement_id"] for item in requirement_coverage
            if item["covered_by_count"] == 0
        ],
        "requirements_below_threshold": [
            item["requirement_id"] for item in requirement_coverage
            if item["evidence_weight"] == "low"
        ],
        "coverage_summary": _coverage_summary(covered, missing),
        "search_failures": search_result["search_failures"],
        "fetch_failures": fetched_result["fetch_failures"],
        "evidence": evidence,
    }


def save_evidence_pack(evidence_pack, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = _slugify(evidence_pack["topic"])
    path = output_dir / f"{timestamp}-{slug}-evidence-pack.json"
    path.write_text(json.dumps(evidence_pack, indent=2), encoding="utf-8")
    return path


def _slugify(value):
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")


def _index_evidence(evidence):
    indexed = {}
    for item in evidence:
        if item.get("url"):
            indexed[("url", item["url"])] = item
        if item.get("title"):
            indexed[("title", item["title"])] = item
    return indexed


def _merge_source_identity(source, evidence_index):
    matched = evidence_index.get(("url", source.get("url", ""))) or evidence_index.get(("title", source.get("title", "")))
    if not matched:
        return source
    merged = dict(source)
    if not merged.get("source_id"):
        merged["source_id"] = matched.get("source_id", "")
    if not merged.get("title"):
        merged["title"] = matched.get("title", source.get("title", ""))
    return merged


def _coverage_summary(covered, missing):
    if not missing:
        return "All required evidence categories are represented."
    return f"Covered {len(covered)} categories; missing: {', '.join(missing)}."


def _requirement_coverage(requirements, evidence):
    coverage = []
    for requirement in requirements:
        matching = [
            item for item in evidence
            if item.get("source_type") in _normalised_source_types(requirement["preferred_source_types"])
            or _requirement_name_matches(requirement["requirement_name"], item)
        ]
        coverage.append(
            {
                "requirement_id": requirement["requirement_id"],
                "requirement_name": requirement["requirement_name"],
                "why_required": requirement["why_required"],
                "covered_by": [item["source_id"] for item in matching],
                "covered_by_count": len(matching),
                "evidence_weight": _evidence_weight(len(matching), requirement),
                "decision_questions_supported": requirement["decision_questions_supported"],
                "remaining_gap": _remaining_gap(len(matching), requirement),
            }
        )
    return coverage


def _evidence_by_requirement(requirement_coverage):
    return {
        item["requirement_id"]: item["covered_by"]
        for item in requirement_coverage
    }


def _search_queries_by_requirement(source_strategy):
    return {
        item["requirement_id"]: item.get("queries", [])
        for item in source_strategy.get("categories", [])
    }


def _candidate_ids_by_query(candidates_by_query):
    return {
        query: [item.get("source_id") or item.get("url", "") for item in results]
        for query, results in candidates_by_query.items()
    }


def _sources_by_requirement(sources):
    grouped = {}
    for source in sources:
        key = source.get("requirement_id") or "unmapped"
        grouped.setdefault(key, []).append(source.get("source_id") or source.get("url", ""))
    return grouped


def _evidence_by_risk_driver(evidence):
    grouped = {}
    for item in evidence:
        grouped.setdefault(item.get("risk_driver", "General commercial risk"), []).append(item.get("source_id", ""))
    return grouped


def _refresh_priorities(risk_drivers):
    return [
        {
            "risk_driver": item["driver_name"],
            "refresh_trigger": item["refresh_trigger"],
            "highest_weight_sources": item["highest_weight_sources"],
        }
        for item in risk_drivers
    ]


def _normalised_source_types(source_types):
    return ["official_primary" if item == "official_guidance" else item for item in source_types]


def _requirement_name_matches(requirement_name, evidence):
    text = " ".join(
        [
            evidence.get("title", ""),
            evidence.get("claim_supported", ""),
            evidence.get("commercial_relevance", ""),
            evidence.get("marine_insurance_implication", ""),
        ]
    ).lower()
    if requirement_name == "sanctions_compliance":
        return "sanctions" in text or "compliance" in text
    if requirement_name == "carrier_operational_behaviour":
        return "carrier" in text or "transit" in text
    return False


def _evidence_weight(count, requirement):
    if count >= requirement.get("minimum_sources", 1):
        return "high" if requirement.get("strength_threshold") == "high" else "medium"
    return "low"


def _remaining_gap(count, requirement):
    if count == 0:
        return "No selected source directly satisfies this requirement."
    if count < requirement.get("minimum_sources", 1):
        return "Below minimum source count."
    return "No immediate coverage gap; analyst should still verify recency and source content."
