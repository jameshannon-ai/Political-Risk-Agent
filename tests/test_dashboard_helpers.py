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


if __name__ == "__main__":
    unittest.main()
