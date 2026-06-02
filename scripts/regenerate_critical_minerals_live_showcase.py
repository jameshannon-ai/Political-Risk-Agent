import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from agent.brief_generator import generate_brief
from agent.evidence_pack_builder import build_evidence_pack, save_evidence_pack
from agent.source_audit import generate_source_audit, save_source_audit
from agent.source_fetcher import fetch_selected_sources
from agent.source_ranker import rank_candidate_sources
from agent.source_strategy import SOURCE_CATEGORIES, create_source_strategy
from agent.live_search import run_live_searches


SHOWCASE = ROOT / "showcase"
OUTPUTS = ROOT / "outputs"


def main():
    load_dotenv()
    topic = "Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers"
    business_user = "advanced_manufacturer"
    region = "UK advanced manufacturer exposed to global rare earth magnet supply chains"
    time_horizon = "1-6 months"
    concerns = [
        "production continuity under export-control disruption",
        "rare earth magnet input dependency",
        "supplier concentration",
        "inventory runway versus qualification lag",
        "stockpile versus alternative supplier qualification",
        "technical substitution feasibility",
        "allocation of scarce inventory",
        "production hold threshold",
    ]

    strategy = create_source_strategy(
        topic=topic,
        region=region,
        time_horizon=time_horizon,
        business_user=business_user,
        concerns=concerns,
        domain="critical_minerals_supply_chain",
    )
    search_result = run_live_searches(strategy)
    ranking = rank_candidate_sources(
        search_result["candidate_sources"],
        topic=topic,
        categories=SOURCE_CATEGORIES,
        per_category=1,
    )
    fetched_result = fetch_selected_sources(
        ranking["selected_sources"],
        fallback_demo_data_used=search_result["fallback_demo_data_used"],
    )
    evidence_pack = build_evidence_pack(
        topic=topic,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        source_strategy=strategy,
        search_result=search_result,
        selected_sources=ranking["selected_sources"],
        rejected_sources=ranking["rejected_sources"],
        fetched_result=fetched_result,
    )
    evidence_pack["duplicate_urls_removed"] = ranking["duplicate_urls_removed"]
    evidence_pack["scenario_inputs"] = {
        "inventory_runway_days": {"value": 45, "label": "illustrative"},
        "alternative_supplier_qualification_days": {"value": 180, "label": "illustrative"},
        "china_linked_supply_share_pct": {"value": 70, "label": "illustrative"},
        "exposed_product_line_revenue_gbp": {"value": 50000000, "label": "illustrative"},
        "substitution_difficulty": {"value": "high", "label": "illustrative"},
        "customer_delivery_criticality": {"value": "high", "label": "illustrative"},
        "production_continuity_gap_days": {"value": 135, "label": "derived"},
    }

    evidence_path = save_evidence_pack(evidence_pack, OUTPUTS)
    audit = generate_source_audit(evidence_pack)
    audit_path = save_source_audit(audit, OUTPUTS, topic)
    brief = generate_brief(
        topic=topic,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        sources=evidence_pack["evidence"],
        evidence_pack=evidence_pack,
    )
    brief_path = OUTPUTS / f"{evidence_path.stem.replace('-evidence-pack', '')}.md"
    brief_path.write_text(brief, encoding="utf-8")

    (SHOWCASE / "critical_minerals_evidence_pack.json").write_text(json.dumps(evidence_pack, indent=2), encoding="utf-8")
    (SHOWCASE / "critical_minerals_source_audit.md").write_text(audit, encoding="utf-8")
    (SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md").write_text(brief, encoding="utf-8")

    print(search_result["provider"], search_result["fallback_demo_data_used"], search_result.get("total_queries_run", 0), len(ranking["selected_sources"]))
    print(evidence_path)
    print(audit_path)
    print(brief_path)


if __name__ == "__main__":
    main()
