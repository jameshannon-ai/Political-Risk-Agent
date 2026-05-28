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
PACK_PATH = SHOWCASE / "uk_ets_evidence_pack.json"
BRIEF_PATH = SHOWCASE / "uk_ets_shipping_operator_brief.md"
AUDIT_PATH = SHOWCASE / "uk_ets_source_audit.md"


st.set_page_config(
    page_title="Political Risk Agent | UK ETS",
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
    .section-card {
        background: white;
        border: 1px solid #d8dde6;
        border-radius: 0.5rem;
        padding: 1rem 1rem 0.5rem 1rem;
        margin-bottom: 1rem;
    }
    .small-note {
        color: #4b5563;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    pack = load_json(PACK_PATH)
    brief = load_markdown(BRIEF_PATH)
    audit = load_markdown(AUDIT_PATH)

    carbon_cost = _build_carbon_cost_metrics(pack, brief)
    overview = _build_overview_metrics(pack, brief, carbon_cost)

    st.title("Political Risk Agent")
    st.subheader("UK ETS Maritime Expansion: Carbon Cost Exposure")
    st.caption(
        "Source-audited political risk workflow converting UK ETS maritime policy into operator-relevant carbon cost exposure, route applicability, risk scoring and review controls."
    )

    _render_metrics(overview)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Operator Decision", "Carbon Cost", "Evidence & Scores", "Source Audit"]
    )

    with tab1:
        _render_operator_decision(brief)

    with tab2:
        _render_carbon_cost(brief, carbon_cost)

    with tab3:
        _render_evidence_and_scores(brief)

    with tab4:
        _render_source_audit(pack, audit)


def _render_metrics(overview):
    labels = [
        "Overall risk level",
        "Confidence score",
        "Evidence mode",
        "Source provider",
        "Fallback used",
        "Source requirement coverage",
        "Selected sources",
        "Estimated cost per voyage",
        "Annualised cost",
    ]
    cols = st.columns(3)
    for index, label in enumerate(labels):
        with cols[index % 3]:
            st.metric(label, overview[label])


def _render_operator_decision(brief):
    _render_markdown_table_section(brief, "1. Operator Stance")
    _render_markdown_table_section(brief, "2. Applicability Check")
    _render_text_section(brief, "3. Executive Judgement")
    _render_markdown_table_section(brief, "8. Decision Implications")
    _render_text_section(brief, "12. Recommended Actions")


def _render_carbon_cost(brief, carbon_cost):
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


def _render_evidence_and_scores(brief):
    for heading in [
        "5. Risk Scorecard",
        "6. Quantified Evidence Readout",
        "7. Evidence-To-Score Bridge",
        "14. Source Requirement Coverage",
    ]:
        _render_markdown_table_section(brief, heading)


def _render_source_audit(pack, audit):
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

    st.markdown("### Refresh priorities")
    refresh_df = pd.DataFrame(pack.get("refresh_priorities", []))
    if not refresh_df.empty:
        st.dataframe(refresh_df, use_container_width=True, hide_index=True)

    st.markdown("### Full source audit")
    st.markdown(audit)


def _render_markdown_table_section(markdown, heading):
    section = extract_markdown_section(markdown, heading)
    if not section:
        return
    st.markdown(f"### {heading.split('. ', 1)[1] if '. ' in heading else heading}")
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
        st.markdown(f"### {heading.split('. ', 1)[1] if '. ' in heading else heading}")
        st.markdown(section)


def _build_overview_metrics(pack, brief, carbon_cost):
    risk_level = _extract_field_value(brief, "Overall risk level")
    confidence = _extract_field_value(brief, "Confidence")
    evidence_mode = pack.get("evidence_mode", _extract_field_value(brief, "Evidence mode"))
    provider = pack.get("source_provider", "")
    fallback = str(pack.get("fallback_used", pack.get("fallback_demo_data_used", ""))).lower()
    coverage = f"{get_nested_value(pack, [['quantified_evidence_readout', 'requirement_coverage_percent']], 0)}%"
    selected_sources = str(pack.get("selected_count", len(pack.get("selected_sources", []))))
    per_voyage = carbon_cost["cost_per_voyage"]
    annualised = carbon_cost["annualised_cost"]

    return {
        "Overall risk level": risk_level,
        "Confidence score": confidence,
        "Evidence mode": evidence_mode,
        "Source provider": provider,
        "Fallback used": fallback,
        "Source requirement coverage": coverage,
        "Selected sources": selected_sources,
        "Estimated cost per voyage": per_voyage,
        "Annualised cost": annualised,
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
    match = None
    for line in brief.splitlines():
        if line.startswith(f"| {field_name} |"):
            match = line
            break
    if not match:
        return ""
    cells = [cell.strip() for cell in match.strip("|").split("|")]
    return cells[1] if len(cells) > 1 else ""


def _row_value(rows, key_name, key_value):
    key_value = key_value.lower()
    for row in rows:
        if str(row.get(key_name, "")).strip().lower() == key_value:
            for field in ("Value", "Assessment"):
                if field in row:
                    return row[field]
    return ""


def _format_currency(value, decimals):
    if decimals == 0:
        return f"£{float(value):,.0f}"
    return f"£{float(value):,.{decimals}f}"


if __name__ == "__main__":
    main()
