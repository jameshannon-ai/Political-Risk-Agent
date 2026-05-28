# Source Audit

## Search Configuration

- Topic: Strait of Hormuz Transit Controls
- Business user: shipping_operator
- Region: Persian Gulf / UK shipping operators
- Time horizon: 1-3 months
- Concerns: Should a UK shipping operator transit, delay, reroute or escalate a Hormuz-linked voyage for legal/compliance review?, Do transit controls or detention risks make direct passage operationally unacceptable?, Does sanctions or war-risk pressure override the cheaper direct route?, What evidence would justify relaxation?, Should Hormuz-linked voyages require enhanced operational approval?, Is this a live vessel security risk or mainly a commercial-pricing issue?, Are vessels being required to coordinate passage with Iranian authorities?, Does the transit-control mechanism create operational or detention risk?, Is direct transit still operationally acceptable?, Could a transit demand create sanctions exposure?, Should the voyage be escalated to legal/compliance review?, Does sanctions risk override a cheaper direct transit option?, Is war-risk cover available?, Has premium repricing changed the voyage economics?, Are exclusions, cancellation provisions or additional premiums relevant?, Are vessel flows recovering or still abnormal?, Are AIS/transponder behaviours creating operational or compliance red flags?, Should traffic recovery be treated as evidence for relaxation?, Why does Hormuz matter commercially?, Which cargoes and vessel types create the largest exposure?, Does cargo criticality increase charter, client or delivery pressure?, Is the cheaper route still acceptable once sanctions and insurance risk are included?, What are the cost trade-offs between transit, delay and reroute?, Which option has the best risk-adjusted commercial case?, What evidence would justify relaxing controls?, Has de-escalation translated into practical vessel-flow recovery?, Are insurance, sanctions and operator confidence improving together?
- Search provider used: fallback_demo_search
- Evidence mode: Reproducible curated source pack
- Fallback data used: true
- Provider error: None
- Retrieval timestamp: 2026-05-28T16:53:47

## Research Plan

- Research objective: Build a governed evidence base for shipping_operator decision-making on Strait of Hormuz Transit Controls in Persian Gulf / UK shipping operators over 1-3 months, using the maritime_trade domain pack.
- Decision questions:
  - Should a UK shipping operator transit, delay, reroute or escalate a Hormuz-linked voyage for legal/compliance review?
  - Do transit controls or detention risks make direct passage operationally unacceptable?
  - Does sanctions or war-risk pressure override the cheaper direct route?
  - What evidence would justify relaxation?
  - Should Hormuz-linked voyages require enhanced operational approval?
  - Is this a live vessel security risk or mainly a commercial-pricing issue?
  - Are vessels being required to coordinate passage with Iranian authorities?
  - Does the transit-control mechanism create operational or detention risk?
  - Is direct transit still operationally acceptable?
  - Could a transit demand create sanctions exposure?
  - Should the voyage be escalated to legal/compliance review?
  - Does sanctions risk override a cheaper direct transit option?
  - Is war-risk cover available?
  - Has premium repricing changed the voyage economics?
  - Are exclusions, cancellation provisions or additional premiums relevant?
  - Are vessel flows recovering or still abnormal?
  - Are AIS/transponder behaviours creating operational or compliance red flags?
  - Should traffic recovery be treated as evidence for relaxation?
  - Why does Hormuz matter commercially?
  - Which cargoes and vessel types create the largest exposure?
  - Does cargo criticality increase charter, client or delivery pressure?
  - Is the cheaper route still acceptable once sanctions and insurance risk are included?
  - What are the cost trade-offs between transit, delay and reroute?
  - Which option has the best risk-adjusted commercial case?
  - What evidence would justify relaxing controls?
  - Has de-escalation translated into practical vessel-flow recovery?
  - Are insurance, sanctions and operator confidence improving together?
- Required source mix:
  - official maritime/security advisory
  - transit-control and detention reporting
  - sanctions and legal guidance
  - energy/freight/vessel-flow data
  - insurance and route-cost evidence
  - contrary or de-escalation evidence
- Expected evidence types: official_primary, company_update, energy_chokepoint_data, insurance_market_evidence, vessel_flow_or_freight_market_evidence, reputable_news, specialist_analysis, contrary_or_stabilising_evidence
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
- Evidence question: Should Hormuz-linked voyages require enhanced operational approval?
- Preferred domains: ukmto.org, imo.org, ics-shipping.org, bimco.org, intertanko.com, ocimf.org
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:ukmto.org Strait of Hormuz Transit Controls official maritime security 1-3 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current official maritime/security guidance, preferably checked within 30 days.

### reputable_news

- Why it matters: Corroborates current events and commercial impacts.
- Source requirement: transit_control_or_constabulary_actions
- Evidence question: Are vessels being required to coordinate passage with Iranian authorities?
- Preferred domains: reuters.com, apnews.com, ukmto.org, imo.org, gov.uk
- Preferred source types: reputable_news, official_primary
- Generated queries:
  - Reuters Iran sets up mechanism to manage vessel transit through Hormuz
  - AP Iran transit controls Hormuz vessel coordination detention risk
  - site:reuters.com Strait of Hormuz Transit Controls transit control or constabulary actions 1-3 months
  - site:reuters.com Strait of Hormuz Transit Controls transit control or constabulary actions
- Minimum acceptable evidence: 1
- Refresh expectation: Current operational reporting and advisories, preferably within 30 days.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: sanctions_and_safe_passage_payment_risk
- Evidence question: Could a transit demand create sanctions exposure?
- Preferred domains: ofac.treasury.gov, ofsi.gov.uk, gov.uk, reuters.com, apnews.com
- Preferred source types: official_primary, specialist_analysis, reputable_news
- Generated queries:
  - OFAC FAQ 1249 sanctions risks toll safe-passage payments Hormuz
  - AP US sanctions Iran Persian Gulf Strait Authority
  - site:ofac.treasury.gov Strait of Hormuz Transit Controls sanctions and safe passage payment risk 1-3 months
  - Strait of Hormuz Transit Controls sanctions and safe passage payment risk specialist analysis
  - site:reuters.com Strait of Hormuz Transit Controls sanctions and safe passage payment risk
- Minimum acceptable evidence: 1
- Refresh expectation: Current sanctions guidance or reporting, preferably within 30 days.

### insurance_market_evidence

- Why it matters: Supports premium, reinsurance and underwriting assessment.
- Source requirement: war_risk_insurance_pricing
- Evidence question: Is war-risk cover available?
- Preferred domains: howdenre.com, lmalloyds.com, lloydslist.com, reuters.com
- Preferred source types: insurance_market_evidence, reputable_news
- Generated queries:
  - Howden Re Strait of Hormuz war risk pricing
  - Reuters Hormuz war risk insurance premium shipping
  - site:howdenre.com Strait of Hormuz Transit Controls war risk insurance pricing 1-3 months
  - site:howdenre.com Strait of Hormuz Transit Controls war risk insurance pricing
  - site:reuters.com Strait of Hormuz Transit Controls war risk insurance pricing
- Minimum acceptable evidence: 1
- Refresh expectation: Current insurance-market evidence, preferably within 30 days.

### vessel_flow_or_freight_market_evidence

- Why it matters: Shows whether market behaviour confirms disruption.
- Source requirement: vessel_flow_and_AIS_behaviour
- Evidence question: Are vessel flows recovering or still abnormal?
- Preferred domains: reuters.com, kpler.com, vortexa.com, lloydslist.com, marinetraffic.com, gibsons.co.uk, apnews.com
- Preferred source types: vessel_flow_or_freight_market_evidence, reputable_news, specialist_analysis
- Generated queries:
  - Reuters Hormuz tanker traffic AIS transponder behaviour
  - AP Hormuz vessel flows AIS disruption
  - site:reuters.com Strait of Hormuz Transit Controls vessel flow and AIS behaviour 1-3 months
  - site:lloydslist.com Strait of Hormuz Transit Controls vessel flow and AIS behaviour
  - site:reuters.com Strait of Hormuz Transit Controls vessel flow and AIS behaviour
- Minimum acceptable evidence: 1
- Refresh expectation: Recent vessel-flow or AIS evidence, preferably within 30 days.

### energy_chokepoint_data

- Why it matters: Quantifies oil, LNG and strategic trade exposure.
- Source requirement: energy_cargo_and_chokepoint_exposure
- Evidence question: Why does Hormuz matter commercially?
- Preferred domains: eia.gov, iea.org, unctad.org, spglobal.com
- Preferred source types: energy_chokepoint_data, specialist_analysis
- Generated queries:
  - EIA Strait of Hormuz chokepoint oil LNG exposure
  - IEA Strait of Hormuz oil LNG chokepoint exposure
  - site:eia.gov Strait of Hormuz Transit Controls energy cargo and chokepoint exposure 1-3 months
  - site:spglobal.com Strait of Hormuz Transit Controls energy cargo and chokepoint exposure
- Minimum acceptable evidence: 1
- Refresh expectation: Recent structural data or current maintained chokepoint data.

### insurance_market_evidence

- Why it matters: Supports premium, reinsurance and underwriting assessment.
- Source requirement: route_cost_and_arbitrage_inputs
- Evidence question: Is the cheaper route still acceptable once sanctions and insurance risk are included?
- Preferred domains: howdenre.com, lloydslist.com, spglobal.com, reuters.com
- Preferred source types: insurance_market_evidence, specialist_analysis, reputable_news
- Generated queries:
  - site:howdenre.com Strait of Hormuz Transit Controls route cost and arbitrage inputs 1-3 months
  - site:howdenre.com Strait of Hormuz Transit Controls route cost and arbitrage inputs
  - site:reuters.com Strait of Hormuz Transit Controls route cost and arbitrage inputs
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
  - site:reuters.com Strait of Hormuz Transit Controls contrary or de escalation evidence 1-3 months
  - site:reuters.com Strait of Hormuz Transit Controls contrary or de escalation evidence
  - Strait of Hormuz Transit Controls contrary or de escalation evidence scope limited stabilising contrary evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current de-escalation reporting and vessel-flow evidence, preferably within 30 days.

## Search Results Summary

- Total candidate sources found: 9
- Total queries run: 0
- Total selected sources: 9
- Duplicate URLs removed: 0
- Source categories covered: contrary_or_stabilising_evidence, energy_chokepoint_data, insurance_market_evidence, official_primary, reputable_news, specialist_analysis, vessel_flow_or_freight_market_evidence
- Source categories missing: None
- Fetch failures: 0

## Quantified Evidence Summary

- Source count: 9
- Source coverage: 100%
- High-weight source count: 0
- Quantified facts: 12
- Score support summary: Scores are supported by 9 selected sources, 100% requirement coverage and 12 extracted quantified facts.
- Confidence cap reason: Confidence capped below 5 because evidence came from a reproducible curated source pack rather than live retrieval.

## Source Requirement Coverage

| Requirement | Why Required | Covered By | Evidence Weight | Decision Questions Supported | Remaining Gap |
| --- | --- | --- | --- | --- | --- |
| official_maritime_security | Establishes whether transit conditions create live security, detention, crew-safety or voyage-approval risk. | HSO-001, HSO-002, HSO-003 | high | Should Hormuz-linked voyages require enhanced operational approval?; Is this a live vessel security risk or mainly a commercial-pricing issue? | No immediate coverage gap; analyst should still verify recency and source content. |
| transit_control_or_constabulary_actions | Captures Iranian transit-control mechanisms, vessel coordination requirements, detention risk, naval warnings or expanded control claims. | HSO-001, HSO-002, HSO-003, HSO-004 | high | Are vessels being required to coordinate passage with Iranian authorities?; Does the transit-control mechanism create operational or detention risk?; Is direct transit still operationally acceptable? | No immediate coverage gap; analyst should still verify recency and source content. |
| sanctions_and_safe_passage_payment_risk | Identifies whether tolls, safe-passage payments, digital asset payments, offsets, swaps, guarantees or in-kind arrangements could create sanctions exposure. | HSO-001, HSO-002, HSO-003, HSO-004, HSO-008 | high | Could a transit demand create sanctions exposure?; Should the voyage be escalated to legal/compliance review?; Does sanctions risk override a cheaper direct transit option? | No immediate coverage gap; analyst should still verify recency and source content. |
| war_risk_insurance_pricing | Measures how insurance repricing affects voyage economics and whether insurance cost changes route decisions. | HSO-004, HSO-006 | high | Is war-risk cover available?; Has premium repricing changed the voyage economics?; Are exclusions, cancellation provisions or additional premiums relevant? | No immediate coverage gap; analyst should still verify recency and source content. |
| vessel_flow_and_AIS_behaviour | Shows whether actual vessel behaviour confirms constrained transit, AIS suppression, trapped vessels, traffic collapse or partial reopening. | HSO-004, HSO-007, HSO-008 | high | Are vessel flows recovering or still abnormal?; Are AIS/transponder behaviours creating operational or compliance red flags?; Should traffic recovery be treated as evidence for relaxation? | No immediate coverage gap; analyst should still verify recency and source content. |
| energy_cargo_and_chokepoint_exposure | Quantifies why Hormuz disruption matters for oil, LNG, tanker cargoes and UK-linked energy/shipping exposure. | HSO-005, HSO-008 | high | Why does Hormuz matter commercially?; Which cargoes and vessel types create the largest exposure?; Does cargo criticality increase charter, client or delivery pressure? | No immediate coverage gap; analyst should still verify recency and source content. |
| route_cost_and_arbitrage_inputs | Supports comparison of transit, delay and rerouting options through fuel cost, voyage days, insurance premium, demurrage and charter exposure. | HSO-004, HSO-006, HSO-008 | medium | Is the cheaper route still acceptable once sanctions and insurance risk are included?; What are the cost trade-offs between transit, delay and reroute?; Which option has the best risk-adjusted commercial case? | No immediate coverage gap; analyst should still verify recency and source content. |
| contrary_or_de_escalation_evidence | Prevents one-way escalation analysis and defines conditions under which direct transit may become acceptable again. | HSO-001, HSO-002, HSO-003, HSO-004, HSO-009 | medium | What evidence would justify relaxing controls?; Has de-escalation translated into practical vessel-flow recovery?; Are insurance, sanctions and operator confidence improving together? | No immediate coverage gap; analyst should still verify recency and source content. |

## Selected Sources

| Source ID | Requirement | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| HSO-001 | official_primary |  |  | No safe transit through Strait of Hormuz: IMO Secretary-General |  |  |  |  |  |  |  |  |  | demo | Official safety guidance is strong on risk conditions but does not resolve sanctions or route-cost decisions. |
| HSO-002 | official_primary |  |  | OFAC Alert: Sanctions Risks of Iranian Demands for Strait of Hormuz Passage |  |  |  |  |  |  |  |  |  | demo | U.S. sanctions guidance should be translated into operator-specific legal advice for UK-controlled voyages. |
| HSO-003 | official_primary |  |  | 1249 \| Office of Foreign Assets Control |  |  |  |  |  |  |  |  |  | demo | The FAQ is U.S.-specific and should be combined with UK sanctions and operator counsel review. |
| HSO-004 | reputable_news |  |  | US imposes sanctions on Iranian agency trying to control shipping in the Strait of Hormuz |  |  |  |  |  |  |  |  |  | demo | Reporting should be cross-checked against primary designation records for named entities and counterparties. |
| HSO-005 | energy_chokepoint_data |  |  | Strait of Hormuz |  |  |  |  |  |  |  |  |  | demo | Structural chokepoint exposure does not by itself prove current transit conditions. |
| HSO-006 | insurance_market_evidence |  |  | Strait of Hormuz: (Re)insurance impact |  |  |  |  |  |  |  |  |  | demo | Broker analysis should be refreshed against current quoted terms before sailing. |
| HSO-007 | vessel_flow_or_freight_market_evidence |  |  | Shippers whipsawed by changing stances as vessels remain stuck in Strait of Hormuz |  |  |  |  |  |  |  |  |  | demo | News synthesis should be checked against live vessel-tracking and operator updates before changing stance. |
| HSO-008 | specialist_analysis |  |  | Market Insights \| Strait of Hormuz Spotlight |  |  |  |  |  |  |  |  |  | demo | Specialist analysis is interpretive and should be paired with primary or reputable reporting. |
| HSO-009 | contrary_or_stabilising_evidence |  |  | Trump says a deal with Iran and opening of Strait of Hormuz are 'largely negotiated' |  |  |  |  |  |  |  |  |  | demo | Diplomatic reporting should not be treated as proof of operational reopening. |

## Rejected Sources

| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |
| --- | --- | --- | ---: | --- | --- | --- |
| Reuters Iran sets up mechanism to manage vessel transit through Hormuz | transit_control_or_constabulary_actions | Reuters Iran sets up mechanism to manage vessel transit through Hormuz | 0 |  | requires review because a directly verified source page was not captured for the curated fallback pack | no |

## Evidence Coverage Assessment

- Strongest evidence category: official_primary
- Weakest evidence category: live retrieval status
- Missing evidence: None identified
- Contrary/stabilising evidence: Present
- Confidence impact: Confidence capped because the run used a curated fallback source pack rather than live API retrieval.

## Route-Cost Assumptions

- Direct, delay and reroute comparisons use illustrative voyage assumptions requiring operator validation.
- Validate voyage days, bunker burn, daily vessel cost, war-risk premiums, demurrage and compliance hold assumptions before route approval.
- Sanctions risk should be treated as a legal override, not just a line item in the direct-route cost stack.

## Refresh Triggers

- Refresh before major underwriting or commercial decisions.
- Refresh before major underwriting or commercial decisions.
- Refresh before major underwriting or commercial decisions.
- Refresh before major underwriting or commercial decisions.
- Refresh before major underwriting or commercial decisions.
- Refresh before major underwriting or commercial decisions.

## Analyst Review Controls

- Verify publication dates.
- Verify fetched content against source page.
- Check source freshness.
- Check carrier/company updates remain current.
- Check market pricing recency.
- Check de-escalation reporting.
- Check sanctions/legal implications.
