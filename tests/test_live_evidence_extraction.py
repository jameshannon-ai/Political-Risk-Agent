import unittest

from agent.live_evidence_extraction import extract_live_evidence


class LiveEvidenceExtractionTests(unittest.TestCase):
    def test_captures_numbers_and_insurance_terms(self):
        sources = [
            {
                "title": "War-risk premiums rise 25% near Strait of Hormuz",
                "publisher": "Market Indicator",
                "url": "https://www.howdenre.com/example",
                "publication_date": "2026-05-27",
                "source_type": "insurance_market_evidence",
                "requirement_id": "REQ-D",
                "requirement_name": "insurance_pricing_reinsurance",
                "evidence_weight": "high",
                "reliability_score": 5,
                "relevance_score": 5,
                "recency_score": 5,
                "specificity_score": 5,
                "decision_value_score": 5,
                "snippet": "Marine insurance war-risk premium increased 25% for tanker transit.",
                "content": "Marine insurance war-risk premium increased 25% for tanker transit.",
                "fetch_status": "ok",
            }
        ]

        evidence = extract_live_evidence(sources, business_user="marine_insurer")

        self.assertIn("25%", evidence[0]["key_facts"])
        self.assertIn("25%", evidence[0]["quantified_facts"])
        self.assertIn("insurance", evidence[0]["key_facts"])
        self.assertEqual(evidence[0]["risk_dimension"], "impact")
        self.assertIn("commercial_meaning", evidence[0])
        self.assertIn("business_user_implication", evidence[0])
        self.assertIn("decision_use", evidence[0])
        self.assertIn("refresh_requirement", evidence[0])

    def test_html_script_fragments_are_removed_from_claims(self):
        sources = [
            {
                "title": "UK ETS scope expansion: maritime sector",
                "url": "https://www.gov.uk/example",
                "source_type": "official_primary",
                "requirement_name": "policy_scope",
                "snippet": "Official UK ETS policy confirms domestic maritime expansion from 1 July 2026.",
                "content": "<!DOCTYPE html><html><head><script>var bad = true;</script></head><body><nav>Menu</nav><p>Official UK ETS policy confirms domestic maritime expansion from 1 July 2026 for covered vessels and routes.</p></body></html>",
                "fetch_status": "ok",
            }
        ]

        evidence = extract_live_evidence(sources, business_user="shipping_operator")

        claim = evidence[0]["claim_supported"].lower()
        self.assertNotIn("<script", claim)
        self.assertNotIn("<!doctype", claim)
        self.assertNotIn("<html", claim)
        self.assertFalse(claim.startswith(("data-", "var", "function", "cookie")))
        self.assertIn("official uk ets policy", claim)


if __name__ == "__main__":
    unittest.main()
