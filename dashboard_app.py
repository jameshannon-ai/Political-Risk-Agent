from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard_helpers import (
    build_selected_source_rows,
    extract_markdown_section,
    extract_markdown_table,
    get_nested_value,
    load_json,
    load_markdown,
    parse_first_number,
)


ROOT = Path(__file__).resolve().parent
SHOWCASE = ROOT / "showcase"
UK_ETS_PACK = SHOWCASE / "uk_ets_evidence_pack.json"
UK_ETS_BRIEF = SHOWCASE / "uk_ets_shipping_operator_brief.md"
UK_ETS_AUDIT = SHOWCASE / "uk_ets_source_audit.md"
HORMUZ_PACK = SHOWCASE / "hormuz_evidence_pack.json"
HORMUZ_BRIEF = SHOWCASE / "hormuz_shipping_operator_brief.md"
HORMUZ_AUDIT = SHOWCASE / "hormuz_source_audit.md"
CRITICAL_MINERALS_PACK = SHOWCASE / "critical_minerals_evidence_pack.json"
CRITICAL_MINERALS_BRIEF = SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md"
CRITICAL_MINERALS_AUDIT = SHOWCASE / "critical_minerals_source_audit.md"
SANCTIONS_PACK = SHOWCASE / "sanctions_evidence_pack.json"
SANCTIONS_BRIEF = SHOWCASE / "sanctions_trade_finance_exposure_brief.md"
SANCTIONS_AUDIT = SHOWCASE / "sanctions_source_audit.md"

CASES = {
    "UK ETS Maritime Expansion": {
        "brief": UK_ETS_BRIEF,
        "audit": UK_ETS_AUDIT,
        "pack": UK_ETS_PACK,
        "title": "UK ETS Maritime Expansion: Carbon Cost Exposure",
        "description": "Source-audited political risk workflow converting UK ETS maritime policy into operator-relevant carbon cost exposure, route applicability, risk scoring and review controls.",
    },
    "Hormuz Route Decision Engine": {
        "brief": HORMUZ_BRIEF,
        "audit": HORMUZ_AUDIT,
        "pack": HORMUZ_PACK,
        "title": "Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs",
        "description": "Trigger-based shipping-operator decision workflow for transit, delay, reroute or legal hold across sanctions, insurance, AIS/vessel-flow and detention risk conditions.",
    },
    "Critical Minerals Exposure Engine": {
        "brief": CRITICAL_MINERALS_BRIEF,
        "audit": CRITICAL_MINERALS_AUDIT,
        "pack": CRITICAL_MINERALS_PACK,
        "title": "Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers",
        "description": "Production-continuity decision workflow for stockpile, alternative supplier qualification, redesign, customer allocation and production-hold decisions under rare earth magnet supply disruption.",
    },
    "Sanctions Trade Finance Exposure Engine": {
        "brief": SANCTIONS_BRIEF,
        "audit": SANCTIONS_AUDIT,
        "pack": SANCTIONS_PACK,
        "title": "Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk",
        "description": "Transaction decision workflow for approve, enhanced due diligence, escalation, legal hold or rejection under sanctions, end-use, counterparty, route, payment and documentation risk.",
    },
}


st.set_page_config(
    page_title="Political Risk Agent",
    page_icon="",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #f5f6f8;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1320px;
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #d8dde6;
        padding: 0.8rem 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    case_name = st.sidebar.radio("Cases", list(CASES.keys()))
    case = CASES[case_name]
    pack = load_json(case["pack"])
    brief = load_markdown(case["brief"])
    audit = load_markdown(case["audit"])

    st.title("Political Risk Agent")
    st.subheader("Source-audited political risk workflow for turning public/live evidence into decision-useful commercial risk outputs.")
    st.caption("This dashboard displays saved showcase artefacts only. It does not call Tavily or spend live-search credits.")
    st.markdown(
        """
        **Current showcase cases:**
        - UK ETS: regulatory policy into route-level carbon cost exposure
        - Hormuz: geopolitical/security risk into transit, delay, reroute or legal-hold decision
        - Critical Minerals: strategic competition into production-continuity risk
        - Sanctions Trade Finance: sanctions/export controls into transaction approval, escalation, legal hold or rejection

        The dashboard is designed as an expandable case portfolio. Future cases can be added using the same saved-showcase pattern.
        """
    )
    st.markdown(f"## {case['title']}")
    st.caption(case["description"])

    if case_name == "UK ETS Maritime Expansion":
        _render_uk_ets(pack, brief, audit)
    elif case_name == "Hormuz Route Decision Engine":
        _render_hormuz(pack, brief, audit)
    elif case_name == "Critical Minerals Exposure Engine":
        _render_critical_minerals(pack, brief, audit)
    else:
        _render_sanctions(pack, brief, audit)


def _render_uk_ets(pack, brief, audit):
    carbon_cost = _build_carbon_cost_metrics(pack, brief)
    overview = _build_uk_ets_overview_metrics(pack, brief, carbon_cost)
    _render_metrics(overview)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Operator Decision", "Carbon Cost", "Evidence & Scores", "Source Audit"]
    )

    with tab1:
        _render_markdown_table_section(brief, "1. Operator Stance")
        _render_markdown_table_section(brief, "2. Applicability Check")
        _render_text_section(brief, "3. Executive Judgement")
        _render_markdown_table_section(brief, "8. Decision Implications")
        _render_text_section(brief, "12. Recommended Actions")

    with tab2:
        st.markdown("### Source-confirmed policy inputs")
        st.dataframe(pd.DataFrame(carbon_cost["policy_inputs"]), use_container_width=True, hide_index=True)
        st.markdown("### Operator / illustrative assumptions")
        st.dataframe(pd.DataFrame(carbon_cost["assumptions"]), use_container_width=True, hide_index=True)
        st.markdown("### Market / manual inputs")
        st.dataframe(pd.DataFrame(carbon_cost["market_inputs"]), use_container_width=True, hide_index=True)
        st.markdown("### Derived cost outputs")
        st.dataframe(pd.DataFrame(carbon_cost["derived_outputs"]), use_container_width=True, hide_index=True)
        if carbon_cost["sensitivity"]:
            st.markdown("### UKA price sensitivity")
            st.dataframe(pd.DataFrame(carbon_cost["sensitivity"]), use_container_width=True, hide_index=True)

    with tab3:
        for heading in [
            "5. Risk Scorecard",
            "6. Quantified Evidence Readout",
            "7. Evidence-To-Score Bridge",
            "14. Source Requirement Coverage",
        ]:
            _render_markdown_table_section(brief, heading)

    with tab4:
        _render_source_audit_metrics(pack)
        _render_markdown_table_section(brief, "15. Source Quality Notes")
        _render_selected_sources(pack)
        st.markdown("### Refresh priorities")
        _render_refresh_df(pack)
        with st.expander("Full source audit", expanded=False):
            st.markdown(audit)


def _render_hormuz(pack, brief, audit):
    overview = _build_hormuz_overview_metrics(pack, brief)
    _render_metrics(overview)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Decision", "Route-Cost and Insurance", "Sanctions and Vessel Signals", "Evidence and Sources", "Full Brief / Source Audit"]
    )

    with tab1:
        _render_hormuz_decision_summary()
        _render_markdown_table_section(brief, "Dashboard Summary")
        with st.expander("Full decision recommendation", expanded=False):
            _render_markdown_table_section(brief, "1. Decision Recommendation")
        _render_text_section(brief, "3. Executive Judgement")
        with st.expander("Full route decision optimiser", expanded=False):
            _render_markdown_table_section(brief, "4. Route Decision Optimiser")

    with tab2:
        _render_markdown_table_section(brief, "5. Illustrative Route-Cost Scenario")
        _render_markdown_table_section(brief, "7. Insurance Break-Even Analysis")

    with tab3:
        _render_hormuz_trigger_summary()
        _render_markdown_table_section(brief, "6. Sanctions Red-Flag Assessment")
        _render_markdown_table_section(brief, "8. AIS and Vessel-Flow Signals")
        _render_markdown_table_section(brief, "13. Relaxation and Escalation Triggers")
        if not extract_markdown_section(brief, "13. Relaxation and Escalation Triggers"):
            _render_text_section(brief, "13. Relaxation and Escalation Triggers")

    with tab4:
        _render_hormuz_source_governance_summary()
        _render_markdown_table_section(brief, "9. Risk Scorecard")
        _render_markdown_table_section(brief, "10. Evidence-To-Score Bridge")
        _render_markdown_table_section(brief, "11. Source Requirement Coverage")
        _render_selected_sources(pack)
        with st.expander("Evidence Appendix", expanded=False):
            _render_markdown_table_section(brief, "14. Evidence Appendix")
        _render_markdown_table_section(brief, "15. Source Audit Summary")
        with st.expander("Full source audit", expanded=False):
            st.markdown(audit)

    with tab5:
        with st.expander("Full brief markdown", expanded=False):
            st.markdown(brief)
        _render_audit_detail_expanders(audit)
        with st.expander("Full source audit markdown", expanded=False):
            st.markdown(audit)


def _render_critical_minerals(pack, brief, audit):
    overview = _build_critical_minerals_overview_metrics(pack, brief)
    _render_metrics(overview)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Decision", "Production Continuity", "Mitigation Options", "Evidence and Sources", "Full Brief / Source Audit"]
    )

    with tab1:
        _render_critical_minerals_decision_summary()
        _render_markdown_table_section(brief, "3. Dashboard Summary")
        with st.expander("Full decision recommendation", expanded=False):
            _render_markdown_table_section(brief, "1. Decision Recommendation")
        _render_text_section(brief, "2. Scope and Specificity")
        _render_markdown_table_section(brief, "4. Exposure Summary")

    with tab2:
        _render_critical_minerals_continuity_summary()
        _render_markdown_table_section(brief, "5. Controlled Input Assessment")
        _render_markdown_table_section(brief, "6. Supplier Concentration Assessment")
        with st.expander("Full production continuity model", expanded=False):
            _render_markdown_table_section(brief, "7. Production Continuity Model")
            _render_markdown_table_section(brief, "8. Inventory Runway vs Supplier Qualification Gap")

    with tab3:
        _render_markdown_table_section(brief, "9. Mitigation Options")
        _render_critical_minerals_company_data_controls(brief)

    with tab4:
        _render_markdown_table_section(brief, "10. Risk Scorecard")
        _render_markdown_table_section(brief, "11. Evidence-To-Score Bridge")
        _render_markdown_table_section(brief, "12. Source Requirement Coverage")
        _render_markdown_table_section(brief, "13. Source Quality Notes")
        _render_selected_sources(pack)
        st.info(
            "Dashboard caveats: substitution feasibility needs stronger magnet-specific engineering or qualification evidence; "
            "market/pricing signal is directional, not a robust pricing benchmark; contrary/easing evidence is secondary and not an all-clear; "
            "company BOM, supplier ownership/country, inventory, contracts and qualification data are required before operational use."
        )
        with st.expander("Evidence Appendix", expanded=False):
            _render_markdown_table_section(brief, "14. Evidence Appendix")

    with tab5:
        with st.expander("Full brief markdown", expanded=False):
            st.markdown(brief)
        _render_audit_detail_expanders(audit)
        with st.expander("Full source audit markdown", expanded=False):
            st.markdown(audit)


def _render_sanctions(pack, brief, audit):
    overview = _build_sanctions_overview_metrics(pack, brief)
    _render_metrics(overview)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Decision", "Transaction Risk", "Decision Engine", "Evidence and Sources", "Full Brief / Source Audit"]
    )

    with tab1:
        _render_sanctions_decision_summary()
        _render_markdown_table_section(brief, "3. Dashboard Summary")
        _render_markdown_table_section(brief, "1. Decision Recommendation")
        _render_text_section(brief, "2. Scope and Specificity")
        _render_markdown_table_section(brief, "4. Transaction Exposure Summary")

    with tab2:
        _render_markdown_table_section(brief, "5. Goods and End-Use Risk Assessment")
        _render_markdown_table_section(brief, "6. Counterparty and Ownership Risk Assessment")
        _render_markdown_table_section(brief, "7. Jurisdiction, Route and Payment Risk Assessment")
        _render_markdown_table_section(brief, "8. Documentation Quality Assessment")

    with tab3:
        _render_markdown_table_section(brief, "9. Transaction Decision Engine")
        _render_text_section(brief, "10. Due Diligence Actions")
        _render_text_section(brief, "18. Methodology and Review Controls")

    with tab4:
        _render_markdown_table_section(brief, "11. Risk Scorecard")
        _render_markdown_table_section(brief, "12. Evidence-To-Score Bridge")
        _render_markdown_table_section(brief, "13. Source Requirement Coverage")
        _render_markdown_table_section(brief, "14. Source Quality Notes")
        _render_selected_sources(pack)
        with st.expander("Evidence Appendix", expanded=False):
            _render_markdown_table_section(brief, "16. Evidence Appendix")

    with tab5:
        with st.expander("Full brief markdown", expanded=False):
            st.markdown(brief)
        _render_audit_detail_expanders(audit)
        with st.expander("Full source audit markdown", expanded=False):
            st.markdown(audit)


def _render_metrics(overview):
    cols = st.columns(3)
    items = list(overview.items())
    for index, (label, value) in enumerate(items):
        with cols[index % 3]:
            st.metric(label, value)


def _render_markdown_table_section(markdown, heading):
    section = extract_markdown_section(markdown, heading)
    if not section:
        return
    label = heading.split(". ", 1)[1] if ". " in heading else heading
    st.markdown(f"### {label}")
    tables = extract_markdown_table(section)
    text_only = "\n".join(line for line in section.splitlines() if not line.startswith("|")).strip()
    if text_only:
        st.markdown(text_only)
    for table in tables:
        if table:
            st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)


def _render_text_section(markdown, heading):
    section = extract_markdown_section(markdown, heading)
    if section:
        label = heading.split(". ", 1)[1] if ". " in heading else heading
        st.markdown(f"### {label}")
        st.markdown(section)


def _render_source_audit_metrics(pack):
    cols = st.columns(4)
    summary_items = [
        ("Source provider", pack.get("source_provider", "")),
        ("Evidence mode", pack.get("evidence_mode", "")),
        ("Total queries run", pack.get("total_queries_run", 0)),
        ("Candidate sources", pack.get("candidate_count", 0)),
        ("Selected / rejected", f"{pack.get('selected_count', 0)} / {pack.get('rejected_count', 0)}"),
        ("Strongest sources", get_nested_value(pack, [["quantified_evidence_readout", "strongest_evidence"]], "")),
    ]
    for index, (label, value) in enumerate(summary_items):
        with cols[index % 4]:
            st.metric(label, value)


def _render_refresh_df(pack):
    refresh_df = pd.DataFrame(pack.get("refresh_priorities", []))
    if not refresh_df.empty:
        st.dataframe(refresh_df, use_container_width=True, hide_index=True)


def _render_selected_sources(pack):
    rows = build_selected_source_rows(pack)
    if not rows:
        return
    st.markdown("### Selected Sources")
    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
        column_config={"URL": st.column_config.LinkColumn("URL")},
    )


def _render_critical_minerals_company_data_controls(brief):
    section = extract_markdown_section(brief, "16. Methodology and Review Controls")
    if not section:
        return
    section = section.split("### Source Strategy", 1)[0].strip()
    st.markdown("### Company Data and Review Controls")
    st.markdown(section)


def _render_table(title, rows):
    st.markdown(f"### {title}")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_hormuz_decision_summary():
    _render_table(
        "Decision Summary",
        [
            {
                "Item": "Preferred option",
                "Value": "Legal hold if sanctions/payment trigger is present; otherwise delay/reroute until clearance",
            },
            {
                "Item": "Current stance",
                "Value": "Transit only after sanctions, insurance and operations clearance",
            },
            {
                "Item": "Legal trigger",
                "Value": "Any safe-passage, toll or payment-equivalent demand",
            },
            {
                "Item": "Reroute trigger",
                "Value": "Direct transit becomes more expensive than reroute after war-risk premium, or detention risk remains high",
            },
        ],
    )


def _render_hormuz_trigger_summary():
    _render_table(
        "Trigger Summary",
        [
            {"Trigger": "Safe-passage/toll/payment demand", "Decision effect": "Legal hold"},
            {"Trigger": "War-risk premium exceeds reroute break-even", "Decision effect": "Reroute"},
            {"Trigger": "AIS/vessel-flow remains disrupted", "Decision effect": "Delay or reroute"},
            {"Trigger": "Official guidance and insurer appetite normalise", "Decision effect": "Conditional transit"},
        ],
    )


def _render_hormuz_source_governance_summary():
    _render_table(
        "Source Governance Summary",
        [
            {
                "Evidence area": "Official maritime/security",
                "Status": "Gap / refresh required",
                "Dashboard caveat": "Refresh UKMTO, IMO, ICS, BIMCO or official advisory before operational use",
            },
            {
                "Evidence area": "Insurance pricing",
                "Status": "Stronger",
                "Dashboard caveat": "Refresh broker/market terms before voyage approval",
            },
            {
                "Evidence area": "Energy chokepoint",
                "Status": "Partial",
                "Dashboard caveat": "Direct EIA or equivalent official data preferred",
            },
            {
                "Evidence area": "De-escalation",
                "Status": "Weak / secondary",
                "Dashboard caveat": "Requires Reuters, AP, official or vessel-flow confirmation before relaxing controls",
            },
        ],
    )


def _render_critical_minerals_decision_summary():
    _render_table(
        "Decision Summary",
        [
            {
                "Item": "Recommendation",
                "Value": "Stockpile now, qualify alternative supplier, and prepare inventory allocation / production-hold contingency",
            },
            {
                "Item": "Current stance",
                "Value": "Heightened continuity controls rather than routine procurement",
            },
            {
                "Item": "Main metric",
                "Value": "Production continuity gap: 135 days",
            },
            {
                "Item": "Company data required",
                "Value": "BOM, supplier ownership/country, inventory, contracts and qualification status",
            },
        ],
    )


def _render_sanctions_decision_summary():
    _render_table(
        "Decision Summary",
        [
            {"Item": "Decision", "Value": "Legal hold or escalation until red flags are cleared"},
            {"Item": "Current stance", "Value": "Escalate or hold unresolved goods, ownership, route, payment or document risk"},
            {"Item": "Legal trigger", "Value": "Sanctioned party, prohibited end-use, unlicensed controlled goods or payment red flag"},
            {"Item": "Missing data", "Value": "Goods, counterparties, ownership, route, payment, licence and documents"},
        ],
    )


def _render_critical_minerals_continuity_summary():
    _render_table(
        "Continuity Summary",
        [
            {"Metric": "Inventory runway", "Value": "45 days", "Meaning": "Time before stock exhaustion"},
            {"Metric": "Supplier qualification", "Value": "180 days", "Meaning": "Time to approve alternative supply"},
            {"Metric": "Continuity gap", "Value": "135 days", "Meaning": "Period where production may be exposed"},
        ],
    )


def _render_audit_detail_expanders(audit):
    for heading in ["Search Configuration", "Source Strategy", "Rejected Sources"]:
        section = extract_markdown_section(audit, heading)
        if section:
            with st.expander(heading, expanded=False):
                st.markdown(section)


def _build_uk_ets_overview_metrics(pack, brief, carbon_cost):
    return {
        "Risk": "Medium-High",
        "Confidence": _extract_field_value(brief, "Confidence"),
        "Sources": str(pack.get("selected_count", len(pack.get("selected_sources", [])))),
        "Cost/voyage": _format_compact_currency(parse_first_number(carbon_cost["cost_per_voyage"])),
        "Annual cost": _format_compact_currency(parse_first_number(carbon_cost["annualised_cost"])),
        "Coverage": f"{get_nested_value(pack, [['quantified_evidence_readout', 'requirement_coverage_percent']], 0)}%",
    }


def _build_hormuz_overview_metrics(pack, brief):
    insurance = extract_markdown_table(extract_markdown_section(brief, "7. Insurance Break-Even Analysis"))
    insurance_rows = insurance[0] if insurance else []
    return {
        "Risk": _extract_field_value(brief, "Overall risk level"),
        "Confidence": _extract_field_value(brief, "Confidence"),
        "Sources": str(pack.get("selected_count", len(pack.get("selected_sources", [])))),
        "Break-even": _row_value(insurance_rows, "Input / Output", "break-even war-risk premium against reroute"),
        "Provider": _title_value(pack.get("source_provider", "")),
        "Fallback": _yes_no(pack.get("fallback_used", pack.get("fallback_demo_data_used", ""))),
    }


def _build_critical_minerals_overview_metrics(pack, brief):
    scenario = pack.get("scenario_inputs", {})
    gap = get_nested_value(scenario, [["production_continuity_gap_days", "value"]], "")
    runway = get_nested_value(scenario, [["inventory_runway_days", "value"]], "")
    qualification = get_nested_value(scenario, [["alternative_supplier_qualification_days", "value"]], "")
    return {
        "Risk": _extract_field_value(brief, "Overall risk level"),
        "Confidence": _extract_field_value(brief, "Confidence"),
        "Sources": str(pack.get("selected_count", len(pack.get("selected_sources", [])))),
        "Gap": f"{gap} days" if gap != "" else "",
        "Inventory": f"{runway} days" if runway != "" else "",
        "Qualification": f"{qualification} days" if qualification != "" else "",
    }


def _build_sanctions_overview_metrics(pack, brief):
    model = pack.get("transaction_decision_model", {}).get("outputs", {})
    return {
        "Decision": "Hold/Escalate",
        "Risk": _extract_field_value(brief, "Overall risk level"),
        "Confidence": _extract_field_value(brief, "Confidence"),
        "Evidence": "Live",
        "Provider": _title_value(pack.get("source_provider", "")),
        "Fallback": _yes_no(pack.get("fallback_used", pack.get("fallback_demo_data_used", ""))),
        "Sources": str(pack.get("selected_count", len(pack.get("selected_sources", [])))),
        "Legal hold": "Yes" if model.get("legal_hold_required") else "Review",
        "Missing data": str(len(model.get("missing_documents", []))) if model else "",
    }


def _build_carbon_cost_metrics(pack, brief):
    section = extract_markdown_section(brief, "4. Carbon Cost Estimate")
    tables = extract_markdown_table(section)
    policy_inputs = tables[0] if len(tables) > 0 else []
    assumptions = tables[1] if len(tables) > 1 else []
    market_inputs = tables[2] if len(tables) > 2 else []
    derived_outputs = tables[3] if len(tables) > 3 else []
    sensitivity = tables[4] if len(tables) > 4 else []

    cost_per_voyage = _row_value(derived_outputs, "Output", "cost per voyage")
    annualised_cost = _row_value(derived_outputs, "Output", "annualised cost")

    if not cost_per_voyage:
        cost_per_voyage = _format_currency(
            get_nested_value(pack, [["calculator_assumptions", "fuel_consumption_tonnes_per_voyage"]], 18)
            * 3.206
            * get_nested_value(pack, [["calculator_assumptions", "coverage_rate"]], 1.0)
            * get_nested_value(pack, [["calculator_assumptions", "uka_price_per_tonne"]], 48),
            0,
        )
    if not annualised_cost:
        annualised_cost = _format_currency(
            parse_first_number(cost_per_voyage) * get_nested_value(pack, [["calculator_assumptions", "voyages_per_week"]], 6) * 4.345 * 12,
            0,
        )

    return {
        "policy_inputs": policy_inputs,
        "assumptions": assumptions,
        "market_inputs": market_inputs,
        "derived_outputs": derived_outputs,
        "sensitivity": sensitivity,
        "cost_per_voyage": _format_currency(parse_first_number(cost_per_voyage), 0),
        "annualised_cost": _format_currency(parse_first_number(annualised_cost), 0),
    }


def _extract_field_value(brief, field_name):
    for line in brief.splitlines():
        if line.startswith(f"| {field_name} |"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            return cells[1] if len(cells) > 1 else ""
    return ""


def _row_value(rows, key_name, key_value):
    key_value = key_value.lower()
    for row in rows:
        if str(row.get(key_name, "")).strip().lower() == key_value:
            for field in ("Value", "Assessment", "Note"):
                if field in row and field != key_name:
                    return row[field]
    return ""


def _format_currency(value, decimals):
    if decimals == 0:
        return f"£{float(value):,.0f}"
    return f"£{float(value):,.{decimals}f}"


def _format_compact_currency(value):
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"£{value / 1_000_000:.1f}m"
    if abs(value) >= 1_000:
        return f"£{value / 1_000:.1f}k"
    return f"£{value:,.0f}"


def _title_value(value):
    return str(value).strip().title()


def _yes_no(value):
    return "Yes" if bool(value) else "No"


if __name__ == "__main__":
    main()
