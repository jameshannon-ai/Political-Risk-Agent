from agent.source_planner import create_source_plan, infer_domain


SOURCE_CATEGORIES = [
    "official_primary",
    "official_guidance",
    "company_update",
    "energy_chokepoint_data",
    "insurance_market_evidence",
    "vessel_flow_or_freight_market_evidence",
    "reputable_news",
    "specialist_analysis",
    "contrary_or_stabilising_evidence",
    "economic_data",
    "market_indicator",
    "industry_guidance",
]

SOURCE_TYPE_ALIASES = {
    "official_guidance": "official_primary",
}


def create_source_strategy(topic, region, time_horizon, business_user="", concerns=None, domain=None, domain_pack=None):
    domain = infer_domain(topic, business_user, domain)
    source_plan = create_source_plan(
        topic=topic,
        domain=domain,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns or [],
    )
    requirements = source_plan["source_requirements"]

    return {
        "topic": topic,
        "region": region,
        "time_horizon": time_horizon,
        "domain": domain,
        "source_plan": source_plan,
        "source_requirements": requirements,
        "categories": _categories_from_requirements(requirements, source_plan),
    }


def _categories_from_requirements(requirements, source_plan):
    categories = []
    for requirement in requirements:
        expected_source_type = _expected_source_type(requirement)
        if expected_source_type not in categories:
            categories.append(expected_source_type)
    if not categories:
        categories = [
            SOURCE_TYPE_ALIASES.get(item, item)
            for item in source_plan.get("expected_evidence_types", [])
            if SOURCE_TYPE_ALIASES.get(item, item) in SOURCE_CATEGORIES
        ] or SOURCE_CATEGORIES

    return [
        {
            "category": category,
            "source_requirement": requirement["requirement_name"],
            "requirement_id": requirement["requirement_id"],
            "requirement_name": requirement["requirement_name"],
            "evidence_question": requirement["decision_questions_supported"][0],
            "target_evidence_question": requirement["decision_questions_supported"][0],
            "preferred_domains": requirement.get("preferred_domains", []),
            "preferred_source_types": requirement.get("preferred_source_types", []),
            "queries": source_plan["search_queries"].get(requirement["requirement_id"], []),
            "minimum_acceptable_evidence": requirement.get("minimum_sources", 1),
            "expected_source_type": category,
            "freshness_expectation": requirement["freshness_expectation"],
            "refresh_expectation": requirement["freshness_expectation"],
        }
        for requirement in requirements
        for category in [_expected_source_type(requirement)]
    ]


def _expected_source_type(requirement):
    for source_type in requirement.get("preferred_source_types", []):
        normalised = SOURCE_TYPE_ALIASES.get(source_type, source_type)
        if normalised in SOURCE_CATEGORIES:
            return normalised
    return "specialist_analysis"
