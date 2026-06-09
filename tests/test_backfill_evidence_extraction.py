import json
import tempfile
import unittest
from pathlib import Path

from scripts.backfill_evidence_extraction import backfill_evidence_pack


class BackfillEvidenceExtractionTests(unittest.TestCase):
    def test_backfill_uses_stored_material_without_live_retrieval(self):
        pack = {
            "fallback_demo_data_used": False,
            "retrieval_timestamp": "2026-06-09T12:00:00",
            "selected_sources": [
                {
                    "source_id": "L1",
                    "title": "Official source",
                    "url": "https://example.com/source",
                    "publisher": "Example",
                    "source_type": "official_primary",
                    "source_role": "official_anchor",
                    "fetch_status": "snippet_used",
                    "snippet": "Official source says procurement timing can change when budgets are reset.",
                    "decision_use": "Supports procurement-delay review.",
                }
            ],
            "evidence": [
                {
                    "source_id": "L1",
                    "claim_supported": "Official source supports procurement-delay review.",
                    "fetch_status": "snippet_used",
                    "snippet": "Official source says procurement timing can change when budgets are reset.",
                    "source_type": "official_primary",
                    "decision_use": "Supports procurement-delay review.",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            pack_path = Path(tmp) / "pack.json"
            pack_path.write_text(json.dumps(pack), encoding="utf-8")
            result = backfill_evidence_pack(pack_path, Path(tmp) / "out")
            enriched = result["pack"]

        self.assertFalse(enriched["backfill_report"]["live_retrieval_used"])
        row = enriched["evidence"][0]
        self.assertEqual(row["evidence_source_mode"], "snippet_only")
        self.assertTrue(row["requires_human_review"])
        self.assertEqual(row["extraction_confidence"], "low")
        self.assertIn("Official source says procurement timing", row["quoted_excerpt_used"])


if __name__ == "__main__":
    unittest.main()
