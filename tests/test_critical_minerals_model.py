import unittest

from agent.brief_generator import generate_brief, select_report_template
from agent.critical_minerals_decision_engine import build_critical_minerals_model


class CriticalMineralsModelTests(unittest.TestCase):
    def test_production_continuity_gap_calculates_qualification_minus_runway(self):
        model = build_critical_minerals_model(
            inventory_runway_days=45,
            alternative_supplier_qualification_days=180,
        )

        self.assertEqual(model["production_continuity_gap_days"], 135)

    def test_template_selection_uses_critical_minerals_showcase(self):
        self.assertEqual(
            select_report_template(
                "Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers",
                "advanced_manufacturer",
                "critical_minerals_supply_chain",
            ),
            "critical_minerals_advanced_manufacturer_showcase",
        )

    def test_generated_brief_uses_case_specific_sections(self):
        brief = generate_brief(
            topic="Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers",
            business_user="advanced_manufacturer",
            region="UK advanced manufacturer exposed to global rare earth magnet supply chains",
            time_horizon="1-6 months",
            concerns=["production continuity", "rare earth magnet dependency"],
            sources=[],
        )

        for phrase in [
            "Production Continuity Model",
            "Inventory Runway vs Supplier Qualification Gap",
            "This is a client-type exposure screen, not a company-specific operational assessment.",
            "bill of materials / input classification",
        ]:
            self.assertIn(phrase, brief)
        self.assertIn("Evidence-To-Score Bridge", brief)


if __name__ == "__main__":
    unittest.main()
