from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class CaseConfig:
    case_id: str
    display_name: str
    domain: str
    business_users: list[str]
    detect_keywords: list[str]
    source_requirements_fn: Callable
    brief_generator_fn: Callable
    scoring_profile: str


def _requirements_fn(name):
    def _call(*args, **kwargs):
        import agent.source_requirements as source_requirements

        return getattr(source_requirements, name)(*args, **kwargs)

    return _call


def _brief_fn(module_name):
    def _call(evidence_pack):
        module = __import__(f"agent.briefs.{module_name}", fromlist=["generate"])
        return module.generate(evidence_pack)

    return _call


CASE_REGISTRY = {
    "hormuz": CaseConfig(
        case_id="hormuz",
        display_name="Hormuz Route Decision Engine",
        domain="maritime_trade",
        business_users=["shipping_operator"],
        detect_keywords=["hormuz", "strait of hormuz", "route decision", "safe-passage", "war-risk"],
        source_requirements_fn=_requirements_fn("_hormuz_shipping_operator_requirements"),
        brief_generator_fn=_brief_fn("hormuz"),
        scoring_profile="maritime_route_decision",
    ),
    "sanctions": CaseConfig(
        case_id="sanctions",
        display_name="Sanctions Trade Finance Exposure Engine",
        domain="sanctions_trade_finance",
        business_users=["trade_finance_lender"],
        detect_keywords=["sanctions", "trade finance", "export controls", "legal-hold", "transaction approval"],
        source_requirements_fn=_requirements_fn("_sanctions_trade_finance_requirements"),
        brief_generator_fn=_brief_fn("sanctions"),
        scoring_profile="sanctions_transaction_decision",
    ),
    "uk_ets": CaseConfig(
        case_id="uk_ets",
        display_name="UK ETS Maritime Expansion",
        domain="regulatory_carbon_shipping",
        business_users=["shipping_operator"],
        detect_keywords=["uk ets", "maritime expansion", "carbon cost", "emissions trading"],
        source_requirements_fn=_requirements_fn("_uk_ets_shipping_operator_requirements"),
        brief_generator_fn=_brief_fn("uk_ets"),
        scoring_profile="regulatory_carbon_shipping",
    ),
    "critical_minerals": CaseConfig(
        case_id="critical_minerals",
        display_name="Critical Minerals Exposure Engine",
        domain="critical_minerals_supply_chain",
        business_users=["advanced_manufacturer"],
        detect_keywords=["critical minerals", "rare earth", "magnet supply", "permanent magnets"],
        source_requirements_fn=_requirements_fn("_critical_minerals_advanced_manufacturer_requirements"),
        brief_generator_fn=_brief_fn("critical_minerals"),
        scoring_profile="production_continuity",
    ),
    "cyber": CaseConfig(
        case_id="cyber",
        display_name="Cyber Business Interruption Engine",
        domain="cyber_business_interruption",
        business_users=["customer_facing_operator"],
        detect_keywords=["cyber business interruption", "ransomware", "operational resilience", "managed service provider", "msp"],
        source_requirements_fn=_requirements_fn("_cyber_business_interruption_requirements"),
        brief_generator_fn=_brief_fn("cyber"),
        scoring_profile="business_interruption",
    ),
    "fiscal": CaseConfig(
        case_id="fiscal",
        display_name="UK Fiscal Instability & Procurement Delay Risk",
        domain="uk_fiscal_procurement_risk",
        business_users=["infrastructure_contractor"],
        detect_keywords=["fiscal instability", "public-sector procurement", "public sector procurement", "gilt", "procurement delay"],
        source_requirements_fn=_requirements_fn("_uk_fiscal_procurement_requirements"),
        brief_generator_fn=_brief_fn("fiscal"),
        scoring_profile="political_economy_procurement",
    ),
}


def get_case(case_id):
    return CASE_REGISTRY.get(case_id)


def cases_for_domain(domain):
    return [case for case in CASE_REGISTRY.values() if case.domain == domain]


def match_case(topic="", business_user="", domain=None):
    normalized_user = normalize_business_user(business_user)
    text = f"{topic} {business_user} {domain or ''}".lower()

    if domain:
        domain_matches = [
            case for case in CASE_REGISTRY.values()
            if case.domain == domain and (not case.business_users or normalized_user in case.business_users)
        ]
        if domain_matches:
            return domain_matches[0]
        loose_domain_matches = [case for case in CASE_REGISTRY.values() if case.domain == domain]
        if loose_domain_matches:
            return loose_domain_matches[0]

    for case in CASE_REGISTRY.values():
        if normalized_user not in case.business_users:
            continue
        if any(keyword in text for keyword in case.detect_keywords):
            return case
    for case in CASE_REGISTRY.values():
        if any(keyword in text for keyword in case.detect_keywords):
            return case
    return None


BUSINESS_USER_ALIASES = {
    "shipping operator": "shipping_operator",
    "shipping_operator": "shipping_operator",
    "marine insurer": "marine_insurer",
    "marine_insurer": "marine_insurer",
    "trade finance lender": "trade_finance_lender",
    "trade_finance_lender": "trade_finance_lender",
    "advanced manufacturer": "advanced_manufacturer",
    "advanced_manufacturer": "advanced_manufacturer",
    "uk advanced manufacturer": "advanced_manufacturer",
    "customer facing operator": "customer_facing_operator",
    "customer_facing_operator": "customer_facing_operator",
    "uk retailer": "customer_facing_operator",
    "critical services operator": "customer_facing_operator",
    "infrastructure contractor": "infrastructure_contractor",
    "infrastructure_contractor": "infrastructure_contractor",
    "uk infrastructure contractor": "infrastructure_contractor",
    "uk_infrastructure_contractor": "infrastructure_contractor",
    "uk infrastructure contractor bidding for government-funded transport and energy projects": "infrastructure_contractor",
    "uk infrastructure contractor bidding for government funded transport and energy projects": "infrastructure_contractor",
}


def normalize_business_user(value):
    if not value:
        return value
    key = str(value).strip().replace("-", " ").replace("_", " ").lower()
    return BUSINESS_USER_ALIASES.get(key, str(value).strip())
