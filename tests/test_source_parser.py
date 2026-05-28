import unittest

from agent.source_parser import infer_source_type, parse_source_notes


class SourceParserTests(unittest.TestCase):
    def test_classifies_source_types(self):
        self.assertEqual(
            infer_source_type("UKMTO", "official maritime advisory", "Vessel incident reported"),
            "official_primary",
        )
        self.assertEqual(
            infer_source_type("Maersk", "carrier update", "Service rerouted"),
            "company_update",
        )
        self.assertEqual(
            infer_source_type("Reuters", "news", "Shipping disruption reported"),
            "reputable_news",
        )

    def test_parses_multisource_notes(self):
        notes = """Source 1:
Publisher: UKMTO
Date: 2026-05-20
Type: official maritime advisory
Summary: Reports vessel security incidents.

Source 2:
Publisher: Maersk
Date: 2026-05-18
Type: carrier update
Summary: Services avoid the route.
"""
        sources = parse_source_notes(notes)

        self.assertEqual(len(sources), 2)
        self.assertEqual(sources[0]["source_id"], "S1")
        self.assertEqual(sources[1]["inferred_source_type"], "company_update")


if __name__ == "__main__":
    unittest.main()
