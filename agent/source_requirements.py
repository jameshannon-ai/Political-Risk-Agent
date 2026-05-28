def generate_source_requirements(topic, business_user, region, time_horizon, concerns, domain_pack=None):
    if _is_uk_ets_shipping_operator(topic, business_user, domain_pack):
        return _uk_ets_shipping_operator_requirements()
    if "hormuz" in topic.lower() and business_user == "shipping_operator":
        return _hormuz_shipping_operator_requirements()
    if "hormuz" in topic.lower() and business_user == "marine_insurer":
        return _hormuz_marine_insurer_requirements()
    if _is_sanctions_trade_finance(topic, business_user, domain_pack):
        return _sanctions_trade_finance_requirements()

    domain_pack = domain_pack or {}
    categories = domain_pack.get("source_requirements") or domain_pack.get("default_source_categories") or ["official_primary", "reputable_news", "specialist_analysis"]
    requirements = []
    for index, category in enumerate(categories, start=1):
        requirements.append(
            {
                "requirement_id": f"REQ-{index:03d}",
                "requirement_name": category,
                "why_required": f"Provides evidence for {category.replace('_', ' ')} linked to {topic}.",
                "preferred_source_types": [category],
                "preferred_domains": [],
                "minimum_sources": 1,
                "decision_questions_supported": [
                    f"How does {topic} affect {business_user} exposure in {region}?",
                ],
                "freshness_expectation": f"Relevant to {time_horizon}",
                "strength_threshold": "medium",
            }
        )
    return requirements


def _is_sanctions_trade_finance(topic, business_user, domain_pack):
    return (
        business_user == "trade_finance_lender"
        and ("sanctions" in topic.lower() or (domain_pack or {}).get("domain") == "sanctions_trade_finance")
    )


def _is_uk_ets_shipping_operator(topic, business_user, domain_pack):
    return (
        business_user == "shipping_operator"
        and (
            "uk ets" in topic.lower()
            or "maritime expansion" in topic.lower()
            or (domain_pack or {}).get("domain") == "regulatory_carbon_shipping"
        )
    )


def _sanctions_trade_finance_requirements():
    return [
        {
            "requirement_id": "REQ-STF-A",
            "requirement_name": "official_sanctions_guidance",
            "why_required": "Defines the legal and regulatory basis for sanctions end-use controls, including when exporters or counterparties may need a licence or compliance escalation.",
            "preferred_source_types": ["official_primary", "official_guidance"],
            "preferred_domains": ["gov.uk", "ofsi.gov.uk", "businessandtrade.gov.uk"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Does the transaction create sanctions end-use exposure?",
                "Has a government notification or licensing trigger been identified?",
                "Does the lender need to hold, escalate or decline the transaction?",
            ],
            "freshness_expectation": "Current official guidance, preferably checked within 30 days before transaction approval.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-STF-B",
            "requirement_name": "sanctions_regime_context",
            "why_required": "Shows how end-use controls sit inside wider UK sanctions regimes, especially Russia-related trade restrictions and circumvention controls.",
            "preferred_source_types": ["official_primary", "official_guidance"],
            "preferred_domains": ["gov.uk", "legislation.gov.uk", "ofsi.gov.uk"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Is the transaction connected to a sanctioned destination, person or restricted trade route?",
                "Does the transaction raise Russia or sanctioned-territory diversion risk?",
            ],
            "freshness_expectation": "Current sanctions regime guidance, preferably checked within 30 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-STF-C",
            "requirement_name": "export_control_and_dual_use_risk",
            "why_required": "Identifies whether goods or technology may be sensitive, dual-use, strategically controlled or vulnerable to diversion.",
            "preferred_source_types": ["official_primary", "official_guidance"],
            "preferred_domains": ["gov.uk", "great.gov.uk", "legislation.gov.uk"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Are the goods or technology sensitive enough to require enhanced due diligence?",
                "Does the lender need specialist export-control review before financing?",
            ],
            "freshness_expectation": "Current official goods classification or export-control evidence.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-STF-D",
            "requirement_name": "legal_practical_analysis",
            "why_required": "Explains how the rules operate in practice, including timing, notification, licensing, due diligence and business obligations.",
            "preferred_source_types": ["specialist_analysis"],
            "preferred_domains": ["skadden.com", "akingump.com", "bakermckenzie.com", "eversheds-sutherland.com", "ashurst.com", "osborneclarke.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "What practical checks should the lender require?",
                "Which transaction features should trigger legal/compliance escalation?",
            ],
            "freshness_expectation": "Recent legal or compliance analysis, preferably within 90 days.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-STF-E",
            "requirement_name": "trade_route_and_diversion_risk",
            "why_required": "Identifies third-country diversion patterns, suspicious routing, end-use opacity and circumvention indicators.",
            "preferred_source_types": ["reputable_news", "official_primary", "specialist_analysis"],
            "preferred_domains": ["reuters.com", "ft.com", "theguardian.com", "gov.uk", "sanctions-related official advisories"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Does the transaction involve a route, counterparty or goods profile associated with diversion?",
                "Should the lender require enhanced end-use documentation?",
            ],
            "freshness_expectation": "Recent diversion typology or sanctions evasion reporting, preferably within 90 days.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-STF-F",
            "requirement_name": "banking_and_payment_risk",
            "why_required": "Links sanctions exposure to payment execution, correspondent banking, blocked payment risk, facility drawdown and transaction settlement.",
            "preferred_source_types": ["specialist_analysis", "official_primary", "reputable_news"],
            "preferred_domains": ["wolfsberg-principles.com", "fatf-gafi.org", "ofsi.gov.uk", "reuters.com", "legal/compliance analysis sources"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Could payment be delayed, blocked or rejected?",
                "Should the lender require sanctions screening, correspondent-bank confirmation or facility conditions?",
            ],
            "freshness_expectation": "Current banking compliance guidance or payment-risk evidence.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-STF-G",
            "requirement_name": "contrary_or_scope_limited_evidence",
            "why_required": "Prevents over-escalation by identifying where controls apply only after a notification, where goods are outside scope, or where documentation mitigates risk.",
            "preferred_source_types": ["contrary_or_stabilising_evidence", "official_primary", "specialist_analysis"],
            "preferred_domains": ["gov.uk", "legal analysis sources", "official guidance"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "What evidence would justify approval after enhanced due diligence?",
                "Is the risk specific and controllable rather than automatically prohibitive?",
            ],
            "freshness_expectation": "Current official or legal scope analysis.",
            "strength_threshold": "medium",
        },
    ]


def _hormuz_marine_insurer_requirements():
    return [
        {
            "requirement_id": "REQ-A",
            "requirement_name": "official_maritime_security",
            "why_required": "Establishes whether the security environment justifies enhanced route controls, voyage approval thresholds and hull war caution.",
            "preferred_source_types": ["official_primary", "official_guidance"],
            "preferred_domains": ["ukmto.org", "imo.org", "bimco.org", "ics-shipping.org", "ocimf.org"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Should Gulf/Hormuz transits remain subject to enhanced referral?",
                "Is this a live vessel security risk or mainly a market-pricing risk?",
            ],
            "freshness_expectation": "Current or recent official maritime/security guidance, preferably within 90 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-B",
            "requirement_name": "carrier_operational_behaviour",
            "why_required": "Shows whether operators are treating the risk as a practical routing, service continuity or port-call constraint.",
            "preferred_source_types": ["company_update", "reputable_news"],
            "preferred_domains": ["maersk.com", "hapag-lloyd.com", "cma-cgm.com", "msc.com", "lloydslist.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Are carriers still willing to transit or serve Gulf ports?",
                "Are service changes creating trapped vessel, delay or deviation exposure?",
            ],
            "freshness_expectation": "Current carrier or operational reporting, preferably within 60 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-C",
            "requirement_name": "energy_chokepoint_exposure",
            "why_required": "Quantifies structural exposure to oil, LNG, tanker movements and systemic commercial impact.",
            "preferred_source_types": ["energy_chokepoint_data", "specialist_analysis"],
            "preferred_domains": ["eia.gov", "iea.org", "spglobal.com", "energyintel.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Should impact be treated as severe even without full closure?",
                "Which cargo and tanker exposures create accumulation risk?",
            ],
            "freshness_expectation": "Recent structural data or annually maintained chokepoint data.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-D",
            "requirement_name": "insurance_pricing_reinsurance",
            "why_required": "Tests whether market pricing, war-risk premiums or reinsurance appetite have already moved.",
            "preferred_source_types": ["insurance_market_evidence", "reputable_news"],
            "preferred_domains": ["howdenre.com", "marsh.com", "ajg.com", "wtwco.com", "lmalloyds.com", "reuters.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Is premium adequacy under pressure?",
                "Do referral thresholds, deductibles, limits or reinsurance appetite need review?",
            ],
            "freshness_expectation": "Current market pricing evidence, preferably within 30-60 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-E",
            "requirement_name": "vessel_flow_freight_market",
            "why_required": "Shows whether actual vessel behaviour confirms disruption, normalisation or trapped exposure.",
            "preferred_source_types": ["vessel_flow_or_freight_market_evidence", "specialist_analysis", "reputable_news"],
            "preferred_domains": ["kpler.com", "vortexa.com", "gibsons.co.uk", "lloydslist.com", "tradewindsnews.com", "reuters.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Are flows recovering or still abnormal?",
                "Is there evidence of floating cargo, congestion or delayed transit?",
            ],
            "freshness_expectation": "Recent vessel-flow or freight evidence, preferably within 30-60 days.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-F",
            "requirement_name": "sanctions_compliance",
            "why_required": "Identifies whether cargo, vessel ownership, counterparties or state controls create compliance and claims uncertainty.",
            "preferred_source_types": ["official_primary", "reputable_news", "specialist_analysis"],
            "preferred_domains": ["gov.uk", "treasury.gov", "ofac.treasury.gov", "europa.eu", "lmalloyds.com", "reuters.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Are sanctions exclusions, payment risk or counterparty controls relevant?",
                "Should unclear cargo or ownership structures be escalated?",
            ],
            "freshness_expectation": "Current sanctions or compliance evidence, preferably within 90 days.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-G",
            "requirement_name": "contrary_de_escalation",
            "why_required": "Prevents one-way escalation analysis by identifying reopening, diplomacy, stabilisation or normalisation signals.",
            "preferred_source_types": ["contrary_or_stabilising_evidence", "reputable_news", "official_primary"],
            "preferred_domains": ["reuters.com", "apnews.com", "ft.com", "official government sources"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "What evidence would justify relaxing controls?",
                "Are worst-case assumptions being overstated?",
            ],
            "freshness_expectation": "Current de-escalation or stabilisation reporting, preferably within 30 days.",
            "strength_threshold": "medium",
        },
    ]


def _hormuz_shipping_operator_requirements():
    return [
        {
            "requirement_id": "REQ-HSO-A",
            "requirement_name": "official_maritime_security",
            "why_required": "Establishes whether transit conditions create live security, detention, crew-safety or voyage-approval risk.",
            "preferred_source_types": ["official_primary", "official_guidance"],
            "preferred_domains": ["ukmto.org", "imo.org", "ics-shipping.org", "bimco.org", "intertanko.com", "ocimf.org"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Should the operator transit, delay, reroute or place the voyage on legal hold?",
            ],
            "freshness_expectation": "Current official maritime/security guidance, preferably checked within 30 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-HSO-B",
            "requirement_name": "transit_control_or_constabulary_actions",
            "why_required": "Captures Iranian transit-control mechanisms, vessel coordination requirements, detention risk, naval warnings or expanded control claims.",
            "preferred_source_types": ["reputable_news", "official_primary"],
            "preferred_domains": ["reuters.com", "apnews.com", "ukmto.org", "imo.org", "gov.uk"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Should the operator transit, delay, reroute or place the voyage on legal hold?",
                "Do AIS/vessel-flow indicators show route normalisation or continuing operating stress?",
            ],
            "freshness_expectation": "Current operational reporting and advisories, preferably within 30 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-HSO-C",
            "requirement_name": "sanctions_and_safe_passage_payment_risk",
            "why_required": "Identifies whether tolls, safe-passage payments, digital asset payments, offsets, swaps, guarantees or in-kind arrangements could create sanctions exposure.",
            "preferred_source_types": ["official_primary", "specialist_analysis", "reputable_news"],
            "preferred_domains": ["ofac.treasury.gov", "ofsi.gov.uk", "gov.uk", "reuters.com", "apnews.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Is there a sanctions red flag from tolls, safe-passage demands, offsets, swaps, guarantees, in-kind arrangements or Iranian coordination?",
            ],
            "freshness_expectation": "Current sanctions guidance or reporting, preferably within 30 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-HSO-D",
            "requirement_name": "war_risk_insurance_pricing",
            "why_required": "Measures how insurance repricing affects voyage economics and whether insurance cost changes route decisions.",
            "preferred_source_types": ["insurance_market_evidence", "reputable_news"],
            "preferred_domains": ["howdenre.com", "lmalloyds.com", "lloydslist.com", "reuters.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Is war-risk cover available and economically viable?",
            ],
            "freshness_expectation": "Current insurance-market evidence, preferably within 30 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-HSO-E",
            "requirement_name": "vessel_flow_and_AIS_behaviour",
            "why_required": "Shows whether actual vessel behaviour confirms constrained transit, AIS suppression, trapped vessels, traffic collapse or partial reopening.",
            "preferred_source_types": ["vessel_flow_or_freight_market_evidence", "reputable_news", "specialist_analysis"],
            "preferred_domains": ["reuters.com", "kpler.com", "vortexa.com", "lloydslist.com", "marinetraffic.com", "gibsons.co.uk", "apnews.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Do AIS/vessel-flow indicators show route normalisation or continuing operating stress?",
                "What evidence would justify relaxing controls?",
            ],
            "freshness_expectation": "Recent vessel-flow or AIS evidence, preferably within 30 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-HSO-F",
            "requirement_name": "energy_cargo_and_chokepoint_exposure",
            "why_required": "Quantifies why Hormuz disruption matters for oil, LNG, tanker cargoes and UK-linked energy/shipping exposure.",
            "preferred_source_types": ["energy_chokepoint_data", "specialist_analysis"],
            "preferred_domains": ["eia.gov", "iea.org", "unctad.org", "spglobal.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included?",
            ],
            "freshness_expectation": "Recent structural data or current maintained chokepoint data.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-HSO-G",
            "requirement_name": "route_cost_and_arbitrage_inputs",
            "why_required": "Supports comparison of transit, delay and rerouting options through fuel cost, voyage days, insurance premium, demurrage and charter exposure.",
            "preferred_source_types": ["insurance_market_evidence", "specialist_analysis", "reputable_news"],
            "preferred_domains": ["howdenre.com", "lloydslist.com", "spglobal.com", "reuters.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included?",
            ],
            "freshness_expectation": "Current market inputs plus operator assumptions validated for the voyage.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-HSO-H",
            "requirement_name": "contrary_or_de_escalation_evidence",
            "why_required": "Prevents one-way escalation analysis and defines conditions under which direct transit may become acceptable again.",
            "preferred_source_types": ["contrary_or_stabilising_evidence", "reputable_news", "official_primary"],
            "preferred_domains": ["reuters.com", "apnews.com", "gov.uk", "ukmto.org", "imo.org"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "What evidence would justify relaxing controls?",
            ],
            "freshness_expectation": "Current de-escalation reporting and vessel-flow evidence, preferably within 30 days.",
            "strength_threshold": "medium",
        },
    ]


def _uk_ets_shipping_operator_requirements():
    return [
        {
            "requirement_id": "REQ-UKETS-A",
            "requirement_name": "official_policy_scope",
            "why_required": "Confirms whether the rule applies to the vessel, voyage and emissions type.",
            "preferred_source_types": ["official_primary", "official_guidance"],
            "preferred_domains": ["gov.uk", "gov.scot", "gov.wales", "icapcarbonaction.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Does UK ETS apply to this vessel and route?",
                "Is the voyage domestic UK, at-berth, offshore or international?",
                "Is the route inside the confirmed 2026 scope or only a future scenario?",
            ],
            "freshness_expectation": "Current policy response or implementation guidance, preferably within 90 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-UKETS-B",
            "requirement_name": "reporting_surrender_timeline",
            "why_required": "Confirms MRV, reporting and allowance surrender deadlines.",
            "preferred_source_types": ["official_primary", "specialist_analysis"],
            "preferred_domains": ["gov.uk", "lr.org", "hfw.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "When must emissions be reported?",
                "When must allowances be surrendered?",
                "Is the first surrender affected by the double-surrender window?",
            ],
            "freshness_expectation": "Current implementation guidance, preferably within 90 days.",
            "strength_threshold": "high",
        },
        {
            "requirement_id": "REQ-UKETS-C",
            "requirement_name": "carbon_price_evidence",
            "why_required": "Provides the allowance price needed to calculate estimated carbon cost exposure.",
            "preferred_source_types": ["market_indicator", "reputable_news", "specialist_analysis"],
            "preferred_domains": ["theice.com", "market data sources", "lloydslist.com", "icapcarbonaction.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "What UKA price should be used?",
                "How sensitive is voyage cost to UKA price movement?",
            ],
            "freshness_expectation": "Current market or clearly labelled manual fallback price.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-UKETS-D",
            "requirement_name": "emissions_factor_evidence",
            "why_required": "Converts fuel consumption into estimated emissions.",
            "preferred_source_types": ["official_primary", "specialist_analysis"],
            "preferred_domains": ["imo.org", "gov.uk", "lr.org"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Which emissions factor should be used for the selected fuel?",
                "What is the estimated tCO2e per voyage?",
            ],
            "freshness_expectation": "Current or still-valid conversion-factor guidance.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-UKETS-E",
            "requirement_name": "operator_guidance",
            "why_required": "Shows how shipping operators and maritime advisers are interpreting and implementing the rule.",
            "preferred_source_types": ["company_update", "specialist_analysis", "reputable_news"],
            "preferred_domains": ["maersk.com", "lr.org", "lloydslist.com", "ukchamberofshipping.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "How are operators preparing?",
                "Are carbon costs being passed through to customers?",
                "Which operators or routes are most exposed?",
            ],
            "freshness_expectation": "Recent implementation commentary, preferably within 90 days.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-UKETS-F",
            "requirement_name": "legal_practical_analysis",
            "why_required": "Explains obligations, exemptions, uncertainty and compliance approach.",
            "preferred_source_types": ["specialist_analysis", "official_guidance"],
            "preferred_domains": ["hfw.com", "watsonfarley.com", "nortonrosefulbright.com", "stephensonharwood.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Which entity is responsible?",
                "What documentation or MRV process is needed?",
                "What uncertainties remain?",
            ],
            "freshness_expectation": "Current legal/compliance analysis, preferably within 180 days.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-UKETS-G",
            "requirement_name": "future_scope_or_international_extension",
            "why_required": "Captures the risk that future policy may expand to international voyages or wider emissions categories.",
            "preferred_source_types": ["official_primary", "specialist_analysis", "contrary_or_stabilising_evidence"],
            "preferred_domains": ["gov.uk", "icapcarbonaction.com", "icct.org"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Could future expansion affect UK-international routes?",
                "Which routes are confirmed in scope and which are scenario-only?",
            ],
            "freshness_expectation": "Current consultation or policy-expansion evidence, preferably within 180 days.",
            "strength_threshold": "medium",
        },
        {
            "requirement_id": "REQ-UKETS-H",
            "requirement_name": "contrary_or_scope_limited_evidence",
            "why_required": "Prevents over-application to routes, vessels or emissions outside scope.",
            "preferred_source_types": ["contrary_or_stabilising_evidence", "official_primary", "specialist_analysis"],
            "preferred_domains": ["gov.uk", "lr.org", "hfw.com", "icapcarbonaction.com"],
            "minimum_sources": 1,
            "decision_questions_supported": [
                "Is this route outside confirmed 2026 scope?",
                "Are there exemptions or delayed implementation issues?",
                "Should a route be treated as scenario exposure rather than current obligation?",
            ],
            "freshness_expectation": "Current scope-limiting guidance or implementation caveats.",
            "strength_threshold": "medium",
        },
    ]
