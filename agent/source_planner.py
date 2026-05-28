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
