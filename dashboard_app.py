from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard_helpers import (
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
    st.markdown(f"## {case['title']}")
    st.caption(case["description"])

    if case_name == "UK ETS Maritime Expansion":
        _render_uk_ets(pack, brief, audit)
    else:
        _render_hormuz(pack, brief, audit)


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
        st.markdown("### Refresh priorities")
        _render_refresh_df(pack)
        st.markdown("### Full source audit")
        st.markdown(audit)


def _render_hormuz(pack, brief, audit):
    overview = _build_hormuz_overview_metrics(pack, brief)
    _render_metrics(overview)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Decision", "Route-Cost and Insurance", "Sanctions and Vessel Signals", "Evidence and Sources", "Full Brief / Source Audit"]
    )

    with tab1:
        _render_markdown_table_section(brief, "Dashboard Summary")
        _render_markdown_table_section(brief, "1. Decision Recommendation")
        _render_text_section(brief, "3. Executive Judgement")
        _render_markdown_table_section(brief, "4. Route Decision Optimiser")

    with tab2:
        _render_markdown_table_section(brief, "5. Route-Cost Assumptions")
        _render_markdown_table_section(brief, "7. Insurance Break-Even Analysis")

    with tab3:
        _render_markdown_table_section(brief, "6. Sanctions Red-Flag Assessment")
        _render_markdown_table_section(brief, "8. AIS and Vessel-Flow Signals")
        _render_markdown_table_section(brief, "13. Relaxation and Escalation Triggers")
        if not extract_markdown_section(brief, "13. Relaxation and Escalation Triggers"):
            _render_text_section(brief, "13. Relaxation and Escalation Triggers")

    with tab4:
        _render_markdown_table_section(brief, "9. Risk Scorecard")
        _render_markdown_table_section(brief, "10. Evidence-To-Score Bridge")
        _render_markdown_table_section(brief, "11. Source Requirement Coverage")
        with st.expander("Evidence Appendix", expanded=False):
            _render_markdown_table_section(brief, "14. Evidence Appendix")
        _render_markdown_table_section(brief, "15. Source Audit Summary")
        st.markdown("### Full source audit summary")
        st.markdown(audit)

    with tab5:
        with st.expander("Full brief markdown", expanded=False):
            st.markdown(brief)
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


def _build_uk_ets_overview_metrics(pack, brief, carbon_cost):
    return {
        "Overall risk level": _extract_field_value(brief, "Overall risk level"),
        "Confidence score": _extract_field_value(brief, "Confidence"),
        "Evidence mode": pack.get("evidence_mode", _extract_field_value(brief, "Evidence mode")),
        "Source provider": pack.get("source_provider", ""),
        "Fallback used": str(pack.get("fallback_used", pack.get("fallback_demo_data_used", ""))).lower(),
        "Source requirement coverage": f"{get_nested_value(pack, [['quantified_evidence_readout', 'requirement_coverage_percent']], 0)}%",
        "Selected sources": str(pack.get("selected_count", len(pack.get("selected_sources", [])))),
        "Estimated cost per voyage": carbon_cost["cost_per_voyage"],
        "Annualised cost": carbon_cost["annualised_cost"],
    }


def _build_hormuz_overview_metrics(pack, brief):
    decision = extract_markdown_table(extract_markdown_section(brief, "1. Decision Recommendation"))
    dashboard_summary = extract_markdown_table(extract_markdown_section(brief, "Dashboard Summary"))
    insurance = extract_markdown_table(extract_markdown_section(brief, "7. Insurance Break-Even Analysis"))
    decision_rows = decision[0] if decision else []
    summary_rows = dashboard_summary[0] if dashboard_summary else []
    insurance_rows = insurance[0] if insurance else []
    return {
        "Preferred option": _row_value(decision_rows, "Item", "Preferred option"),
        "Overall risk level": _extract_field_value(brief, "Overall risk level"),
        "Confidence": _extract_field_value(brief, "Confidence"),
        "Evidence mode": pack.get("evidence_mode", ""),
        "Source provider": pack.get("source_provider", ""),
        "Fallback used": str(pack.get("fallback_used", pack.get("fallback_demo_data_used", ""))).lower(),
        "Selected sources": str(pack.get("selected_count", len(pack.get("selected_sources", [])))),
        "Primary legal trigger": _row_value(summary_rows, "Item", "Primary legal trigger"),
        "Insurance break-even against reroute": _row_value(insurance_rows, "Input / Output", "break-even war-risk premium against reroute").upper(),
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


if __name__ == "__main__":
    main()
