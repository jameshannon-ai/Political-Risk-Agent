ILLUSTRATIVE_INPUT_CAVEAT = "Illustrative cost inputs requiring operator validation unless replaced by operator-provided values."


def evaluate_hormuz_route_decision(
    sanctions_red_flag,
    war_risk_premium_pct,
    vessel_value,
    direct_voyage_cost,
    delay_days,
    delay_cost_per_day,
    reroute_extra_days,
    reroute_cost_per_day,
    ais_disruption_level,
    vessel_flow_status,
    detention_risk,
    insurance_cover_status,
    official_guidance_status,
):
    war_risk_cost = float(vessel_value) * float(war_risk_premium_pct)
    direct_total_cost = float(direct_voyage_cost) + war_risk_cost
    delay_total_cost = direct_total_cost + (float(delay_days) * float(delay_cost_per_day))
    reroute_total_cost = float(direct_voyage_cost) + (float(reroute_extra_days) * float(reroute_cost_per_day))

    legal_hold_required = bool(sanctions_red_flag is True)
    sanctions_unclear = sanctions_red_flag == "unclear"
    ais_high = ais_disruption_level == "high"
    severe_flow = vessel_flow_status == "severely_disrupted"
    disrupted_flow = vessel_flow_status == "disrupted"
    detention_high = detention_risk == "high"
    detention_low_or_medium = detention_risk in {"low", "medium"}
    insurance_confirmed = insurance_cover_status == "confirmed"
    insurance_excluded = insurance_cover_status == "excluded"
    guidance_supportive = official_guidance_status == "normal"

    transit_allowed_conditionally = (
        not legal_hold_required
        and not sanctions_unclear
        and insurance_confirmed
        and detention_low_or_medium
        and vessel_flow_status == "normalising"
        and not ais_high
        and guidance_supportive
    )

    option_ranking = [
        _option_row("Direct transit", direct_total_cost, legal_risk=_legal_risk(sanctions_red_flag), insurance_risk=_insurance_risk(insurance_cover_status, war_risk_premium_pct), operational_risk=_operational_risk(ais_disruption_level, vessel_flow_status, detention_risk), decision="Review"),
        _option_row("Delay / wait", delay_total_cost, legal_risk="Moderate" if sanctions_unclear else "Low", insurance_risk="Moderate", operational_risk="Moderate" if severe_flow or disrupted_flow else "Low", decision="Review"),
        _option_row("Reroute", reroute_total_cost, legal_risk="Low" if sanctions_red_flag is False else "Moderate", insurance_risk="Lower than direct transit", operational_risk="Moderate", decision="Review"),
        _option_row("Legal hold", 0.0, legal_risk="Control action", insurance_risk="Preserves cover position", operational_risk="Stops sailing until cleared", decision="Escalate"),
    ]

    preferred_option = _preferred_option(
        legal_hold_required=legal_hold_required,
        sanctions_unclear=sanctions_unclear,
        insurance_excluded=insurance_excluded,
        direct_total_cost=direct_total_cost,
        delay_total_cost=delay_total_cost,
        reroute_total_cost=reroute_total_cost,
        severe_flow=severe_flow,
        disrupted_flow=disrupted_flow,
        detention_high=detention_high,
        ais_high=ais_high,
        transit_allowed_conditionally=transit_allowed_conditionally,
    )

    option_ranking = _set_option_decisions(option_ranking, preferred_option, transit_allowed_conditionally, legal_hold_required)

    return {
        "preferred_option": preferred_option,
        "option_ranking": option_ranking,
        "legal_hold_required": legal_hold_required,
        "transit_allowed_conditionally": transit_allowed_conditionally,
        "insurance_break_even": {
            "war_risk_cost": round(war_risk_cost, 2),
            "direct_total_cost": round(direct_total_cost, 2),
            "delay_total_cost": round(delay_total_cost, 2),
            "reroute_total_cost": round(reroute_total_cost, 2),
            "premium_pct_break_even_vs_reroute": round(_break_even_pct(float(vessel_value), reroute_total_cost - float(direct_voyage_cost)), 6),
            "premium_pct_break_even_vs_delay": round(_break_even_pct(float(vessel_value), delay_total_cost - float(direct_voyage_cost)), 6),
            "illustrative_caveat": ILLUSTRATIVE_INPUT_CAVEAT,
        },
        "decision_rationale": _decision_rationale(
            preferred_option,
            legal_hold_required,
            insurance_excluded,
            detention_high,
            severe_flow,
            ais_high,
            direct_total_cost,
            reroute_total_cost,
        ),
        "relaxation_triggers": [
            "Official guidance returns to normal and no new transit-control warnings are issued.",
            "War-risk cover is confirmed on acceptable terms and not subject to exclusion or withdrawal.",
            "AIS disruption falls to low or medium and vessel-flow signals move from disrupted to normalising.",
            "No toll, safe-passage, offset, swap, guarantee or in-kind payment demand is present.",
            "Detention risk is no higher than medium and compliance review clears the voyage.",
        ],
        "escalation_triggers": [
            "Any safe-passage payment, toll, offset, swap, guarantee or in-kind arrangement is requested.",
            "Insurance cover is excluded, withdrawn or only available on uneconomic terms.",
            "AIS disruption is high or vessel-flow status is severely disrupted.",
            "Detention risk remains high or official guidance shifts to enhanced warning or restrictive.",
            "Direct transit becomes more expensive than reroute after war-risk premium is included.",
        ],
    }


def _preferred_option(
    legal_hold_required,
    sanctions_unclear,
    insurance_excluded,
    direct_total_cost,
    delay_total_cost,
    reroute_total_cost,
    severe_flow,
    disrupted_flow,
    detention_high,
    ais_high,
    transit_allowed_conditionally,
):
    if legal_hold_required:
        return "Legal hold"
    if insurance_excluded:
        return "Reroute" if reroute_total_cost <= delay_total_cost else "Delay / wait"
    if detention_high and severe_flow:
        return "Delay / wait" if delay_total_cost <= reroute_total_cost else "Reroute"
    if reroute_total_cost < direct_total_cost:
        return "Reroute"
    if ais_high or sanctions_unclear or disrupted_flow:
        return "Delay / wait" if delay_total_cost <= reroute_total_cost else "Reroute"
    if transit_allowed_conditionally:
        return "Conditional transit"
    return "Delay / wait" if delay_total_cost <= reroute_total_cost else "Reroute"


def _option_row(option, estimated_cost, legal_risk, insurance_risk, operational_risk, decision):
    return {
        "option": option,
        "estimated_cost": round(float(estimated_cost), 2),
        "legal_sanctions_risk": legal_risk,
        "insurance_risk": insurance_risk,
        "operational_risk": operational_risk,
        "decision": decision,
    }


def _set_option_decisions(rows, preferred_option, transit_allowed_conditionally, legal_hold_required):
    label_map = {
        "Legal hold": "Legal hold",
        "Conditional transit": "Direct transit",
        "Delay / wait": "Delay / wait",
        "Reroute": "Reroute",
    }
    preferred_label = label_map.get(preferred_option, preferred_option)
    updated = []
    for row in rows:
        decision = "Not preferred"
        if row["option"] == preferred_label:
            decision = "Preferred"
        if row["option"] == "Direct transit" and transit_allowed_conditionally:
            decision = "Preferred with conditions"
        if row["option"] == "Legal hold" and legal_hold_required:
            decision = "Required"
        updated.append({**row, "decision": decision})
    return updated


def _break_even_pct(vessel_value, war_risk_cost):
    if vessel_value <= 0:
        return 0.0
    return max(0.0, war_risk_cost / vessel_value)


def _legal_risk(sanctions_red_flag):
    if sanctions_red_flag is True:
        return "High"
    if sanctions_red_flag == "unclear":
        return "Medium-high"
    return "Low"


def _insurance_risk(insurance_cover_status, war_risk_premium_pct):
    if insurance_cover_status == "excluded":
        return "Excluded"
    if insurance_cover_status == "unclear":
        return "Unclear"
    if float(war_risk_premium_pct) >= 0.02:
        return "High cost"
    return "Confirmed"


def _operational_risk(ais_disruption_level, vessel_flow_status, detention_risk):
    if detention_risk == "high" and vessel_flow_status == "severely_disrupted":
        return "High"
    if ais_disruption_level == "high" or vessel_flow_status == "disrupted":
        return "Medium-high"
    return "Medium" if detention_risk == "medium" else "Low"


def _decision_rationale(preferred_option, legal_hold_required, insurance_excluded, detention_high, severe_flow, ais_high, direct_total_cost, reroute_total_cost):
    reasons = []
    if legal_hold_required:
        reasons.append("Sanctions red flags force legal/compliance hold regardless of route economics.")
    if insurance_excluded:
        reasons.append("Transit cannot be preferred when war-risk cover is excluded.")
    if detention_high and severe_flow:
        reasons.append("High detention risk and severely disrupted vessel flows make direct transit operationally unacceptable.")
    if reroute_total_cost < direct_total_cost:
        reasons.append("War-risk pricing makes reroute cheaper than direct transit.")
    if ais_high:
        reasons.append("High AIS disruption requires compliance review before any transit option can proceed.")
    if not reasons:
        reasons.append(f"{preferred_option} is preferred after comparing sanctions, insurance and delay-cost trade-offs.")
    return " ".join(reasons)
