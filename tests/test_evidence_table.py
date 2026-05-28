import unittest

from agent.evidence_table import assign_evidence_strength


class EvidenceTableTests(unittest.TestCase):
    def test_official_and_company_sources_are_high_strength(self):
        official = {"inferred_source_type": "official_primary", "summary": "Reports vessel incident."}
        company = {"inferred_source_type": "company_update", "summary": "Carrier avoids route."}

        self.assertEqual(assign_evidence_strength(official), "high")
        self.assertEqual(assign_evidence_strength(company), "high")

    def test_unknown_source_is_low_strength(self):
        source = {"inferred_source_type": "unknown", "summary": "Unclear claim."}

        self.assertEqual(assign_evidence_strength(source), "low")


if __name__ == "__main__":
    unittest.main()
