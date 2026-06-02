def build_critical_minerals_model(
    inventory_runway_days=45,
    alternative_supplier_qualification_days=180,
    china_linked_supply_share_pct=70,
    exposed_product_line_revenue_gbp=50_000_000,
    substitution_difficulty="high",
    customer_delivery_criticality="high",
):
    continuity_gap = alternative_supplier_qualification_days - inventory_runway_days
    recommended_actions = []

    if inventory_runway_days < alternative_supplier_qualification_days:
        recommended_actions.append("Stockpile")
    if china_linked_supply_share_pct >= 60 and substitution_difficulty == "high":
        recommended_actions.append("Qualify alternative supplier")
    if substitution_difficulty in {"medium", "plausible"}:
        recommended_actions.append("Redesign input")
    if customer_delivery_criticality == "high":
        recommended_actions.append("Allocate scarce inventory")
    if continuity_gap > 0 and substitution_difficulty == "high":
        recommended_actions.append("Production hold")

    preferred = _preferred_action(
        continuity_gap=continuity_gap,
        substitution_difficulty=substitution_difficulty,
        customer_delivery_criticality=customer_delivery_criticality,
        china_linked_supply_share_pct=china_linked_supply_share_pct,
    )

    return {
        "inventory_runway_days": inventory_runway_days,
        "alternative_supplier_qualification_days": alternative_supplier_qualification_days,
        "production_continuity_gap_days": continuity_gap,
        "china_linked_supply_share_pct": china_linked_supply_share_pct,
        "exposed_product_line_revenue_gbp": exposed_product_line_revenue_gbp,
        "substitution_difficulty": substitution_difficulty,
        "customer_delivery_criticality": customer_delivery_criticality,
        "recommended_actions": recommended_actions,
        "preferred_action": preferred,
        "decision_implication": _decision_implication(continuity_gap, substitution_difficulty, customer_delivery_criticality),
    }


def _preferred_action(continuity_gap, substitution_difficulty, customer_delivery_criticality, china_linked_supply_share_pct):
    if continuity_gap > 0 and substitution_difficulty == "high" and customer_delivery_criticality == "high":
        return "Stockpile now, qualify alternative supplier, and prepare inventory allocation / production hold contingency."
    if continuity_gap > 0 and china_linked_supply_share_pct >= 60:
        return "Qualify alternative supplier and build targeted stockpile."
    if substitution_difficulty in {"medium", "plausible"}:
        return "Redesign input while qualifying alternative supply."
    return "Continue with current supplier base while monitoring concentration and export-control triggers."


def _decision_implication(continuity_gap, substitution_difficulty, customer_delivery_criticality):
    if continuity_gap <= 0:
        return "Inventory runway is not currently shorter than qualification time, so continuity risk is more manageable if supply remains physically available."
    if substitution_difficulty == "high" and customer_delivery_criticality == "high":
        return "Qualification lag exceeds inventory runway, so the manufacturer should treat disruption as a production-continuity problem rather than a procurement inconvenience."
    return "Qualification lag exceeds inventory runway, so mitigation action is needed before the sourcing model can be treated as resilient."
