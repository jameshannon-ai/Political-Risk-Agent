def build_cyber_business_interruption_model(
    expected_outage_days=5,
    maximum_tolerable_downtime_days=2,
    daily_revenue_at_risk=2_000_000,
    insurance_waiting_period_hours=24,
    customer_harm_severity="high",
    regulatory_notification_trigger="source-supported where applicable",
):
    business_interruption_exposure = expected_outage_days * daily_revenue_at_risk
    resilience_gap_days = maximum_tolerable_downtime_days - expected_outage_days
    waiting_period_days = insurance_waiting_period_hours / 24

    decisions = []
    if expected_outage_days > maximum_tolerable_downtime_days:
        decisions.extend(
            [
                "activate incident response",
                "switch to manual contingency where viable",
                "prioritise system restoration",
                "increase resilience investment",
            ]
        )
    if expected_outage_days >= waiting_period_days:
        decisions.append("trigger cyber insurance claim process")
    if customer_harm_severity == "high" or regulatory_notification_trigger:
        decisions.append("escalate regulatory/customer notification review")

    return {
        "expected_outage_days": expected_outage_days,
        "maximum_tolerable_downtime_days": maximum_tolerable_downtime_days,
        "daily_revenue_at_risk": daily_revenue_at_risk,
        "business_interruption_exposure": business_interruption_exposure,
        "resilience_gap_days": resilience_gap_days,
        "insurance_waiting_period_hours": insurance_waiting_period_hours,
        "customer_harm_severity": customer_harm_severity,
        "regulatory_notification_trigger": regulatory_notification_trigger,
        "decision_implication": "; ".join(dict.fromkeys(decisions)),
        "scenario_inputs": {
            "expected_outage": {
                "value": f"{expected_outage_days} days",
                "label": "illustrative",
            },
            "maximum_tolerable_downtime": {
                "value": f"{maximum_tolerable_downtime_days} days",
                "label": "illustrative",
            },
            "resilience_gap": {
                "value": f"{resilience_gap_days} days",
                "label": "derived",
            },
            "daily_revenue_at_risk": {
                "value": f"GBP{daily_revenue_at_risk:,.0f}",
                "label": "illustrative",
            },
            "gross_revenue_disruption": {
                "value": f"GBP{business_interruption_exposure:,.0f}",
                "label": "derived",
            },
            "insurance_waiting_period": {
                "value": f"{insurance_waiting_period_hours} hours",
                "label": "illustrative",
            },
            "regulatory_notification_trigger": {
                "value": regulatory_notification_trigger,
                "label": "source-supported",
            },
            "customer_harm_service_disruption_severity": {
                "value": customer_harm_severity,
                "label": "illustrative",
            },
            "company_specific_recovery_data": {
                "value": "RTO/RPO, systems map, backup capability, supplier dependency and incident facts required",
                "label": "company-provided",
            },
        },
    }
