import os
from pathlib import Path

from nicegui import ui

from dashboard_helpers import (
    build_selected_source_rows,
    extract_markdown_section,
    extract_markdown_table,
    get_nested_value,
    load_json,
    load_markdown,
)


ROOT = Path(__file__).resolve().parent
SHOWCASE = ROOT / "showcase"

CASES = {
    "UK ETS Maritime Expansion": {
        "brief": SHOWCASE / "uk_ets_shipping_operator_brief.md",
        "audit": SHOWCASE / "uk_ets_source_audit.md",
        "pack": SHOWCASE / "uk_ets_evidence_pack.json",
        "title": "UK ETS Maritime Expansion: Carbon Cost Exposure",
        "description": "Source-audited political risk workflow converting UK ETS maritime policy into operator-relevant carbon cost exposure, route applicability, risk scoring and review controls.",
        "decision_sections": ["1. Operator Stance", "2. Applicability Check", "3. Executive Judgement", "8. Decision Implications"],
        "evidence_sections": ["5. Risk Scorecard", "6. Quantified Evidence Readout", "7. Evidence-To-Score Bridge", "14. Source Requirement Coverage", "15. Source Quality Notes"],
        "methodology_sections": ["12. Recommended Actions"],
    },
    "Hormuz Route Decision Engine": {
        "brief": SHOWCASE / "hormuz_shipping_operator_brief.md",
        "audit": SHOWCASE / "hormuz_source_audit.md",
        "pack": SHOWCASE / "hormuz_evidence_pack.json",
        "title": "Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs",
        "description": "Trigger-based shipping-operator decision workflow for transit, delay, reroute or legal hold across sanctions, insurance, AIS/vessel-flow and detention risk conditions.",
        "decision_sections": ["Dashboard Summary", "1. Decision Recommendation", "3. Executive Judgement", "4. Route Decision Optimiser"],
        "evidence_sections": ["9. Risk Scorecard", "10. Evidence-To-Score Bridge", "11. Source Requirement Coverage", "15. Source Audit Summary"],
        "methodology_sections": ["5. Illustrative Route-Cost Scenario", "6. Sanctions Red-Flag Assessment", "7. Insurance Break-Even Analysis", "13. Relaxation and Escalation Triggers"],
    },
    "Critical Minerals Exposure Engine": {
        "brief": SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md",
        "audit": SHOWCASE / "critical_minerals_source_audit.md",
        "pack": SHOWCASE / "critical_minerals_evidence_pack.json",
        "title": "Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers",
        "description": "Production-continuity decision workflow for stockpile, alternative supplier qualification, redesign, customer allocation and production-hold decisions under rare earth magnet supply disruption.",
        "decision_sections": ["3. Dashboard Summary", "1. Decision Recommendation", "2. Scope and Specificity", "4. Exposure Summary"],
        "evidence_sections": ["10. Risk Scorecard", "11. Evidence-To-Score Bridge", "12. Source Requirement Coverage", "13. Source Quality Notes"],
        "methodology_sections": ["7. Production Continuity Model", "8. Inventory Runway vs Supplier Qualification Gap", "9. Mitigation Options", "16. Methodology and Review Controls"],
    },
    "Sanctions Trade Finance Exposure Engine": {
        "brief": SHOWCASE / "sanctions_trade_finance_exposure_brief.md",
        "audit": SHOWCASE / "sanctions_source_audit.md",
        "pack": SHOWCASE / "sanctions_evidence_pack.json",
        "title": "Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk",
        "description": "Transaction decision workflow for approve, enhanced due diligence, escalation, legal hold or rejection under sanctions, end-use, counterparty, route, payment and documentation risk.",
        "decision_sections": ["3. Dashboard Summary", "1. Decision Recommendation", "2. Scope and Specificity", "4. Transaction Exposure Summary"],
        "evidence_sections": ["11. Risk Scorecard", "12. Evidence-To-Score Bridge", "13. Source Requirement Coverage", "14. Source Quality Notes"],
        "methodology_sections": ["5. Goods and End-Use Risk Assessment", "9. Transaction Decision Engine", "10. Due Diligence Actions", "18. Methodology and Review Controls"],
    },
    "Cyber Business Interruption Engine": {
        "brief": SHOWCASE / "cyber_business_interruption_brief.md",
        "audit": SHOWCASE / "cyber_source_audit.md",
        "pack": SHOWCASE / "cyber_evidence_pack.json",
        "title": "Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services",
        "description": "Business-interruption decision workflow for incident response, notification, insurance claim readiness, manual fallback, supplier escalation and resilience investment.",
        "decision_sections": ["3. Dashboard Summary", "1. Decision Recommendation", "2. Scope and Specificity", "4. Incident Exposure Summary"],
        "evidence_sections": ["12. Risk Scorecard", "13. Evidence-To-Score Bridge", "14. Source Requirement Coverage", "15. Source Quality Notes"],
        "methodology_sections": ["6. Business Interruption Model", "7. Downtime / Revenue-at-Risk Assessment", "11. Mitigation Options", "19. Methodology and Review Controls"],
    },
    "UK Fiscal Instability & Procurement Delay Risk": {
        "brief": SHOWCASE / "uk_fiscal_instability_procurement_brief.md",
        "audit": SHOWCASE / "uk_fiscal_instability_procurement_source_audit.md",
        "pack": SHOWCASE / "uk_fiscal_instability_procurement_evidence_pack.json",
        "title": "UK Fiscal Instability & Procurement Delay Risk",
        "description": "Political economy risk for a UK infrastructure contractor bidding for government-funded transport and energy projects.",
        "decision_sections": ["Decision Question", "Executive Judgement", "Human Review And Company Data Required"],
        "evidence_sections": ["Risk Scorecard", "Evidence-To-Score Bridge", "Scoring Traceability", "Source Governance", "Source Requirement Coverage"],
        "methodology_sections": ["Key Risks", "Exposure Map", "Review Controls"],
    },
}


def main() -> None:
    ui.page_title("Political Risk Agent")
    _add_styles()

    with ui.column().classes("w-full max-w-screen-xl mx-auto gap-5 p-6"):
        ui.label("Political Risk Agent").classes("text-4xl font-bold")
        ui.label("Source-audited political risk workflow for turning public/live evidence into decision-useful commercial risk outputs.").classes(
            "text-lg text-gray-700"
        )
        ui.label("This dashboard displays saved showcase artefacts only. It does not call Tavily or spend live-search credits.").classes(
            "text-sm text-gray-600"
        )
        ui.markdown(
            "This dashboard demonstrates a reusable political-risk workflow: identify a political, geopolitical, regulatory or state-linked trigger; "
            "map it to business exposure; assess the evidence base; and convert it into a decision-support output with source caveats and company-data requirements."
        ).classes("text-gray-800")
        ui.markdown(
            """
            **Current showcase cases:**
            - UK ETS: regulatory policy into route-level carbon cost exposure
            - Hormuz: geopolitical/security risk into transit, delay, reroute or legal-hold decision
            - Critical Minerals: strategic competition into production-continuity risk
            - Sanctions Trade Finance: sanctions/export controls into transaction approval, escalation, legal hold or rejection
            - Cyber Business Interruption: geopolitical cyber and ransomware risk into downtime, notification, insurance and recovery decisions
            - UK Fiscal: political economy risk into bid pipeline review, delay contingency, repricing and board exposure reporting

            The dashboard is designed as an expandable case portfolio. Future cases can be added using the same saved-showcase pattern.
            """
        )
        ui.markdown(
            "Each case starts with the business decision, then shows the model output, evidence base, source caveats and company-data needed for operational use."
        )

        case_panel = ui.column().classes("w-full gap-4")
        selector = ui.select(
            list(CASES.keys()),
            value=list(CASES.keys())[0],
            label="Case study",
            on_change=lambda event: render_case(case_panel, event.value),
        ).classes("w-full max-w-xl")
        render_case(case_panel, selector.value)


def render_case(container, case_name: str) -> None:
    container.clear()
    case = CASES[case_name]
    pack = load_json(case["pack"])
    brief = load_markdown(case["brief"])
    audit = load_markdown(case["audit"])

    with container:
        ui.separator()
        ui.label(case["title"]).classes("text-2xl font-semibold")
        ui.label(case["description"]).classes("text-gray-700")
        _render_metric_cards(pack, brief)

        with ui.tabs().classes("w-full") as tabs:
            overview = ui.tab("Overview")
            decision = ui.tab("Decision")
            evidence = ui.tab("Evidence & Sources")
            methodology = ui.tab("Methodology")
            full_detail = ui.tab("Full Brief / Audit")

        with ui.tab_panels(tabs, value=overview).classes("w-full"):
            with ui.tab_panel(overview):
                _render_overview(pack, brief)
            with ui.tab_panel(decision):
                _render_sections(brief, case["decision_sections"])
            with ui.tab_panel(evidence):
                _render_scores(pack)
                _render_sections(brief, case["evidence_sections"])
                _render_selected_sources(pack)
                _render_evidence_preview(pack)
            with ui.tab_panel(methodology):
                _render_sections(brief, case["methodology_sections"])
                _render_refresh_priorities(pack)
            with ui.tab_panel(full_detail):
                _render_expansion("Full brief markdown", brief)
                _render_expansion("Full source audit markdown", audit)


def _render_overview(pack: dict, brief: str) -> None:
    _render_first_existing_section(
        brief,
        [
            "Dashboard Summary",
            "3. Dashboard Summary",
            "1. Operator Stance",
            "Decision Question",
            "Executive Judgement",
        ],
    )
    summary_rows = [
        {"Item": "Evidence mode", "Value": pack.get("evidence_mode", "")},
        {"Item": "Source provider", "Value": pack.get("source_provider") or pack.get("search_provider", "")},
        {"Item": "Fallback used", "Value": _format_bool(pack.get("fallback_used", pack.get("fallback_demo_data_used", "")))},
        {"Item": "Selected sources", "Value": str(_selected_count(pack))},
        {"Item": "Rejected sources", "Value": str(pack.get("rejected_count", len(pack.get("rejected_sources", []))))},
    ]
    _table("Showcase Metadata", summary_rows)


def _render_metric_cards(pack: dict, brief: str) -> None:
    metrics = _overview_metrics(pack, brief)
    with ui.grid(columns=3).classes("w-full gap-3"):
        for label, value in metrics:
            with ui.card().classes("metric-card"):
                ui.label(label).classes("text-xs uppercase tracking-wide text-gray-500")
                ui.label(str(value)).classes("text-xl font-semibold")


def _overview_metrics(pack: dict, brief: str) -> list[tuple[str, str]]:
    scores = _score_rows(pack)
    risk = _extract_table_value(brief, ["Overall risk level", "Risk level", "Risk"])
    confidence = _extract_table_value(brief, ["Confidence", "Confidence score"]) or _score_value(scores, "confidence")
    decision = _extract_table_value(brief, ["Current stance", "Decision recommendation", "Preferred option", "Recommendation"])
    return [
        ("Decision", _shorten(decision or "See brief", 28)),
        ("Risk", _shorten(risk or _score_value(scores, "impact") or "See scorecard", 20)),
        ("Confidence", _shorten(confidence or "See scorecard", 18)),
        ("Evidence", _shorten(pack.get("evidence_mode", "Saved showcase"), 22)),
        ("Provider", pack.get("source_provider") or pack.get("search_provider", "saved")),
        ("Sources", str(_selected_count(pack))),
    ]


def _render_scores(pack: dict) -> None:
    rows = _score_rows(pack)
    if rows:
        _table("Traceable Scores", rows)


def _score_rows(pack: dict) -> list[dict]:
    raw_scores = pack.get("traceable_scores") or get_nested_value(pack, [["scoring", "traceable_scores"]], {})
    if isinstance(raw_scores, dict):
        iterable = raw_scores.items()
    elif isinstance(raw_scores, list):
        iterable = [(score.get("dimension", f"score_{index + 1}"), score) for index, score in enumerate(raw_scores)]
    else:
        iterable = []

    rows = []
    for dimension, score in iterable:
        if not isinstance(score, dict):
            continue
        supporting = score.get("supporting_evidence") or score.get("evidence_supporting_score") or []
        if isinstance(supporting, list):
            supporting = ", ".join(str(item) for item in supporting[:3])
        rows.append(
            {
                "Dimension": score.get("dimension", dimension),
                "Score": score.get("score", ""),
                "Label": score.get("score_label", ""),
                "Score type": score.get("score_type", ""),
                "Supporting evidence": supporting,
                "Cap reason": score.get("confidence_cap_reason") or score.get("reason_score_is_capped", ""),
            }
        )
    return rows


def _score_value(rows: list[dict], dimension: str) -> str:
    for row in rows:
        if str(row.get("Dimension", "")).lower() == dimension:
            score = row.get("Score", "")
            label = row.get("Label", "")
            return f"{score}/5 {label}".strip()
    return ""


def _render_sections(markdown: str, headings: list[str]) -> None:
    for heading in headings:
        _render_section(markdown, heading)


def _render_first_existing_section(markdown: str, headings: list[str]) -> None:
    for heading in headings:
        if extract_markdown_section(markdown, heading):
            _render_section(markdown, heading)
            return


def _render_section(markdown: str, heading: str) -> None:
    section = extract_markdown_section(markdown, heading)
    if not section:
        return
    label = heading.split(". ", 1)[1] if ". " in heading else heading
    ui.label(label).classes("text-xl font-semibold mt-4")

    tables = extract_markdown_table(section)
    text = "\n".join(line for line in section.splitlines() if not line.startswith("|")).strip()
    if text:
        ui.markdown(text).classes("prose max-w-none")
    for table in tables:
        if table:
            _table("", table)


def _render_selected_sources(pack: dict) -> None:
    rows = build_selected_source_rows(pack)
    if rows:
        _table("Selected Sources", rows)


def _render_evidence_preview(pack: dict) -> None:
    evidence = pack.get("evidence", [])
    rows = []
    for item in evidence[:20]:
        mode = item.get("evidence_source_mode", "")
        rows.append(
            {
                "Source ID": item.get("source_id", ""),
                "Title": item.get("source_title", item.get("title", "")),
                "Mode": mode,
                "Claim": item.get("extracted_claim") or item.get("claim_supported") or item.get("snippet", ""),
                "Commercial relevance": item.get("commercial_relevance") or item.get("commercial_meaning") or item.get("business_user_implication", ""),
                "Review required": str(item.get("requires_human_review") or mode in {"snippet_only", "metadata_only", "fallback", "manual_input"}),
            }
        )
    if rows:
        _table("Evidence Preview", rows)


def _render_refresh_priorities(pack: dict) -> None:
    rows = pack.get("refresh_priorities", [])
    if rows:
        _table("Refresh Priorities", rows)


def _render_expansion(title: str, markdown: str) -> None:
    with ui.expansion(title, icon="article").classes("w-full"):
        ui.markdown(markdown).classes("prose max-w-none")


def _table(title: str, rows: list[dict]) -> None:
    if not rows:
        return
    if title:
        ui.label(title).classes("text-xl font-semibold mt-4")
    columns = [{"name": key, "label": key, "field": key, "align": "left"} for key in rows[0].keys()]
    ui.table(columns=columns, rows=rows, row_key=next(iter(rows[0].keys()))).classes("w-full").props("flat bordered wrap-cells")


def _extract_table_value(markdown: str, fields: list[str]) -> str:
    for heading in [
        "Dashboard Summary",
        "3. Dashboard Summary",
        "1. Decision Recommendation",
        "Decision Recommendation",
        "Risk Scorecard",
        "5. Risk Scorecard",
        "9. Risk Scorecard",
        "10. Risk Scorecard",
        "11. Risk Scorecard",
        "12. Risk Scorecard",
    ]:
        section = extract_markdown_section(markdown, heading)
        for table in extract_markdown_table(section):
            for row in table:
                values = {str(k).strip().lower(): v for k, v in row.items()}
                item = str(values.get("item") or values.get("dimension") or values.get("metric") or "").strip().lower()
                for field in fields:
                    if item == field.lower():
                        return str(values.get("value") or values.get("assessment") or values.get("score") or "")
    return ""


def _selected_count(pack: dict) -> int:
    return int(pack.get("selected_count") or len(pack.get("selected_sources", [])))


def _shorten(value: str, limit: int) -> str:
    value = " ".join(str(value).split())
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def _format_bool(value) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)


def _add_styles() -> None:
    ui.add_head_html(
        """
        <style>
        body { background: #f5f6f8; }
        .metric-card {
            background: white;
            border: 1px solid #d8dde6;
            border-radius: 8px;
            padding: 14px 16px;
            min-height: 92px;
        }
        .nicegui-content { max-width: none; }
        .q-table td, .q-table th { white-space: normal; vertical-align: top; }
        </style>
        """
    )


main()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
        reload=False,
    )
