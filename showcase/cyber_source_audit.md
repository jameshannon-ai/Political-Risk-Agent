# Source Audit

## Search Configuration

- Topic: Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services
- Business user: customer_facing_operator
- Region: UK business exposed to ransomware, state-linked cyber, supplier/MSP compromise and operational resilience risk
- Time horizon: 1-6 months
- Concerns: business interruption, ransomware, operational resilience, regulatory notification, cyber insurance claims, supplier MSP dependency, revenue at risk
- Search provider used: tavily
- Evidence mode: Live source retrieval
- Fallback data used: false
- Provider error: None
- Retrieval timestamp: 2026-06-03T12:18:49

## Research Plan

- Research objective: Build a governed evidence base for customer_facing_operator decision-making on Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services in UK business exposed to ransomware, state-linked cyber, supplier/MSP compromise and operational resilience risk over 1-6 months, using the cyber_business_interruption domain pack.
- Decision questions:
  - Can the operator absorb and recover from a cyber incident without unacceptable downtime, revenue loss, regulatory exposure, customer harm or insurance coverage failure?
  - Do outage, notification, insurance, supplier or customer-harm triggers require incident response, manual contingency, pause or resilience investment?
  - What evidence would justify moving from incident response or manual contingency back toward normal operations?
  - Is the UK cyber threat environment severe enough to justify heightened operational resilience controls?
  - Does ransomware or state-linked cyber activity create a credible interruption risk?
  - How common are cyber breaches or ransomware incidents for UK organisations?
  - Does prevalence support likelihood scoring for a UK customer-facing operator?
  - What should boards and senior managers do before or during cyber disruption?
  - Which governance expectations support resilience investment or escalation?
  - Do live or recent incidents show cyber attacks causing operational downtime or customer-service disruption?
  - Should the operator activate incident response, manual fallback or restoration prioritisation?
  - Does the incident trigger cyber insurance notice or claim readiness?
  - How should waiting periods, exclusions and policy wording affect the business decision?
  - Does personal data exposure or service disruption require regulator or affected-customer notification review?
  - Which source-supported notification triggers must be escalated to legal/compliance review?
  - Could supplier, MSP, cloud, payment or fulfilment dependency block recovery?
  - Should third-party dependency risk be escalated before normal operations resume?
  - Which resilience measures reduce business interruption impact?
  - What company-specific systems, revenue, policy wording, supplier and recovery data is needed before relying on the model?
- Required source mix:
  - UK official cyber threat / NCSC evidence
  - UK cyber breach prevalence data
  - board cyber governance / operational resilience expectations
  - ransomware or operational disruption evidence
  - cyber insurance / business interruption evidence
  - incident reporting / regulatory notification guidance
  - supplier / MSP dependency risk
  - contrary / mitigation evidence
  - company-data requirements / anti-overclaiming controls
- Expected evidence types: official_primary, official_guidance, reputable_news, specialist_analysis, insurance_market_evidence, contrary_or_stabilising_evidence
- Minimum acceptable coverage: {'minimum_total_requirements': 9, 'minimum_high_priority_requirements': 5, 'high_priority_requirements': ['uk_official_cyber_threat_ncsc_evidence', 'uk_cyber_breach_prevalence_data', 'ransomware_or_operational_disruption_evidence', 'incident_reporting_and_regulatory_notification_guidance', 'cyber_company_data_requirements_and_anti_overclaiming_controls'], 'minimum_sources_per_requirement': {'REQ-CYB-A': 1, 'REQ-CYB-B': 1, 'REQ-CYB-C': 1, 'REQ-CYB-D': 1, 'REQ-CYB-E': 1, 'REQ-CYB-F': 1, 'REQ-CYB-G': 1, 'REQ-CYB-H': 1, 'REQ-CYB-I': 1}}
- Refresh priorities:
  - uk_official_cyber_threat_ncsc_evidence: Current or maintained NCSC/GOV.UK threat evidence, preferably checked within 30 days before operational use.
  - uk_cyber_breach_prevalence_data: Latest official UK survey or maintained data source.
  - board_cyber_governance_and_resilience_expectations: Current or maintained governance/resilience guidance.
  - ransomware_or_operational_disruption_evidence: Current or recent incident reporting, preferably within 90 days.
  - cyber_insurance_business_interruption_evidence: Current insurance-market evidence or maintained broker/insurer guidance.
  - incident_reporting_and_regulatory_notification_guidance: Current official regulator guidance, checked before incident use.
  - supplier_msp_dependency_risk: Current third-party/supplier cyber risk evidence or maintained operational resilience guidance.
  - contrary_or_mitigation_evidence: Current official or specialist mitigation evidence.
  - cyber_company_data_requirements_and_anti_overclaiming_controls: Maintained guidance or implementation evidence.

## Source Strategy

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: uk_official_cyber_threat_ncsc_evidence
- Evidence question: Is the UK cyber threat environment severe enough to justify heightened operational resilience controls?
- Preferred domains: ncsc.gov.uk, gov.uk
- Preferred source types: official_primary
- Generated queries:
  - site:ncsc.gov.uk annual review ransomware UK organisations operational disruption
  - site:ncsc.gov.uk ransomware cyber threat UK organisations operational resilience
  - site:ncsc.gov.uk Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services uk official cyber threat ncsc evidence 1-6 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained NCSC/GOV.UK threat evidence, preferably checked within 30 days before operational use.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: uk_cyber_breach_prevalence_data
- Evidence question: How common are cyber breaches or ransomware incidents for UK organisations?
- Preferred domains: gov.uk, dcms.gov.uk
- Preferred source types: official_primary, specialist_analysis
- Generated queries:
  - site:gov.uk Cyber Security Breaches Survey 2026 UK business ransomware
  - site:gov.uk Cyber Security Breaches Survey UK businesses cyber breach prevalence ransomware
  - site:gov.uk Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services uk cyber breach prevalence data 1-6 months
  - Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services uk cyber breach prevalence data specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Latest official UK survey or maintained data source.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: board_cyber_governance_and_resilience_expectations
- Evidence question: What should boards and senior managers do before or during cyber disruption?
- Preferred domains: gov.uk, ncsc.gov.uk, fca.org.uk, bankofengland.co.uk
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:gov.uk Cyber Governance Code of Practice board cyber risk operational resilience
  - site:ncsc.gov.uk board cyber governance operational resilience incident response
  - site:gov.uk Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services board cyber governance and resilience expectations 1-6 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current or maintained governance/resilience guidance.

### reputable_news

- Why it matters: Corroborates current events and commercial impacts.
- Source requirement: ransomware_or_operational_disruption_evidence
- Evidence question: Do live or recent incidents show cyber attacks causing operational downtime or customer-service disruption?
- Preferred domains: reuters.com, apnews.com, ncsc.gov.uk
- Preferred source types: reputable_news, official_primary
- Generated queries:
  - site:reuters.com UK retailer cyber attack operational disruption ransomware
  - site:apnews.com UK ransomware operational disruption retailer customer service
  - site:reuters.com Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services ransomware or operational disruption evidence 1-6 months
  - site:reuters.com Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services ransomware or operational disruption evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current or recent incident reporting, preferably within 90 days.

### insurance_market_evidence

- Why it matters: Supports premium, reinsurance and underwriting assessment.
- Source requirement: cyber_insurance_business_interruption_evidence
- Evidence question: Does the incident trigger cyber insurance notice or claim readiness?
- Preferred domains: marsh.com, aon.com, wtwco.com, allianz.com, howdengroup.com, reuters.com
- Preferred source types: insurance_market_evidence, specialist_analysis
- Generated queries:
  - site:marsh.com cyber insurance business interruption waiting period ransomware UK
  - site:aon.com cyber insurance business interruption ransomware waiting period claims
  - site:wtwco.com cyber insurance business interruption ransomware claims
  - site:marsh.com Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services cyber insurance business interruption evidence 1-6 months
  - site:howdengroup.com Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services cyber insurance business interruption evidence
  - site:reuters.com Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services cyber insurance business interruption evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current insurance-market evidence or maintained broker/insurer guidance.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: incident_reporting_and_regulatory_notification_guidance
- Evidence question: Does personal data exposure or service disruption require regulator or affected-customer notification review?
- Preferred domains: ico.org.uk, gov.uk, fca.org.uk, bankofengland.co.uk
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:ico.org.uk personal data breach notification 72 hours UK cyber incident
  - site:ico.org.uk ransomware personal data breach notification customers
  - site:ico.org.uk Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services incident reporting and regulatory notification guidance 1-6 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current official regulator guidance, checked before incident use.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: supplier_msp_dependency_risk
- Evidence question: Could supplier, MSP, cloud, payment or fulfilment dependency block recovery?
- Preferred domains: ncsc.gov.uk, fca.org.uk, bankofengland.co.uk, reuters.com, apnews.com
- Preferred source types: specialist_analysis, reputable_news, official_primary
- Generated queries:
  - site:ncsc.gov.uk managed service provider cyber attack supply chain UK business disruption
  - site:fca.org.uk operational resilience third party supplier cyber incident outage
  - site:ncsc.gov.uk Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services supplier msp dependency risk 1-6 months
  - Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services supplier msp dependency risk specialist analysis
  - site:reuters.com Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services supplier msp dependency risk
- Minimum acceptable evidence: 1
- Refresh expectation: Current third-party/supplier cyber risk evidence or maintained operational resilience guidance.

### contrary_or_stabilising_evidence

- Why it matters: Tests the downside case and supports confidence discipline.
- Source requirement: contrary_or_mitigation_evidence
- Evidence question: What evidence would justify moving from incident response or manual contingency back toward normal operations?
- Preferred domains: ncsc.gov.uk, gov.uk, ico.org.uk, fca.org.uk, bankofengland.co.uk
- Preferred source types: contrary_or_stabilising_evidence, official_primary, specialist_analysis
- Generated queries:
  - site:ncsc.gov.uk ransomware recovery backup business continuity guidance
  - site:gov.uk cyber resilience actions business continuity recovery
  - site:ncsc.gov.uk Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services contrary or mitigation evidence 1-6 months
  - Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services contrary or mitigation evidence specialist analysis
  - Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services contrary or mitigation evidence scope limited stabilising contrary evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current official or specialist mitigation evidence.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: cyber_company_data_requirements_and_anti_overclaiming_controls
- Evidence question: What company-specific systems, revenue, policy wording, supplier and recovery data is needed before relying on the model?
- Preferred domains: ncsc.gov.uk, gov.uk, ico.org.uk, marsh.com, aon.com
- Preferred source types: specialist_analysis, official_primary
- Generated queries:
  - site:ncsc.gov.uk incident response plan business continuity recovery time objectives
  - site:marsh.com cyber insurance claim notice policy wording business interruption
  - site:ncsc.gov.uk Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services cyber company data requirements and anti overclaiming controls 1-6 months
  - Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services cyber company data requirements and anti overclaiming controls specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Maintained guidance or implementation evidence.

## Search Results Summary

- Total candidate sources found: 73
- Total queries run: 37
- Total selected sources: 9
- Duplicate URLs removed: 0
- Source categories covered: contrary_or_stabilising_evidence, insurance_market_evidence, official_primary, reputable_news
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
- High-weight source count: 4
- Quantified facts: 24
- Score support summary: Cyber business interruption scores are supported by official UK threat/prevalence/notification evidence, live retail incident reporting, cyber insurance evidence and a clearly labelled illustrative resilience model.
- Confidence cap reason: Confidence capped at 3/5 because company-specific systems, revenue, RTO/RPO, insurance wording, supplier dependency and incident facts are missing.

## Provenance And Extraction Limits

| Source ID | Evidence mode | Fetch status | Inference strength | Extraction confidence | Human review | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| L1 |  | ok |  |  | false |  |
| L2 |  | metadata_supported |  |  | false |  |
| L3 |  | ok |  |  | false |  |
| L4 |  | snippet_used |  |  | false |  |
| L5 |  | ok |  |  | false |  |
| L6 |  | metadata_supported |  |  | false |  |
| L7 |  | ok |  |  | false |  |
| L8 |  | metadata_supported |  |  | false |  |
| L9 |  | ok |  |  | false |  |

## Scoring Traceability

| Dimension | Score | Label | Score Type | Confidence | Supporting Evidence | Weakening Evidence | Evidence Quality Limits | Missing Evidence | Cap / Review Reason |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| likelihood | 4 | High | analyst_assumption | high | L2, L4, L5, L6, L8 | L8 | None | None |  |
| impact | 4 | High | analyst_assumption | high | L2, L4, L6 | L8 | None | None |  |
| immediacy | 4 | High | analyst_assumption | high | L1, L2, L3 | L8 | None | None |  |
| exposure | 4 | High | analyst_assumption | high | L4, L6, L7 | L8 | None | None |  |
| confidence | 3 | Moderate | analyst_assumption | high | L2, L6 | L8 | None | None | Capped because Confidence capped at 3/5 because company-specific systems, revenue, RTO/RPO, insurance wording, supplier dependency and incident facts are missing. |
| decision_urgency | 4 | High | analyst_assumption | high | L1, L2, L3 | L8 | None | None |  |

## Evidence-To-Score Bridge

| Dimension | Score | Evidence Basis | Confidence Effect | Cap Reason |
| --- | ---: | --- | --- | --- |
| likelihood | 4 | Likelihood is based on UK cyber threat level, ransomware prevalence, sector exposure, state-linked/supplier risk and live incident patterns. |  | Confidence capped at 3/5 because company-specific systems, revenue, RTO/RPO, insurance wording, supplier dependency and incident facts are missing. |
| impact | 4 | Impact is based on downtime, revenue at risk, operational dependency, customer harm, regulatory exposure and insurance uncertainty. |  | Confidence capped at 3/5 because company-specific systems, revenue, RTO/RPO, insurance wording, supplier dependency and incident facts are missing. |
| immediacy | 4 | Immediacy is based on current threat indicators, incident prevalence, the resilience gap and dependency on exposed systems/suppliers. |  | Confidence capped at 3/5 because company-specific systems, revenue, RTO/RPO, insurance wording, supplier dependency and incident facts are missing. |
| confidence | 3 | Confidence is capped because public sources do not include company-specific systems, revenue, policy wording, supplier dependency or recovery data. |  | Confidence capped at 3/5 because company-specific systems, revenue, RTO/RPO, insurance wording, supplier dependency and incident facts are missing. |

## Source Requirement Coverage

- Requirements identified: 9/9
- Strongly covered: 0/9
- Direct snippet-only: 0/9
- Partial or indirect: 9/9
- Historical/context only: 0/9
- Missing: 0/9

| Requirement | Coverage Grade | Supporting Sources | Reason For Grade | Remaining Gap | Gap Affects Confidence |
| --- | --- | --- | --- | --- | --- |
| uk_official_cyber_threat_ncsc_evidence | high | L1 | Anchors the UK cyber threat, ransomware and state-linked risk environment for business interruption decisions. | Threat evidence supports likelihood; company exposure still depends on systems, controls and incident facts. | false |
| uk_cyber_breach_prevalence_data | high | L2 | Quantifies prevalence and relevance of cyber incidents, ransomware and breach exposure for UK businesses. | Survey-level prevalence does not identify this operator’s actual exposure or control maturity. | false |
| board_cyber_governance_and_resilience_expectations | medium | L3 | Shows what senior management is expected to do on cyber governance, incident readiness and operational resilience. | Guidance does not prove this operator has an adequate response plan or tested recovery process. | false |
| ransomware_or_operational_disruption_evidence | medium | L4 | Connects cyber events to downtime, customer disruption, supplier compromise and recovery pressure. | Reuters reporting is a peer incident signal, not evidence that the showcase operator has been compromised. | false |
| cyber_insurance_business_interruption_evidence | high | L5 | Shows claim, coverage, waiting-period, exclusion, incident-response panel or market implications for business interruption. | Insurance evidence is market guidance, not a coverage determination for any specific policy. | false |
| incident_reporting_and_regulatory_notification_guidance | high | L6 | Captures ICO, affected-customer and sector-regulator notification triggers. | Notification duty depends on actual personal-data exposure, harm likelihood and legal review. | false |
| supplier_msp_dependency_risk | medium | L7 | Captures third-party technology, cloud, payment, fulfilment or managed-service disruption as a recovery blocker. | FCA evidence is strongest for regulated financial services; retail operators should use it as a resilience analogue unless sector duties apply. | false |
| contrary_or_mitigation_evidence | medium | L8 | Shows resilience measures, recovery practices, controls or stabilising evidence that reduce impact and prevent overstatement. | Mitigation evidence reduces impact only if the operator has implemented and tested equivalent controls. | false |
| cyber_company_data_requirements_and_anti_overclaiming_controls | medium | L9 | Shows what cannot be concluded from public sources alone and which company facts are required for operational use. | Official NCSC guidance identifies the planning discipline, but company systems, revenue, RTO/RPO, policy and incident facts are still required. | false |

## Source Quality Notes

| Evidence area | Current source quality | Action before operational use |
| --- | --- | --- |
| UK official cyber threat / NCSC evidence | Official threat framing supports likelihood but not a company-specific incident forecast. | Refresh if NCSC threat posture or ransomware reporting changes. |
| UK breach prevalence data | Useful prevalence context; sector and company exposure need validation. | Refresh after new breach survey or sector incident reporting. |
| Board governance / resilience expectations | Regulatory and governance material supports escalation expectations. | Refresh if ICO / FCA / PRA / sector notification guidance changes. |
| Cyber insurance / business interruption evidence | Insurance-market evidence is useful but not coverage advice. | Refresh if cyber insurance waiting periods, exclusions or claims conditions change. |
| Business interruption exposure | Illustrative model output, not company-specific loss calculation. | Refresh when revenue exposure, recovery time and policy wording are available. |
| Resilience gap | Decision trigger is useful only after company RTO/RPO and recovery assumptions are confirmed. | Refresh when company systems map, recovery time or supplier/MSP dependency data becomes available. |

## Selected Sources

| Source ID | Requirement | Source role | Source value | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| L1 | uk_official_cyber_threat_ncsc_evidence | official_anchor | Official UK cyber authority evidence anchoring ransomware and state-linked threat relevance. |  |  | NCSC: Global ransomware threat expected to rise with AI |  |  |  |  |  |  | high | selected as strongest available source for the cyber business interruption requirement | Supports whether heightened operational resilience and incident readiness controls are justified. | ok | Threat evidence supports likelihood; company exposure still depends on systems, controls and incident facts. |
| L2 | uk_cyber_breach_prevalence_data | data_or_indicator_source | Official UK survey evidence quantifying cyber breach prevalence for UK organisations. |  |  | GOV.UK Cyber Security Breaches Survey 2025/2026 |  |  |  |  |  |  | high | selected as strongest available source for the cyber business interruption requirement | Supports likelihood scoring and the case for testing recovery and business-continuity assumptions. | metadata_supported | Survey-level prevalence does not identify this operator’s actual exposure or control maturity. |
| L3 | board_cyber_governance_and_resilience_expectations | regulatory_guidance | Official NCSC governance material translating cyber incidents into board-level incident planning and recovery expectations. |  |  | NCSC Cyber Governance: Incident Planning, Response and Recovery |  |  |  |  |  |  | medium | selected as strongest available source for the cyber business interruption requirement | Supports incident response activation, management escalation and resilience investment decisions. | ok | Guidance does not prove this operator has an adequate response plan or tested recovery process. |
| L4 | ransomware_or_operational_disruption_evidence | live_event_reporting | Current reputable reporting connecting UK retail cyber incidents to customer data and operating pressure. |  |  | Reuters: UK M&S customer data was taken in cyber attack |  |  |  |  |  |  | medium | selected as strongest available source for the cyber business interruption requirement | Supports incident response, customer-impact review, manual fallback and restoration prioritisation. | snippet_used | Reuters reporting is a peer incident signal, not evidence that the showcase operator has been compromised. |
| L5 | cyber_insurance_business_interruption_evidence | insurance_market_evidence | Broker evidence explaining how cyber insurance responds to technology outages and business interruption. |  |  | Marsh: Cyber insurance and its role when tech outages occur |  |  |  |  |  |  | high | selected as strongest available source for the cyber business interruption requirement | Supports triggering the cyber insurance claim process and checking policy wording, waiting period and coverage readiness. | ok | Insurance evidence is market guidance, not a coverage determination for any specific policy. |
| L6 | incident_reporting_and_regulatory_notification_guidance | regulatory_guidance | Official UK data-protection regulator guidance anchoring breach notification review. |  |  | ICO: Personal data breach reporting |  |  |  |  |  |  | high | selected as strongest available source for the cyber business interruption requirement | Supports ICO, affected-customer and legal/compliance notification review triggers. | metadata_supported | Notification duty depends on actual personal-data exposure, harm likelihood and legal review. |
| L7 | supplier_msp_dependency_risk | regulatory_guidance | UK regulator evidence showing how third-party technology outages create operational resilience lessons. |  |  | FCA: CrowdStrike outage lessons for operational resilience |  |  |  |  |  |  | medium | selected as strongest available source for the cyber business interruption requirement | Supports supplier, MSP, cloud, payment or fulfilment dependency escalation before returning to normal operations. | ok | FCA evidence is strongest for regulated financial services; retail operators should use it as a resilience analogue unless sector duties apply. |
| L8 | contrary_or_mitigation_evidence | contrary_scope_limit | Official mitigation evidence showing how integrated recovery planning can reduce interruption impact. |  |  | NCSC: Integrate recovery plans with wider organisational planning |  |  |  |  |  |  | medium | selected as strongest available source for the cyber business interruption requirement | Supports relaxation triggers and resilience-control validation before returning to normal operations. | metadata_supported | Mitigation evidence reduces impact only if the operator has implemented and tested equivalent controls. |
| L9 | cyber_company_data_requirements_and_anti_overclaiming_controls | regulatory_guidance | Official NCSC response and recovery planning evidence used to define company-data requirements and anti-overclaiming limits. |  |  | NCSC: Preparing for severe cyber threats |  |  |  |  |  |  | medium | selected as strongest available source for the cyber business interruption requirement | Supports anti-overclaiming and company-data requirements before operational use. | ok | Public guidance cannot confirm this operator’s recovery capability, backup status or policy response. |

## Rejected Sources

| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |
| --- | --- | --- | ---: | --- | --- | --- |
| Cyber insurance and its role when tech outages occur | cyber_insurance_business_interruption_evidence | site:marsh.com cyber insurance business interruption waiting period ransomware UK | 28 | recency_score | stronger source already selected for the same requirement | yes |
| Cyber Insurance Market Update Q3/H1 2022 - WTW | cyber_insurance_business_interruption_evidence | site:wtwco.com cyber insurance business interruption ransomware claims | 28 | recency_score | stronger source already selected for the same requirement | yes |
| Cyber spotlights on the manufacturing industry - WTW UK | cyber_insurance_business_interruption_evidence | site:wtwco.com cyber insurance business interruption ransomware claims | 28 | recency_score | stronger source already selected for the same requirement | yes |
| UK Cyber Market Report 2026 \| AJG United Kingdom | contrary_or_mitigation_evidence | Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services contrary or mitigation evidence specialist analysis | 28 | reliability_score | stronger source already selected for the same requirement | yes |
| Market update: GB cyber insurance - WTW | cyber_insurance_business_interruption_evidence | site:wtwco.com cyber insurance business interruption ransomware claims | 27 | recency_score | stronger source already selected for the same requirement | yes |
| 4.3 Integrate recovery plans with wider organisational planning | contrary_or_mitigation_evidence | site:gov.uk cyber resilience actions business continuity recovery | 27 | decision_value_score | stronger source already selected for the same requirement | yes |
| Operational Resilience of UK and European businesses in 2026 | contrary_or_mitigation_evidence | Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services contrary or mitigation evidence specialist analysis | 27 | reliability_score | stronger source already selected for the same requirement | yes |
| Operational resilience of the financial sector - Bank of England | contrary_or_mitigation_evidence | Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services contrary or mitigation evidence scope limited stabilising contrary evidence | 27 | decision_value_score | stronger source already selected for the same requirement | yes |
| Cyber Security and Resilience (Network and Information Systems ... | contrary_or_mitigation_evidence | Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services contrary or mitigation evidence scope limited stabilising contrary evidence | 27 | decision_value_score | stronger source already selected for the same requirement | yes |
| Cyber security resilience 2025 | uk_cyber_breach_prevalence_data | Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services uk cyber breach prevalence data specialist analysis | 26 | recency_score | stronger source already selected for the same requirement | yes |

## Evidence Coverage Assessment

- Strongest evidence category: official_primary
- Weakest evidence category: None identified
- Missing evidence: None identified
- Contrary/stabilising evidence: Present
- Confidence impact: Evidence coverage supports higher confidence, subject to analyst review.

## Illustrative Route-Cost Scenario

- Scenario assumptions are case-specific and were not foregrounded in this business-user path.

## Refresh Triggers

- Refresh if NCSC threat posture or ransomware reporting changes.
- Refresh if a major UK retail / critical services cyber incident occurs.
- Refresh if ICO / FCA / PRA / sector notification guidance changes.
- Refresh if cyber insurance waiting periods, exclusions or claims conditions change.
- Refresh when company systems map, revenue exposure, policy wording, recovery time or supplier/MSP dependency data becomes available.

## Analyst Review Controls

- Verify NCSC, ICO and sector-regulator guidance before operational use.
- Validate affected systems, revenue exposure, RTO/RPO, backup capability and supplier/MSP dependencies.
- Review cyber insurance policy wording, waiting periods, retentions and exclusions with broker/legal teams.
- Treat the resilience gap and business interruption exposure as illustrative until incident facts and company data are supplied.
- Keep the analysis focused on interruption, notification, claims and recovery decisions rather than technical cybersecurity advice.
