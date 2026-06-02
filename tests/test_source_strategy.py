import unittest

from agent.source_strategy import SOURCE_CATEGORIES, create_source_strategy


class SourceStrategyTests(unittest.TestCase):
    def test_strategy_includes_all_required_categories(self):
        strategy = create_source_strategy(
            topic="Strait of Hormuz disruption",
            region="Persian Gulf",
            time_horizon="1-3 months",
            business_user="marine_insurer",
        )
        categories = [item["category"] for item in strategy["categories"]]

        self.assertIn("source_requirements", strategy)
        self.assertIn("source_plan", strategy)
        self.assertGreaterEqual(len(strategy["source_requirements"]), 7)
        self.assertTrue(set(categories).issubset(set(SOURCE_CATEGORIES)))
        self.assertTrue(all(item["queries"] for item in strategy["categories"]))
        self.assertTrue(all("target_evidence_question" in item for item in strategy["categories"]))
        self.assertTrue(all("source_requirement" in item for item in strategy["categories"]))

    def test_uk_ets_strategy_uses_regulatory_carbon_shipping_domain(self):
        strategy = create_source_strategy(
            topic="UK ETS Maritime Expansion",
            region="UK domestic maritime",
            time_horizon="1-12 months",
            business_user="shipping_operator",
            domain="regulatory_carbon_shipping",
        )

        self.assertEqual(strategy["domain"], "regulatory_carbon_shipping")
        self.assertGreaterEqual(len(strategy["source_requirements"]), 8)
        queries = " ".join(query for item in strategy["categories"] for query in item["queries"])
        self.assertIn("GOV.UK UK ETS domestic maritime", queries)
        self.assertIn("IMO marine gas oil emission factor", queries)

    def test_critical_minerals_strategy_uses_advanced_manufacturer_domain(self):
        strategy = create_source_strategy(
            topic="Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers",
            region="UK advanced manufacturer exposed to global rare earth magnet supply chains",
            time_horizon="1-6 months",
            business_user="advanced_manufacturer",
            domain="critical_minerals_supply_chain",
        )

        self.assertEqual(strategy["domain"], "critical_minerals_supply_chain")
        self.assertGreaterEqual(len(strategy["source_requirements"]), 9)
        queries = " ".join(query for item in strategy["categories"] for query in item["queries"])
        self.assertIn("site:gov.uk UK critical minerals strategy", queries)
        self.assertIn("site:reuters.com China rare earth magnet export controls", queries)


if __name__ == "__main__":
    unittest.main()
