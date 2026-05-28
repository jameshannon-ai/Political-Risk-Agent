from datetime import datetime
from pathlib import Path
import re

from agent.confidence_model import calculate_confidence
from agent.carbon_cost_calculator import calculate_carbon_cost
from agent.exposure_mapping import get_exposure_map
from agent.hormuz_decision_engine import evaluate_hormuz_route_decision
from agent.route_cost_assessment import assess_route_cost
from agent.review_flags import generate_review_flags
from agent.risk_scoring import score_risk
from agent.risk_driver_synthesis import synthesize_risk_drivers
from agent.quantitative_assessment import build_evidence_to_score_bridge, build_quantified_evidence_readout

# Template selection keeps the reusable political risk engine separate from
# showcase-specific briefing templates.


def _slugify(value):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "risk-brief"


def _escape_table_cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def _format_bullets(items):
    if not items:
        return "- No items supplied."
    return "\n".join(f"- {item}" for item in items)


def _is_hormuz_marine_insurer(topic, business_user):
    return "hormuz" in topic.lower() and business_user == "marine_insurer"


def _is_hormuz_shipping_operator(topic, business_user):
    return "hormuz" in topic.lower() and business_user == "shipping_operator"


def _is_uk_ets_shipping_operator(topic, business_user):
    lowered = topic.lower()
    return business_user == "shipping_operator" and ("uk ets" in lowered or "maritime expansion" in lowered)


def select_report_template(topic, business_user, domain=None):
    if _is_uk_ets_shipping_operator(topic, business_user):
        return "uk_ets_shipping_operator_showcase"
    if _is_hormuz_shipping_operator(topic, business_user):
        return "hormuz_shipping_operator_showcase"
    if _is_hormuz_marine_insurer(topic, business_user):
        return "hormuz_marine_insurer_showcase"
    if "sanctions" in topic.lower() and business_user == "trade_finance_lender":
        return "sanctions_trade_finance_showcase"
    return "generic_political_risk"


def _overall_rating(scores):
    average = (scores["likelihood"]["score"] + scores["impact"]["score"] + scores["immediacy"]["score"]) / 3
    if average >= 4.5:
        return "Severe"
    if average >= 3.5:
        return "High"
    if average >= 2.5:
        return "Moderate"
    return "Low"


def _sanctions_scores(scores, confidence, evidence_pack):
    confidence_score = 4 if evidence_pack and evidence_pack.get("fallback_demo_data_used") else confidence["confidence_score"]
    return {
        "likelihood": {
            "score": 4,
            "direction": "Elevated",
            "rationale": "Official sanctions guidance, regime context and legal analysis show live transaction-screening obligations for end-use exposure.",
        },
        "impact": {
            "score": 4,
            "direction": "High",
            "rationale": "Evidence links end-use controls to counterparty, payment, documentation, collateral and regulatory penalty exposure.",
        },
        "immediacy": {
            "score": 5,
            "direction": "Near-term",
            "rationale": "The 1-3 month horizon and current guidance require transaction teams to apply controls before approval, drawdown or settlement.",
        },
        "confidence": {
            "score": min(confidence_score, 4),
            "direction": "Moderate-high",
            "rationale": "Evidence is anchored in official and legal sources, but confidence remains below 5 because transaction-level facts, licensing position and payment route must be verified.",
        },
    }


def _display_scores(topic, time_horizon, scores, confidence, evidence_pack):
    display = {
        "likelihood": dict(scores["likelihood"]),
        "impact": dict(scores["impact"]),
        "immediacy": dict(scores["immediacy"]),
        "confidence": {
            "score": confidence["confidence_score"],
            "rationale": confidence["confidence_rationale"],
        },
    }

    if "hormuz" in topic.lower() and "1-3" in time_horizon:
        display["likelihood"] = {
            "score": 5,
            "direction": "Elevated",
            "rationale": "Transit-control, sanctions/legal and reputable reporting indicate constrained transit, security risk and active route-level controls around Hormuz.",
        }
        display["impact"] = {
            "score": 5,
            "direction": "Severe",
            "rationale": "Energy chokepoint, insurance-market and vessel-flow evidence show material exposure for tanker flows, cargo values, energy markets and marine war-risk pricing.",
        }
        display["immediacy"] = {
            "score": 5,
            "direction": "Near-term",
            "rationale": "The time horizon is 1-3 months and current transit-control, insurance and vessel-flow evidence describe conditions that require active monitoring now.",
        }
        confidence_score = 4 if evidence_pack and evidence_pack.get("fallback_demo_data_used") else display["confidence"]["score"]
        display["confidence"] = {
            "score": confidence_score,
            "direction": "Moderate-high",
            "rationale": "Evidence is diverse, but confidence is capped because conditions, diplomatic signals, vessel-flow data and war-risk pricing are fast-moving.",
        }

    if _is_uk_ets_shipping_operator(topic, "shipping_operator"):
        annualised_cost = 0
        if evidence_pack and evidence_pack.get("calculator_assumptions"):
            annualised_cost = 866561.79
        display["likelihood"] = {
            "score": 5,
            "direction": "Confirmed",
            "rationale": "Official UK ETS policy sources confirm domestic maritime expansion from 1 July 2026 for covered vessels and routes.",
        }
        display["impact"] = {
            "score": 4 if annualised_cost >= 500000 else 3,
            "direction": "Material",
            "rationale": "Impact is material for in-scope domestic routes because allowance cost becomes a recurring voyage-level cost, but the score is limited because UK-international routes remain scenario-only and operator-specific fuel burn must be validated.",
        }
        display["immediacy"] = {
            "score": 5,
            "direction": "Near-term",
            "rationale": "Immediacy is high because operators need to prepare MRV, reporting, verification, allowance procurement and pricing/pass-through processes before the scheme date.",
        }
        display["confidence"] = {
            "score": 4,
            "direction": "Moderate-high",
            "rationale": "Confidence is capped at 4/5 because official policy evidence is strong, but the calculation uses illustrative voyage assumptions and a manual UKA price rather than an embedded live price feed.",
        }

    return display


def _executive_judgement(topic, business_user, time_horizon):
    if _is_hormuz_marine_insurer(topic, business_user):
        return (
            "The Strait of Hormuz remains a severe marine insurance exposure because disruption is expressed through connected "
            "channels: safe transit uncertainty, carrier caution, oil and LNG cargo concentration, war-risk repricing, trapped "
            "vessel exposure and sanctions/compliance complexity.\n\n"
            "For a marine insurer, the central issue is accumulation. Hull war, cargo war, liability, reinsurance appetite and "
            f"policy wording can all be affected by the same transit shock. The underwriting stance should remain conservative over "
            f"the next {time_horizon}, with controls relaxed only when practical operating evidence confirms normalisation.\n\n"
            "De-escalation evidence should affect monitoring posture before underwriting controls. The practical tests are vessel-flow "
            "recovery, carrier willingness to transit, broker/reinsurance pricing and updated official maritime guidance."
        )

    return (
        f"{topic} presents a commercial risk over {time_horizon}. The immediate priority is to identify which exposures are "
        "supported by evidence, where confidence is strongest, and which controls should be adjusted."
    )


def _key_judgements(topic):
    if "hormuz" in topic.lower():
        rows = [
            (
                "Safe transit risk remains material",
                "IMO official reporting indicates severe maritime-security conditions and uncertainty over safe passage.",
                "Official source; high-priority requirement; route named as Strait of Hormuz.",
                "Supports active hull war controls, route approval thresholds and accumulation review.",
            ),
            (
                "Carrier caution indicates practical operating constraints",
                "Maersk operational reporting describes constrained conditions and continued caution around Gulf transit.",
                "Company update; current operational decision signal.",
                "Carrier behaviour is a practical signal for voyage approval, delay, trapped-vessel and service-continuity exposure.",
            ),
            (
                "Energy chokepoint exposure makes impact severe",
                "IEA data shows Hormuz is central to global oil and LNG flows.",
                "Quantified oil/LNG transit exposure in source pack.",
                "Raises cargo war, tanker, energy trade and trade finance exposure even before a full closure scenario.",
            ),
            (
                "War-risk pricing and reinsurance appetite require active review",
                "Howden Re evidence points to major war-risk repricing and higher voyage-cost assumptions.",
                "High-weight insurance source; premium figures extracted.",
                "Premium adequacy, referral thresholds, reinsurance appetite and policy wording should be actively reviewed.",
            ),
            (
                "Vessel-flow disruption supports high immediacy",
                "Kpler, AP and specialist vessel-flow sources describe disrupted or abnormal tanker and vessel behaviour.",
                "Vessel counts, flow data and current operational reporting.",
                "Supports near-term monitoring of aggregation, trapped vessels, floating cargo and claims scenarios.",
            ),
            (
                "De-escalation evidence reduces certainty around worst-case assumptions",
                "Axios reporting points to possible reopening or diplomatic pathways but with operational recovery uncertainty.",
                "Contrary source present; confidence capped at 4/5 in curated mode.",
                "Worst-case assumptions should be balanced, but controls should not be relaxed until transit, pricing and carrier confidence improve.",
            ),
        ]
    else:
        rows = [
            ("Evidence supports a live commercial risk", "Multiple source types indicate disruption potential.", "Source coverage and recency should be reviewed.", "Review exposure, controls and decision triggers."),
        ]

    return _table(["Judgement", "Evidence basis", "Concrete signal", "Client relevance"], rows)


def _risk_scorecard(scores):
    rows = [
        ("Likelihood", f"{scores['likelihood']['score']}/5", scores["likelihood"].get("direction", "Elevated"), scores["likelihood"]["rationale"]),
        ("Impact", f"{scores['impact']['score']}/5", scores["impact"].get("direction", "Severe"), scores["impact"]["rationale"]),
        ("Immediacy", f"{scores['immediacy']['score']}/5", scores["immediacy"].get("direction", "Near-term"), scores["immediacy"]["rationale"]),
        ("Confidence", f"{scores['confidence']['score']}/5", scores["confidence"].get("direction", "Moderate-high"), scores["confidence"]["rationale"]),
    ]
    return _table(["Dimension", "Score", "Direction", "Evidence-based rationale"], rows)


def _risk_driver_sections(topic, evidence_pack=None, sources=None):
    synthesized = []
    if evidence_pack and evidence_pack.get("risk_drivers"):
        synthesized = evidence_pack["risk_drivers"]
    elif sources:
        synthesized = synthesize_risk_drivers(sources)
    if synthesized:
        return _risk_driver_sections_from_synthesis(synthesized)

    if "hormuz" not in topic.lower():
        return "### A. Primary risk driver\n**Evidence used:** Supplied source pack.\n\n**Why it matters:** The evidence indicates a plausible commercial disruption pathway.\n\n**Commercial implication:** Review affected exposures and controls.\n\n**Action / watchpoint:** Track source updates before changing controls."

    drivers = [
        (
            "A. Maritime security and transit risk",
            "IMO official evidence indicates severe maritime-security conditions and uncertainty over safe transit.",
            "Safe passage uncertainty affects vessel approval, crew risk, voyage continuity and the probability of war-risk claims.",
            "Hull war, liability, crew welfare and route approval thresholds should remain under enhanced control.",
            "Use official maritime advisories and incident reporting as hard triggers for referral, escalation or relaxation.",
        ),
        (
            "B. Carrier and operational disruption",
            "Maersk company evidence and AP reporting indicate constrained operating conditions, carrier caution and vessels affected by Gulf access uncertainty.",
            "Carrier caution is a practical market signal that the risk is affecting operating decisions, not only headline sentiment.",
            "Trapped vessel, cargo delay, voyage deviation and service continuity exposures should be referred where Gulf transit is material.",
            "Track carrier willingness to transit, Gulf call acceptance and service updates before changing underwriting stance.",
        ),
        (
            "C. Energy chokepoint exposure",
            "IEA data shows Hormuz is central to global oil and LNG flows, including major shares of seaborne oil trade and Gulf LNG exports.",
            "Cargo concentration and limited alternatives make even partial disruption material for tanker demand, cargo values and energy-market volatility.",
            "Cargo war, tanker hull war aggregation and energy-linked trade finance exposures require stress testing.",
            "Monitor oil/LNG flow changes, alternative export-route use and any state controls over maritime passage.",
        ),
        (
            "D. Insurance-market repricing",
            "Howden Re evidence points to significant Hormuz war-risk repricing and higher per-transit premium assumptions.",
            "Pricing can move faster than physical incident counts when underwriters, brokers and reinsurers reassess route severity.",
            "Premium adequacy, reinsurance appetite, deductibles, limits and referral thresholds should be actively reviewed.",
            "Use broker indications, reinsurer feedback and quoted war-risk rates as controls for binding or relaxing Gulf-linked risks.",
        ),
        (
            "E. Vessel-flow and market behaviour",
            "Kpler vessel-flow evidence, AP reporting and specialist market analysis indicate abnormal tanker behaviour, floating cargo and reduced or disrupted flows.",
            "Vessel-flow data shows whether commercial traffic is normalising or whether disruption is still embedded in market behaviour.",
            "Claims aggregation, floating cargo, port congestion and trapped vessel exposure should be monitored by assured, cargo and vessel class.",
            "Use vessel-flow recovery and reduced congestion/floating storage as practical tests before easing controls.",
        ),
        (
            "F. De-escalation and stabilisation evidence",
            "Axios reporting indicates possible diplomatic or reopening pathways, while noting that normalisation may be stop-start and confidence-dependent.",
            "Stabilising evidence reduces certainty around worst-case assumptions but does not prove that operating conditions have normalised.",
            "Underwriting controls should respond to practical evidence before diplomatic headlines: flow recovery, carrier confidence and lower pricing.",
            "Use de-escalation reporting as a monitoring input, not a standalone trigger to relax controls.",
        ),
    ]

    sections = []
    for title, evidence, why, implication, action in drivers:
        sections.append(
            f"### {title}\n"
            f"**Evidence signal:** {evidence}\n\n"
            f"**Commercial meaning:** {why}\n\n"
            f"**Insurance implication:** {implication}\n\n"
            f"**Decision use:** {action}"
        )
    return "\n\n".join(sections)


def _risk_driver_sections_from_synthesis(drivers):
    sections = []
    for index, driver in enumerate(drivers, start=1):
        sections.append(
            "### {index}. {name}\n"
            "**Evidence signal:** {summary}\n\n"
            "**Quantified detail:** {quantified}\n\n"
            "**Highest-weight sources:** {sources}\n\n"
            "**Why it matters commercially:** {commercial}\n\n"
            "**Client implication:** {implication}\n\n"
            "**Decision use:** {decision}\n\n"
            "**Refresh trigger:** {refresh}".format(
                index=index,
                name=driver.get("driver_name", "Risk driver"),
                summary=driver.get("evidence_summary", "No evidence summary available."),
                quantified=", ".join(driver.get("quantified_facts", [])[:6]) or "No quantified detail extracted.",
                sources=", ".join(driver.get("highest_weight_sources", [])) or "None",
                commercial=driver.get("commercial_meaning", "Analyst review required."),
                implication=driver.get("business_user_implication", "Analyst review required."),
                decision=driver.get("decision_use", "Analyst review required."),
                refresh=driver.get("refresh_trigger", "Refresh before major decisions."),
            )
        )
    return "\n\n".join(sections)


def _decision_stance(scores, evidence_pack):
    return _table(
        ["Item", "Assessment"],
        [
            ("Current stance", "Maintain enhanced controls for Gulf / Hormuz-linked exposure"),
            ("Risk level", _overall_rating(scores)),
            ("Confidence", f"{scores['confidence']['score']}/5"),
            ("Primary risk", "Accumulation and pricing pressure across hull war, cargo war, trapped vessel exposure, sanctions/compliance and reinsurance appetite"),
            ("Action bias", "Tighten referral, review wording, reassess premium adequacy and monitor de-escalation evidence before relaxing controls"),
            ("Relaxation trigger", "Sustained vessel-flow recovery, carrier confidence, lower war-risk pricing and updated official maritime guidance"),
        ],
    )


def _decision_implications():
    rows = [
        ("Bind / refer / decline", "Gulf-linked risks should move toward referral unless exposure is clearly limited and priced.", "Apply enhanced referral for tanker cargoes, unclear counterparties and Hormuz transit dependency."),
        ("Premium adequacy", "Observed war-risk repricing creates risk of underpriced new or renewed exposure.", "Benchmark terms against broker and reinsurance market signals before binding."),
        ("Aggregation monitoring", "The same transit shock can affect multiple assureds, vessels, cargoes and classes.", "Refresh route-level accumulation views across hull war and cargo war."),
        ("Policy wording", "Blocking/trapping, sanctions, notice and cancellation language may determine loss response.", "Review wording before binding or renewing Gulf-linked exposure."),
        ("Reinsurance appetite", "Capacity or exclusions may move quickly if market perception worsens.", "Confirm current appetite, attachment points and exclusions."),
        ("Sanctions/compliance", "Cargo, counterparties and state controls may create legal and payment complications.", "Tighten screening and require escalation for unclear parties or sanctions-sensitive cargoes."),
        ("Claims preparedness", "Trapped vessel, blocked passage, cargo delay and crew welfare claims may emerge together.", "Check claims playbooks and operational response assumptions."),
        ("Broker/client communication", "Clients need clear stance, referral requirements and relaxation conditions.", "Communicate controls and evidence-based triggers clearly."),
    ]
    return _table(["Decision area", "Current implication", "Required response"], rows)


def _exposure_pressure_map():
    rows = [
        ("Hull war", "High", "Official security and carrier caution evidence.", "Maintain route-level controls and require referral for Gulf transits.", "Updated official guidance and sustained normal transit."),
        ("Cargo war", "High", "Energy chokepoint and cargo concentration evidence.", "Review limits, accumulation and cargo-war pricing assumptions.", "Lower cargo disruption indicators and improved tanker-flow data."),
        ("Trapped/blocked vessel exposure", "High", "Carrier, news and vessel-flow evidence.", "Model trapped vessel scenarios by assured, vessel class and cargo.", "Reduced port congestion, fewer trapped-vessel reports and carrier confidence."),
        ("Liability / crew welfare", "High", "Official safety and crew welfare signals.", "Check liability wording, crew welfare response and claims protocols.", "Improved official safety advisories and incident trend reduction."),
        ("Reinsurance appetite", "High", "Insurance-market repricing evidence.", "Engage reinsurers and brokers on appetite, capacity and attachment points.", "Reinsurer appetite stabilises and war-risk pricing falls."),
        ("Sanctions/compliance", "High", "State-control and counterparty complexity.", "Tighten screening for unclear counterparties, cargoes and vessel links.", "Updated legal/sanctions review confirms lower exposure."),
        ("Policy wording", "Medium-high", "Blocking/trapping, sanctions and notice provisions may determine response.", "Review war, strikes, blocking/trapping, sanctions, notice and cancellation clauses.", "Wording review complete and risk appetite agreed."),
        ("Claims aggregation", "High", "Common transit shock can affect multiple policies.", "Refresh aggregation by route, assured, vessel class, cargo type and limits.", "Aggregation returns within appetite after flow and pricing normalise."),
    ]
    return _table(["Exposure channel", "Pressure", "Evidence basis", "Underwriting response", "Relaxation trigger"], rows)


def _scenario_outlook():
    rows = [
        ("Base case: constrained partial transit", "Some transit continues, but carrier caution, elevated premiums and selective controls remain.", "Renewed incident reporting, weaker carrier confidence or rising quoted premiums.", "Stable vessel-flow recovery, fewer incident reports and no further market repricing.", "Maintain controls; reprice and refer higher-risk Gulf transits."),
        ("Downside case: renewed security incidents or tighter state controls", "New incidents, detention risk or state restrictions reduce flows and increase trapped vessel exposure.", "Official advisories worsen, state controls tighten or carrier services pull back.", "Clear official improvement and restored commercial transit patterns.", "Escalate aggregation controls, tighten limits and reassess reinsurance appetite."),
        ("Stabilisation case: de-escalation and gradual reopening", "Diplomatic progress or reopening signals improve confidence, but operating normalisation is gradual.", "Talks fail, incident risk returns or insurers/reinsurers keep pricing elevated.", "Vessel-flow recovery, carrier confidence, lower war-risk pricing and updated official guidance.", "Relax controls only after operational evidence confirms improvement."),
    ]
    return _table(["Scenario", "Description", "Escalation trigger", "Relaxation trigger", "Insurance implication"], rows)


def _underwriting_actions():
    return "\n".join(
        [
            "1. Accumulation review: refresh route-level exposure across hull war, cargo war, assured, vessel class, cargo type and Gulf transit dependency.",
            "2. Pricing review: benchmark premium adequacy against current broker and reinsurance indicators before binding new Gulf-linked risks.",
            "3. Referral controls: tighten referral rules for Gulf transit, tanker cargoes, unclear counterparties and sanctions-sensitive cargoes.",
            "4. Wording review: check war, strikes, blocking/trapping, sanctions, notice and cancellation provisions.",
            "5. Reinsurance check: confirm appetite, exclusions, attachment points and any changes in available capacity.",
            "6. Claims preparedness: review trapped vessel, blocked passage, cargo delay and crew welfare response assumptions.",
            "7. Relaxation test: ease controls only after vessel-flow recovery, carrier confidence and war-risk premium movement support normalisation.",
        ]
    )


def _watchlist():
    rows = [
        ("Official maritime advisories", "Confirms safety conditions, incident severity and route-level control requirements.", "Official maritime/security sources"),
        ("Carrier service updates", "Shows whether operators are willing to accept practical transit risk.", "Carrier/company updates"),
        ("War-risk premium movement", "Direct signal of underwriting and reinsurance market appetite.", "Insurance market evidence"),
        ("Vessel-flow recovery", "Indicates whether trade is normalising or still constrained.", "Vessel-flow/freight market evidence"),
        ("Sanctions announcements", "Affects cargo legality, counterparty screening and claims response.", "Official sanctions/legal sources"),
        ("Diplomatic de-escalation", "Can reduce downside risk but requires operational confirmation.", "Reputable news and official sources"),
        ("Port congestion or trapped vessel reporting", "Signals accumulation, delay and blocked vessel exposure.", "Port, carrier and reputable news sources"),
        ("Reinsurance appetite changes", "Determines capacity, attachment points and net exposure tolerance.", "Broker/reinsurance market evidence"),
    ]
    return _table(["Indicator", "Why it matters", "Source type to monitor"], rows)


def _evidence_appendix(sources, domain=""):
    if not sources:
        return "No source evidence supplied."

    rows = []
    for source in sources:
        if domain == "maritime_trade":
            rows.append(
                (
                    source.get("source_id", ""),
                    source.get("requirement_name", ""),
                    source.get("source_role", source.get("source_type", source.get("inferred_source_type", "unknown"))),
                    source.get("evidence_weight", ""),
                    source.get("claim_supported") or source.get("extracted_claim") or source.get("summary", ""),
                    "; ".join(source.get("quantified_facts", [])[:2]) or "No quantified signal extracted.",
                    source.get("decision_use", ""),
                    source.get("caveat", ""),
                    source.get("refresh_trigger", _refresh_trigger_for_requirement(source.get("requirement_name", ""))),
                )
            )
        else:
            rows.append(
                (
                    source.get("source_id", ""),
                    source.get("requirement_name", ""),
                    source.get("evidence_weight", ""),
                    source.get("source_type", source.get("inferred_source_type", "unknown")),
                    source.get("risk_driver") or _risk_driver_for_source(source.get("source_type", "")),
                    source.get("judgement_supported") or _judgement_for_source(source.get("source_type", "")),
                    source.get("extracted_claim") or source.get("claim_supported") or source.get("summary", ""),
                    source.get("decision_use", ""),
                    source.get("caveat", ""),
                )
            )
    if domain == "maritime_trade":
        return _table(
            ["Source ID", "Requirement", "Source role", "Evidence weight", "Claim", "Quantified / concrete signal", "Decision use", "Caveat", "Refresh trigger"],
            rows,
        )
    return _table(["Source ID", "Requirement", "Weight", "Source Type", "Risk Driver", "Judgement Supported", "Claim", "Decision Use", "Caveat"], rows)


def _source_requirement_coverage(evidence_pack):
    if not evidence_pack or not evidence_pack.get("requirement_coverage"):
        return "No source requirement coverage available."
    rows = []
    sources_by_id = {item.get("source_id"): item for item in evidence_pack.get("selected_sources", [])}
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    for item in evidence_pack["requirement_coverage"]:
        strongest = _strongest_requirement_source(item.get("covered_by", []), sources_by_id)
        if domain == "maritime_trade":
            rows.append(
                (
                    item["requirement_name"],
                    _coverage_label(item),
                    strongest["label"],
                    strongest["role"],
                    item["evidence_weight"],
                    item["decision_questions_supported"][0] if item.get("decision_questions_supported") else "",
                    item["remaining_gap"],
                )
            )
        else:
            rows.append(
                (
                    item["requirement_name"],
                    _coverage_label(item),
                    item["evidence_weight"],
                    strongest["label"],
                    item["decision_questions_supported"][0] if item.get("decision_questions_supported") else "",
                    item["remaining_gap"],
                )
            )
    if domain == "maritime_trade":
        return _table(["Requirement", "Coverage", "Strongest source", "Source role", "Evidence weight", "Decision supported", "Gap / refresh need"], rows)
    return _table(["Requirement", "Coverage", "Evidence weight", "Strongest source", "Decision supported", "Gap / refresh need"], rows)


def _coverage_label(item):
    explicit = item.get("coverage_status")
    if explicit == "gap":
        return "Gap"
    if explicit == "partially_covered":
        covered_by = ", ".join(item.get("covered_by", [])) or "None"
        return f"Partially covered: {covered_by}"
    if explicit == "covered":
        covered_by = ", ".join(item.get("covered_by", [])) or "None"
        return f"Covered by {item.get('covered_by_count', 0)} source(s): {covered_by}"
    count = item.get("covered_by_count", 0)
    if count == 0:
        return "Gap"
    return f"Covered by {count} source(s): {', '.join(item.get('covered_by', []))}"


def _strongest_requirement_source(source_ids, sources_by_id):
    sources = [sources_by_id[source_id] for source_id in source_ids if source_id in sources_by_id]
    if not sources:
        return {"label": "None", "role": "None"}
    strongest = sorted(
        sources,
        key=lambda item: (
            3 if item.get("evidence_weight") == "high" else 2 if item.get("evidence_weight") == "medium" else 1,
            item.get("total_score", 0),
        ),
        reverse=True,
    )[0]
    title = _clean_source_title(strongest.get("title", "") or "Source")
    publisher = strongest.get("publisher", "")
    label = f"{strongest.get('source_id', '')} — {title}"
    if publisher:
        label = f"{label} ({publisher})"
    return {"label": label, "role": strongest.get("source_role", strongest.get("source_type", ""))}


def _refresh_trigger_for_requirement(requirement_name):
    mapping = {
        "official_maritime_security": "Refresh if official maritime or security guidance changes.",
        "transit_control_or_constabulary_actions": "Refresh if detention reports, coordination demands or transit-control notices change.",
        "sanctions_and_safe_passage_payment_risk": "Refresh immediately if any toll, payment, guarantee, offset, swap or in-kind demand appears.",
        "war_risk_insurance_pricing": "Refresh before voyage approval if war-risk premium, exclusions or cancellation wording changes.",
        "vessel_flow_and_AIS_behaviour": "Refresh if AIS disruption, vessel-flow conditions or recovery signals change.",
        "energy_cargo_and_chokepoint_exposure": "Refresh if cargo exposure or structural chokepoint assumptions change.",
        "route_cost_and_arbitrage_inputs": "Refresh before commercial use if delay, reroute or charter assumptions change.",
        "contrary_or_de_escalation_evidence": "Refresh before relaxing controls if de-escalation claims emerge.",
    }
    return mapping.get(requirement_name, "Refresh before operational use.")


def _risk_driver_for_source(source_type):
    mapping = {
        "official_primary": "Maritime security and transit risk",
        "company_update": "Carrier and operational disruption",
        "energy_chokepoint_data": "Energy chokepoint exposure",
        "insurance_market_evidence": "Insurance-market repricing",
        "vessel_flow_or_freight_market_evidence": "Vessel-flow and market behaviour",
        "reputable_news": "Carrier and operational disruption",
        "specialist_analysis": "Vessel-flow and market behaviour",
        "contrary_or_stabilising_evidence": "De-escalation and stabilisation evidence",
    }
    return mapping.get(source_type, "General evidence")


def _judgement_for_source(source_type):
    mapping = {
        "official_primary": "Safe transit risk remains material",
        "company_update": "Carrier caution indicates practical operating constraints",
        "energy_chokepoint_data": "Energy chokepoint exposure makes impact severe",
        "insurance_market_evidence": "War-risk pricing and reinsurance appetite require active review",
        "vessel_flow_or_freight_market_evidence": "Vessel-flow disruption supports high immediacy",
        "reputable_news": "Vessel-flow disruption supports high immediacy",
        "specialist_analysis": "Vessel-flow disruption supports high immediacy",
        "contrary_or_stabilising_evidence": "De-escalation evidence reduces certainty around worst-case assumptions",
    }
    return mapping.get(source_type, "Evidence supports commercial risk assessment")


def _source_strategy(evidence_pack):
    if not evidence_pack:
        return "- No live source strategy supplied."
    return _format_bullets(
        f"`{item['category']}`: {item['queries'][0]}"
        for item in evidence_pack["source_strategy"]["categories"]
    )


def _source_requirements(evidence_pack):
    if not evidence_pack or not evidence_pack.get("source_requirements"):
        return "No source requirements supplied."
    rows = []
    for item in evidence_pack["source_requirements"]:
        rows.append(
            (
                item["requirement_id"],
                item["requirement_name"],
                item["why_required"],
                ", ".join(item["preferred_source_types"]),
                ", ".join(item["preferred_domains"]),
                item["freshness_expectation"],
            )
        )
    return _table(["ID", "Requirement", "Why required", "Preferred source types", "Preferred domains", "Freshness expectation"], rows)


def _source_register(evidence_pack):
    if not evidence_pack:
        return "No source register supplied."
    rows = [
        (
            item.get("source_id", ""),
            item["source_type"],
            item["publisher"],
            item["publication_date"],
            item["url"],
        )
        for item in evidence_pack["evidence"]
    ]
    return _table(["Source ID", "Source Type", "Publisher", "Date", "URL"], rows)


def _source_audit_summary(evidence_pack):
    if not evidence_pack:
        return "No source audit metadata supplied."
    readout = evidence_pack.get("quantified_evidence_readout", {})
    rows = [
        ("Search provider", evidence_pack.get("search_provider", "")),
        ("Evidence mode", evidence_pack.get("evidence_mode", "")),
        ("Fallback data used", str(evidence_pack.get("fallback_demo_data_used", False)).lower()),
        ("Provider error", evidence_pack.get("provider_error", "") or "None"),
        ("Evidence categories covered", ", ".join(evidence_pack.get("source_categories_covered", [])) or "None"),
        ("Evidence categories missing", ", ".join(evidence_pack.get("source_categories_missing", [])) or "None"),
        ("Total queries run", evidence_pack.get("total_queries_run", 0)),
        ("Candidate sources", evidence_pack.get("candidate_count", "")),
        ("Selected sources", evidence_pack.get("selected_count", "")),
        ("Rejected sources", evidence_pack.get("rejected_count", "")),
        ("Strongest sources", readout.get("strongest_evidence", "")),
        ("Weakest evidence area", readout.get("weakest_evidence", "")),
        ("Missing or stale evidence", ", ".join(evidence_pack.get("requirements_missing", [])) or "None flagged"),
        ("Source hierarchy coverage", f"{readout.get('requirement_coverage_percent', 0)}% requirement coverage"),
        ("Confidence cap reason", evidence_pack.get("confidence_cap_reason", readout.get("confidence_cap", ""))),
        ("Refresh priorities", _refresh_priority_summary(evidence_pack)),
    ]
    return _table(["Item", "Value"], rows)


def _review_controls(evidence_pack):
    fallback = bool(evidence_pack and evidence_pack.get("fallback_demo_data_used"))
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "regulatory_carbon_shipping":
        rows = [
            ("Evidence mode", "Review" if fallback else "Passed", "Confirm whether live retrieval remains appropriate and rerun if material policy updates appear."),
            ("Source freshness", "Passed", "Publication dates are visible in the appendix and audit trail."),
            ("UKA price recency", "Review", "Refresh the manual UKA input until an embedded live price feed is available."),
            ("Methodology validation", "Review", "Confirm fuel-consumption assumptions and emissions factor against verifier-approved methodology."),
            ("Scope control", "Passed", "Keep UK-international routes as scenario-only unless later policy confirms live scope."),
            ("Reporting timeline", "Warning", "Monitor verified reporting and surrender deadlines as implementation guidance evolves."),
            ("Operator data sign-off", "Warning", "Replace illustrative voyage assumptions with operator-specific route and vessel data before final decisions."),
        ]
        return _table(["Control", "Status", "Required action"], rows)
    if domain == "maritime_trade":
        rows = [
            ("Evidence mode", "Review" if fallback else "Passed", "Confirm whether live retrieval remains appropriate for the voyage decision context."),
            ("Source freshness", "Passed", "Publication dates are visible in the appendix and audit trail."),
            ("Sanctions/payment trigger", "Warning", "Treat any toll, safe-passage fee, guarantee, offset, swap or in-kind demand as legal/compliance escalation."),
            ("Insurance wording", "Review", "Confirm war-risk cover, exclusions, cancellation language and premium validity before transit."),
            ("AIS and routing review", "Review", "Validate transponder behaviour, routing instructions and detention indicators before sailing."),
            ("Cost assumption validation", "Warning", "Replace illustrative vessel value, delay and reroute assumptions with operator-specific data before commercial use."),
            ("Relaxation gate", "Warning", "Move from hold or reroute to conditional transit only when official guidance, insurer appetite and vessel-flow recovery align."),
        ]
        return _table(["Control", "Status", "Required action"], rows)
    rows = [
        ("Evidence mode", "Review" if fallback else "Passed", "Confirm whether curated pack or live retrieval is appropriate for the decision context."),
        ("Source freshness", "Passed", "Publication dates are visible in the appendix and audit trail."),
        ("Market-pricing recency", "Review", "Refresh broker and reinsurance indications before binding or relaxing Gulf-linked risks."),
        ("De-escalation update", "Review", "Refresh diplomatic and reopening reporting before changing stance."),
        ("Primary-source verification", "Passed", "Official, company, energy and insurance-market sources are represented."),
        ("Sanctions/legal review", "Warning", "Specialist legal review is required for sanctions-sensitive counterparties, cargoes or vessels."),
        ("Underwriting sign-off", "Warning", "Enhanced controls should be changed only with underwriting governance approval."),
    ]
    return _table(["Control", "Status", "Required action"], rows)


def _methodology(evidence_pack):
    return (
        "Method: source plan, source requirements, source ranking, claim extraction, quantified fact extraction, risk-driver synthesis, "
        "score bridge and review controls. Scoring is rule-based and transparent; changes to official, market, legal or operational evidence should trigger refresh."
    )


def _quantified_evidence_readout(evidence_pack, business_user):
    if not evidence_pack:
        return "No quantified evidence readout available."
    readout = evidence_pack.get("quantified_evidence_readout") or build_quantified_evidence_readout(evidence_pack)
    facts = readout.get("quantified_facts", [])
    rows = [
        ("selected sources", readout.get("source_count", 0), "Shows breadth of selected evidence."),
        ("high-weight sources", readout.get("high_weight_source_count", 0), "Shows how much source evidence carries stronger analyst weight."),
        ("source requirement coverage", f"{readout.get('requirement_coverage_percent', 0)}%", "Shows whether required evidence questions are covered."),
        ("average source quality", readout.get("average_source_quality", 0), "Average of reliability, relevance, recency, specificity and decision value."),
        ("quantified facts extracted", len(facts), "Shows how much numeric evidence supports the judgement."),
        ("confidence cap", readout.get("confidence_cap", ""), "Explains why confidence is not overstated."),
    ]
    if business_user == "trade_finance_lender":
        rows.extend(
            [
                ("official/legal source count", _count_trade_finance_sources(evidence_pack), "Shows whether the control framework is anchored in official/legal evidence."),
                ("transaction control points identified", _count_matching_terms(evidence_pack, ["hold", "decline", "escalation", "licence", "drawdown"]), "Shows approval/hold/decline control coverage."),
                ("documentation triggers", _count_matching_terms(evidence_pack, ["documentation", "end-use", "classification", "contractual"]), "Shows evidence for document requests."),
                ("payment / compliance triggers", _count_matching_terms(evidence_pack, ["payment", "correspondent", "sanctions", "licensing"]), "Shows payment and compliance escalation evidence."),
            ]
        )
    return _table(["Metric", "Value", "Why it matters"], rows)


def _evidence_to_score_bridge(evidence_pack, scores):
    if not evidence_pack:
        return "No evidence-to-score bridge available."
    bridge = build_evidence_to_score_bridge(evidence_pack, scores)
    rows = []
    for dimension in ["likelihood", "impact", "immediacy", "confidence"]:
        item = bridge[dimension]
        rows.append(
            (
                dimension.title(),
                f"{item['score']}/5",
                f"{item['evidence_basis']} Supporting sources: {', '.join(item.get('supporting_sources', [])) or 'none recorded'}. Key facts: {'; '.join(item.get('quantified_facts_used', [])[:4]) or 'none extracted'}.",
                f"Higher: {item['why_score_not_higher']} Lower: {item['why_score_not_lower']}",
                item["review_trigger"],
            )
        )
    return _table(["Score dimension", "Score", "Evidence basis", "Why not higher / lower", "Review trigger"], rows)


def _refresh_priority_summary(evidence_pack):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "regulatory_carbon_shipping":
        return "; ".join(
            [
                "Refresh UKA price before pricing or contract decisions.",
                "Refresh UK ETS Authority guidance if maritime scope, reporting or surrender deadlines change.",
                "Validate operator-specific fuel burn and route classification before using the cost estimate commercially.",
                "Refresh future-scope assumptions if UK-international maritime expansion policy changes.",
                "Review emissions factor methodology with verifier / MRV process.",
            ]
        )
    return "; ".join(item.get("refresh_trigger", "") for item in evidence_pack.get("refresh_priorities", [])[:3])


def _clean_source_title(title):
    title = title.replace("[PDF] ", "").replace(":: Lloyd's List", "").replace(" - GOV.UK", "")
    title = title.replace(" | Stephenson Harwood", "").replace(" - International Council on Clean Transportation", " - ICCT")
    title = title.replace(" ...", "").replace("...", "")
    title = " ".join(title.split())
    return title[:70]


def _count_trade_finance_sources(evidence_pack):
    return sum(
        1 for source in evidence_pack.get("selected_sources", [])
        if source.get("source_type") in {"official_primary", "specialist_analysis"}
    )


def _count_matching_terms(evidence_pack, terms):
    count = 0
    for evidence in evidence_pack.get("evidence", []):
        text = " ".join([evidence.get("extracted_claim", ""), evidence.get("decision_use", ""), evidence.get("commercial_meaning", "")]).lower()
        if any(term in text for term in terms):
            count += 1
    return count


def _table(headers, rows):
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(_escape_table_cell(value) for value in row) + " |")
    return "\n".join(output)


def _hormuz_option_decision_label(option, decision, preferred_option):
    if option == "Direct transit":
        return "Blocked unless sanctions, insurance and vessel-flow triggers clear."
    if option == "Delay / wait":
        return "Use only if uncertainty looks short-lived and waiting remains cheaper than reroute."
    if option == "Reroute":
        return "Preferred when premium pressure or detention risk makes direct transit uneconomic."
    if option == "Legal hold":
        return "Required if any payment, toll, guarantee, offset, swap or coordination demand appears."
    return decision or preferred_option


def generate_brief(topic, business_user, region, time_horizon, concerns, sources=None, evidence_pack=None):
    sources = sources or []
    base_scores = score_risk(topic=topic, concerns=concerns, region=region, time_horizon=time_horizon, sources=sources)
    confidence = calculate_confidence(sources)
    scores = _display_scores(topic, time_horizon, base_scores, confidence, evidence_pack)
    review_flags = generate_review_flags(sources, evidence_pack=evidence_pack)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    if select_report_template(topic, business_user) == "uk_ets_shipping_operator_showcase":
        return _generate_uk_ets_shipping_operator_brief(
            topic=topic,
            business_user=business_user,
            region=region,
            time_horizon=time_horizon,
            sources=sources,
            evidence_pack=evidence_pack,
            scores=scores,
            review_flags=review_flags,
            generated_at=generated_at,
        )
    if select_report_template(topic, business_user) == "hormuz_shipping_operator_showcase":
        return _generate_hormuz_shipping_operator_brief(
            topic=topic,
            business_user=business_user,
            region=region,
            time_horizon=time_horizon,
            sources=sources,
            evidence_pack=evidence_pack,
            scores=scores,
            review_flags=review_flags,
            generated_at=generated_at,
        )
    if select_report_template(topic, business_user) == "generic_political_risk":
        return _generate_generic_brief(
            topic=topic,
            business_user=business_user,
            region=region,
            time_horizon=time_horizon,
            sources=sources,
            evidence_pack=evidence_pack,
            scores=scores,
            review_flags=review_flags,
            generated_at=generated_at,
        )
    if select_report_template(topic, business_user) == "sanctions_trade_finance_showcase":
        sanctions_scores = _sanctions_scores(base_scores, confidence, evidence_pack)
        return _generate_sanctions_trade_finance_brief(
            topic=topic,
            business_user=business_user,
            region=region,
            time_horizon=time_horizon,
            sources=sources,
            evidence_pack=evidence_pack,
            scores=sanctions_scores,
            review_flags=review_flags,
            generated_at=generated_at,
        )

    return f"""# Marine & Trade Risk Brief
## {topic} — {business_user.replace("_", " ")} exposure

| Field | Value |
| --- | --- |
| Risk issue | {topic} |
| Business lens | Marine insurance underwriting and accumulation management |
| Region | {region} |
| Time horizon | {time_horizon} |
| Overall risk level | {_overall_rating(scores)} |
| Confidence | {scores["confidence"]["score"]}/5 |
| Evidence mode | {_evidence_status(evidence_pack)} |

## Decision Stance

{_decision_stance(scores, evidence_pack)}

## 1. Executive Judgement

{_executive_judgement(topic, business_user, time_horizon)}

## 2. Key Judgements

{_key_judgements(topic)}

## 3. Risk Scorecard

{_risk_scorecard(scores)}

## Quantified Evidence Readout

{_quantified_evidence_readout(evidence_pack, business_user)}

## Evidence-To-Score Bridge

{_evidence_to_score_bridge(evidence_pack, scores)}

## Decision Implications

{_decision_implications()}

## 4. Evidence-Led Risk Drivers

{_risk_driver_sections(topic, evidence_pack=evidence_pack, sources=sources)}

## 5. Exposure Pressure Map

{_exposure_pressure_map()}

## 6. Scenario Outlook

{_scenario_outlook()}

## 7. Recommended Underwriting Actions

{_underwriting_actions()}

## 8. Watchlist / Early Warning Indicators

{_watchlist()}

## Source Requirement Coverage

{_source_requirement_coverage(evidence_pack)}

## 9. Evidence Appendix

{_evidence_appendix(sources)}

## 10. Methodology and Review Controls

{_methodology(evidence_pack)}

### Source Strategy

{_source_strategy(evidence_pack)}

### Source Requirements

{_source_requirements(evidence_pack)}

### Source Audit Summary

{_source_audit_summary(evidence_pack)}

### Source Register

{_source_register(evidence_pack)}

### Review Flags

{_format_bullets(review_flags)}

### Review Controls

{_review_controls(evidence_pack)}
"""


def _evidence_status(evidence_pack):
    if evidence_pack and evidence_pack.get("fallback_demo_data_used"):
        return "Reproducible curated source pack"
    if evidence_pack:
        return "Live source retrieval"
    return "Manual source mode."


def _generate_hormuz_shipping_operator_brief(topic, business_user, region, time_horizon, sources, evidence_pack, scores, review_flags, generated_at):
    route_cost = assess_route_cost(
        route_name="Hormuz-linked UK operator voyage",
        direct_transit_allowed=False,
        estimated_direct_voyage_days=14,
        estimated_reroute_days=24,
        daily_vessel_cost=45000,
        bunker_cost_per_day=28000,
        war_risk_premium_direct=750000,
        war_risk_premium_reroute=150000,
        demurrage_or_delay_cost_per_day=35000,
        sanctions_risk_flag=True,
        compliance_hold_days=5,
    )
    engine = evaluate_hormuz_route_decision(
        sanctions_red_flag=True,
        war_risk_premium_pct=0.02,
        vessel_value=100000000,
        direct_voyage_cost=(14 * (45000 + 28000)),
        delay_days=5,
        delay_cost_per_day=35000 + 45000 + 28000,
        reroute_extra_days=10,
        reroute_cost_per_day=45000 + 28000,
        ais_disruption_level="high",
        vessel_flow_status="severely_disrupted",
        detention_risk="high",
        insurance_cover_status="unclear",
        official_guidance_status="restrictive",
    )
    sanctions_claims = [item for item in sources if item.get("requirement_name") == "sanctions_and_safe_passage_payment_risk"][:2]
    flow_claims = [item for item in sources if item.get("requirement_name") == "vessel_flow_and_AIS_behaviour"][:2]
    return f"""# Political Risk Brief
## Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs

| Field | Value |
| --- | --- |
| Generated date | {generated_at} |
| Risk issue | {topic} |
| Business lens | UK shipping operator route decision across transit, delay, reroute and legal hold |
| Region | {region} |
| Time horizon | {time_horizon} |
| Overall risk level | Severe |
| Confidence | 4/5 |
| Evidence mode | {_evidence_status(evidence_pack)} |

## 1. Decision Recommendation

{_table(
    ["Item", "Assessment"],
    [
        ("Preferred option", "Legal hold if any sanctions/payment trigger is present; otherwise delay or reroute until insurance, AIS/vessel-flow and official guidance conditions support conditional transit."),
        ("Current stance", "Transit only after sanctions, insurance and operations clearance"),
        ("Primary blocker", "Safe-passage/toll demand, insurance uncertainty, detention risk or AIS/vessel-flow disruption"),
        ("Legal hold trigger", "Any safe-passage payment, toll, guarantee, offset, swap, in-kind arrangement or indirect payment demand"),
        ("Reroute trigger", "Direct transit cost exceeds reroute cost after war-risk premium, or detention risk remains high"),
        ("Delay trigger", "Short-lived uncertainty and delay cost remains below reroute cost"),
        ("Conditional transit trigger", "Clean sanctions position, confirmed war-risk cover, acceptable official guidance and normalising vessel-flow/AIS signals"),
        ("Relaxation trigger", "Official guidance, insurance appetite and vessel-flow/AIS recovery align"),
    ],
)}

## Dashboard Summary

{_table(
    ["Item", "Value"],
    [
        ("Decision engine", "Transit / delay / reroute / legal hold"),
        ("Current stance", "Transit only after sanctions, insurance and operations clearance"),
        ("Primary legal trigger", "Any safe-passage/toll/payment-equivalent demand"),
        ("Primary commercial trigger", "War-risk premium or detention risk makes direct transit weaker than delay/reroute"),
        ("Evidence mode", _evidence_status(evidence_pack)),
        ("Source provider", (evidence_pack or {}).get("source_provider", "")),
        ("Key data limits", "Route-cost assumptions are illustrative and require operator validation"),
    ],
)}

## 2. Scope and Specificity

This brief is a route-decision product for a shipping operator choosing between direct transit, delay / wait, reroute or legal hold for a Gulf-linked voyage. It is not a blanket warning to avoid Hormuz; it is a structured comparison of route options once sanctions, insurance, AIS/vessel-flow and detention risks are included.

## 3. Executive Judgement

Direct transit may be cheaper on voyage days alone, but it becomes commercially or legally unacceptable where sanctions-linked payment demands, war-risk pricing, AIS disruption, detention risk or unstable vessel-flow conditions are present. The current stance is not a blanket avoidance recommendation: it is a trigger-based decision framework. Legal hold applies where a sanctions/payment trigger exists; otherwise delay or reroute remains preferred until insurance, official guidance and vessel-flow signals support conditional transit.

## 4. Route Decision Optimiser

{_table(
    ["Option", "Estimated cost", "Legal/sanctions risk", "Insurance risk", "Operational risk", "Decision"],
    [
        (
            row["option"],
            f"${row['estimated_cost']:,.0f}" if row["estimated_cost"] else "Hold pending clearance",
            row["legal_sanctions_risk"],
            row["insurance_risk"],
            row["operational_risk"],
            _hormuz_option_decision_label(row["option"], row["decision"], engine["preferred_option"]),
        )
        for row in engine["option_ranking"]
    ],
)}

## 5. Illustrative Route-Cost Scenario

The values below are illustrative scenario inputs used to show how the decision engine compares direct transit, delay and reroute options. They are not company-specific figures. A shipping operator would replace these inputs with vessel value, charter rate, bunker cost, insurance quote, demurrage exposure and voyage plan data before using the model commercially.

{_table(
    ["Input", "Value", "Basis", "Use in model", "Replace with"],
    [
        ("Vessel value", "$100m", "Illustrative tanker scenario", "Calculates war-risk premium cost", "Insured vessel value / market value"),
        ("War-risk premium", "2.0%", "Manual stress-case input informed by reported premium pressure", "Tests whether direct transit becomes uneconomic", "Broker quote / underwriter indication"),
        ("Base direct voyage cost", "$1.02m", "Illustrative voyage-cost input", "Baseline direct transit cost before risk premium", "Charter hire, fuel, port, cargo and operating cost data"),
        ("Delay period", "5 days", "Illustrative waiting scenario", "Tests short delay versus reroute", "Voyage plan and security guidance"),
        ("Delay cost per day", "$108k", "Illustrative delay/demurrage input", "Calculates cost of waiting", "Charterparty/demurrage/vessel cost"),
        ("Reroute extra days", "10 days", "Illustrative rerouting scenario", "Tests longer route cost", "Actual routing estimate"),
        ("Reroute cost per day", "$73k", "Illustrative incremental operating cost", "Calculates reroute cost", "Fuel, hire, port and schedule data"),
        ("Compliance hold days", "5 days", "Operator-required input", "Shows data needed for legal hold costing", "Internal legal/compliance review timing"),
    ],
)}

### Assumption Confidence

{_table(
    ["Input type", "Confidence", "Reason"],
    [
        ("Legal trigger logic", "High", "Based on sanctions/payment-risk source evidence"),
        ("War-risk premium direction", "Medium-high", "Source evidence supports premium pressure, exact quote needs broker validation"),
        ("Route-cost scenario", "Medium", "Useful for comparison, needs operator-specific data"),
        ("Final voyage recommendation", "Medium", "Requires vessel, cargo, insurance and charterparty data"),
    ],
)}

## 6. Sanctions Red-Flag Assessment

{_table(
    ["Trigger", "Decision effect", "Why it matters"],
    [
        ("safe-passage payment", "legal hold / compliance escalation", "A payment framed as passage clearance can create sanctions exposure that overrides commercial convenience."),
        ("toll demand", "legal hold / compliance escalation", "A toll or fee linked to passage may amount to a prohibited or escalation-triggering transfer."),
        ("guarantee", "legal hold / compliance escalation", "Guarantees can replicate the economic effect of a direct payment."),
        ("offset", "legal hold / compliance escalation", "Offsets may disguise value transfer to a restricted counterparty or coordination chain."),
        ("swap", "legal hold / compliance escalation", "Swap structures can create indirect payment exposure even if no cash toll is paid."),
        ("in-kind arrangement", "legal hold / compliance escalation", "In-kind consideration can still satisfy a demanded benefit and trigger review."),
        ("indirect payment", "legal hold / compliance escalation", "Routing payment through an intermediary does not remove legal or compliance risk."),
        ("Iranian coordination requirement", "legal hold / compliance escalation", "Coordination demands may indicate a state-linked control structure requiring legal review."),
        ("unclear counterparty/payment instruction", "legal hold / compliance escalation", "Ambiguous instructions make it unsafe to assume the transaction is commercially routine."),
    ],
)}

{_format_bullets([item.get("claim_supported", "") for item in sanctions_claims if item.get("claim_supported")])}

## 7. Insurance Break-Even Analysis

{_table(
    ["Input / Output", "Value", "Note"],
    [
        ("war-risk cost", f"${engine['insurance_break_even']['war_risk_cost']:,.0f}", "Illustrative premium cost based on vessel value and manual premium assumption."),
        ("direct total cost", f"${engine['insurance_break_even']['direct_total_cost']:,.0f}", "Illustrative direct-transit cost once war-risk premium is added."),
        ("delay total cost", f"${engine['insurance_break_even']['delay_total_cost']:,.0f}", "Illustrative direct cost plus premium plus delay cost."),
        ("reroute total cost", f"${engine['insurance_break_even']['reroute_total_cost']:,.0f}", "Illustrative reroute cost without a direct-transit premium assumption."),
        ("break-even war-risk premium against reroute", f"{engine['insurance_break_even']['premium_pct_break_even_vs_reroute'] * 100:.2f}%", "Above this premium, reroute is cheaper than direct transit."),
        ("break-even war-risk premium against delay", f"{engine['insurance_break_even']['premium_pct_break_even_vs_delay'] * 100:.2f}%", "Above this premium, waiting is cheaper than direct transit."),
        ("commercial interpretation", "Illustrative direct transit is commercially weaker than reroute once premium pressure and detention stress are high.", "Use operator-specific costs before treating this as a voyage-specific recommendation."),
    ],
)}

## 8. AIS and Vessel-Flow Signals

{_table(
    ["Signal", "Current evidence", "Decision use", "Refresh trigger"],
    [
        ("AIS/transponder disruption", "AIS disruption remains a live compliance and routing red flag rather than a closed issue.", "Requires compliance review before any conditional transit decision.", "Refresh if routing instructions or AIS suppression reports change."),
        ("traffic disruption", "Selected live reporting still points to disrupted or only partially recovered passage conditions.", "Supports continued control posture rather than routine transit.", "Refresh if vessel-flow signals materially recover."),
        ("stranded vessel/seafarer signal", "Official security reporting referenced significant vessel and seafarer disruption during the stress phase.", "Supports a cautious stance on detention and crew-safety exposure.", "Refresh if official incident reporting improves or worsens."),
        ("official/security guidance", "Current operating posture still depends on live official guidance rather than a generic reopening narrative.", "Sets the threshold for whether transit can move from restricted to conditional.", "Refresh before voyage approval if guidance changes."),
        ("vessel-flow recovery", "Recovery evidence is partial and should not be treated as normalisation on its own.", "Defines whether controls can relax from hold/reroute to conditional transit.", "Refresh before relaxing controls."),
    ],
)}

{_format_bullets([item.get("claim_supported", "") for item in flow_claims if item.get("claim_supported")])}

## 9. Risk Scorecard

{_risk_scorecard(scores)}

## 10. Evidence-To-Score Bridge

{_evidence_to_score_bridge(evidence_pack, scores)}

## 11. Source Requirement Coverage

{_source_requirement_coverage(evidence_pack)}

## 12. Recommended Operator Actions

1. Voyage approval: require operations, insurance and sanctions review before Hormuz transit.
2. Sanctions escalation: treat any toll, safe-passage payment, offset, swap, guarantee or informal payment demand as legal escalation.
3. Insurance check: confirm war-risk cover, cancellation clauses, additional premium and exclusions before sailing.
4. AIS/compliance check: review transponder behaviour, vessel routing and counterparty instructions.
5. Route-cost comparison: compare direct, delay and reroute options using fuel, war-risk premium, charter delay and demurrage.
6. Client communication: explain whether route decisions are driven by safety, sanctions, insurance or cost.
7. Relaxation test: relax controls only after official guidance, insurer appetite and vessel-flow recovery align.

## 13. Relaxation and Escalation Triggers

**Relaxation triggers**

{_format_bullets(engine["relaxation_triggers"])}

**Escalation triggers**

{_format_bullets(engine["escalation_triggers"])}

## 14. Evidence Appendix

{_evidence_appendix(sources, domain="maritime_trade")}

## 15. Source Audit Summary

{_source_audit_summary(evidence_pack)}

### Source Register

{_source_register(evidence_pack)}

## 16. Methodology and Review Controls

{_methodology(evidence_pack)}

### Source Strategy

{_source_strategy(evidence_pack)}

### Source Requirements

{_source_requirements(evidence_pack)}

### Review Flags

{_format_bullets(review_flags)}

### Review Controls

{_review_controls(evidence_pack)}
"""


def _generate_uk_ets_shipping_operator_brief(topic, business_user, region, time_horizon, sources, evidence_pack, scores, review_flags, generated_at):
    carbon_cost = calculate_carbon_cost(
        vessel_name="Illustrative Ro-Ro ferry",
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
    return f"""# Political Risk Brief
## UK ETS Maritime Expansion: Carbon Cost Exposure

| Field | Value |
| --- | --- |
| Generated date | {generated_at} |
| Risk issue | {topic} |
| Business lens | UK shipowner/operator carbon cost exposure, reporting readiness and route economics |
| Region | {region} |
| Time horizon | {time_horizon} |
| Overall risk level | Medium-High |
| Confidence | 4/5 |
| Evidence mode | {_evidence_status(evidence_pack)} |

## 1. Operator Stance

{_table(
    ["Item", "Assessment"],
    [
        ("Current stance", "Treat domestic UK voyages by vessels 5,000 GT and above as in-scope from July 2026, with carbon cost now part of voyage economics"),
        ("Risk level", "Medium-High"),
        ("Confidence", "4/5"),
        ("Primary risk", "Carbon allowance cost, reporting readiness and margin pressure on in-scope domestic routes"),
        ("Action bias", "Quantify route-level exposure, prepare reporting process and test cost pass-through options"),
        ("Escalation trigger", "UKA price increase, route falls clearly within scope, reporting gap, allowance procurement risk"),
        ("Scenario trigger", "International voyages become part of future UK ETS expansion"),
    ],
)}

## 2. Applicability Check

{_table(
    ["Factor", "Assessment", "Evidence basis"],
    [
        ("Vessel threshold", "5,000 GT and above", "Confirmed first-stage threshold in GOV.UK authority response and implementation guidance."),
        ("Route type", "domestic / international / scenario", "Domestic UK and at-berth emissions are confirmed; international routes remain future/scenario unless later confirmed."),
        ("Emissions covered", "domestic voyage and at-berth emissions", "Current confirmed scope is domestic UK voyages and emissions while at anchor or moored."),
        ("Reporting obligation", "verified annual emissions report", "Verified annual emissions reporting remains required in the compliance cycle."),
        ("Surrender obligation", "allowance surrender deadline", "Allowances are surrendered after reporting, with transitional double-surrender treatment for the first maritime years."),
        ("Caveat", "international routes should be modelled as future scenario unless confirmed", "Future expansion consultation exists, but this brief does not treat UK-international routes as current scope."),
    ],
)}

## 3. Executive Judgement

UK ETS maritime expansion creates a near-term compliance and margin risk for UK shipping operators with in-scope domestic voyages. The rule is confirmed for domestic maritime emissions from vessels of 5,000 GT and above from 1 July 2026, making carbon cost a route-level operating input rather than a long-term policy abstraction.

For the illustrative Liverpool-Belfast Ro-Ro profile, the model estimates a carbon allowance cost of 2,770 per voyage and approximately 866,562 annualised, based on stated fuel, emissions factor and UKA price assumptions. These figures should be treated as decision-support estimates, not final compliance values, until operator-specific fuel burn, verifier methodology and current UKA pricing are confirmed.

## 4. Carbon Cost Estimate

### A. Source-confirmed policy inputs

{_table(
    ["Input", "Value", "Evidence basis"],
    [
        ("vessel threshold", "5,000 GT and above", "Confirmed first-stage policy scope."),
        ("route scope", "Domestic UK voyages and at-berth emissions", "Confirmed July 2026 policy scope."),
        ("start date", "1 July 2026", "Official implementation date."),
        ("coverage rate", "100% for the illustrative domestic route", "Applied because the route is treated as confirmed domestic scope."),
        ("reporting / surrender timeline", carbon_cost["compliance_timeline"], "Implementation guidance and LR summary."),
    ],
)}

### B. Operator / illustrative assumptions

{_table(
    ["Assumption", "Value", "Note"],
    [
        ("route", "Liverpool to Belfast", "Illustrative route requiring operator validation."),
        ("vessel type", "Ro-Ro ferry", "Illustrative vessel profile."),
        ("fuel type", "MGO", "Illustrative operating assumption."),
        ("fuel consumption per voyage", "18 tonnes", "Illustrative fuel-burn assumption requiring operator validation."),
        ("voyages per week", "6", "Illustrative service frequency."),
    ],
)}

### C. Market/manual inputs

{_table(
    ["Input", "Value", "Note"],
    [
        ("UKA price", "48 per tonne", "Manual fallback value used because no embedded live UKA price feed is available in the calculator."),
        ("price source", "Manual fallback input", "Refresh against live market evidence before final decisions."),
        ("live or manual", "Manual fallback", "Confidence is capped below 5 because live pricing is not embedded."),
    ],
)}

### D. Derived outputs

{_table(
    ["Output", "Value", "Note"],
    [
        ("estimated tCO2e per voyage", f"{carbon_cost['estimated_tco2e_per_voyage']}", "Fuel burn multiplied by emissions factor."),
        ("cost per voyage", f"{carbon_cost['estimated_carbon_cost_per_voyage']}", "Illustrative voyage-level carbon allowance cost."),
        ("weekly cost", f"{carbon_cost['weekly_carbon_cost']}", "Based on six illustrative voyages per week."),
        ("monthly cost", f"{carbon_cost['monthly_carbon_cost']}", "4.345-week month approximation."),
        ("annualised cost", f"{carbon_cost['annualised_carbon_cost']}", "Illustrative annualised run rate."),
    ],
)}

{_table(
    ["Sensitivity", "UKA Price", "Estimated cost per voyage"],
    [(item["label"], item["uka_price_per_tonne"], item["estimated_cost_per_voyage"]) for item in carbon_cost["uka_price_sensitivity"]],
)}

## 5. Risk Scorecard

{_risk_scorecard(scores)}

## 6. Quantified Evidence Readout

{_quantified_evidence_readout(evidence_pack, business_user)}

## 7. Evidence-To-Score Bridge

{_evidence_to_score_bridge(evidence_pack, scores)}

## 8. Decision Implications

{_table(
    ["Decision area", "Current implication", "Required response"],
    [
        ("Route applicability", "Not every route is currently in scope.", "Separate confirmed domestic exposure from international scenario modelling."),
        ("Allowance cost", "Carbon cost becomes a recurring voyage input for in-scope routes.", "Model route-level margin effect and procurement timing."),
        ("Reporting readiness", "MRV and verified reporting are operational prerequisites.", "Check systems, accountable entity and verifier readiness."),
        ("Pass-through", "Operators may not fully recover carbon cost from customers.", "Test surcharge, contract and pricing options."),
        ("Future expansion", "International routes may be captured later.", "Maintain scenario models without treating them as current obligations."),
    ],
)}

## 9. Compliance Timeline

{carbon_cost['compliance_timeline']}

## 10. Scenario Analysis

{_table(
    ["Scenario", "Description", "Operator implication", "Trigger"],
    [
        ("Base case: domestic scope only", "Confirmed July 2026 domestic and at-berth exposure applies to covered ships and routes.", "Current cost and compliance planning required.", "Route is clearly domestic UK and vessel exceeds 5,000 GT."),
        ("Price stress case", "UKA price rises faster than expected while operators are still building pass-through mechanisms.", "Margin pressure intensifies and procurement timing matters more.", "Allowance market tightens or operator hedging is absent."),
        ("Future expansion case", "UK-international voyages are brought into scope by later policy.", "Broader route set requires scenario refresh and revised cost models.", "Future consultation response confirms international inclusion."),
    ],
)}

## 11. Cost Pass-Through Considerations

Carbon cost does not automatically become recoverable revenue. The practical question is whether contract terms, customer bargaining power and route competition allow a clean surcharge or whether the operator absorbs part of the allowance cost. This is where policy text turns into commercial pressure.

## 12. Recommended Actions

1. Confirm scope: classify routes into confirmed current scope, partial scope and scenario-only exposure.
2. Build the calculator into route economics: add carbon cost to voyage approval and route profitability checks.
3. Check accountability: confirm the responsible entity, reporting workflow, verifier process and registry/allowance preparation.
4. Test pass-through: review charterparty, freight and surcharge mechanics for recovering some or all carbon cost.
5. Monitor UKA price: refresh the cost model when allowance prices move materially.
6. Keep international routes separate: model them as future scenario exposure unless later evidence confirms current scope.

## 13. Watchlist

{_table(
    ["Indicator", "Why it matters", "Decision use"],
    [
        ("UKA price movement", "Directly changes route-level carbon cost.", "Refresh cost assumptions."),
        ("Route falls clearly within scope", "Converts scenario planning into current obligation.", "Move route into live cost model."),
        ("Reporting process gap", "Can create compliance failure despite known cost exposure.", "Escalate implementation readiness."),
        ("Allowance procurement risk", "Can create cash-flow and timing pressure.", "Prepare purchasing and treasury plan."),
        ("Future international expansion", "May broaden the route set materially.", "Update scenario models."),
    ],
)}

## 14. Source Requirement Coverage

{_source_requirement_coverage(evidence_pack)}

## 15. Evidence Appendix

{_evidence_appendix(sources)}

## 16. Source Audit Summary

{_source_audit_summary(evidence_pack)}

## 17. Methodology and Review Controls

{_methodology(evidence_pack)}

### Source Strategy

{_source_strategy(evidence_pack)}

### Source Requirements

{_source_requirements(evidence_pack)}

### Review Flags

{_format_bullets(review_flags)}

### Review Controls

{_review_controls(evidence_pack)}
"""


def _generate_sanctions_trade_finance_brief(topic, business_user, region, time_horizon, sources, evidence_pack, scores, review_flags, generated_at):
    return f"""# Political Risk Brief
## Sanctions End-Use Controls: Trade Finance Exposure

| Field | Value |
| --- | --- |
| Risk issue | {topic} |
| Business lens | Trade finance transaction approval, compliance escalation and facility controls |
| Region | {region} |
| Time horizon | {time_horizon} |
| Overall risk level | {_overall_rating(scores)} |
| Confidence | {scores["confidence"]["score"]}/5 |
| Evidence mode | {_evidence_status(evidence_pack)} |

## 1. Transaction Stance

{_sanctions_transaction_stance(scores)}

## 2. Executive Judgement

Sanctions end-use controls create a high trade finance risk because the lender's exposure can crystallise before shipment failure: during onboarding, document review, drawdown, payment execution or collateral enforcement. The core question is whether the financed goods, buyer, end user, intermediaries, route or payment chain create a sanctions end-use concern that requires escalation, licence confirmation or refusal.

For a trade finance lender, the practical stance should be enhanced due diligence over the next {time_horizon}. Transactions involving sensitive goods, third-country routing, unclear end users, opaque ownership or sanctions-linked jurisdictions should be held or escalated until the goods classification, end-use evidence, counterparty screening and payment route are clean.

Scope-limited evidence matters. Not every transaction is automatically prohibitive, but approval should depend on documented end use, screened counterparties, a confirmed licence position and a payment route that correspondent banks are likely to process.

## 3. Key Judgements

{_sanctions_key_judgements()}

## 4. Risk Scorecard

{_risk_scorecard(scores)}

## Quantified Evidence Readout

{_quantified_evidence_readout(evidence_pack, business_user)}

## Evidence-To-Score Bridge

{_evidence_to_score_bridge(evidence_pack, scores)}

## 5. Decision Implications

{_sanctions_decision_implications()}

## 6. Counterparty Exposure

{_sanctions_counterparty_exposure()}

## 7. Goods / End-Use Risk

{_sanctions_goods_risk()}

## 8. Payment and Documentation Risk

{_sanctions_payment_documentation_risk()}

## 9. Collateral / Cargo Risk

{_sanctions_collateral_risk()}

## 10. Compliance Escalation

{_sanctions_compliance_escalation()}

## 11. Scenario Outlook

{_sanctions_scenario_outlook()}

## 12. Recommended Actions

{_sanctions_recommended_actions()}

## 13. Watchlist / Early Warning Indicators

{_sanctions_watchlist()}

## 14. Source Requirement Coverage

{_source_requirement_coverage(evidence_pack)}

## 15. Evidence Appendix

{_evidence_appendix(sources)}

## 16. Source Audit Summary

{_source_audit_summary(evidence_pack)}

### Source Register

{_source_register(evidence_pack)}

## 17. Methodology and Review Controls

{_methodology(evidence_pack)}

### Source Requirements

{_source_requirements(evidence_pack)}

### Review Flags

{_format_bullets(review_flags)}

### Review Controls

{_review_controls(evidence_pack)}
"""


def _sanctions_transaction_stance(scores):
    return _table(
        ["Item", "Assessment"],
        [
            ("Current stance", "Enhanced due diligence and compliance escalation for transactions involving sensitive goods, third-country routing, unclear end-use or counterparties linked to sanctioned jurisdictions"),
            ("Risk level", "High"),
            ("Confidence", f"{scores['confidence']['score']}/5"),
            ("Primary risk", "Diversion of goods or technology to sanctioned destinations or sanctioned-connected persons, creating payment, documentation, collateral and regulatory exposure"),
            ("Action bias", "Hold or escalate transactions with incomplete end-use evidence, opaque counterparties, unusual routing or licence uncertainty"),
            ("Approval trigger", "Clear end-use evidence, screened counterparties, documented goods classification, confirmed licence position and clean payment route"),
            ("Hold / decline trigger", "Government notification, unresolved diversion indicators, sanctions-connected parties, weak documentation or payment-route concerns"),
        ],
    )


def _sanctions_key_judgements():
    rows = [
        ("Sanctions end-use controls create a clear transaction-screening risk for trade finance.", "Official sanctions guidance defines when end-use exposure can require notification, licensing or escalation.", "GOV.UK source; 13 May 2026 regulatory start date in source pack.", "Supports hold / escalate / decline controls before approval or drawdown."),
        ("Third-country diversion risk is central to the case.", "Sanctions regime and reputable reporting identify circumvention concerns involving routes, intermediaries and opaque end users.", "Named control point: third-country routing and restricted destination screening.", "Requires enhanced route, counterparty and end-use checks."),
        ("Counterparty and end-use opacity should drive escalation.", "Evidence links sanctions exposure to beneficial ownership, end user, goods and destination uncertainty.", "Transaction-control point: buyer, end user, intermediaries and beneficial owners.", "Incomplete end-use or ownership evidence should block routine approval."),
        ("Payment and correspondent banking risk can crystallise before shipment failure.", "Banking compliance evidence links sanctions screening to blocked or delayed payments and settlement risk.", "Control point: payment route and correspondent-bank confirmation before drawdown.", "Payment route and correspondent-bank exposure need pre-drawdown review."),
        ("Documentation quality is central to approve / hold / decline decisions.", "Official and legal sources emphasise goods scope, notification, licensing and supporting evidence.", "Documents: end-use statement, goods classification, licence position and payment instructions.", "End-use statements, contracts, invoices and shipping documents become decision evidence."),
        ("Legal analysis is useful, but official guidance should anchor the control framework.", "Law-firm analysis explains practice, while official guidance defines the regulatory basis.", "Source hierarchy: official guidance first, legal analysis for implementation.", "Use legal analysis for implementation while official controls anchor the decision."),
        ("Scope-limited evidence matters because the rules may hinge on notification, goods scope and available documentation.", "Contrary or scope-limited sources show risk can be controllable where facts are clear.", "Approval trigger: documented goods scope, clean counterparties and confirmed licence position.", "Supports approval after enhanced due diligence where red flags are resolved."),
    ]
    return _table(["Judgement", "Evidence basis", "Concrete signal", "Client relevance"], rows)


def _sanctions_decision_implications():
    rows = [
        ("Approve / hold / decline", "Routine approval is inappropriate where end-use, route or counterparty facts are incomplete.", "Hold or escalate until licence, goods scope, counterparties and payment route are clear."),
        ("Counterparty screening", "Beneficial ownership, intermediaries and end users can create sanctions exposure.", "Screen buyers, end users, owners, freight parties and payment counterparties."),
        ("End-use documentation", "End-use evidence determines whether the risk is controllable.", "Require end-use statements, contractual restrictions and supporting documents."),
        ("Goods classification", "Sensitive or dual-use goods raise diversion and licensing risk.", "Confirm commodity code, controls status and sanctions sensitivity."),
        ("Payment route", "Correspondent banks may reject or delay exposed payments.", "Check currency, correspondent route, beneficiary bank and blocked-payment risk."),
        ("Collateral control", "Collateral may be impaired if cargo is detained, diverted or legally restricted.", "Tie drawdown and collateral release to clean documents and route evidence."),
        ("Licence position", "Notification or licence uncertainty can prevent settlement.", "Confirm whether notification, licensing or legal sign-off is required."),
        ("Compliance escalation", "Unresolved red flags create regulatory penalty exposure.", "Escalate to sanctions/export-control specialists before commitment."),
        ("Client communication", "Clients need clear evidence requests and decision triggers.", "Communicate hold conditions, approval evidence and decline triggers early."),
    ]
    return _table(["Decision area", "Current implication", "Required response"], rows)


def _sanctions_counterparty_exposure():
    return "Counterparty risk should be assessed across buyer, seller, end user, beneficial owners, intermediaries, freight parties, banks and payment beneficiaries. Any sanctions-connected party, opaque ownership chain or unexplained intermediary should trigger enhanced due diligence and compliance escalation."


def _sanctions_goods_risk():
    return "Goods and technology should be classified before financing. Sensitive, dual-use, strategically controlled or diversion-prone goods require stronger end-use evidence, contractual restrictions and specialist export-control review before approval."


def _sanctions_payment_documentation_risk():
    return "Payment risk can arise from sanctions screening, correspondent-bank appetite, currency routing, beneficiary-bank exposure or inconsistent trade documents. Documentation should reconcile goods, route, buyer, end user, shipping parties, licence position and payment instructions."


def _sanctions_collateral_risk():
    return "Collateral value may be impaired if cargo is detained, diverted, rejected by banks, blocked by licence uncertainty or exposed to sanctions restrictions. Facility controls should link drawdown and release to clean documents and verified route/end-use evidence."


def _sanctions_compliance_escalation():
    return "Escalate transactions where there is a government notification, unclear licence position, sanctioned-party link, third-country diversion indicator, sensitive goods profile, opaque end user, inconsistent documents or payment-route concern. Approval should require documented resolution of the specific red flag."


def _sanctions_scenario_outlook():
    rows = [
        ("Base case: enhanced due diligence", "Transactions continue, but sensitive goods, routes and counterparties require stronger evidence.", "New guidance, notification trigger or bank rejection.", "Clean end-use pack, screened parties and confirmed payment route.", "Hold/escalate higher-risk transactions before drawdown."),
        ("Downside case: enforcement or circumvention finding", "Regulators or banks identify sanctions evasion patterns linked to goods, routes or counterparties.", "New designations, enforcement action or correspondent-bank refusal.", "No sanctions link and legal sign-off confirms controllable exposure.", "Decline or suspend transactions with unresolved red flags."),
        ("Scope-limited approval case", "Controls apply narrowly or documentation resolves end-use concerns.", "New facts connect the deal to sanctioned parties or restricted end use.", "Documented goods scope, licence position and clean counterparties.", "Approve with covenants, documentary controls and monitoring."),
    ]
    return _table(["Scenario", "Description", "Escalation trigger", "Approval trigger", "Trade finance implication"], rows)


def _sanctions_recommended_actions():
    return "\n".join(
        [
            "1. Transaction screen: identify goods, technology, buyer, end user, intermediaries, routing and destination.",
            "2. End-use evidence: obtain end-use statements, contractual restrictions and supporting documents.",
            "3. Counterparty review: screen beneficial owners, intermediaries, freight parties and payment counterparties.",
            "4. Goods classification: confirm whether goods are strategically controlled, dual-use, sanctioned or diversion-prone.",
            "5. Licence position: confirm whether a notification, licensing requirement or legal escalation applies.",
            "6. Payment controls: check correspondent bank exposure, currency route and blocked-payment risk.",
            "7. Facility controls: add conditions precedent, drawdown restrictions or documentary covenants where needed.",
            "8. Escalation trigger: hold or decline where end-use, ownership, routing or payment risk remains unresolved.",
        ]
    )


def _sanctions_watchlist():
    rows = [
        ("Official sanctions guidance updates", "Can change notification, licensing or transaction escalation triggers.", "Official primary"),
        ("New designations or regime amendments", "Can convert a live transaction into a blocked or prohibited exposure.", "Official sanctions sources"),
        ("Third-country diversion reporting", "Signals routes, intermediaries or goods profiles requiring enhanced checks.", "Reputable news / official advisories"),
        ("Goods classification changes", "Affects whether the financed goods are controlled or diversion-prone.", "Trade tariff / export-control sources"),
        ("Correspondent-bank refusals", "Shows payment route and settlement risk before shipment failure.", "Banking compliance evidence"),
        ("Licence delays or refusals", "Affects drawdown, shipment timing and repayment risk.", "Official/legal analysis"),
        ("Document inconsistencies", "Can indicate end-use opacity or diversion risk.", "Transaction documents"),
    ]
    return _table(["Indicator", "Why it matters", "Source type to monitor"], rows)


def _generate_generic_brief(topic, business_user, region, time_horizon, sources, evidence_pack, scores, review_flags, generated_at):
    exposure_map = get_exposure_map(business_user)
    return f"""# Marine & Trade Risk Brief
## {topic} — {business_user.replace("_", " ")} exposure

| Field | Value |
| --- | --- |
| Generated date | {generated_at} |
| Business user | `{business_user}` |
| Region | {region} |
| Time horizon | {time_horizon} |
| Overall risk rating | {_overall_rating(scores)} |
| Confidence score | {scores["confidence"]["score"]}/5 |
| Evidence status | {_evidence_status(evidence_pack)} |

## Executive Judgement

{topic} presents a commercial risk over {time_horizon}. The priority for `{business_user}` is to identify exposed contracts, counterparties, assets and timelines, then adjust controls where the evidence supports a material disruption pathway.

## Key Risks

{_format_bullets(_generic_key_risks(topic))}

## Exposure Map

{_format_bullets(exposure_map)}

## Risk Scorecard

{_risk_scorecard(scores)}

## Evidence Appendix

{_evidence_appendix(sources)}

## Review Controls

{_format_bullets(review_flags)}

{_review_controls(evidence_pack)}
"""


def _generic_key_risks(topic):
    return [
        f"Commercial disruption linked to {topic}.",
        "Potential cost, timing, contractual or counterparty effects.",
        "Need for source verification and human review before decisions.",
    ]


def save_brief(markdown, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    title_line = markdown.splitlines()[1].replace("## ", "")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}-{_slugify(title_line)}.md"
    output_path = output_dir / filename
    output_path.write_text(markdown, encoding="utf-8")
    return output_path
