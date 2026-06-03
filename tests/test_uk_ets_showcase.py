import json
import unittest
from pathlib import Path

from agent.brief_generator import generate_brief, select_report_template
from agent.risk_scoring import score_risk


class UKETSShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.brief_path = Path("showcase/uk_ets_shipping_operator_brief.md")
        self.audit_path = Path("showcase/uk_ets_source_audit.md")
        self.pack_path = Path("showcase/uk_ets_evidence_pack.json")

    def test_domain_pack_exists(self):
        packs = json.loads(Path("config/domain_packs.json").read_text(encoding="utf-8"))
        self.assertIn("regulatory_carbon_shipping", packs)

    def test_template_selection_works(self):
        self.assertEqual(
            select_report_template("UK ETS Maritime Expansion", "shipping_operator"),
            "uk_ets_shipping_operator_showcase",
        )

    def test_showcase_files_exist(self):
        self.assertTrue(self.brief_path.exists())
        self.assertTrue(self.audit_path.exists())
        self.assertTrue(self.pack_path.exists())

    def test_brief_contains_required_sections(self):
        text = self.brief_path.read_text(encoding="utf-8")
        for phrase in ["Operator Stance", "Applicability Check", "Carbon Cost Estimate"]:
            self.assertIn(phrase, text)
        for phrase in ["Start date: 1 July 2026", "Vessel threshold: 5,000 GT", "Estimated cost: £2,770 per voyage"]:
            self.assertIn(phrase, text)

    def test_evidence_pack_includes_source_requirements(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        self.assertIn("source_requirements", pack)
        self.assertGreaterEqual(len(pack["source_requirements"]), 8)
        self.assertEqual(pack["search_provider"], "tavily")
        self.assertEqual(pack["source_provider"], "tavily")
        self.assertFalse(pack["fallback_used"])
        self.assertFalse(pack["fallback_demo_data_used"])
        self.assertEqual(pack["evidence_mode"], "Live source retrieval")

    def test_uk_ets_selected_source_taxonomy_is_conservative(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        for source in pack["selected_sources"]:
            title = source["title"]
            if "ICCT" in title or "Stephenson Harwood" in title or "Azolla" in title:
                self.assertNotEqual(source["source_type"], "official_primary", title)
            self.assertTrue(source.get("source_role"), title)
            self.assertTrue(source.get("source_value_explanation"), title)
            self.assertTrue(source.get("url"), title)

        gov_source = next(source for source in pack["selected_sources"] if "GOV.UK" in source["title"])
        self.assertEqual(gov_source["source_type"], "official_primary")
        self.assertEqual(gov_source["source_role"], "official_anchor")

    def test_generate_brief_for_uk_ets(self):
        brief = generate_brief(
            topic="UK ETS Maritime Expansion",
            business_user="shipping_operator",
            region="UK domestic maritime",
            time_horizon="1-12 months",
            concerns=["carbon cost exposure"],
            sources=[],
        )
        self.assertIn("## 1. Operator Stance", brief)
        self.assertIn("## 2. Applicability Check", brief)

    def test_uk_ets_scores_reflect_confirmed_policy_and_confidence_cap(self):
        scores = score_risk(
            topic="UK ETS Maritime Expansion",
            concerns=["carbon cost exposure", "manual UKA price", "illustrative fuel consumption"],
            region="UK domestic maritime",
            time_horizon="1-12 months",
        )
        self.assertEqual(scores["likelihood"]["score"], 5)
        self.assertEqual(scores["immediacy"]["score"], 5)
        self.assertEqual(scores["confidence"]["score"], 4)
        self.assertLess(scores["confidence"]["score"], 5)


if __name__ == "__main__":
    unittest.main()
