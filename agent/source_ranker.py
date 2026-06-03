from datetime import datetime
from urllib.parse import urlparse

TRUSTED_DOMAINS = [
    "ukmto.org",
    "imo.org",
    "maersk.com",
    "hapag-lloyd.com",
    "cma-cgm.com",
    "eia.gov",
    "iea.org",
    "reuters.com",
    "apnews.com",
    "gov.uk",
    "parliament.uk",
    "bgs.ac.uk",
    "oecd.org",
    "usgs.gov",
    "csis.org",
    "rusi.org",
    "css.ethz.ch",
    "hvm.catapult.org.uk",
    "lloydslist.com",
    "gibsons.co.uk",
    "kpler.com",
    "thesignalgroup.com",
    "howdenre.com",
    "spglobal.com",
    "axios.com",
    "ofsi.blog.gov.uk",
    "ofac.treasury.gov",
    "treasury.gov",
    "fca.org.uk",
    "fatf-gafi.org",
    "wolfsberg-principles.com",
    "iccwbo.org",
    "baft.org",
    "ncsc.gov.uk",
    "ico.org.uk",
    "bankofengland.co.uk",
    "marsh.com",
    "aon.com",
    "wtwco.com",
    "allianz.com",
    "howdengroup.com",
]

USEFUL_TERMS = [
    "hormuz",
    "strait",
    "vessel",
    "tanker",
    "transit",
    "war-risk",
    "premium",
    "insurance",
    "lng",
    "oil",
    "freight",
    "sanctions",
    "de-escalation",
    "rare earth",
    "magnet",
    "critical minerals",
    "export control",
    "inventory",
    "qualification",
    "cyber",
    "ransomware",
    "outage",
    "incident response",
    "business interruption",
    "operational resilience",
    "notification",
    "managed service provider",
    "msp",
]

REQUIREMENT_BY_SOURCE_TYPE = {
    "official_primary": ("REQ-A", "official_maritime_security"),
    "company_update": ("REQ-B", "carrier_operational_behaviour"),
    "energy_chokepoint_data": ("REQ-C", "energy_chokepoint_exposure"),
    "insurance_market_evidence": ("REQ-D", "insurance_pricing_reinsurance"),
    "vessel_flow_or_freight_market_evidence": ("REQ-E", "vessel_flow_freight_market"),
    "reputable_news": ("REQ-F", "sanctions_compliance"),
    "specialist_analysis": ("REQ-E", "vessel_flow_freight_market"),
    "sanctions_compliance": ("REQ-F", "sanctions_compliance"),
    "contrary_or_stabilising_evidence": ("REQ-G", "contrary_de_escalation"),
}


def rank_candidate_sources(candidates, topic, categories=None, per_category=1):
    scored = []
    rejected = []
    seen_urls = set()
    for candidate in candidates:
        url = candidate.get("url", "")
        scored_candidate = _scored_candidate(candidate, topic)
        if url and url in seen_urls:
            rejected.append(
                {
                    **scored_candidate,
                    "rejection_reason": "duplicate or near-duplicate",
                    "lowest_scoring_dimension": "independence_score",
                }
            )
            continue
        seen_urls.add(url)
        scored.append((scored_candidate["total_score"], scored_candidate))

    scored.sort(key=lambda item: item[0], reverse=True)
    if not categories:
        return {
            "selected_sources": [_selected(candidate, topic) for _, candidate in scored],
            "rejected_sources": rejected,
            "duplicate_urls_removed": len(rejected),
        }

    selected = []
    selected_urls = set()
    requirement_ids = sorted({candidate.get("requirement_id") for _, candidate in scored if candidate.get("requirement_id")})
    if requirement_ids:
        for requirement_id in requirement_ids:
            matches = [
                candidate for _, candidate in scored
                if candidate.get("requirement_id") == requirement_id and candidate.get("url") not in selected_urls
            ]
            for candidate in matches[:per_category]:
                selected.append(_selected(candidate, topic))
                selected_urls.add(candidate.get("url"))
    else:
        for category in categories:
            matches = [
                candidate for _, candidate in scored
                if candidate.get("source_type") == category and candidate.get("url") not in selected_urls
            ]
            for candidate in matches[:per_category]:
                selected.append(_selected(candidate, topic))
                selected_urls.add(candidate.get("url"))

    selected_url_set = {source.get("url") for source in selected}
    for _, candidate in scored:
        if candidate.get("url") in selected_url_set:
            continue
        rejected.append(_rejected(candidate, topic, categories))

    return {
        "selected_sources": selected,
        "rejected_sources": rejected,
        "duplicate_urls_removed": sum(1 for source in rejected if source.get("rejection_reason") == "duplicate URL"),
    }


def _selected(candidate, topic):
    return {
        **candidate,
        "selection_reason": _selection_reason(candidate, topic),
        "evidence_value": _evidence_value(candidate),
        "source_role": _source_role(candidate),
        "source_value_explanation": _source_value_explanation(candidate),
        "decision_use": _decision_use(candidate),
    }


def _rejected(candidate, topic, categories):
    reason = "stronger source already selected for the same requirement"
    if candidate.get("reliability_score", 1) <= 2:
        reason = "low reliability"
    elif candidate.get("source_type") not in categories:
        reason = "weak source requirement fit"
    elif candidate.get("relevance_score", 1) <= 2:
        reason = "weak relevance"
    elif candidate.get("recency_score", 1) <= 2:
        reason = "stale source"
    elif candidate.get("specificity_score", 1) <= 2:
        reason = "low specificity"

    return {
        **candidate,
        "rejection_reason": reason,
        "lowest_scoring_dimension": _lowest_scoring_dimension(candidate),
    }


def _selection_reason(candidate, topic):
    reasons = []
    if _trusted_domain(candidate.get("url", "")):
        reasons.append("trusted domain")
    if any(token in " ".join([candidate.get("title", ""), candidate.get("snippet", "")]).lower() for token in topic.lower().split()):
        reasons.append("direct topic match")
    if candidate.get("source_type"):
        reasons.append(f"fits {candidate['source_type']}")
    if _is_recent(candidate.get("publication_date", "")):
        reasons.append("recent source")
    return ", ".join(reasons) or "selected as best available category match"


def _evidence_value(candidate):
    source_type = candidate.get("source_type", "unknown")
    values = {
        "official_primary": "Primary safety and security baseline.",
        "company_update": "Operational signal from market participant.",
        "energy_chokepoint_data": "Structural impact evidence for oil and LNG exposure.",
        "insurance_market_evidence": "Direct pricing and underwriting signal.",
        "vessel_flow_or_freight_market_evidence": "Market behaviour and flow signal.",
        "reputable_news": "Corroborating current-events evidence.",
        "specialist_analysis": "Scenario and market interpretation.",
        "contrary_or_stabilising_evidence": "Balances downside case and confidence.",
    }
    return values.get(source_type, "Supporting context.")


def _decision_use(candidate):
    requirement_name = candidate.get("requirement_name", "")
    requirement_uses = {
        "official_maritime_security": "Supports transit approval thresholds and tests whether official guidance still justifies enhanced controls.",
        "transit_control_or_constabulary_actions": "Supports the transit versus delay versus reroute decision by showing whether direct passage remains operationally acceptable.",
        "sanctions_and_safe_passage_payment_risk": "Supports legal-hold escalation if tolls, safe-passage payments, offsets, swaps, guarantees or in-kind demands appear.",
        "war_risk_insurance_pricing": "Supports insurance viability checks and the break-even comparison between direct transit and reroute.",
        "vessel_flow_and_AIS_behaviour": "Supports whether AIS and vessel-flow signals justify continued controls or conditional relaxation.",
        "energy_cargo_and_chokepoint_exposure": "Supports impact severity and client communication on why Hormuz route decisions matter commercially.",
        "route_cost_and_arbitrage_inputs": "Supports direct transit, delay and reroute cost comparison after insurance and hold costs are included.",
        "contrary_or_de_escalation_evidence": "Supports the evidence threshold for moving from hold or reroute back to conditional transit.",
        "uk_critical_minerals_policy_and_manufacturing_resilience": "Supports the UK manufacturing-resilience baseline and explains why the case is decision-relevant for a UK advanced manufacturer.",
        "export_control_direction_and_live_trigger": "Supports whether export-control direction or live policy triggers justify heightened procurement controls.",
        "rare_earth_magnet_or_controlled_input_classification": "Supports identifying which exact input or subcomponent is exposed before action is taken.",
        "supply_concentration_and_dependency_data": "Supports concentration scoring and whether the current supplier base is too dependency-heavy to leave unchanged.",
        "uk_industry_exposure_and_advanced_manufacturing_relevance": "Supports why the issue matters to UK production continuity, customer delivery and management escalation.",
        "substitution_feasibility_and_alternative_supplier_qualification": "Supports whether the preferred response is qualification, redesign or eventual production hold.",
        "market_pricing_or_shortage_signal": "Supports stockpile, allocation and accelerated sourcing decisions when shortage signals tighten.",
        "contrary_or_easing_evidence": "Supports the threshold for relaxing a high-control sourcing stance back toward normal procurement.",
        "company_data_requirements_and_anti_overclaiming_controls": "Supports anti-overclaiming controls by showing which company facts are still required before operational decisions.",
        "uk_sanctions_ofsi_official_guidance": "Anchors UK sanctions/OFSI relevance and the approve, escalate, legal-hold or reject decision frame.",
        "sanctions_end_use_controls_and_controlled_goods_risk": "Supports goods, technology, end-use and licence checks before approval or drawdown.",
        "counterparty_and_ownership_exposure": "Supports counterparty, beneficial ownership, intermediary, bank, vessel and consignee screening decisions.",
        "jurisdiction_route_and_diversion_exposure": "Supports escalation where jurisdiction, route, transshipment or diversion indicators are unresolved.",
        "documentation_and_transaction_quality_evidence": "Supports document-request and hold triggers for invoices, bills of lading, end-use statements and payment instructions.",
        "enforcement_penalty_and_regulatory_expectations": "Supports legal-hold and rejection thresholds by showing regulatory consequences and expected controls.",
        "financial_institution_trade_finance_operating_impact": "Supports facility conditions, drawdown controls, credit exposure review and operational escalation.",
        "contrary_clearance_or_de_escalation_evidence": "Supports approval or enhanced due diligence only where clean counterparties, licences, exemptions and documents resolve red flags.",
        "sanctions_company_data_requirements_and_anti_overclaiming_controls": "Supports anti-overclaiming controls by showing the transaction data still required before clearance.",
        "uk_official_cyber_threat_ncsc_evidence": "Anchors the UK cyber threat and ransomware environment for business-interruption likelihood scoring.",
        "uk_cyber_breach_prevalence_data": "Supports likelihood scoring by quantifying cyber incident and breach prevalence among UK organisations.",
        "board_cyber_governance_and_resilience_expectations": "Supports board, CFO/COO and risk-manager escalation for operational resilience readiness.",
        "ransomware_or_operational_disruption_evidence": "Supports incident-response, manual contingency and restoration-priority decisions where cyber events cause downtime.",
        "cyber_insurance_business_interruption_evidence": "Supports claim-notice, waiting-period, coverage and policy-wording review before relying on insurance recovery.",
        "incident_reporting_and_regulatory_notification_guidance": "Supports ICO, sector-regulator and affected-customer notification review triggers.",
        "supplier_msp_dependency_risk": "Supports supplier, MSP, cloud, payment or fulfilment escalation where third-party recovery blocks operations.",
        "contrary_or_mitigation_evidence": "Supports the evidence threshold for reducing controls when resilience, recovery or mitigation evidence is strong.",
        "cyber_company_data_requirements_and_anti_overclaiming_controls": "Supports anti-overclaiming controls by showing which systems, revenue, policy and recovery data is still required.",
    }
    if requirement_name in requirement_uses:
        return requirement_uses[requirement_name]

    source_type = candidate.get("source_type", "unknown")
    uses = {
        "official_primary": "Supports enhanced referral and route-level controls.",
        "company_update": "Informs whether transit controls should remain enhanced.",
        "energy_chokepoint_data": "Supports severe impact scoring and accumulation stress testing.",
        "insurance_market_evidence": "Supports pricing review, referral thresholds and capacity check.",
        "vessel_flow_or_freight_market_evidence": "Supports immediacy scoring and relaxation triggers.",
        "reputable_news": "Corroborates current conditions and management escalation needs.",
        "specialist_analysis": "Supports scenario framing and market interpretation.",
        "contrary_or_stabilising_evidence": "Informs relaxation triggers without automatically reducing controls.",
    }
    return uses.get(source_type, "Supports analyst judgement and review controls.")


def _source_role(candidate):
    requirement_name = candidate.get("requirement_name", "")
    mapping = {
        "official_maritime_security": "official_anchor",
        "transit_control_or_constabulary_actions": "live_event_reporting",
        "sanctions_and_safe_passage_payment_risk": "sanctions_legal_guidance",
        "war_risk_insurance_pricing": "insurance_market_evidence",
        "vessel_flow_and_AIS_behaviour": "vessel_flow_or_AIS_data",
        "energy_cargo_and_chokepoint_exposure": "energy_chokepoint_data",
        "route_cost_and_arbitrage_inputs": "operator_or_industry_guidance",
        "contrary_or_de_escalation_evidence": "contrary_or_de_escalation_evidence",
        "uk_critical_minerals_policy_and_manufacturing_resilience": "official_anchor",
        "export_control_direction_and_live_trigger": "live_event_reporting",
        "rare_earth_magnet_or_controlled_input_classification": "data_or_indicator_source",
        "supply_concentration_and_dependency_data": "data_or_indicator_source",
        "uk_industry_exposure_and_advanced_manufacturing_relevance": "operator_or_industry_guidance",
        "substitution_feasibility_and_alternative_supplier_qualification": "specialist_interpretation",
        "market_pricing_or_shortage_signal": "market_pricing",
        "contrary_or_easing_evidence": "contrary_scope_limit",
        "company_data_requirements_and_anti_overclaiming_controls": "specialist_interpretation",
        "uk_sanctions_ofsi_official_guidance": "official_anchor",
        "sanctions_end_use_controls_and_controlled_goods_risk": "regulatory_guidance",
        "counterparty_and_ownership_exposure": "regulatory_guidance",
        "jurisdiction_route_and_diversion_exposure": "live_event_reporting",
        "documentation_and_transaction_quality_evidence": "financial_sector_guidance",
        "enforcement_penalty_and_regulatory_expectations": "enforcement_evidence",
        "financial_institution_trade_finance_operating_impact": "financial_sector_guidance",
        "contrary_clearance_or_de_escalation_evidence": "contrary_scope_limit",
        "sanctions_company_data_requirements_and_anti_overclaiming_controls": "company_required_data",
        "uk_official_cyber_threat_ncsc_evidence": "official_anchor",
        "uk_cyber_breach_prevalence_data": "data_or_indicator_source",
        "board_cyber_governance_and_resilience_expectations": "regulatory_guidance",
        "ransomware_or_operational_disruption_evidence": "live_event_reporting",
        "cyber_insurance_business_interruption_evidence": "insurance_market_evidence",
        "incident_reporting_and_regulatory_notification_guidance": "regulatory_guidance",
        "supplier_msp_dependency_risk": "specialist_interpretation",
        "contrary_or_mitigation_evidence": "contrary_scope_limit",
        "cyber_company_data_requirements_and_anti_overclaiming_controls": "company_required_data",
    }
    return mapping.get(requirement_name, candidate.get("source_type", "unknown"))


def _source_value_explanation(candidate):
    role = _source_role(candidate)
    explanations = {
        "official_anchor": "Anchors whether official guidance still supports transit or requires enhanced warning or restriction.",
        "live_event_reporting": "Shows whether direct passage remains disrupted through detentions, coordination demands or live transit controls.",
        "sanctions_legal_guidance": "Explains when safe-passage demands turn into legal/compliance hold triggers.",
        "insurance_market_evidence": "Shows whether war-risk cover is available and when premium pressure makes reroute economically preferable.",
        "vessel_flow_or_AIS_data": "Shows whether AIS and vessel-flow behaviour support normalisation or continued stress.",
        "energy_chokepoint_data": "Quantifies why a Hormuz routing decision matters for cargo, customer and timing exposure.",
        "operator_or_industry_guidance": "Translates the disruption into operator-facing route-cost, delay and pass-through decisions.",
        "contrary_or_de_escalation_evidence": "Tests whether there is enough practical recovery evidence to relax from hold or reroute to conditional transit.",
        "data_or_indicator_source": "Quantifies concentration, dependency and controlled-input exposure needed for continuity decisions.",
        "operator_or_industry_guidance": "Shows how UK advanced manufacturers are exposed in practice and where delivery pressure may appear first.",
        "specialist_interpretation": "Explains qualification lag, substitution limits and the company-data conditions for using the model responsibly.",
        "market_pricing": "Shows whether scarcity or pricing pressure is strong enough to justify stockpile, allocation or accelerated sourcing action.",
        "contrary_scope_limit": "Tests whether easing, alternative supply or licence clarification narrows the need for severe mitigation action.",
        "regulatory_guidance": "Explains regulatory controls that turn goods, end-use, ownership or payment red flags into escalation or hold decisions.",
        "enforcement_evidence": "Shows regulatory consequences and control expectations when sanctions checks fail.",
        "financial_sector_guidance": "Translates sanctions exposure into trade-finance document, payment, drawdown and facility controls.",
        "company_required_data": "Identifies transaction-specific data needed before a lender can move from exposure screen to clearance decision.",
        "official_anchor": "Anchors the official threat, policy or regulatory baseline for the client decision.",
        "regulatory_guidance": "Shows notification, governance or resilience expectations that convert cyber disruption into management action.",
        "live_event_reporting": "Shows whether cyber incidents are causing live downtime, customer harm or recovery pressure.",
        "insurance_market_evidence": "Shows claim, coverage, waiting-period, exclusion or market evidence relevant to insurance response.",
        "data_or_indicator_source": "Quantifies threat prevalence, outage exposure or other indicators needed for scoring.",
        "contrary_scope_limit": "Identifies mitigation, recovery or resilience evidence that prevents overstating the downside case.",
    }
    return explanations.get(role, _evidence_value(candidate))


def _scored_candidate(candidate, topic):
    scores = {
        "reliability_score": _reliability_score(candidate),
        "relevance_score": _relevance_score(candidate, topic),
        "recency_score": _recency_score(candidate),
        "specificity_score": _specificity_score(candidate),
        "decision_value_score": _decision_value_score(candidate),
        "independence_score": 5,
        "contrary_value_score": _contrary_value_score(candidate),
    }
    total_score = sum(scores.values())
    requirement_id, requirement_name = _requirement_for(candidate.get("source_type", "unknown"))
    return {
        **candidate,
        **scores,
        "requirement_id": candidate.get("requirement_id", requirement_id),
        "requirement_name": candidate.get("requirement_name", requirement_name),
        "total_score": total_score,
        "ranking_score": total_score,
        "evidence_weight": _evidence_weight(total_score),
    }


def _requirement_for(source_type):
    return REQUIREMENT_BY_SOURCE_TYPE.get(source_type, ("", ""))


def _score(candidate, topic):
    return _scored_candidate(candidate, topic)["total_score"]


def _reliability_score(candidate):
    source_type = candidate.get("source_type", "unknown")
    domain = urlparse(candidate.get("url", "")).netloc.lower()
    if any(term in domain for term in ["facebook.com", "linkedin.com", "x.com", "twitter.com", "instagram.com"]):
        return 1
    trusted = _trusted_domain(candidate.get("url", ""))
    if source_type in {"official_primary", "company_update", "energy_chokepoint_data", "insurance_market_evidence"}:
        return 5 if trusted else 4
    if source_type in {"vessel_flow_or_freight_market_evidence", "specialist_analysis", "reputable_news", "contrary_or_stabilising_evidence"}:
        return 4 if trusted else 3
    if trusted:
        return 3
    return 2


def _relevance_score(candidate, topic):
    text = _candidate_text(candidate)
    tokens = [token for token in topic.lower().split() if len(token) > 3]
    matches = sum(1 for token in tokens if token in text)
    if matches >= 2:
        return 5
    if matches == 1 or candidate.get("source_type"):
        return 4
    if any(term in text for term in USEFUL_TERMS):
        return 3
    return 2


def _recency_score(candidate):
    date_value = candidate.get("publication_date", "")
    if not date_value:
        return 3
    try:
        publication_date = datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        return 2
    age_days = (datetime.now().date() - publication_date).days
    if age_days <= 30:
        return 5
    if age_days <= 90:
        return 4
    if age_days <= 180:
        return 3
    return 2


def _specificity_score(candidate):
    text = _candidate_text(candidate)
    signals = 0
    signals += 1 if any(term in text for term in ROUTE_SIGNAL_TERMS) else 0
    signals += 1 if any(term in text for term in INSURANCE_SIGNAL_TERMS) else 0
    signals += 1 if any(term in text for term in VESSEL_SIGNAL_TERMS) else 0
    signals += 1 if any(char.isdigit() for char in text) else 0
    signals += 1 if any(term in text for term in ["premium", "rate", "percent", "%", "barrels", "lng", "cargo", "outage", "ransomware", "incident", "72 hours"]) else 0
    return min(5, max(2, signals + 1))


def _decision_value_score(candidate):
    text = _candidate_text(candidate)
    decision_terms = [
        "stance", "pricing", "premium", "referral", "aggregation", "wording",
        "sanctions", "reinsurance", "capacity", "route", "transit", "relax",
        "reopen", "de-escalation", "operations",
        "outage", "incident", "notification", "claim", "resilience", "downtime",
        "recovery", "ransomware", "manual", "supplier", "msp",
    ]
    matches = sum(1 for term in decision_terms if term in text)
    if candidate.get("source_type") in {"official_primary", "insurance_market_evidence", "company_update"}:
        matches += 2
    return min(5, max(2, matches))


def _contrary_value_score(candidate):
    if candidate.get("source_type") == "contrary_or_stabilising_evidence":
        return 5
    text = _candidate_text(candidate)
    if any(term in text for term in ["de-escalation", "reopen", "restored", "normalisation", "normalization"]):
        return 4
    return 1


ROUTE_SIGNAL_TERMS = ["hormuz", "strait", "gulf", "route", "waterway", "chokepoint"]
INSURANCE_SIGNAL_TERMS = ["insurance", "war-risk", "war risk", "premium", "reinsurance", "underwriting"]
VESSEL_SIGNAL_TERMS = ["vessel", "tanker", "traffic", "transit", "flows", "freight", "shipping"]


def _candidate_text(candidate):
    return " ".join([candidate.get("title", ""), candidate.get("snippet", ""), candidate.get("claim_supported", "")]).lower()


def _evidence_weight(total_score):
    if total_score >= 28:
        return "high"
    if total_score >= 20:
        return "medium"
    return "low"


def _lowest_scoring_dimension(candidate):
    dimensions = [
        "reliability_score",
        "relevance_score",
        "recency_score",
        "specificity_score",
        "decision_value_score",
        "independence_score",
    ]
    return min(dimensions, key=lambda name: candidate.get(name, 0))


def _legacy_score(candidate, topic):
    text = " ".join([candidate.get("title", ""), candidate.get("snippet", "")]).lower()
    score = 0

    for token in topic.lower().split():
        if token in text:
            score += 2
    if _trusted_domain(candidate.get("url", "")):
        score += 5
    if candidate.get("source_type"):
        score += 2
    if _is_recent(candidate.get("publication_date", "")):
        score += 2
    score += sum(1 for term in USEFUL_TERMS if term in text)

    return score


def _trusted_domain(url):
    domain = urlparse(url).netloc.lower().replace("www.", "")
    return any(domain == trusted or domain.endswith("." + trusted) for trusted in TRUSTED_DOMAINS)


def _is_recent(date_value):
    if not date_value:
        return False
    try:
        publication_date = datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        return False
    return (datetime.now().date() - publication_date).days <= 90
