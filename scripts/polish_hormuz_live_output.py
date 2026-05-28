import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.brief_generator import generate_brief
from agent.source_audit import generate_source_audit
from agent.quantitative_assessment import build_evidence_to_score_bridge, build_quantified_evidence_readout


SHOWCASE = ROOT / "showcase"
OUTPUTS = ROOT / "outputs"
OUTPUT_STEM = "20260528-210200-hormuz-route-decision-engine--sanctions--insurance-and-delay-cost-trade-offs"
CORE_DECISION_QUESTIONS = [
    "Should the operator transit, delay, reroute or place the voyage on legal hold?",
    "Is there a sanctions red flag from tolls, safe-passage demands, offsets, swaps, guarantees, in-kind arrangements or Iranian coordination?",
    "Is war-risk cover available and economically viable?",
    "Do AIS/vessel-flow indicators show route normalisation or continuing operating stress?",
    "How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included?",
    "What evidence would justify relaxing controls?",
]
REFRESH_TRIGGER_BY_REQUIREMENT = {
    "official_maritime_security": "Refresh if official maritime or security guidance changes.",
    "transit_control_or_constabulary_actions": "Refresh if detention reports, coordination demands or transit-control notices change.",
    "sanctions_and_safe_passage_payment_risk": "Refresh immediately if any toll, payment, guarantee, offset, swap or in-kind demand appears.",
    "war_risk_insurance_pricing": "Refresh before voyage approval if war-risk premium, exclusions or cancellation wording changes.",
    "vessel_flow_and_AIS_behaviour": "Refresh if AIS disruption, vessel-flow conditions or recovery signals change.",
    "energy_cargo_and_chokepoint_exposure": "Refresh if cargo exposure or structural chokepoint assumptions change.",
    "route_cost_and_arbitrage_inputs": "Refresh before commercial use if delay, reroute or charter assumptions change.",
    "contrary_or_de_escalation_evidence": "Refresh before relaxing controls if de-escalation claims emerge.",
}
PRIMARY_QUESTION_BY_REQUIREMENT = {
    "official_maritime_security": CORE_DECISION_QUESTIONS[0],
    "transit_control_or_constabulary_actions": CORE_DECISION_QUESTIONS[0],
    "sanctions_and_safe_passage_payment_risk": CORE_DECISION_QUESTIONS[1],
    "war_risk_insurance_pricing": CORE_DECISION_QUESTIONS[2],
    "vessel_flow_and_AIS_behaviour": CORE_DECISION_QUESTIONS[3],
    "energy_cargo_and_chokepoint_exposure": CORE_DECISION_QUESTIONS[4],
    "route_cost_and_arbitrage_inputs": CORE_DECISION_QUESTIONS[4],
    "contrary_or_de_escalation_evidence": CORE_DECISION_QUESTIONS[5],
}


SOURCE_PATCHES = {
    "L1": {
        "title": "Al-Monitor Summary of Reuters Hormuz Transit-Control Report",
        "summary": "Transit-control mechanism: Reuters reported on 5 May 2026 that Iran had set up a new mechanism to manage vessel transit through the Strait of Hormuz.",
        "claim_supported": "Transit-control mechanism: Reuters reported on 5 May 2026 that Iran had set up a new mechanism to manage vessel transit through the Strait of Hormuz.",
        "quantified_facts": [
            "Transit-control mechanism reported: 5 May 2026",
            "Source basis: Reuters-reported via Al-Monitor",
        ],
        "caveat": "Operational reporting should still be checked against current official guidance before transit approval.",
        "source_type": "reputable_news",
        "source_role": "live_event_reporting",
    },
    "L2": {
        "title": "IndexBox / PGSA Hormuz Fees and Sanctions Risk Note",
        "summary": "Safe-passage fee signal: specialist reporting said Iran planned a Strait of Hormuz vessel-traffic system with charges for specialised services, creating sanctions escalation risk if payments, offsets or guarantees are demanded.",
        "claim_supported": "Safe-passage fee signal: specialist reporting said Iran planned a Strait of Hormuz vessel-traffic system with charges for specialised services, creating sanctions escalation risk if payments, offsets or guarantees are demanded.",
        "quantified_facts": [
            "Potential fee system reported: specialised service charges",
            "Legal hold trigger: any toll or equivalent payment demand",
        ],
        "caveat": "Specialist analysis should be validated against current legal guidance before any payment-related decision.",
        "source_type": "specialist_analysis",
        "source_role": "specialist_interpretation",
    },
    "L3": {
        "title": "Howden Re Hormuz War-Risk Pricing Analysis",
        "summary": "War-risk pricing: Howden Re reported marine war-risk pricing up to 12x pre-crisis levels, with tanker premiums around $7.5m at a 3% rate.",
        "claim_supported": "War-risk pricing: Howden Re reported marine war-risk pricing up to 12x pre-crisis levels, with tanker premiums around $7.5m at a 3% rate.",
        "quantified_facts": [
            "War-risk pricing: up to 12x pre-crisis levels",
            "Illustrative tanker premium: about $7.5m at a 3% rate",
        ],
        "caveat": "Market pricing is fast-moving and should be refreshed with broker or underwriter quotes before sailing.",
        "source_type": "insurance_market_evidence",
        "source_role": "market_pricing",
    },
    "L4": {
        "title": "Lloyd's List Hormuz Traffic Stress Monitor",
        "summary": "AIS and vessel-flow stress: Lloyd's List maintained a dedicated Strait of Hormuz crisis tracker, supporting the view that route conditions remained under active disruption review rather than full normalisation.",
        "claim_supported": "AIS and vessel-flow stress: Lloyd's List maintained a dedicated Strait of Hormuz crisis tracker, supporting the view that route conditions remained under active disruption review rather than full normalisation.",
        "quantified_facts": [
            "Traffic status: disruption tracker remained active",
            "Decision use: not sufficient on its own to justify relaxation",
        ],
        "caveat": "Fetched page text was not decision-grade; pair this signal with Reuters, AP or vessel-tracking evidence before relaxing controls.",
        "source_type": "vessel_flow_or_freight_market_evidence",
        "source_role": "data_or_indicator_source",
    },
    "L5": {
        "title": "World Oil Report on EIA Hormuz Chokepoint Dataset Update",
        "summary": "Chokepoint exposure: World Oil reported that the U.S. EIA would publish new strategic petroleum reserve and shipping-flow datasets as Hormuz disruption continued to reshape oil and LNG trade routes.",
        "claim_supported": "Chokepoint exposure: World Oil reported that the U.S. EIA would publish new strategic petroleum reserve and shipping-flow datasets as Hormuz disruption continued to reshape oil and LNG trade routes.",
        "quantified_facts": [
            "Source basis: World Oil citing U.S. EIA dataset launch",
            "Commercial relevance: Hormuz disruption affects oil and LNG routing",
        ],
        "caveat": "Use the underlying EIA chokepoint data for final cargo exposure calculations where available.",
        "source_type": "reputable_news",
        "source_role": "data_or_indicator_source",
    },
    "L6": {
        "title": "Reuters Hormuz Shipping Cost Surge Report",
        "summary": "Freight cost signal: Reuters reported Gulf-linked oil and gas shipping costs surged, with Mideast-China VLCC rates above $400,000 per day.",
        "claim_supported": "Freight cost signal: Reuters reported Gulf-linked oil and gas shipping costs surged, with Mideast-China VLCC rates above $400,000 per day.",
        "quantified_facts": [
            "VLCC rate signal: above $400,000/day",
            "Decision use: direct transit cost should be tested against reroute economics",
        ],
        "caveat": "This source is snippet-based because page fetch failed; refresh with full article access or broker data before using commercially.",
        "fetch_status": "snippet_used",
        "source_type": "insurance_market_evidence",
        "source_role": "market_pricing",
    },
    "L7": {
        "title": "STL.News De-escalation Signal Requiring Stronger Confirmation",
        "summary": "De-escalation signal: reopening claims point to some recovery in commercial passage, but they do not justify relaxing controls without matching insurer, official and vessel-flow confirmation.",
        "claim_supported": "De-escalation signal: reopening claims point to some recovery in commercial passage, but they do not justify relaxing controls without matching insurer, official and vessel-flow confirmation.",
        "quantified_facts": [
            "Recovery signal: reopening claim reported",
            "Relaxation test: insurer, official and vessel-flow confirmation still required",
        ],
        "caveat": "Contrary evidence should be treated as conditional until stronger operational recovery evidence is available.",
        "source_type": "contrary_or_stabilising_evidence",
        "source_role": "contrary_scope_limit",
    },
}


def _apply_source_patches(pack):
    selected_by_id = {item.get("source_id"): item for item in pack.get("selected_sources", [])}
    pack["source_plan"]["decision_questions"] = CORE_DECISION_QUESTIONS
    pack["source_plan"]["expected_evidence_types"] = [
        "official_primary",
        "energy_chokepoint_data",
        "insurance_market_evidence",
        "vessel_flow_or_freight_market_evidence",
        "reputable_news",
        "specialist_analysis",
        "contrary_or_stabilising_evidence",
    ]
    for category in pack.get("source_strategy", {}).get("categories", []):
        category["evidence_question"] = PRIMARY_QUESTION_BY_REQUIREMENT.get(
            category.get("requirement_name", ""),
            CORE_DECISION_QUESTIONS[0],
        )
        category["target_evidence_question"] = category["evidence_question"]
    for requirement in pack.get("source_requirements", []):
        requirement["decision_questions_supported"] = [
            PRIMARY_QUESTION_BY_REQUIREMENT.get(requirement.get("requirement_name", ""), CORE_DECISION_QUESTIONS[0])
        ]
    for item in pack.get("requirement_coverage", []):
        item["decision_questions_supported"] = [
            PRIMARY_QUESTION_BY_REQUIREMENT.get(item.get("requirement_name", ""), CORE_DECISION_QUESTIONS[0])
        ]
    for evidence in pack.get("evidence", []):
        source_id = evidence.get("source_id")
        patch = SOURCE_PATCHES.get(source_id)
        if not patch:
            continue
        evidence["summary"] = patch["summary"]
        evidence["extracted_claim"] = patch["claim_supported"]
        evidence["claim_supported"] = patch["claim_supported"]
        evidence["caveat"] = patch["caveat"]
        evidence["quantified_facts"] = patch["quantified_facts"]
        evidence["source_type"] = patch.get("source_type", evidence.get("source_type"))
        evidence["source_role"] = patch.get("source_role", evidence.get("source_role"))
        evidence["refresh_trigger"] = REFRESH_TRIGGER_BY_REQUIREMENT.get(
            evidence.get("requirement_name", ""),
            "Refresh before operational use.",
        )
        if patch.get("fetch_status"):
            evidence["fetch_status"] = patch["fetch_status"]
        if source_id in selected_by_id:
            selected_by_id[source_id]["title"] = patch["title"]
            selected_by_id[source_id]["publisher"] = evidence.get("publisher", selected_by_id[source_id].get("publisher", ""))
            selected_by_id[source_id]["refresh_trigger"] = evidence["refresh_trigger"]
            selected_by_id[source_id]["source_type"] = patch.get("source_type", selected_by_id[source_id].get("source_type"))
            selected_by_id[source_id]["source_role"] = patch.get("source_role", selected_by_id[source_id].get("source_role"))
            evidence["source_role"] = selected_by_id[source_id].get("source_role", evidence.get("source_type", ""))

    for item in pack.get("selected_sources", []):
        if item.get("source_id") == "L2":
            item["selection_reason"] = "direct topic match, specialist interpretation of sanctions-linked payment risk"
            item["evidence_weight"] = "medium"
        if item.get("source_id") == "L5":
            item["selection_reason"] = "secondary reporting of EIA-linked chokepoint data; useful until direct official refresh"
            item["evidence_weight"] = "medium"
        if item.get("source_id") == "L3":
            item["evidence_weight"] = "high"
        if item.get("source_id") == "L7":
            item["selection_reason"] = "scope-limiting de-escalation signal, but weaker than a direct official or Reuters/AP recovery source"
            item["evidence_weight"] = "medium"
            item["total_score"] = min(item.get("total_score", 0), 20)

    for evidence in pack.get("evidence", []):
        if evidence.get("source_id") == "L3":
            evidence["evidence_weight"] = "high"
        if evidence.get("source_id") == "L7":
            evidence["evidence_weight"] = "medium"

    for item in pack.get("requirement_coverage", []):
        requirement = item.get("requirement_name")
        if requirement == "official_maritime_security":
            item["covered_by"] = []
            item["covered_by_count"] = 0
            item["evidence_weight"] = "low"
            item["coverage_status"] = "partially_covered"
            item["remaining_gap"] = "Requires UKMTO, IMO, ICS, BIMCO, INTERTANKO, OCIMF or government advisory refresh before operational use."
        elif requirement == "contrary_or_de_escalation_evidence":
            item["coverage_status"] = "partially_covered"
            item["remaining_gap"] = "Current contrary signal is weak secondary reporting; refresh with Reuters, AP or official recovery evidence before treating relaxation as credible."
        elif requirement == "energy_cargo_and_chokepoint_exposure":
            item["coverage_status"] = "partially_covered"
            item["remaining_gap"] = "Current evidence is secondary reporting of EIA-linked data; refresh with direct EIA or equivalent official dataset before operational use."
        else:
            item["coverage_status"] = "covered"

    pack["requirements_missing"] = ["REQ-HSO-A"]
    pack["requirements_below_threshold"] = ["REQ-HSO-A"]
    covered = sorted({item.get("source_type", "unknown") for item in pack.get("selected_sources", [])})
    pack["source_categories_covered"] = covered
    source_categories = [item.get("category") for item in pack.get("source_strategy", {}).get("categories", [])]
    pack["source_categories_missing"] = [item for item in source_categories if item and item not in covered]

    pack["refresh_priorities"] = [
        {
            "risk_driver": "sanctions payment trigger",
            "refresh_trigger": "Refresh immediately if any toll, safe-passage fee, guarantee, offset, swap or in-kind demand is reported.",
            "highest_weight_sources": ["L2"],
        },
        {
            "risk_driver": "insurance viability",
            "refresh_trigger": "Refresh before voyage approval if war-risk premium, exclusions, cancellation wording or insurer appetite changes.",
            "highest_weight_sources": ["L3", "L6"],
        },
        {
            "risk_driver": "operational transit stress",
            "refresh_trigger": "Refresh if AIS disruption, detention reports, transit-control notices or official guidance change.",
            "highest_weight_sources": ["L1", "L4"],
        },
        {
            "risk_driver": "route-cost assumptions",
            "refresh_trigger": "Validate vessel value, delay-cost, reroute-cost and charter assumptions before using the optimiser commercially.",
            "highest_weight_sources": ["L3", "L6"],
        },
        {
            "risk_driver": "relaxation threshold",
            "refresh_trigger": "Relax from hold or reroute only after official guidance, insurer appetite and vessel-flow recovery improve together.",
            "highest_weight_sources": ["L1", "L4", "L7"],
        },
    ]
    return pack


def main():
    pack_path = SHOWCASE / "hormuz_evidence_pack.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    pack = _apply_source_patches(pack)
    pack["quantified_evidence_readout"] = build_quantified_evidence_readout(pack)
    pack["evidence_to_score_bridge"] = build_evidence_to_score_bridge(
        pack,
        {
            "likelihood": {"score": 5},
            "impact": {"score": 5},
            "immediacy": {"score": 5},
            "confidence": {"score": 4},
        },
    )
    pack["confidence_cap_reason"] = pack["quantified_evidence_readout"]["confidence_cap"]

    brief = generate_brief(
        topic=pack["topic"],
        business_user=pack["business_user"],
        region=pack["region"],
        time_horizon=pack["time_horizon"],
        concerns=pack["concerns"],
        sources=pack["evidence"],
        evidence_pack=pack,
    )
    audit = generate_source_audit(pack)

    pack_json = json.dumps(pack, indent=2)
    pack_path.write_text(pack_json, encoding="utf-8")
    (SHOWCASE / "hormuz_shipping_operator_brief.md").write_text(brief, encoding="utf-8")
    (SHOWCASE / "hormuz_source_audit.md").write_text(audit, encoding="utf-8")

    (OUTPUTS / f"{OUTPUT_STEM}-evidence-pack.json").write_text(pack_json, encoding="utf-8")
    (OUTPUTS / f"{OUTPUT_STEM}.md").write_text(brief, encoding="utf-8")
    (OUTPUTS / f"{OUTPUT_STEM}-source-audit.md").write_text(audit, encoding="utf-8")

    print("Polished Hormuz live showcase output from saved evidence pack.")


if __name__ == "__main__":
    main()
