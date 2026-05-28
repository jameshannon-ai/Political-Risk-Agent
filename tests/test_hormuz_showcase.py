import json
import unittest
from pathlib import Path

from agent.hormuz_decision_engine import evaluate_hormuz_route_decision


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
            "Hormuz Route Decision Engine",
            "Decision Recommendation",
            "Dashboard Summary",
            "Illustrative Route-Cost Scenario",
            "not company-specific figures",
            "Replace with",
            "Assumption Confidence",
            "Route Decision Optimiser",
            "Sanctions Red-Flag Assessment",
            "Insurance Break-Even Analysis",
            "AIS and Vessel-Flow Signals",
            "Legal hold trigger",
        ]:
            self.assertIn(phrase, brief)
        for phrase in ["Marine Insurer Exposure Assessment", "Exposure Pressure Map"]:
            self.assertNotIn(phrase, brief)
        for phrase in ["Search IndexBox", "Hot Topics Strait of Hormuz crisis", "Skip to main content Iran sets up new mechanism"]:
            self.assertNotIn(phrase, brief)

    def test_pack_uses_shipping_operator(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        self.assertEqual(pack["business_user"], "shipping_operator")
        self.assertIn("source_requirements", pack)
        self.assertIn("source_plan", pack)
        self.assertEqual(pack["search_provider"], "tavily")
        self.assertEqual(pack["source_provider"], "tavily")
        self.assertFalse(pack["fallback_used"])
        self.assertFalse(pack["fallback_demo_data_used"])
        self.assertEqual(pack["evidence_mode"], "Live source retrieval")

    def test_polished_claims_are_readable(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        claims = {item["source_id"]: item.get("claim_supported", "") for item in pack["evidence"]}
        self.assertIn("Transit-control mechanism:", claims["L1"])
        self.assertIn("Safe-passage fee signal:", claims["L2"])
        self.assertIn("Freight cost signal:", claims["L6"])
        self.assertNotIn("Hot Topics Strait of Hormuz crisis", claims["L4"])
        self.assertNotIn("Search IndexBox", claims["L2"])
        self.assertEqual(len(pack["source_plan"]["decision_questions"]), 6)

    def test_brief_uses_specific_decision_language(self):
        brief = self.brief_path.read_text(encoding="utf-8")
        self.assertIn("Conditional transit trigger", brief)
        self.assertIn("legal hold / compliance escalation", brief)
        self.assertIn("Refresh before relaxing controls.", brief)
        self.assertNotIn("Supports operator review and control decisions.", brief)
        self.assertIn(
            "Preferred option | Legal hold if any sanctions/payment trigger is present; otherwise delay or reroute until insurance, AIS/vessel-flow and official guidance conditions support conditional transit.",
            brief,
        )

    def test_source_classification_and_official_gap_are_honest(self):
        pack = json.loads(self.pack_path.read_text(encoding="utf-8"))
        selected = {item["source_id"]: item for item in pack["selected_sources"]}
        self.assertEqual(selected["L2"]["source_type"], "specialist_analysis")
        self.assertNotEqual(selected["L5"]["source_type"], "energy_chokepoint_data")
        official_cov = next(item for item in pack["requirement_coverage"] if item["requirement_name"] == "official_maritime_security")
        self.assertEqual(official_cov["coverage_status"], "partially_covered")
        self.assertEqual(official_cov["covered_by_count"], 0)
        self.assertIn("Requires UKMTO, IMO, ICS, BIMCO, INTERTANKO, OCIMF or government advisory refresh", official_cov["remaining_gap"])

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

    def test_dashboard_supports_both_offline_showcases(self):
        dashboard = Path("dashboard_app.py").read_text(encoding="utf-8")
        self.assertIn("UK ETS Maritime Expansion: Carbon Cost Exposure", dashboard)
        self.assertIn("Hormuz Route Decision Engine", dashboard)
        self.assertIn("saved showcase artefacts only", dashboard)
        self.assertIn('SHOWCASE / "hormuz_evidence_pack.json"', dashboard)
        self.assertNotIn("TavilyClient", dashboard)
        self.assertNotIn("live_search_mode", dashboard)
        self.assertNotIn(".env", dashboard)

    def test_sanctions_showcase_remains_intact(self):
        sanctions = Path("showcase/sanctions_trade_finance_sample.md").read_text(encoding="utf-8")
        self.assertIn("Transaction Stance", sanctions)
        self.assertIn("Payment and Documentation Risk", sanctions)

    def test_sanctions_red_flag_forces_legal_hold(self):
        result = evaluate_hormuz_route_decision(
            sanctions_red_flag=True,
            war_risk_premium_pct=0.01,
            vessel_value=100000000,
            direct_voyage_cost=1000000,
            delay_days=2,
            delay_cost_per_day=50000,
            reroute_extra_days=5,
            reroute_cost_per_day=70000,
            ais_disruption_level="medium",
            vessel_flow_status="disrupted",
            detention_risk="medium",
            insurance_cover_status="confirmed",
            official_guidance_status="enhanced_warning",
        )

        self.assertTrue(result["legal_hold_required"])
        self.assertEqual(result["preferred_option"], "Legal hold")

    def test_excluded_cover_prevents_transit_being_preferred(self):
        result = evaluate_hormuz_route_decision(
            sanctions_red_flag=False,
            war_risk_premium_pct=0.005,
            vessel_value=100000000,
            direct_voyage_cost=1000000,
            delay_days=2,
            delay_cost_per_day=50000,
            reroute_extra_days=5,
            reroute_cost_per_day=70000,
            ais_disruption_level="low",
            vessel_flow_status="normalising",
            detention_risk="low",
            insurance_cover_status="excluded",
            official_guidance_status="normal",
        )

        self.assertNotIn(result["preferred_option"], {"Conditional transit", "Direct transit"})

    def test_high_detention_and_severe_flow_prevent_transit(self):
        result = evaluate_hormuz_route_decision(
            sanctions_red_flag=False,
            war_risk_premium_pct=0.005,
            vessel_value=100000000,
            direct_voyage_cost=1000000,
            delay_days=2,
            delay_cost_per_day=50000,
            reroute_extra_days=5,
            reroute_cost_per_day=70000,
            ais_disruption_level="medium",
            vessel_flow_status="severely_disrupted",
            detention_risk="high",
            insurance_cover_status="confirmed",
            official_guidance_status="enhanced_warning",
        )

        self.assertNotIn(result["preferred_option"], {"Conditional transit", "Direct transit"})

    def test_insurance_break_even_is_calculated(self):
        result = evaluate_hormuz_route_decision(
            sanctions_red_flag=False,
            war_risk_premium_pct=0.02,
            vessel_value=100000000,
            direct_voyage_cost=1022000,
            delay_days=5,
            delay_cost_per_day=108000,
            reroute_extra_days=10,
            reroute_cost_per_day=73000,
            ais_disruption_level="high",
            vessel_flow_status="severely_disrupted",
            detention_risk="high",
            insurance_cover_status="unclear",
            official_guidance_status="restrictive",
        )

        self.assertGreater(result["insurance_break_even"]["premium_pct_break_even_vs_reroute"], 0)


if __name__ == "__main__":
    unittest.main()
