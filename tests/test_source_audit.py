import json
import tempfile
import unittest
from pathlib import Path

from agent.evidence_pack_builder import build_evidence_pack
from agent.source_audit import generate_source_audit, save_source_audit
from agent.source_strategy import create_source_strategy


class SourceAuditTests(unittest.TestCase):
    def test_source_audit_file_creation(self):
        source = {
            "source_id": "H1",
            "title": "Official Hormuz advisory",
            "publisher": "Official body",
            "url": "https://www.imo.org/example",
            "publication_date": "2026-05-01",
            "source_type": "official_primary",
            "snippet": "Official advisory on Strait of Hormuz transit.",
            "ranking_score": 10,
            "total_score": 30,
            "reliability_score": 5,
            "relevance_score": 5,
            "recency_score": 5,
            "specificity_score": 4,
            "decision_value_score": 5,
            "independence_score": 5,
            "evidence_weight": "high",
            "requirement_id": "REQ-A",
            "requirement_name": "official_maritime_security",
            "selection_reason": "trusted domain",
            "evidence_value": "Primary safety baseline.",
            "decision_use": "Supports enhanced referral and route-level controls.",
        }
        strategy = create_source_strategy("Strait of Hormuz disruption", "Persian Gulf", "1-3 months")
        pack = build_evidence_pack(
            topic="Strait of Hormuz disruption",
            business_user="marine_insurer",
            region="Persian Gulf",
            time_horizon="1-3 months",
            concerns=["war-risk premiums"],
            source_strategy=strategy,
            search_result={
                "provider": "fallback_demo_search",
                "fallback_demo_data_used": True,
                "candidate_sources": [source],
                "candidates_by_query": {"query": [source]},
                "search_failures": [],
            },
            selected_sources=[source],
            rejected_sources=[{"title": "Rejected source", "url": "https://example.com", "source_type": "unknown", "ranking_score": 1, "rejection_reason": "weak relevance"}],
            fetched_result={"fetched_sources": [{**source, "content": source["snippet"], "fetch_status": "demo"}], "fetch_failures": []},
        )
        pack["duplicate_urls_removed"] = 0
        markdown = generate_source_audit(pack)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = save_source_audit(markdown, Path(tmpdir), pack["topic"])
            self.assertTrue(path.exists())
            written = path.read_text(encoding="utf-8")
            self.assertIn("# Source Audit", written)
            self.assertIn("## Research Plan", written)
            self.assertIn("## Source Requirement Coverage", written)
            self.assertIn("| Source ID | Requirement | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use |", written)
            self.assertIn("| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |", written)

    def test_uk_ets_audit_uses_domain_specific_refresh_triggers(self):
        pack = {
            "topic": "UK ETS Maritime Expansion",
            "business_user": "shipping_operator",
            "region": "UK domestic maritime",
            "time_horizon": "1-12 months",
            "concerns": ["carbon cost exposure"],
            "search_provider": "tavily",
            "evidence_mode": "Live source retrieval",
            "fallback_demo_data_used": False,
            "provider_error": "",
            "retrieval_timestamp": "2026-05-28T16:54:46",
            "source_plan": {"research_objective": "Objective", "decision_questions": [], "required_source_mix": [], "expected_evidence_types": [], "minimum_acceptable_coverage": {}, "refresh_priorities": []},
            "source_strategy": {"domain": "regulatory_carbon_shipping", "categories": []},
            "candidate_count": 8,
            "total_queries_run": 34,
            "selected_count": 1,
            "duplicate_urls_removed": 0,
            "source_categories_covered": ["official_primary"],
            "source_categories_missing": [],
            "fetch_failures": [],
            "selected_sources": [],
            "rejected_sources": [],
            "evidence": [],
            "requirement_coverage": [],
            "quantified_evidence_readout": {"score_support_summary": "summary"},
            "confidence_cap_reason": "Confidence capped below 5 because manual inputs remain.",
            "refresh_priorities": [],
        }

        markdown = generate_source_audit(pack)

        self.assertIn("Refresh UKA price before pricing or contract decisions.", markdown)
        self.assertIn("Review emissions factor methodology with verifier / MRV process.", markdown)


if __name__ == "__main__":
    unittest.main()
