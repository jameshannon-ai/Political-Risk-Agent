import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "outputs" / "tavily_regeneration_review_20260610-145056" / "candidate_promoted_showcase"


class SourcePromotionTests(unittest.TestCase):
    def test_candidate_promoted_packs_exist(self):
        for case_id in ["hormuz", "sanctions", "uk_ets", "critical_minerals", "cyber", "fiscal"]:
            self.assertTrue((CANDIDATES / f"{case_id}_candidate_evidence_pack.json").exists())
            self.assertTrue((CANDIDATES / f"{case_id}_source_promotion_report.json").exists())
            self.assertTrue((CANDIDATES / f"{case_id}_candidate_brief.md").exists())

    def test_sitemap_xml_or_generic_index_sources_are_not_promoted(self):
        for report_path in CANDIDATES.glob("*_source_promotion_report.json"):
            rows = json.loads(report_path.read_text(encoding="utf-8"))
            for row in rows:
                text = " ".join([row.get("title", ""), row.get("url", "")]).lower()
                if any(marker in text for marker in ["sitemap", ".xml", "search results"]):
                    self.assertNotIn(row["promotion_decision"], {"promote", "promote_with_review"}, row)

    def test_rejected_sources_do_not_support_scores(self):
        for pack_path in CANDIDATES.glob("*_candidate_evidence_pack.json"):
            pack = json.loads(pack_path.read_text(encoding="utf-8"))
            rejected_ids = {source.get("source_id") for source in pack.get("rejected_regenerated_sources", [])}
            for score in pack.get("traceable_scores", {}).values():
                self.assertFalse(rejected_ids & set(score.get("supporting_evidence", [])), pack_path)

    def test_snippet_only_promotion_requires_review(self):
        for pack_path in CANDIDATES.glob("*_candidate_evidence_pack.json"):
            pack = json.loads(pack_path.read_text(encoding="utf-8"))
            for item in pack.get("evidence", []):
                if item.get("evidence_source_mode") == "snippet_only" and item.get("promotion_decision") == "promote_with_review":
                    self.assertTrue(item.get("review_required") or item.get("requires_human_review"), item)

    def test_candidate_briefs_preserve_source_quality_notes(self):
        for brief_path in CANDIDATES.glob("*_candidate_brief.md"):
            text = brief_path.read_text(encoding="utf-8")
            if "cyber_candidate" in brief_path.name or "fiscal_candidate" in brief_path.name:
                continue
            self.assertIn("Source Quality Notes", text, brief_path)
            self.assertIn("Evidence-To-Score Bridge", text, brief_path)


if __name__ == "__main__":
    unittest.main()

