from agent.briefs import legacy
from agent.cases.registry import match_case, normalize_business_user


TEMPLATE_BY_CASE_ID = {
    "critical_minerals": "critical_minerals_advanced_manufacturer_showcase",
    "uk_ets": "uk_ets_shipping_operator_showcase",
    "hormuz": "hormuz_shipping_operator_showcase",
    "sanctions": "sanctions_trade_finance_showcase",
    "cyber": "generic_political_risk",
    "fiscal": "generic_political_risk",
}


def select_report_template(topic, business_user, domain=None):
    case = match_case(topic=topic, business_user=business_user, domain=domain)
    if case:
        return TEMPLATE_BY_CASE_ID.get(case.case_id, "generic_political_risk")
    if "hormuz" in topic.lower() and normalize_business_user(business_user) == "marine_insurer":
        return "hormuz_marine_insurer_showcase"
    return "generic_political_risk"


def generate_brief(topic, business_user, region, time_horizon, concerns, sources=None, evidence_pack=None):
    normalized_user = normalize_business_user(business_user)
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain")
    case = match_case(topic=topic, business_user=normalized_user, domain=domain)
    if case and evidence_pack:
        routed_pack = {
            **evidence_pack,
            "business_user": normalized_user,
            "topic": topic,
            "region": region,
            "time_horizon": time_horizon,
            "concerns": concerns,
            "evidence": sources if sources is not None else evidence_pack.get("evidence", []),
        }
        return case.brief_generator_fn(routed_pack)
    return legacy.generate_brief(
        topic=topic,
        business_user=normalized_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        sources=sources,
        evidence_pack=evidence_pack,
    )


def save_brief(markdown, output_dir):
    return legacy.save_brief(markdown, output_dir)


def _source_requirement_coverage(evidence_pack):
    return legacy._source_requirement_coverage(evidence_pack)


def _evidence_to_score_bridge(evidence_pack, scores):
    return legacy._evidence_to_score_bridge(evidence_pack, scores)

