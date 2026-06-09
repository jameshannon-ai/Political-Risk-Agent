import json
import tempfile
import unittest
from pathlib import Path

from agent.core.workflow import run_topic_workflow
from agent.evidence_pack_builder import _requirement_coverage, build_evidence_pack
from agent.source_strategy import create_source_strategy


class GovernedWorkflowTests(unittest.TestCase):
    def _pack(self):
        strategy = create_source_strategy(
            "Fresh sanctions risk",
            "UK",
            "1-3 months",
            business_user="trade_finance_lender",
            concerns=["transaction approval"],
        )
        selected_sources = [
            {
                "source_id": "S1",
                "title": "Official sanctions guidance",
                "publisher": "GOV.UK",
                "url": "https://www.gov.uk/example",
                "publication_date": "2026-01-01",
                "source_type": "official_primary",
                "source_role": "official_anchor",
                "requirement_id": "REQ-A",
                "requirement_name": "uk_sanctions_guidance",
                "snippet": "Official guidance explains sanctions screening and escalation expectations for UK firms.",
                "decision_use": "Supports escalation and legal-hold thresholds for transaction approval.",
                "evidence_weight": "high",
                "selection_reason": "trusted official source",
            }
        ]
        search_result = {
            "provider": "manual_input",
            "fallback_demo_data_used": False,
            "evidence_mode": "Manual source input",
            "provider_error": "",
            "total_queries_run": 0,
            "candidate_sources": selected_sources,
            "candidates_by_query": {"manual": selected_sources},
            "search_failures": [],
        }
        fetched_result = {
            "fetched_sources": [
                {
                    **selected_sources[0],
                    "content": "Official guidance explains sanctions screening and escalation expectations for UK firms. Firms should assess counterparties, ownership and payments before approval.",
                    "fetch_status": "manual",
                    "manual_input": True,
                    "evidence_source_mode": "manual_input",
                }
            ],
            "fetch_failures": [],
        }
        return build_evidence_pack(
            topic="Fresh sanctions risk",
            business_user="trade_finance_lender",
            region="UK",
            time_horizon="1-3 months",
            concerns=["transaction approval"],
            source_strategy=strategy,
            search_result=search_result,
            selected_sources=selected_sources,
            rejected_sources=[],
            fetched_result=fetched_result,
        )

    def test_evidence_rows_include_extraction_and_provenance_fields(self):
        evidence = self._pack()["evidence"][0]
        for field in [
            "source_claim",
            "extracted_evidence",
            "analyst_inference",
            "inference_strength",
            "evidence_type",
            "quoted_excerpt_used",
            "extraction_confidence",
            "requires_human_review",
            "source_url",
            "source_title",
            "retrieval_timestamp",
            "evidence_source_mode",
            "content_hash",
            "source_excerpt_character_count",
            "source_limitations",
            "why_source_matters_for_decision",
        ]:
            self.assertIn(field, evidence)
        self.assertEqual(evidence["evidence_source_mode"], "manual_input")
        self.assertTrue(evidence["requires_human_review"])

    def test_scores_include_traceability_fields(self):
        pack = self._pack()
        self.assertIn("traceable_scores", pack)
        for dimension, score in pack["traceable_scores"].items():
            for field in [
                "score",
                "score_label",
                "score_type",
                "supporting_evidence",
                "contrary_evidence",
                "evidence_quality_limits",
                "missing_evidence",
                "reason_for_score",
                "reason_score_is_capped",
                "confidence",
                "review_required",
            ]:
                self.assertIn(field, score, dimension)
        self.assertEqual(pack["traceable_scores"]["likelihood"]["score_type"], "Evidence-backed decision-support score")

    def test_fresh_topic_workflow_generates_core_artefacts(self):
        notes = "\n".join(
            [
                "Source: S1",
                "Title: Official sanctions guidance",
                "Publisher: GOV.UK",
                "URL: https://www.gov.uk/example",
                "Type: official guidance",
                "Summary: Official guidance explains sanctions screening and escalation expectations for UK firms.",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_topic_workflow(
                topic="Fresh sanctions risk",
                business_user="trade_finance_lender",
                decision_context="Approve, escalate or hold a transaction.",
                region="UK",
                time_horizon="1-3 months",
                concerns=["transaction approval"],
                output_dir=tmpdir,
                source_notes=notes,
                live=False,
            )
            for key in ["evidence_pack_path", "source_audit_path", "brief_path"]:
                self.assertTrue(Path(result[key]).exists(), key)
            pack = json.loads(Path(result["evidence_pack_path"]).read_text(encoding="utf-8"))
            self.assertEqual(pack["source_provider"], "manual_input")
            self.assertFalse(pack["fallback_demo_data_used"])
            self.assertIn("traceable_scores", pack)
            audit = Path(result["source_audit_path"]).read_text(encoding="utf-8")
            self.assertIn("Provenance And Extraction Limits", audit)
            self.assertIn("Scoring Traceability", audit)

    def test_requirement_coverage_uses_specific_mapping_before_source_type_fallback(self):
        requirements = [
            {
                "requirement_id": "REQ-ONE",
                "requirement_name": "official_policy_one",
                "minimum_sources": 1,
                "priority": "high",
                "why_required": "First official requirement.",
            },
            {
                "requirement_id": "REQ-TWO",
                "requirement_name": "official_policy_two",
                "minimum_sources": 1,
                "priority": "high",
                "why_required": "Second official requirement.",
            },
        ]
        evidence = [
            {
                "source_id": "L1",
                "source_type": "official_primary",
                "requirement_id": "REQ-ONE",
                "requirement_name": "official_policy_one",
                "evidence_weight": "high",
            }
        ]

        coverage = _requirement_coverage(requirements, evidence)

        by_id = {item["requirement_id"]: item for item in coverage}
        self.assertEqual(by_id["REQ-ONE"]["covered_by"], ["L1"])
        self.assertEqual(by_id["REQ-TWO"]["covered_by"], [])
        self.assertEqual(by_id["REQ-ONE"]["coverage_grade"], "partial_or_indirect")
        self.assertEqual(by_id["REQ-TWO"]["coverage_grade"], "missing")

    def test_core_modules_do_not_import_dashboard_dependencies(self):
        root = Path(__file__).resolve().parents[1]
        for relative in [
            "agent/core/workflow.py",
            "agent/core/provenance.py",
            "agent/core/scoring.py",
        ]:
            text = (root / relative).read_text(encoding="utf-8")
            self.assertNotIn("streamlit", text.lower(), relative)
            self.assertNotIn("dashboard_app", text, relative)

    def test_dashboard_has_streamlit_import_fallback(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "dashboard_app.py").read_text(encoding="utf-8")
        self.assertIn("except ImportError", text)
        self.assertIn("_StreamlitUnavailable", text)


if __name__ == "__main__":
    unittest.main()
