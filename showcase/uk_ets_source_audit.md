# Source Audit

## Search Configuration

- Topic: UK ETS Maritime Expansion and carbon cost exposure for shipping operators
- Business user: shipping_operator
- Region: UK domestic maritime
- Time horizon: 1-12 months
- Concerns: carbon cost exposure, reporting deadline, allowance surrender obligation, UKA price movement, voyage cost pass-through, competitiveness, future international expansion, route applicability, compliance failure
- Search provider used: tavily
- Evidence mode: Live source retrieval
- Fallback data used: false
- Provider error: None
- Retrieval timestamp: 2026-05-28T16:54:46

## Research Plan

- Research objective: Build a governed evidence base for shipping_operator decision-making on UK ETS Maritime Expansion and carbon cost exposure for shipping operators in UK domestic maritime over 1-12 months, using the regulatory_carbon_shipping domain pack.
- Decision questions:
  - Does UK ETS apply to this vessel and route today, or only as a future scenario?
  - What is the quantified voyage-level carbon cost exposure at current UKA assumptions?
  - Are reporting and surrender processes ready for the first compliance periods?
  - Can the operator pass carbon cost through, or will margins absorb it?
  - Does UK ETS apply to this vessel and route?
  - Is the voyage domestic UK, at-berth, offshore or international?
  - Is the route inside the confirmed 2026 scope or only a future scenario?
  - When must emissions be reported?
  - When must allowances be surrendered?
  - Is the first surrender affected by the double-surrender window?
  - What UKA price should be used?
  - How sensitive is voyage cost to UKA price movement?
  - Which emissions factor should be used for the selected fuel?
  - What is the estimated tCO2e per voyage?
  - How are operators preparing?
  - Are carbon costs being passed through to customers?
  - Which operators or routes are most exposed?
  - Which entity is responsible?
  - What documentation or MRV process is needed?
  - What uncertainties remain?
  - Could future expansion affect UK-international routes?
  - Which routes are confirmed in scope and which are scenario-only?
  - Is this route outside confirmed 2026 scope?
  - Are there exemptions or delayed implementation issues?
  - Should a route be treated as scenario exposure rather than current obligation?
- Required source mix:
  - official policy scope source
  - timeline / reporting source
  - carbon price source or manual fallback
  - emissions factor source
  - operator implementation guidance
  - legal practical analysis
  - future-scope evidence
  - scope-limiting evidence
- Expected evidence types: official_primary, official_guidance, market_indicator, specialist_analysis, reputable_news, contrary_or_stabilising_evidence
- Minimum acceptable coverage: {'minimum_total_requirements': 8, 'minimum_high_priority_requirements': 2, 'high_priority_requirements': ['official_policy_scope', 'reporting_surrender_timeline'], 'minimum_sources_per_requirement': {'REQ-UKETS-A': 1, 'REQ-UKETS-B': 1, 'REQ-UKETS-C': 1, 'REQ-UKETS-D': 1, 'REQ-UKETS-E': 1, 'REQ-UKETS-F': 1, 'REQ-UKETS-G': 1, 'REQ-UKETS-H': 1}}
- Refresh priorities:
  - official_policy_scope: Current policy response or implementation guidance, preferably within 90 days.
  - reporting_surrender_timeline: Current implementation guidance, preferably within 90 days.
  - carbon_price_evidence: Current market or clearly labelled manual fallback price.
  - emissions_factor_evidence: Current or still-valid conversion-factor guidance.
  - operator_guidance: Recent implementation commentary, preferably within 90 days.
  - legal_practical_analysis: Current legal/compliance analysis, preferably within 180 days.
  - future_scope_or_international_extension: Current consultation or policy-expansion evidence, preferably within 180 days.
  - contrary_or_scope_limited_evidence: Current scope-limiting guidance or implementation caveats.

## Source Strategy

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: official_policy_scope
- Evidence question: Does UK ETS apply to this vessel and route?
- Preferred domains: gov.uk, gov.scot, gov.wales, icapcarbonaction.com
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - GOV.UK UK ETS domestic maritime 1 July 2026 5000 GT UK ports
  - ICAP UK ETS domestic maritime 2026 5000 GT
  - site:gov.uk UK ETS Maritime Expansion and carbon cost exposure for shipping operators official policy scope 1-12 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current policy response or implementation guidance, preferably within 90 days.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: reporting_surrender_timeline
- Evidence question: When must emissions be reported?
- Preferred domains: gov.uk, lr.org, hfw.com
- Preferred source types: official_primary, specialist_analysis
- Generated queries:
  - GOV.UK UK ETS maritime verified annual emissions report 31 March 30 April 2028
  - LR UK ETS domestic maritime reporting surrender deadline 2026 2028
  - site:gov.uk UK ETS Maritime Expansion and carbon cost exposure for shipping operators reporting surrender timeline 1-12 months
  - UK ETS Maritime Expansion and carbon cost exposure for shipping operators reporting surrender timeline specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current implementation guidance, preferably within 90 days.

### reputable_news

- Why it matters: Corroborates current events and commercial impacts.
- Source requirement: carbon_price_evidence
- Evidence question: What UKA price should be used?
- Preferred domains: theice.com, market data sources, lloydslist.com, icapcarbonaction.com
- Preferred source types: market_indicator, reputable_news, specialist_analysis
- Generated queries:
  - UKA carbon price UK ETS allowance price maritime 2026
  - UK ETS allowance price manual fallback shipping operator
  - site:theice.com UK ETS Maritime Expansion and carbon cost exposure for shipping operators carbon price evidence 1-12 months
  - site:lloydslist.com UK ETS Maritime Expansion and carbon cost exposure for shipping operators carbon price evidence
  - UK ETS Maritime Expansion and carbon cost exposure for shipping operators carbon price evidence Reuters
- Minimum acceptable evidence: 1
- Refresh expectation: Current market or clearly labelled manual fallback price.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: emissions_factor_evidence
- Evidence question: Which emissions factor should be used for the selected fuel?
- Preferred domains: imo.org, gov.uk, lr.org
- Preferred source types: official_primary, specialist_analysis
- Generated queries:
  - IMO marine gas oil emission factor CO2 per tonne fuel
  - GOV.UK greenhouse gas conversion factor marine gas oil
  - site:imo.org UK ETS Maritime Expansion and carbon cost exposure for shipping operators emissions factor evidence 1-12 months
  - UK ETS Maritime Expansion and carbon cost exposure for shipping operators emissions factor evidence specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current or still-valid conversion-factor guidance.

### company_update

- Why it matters: Shows operational decisions by carriers or market participants.
- Source requirement: operator_guidance
- Evidence question: How are operators preparing?
- Preferred domains: maersk.com, lr.org, lloydslist.com, ukchamberofshipping.com
- Preferred source types: company_update, specialist_analysis, reputable_news
- Generated queries:
  - LR UK ETS domestic maritime operator guidance cost pass through
  - UK Chamber of Shipping UK ETS maritime operator exposure
  - site:maersk.com UK ETS Maritime Expansion and carbon cost exposure for shipping operators operator guidance 1-12 months
  - site:lloydslist.com UK ETS Maritime Expansion and carbon cost exposure for shipping operators operator guidance
  - UK ETS Maritime Expansion and carbon cost exposure for shipping operators operator guidance Reuters
- Minimum acceptable evidence: 1
- Refresh expectation: Recent implementation commentary, preferably within 90 days.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: legal_practical_analysis
- Evidence question: Which entity is responsible?
- Preferred domains: hfw.com, watsonfarley.com, nortonrosefulbright.com, stephensonharwood.com
- Preferred source types: specialist_analysis, official_guidance
- Generated queries:
  - HFW UK ETS domestic shipping 2026 compliance responsibility
  - Watson Farley UK ETS maritime domestic shipping 2026
  - site:hfw.com UK ETS Maritime Expansion and carbon cost exposure for shipping operators legal practical analysis 1-12 months
  - UK ETS Maritime Expansion and carbon cost exposure for shipping operators legal practical analysis specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current legal/compliance analysis, preferably within 180 days.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: future_scope_or_international_extension
- Evidence question: Could future expansion affect UK-international routes?
- Preferred domains: gov.uk, icapcarbonaction.com, icct.org
- Preferred source types: official_primary, specialist_analysis, contrary_or_stabilising_evidence
- Generated queries:
  - GOV.UK UK ETS international maritime consultation
  - ICAP UK ETS international maritime consultation domestic shipping
  - site:gov.uk UK ETS Maritime Expansion and carbon cost exposure for shipping operators future scope or international extension 1-12 months
  - UK ETS Maritime Expansion and carbon cost exposure for shipping operators future scope or international extension specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current consultation or policy-expansion evidence, preferably within 180 days.

### contrary_or_stabilising_evidence

- Why it matters: Tests the downside case and supports confidence discipline.
- Source requirement: contrary_or_scope_limited_evidence
- Evidence question: Is this route outside confirmed 2026 scope?
- Preferred domains: gov.uk, lr.org, hfw.com, icapcarbonaction.com
- Preferred source types: contrary_or_stabilising_evidence, official_primary, specialist_analysis
- Generated queries:
  - GOV.UK UK ETS maritime exemptions offshore delayed 2027
  - LR UK ETS domestic maritime exemptions international routes not in scope
  - site:gov.uk UK ETS Maritime Expansion and carbon cost exposure for shipping operators contrary or scope limited evidence 1-12 months
  - UK ETS Maritime Expansion and carbon cost exposure for shipping operators contrary or scope limited evidence specialist analysis
  - UK ETS Maritime Expansion and carbon cost exposure for shipping operators contrary or scope limited evidence scope limited stabilising contrary evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current scope-limiting guidance or implementation caveats.

## Search Results Summary

- Total candidate sources found: 78
- Total queries run: 34
- Total selected sources: 8
- Duplicate URLs removed: 0
- Source categories covered: company_update, contrary_or_stabilising_evidence, official_primary, reputable_news, specialist_analysis
- Source categories missing: None
- Fetch failures: 0

## Quantified Evidence Summary

- Source count: 8
- Source coverage: 100%
- High-weight source count: 3
- Quantified facts: 21
- Score support summary: Scores are supported by 8 selected sources, 100% requirement coverage and 21 extracted quantified facts.
- Confidence cap reason: Confidence capped below 5 because official policy evidence is strong, but the calculation uses illustrative voyage assumptions and a manual UKA price rather than an embedded live price feed.

## Source Requirement Coverage

| Requirement | Why Required | Covered By | Evidence Weight | Decision Questions Supported | Remaining Gap |
| --- | --- | --- | --- | --- | --- |
| official_policy_scope | Confirms whether the rule applies to the vessel, voyage and emissions type. | L1, L2, L4, L7 | high | Does UK ETS apply to this vessel and route?; Is the voyage domestic UK, at-berth, offshore or international?; Is the route inside the confirmed 2026 scope or only a future scenario? | No immediate coverage gap; analyst should still verify recency and source content. |
| reporting_surrender_timeline | Confirms MRV, reporting and allowance surrender deadlines. | L1, L2, L4, L6, L7 | high | When must emissions be reported?; When must allowances be surrendered?; Is the first surrender affected by the double-surrender window? | No immediate coverage gap; analyst should still verify recency and source content. |
| carbon_price_evidence | Provides the allowance price needed to calculate estimated carbon cost exposure. | L3, L6 | medium | What UKA price should be used?; How sensitive is voyage cost to UKA price movement? | No immediate coverage gap; analyst should still verify recency and source content. |
| emissions_factor_evidence | Converts fuel consumption into estimated emissions. | L1, L2, L4, L6, L7 | medium | Which emissions factor should be used for the selected fuel?; What is the estimated tCO2e per voyage? | No immediate coverage gap; analyst should still verify recency and source content. |
| operator_guidance | Shows how shipping operators and maritime advisers are interpreting and implementing the rule. | L3, L5, L6 | medium | How are operators preparing?; Are carbon costs being passed through to customers?; Which operators or routes are most exposed? | No immediate coverage gap; analyst should still verify recency and source content. |
| legal_practical_analysis | Explains obligations, exemptions, uncertainty and compliance approach. | L1, L2, L4, L6, L7 | medium | Which entity is responsible?; What documentation or MRV process is needed?; What uncertainties remain? | No immediate coverage gap; analyst should still verify recency and source content. |
| future_scope_or_international_extension | Captures the risk that future policy may expand to international voyages or wider emissions categories. | L1, L2, L4, L6, L7, L8 | medium | Could future expansion affect UK-international routes?; Which routes are confirmed in scope and which are scenario-only? | No immediate coverage gap; analyst should still verify recency and source content. |
| contrary_or_scope_limited_evidence | Prevents over-application to routes, vessels or emissions outside scope. | L1, L2, L4, L6, L7, L8 | medium | Is this route outside confirmed 2026 scope?; Are there exemptions or delayed implementation issues?; Should a route be treated as scenario exposure rather than current obligation? | No immediate coverage gap; analyst should still verify recency and source content. |

## Selected Sources

| Source ID | Requirement | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| L1 | official_policy_scope | GOV.UK UK ETS domestic maritime 1 July 2026 5000 GT UK ports | Does UK ETS apply to this vessel and route? | ICCT UK ETS Maritime Expansion Brief | 4 | 5 | 3 | 4 | 2 | 5 | high | direct topic match, fits specialist_analysis | Supports confirmed-versus-scenario scope classification for route economics. | ok | Policy context is useful, but operators should anchor live scope decisions in the latest UK ETS Authority wording. |
| L2 | reporting_surrender_timeline | GOV.UK UK ETS maritime verified annual emissions report 31 March 30 April 2028 | When must emissions be reported? | Stephenson Harwood UK ETS Maritime Detail Note | 4 | 5 | 3 | 4 | 3 | 5 | high | direct topic match, fits specialist_analysis | Supports reporting, monitoring and surrender-readiness planning. | snippet_used | Legal commentary helps with implementation detail, but final compliance steps should still be checked against Authority guidance. |
| L3 | carbon_price_evidence | site:lloydslist.com UK ETS Maritime Expansion and carbon cost exposure for shipping operators carbon price evidence | What UKA price should be used? | Lloyd's List UK ETS Domestic Shipping Consultation Report | 4 | 5 | 3 | 4 | 2 | 5 | medium | trusted domain, direct topic match, fits reputable_news | Supports manual UKA price governance and allowance-cost sensitivity discussion. | ok | This source supports policy and operator context rather than a live UKA market quote, so the calculator still uses a manual price input. |
| L4 | emissions_factor_evidence | UK ETS Maritime Expansion and carbon cost exposure for shipping operators emissions factor evidence specialist analysis | Which emissions factor should be used for the selected fuel? | Azolla UK ETS Shipping Scope, Costs and Compliance Note | 4 | 5 | 3 | 4 | 2 | 5 | medium | direct topic match, fits specialist_analysis | Supports emissions-factor choice and voyage-level carbon-cost calculation structure. | ok | Secondary guidance is helpful for framing assumptions, but the emissions factor should still be checked against verifier-approved methodology. |
| L5 | operator_guidance | site:lloydslist.com UK ETS Maritime Expansion and carbon cost exposure for shipping operators operator guidance | How are operators preparing? | Lloyd's List UK Shipping ETS Preparation Report | 5 | 5 | 3 | 4 | 2 | 5 | medium | trusted domain, direct topic match, fits company_update | Supports pass-through, customer-pricing and operator-readiness discussion. | ok | Operator-readiness commentary is commercially useful, but route-specific pass-through still depends on contract and customer terms. |
| L6 | legal_practical_analysis | HFW UK ETS domestic shipping 2026 compliance responsibility | Which entity is responsible? | HFW UK ETS Domestic Shipping Compliance Note | 3 | 5 | 3 | 4 | 2 | 5 | medium | direct topic match, fits specialist_analysis | Supports accountable-entity, MRV and compliance-governance review. | snippet_used | Legal analysis should be read alongside current Authority guidance and the operator's MRV process. |
| L7 | future_scope_or_international_extension | GOV.UK UK ETS international maritime consultation | Could future expansion affect UK-international routes? | GOV.UK UK ETS Maritime Scope Expansion | 4 | 5 | 3 | 3 | 2 | 5 | high | direct topic match, fits official_primary | Supports core policy confirmation for start date, route scope and future-scope separation. | ok | This is the strongest live scope anchor, but reporting and surrender detail should still be monitored for updates. |
| L8 | contrary_or_scope_limited_evidence | GOV.UK UK ETS maritime exemptions offshore delayed 2027 | Is this route outside confirmed 2026 scope? | Stephenson Harwood UK ETS Maritime Scope Update | 3 | 5 | 3 | 4 | 2 | 5 | medium | direct topic match, fits contrary_or_stabilising_evidence | Supports scope-limiting caveats and scenario-only treatment for future international expansion. | ok | Helpful for scope-limiting interpretation, but future international treatment remains policy-contingent. |

## Rejected Sources

| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |
| --- | --- | --- | ---: | --- | --- | --- |
| UK ETS to cover domestic maritime transport from July 2026 - LinkedIn | official_policy_scope | ICAP UK ETS domestic maritime 2026 5000 GT | 21 | independence_score | duplicate or near-duplicate | no |
| 06/2026: UK ETS extends to domestic maritime sector \| LR | official_policy_scope | ICAP UK ETS domestic maritime 2026 5000 GT | 21 | independence_score | duplicate or near-duplicate | no |
| Expanding the UK Emissions Trading Scheme to International ... | official_policy_scope | ICAP UK ETS domestic maritime 2026 5000 GT | 24 | independence_score | duplicate or near-duplicate | no |
| UK ETS for the Maritime Sector – Update – Part 1 of 2 - Clyde & Co | reporting_surrender_timeline | LR UK ETS domestic maritime reporting surrender deadline 2026 2028 | 22 | independence_score | duplicate or near-duplicate | no |
| UK ETS for maritime: Key takeaways and comparison with the EU ETS | reporting_surrender_timeline | LR UK ETS domestic maritime reporting surrender deadline 2026 2028 | 24 | independence_score | duplicate or near-duplicate | no |
| UK ETS Maritime Regulation: Timeline and Scope - OceanScore | reporting_surrender_timeline | UK ETS Maritime Expansion and carbon cost exposure for shipping operators reporting surrender timeline specialist analysis | 24 | independence_score | duplicate or near-duplicate | no |
| UK announces major policy decisions and launches new ... | carbon_price_evidence | UKA carbon price UK ETS allowance price maritime 2026 | 21 | independence_score | duplicate or near-duplicate | no |
| UK Emissions Trading Scheme (UK-ETS) Expansion to Shipping | emissions_factor_evidence | UK ETS Maritime Expansion and carbon cost exposure for shipping operators emissions factor evidence specialist analysis | 24 | independence_score | duplicate or near-duplicate | no |
| 06/2026: UK ETS extends to domestic maritime sector \| LR | operator_guidance | LR UK ETS domestic maritime operator guidance cost pass through | 21 | independence_score | duplicate or near-duplicate | no |
| UK Emissions Trading Scheme (UK-ETS) Expansion to Shipping | operator_guidance | UK Chamber of Shipping UK ETS maritime operator exposure | 24 | independence_score | duplicate or near-duplicate | no |

## Evidence Coverage Assessment

- Strongest evidence category: official_primary
- Weakest evidence category: None identified
- Missing evidence: None identified
- Contrary/stabilising evidence: Present
- Confidence impact: Evidence coverage supports higher confidence, subject to analyst review.

## Source Quality Notes

| Evidence area | Current source quality | Dashboard caveat |
| --- | --- | --- |
| Official / policy scope | Strong where GOV.UK / UK ETS Authority evidence is present. | Use official sources for implementation date, scope and vessel threshold. |
| Legal / compliance interpretation | Specialist analysis, not official policy. | Treat law-firm commentary as interpretation requiring legal review before operational use. |
| Carbon cost inputs | Illustrative until operator fuel burn, verifier methodology and current UKA price are confirmed. | Replace manual UKA price and illustrative fuel burn before commercial pricing decisions. |
| International-route exposure | Scenario-only unless confirmed by official evidence. | Keep UK-international exposure assumptions separate from confirmed domestic scope. |

## Route-Cost Assumptions

- Carbon-cost outputs use illustrative route, vessel, fuel-burn and UKA price assumptions that require operator sign-off.
- Validate route classification, responsible entity, fuel consumption and verifier methodology before relying on the estimate commercially.
- Refresh the manual UKA input before pricing, contracting or allowance procurement decisions.

## Refresh Triggers

- Refresh UKA price before pricing or contract decisions.
- Refresh UK ETS Authority guidance if maritime scope, reporting or surrender deadlines change.
- Validate operator-specific fuel burn and route classification before using the cost estimate commercially.
- Refresh future-scope assumptions if UK-international maritime expansion policy changes.
- Review emissions factor methodology with verifier / MRV process.

## Analyst Review Controls

- Verify publication dates.
- Verify fetched content against source page.
- Check source freshness.
- Check carrier/company updates remain current.
- Check market pricing recency.
- Check de-escalation reporting.
- Check sanctions/legal implications.
