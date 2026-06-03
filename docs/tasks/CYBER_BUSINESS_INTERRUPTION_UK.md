# Task Brief: Cyber Business Interruption Engine

## Objective

Create a fifth showcase case brief, at a later implementation stage, for:

**Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services**

The case should demonstrate how the Political Risk Agent converts geopolitical cyber, ransomware, operational resilience and cyber-insurance risk into a business-interruption decision product for a UK operator.

The future output must focus on business interruption, escalation, regulatory notification, insurance response and resilience investment. It must not become a technical cybersecurity report.

## Current status

This is a task brief only. Do not generate the case yet.

Current active dashboard cases are:
- UK ETS Maritime Expansion
- Hormuz Route Decision Engine
- Critical Minerals Exposure Engine
- Sanctions Trade Finance Exposure Engine

The cyber business interruption case is a proposed fifth showcase. It should be implemented later as a saved-showcase artefact set before any dashboard integration.

## Business decision

Client type:
UK retailer / critical services operator

Primary showcase archetype:
UK customer-facing operator with material digital trading, payment, fulfilment, customer-service or essential-service dependency.

Use retail as the base dashboard scenario unless a later task explicitly chooses a critical-services sub-sector. Critical-services language should remain a scope extension because regulatory notification and operational resilience duties differ by sector.

Practical users:
- CFO
- COO
- Risk Manager
- Head of Operations
- Incident response lead
- Cyber insurance underwriter

Core business question:

Can a UK operator absorb and recover from a cyber incident without unacceptable downtime, revenue loss, regulatory exposure, customer harm or insurance coverage failure?

Risk pattern:

Geopolitical cyber / ransomware / operational resilience risk -> downtime, revenue loss, notification, insurance and recovery decision.

Decision options:
- continue normal operations
- activate incident response
- notify regulator / affected customers where required
- trigger cyber insurance claim process
- switch to manual contingency operations
- prioritise system restoration
- escalate supplier / MSP dependency risk
- pause exposed digital operations
- increase resilience investment

The output should answer:
- Is the operator still inside tolerable downtime?
- Which business process or customer service exposure drives the decision?
- Does the incident trigger regulatory notification or customer communication review?
- Does the incident trigger the cyber insurance claim process?
- Are manual contingency operations viable?
- Are supplier, MSP or cloud dependencies creating a recovery bottleneck?
- Is resilience investment needed because expected recovery exceeds tolerance?
- Which evidence would move the decision from incident response / manual contingency back to normal operations?
- Which missing company data prevents a firmer recommendation?

## In scope

- UK cyber and operational resilience framing.
- Geopolitical cyber and ransomware threat framing where it affects UK business interruption, not technical attribution.
- Business interruption and revenue-at-risk modelling.
- Cyber insurance / business interruption coverage readiness.
- Regulatory notification and customer harm decision triggers.
- Supplier / MSP dependency risk as an operational recovery constraint.
- Client-type decision support for a UK retailer / critical services operator.
- Evidence-to-score bridge for likelihood, impact, immediacy and confidence.
- Source requirement coverage, source quality notes, selected sources, evidence appendix and source audit.
- Clear separation between public/live evidence, illustrative assumptions, company-provided data and derived calculations.

Quantitative model:

Business interruption exposure = outage duration x daily revenue at risk

Resilience gap = maximum tolerable downtime - expected recovery time

Interpretation:
The resilience gap is negative where expected recovery takes longer than maximum tolerable downtime. In the illustrative scenario, a -3 day gap means expected recovery exceeds tolerance by three days, making incident response, manual contingency, insurance notification and resilience investment near-term management decisions.

Illustrative scenario inputs:

| Input | Value | Label | Use |
|---|---:|---|---|
| Expected outage | 5 days | illustrative | Estimates downtime exposure |
| Maximum tolerable downtime | 2 days | illustrative / company-provided when available | Tests resilience tolerance |
| Resilience gap | -3 days | derived | Shows expected recovery exceeds tolerance |
| Daily revenue at risk | illustrative GBP2m | illustrative | Estimates gross revenue disruption |
| Gross revenue disruption | derived GBP10m | derived | Outage duration x daily revenue at risk |
| Insurance waiting period | 24 hours | illustrative | Tests claim timing and uninsured loss period |
| Regulatory notification trigger | source-supported where applicable | source-supported | Tests ICO / regulator notification review |
| Customer harm / service disruption severity | high | illustrative | Supports notification, prioritisation and customer-impact review |

Decision thresholds for the future model:

| Condition | Decision implication |
|---|---|
| Expected recovery is inside maximum tolerable downtime | Continue normal operations or monitor if no notification / insurance trigger exists |
| Expected recovery exceeds maximum tolerable downtime | Activate incident response and prioritise restoration |
| Outage exceeds insurance waiting period or policy notice condition may apply | Trigger cyber insurance claim notification process |
| Personal data exposure or customer harm may meet reporting threshold | Escalate ICO / regulator / customer notification review |
| Core digital channel unavailable but manual process can preserve critical service | Switch to manual contingency operations |
| Supplier, MSP or cloud dependency controls recovery path | Escalate third-party dependency risk |
| Customer harm, data exposure or uncontrolled losses worsen through continued operation | Pause exposed digital operations |

## Out of scope

- Do not generate the live case in this task brief.
- Do not call Tavily.
- Do not run `live_search_mode`.
- Do not edit `dashboard_app.py`.
- Do not change UK ETS, Hormuz, Critical Minerals or Sanctions saved outputs.
- Do not add broad framework features.
- Do not provide technical cybersecurity advice such as network hardening, exploit remediation, malware reverse engineering or detailed system configuration.
- Do not claim company-specific outage loss, recovery capability, coverage status or notification requirement without company data.
- Do not present illustrative values as facts.
- Do not produce a generic cyber threat report.

## Source requirements

Future source planning should include these source requirements:

1. UK official cyber threat / NCSC evidence
   - Purpose: anchor UK threat, ransomware and state-linked or geopolitically influenced cyber relevance.
   - Preferred role: official_anchor.

2. UK cyber breach prevalence data
   - Purpose: quantify baseline cyber incident and ransomware prevalence for UK organisations.
   - Preferred role: data_or_indicator_source.

3. Board cyber governance / resilience expectations
   - Purpose: connect cyber risk to board-level operational resilience and accountability.
   - Preferred role: regulatory_guidance or official_anchor.

4. Ransomware or operational disruption evidence
   - Purpose: show live or recent patterns of downtime, service disruption, supplier compromise, customer harm and recovery pressure.
   - Preferred role: live_event_reporting.

5. Cyber insurance / business interruption evidence
   - Purpose: explain insurance waiting periods, claim notice, incident-response panel requirements, exclusions, coverage uncertainty and revenue-loss exposure.
   - Preferred role: insurance_market_evidence.

6. Incident reporting / regulatory notification guidance
   - Purpose: identify when ICO, sector regulator or affected-customer notification review is required.
   - Preferred role: regulatory_guidance.

7. Sector-specific resilience evidence for retail or critical services
   - Purpose: tie generic cyber disruption to customer service, essential operations, payment, fulfilment or critical-service continuity.
   - Preferred role: specialist_interpretation or data_or_indicator_source.

8. Contrary / mitigation evidence showing resilience actions or recovery indicators
   - Purpose: prevent overstatement by identifying evidence of recovery, effective continuity plans, resilience investment or mitigations.
   - Preferred role: contrary_scope_limit.

9. Company-data requirements / anti-overclaiming controls
   - Purpose: make clear what cannot be concluded from public sources alone.
   - Preferred role: company_required_data.

Source roles:
- official_anchor
- regulatory_guidance
- data_or_indicator_source
- live_event_reporting
- specialist_interpretation
- insurance_market_evidence
- contrary_scope_limit
- company_required_data

Preferred source targets:
- NCSC Annual Review
- NCSC ransomware / cyber threat guidance where relevant
- GOV.UK Cyber Security Breaches Survey
- GOV.UK Cyber Governance Code of Practice
- ICO incident reporting / personal data breach guidance
- FCA / PRA operational resilience guidance where relevant
- NIS / UK essential services or digital services guidance where relevant to the selected sub-sector
- Reuters / AP for live cyber incident reporting
- Allianz / Marsh / Aon / Howden / WTW for cyber insurance and business interruption evidence
- reputable legal or cyber incident response firms for notification and claims interpretation

Source quality requirements:
- Do not treat insurer market commentary as official regulatory guidance.
- Do not treat incident reporting as proof of company-specific exposure unless the affected company is the client and facts are provided.
- Do not treat technical cyber guidance as business-interruption evidence unless it supports downtime, notification, recovery or resilience decisions.
- Do not infer a legal notification duty from public incident examples alone; use official ICO or sector-regulator guidance and flag legal review.
- Treat geopolitical attribution as relevant only where it changes threat likelihood, resilience urgency, sanctions/payment constraints, insurance treatment or supplier-risk review.
- Selected sources should include source role, source value explanation, requirement mapping, readable claim, quantified or concrete signal, commercial meaning, decision use, caveat and refresh trigger.

## Output requirements

The future brief should be titled:

```markdown
# Political Risk Brief
## Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services
```

The future brief should include:
- Decision Recommendation
- Scope and Specificity
- Dashboard Summary
- Incident Exposure Summary
- Operational Dependency Assessment
- Business Interruption Model
- Downtime / Revenue-at-Risk Assessment
- Regulatory Notification Assessment
- Insurance and Claims Readiness Assessment
- Supplier / MSP Dependency Risk
- Mitigation Options
- Risk Scorecard
- Evidence-To-Score Bridge
- Source Requirement Coverage
- Source Quality Notes
- Selected Sources
- Evidence Appendix
- Source Audit Summary
- Methodology and Review Controls

Dashboard Summary should later include:

| Item | Value |
|---|---|
| Decision engine | normal operations / incident response / notification / insurance claim / manual contingency / pause operations / resilience investment |
| Current stance | Escalate if expected recovery exceeds tolerable downtime or notification / insurance triggers are unresolved |
| Primary operational trigger | Expected outage exceeds maximum tolerable downtime |
| Primary financial trigger | Revenue at risk and uninsured waiting-period exposure become material |
| Primary regulatory trigger | Personal data exposure or service disruption requires notification review |
| Primary insurance trigger | Outage, response cost or policy notice condition may activate claim process |
| Primary supplier trigger | MSP, cloud, payment or fulfilment dependency blocks recovery |
| Evidence mode | Live source retrieval / saved showcase when generated |
| Key data limits | Systems, revenue, RTO/RPO, insurance wording, customer impact and supplier dependency data required |

Decision recommendation logic should be conditional:
- Continue normal operations only if threat exposure is monitored, critical systems are stable, no notification trigger is present and recovery capability is inside tolerance.
- Activate incident response when disruption is confirmed or credible indicators suggest business service impact.
- Notify regulator / affected customers where source-supported legal or regulatory triggers may apply.
- Trigger cyber insurance claim process when outage, waiting period, policy notice requirements or forensic-cost triggers may apply.
- Switch to manual contingency operations where critical services can be maintained while systems recover.
- Prioritise system restoration where downtime exceeds tolerance or customer harm is high.
- Escalate supplier / MSP dependency risk where third-party recovery limits the operator's recovery path.
- Pause exposed digital operations where continued operation worsens customer harm, data exposure or operational loss.
- Increase resilience investment where expected recovery exceeds maximum tolerable downtime.

Evidence-to-score bridge should use:

Likelihood:
Based on UK cyber threat level, ransomware prevalence, geopolitically influenced threat activity, sector exposure and live incident patterns.

Impact:
Based on downtime, revenue at risk, operational dependency, customer harm, regulatory exposure and insurance uncertainty.

Immediacy:
Based on current threat indicators, incident prevalence, resilience gaps and dependency on exposed systems/suppliers.

Confidence:
Based on source coverage and missing company-specific systems, revenue, policy wording and recovery data.

Review and refresh priorities should include:
- Refresh NCSC / GOV.UK threat and breach prevalence evidence before implementation.
- Refresh live incident reporting if a sector peer or supplier incident changes exposure.
- Refresh ICO / sector-regulator guidance if notification thresholds or resilience duties change.
- Refresh cyber insurance market evidence if waiting periods, exclusions, ransomware treatment or claim notice expectations change.
- Refresh model outputs when company RTO/RPO, backup capability, revenue-at-risk, policy wording or supplier dependency data is supplied.

Anti-overclaiming language required:

This is a client-type cyber business-interruption exposure screen, not technical cybersecurity advice, legal advice, insurance coverage advice or a company-specific recovery assessment.

Company-specific use requires:
- affected systems and process map
- daily revenue by channel / service
- recovery time objective and recovery point objective
- backup and restore capability
- cyber insurance policy wording
- waiting period / retention / exclusions
- customer notification requirements
- personal data exposure assessment
- supplier / MSP dependency map
- incident response plan and legal/compliance review

## Files likely to change

For this task brief only:
- `docs/tasks/CYBER_BUSINESS_INTERRUPTION_UK.md`

For a future implementation task, likely files may include:
- `config/domain_packs.json`
- `agent/source_requirements.py`
- `agent/source_planner.py`
- `agent/source_ranker.py`
- `agent/live_evidence_extraction.py`
- a cyber business interruption model module if needed
- `showcase/cyber_business_interruption_brief.md`
- `showcase/cyber_business_interruption_source_audit.md`
- `showcase/cyber_business_interruption_evidence_pack.json`
- tests for source requirements, model logic, saved showcase sections and dashboard helpers

Dashboard integration should happen only after a saved live-source showcase exists and passes quality checks.

## Do not change

For this task:
- Do not call Tavily.
- Do not run `live_search_mode`.
- Do not edit `dashboard_app.py`.
- Do not change UK ETS, Hormuz, Critical Minerals or Sanctions saved outputs.
- Do not add broad framework features.
- Do not generate the cyber case.

For future implementation:
- Do not imply the current portfolio is final.
- Do not weaken existing case-specific models.
- Do not turn the output into a technical cybersecurity report.
- Do not claim company-specific precision without company data.

## Verification commands

Run:

```bash
python3 scripts/check_dashboard_files.py
python3 -m unittest discover tests
python3 scripts/quality_check.py
```

## Acceptance criteria

- Task brief is complete and stored at `docs/tasks/CYBER_BUSINESS_INTERRUPTION_UK.md`.
- The brief follows `docs/TASK_BRIEF_TEMPLATE.md`.
- The business decision is specific to UK retailer / critical services business interruption.
- Source requirements cover official UK cyber evidence, breach prevalence, governance, ransomware/disruption, insurance, notification, sector resilience, mitigation/contrary evidence and company-data limits.
- Quantitative model and illustrative inputs are labelled as source-supported, illustrative, company-provided or derived.
- The future output requirements connect evidence to incident response, notification, claims, manual fallback, supplier escalation and resilience investment decisions.
- No live sources are called.
- No dashboard changes are made.
- No existing showcase outputs are changed.
- Tests and quality check pass.
- The case is ready for a later implementation/live-source task, but is not generated yet.
