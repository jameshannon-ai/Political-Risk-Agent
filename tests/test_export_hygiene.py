import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExportHygieneTests(unittest.TestCase):
    def test_gitignore_covers_sensitive_and_generated_files(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for phrase in [
            ".env",
            ".venv/",
            "venv/",
            "env/",
            "__pycache__/",
            "*.pyc",
            ".DS_Store",
            "*.zip",
            "outputs/*.md",
            "outputs/*.json",
            "!outputs/.gitkeep",
        ]:
            self.assertIn(phrase, gitignore)

    def test_clean_export_script_excludes_sensitive_paths(self):
        script = (ROOT / "scripts" / "create_clean_project_zip.py").read_text(encoding="utf-8")
        for phrase in [
            ".env",
            ".venv",
            ".git",
            "__pycache__",
            ".DS_Store",
            "*.zip",
            "outputs",
            "political-risk-agent-clean.zip",
        ]:
            self.assertIn(phrase, script)

    def test_framework_guidance_files_exist(self):
        for relative in [
            "AGENTS.md",
            "docs/FRAMEWORK_PRINCIPLES.md",
            "docs/TASK_BRIEF_TEMPLATE.md",
        ]:
            self.assertTrue((ROOT / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
