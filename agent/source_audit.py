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
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
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

## Provenance And Extraction Limits

{_provenance_limits(evidence_pack)}

## Scoring Traceability

{_scoring_traceability(evidence_pack)}

## Evidence-To-Score Bridge

{_evidence_to_score_bridge(evidence_pack)}

## Source Requirement Coverage

{_requirement_coverage(evidence_pack)}

## Source Quality Notes

{_source_quality_notes(evidence_pack)}

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

## {_assumption_section_title(domain)}

{_route_cost_assumptions(evidence_pack)}

## Refresh Triggers

{_refresh_triggers(evidence_pack)}

## Analyst Review Controls

{_analyst_review_controls(domain)}
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
    graded = _coverage_grade_counts(evidence_pack)
    rows = [
        ("Source count", assessment["total_selected_sources"]),
        ("Requirements identified", f"{graded['identified']}/{graded['identified']}"),
        ("Strongly covered", f"{graded['strong_direct_full_text']}/{graded['identified']}"),
        ("Direct snippet-only", f"{graded['direct_snippet_only']}/{graded['identified']}"),
        ("Partial or indirect", f"{graded['partial_or_indirect']}/{graded['identified']}"),
        ("Historical/context only", f"{graded['historical_context_only']}/{graded['identified']}"),
        ("Missing", f"{graded['missing']}/{graded['identified']}"),
        ("High-weight source count", assessment["high_weight_sources"]),
        ("Quantified facts", assessment["number_of_quantified_facts_extracted"]),
        ("Score support summary", readout.get("score_support_summary", assessment["evidence_strength_summary"])),
        ("Confidence cap reason", evidence_pack.get("confidence_cap_reason", assessment["confidence_cap_reason"])),
    ]
    return "\n".join(f"- {label}: {value}" for label, value in rows)


def _provenance_limits(evidence_pack):
    evidence = evidence_pack.get("evidence", [])
    if not evidence:
        return "- No extracted evidence rows available."
    rows = [
        "| Source ID | Evidence mode | Fetch status | Inference strength | Extraction confidence | Human review | Limitation |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in evidence:
        rows.append(
            "| {source_id} | {mode} | {fetch_status} | {strength} | {confidence} | {review} | {limit} |".format(
                source_id=_cell(item.get("source_id", "")),
                mode=_cell(item.get("evidence_source_mode", "")),
                fetch_status=_cell(item.get("fetch_status", "")),
                strength=_cell(item.get("inference_strength", "")),
                confidence=_cell(item.get("extraction_confidence", "")),
                review=_cell(str(item.get("requires_human_review", False)).lower()),
                limit=_cell(item.get("source_limitations", "")),
            )
        )
    return "\n".join(rows)


def _scoring_traceability(evidence_pack):
    traceable = evidence_pack.get("traceable_scores", {})
    if not traceable:
        return "- Traceable score object not available for this pack."
    rows = [
        "| Dimension | Score | Label | Score Type | Confidence | Supporting Evidence | Weakening Evidence | Evidence Quality Limits | Missing Evidence | Cap / Review Reason |",
        "| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for dimension, item in traceable.items():
        rows.append(
            "| {dimension} | {score} | {label} | {score_type} | {confidence} | {supporting} | {contrary} | {quality} | {missing} | {cap} |".format(
                dimension=_cell(dimension),
                score=_cell(item.get("score", "")),
                label=_cell(item.get("score_label", "")),
                score_type=_cell(item.get("score_type", "")),
                confidence=_cell(item.get("confidence", "")),
                supporting=_cell(", ".join(_ref_ids(item.get("supporting_evidence", item.get("evidence_supporting_score", [])))) or "None"),
                contrary=_cell(", ".join(_ref_ids(item.get("weakening_evidence", item.get("contrary_evidence", item.get("evidence_weakening_score", []))))) or "None"),
                quality=_cell(", ".join(_ref_ids(item.get("evidence_quality_limits", []))) or "None"),
                missing=_cell(", ".join(item.get("missing_evidence", [])) or "None"),
                cap=_cell(item.get("confidence_cap_reason", item.get("reason_score_is_capped", ""))),
            )
        )
    return "\n".join(rows)


def _evidence_to_score_bridge(evidence_pack):
    bridge = evidence_pack.get("evidence_to_score_bridge", {})
    if not bridge:
        return "- Evidence-to-score bridge not available for this pack."
    rows = [
        "| Dimension | Score | Evidence Basis | Confidence Effect | Cap Reason |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for dimension, item in bridge.items():
        if not isinstance(item, dict):
            continue
        rows.append(
            "| {dimension} | {score} | {basis} | {effect} | {cap} |".format(
                dimension=_cell(dimension),
                score=_cell(item.get("score", "")),
                basis=_cell(item.get("evidence_basis", item.get("reason_for_score", ""))),
                effect=_cell(item.get("confidence_effect", "")),
                cap=_cell(item.get("confidence_cap_reason", item.get("reason_score_is_capped", ""))),
            )
        )
    return "\n".join(rows) if len(rows) > 2 else "- Evidence-to-score bridge not available for this pack."


def _ref_ids(rows):
    ids = []
    for row in rows:
        if isinstance(row, str) and row:
            ids.append(row)
        elif isinstance(row, dict) and row.get("source_id"):
            ids.append(row["source_id"])
    return ids


def _requirement_coverage(evidence_pack):
    rows = [
        _graded_coverage_summary(evidence_pack),
        "",
        "| Requirement | Coverage Grade | Supporting Sources | Reason For Grade | Remaining Gap | Gap Affects Confidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in evidence_pack.get("requirement_coverage", []):
        rows.append(
            "| {requirement} | {grade} | {covered_by} | {reason} | {gap} | {confidence} |".format(
                requirement=_cell(item["requirement_name"]),
                grade=_cell(item.get("coverage_grade", item.get("evidence_weight", ""))),
                covered_by=_cell(", ".join(item["covered_by"]) or "None"),
                reason=_cell(item.get("coverage_grade_reason", item["why_required"])),
                gap=_cell(item["remaining_gap"]),
                confidence=_cell(str(item.get("gap_affects_confidence", item.get("covered_by_count", 0) == 0)).lower()),
            )
        )
    return "\n".join(rows) if len(rows) > 4 else "No source requirements available."


def _coverage_grade_counts(evidence_pack):
    coverage = evidence_pack.get("requirement_coverage", [])
    counts = {
        "identified": len(coverage),
        "strong_direct_full_text": 0,
        "direct_snippet_only": 0,
        "partial_or_indirect": 0,
        "historical_context_only": 0,
        "missing": 0,
    }
    for item in coverage:
        grade = item.get("coverage_grade") or ("missing" if item.get("covered_by_count", 0) == 0 else "partial_or_indirect")
        if grade in counts:
            counts[grade] += 1
    return counts


def _graded_coverage_summary(evidence_pack):
    counts = _coverage_grade_counts(evidence_pack)
    total = counts["identified"]
    return "\n".join(
        [
            f"- Requirements identified: {total}/{total}",
            f"- Strongly covered: {counts['strong_direct_full_text']}/{total}",
            f"- Direct snippet-only: {counts['direct_snippet_only']}/{total}",
            f"- Partial or indirect: {counts['partial_or_indirect']}/{total}",
            f"- Historical/context only: {counts['historical_context_only']}/{total}",
            f"- Missing: {counts['missing']}/{total}",
        ]
    )


def _route_cost_assumptions(evidence_pack):
    if evidence_pack.get("business_user") != "shipping_operator":
        domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
        if domain == "critical_minerals_supply_chain":
            return "\n".join(
                [
                    "- Production continuity outputs use illustrative inventory, qualification, concentration and revenue inputs unless company data is supplied.",
                    "- Replace bill of materials, supplier-country, inventory, purchase order, contract and customer data before using the model commercially.",
                    "- Treat the continuity gap as a client-type decision aid, not a company-specific production forecast.",
                ]
            )
        if domain == "uk_fiscal_procurement_risk":
            return "\n".join(
                [
                    "- Public evidence screens fiscal, procurement and payment-risk exposure; it does not measure a contractor-specific order book.",
                    "- Replace public evidence with customer mix, bid pipeline, payment terms, margin and working-capital data before operational use.",
                    "- Treat procurement-delay and payment-risk scoring as decision-support, not a forecast of any individual contract award or payment.",
                ]
            )
        return "- Scenario assumptions are case-specific and were not foregrounded in this business-user path."
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
            "- Direct, delay and reroute comparisons use illustrative scenario inputs rather than company-specific voyage facts.",
            "- Replace vessel value, charter rate, bunker cost, insurance quote, demurrage exposure and voyage-plan assumptions before commercial use.",
            "- Validate voyage days, bunker burn, daily vessel cost, war-risk premiums, demurrage and compliance hold assumptions before route approval.",
            "- Sanctions risk should be treated as a legal override, not just a line item in the direct-route cost stack.",
        ]
    )


def _refresh_triggers(evidence_pack):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "critical_minerals_supply_chain":
        return "\n".join(
            [
                "- Refresh if export-control rules or licensing practice changes.",
                "- Refresh if China-linked export licences tighten or ease.",
                "- Refresh if rare earth magnet shortage or price signals change.",
                "- Refresh if alternative supplier qualification assumptions change.",
                "- Refresh when company BOM, supplier, inventory or contract data becomes available.",
            ]
        )
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
    if domain == "maritime_trade":
        return "\n".join(
            [
                "- Refresh immediately if any toll, safe-passage fee, guarantee, offset, swap or in-kind demand is reported.",
                "- Refresh before voyage approval if war-risk premium, exclusions, cancellation wording or insurer appetite changes.",
                "- Refresh if AIS disruption, detention reports, transit-control notices or official guidance change.",
                "- Validate vessel value, delay-cost, reroute-cost and charter assumptions before using the optimiser commercially.",
                "- Relax from hold or reroute only after official guidance, insurer appetite and vessel-flow recovery improve together.",
            ]
        )
    if domain == "uk_fiscal_procurement_risk":
        return "\n".join(
            [
                "- Refresh OBR outlook and ONS public-finance data after new releases.",
                "- Refresh HM Treasury spending, Budget or Spending Review material after fiscal-policy updates.",
                "- Refresh Bank of England and market-confidence evidence if gilt yields or financial-stability signals move materially.",
                "- Refresh procurement and infrastructure-pipeline evidence before changing bid/no-bid or project-delay controls.",
                "- Replace public evidence with contractor order book, customer mix, payment terms, margin and working-capital data before operational use.",
            ]
        )
    if domain == "sanctions_trade_finance":
        return "\n".join(
            [
                "- Refresh if sanctions designations, OFSI guidance or export-control rules change.",
                "- Refresh if goods classification, licence, authorisation or end-use status changes.",
                "- Refresh if sanctions screening, beneficial ownership, bank or intermediary data changes.",
                "- Refresh when invoices, bills of lading, contracts, end-use statements or payment instructions change.",
                "- Refresh before moving from legal hold or escalation back to approval.",
            ]
        )
    if domain == "cyber_business_interruption":
        return "\n".join(
            [
                "- Refresh if NCSC threat posture or ransomware reporting changes.",
                "- Refresh if a major UK retail / critical services cyber incident occurs.",
                "- Refresh if ICO / FCA / PRA / sector notification guidance changes.",
                "- Refresh if cyber insurance waiting periods, exclusions or claims conditions change.",
                "- Refresh when company systems map, revenue exposure, policy wording, recovery time or supplier/MSP dependency data becomes available.",
            ]
        )
    triggers = [
        item.get("refresh_trigger", "") if isinstance(item, dict) else str(item)
        for item in evidence_pack.get("refresh_priorities", [])
        if (item.get("refresh_trigger") if isinstance(item, dict) else item)
    ]
    if not triggers:
        return "- Refresh before major commercial decisions."
    return "\n".join(f"- {trigger}" for trigger in triggers[:8])


def _selected_sources(evidence_pack):
    if not evidence_pack["selected_sources"]:
        return "No selected sources."
    rows = [
        "| Source ID | Requirement | Source role | Source value | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    evidence_by_id = {item["source_id"]: item for item in evidence_pack["evidence"]}
    for source in evidence_pack["selected_sources"]:
        evidence = evidence_by_id.get(source.get("source_id"), {})
        rows.append(
            "| {source_id} | {requirement} | {role} | {value} | {query} | {question} | {title} | {reliability} | {relevance} | {recency} | {specificity} | {decision_value} | {independence} | {weight} | {reason} | {decision_use} | {fetch_status} | {caveat} |".format(
                source_id=_cell(source.get("source_id", "")),
                requirement=_cell(source.get("requirement_name", "") or source.get("source_type", "")),
                role=_cell(source.get("source_role", "")),
                value=_cell(source.get("source_value_explanation", source.get("evidence_value", ""))),
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
    selected = evidence_pack.get("selected_sources", [])
    if not selected:
        return "None"
    ranked = sorted(
        selected,
        key=lambda item: (
            3 if item.get("evidence_weight") == "high" else 2 if item.get("evidence_weight") == "medium" else 1,
            item.get("total_score", 0),
        ),
        reverse=True,
    )
    return ranked[0].get("source_type", "None")


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


def _analyst_review_controls(domain):
    if domain == "maritime_trade":
        return "\n".join(
            [
                "- Verify publication dates.",
                "- Verify fetched content against the source page or search snippet.",
                "- Check transit-control, detention and AIS evidence remain current.",
                "- Check war-risk premium, exclusions and insurer appetite before voyage approval.",
                "- Check sanctions/legal implications of any toll, payment, guarantee, offset or swap demand.",
                "- Check de-escalation reporting against practical vessel-flow recovery before relaxing controls.",
            ]
        )
    if domain == "uk_fiscal_procurement_risk":
        return "\n".join(
            [
                "- Verify publication dates and current fiscal-policy context.",
                "- Verify snippet-only sources against full source text before operational use.",
                "- Refresh OBR, ONS, HM Treasury and Bank of England evidence after material releases.",
                "- Check procurement pipeline and department-specific programme exposure before bid decisions.",
                "- Validate payment terms, retentions, aged receivables, margins and working-capital exposure with company data.",
                "- Escalate concentrated public-sector exposure to finance, commercial and board review before changing controls.",
            ]
        )
    if domain == "critical_minerals_supply_chain":
        return "\n".join(
            [
                "- Verify publication dates and current export-control context.",
                "- Refresh rare earth magnet licensing, shortage and price evidence before operational sourcing decisions.",
                "- Validate BOM, supplier ownership/country, inventory, contracts and qualification status with company data.",
                "- Treat substitution and redesign evidence as engineering input requiring technical review.",
                "- Keep contrary/easing evidence secondary until confirmed by official or high-quality market sources.",
            ]
        )
    if domain == "sanctions_trade_finance":
        return "\n".join(
            [
                "- Verify current OFSI, UK sanctions and export-control guidance before transaction approval.",
                "- Confirm goods classification, end-use, counterparty, ownership, route and payment data.",
                "- Escalate unresolved red flags to sanctions/export-control legal review.",
                "- Treat source evidence as a client-type exposure screen, not a transaction clearance decision.",
                "- Require internal risk appetite and legal/compliance sign-off before approval or release.",
            ]
        )
    if domain == "cyber_business_interruption":
        return "\n".join(
            [
                "- Verify NCSC, ICO and sector-regulator guidance before operational use.",
                "- Validate affected systems, revenue exposure, RTO/RPO, backup capability and supplier/MSP dependencies.",
                "- Review cyber insurance policy wording, waiting periods, retentions and exclusions with broker/legal teams.",
                "- Treat the resilience gap and business interruption exposure as illustrative until incident facts and company data are supplied.",
                "- Keep the analysis focused on interruption, notification, claims and recovery decisions rather than technical cybersecurity advice.",
            ]
        )
    return "\n".join(
        [
            "- Verify publication dates.",
            "- Verify fetched content against source page.",
            "- Check source freshness.",
            "- Check carrier/company updates remain current.",
            "- Check market pricing recency.",
            "- Check de-escalation reporting.",
            "- Check sanctions/legal implications.",
        ]
    )


def _assumption_section_title(domain):
    if domain == "critical_minerals_supply_chain":
        return "Production Continuity Assumptions"
    if domain == "uk_fiscal_procurement_risk":
        return "Scenario And Exposure Limits"
    return "Illustrative Route-Cost Scenario"


def _source_quality_notes(evidence_pack):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "regulatory_carbon_shipping":
        rows = [
            ("Official / policy scope", "Strong where GOV.UK or UK ETS Authority evidence is present.", "Refresh official maritime scope, reporting and surrender guidance before operational reliance."),
            ("Legal / compliance interpretation", "Specialist analysis only; not official policy.", "Validate with counsel, verifier and responsible-entity analysis."),
            ("Carbon cost inputs", "Illustrative until operator fuel burn, verifier methodology and current UKA price are confirmed.", "Manual fallback UKA price should be refreshed before pricing or contracting."),
            ("International route exposure", "Scenario-only unless confirmed by official evidence.", "Keep future-scope assumptions separate from confirmed domestic coverage."),
        ]
    elif domain == "critical_minerals_supply_chain":
        rows = [
            ("UK policy anchor", "Useful official policy context; not a company-specific supply assurance.", "Refresh if UK critical minerals or manufacturing resilience policy changes."),
            ("Export-control trigger", "Live reporting supports licensing friction, but operational exposure depends on exact inputs.", "Refresh if export-control rules or licensing practice changes."),
            ("Supply concentration", "Good directional evidence; map to the manufacturer BOM before operational use.", "Refresh if China-linked export licences tighten or ease."),
            ("Substitution feasibility", "Medium evidence quality; magnet-specific engineering qualification remains weak.", "Refresh if alternative supplier qualification assumptions change."),
            ("Market/pricing shortage signal", "Directional rather than a robust pricing benchmark.", "Refresh if rare earth magnet shortage or price signals change."),
            ("Company-specific data requirements", "Public evidence cannot measure actual inventory runway or contract exposure.", "Refresh when company BOM, supplier, inventory or contract data becomes available."),
        ]
    elif domain == "sanctions_trade_finance":
        rows = [
            ("UK sanctions / OFSI anchor", "Official guidance supports legal and compliance relevance.", "Refresh if sanctions designations, OFSI guidance or export-control rules change."),
            ("End-use and controlled goods", "Regulatory guidance supports hold/escalation triggers but not transaction clearance.", "Confirm goods classification, licence and end-use data."),
            ("Counterparty and ownership", "Official ownership/control guidance is strong, but named-party screening is private.", "Refresh screening and beneficial ownership data before approval."),
            ("Documentation quality", "Trade finance guidance supports document controls.", "Transaction-specific use requires invoices, bills of lading, contracts, payment instructions and end-user statements."),
            ("Clearance / contrary evidence", "Licences or exceptions can reduce risk only where exact conditions are met.", "Treat exceptions as conditional, not an all-clear."),
        ]
    elif domain == "cyber_business_interruption":
        rows = [
            ("UK official cyber threat / NCSC evidence", "Official threat framing supports likelihood but not a company-specific incident forecast.", "Refresh if NCSC threat posture or ransomware reporting changes."),
            ("UK breach prevalence data", "Useful prevalence context; sector and company exposure need validation.", "Refresh after new breach survey or sector incident reporting."),
            ("Board governance / resilience expectations", "Regulatory and governance material supports escalation expectations.", "Refresh if ICO / FCA / PRA / sector notification guidance changes."),
            ("Cyber insurance / business interruption evidence", "Insurance-market evidence is useful but not coverage advice.", "Refresh if cyber insurance waiting periods, exclusions or claims conditions change."),
            ("Business interruption exposure", "Illustrative model output, not company-specific loss calculation.", "Refresh when revenue exposure, recovery time and policy wording are available."),
            ("Resilience gap", "Decision trigger is useful only after company RTO/RPO and recovery assumptions are confirmed.", "Refresh when company systems map, recovery time or supplier/MSP dependency data becomes available."),
        ]
    elif domain == "uk_fiscal_procurement_risk":
        rows = [
            ("Fiscal baseline", "Official fiscal evidence anchors public-finance pressure.", "Refresh OBR outlook and ONS public-finance data after new releases."),
            ("Market confidence", "Bank and market evidence informs gilt-sensitivity but is not contractor-specific.", "Refresh if gilt yields or financial-stability signals move materially."),
            ("Procurement delay", "Public procurement evidence is indicative, not a contract-award forecast.", "Refresh pipeline and department-specific evidence before bid/no-bid decisions."),
            ("Company exposure", "Public evidence cannot measure order book, payment terms or working-capital exposure.", "Replace public evidence with contractor data before operational use."),
        ]
    else:
        rows = [
            ("Source coverage", "Selected sources support a client-type risk screen.", "Refresh before operational use."),
            ("Company data", "Public evidence does not provide transaction- or company-specific exposure.", "Validate with private data and human review."),
        ]
    table = [
        "| Evidence area | Current source quality | Action before operational use |",
        "| --- | --- | --- |",
    ]
    table.extend(f"| {_cell(area)} | {_cell(quality)} | {_cell(action)} |" for area, quality, action in rows)
    return "\n".join(table)


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def _slugify(value):
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
