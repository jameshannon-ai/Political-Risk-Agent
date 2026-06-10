import json
import unittest
from pathlib import Path


class CriticalMineralsShowcaseTests(unittest.TestCase):
    def setUp(self):
        self.brief_path = Path("showcase/critical_minerals_advanced_manufacturer_brief.md")
        self.audit_path = Path("showcase/critical_minerals_source_audit.md")
        self.pack_path = Path("showcase/critical_minerals_evidence_pack.json")

    def test_files_exist(self):
        self.assertTrue(self.brief_path.exists())
        self.assertTrue(self.audit_path.exists())
        self.assertTrue(self.pack_path.exists())

    def test_pack_is_live_tavily(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        self.assertEqual(pack["search_provider"], "tavily")
        self.assertEqual(pack["source_provider"], "tavily")
        self.assertFalse(pack["fallback_used"])
        self.assertFalse(pack["fallback_demo_data_used"])
        self.assertEqual(pack["evidence_mode"], "Live source retrieval")

    def test_brief_contains_required_sections_and_controls(self):
        brief = self.brief_path.read_text(encoding="utf-8")
        for phrase in [
            "Critical Minerals Exposure Engine",
            "Decision Recommendation",
            "Dashboard Summary",
            "Exposure Summary",
            "Controlled Input Assessment",
            "Supplier Concentration Assessment",
            "Production Continuity Model",
            "Inventory Runway vs Supplier Qualification Gap",
            "Mitigation Options",
            "Evidence-To-Score Bridge",
            "production continuity gap",
            "Source Quality Notes",
            "The continuity gap is positive where alternative supplier qualification takes longer than available inventory.",
            "snippet/metadata-supported",
            "This is a client-type exposure screen, not a company-specific operational assessment.",
            "bill of materials / input classification",
            "supplier country and ownership data",
            "### Likelihood: 4/5",
            "Evidence used:",
            "Claim:",
            "Commercial relevance:",
            "Confidence effect:",
        ]:
            self.assertIn(phrase, brief)
        for phrase in ["cargo", "collateral", "underwriting", "demurrage", "voyage", "We use some essential"]:
            self.assertNotIn(phrase, brief)

    def test_brief_uses_critical_minerals_specific_bridge_language(self):
        brief = self.brief_path.read_text(encoding="utf-8")
        self.assertIn("licensing friction", brief)
        self.assertIn("supplier concentration", brief)
        self.assertIn("Inventory runway is materially shorter than illustrative supplier qualification time", brief)
        self.assertIn("lacks company-specific BOM, supplier, inventory, contract and qualification data", brief)

    def test_audit_contains_source_quality_notes_and_refresh_controls(self):
        audit = self.audit_path.read_text(encoding="utf-8")
        for phrase in [
            "Source Quality Notes",
            "Refresh if export-control rules or licensing practice changes.",
            "Refresh if China-linked export licences tighten or ease.",
            "Refresh if rare earth magnet shortage or price signals change.",
            "Refresh if alternative supplier qualification assumptions change.",
            "Refresh when company BOM, supplier, inventory or contract data becomes available.",
        ]:
            self.assertIn(phrase, audit)
        for phrase in ["underwriting", "demurrage", "voyage", "carrier/company updates"]:
            self.assertNotIn(phrase, audit)

    def test_pack_claims_and_roles_are_polished(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        claims = {item["source_id"]: item["claim_supported"] for item in pack["evidence"]}
        selected = {item["source_id"]: item for item in pack["selected_sources"]}
        self.assertNotIn("We use some essential", claims["L1"])
        self.assertIn("licensing friction", claims["L2"])
        self.assertIn("weakly supportive", claims["L6"])
        self.assertIn("weak market signal", claims["L7"])
        self.assertEqual(pack["evidence_to_score_bridge"]["confidence"]["score"], 3)
        self.assertEqual(selected["L6"]["evidence_weight"], "low")

    def test_dashboard_supports_offline_critical_minerals_showcase(self):
        dashboard = Path("dashboard_app.py").read_text(encoding="utf-8")
        self.assertIn("Critical Minerals Exposure Engine", dashboard)
        self.assertIn('SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md"', dashboard)
        self.assertIn('SHOWCASE / "critical_minerals_source_audit.md"', dashboard)
        self.assertIn('SHOWCASE / "critical_minerals_evidence_pack.json"', dashboard)
        self.assertIn("Production continuity gap", dashboard)
        self.assertIn("substitution feasibility needs stronger magnet-specific engineering", dashboard)
        self.assertNotIn("TavilyClient", dashboard)
        self.assertNotIn("live_search_mode", dashboard)
        self.assertNotIn(".env", dashboard)

    def test_existing_showcases_remain_present(self):
        self.assertTrue(Path("showcase/uk_ets_shipping_operator_brief.md").exists())
        self.assertTrue(Path("showcase/hormuz_shipping_operator_brief.md").exists())


if __name__ == "__main__":
    unittest.main()
