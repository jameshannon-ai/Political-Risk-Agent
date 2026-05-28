from datetime import datetime
from pathlib import Path

from agent.quantitative_assessment import calculate_quantitative_assessment


CATEGORY_PURPOSES = {
    "official_primary": "Establishes verified safety, security or regulatory baseline.",
    "company_update": "Shows operational decisions by carriers or market participants.",
    "energy_chokepoint_data": "Quantifies oil, LNG and strategic trade exposure.",
    "insurance_market_evidence": "Supports premium, reinsurance and underwriting assessment.",
    "vessel_flow_or_freight_market_evidence": "Shows whether market behaviour confirms disruption.",
    "reputable_news": "Corroborates current events and commercial impacts.",
    "specialist_analysis": "Adds market interpretation and scenario framing.",
    "contrary_or_stabilising_evidence": "Tests the downside case and supports confidence discipline.",
}


def generate_source_audit(evidence_pack):
    return f"""# Source Audit

## Search Configuration

- Topic: {evidence_pack["topic"]}
- Business user: {evidence_pack["business_user"]}
- Region: {evidence_pack["region"]}
- Time horizon: {evidence_pack["time_horizon"]}
- Concerns: {", ".join(evidence_pack["concerns"])}
- Search provider used: {evidence_pack["search_provider"]}
- Evidence mode: {evidence_pack.get("evidence_mode", "")}
- Fallback data used: {str(evidence_pack["fallback_demo_data_used"]).lower()}
- Provider error: {evidence_pack.get("provider_error", "") or "None"}
- Retrieval timestamp: {evidence_pack["retrieval_timestamp"]}

## Research Plan

{_research_plan(evidence_pack)}

## Source Strategy

{_source_strategy(evidence_pack)}

## Search Results Summary

- Total candidate sources found: {evidence_pack["candidate_count"]}
- Total queries run: {evidence_pack.get("total_queries_run", 0)}
- Total selected sources: {evidence_pack["selected_count"]}
- Duplicate URLs removed: {evidence_pack.get("duplicate_urls_removed", 0)}
- Source categories covered: {", ".join(evidence_pack["source_categories_covered"]) or "None"}
- Source categories missing: {", ".join(evidence_pack["source_categories_missing"]) or "None"}
- Fetch failures: {len(evidence_pack["fetch_failures"])}

## Quantified Evidence Summary

{_quantified_evidence_summary(evidence_pack)}

## Source Requirement Coverage

{_requirement_coverage(evidence_pack)}

## Selected Sources

{_selected_sources(evidence_pack)}

## Rejected Sources

{_rejected_sources(evidence_pack)}

## Evidence Coverage Assessment

- Strongest evidence category: {_strongest_category(evidence_pack)}
- Weakest evidence category: {_weakest_category(evidence_pack)}
- Missing evidence: {", ".join(evidence_pack["source_categories_missing"]) or "None identified"}
- Contrary/stabilising evidence: {_contrary_status(evidence_pack)}
- Confidence impact: {_confidence_impact(evidence_pack)}

## Route-Cost Assumptions

{_route_cost_assumptions(evidence_pack)}

## Refresh Triggers

{_refresh_triggers(evidence_pack)}

## Analyst Review Controls

- Verify publication dates.
- Verify fetched content against source page.
- Check source freshness.
- Check carrier/company updates remain current.
- Check market pricing recency.
- Check de-escalation reporting.
- Check sanctions/legal implications.
"""


def save_source_audit(markdown, output_dir, topic):
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = output_dir / f"{timestamp}-{_slugify(topic)}-source-audit.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def _source_strategy(evidence_pack):
    blocks = []
    for item in evidence_pack["source_strategy"]["categories"]:
        category = item["category"]
        blocks.append(
            "### {category}\n\n"
            "- Why it matters: {why}\n"
            "- Source requirement: {requirement}\n"
            "- Evidence question: {question}\n"
            "- Preferred domains: {domains}\n"
            "- Preferred source types: {source_types}\n"
            "- Generated queries:\n{queries}\n"
            "- Minimum acceptable evidence: {minimum}\n"
            "- Refresh expectation: {refresh}".format(
                category=category,
                why=CATEGORY_PURPOSES.get(category, "Supports evidence coverage."),
                requirement=item.get("requirement_name", item.get("source_requirement", "")),
                question=item.get("evidence_question", item.get("target_evidence_question", "")),
                domains=", ".join(item.get("preferred_domains", [])) or "None specified",
                source_types=", ".join(item.get("preferred_source_types", [])) or item.get("expected_source_type", ""),
                queries="\n".join(f"  - {query}" for query in item["queries"]),
                minimum=item.get("minimum_acceptable_evidence", 1),
                refresh=item.get("refresh_expectation", item.get("freshness_expectation", "")),
            )
        )
    return "\n\n".join(blocks)


def _research_plan(evidence_pack):
    plan = evidence_pack.get("source_plan", {})
    if not plan:
        return "No research plan available."
    return "\n".join(
        [
            f"- Research objective: {plan.get('research_objective', '')}",
            "- Decision questions:",
            *[f"  - {question}" for question in plan.get("decision_questions", [])],
            "- Required source mix:",
            *[f"  - {item}" for item in plan.get("required_source_mix", [])],
            "- Expected evidence types: " + (", ".join(plan.get("expected_evidence_types", [])) or "None specified"),
            f"- Minimum acceptable coverage: {plan.get('minimum_acceptable_coverage', {})}",
            "- Refresh priorities:",
            *[
                f"  - {item.get('requirement_name')}: {item.get('refresh_expectation')}"
                for item in plan.get("refresh_priorities", [])
            ],
        ]
    )


def _quantified_evidence_summary(evidence_pack):
    assessment = calculate_quantitative_assessment(evidence_pack)
    readout = evidence_pack.get("quantified_evidence_readout", {})
    rows = [
        ("Source count", assessment["total_selected_sources"]),
        ("Source coverage", f"{assessment['required_source_coverage_percentage']}%"),
        ("High-weight source count", assessment["high_weight_sources"]),
        ("Quantified facts", assessment["number_of_quantified_facts_extracted"]),
        ("Score support summary", readout.get("score_support_summary", assessment["evidence_strength_summary"])),
        ("Confidence cap reason", evidence_pack.get("confidence_cap_reason", assessment["confidence_cap_reason"])),
    ]
    return "\n".join(f"- {label}: {value}" for label, value in rows)


def _requirement_coverage(evidence_pack):
    rows = [
        "| Requirement | Why Required | Covered By | Evidence Weight | Decision Questions Supported | Remaining Gap |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in evidence_pack.get("requirement_coverage", []):
        rows.append(
            "| {requirement} | {why} | {covered_by} | {weight} | {questions} | {gap} |".format(
                requirement=_cell(item["requirement_name"]),
                why=_cell(item["why_required"]),
                covered_by=_cell(", ".join(item["covered_by"]) or "None"),
                weight=_cell(item["evidence_weight"]),
                questions=_cell("; ".join(item["decision_questions_supported"])),
                gap=_cell(item["remaining_gap"]),
            )
        )
    return "\n".join(rows) if len(rows) > 2 else "No source requirements available."


def _route_cost_assumptions(evidence_pack):
    if evidence_pack.get("business_user") != "shipping_operator":
        return "- Route-cost assumptions are case-specific and were not foregrounded in this business-user path."
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "regulatory_carbon_shipping":
        return "\n".join(
            [
                "- Carbon-cost outputs use illustrative route, vessel, fuel-burn and UKA price assumptions that require operator sign-off.",
                "- Validate route classification, responsible entity, fuel consumption and verifier methodology before relying on the estimate commercially.",
                "- Refresh the manual UKA input before pricing, contracting or allowance procurement decisions.",
            ]
        )
    return "\n".join(
        [
            "- Direct, delay and reroute comparisons use illustrative voyage assumptions requiring operator validation.",
            "- Validate voyage days, bunker burn, daily vessel cost, war-risk premiums, demurrage and compliance hold assumptions before route approval.",
            "- Sanctions risk should be treated as a legal override, not just a line item in the direct-route cost stack.",
        ]
    )


def _refresh_triggers(evidence_pack):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "regulatory_carbon_shipping":
        return "\n".join(
            [
                "- Refresh UKA price before pricing or contract decisions.",
                "- Refresh UK ETS Authority guidance if maritime scope, reporting or surrender deadlines change.",
                "- Validate operator-specific fuel burn and route classification before using the cost estimate commercially.",
                "- Refresh future-scope assumptions if UK-international maritime expansion policy changes.",
                "- Review emissions factor methodology with verifier / MRV process.",
            ]
        )
    triggers = [
        item.get("refresh_trigger", "")
        for item in evidence_pack.get("refresh_priorities", [])
        if item.get("refresh_trigger")
    ]
    if not triggers:
        return "- Refresh before major commercial decisions."
    return "\n".join(f"- {trigger}" for trigger in triggers[:8])


def _selected_sources(evidence_pack):
    if not evidence_pack["selected_sources"]:
        return "No selected sources."
    rows = [
        "| Source ID | Requirement | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    evidence_by_id = {item["source_id"]: item for item in evidence_pack["evidence"]}
    for source in evidence_pack["selected_sources"]:
        evidence = evidence_by_id.get(source.get("source_id"), {})
        rows.append(
            "| {source_id} | {requirement} | {query} | {question} | {title} | {reliability} | {relevance} | {recency} | {specificity} | {decision_value} | {independence} | {weight} | {reason} | {decision_use} | {fetch_status} | {caveat} |".format(
                source_id=_cell(source.get("source_id", "")),
                requirement=_cell(source.get("requirement_name", "") or source.get("source_type", "")),
                query=_cell(source.get("query", "")),
                question=_cell(source.get("decision_question_supported", "")),
                title=_cell(_clean_title(source.get("title", ""))),
                reliability=source.get("reliability_score", ""),
                relevance=source.get("relevance_score", ""),
                recency=source.get("recency_score", ""),
                specificity=source.get("specificity_score", ""),
                decision_value=source.get("decision_value_score", ""),
                independence=source.get("independence_score", ""),
                weight=_cell(source.get("evidence_weight", "")),
                reason=_cell(source.get("selection_reason", "")),
                decision_use=_cell(source.get("decision_use", "")),
                fetch_status=_cell(evidence.get("fetch_status", "")),
                caveat=_cell(evidence.get("caveat", source.get("caveat", ""))),
            )
        )
    return "\n".join(rows)


def _rejected_sources(evidence_pack, limit=10):
    rejected = evidence_pack.get("rejected_sources", [])[:limit]
    if not rejected:
        return "No rejected sources recorded."
    rows = [
        "| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for source in rejected:
        rows.append(
            "| {title} | {requirement} | {query} | {score} | {lowest} | {reason} | {covered} |".format(
                title=_cell(source.get("title", "")),
                requirement=_cell(source.get("requirement_name", "") or source.get("source_type", "")),
                query=_cell(source.get("query", "")),
                score=source.get("total_score", source.get("ranking_score", "")),
                lowest=_cell(source.get("lowest_scoring_dimension", "")),
                reason=_cell(source.get("rejection_reason", "")),
                covered="yes" if "stronger source" in source.get("rejection_reason", "") else "no",
            )
        )
    return "\n".join(rows)


def _strongest_category(evidence_pack):
    if "official_primary" in evidence_pack["source_categories_covered"]:
        return "official_primary"
    return evidence_pack["source_categories_covered"][0] if evidence_pack["source_categories_covered"] else "None"


def _weakest_category(evidence_pack):
    if evidence_pack["source_categories_missing"]:
        return evidence_pack["source_categories_missing"][0]
    if evidence_pack.get("fallback_demo_data_used"):
        return "live retrieval status"
    return "None identified"


def _contrary_status(evidence_pack):
    return "Present" if "contrary_or_stabilising_evidence" in evidence_pack["source_categories_covered"] else "Missing"


def _confidence_impact(evidence_pack):
    if evidence_pack.get("fallback_demo_data_used"):
        return "Confidence capped because the run used a curated fallback source pack rather than live API retrieval."
    if evidence_pack["source_categories_missing"]:
        return "Confidence reduced by missing evidence categories."
    return "Evidence coverage supports higher confidence, subject to analyst review."


def _clean_title(title):
    title = title.replace("[PDF] ", "").replace(":: Lloyd's List", "").replace(" - GOV.UK", "")
    title = title.replace(" | Stephenson Harwood", "").replace(" - International Council on Clean Transportation", " - ICCT")
    title = title.replace(" ...", "").replace("...", "")
    return " ".join(title.split())


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def _slugify(value):
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
