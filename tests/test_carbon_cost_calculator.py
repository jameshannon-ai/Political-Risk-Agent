import unittest

from agent.carbon_cost_calculator import calculate_carbon_cost


class CarbonCostCalculatorTests(unittest.TestCase):
    def test_module_returns_expected_costs(self):
        result = calculate_carbon_cost(
            vessel_name="Test ferry",
            gross_tonnage=8500,
            route_name="Liverpool to Belfast",
            route_type="domestic_uk",
            fuel_type="MGO",
            fuel_consumption_tonnes_per_voyage=18,
            voyages_per_week=6,
            uka_price_per_tonne=48,
            coverage_rate=1.0,
            reporting_period_months=6,
        )

        self.assertTrue(result["applies_to_uk_ets"])
        self.assertAlmostEqual(result["estimated_tco2e_per_voyage"], 57.708, places=3)
        self.assertAlmostEqual(result["estimated_carbon_cost_per_voyage"], 2769.98, places=2)
        self.assertAlmostEqual(result["weekly_carbon_cost"], 16619.9, places=1)

    def test_international_route_is_scenario_unless_confirmed(self):
        result = calculate_carbon_cost(
            gross_tonnage=8500,
            route_name="Southampton to Rotterdam",
            route_type="uk_international",
            fuel_type="MGO",
            fuel_consumption_tonnes_per_voyage=18,
            voyages_per_week=2,
            uka_price_per_tonne=48,
            coverage_rate=1.0,
            reporting_period_months=12,
        )

        self.assertEqual(result["applies_to_uk_ets"], "scenario")
        self.assertIn("future/scenario exposure", result["applicability_reason"])


if __name__ == "__main__":
    unittest.main()
