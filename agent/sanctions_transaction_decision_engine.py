def evaluate_sanctions_transaction_decision(
    goods_control_risk="medium",
    counterparty_risk="medium",
    jurisdiction_route_risk="medium",
    documentation_quality="adequate",
    ownership_transparency="partial",
    licence_or_authorisation_status="unclear",
    payment_red_flag="unclear",
    vessel_or_logistics_red_flag="unclear",
    end_use_red_flag="unclear",
    sanctioned_counterparty_confirmed=False,
    prohibited_end_use_confirmed=False,
    transaction_specific_data_available=False,
):
    legal_hold_required = False
    rejection_triggered = False
    escalation_required = False
    reasons = []

    if sanctioned_counterparty_confirmed or prohibited_end_use_confirmed:
        rejection_triggered = True
        legal_hold_required = True
        escalation_required = True
        reasons.append("Confirmed sanctioned counterparty or prohibited end-use blocks routine approval.")

    if goods_control_risk == "high" and licence_or_authorisation_status in {"absent", "unclear"}:
        legal_hold_required = True
        escalation_required = True
        reasons.append("High goods/end-use risk without confirmed licence or authorisation requires legal hold.")

    if documentation_quality in {"missing", "weak"}:
        escalation_required = True
        reasons.append("Missing or weak documents prevent routine approval.")
        if documentation_quality == "missing":
            legal_hold_required = True

    if ownership_transparency in {"unclear", "partial"} or counterparty_risk in {"medium", "high"}:
        escalation_required = True
        reasons.append("Counterparty or ownership exposure is not clean enough for routine approval.")

    if jurisdiction_route_risk == "high" or vessel_or_logistics_red_flag is True:
        escalation_required = True
        reasons.append("Route, vessel or logistics red flags require sanctions/compliance review.")

    if payment_red_flag is True:
        legal_hold_required = True
        escalation_required = True
        reasons.append("Payment red flag requires legal hold until cleared.")

    if end_use_red_flag is True:
        legal_hold_required = True
        escalation_required = True
        reasons.append("End-use red flag requires legal hold until cleared.")
    elif end_use_red_flag == "unclear":
        escalation_required = True
        reasons.append("Unclear end-use requires enhanced due diligence.")

    recommended_decision = "approve with enhanced due diligence"
    if rejection_triggered:
        recommended_decision = "reject / legal hold"
    elif legal_hold_required:
        recommended_decision = "legal hold"
    elif escalation_required:
        recommended_decision = "escalate to sanctions/compliance review"
    elif _all_core_checks_clean(
        goods_control_risk,
        counterparty_risk,
        jurisdiction_route_risk,
        documentation_quality,
        ownership_transparency,
        licence_or_authorisation_status,
        payment_red_flag,
        vessel_or_logistics_red_flag,
        end_use_red_flag,
    ):
        recommended_decision = "approve"

    missing_documents = _missing_documents(
        documentation_quality,
        ownership_transparency,
        licence_or_authorisation_status,
        payment_red_flag,
        vessel_or_logistics_red_flag,
        end_use_red_flag,
    )
    confidence_score = 4 if transaction_specific_data_available else 3
    if documentation_quality in {"missing", "weak"} or ownership_transparency == "unclear":
        confidence_score = min(confidence_score, 3)

    return {
        "recommended_decision": recommended_decision,
        "escalation_required": escalation_required,
        "legal_hold_required": legal_hold_required,
        "rejection_triggered": rejection_triggered,
        "due_diligence_actions": _due_diligence_actions(),
        "missing_documents": missing_documents,
        "confidence_score": confidence_score,
        "decision_rationale": reasons or ["All core checks appear clean on the supplied inputs."],
        "refresh_triggers": [
            "Refresh if sanctions designations, OFSI guidance or export-control rules change.",
            "Refresh if goods classification, licence position or end-use statement changes.",
            "Refresh if counterparty ownership, payment route, vessel or logistics data changes.",
        ],
    }


def _all_core_checks_clean(
    goods_control_risk,
    counterparty_risk,
    jurisdiction_route_risk,
    documentation_quality,
    ownership_transparency,
    licence_or_authorisation_status,
    payment_red_flag,
    vessel_or_logistics_red_flag,
    end_use_red_flag,
):
    return all(
        [
            goods_control_risk == "low",
            counterparty_risk == "low",
            jurisdiction_route_risk == "low",
            documentation_quality == "strong",
            ownership_transparency == "clear",
            licence_or_authorisation_status == "confirmed",
            payment_red_flag is False,
            vessel_or_logistics_red_flag is False,
            end_use_red_flag is False,
        ]
    )


def _missing_documents(
    documentation_quality,
    ownership_transparency,
    licence_or_authorisation_status,
    payment_red_flag,
    vessel_or_logistics_red_flag,
    end_use_red_flag,
):
    missing = []
    if documentation_quality in {"missing", "weak"}:
        missing.extend(["invoice pack", "bills of lading", "contracts", "end-user statement"])
    if ownership_transparency in {"partial", "unclear"}:
        missing.append("beneficial ownership declaration")
    if licence_or_authorisation_status in {"absent", "unclear"}:
        missing.append("licence, authorisation or exemption evidence")
    if payment_red_flag in {True, "unclear"}:
        missing.append("bank/intermediary/payment route confirmation")
    if vessel_or_logistics_red_flag in {True, "unclear"}:
        missing.append("vessel, port and logistics route evidence")
    if end_use_red_flag in {True, "unclear"}:
        missing.append("end-use and end-user statement")
    return list(dict.fromkeys(missing))


def _due_diligence_actions():
    return [
        "Classify goods and check whether they are controlled, dual-use or sanctions-sensitive.",
        "Screen buyer, seller, consignee, banks, intermediaries and beneficial owners.",
        "Validate end-use, end-user and diversion risk with supporting documents.",
        "Confirm licence, authorisation or exemption status before approval or drawdown.",
        "Check payment route, correspondent bank exposure and blocked-payment risk.",
        "Validate ports, vessel, transshipment and logistics route before financing.",
        "Escalate unresolved red flags to sanctions/compliance and legal sign-off.",
    ]
