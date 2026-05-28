ILLUSTRATIVE_CAVEAT = "Illustrative voyage assumptions requiring operator validation."


def assess_route_cost(
    route_name,
    direct_transit_allowed,
    estimated_direct_voyage_days,
    estimated_reroute_days,
    daily_vessel_cost,
    bunker_cost_per_day,
    war_risk_premium_direct,
    war_risk_premium_reroute,
    demurrage_or_delay_cost_per_day,
    sanctions_risk_flag,
    compliance_hold_days,
):
    direct_days = float(estimated_direct_voyage_days)
    reroute_days = float(estimated_reroute_days)
    vessel_daily = float(daily_vessel_cost)
    bunker_daily = float(bunker_cost_per_day)
    direct_premium = float(war_risk_premium_direct)
    reroute_premium = float(war_risk_premium_reroute)
    delay_daily = float(demurrage_or_delay_cost_per_day)
    hold_days = float(compliance_hold_days)

    direct_route_estimated_cost = _voyage_cost(direct_days, vessel_daily, bunker_daily, direct_premium)
    reroute_estimated_cost = _voyage_cost(reroute_days, vessel_daily, bunker_daily, reroute_premium)
    delay_estimated_cost = (
        direct_route_estimated_cost
        + (delay_daily + vessel_daily + bunker_daily) * hold_days
    )

    sanctions_adjusted_decision = _sanctions_adjusted_decision(direct_transit_allowed, sanctions_risk_flag)
    preferred_option = _preferred_option(
        direct_transit_allowed,
        sanctions_risk_flag,
        direct_route_estimated_cost,
        reroute_estimated_cost,
        delay_estimated_cost,
    )

    return {
        "route_name": route_name,
        "direct_route_estimated_cost": round(direct_route_estimated_cost, 2),
        "reroute_estimated_cost": round(reroute_estimated_cost, 2),
        "delay_estimated_cost": round(delay_estimated_cost, 2),
        "incremental_reroute_cost": round(reroute_estimated_cost - direct_route_estimated_cost, 2),
        "incremental_delay_cost": round(delay_estimated_cost - direct_route_estimated_cost, 2),
        "sanctions_adjusted_decision": sanctions_adjusted_decision,
        "preferred_option": preferred_option,
        "caveat": ILLUSTRATIVE_CAVEAT,
    }


def _voyage_cost(days, daily_vessel_cost, bunker_cost_per_day, premium):
    return (days * daily_vessel_cost) + (days * bunker_cost_per_day) + premium


def _sanctions_adjusted_decision(direct_transit_allowed, sanctions_risk_flag):
    if sanctions_risk_flag:
        return "Direct transit is not acceptable until legal/compliance review clears sanctions risk."
    if direct_transit_allowed is False:
        return "Direct transit is operationally blocked; compare reroute versus delay."
    if direct_transit_allowed == "uncertain":
        return "Direct transit remains uncertain; hold or reroute pending operational and legal confirmation."
    return "Direct transit can be compared commercially, subject to safety and insurance review."


def _preferred_option(direct_transit_allowed, sanctions_risk_flag, direct_cost, reroute_cost, delay_cost):
    if sanctions_risk_flag:
        return "Escalate / legal hold"
    if direct_transit_allowed is False:
        return "Reroute" if reroute_cost <= delay_cost else "Delay / wait"
    if direct_transit_allowed == "uncertain":
        return "Delay / wait" if delay_cost <= reroute_cost else "Reroute"
    cheapest = min(
        [("Transit", direct_cost), ("Delay / wait", delay_cost), ("Reroute", reroute_cost)],
        key=lambda item: item[1],
    )
    return cheapest[0]
