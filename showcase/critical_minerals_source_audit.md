# Source Audit

## Search Configuration

- Topic: Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers
- Business user: advanced_manufacturer
- Region: UK advanced manufacturer exposed to global rare earth magnet supply chains
- Time horizon: 1-6 months
- Concerns: production continuity under export-control disruption, rare earth magnet input dependency, supplier concentration, inventory runway versus qualification lag, stockpile versus alternative supplier qualification, technical substitution feasibility, allocation of scarce inventory, production hold threshold
- Search provider used: tavily
- Evidence mode: Live source retrieval
- Fallback data used: false
- Provider error: None
- Retrieval timestamp: 2026-06-01T20:22:32

## Research Plan

- Research objective: Build a governed evidence base for advanced_manufacturer decision-making on Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers in UK advanced manufacturer exposed to global rare earth magnet supply chains over 1-6 months, using the critical_minerals_supply_chain domain pack.
- Decision questions:
  - Can the manufacturer continue production with the current supplier base if export-control disruption intensifies?
  - Which exact input is controlled or concentration-exposed: finished magnet, oxide, alloy, sintered component or magnet-dependent subassembly?
  - How concentrated is supply for the relevant rare earth magnet input, and how much is China-linked?
  - Can the input be substituted, redesigned or qualified from another supplier within a commercially useful timeframe?
  - Do export-control direction, licensing friction and shortage signals justify stockpiling, allocation or accelerated qualification?
  - How long can production continue based on inventory runway versus alternative supplier qualification time?
  - What evidence would justify relaxing a high-control sourcing stance back to normal procurement?
- Required source mix:
  - official_anchor
  - data_or_indicator_source
  - specialist_interpretation
  - operator_or_industry_guidance
  - market_pricing
  - live_event_reporting
  - contrary_scope_limit
- Expected evidence types: official_primary, specialist_analysis, reputable_news, company_update, contrary_or_stabilising_evidence
- Minimum acceptable coverage: {'minimum_total_requirements': 9, 'minimum_high_priority_requirements': 6, 'high_priority_requirements': ['uk_critical_minerals_policy_and_manufacturing_resilience', 'export_control_direction_and_live_trigger', 'rare_earth_magnet_or_controlled_input_classification', 'supply_concentration_and_dependency_data', 'substitution_feasibility_and_alternative_supplier_qualification', 'company_data_requirements_and_anti_overclaiming_controls'], 'minimum_sources_per_requirement': {'REQ-CM-A': 1, 'REQ-CM-B': 1, 'REQ-CM-C': 1, 'REQ-CM-D': 1, 'REQ-CM-E': 1, 'REQ-CM-F': 1, 'REQ-CM-G': 1, 'REQ-CM-H': 1, 'REQ-CM-I': 1}}
- Refresh priorities:
  - uk_critical_minerals_policy_and_manufacturing_resilience: Current or maintained UK policy/resilience evidence.
  - export_control_direction_and_live_trigger: Current live reporting or official update, preferably within 30 days.
  - rare_earth_magnet_or_controlled_input_classification: Current or maintained classification evidence.
  - supply_concentration_and_dependency_data: Current or maintained dependency data.
  - uk_industry_exposure_and_advanced_manufacturing_relevance: Recent or maintained UK industry exposure evidence.
  - substitution_feasibility_and_alternative_supplier_qualification: Recent specialist or industry evidence.
  - market_pricing_or_shortage_signal: Current market or shortage signal, preferably within 30-60 days.
  - contrary_or_easing_evidence: Current easing or contrary evidence, preferably within 30 days.
  - company_data_requirements_and_anti_overclaiming_controls: Current or maintained control guidance.

## Source Strategy

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: uk_critical_minerals_policy_and_manufacturing_resilience
- Evidence question: Why is this a live UK manufacturing continuity issue rather than a generic global commodity story?
- Preferred domains: gov.uk, parliament.uk, bgs.ac.uk
- Preferred source types: official_primary
- Generated queries:
  - site:gov.uk UK critical minerals strategy vision 2035 rare earth magnets manufacturing
  - site:parliament.uk UK critical minerals manufacturing resilience rare earth magnets
  - site:gov.uk Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers uk critical minerals policy and manufacturing resilience 1-6 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained UK policy/resilience evidence.

### reputable_news

- Why it matters: Corroborates current events and commercial impacts.
- Source requirement: export_control_direction_and_live_trigger
- Evidence question: Is there a live export-control or geopolitical trigger that could disrupt access to rare earth magnets or critical-mineral inputs?
- Preferred domains: reuters.com, apnews.com, gov.uk, oecd.org
- Preferred source types: reputable_news, official_primary
- Generated queries:
  - site:reuters.com China rare earth magnet export controls licences Reuters
  - site:apnews.com rare earth export controls magnets licences AP
  - site:reuters.com Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers export control direction and live trigger 1-6 months
  - site:reuters.com Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers export control direction and live trigger
- Minimum acceptable evidence: 1
- Refresh expectation: Current live reporting or official update, preferably within 30 days.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: rare_earth_magnet_or_controlled_input_classification
- Evidence question: Which exact input is controlled or concentration-exposed: finished magnet, oxide, alloy, sintered component or magnet-dependent subassembly?
- Preferred domains: usgs.gov, iea.org, bgs.ac.uk
- Preferred source types: official_primary, specialist_analysis
- Generated queries:
  - site:usgs.gov rare earth permanent magnets supply chain NdFeB dysprosium terbium
  - site:iea.org rare earth permanent magnets supply chain manufacturing
  - site:usgs.gov Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers rare earth magnet or controlled input classification 1-6 months
  - Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers rare earth magnet or controlled input classification specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained classification evidence.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: supply_concentration_and_dependency_data
- Evidence question: How concentrated is supply for the relevant rare earth magnet input, and how much is China-linked?
- Preferred domains: oecd.org, usgs.gov, iea.org
- Preferred source types: official_primary, specialist_analysis
- Generated queries:
  - site:oecd.org export restrictions critical raw materials rare earth magnets China
  - site:usgs.gov rare earths production concentration China permanent magnets
  - site:oecd.org Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers supply concentration and dependency data 1-6 months
  - Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers supply concentration and dependency data specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained dependency data.

### company_update

- Why it matters: Shows operational decisions by carriers or market participants.
- Source requirement: uk_industry_exposure_and_advanced_manufacturing_relevance
- Evidence question: Why is this relevant to a UK advanced manufacturer rather than only to upstream miners or battery policy?
- Preferred domains: hvm.catapult.org.uk, bgs.ac.uk, parliament.uk, gov.uk
- Preferred source types: company_update, specialist_analysis, official_primary
- Generated queries:
  - site:hvm.catapult.org.uk rare earth magnets UK advanced manufacturing exposure
  - site:bgs.ac.uk rare earth magnets UK industry exposure
  - site:hvm.catapult.org.uk Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers uk industry exposure and advanced manufacturing relevance 1-6 months
  - Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers uk industry exposure and advanced manufacturing relevance specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Recent or maintained UK industry exposure evidence.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: substitution_feasibility_and_alternative_supplier_qualification
- Evidence question: Can the input be substituted, redesigned or qualified from another supplier within a commercially useful timeframe?
- Preferred domains: csis.org, rusi.org, css.ethz.ch, hvm.catapult.org.uk
- Preferred source types: specialist_analysis, company_update, reputable_news
- Generated queries:
  - site:csis.org rare earth magnet substitution qualification alternative suppliers
  - site:rusi.org rare earth magnets alternative supplier qualification manufacturing
  - site:csis.org Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers substitution feasibility and alternative supplier qualification 1-6 months
  - Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers substitution feasibility and alternative supplier qualification specialist analysis
  - Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers substitution feasibility and alternative supplier qualification Reuters
- Minimum acceptable evidence: 1
- Refresh expectation: Recent specialist or industry evidence.

### reputable_news

- Why it matters: Corroborates current events and commercial impacts.
- Source requirement: market_pricing_or_shortage_signal
- Evidence question: Do shortage or pricing signals justify stockpiling, allocation or accelerated qualification?
- Preferred domains: reuters.com, apnews.com, iea.org, usgs.gov
- Preferred source types: reputable_news, specialist_analysis
- Generated queries:
  - site:reuters.com rare earth magnet shortage prices manufacturing Reuters
  - site:reuters.com rare earth magnet users paying premium prices ex China supply Reuters
  - site:reuters.com Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers market pricing or shortage signal 1-6 months
  - Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers market pricing or shortage signal specialist analysis
  - site:reuters.com Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers market pricing or shortage signal
- Minimum acceptable evidence: 1
- Refresh expectation: Current market or shortage signal, preferably within 30-60 days.

### contrary_or_stabilising_evidence

- Why it matters: Tests the downside case and supports confidence discipline.
- Source requirement: contrary_or_easing_evidence
- Evidence question: What evidence would justify relaxing a high-control sourcing stance back to normal procurement?
- Preferred domains: reuters.com, apnews.com, gov.uk, iea.org
- Preferred source types: contrary_or_stabilising_evidence, reputable_news, official_primary
- Generated queries:
  - site:reuters.com rare earth export controls easing licence approvals magnet supply
  - site:reuters.com alternative rare earth magnet supply easing capacity Reuters
  - site:reuters.com Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers contrary or easing evidence 1-6 months
  - site:reuters.com Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers contrary or easing evidence
  - Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers contrary or easing evidence scope limited stabilising contrary evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current easing or contrary evidence, preferably within 30 days.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: company_data_requirements_and_anti_overclaiming_controls
- Evidence question: What company-specific data is required before turning a client-type exposure screen into an operational production decision?
- Preferred domains: gov.uk, hvm.catapult.org.uk, csis.org, rusi.org
- Preferred source types: specialist_analysis, official_primary
- Generated queries:
  - site:hvm.catapult.org.uk advanced manufacturer rare earth magnet supply chain inventory supplier qualification
  - site:csis.org rare earth magnet supply chain company data qualification inventory risk
  - site:gov.uk Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers company data requirements and anti overclaiming controls 1-6 months
  - Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers company data requirements and anti overclaiming controls specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained control guidance.

## Search Results Summary

- Total candidate sources found: 62
- Total queries run: 38
- Total selected sources: 9
- Duplicate URLs removed: 0
- Source categories covered: company_update, contrary_or_stabilising_evidence, official_primary, reputable_news, specialist_analysis
- Source categories missing: None
- Fetch failures: 3

## Quantified Evidence Summary

- Source count: 9
- Source coverage: 100%
- High-weight source count: 0
- Quantified facts: 64
- Score support summary: Scores are supported by 9 selected sources, 100% requirement coverage and 64 extracted quantified facts.
- Confidence cap reason: Confidence capped because live evidence can screen client-type exposure, but BOM, supplier, inventory and contract data are still required for company-specific production decisions.

## Source Requirement Coverage

| Requirement | Why Required | Covered By | Evidence Weight | Decision Questions Supported | Remaining Gap |
| --- | --- | --- | --- | --- | --- |
| uk_critical_minerals_policy_and_manufacturing_resilience | Anchors the UK policy and resilience context for why critical-mineral and rare-earth disruption matters to UK advanced manufacturers. | L1, L3, L4 | medium | Why is this a live UK manufacturing continuity issue rather than a generic global commodity story? | Policy anchor is strong enough for framing, but the saved extraction should be refreshed before quoting policy language. |
| export_control_direction_and_live_trigger | Shows whether new export controls, licences, restrictions or geopolitical triggers could interrupt procurement in the near term. | L1, L2, L3, L4, L7 | medium | Can the manufacturer continue production with the current supplier base if export-control disruption intensifies? | Partially covered; direct official export-control or licensing evidence is still needed before operational use. |
| rare_earth_magnet_or_controlled_input_classification | Defines which exact input or subcomponent is exposed so the case does not drift into generic critical-minerals commentary. | L1, L3, L4, L6, L9 | medium | Which exact input is controlled or concentration-exposed: finished magnet, oxide, alloy, sintered component or magnet-dependent subassembly? | Public evidence is useful, but BOM verification is still required. |
| supply_concentration_and_dependency_data | Quantifies dependency and concentration so the decision can distinguish manageable sourcing friction from structural supply risk. | L1, L3, L4, L6, L9 | medium | How concentrated is supply for the relevant rare earth magnet input, and how much is China-linked? | Strongest evidence area in the saved pack; refresh only if control scope or chemistry assumptions change. |
| uk_industry_exposure_and_advanced_manufacturing_relevance | Connects the global supply-chain issue to UK advanced-manufacturing production continuity and customer delivery risk. | L1, L3, L4, L5, L6, L9 | medium | Why is this relevant to a UK advanced manufacturer rather than only to upstream miners or battery policy? | Partially covered; the saved pack would benefit from broader UK sector evidence beyond a company perspective. |
| substitution_feasibility_and_alternative_supplier_qualification | Tests whether the manufacturer can redesign, dual-source or qualify alternative suppliers before inventory is exhausted. | L2, L5, L6, L7, L9 | low | Can the input be substituted, redesigned or qualified from another supplier within a commercially useful timeframe? | Weakest requirement; stronger magnet-specific engineering or qualification evidence is still needed. |
| market_pricing_or_shortage_signal | Shows whether pricing, scarcity or allocation conditions are tightening enough to affect stockpile or procurement decisions. | L2, L6, L7, L9 | low | Do export-control direction, licensing friction and shortage signals justify stockpiling, allocation or accelerated qualification? | Only directionally covered; the saved Reuters stock-page snippet is not a robust pricing series. |
| contrary_or_easing_evidence | Prevents one-way escalation by identifying easing, new capacity, licence clarification or alternative supply that could narrow the continuity risk. | L1, L2, L3, L4, L7, L8 | medium | What evidence would justify relaxing a high-control sourcing stance back to normal procurement? | Partially covered; easing evidence remains secondary and should be refreshed before controls are relaxed. |
| company_data_requirements_and_anti_overclaiming_controls | Makes visible which conclusions remain illustrative until bill of materials, supplier, inventory and contract data are supplied. | L1, L3, L4, L6, L9 | medium | What company-specific data is required before turning a client-type exposure screen into an operational production decision? | Covered as a control list, but public evidence is not a substitute for company data. |

## Source Quality Notes

| Evidence area | Current source quality | Action before operational use |
| --- | --- | --- |
| UK policy anchor | Medium-high. GOV.UK is a credible anchor, but the saved claim is snippet-based rather than a clean direct quotation. | Refresh the exact policy passage if the brief will be used in management or board materials. |
| Export-control trigger | Medium. Reuters is credible, but the saved export-control evidence is snippet-only and not an official notice. | Refresh the live reporting and add a direct official control or licensing source before operational use. |
| Supply concentration | High. USGS commodity evidence is the strongest structural part of the pack. | Recheck if the affected chemistry or control scope changes. |
| Substitution feasibility | Weak-medium. The saved specialist evidence is not strong enough to support engineering timing claims on its own. | Replace with magnet-specific qualification or redesign evidence before operational use. |
| Market/pricing shortage signal | Weak-medium. The saved Reuters stock-page snippet is directional only. | Refresh with stronger shortage or pricing evidence before using the output for budgeting or contracting. |
| Contrary/easing evidence | Medium. Reuters legal analysis is useful for scope limits, not as a clean all-clear signal. | Refresh with fresher easing evidence before relaxing controls. |
| Company-specific data requirements | High as a control framework, but still incomplete for a real operating decision. | Load BOM, supplier, inventory, contract and qualification data before using the model commercially. |

## Selected Sources

| Source ID | Requirement | Source role | Source value | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| L1 | uk_critical_minerals_policy_and_manufacturing_resilience | official_anchor | Anchors the UK policy and manufacturing-resilience baseline for why this is a live advanced-manufacturing continuity issue. | site:gov.uk UK critical minerals strategy vision 2035 rare earth magnets manufacturing | Why is this a live UK manufacturing continuity issue rather than a generic global commodity story? | Resilience for the Future: The UK's Critical Minerals Strategy | 5 | 5 | 3 | 3 | 3 | 5 | medium | trusted domain, direct topic match, fits official_primary | Supports the UK policy relevance for stockpile, alternative supplier qualification and redesign decisions. | snippet_used | Snippet/metadata-supported; confirm the exact policy passage before using it as a quoted management reference. |
| L2 | export_control_direction_and_live_trigger | live_event_reporting | Shows whether licensing practice is tightening, easing or becoming more selective for rare earth magnet exports. | site:reuters.com China rare earth magnet export controls licences Reuters | Can the manufacturer continue production with the current supplier base if export-control disruption intensifies? | China rare earths magnets maker says it has received export licences | 4 | 5 | 3 | 2 | 2 | 5 | medium | trusted domain, direct topic match, fits reputable_news | Supports export-control trigger monitoring and the threshold for moving from current sourcing to stockpile or qualification action. | failed | Fetch failed; evidence uses Reuters snippet only and should be refreshed before operational use. |
| L3 | rare_earth_magnet_or_controlled_input_classification | data_or_indicator_source | Quantifies concentration, dependency and controlled-input exposure needed for continuity decisions. | site:usgs.gov rare earth permanent magnets supply chain NdFeB dysprosium terbium | Which exact input is controlled or concentration-exposed: finished magnet, oxide, alloy, sintered component or magnet-dependent subassembly? | Mineral Commodity Summaries 2024: Rare Earths - USGS.gov | 5 | 5 | 3 | 3 | 2 | 5 | medium | trusted domain, direct topic match, fits official_primary | Supports identifying which exact input or subcomponent is exposed before action is taken. | snippet_used | Rule-based extraction; analyst should verify facts and context. |
| L4 | supply_concentration_and_dependency_data | data_or_indicator_source | Quantifies concentration, dependency and controlled-input exposure needed for continuity decisions. | site:usgs.gov rare earths production concentration China permanent magnets | How concentrated is supply for the relevant rare earth magnet input, and how much is China-linked? | Heavy Rare Earths - Mineral Commodity Summaries 2026 - USGS.gov | 5 | 5 | 3 | 3 | 2 | 5 | medium | trusted domain, direct topic match, fits official_primary | Supports concentration scoring and whether the current supplier base is too dependency-heavy to leave unchanged. | snippet_used | Rule-based extraction; analyst should verify facts and context. |
| L5 | uk_industry_exposure_and_advanced_manufacturing_relevance | operator_or_industry_guidance | Provides a company or industry perspective on how rare earth dependency can constrain UK advanced-manufacturing delivery plans. | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers uk industry exposure and advanced manufacturing relevance specialist analysis | Why is this relevant to a UK advanced manufacturer rather than only to upstream miners or battery policy? | Are automotive supply chains sleepwalking into the next pandemic? | 4 | 5 | 3 | 3 | 3 | 5 | medium | direct topic match, fits company_update | Supports UK industry exposure assessment and the case for customer allocation or management escalation planning. | snippet_used | Company/industry perspective; not a neutral sector-wide official source. |
| L6 | substitution_feasibility_and_alternative_supplier_qualification | specialist_interpretation | Only weakly supports substitution analysis; use it as a caveat, not as a strong engineering anchor. | site:csis.org rare earth magnet substitution qualification alternative suppliers | Can the input be substituted, redesigned or qualified from another supplier within a commercially useful timeframe? | 2020 NASA Technology Taxonomy | 4 | 5 | 3 | 4 | 2 | 5 | low | trusted domain, direct topic match, fits specialist_analysis | Supports caution on redesign and alternative-supplier feasibility until stronger engineering or industry evidence is added. | snippet_used | Weak fit for the requirement; stronger magnet-specific substitution evidence is still needed. |
| L7 | market_pricing_or_shortage_signal | market_pricing | Provides a weak, snippet-only shortage signal rather than a strong market-pricing anchor. | site:reuters.com rare earth magnet users paying premium prices ex China supply Reuters | Do export-control direction, licensing friction and shortage signals justify stockpiling, allocation or accelerated qualification? | (NEO.TO) \| Stock Price & Latest News \| Reuters | 4 | 5 | 3 | 4 | 2 | 5 | low | trusted domain, direct topic match, fits reputable_news | Supports stockpile timing and shortage monitoring, but not precise pricing decisions. | failed | Fetch failed and the saved source is a Reuters company page rather than a dedicated pricing series. |
| L8 | contrary_or_easing_evidence | contrary_scope_limit | Provides scope-limiting legal and trade-policy context for when controls might be relaxed, but it is not a direct official easing signal. | site:reuters.com alternative rare earth magnet supply easing capacity Reuters | What evidence would justify relaxing a high-control sourcing stance back to normal procurement? | Critical minerals: licensing, tariffs, and the new supply-chain risk | 4 | 5 | 3 | 3 | 2 | 5 | medium | trusted domain, direct topic match, fits contrary_or_stabilising_evidence | Supports the threshold for stepping back from stockpile, allocation or production-hold contingencies when easing evidence strengthens. | failed | Secondary legal-analysis source; pair with fresher live reporting or official notices before relaxing controls operationally. |
| L9 | company_data_requirements_and_anti_overclaiming_controls | specialist_interpretation | Provides partial market context, but mainly reinforces the limits of using public evidence without company data. | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers company data requirements and anti overclaiming controls specialist analysis | What company-specific data is required before turning a client-type exposure screen into an operational production decision? | Rare Earth Magnets 2026-2036: Technologies, Supply, Markets | 1 | 5 | 3 | 2 | 2 | 5 | low | direct topic match, fits specialist_analysis | Supports anti-overclaiming controls and the requirement to gather BOM, supplier, inventory and contract data before using the model commercially. | snippet_used | Report-summary evidence only; not a strong standalone technical or pricing source. |

## Rejected Sources

| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |
| --- | --- | --- | ---: | --- | --- | --- |
| [PDF] Mineral Commodity Summaries 2024: Rare Earths - USGS.gov | supply_concentration_and_dependency_data | site:usgs.gov rare earths production concentration China permanent magnets | 24 | independence_score | duplicate or near-duplicate | no |
| [PDF] Rare Earth Permanent Magnets - Department of Energy | supply_concentration_and_dependency_data | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers supply concentration and dependency data specialist analysis | 22 | independence_score | duplicate or near-duplicate | no |
| [PDF] Rare Earth Permanent Magnets - Department of Energy | substitution_feasibility_and_alternative_supplier_qualification | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers substitution feasibility and alternative supplier qualification specialist analysis | 21 | independence_score | duplicate or near-duplicate | no |
| [PDF] Rare Earth Permanent Magnets - Department of Energy | substitution_feasibility_and_alternative_supplier_qualification | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers substitution feasibility and alternative supplier qualification Reuters | 21 | independence_score | duplicate or near-duplicate | no |
| [PDF] Rare Earth Permanent Magnets - Department of Energy | market_pricing_or_shortage_signal | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers market pricing or shortage signal specialist analysis | 21 | independence_score | duplicate or near-duplicate | no |
| China is issuing streamlined licenses for rare earth exports, state ... | contrary_or_easing_evidence | site:reuters.com rare earth export controls easing licence approvals magnet supply | 26 | independence_score | duplicate or near-duplicate | no |
| [PDF] Are automotive supply chains sleepwalking into the next pandemic? | contrary_or_easing_evidence | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers contrary or easing evidence scope limited stabilising contrary evidence | 26 | independence_score | duplicate or near-duplicate | no |
| With new export controls on critical minerals, supply concentration ... | contrary_or_easing_evidence | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers contrary or easing evidence scope limited stabilising contrary evidence | 27 | independence_score | duplicate or near-duplicate | no |
| [PDF] 2020 NASA Technology Taxonomy | company_data_requirements_and_anti_overclaiming_controls | site:csis.org rare earth magnet supply chain company data qualification inventory risk | 24 | independence_score | duplicate or near-duplicate | no |
| [PDF] Rare Earth Permanent Magnets - Department of Energy | company_data_requirements_and_anti_overclaiming_controls | Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers company data requirements and anti overclaiming controls specialist analysis | 21 | independence_score | duplicate or near-duplicate | no |

## Evidence Coverage Assessment

- Strongest evidence category: official policy and commodity concentration data
- Weakest evidence category: substitution feasibility and market-pricing evidence
- Missing evidence: direct official export-control notice and company-specific operating data
- Contrary/stabilising evidence: Present, but secondary rather than decisive
- Confidence impact: Evidence coverage supports a screened client-type recommendation, but confidence remains capped by weaker substitution and pricing evidence plus missing company data.

## Illustrative Route-Cost Scenario

- Production continuity outputs use illustrative inventory, qualification, concentration and revenue inputs unless company data is supplied.
- Replace bill of materials, supplier-country, inventory, purchase order, contract and customer data before using the model commercially.
- Treat the continuity gap as a client-type decision aid, not a company-specific production forecast.

## Refresh Triggers

- Refresh if export-control rules or licensing practice changes.
- Refresh if China-linked export licences tighten or ease.
- Refresh if rare earth magnet shortage or price signals change.
- Refresh if alternative supplier qualification assumptions change.
- Refresh when company BOM, supplier, inventory or contract data becomes available.

## Analyst Review Controls

- Verify publication dates.
- Verify fetched content against source page.
- Check source freshness.
- Check export-control and licensing updates remain current.
- Check shortage and pricing signals remain current.
- Check easing evidence before relaxing controls.
- Confirm BOM, supplier, inventory and qualification assumptions with the operator.
