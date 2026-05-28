import json
import unittest
from pathlib import Path

from agent.brief_generator import generate_brief


class SanctionsShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.sample_path = Path("showcase/sanctions_trade_finance_sample.md")
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
        self.assertIn("## 1. Transaction Stance", self.sample)
        self.assertIn("## Quantified Evidence Readout", self.sample)
        self.assertIn("## Evidence-To-Score Bridge", self.sample)
        self.assertIn("## 8. Payment and Documentation Risk", self.sample)
        self.assertIn("## 10. Compliance Escalation", self.sample)
        self.assertIn("## 14. Source Requirement Coverage", self.sample)
        self.assertIn("official/legal source count", self.sample)
        self.assertIn("| Judgement | Evidence basis | Concrete signal | Client relevance |", self.sample)

    def test_sanctions_pack_and_audit_include_governance(self):
        self.assertIn("source_requirements", self.pack)
        self.assertGreaterEqual(len(self.pack["source_requirements"]), 7)
        self.assertIn("Reliability", self.audit)
        self.assertIn("Decision value", self.audit)
        self.assertIn("Evidence weight", self.audit)

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
