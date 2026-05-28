import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.brief_generator import generate_brief
from agent.evidence_pack_builder import build_evidence_pack
from agent.source_audit import generate_source_audit
from agent.source_strategy import create_source_strategy


SHOWCASE = ROOT / "showcase"
ARCHIVE = SHOWCASE / "archive"


def main():
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    _archive_existing_hormuz_brief()
    _generate_hormuz_shipping_operator_showcase()
    _generate_uk_ets_shipping_operator_showcase()


def _archive_existing_hormuz_brief():
    current = SHOWCASE / "hormuz_marine_insurer_brief.md"
    archived = ARCHIVE / "hormuz_marine_insurer_brief.md"
    if current.exists() and not archived.exists():
        archived.write_text(current.read_text(encoding="utf-8"), encoding="utf-8")


def _generate_hormuz_shipping_operator_showcase():
    case_path = ROOT / "examples" / "hormuz_real_evidence_case.json"
    selected_sources = json.loads(case_path.read_text(encoding="utf-8"))["demo_search_results"]
    strategy = create_source_strategy(
        "Strait of Hormuz Transit Controls",
        "Persian Gulf / UK shipping operators",
        "1-3 months",
        business_user="shipping_operator",
        concerns=[
            "transit controls",
            "vessel detention",
            "safe-passage demands",
            "sanctions exposure",
            "war-risk insurance premiums",
            "AIS/transponder disruption",
            "oil and LNG artery disruption",
            "route delay",
            "rerouting cost",
            "charterparty exposure",
            "crew safety",
            "de-escalation uncertainty",
        ],
    )
    search_result = {
        "provider": "fallback_demo_search",
        "fallback_demo_data_used": True,
        "candidate_sources": selected_sources,
        "candidates_by_query": {source["title"]: [source] for source in selected_sources},
        "search_failures": [],
    }
    fetched_result = {
        "fetched_sources": [{**source, "content": source["claim_supported"], "fetch_status": "demo"} for source in selected_sources],
        "fetch_failures": [],
    }
    evidence_pack = build_evidence_pack(
        topic="Strait of Hormuz Transit Controls",
        business_user="shipping_operator",
        region="Persian Gulf / UK shipping operators",
        time_horizon="1-3 months",
        concerns=strategy["source_plan"]["decision_questions"],
        source_strategy=strategy,
        search_result=search_result,
        selected_sources=selected_sources,
        rejected_sources=[
            {
                "title": "Reuters Iran sets up mechanism to manage vessel transit through Hormuz",
                "requirement_name": "transit_control_or_constabulary_actions",
                "query": "Reuters Iran sets up mechanism to manage vessel transit through Hormuz",
                "ranking_score": 0,
                "rejection_reason": "requires review because a directly verified source page was not captured for the curated fallback pack",
            }
        ],
        fetched_result=fetched_result,
    )
    evidence_pack["duplicate_urls_removed"] = 0
    evidence_pack["route_cost_assumptions"] = {
        "illustrative": True,
        "estimated_direct_voyage_days": 14,
        "estimated_reroute_days": 24,
        "daily_vessel_cost": 45000,
        "bunker_cost_per_day": 28000,
        "war_risk_premium_direct": 750000,
        "war_risk_premium_reroute": 150000,
        "demurrage_or_delay_cost_per_day": 35000,
        "compliance_hold_days": 5,
        "caveat": "Illustrative voyage assumptions requiring operator validation.",
    }
    (SHOWCASE / "hormuz_evidence_pack.json").write_text(json.dumps(evidence_pack, indent=2), encoding="utf-8")
    (SHOWCASE / "hormuz_source_audit.md").write_text(generate_source_audit(evidence_pack), encoding="utf-8")
    brief = generate_brief(
        topic="Strait of Hormuz Transit Controls",
        business_user="shipping_operator",
        region="Persian Gulf / UK shipping operators",
        time_horizon="1-3 months",
        concerns=[
            "transit controls",
            "vessel detention",
            "safe-passage demands",
            "sanctions exposure",
            "war-risk insurance premiums",
            "AIS/transponder disruption",
            "oil and LNG artery disruption",
            "route delay",
            "rerouting cost",
            "charterparty exposure",
            "crew safety",
            "de-escalation uncertainty",
        ],
        sources=evidence_pack["evidence"],
        evidence_pack=evidence_pack,
    )
    (SHOWCASE / "hormuz_shipping_operator_brief.md").write_text(brief, encoding="utf-8")


def _generate_uk_ets_shipping_operator_showcase():
    case_path = ROOT / "examples" / "uk_ets_real_evidence_case.json"
    selected_sources = json.loads(case_path.read_text(encoding="utf-8"))["demo_search_results"]
    concerns = [
        "carbon cost exposure",
        "reporting deadline",
        "allowance surrender obligation",
        "UKA price movement",
        "voyage cost pass-through",
        "competitiveness",
        "future international expansion",
        "route applicability",
        "compliance failure",
    ]
    strategy = create_source_strategy(
        "UK ETS Maritime Expansion",
        "UK domestic maritime",
        "1-12 months",
        business_user="shipping_operator",
        concerns=concerns,
        domain="regulatory_carbon_shipping",
    )
    search_result = {
        "provider": "fallback_demo_search",
        "fallback_demo_data_used": True,
        "candidate_sources": selected_sources,
        "candidates_by_query": {source["title"]: [source] for source in selected_sources},
        "search_failures": [],
    }
    fetched_result = {
        "fetched_sources": [{**source, "content": source["claim_supported"], "fetch_status": "demo"} for source in selected_sources],
        "fetch_failures": [],
    }
    evidence_pack = build_evidence_pack(
        topic="UK ETS Maritime Expansion",
        business_user="shipping_operator",
        region="UK domestic maritime",
        time_horizon="1-12 months",
        concerns=concerns,
        source_strategy=strategy,
        search_result=search_result,
        selected_sources=selected_sources,
        rejected_sources=[],
        fetched_result=fetched_result,
    )
    evidence_pack["duplicate_urls_removed"] = 0
    evidence_pack["calculator_assumptions"] = {
        "illustrative": True,
        "vessel_type": "Ro-Ro ferry",
        "gross_tonnage": 8500,
        "route": "Liverpool to Belfast",
        "route_type": "domestic_uk",
        "fuel_type": "MGO",
        "fuel_consumption_tonnes_per_voyage": 18,
        "voyages_per_week": 6,
        "uka_price_per_tonne": 48,
        "coverage_rate": 1.0,
        "reporting_period_months": 6,
        "caveat": "Illustrative voyage assumptions requiring operator validation.",
    }
    (SHOWCASE / "uk_ets_evidence_pack.json").write_text(json.dumps(evidence_pack, indent=2), encoding="utf-8")
    (SHOWCASE / "uk_ets_source_audit.md").write_text(generate_source_audit(evidence_pack), encoding="utf-8")
    brief = generate_brief(
        topic="UK ETS Maritime Expansion",
        business_user="shipping_operator",
        region="UK domestic maritime",
        time_horizon="1-12 months",
        concerns=concerns,
        sources=evidence_pack["evidence"],
        evidence_pack=evidence_pack,
    )
    (SHOWCASE / "uk_ets_shipping_operator_brief.md").write_text(brief, encoding="utf-8")


if __name__ == "__main__":
    main()
