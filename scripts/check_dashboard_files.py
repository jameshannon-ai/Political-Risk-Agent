import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dashboard_helpers import (  # noqa: E402
    build_selected_source_rows,
    extract_markdown_section,
    load_json,
    load_markdown,
)


SHOWCASE = ROOT / "showcase"
DASHBOARD = ROOT / "dashboard_app.py"

CASES = {
    "UK ETS": {
        "files": [
            SHOWCASE / "uk_ets_shipping_operator_brief.md",
            SHOWCASE / "uk_ets_source_audit.md",
            SHOWCASE / "uk_ets_evidence_pack.json",
        ],
        "brief": SHOWCASE / "uk_ets_shipping_operator_brief.md",
        "sections": [
            "1. Operator Stance",
            "2. Applicability Check",
            "4. Carbon Cost Estimate",
            "7. Evidence-To-Score Bridge",
            "14. Source Requirement Coverage",
        ],
    },
    "Hormuz": {
        "files": [
            SHOWCASE / "hormuz_shipping_operator_brief.md",
            SHOWCASE / "hormuz_source_audit.md",
            SHOWCASE / "hormuz_evidence_pack.json",
        ],
        "brief": SHOWCASE / "hormuz_shipping_operator_brief.md",
        "sections": [
            "Dashboard Summary",
            "1. Decision Recommendation",
            "4. Route Decision Optimiser",
            "5. Illustrative Route-Cost Scenario",
            "11. Source Requirement Coverage",
        ],
    },
    "Critical Minerals": {
        "files": [
            SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md",
            SHOWCASE / "critical_minerals_source_audit.md",
            SHOWCASE / "critical_minerals_evidence_pack.json",
        ],
        "brief": SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md",
        "sections": [
            "3. Dashboard Summary",
            "1. Decision Recommendation",
            "7. Production Continuity Model",
            "8. Inventory Runway vs Supplier Qualification Gap",
            "13. Source Quality Notes",
        ],
    },
    "Sanctions": {
        "files": [
            SHOWCASE / "sanctions_trade_finance_exposure_brief.md",
            SHOWCASE / "sanctions_source_audit.md",
            SHOWCASE / "sanctions_evidence_pack.json",
        ],
        "brief": SHOWCASE / "sanctions_trade_finance_exposure_brief.md",
        "sections": [
            "3. Dashboard Summary",
            "1. Decision Recommendation",
            "9. Transaction Decision Engine",
            "12. Evidence-To-Score Bridge",
            "13. Source Requirement Coverage",
            "14. Source Quality Notes",
            "15. Selected Sources",
        ],
    },
    "Cyber Business Interruption": {
        "files": [
            SHOWCASE / "cyber_business_interruption_brief.md",
            SHOWCASE / "cyber_source_audit.md",
            SHOWCASE / "cyber_evidence_pack.json",
        ],
        "brief": SHOWCASE / "cyber_business_interruption_brief.md",
        "sections": [
            "3. Dashboard Summary",
            "1. Decision Recommendation",
            "4. Incident Exposure Summary",
            "5. Operational Dependency Assessment",
            "6. Business Interruption Model",
            "7. Downtime / Revenue-at-Risk Assessment",
            "8. Regulatory Notification Assessment",
            "9. Insurance and Claims Readiness Assessment",
            "10. Supplier / MSP Dependency Risk",
            "15. Source Quality Notes",
            "14. Source Requirement Coverage",
        ],
    },
    "UK Fiscal Instability": {
        "files": [
            SHOWCASE / "uk_fiscal_instability_procurement_brief.md",
            SHOWCASE / "uk_fiscal_instability_procurement_source_audit.md",
            SHOWCASE / "uk_fiscal_instability_procurement_evidence_pack.json",
        ],
        "brief": SHOWCASE / "uk_fiscal_instability_procurement_brief.md",
        "sections": [
            "Decision Question",
            "Executive Judgement",
            "Risk Scorecard",
            "Evidence-To-Score Bridge",
            "Scoring Traceability",
            "Source Governance",
            "Source Requirement Coverage",
            "Evidence Appendix",
            "Human Review And Company Data Required",
        ],
    },
}


def main():
    failures = []

    if not DASHBOARD.exists():
        failures.append("dashboard_app.py is missing")
    else:
        dashboard = DASHBOARD.read_text(encoding="utf-8")
        for forbidden in ["TavilyClient", "live_search_mode", ".env"]:
            if forbidden in dashboard:
                failures.append(f"dashboard_app.py contains forbidden live or secret reference: {forbidden}")
        for phrase in [
            "Current showcase cases:",
            "The dashboard is designed as an expandable case portfolio.",
            "This dashboard demonstrates a reusable political-risk workflow: identify a political, geopolitical, regulatory or state-linked trigger; map it to business exposure; assess the evidence base; and convert it into a decision-support output with source caveats and company-data requirements.",
            "Each case starts with the business decision, then shows the model output, evidence base, source caveats and company-data needed for operational use.",
            "UK ETS: regulatory policy into route-level carbon cost exposure",
            "Hormuz: geopolitical/security risk into transit, delay, reroute or legal-hold decision",
            "Critical Minerals: strategic competition into production-continuity risk",
            "Sanctions Trade Finance: sanctions/export controls into transaction approval, escalation, legal hold or rejection",
            "Cyber Business Interruption: geopolitical cyber and ransomware risk into downtime, notification, insurance and recovery decisions",
            "UK Fiscal: political economy risk into bid pipeline review, delay contingency, repricing and board exposure reporting",
            "Sanctions Trade Finance Exposure Engine",
            "Cyber Business Interruption Engine",
            "UK Fiscal Instability & Procurement Delay Risk",
            "Political economy risk for a UK infrastructure contractor bidding for government-funded transport and energy projects.",
            'SHOWCASE / "uk_fiscal_instability_procurement_evidence_pack.json"',
            'SHOWCASE / "uk_fiscal_instability_procurement_brief.md"',
            'SHOWCASE / "uk_fiscal_instability_procurement_source_audit.md"',
            "Activate controls",
            "£2,770 per voyage",
            "£866,562 annualised",
            "£48/tCO2e",
            "57.71 tCO2e",
            "£2,769.98",
            "£16,619.90",
            "£72,213.48",
            "£866,561.79",
            "Manual fallback used because no live UKA price feed is embedded.",
            "Scenario",
            "UKA price",
            "Estimated cost per voyage",
            "£38.40/tCO2e",
            "£48.00/tCO2e",
            "£57.60/tCO2e",
            "£2,215.99",
            "£3,323.98",
            "Decision Summary",
            "First-Reader Summary",
            "Business problem",
            "Political risk trigger",
            "UK carbon regulation is expanding into maritime emissions, creating new compliance and cost exposure for in-scope shipping routes.",
            "State-linked disruption, transit-control threats, sanctions/payment risk and regional security escalation can change whether a voyage remains commercially and legally viable.",
            "Export controls, strategic competition and concentration of rare earth magnet supply can interrupt production-critical inputs for UK manufacturers.",
            "Government sanctions, end-use controls and enforcement expectations can turn transaction exposure into approval, escalation, legal-hold or rejection risk.",
            "State-linked cyber activity, ransomware ecosystems, national resilience policy and supplier/MSP dependency can turn cyber disruption into business interruption, notification and insurance-response risk.",
            "UK fiscal pressure, public spending trade-offs, gilt-market sensitivity and political budget choices can change procurement confidence and programme timing.",
            "Decision supported",
            "Evidence-to-output logic",
            "Company data needed",
            "Evidence Category Guide",
            "Political/regulatory trigger evidence",
            "Business exposure evidence",
            "Illustrative scenario assumptions",
            "Company-required data",
            "UK ETS maritime expansion turns carbon policy into a route-level operating cost for in-scope UK voyages.",
            "Strait of Hormuz disruption can turn a voyage decision into a combined sanctions, insurance, detention and route-cost problem.",
            "A UK manufacturer may lose access to rare earth magnet inputs before an alternative supplier can be qualified.",
            "A trade finance transaction can become unacceptable where goods, counterparties, ownership, route, payment or documentation create sanctions/export-control exposure.",
            "Cyber disruption can turn digital trading, payment, fulfilment or service dependency into downtime, customer harm and revenue loss.",
            "Fiscal credibility, gilt-market sensitivity and departmental budget uncertainty can affect public-sector infrastructure awards, payment assumptions and working-capital exposure.",
            "Resilience Gap Summary",
            "Requirement Coverage Summary",
            "Scoring Traceability",
            "Source Governance Summary",
            "Traceable Scorecard",
            "build_traceable_score_rows",
            "Decision Panel",
            "build_decision_panel_rows",
            "Evidence Quality Summary",
            "build_evidence_quality_rows",
            "Key Judgements / Evidence Cards",
            "build_evidence_card_rows",
            "build_requirement_coverage_quality_rows",
            "Evidence Trace",
            "build_evidence_trace_rows",
            "Selected Sources",
            "build_selected_source_rows",
            "LinkColumn",
            "Continuity Summary",
            "Dashboard caveats: substitution feasibility needs stronger magnet-specific engineering",
            "saved showcase artefacts only",
            "This is a client-type cyber business interruption exposure screen, not technical cybersecurity advice, legal advice or an insurance coverage determination.",
        ]:
            if phrase not in dashboard:
                failures.append(f"dashboard_app.py missing presentation phrase: {phrase}")
        for phrase in [
            "How to read this dashboard",
            "Start with the decision recommendation.",
            "Check the model output and key trigger.",
            "Review source caveats and company-data requirements before treating the result as operational.",
        ]:
            if phrase in dashboard:
                failures.append(f"dashboard_app.py still contains old reading guidance phrase: {phrase}")
        for phrase in ['st.json', 'st.write(pack)', 'st.write(brief)', 'st.write(audit)', 'st.markdown("empty', "st.markdown('empty"]:
            if phrase in dashboard:
                failures.append(f"dashboard_app.py contains raw dump or visible empty marker: {phrase}")
        if '"Decision": "Resilience controls"' in dashboard:
            failures.append("Cyber decision metric should use short display text, not Resilience controls")
        if '"Risk": _extract_field_value(brief, "Overall risk level")' in dashboard and "def _build_cyber_overview_metrics" in dashboard:
            cyber_metric_block = dashboard.split("def _build_cyber_overview_metrics", 1)[1].split("def _build_carbon_cost_metrics", 1)[0]
            if '"Risk": _extract_field_value(brief, "Overall risk level")' in cyber_metric_block:
                failures.append("Cyber risk metric should not render an empty unsupported risk card")

    for case_name, config in CASES.items():
        for path in config["files"]:
            if not path.exists():
                failures.append(f"{case_name} missing saved dashboard file: {path.relative_to(ROOT)}")
        if config["brief"].exists():
            brief = load_markdown(config["brief"])
            for section in config["sections"]:
                if not extract_markdown_section(brief, section):
                    failures.append(f"{case_name} brief missing dashboard section: {section}")

        pack_path = config["files"][2]
        if pack_path.exists():
            rows = build_selected_source_rows(load_json(pack_path))
            if not rows:
                failures.append(f"{case_name} selected source table has no rows")
            for row in rows:
                if not row.get("URL"):
                    failures.append(f"{case_name} selected source missing URL: {row.get('Source ID')}")
                if not row.get("Source role") or row.get("Source role") == "source_role_unclassified":
                    failures.append(f"{case_name} selected source missing conservative source role: {row.get('Source ID')}")
                if not row.get("Source type"):
                    failures.append(f"{case_name} selected source missing source type: {row.get('Source ID')}")
            if case_name == "UK ETS":
                for row in rows:
                    title = row.get("Title", "")
                    if ("ICCT" in title or "Stephenson Harwood" in title) and row.get("Source type") == "official_primary":
                        failures.append(f"UK ETS source taxonomy overstates specialist source as official_primary: {title}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)

    print("Dashboard file check passed.")


if __name__ == "__main__":
    main()
