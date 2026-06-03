import json
import unittest
from pathlib import Path

from agent.brief_generator import generate_brief
from agent.sanctions_transaction_decision_engine import evaluate_sanctions_transaction_decision


class SanctionsShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.sample_path = Path("showcase/sanctions_trade_finance_exposure_brief.md")
        self.audit_path = Path("showcase/sanctions_source_audit.md")
        self.pack_path = Path("showcase/sanctions_evidence_pack.json")
        self.sample = self.sample_path.read_text(encoding="utf-8")
        self.audit = self.audit_path.read_text(encoding="utf-8")
        self.pack = json.loads(self.pack_path.read_text(encoding="utf-8"))

    def test_sanctions_trade_finance_sample_is_generated(self):
        self.assertTrue(self.sample_path.exists())
        self.assertTrue(self.audit_path.exists())
        self.assertTrue(self.pack_path.exists())

    def test_sanctions_sample_has_trade_finance_sections(self):
        for phrase in [
            "## Sanctions Trade Finance Exposure Engine",
            "## 1. Decision Recommendation",
            "## 3. Dashboard Summary",
            "## 4. Transaction Exposure Summary",
            "## 5. Goods and End-Use Risk Assessment",
            "## 6. Counterparty and Ownership Risk Assessment",
            "## 7. Jurisdiction, Route and Payment Risk Assessment",
            "## 8. Documentation Quality Assessment",
            "## 9. Transaction Decision Engine",
            "## 10. Due Diligence Actions",
            "## 12. Evidence-To-Score Bridge",
            "## 13. Source Requirement Coverage",
            "## 14. Source Quality Notes",
            "## 15. Selected Sources",
            "This is a client-type sanctions and trade-finance exposure screen, not legal advice and not a transaction clearance decision.",
            "Transaction-specific use requires",
        ]:
            self.assertIn(phrase, self.sample)

    def test_sanctions_pack_and_audit_include_governance(self):
        self.assertIn("source_requirements", self.pack)
        self.assertGreaterEqual(len(self.pack["source_requirements"]), 9)
        self.assertEqual(self.pack.get("search_provider"), "tavily")
        self.assertEqual(self.pack.get("source_provider"), "tavily")
        self.assertFalse(self.pack.get("fallback_used"))
        self.assertFalse(self.pack.get("fallback_demo_data_used"))
        self.assertEqual(self.pack.get("evidence_mode"), "Live source retrieval")
        self.assertIn("Research Plan", self.audit)
        self.assertIn("Source Requirement Coverage", self.audit)
        self.assertIn("Source Quality Notes", self.audit)
        self.assertIn("Evidence-To-Score Bridge", self.audit)

    def test_sanctions_selected_sources_have_dashboard_fields(self):
        for source in self.pack.get("selected_sources", []):
            for field in [
                "source_id",
                "title",
                "publisher",
                "url",
                "source_type",
                "source_role",
                "source_value_explanation",
                "requirement_name",
                "evidence_weight",
                "decision_use",
                "caveat",
                "refresh_trigger",
            ]:
                self.assertTrue(source.get(field), f"{source.get('source_id')} missing {field}")

    def test_sanctions_transaction_model_triggers_hold_and_reject(self):
        result = evaluate_sanctions_transaction_decision(
            sanctioned_counterparty_confirmed=True,
            transaction_specific_data_available=False,
        )

        self.assertTrue(result["legal_hold_required"])
        self.assertTrue(result["rejection_triggered"])
        self.assertIn("reject", result["recommended_decision"])

    def test_missing_documentation_triggers_hold_or_escalation(self):
        result = evaluate_sanctions_transaction_decision(
            documentation_quality="missing",
            transaction_specific_data_available=False,
        )

        self.assertTrue(result["escalation_required"])
        self.assertTrue(result["legal_hold_required"])
        self.assertIn("invoice pack", result["missing_documents"])

    def test_confidence_capped_without_transaction_specific_data(self):
        result = evaluate_sanctions_transaction_decision(
            goods_control_risk="low",
            counterparty_risk="low",
            jurisdiction_route_risk="low",
            documentation_quality="strong",
            ownership_transparency="clear",
            licence_or_authorisation_status="confirmed",
            payment_red_flag=False,
            vessel_or_logistics_red_flag=False,
            end_use_red_flag=False,
            transaction_specific_data_available=False,
        )

        self.assertEqual(result["recommended_decision"], "approve")
        self.assertLessEqual(result["confidence_score"], 3)

    def test_sanctions_sample_excludes_marine_insurance_only_sections(self):
        for phrase in ["Hull war", "Cargo war", "War-risk premium", "Marine Insurance Implications"]:
            self.assertNotIn(phrase, self.sample)

    def test_product_docs_avoid_what_this_demonstrates(self):
        for path in [Path("README.md"), Path("showcase/README.md")]:
            self.assertNotIn("what this demonstrates", path.read_text(encoding="utf-8").lower())

    def test_hormuz_showcase_still_exists(self):
        self.assertTrue(Path("showcase/hormuz_shipping_operator_brief.md").exists())
        self.assertTrue(Path("showcase/archive/hormuz_marine_insurer_brief.md").exists())
        self.assertTrue(Path("showcase/hormuz_source_audit.md").exists())
        self.assertTrue(Path("showcase/hormuz_evidence_pack.json").exists())
        self.assertTrue(Path("showcase/uk_ets_shipping_operator_brief.md").exists())

    def test_generic_political_risk_path_still_works(self):
        brief = generate_brief(
            topic="Election uncertainty affecting energy investors",
            business_user="consultant",
            region="Europe",
            time_horizon="3 months",
            concerns=["policy uncertainty"],
            sources=[],
        )

        self.assertIn("## Executive Judgement", brief)
        self.assertNotIn("Transaction Stance", brief)
        self.assertNotIn("Exposure Pressure Map", brief)


if __name__ == "__main__":
    unittest.main()
