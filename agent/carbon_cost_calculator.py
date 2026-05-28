DEFAULT_EMISSION_FACTORS = {
    "MGO": 3.206,
    "MDO": 3.206,
    "HFO": 3.114,
    "LNG": 2.75,
}


def calculate_carbon_cost(
    gross_tonnage,
    route_name,
    route_type,
    fuel_type,
    fuel_consumption_tonnes_per_voyage,
    voyages_per_week,
    uka_price_per_tonne,
    coverage_rate,
    reporting_period_months,
    vessel_name="",
):
    factor, factor_note = _emission_factor(fuel_type)
    applicability = _applicability(gross_tonnage, route_type)
    estimated_tco2e_per_voyage = float(fuel_consumption_tonnes_per_voyage) * factor
    cost_per_voyage = estimated_tco2e_per_voyage * float(coverage_rate) * float(uka_price_per_tonne)
    weekly_cost = cost_per_voyage * float(voyages_per_week)
    monthly_cost = weekly_cost * 4.345
    annualised_cost = monthly_cost * 12
    sensitivity = _sensitivity(estimated_tco2e_per_voyage, float(coverage_rate), float(uka_price_per_tonne))

    return {
        "vessel_name": vessel_name,
        "gross_tonnage": gross_tonnage,
        "route_name": route_name,
        "route_type": route_type,
        "applies_to_uk_ets": applicability["status"],
        "applicability_reason": applicability["reason"],
        "estimated_tco2e_per_voyage": round(estimated_tco2e_per_voyage, 3),
        "estimated_carbon_cost_per_voyage": round(cost_per_voyage, 2),
        "weekly_carbon_cost": round(weekly_cost, 2),
        "monthly_carbon_cost": round(monthly_cost, 2),
        "annualised_carbon_cost": round(annualised_cost, 2),
        "uka_price_sensitivity": sensitivity,
        "compliance_timeline": _compliance_timeline(route_type, reporting_period_months),
        "caveats": [
            factor_note,
            "Illustrative voyage assumptions requiring operator validation.",
        ],
    }


def _emission_factor(fuel_type):
    factor = DEFAULT_EMISSION_FACTORS.get(fuel_type.upper(), DEFAULT_EMISSION_FACTORS["MGO"])
    return factor, f"Using default emission factor {factor} tCO2e per tonne of {fuel_type.upper()} fuel; review against current verified methodology."


def _applicability(gross_tonnage, route_type):
    if float(gross_tonnage) < 5000:
        return {"status": False, "reason": "Below the confirmed 5,000 GT threshold for first-stage UK ETS maritime scope."}
    if route_type == "uk_international" or route_type == "scenario_only":
        return {"status": "scenario", "reason": "UK-international voyages should be treated as future/scenario exposure unless confirmed in scope by later policy."}
    if route_type == "offshore":
        return {"status": "scenario", "reason": "Offshore ships are delayed beyond the first-stage July 2026 domestic scope and should be treated as later-scope exposure here."}
    if route_type == "gb_ni":
        return {"status": True, "reason": "Voyages between Great Britain and Northern Ireland are treated as in scope with partial coverage in current implementation guidance."}
    if route_type in {"domestic_uk", "at_berth"}:
        return {"status": True, "reason": "Domestic UK voyages and at-berth emissions for ships 5,000 GT and above fall within confirmed first-stage UK ETS maritime scope from 1 July 2026."}
    return {"status": "scenario", "reason": "Route type requires manual scope confirmation."}


def _sensitivity(estimated_tco2e_per_voyage, coverage_rate, uka_price):
    points = []
    for label, price in [
        ("UKA -20%", uka_price * 0.8),
        ("UKA base", uka_price),
        ("UKA +20%", uka_price * 1.2),
    ]:
        points.append(
            {
                "label": label,
                "uka_price_per_tonne": round(price, 2),
                "estimated_cost_per_voyage": round(estimated_tco2e_per_voyage * coverage_rate * price, 2),
            }
        )
    return points


def _compliance_timeline(route_type, reporting_period_months):
    if route_type in {"uk_international", "scenario_only", "offshore"}:
        return "Current route is treated as scenario exposure; monitor future scope decisions before setting surrender assumptions."
    if int(reporting_period_months) <= 6:
        return "Verified emissions report due by 31 March following the scheme year; first two maritime surrender years can use the one-off 30 April 2028 double-surrender window."
    return "Verified annual emissions report due by 31 March following the scheme year; allowance surrender deadline is 30 April following the scheme year unless a specific transitional window applies."
