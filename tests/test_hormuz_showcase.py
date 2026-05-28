import json
import unittest
from pathlib import Path


class HormuzShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.brief_path = Path("showcase/hormuz_shipping_operator_brief.md")
        self.audit_path = Path("showcase/hormuz_source_audit.md")
        self.pack_path = Path("showcase/hormuz_evidence_pack.json")
        self.archive_path = Path("showcase/archive/hormuz_marine_insurer_brief.md")

    def test_files_exist(self):
        self.assertTrue(self.brief_path.exists())
        self.assertTrue(self.audit_path.exists())
        self.assertTrue(self.pack_path.exists())
        self.assertTrue(self.archive_path.exists())

    def test_brief_contains_required_sections(self):
        brief = self.brief_path.read_text(encoding="utf-8")
        for phrase in [
            "Operator Decision Stance",
            "Voyage Decision Matrix",
            "Sanctions and Safe-Passage Risk",
            "Dynamic Route-Cost Assessment",
        ]:
            self.assertIn(phrase, brief)
        for phrase in ["Marine Insurer Exposure Assessment", "Exposure Pressure Map"]:
            self.assertNotIn(phrase, brief)

    def test_pack_uses_shipping_operator(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        self.assertEqual(pack["business_user"], "shipping_operator")
        self.assertIn("source_requirements", pack)
        self.assertIn("source_plan", pack)

    def test_no_env_content_is_exposed(self):
        for path in [
            Path("README.md"),
            Path("showcase/README.md"),
            self.brief_path,
            self.audit_path,
            self.pack_path,
        ]:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("TAVILY_API_KEY=sk", text)


if __name__ == "__main__":
    unittest.main()
