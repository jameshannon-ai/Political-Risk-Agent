import json
import unittest
from pathlib import Path

from agent.brief_generator import generate_brief, _source_requirement_coverage
from agent.evidence_pack_builder import build_evidence_pack
from agent.source_strategy import create_source_strategy


class BriefGeneratorStructureTests(unittest.TestCase):
    def setUp(self):
        case_path = Path("examples/hormuz_real_evidence_case.json")
        selected_sources = json.loads(case_path.read_text(encoding="utf-8"))["demo_search_results"]
        source_strategy = create_source_strategy(
            "Strait of Hormuz Transit Controls",
            "Persian Gulf / UK shipping operators",
            "1-3 months",
            business_user="shipping_operator",
        )
        search_result = {
            "provider": "fallback_demo_search",
            "fallback_demo_data_used": True,
            "candidate_sources": selected_sources,
            "candidates_by_query": {source["title"]: [source] for source in selected_sources},
            "search_failures": [],
        }
        fetched_result = {
            "fetched_sources": [{**source, "content": source["claim_supported"], "fetch_status": "demo"} for source in selected_sources],
            "fetch_failures": [],
        }
        self.evidence_pack = build_evidence_pack(
            topic="Strait of Hormuz Transit Controls",
            business_user="shipping_operator",
            region="Persian Gulf / UK shipping operators",
            time_horizon="1-3 months",
            concerns=["transit controls", "sanctions exposure"],
            source_strategy=source_strategy,
            search_result=search_result,
            selected_sources=selected_sources,
            fetched_result=fetched_result,
        )
        self.brief = generate_brief(
            topic="Strait of Hormuz Transit Controls",
            business_user="shipping_operator",
            region="Persian Gulf / UK shipping operators",
            time_horizon="1-3 months",
            concerns=["transit controls", "sanctions exposure", "war-risk insurance premiums"],
            sources=self.evidence_pack["evidence"],
            evidence_pack=self.evidence_pack,
        )

    def test_required_shipping_operator_sections_are_present(self):
        for phrase in [
            "## 1. Operator Decision Stance",
            "## 7. Voyage Decision Matrix",
            "## 8. Sanctions and Safe-Passage Risk",
            "## 11. Dynamic Route-Cost Assessment",
            "## 13. Recommended Operator Actions",
        ]:
            self.assertIn(phrase, self.brief)

    def test_shipping_operator_brief_omits_marine_insurer_only_sections(self):
        for phrase in ["Marine Insurer Exposure Assessment", "Exposure Pressure Map", "Recommended Underwriting Actions"]:
            self.assertNotIn(phrase, self.brief)

    def test_fallback_confidence_is_capped(self):
        self.assertIn("| Confidence | 4/5 |", self.brief)
        self.assertIn("Reproducible curated source pack", self.brief)
        self.assertIn("Illustrative voyage assumptions requiring operator validation.", self.brief)

    def test_generic_output_still_works(self):
        brief = generate_brief(
            topic="Port disruption",
            business_user="shipping_operator",
            region="Northern Europe",
            time_horizon="30 days",
            concerns=["port access"],
            sources=[],
        )

        self.assertIn("## Executive Judgement", brief)
        self.assertNotIn("Voyage Decision Matrix", brief)

    def test_strongest_source_is_populated_for_covered_requirements(self):
        evidence_pack = {
            "selected_sources": [
                {
                    "source_id": "L1",
                    "title": "GOV.UK UK ETS scope expansion",
                    "evidence_weight": "high",
                    "total_score": 25,
                }
            ],
            "requirement_coverage": [
                {
                    "requirement_name": "policy_scope",
                    "covered_by": ["L1"],
                    "covered_by_count": 1,
                    "evidence_weight": "high",
                    "decision_questions_supported": ["Does the route fall in scope?"],
                    "remaining_gap": "No immediate coverage gap.",
                }
            ],
        }

        coverage = _source_requirement_coverage(evidence_pack)

        self.assertIn("L1", coverage)
        self.assertIn("GOV.UK UK ETS scope expansion", coverage)
        self.assertNotIn("| None |", coverage)


if __name__ == "__main__":
    unittest.main()
