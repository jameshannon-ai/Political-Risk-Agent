# Source Audit

## Search Configuration

- Topic: Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs
- Business user: shipping_operator
- Region: Persian Gulf / UK shipping operators
- Time horizon: 1-3 months
- Concerns: transit versus delay versus reroute decision, sanctions red flags from tolls or safe-passage demands, war-risk insurance viability, AIS and vessel-flow disruption, detention risk, route cost trade-offs, legal hold threshold, relaxation triggers
- Search provider used: tavily
- Evidence mode: Live source retrieval
- Fallback data used: false
- Provider error: None
- Retrieval timestamp: 2026-05-28T21:02:00

## Research Plan

- Research objective: Build a governed evidence base for shipping_operator decision-making on Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs in Persian Gulf / UK shipping operators over 1-3 months, using the maritime_trade domain pack.
- Decision questions:
  - Should the operator transit, delay, reroute or place the voyage on legal hold?
  - Is there a sanctions red flag from tolls, safe-passage demands, offsets, swaps, guarantees, in-kind arrangements or Iranian coordination?
  - Is war-risk cover available and economically viable?
  - Do AIS/vessel-flow indicators show route normalisation or continuing operating stress?
  - How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included?
  - What evidence would justify relaxing controls?
- Required source mix:
  - official maritime/security advisory
  - transit-control and detention reporting
  - sanctions and legal guidance
  - energy/freight/vessel-flow data
  - insurance and route-cost evidence
  - contrary or de-escalation evidence
- Expected evidence types: official_primary, energy_chokepoint_data, insurance_market_evidence, vessel_flow_or_freight_market_evidence, reputable_news, specialist_analysis, contrary_or_stabilising_evidence
- Minimum acceptable coverage: {'minimum_total_requirements': 8, 'minimum_high_priority_requirements': 6, 'high_priority_requirements': ['official_maritime_security', 'transit_control_or_constabulary_actions', 'sanctions_and_safe_passage_payment_risk', 'war_risk_insurance_pricing', 'vessel_flow_and_AIS_behaviour', 'energy_cargo_and_chokepoint_exposure'], 'minimum_sources_per_requirement': {'REQ-HSO-A': 1, 'REQ-HSO-B': 1, 'REQ-HSO-C': 1, 'REQ-HSO-D': 1, 'REQ-HSO-E': 1, 'REQ-HSO-F': 1, 'REQ-HSO-G': 1, 'REQ-HSO-H': 1}}
- Refresh priorities:
  - official_maritime_security: Current official maritime/security guidance, preferably checked within 30 days.
  - transit_control_or_constabulary_actions: Current operational reporting and advisories, preferably within 30 days.
  - sanctions_and_safe_passage_payment_risk: Current sanctions guidance or reporting, preferably within 30 days.
  - war_risk_insurance_pricing: Current insurance-market evidence, preferably within 30 days.
  - vessel_flow_and_AIS_behaviour: Recent vessel-flow or AIS evidence, preferably within 30 days.
  - energy_cargo_and_chokepoint_exposure: Recent structural data or current maintained chokepoint data.
  - route_cost_and_arbitrage_inputs: Current market inputs plus operator assumptions validated for the voyage.
  - contrary_or_de_escalation_evidence: Current de-escalation reporting and vessel-flow evidence, preferably within 30 days.

## Source Strategy

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: official_maritime_security
- Evidence question: Should the operator transit, delay, reroute or place the voyage on legal hold?
- Preferred domains: ukmto.org, imo.org, ics-shipping.org, bimco.org, intertanko.com, ocimf.org
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:ukmto.org Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs official maritime security 1-3 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current official maritime/security guidance, preferably checked within 30 days.

### reputable_news

- Why it matters: Corroborates current events and commercial impacts.
- Source requirement: transit_control_or_constabulary_actions
- Evidence question: Should the operator transit, delay, reroute or place the voyage on legal hold?
- Preferred domains: reuters.com, apnews.com, ukmto.org, imo.org, gov.uk
- Preferred source types: reputable_news, official_primary
- Generated queries:
  - Reuters Iran sets up mechanism to manage vessel transit through Hormuz
  - AP Iran transit controls Hormuz vessel coordination detention risk
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs transit control or constabulary actions 1-3 months
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs transit control or constabulary actions
- Minimum acceptable evidence: 1
- Refresh expectation: Current operational reporting and advisories, preferably within 30 days.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: sanctions_and_safe_passage_payment_risk
- Evidence question: Is there a sanctions red flag from tolls, safe-passage demands, offsets, swaps, guarantees, in-kind arrangements or Iranian coordination?
- Preferred domains: ofac.treasury.gov, ofsi.gov.uk, gov.uk, reuters.com, apnews.com
- Preferred source types: official_primary, specialist_analysis, reputable_news
- Generated queries:
  - OFAC FAQ 1249 sanctions risks toll safe-passage payments Hormuz
  - AP US sanctions Iran Persian Gulf Strait Authority
  - site:ofac.treasury.gov Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs sanctions and safe passage payment risk 1-3 months
  - Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs sanctions and safe passage payment risk specialist analysis
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs sanctions and safe passage payment risk
- Minimum acceptable evidence: 1
- Refresh expectation: Current sanctions guidance or reporting, preferably within 30 days.

### insurance_market_evidence

- Why it matters: Supports premium, reinsurance and underwriting assessment.
- Source requirement: war_risk_insurance_pricing
- Evidence question: Is war-risk cover available and economically viable?
- Preferred domains: howdenre.com, lmalloyds.com, lloydslist.com, reuters.com
- Preferred source types: insurance_market_evidence, reputable_news
- Generated queries:
  - Howden Re Strait of Hormuz war risk pricing
  - Reuters Hormuz war risk insurance premium shipping
  - site:howdenre.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs war risk insurance pricing 1-3 months
  - site:howdenre.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs war risk insurance pricing
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs war risk insurance pricing
- Minimum acceptable evidence: 1
- Refresh expectation: Current insurance-market evidence, preferably within 30 days.

### vessel_flow_or_freight_market_evidence

- Why it matters: Shows whether market behaviour confirms disruption.
- Source requirement: vessel_flow_and_AIS_behaviour
- Evidence question: Do AIS/vessel-flow indicators show route normalisation or continuing operating stress?
- Preferred domains: reuters.com, kpler.com, vortexa.com, lloydslist.com, marinetraffic.com, gibsons.co.uk, apnews.com
- Preferred source types: vessel_flow_or_freight_market_evidence, reputable_news, specialist_analysis
- Generated queries:
  - Reuters Hormuz tanker traffic AIS transponder behaviour
  - AP Hormuz vessel flows AIS disruption
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs vessel flow and AIS behaviour 1-3 months
  - site:lloydslist.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs vessel flow and AIS behaviour
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs vessel flow and AIS behaviour
- Minimum acceptable evidence: 1
- Refresh expectation: Recent vessel-flow or AIS evidence, preferably within 30 days.

### energy_chokepoint_data

- Why it matters: Quantifies oil, LNG and strategic trade exposure.
- Source requirement: energy_cargo_and_chokepoint_exposure
- Evidence question: How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included?
- Preferred domains: eia.gov, iea.org, unctad.org, spglobal.com
- Preferred source types: energy_chokepoint_data, specialist_analysis
- Generated queries:
  - EIA Strait of Hormuz chokepoint oil LNG exposure
  - IEA Strait of Hormuz oil LNG chokepoint exposure
  - site:eia.gov Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs energy cargo and chokepoint exposure 1-3 months
  - site:spglobal.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs energy cargo and chokepoint exposure
- Minimum acceptable evidence: 1
- Refresh expectation: Recent structural data or current maintained chokepoint data.

### insurance_market_evidence

- Why it matters: Supports premium, reinsurance and underwriting assessment.
- Source requirement: route_cost_and_arbitrage_inputs
- Evidence question: How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included?
- Preferred domains: howdenre.com, lloydslist.com, spglobal.com, reuters.com
- Preferred source types: insurance_market_evidence, specialist_analysis, reputable_news
- Generated queries:
  - site:howdenre.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs route cost and arbitrage inputs 1-3 months
  - site:howdenre.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs route cost and arbitrage inputs
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs route cost and arbitrage inputs
- Minimum acceptable evidence: 1
- Refresh expectation: Current market inputs plus operator assumptions validated for the voyage.

### contrary_or_stabilising_evidence

- Why it matters: Tests the downside case and supports confidence discipline.
- Source requirement: contrary_or_de_escalation_evidence
- Evidence question: What evidence would justify relaxing controls?
- Preferred domains: reuters.com, apnews.com, gov.uk, ukmto.org, imo.org
- Preferred source types: contrary_or_stabilising_evidence, reputable_news, official_primary
- Generated queries:
  - Reuters Strait of Hormuz reopening conditions shipping de-escalation
  - AP Strait of Hormuz de-escalation vessel flows reopening
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs contrary or de escalation evidence 1-3 months
  - site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs contrary or de escalation evidence
  - Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs contrary or de escalation evidence scope limited stabilising contrary evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current de-escalation reporting and vessel-flow evidence, preferably within 30 days.

## Search Results Summary

- Total candidate sources found: 50
- Total queries run: 32
- Total selected sources: 7
- Duplicate URLs removed: 0
- Source categories covered: contrary_or_stabilising_evidence, insurance_market_evidence, reputable_news, specialist_analysis, vessel_flow_or_freight_market_evidence
- Source categories missing: official_primary, official_primary, energy_chokepoint_data
- Fetch failures: 1

## Quantified Evidence Summary

- Source count: 7
- Source coverage: 88%
- High-weight source count: 1
- Quantified facts: 14
- Score support summary: Scores are supported by 7 selected sources, 88% requirement coverage and 14 extracted quantified facts.
- Confidence cap reason: Confidence capped because one or more source requirements are not covered.

## Source Requirement Coverage

| Requirement | Why Required | Covered By | Evidence Weight | Decision Questions Supported | Remaining Gap |
| --- | --- | --- | --- | --- | --- |
| official_maritime_security | Establishes whether transit conditions create live security, detention, crew-safety or voyage-approval risk. | None | low | Should the operator transit, delay, reroute or place the voyage on legal hold? | Requires UKMTO, IMO, ICS, BIMCO, INTERTANKO, OCIMF or government advisory refresh before operational use. |
| transit_control_or_constabulary_actions | Captures Iranian transit-control mechanisms, vessel coordination requirements, detention risk, naval warnings or expanded control claims. | L1, L2 | high | Should the operator transit, delay, reroute or place the voyage on legal hold? | No immediate coverage gap; analyst should still verify recency and source content. |
| sanctions_and_safe_passage_payment_risk | Identifies whether tolls, safe-passage payments, digital asset payments, offsets, swaps, guarantees or in-kind arrangements could create sanctions exposure. | L1, L2 | high | Is there a sanctions red flag from tolls, safe-passage demands, offsets, swaps, guarantees, in-kind arrangements or Iranian coordination? | No immediate coverage gap; analyst should still verify recency and source content. |
| war_risk_insurance_pricing | Measures how insurance repricing affects voyage economics and whether insurance cost changes route decisions. | L1, L3, L6 | high | Is war-risk cover available and economically viable? | No immediate coverage gap; analyst should still verify recency and source content. |
| vessel_flow_and_AIS_behaviour | Shows whether actual vessel behaviour confirms constrained transit, AIS suppression, trapped vessels, traffic collapse or partial reopening. | L1, L4 | high | Do AIS/vessel-flow indicators show route normalisation or continuing operating stress? | No immediate coverage gap; analyst should still verify recency and source content. |
| energy_cargo_and_chokepoint_exposure | Quantifies why Hormuz disruption matters for oil, LNG, tanker cargoes and UK-linked energy/shipping exposure. | L5 | high | How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included? | Current evidence is secondary reporting of EIA-linked data; refresh with direct EIA or equivalent official dataset before operational use. |
| route_cost_and_arbitrage_inputs | Supports comparison of transit, delay and rerouting options through fuel cost, voyage days, insurance premium, demurrage and charter exposure. | L1, L3, L6 | medium | How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included? | No immediate coverage gap; analyst should still verify recency and source content. |
| contrary_or_de_escalation_evidence | Prevents one-way escalation analysis and defines conditions under which direct transit may become acceptable again. | L1, L2, L7 | medium | What evidence would justify relaxing controls? | Current contrary signal is weak secondary reporting; refresh with Reuters, AP or official recovery evidence before treating relaxation as credible. |

## Selected Sources

| Source ID | Requirement | Source role | Source value | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| L1 | transit_control_or_constabulary_actions | live_event_reporting | Shows whether direct passage remains disrupted through detentions, coordination demands or live transit controls. | Reuters Iran sets up mechanism to manage vessel transit through Hormuz | Should the operator transit, delay, reroute or place the voyage on legal hold? | Al-Monitor Summary of Reuters Hormuz Transit-Control Report | 3 | 4 | 3 | 4 | 2 | 5 | medium | direct topic match, fits reputable_news | Supports the transit versus delay versus reroute decision by showing whether direct passage remains operationally acceptable. | ok | Operational reporting should still be checked against current official guidance before transit approval. |
| L2 | sanctions_and_safe_passage_payment_risk | specialist_interpretation | Explains when safe-passage demands turn into legal/compliance hold triggers. | Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs sanctions and safe passage payment risk specialist analysis | Is there a sanctions red flag from tolls, safe-passage demands, offsets, swaps, guarantees, in-kind arrangements or Iranian coordination? | IndexBox / PGSA Hormuz Fees and Sanctions Risk Note | 4 | 5 | 3 | 5 | 4 | 5 | medium | direct topic match, specialist interpretation of sanctions-linked payment risk | Supports legal-hold escalation if tolls, safe-passage payments, offsets, swaps, guarantees or in-kind demands appear. | ok | Specialist analysis should be validated against current legal guidance before any payment-related decision. |
| L3 | war_risk_insurance_pricing | market_pricing | Shows whether war-risk cover is available and when premium pressure makes reroute economically preferable. | Howden Re Strait of Hormuz war risk pricing | Is war-risk cover available? | Howden Re Hormuz War-Risk Pricing Analysis | 4 | 4 | 3 | 5 | 5 | 5 | high | direct topic match, fits insurance_market_evidence | Supports insurance viability checks and the break-even comparison between direct transit and reroute. | ok | Market pricing is fast-moving and should be refreshed with broker or underwriter quotes before sailing. |
| L4 | vessel_flow_and_AIS_behaviour | data_or_indicator_source | Shows whether AIS and vessel-flow behaviour support normalisation or continued stress. | site:lloydslist.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs vessel flow and AIS behaviour | Do AIS/vessel-flow indicators show route normalisation or continuing stress? | Lloyd's List Hormuz Traffic Stress Monitor | 4 | 4 | 3 | 5 | 2 | 5 | medium | trusted domain, direct topic match, fits vessel_flow_or_freight_market_evidence | Supports whether AIS and vessel-flow signals justify continued controls or conditional relaxation. | ok | Fetched page text was not decision-grade; pair this signal with Reuters, AP or vessel-tracking evidence before relaxing controls. |
| L5 | energy_cargo_and_chokepoint_exposure | data_or_indicator_source | Quantifies why a Hormuz routing decision matters for cargo, customer and timing exposure. | EIA Strait of Hormuz chokepoint oil LNG exposure | Why does Hormuz matter commercially? | World Oil Report on EIA Hormuz Chokepoint Dataset Update | 4 | 5 | 3 | 5 | 2 | 5 | medium | secondary reporting of EIA-linked chokepoint data; useful until direct official refresh | Supports impact severity and client communication on why Hormuz route decisions matter commercially. | ok | Use the underlying EIA chokepoint data for final cargo exposure calculations where available. |
| L6 | route_cost_and_arbitrage_inputs | market_pricing | Translates the disruption into operator-facing route-cost, delay and pass-through decisions. | site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs route cost and arbitrage inputs | How do direct transit, delay and reroute compare once insurance, sanctions and delay costs are included? | Reuters Hormuz Shipping Cost Surge Report | 5 | 4 | 3 | 5 | 2 | 5 | medium | trusted domain, direct topic match, fits insurance_market_evidence | Supports direct transit, delay and reroute cost comparison after insurance and hold costs are included. | snippet_used | This source is snippet-based because page fetch failed; refresh with full article access or broker data before using commercially. |
| L7 | contrary_or_de_escalation_evidence | contrary_scope_limit | Tests whether there is enough practical recovery evidence to relax from hold or reroute to conditional transit. | Reuters Strait of Hormuz reopening conditions shipping de-escalation | What evidence would justify relaxing controls? | STL.News De-escalation Signal Requiring Stronger Confirmation | 3 | 5 | 3 | 5 | 4 | 5 | medium | scope-limiting de-escalation signal, but weaker than a direct official or Reuters/AP recovery source | Supports the evidence threshold for moving from hold or reroute back to conditional transit. | ok | Contrary evidence should be treated as conditional until stronger operational recovery evidence is available. |

## Rejected Sources

| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |
| --- | --- | --- | ---: | --- | --- | --- |
| Hormuz at near standstill as Iran warns ships to keep to its waters | war_risk_insurance_pricing | site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs war risk insurance pricing | 26 | independence_score | duplicate or near-duplicate | no |
| Hormuz at near standstill as Iran warns ships to keep to its waters | vessel_flow_and_AIS_behaviour | site:reuters.com Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs vessel flow and AIS behaviour | 24 | independence_score | duplicate or near-duplicate | no |
| Strait of Hormuz reopens to shipping, hinting at US-Iran de-escalation | contrary_or_de_escalation_evidence | Reuters Strait of Hormuz reopening conditions shipping de-escalation | 30 | reliability_score | stronger source already selected for the same requirement | yes |
| US Secures Strait of Hormuz Reopening Amid Ceasefire \| eNewsX | contrary_or_de_escalation_evidence | Reuters Strait of Hormuz reopening conditions shipping de-escalation | 29 | reliability_score | stronger source already selected for the same requirement | yes |
| The Strait of Hormuz: Critical Maritime Trade Route \| University of Wisconsin Law School | contrary_or_de_escalation_evidence | Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs contrary or de escalation evidence scope limited stabilising contrary evidence | 28 | decision_value_score | stronger source already selected for the same requirement | yes |
| [PDF] Iran Conflict and the Strait of Hormuz: Impacts on Oil, Gas, and Other ... | contrary_or_de_escalation_evidence | Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs contrary or de escalation evidence scope limited stabilising contrary evidence | 28 | decision_value_score | stronger source already selected for the same requirement | yes |
| The Global Costs of Instability in the Strait of Hormuz | contrary_or_de_escalation_evidence | Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs contrary or de escalation evidence scope limited stabilising contrary evidence | 28 | decision_value_score | stronger source already selected for the same requirement | yes |
| What stopping war-risk insurance in the Strait of Hormuz tells us | war_risk_insurance_pricing | Reuters Hormuz war risk insurance premium shipping | 27 | recency_score | stronger source already selected for the same requirement | yes |
| US pushes to reopen Strait of Hormuz as Iranian attacks on UAE strain ceasefire \| AP News | contrary_or_de_escalation_evidence | AP Strait of Hormuz de-escalation vessel flows reopening | 27 | decision_value_score | stronger source already selected for the same requirement | yes |
| US claims progress in reopening the Strait of Hormuz, saying 2 merchant ships have transited \| Courthouse News Service | contrary_or_de_escalation_evidence | AP Strait of Hormuz de-escalation vessel flows reopening | 27 | decision_value_score | stronger source already selected for the same requirement | yes |

## Evidence Coverage Assessment

- Strongest evidence category: insurance_market_evidence
- Weakest evidence category: official_primary
- Missing evidence: official_primary, official_primary, energy_chokepoint_data
- Contrary/stabilising evidence: Present
- Confidence impact: Confidence reduced by missing evidence categories.

## Route-Cost Assumptions

- Direct, delay and reroute comparisons use illustrative voyage assumptions requiring operator validation.
- Validate voyage days, bunker burn, daily vessel cost, war-risk premiums, demurrage and compliance hold assumptions before route approval.
- Sanctions risk should be treated as a legal override, not just a line item in the direct-route cost stack.

## Refresh Triggers

- Refresh immediately if any toll, safe-passage fee, guarantee, offset, swap or in-kind demand is reported.
- Refresh before voyage approval if war-risk premium, exclusions, cancellation wording or insurer appetite changes.
- Refresh if AIS disruption, detention reports, transit-control notices or official guidance change.
- Validate vessel value, delay-cost, reroute-cost and charter assumptions before using the optimiser commercially.
- Relax from hold or reroute only after official guidance, insurer appetite and vessel-flow recovery improve together.

## Analyst Review Controls

- Verify publication dates.
- Verify fetched content against the source page or search snippet.
- Check transit-control, detention and AIS evidence remain current.
- Check war-risk premium, exclusions and insurer appetite before voyage approval.
- Check sanctions/legal implications of any toll, payment, guarantee, offset or swap demand.
- Check de-escalation reporting against practical vessel-flow recovery before relaxing controls.
