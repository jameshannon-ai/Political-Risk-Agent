import tempfile
import unittest
from pathlib import Path

from dashboard_helpers import (
    extract_markdown_section,
    extract_markdown_table,
    get_nested_value,
    load_json,
    load_markdown,
)


class DashboardHelperTests(unittest.TestCase):
    def setUp(self):
        self.uk_ets_brief = Path("showcase/uk_ets_shipping_operator_brief.md")
        self.hormuz_brief = Path("showcase/hormuz_shipping_operator_brief.md")
        self.uk_ets_pack = Path("showcase/uk_ets_evidence_pack.json")
        self.hormuz_pack = Path("showcase/hormuz_evidence_pack.json")

    def test_loaders_read_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            json_path = root / "sample.json"
            md_path = root / "sample.md"
            json_path.write_text('{"a": 1}', encoding="utf-8")
            md_path.write_text("# Title\n\nBody", encoding="utf-8")

            self.assertEqual(load_json(json_path), {"a": 1})
            self.assertIn("Body", load_markdown(md_path))

    def test_extract_markdown_section(self):
        markdown = "## One\nalpha\n\n## Two\nbeta\n"
        self.assertEqual(extract_markdown_section(markdown, "Two"), "beta")

    def test_extract_markdown_table(self):
        section = """
| A | B |
| --- | --- |
| 1 | 2 |
| 3 | 4 |
"""
        tables = extract_markdown_table(section)
        self.assertEqual(tables[0][0]["A"], "1")
        self.assertEqual(tables[0][1]["B"], "4")

    def test_get_nested_value(self):
        data = {"a": {"b": 7}}
        self.assertEqual(get_nested_value(data, [["a", "b"], ["x"]], 0), 7)
        self.assertEqual(get_nested_value(data, [["x", "y"]], 5), 5)

    def test_saved_showcase_files_exist_for_both_cases(self):
        for path in [self.uk_ets_brief, self.hormuz_brief, self.uk_ets_pack, self.hormuz_pack]:
            self.assertTrue(path.exists(), f"Missing saved showcase file: {path}")

    def test_hormuz_sections_can_be_extracted(self):
        brief = load_markdown(self.hormuz_brief)
        for heading in [
            "Dashboard Summary",
            "1. Decision Recommendation",
            "4. Route Decision Optimiser",
            "5. Illustrative Route-Cost Scenario",
            "6. Sanctions Red-Flag Assessment",
            "7. Insurance Break-Even Analysis",
            "8. AIS and Vessel-Flow Signals",
            "11. Source Requirement Coverage",
        ]:
            section = extract_markdown_section(brief, heading)
            self.assertTrue(section, f"Expected section to be extractable: {heading}")
            self.assertTrue(extract_markdown_table(section), f"Expected table in section: {heading}")

    def test_helpers_work_for_both_case_briefs(self):
        uk_ets = load_markdown(self.uk_ets_brief)
        hormuz = load_markdown(self.hormuz_brief)

        uk_section = extract_markdown_section(uk_ets, "1. Operator Stance")
        hormuz_section = extract_markdown_section(hormuz, "1. Decision Recommendation")

        self.assertTrue(extract_markdown_table(uk_section))
        self.assertTrue(extract_markdown_table(hormuz_section))
        self.assertIn("Current stance", str(extract_markdown_table(uk_section)[0][0]))
        self.assertIn("Preferred option", str(extract_markdown_table(hormuz_section)[0][0]))


if __name__ == "__main__":
    unittest.main()
