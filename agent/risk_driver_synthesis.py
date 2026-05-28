WEIGHT_ORDER = {"high": 3, "medium": 2, "low": 1}


def synthesize_risk_drivers(evidence):
    grouped = {}
    for item in evidence:
        driver = item.get("risk_driver") or "General commercial risk"
        grouped.setdefault(driver, []).append(item)

    drivers = []
    for driver_name, items in grouped.items():
        sorted_items = sorted(
            items,
            key=lambda item: (
                WEIGHT_ORDER.get(item.get("evidence_weight", "low"), 1),
                item.get("decision_value_score") or 0,
            ),
            reverse=True,
        )
        top_items = sorted_items[:3]
        drivers.append(
            {
                "driver_name": driver_name,
                "source_requirements_covered": sorted(
                    {
                        item.get("requirement_name")
                        for item in items
                        if item.get("requirement_name")
                    }
                ),
                "highest_weight_sources": [item.get("source_id", "") for item in top_items],
                "evidence_summary": _join_claims(top_items),
                "quantified_facts": _quantified_facts(top_items),
                "commercial_meaning": _first_value(top_items, "commercial_meaning"),
                "business_user_implication": _first_value(top_items, "business_user_implication"),
                "decision_use": _first_value(top_items, "decision_use"),
                "uncertainty_or_caveat": _first_value(top_items, "caveat"),
                "refresh_trigger": _first_value(top_items, "refresh_requirement"),
            }
        )

    return sorted(drivers, key=lambda item: item["driver_name"])


def _join_claims(items):
    claims = [
        item.get("extracted_claim") or item.get("claim_supported", "")
        for item in items
        if item.get("extracted_claim") or item.get("claim_supported")
    ]
    return " ".join(claims[:2]) or "No concise evidence summary extracted."


def _first_value(items, key):
    for item in items:
        if item.get(key):
            return item[key]
    return "Analyst review required."


def _quantified_facts(items):
    facts = []
    for item in items:
        for fact in item.get("quantified_facts", []):
            if fact not in facts:
                facts.append(fact)
    return facts[:10]
