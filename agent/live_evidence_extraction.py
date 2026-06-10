import re
from datetime import datetime
from urllib.parse import urlparse

from agent.core.provenance import normalize_evidence_record


INSURANCE_TERMS = ["insurance", "war-risk", "war risk", "premium", "underwriting", "claims"]
VESSEL_FLOW_TERMS = ["vessel", "tanker", "traffic", "transit", "flows", "freight", "shipping"]
ROUTE_TERMS = ["strait of hormuz", "persian gulf", "gulf", "waterway", "chokepoint"]
CARRIER_TERMS = ["route", "routing", "service", "operations", "transit", "security review"]
DEESCALATION_TERMS = [
    "de-escalation",
    "deescalation",
    "reopen",
    "reopening",
    "restored",
    "reduced near-term disruption",
    "stabilising",
    "stabilizing",
]


from agent.cases.registry import normalize_business_user


def extract_live_evidence(fetched_sources, business_user):
    business_user = normalize_business_user(business_user)
    return [
        _extract_source(source, index + 1, business_user)
        for index, source in enumerate(fetched_sources)
    ]


def _extract_source(source, index, business_user):
    body_text = source.get("content") or source.get("claim_supported") or source.get("snippet", "")
    body_text = _clean_extracted_text(body_text)
    text = " ".join([source.get("title", ""), body_text])
    lower_text = text.lower()
    source_type = source.get("source_type", "unknown")
    contrary_signal = any(term in lower_text for term in DEESCALATION_TERMS)
    claim_supported = _best_claim(source, body_text or text)
    requirement_name = source.get("requirement_name", "")
    decision_profile = _decision_profile(requirement_name, source_type, business_user)

    evidence = {
        "source_id": source.get("source_id", f"L{index}"),
        "requirement_id": source.get("requirement_id", ""),
        "requirement_name": requirement_name,
        "title": source.get("title", ""),
        "publisher": source.get("publisher") or _publisher_from_url(source.get("url", "")),
        "url": source.get("url", ""),
        "publication_date": source.get("publication_date", ""),
        "retrieval_date": datetime.now().date().isoformat(),
        "source_type": source_type,
        "date": source.get("publication_date", ""),
        "summary": claim_supported,
        "evidence_label": source_type.replace("_", " ").title(),
        "extracted_claim": claim_supported,
        "claim_supported": claim_supported,
        "supporting_detail": _supporting_detail(source, text),
        "quantified_facts": _quantified_facts(text),
        "key_facts": _key_facts(text),
        "commercial_relevance": source.get("commercial_relevance") or decision_profile["commercial_meaning"],
        "commercial_meaning": decision_profile["commercial_meaning"],
        "business_user_relevance": decision_profile["business_user_implication"],
        "business_user_implication": decision_profile["business_user_implication"],
        "marine_insurance_implication": _marine_insurance_implication(source_type),
        "risk_dimension": _risk_dimension(lower_text, source_type),
        "risk_driver": _risk_driver(requirement_name, source_type),
        "judgement_supported": _judgement_supported(requirement_name, source_type),
        "decision_use": decision_profile["decision_use"] if requirement_name else source.get("decision_use") or decision_profile["decision_use"],
        "contrary_signal": contrary_signal,
        "confidence_impact": _confidence_impact(source_type, contrary_signal),
        "caveat": source.get("caveat") or _caveat(source_type, source.get("fetch_status", "")),
        "refresh_requirement": _refresh_requirement(requirement_name, source_type),
        "evidence_weight": source.get("evidence_weight", "medium"),
        "reliability_score": source.get("reliability_score", ""),
        "relevance_score": source.get("relevance_score", ""),
        "recency_score": source.get("recency_score", ""),
        "specificity_score": source.get("specificity_score", ""),
        "decision_value_score": source.get("decision_value_score", ""),
        "fetch_status": source.get("fetch_status", ""),
    }
    return normalize_evidence_record(
        evidence,
        source=source,
        fallback_demo_data_used=source.get("evidence_source_mode") == "fallback" or source.get("fetch_status") == "demo",
        retrieval_timestamp=source.get("retrieval_timestamp"),
    )


def _claim_supported(text):
    sentence = re.split(r"(?<=[.!?])\s+", text.strip())[0]
    return sentence[:500] if sentence else "No concise claim extracted."


def _best_claim(source, text):
    cleaned = _clean_extracted_text(text)
    if _looks_like_bad_claim(cleaned):
        snippet = _clean_extracted_text(source.get("snippet", ""))
        if snippet and not _looks_like_bad_claim(snippet):
            source["fetch_status"] = "snippet_used"
            return _claim_supported(snippet)
        claim_supported = _clean_extracted_text(source.get("claim_supported", ""))
        if claim_supported and not _looks_like_bad_claim(claim_supported):
            source["fetch_status"] = "snippet_used"
            return _claim_supported(claim_supported)
    return _claim_supported(cleaned)


def _clean_extracted_text(text):
    text = re.sub(r"(?is)<(script|style|nav|footer|header|noscript|form|aside)\b.*?</\1>", " ", text or "")
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\b(cookie|cookies|privacy policy|accept all|skip to content|on GOV\.UK)\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bWe (use|would like to set) (some )?(essential|necessary|additional)?\s*(cookies?)?.{0,120}?(website work|site work|government services|settings)\.?", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bOur use of\s+We use necessary to make our site work\.?", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(function|var|return|data-[a-z0-9_-]+)\b.*", " ", text, flags=re.IGNORECASE)
    text = " ".join(text.split())
    return text[:5000]


def _looks_like_bad_claim(text):
    if not text or len(text.strip()) < 25:
        return True
    lowered = text.strip().lower()
    bad_prefixes = ("<script", "<!doctype", "<html", "data-", "var", "function", "cookie")
    if lowered.startswith(bad_prefixes):
        return True
    if any(token in lowered for token in ["<!doctype", "<html", "<script", "javascript", "window.datalayer", "we use some essential", "we use necessary", "we'd like to set additional cookies", "our use of we use necessary"]):
        return True
    return False


def _key_facts(text):
    facts = []
    facts.extend(re.findall(r"(?<!\w)\d+(?:\.\d+)?%?", text))
    facts.extend(term for term in ROUTE_TERMS if term in text.lower())
    facts.extend(term for term in INSURANCE_TERMS if term in text.lower())
    facts.extend(term for term in VESSEL_FLOW_TERMS if term in text.lower())
    return sorted(set(facts))[:12]


def _quantified_facts(text):
    patterns = [
        r"\b\d+(?:\.\d+)?\s?%",
        r"(?:\$|£|€)\s?\d+(?:\.\d+)?\s?(?:m|mn|million|bn|billion)?",
        r"\b\d+(?:\.\d+)?\s?(?:m|mn|million|bn|billion)\b",
        r"\b\d+(?:\.\d+)?\s?(?:mb/d|b/d|barrels per day|barrels|vessels|seafarers|tankers|ships)\b",
        r"\b\d+(?:\.\d+)?\s?(?:LNG|oil|crude|cargo|transit|transits)\b",
        r"\b\d+(?:\.\d+)?\s?(?:basis points|bps|premium|premiums|rate|rates)\b",
        r"\b\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b(?:13 May 2026|22 April 2026|1-3 months)\b",
        r"\b(?:licen[cs]e|notification|penalt(?:y|ies)|payment|collateral)\s.{0,40}?\d+(?:\.\d+)?%?",
        r"\b(?:borrowing|debt|debt interest|gilt yield|gilts|spending|capital budget|procurement|infrastructure)\s.{0,60}?(?:\$|£|€)?\d+(?:\.\d+)?\s?(?:%|m|mn|million|bn|billion)?",
    ]
    facts = []
    for pattern in patterns:
        facts.extend(match.strip() for match in re.findall(pattern, text, flags=re.IGNORECASE))
    facts.extend(re.findall(r"(?<!\w)\d+(?:\.\d+)?%?", text))
    return sorted(set(facts), key=lambda item: text.lower().find(item.lower()))[:20]


def _supporting_detail(source, text):
    key_facts = source.get("key_facts") or _key_facts(text)
    if key_facts:
        return "Key facts: " + "; ".join(str(fact) for fact in key_facts[:5])
    return "No discrete supporting detail extracted beyond the claim summary."


def _commercial_relevance(text, source_type):
    if source_type == "contrary_or_stabilising_evidence":
        return "Scenario balance and de-escalation monitoring."
    if any(term in text for term in INSURANCE_TERMS):
        return "Insurance pricing, claims aggregation, and underwriting exposure."
    if any(term in text for term in ["oil", "lng", "energy", "chokepoint"]):
        return "Energy tanker and commodity supply-chain exposure."
    if any(term in text for term in VESSEL_FLOW_TERMS):
        return "Vessel flow, freight, and transit disruption exposure."
    return "Relevant evidence for analyst review."


def _business_user_relevance(business_user, text):
    business_user = normalize_business_user(business_user)
    if business_user == "infrastructure_contractor":
        return "Relevant to public-sector bid pipeline, contract-award timing, payment risk, repricing assumptions, working-capital exposure and board monitoring."
    if business_user == "customer_facing_operator":
        return "Relevant to downtime tolerance, revenue-at-risk, regulatory notification, customer harm, insurance claim readiness and recovery controls."
    if business_user == "marine_insurer":
        return "Relevant to war-risk pricing, accumulation control, policy wording, and claims scenarios."
    if business_user == "shipping_operator":
        return "Relevant to routing, vessel security, crew safety, and customer commitments."
    if business_user == "advanced_manufacturer":
        return "Relevant to production continuity, supplier concentration, inventory runway, qualification lag and customer delivery commitments."
    if business_user == "trade_finance_lender":
        return "Relevant to counterparty, sanctions, cargo documentation, and collateral risk."
    return "Relevant to this user's exposure mapping and risk brief."


def _marine_insurance_implication(source_type):
    implications = {
        "insurance_market_evidence": "Maps to premium adequacy, reinsurance appetite, underwriting controls and claims aggregation.",
        "energy_chokepoint_data": "Maps to tanker exposure, cargo values, LNG/oil disruption and accumulation risk.",
        "company_update": "Maps to routing, service continuity, trapped vessel and cargo delay risk.",
        "official_primary": "Maps to vessel security, safe transit, crew welfare and route approval.",
        "vessel_flow_or_freight_market_evidence": "Maps to transit recovery, floating storage, congestion and accumulation.",
        "contrary_or_stabilising_evidence": "Maps to scenario balance and conditions for relaxing controls.",
        "reputable_news": "Corroborates operational disruption, insurance stress and management attention.",
        "specialist_analysis": "Supports scenario design, market interpretation and stress testing.",
    }
    return implications.get(source_type, "Supports analyst review of relevant insurance exposure.")


def _confidence_impact(source_type, contrary_signal):
    if contrary_signal or source_type == "contrary_or_stabilising_evidence":
        return "adds scenario balance but caps certainty"
    if source_type == "unknown":
        return "limited confidence impact"
    return "raises confidence through source diversity"


def _risk_dimension(text, source_type):
    if any(term in text for term in INSURANCE_TERMS):
        return "impact"
    if any(term in text for term in DEESCALATION_TERMS):
        return "confidence"
    if source_type == "official_primary":
        return "likelihood"
    return "commercial exposure"


def _caveat(source_type, fetch_status):
    if fetch_status == "failed":
        return "Fetch failed; evidence uses search snippet only."
    if source_type == "contrary_or_stabilising_evidence":
        return "Stabilising signal should be checked against newer escalation indicators."
    return "Rule-based extraction; analyst should verify facts and context."


def _decision_profile(requirement_name, source_type, business_user):
    business_user = normalize_business_user(business_user)
    if business_user == "infrastructure_contractor" or requirement_name.startswith(("obr_", "ons_", "hm_treasury", "bank_of_england", "credible_market_analysis", "public_procurement", "contractor_industry", "contrary_or_stabilising_fiscal", "company_data_requirements_for_contractor")):
        return _uk_fiscal_procurement_decision_profile(requirement_name, source_type)
    if business_user == "customer_facing_operator" or requirement_name.startswith("uk_official_cyber") or requirement_name.startswith("cyber_") or requirement_name in {
        "uk_cyber_breach_prevalence_data",
        "board_cyber_governance_and_resilience_expectations",
        "ransomware_or_operational_disruption_evidence",
        "incident_reporting_and_regulatory_notification_guidance",
        "supplier_msp_dependency_risk",
        "contrary_or_mitigation_evidence",
    }:
        return _cyber_business_interruption_decision_profile(requirement_name, source_type)
    if business_user == "advanced_manufacturer":
        return _advanced_manufacturer_decision_profile(requirement_name, source_type)
    if business_user == "trade_finance_lender":
        return _trade_finance_decision_profile(requirement_name, source_type)
    if _is_uk_ets_requirement(requirement_name):
        return _uk_ets_shipping_operator_decision_profile(requirement_name, source_type)
    if business_user == "shipping_operator":
        return _shipping_operator_decision_profile(requirement_name, source_type)
    if business_user != "marine_insurer":
        return {
            "commercial_meaning": _commercial_relevance("", source_type),
            "business_user_implication": _business_user_relevance(business_user, ""),
            "decision_use": "Supports exposure review, control adjustment and monitoring triggers.",
        }

    profiles = {
        "official_maritime_security": (
            "Safe passage uncertainty, crew welfare, route approval and live transit risk.",
            "Hull war controls, liability exposure, claims preparedness and voyage approval.",
            "Supports enhanced referral and route-level controls.",
        ),
        "carrier_operational_behaviour": (
            "Operator risk appetite and practical service constraints.",
            "Trapped vessel, delay, deviation and cargo accumulation risk.",
            "Informs whether transit controls should remain enhanced.",
        ),
        "energy_chokepoint_exposure": (
            "Structural exposure across oil, LNG, tanker demand and cargo values.",
            "Severe impact rating and accumulation stress testing.",
            "Supports severe impact scoring even where transit partially resumes.",
        ),
        "insurance_pricing_reinsurance": (
            "Pricing and reinsurance markets have repriced route risk.",
            "Premium adequacy, limits, deductibles, reinsurance appetite and referral thresholds.",
            "Supports pricing review and capacity check.",
        ),
        "vessel_flow_freight_market": (
            "Vessel behaviour shows operational normalisation or continuing friction.",
            "Floating cargo, trapped vessels, congestion and accumulation exposure.",
            "Supports immediacy score and relaxation triggers.",
        ),
        "sanctions_compliance": (
            "Counterparty, cargo, vessel control and payment risk can affect coverage and claims.",
            "Sanctions exclusions, legal review, claims uncertainty and referral controls.",
            "Supports compliance escalation and wording review.",
        ),
        "contrary_de_escalation": (
            "Credible stabilising evidence defines conditions under which disruption may ease.",
            "Prevents excessive downside bias while preserving controls.",
            "Informs relaxation triggers without automatically reducing controls.",
        ),
    }
    commercial, implication, decision = profiles.get(
        requirement_name,
        (_commercial_relevance("", source_type), _marine_insurance_implication(source_type), "Supports analyst review and decision controls."),
    )
    return {
        "commercial_meaning": commercial,
        "business_user_implication": implication,
        "decision_use": decision,
    }


def _advanced_manufacturer_decision_profile(requirement_name, source_type):
    profiles = {
        "uk_critical_minerals_policy_and_manufacturing_resilience": (
            "UK policy and resilience framing shows why critical-mineral disruption matters for production continuity rather than only industrial strategy.",
            "Supports management escalation and board-level framing for UK manufacturing resilience.",
            "Supports the UK decision context for stockpile, qualification and redesign discussions.",
        ),
        "export_control_direction_and_live_trigger": (
            "Live export-control direction can turn concentration exposure into immediate procurement disruption.",
            "Supports deciding whether the current supplier base is still commercially acceptable.",
            "Supports trigger-based escalation from normal procurement to heightened sourcing controls.",
        ),
        "rare_earth_magnet_or_controlled_input_classification": (
            "Controlled-input identification prevents the case from drifting into generic critical-minerals commentary.",
            "Supports BOM-level scoping of which product lines are genuinely exposed.",
            "Supports confirming whether the at-risk item is a magnet, oxide, alloy or dependent subassembly before mitigation is chosen.",
        ),
        "supply_concentration_and_dependency_data": (
            "Concentration and dependency data show whether supply risk is structural rather than incidental.",
            "Supports whether dual-source qualification should be accelerated.",
            "Supports concentration scoring and continuity-gap severity assessment.",
        ),
        "uk_industry_exposure_and_advanced_manufacturing_relevance": (
            "UK industry exposure evidence connects global rare-earth risk to domestic production continuity and delivery risk.",
            "Supports whether management should treat the issue as a live manufacturing-control problem.",
            "Supports customer-priority, allocation and continuity planning decisions.",
        ),
        "substitution_feasibility_and_alternative_supplier_qualification": (
            "Qualification and substitution evidence determine whether redesign or alternative sourcing is realistic before inventory runs out.",
            "Supports engineering, procurement and quality review of the mitigation path.",
            "Supports whether the preferred action is qualify alternative supplier, redesign input or prepare for hold.",
        ),
        "market_pricing_or_shortage_signal": (
            "Shortage and price signals show whether scarcity pressure is tightening beyond background concentration risk.",
            "Supports timing of stockpile or allocation decisions.",
            "Supports stockpile and procurement acceleration decisions where shortage signals intensify.",
        ),
        "contrary_or_easing_evidence": (
            "Easing evidence helps prevent one-way escalation where licences, supply expansion or alternative routes improve the picture.",
            "Supports relaxing controls only when the operational evidence genuinely improves.",
            "Supports the threshold for stepping back from stockpile, allocation or hold recommendations.",
        ),
        "company_data_requirements_and_anti_overclaiming_controls": (
            "Public evidence can screen exposure, but company data determines whether the recommendation is operationally valid.",
            "Supports anti-overclaiming controls across BOM, inventory, suppliers and delivery commitments.",
            "Supports stating what company-specific information is required before using the model commercially.",
        ),
    }
    commercial, implication, decision = profiles.get(
        requirement_name,
        (_commercial_relevance("", source_type), _business_user_relevance("advanced_manufacturer", ""), "Supports production-continuity review and sourcing control decisions."),
    )
    return {
        "commercial_meaning": commercial,
        "business_user_implication": implication,
        "decision_use": decision,
    }

def _uk_fiscal_procurement_decision_profile(requirement_name, source_type):
    profiles = {
        "obr_fiscal_outlook_and_fiscal_risks": (
            "Fiscal headroom, borrowing and debt-interest constraints can weaken confidence in public spending commitments.",
            "Supports bid-pipeline review and board monitoring of public-sector exposure.",
            "Supports likelihood scoring for continued fiscal pressure and departmental budget uncertainty.",
        ),
        "ons_public_finances_data": (
            "Official borrowing, debt and debt-interest data grounds the fiscal-pressure baseline.",
            "Supports payment-risk and procurement-confidence monitoring using official public-finance indicators.",
            "Supports evidence-backed monitoring of fiscal deterioration or stabilisation.",
        ),
        "hm_treasury_fiscal_policy_and_spending_control": (
            "Fiscal rules, spending controls and departmental budgets shape public-sector contract-award confidence.",
            "Supports bid/no-bid review, contract-pricing assumptions and programme-delay contingency planning.",
            "Supports assessment of whether spending constraints may affect awards, deferrals or repricing.",
        ),
        "bank_of_england_gilt_market_and_financial_stability": (
            "Gilt-market sensitivity and financial-stability conditions can transmit fiscal credibility concerns into financing pressure.",
            "Supports board-level monitoring of market-confidence and rate-sensitive procurement risk.",
            "Supports immediacy and confidence scoring where market stress affects fiscal room for manoeuvre.",
        ),
        "credible_market_analysis_on_gilts_and_fiscal_credibility": (
            "Market analysis interprets gilt-yield and fiscal-credibility signals beyond official data releases.",
            "Supports scenario monitoring and management escalation where investor confidence becomes politically salient.",
            "Supports market-confidence evidence, with caveats if analysis is indirect or snippet-only.",
        ),
        "public_procurement_and_infrastructure_delay_evidence": (
            "Procurement and infrastructure delivery evidence links fiscal pressure to awards, deferrals and project delays.",
            "Supports bid-pipeline review, project-delay contingencies and contract repricing controls.",
            "Supports impact scoring for public-sector contract and programme exposure.",
        ),
        "contractor_industry_working_capital_and_payment_risk": (
            "Industry evidence translates public-sector uncertainty into payment, cash-flow and working-capital exposure.",
            "Supports payment-risk monitoring, repricing and exposure reporting by customer or department.",
            "Supports exposure and decision-urgency scoring for contractor cash-flow controls.",
        ),
        "contrary_or_stabilising_fiscal_evidence": (
            "Stabilising evidence can narrow the downside case if funding commitments, market conditions or fiscal credibility improve.",
            "Supports conditions for relaxing heightened bid, payment and board-reporting controls.",
            "Supports confidence discipline and prevents one-way escalation.",
        ),
        "company_data_requirements_for_contractor_exposure": (
            "Company-specific backlog, customer mix, payment terms, margin and working-capital data are required before operational use.",
            "Supports anti-overclaiming controls and confidence caps.",
            "Supports review requirements before using the screen for a contractor-specific board decision.",
        ),
    }
    commercial, implication, decision = profiles.get(
        requirement_name,
        (
            "Fiscal and procurement evidence may affect public-sector contracting confidence.",
            "Relevant to bid pipeline, payment-risk and board monitoring decisions.",
            "Supports contractor exposure review and human verification before operational use.",
        ),
    )
    return {
        "commercial_meaning": commercial,
        "business_user_implication": implication,
        "decision_use": decision,
    }


def _cyber_business_interruption_decision_profile(requirement_name, source_type):
    profiles = {
        "uk_official_cyber_threat_ncsc_evidence": (
            "Official UK threat evidence anchors the ransomware, state-linked and cyber disruption environment.",
            "Supports CFO/COO escalation and likelihood scoring for a UK customer-facing operator.",
            "Supports whether heightened operational resilience and incident readiness controls are justified.",
        ),
        "uk_cyber_breach_prevalence_data": (
            "Prevalence data turns cyber threat into a measurable UK business interruption likelihood signal.",
            "Supports board and risk-manager prioritisation of resilience investment and response readiness.",
            "Supports likelihood scoring and the case for testing recovery assumptions.",
        ),
        "board_cyber_governance_and_resilience_expectations": (
            "Governance evidence defines what senior management should do before and during cyber disruption.",
            "Supports escalation from IT issue to board-level operational resilience decision.",
            "Supports incident response activation and resilience investment decisions.",
        ),
        "ransomware_or_operational_disruption_evidence": (
            "Live disruption evidence connects cyber incidents to downtime, customer harm and recovery pressure.",
            "Supports manual contingency, restoration priority and pause decisions where digital operations are impaired.",
            "Supports incident response, manual fallback and restoration prioritisation.",
        ),
        "cyber_insurance_business_interruption_evidence": (
            "Insurance evidence shows how waiting periods, notice conditions, exclusions and policy wording affect recovery economics.",
            "Supports claim notification and policy-wording review before assuming insured recovery.",
            "Supports triggering the cyber insurance claim process and checking coverage readiness.",
        ),
        "incident_reporting_and_regulatory_notification_guidance": (
            "Notification guidance defines when personal data, customer harm or sector thresholds require legal/compliance review.",
            "Supports ICO, sector-regulator and affected-customer notification escalation.",
            "Supports regulator/customer notification review triggers.",
        ),
        "supplier_msp_dependency_risk": (
            "Supplier and MSP evidence shows when third-party technology, payment, cloud or fulfilment dependencies block recovery.",
            "Supports supplier escalation and recovery bottleneck management.",
            "Supports supplier/MSP dependency escalation before returning to normal operations.",
        ),
        "contrary_or_mitigation_evidence": (
            "Mitigation evidence identifies recovery, backup, continuity or resilience controls that can reduce impact.",
            "Supports moving from manual contingency or incident response back toward normal operations only when controls are validated.",
            "Supports relaxation triggers and resilience-control validation.",
        ),
        "cyber_company_data_requirements_and_anti_overclaiming_controls": (
            "Public evidence can screen exposure, but company systems, revenue, policy wording and recovery data determine operational use.",
            "Caps confidence until the operator provides incident, systems, revenue, supplier and policy data.",
            "Supports anti-overclaiming and company-data requirements before operational use.",
        ),
    }
    commercial, implication, decision = profiles.get(
        requirement_name,
        (_commercial_relevance("", source_type), _business_user_relevance("customer_facing_operator", ""), "Supports business interruption review and operational resilience controls."),
    )
    return {
        "commercial_meaning": commercial,
        "business_user_implication": implication,
        "decision_use": decision,
    }


def _shipping_operator_decision_profile(requirement_name, source_type):
    profiles = {
        "official_maritime_security": (
            "Defines whether security conditions, detention risk or crew-safety concerns justify enhanced voyage approval before transit.",
            "Drives routing approval, crew-safety controls and customer-commitment management.",
            "Supports hold, reroute or escalate decisions before sailing.",
        ),
        "transit_control_or_constabulary_actions": (
            "Shows whether passage is subject to Iranian coordination demands, constabulary controls or detention risk.",
            "Creates direct voyage-approval risk and can make direct transit operationally unacceptable.",
            "Supports the transit versus delay versus reroute decision.",
        ),
        "sanctions_and_safe_passage_payment_risk": (
            "Defines whether tolls, safe-passage payments, swaps, offsets or guarantees create sanctions exposure.",
            "Can force legal/compliance escalation even if direct transit looks commercially cheaper.",
            "Supports sanctions red-flag escalation and payment prohibition controls.",
        ),
        "war_risk_insurance_pricing": (
            "Shows whether war-risk cover remains available and whether repricing changes voyage economics.",
            "Affects route cost, charterparty economics, exclusions, cancellation clauses and additional premium decisions.",
            "Supports insurance confirmation and route-cost comparison before transit.",
        ),
        "vessel_flow_and_AIS_behaviour": (
            "Shows whether vessel behaviour confirms constrained transit, AIS suppression or practical recovery.",
            "Affects routing confidence, compliance red flags and relaxation thresholds.",
            "Supports live operating stance and practical reopening tests.",
        ),
        "energy_cargo_and_chokepoint_exposure": (
            "Quantifies why Hormuz matters commercially for oil, LNG and time-sensitive cargoes.",
            "Explains charter, customer and delivery pressure if transit is delayed or rerouted.",
            "Supports impact severity and client communication.",
        ),
        "route_cost_and_arbitrage_inputs": (
            "Compares direct transit, delay and reroute economics using voyage days, bunker burn, insurance and hold costs.",
            "Helps translate political risk into a risk-adjusted commercial routing decision.",
            "Supports preferred option selection subject to sanctions and safety overrides.",
        ),
        "contrary_or_de_escalation_evidence": (
            "Identifies whether de-escalation has turned into practical reopening rather than headline-only improvement.",
            "Prevents one-way escalation while keeping relaxation tied to vessel-flow, insurance and legal evidence.",
            "Defines relaxation triggers before normal routing resumes.",
        ),
    }
    commercial, implication, decision = profiles.get(
        requirement_name,
        (_commercial_relevance("", source_type), _business_user_relevance("shipping_operator", ""), "Supports operator review and control decisions."),
    )
    return {
        "commercial_meaning": commercial,
        "business_user_implication": implication,
        "decision_use": decision,
    }


def _uk_ets_shipping_operator_decision_profile(requirement_name, source_type):
    profiles = {
        "official_policy_scope": (
            "Defines whether the vessel, route and emissions category are in confirmed scope or only future scenario exposure.",
            "Determines whether carbon cost belongs in current voyage economics or scenario planning only.",
            "Supports route applicability and current-versus-scenario classification.",
        ),
        "reporting_surrender_timeline": (
            "Sets the reporting calendar, surrender timing and first-cycle compliance burden.",
            "Determines whether the operator is ready for MRV, reporting and allowance procurement deadlines.",
            "Supports compliance readiness and timeline escalation.",
        ),
        "carbon_price_evidence": (
            "Provides the allowance price used to convert emissions into route-level cost.",
            "Drives sensitivity to UKA price movement and procurement timing.",
            "Supports base-case and stressed carbon cost estimates.",
        ),
        "emissions_factor_evidence": (
            "Converts fuel burn into estimated tCO2e exposure per voyage.",
            "Drives the arithmetic behind voyage-level carbon cost exposure.",
            "Supports deterministic carbon cost calculation.",
        ),
        "operator_guidance": (
            "Shows how operators and advisers are preparing for reporting, procurement and cost pass-through.",
            "Highlights likely margin pressure and customer pricing decisions.",
            "Supports pass-through and implementation planning.",
        ),
        "legal_practical_analysis": (
            "Clarifies the responsible entity, documentation, MRV process and practical compliance approach.",
            "Reduces risk of mis-allocating responsibility or missing documentary controls.",
            "Supports governance and compliance escalation where responsibilities are unclear.",
        ),
        "future_scope_or_international_extension": (
            "Shows how future policy may extend the exposure to wider route sets.",
            "Helps separate confirmed 2026 exposure from strategic scenario planning.",
            "Supports scenario analysis for UK-international routes.",
        ),
        "contrary_or_scope_limited_evidence": (
            "Prevents the operator from applying current carbon cost assumptions to routes or vessels outside confirmed scope.",
            "Protects against overstating current obligation or coverage rate.",
            "Supports scope-limiting caveats and scenario-only treatment where needed.",
        ),
    }
    commercial, implication, decision = profiles.get(
        requirement_name,
        (_commercial_relevance("", source_type), _business_user_relevance("shipping_operator", ""), "Supports operator review and control decisions."),
    )
    return {
        "commercial_meaning": commercial,
        "business_user_implication": implication,
        "decision_use": decision,
    }


def _trade_finance_decision_profile(requirement_name, source_type):
    profiles = {
        "uk_sanctions_ofsi_official_guidance": (
            "Anchors UK sanctions and OFSI relevance for transaction approval, escalation, legal hold or rejection.",
            "Determines whether a UK lender can rely on routine approval or must escalate to sanctions/compliance review.",
            "Anchors UK sanctions screening, OFSI escalation and legal-hold thresholds.",
        ),
        "sanctions_end_use_controls_and_controlled_goods_risk": (
            "Identifies controlled goods, dual-use technology, licence and end-use red flags.",
            "Drives goods classification, licence checks and legal hold where controlled goods or prohibited end-use cannot be cleared.",
            "Supports goods, end-use and licence checks before approval or drawdown.",
        ),
        "counterparty_and_ownership_exposure": (
            "Tests buyer, seller, consignee, bank, intermediary and beneficial ownership exposure.",
            "Opaque ownership or sanctions-screening uncertainty blocks routine approval.",
            "Supports counterparty screening and ownership escalation.",
        ),
        "jurisdiction_route_and_diversion_exposure": (
            "Identifies route, port, transshipment, diversion and jurisdiction indicators.",
            "Raises escalation risk where route facts suggest sanctions evasion or diversion.",
            "Supports route and diversion red-flag escalation.",
        ),
        "documentation_and_transaction_quality_evidence": (
            "Defines the documents needed to test goods, end-use, ownership, route and payment claims.",
            "Weak or missing documents should trigger escalation or hold before approval.",
            "Supports document-request and missing-data controls.",
        ),
        "enforcement_penalty_and_regulatory_expectations": (
            "Shows regulator expectations and consequences when sanctions controls fail.",
            "Raises the cost of unresolved red flags and supports conservative legal-hold triggers.",
            "Supports enforcement-aware legal hold, rejection and confidence discipline.",
        ),
        "financial_institution_trade_finance_operating_impact": (
            "Translates sanctions exposure into facility, drawdown, payment, credit and insurance controls.",
            "Shows why sanctions risk affects financing approval and operational execution.",
            "Supports trade-finance due diligence actions and facility controls.",
        ),
        "contrary_clearance_or_de_escalation_evidence": (
            "Identifies evidence that could support approval or de-escalation, such as clean screening, licence evidence or exemptions.",
            "Prevents over-escalation where facts are clean and documents are reliable.",
            "Defines evidence needed to move from hold/escalation to approval or enhanced due diligence.",
        ),
        "sanctions_company_data_requirements_and_anti_overclaiming_controls": (
            "Identifies transaction-specific data required before public evidence can support a clearance decision.",
            "Caps confidence until goods, counterparties, ownership, route, payment, licence and documents are validated.",
            "Supports anti-overclaiming and company-data requirements before operational use.",
        ),
        "official_sanctions_guidance": (
            "Defines the legal basis for end-use exposure, notification, licensing and transaction escalation.",
            "Determines whether the lender should approve, hold, escalate or decline a transaction.",
            "Anchors transaction screening, hold/decline triggers and compliance escalation.",
        ),
        "sanctions_regime_context": (
            "Places the transaction inside wider UK/EU sanctions, Russia restrictions and circumvention controls.",
            "Raises counterparty, destination, restricted trade route and regulatory penalty exposure.",
            "Supports regime screening and sanctions-connected party escalation.",
        ),
        "export_control_and_dual_use_risk": (
            "Identifies sensitive goods, dual-use technology and diversion-prone cargo profiles.",
            "Drives goods classification, documentation requirements and specialist export-control review.",
            "Supports goods classification checks before financing or drawdown.",
        ),
        "legal_practical_analysis": (
            "Explains practical timing, notification, licensing, due diligence and business obligations.",
            "Helps translate legal requirements into transaction controls and conditions precedent.",
            "Supports compliance checklist design and legal escalation thresholds.",
        ),
        "trade_route_and_diversion_risk": (
            "Identifies third-country routing, intermediaries and end-use opacity associated with circumvention.",
            "Raises counterparty, documentation, collateral and regulatory exposure.",
            "Supports enhanced end-use documentation and route-level escalation.",
        ),
        "banking_and_payment_risk": (
            "Links sanctions exposure to blocked payments, correspondent banking friction and settlement risk.",
            "Affects payment execution, facility drawdown, reimbursement and client communication.",
            "Supports payment-route checks and facility controls.",
        ),
        "contrary_or_scope_limited_evidence": (
            "Identifies where risk may be specific, documentable and controllable rather than automatically prohibitive.",
            "Supports approval after enhanced due diligence where goods scope, end-use and counterparties are clear.",
            "Defines approval triggers without weakening escalation for unresolved red flags.",
        ),
    }
    commercial, implication, decision = profiles.get(
        requirement_name,
        (_commercial_relevance("", source_type), _business_user_relevance("trade_finance_lender", ""), "Supports transaction review and compliance controls."),
    )
    return {
        "commercial_meaning": commercial,
        "business_user_implication": implication,
        "decision_use": decision,
    }


def _risk_driver(requirement_name, source_type):
    requirement_mapping = {
        "official_policy_scope": "policy_scope_and_route_applicability",
        "reporting_surrender_timeline": "reporting_and_surrender_readiness",
        "carbon_price_evidence": "carbon_price_and_allowance_cost",
        "emissions_factor_evidence": "emissions_factor_and_voyage_calculation",
        "operator_guidance": "operator_margin_and_pass_through_pressure",
        "legal_practical_analysis": "reporting_and_surrender_readiness",
        "future_scope_or_international_extension": "future_international_expansion_risk",
        "contrary_or_scope_limited_evidence": "scope_limited_or_exemption_constraints",
        "official_maritime_security": "transit_control_risk",
        "carrier_operational_behaviour": "Carrier and operational disruption",
        "transit_control_or_constabulary_actions": "transit_control_risk",
        "sanctions_and_safe_passage_payment_risk": "sanctions_safe_passage_risk",
        "war_risk_insurance_pricing": "war_risk_insurance_pressure",
        "vessel_flow_and_AIS_behaviour": "vessel_flow_AIS_disruption",
        "energy_cargo_and_chokepoint_exposure": "energy_chokepoint_exposure",
        "route_cost_and_arbitrage_inputs": "route_cost_arbitrage",
        "contrary_or_de_escalation_evidence": "de_escalation_monitoring",
        "energy_chokepoint_exposure": "Energy chokepoint exposure",
        "insurance_pricing_reinsurance": "Insurance-market repricing",
        "vessel_flow_freight_market": "Vessel-flow and market behaviour",
        "sanctions_compliance": "Sanctions and compliance risk",
        "contrary_de_escalation": "De-escalation and stabilisation evidence",
        "official_sanctions_guidance": "Official sanctions guidance",
        "sanctions_regime_context": "Sanctions regime context",
        "export_control_and_dual_use_risk": "Goods and end-use risk",
        "legal_practical_analysis": "Legal and practical controls",
        "trade_route_and_diversion_risk": "Trade route and diversion risk",
        "banking_and_payment_risk": "Payment and documentation risk",
        "contrary_or_scope_limited_evidence": "Scope-limited approval evidence",
        "uk_sanctions_ofsi_official_guidance": "UK sanctions and OFSI guidance",
        "sanctions_end_use_controls_and_controlled_goods_risk": "Goods and end-use risk",
        "counterparty_and_ownership_exposure": "Counterparty and ownership exposure",
        "jurisdiction_route_and_diversion_exposure": "Jurisdiction, route and diversion exposure",
        "documentation_and_transaction_quality_evidence": "Documentation quality",
        "enforcement_penalty_and_regulatory_expectations": "Enforcement and regulatory expectations",
        "financial_institution_trade_finance_operating_impact": "Trade-finance operating impact",
        "contrary_clearance_or_de_escalation_evidence": "Clearance and de-escalation evidence",
        "sanctions_company_data_requirements_and_anti_overclaiming_controls": "Company data and anti-overclaiming controls",
        "uk_official_cyber_threat_ncsc_evidence": "UK cyber threat and ransomware prevalence",
        "uk_cyber_breach_prevalence_data": "UK cyber breach prevalence",
        "board_cyber_governance_and_resilience_expectations": "Board governance and operational resilience",
        "ransomware_or_operational_disruption_evidence": "Ransomware and operational disruption",
        "cyber_insurance_business_interruption_evidence": "Cyber insurance and claims readiness",
        "incident_reporting_and_regulatory_notification_guidance": "Regulatory notification exposure",
        "supplier_msp_dependency_risk": "Supplier and MSP dependency",
        "contrary_or_mitigation_evidence": "Mitigation and recovery evidence",
        "cyber_company_data_requirements_and_anti_overclaiming_controls": "Company data and anti-overclaiming controls",
        "obr_fiscal_outlook_and_fiscal_risks": "Fiscal headroom and debt-interest pressure",
        "ons_public_finances_data": "Public finances and borrowing indicators",
        "hm_treasury_fiscal_policy_and_spending_control": "Fiscal policy and departmental spending control",
        "bank_of_england_gilt_market_and_financial_stability": "Gilt-market sensitivity and financial stability",
        "credible_market_analysis_on_gilts_and_fiscal_credibility": "Fiscal credibility and market confidence",
        "public_procurement_and_infrastructure_delay_evidence": "Procurement delay and infrastructure deferral risk",
        "contractor_industry_working_capital_and_payment_risk": "Contractor payment and working-capital risk",
        "contrary_or_stabilising_fiscal_evidence": "Stabilising fiscal or market evidence",
        "company_data_requirements_for_contractor_exposure": "Contractor-specific data requirements",
    }
    source_type_mapping = {
        "official_primary": "Maritime security and transit risk",
        "company_update": "Carrier and operational disruption",
        "energy_chokepoint_data": "Energy chokepoint exposure",
        "insurance_market_evidence": "Insurance-market repricing",
        "vessel_flow_or_freight_market_evidence": "Vessel-flow and market behaviour",
        "contrary_or_stabilising_evidence": "De-escalation and stabilisation evidence",
    }
    return requirement_mapping.get(requirement_name) or source_type_mapping.get(source_type, "General commercial risk")


def _judgement_supported(requirement_name, source_type):
    mapping = {
        "official_policy_scope": "Confirmed scope should be separated from future scenario exposure",
        "reporting_surrender_timeline": "Reporting and surrender timing create a live readiness issue",
        "carbon_price_evidence": "UKA pricing can materially alter route economics",
        "emissions_factor_evidence": "Fuel burn can be translated into deterministic tCO2e exposure",
        "operator_guidance": "Operators face margin and pass-through pressure",
        "legal_practical_analysis": "Entity responsibility and MRV controls must be clarified",
        "future_scope_or_international_extension": "International exposure should remain scenario-only unless confirmed",
        "contrary_or_scope_limited_evidence": "Routes outside confirmed scope should not be overstated as current liability",
        "official_maritime_security": "Official guidance indicates live security and crew-safety risk",
        "transit_control_or_constabulary_actions": "Iran-linked transit controls create voyage approval risk",
        "sanctions_and_safe_passage_payment_risk": "Safe-passage demands create sanctions escalation risk",
        "war_risk_insurance_pricing": "War-risk repricing changes voyage economics",
        "vessel_flow_and_AIS_behaviour": "AIS disruption and abnormal flows confirm practical operating stress",
        "energy_cargo_and_chokepoint_exposure": "Hormuz cargo concentration makes commercial impact severe",
        "route_cost_and_arbitrage_inputs": "Route-cost comparisons should inform transit, delay and reroute choices",
        "contrary_or_de_escalation_evidence": "De-escalation should change monitoring before changing stance",
        "carrier_operational_behaviour": "Carrier caution indicates practical operating constraints",
        "energy_chokepoint_exposure": "Energy chokepoint exposure makes impact severe",
        "insurance_pricing_reinsurance": "War-risk pricing and reinsurance appetite require active review",
        "vessel_flow_freight_market": "Vessel-flow disruption supports high immediacy",
        "sanctions_compliance": "Sanctions and compliance risk requires escalation controls",
        "contrary_de_escalation": "De-escalation evidence reduces certainty around worst-case assumptions",
        "official_sanctions_guidance": "Sanctions end-use controls create transaction-screening risk",
        "sanctions_regime_context": "Third-country diversion risk is central to the case",
        "export_control_and_dual_use_risk": "Goods and end-use opacity should drive escalation",
        "legal_practical_analysis": "Official guidance should anchor practical controls",
        "trade_route_and_diversion_risk": "Diversion indicators should drive enhanced due diligence",
        "banking_and_payment_risk": "Payment and correspondent banking risk can crystallise early",
        "contrary_or_scope_limited_evidence": "Scope-limited evidence can support approval after enhanced due diligence",
        "uk_sanctions_ofsi_official_guidance": "UK sanctions and OFSI guidance anchor the transaction decision",
        "sanctions_end_use_controls_and_controlled_goods_risk": "Goods and end-use controls can trigger legal hold",
        "counterparty_and_ownership_exposure": "Counterparty and ownership opacity should drive escalation",
        "jurisdiction_route_and_diversion_exposure": "Route and diversion indicators should drive enhanced due diligence",
        "documentation_and_transaction_quality_evidence": "Weak documents prevent routine approval",
        "enforcement_penalty_and_regulatory_expectations": "Enforcement expectations justify conservative controls",
        "financial_institution_trade_finance_operating_impact": "Sanctions risk affects drawdown, payment and facility controls",
        "contrary_clearance_or_de_escalation_evidence": "Clean evidence can support approval after enhanced due diligence",
        "sanctions_company_data_requirements_and_anti_overclaiming_controls": "Transaction-specific data is required before clearance",
        "uk_official_cyber_threat_ncsc_evidence": "UK cyber threat supports business interruption likelihood",
        "uk_cyber_breach_prevalence_data": "Prevalence evidence supports likelihood scoring",
        "board_cyber_governance_and_resilience_expectations": "Senior management should treat cyber disruption as operational resilience risk",
        "ransomware_or_operational_disruption_evidence": "Cyber incidents can cause downtime and recovery pressure",
        "cyber_insurance_business_interruption_evidence": "Insurance recovery depends on policy wording and claim conditions",
        "incident_reporting_and_regulatory_notification_guidance": "Notification triggers require legal and compliance review",
        "supplier_msp_dependency_risk": "Third-party dependencies can block recovery",
        "contrary_or_mitigation_evidence": "Validated recovery controls can reduce impact",
        "cyber_company_data_requirements_and_anti_overclaiming_controls": "Company-specific systems, revenue, policy and recovery data are required",
        "obr_fiscal_outlook_and_fiscal_risks": "Fiscal constraints can affect public spending confidence and procurement timing",
        "ons_public_finances_data": "Official public finance data supports fiscal-pressure monitoring",
        "hm_treasury_fiscal_policy_and_spending_control": "Spending controls can affect departmental procurement confidence",
        "bank_of_england_gilt_market_and_financial_stability": "Gilt-market sensitivity can justify board-level fiscal-risk monitoring",
        "credible_market_analysis_on_gilts_and_fiscal_credibility": "Market confidence evidence helps test fiscal credibility risk",
        "public_procurement_and_infrastructure_delay_evidence": "Procurement and infrastructure evidence supports delay and deferral controls",
        "contractor_industry_working_capital_and_payment_risk": "Payment and working-capital evidence supports contractor cash-flow controls",
        "contrary_or_stabilising_fiscal_evidence": "Stabilising evidence can reduce but not remove monitoring requirements",
        "company_data_requirements_for_contractor_exposure": "Contractor-specific order book and working-capital data are required",
    }
    return mapping.get(requirement_name, _risk_driver(requirement_name, source_type))


def _refresh_requirement(requirement_name, source_type):
    mapping = {
        "official_policy_scope": "Refresh if route scope, threshold or exemption guidance changes.",
        "reporting_surrender_timeline": "Refresh before the first verified report and allowance procurement cycle.",
        "carbon_price_evidence": "Refresh when UKA market levels move materially or no live price is available.",
        "emissions_factor_evidence": "Refresh if verified fuel mix or approved emissions methodology changes.",
        "operator_guidance": "Refresh when operator pass-through or implementation practice changes.",
        "legal_practical_analysis": "Refresh if responsible entity, MRV process or exemptions are clarified further.",
        "future_scope_or_international_extension": "Refresh when consultation responses or expansion decisions are published.",
        "contrary_or_scope_limited_evidence": "Refresh before applying current carbon cost logic to routes near the edge of scope.",
        "official_maritime_security": "Refresh before approving transit or relaxing operator controls.",
        "transit_control_or_constabulary_actions": "Refresh if transit coordination demands, detention incidents or naval warnings change.",
        "sanctions_and_safe_passage_payment_risk": "Refresh immediately if any toll, guarantee, swap or payment demand is reported.",
        "war_risk_insurance_pricing": "Refresh before sailing if premiums, exclusions or cancellation clauses change.",
        "vessel_flow_and_AIS_behaviour": "Refresh weekly during disruption or before treating recovery as a relaxation trigger.",
        "energy_cargo_and_chokepoint_exposure": "Refresh when cargo criticality or chokepoint data assumptions are updated.",
        "route_cost_and_arbitrage_inputs": "Refresh voyage assumptions before final route approval.",
        "contrary_or_de_escalation_evidence": "Refresh before relaxing controls; confirm with vessel-flow, insurance and sanctions evidence.",
        "carrier_operational_behaviour": "Refresh before changing referral rules or after major carrier service updates.",
        "energy_chokepoint_exposure": "Refresh when structural oil/LNG flow assumptions or chokepoint data are updated.",
        "insurance_pricing_reinsurance": "Refresh before binding Gulf-linked risk or after broker/reinsurance market movement.",
        "vessel_flow_freight_market": "Refresh weekly during disruption or before using flow recovery as a relaxation trigger.",
        "sanctions_compliance": "Refresh after sanctions, ownership, cargo or payment-control announcements.",
        "contrary_de_escalation": "Refresh before relaxing controls; verify against operational and pricing evidence.",
        "official_sanctions_guidance": "Refresh before approval if official guidance, notices or licensing triggers change.",
        "sanctions_regime_context": "Refresh after sanctions designations, regime amendments or Russia-related updates.",
        "export_control_and_dual_use_risk": "Refresh before drawdown if goods classification or export-control status changes.",
        "legal_practical_analysis": "Refresh when legal interpretation, notification or licensing practice changes.",
        "trade_route_and_diversion_risk": "Refresh when routing, intermediary, end user or destination changes.",
        "banking_and_payment_risk": "Refresh before payment execution or facility drawdown.",
        "contrary_or_scope_limited_evidence": "Refresh before approving transactions previously held for scope or documentation gaps.",
        "uk_sanctions_ofsi_official_guidance": "Refresh before approval if OFSI or UK sanctions guidance changes.",
        "sanctions_end_use_controls_and_controlled_goods_risk": "Refresh if goods classification, end-use controls, licence or authorisation status changes.",
        "counterparty_and_ownership_exposure": "Refresh if buyer, seller, beneficial owner, bank, intermediary, vessel or consignee data changes.",
        "jurisdiction_route_and_diversion_exposure": "Refresh if route, port, transshipment, diversion or sanctioned-jurisdiction indicators change.",
        "documentation_and_transaction_quality_evidence": "Refresh when invoices, bills of lading, end-use statements, ownership declarations or payment instructions change.",
        "enforcement_penalty_and_regulatory_expectations": "Refresh if OFSI, FCA or other enforcement expectations change.",
        "financial_institution_trade_finance_operating_impact": "Refresh before approval, drawdown, payment execution or credit/insurance commitment.",
        "contrary_clearance_or_de_escalation_evidence": "Refresh before moving a held transaction back to enhanced due diligence or approval.",
        "sanctions_company_data_requirements_and_anti_overclaiming_controls": "Refresh when transaction-specific goods, counterparty, ownership, route, payment, licence or document data becomes available.",
        "uk_official_cyber_threat_ncsc_evidence": "Refresh if NCSC threat, ransomware or state-linked cyber guidance changes.",
        "uk_cyber_breach_prevalence_data": "Refresh when the latest UK cyber breach prevalence data is published.",
        "board_cyber_governance_and_resilience_expectations": "Refresh if board cyber governance or operational resilience expectations change.",
        "ransomware_or_operational_disruption_evidence": "Refresh if sector-peer, supplier, MSP or live incident reporting changes.",
        "cyber_insurance_business_interruption_evidence": "Refresh if policy wording, waiting periods, exclusions, ransomware treatment or claim-notice expectations change.",
        "incident_reporting_and_regulatory_notification_guidance": "Refresh if ICO, customer-notification or sector-regulator guidance changes.",
        "supplier_msp_dependency_risk": "Refresh when supplier, MSP, cloud, payment or fulfilment dependency data changes.",
        "contrary_or_mitigation_evidence": "Refresh before relaxing incident controls or returning exposed digital operations to normal.",
        "cyber_company_data_requirements_and_anti_overclaiming_controls": "Refresh when systems, revenue, RTO/RPO, backup, supplier, policy or incident facts become available.",
        "obr_fiscal_outlook_and_fiscal_risks": "Refresh when the OBR updates fiscal outlook, fiscal risks, headroom or debt-interest assumptions.",
        "ons_public_finances_data": "Refresh when ONS publishes new public sector finances data.",
        "hm_treasury_fiscal_policy_and_spending_control": "Refresh after Budgets, fiscal statements, Spending Reviews or departmental budget changes.",
        "bank_of_england_gilt_market_and_financial_stability": "Refresh when gilt-market, rates or financial-stability signals materially change.",
        "credible_market_analysis_on_gilts_and_fiscal_credibility": "Refresh if market confidence, gilt-yield or fiscal-credibility analysis changes.",
        "public_procurement_and_infrastructure_delay_evidence": "Refresh when infrastructure pipeline, procurement or project-delay evidence changes.",
        "contractor_industry_working_capital_and_payment_risk": "Refresh when payment-risk, retentions, working-capital or contractor-industry evidence changes.",
        "contrary_or_stabilising_fiscal_evidence": "Refresh before relaxing heightened bid or payment-risk monitoring.",
        "company_data_requirements_for_contractor_exposure": "Refresh when order book, customer mix, payment terms, margins or working-capital data becomes available.",
    }
    return mapping.get(requirement_name, "Refresh before major underwriting or commercial decisions.")


def _is_uk_ets_requirement(requirement_name):
    return requirement_name in {
        "official_policy_scope",
        "reporting_surrender_timeline",
        "carbon_price_evidence",
        "emissions_factor_evidence",
        "operator_guidance",
        "legal_practical_analysis",
        "future_scope_or_international_extension",
        "contrary_or_scope_limited_evidence",
    }


def _publisher_from_url(url):
    return urlparse(url).netloc.replace("www.", "") or "Unknown"
