import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase"


class FiscalProcurementShowcaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack_path = SHOWCASE / "uk_fiscal_instability_procurement_evidence_pack.json"
        cls.brief_path = SHOWCASE / "uk_fiscal_instability_procurement_brief.md"
        cls.audit_path = SHOWCASE / "uk_fiscal_instability_procurement_source_audit.md"
        cls.pack = json.loads(cls.pack_path.read_text(encoding="utf-8"))
        cls.brief = cls.brief_path.read_text(encoding="utf-8")
        cls.audit = cls.audit_path.read_text(encoding="utf-8")

    def test_fiscal_showcase_files_exist_and_are_live_backed(self):
        self.assertTrue(self.pack_path.exists())
        self.assertTrue(self.brief_path.exists())
        self.assertTrue(self.audit_path.exists())
        self.assertEqual(self.pack["source_provider"], "tavily")
        self.assertEqual(self.pack["evidence_mode"], "Live source retrieval")
        self.assertFalse(self.pack["fallback_demo_data_used"])
        self.assertGreaterEqual(self.pack["selected_count"], 5)

    def test_evidence_rows_have_meaningful_extraction_and_provenance(self):
        required_fields = [
            "source_id",
            "source_url",
            "source_title",
            "publisher",
            "source_claim",
            "extracted_evidence",
            "analyst_inference",
            "inference_strength",
            "evidence_type",
            "quoted_excerpt_used",
            "extraction_confidence",
            "evidence_source_mode",
            "source_limitations",
            "why_source_was_selected",
            "why_source_matters_for_decision",
        ]
        for row in self.pack["evidence"]:
            for field in required_fields:
                self.assertTrue(row.get(field), f"{row.get('source_id')} missing {field}")
            claim_text = " ".join(
                [
                    row.get("source_claim", ""),
                    row.get("extracted_evidence", ""),
                    row.get("analyst_inference", ""),
                ]
            )
            self.assertNotIn("We use some essential", claim_text)
            self.assertNotIn("<script", claim_text.lower())
            self.assertNotEqual(row["source_claim"], row["analyst_inference"])

    def test_snippet_only_rows_trigger_review_and_lower_confidence(self):
        snippet_rows = [row for row in self.pack["evidence"] if row.get("evidence_source_mode") == "snippet_only"]
        self.assertTrue(snippet_rows)
        for row in snippet_rows:
            self.assertTrue(row.get("requires_human_review"), row.get("source_id"))
            self.assertIn(row.get("extraction_confidence"), {"low", "medium"})

    def test_traceable_scores_reference_evidence_and_cap_confidence(self):
        traceable = self.pack["traceable_scores"]
        for dimension in ["likelihood", "impact", "immediacy", "exposure", "confidence", "decision_urgency"]:
            score = traceable[dimension]
            self.assertTrue(score["supporting_evidence"], dimension)
            self.assertIn("contrary_evidence", score)
            self.assertIn("evidence_quality_limits", score)
            self.assertTrue(score["reason_for_score"], dimension)
            self.assertTrue(score["reason_score_is_capped"], dimension)
            for ref in score["supporting_evidence"]:
                self.assertRegex(ref, r"^L\d+")
        quality_ids = set(traceable["likelihood"]["evidence_quality_limits"])
        contrary_ids = set(traceable["likelihood"]["contrary_evidence"])
        self.assertIn("L8", contrary_ids)
        self.assertNotEqual(quality_ids, contrary_ids)
        self.assertLessEqual(traceable["confidence"]["score"], 3)
        self.assertIn("contractor order book", " ".join(traceable["confidence"]["missing_evidence"]))

    def test_brief_and_audit_are_case_specific_not_generic(self):
        for phrase in [
            "UK infrastructure contractor",
            "political-economy risk",
            "bid pipeline",
            "payment-risk monitoring",
            "contract repricing",
            "working-capital exposure",
            "Scoring Traceability",
            "Human Review And Company Data Required",
        ]:
            self.assertIn(phrase, self.brief)
        for forbidden in [
            "Missing insurance evidence",
            "energy chokepoint",
            "underwriting",
            "carrier/company updates",
            "Illustrative Route-Cost Scenario",
            "voyage",
            "cargo",
        ]:
            self.assertNotIn(forbidden, self.brief)
            self.assertNotIn(forbidden, self.audit)
        self.assertIn("Scenario And Exposure Limits", self.audit)
        self.assertIn("Provenance And Extraction Limits", self.audit)
        self.assertIn("Scoring Traceability", self.audit)
        self.assertIn("Coverage Grade", self.audit)
        self.assertIn("Direct snippet-only", self.audit)

    def test_source_taxonomy_is_conservative_for_selected_sources(self):
        source_l6 = next(source for source in self.pack["selected_sources"] if source["source_id"] == "L6")
        evidence_l6 = next(row for row in self.pack["evidence"] if row["source_id"] == "L6")
        self.assertEqual(source_l6["source_type"], "official_primary")
        self.assertEqual(source_l6["source_role"], "official_anchor")
        self.assertIn("NAO", evidence_l6["source_claim"])
        source_l9 = next(source for source in self.pack["selected_sources"] if source["source_id"] == "L9")
        self.assertEqual(source_l9["source_type"], "industry_guidance")
        self.assertEqual(source_l9["source_role"], "company_required_data")

    def test_coverage_grades_are_visible_and_not_binary(self):
        grades = {row["requirement_name"]: row["coverage_grade"] for row in self.pack["requirement_coverage"]}
        self.assertIn("strong_direct_full_text", set(grades.values()))
        self.assertIn("direct_snippet_only", set(grades.values()))
        for row in self.pack["requirement_coverage"]:
            self.assertIn("coverage_grade_reason", row)
            self.assertIn("gap_affects_confidence", row)


if __name__ == "__main__":
    unittest.main()
