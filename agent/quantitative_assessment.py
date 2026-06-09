def calculate_quantitative_assessment(evidence_pack):
    selected = evidence_pack.get("selected_sources", [])
    evidence = evidence_pack.get("evidence", [])
    requirements = evidence_pack.get("requirement_coverage", [])
    quantified_facts = _all_quantified_facts(evidence)
    covered_requirements = [item for item in requirements if item.get("covered_by_count", 0) > 0]
    coverage_percent = round((len(covered_requirements) / len(requirements)) * 100) if requirements else 0

    return {
        "total_selected_sources": len(selected),
        "high_weight_sources": _count_weight(selected, "high"),
        "medium_weight_sources": _count_weight(selected, "medium"),
        "low_weight_sources": _count_weight(selected, "low"),
        "required_source_coverage_percentage": coverage_percent,
        "missing_source_requirements": [item["requirement_name"] for item in requirements if item.get("covered_by_count", 0) == 0],
        "average_reliability_score": _average(selected, "reliability_score"),
        "average_relevance_score": _average(selected, "relevance_score"),
        "average_recency_score": _average(selected, "recency_score"),
        "average_specificity_score": _average(selected, "specificity_score"),
        "average_decision_value_score": _average(selected, "decision_value_score"),
        "number_of_quantified_facts_extracted": len(quantified_facts),
        "number_of_contrary_or_stabilising_evidence_items": sum(1 for item in evidence if item.get("contrary_signal") or item.get("source_type") == "contrary_or_stabilising_evidence"),
        "confidence_cap_reason": _confidence_cap_reason(evidence_pack),
        "evidence_strength_summary": _evidence_strength_summary(selected, coverage_percent),
    }


def build_quantified_evidence_readout(evidence_pack):
    assessment = calculate_quantitative_assessment(evidence_pack)
    facts = _display_quantified_facts(evidence_pack)
    return {
        "source_count": assessment["total_selected_sources"],
        "high_weight_source_count": assessment["high_weight_sources"],
        "requirement_coverage_percent": assessment["required_source_coverage_percentage"],
        "average_source_quality": _average_quality(assessment),
        "quantified_facts": facts,
        "strongest_evidence": _strongest_evidence(evidence_pack),
        "weakest_evidence": _weakest_evidence(evidence_pack),
        "confidence_cap": assessment["confidence_cap_reason"],
        "score_support_summary": _score_support_summary(evidence_pack, assessment),
    }


def build_evidence_to_score_bridge(evidence_pack, risk_scores):
    evidence = evidence_pack.get("evidence", [])
    source_ids = [item.get("source_id", "") for item in evidence[:4]]
    fallback = evidence_pack.get("fallback_demo_data_used", False)

    bridge = {}
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    for dimension in ["likelihood", "impact", "immediacy", "confidence"]:
        score_data = risk_scores.get(dimension, {})
        score = score_data.get("score", "")
        bridge[dimension] = {
            "score": score,
            "score_label": _score_label(score),
            "score_type": "Evidence-backed decision-support score",
            "evidence_basis": _dimension_basis(dimension, evidence_pack, score_data, domain),
            "supporting_sources": _supporting_sources_for_dimension(dimension, evidence),
            "quantified_facts_used": _bridge_quantified_facts(evidence_pack, dimension),
            "why_score_not_higher": _why_not_higher(dimension, score, fallback),
            "why_score_not_lower": _why_not_lower(dimension, score, evidence_pack),
            "review_trigger": _review_trigger(dimension, evidence_pack),
            "supporting_evidence": _evidence_refs(_supporting_sources_for_dimension(dimension, evidence), evidence),
            "contrary_evidence": _contrary_refs(evidence),
            "evidence_quality_limits": _quality_limit_refs(evidence),
            "missing_evidence": evidence_pack.get("requirements_missing", []),
            "reason_for_score": _dimension_basis(dimension, evidence_pack, score_data, domain),
            "reason_score_is_capped": _why_not_higher(dimension, score, fallback),
            "confidence": _bridge_confidence(dimension, evidence_pack),
            "review_required": bool(evidence_pack.get("requirements_missing") or fallback),
        }
        bridge[dimension]["evidence_supporting_score"] = bridge[dimension]["supporting_evidence"]
        bridge[dimension]["evidence_weakening_score"] = bridge[dimension]["contrary_evidence"]
        if not bridge[dimension]["supporting_sources"]:
            bridge[dimension]["supporting_sources"] = source_ids
    return bridge


def _score_label(score):
    labels = {1: "Low", 2: "Guarded", 3: "Moderate", 4: "High", 5: "Severe"}
    return labels.get(score, "Unscored")


def _evidence_refs(source_ids, evidence):
    by_id = {item.get("source_id"): item for item in evidence}
    refs = []
    for source_id in source_ids:
        item = by_id.get(source_id)
        if item:
            refs.append(
                {
                    "source_id": source_id,
                    "source_title": item.get("source_title") or item.get("title", ""),
                    "claim": item.get("source_claim") or item.get("claim_supported", ""),
                    "inference_strength": item.get("inference_strength", ""),
                }
            )
    return refs


def _weakening_refs(evidence):
    return _contrary_refs(evidence)


def _contrary_refs(evidence):
    return [
        {
            "source_id": item.get("source_id", ""),
            "source_title": item.get("source_title") or item.get("title", ""),
            "reason": item.get("caveat", "") or "Contrary or stabilising evidence.",
        }
        for item in evidence
        if item.get("contrary_signal") or item.get("source_type") in {"contrary_or_stabilising_evidence", "contrary_scope_limit"}
    ][:5]


def _quality_limit_refs(evidence):
    return [
        {
            "source_id": item.get("source_id", ""),
            "source_title": item.get("source_title") or item.get("title", ""),
            "reason": item.get("source_limitations", "") or item.get("caveat", "") or "Evidence quality limit.",
        }
        for item in evidence
        if item.get("evidence_source_mode") in {"snippet_only", "fallback", "manual_input"}
        or item.get("requires_human_review")
        or item.get("inference_strength") == "weak"
        or item.get("extraction_confidence") == "low"
    ][:8]


def _bridge_confidence(dimension, evidence_pack):
    if evidence_pack.get("fallback_demo_data_used") or evidence_pack.get("requirements_missing"):
        return "medium" if dimension != "confidence" else "low"
    if any(item.get("evidence_source_mode") == "snippet_only" for item in evidence_pack.get("evidence", [])):
        return "medium"
    return "high"


def _all_quantified_facts(evidence):
    facts = []
    for item in evidence:
        for fact in item.get("quantified_facts", []):
            if fact not in facts:
                facts.append(fact)
    return facts


def _count_weight(sources, weight):
    return sum(1 for source in sources if source.get("evidence_weight") == weight)


def _average(sources, key):
    values = [source.get(key) for source in sources if isinstance(source.get(key), (int, float))]
    return round(sum(values) / len(values), 1) if values else 0


def _average_quality(assessment):
    values = [
        assessment["average_reliability_score"],
        assessment["average_relevance_score"],
        assessment["average_recency_score"],
        assessment["average_specificity_score"],
        assessment["average_decision_value_score"],
    ]
    values = [value for value in values if value]
    return round(sum(values) / len(values), 1) if values else 0


def _confidence_cap_reason(evidence_pack):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "critical_minerals_supply_chain":
        return "Confidence capped because live evidence can screen client-type exposure, but BOM, supplier, inventory and contract data are still required for company-specific production decisions."
    if domain == "uk_fiscal_procurement_risk":
        return "Confidence capped because public evidence can screen fiscal/procurement risk, but contractor order book, department exposure, payment terms, margins and working-capital data are required for operational decisions."
    if domain == "regulatory_carbon_shipping":
        return "Confidence capped below 5 because official policy evidence is strong, but the calculation uses illustrative voyage assumptions and a manual UKA price rather than an embedded live price feed."
    if evidence_pack.get("fallback_demo_data_used"):
        return "Confidence capped below 5 because evidence came from a reproducible curated source pack rather than live retrieval."
    if evidence_pack.get("requirements_missing"):
        return "Confidence capped because one or more source requirements are not covered."
    return "No explicit confidence cap from source mode; maintain review discipline for fast-moving evidence."


def _display_quantified_facts(evidence_pack):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "critical_minerals_supply_chain":
        return _critical_minerals_display_facts()
    if domain == "uk_fiscal_procurement_risk":
        return _uk_fiscal_procurement_display_facts(evidence_pack)
    if domain == "regulatory_carbon_shipping":
        return _uk_ets_display_facts(evidence_pack)
    if domain == "maritime_trade" and "hormuz" in evidence_pack.get("topic", "").lower():
        return _hormuz_display_facts()
    return _all_quantified_facts(evidence_pack.get("evidence", []))


def _bridge_quantified_facts(evidence_pack, dimension):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "critical_minerals_supply_chain":
        facts = {
            "likelihood": [
                "China-linked supply share: 70%",
                "Controlled rare earth magnet input identified",
                "Live export-control trigger evidence requires monitoring",
            ],
            "impact": [
                "Exposed product-line revenue: £50m illustrative",
                "Substitution difficulty: high",
                "Production continuity gap: 135 days",
            ],
            "immediacy": [
                "Inventory runway: 45 days",
                "Alternative supplier qualification time: 180 days",
                "Qualification lag exceeds current runway",
            ],
            "confidence": [
                "Client-type exposure screen only",
                "BOM / supplier / inventory data still required",
                "Customer delivery commitments still need validation",
            ],
        }
        return facts[dimension]
    if domain == "uk_fiscal_procurement_risk":
        facts = {
            "likelihood": [
                "Fiscal pressure indicator: OBR / ONS / HMT evidence required",
                "Market confidence indicator: gilt-market or fiscal credibility evidence required",
                "Political economy trigger: fiscal rules, tax/spending trade-offs and departmental budgets",
            ],
            "impact": [
                "Commercial channels: contract awards, procurement delays, deferrals and repricing",
                "Contractor exposure: public-sector customer mix and order book required",
                "Working-capital channel: payment terms and cash conversion require company data",
            ],
            "immediacy": [
                "Decision horizon: bid pipeline and board reporting should be refreshed near-term",
                "Procurement timing: department and programme evidence required",
                "Payment-risk monitoring: customer-level exposure required",
            ],
            "confidence": [
                "Company data missing: order book, departmental exposure, margins and payment terms",
                "Source coverage must include official fiscal, market and procurement evidence",
                "Snippet-only evidence triggers human review",
            ],
        }
        return facts.get(dimension, [])
    if domain == "maritime_trade" and "hormuz" in evidence_pack.get("topic", "").lower():
        facts = {
            "likelihood": [
                "Transit-control mechanism reported: 5 May 2026",
                "Safe-passage fee system reported with sanctions implications",
                "Official or quasi-official transit controls remain active",
            ],
            "impact": [
                "War-risk pricing: up to 12x pre-crisis levels",
                "Illustrative tanker premium: about $7.5m at a 3% rate",
                "VLCC shipping rate signal: above $400,000/day",
            ],
            "immediacy": [
                "AIS and vessel-flow disruption remains active",
                "Detention and transit-control risk remains live",
                "Recovery evidence is partial rather than normalised",
            ],
            "confidence": [
                "De-escalation evidence exists but remains conditional",
                "One fetch fell back to snippet-only evidence",
                "Insurance, sanctions and flow signals are still fast-moving",
            ],
        }
        return facts[dimension]
    if domain != "regulatory_carbon_shipping":
        return _all_quantified_facts(evidence_pack.get("evidence", []))[:6]

    facts = {
        "likelihood": [
            "Start date: 1 July 2026",
            "Vessel threshold: 5,000 GT",
            "Coverage: domestic UK voyages and at-berth emissions",
        ],
        "impact": [
            "Estimated cost: " + _format_gbp(_calculator_value(evidence_pack, "estimated_carbon_cost_per_voyage"), 0) + " per voyage",
            "Annualised estimate: " + _format_gbp(_calculator_value(evidence_pack, "annualised_carbon_cost"), 0),
            "Manual UKA input: " + _format_gbp(_calculator_assumption(evidence_pack, "uka_price_per_tonne"), 0) + "/t",
        ],
        "immediacy": [
            "Preparation window: within 12 months",
            "Reporting timeline: verified emissions report due by 31 March",
            "Surrender timing: transitional 30 April 2028 double-surrender window applies",
        ],
        "confidence": [
            "Pricing basis: manual UKA fallback",
            "Fuel-burn basis: 18 tonnes MGO per voyage (illustrative)",
            "Methodology caveat: emissions factor requires verifier review",
        ],
    }
    return facts[dimension]


def _evidence_strength_summary(selected, coverage_percent):
    return (
        f"{len(selected)} selected sources; {_count_weight(selected, 'high')} high-weight, "
        f"{_count_weight(selected, 'medium')} medium-weight, {_count_weight(selected, 'low')} low-weight; "
        f"{coverage_percent}% source-requirement coverage."
    )


def _strongest_evidence(evidence_pack):
    selected = sorted(
        evidence_pack.get("selected_sources", []),
        key=lambda item: (
            3 if item.get("evidence_weight") == "high" else 2 if item.get("evidence_weight") == "medium" else 1,
            item.get("total_score", 0),
        ),
        reverse=True,
    )
    if not selected:
        return "No selected source evidence."
    top = selected[0]
    return f"{top.get('source_id', '')} — {_clean_title(top.get('title', '') or 'Selected source')} ({top.get('evidence_weight', 'unknown')} weight)"


def _weakest_evidence(evidence_pack):
    missing = evidence_pack.get("requirements_missing", [])
    if missing:
        return "Missing requirements: " + ", ".join(missing)
    selected = sorted(evidence_pack.get("selected_sources", []), key=lambda item: item.get("total_score", 0))
    if selected:
        low = selected[0]
        return f"Lowest selected score: {low.get('source_id', '')} / {low.get('requirement_name', '')}"
    return "No weak evidence area identified."


def _score_support_summary(evidence_pack, assessment):
    return (
        f"Scores are supported by {assessment['total_selected_sources']} selected sources, "
        f"{assessment['required_source_coverage_percentage']}% requirement coverage and "
        f"{assessment['number_of_quantified_facts_extracted']} extracted quantified facts."
    )


def _dimension_basis(dimension, evidence_pack, score_data, domain=""):
    if domain == "critical_minerals_supply_chain":
        mapping = {
            "likelihood": "Likelihood is based on export-control direction, source concentration and live geopolitical or licensing triggers affecting rare earth magnet inputs.",
            "impact": "Impact is based on product criticality, revenue exposure, substitution difficulty, supplier concentration and the production continuity gap between inventory runway and qualification time.",
            "immediacy": "Immediacy is based on inventory runway versus alternative supplier qualification time and any evidence of shipment, licensing or procurement delay.",
            "confidence": "Confidence is based on source coverage, but capped by missing company-specific BOM, supplier, inventory and contract data.",
        }
        return mapping[dimension]
    if domain == "regulatory_carbon_shipping":
        mapping = {
            "likelihood": "Official UK ETS policy sources confirm domestic maritime expansion from 1 July 2026 for covered vessels and routes.",
            "impact": "Impact is material for in-scope domestic routes because allowance cost becomes a recurring voyage-level cost, but the score is limited because UK-international routes remain scenario-only and operator-specific fuel burn must be validated.",
            "immediacy": "Immediacy is high because operators need to prepare MRV, reporting, verification, allowance procurement and pricing/pass-through processes before the scheme date.",
            "confidence": "Confidence is capped at 4/5 because official policy evidence is strong, but the calculation uses illustrative voyage assumptions and a manual UKA price rather than an embedded live price feed.",
        }
        return mapping[dimension]
    if score_data.get("rationale"):
        return score_data["rationale"]
    mapping = {
        "likelihood": "Supported by current source coverage and source relevance.",
        "impact": "Supported by source claims on commercial exposure and risk-driver severity.",
        "immediacy": "Supported by source recency and time-horizon alignment.",
        "confidence": "Supported by source diversity, coverage and confidence caps.",
    }
    return mapping[dimension]


def _supporting_sources_for_dimension(dimension, evidence):
    terms = {
        "likelihood": ["official", "carrier", "regime", "guidance"],
        "impact": ["insurance", "energy", "payment", "collateral", "pricing"],
        "immediacy": ["flow", "operational", "current", "licence", "drawdown"],
        "confidence": ["contrary", "scope", "stabilising", "de-escalation"],
    }[dimension]
    matches = []
    for item in evidence:
        text = " ".join([item.get("risk_driver", ""), item.get("commercial_meaning", ""), item.get("judgement_supported", "")]).lower()
        if any(term in text for term in terms):
            matches.append(item.get("source_id", ""))
    return matches[:4]


def _why_not_higher(dimension, score, fallback):
    if fallback:
        return "Curated evidence mode caps confidence and requires live refresh before a higher score."
    if score and score >= 5:
        return "Already at maximum score; review only if evidence improves the confidence basis."
    return "Score is capped by remaining uncertainty, source freshness and transaction-specific facts."


def _why_not_lower(dimension, score, evidence_pack):
    coverage = build_quantified_evidence_readout(evidence_pack)["requirement_coverage_percent"]
    if coverage >= 80:
        return "Broad requirement coverage and weighted source evidence support the current score."
    return "Partial coverage supports the score but leaves review gaps."


def _review_trigger(dimension, evidence_pack):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "uk_fiscal_procurement_risk":
        if dimension == "confidence":
            return "Refresh live sources and add contractor order book, customer mix, payment terms and working-capital data before increasing confidence."
        if dimension == "immediacy":
            return "Refresh if fiscal statements, OBR/ONS releases, gilt-market stress or departmental budget signals change the near-term picture."
        if dimension == "impact":
            return "Refresh if procurement pipeline, project deferral, payment-risk or contract-pricing evidence changes."
        return "Refresh if official fiscal evidence, market confidence signals or credible stabilising evidence changes the risk direction."
    if dimension == "confidence":
        return "Refresh live sources or resolve missing requirements before increasing confidence."
    if dimension == "immediacy":
        return "Refresh if new operational, market, licensing or payment evidence changes the near-term picture."
    if dimension == "impact":
        return "Refresh if pricing, exposure, cargo, collateral or regulatory-penalty evidence changes."
    return "Refresh if official, company, regulator or credible contrary evidence changes the risk direction."


def _uk_ets_display_facts(evidence_pack):
    return [
        "Start date: 1 July 2026",
        "Vessel threshold: 5,000 GT",
        "Coverage: domestic UK voyages and at-berth emissions",
        "Estimated cost: " + _format_gbp(_calculator_value(evidence_pack, "estimated_carbon_cost_per_voyage"), 0) + " per voyage",
        "Annualised estimate: " + _format_gbp(_calculator_value(evidence_pack, "annualised_carbon_cost"), 0),
        "Manual UKA input: " + _format_gbp(_calculator_assumption(evidence_pack, "uka_price_per_tonne"), 0) + "/t",
    ]


def _hormuz_display_facts():
    return [
        "Transit-control mechanism reported: 5 May 2026",
        "War-risk pricing: up to 12x pre-crisis levels",
        "Illustrative tanker premium: about $7.5m at a 3% rate",
        "VLCC rate signal: above $400,000/day",
        "Legal hold trigger: any safe-passage toll or equivalent payment demand",
        "Recovery test: AIS and vessel-flow signals must normalise before conditional transit returns",
    ]


def _critical_minerals_display_facts():
    return [
        "Inventory runway: 45 days",
        "Alternative supplier qualification time: 180 days",
        "Production continuity gap: 135 days",
        "China-linked supply share: 70%",
        "Exposed product-line revenue: £50m illustrative",
        "Substitution difficulty: high",
    ]


def _uk_fiscal_procurement_display_facts(evidence_pack):
    facts = _all_quantified_facts(evidence_pack.get("evidence", []))
    labelled = [
        "Political economy trigger: fiscal credibility, gilt-market sensitivity and departmental budget uncertainty",
        "Commercial channels: public-sector awards, procurement delay, project deferral, repricing and payment-risk monitoring",
        "Company data required: order book, department/customer mix, bid pipeline, payment terms, margins and working-capital exposure",
    ]
    return labelled + facts[:6]


def _calculator_value(evidence_pack, key):
    assumptions = evidence_pack.get("calculator_assumptions", {})
    if not assumptions:
        return 0
    if key == "estimated_carbon_cost_per_voyage":
        return assumptions.get("fuel_consumption_tonnes_per_voyage", 0) * 3.206 * assumptions.get("coverage_rate", 0) * assumptions.get("uka_price_per_tonne", 0)
    if key == "annualised_carbon_cost":
        per_voyage = _calculator_value(evidence_pack, "estimated_carbon_cost_per_voyage")
        return per_voyage * assumptions.get("voyages_per_week", 0) * 4.345 * 12
    return assumptions.get(key, 0)


def _calculator_assumption(evidence_pack, key):
    return evidence_pack.get("calculator_assumptions", {}).get(key, 0)


def _format_gbp(value, decimals):
    amount = float(value or 0)
    if decimals == 0:
        return f"£{amount:,.0f}"
    return f"£{amount:,.{decimals}f}"


def _clean_title(title):
    title = title.replace("[PDF] ", "").replace(":: Lloyd's List", "").replace(" - GOV.UK", "")
    title = title.replace(" | Stephenson Harwood", "").replace(" - International Council on Clean Transportation", " - ICCT")
    return " ".join(title.split())
