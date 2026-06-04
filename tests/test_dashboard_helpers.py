import tempfile
import unittest
import subprocess
from pathlib import Path

from dashboard_helpers import (
    build_selected_source_rows,
    extract_markdown_section,
    extract_markdown_table,
    get_nested_value,
    load_json,
    load_markdown,
)


class DashboardHelperTests(unittest.TestCase):
    def setUp(self):
        self.uk_ets_brief = Path("showcase/uk_ets_shipping_operator_brief.md")
        self.hormuz_brief = Path("showcase/hormuz_shipping_operator_brief.md")
        self.critical_minerals_brief = Path("showcase/critical_minerals_advanced_manufacturer_brief.md")
        self.sanctions_brief = Path("showcase/sanctions_trade_finance_exposure_brief.md")
        self.cyber_brief = Path("showcase/cyber_business_interruption_brief.md")
        self.uk_ets_pack = Path("showcase/uk_ets_evidence_pack.json")
        self.hormuz_pack = Path("showcase/hormuz_evidence_pack.json")
        self.critical_minerals_pack = Path("showcase/critical_minerals_evidence_pack.json")
        self.sanctions_pack = Path("showcase/sanctions_evidence_pack.json")
        self.cyber_pack = Path("showcase/cyber_evidence_pack.json")

    def test_loaders_read_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            json_path = root / "sample.json"
            md_path = root / "sample.md"
            json_path.write_text('{"a": 1}', encoding="utf-8")
            md_path.write_text("# Title\n\nBody", encoding="utf-8")

            self.assertEqual(load_json(json_path), {"a": 1})
            self.assertIn("Body", load_markdown(md_path))

    def test_extract_markdown_section(self):
        markdown = "## One\nalpha\n\n## Two\nbeta\n"
        self.assertEqual(extract_markdown_section(markdown, "Two"), "beta")

    def test_extract_markdown_table(self):
        section = """
| A | B |
| --- | --- |
| 1 | 2 |
| 3 | 4 |
"""
        tables = extract_markdown_table(section)
        self.assertEqual(tables[0][0]["A"], "1")
        self.assertEqual(tables[0][1]["B"], "4")

    def test_get_nested_value(self):
        data = {"a": {"b": 7}}
        self.assertEqual(get_nested_value(data, [["a", "b"], ["x"]], 0), 7)
        self.assertEqual(get_nested_value(data, [["x", "y"]], 5), 5)

    def test_saved_showcase_files_exist_for_all_active_cases(self):
        for path in [
            self.uk_ets_brief,
            self.hormuz_brief,
            self.critical_minerals_brief,
            self.sanctions_brief,
            self.cyber_brief,
            self.uk_ets_pack,
            self.hormuz_pack,
            self.critical_minerals_pack,
            self.sanctions_pack,
            self.cyber_pack,
            Path("showcase/uk_ets_source_audit.md"),
            Path("showcase/hormuz_source_audit.md"),
            Path("showcase/critical_minerals_source_audit.md"),
            Path("showcase/sanctions_source_audit.md"),
            Path("showcase/cyber_source_audit.md"),
        ]:
            self.assertTrue(path.exists(), f"Missing saved showcase file: {path}")

    def test_hormuz_sections_can_be_extracted(self):
        brief = load_markdown(self.hormuz_brief)
        for heading in [
            "Dashboard Summary",
            "1. Decision Recommendation",
            "4. Route Decision Optimiser",
            "5. Illustrative Route-Cost Scenario",
            "6. Sanctions Red-Flag Assessment",
            "7. Insurance Break-Even Analysis",
            "8. AIS and Vessel-Flow Signals",
            "11. Source Requirement Coverage",
        ]:
            section = extract_markdown_section(brief, heading)
            self.assertTrue(section, f"Expected section to be extractable: {heading}")
            if heading != "10. Due Diligence Actions":
                self.assertTrue(extract_markdown_table(section), f"Expected table in section: {heading}")

    def test_critical_minerals_sections_can_be_extracted(self):
        brief = load_markdown(self.critical_minerals_brief)
        for heading in [
            "3. Dashboard Summary",
            "1. Decision Recommendation",
            "4. Exposure Summary",
            "5. Controlled Input Assessment",
            "6. Supplier Concentration Assessment",
            "7. Production Continuity Model",
            "8. Inventory Runway vs Supplier Qualification Gap",
            "9. Mitigation Options",
            "13. Source Quality Notes",
            "12. Source Requirement Coverage",
        ]:
            section = extract_markdown_section(brief, heading)
            self.assertTrue(section, f"Expected section to be extractable: {heading}")
            if heading != "10. Due Diligence Actions":
                self.assertTrue(extract_markdown_table(section), f"Expected table in section: {heading}")

    def test_sanctions_sections_can_be_extracted(self):
        brief = load_markdown(self.sanctions_brief)
        for heading in [
            "3. Dashboard Summary",
            "1. Decision Recommendation",
            "4. Transaction Exposure Summary",
            "5. Goods and End-Use Risk Assessment",
            "6. Counterparty and Ownership Risk Assessment",
            "7. Jurisdiction, Route and Payment Risk Assessment",
            "8. Documentation Quality Assessment",
            "9. Transaction Decision Engine",
            "10. Due Diligence Actions",
            "13. Source Requirement Coverage",
            "14. Source Quality Notes",
            "15. Selected Sources",
        ]:
            section = extract_markdown_section(brief, heading)
            self.assertTrue(section, f"Expected section to be extractable: {heading}")
            if heading != "10. Due Diligence Actions":
                self.assertTrue(extract_markdown_table(section), f"Expected table in section: {heading}")

    def test_cyber_sections_can_be_extracted(self):
        brief = load_markdown(self.cyber_brief)
        for heading in [
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
        ]:
            section = extract_markdown_section(brief, heading)
            self.assertTrue(section, f"Expected section to be extractable: {heading}")
            self.assertTrue(extract_markdown_table(section), f"Expected table in section: {heading}")

    def test_helpers_work_for_all_active_case_briefs(self):
        uk_ets = load_markdown(self.uk_ets_brief)
        hormuz = load_markdown(self.hormuz_brief)
        critical_minerals = load_markdown(self.critical_minerals_brief)
        sanctions = load_markdown(self.sanctions_brief)
        cyber = load_markdown(self.cyber_brief)

        uk_section = extract_markdown_section(uk_ets, "1. Operator Stance")
        hormuz_section = extract_markdown_section(hormuz, "1. Decision Recommendation")
        critical_section = extract_markdown_section(critical_minerals, "1. Decision Recommendation")
        sanctions_section = extract_markdown_section(sanctions, "1. Decision Recommendation")
        cyber_section = extract_markdown_section(cyber, "1. Decision Recommendation")

        self.assertTrue(extract_markdown_table(uk_section))
        self.assertTrue(extract_markdown_table(hormuz_section))
        self.assertTrue(extract_markdown_table(critical_section))
        self.assertTrue(extract_markdown_table(sanctions_section))
        self.assertTrue(extract_markdown_table(cyber_section))
        self.assertIn("Current stance", str(extract_markdown_table(uk_section)[0][0]))
        self.assertIn("Preferred option", str(extract_markdown_table(hormuz_section)[0][0]))
        self.assertIn("Recommended action", str(extract_markdown_table(critical_section)[0][0]))
        self.assertIn("Recommended decision", str(extract_markdown_table(sanctions_section)[0][0]))
        self.assertIn("Recommended stance", str(extract_markdown_table(cyber_section)[0][0]))

    def test_dashboard_file_check_script_passes(self):
        result = subprocess.run(
            ["python3", "scripts/check_dashboard_files.py"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Dashboard file check passed.", result.stdout)

    def test_dashboard_presentation_copy_is_portfolio_ready(self):
        dashboard = Path("dashboard_app.py").read_text(encoding="utf-8")
        for phrase in [
            "Current showcase cases:",
            "The dashboard is designed as an expandable case portfolio.",
            "How to read this dashboard",
            "Start with the decision recommendation.",
            "Check the model output and key trigger.",
            "Review source caveats and company-data requirements before treating the result as operational.",
            "Decision Summary",
            "Source Governance Summary",
            "Selected Sources",
            "build_selected_source_rows",
            "LinkColumn",
            "Continuity Summary",
            "Cost/voyage",
            "Annual cost",
            "Break-even",
            "Gap",
            "Inventory",
            "Qualification",
            "Sanctions Trade Finance Exposure Engine",
            "Cyber Business Interruption Engine",
            "Legal hold",
            "Missing data",
            "Resilience gap",
            "Revenue at risk",
            "Expected outage",
            "First-Reader Summary",
            "Business problem",
            "Decision supported",
            "Evidence-to-output logic",
            "Company data needed",
            "UK ETS maritime expansion turns carbon policy into a route-level operating cost for in-scope UK voyages.",
            "Strait of Hormuz disruption can turn a voyage decision into a combined sanctions, insurance, detention and route-cost problem.",
            "A UK manufacturer may lose access to rare earth magnet inputs before an alternative supplier can be qualified.",
            "A trade finance transaction can become unacceptable where goods, counterparties, ownership, route, payment or documentation create sanctions/export-control exposure.",
            "Cyber disruption can turn digital trading, payment, fulfilment or service dependency into downtime, customer harm and revenue loss.",
            "Resilience Gap Summary",
            "technical cybersecurity advice, legal advice or an insurance coverage determination",
        ]:
            self.assertIn(phrase, dashboard)
        for phrase in ["TavilyClient", "live_search_mode", "st.json", "st.write(pack)", 'st.markdown("empty']:
            self.assertNotIn(phrase, dashboard)

    def test_selected_source_rows_build_for_all_active_cases(self):
        required_columns = {
            "Source ID",
            "Title",
            "Publisher",
            "Source role",
            "Source type",
            "Requirement",
            "Weight",
            "Decision use",
            "URL",
        }
        for pack_path in [self.uk_ets_pack, self.hormuz_pack, self.critical_minerals_pack, self.sanctions_pack, self.cyber_pack]:
            rows = build_selected_source_rows(load_json(pack_path))
            self.assertTrue(rows, f"Expected selected source rows for {pack_path}")
            for row in rows:
                self.assertEqual(required_columns, set(row))
                self.assertTrue(row["URL"], f"Expected URL for {row['Source ID']} in {pack_path}")
                self.assertTrue(row["Source role"], f"Expected source role for {row['Source ID']} in {pack_path}")
                self.assertNotEqual(row["Source role"], "source_role_unclassified")
                self.assertTrue(row["Source type"], f"Expected source type for {row['Source ID']} in {pack_path}")

    def test_uk_ets_source_taxonomy_is_conservative_in_dashboard_rows(self):
        rows = build_selected_source_rows(load_json(self.uk_ets_pack))
        by_title = {row["Title"]: row for row in rows}

        for title, row in by_title.items():
            if "ICCT" in title or "Stephenson Harwood" in title or "Azolla" in title:
                self.assertNotEqual(row["Source type"], "official_primary", title)

        gov_rows = [row for row in rows if "GOV.UK" in row["Title"]]
        self.assertTrue(gov_rows)
        self.assertEqual(gov_rows[0]["Source type"], "official_primary")
        self.assertEqual(gov_rows[0]["Source role"], "official_anchor")

    def test_source_quality_notes_are_visible_for_active_cases(self):
        self.assertIn("Source Quality Notes", load_markdown(self.uk_ets_brief))
        self.assertIn("Source Governance Summary", Path("dashboard_app.py").read_text(encoding="utf-8"))
        self.assertIn("Source Quality Notes", load_markdown(self.critical_minerals_brief))
        self.assertIn("Source Quality Notes", load_markdown(self.sanctions_brief))
        self.assertIn("Source Quality Notes", load_markdown(self.cyber_brief))


if __name__ == "__main__":
    unittest.main()
