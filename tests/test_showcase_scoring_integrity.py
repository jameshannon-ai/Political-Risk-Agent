import json
import unittest
from pathlib import Path


ACTIVE_PACKS = [
    Path("showcase/hormuz_evidence_pack.json"),
    Path("showcase/sanctions_evidence_pack.json"),
    Path("showcase/uk_ets_evidence_pack.json"),
    Path("showcase/critical_minerals_evidence_pack.json"),
    Path("showcase/cyber_evidence_pack.json"),
    Path("showcase/uk_fiscal_instability_procurement_evidence_pack.json"),
]


class ShowcaseScoringIntegrityTests(unittest.TestCase):
    def test_active_showcases_have_traceable_scores(self):
        for path in ACTIVE_PACKS:
            pack = _load(path)
            self.assertTrue(pack.get("traceable_scores"), f"{path} missing traceable_scores")

    def test_every_score_has_integrity_fields(self):
        required = {
            "dimension",
            "score",
            "score_label",
            "score_type",
            "supporting_evidence",
            "weakening_evidence",
            "missing_evidence",
            "confidence_cap_applied",
            "confidence_cap_reason",
            "reason_for_score",
            "review_required",
        }
        allowed_types = {"evidence_backed", "analyst_assumption", "illustrative_fallback"}
        for path in ACTIVE_PACKS:
            pack = _load(path)
            for dimension, score in pack["traceable_scores"].items():
                self.assertTrue(required.issubset(score), f"{path} {dimension} missing scoring fields")
                self.assertEqual(score["dimension"], dimension)
                self.assertIn(score["score_type"], allowed_types)
                self.assertIsInstance(score["supporting_evidence"], list)
                self.assertIsInstance(score["weakening_evidence"], list)
                self.assertIsInstance(score["missing_evidence"], list)
                self.assertIsInstance(score["confidence_cap_applied"], bool)
                self.assertIsInstance(score["review_required"], bool)

    def test_evidence_backed_scores_must_have_supporting_evidence(self):
        for path in ACTIVE_PACKS:
            pack = _load(path)
            for dimension, score in pack["traceable_scores"].items():
                if score["score_type"] == "evidence_backed":
                    self.assertTrue(score["supporting_evidence"], f"{path} {dimension} is evidence_backed without sources")

    def test_hardcoded_showcase_scores_are_not_mislabeled_as_evidence_backed(self):
        for path in ACTIVE_PACKS:
            pack = _load(path)
            for dimension, score in pack["traceable_scores"].items():
                self.assertIn(
                    score["score_type"],
                    {"analyst_assumption", "illustrative_fallback", "evidence_backed"},
                    f"{path} {dimension} missing explicit static-score label",
                )
                if score["score_type"] in {"analyst_assumption", "illustrative_fallback"}:
                    self.assertTrue(score["reason_for_score"], f"{path} {dimension} needs score rationale")

    def test_snippet_only_confidence_cap(self):
        for path in ACTIVE_PACKS:
            pack = _load(path)
            evidence_by_id = {item.get("source_id"): item for item in pack.get("evidence", [])}
            confidence = pack["traceable_scores"]["confidence"]
            supporting = [evidence_by_id.get(source_id, {}) for source_id in confidence.get("supporting_evidence", [])]
            modes = [item.get("evidence_source_mode") for item in supporting if item.get("evidence_source_mode")]
            if modes and sum(1 for mode in modes if mode == "snippet_only") > len(modes) / 2:
                self.assertLessEqual(confidence["score"], 3, f"{path} confidence should be capped for snippet-only support")
                self.assertTrue(confidence["confidence_cap_applied"], f"{path} confidence cap flag missing")
                self.assertIn("snippet", confidence["confidence_cap_reason"].lower())


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
