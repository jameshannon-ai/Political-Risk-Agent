# Political Risk Brief
## Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk

| Field | Value |
| --- | --- |
| Risk issue | Sanctions/export-control exposure in trade finance transaction approval |
| Business lens | UK trade finance lender / bank / credit insurer |
| Region | UK trade finance / cross-border transaction screening |
| Time horizon | 1-3 months |
| Overall risk level | High |
| Confidence | 3/5 |
| Evidence mode | Live source retrieval |
| Source provider | tavily |

## 1. Decision Recommendation

| Item | Assessment |
| --- | --- |
| Recommended decision | Legal hold where goods, end-use, licence, payment or sanctioned-party red flags remain unresolved; otherwise escalate to sanctions/compliance review before approval. |
| Current stance | Escalate or hold where goods, counterparty, ownership, route, payment or documentation red flags are unresolved. |
| Approve if | Goods are non-controlled or licensed, counterparties screen clean, ownership is clear, route/payment are acceptable and documents are reliable. |
| Enhanced due diligence if | Residual uncertainty is documentable and controllable, with legal/compliance sign-off and facility conditions. |
| Legal hold trigger | Sanctioned counterparty, prohibited end-use, controlled goods without licence, payment red flag, missing core documents or unclear ownership. |
| Reject trigger | Confirmed sanctioned counterparty, prohibited end-use, false documents, unavailable required licence or unacceptable payment route. |

## 2. Scope and Specificity

This is a client-type sanctions and trade-finance exposure screen, not legal advice and not a transaction clearance decision. It models how a UK trade finance lender, bank or credit insurer should structure approval, escalation, legal-hold and rejection controls when public sanctions/export-control evidence intersects with a proposed transaction.

The output does not claim that any named borrower, buyer, vessel, bank, commodity or route is clear or prohibited. Transaction-specific use requires private deal data and legal/compliance sign-off.

## 3. Dashboard Summary

| Item | Value |
| --- | --- |
| Decision engine | approve / enhanced due diligence / escalate / legal hold / reject |
| Current stance | Escalate or hold where goods, counterparty, ownership, route, payment or documentation red flags are unresolved |
| Primary legal trigger | sanctioned counterparty, prohibited end-use, controlled goods without licence, or payment red flag |
| Primary commercial trigger | financing delay, documentation failure, credit exposure or insurance/underwriting exclusion |
| Evidence mode | Live source retrieval / saved showcase |
| Source provider | Tavily |
| Key data limits | Transaction-specific goods, counterparty, ownership, route, documents and licence data required |

## 4. Transaction Exposure Summary

| Exposure channel | Current assessment | Decision implication |
| --- | --- | --- |
| Goods / end-use | High in the illustrative screen because controlled goods and licence status are unresolved. | Legal hold until classification, end-use and licence position are clear. |
| Counterparty / ownership | Medium because public evidence cannot clear named parties or beneficial owners. | Escalate until screening and ownership evidence is complete. |
| Route / jurisdiction | Medium with diversion and transshipment risk requiring validation. | Enhanced route and logistics checks before approval. |
| Payment route | Unclear until bank/intermediary/payment path is validated. | Hold or escalate if payment red flags remain unresolved. |
| Documentation | Weak in the illustrative screen. | Request missing documents before drawdown or document honouring. |

## 5. Goods and End-Use Risk Assessment

| Control question | Assessment | Decision use |
| --- | --- | --- |
| Are goods controlled, dual-use or sanctions-sensitive? | Unclear/high in the illustrative scenario. | Hold until HS/commodity classification, control-list status and licence position are validated. |
| Is end-use or end-user clear? | Unclear without private transaction documents. | Escalate if end-use statement is missing, vague or inconsistent. |
| Is licence/authorisation confirmed? | Unclear in the illustrative scenario. | Legal hold if controlled goods require a licence and no valid authorisation is available. |

## 6. Counterparty and Ownership Risk Assessment

| Counterparty area | Assessment | Decision use |
| --- | --- | --- |
| Buyer / seller / consignee | Public evidence cannot clear named parties. | Screen all parties and hold if any designated or blocked party appears. |
| Beneficial ownership | Partial/unclear in the illustrative scenario. | Escalate until ownership/control evidence is complete. |
| Banks / intermediaries | Payment chain not validated. | Confirm correspondent, beneficiary and intermediary bank exposure before drawdown. |
| Vessel / logistics parties | Unclear in the illustrative scenario. | Screen vessel, carrier, freight forwarder and port agents where relevant. |

## 7. Jurisdiction, Route and Payment Risk Assessment

| Risk area | Assessment | Decision use |
| --- | --- | --- |
| Jurisdiction | Medium in the illustrative scenario. | Review sanctioned-jurisdiction nexus, origin, destination and transshipment. |
| Route / transshipment | Requires validation against diversion indicators. | Escalate unusual routing, inconsistent ports or unexplained intermediaries. |
| Payment route | Unclear until bank path is supplied. | Legal hold if payment instruction, intermediary bank or beneficiary creates a red flag. |
| Currency / correspondent bank | Not assessed without private data. | Validate payment processing feasibility before approval. |

## 8. Documentation Quality Assessment

| Document area | Current status | Decision use |
| --- | --- | --- |
| Invoices and contracts | Company-required. | Check goods, parties, price, delivery terms and sanctions clauses. |
| Bills of lading / transport documents | Company-required. | Reconcile vessel, ports, route and consignee. |
| End-use / end-user statement | Company-required. | Core approval evidence for end-use risk. |
| Ownership declarations | Company-required. | Supports counterparty and beneficial ownership screening. |
| Licence / exemption evidence | Company-required. | Required before approval where controlled goods or sanctions restrictions apply. |
| Payment instructions | Company-required. | Tests payment red flags and correspondent-bank feasibility. |

## 9. Transaction Decision Engine

| Input | Value | Status | Decision use |
| --- | --- | --- | --- |
| goods_control_risk | high | illustrative | Tests whether controlled goods or end-use risk trigger hold. |
| counterparty_risk | medium | illustrative | Tests whether counterparty exposure blocks routine approval. |
| jurisdiction_route_risk | medium | illustrative | Tests route/diversion escalation. |
| documentation_quality | weak | illustrative | Tests missing-document hold/escalation. |
| ownership_transparency | partial | illustrative | Tests beneficial ownership escalation. |
| licence_or_authorisation_status | unclear | company-required | Determines whether controlled goods can proceed. |
| payment_red_flag | unclear | company-required | Tests legal hold/payment review. |
| vessel_or_logistics_red_flag | unclear | company-required | Tests route/logistics escalation. |
| end_use_red_flag | unclear | company-required | Tests legal hold/end-use review. |

| Output | Value |
| --- | --- |
| Recommended decision | legal hold |
| Escalation required | true |
| Legal hold required | true |
| Rejection triggered | false |
| Confidence score | 3/5 |
| Decision rationale | High goods/end-use risk without confirmed licence or authorisation requires legal hold.; Missing or weak documents prevent routine approval.; Counterparty or ownership exposure is not clean enough for routine approval.; Unclear end-use requires enhanced due diligence. |
| Missing documents | invoice pack; bills of lading; contracts; end-user statement; beneficial ownership declaration; licence, authorisation or exemption evidence; bank/intermediary/payment route confirmation; vessel, port and logistics route evidence; end-use and end-user statement |

## 10. Due Diligence Actions

1. Classify goods and check whether they are controlled, dual-use or sanctions-sensitive.
2. Screen buyer, seller, consignee, banks, intermediaries and beneficial owners.
3. Validate end-use, end-user and diversion risk with supporting documents.
4. Confirm licence, authorisation or exemption status before approval or drawdown.
5. Check payment route, correspondent bank exposure and blocked-payment risk.
6. Validate ports, vessel, transshipment and logistics route before financing.
7. Escalate unresolved red flags to sanctions/compliance and legal sign-off.

## 11. Risk Scorecard

| Dimension | Score | Direction | Evidence-based rationale |
| --- | --- | --- | --- |
| Likelihood | 4/5 | Elevated | Official sanctions/end-use guidance, counterparty exposure, route/diversion indicators and documentation controls create a credible escalation pathway. |
| Impact | 4/5 | High | Unresolved sanctions, end-use, ownership, route, payment or document red flags can block financing, delay payment, trigger legal hold or require rejection. |
| Immediacy | 4/5 | Near-term | The decision must be made before approval, drawdown, document honouring or payment execution. |
| Confidence | 3/5 | Moderate | Confidence capped at 3/5 because live public evidence is strong enough for a client-type screen, but transaction-specific goods, counterparty, ownership, route, payment, licence and document data are missing. |

## 12. Evidence-To-Score Bridge

| Score dimension | Score | Evidence basis | Why not higher / lower | Review trigger |
| --- | --- | --- | --- | --- |
| Likelihood | 4/5 | Likelihood is driven by official UK sanctions/end-use guidance, controlled-goods risk, ownership/counterparty exposure and live route/diversion indicators. | Higher only with current transaction screening and licence data; lower would understate official/legal control evidence. | Refresh if sanctions designations, guidance or export-control rules change. |
| Impact | 4/5 | Impact is driven by legal hold/rejection risk, payment blockage, documentation failure, credit exposure, insurance/underwriting exclusion and regulatory penalty consequences. | Higher if a sanctioned party/prohibited end-use is confirmed; lower if clean documents and licences resolve red flags. | Refresh when payment, credit, insurance or document risk changes. |
| Immediacy | 4/5 | Immediacy is high because checks must be resolved before approval, drawdown, document honouring or payment execution. | Higher if drawdown/payment is imminent; lower if transaction is only early-stage pipeline. | Refresh before approval, drawdown or payment execution. |
| Confidence | 3/5 | Confidence is capped because public evidence does not include transaction-specific goods, ownership, screening, route, payment, licence or document data. | Public sources support a screen, not transaction clearance. | Increase only after BOM/goods, counterparty, ownership, route, payment and document data are supplied. |

## 13. Source Requirement Coverage

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

## 14. Source Quality Notes

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

## 15. Selected Sources

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

## 16. Evidence Appendix

| Source ID | Requirement | Source role | Evidence weight | Claim | Concrete signal | Decision use | Caveat | Refresh trigger |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | uk_sanctions_ofsi_official_guidance | official_anchor | medium | GOV.UK guidance confirms that sanctions end-use controls can make goods, technology, destination, end user and licence status decisive for whether a transaction may proceed. | Official UK sanctions end-use guidance | Anchors UK sanctions screening, OFSI escalation and legal-hold thresholds for trade finance approval. | Official guidance must be refreshed before approving a live transaction because sanctions scope and licensing practice can change. | Refresh before approval if UK sanctions, OFSI or end-use guidance changes. |
| L2 | sanctions_end_use_controls_and_controlled_goods_risk | regulatory_guidance | medium | GOV.UK exporter notices provide an official channel for export-control and licence updates that can affect controlled goods, dual-use items and end-use review. | Official export-control update channel | Supports goods classification, controlled-goods checks and licence/authorisation hold triggers before drawdown. | Notices must be checked against the exact goods, destination and transaction date. | Refresh if goods classification, licence status or exporter notices change. |
| L3 | counterparty_and_ownership_exposure | regulatory_guidance | medium | OFSI financial sanctions guidance highlights designated-person exposure, ownership/control issues, reporting obligations, licence conditions and offences relevant to transaction approval. | Ownership/control and reporting obligations | Supports counterparty, beneficial ownership, intermediary, bank and consignee screening decisions. | Public guidance does not clear a named counterparty; transaction-specific screening and ownership data are still required. | Refresh if buyer, seller, beneficial owner, bank, intermediary, vessel or consignee data changes. |
| L4 | jurisdiction_route_and_diversion_exposure | specialist_interpretation | medium | Reuters Practical Law describes sanctions and export-control compliance as requiring structured risk assessment across counterparties, jurisdictions, goods, screening and documentation. | Compliance roadmap / specialist interpretation | Supports escalation where jurisdiction, route, transshipment or diversion indicators are unresolved. | This is specialist interpretation rather than live official route intelligence; refresh Reuters/AP or official diversion evidence before operational reliance. | Refresh if route, port, transshipment, diversion or sanctioned-jurisdiction indicators change. |
| L5 | documentation_and_transaction_quality_evidence | financial_sector_guidance | medium | ICC Academy trade-finance guidance links sanctions risk to letters of credit, bank document review and the need to identify sanctions problems before payment or honouring obligations. | Letters of credit / document-review guidance | Supports document-request and hold triggers for invoices, bills of lading, end-use statements and payment instructions. | Useful operating guidance, but transaction documents must still be reviewed against internal policy and legal advice. | Refresh when invoices, bills of lading, end-use statements, ownership declarations or payment instructions change. |
| L6 | enforcement_penalty_and_regulatory_expectations | enforcement_evidence | medium | OFSI strategy emphasises licensing, enforcement, suspected breach reporting, practical guidance and stronger financial-sanctions compliance controls. | OFSI strategy 2026-29 | Supports legal-hold and rejection thresholds by showing regulatory consequences and expected controls. | Strategy evidence shows regulatory expectation, not a transaction-specific enforcement finding. | Refresh if OFSI enforcement, licensing, breach-reporting or compliance expectations change. |
| L7 | financial_institution_trade_finance_operating_impact | financial_sector_guidance | medium | BAFT trade-finance resources point to bank operating controls, KYC expectations and documentation discipline as core parts of transaction risk management. | Trade-finance operating-impact guidance | Supports facility conditions, drawdown controls, credit exposure review and operational escalation. | The selected BAFT page is a weak/secondary source and should be replaced with specific bank policy, ICC/Wolfsberg/BAFT principles or regulator guidance before operational use. | Refresh before approval, drawdown, payment execution or credit/insurance commitment. |
| L8 | contrary_clearance_or_de_escalation_evidence | contrary_scope_limit | medium | GOV.UK guidance explains that exceptions and licences may permit certain transactions, goods or services, but only after checking the relevant sanctions measure and licence conditions. | Exceptions / licence pathway | Supports approval or enhanced due diligence only where clean counterparties, licences, exemptions and documents resolve red flags. | Licence or exception evidence is not an all-clear; it must match the exact goods, counterparties, route and transaction facts. | Refresh before moving a held transaction back to enhanced due diligence or approval. |
| L9 | sanctions_company_data_requirements_and_anti_overclaiming_controls | company_required_data | medium | The Wolfsberg, ICC and BAFT trade finance principles identify transaction parties, goods, documents, routing and red-flag review as core inputs for financial crime and sanctions controls. | Trade finance principles / red-flag inputs | Supports anti-overclaiming controls by showing the transaction data still required before clearance. | Principles are maintained guidance, not transaction clearance; internal risk appetite and legal/compliance sign-off remain required. | Refresh when transaction-specific goods, counterparty, ownership, route, payment, licence or document data becomes available. |

## 17. Source Audit Summary

| Item | Value |
| --- | --- |
| Search provider | tavily |
| Evidence mode | Live source retrieval |
| Fallback data used | false |
| Total queries run | 36 |
| Candidate sources | 76 |
| Selected sources | 9 |
| Rejected sources | 67 |
| Fetch failures | 1 |
| Source hierarchy coverage | 100% requirement coverage with caveated partial areas |
| Confidence cap reason | Confidence capped at 3/5 because live public evidence is strong enough for a client-type screen, but transaction-specific goods, counterparty, ownership, route, payment, licence and document data are missing. |
| Refresh priorities | Refresh before approval if OFSI or UK sanctions guidance changes.; Refresh if goods classification, licence, authorisation or end-use status changes.; Refresh if sanctions screening, beneficial ownership, bank or intermediary data changes.; Refresh when invoices, bills of lading, contracts, end-use statements or payment instructions change.; Refresh before moving from legal hold or escalation back to approval. |

## 18. Methodology and Review Controls

Method: source plan, live Tavily retrieval, source ranking, source fetching, claim cleanup, source requirement coverage, transaction decision model, evidence-to-score bridge, confidence cap and review controls.

This is a client-type sanctions and trade-finance exposure screen, not legal advice and not a transaction clearance decision.

Transaction-specific use requires:

- goods description and HS/commodity classification
- end-use and end-user statement
- buyer, seller, consignee and beneficial ownership data
- sanctions screening results
- bank/intermediary/payment route
- ports, vessel and logistics route
- licences, authorisations or exemptions
- invoices, bills of lading, contracts and insurance documents
- internal risk appetite and legal/compliance sign-off

| Control | Status | Required action |
| --- | --- | --- |
| Evidence mode | Passed | Live Tavily-backed source retrieval is visible; dashboard uses saved files only. |
| Legal advice boundary | Warning | Treat this as a client-type exposure screen, not legal advice or clearance. |
| Transaction data | Warning | Obtain goods, counterparty, ownership, route, payment, licence and document data. |
| Source freshness | Review | Refresh official guidance and live sanctions/diversion developments before operational use. |
| Approval governance | Warning | Approval, hold, rejection or relaxation requires legal/compliance sign-off. |
