import json
from pathlib import Path

from agent.source_requirements import generate_source_requirements


DOMAIN_PACKS_PATH = Path("config/domain_packs.json")


def create_source_plan(topic, domain, business_user, region, time_horizon, concerns):
    domain_pack = _load_domain_pack(domain)
    requirements = generate_source_requirements(
        topic=topic,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        domain_pack={**domain_pack, "domain": domain},
    )
    decision_questions = _decision_questions(domain_pack, business_user, requirements)
    search_queries = _search_queries(topic, region, time_horizon, requirements)

    return {
        "research_objective": _research_objective(topic, domain, business_user, region, time_horizon),
        "decision_questions": decision_questions,
        "required_source_mix": domain_pack.get("required_source_mix", []),
        "source_requirements": requirements,
        "search_queries": search_queries,
        "expected_evidence_types": domain_pack.get("preferred_source_types", []),
        "minimum_acceptable_coverage": _minimum_acceptable_coverage(requirements),
        "refresh_priorities": _refresh_priorities(domain_pack, requirements),
        "domain": domain,
        "client_decision_outputs": domain_pack.get("client_decision_outputs", []),
        "risk_drivers": domain_pack.get("risk_drivers", []),
    }


def infer_domain(topic, business_user, domain=None):
    if domain:
        return domain
    text = f"{topic} {business_user}".lower()
    if (
        "fiscal instability" in text
        or "public-sector procurement" in text
        or "public sector procurement" in text
        or "gilt" in text
        or business_user in {"uk_infrastructure_contractor", "infrastructure_contractor", "UK infrastructure contractor"}
    ):
        return "uk_fiscal_procurement_risk"
    if "cyber business interruption" in text or ("cyber" in text and "operational resilience" in text) or business_user in {"customer_facing_operator", "uk_retailer", "critical_services_operator"}:
        return "cyber_business_interruption"
    if "critical minerals" in text or "rare earth" in text or "magnet supply" in text or business_user == "advanced_manufacturer":
        return "critical_minerals_supply_chain"
    if "hormuz" in text or "maritime" in text or "shipping" in text:
        if "uk ets" in text or "carbon" in text or "emissions trading" in text:
            return "regulatory_carbon_shipping"
        return "maritime_trade"
    if "sanctions" in text or "trade finance" in text:
        return "sanctions_trade_finance"
    if "election" in text or "investor" in text:
        return "election_investor_risk"
    if "civil unrest" in text or "supply chain" in text:
        return "civil_unrest_supply_chain"
    if "regulatory" in text or "insurance" in text:
        return "regulatory_change_insurance"
    return "maritime_trade"


def _load_domain_pack(domain):
    if not DOMAIN_PACKS_PATH.exists():
        return {}
    packs = json.loads(DOMAIN_PACKS_PATH.read_text(encoding="utf-8"))
    return packs.get(domain, {})


def _research_objective(topic, domain, business_user, region, time_horizon):
    return (
        f"Build a governed evidence base for {business_user} decision-making on {topic} "
        f"in {region} over {time_horizon}, using the {domain} domain pack."
    )


def _decision_questions(domain_pack, business_user, requirements):
    configured = domain_pack.get("decision_questions") or domain_pack.get("business_user_decision_questions", {}).get(business_user, [])
    questions = list(configured)
    for requirement in requirements:
        for question in requirement.get("decision_questions_supported", []):
            if question not in questions:
                questions.append(question)
    return questions


def _search_queries(topic, region, time_horizon, requirements):
    return {
        requirement["requirement_id"]: _queries_for_requirement(topic, region, time_horizon, requirement)
        for requirement in requirements
    }


def _queries_for_requirement(topic, region, time_horizon, requirement):
    name = requirement["requirement_name"].replace("_", " ")
    domains = requirement.get("preferred_domains", [])
    source_types = requirement.get("preferred_source_types", [])
    requirement_name = requirement["requirement_name"]
    queries = []

    targeted_queries = {
        "official_policy_scope": [
            "GOV.UK UK ETS domestic maritime 1 July 2026 5000 GT UK ports",
            "ICAP UK ETS domestic maritime 2026 5000 GT",
        ],
        "reporting_surrender_timeline": [
            "GOV.UK UK ETS maritime verified annual emissions report 31 March 30 April 2028",
            "LR UK ETS domestic maritime reporting surrender deadline 2026 2028",
        ],
        "carbon_price_evidence": [
            "UKA carbon price UK ETS allowance price maritime 2026",
            "UK ETS allowance price manual fallback shipping operator",
        ],
        "emissions_factor_evidence": [
            "IMO marine gas oil emission factor CO2 per tonne fuel",
            "GOV.UK greenhouse gas conversion factor marine gas oil",
        ],
        "operator_guidance": [
            "LR UK ETS domestic maritime operator guidance cost pass through",
            "UK Chamber of Shipping UK ETS maritime operator exposure",
        ],
        "legal_practical_analysis": [
            "HFW UK ETS domestic shipping 2026 compliance responsibility",
            "Watson Farley UK ETS maritime domestic shipping 2026",
        ],
        "future_scope_or_international_extension": [
            "GOV.UK UK ETS international maritime consultation",
            "ICAP UK ETS international maritime consultation domestic shipping",
        ],
        "contrary_or_scope_limited_evidence": [
            "GOV.UK UK ETS maritime exemptions offshore delayed 2027",
            "LR UK ETS domestic maritime exemptions international routes not in scope",
        ],
        "transit_control_or_constabulary_actions": [
            "Reuters Iran sets up mechanism to manage vessel transit through Hormuz",
            "AP Iran transit controls Hormuz vessel coordination detention risk",
        ],
        "sanctions_and_safe_passage_payment_risk": [
            "OFAC FAQ 1249 sanctions risks toll safe-passage payments Hormuz",
            "AP US sanctions Iran Persian Gulf Strait Authority",
        ],
        "vessel_flow_and_AIS_behaviour": [
            "Reuters Hormuz tanker traffic AIS transponder behaviour",
            "AP Hormuz vessel flows AIS disruption",
        ],
        "energy_cargo_and_chokepoint_exposure": [
            "EIA Strait of Hormuz chokepoint oil LNG exposure",
            "IEA Strait of Hormuz oil LNG chokepoint exposure",
        ],
        "war_risk_insurance_pricing": [
            "Howden Re Strait of Hormuz war risk pricing",
            "Reuters Hormuz war risk insurance premium shipping",
        ],
        "contrary_or_de_escalation_evidence": [
            "Reuters Strait of Hormuz reopening conditions shipping de-escalation",
            "AP Strait of Hormuz de-escalation vessel flows reopening",
        ],
        "uk_critical_minerals_policy_and_manufacturing_resilience": [
            "site:gov.uk UK critical minerals strategy vision 2035 rare earth magnets manufacturing",
            "site:parliament.uk UK critical minerals manufacturing resilience rare earth magnets",
        ],
        "export_control_direction_and_live_trigger": [
            "site:reuters.com China rare earth magnet export controls licences Reuters",
            "site:apnews.com rare earth export controls magnets licences AP",
        ],
        "rare_earth_magnet_or_controlled_input_classification": [
            "site:usgs.gov rare earth permanent magnets supply chain NdFeB dysprosium terbium",
            "site:iea.org rare earth permanent magnets supply chain manufacturing",
        ],
        "supply_concentration_and_dependency_data": [
            "site:oecd.org export restrictions critical raw materials rare earth magnets China",
            "site:usgs.gov rare earths production concentration China permanent magnets",
        ],
        "uk_industry_exposure_and_advanced_manufacturing_relevance": [
            "site:hvm.catapult.org.uk rare earth magnets UK advanced manufacturing exposure",
            "site:bgs.ac.uk rare earth magnets UK industry exposure",
        ],
        "substitution_feasibility_and_alternative_supplier_qualification": [
            "site:csis.org rare earth magnet substitution qualification alternative suppliers",
            "site:rusi.org rare earth magnets alternative supplier qualification manufacturing",
        ],
        "market_pricing_or_shortage_signal": [
            "site:reuters.com rare earth magnet shortage prices manufacturing Reuters",
            "site:reuters.com rare earth magnet users paying premium prices ex China supply Reuters",
        ],
        "contrary_or_easing_evidence": [
            "site:reuters.com rare earth export controls easing licence approvals magnet supply",
            "site:reuters.com alternative rare earth magnet supply easing capacity Reuters",
        ],
        "company_data_requirements_and_anti_overclaiming_controls": [
            "site:hvm.catapult.org.uk advanced manufacturer rare earth magnet supply chain inventory supplier qualification",
            "site:csis.org rare earth magnet supply chain company data qualification inventory risk",
        ],
        "uk_sanctions_ofsi_official_guidance": [
            "site:gov.uk OFSI financial sanctions guidance UK trade finance sanctions compliance",
            "site:gov.uk sanctions end-use controls guidance businesses UK",
        ],
        "sanctions_end_use_controls_and_controlled_goods_risk": [
            "site:gov.uk sanctions end-use controls controlled goods licence notification",
            "site:gov.uk strategic export controls dual-use goods end-use sanctions",
        ],
        "counterparty_and_ownership_exposure": [
            "site:gov.uk OFSI ownership and control sanctions guidance counterparty beneficial ownership",
            "site:wolfsberg-principles.com sanctions screening trade finance beneficial ownership",
        ],
        "jurisdiction_route_and_diversion_exposure": [
            "site:reuters.com sanctions diversion third country route trade finance export controls",
            "site:gov.uk sanctions circumvention diversion third countries export controls",
        ],
        "documentation_and_transaction_quality_evidence": [
            "site:iccwbo.org trade finance sanctions due diligence documents bills of lading invoices",
            "site:wolfsberg-principles.com trade finance sanctions due diligence documents",
        ],
        "enforcement_penalty_and_regulatory_expectations": [
            "site:gov.uk OFSI financial sanctions enforcement penalties guidance",
            "site:ofsi.blog.gov.uk OFSI strategy enforcement financial sanctions compliance",
        ],
        "financial_institution_trade_finance_operating_impact": [
            "site:wolfsberg-principles.com trade finance sanctions controls financial institutions",
            "site:baft.org trade finance sanctions compliance controls",
        ],
        "contrary_clearance_or_de_escalation_evidence": [
            "site:gov.uk sanctions licence exemption authorisation guidance trade goods",
            "site:bakermckenzie.com UK sanctions end-use controls licence exemption scope analysis",
        ],
        "sanctions_company_data_requirements_and_anti_overclaiming_controls": [
            "site:wolfsberg-principles.com trade finance sanctions due diligence customer transaction data",
            "site:iccwbo.org trade finance due diligence transaction documents sanctions",
        ],
        "uk_official_cyber_threat_ncsc_evidence": [
            "site:ncsc.gov.uk annual review ransomware UK organisations operational disruption",
            "site:ncsc.gov.uk ransomware cyber threat UK organisations operational resilience",
        ],
        "uk_cyber_breach_prevalence_data": [
            "site:gov.uk Cyber Security Breaches Survey 2026 UK business ransomware",
            "site:gov.uk Cyber Security Breaches Survey UK businesses cyber breach prevalence ransomware",
        ],
        "board_cyber_governance_and_resilience_expectations": [
            "site:gov.uk Cyber Governance Code of Practice board cyber risk operational resilience",
            "site:ncsc.gov.uk board cyber governance operational resilience incident response",
        ],
        "ransomware_or_operational_disruption_evidence": [
            "site:reuters.com UK retailer cyber attack operational disruption ransomware",
            "site:apnews.com UK ransomware operational disruption retailer customer service",
        ],
        "cyber_insurance_business_interruption_evidence": [
            "site:marsh.com cyber insurance business interruption waiting period ransomware UK",
            "site:aon.com cyber insurance business interruption ransomware waiting period claims",
            "site:wtwco.com cyber insurance business interruption ransomware claims",
        ],
        "incident_reporting_and_regulatory_notification_guidance": [
            "site:ico.org.uk personal data breach notification 72 hours UK cyber incident",
            "site:ico.org.uk ransomware personal data breach notification customers",
        ],
        "supplier_msp_dependency_risk": [
            "site:ncsc.gov.uk managed service provider cyber attack supply chain UK business disruption",
            "site:fca.org.uk operational resilience third party supplier cyber incident outage",
        ],
        "contrary_or_mitigation_evidence": [
            "site:ncsc.gov.uk ransomware recovery backup business continuity guidance",
            "site:gov.uk cyber resilience actions business continuity recovery",
        ],
        "cyber_company_data_requirements_and_anti_overclaiming_controls": [
            "site:ncsc.gov.uk incident response plan business continuity recovery time objectives",
            "site:marsh.com cyber insurance claim notice policy wording business interruption",
        ],
        "obr_fiscal_outlook_and_fiscal_risks": [
            "site:obr.uk Economic and fiscal outlook 2026 fiscal headroom debt interest borrowing",
            "site:obr.uk Fiscal risks and sustainability 2025 UK debt interest spending pressures",
            "site:obr.uk welfare trends spending pressures fiscal outlook public finances 2026",
        ],
        "ons_public_finances_data": [
            "site:ons.gov.uk public sector finances UK latest borrowing debt interest 2026",
            "site:ons.gov.uk public sector finances borrowing debt UK fiscal position May 2026",
        ],
        "hm_treasury_fiscal_policy_and_spending_control": [
            "site:gov.uk Spending Review 2025 departmental budgets infrastructure HM Treasury",
            "site:gov.uk Spring Statement 2025 fiscal rules departmental spending public investment",
            "site:gov.uk HM Treasury fiscal rules public spending infrastructure pipeline",
        ],
        "bank_of_england_gilt_market_and_financial_stability": [
            "site:bankofengland.co.uk financial stability report gilt market government bonds 2025 2026",
            "site:bankofengland.co.uk gilt market conditions financial stability UK rates 2026",
            "site:bankofengland.co.uk monetary policy report gilt yields UK government bonds",
        ],
        "credible_market_analysis_on_gilts_and_fiscal_credibility": [
            "site:reuters.com UK gilt yields fiscal credibility public finances 2026",
            "site:ifs.org.uk UK fiscal outlook spending review debt interest 2026",
            "site:resolutionfoundation.org UK fiscal headroom gilt yields public finances 2026",
        ],
        "public_procurement_and_infrastructure_delay_evidence": [
            "site:nao.org.uk infrastructure projects delay public procurement major projects 2025 2026",
            "site:ipa.gov.uk annual report on major projects infrastructure delays government portfolio 2025",
            "site:gov.uk National Infrastructure and Construction Pipeline 2025 procurement projects",
            "site:gov.uk Construction Pipeline public procurement infrastructure projects 2026",
            "site:cabinetoffice.gov.uk public procurement pipeline infrastructure government contracts",
        ],
        "contractor_industry_working_capital_and_payment_risk": [
            "site:builduk.org construction payment performance public sector working capital 2025 2026",
            "site:civilengineeringcontractors.com infrastructure contractor procurement delay payment risk 2025",
            "site:constructionleadershipcouncil.co.uk payment performance construction working capital procurement",
            "site:icaew.com late payments construction working capital public sector 2025",
        ],
        "contrary_or_stabilising_fiscal_evidence": [
            "site:gov.uk National Infrastructure and Construction Pipeline committed projects 2025",
            "site:gov.uk 10 Year Infrastructure Strategy pipeline certainty 2025",
            "site:obr.uk fiscal headroom debt falling forecast public finances 2026",
            "site:bankofengland.co.uk gilt market functioning stable financial stability 2025",
        ],
        "company_data_requirements_for_contractor_exposure": [
            "site:builduk.org construction contractor working capital payment terms public sector clients",
            "site:icaew.com construction working capital public sector contract payment risk",
        ],
    }
    queries.extend(targeted_queries.get(requirement_name, []))

    if domains:
        queries.append(f"site:{domains[0]} {topic} {name} {time_horizon}".strip())
    else:
        queries.append(f"{topic} {region} {name}".strip())

    specialist_domain = _first_domain_matching(domains, ["skadden", "akingump", "bakermckenzie", "osborneclarke", "lloydslist", "howden", "spglobal"])
    if specialist_domain:
        queries.append(f"site:{specialist_domain} {topic} {name}")
    elif "specialist_analysis" in source_types:
        queries.append(f"{topic} {name} specialist analysis")

    news_domain = _first_domain_matching(domains, ["reuters", "ft.com", "apnews", "theguardian"])
    if news_domain:
        queries.append(f"site:{news_domain} {topic} {name}")
    elif "reputable_news" in source_types:
        queries.append(f"{topic} {name} Reuters")

    if "contrary" in requirement["requirement_name"] or "scope_limited" in requirement["requirement_name"] or "stabilising" in requirement["requirement_name"]:
        queries.append(f"{topic} {name} scope limited stabilising contrary evidence")

    return _dedupe(queries)


def _minimum_acceptable_coverage(requirements):
    high_priority = [item["requirement_name"] for item in requirements if item.get("strength_threshold") == "high"]
    return {
        "minimum_total_requirements": len(requirements),
        "minimum_high_priority_requirements": len(high_priority),
        "high_priority_requirements": high_priority,
        "minimum_sources_per_requirement": {
            item["requirement_id"]: item.get("minimum_sources", 1)
            for item in requirements
        },
    }


def _refresh_priorities(domain_pack, requirements):
    watchlist = domain_pack.get("watchlist_indicators", [])
    return [
        {
            "requirement_id": requirement["requirement_id"],
            "requirement_name": requirement["requirement_name"],
            "refresh_expectation": requirement["freshness_expectation"],
            "watchlist_indicators": watchlist[:4],
        }
        for requirement in requirements
    ]


def _first_domain_matching(domains, needles):
    for domain in domains:
        if any(needle in domain for needle in needles):
            return domain
    return ""


def _dedupe(items):
    deduped = []
    for item in items:
        if item and item not in deduped:
            deduped.append(item)
    return deduped
