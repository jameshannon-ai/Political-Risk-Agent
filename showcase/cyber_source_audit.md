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
- Retrieval timestamp: 2026-06-03T12:18:49

## Research Plan

- Research objective: Build a governed evidence base for a UK customer-facing operator cyber business interruption decision.
- Decision questions:
  - Can the operator absorb and recover from cyber disruption without unacceptable downtime, revenue loss, regulatory exposure, customer harm or insurance coverage failure?
  - Do outage, notification, insurance, supplier or customer-harm triggers require incident response, manual contingency, pause or resilience investment?
  - What evidence would justify moving from incident response or manual contingency back toward normal operations?
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

## Search Results Summary

- Total candidate sources found: 73
- Total queries run: 37
- Total selected sources: 9
- Duplicate URLs removed: 0
- Source categories covered: contrary_or_stabilising_evidence, insurance_market_evidence, official_primary, reputable_news, specialist_analysis
- Fetch failures: 1

## Quantified Evidence Summary

- Business interruption exposure: £10.0m
- Resilience gap: -3 days
- Expected outage: 5 days
- Maximum tolerable downtime: 2 days
- Daily revenue at risk: £2.0m
- Confidence cap reason: Confidence capped at 3/5 because company-specific systems, revenue, RTO/RPO, insurance wording, supplier dependency and incident facts are missing.

## Source Requirement Coverage

| Requirement | Coverage | Strongest source | Source role | Evidence weight | Decision supported | Gap / refresh need |
| --- | --- | --- | --- | --- | --- | --- |
| uk_official_cyber_threat_ncsc_evidence | covered | L1 — NCSC: Global ransomware threat expected to rise with AI (National Cyber Security Centre) | official_anchor | high | Supports whether heightened operational resilience and incident readiness controls are justified. | Threat evidence supports likelihood; company exposure still depends on systems, controls and incident facts. |
| uk_cyber_breach_prevalence_data | covered | L2 — GOV.UK Cyber Security Breaches Survey 2025/2026 (GOV.UK / Department for Science, Innovation and Technology) | data_or_indicator_source | high | Supports likelihood scoring and the case for testing recovery and business-continuity assumptions. | Survey-level prevalence does not identify this operator’s actual exposure or control maturity. |
| board_cyber_governance_and_resilience_expectations | covered | L3 — NCSC Cyber Governance: Incident Planning, Response and Recovery (National Cyber Security Centre) | regulatory_guidance | medium | Supports incident response activation, management escalation and resilience investment decisions. | Guidance does not prove this operator has an adequate response plan or tested recovery process. |
| ransomware_or_operational_disruption_evidence | covered | L4 — Reuters: UK M&S customer data was taken in cyber attack (Reuters) | live_event_reporting | medium | Supports incident response, customer-impact review, manual fallback and restoration prioritisation. | Reuters reporting is a peer incident signal, not evidence that the showcase operator has been compromised. |
| cyber_insurance_business_interruption_evidence | covered | L5 — Marsh: Cyber insurance and its role when tech outages occur (Marsh) | insurance_market_evidence | high | Supports triggering the cyber insurance claim process and checking policy wording, waiting period and coverage readiness. | Insurance evidence is market guidance, not a coverage determination for any specific policy. |
| incident_reporting_and_regulatory_notification_guidance | covered | L6 — ICO: Personal data breach reporting (Information Commissioner’s Office) | regulatory_guidance | high | Supports ICO, affected-customer and legal/compliance notification review triggers. | Notification duty depends on actual personal-data exposure, harm likelihood and legal review. |
| supplier_msp_dependency_risk | covered | L7 — FCA: CrowdStrike outage lessons for operational resilience (Financial Conduct Authority) | regulatory_guidance | medium | Supports supplier, MSP, cloud, payment or fulfilment dependency escalation before returning to normal operations. | FCA evidence is strongest for regulated financial services; retail operators should use it as a resilience analogue unless sector duties apply. |
| contrary_or_mitigation_evidence | covered | L8 — NCSC: Integrate recovery plans with wider organisational planning (National Cyber Security Centre) | contrary_scope_limit | medium | Supports relaxation triggers and resilience-control validation before returning to normal operations. | Mitigation evidence reduces impact only if the operator has implemented and tested equivalent controls. |
| cyber_company_data_requirements_and_anti_overclaiming_controls | covered | L9 — NCSC: Preparing for severe cyber threats (National Cyber Security Centre) | regulatory_guidance | medium | Supports anti-overclaiming and company-data requirements before operational use. | Official NCSC guidance identifies the planning discipline, but company systems, revenue, RTO/RPO, policy and incident facts are still required. |

## Selected Sources

| Source ID | Title | Publisher | Source role | Source type | Requirement | Weight | Decision use | URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | NCSC: Global ransomware threat expected to rise with AI | National Cyber Security Centre | official_anchor | official_primary | uk_official_cyber_threat_ncsc_evidence | high | Supports whether heightened operational resilience and incident readiness controls are justified. | https://www.ncsc.gov.uk/news/global-ransomware-threat-expected-to-rise-with-ai |
| L2 | GOV.UK Cyber Security Breaches Survey 2025/2026 | GOV.UK / Department for Science, Innovation and Technology | data_or_indicator_source | official_primary | uk_cyber_breach_prevalence_data | high | Supports likelihood scoring and the case for testing recovery and business-continuity assumptions. | https://www.gov.uk/government/statistics/cyber-security-breaches-survey-20252026/cyber-security-breaches-survey-20252026 |
| L3 | NCSC Cyber Governance: Incident Planning, Response and Recovery | National Cyber Security Centre | regulatory_guidance | official_primary | board_cyber_governance_and_resilience_expectations | medium | Supports incident response activation, management escalation and resilience investment decisions. | https://www.ncsc.gov.uk/training/cyber-governance/Incident_Planning_Response_and_Recovery/NCSC-CyberGovernanceforBoards-IncidentPlanningResponseandRecovery-v5.1-Web/index.html |
| L4 | Reuters: UK M&S customer data was taken in cyber attack | Reuters | live_event_reporting | reputable_news | ransomware_or_operational_disruption_evidence | medium | Supports incident response, customer-impact review, manual fallback and restoration prioritisation. | https://www.reuters.com/business/retail-consumer/uks-ms-says-customer-information-was-taken-cyber-attack-2025-05-13 |
| L5 | Marsh: Cyber insurance and its role when tech outages occur | Marsh | insurance_market_evidence | insurance_market_evidence | cyber_insurance_business_interruption_evidence | high | Supports triggering the cyber insurance claim process and checking policy wording, waiting period and coverage readiness. | https://www.marsh.com/sg/services/cyber-risk/insights/cyber-insurance-role-tech-outages.html |
| L6 | ICO: Personal data breach reporting | Information Commissioner’s Office | regulatory_guidance | official_primary | incident_reporting_and_regulatory_notification_guidance | high | Supports ICO, affected-customer and legal/compliance notification review triggers. | https://ico.org.uk/for-organisations/report-a-breach/personal-data-breach |
| L7 | FCA: CrowdStrike outage lessons for operational resilience | Financial Conduct Authority | regulatory_guidance | official_primary | supplier_msp_dependency_risk | medium | Supports supplier, MSP, cloud, payment or fulfilment dependency escalation before returning to normal operations. | https://www.fca.org.uk/firms/operational-resilience/crowdstrike-outage-lessons-operational-resilience |
| L8 | NCSC: Integrate recovery plans with wider organisational planning | National Cyber Security Centre | contrary_scope_limit | contrary_or_stabilising_evidence | contrary_or_mitigation_evidence | medium | Supports relaxation triggers and resilience-control validation before returning to normal operations. | https://www.ncsc.gov.uk/collection/how-to-prepare-and-plan-your-organisations-response-to-severe-cyber-threat-a-guide-for-cni/activity-4-withstand-and-recover/4-3-integrate-recovery-plans-with-wider-organisational-planning |
| L9 | NCSC: Preparing for severe cyber threats | National Cyber Security Centre | regulatory_guidance | official_primary | cyber_company_data_requirements_and_anti_overclaiming_controls | medium | Supports anti-overclaiming and company-data requirements before operational use. | https://www.ncsc.gov.uk/sites/default/files/documents/ncsc-how-to-prepare-for-and-plan-your-organisation-s-response-to-severe-cyber-threat-a-guide-for-cni.pdf |

## Source Quality Notes

| Evidence area | Current source quality | Action before operational use |
| --- | --- | --- |
| UK cyber threat / NCSC evidence | Strong: official NCSC source anchors ransomware and threat environment. | Refresh NCSC threat evidence before operational use. |
| Breach prevalence | Strong: official GOV.UK survey evidence is available, but operator-specific control maturity is absent. | Replace prevalence screen with company incident history and control evidence. |
| Operational disruption | Medium-high: Reuters peer incident evidence is useful but not company-specific. | Refresh live reporting and validate actual incident facts. |
| Insurance / business interruption | Medium: broker evidence supports claims-readiness framing, not policy coverage. | Review policy wording, waiting period, retentions, exclusions and notice duties. |
| Regulatory notification | Strong: ICO guidance anchors notification review, but facts determine duty. | Run legal/compliance review using actual personal-data and customer-harm facts. |
| Supplier / MSP dependency | Medium-high: FCA resilience evidence is strong by analogy; sector duties vary. | Map MSP, cloud, payment, fulfilment and key technology dependencies. |
| Mitigation / recovery evidence | Medium: NCSC recovery guidance is useful but implementation is unproven. | Validate tested recovery plans, manual fallback and backup/restore capability. |
| Company data requirements | Strong as an anti-overclaiming control. | Obtain systems map, RTO/RPO, revenue, supplier and insurance-policy data. |

## Evidence-To-Score Bridge

| Dimension | Score | Evidence basis | Review trigger |
| --- | --- | --- | --- |
| Likelihood | 4/5 | Likelihood is based on UK cyber threat level, ransomware prevalence, sector exposure, state-linked/supplier risk and live incident patterns. | Refresh NCSC/GOV.UK threat and breach prevalence evidence before implementation or when sector-peer incidents change exposure. |
| Impact | 4/5 | Impact is based on downtime, revenue at risk, operational dependency, customer harm, regulatory exposure and insurance uncertainty. | Refresh when company revenue, service criticality, policy wording or customer impact data becomes available. |
| Immediacy | 4/5 | Immediacy is based on current threat indicators, incident prevalence, the resilience gap and dependency on exposed systems/suppliers. | Refresh if incident facts, recovery estimates, supplier status or live ransomware reporting changes. |
| Confidence | 3/5 | Confidence is capped because public sources do not include company-specific systems, revenue, policy wording, supplier dependency or recovery data. | Increase confidence only after systems map, revenue-at-risk, policy wording, supplier dependency and incident facts are supplied. |

## Rejected Sources

Rejected sources are retained in `showcase/cyber_evidence_pack.json` to preserve the Tavily search trail. The selected set prioritises official UK sources, reputable live incident reporting, cyber insurance/business interruption evidence and company-data controls.

## Refresh Priorities

- Refresh if NCSC threat posture or ransomware reporting changes.
- Refresh if a major UK retail / critical services cyber incident occurs.
- Refresh if ICO / FCA / PRA / sector notification guidance changes.
- Refresh if cyber insurance waiting periods, exclusions or claims conditions change.
- Refresh when company systems map, revenue exposure, policy wording, recovery time or supplier/MSP dependency data becomes available.

## Methodology and Review Controls

The source audit preserves the live Tavily source trail, selected source reasoning, coverage gaps and confidence limits. Public-source evidence cannot confirm company-specific outage duration, revenue loss, notification duty, insurance recovery or supplier dependency. Before operational use, validate systems, revenue, RTO/RPO, backup/restore capability, policy wording, supplier map, incident facts and legal/compliance review.
