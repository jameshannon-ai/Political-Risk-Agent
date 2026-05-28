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
    topic = "Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs"
    business_user = "shipping_operator"
    region = "Persian Gulf / UK shipping operators"
    time_horizon = "1-3 months"
    concerns = [
        "transit versus delay versus reroute decision",
        "sanctions red flags from tolls or safe-passage demands",
        "war-risk insurance viability",
        "AIS and vessel-flow disruption",
        "detention risk",
        "route cost trade-offs",
        "legal hold threshold",
        "relaxation triggers",
    ]

    strategy = create_source_strategy(
        topic=topic,
        region=region,
        time_horizon=time_horizon,
        business_user=business_user,
        concerns=concerns,
        domain="maritime_trade",
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
    evidence_pack["route_cost_assumptions"] = {
        "illustrative": True,
        "vessel_value": 100000000,
        "war_risk_premium_pct": 0.02,
        "estimated_direct_voyage_days": 14,
        "estimated_reroute_days": 24,
        "daily_vessel_cost": 45000,
        "bunker_cost_per_day": 28000,
        "demurrage_or_delay_cost_per_day": 35000,
        "compliance_hold_days": 5,
        "caveat": "Illustrative voyage assumptions requiring operator validation.",
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

    (SHOWCASE / "hormuz_evidence_pack.json").write_text(json.dumps(evidence_pack, indent=2), encoding="utf-8")
    (SHOWCASE / "hormuz_source_audit.md").write_text(audit, encoding="utf-8")
    (SHOWCASE / "hormuz_shipping_operator_brief.md").write_text(brief, encoding="utf-8")

    print(search_result["provider"], search_result["fallback_demo_data_used"], len(search_result["candidate_sources"]), len(ranking["selected_sources"]))
    print(evidence_path)
    print(audit_path)
    print(brief_path)


if __name__ == "__main__":
    main()
