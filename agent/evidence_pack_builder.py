from datetime import datetime
from pathlib import Path
import json

from agent.core.provenance import enrich_source_provenance
from agent.core.scoring import build_traceable_scores
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
    selected_sources = [
        enrich_source_provenance(source, search_result["fallback_demo_data_used"], retrieval_timestamp)
        for source in selected_sources
    ]
    rejected_sources = [
        enrich_source_provenance(source, search_result["fallback_demo_data_used"], retrieval_timestamp)
        for source in rejected_sources
    ]
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
    traceable_scores = build_traceable_scores(risk_scores, {**partial_pack, "confidence_cap_reason": quantified_readout["confidence_cap"]})
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
        "traceable_scores": traceable_scores,
        "scoring_method_note": "Structured analyst score; evidence-backed decision support, not a predictive or statistically validated model.",
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
        exact_matching = [
            item for item in evidence
            if item.get("requirement_id") == requirement.get("requirement_id")
            or item.get("requirement_name") == requirement.get("requirement_name")
        ]
        if exact_matching:
            matching = exact_matching
        else:
            unmapped_evidence = [
                item for item in evidence
                if not item.get("requirement_id") and not item.get("requirement_name")
            ]
            matching = [
                item for item in unmapped_evidence
                if item.get("source_type") in _normalised_source_types(requirement["preferred_source_types"])
                or _requirement_name_matches(requirement["requirement_name"], item)
            ]
        grade = _coverage_grade(requirement, matching)
        coverage.append(
            {
                "requirement_id": requirement["requirement_id"],
                "requirement_name": requirement["requirement_name"],
                "why_required": requirement["why_required"],
                "covered_by": [item["source_id"] for item in matching],
                "covered_by_count": len(matching),
                "evidence_weight": _evidence_weight(len(matching), requirement),
                "coverage_grade": grade["coverage_grade"],
                "coverage_grade_reason": grade["coverage_grade_reason"],
                "confidence_impact": grade["confidence_impact"],
                "gap_affects_confidence": grade["gap_affects_confidence"],
                "decision_questions_supported": requirement.get("decision_questions_supported", []),
                "remaining_gap": _graded_remaining_gap(len(matching), requirement, grade),
            }
        )
    return coverage


def _coverage_grade(requirement, matching):
    if not matching:
        return {
            "coverage_grade": "missing",
            "coverage_grade_reason": "No selected source is mapped to this requirement.",
            "confidence_impact": "High: this missing requirement should cap confidence.",
            "gap_affects_confidence": True,
        }

    strongest = sorted(matching, key=_coverage_strength, reverse=True)[0]
    mode = strongest.get("evidence_source_mode", "")
    inference = strongest.get("inference_strength", "")
    source_type = strongest.get("source_type", "")
    title = " ".join([strongest.get("title", ""), strongest.get("source_title", "")]).lower()
    caveat_text = " ".join([strongest.get("caveat", ""), strongest.get("source_limitations", "")]).lower()

    if _historical_context_only(strongest, title):
        return {
            "coverage_grade": "historical_context_only",
            "coverage_grade_reason": f"{strongest.get('source_id', '')} is useful as historical/contextual evidence but does not provide a current direct signal.",
            "confidence_impact": "Medium-high: historical evidence supports analogy only and should not drive current scoring alone.",
            "gap_affects_confidence": True,
        }

    if mode in {"full_text", "pdf_text"} and inference in {"direct", "moderate"} and source_type != "unknown" and "snippet" not in caveat_text:
        return {
            "coverage_grade": "strong_direct_full_text",
            "coverage_grade_reason": f"{strongest.get('source_id', '')} provides direct full-text or PDF-text evidence for the requirement.",
            "confidence_impact": "Lower: this requirement is strongly covered, subject to normal recency and context review.",
            "gap_affects_confidence": False,
        }

    if mode == "snippet_only":
        return {
            "coverage_grade": "direct_snippet_only",
            "coverage_grade_reason": f"{strongest.get('source_id', '')} is mapped to the requirement but only snippet/metadata evidence is available.",
            "confidence_impact": "Medium: source should be verified before operational use.",
            "gap_affects_confidence": True,
        }

    return {
        "coverage_grade": "partial_or_indirect",
        "coverage_grade_reason": f"{strongest.get('source_id', '')} is relevant but indirect, low-specificity or not operationally sufficient by itself.",
        "confidence_impact": "Medium: partial coverage supports screening but caps operational confidence.",
        "gap_affects_confidence": True,
    }


def _coverage_strength(item):
    mode_score = {"full_text": 4, "pdf_text": 3, "manual_input": 2, "snippet_only": 1, "fallback": 0}.get(item.get("evidence_source_mode", ""), 1)
    inference_score = {"direct": 3, "moderate": 2, "weak": 1}.get(item.get("inference_strength", ""), 1)
    weight_score = {"high": 3, "medium": 2, "low": 1}.get(item.get("evidence_weight", ""), 1)
    return (mode_score, inference_score, weight_score, item.get("total_score") or 0)


def _historical_context_only(item, title):
    text = " ".join(
        [
            title,
            item.get("source_claim", ""),
            item.get("extracted_evidence", ""),
            item.get("analyst_inference", ""),
            item.get("caveat", ""),
        ]
    ).lower()
    if "historical" in text or "precedent" in text or "context only" in text:
        return True
    date_value = item.get("publication_date") or item.get("date") or ""
    return date_value.startswith(("2020", "2021", "2022", "2023")) and any(term in text for term in ["precedent", "case study", "u-turn", "temporary gilt"])


def _graded_remaining_gap(count, requirement, grade):
    if count == 0:
        return _remaining_gap(count, requirement)
    if grade["coverage_grade"] == "strong_direct_full_text":
        return "No major source-coverage gap; verify recency, context and operational applicability."
    if grade["coverage_grade"] == "direct_snippet_only":
        return "Mapped source is snippet-only; verify full source text before using this requirement operationally."
    if grade["coverage_grade"] == "historical_context_only":
        return "Evidence is historical/contextual; refresh with current direct evidence before increasing confidence."
    return "Evidence is partial or indirect; add a stronger current direct source before treating this requirement as operationally sufficient."


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
