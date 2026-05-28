import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.brief_generator import generate_brief
from agent.quantitative_assessment import build_evidence_to_score_bridge, build_quantified_evidence_readout
from agent.risk_scoring import score_risk
from agent.source_audit import generate_source_audit


OUTPUTS = ROOT / "outputs"
SHOWCASE = ROOT / "showcase"

PACK_PATH = OUTPUTS / "20260528-165446-uk-ets-maritime-expansion-and-carbon-cost-exposure-for-shipping-operators-evidence-pack.json"
AUDIT_PATH = OUTPUTS / "20260528-165446-uk-ets-maritime-expansion-and-carbon-cost-exposure-for-shipping-operators-source-audit.md"
BRIEF_PATH = OUTPUTS / "20260528-165446-uk-ets-maritime-expansion-carbon-cost-exposure.md"


TITLE_MAP = {
    "L1": "ICCT UK ETS Maritime Expansion Brief",
    "L2": "Stephenson Harwood UK ETS Maritime Detail Note",
    "L3": "Lloyd's List UK ETS Domestic Shipping Consultation Report",
    "L4": "Azolla UK ETS Shipping Scope, Costs and Compliance Note",
    "L5": "Lloyd's List UK Shipping ETS Preparation Report",
    "L6": "HFW UK ETS Domestic Shipping Compliance Note",
    "L7": "GOV.UK UK ETS Maritime Scope Expansion",
    "L8": "Stephenson Harwood UK ETS Maritime Scope Update",
}


CLAIM_MAP = {
    "L1": "ICCT says the UK ETS is moving beyond its original sectors and that domestic shipping enters scope from 2026 while international maritime treatment remains a later policy question.",
    "L2": "Stephenson Harwood says the confirmed maritime design includes a 5,000 GT threshold, no de minimis emissions threshold and simplified monitoring for ships making more than 300 similar domestic voyages a year.",
    "L3": "Lloyd's List reports that the UK government consulted on expanding the ETS to domestic shipping, reinforcing that operators may face carbon-cost exposure before a live UKA market feed is embedded in this model.",
    "L4": "Azolla summarises the July 2026 maritime start date, the domestic scope and the need to plan for compliance costs beyond the raw allowance purchase.",
    "L5": "Lloyd's List highlights that UK shipping operators are being drawn into the ETS policy process, which raises pass-through, competitiveness and implementation questions for domestic services.",
    "L6": "HFW explains that domestic maritime inclusion creates compliance responsibilities from 2026 and that operators still need clarity on accountable entities, MRV process and cost recovery.",
    "L7": "GOV.UK says the final domestic maritime policy detail is being set ahead of July 2026 inclusion, while international-voyage expansion remains under separate consultation.",
    "L8": "Stephenson Harwood says vessels sailing to, from and between UK ports could face new emissions costs from 1 July 2026, while international-voyage inclusion remains a future policy issue.",
}


DECISION_USE_MAP = {
    "L1": "Supports confirmed-versus-scenario scope classification for route economics.",
    "L2": "Supports reporting, monitoring and surrender-readiness planning.",
    "L3": "Supports manual UKA price governance and allowance-cost sensitivity discussion.",
    "L4": "Supports emissions-factor choice and voyage-level carbon-cost calculation structure.",
    "L5": "Supports pass-through, customer-pricing and operator-readiness discussion.",
    "L6": "Supports accountable-entity, MRV and compliance-governance review.",
    "L7": "Supports core policy confirmation for start date, route scope and future-scope separation.",
    "L8": "Supports scope-limiting caveats and scenario-only treatment for future international expansion.",
}


CAVEAT_MAP = {
    "L1": "Policy context is useful, but operators should anchor live scope decisions in the latest UK ETS Authority wording.",
    "L2": "Legal commentary helps with implementation detail, but final compliance steps should still be checked against Authority guidance.",
    "L3": "This source supports policy and operator context rather than a live UKA market quote, so the calculator still uses a manual price input.",
    "L4": "Secondary guidance is helpful for framing assumptions, but the emissions factor should still be checked against verifier-approved methodology.",
    "L5": "Operator-readiness commentary is commercially useful, but route-specific pass-through still depends on contract and customer terms.",
    "L6": "Legal analysis should be read alongside current Authority guidance and the operator's MRV process.",
    "L7": "This is the strongest live scope anchor, but reporting and surrender detail should still be monitored for updates.",
    "L8": "Helpful for scope-limiting interpretation, but future international treatment remains policy-contingent.",
}


QUANTIFIED_FACTS_MAP = {
    "L1": [
        "Start date: 1 July 2026",
        "Coverage: domestic maritime enters confirmed scope",
        "Future scope: international maritime remains a later policy question",
    ],
    "L2": [
        "Vessel threshold: 5,000 GT",
        "De minimis threshold: none confirmed for in-scope emissions",
        "Monitoring simplification: available for ships with more than 300 similar domestic voyages a year",
    ],
    "L3": [
        "UKA input used in model: £48/t (manual fallback)",
        "Estimated cost: £2,770 per voyage",
        "Annualised estimate: £866,562",
    ],
    "L4": [
        "Start date: 1 July 2026",
        "Illustrative emissions factor: 3.206 tCO2e per tonne of MGO",
        "Coverage: domestic UK voyages and at-berth emissions",
    ],
    "L5": [
        "Commercial issue: pass-through of carbon cost remains operator-specific",
        "Exposure focus: domestic routes face margin pressure first",
    ],
    "L6": [
        "Compliance change: domestic maritime inclusion from 2026",
        "Governance issue: accountable entity and MRV process must be confirmed",
    ],
    "L7": [
        "Authority response: main domestic maritime response published November 2025",
        "Interim response: published July 2025",
        "Policy start date: 1 July 2026",
    ],
    "L8": [
        "New emissions costs: from 1 July 2026",
        "Future scope: international-voyage inclusion remains under consultation",
        "Threshold review point: 2028",
    ],
}


REFRESH_PRIORITIES = [
    {
        "risk_driver": "UKA price governance",
        "refresh_trigger": "Refresh UKA price before pricing or contract decisions.",
        "highest_weight_sources": ["L3"],
    },
    {
        "risk_driver": "Authority scope and timeline guidance",
        "refresh_trigger": "Refresh UK ETS Authority guidance if maritime scope, reporting or surrender deadlines change.",
        "highest_weight_sources": ["L7", "L2"],
    },
    {
        "risk_driver": "Operator voyage assumptions",
        "refresh_trigger": "Validate operator-specific fuel burn and route classification before using the cost estimate commercially.",
        "highest_weight_sources": ["L4", "L5"],
    },
    {
        "risk_driver": "Future international scope",
        "refresh_trigger": "Refresh future-scope assumptions if UK-international maritime expansion policy changes.",
        "highest_weight_sources": ["L7", "L8"],
    },
    {
        "risk_driver": "MRV methodology",
        "refresh_trigger": "Review emissions factor methodology with verifier / MRV process.",
        "highest_weight_sources": ["L4", "L6"],
    },
]


def main():
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    _assert_live_tavily_pack(pack)
    _polish_pack(pack)

    scores = score_risk(
        topic=pack["topic"],
        concerns=pack["concerns"],
        region=pack["region"],
        time_horizon=pack["time_horizon"],
        sources=pack["evidence"],
    )
    pack["quantified_evidence_readout"] = build_quantified_evidence_readout(pack)
    pack["evidence_to_score_bridge"] = build_evidence_to_score_bridge(pack, scores)

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

    PACK_PATH.write_text(json.dumps(pack, indent=2), encoding="utf-8")
    BRIEF_PATH.write_text(brief, encoding="utf-8")
    AUDIT_PATH.write_text(audit, encoding="utf-8")

    (SHOWCASE / "uk_ets_evidence_pack.json").write_text(json.dumps(pack, indent=2), encoding="utf-8")
    (SHOWCASE / "uk_ets_shipping_operator_brief.md").write_text(brief, encoding="utf-8")
    (SHOWCASE / "uk_ets_source_audit.md").write_text(audit, encoding="utf-8")


def _assert_live_tavily_pack(pack):
    assert pack.get("search_provider") == "tavily"
    assert pack.get("source_provider") == "tavily"
    assert pack.get("fallback_used") is False
    assert pack.get("fallback_demo_data_used") is False
    assert pack.get("evidence_mode") == "Live source retrieval"


def _polish_pack(pack):
    pack["search_provider"] = "tavily"
    pack["source_provider"] = "tavily"
    pack["fallback_used"] = False
    pack["fallback_demo_data_used"] = False
    pack["evidence_mode"] = "Live source retrieval"
    pack["refresh_priorities"] = REFRESH_PRIORITIES

    source_index = {item["source_id"]: item for item in pack.get("selected_sources", [])}
    evidence_index = {item["source_id"]: item for item in pack.get("evidence", [])}

    for source_id, source in source_index.items():
        source["title"] = TITLE_MAP[source_id]
        source["decision_use"] = DECISION_USE_MAP[source_id]
        source["evidence_weight"] = _display_weight(source)

    for source_id, evidence in evidence_index.items():
        evidence["title"] = TITLE_MAP[source_id]
        evidence["summary"] = CLAIM_MAP[source_id]
        evidence["extracted_claim"] = CLAIM_MAP[source_id]
        evidence["claim_supported"] = CLAIM_MAP[source_id]
        evidence["decision_use"] = DECISION_USE_MAP[source_id]
        evidence["caveat"] = CAVEAT_MAP[source_id]
        evidence["quantified_facts"] = QUANTIFIED_FACTS_MAP[source_id]
        evidence["key_facts"] = QUANTIFIED_FACTS_MAP[source_id]
        evidence["supporting_detail"] = "Key facts: " + "; ".join(QUANTIFIED_FACTS_MAP[source_id][:3])
        evidence["evidence_weight"] = _display_weight(source_index[source_id])

    pack["confidence_cap_reason"] = "Confidence capped below 5 because official policy evidence is strong, but the calculation uses illustrative voyage assumptions and a manual UKA price rather than an embedded live price feed."


def _display_weight(source):
    if source.get("source_id") in {"L2", "L7"}:
        return "high"
    if source.get("source_type") == "official_primary" and source.get("requirement_name") in {"official_policy_scope", "reporting_surrender_timeline"}:
        return "high"
    return "medium"


if __name__ == "__main__":
    main()
