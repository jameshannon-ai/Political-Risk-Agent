# Source Audit

## Search Configuration

- Topic: Sanctions End-Use Controls affecting trade finance
- Business user: trade_finance_lender
- Region: UK / EU
- Time horizon: 1-3 months
- Concerns: sanctions exposure, diversion through third countries, counterparty risk, payment disruption, documentation risk, collateral risk, licensing delay, regulatory penalties
- Search provider used: fallback_demo_search
- Fallback data used: true
- Retrieval timestamp: 2026-05-28T12:34:42

## Research Plan

- Research objective: Build a governed evidence base for trade_finance_lender decision-making on Sanctions End-Use Controls affecting trade finance in UK / EU over 1-3 months, using the sanctions_trade_finance domain pack.
- Decision questions:
  - Does the transaction create sanctions end-use exposure?
  - Does the route, counterparty or goods profile suggest diversion risk?
  - Could payment be delayed, blocked or rejected?
  - What evidence would justify approval after enhanced due diligence?
  - Has a government notification or licensing trigger been identified?
  - Does the lender need to hold, escalate or decline the transaction?
  - Is the transaction connected to a sanctioned destination, person or restricted trade route?
  - Does the transaction raise Russia or sanctioned-territory diversion risk?
  - Are the goods or technology sensitive enough to require enhanced due diligence?
  - Does the lender need specialist export-control review before financing?
  - What practical checks should the lender require?
  - Which transaction features should trigger legal/compliance escalation?
  - Does the transaction involve a route, counterparty or goods profile associated with diversion?
  - Should the lender require enhanced end-use documentation?
  - Should the lender require sanctions screening, correspondent-bank confirmation or facility conditions?
  - Is the risk specific and controllable rather than automatically prohibitive?
- Required source mix:
  - official sanctions guidance
  - sanctions regime context
  - export-control / dual-use guidance
  - legal practical analysis
  - trade-route / diversion evidence
  - banking and payment-risk evidence
  - scope-limited or contrary evidence
- Expected evidence types: official_primary, official_guidance, specialist_analysis, reputable_news, contrary_or_stabilising_evidence
- Minimum acceptable coverage: {'minimum_total_requirements': 7, 'minimum_high_priority_requirements': 3, 'high_priority_requirements': ['official_sanctions_guidance', 'sanctions_regime_context', 'export_control_and_dual_use_risk'], 'minimum_sources_per_requirement': {'REQ-STF-A': 1, 'REQ-STF-B': 1, 'REQ-STF-C': 1, 'REQ-STF-D': 1, 'REQ-STF-E': 1, 'REQ-STF-F': 1, 'REQ-STF-G': 1}}
- Refresh priorities:
  - official_sanctions_guidance: Current official guidance, preferably checked within 30 days before transaction approval.
  - sanctions_regime_context: Current sanctions regime guidance, preferably checked within 30 days.
  - export_control_and_dual_use_risk: Current official goods classification or export-control evidence.
  - legal_practical_analysis: Recent legal or compliance analysis, preferably within 90 days.
  - trade_route_and_diversion_risk: Recent diversion typology or sanctions evasion reporting, preferably within 90 days.
  - banking_and_payment_risk: Current banking compliance guidance or payment-risk evidence.
  - contrary_or_scope_limited_evidence: Current official or legal scope analysis.

## Source Strategy

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: official_sanctions_guidance
- Evidence question: Does the transaction create sanctions end-use exposure?
- Preferred domains: gov.uk, ofsi.gov.uk, businessandtrade.gov.uk
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:gov.uk Sanctions End-Use Controls affecting trade finance official sanctions guidance 1-3 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current official guidance, preferably checked within 30 days before transaction approval.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: sanctions_regime_context
- Evidence question: Is the transaction connected to a sanctioned destination, person or restricted trade route?
- Preferred domains: gov.uk, legislation.gov.uk, ofsi.gov.uk
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:gov.uk Sanctions End-Use Controls affecting trade finance sanctions regime context 1-3 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current sanctions regime guidance, preferably checked within 30 days.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: export_control_and_dual_use_risk
- Evidence question: Are the goods or technology sensitive enough to require enhanced due diligence?
- Preferred domains: gov.uk, great.gov.uk, legislation.gov.uk
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:gov.uk Sanctions End-Use Controls affecting trade finance export control and dual use risk 1-3 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current official goods classification or export-control evidence.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: legal_practical_analysis
- Evidence question: What practical checks should the lender require?
- Preferred domains: skadden.com, akingump.com, bakermckenzie.com, eversheds-sutherland.com, ashurst.com, osborneclarke.com
- Preferred source types: specialist_analysis
- Generated queries:
  - site:skadden.com Sanctions End-Use Controls affecting trade finance legal practical analysis 1-3 months
  - site:skadden.com Sanctions End-Use Controls affecting trade finance legal practical analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Recent legal or compliance analysis, preferably within 90 days.

### reputable_news

- Why it matters: Corroborates current events and commercial impacts.
- Source requirement: trade_route_and_diversion_risk
- Evidence question: Does the transaction involve a route, counterparty or goods profile associated with diversion?
- Preferred domains: reuters.com, ft.com, theguardian.com, gov.uk, sanctions-related official advisories
- Preferred source types: reputable_news, official_primary, specialist_analysis
- Generated queries:
  - site:reuters.com Sanctions End-Use Controls affecting trade finance trade route and diversion risk 1-3 months
  - Sanctions End-Use Controls affecting trade finance trade route and diversion risk specialist analysis
  - site:reuters.com Sanctions End-Use Controls affecting trade finance trade route and diversion risk
- Minimum acceptable evidence: 1
- Refresh expectation: Recent diversion typology or sanctions evasion reporting, preferably within 90 days.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: banking_and_payment_risk
- Evidence question: Could payment be delayed, blocked or rejected?
- Preferred domains: wolfsberg-principles.com, fatf-gafi.org, ofsi.gov.uk, reuters.com, legal/compliance analysis sources
- Preferred source types: specialist_analysis, official_primary, reputable_news
- Generated queries:
  - site:wolfsberg-principles.com Sanctions End-Use Controls affecting trade finance banking and payment risk 1-3 months
  - Sanctions End-Use Controls affecting trade finance banking and payment risk specialist analysis
  - site:reuters.com Sanctions End-Use Controls affecting trade finance banking and payment risk
- Minimum acceptable evidence: 1
- Refresh expectation: Current banking compliance guidance or payment-risk evidence.

### contrary_or_stabilising_evidence

- Why it matters: Tests the downside case and supports confidence discipline.
- Source requirement: contrary_or_scope_limited_evidence
- Evidence question: What evidence would justify approval after enhanced due diligence?
- Preferred domains: gov.uk, legal analysis sources, official guidance
- Preferred source types: contrary_or_stabilising_evidence, official_primary, specialist_analysis
- Generated queries:
  - site:gov.uk Sanctions End-Use Controls affecting trade finance contrary or scope limited evidence 1-3 months
  - Sanctions End-Use Controls affecting trade finance contrary or scope limited evidence specialist analysis
  - Sanctions End-Use Controls affecting trade finance contrary or scope limited evidence scope limited stabilising contrary evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current official or legal scope analysis.

## Search Results Summary

- Total candidate sources found: 27
- Total selected sources: 6
- Duplicate URLs removed: 0
- Source categories covered: contrary_or_stabilising_evidence, official_primary, specialist_analysis
- Source categories missing: reputable_news
- Fetch failures: 0

## Quantified Evidence Summary

- Source count: 6
- Source coverage: 100%
- High-weight source count: 0
- Quantified facts: 2
- Score support summary: Scores are supported by 6 selected sources, 100% requirement coverage and 2 extracted quantified facts.
- Confidence cap reason: Confidence capped below 5 because evidence came from a reproducible curated source pack rather than live retrieval.

## Source Requirement Coverage

| Requirement | Why Required | Covered By | Evidence Weight | Decision Questions Supported | Remaining Gap |
| --- | --- | --- | --- | --- | --- |
| official_sanctions_guidance | Defines the legal and regulatory basis for sanctions end-use controls, including when exporters or counterparties may need a licence or compliance escalation. | SANCTIONS-001, SANCTIONS-002, SANCTIONS-003 | high | Does the transaction create sanctions end-use exposure?; Has a government notification or licensing trigger been identified?; Does the lender need to hold, escalate or decline the transaction? | No immediate coverage gap; analyst should still verify recency and source content. |
| sanctions_regime_context | Shows how end-use controls sit inside wider UK sanctions regimes, especially Russia-related trade restrictions and circumvention controls. | SANCTIONS-001, SANCTIONS-002, SANCTIONS-003 | high | Is the transaction connected to a sanctioned destination, person or restricted trade route?; Does the transaction raise Russia or sanctioned-territory diversion risk? | No immediate coverage gap; analyst should still verify recency and source content. |
| export_control_and_dual_use_risk | Identifies whether goods or technology may be sensitive, dual-use, strategically controlled or vulnerable to diversion. | SANCTIONS-001, SANCTIONS-002, SANCTIONS-003 | high | Are the goods or technology sensitive enough to require enhanced due diligence?; Does the lender need specialist export-control review before financing? | No immediate coverage gap; analyst should still verify recency and source content. |
| legal_practical_analysis | Explains how the rules operate in practice, including timing, notification, licensing, due diligence and business obligations. | SANCTIONS-004, SANCTIONS-007 | medium | What practical checks should the lender require?; Which transaction features should trigger legal/compliance escalation? | No immediate coverage gap; analyst should still verify recency and source content. |
| trade_route_and_diversion_risk | Identifies third-country diversion patterns, suspicious routing, end-use opacity and circumvention indicators. | SANCTIONS-001, SANCTIONS-002, SANCTIONS-003, SANCTIONS-004, SANCTIONS-007 | medium | Does the transaction involve a route, counterparty or goods profile associated with diversion?; Should the lender require enhanced end-use documentation? | No immediate coverage gap; analyst should still verify recency and source content. |
| banking_and_payment_risk | Links sanctions exposure to payment execution, correspondent banking, blocked payment risk, facility drawdown and transaction settlement. | SANCTIONS-001, SANCTIONS-002, SANCTIONS-003, SANCTIONS-004, SANCTIONS-007 | medium | Could payment be delayed, blocked or rejected?; Should the lender require sanctions screening, correspondent-bank confirmation or facility conditions? | No immediate coverage gap; analyst should still verify recency and source content. |
| contrary_or_scope_limited_evidence | Prevents over-escalation by identifying where controls apply only after a notification, where goods are outside scope, or where documentation mitigates risk. | SANCTIONS-001, SANCTIONS-002, SANCTIONS-003, SANCTIONS-004, SANCTIONS-007, SANCTIONS-008 | medium | What evidence would justify approval after enhanced due diligence?; Is the risk specific and controllable rather than automatically prohibitive? | No immediate coverage gap; analyst should still verify recency and source content. |

## Selected Sources

| Source ID | Requirement | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| SANCTIONS-001 | official_sanctions_guidance | site:gov.uk Sanctions End-Use Controls affecting trade finance official sanctions guidance 1-3 months | Does the transaction create sanctions end-use exposure? | Sanctions end-use controls guidance for businesses | 4 | 5 | 4 | 2 | 4 | 5 | medium | direct topic match, fits official_primary, recent source | Supports enhanced referral and route-level controls. | demo | Official guidance should be checked for updates before approving live transactions. |
| SANCTIONS-002 | sanctions_regime_context | site:gov.uk Sanctions End-Use Controls affecting trade finance official sanctions guidance 1-3 months | Does the transaction create sanctions end-use exposure? | Russia sanctions: guidance | 4 | 5 | 5 | 2 | 3 | 5 | medium | direct topic match, fits official_primary, recent source | Supports enhanced referral and route-level controls. | demo | Regime guidance is broad; transaction-specific legal analysis may still be required. |
| SANCTIONS-003 | export_control_and_dual_use_risk | site:gov.uk Sanctions End-Use Controls affecting trade finance official sanctions guidance 1-3 months | Does the transaction create sanctions end-use exposure? | UK Trade Tariff | 4 | 5 | 5 | 2 | 2 | 5 | medium | direct topic match, fits official_primary, recent source | Supports enhanced referral and route-level controls. | demo | Tariff classification is an input to controls review and does not replace specialist export-control advice. |
| SANCTIONS-004 | legal_practical_analysis | site:skadden.com Sanctions End-Use Controls affecting trade finance legal practical analysis 1-3 months | What practical checks should the lender require? | UK Introduces Sanctions End-Use Controls | 3 | 5 | 5 | 2 | 2 | 5 | medium | direct topic match, fits specialist_analysis, recent source | Supports scenario framing and market interpretation. | demo | Legal analysis should support but not replace internal counsel or official guidance. |
| SANCTIONS-007 | banking_and_payment_risk | site:skadden.com Sanctions End-Use Controls affecting trade finance legal practical analysis 1-3 months | What practical checks should the lender require? | OFSI Strategy 2026-29 | 3 | 5 | 4 | 3 | 2 | 5 | medium | direct topic match, fits specialist_analysis, recent source | Supports scenario framing and market interpretation. | demo | OFSI strategy is a control and enforcement signal rather than transaction-specific payment evidence. |
| SANCTIONS-008 | contrary_or_scope_limited_evidence | site:gov.uk Sanctions End-Use Controls affecting trade finance contrary or scope limited evidence 1-3 months | What evidence would justify approval after enhanced due diligence? | UK Introduces Sanctions End-Use Controls | 3 | 5 | 5 | 2 | 2 | 5 | medium | direct topic match, fits contrary_or_stabilising_evidence, recent source | Informs relaxation triggers without automatically reducing controls. | demo | Scope-limited evidence must be validated against official guidance and transaction-specific facts. |

## Rejected Sources

| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |
| --- | --- | --- | ---: | --- | --- | --- |
| Sanctions end-use controls guidance for businesses | official_sanctions_guidance | site:gov.uk Sanctions End-Use Controls affecting trade finance sanctions regime context 1-3 months | 25 | independence_score | duplicate or near-duplicate | no |
| Russia sanctions: guidance | sanctions_regime_context | site:gov.uk Sanctions End-Use Controls affecting trade finance sanctions regime context 1-3 months | 25 | independence_score | duplicate or near-duplicate | no |
| UK Trade Tariff | export_control_and_dual_use_risk | site:gov.uk Sanctions End-Use Controls affecting trade finance sanctions regime context 1-3 months | 24 | independence_score | duplicate or near-duplicate | no |
| Sanctions end-use controls guidance for businesses | official_sanctions_guidance | site:gov.uk Sanctions End-Use Controls affecting trade finance export control and dual use risk 1-3 months | 25 | independence_score | duplicate or near-duplicate | no |
| Russia sanctions: guidance | sanctions_regime_context | site:gov.uk Sanctions End-Use Controls affecting trade finance export control and dual use risk 1-3 months | 25 | independence_score | duplicate or near-duplicate | no |
| UK Trade Tariff | export_control_and_dual_use_risk | site:gov.uk Sanctions End-Use Controls affecting trade finance export control and dual use risk 1-3 months | 24 | independence_score | duplicate or near-duplicate | no |
| UK Introduces Sanctions End-Use Controls | legal_practical_analysis | site:skadden.com Sanctions End-Use Controls affecting trade finance legal practical analysis | 23 | independence_score | duplicate or near-duplicate | no |
| UK Introduces Sanctions End-Use Controls | legal_practical_analysis | site:skadden.com Sanctions End-Use Controls affecting trade finance legal practical analysis | 23 | independence_score | duplicate or near-duplicate | no |
| OFSI Strategy 2026-29 | banking_and_payment_risk | site:skadden.com Sanctions End-Use Controls affecting trade finance legal practical analysis | 23 | independence_score | duplicate or near-duplicate | no |
| UK Introduces Sanctions End-Use Controls | legal_practical_analysis | site:wolfsberg-principles.com Sanctions End-Use Controls affecting trade finance banking and payment risk 1-3 months | 23 | independence_score | duplicate or near-duplicate | no |

## Evidence Coverage Assessment

- Strongest evidence category: official_primary
- Weakest evidence category: reputable_news
- Missing evidence: reputable_news
- Contrary/stabilising evidence: Present
- Confidence impact: Confidence capped because the run used a curated fallback source pack rather than live API retrieval.

## Analyst Review Controls

- Verify publication dates.
- Verify fetched content against source page.
- Check source freshness.
- Check carrier/company updates remain current.
- Check market pricing recency.
- Check de-escalation reporting.
- Check sanctions/legal implications.
