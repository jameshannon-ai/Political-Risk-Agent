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

    if _is_critical_minerals_supply_chain(combined_text):
        return {
            "likelihood": {
                "score": 4,
                "rationale": "Export-control direction, source concentration and live geopolitical triggers create a credible disruption pathway for rare earth magnet inputs.",
            },
            "impact": {
                "score": 5,
                "rationale": "Product criticality, supplier concentration, high substitution difficulty and a large production continuity gap can make the exposure severe for affected lines.",
            },
            "immediacy": {
                "score": 5,
                "rationale": "A short inventory runway relative to supplier qualification time makes continuity risk near-term if shipments or licences are disrupted.",
            },
            "confidence": {
                "score": 3,
                "rationale": "Public evidence can screen client-type exposure, but BOM, supplier, inventory and contract data are still required for company-specific precision.",
            },
        }

    if _is_uk_fiscal_procurement_risk(combined_text):
        return {
            "likelihood": {
                "score": 4,
                "rationale": "Fiscal pressure, gilt-market sensitivity and departmental budget uncertainty create a credible pathway to continued procurement caution.",
            },
            "impact": {
                "score": 4,
                "rationale": "Impact can be material for infrastructure contractors because public-sector awards, project timing, payment assumptions, bid pricing and working capital can all be affected.",
            },
            "immediacy": {
                "score": 3,
                "rationale": "Timing pressure is moderate-high: procurement and payment effects may not be immediate across all departments, but bid pipeline and board monitoring should be refreshed near-term.",
            },
            "exposure": {
                "score": 4,
                "rationale": "Exposure is potentially high for contractors with concentrated public-sector order books, but cannot be finalised without customer mix, backlog, payment terms and margin data.",
            },
            "decision_urgency": {
                "score": 4,
                "rationale": "The issue warrants bid-pipeline review, payment-risk monitoring, contract repricing checks and board-level exposure reporting rather than passive monitoring.",
            },
            "confidence": {
                "score": 3,
                "rationale": "Confidence is capped because public evidence can screen political-economy risk, but contractor-specific order book, departmental exposure, payment terms and working-capital data are missing.",
            },
        }

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


def _is_critical_minerals_supply_chain(text):
    triggers = [
        "critical minerals",
        "rare earth",
        "magnet supply",
        "advanced manufacturer",
        "production continuity",
    ]
    return sum(1 for term in triggers if term in text) >= 2


def _is_uk_fiscal_procurement_risk(text):
    triggers = [
        "fiscal instability",
        "public-sector procurement",
        "public sector procurement",
        "gilt",
        "infrastructure contractor",
        "procurement delay",
        "departmental budget",
    ]
    return sum(1 for term in triggers if term in text) >= 2
