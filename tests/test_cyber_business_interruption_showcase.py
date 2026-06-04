import json
import unittest
from pathlib import Path

from agent.cyber_business_interruption_model import build_cyber_business_interruption_model
from agent.source_requirements import generate_source_requirements


class CyberBusinessInterruptionShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.brief_path = Path("showcase/cyber_business_interruption_brief.md")
        self.audit_path = Path("showcase/cyber_source_audit.md")
        self.pack_path = Path("showcase/cyber_evidence_pack.json")

    def test_cyber_source_requirements_exist(self):
        requirements = generate_source_requirements(
            topic="Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services",
            business_user="customer_facing_operator",
            region="UK business exposed to ransomware and supplier/MSP compromise",
            time_horizon="1-6 months",
            concerns=["business interruption"],
            domain_pack={"domain": "cyber_business_interruption"},
        )

        names = {item["requirement_name"] for item in requirements}
        self.assertGreaterEqual(len(requirements), 9)
        self.assertIn("uk_official_cyber_threat_ncsc_evidence", names)
        self.assertIn("uk_cyber_breach_prevalence_data", names)
        self.assertIn("cyber_insurance_business_interruption_evidence", names)
        self.assertIn("incident_reporting_and_regulatory_notification_guidance", names)
        self.assertIn("supplier_msp_dependency_risk", names)
        self.assertIn("cyber_company_data_requirements_and_anti_overclaiming_controls", names)

    def test_business_interruption_model_calculates_exposure_and_gap(self):
        model = build_cyber_business_interruption_model(
            expected_outage_days=5,
            maximum_tolerable_downtime_days=2,
            daily_revenue_at_risk=2_000_000,
        )

        self.assertEqual(model["business_interruption_exposure"], 10_000_000)
        self.assertEqual(model["resilience_gap_days"], -3)
        self.assertIn("activate incident response", model["decision_implication"])
        self.assertIn("trigger cyber insurance claim process", model["decision_implication"])

    def test_saved_cyber_files_exist_and_are_live(self):
        self.assertTrue(self.brief_path.exists())
        self.assertTrue(self.audit_path.exists())
        self.assertTrue(self.pack_path.exists())

        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        self.assertEqual(pack.get("search_provider"), "tavily")
        self.assertEqual(pack.get("source_provider"), "tavily")
        self.assertFalse(pack.get("fallback_used"))
        self.assertFalse(pack.get("fallback_demo_data_used"))
        self.assertEqual(pack.get("evidence_mode"), "Live source retrieval")

    def test_brief_contains_required_sections_and_controls(self):
        brief = self.brief_path.read_text(encoding="utf-8")
        for phrase in [
            "Cyber Business Interruption Engine",
            "Decision Recommendation",
            "Dashboard Summary",
            "Incident Exposure Summary",
            "Operational Dependency Assessment",
            "Business Interruption Model",
            "Downtime / Revenue-at-Risk Assessment",
            "Regulatory Notification Assessment",
            "Insurance and Claims Readiness Assessment",
            "Supplier / MSP Dependency Risk",
            "Mitigation Options",
            "Risk Scorecard",
            "Evidence-To-Score Bridge",
            "Source Requirement Coverage",
            "Source Quality Notes",
            "Selected Sources",
            "Evidence Appendix",
            "Source Audit Summary",
            "Methodology and Review Controls",
            "business interruption exposure",
            "resilience gap",
            "negative three-day resilience gap",
            "This is a client-type cyber business interruption exposure screen, not technical cybersecurity advice, legal advice or an insurance coverage determination.",
            "affected systems and process map",
            "RTO / RPO",
            "cyber insurance policy wording",
        ]:
            self.assertIn(phrase, brief)

    def test_bridge_uses_cyber_business_interruption_language(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        bridge = pack["evidence_to_score_bridge"]

        self.assertIn("ransomware prevalence", bridge["likelihood"]["evidence_basis"])
        self.assertIn("downtime", bridge["impact"]["evidence_basis"])
        self.assertIn("resilience gap", bridge["immediacy"]["evidence_basis"])
        self.assertIn("policy wording", bridge["confidence"]["evidence_basis"])
        self.assertEqual(bridge["confidence"]["score"], 3)

    def test_technical_cybersecurity_advice_is_absent(self):
        brief = self.brief_path.read_text(encoding="utf-8")
        for phrase in [
            "firewall configuration",
            "malware reverse engineering",
            "exploit remediation",
            "network hardening",
            "voyage",
            "demurrage",
            "vessel",
            "charter",
            "cargo",
            "trade finance",
        ]:
            self.assertNotIn(phrase, brief)

    def test_source_roles_are_not_overstated(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        by_id = {source["source_id"]: source for source in pack["selected_sources"]}

        self.assertEqual(by_id["L1"]["source_role"], "official_anchor")
        self.assertEqual(by_id["L4"]["source_role"], "live_event_reporting")
        self.assertEqual(by_id["L5"]["source_role"], "insurance_market_evidence")
        self.assertEqual(by_id["L6"]["source_role"], "regulatory_guidance")
        self.assertEqual(by_id["L9"]["source_role"], "regulatory_guidance")
        self.assertNotEqual(by_id["L5"]["source_role"], "official_anchor")

    def test_existing_showcases_remain_present(self):
        for path in [
            Path("showcase/uk_ets_shipping_operator_brief.md"),
            Path("showcase/hormuz_shipping_operator_brief.md"),
            Path("showcase/critical_minerals_advanced_manufacturer_brief.md"),
            Path("showcase/sanctions_trade_finance_exposure_brief.md"),
        ]:
            self.assertTrue(path.exists())

    def test_dashboard_includes_offline_cyber_showcase(self):
        dashboard = Path("dashboard_app.py").read_text(encoding="utf-8")
        self.assertIn('SHOWCASE / "cyber_evidence_pack.json"', dashboard)
        self.assertIn('SHOWCASE / "cyber_business_interruption_brief.md"', dashboard)
        self.assertIn('SHOWCASE / "cyber_source_audit.md"', dashboard)
        self.assertIn("Cyber Business Interruption Engine", dashboard)
        self.assertIn("First-Reader Summary", dashboard)
        self.assertIn("Resilience Gap Summary", dashboard)
        self.assertNotIn("TavilyClient", dashboard)
        self.assertNotIn("live_search_mode", dashboard)
        self.assertNotIn(".env", dashboard)


if __name__ == "__main__":
    unittest.main()
