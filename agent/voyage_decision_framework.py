def build_voyage_decision_framework(evidence_pack, route_cost_assessment):
    sanctions_hits = [
        item["source_id"]
        for item in evidence_pack.get("evidence", [])
        if item.get("requirement_name") == "sanctions_and_safe_passage_payment_risk"
    ]
    transit_control_hits = [
        item["source_id"]
        for item in evidence_pack.get("evidence", [])
        if item.get("requirement_name") in {"official_maritime_security", "transit_control_or_constabulary_actions"}
    ]
    ais_hits = [
        item["source_id"]
        for item in evidence_pack.get("evidence", [])
        if item.get("requirement_name") == "vessel_flow_and_AIS_behaviour"
    ]
    insurance_hits = [
        item["source_id"]
        for item in evidence_pack.get("evidence", [])
        if item.get("requirement_name") == "war_risk_insurance_pricing"
    ]

    compliance_escalation_required = bool(sanctions_hits)
    operating_stance = (
        "Escalate Hormuz-linked voyages for operational, insurance and sanctions review before transit"
        if transit_control_hits or compliance_escalation_required
        else "Transit can proceed with enhanced monitoring"
    )
    transit_option = "Use only when official guidance, insurance cover and sanctions position are clear."
    delay_option = "Use when direct transit is uncertain but time-limited clarification is plausible."
    reroute_option = "Use when sanctions, detention, AIS or insurance risks materially outweigh direct-route savings."

    return {
        "operating_stance": operating_stance,
        "transit_option": transit_option,
        "delay_option": delay_option,
        "reroute_option": reroute_option,
        "compliance_escalation_required": compliance_escalation_required,
        "sanctions_red_flags": _sanctions_red_flags(sanctions_hits),
        "insurance_cost_pressure": "High" if insurance_hits else "Moderate",
        "route_cost_pressure": "High" if route_cost_assessment["preferred_option"] != "Transit" else "Moderate",
        "crew_safety_pressure": "High" if transit_control_hits or ais_hits else "Moderate",
        "decision_triggers": [
            "Updated official maritime guidance supports transit.",
            "War-risk cover, additional premium and exclusions are confirmed.",
            "No safe-passage payment, guarantee or sanctions-sensitive coordination demand is present.",
            "Vessel-flow and AIS behaviour show practical recovery rather than headline-only de-escalation.",
        ],
        "relaxation_triggers": [
            "Official guidance improves and no new detention or transit-control warnings are issued.",
            "Insurers maintain cover without withdrawal or prohibitive repricing.",
            "Vessel-flow recovery and cleaner AIS behaviour persist across multiple updates.",
            "Legal/compliance review confirms no sanctions red flags from passage demands or counterparties.",
        ],
    }


def _sanctions_red_flags(sanctions_hits):
    flags = [
        "Any toll or safe-passage payment demand.",
        "Digital asset, offset, swap, guarantee or in-kind passage arrangement.",
        "Unclear Iranian counterparty, intermediary or coordination instruction.",
    ]
    if sanctions_hits:
        flags.append("Evidence pack contains sanctions-linked source coverage requiring legal/compliance review.")
    return flags
