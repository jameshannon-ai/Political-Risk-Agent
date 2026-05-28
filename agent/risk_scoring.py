from agent.confidence_model import calculate_confidence


HIGH_RISK_TERMS = {
    "war",
    "attack",
    "missile",
    "sanction",
    "sanctions",
    "blockade",
    "closure",
    "strike",
    "piracy",
    "conflict",
}

IMPACT_TERMS = {
    "route disruption",
    "port access",
    "fuel costs",
    "claims",
    "freight rates",
    "payment disruption",
    "customs disruption",
    "collateral risk",
}

IMMEDIACY_TERMS = {
    "today",
    "immediate",
    "next 7 days",
    "next week",
    "next 30 days",
    "current",
    "active",
}


def _contains_any(text, terms):
    return any(term in text for term in terms)


def _clamp(score):
    return max(1, min(5, score))


def score_risk(topic, concerns=None, region="", time_horizon="", sources=None):
    concerns = concerns or []
    sources = sources or []
    combined_text = " ".join([topic, region, time_horizon, " ".join(concerns)]).lower()

    if _is_uk_ets_maritime(combined_text):
        return {
            "likelihood": {
                "score": 5,
                "rationale": "Confirmed policy implementation, not speculative risk.",
            },
            "impact": {
                "score": 4 if _has_material_uk_ets_cost_context(combined_text) else 3,
                "rationale": "Material for in-scope domestic routes, but not universal across all UK or international voyages.",
            },
            "immediacy": {
                "score": 5,
                "rationale": "Reporting, monitoring and allowance preparation need near-term action before or during implementation.",
            },
            "confidence": {
                "score": 4,
                "rationale": "Capped below 5 because official policy evidence is strong, but UKA price and operator fuel assumptions are not transaction-specific live inputs.",
            },
        }

    likelihood = 2
    impact = 2
    immediacy = 2
    confidence = 3

    if _contains_any(combined_text, HIGH_RISK_TERMS):
        likelihood += 2
        impact += 1

    if _contains_any(combined_text, IMPACT_TERMS):
        impact += 2

    if _contains_any(combined_text, IMMEDIACY_TERMS):
        immediacy += 2

    if sources:
        evidence_confidence = calculate_confidence(sources)
        confidence = evidence_confidence["confidence_score"]
        confidence_rationale = evidence_confidence["confidence_rationale"]
    elif len(concerns) >= 4:
        impact += 1
        confidence += 1
        confidence_rationale = "Higher because the user supplied multiple concrete concerns; no source evidence was supplied."
    elif not concerns:
        confidence -= 1
        confidence_rationale = "Lower because no source evidence and no specific concerns were supplied."
    else:
        confidence_rationale = "Based on supplied concerns only; no source evidence was supplied."

    if any(region_name in combined_text for region_name in ["red sea", "gulf of aden", "black sea", "strait of hormuz"]):
        likelihood += 1
        impact += 1

    return {
        "likelihood": {
            "score": _clamp(likelihood),
            "rationale": "Higher when the topic or region includes active disruption, conflict, sanctions, or strategic chokepoints.",
        },
        "impact": {
            "score": _clamp(impact),
            "rationale": "Higher when concerns point to costs, access constraints, claims, freight, payment, or collateral effects.",
        },
        "immediacy": {
            "score": _clamp(immediacy),
            "rationale": "Higher when the time horizon signals current or near-term exposure.",
        },
        "confidence": {
            "score": _clamp(confidence),
            "rationale": confidence_rationale,
        },
    }


def _is_uk_ets_maritime(text):
    return "uk ets" in text and ("maritime" in text or "shipping" in text or "domestic maritime" in text)


def _has_material_uk_ets_cost_context(text):
    terms = ["carbon cost", "allowance", "uka", "domestic", "route", "voyage", "liverpool", "belfast"]
    return sum(1 for term in terms if term in text) >= 3
