import json
import unittest
from pathlib import Path

from agent.evidence_pack_builder import build_evidence_pack
from agent.quantitative_assessment import build_evidence_to_score_bridge, build_quantified_evidence_readout
from agent.risk_scoring import score_risk
from agent.source_strategy import create_source_strategy


class QuantitativeAssessmentTests(unittest.TestCase):
    def setUp(self):
        sources = json.loads(Path("examples/hormuz_real_evidence_case.json").read_text(encoding="utf-8"))["demo_search_results"]
        strategy = create_source_strategy(
            "Strait of Hormuz disruption",
            "Persian Gulf / UK marine insurance market",
            "1-3 months",
            business_user="marine_insurer",
        )
        self.pack = build_evidence_pack(
            topic="Strait of Hormuz disruption",
            business_user="marine_insurer",
            region="Persian Gulf / UK marine insurance market",
            time_horizon="1-3 months",
            concerns=["war-risk premiums"],
            source_strategy=strategy,
            search_result={
                "provider": "fallback_demo_search",
                "fallback_demo_data_used": True,
                "candidate_sources": sources,
                "candidates_by_query": {"query": sources},
                "search_failures": [],
            },
            selected_sources=sources,
            fetched_result={"fetched_sources": [{**source, "content": source["claim_supported"], "fetch_status": "demo"} for source in sources], "fetch_failures": []},
        )

    def test_quantitative_assessment_module_outputs_readout(self):
        readout = build_quantified_evidence_readout(self.pack)

        self.assertGreater(readout["source_count"], 0)
        self.assertIn("capped", readout["confidence_cap"].lower())
        self.assertTrue(readout["quantified_facts"])

    def test_evidence_pack_includes_quantified_readout(self):
        self.assertIn("quantified_evidence_readout", self.pack)
        self.assertIn("evidence_to_score_bridge", self.pack)
        self.assertIn("confidence_cap_reason", self.pack)

    def test_evidence_to_score_bridge_has_dimensions(self):
        scores = score_risk("Strait of Hormuz disruption", ["war-risk premiums"], "Persian Gulf", "1-3 months", self.pack["evidence"])
        bridge = build_evidence_to_score_bridge(self.pack, scores)

        for dimension in ["likelihood", "impact", "immediacy", "confidence"]:
            self.assertIn("why_score_not_higher", bridge[dimension])
            self.assertIn("review_trigger", bridge[dimension])

    def test_uk_ets_quantified_readout_uses_labelled_facts(self):
        pack = {
            "source_strategy": {"domain": "regulatory_carbon_shipping"},
            "calculator_assumptions": {
                "fuel_consumption_tonnes_per_voyage": 18,
                "coverage_rate": 1.0,
                "uka_price_per_tonne": 48,
                "voyages_per_week": 6,
            },
            "selected_sources": [{"source_id": "L7", "evidence_weight": "high", "total_score": 25, "title": "GOV.UK UK ETS Maritime Scope Expansion"}],
            "evidence": [{"source_id": "L7"}],
            "requirement_coverage": [],
            "fallback_demo_data_used": False,
        }

        readout = build_quantified_evidence_readout(pack)

        self.assertIn("Start date: 1 July 2026", readout["quantified_facts"])
        self.assertIn("Estimated cost: £2,770 per voyage", readout["quantified_facts"])


if __name__ == "__main__":
    unittest.main()
