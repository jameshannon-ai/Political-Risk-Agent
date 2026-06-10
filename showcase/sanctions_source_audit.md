# Source Audit
## Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk

## Search Configuration

| Item | Value |
| --- | --- |
| Topic | Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk |
| Business user | trade_finance_lender |
| Region | UK trade finance / cross-border transaction screening |
| Time horizon | 1-3 months |
| Search provider used | tavily |
| Evidence mode | Live source retrieval |
| Fallback data used | false |
| Total queries run | 36 |
| Candidate sources | 76 |
| Selected sources | 9 |
| Rejected sources | 67 |

## Research Plan

- Research objective: Create a governed evidence base for UK trade finance transaction approval, escalation, legal hold or rejection decisions.
- Core decision: should the lender approve, approve with enhanced due diligence, escalate, legally hold or reject the transaction?
- Required evidence: UK sanctions/OFSI guidance; controlled-goods/end-use evidence; counterparty and ownership exposure; route/diversion risk; documentation controls; enforcement expectations; financial-sector operating impact; contrary/clearance evidence; company-data requirements.

## Quantified Evidence Summary

| Item | Value |
| --- | --- |
| Selected sources | 9 |
| Source requirement coverage | 100% with caveated partial areas |
| Live queries run | 36 |
| Candidate sources reviewed | 76 |
| Quantified / concrete signals | 9 labelled source signals |
| Confidence cap reason | Confidence capped at 3/5 because public evidence does not include transaction-specific goods, counterparty, ownership, route, payment, licence or document data. |

## Source Requirement Coverage

| Requirement | Coverage | Strongest source | Source role | Evidence weight | Decision supported | Gap / refresh need |
| --- | --- | --- | --- | --- | --- | --- |
| uk_sanctions_ofsi_official_guidance | Covered | L1 — GOV.UK Sanctions End-Use Controls Guidance for Businesses (GOV.UK) | official_anchor | high | Should the lender approve, escalate, legally hold or reject the transaction? | Official guidance is strong, but must be refreshed before live transaction approval. |
| sanctions_end_use_controls_and_controlled_goods_risk | Covered | L1 — GOV.UK Sanctions End-Use Controls Guidance for Businesses (GOV.UK) | official_anchor | high | Do goods, technology, dual-use status or end-use controls create a legal hold or rejection trigger? | Goods classification and licence status still require transaction-specific validation. |
| counterparty_and_ownership_exposure | Covered | L3 — GOV.UK UK Financial Sanctions General Guidance (GOV.UK / OFSI) | regulatory_guidance | high | Are counterparties, beneficial owners, banks, intermediaries, vessels or consignees clean enough for approval? | Public guidance cannot clear named parties; sanctions screening and ownership records are required. |
| jurisdiction_route_and_diversion_exposure | Partially covered | L4 — Reuters Practical Law Sanctions and Export Controls Compliance Roadmap (Reuters Practical Law) | specialist_interpretation | medium | Do countries, ports, transshipment patterns, diversion indicators or logistics route create a red flag? | Requires current route, port, transshipment and diversion checks before operational use. |
| documentation_and_transaction_quality_evidence | Covered | L5 — ICC Academy Sanctions and Letters of Credit: What Banks Must Know (ICC Academy) | financial_sector_guidance | medium | Are transaction documents strong enough for approval or do gaps trigger escalation or hold? | Actual invoices, bills of lading, contracts, end-use statements and payment instructions are required. |
| enforcement_penalty_and_regulatory_expectations | Covered | L6 — OFSI Strategy 2026-29 (Office of Financial Sanctions Implementation) | enforcement_evidence | medium | What enforcement or penalty expectations make unresolved red flags unacceptable? | Regulatory expectations are clear; transaction-specific breach exposure requires legal review. |
| financial_institution_trade_finance_operating_impact | Partially covered | L5 — ICC Academy Sanctions and Letters of Credit: What Banks Must Know (ICC Academy) | financial_sector_guidance | medium | How does sanctions risk affect transaction approval, drawdown, credit exposure, insurance or operational controls? | BAFT source is weaker; use internal policy and formal ICC/Wolfsberg/BAFT principles before operational use. |
| contrary_clearance_or_de_escalation_evidence | Covered | L8 — GOV.UK How to Use Exceptions and Licences to Comply With Sanctions (GOV.UK) | contrary_scope_limit | medium | What evidence would justify approval or enhanced due diligence rather than legal hold? | Exceptions or licences support de-escalation only if they match exact transaction facts. |
| sanctions_company_data_requirements_and_anti_overclaiming_controls | Covered | L9 — Wolfsberg Group, ICC and BAFT Trade Finance Principles (Wolfsberg Group / ICC / BAFT) | company_required_data | high | What transaction-specific goods, ownership, route, payment, licence and document data is required before a clearance decision? | Transaction-specific goods, counterparty, ownership, route, payment, licence and document data remain required. |

## Selected Sources

| Source ID | Title | Publisher | Source role | Source type | Requirement | Weight | Decision use | URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | GOV.UK Sanctions End-Use Controls Guidance for Businesses | GOV.UK | official_anchor | official_primary | uk_sanctions_ofsi_official_guidance | medium | Anchors UK sanctions screening, OFSI escalation and legal-hold thresholds for trade finance approval. | https://www.gov.uk/government/publications/sanctions-end-use-controls-guidance-for-businesses/sanctions-end-use-controls-guidance-for-businesses |
| L2 | GOV.UK Notices to Exporters | GOV.UK / Export Control Joint Unit | regulatory_guidance | official_primary | sanctions_end_use_controls_and_controlled_goods_risk | medium | Supports goods classification, controlled-goods checks and licence/authorisation hold triggers before drawdown. | https://www.gov.uk/government/collections/notices-to-exporters |
| L3 | GOV.UK UK Financial Sanctions General Guidance | GOV.UK / OFSI | regulatory_guidance | official_primary | counterparty_and_ownership_exposure | medium | Supports counterparty, beneficial ownership, intermediary, bank and consignee screening decisions. | https://www.gov.uk/government/publications/financial-sanctions-general-guidance/uk-financial-sanctions-general-guidance |
| L4 | Reuters Practical Law Sanctions and Export Controls Compliance Roadmap | Reuters Practical Law | specialist_interpretation | reputable_news | jurisdiction_route_and_diversion_exposure | medium | Supports escalation where jurisdiction, route, transshipment or diversion indicators are unresolved. | https://www.reuters.com/practical-law-the-journal/transactional/sanctions-export-controls-compliance-roadmap-2025-10-01 |
| L5 | ICC Academy Sanctions and Letters of Credit: What Banks Must Know | ICC Academy | financial_sector_guidance | specialist_analysis | documentation_and_transaction_quality_evidence | medium | Supports document-request and hold triggers for invoices, bills of lading, end-use statements and payment instructions. | https://academy.iccwbo.org/trade-finance/article/sanctions-and-letters-of-credit |
| L6 | OFSI Strategy 2026-29 | Office of Financial Sanctions Implementation | enforcement_evidence | official_primary | enforcement_penalty_and_regulatory_expectations | medium | Supports legal-hold and rejection thresholds by showing regulatory consequences and expected controls. | https://ofsi.blog.gov.uk/2026/04/15/ofsi-strategy-2026-29 |
| L7 | BAFT Trade Finance Compliance and KYC Resources | BAFT | financial_sector_guidance | specialist_analysis | financial_institution_trade_finance_operating_impact | medium | Supports facility conditions, drawdown controls, credit exposure review and operational escalation. | https://baft.org/page/5?search=KYC |
| L8 | GOV.UK How to Use Exceptions and Licences to Comply With Sanctions | GOV.UK | contrary_scope_limit | contrary_or_stabilising_evidence | contrary_clearance_or_de_escalation_evidence | medium | Supports approval or enhanced due diligence only where clean counterparties, licences, exemptions and documents resolve red flags. | https://www.gov.uk/guidance/how-to-use-exceptions-and-licences-to-comply-with-sanctions |
| L9 | Wolfsberg Group, ICC and BAFT Trade Finance Principles | Wolfsberg Group / ICC / BAFT | company_required_data | specialist_analysis | sanctions_company_data_requirements_and_anti_overclaiming_controls | medium | Supports anti-overclaiming controls by showing the transaction data still required before clearance. | https://library.iccwbo.org/content/tfb/pdf/trade-finance-principles-2019-amendments-wolfsberg-icc-baft-final.pdf |

## Source Quality Notes

| Evidence area | Current source quality | Action before operational use |
| --- | --- | --- |
| UK sanctions / OFSI guidance | Strong: GOV.UK/OFSI official sources anchor the legal/compliance baseline. | Refresh GOV.UK/OFSI guidance before approving a live transaction. |
| Controlled goods / end-use controls | Strong policy anchor, but goods-specific application is transaction-dependent. | Validate goods description, HS/commodity classification, end-use and licence status. |
| Counterparty and ownership | Medium-high: official guidance supports ownership/control review, but no named-party screening is included. | Run sanctions screening and beneficial ownership checks on all transaction parties. |
| Jurisdiction / route / diversion | Medium: Reuters Practical Law supports compliance framing; live route/diversion evidence should be refreshed. | Refresh current Reuters/AP/official diversion reporting and validate ports, vessel and transshipment data. |
| Documentation quality | Medium-high: ICC/Wolfsberg/BAFT style guidance supports document controls. | Review actual invoices, bills of lading, contracts, end-user statements and payment instructions. |
| Financial-sector operating impact | Medium: BAFT source is weaker/secondary, while ICC/Wolfsberg principles are stronger. | Use internal bank policy, formal principles and legal/compliance sign-off before operational use. |
| Contrary / clearance evidence | Medium: GOV.UK licence/exception evidence supports de-escalation only where exact conditions are met. | Treat licences, exceptions or exemptions as transaction-specific evidence, not an all-clear. |
| Company-data requirements | Strong as an anti-overclaiming control. | Obtain goods, counterparty, ownership, route, payment, licence and document data before clearance. |

## Evidence-To-Score Bridge

| Score dimension | Score | Evidence basis | Why not higher / lower | Review trigger |
| --- | --- | --- | --- | --- |
| Likelihood | 4/5 | Likelihood is driven by official UK sanctions/end-use guidance, controlled-goods risk, ownership/counterparty exposure and live route/diversion indicators. | Higher only with current transaction screening and licence data; lower would understate official/legal control evidence. | Refresh if sanctions designations, OFSI guidance or export-control rules change. |
| Impact | 4/5 | Impact is driven by legal hold/rejection risk, payment blockage, documentation failure, credit exposure, insurance/underwriting exclusion and regulatory penalty consequences. | Higher if a sanctioned party/prohibited end-use is confirmed; lower if clean documents and licences resolve red flags. | Refresh when payment, credit, insurance or document risk changes. |
| Immediacy | 4/5 | Immediacy is high because checks must be resolved before approval, drawdown, document honouring or payment execution. | Higher if drawdown/payment is imminent; lower if transaction is only early-stage pipeline. | Refresh before approval, drawdown or payment execution. |
| Confidence | 3/5 | Confidence is capped because public evidence does not include transaction-specific goods, ownership, screening, route, payment, licence or document data. | Public sources support a screen, not transaction clearance. | Increase only after BOM/goods, counterparty, ownership, route, payment and document data are supplied. |

## Rejected Sources

| Title | Requirement | URL | Total score | Rejection reason |
| --- | --- | --- | --- | --- |
| Sanctions End-Use Controls: guidance for businesses - GOV.UK | sanctions_end_use_controls_and_controlled_goods_risk | https://www.gov.uk/government/publications/sanctions-end-use-controls-guidance-for-businesses/sanctions-end-use-controls-guidance-for-businesses | 25 | duplicate or near-duplicate |
| Sanctions End-Use Controls: guidance for businesses - GOV.UK | sanctions_end_use_controls_and_controlled_goods_risk | https://www.gov.uk/government/publications/sanctions-end-use-controls-guidance-for-businesses/sanctions-end-use-controls-guidance-for-businesses | 25 | duplicate or near-duplicate |
| Assembly Questions with the Index Term Departmental responsibilities | counterparty_and_ownership_exposure | https://aims.niassembly.gov.uk/terms/PrintResults.aspx?se=&so=Ascending&tb=&per=&sp=&fd=&td=&cb1=&cb2=&itn1=ySrULvCABBqYWwYDoiwEdNNquqw5bItTvrvj2jVT4pM%3D&itn2=jc7icOHu4kg%3D&itn3=jc7icOHu4kg%3D&pid=4&pm=&pg=2&tn=1&ito2=&ito3=&ks=jc7icOHu4kg%3D&st=1&pi=0&m=0&mn=All+Questions | 22 | duplicate or near-duplicate |
| Sanctions End-Use Controls: guidance for businesses - GOV.UK | jurisdiction_route_and_diversion_exposure | https://www.gov.uk/government/publications/sanctions-end-use-controls-guidance-for-businesses/sanctions-end-use-controls-guidance-for-businesses | 22 | duplicate or near-duplicate |
| Wolfsberg Group: Home | documentation_and_transaction_quality_evidence | https://www.wolfsberg-principles.com | 21 | duplicate or near-duplicate |
| Sanctions in Trade Finance Masterclass: Real World Examples | documentation_and_transaction_quality_evidence | https://www.youtube.com/watch?v=jBtXT42LG_s | 21 | duplicate or near-duplicate |
| Financial sanctions enforcement and monetary penalties guidance | enforcement_penalty_and_regulatory_expectations | https://www.gov.uk/government/publications/financial-sanctions-enforcement-and-monetary-penalties-guidance/financial-sanctions-enforcement-and-monetary-penalties-guidance | 23 | duplicate or near-duplicate |
| Assembly Questions with the Index Term Departmental responsibilities | enforcement_penalty_and_regulatory_expectations | https://aims.niassembly.gov.uk/terms/PrintResults.aspx?se=&so=Ascending&tb=&per=&sp=&fd=&td=&cb1=&cb2=&itn1=ySrULvCABBqYWwYDoiwEdNNquqw5bItTvrvj2jVT4pM%3D&itn2=jc7icOHu4kg%3D&itn3=jc7icOHu4kg%3D&pid=4&pm=&pg=2&tn=1&ito2=&ito3=&ks=jc7icOHu4kg%3D&st=1&pi=0&m=0&mn=All+Questions | 22 | duplicate or near-duplicate |
| Assembly Questions with the Index Term Children - AIMS Portal | enforcement_penalty_and_regulatory_expectations | https://aims.niassembly.gov.uk/terms/PrintResults.aspx?se=&so=Ascending&tb=&per=&sp=&fd=&td=&cb1=&cb2=&itn1=2OIfEXqLqNgwmfZ3YZr53Q%3D%3D&itn2=jc7icOHu4kg%3D&itn3=jc7icOHu4kg%3D&pid=4&pm=&pg=2&tn=1&ito2=&ito3=&ks=jc7icOHu4kg%3D&st=1&pi=0&m=0&mn=All+Questions | 22 | duplicate or near-duplicate |
| Sanctions Risk | enforcement_penalty_and_regulatory_expectations | https://www.sanctions-risk.com | 23 | duplicate or near-duplicate |
| Wolfsberg Group: Home | financial_institution_trade_finance_operating_impact | https://www.wolfsberg-principles.com | 21 | duplicate or near-duplicate |
| The Sanctions Minefield in Trade Finance: How to Stay Ahead \| sanctions.io | financial_institution_trade_finance_operating_impact | https://www.sanctions.io/blog/the-sanctions-minefield-in-trade-finance-how-to-stay-ahead | 21 | duplicate or near-duplicate |
| Assembly Questions with the Index Term Departmental responsibilities | contrary_clearance_or_de_escalation_evidence | https://aims.niassembly.gov.uk/terms/PrintResults.aspx?se=&so=Ascending&tb=&per=&sp=&fd=&td=&cb1=&cb2=&itn1=ySrULvCABBqYWwYDoiwEdNNquqw5bItTvrvj2jVT4pM%3D&itn2=jc7icOHu4kg%3D&itn3=jc7icOHu4kg%3D&pid=4&pm=&pg=2&tn=1&ito2=&ito3=&ks=jc7icOHu4kg%3D&st=1&pi=0&m=0&mn=All+Questions | 25 | duplicate or near-duplicate |
| Forensic Science Regulator: Code of Practice (accessible) - GOV.UK | contrary_clearance_or_de_escalation_evidence | https://www.gov.uk/government/publications/statutory-code-of-practice-for-forensic-science-activities/forensic-science-regulator-code-of-practice-accessible | 25 | duplicate or near-duplicate |
| Assembly Questions with the Index Term Children - AIMS Portal | contrary_clearance_or_de_escalation_evidence | https://aims.niassembly.gov.uk/terms/PrintResults.aspx?se=&so=Ascending&tb=&per=&sp=&fd=&td=&cb1=&cb2=&itn1=2OIfEXqLqNgwmfZ3YZr53Q%3D%3D&itn2=jc7icOHu4kg%3D&itn3=jc7icOHu4kg%3D&pid=4&pm=&pg=2&tn=1&ito2=&ito3=&ks=jc7icOHu4kg%3D&st=1&pi=0&m=0&mn=All+Questions | 25 | duplicate or near-duplicate |
| Sanctions in Trade Finance Masterclass - YouTube | contrary_clearance_or_de_escalation_evidence | https://www.youtube.com/watch?v=1i_t-PaJsEM | 25 | duplicate or near-duplicate |
| The Sanctions Minefield in Trade Finance: How to Stay ... | contrary_clearance_or_de_escalation_evidence | https://www.sanctions.io/blog/the-sanctions-minefield-in-trade-finance-how-to-stay-ahead | 25 | duplicate or near-duplicate |
| Wolfsberg Group: Home | sanctions_company_data_requirements_and_anti_overclaiming_controls | https://www.wolfsberg-principles.com | 21 | duplicate or near-duplicate |
| load more loading... no more news - ICC Digital Library | sanctions_company_data_requirements_and_anti_overclaiming_controls | https://library.iccwbo.org/content/tfb/news/tfb-news-loadMore.htm | 22 | duplicate or near-duplicate |
| Sanctions in Trade Finance Masterclass - YouTube | sanctions_company_data_requirements_and_anti_overclaiming_controls | https://www.youtube.com/watch?v=QB1Fnvn_yfw | 21 | duplicate or near-duplicate |

## Refresh Priorities

| Risk driver | Refresh trigger | Highest-weight sources |
| --- | --- | --- |
| UK sanctions / OFSI guidance | Refresh before approval if OFSI or UK sanctions guidance changes. | L1, L6 |
| Goods and end-use risk | Refresh if goods classification, licence, authorisation or end-use status changes. | L1, L2 |
| Counterparty and ownership exposure | Refresh if sanctions screening, beneficial ownership, bank or intermediary data changes. | L3, L9 |
| Documentation quality | Refresh when invoices, bills of lading, contracts, end-use statements or payment instructions change. | L5, L9 |
| Clearance evidence | Refresh before moving from legal hold or escalation back to approval. | L8 |

## Methodology and Review Controls

The source audit preserves the live Tavily search trail, selected/rejected source reasoning, coverage gaps and confidence limits. Law-firm or trade-association analysis is treated as specialist or financial-sector guidance, not official legal clearance. Transaction-specific use requires goods, counterparty, ownership, route, payment, licence and document data. Public-source evidence cannot replace transaction-specific screening, ownership review, document checks, licence validation or legal/compliance sign-off.
