# Source Audit

## Search Configuration

- Topic: Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk
- Business user: trade_finance_lender
- Region: UK trade finance / cross-border transaction screening
- Time horizon: 1-3 months
- Concerns: sanctions exposure, end-use controls, controlled goods risk, counterparty exposure, beneficial ownership opacity, jurisdiction and route exposure, payment red flags, documentation weakness, legal hold, transaction rejection
- Search provider used: tavily
- Evidence mode: Live source retrieval
- Fallback data used: false
- Provider error: None
- Retrieval timestamp: 2026-06-03T11:33:01

## Research Plan

- Research objective: Build a governed evidence base for trade_finance_lender decision-making on Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk in UK trade finance / cross-border transaction screening over 1-3 months, using the sanctions_trade_finance domain pack.
- Decision questions:
  - Should the lender approve, approve with enhanced due diligence, escalate, legally hold or reject the transaction?
  - Do goods, end-use, counterparty, ownership, route, payment or documentation red flags require escalation?
  - What evidence would justify approval or de-escalation after enhanced due diligence?
  - Should the lender approve, escalate, legally hold or reject the transaction?
  - Which UK sanctions or OFSI controls anchor the legal/compliance review?
  - Do goods, technology, dual-use status or end-use controls create a legal hold or rejection trigger?
  - Is licence, notification, authorisation or exemption evidence required?
  - Are counterparties, beneficial owners, banks, intermediaries, vessels or consignees clean enough for approval?
  - Does unclear ownership or sanctions screening trigger escalation?
  - Do countries, ports, transshipment patterns, diversion indicators or logistics route create a red flag?
  - Does route exposure require enhanced due diligence or legal hold?
  - Are transaction documents strong enough for approval or do gaps trigger escalation or hold?
  - Which missing documents must be obtained before drawdown?
  - What enforcement or penalty expectations make unresolved red flags unacceptable?
  - How should confidence and review controls reflect regulatory consequences?
  - How does sanctions risk affect transaction approval, drawdown, credit exposure, insurance or operational controls?
  - Which due diligence actions should be required before approval?
  - What evidence would justify approval or enhanced due diligence rather than legal hold?
  - Which official exemptions, licences, clean-screening results or document evidence would relax controls?
  - What transaction-specific goods, ownership, route, payment, licence and document data is required before a clearance decision?
- Required source mix:
  - UK sanctions / OFSI official guidance
  - sanctions end-use controls / controlled-goods risk
  - counterparty and ownership exposure
  - jurisdiction and route exposure
  - documentation and transaction-quality evidence
  - enforcement / penalty / regulatory expectation evidence
  - financial institution / trade finance operating impact
  - contrary / clearance evidence
  - company-data requirements / anti-overclaiming controls
- Expected evidence types: official_primary, official_guidance, specialist_analysis, reputable_news, contrary_or_stabilising_evidence
- Minimum acceptable coverage: {'minimum_total_requirements': 9, 'minimum_high_priority_requirements': 4, 'high_priority_requirements': ['uk_sanctions_ofsi_official_guidance', 'sanctions_end_use_controls_and_controlled_goods_risk', 'counterparty_and_ownership_exposure', 'sanctions_company_data_requirements_and_anti_overclaiming_controls'], 'minimum_sources_per_requirement': {'REQ-STF-A': 1, 'REQ-STF-B': 1, 'REQ-STF-C': 1, 'REQ-STF-D': 1, 'REQ-STF-E': 1, 'REQ-STF-F': 1, 'REQ-STF-G': 1, 'REQ-STF-H': 1, 'REQ-STF-I': 1}}
- Refresh priorities:
  - uk_sanctions_ofsi_official_guidance: Current official guidance, preferably checked within 30 days before transaction approval.
  - sanctions_end_use_controls_and_controlled_goods_risk: Current official export-control or sanctions end-use guidance, preferably checked within 30 days.
  - counterparty_and_ownership_exposure: Current sanctions-screening or financial-crime guidance.
  - jurisdiction_route_and_diversion_exposure: Current official typology or live reporting, preferably within 60 days.
  - documentation_and_transaction_quality_evidence: Current or maintained trade finance and compliance controls guidance.
  - enforcement_penalty_and_regulatory_expectations: Current official enforcement, strategy or penalty evidence.
  - financial_institution_trade_finance_operating_impact: Current or maintained financial-sector/trade-finance controls guidance.
  - contrary_clearance_or_de_escalation_evidence: Current official or specialist scope analysis.
  - sanctions_company_data_requirements_and_anti_overclaiming_controls: Current or maintained control guidance.

## Source Strategy

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: uk_sanctions_ofsi_official_guidance
- Evidence question: Should the lender approve, escalate, legally hold or reject the transaction?
- Preferred domains: gov.uk, ofsi.gov.uk, businessandtrade.gov.uk
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:gov.uk OFSI financial sanctions guidance UK trade finance sanctions compliance
  - site:gov.uk sanctions end-use controls guidance businesses UK
  - site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk uk sanctions ofsi official guidance 1-3 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current official guidance, preferably checked within 30 days before transaction approval.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: sanctions_end_use_controls_and_controlled_goods_risk
- Evidence question: Do goods, technology, dual-use status or end-use controls create a legal hold or rejection trigger?
- Preferred domains: gov.uk, businessandtrade.gov.uk, great.gov.uk, legislation.gov.uk
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:gov.uk sanctions end-use controls controlled goods licence notification
  - site:gov.uk strategic export controls dual-use goods end-use sanctions
  - site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk sanctions end use controls and controlled goods risk 1-3 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current official export-control or sanctions end-use guidance, preferably checked within 30 days.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: counterparty_and_ownership_exposure
- Evidence question: Are counterparties, beneficial owners, banks, intermediaries, vessels or consignees clean enough for approval?
- Preferred domains: gov.uk, ofsi.gov.uk, fatf-gafi.org, wolfsberg-principles.com
- Preferred source types: official_primary, specialist_analysis
- Generated queries:
  - site:gov.uk OFSI ownership and control sanctions guidance counterparty beneficial ownership
  - site:wolfsberg-principles.com sanctions screening trade finance beneficial ownership
  - site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk counterparty and ownership exposure 1-3 months
  - Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk counterparty and ownership exposure specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current sanctions-screening or financial-crime guidance.

### reputable_news

- Why it matters: Corroborates current events and commercial impacts.
- Source requirement: jurisdiction_route_and_diversion_exposure
- Evidence question: Do countries, ports, transshipment patterns, diversion indicators or logistics route create a red flag?
- Preferred domains: reuters.com, apnews.com, gov.uk, fatf-gafi.org
- Preferred source types: reputable_news, official_primary, specialist_analysis
- Generated queries:
  - site:reuters.com sanctions diversion third country route trade finance export controls
  - site:gov.uk sanctions circumvention diversion third countries export controls
  - site:reuters.com Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk jurisdiction route and diversion exposure 1-3 months
  - Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk jurisdiction route and diversion exposure specialist analysis
  - site:reuters.com Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk jurisdiction route and diversion exposure
- Minimum acceptable evidence: 1
- Refresh expectation: Current official typology or live reporting, preferably within 60 days.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: documentation_and_transaction_quality_evidence
- Evidence question: Are transaction documents strong enough for approval or do gaps trigger escalation or hold?
- Preferred domains: iccwbo.org, baft.org, wolfsberg-principles.com, gov.uk
- Preferred source types: financial_sector_guidance, specialist_analysis, official_primary
- Generated queries:
  - site:iccwbo.org trade finance sanctions due diligence documents bills of lading invoices
  - site:wolfsberg-principles.com trade finance sanctions due diligence documents
  - site:iccwbo.org Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk documentation and transaction quality evidence 1-3 months
  - Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk documentation and transaction quality evidence specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained trade finance and compliance controls guidance.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: enforcement_penalty_and_regulatory_expectations
- Evidence question: What enforcement or penalty expectations make unresolved red flags unacceptable?
- Preferred domains: gov.uk, ofsi.gov.uk, fca.org.uk, treasury.gov, justice.gov
- Preferred source types: official_primary, specialist_analysis
- Generated queries:
  - site:gov.uk OFSI financial sanctions enforcement penalties guidance
  - site:ofsi.blog.gov.uk OFSI strategy enforcement financial sanctions compliance
  - site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk enforcement penalty and regulatory expectations 1-3 months
  - Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk enforcement penalty and regulatory expectations specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current official enforcement, strategy or penalty evidence.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: financial_institution_trade_finance_operating_impact
- Evidence question: How does sanctions risk affect transaction approval, drawdown, credit exposure, insurance or operational controls?
- Preferred domains: wolfsberg-principles.com, baft.org, iccwbo.org, fca.org.uk, ofsi.gov.uk
- Preferred source types: specialist_analysis, financial_sector_guidance, official_primary
- Generated queries:
  - site:wolfsberg-principles.com trade finance sanctions controls financial institutions
  - site:baft.org trade finance sanctions compliance controls
  - site:wolfsberg-principles.com Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk financial institution trade finance operating impact 1-3 months
  - Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk financial institution trade finance operating impact specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained financial-sector/trade-finance controls guidance.

### contrary_or_stabilising_evidence

- Why it matters: Tests the downside case and supports confidence discipline.
- Source requirement: contrary_clearance_or_de_escalation_evidence
- Evidence question: What evidence would justify approval or enhanced due diligence rather than legal hold?
- Preferred domains: gov.uk, ofsi.gov.uk, skadden.com, bakermckenzie.com, akingump.com
- Preferred source types: contrary_or_stabilising_evidence, official_primary, specialist_analysis
- Generated queries:
  - site:gov.uk sanctions licence exemption authorisation guidance trade goods
  - site:bakermckenzie.com UK sanctions end-use controls licence exemption scope analysis
  - site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk contrary clearance or de escalation evidence 1-3 months
  - site:skadden.com Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk contrary clearance or de escalation evidence
  - Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk contrary clearance or de escalation evidence scope limited stabilising contrary evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current official or specialist scope analysis.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: sanctions_company_data_requirements_and_anti_overclaiming_controls
- Evidence question: What transaction-specific goods, ownership, route, payment, licence and document data is required before a clearance decision?
- Preferred domains: gov.uk, ofsi.gov.uk, wolfsberg-principles.com, iccwbo.org
- Preferred source types: specialist_analysis, official_primary, financial_sector_guidance
- Generated queries:
  - site:wolfsberg-principles.com trade finance sanctions due diligence customer transaction data
  - site:iccwbo.org trade finance due diligence transaction documents sanctions
  - site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk sanctions company data requirements and anti overclaiming controls 1-3 months
  - Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk sanctions company data requirements and anti overclaiming controls specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained control guidance.

## Search Results Summary

- Total candidate sources found: 76
- Total queries run: 36
- Total selected sources: 9
- Duplicate URLs removed: 0
- Source categories covered: contrary_or_stabilising_evidence, official_primary, reputable_news, specialist_analysis
- Source categories missing: None
- Fetch failures: 1

## Quantified Evidence Summary

- Source count: 9
- Requirements identified: 9/9
- Strongly covered: 0/9
- Direct snippet-only: 0/9
- Partial or indirect: 9/9
- Historical/context only: 0/9
- Missing: 0/9
- High-weight source count: 0
- Quantified facts: 9
- Score support summary: Scores are supported by 9 selected sources, 100% requirement coverage and 53 extracted quantified facts.
- Confidence cap reason: Confidence capped at 3/5 because live public evidence is strong enough for a client-type screen, but transaction-specific goods, counterparty, ownership, route, payment, licence and document data are missing.

## Provenance And Extraction Limits

| Source ID | Evidence mode | Fetch status | Inference strength | Extraction confidence | Human review | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| L1 |  | ok |  |  | false |  |
| L2 |  | ok |  |  | false |  |
| L3 |  | ok |  |  | false |  |
| L4 |  | failed |  |  | false |  |
| L5 |  | ok |  |  | false |  |
| L6 |  | ok |  |  | false |  |
| L7 |  | ok |  |  | false |  |
| L8 |  | ok |  |  | false |  |
| L9 |  | snippet_used |  |  | false |  |

## Scoring Traceability

| Dimension | Score | Label | Score Type | Confidence | Supporting Evidence | Weakening Evidence | Evidence Quality Limits | Missing Evidence | Cap / Review Reason |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| likelihood | 4 | High | analyst_assumption | high | L1, L2, L3, L5, L6 | L8 | None | None |  |
| impact | 4 | High | analyst_assumption | high | L3, L7 | L8 | None | None |  |
| immediacy | 4 | High | analyst_assumption | high | L1, L2, L3 | L8 | None | None |  |
| exposure | 4 | High | analyst_assumption | high | L1, L3, L4, L5, L7, L8, L9 | L8 | None | None |  |
| confidence | 3 | Moderate | analyst_assumption | high | L1, L2, L7 | L8 | None | None | Capped because Confidence capped at 3/5 because live public evidence is strong enough for a client-type screen, but transaction-specific goods, counterparty, ownership, route, payment, licence and document data are missing. |
| decision_urgency | 4 | High | analyst_assumption | high | L1, L2, L5, L6 | L8 | None | None |  |

## Evidence-To-Score Bridge

| Dimension | Score | Evidence Basis | Confidence Effect | Cap Reason |
| --- | ---: | --- | --- | --- |
| likelihood | 4 | Likelihood is driven by official UK sanctions/end-use guidance, controlled-goods risk, ownership/counterparty exposure and live route/diversion indicators. |  | Confidence capped at 3/5 because live public evidence is strong enough for a client-type screen, but transaction-specific goods, counterparty, ownership, route, payment, licence and document data are missing. |
| impact | 4 | Impact is driven by legal hold/rejection risk, payment blockage, documentation failure, credit exposure, insurance/underwriting exclusion and regulatory penalty consequences. |  | Confidence capped at 3/5 because live public evidence is strong enough for a client-type screen, but transaction-specific goods, counterparty, ownership, route, payment, licence and document data are missing. |
| immediacy | 4 | Immediacy is high because checks must be resolved before approval, drawdown, document honouring or payment execution. |  | Confidence capped at 3/5 because live public evidence is strong enough for a client-type screen, but transaction-specific goods, counterparty, ownership, route, payment, licence and document data are missing. |
| confidence | 3 | Confidence is capped because public evidence does not include transaction-specific goods, ownership, screening, route, payment, licence or document data. |  | Confidence capped at 3/5 because live public evidence is strong enough for a client-type screen, but transaction-specific goods, counterparty, ownership, route, payment, licence and document data are missing. |

## Source Requirement Coverage

- Requirements identified: 9/9
- Strongly covered: 0/9
- Direct snippet-only: 0/9
- Partial or indirect: 9/9
- Historical/context only: 0/9
- Missing: 0/9

| Requirement | Coverage Grade | Supporting Sources | Reason For Grade | Remaining Gap | Gap Affects Confidence |
| --- | --- | --- | --- | --- | --- |
| uk_sanctions_ofsi_official_guidance | high | L1, L6 | Anchors UK legal and compliance relevance for a trade finance lender, bank or credit insurer. | Official guidance is strong, but must be refreshed before live transaction approval. | false |
| sanctions_end_use_controls_and_controlled_goods_risk | high | L1, L2 | Identifies goods, technology, dual-use or end-use red flags that can block approval or require a licence. | Goods classification and licence status still require transaction-specific validation. | false |
| counterparty_and_ownership_exposure | high | L3, L9 | Tests buyer, seller, beneficial owner, bank, intermediary, vessel or consignee exposure before financing. | Public guidance cannot clear named parties; sanctions screening and ownership records are required. | false |
| jurisdiction_route_and_diversion_exposure | medium | L4, L1 | Identifies countries, ports, transshipment, diversion or route red flags that can shift approval into escalation or hold. | Requires current route, port, transshipment and diversion checks before operational use. | false |
| documentation_and_transaction_quality_evidence | medium | L5, L9 | Shows which bills of lading, invoices, end-user statements, ownership declarations, vessel data and payment instructions are needed. | Actual invoices, bills of lading, contracts, end-use statements and payment instructions are required. | false |
| enforcement_penalty_and_regulatory_expectations | medium | L6, L3 | Shows consequences and standards expected by regulators when sanctions controls fail. | Regulatory expectations are clear; transaction-specific breach exposure requires legal review. | false |
| financial_institution_trade_finance_operating_impact | medium | L5, L7, L9 | Explains how sanctions risk affects financing approval, credit exposure, insurance and operational controls. | BAFT source is weaker; use internal policy and formal ICC/Wolfsberg/BAFT principles before operational use. | false |
| contrary_clearance_or_de_escalation_evidence | medium | L8 | Identifies evidence that would support approval or de-escalation, such as clean counterparties, licences, reliable documents, non-controlled goods or official exemptions. | Exceptions or licences support de-escalation only if they match exact transaction facts. | false |
| sanctions_company_data_requirements_and_anti_overclaiming_controls | high | L9, L3 | Makes clear what cannot be concluded from public sources alone and what transaction data is required for clearance. | Transaction-specific goods, counterparty, ownership, route, payment, licence and document data remain required. | false |

## Source Quality Notes

| Evidence area | Current source quality | Action before operational use |
| --- | --- | --- |
| UK sanctions / OFSI anchor | Official guidance supports legal and compliance relevance. | Refresh if sanctions designations, OFSI guidance or export-control rules change. |
| End-use and controlled goods | Regulatory guidance supports hold/escalation triggers but not transaction clearance. | Confirm goods classification, licence and end-use data. |
| Counterparty and ownership | Official ownership/control guidance is strong, but named-party screening is private. | Refresh screening and beneficial ownership data before approval. |
| Documentation quality | Trade finance guidance supports document controls. | Transaction-specific use requires invoices, bills of lading, contracts, payment instructions and end-user statements. |
| Clearance / contrary evidence | Licences or exceptions can reduce risk only where exact conditions are met. | Treat exceptions as conditional, not an all-clear. |

## Selected Sources

| Source ID | Requirement | Source role | Source value | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| L1 | uk_sanctions_ofsi_official_guidance | official_anchor | Official UK guidance anchoring sanctions end-use controls and UK transaction escalation relevance. | site:gov.uk sanctions end-use controls guidance businesses UK | Should the lender approve, escalate, legally hold or reject the transaction? | GOV.UK Sanctions End-Use Controls Guidance for Businesses | 5 | 5 | 3 | 2 | 4 | 5 | medium | trusted domain, direct topic match, fits official_primary | Anchors UK sanctions screening, OFSI escalation and legal-hold thresholds for trade finance approval. | ok | Official guidance must be refreshed before approving a live transaction because sanctions scope and licensing practice can change. |
| L2 | sanctions_end_use_controls_and_controlled_goods_risk | regulatory_guidance | Official exporter notices and control updates supporting goods, licence and controlled-item review. | site:gov.uk sanctions end-use controls controlled goods licence notification | Do goods, technology, dual-use status or end-use controls create a legal hold or rejection trigger? | GOV.UK Notices to Exporters | 5 | 5 | 3 | 2 | 3 | 5 | medium | trusted domain, direct topic match, fits official_primary | Supports goods classification, controlled-goods checks and licence/authorisation hold triggers before drawdown. | ok | Notices must be checked against the exact goods, destination and transaction date. |
| L3 | counterparty_and_ownership_exposure | regulatory_guidance | Official financial sanctions guidance supporting ownership/control, reporting and counterparty-screening escalation. | site:gov.uk OFSI ownership and control sanctions guidance counterparty beneficial ownership | Are counterparties, beneficial owners, banks, intermediaries, vessels or consignees clean enough for approval? | GOV.UK UK Financial Sanctions General Guidance | 5 | 4 | 3 | 2 | 3 | 5 | medium | trusted domain, direct topic match, fits official_primary | Supports counterparty, beneficial ownership, intermediary, bank and consignee screening decisions. | ok | Public guidance does not clear a named counterparty; transaction-specific screening and ownership data are still required. |
| L4 | jurisdiction_route_and_diversion_exposure | specialist_interpretation | Specialist compliance interpretation from Reuters Practical Law; useful for route/diversion control framing but not official guidance. | site:reuters.com sanctions diversion third country route trade finance export controls | Do countries, ports, transshipment patterns, diversion indicators or logistics route create a red flag? | Reuters Practical Law Sanctions and Export Controls Compliance Roadmap | 4 | 5 | 3 | 3 | 2 | 5 | medium | trusted domain, direct topic match, fits reputable_news | Supports escalation where jurisdiction, route, transshipment or diversion indicators are unresolved. | failed | This is specialist interpretation rather than live official route intelligence; refresh Reuters/AP or official diversion evidence before operational reliance. |
| L5 | documentation_and_transaction_quality_evidence | financial_sector_guidance | Trade-finance focused guidance showing how sanctions risk interacts with letters of credit and bank document review. | site:iccwbo.org trade finance sanctions due diligence documents bills of lading invoices | Are transaction documents strong enough for approval or do gaps trigger escalation or hold? | ICC Academy Sanctions and Letters of Credit: What Banks Must Know | 4 | 5 | 3 | 3 | 2 | 5 | medium | trusted domain, direct topic match, fits specialist_analysis | Supports document-request and hold triggers for invoices, bills of lading, end-use statements and payment instructions. | ok | Useful operating guidance, but transaction documents must still be reviewed against internal policy and legal advice. |
| L6 | enforcement_penalty_and_regulatory_expectations | enforcement_evidence | Official OFSI strategy showing enforcement, licensing, suspected breach reporting and stronger compliance expectations. | site:ofsi.blog.gov.uk OFSI strategy enforcement financial sanctions compliance | What enforcement or penalty expectations make unresolved red flags unacceptable? | OFSI Strategy 2026-29 | 5 | 5 | 3 | 3 | 3 | 5 | medium | trusted domain, direct topic match, fits official_primary | Supports legal-hold and rejection thresholds by showing regulatory consequences and expected controls. | ok | Strategy evidence shows regulatory expectation, not a transaction-specific enforcement finding. |
| L7 | financial_institution_trade_finance_operating_impact | financial_sector_guidance | Financial-sector trade finance perspective; useful for operating impact but weaker than a formal regulator source. | site:baft.org trade finance sanctions compliance controls | How does sanctions risk affect transaction approval, drawdown, credit exposure, insurance or operational controls? | BAFT Trade Finance Compliance and KYC Resources | 4 | 5 | 3 | 3 | 2 | 5 | medium | trusted domain, direct topic match, fits specialist_analysis | Supports facility conditions, drawdown controls, credit exposure review and operational escalation. | ok | The selected BAFT page is a weak/secondary source and should be replaced with specific bank policy, ICC/Wolfsberg/BAFT principles or regulator guidance before operational use. |
| L8 | contrary_clearance_or_de_escalation_evidence | contrary_scope_limit | Official scope-limiting evidence showing that exceptions and licences can support approval only where conditions are met. | site:gov.uk sanctions licence exemption authorisation guidance trade goods | What evidence would justify approval or enhanced due diligence rather than legal hold? | GOV.UK How to Use Exceptions and Licences to Comply With Sanctions | 4 | 5 | 3 | 3 | 2 | 5 | medium | trusted domain, direct topic match, fits contrary_or_stabilising_evidence | Supports approval or enhanced due diligence only where clean counterparties, licences, exemptions and documents resolve red flags. | ok | Licence or exception evidence is not an all-clear; it must match the exact goods, counterparties, route and transaction facts. |
| L9 | sanctions_company_data_requirements_and_anti_overclaiming_controls | company_required_data | Trade-finance principles identifying transaction data and document controls required before banks can make a risk decision. | site:iccwbo.org trade finance due diligence transaction documents sanctions | What transaction-specific goods, ownership, route, payment, licence and document data is required before a clearance decision? | Wolfsberg Group, ICC and BAFT Trade Finance Principles | 4 | 5 | 3 | 2 | 3 | 5 | medium | trusted domain, direct topic match, fits specialist_analysis | Supports anti-overclaiming controls by showing the transaction data still required before clearance. | snippet_used | Principles are maintained guidance, not transaction clearance; internal risk appetite and legal/compliance sign-off remain required. |

## Rejected Sources

| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |
| --- | --- | --- | ---: | --- | --- | --- |
| Sanctions End-Use Controls: guidance for businesses - GOV.UK | sanctions_end_use_controls_and_controlled_goods_risk | site:gov.uk sanctions end-use controls controlled goods licence notification | 25 | independence_score | duplicate or near-duplicate | no |
| Sanctions End-Use Controls: guidance for businesses - GOV.UK | sanctions_end_use_controls_and_controlled_goods_risk | site:gov.uk strategic export controls dual-use goods end-use sanctions | 25 | independence_score | duplicate or near-duplicate | no |
| Assembly Questions with the Index Term Departmental responsibilities | counterparty_and_ownership_exposure | site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk counterparty and ownership exposure 1-3 months | 22 | independence_score | duplicate or near-duplicate | no |
| Sanctions End-Use Controls: guidance for businesses - GOV.UK | jurisdiction_route_and_diversion_exposure | site:gov.uk sanctions circumvention diversion third countries export controls | 22 | independence_score | duplicate or near-duplicate | no |
| Wolfsberg Group: Home | documentation_and_transaction_quality_evidence | site:wolfsberg-principles.com trade finance sanctions due diligence documents | 21 | independence_score | duplicate or near-duplicate | no |
| Sanctions in Trade Finance Masterclass: Real World Examples | documentation_and_transaction_quality_evidence | Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk documentation and transaction quality evidence specialist analysis | 21 | independence_score | duplicate or near-duplicate | no |
| Financial sanctions enforcement and monetary penalties guidance | enforcement_penalty_and_regulatory_expectations | site:gov.uk OFSI financial sanctions enforcement penalties guidance | 23 | independence_score | duplicate or near-duplicate | no |
| Assembly Questions with the Index Term Departmental responsibilities | enforcement_penalty_and_regulatory_expectations | site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk enforcement penalty and regulatory expectations 1-3 months | 22 | independence_score | duplicate or near-duplicate | no |
| Assembly Questions with the Index Term Children - AIMS Portal | enforcement_penalty_and_regulatory_expectations | site:gov.uk Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk enforcement penalty and regulatory expectations 1-3 months | 22 | independence_score | duplicate or near-duplicate | no |
| Sanctions Risk | enforcement_penalty_and_regulatory_expectations | Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk enforcement penalty and regulatory expectations specialist analysis | 23 | independence_score | duplicate or near-duplicate | no |

## Evidence Coverage Assessment

- Strongest evidence category: contrary_or_stabilising_evidence
- Weakest evidence category: None identified
- Missing evidence: None identified
- Contrary/stabilising evidence: Present
- Confidence impact: Evidence coverage supports higher confidence, subject to analyst review.

## Illustrative Route-Cost Scenario

- Scenario assumptions are case-specific and were not foregrounded in this business-user path.

## Refresh Triggers

- Refresh if sanctions designations, OFSI guidance or export-control rules change.
- Refresh if goods classification, licence, authorisation or end-use status changes.
- Refresh if sanctions screening, beneficial ownership, bank or intermediary data changes.
- Refresh when invoices, bills of lading, contracts, end-use statements or payment instructions change.
- Refresh before moving from legal hold or escalation back to approval.

## Analyst Review Controls

- Verify current OFSI, UK sanctions and export-control guidance before transaction approval.
- Confirm goods classification, end-use, counterparty, ownership, route and payment data.
- Escalate unresolved red flags to sanctions/export-control legal review.
- Treat source evidence as a client-type exposure screen, not a transaction clearance decision.
- Require internal risk appetite and legal/compliance sign-off before approval or release.
