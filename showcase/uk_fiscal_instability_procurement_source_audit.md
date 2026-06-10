# Source Audit

## Search Configuration

- Topic: UK fiscal instability and public-sector procurement delay risk
- Business user: UK infrastructure contractor bidding for government-funded transport and energy projects
- Region: United Kingdom
- Time horizon: 1-6 months
- Concerns: fiscal credibility, gilt-market sensitivity, public finances, departmental budgets, procurement delays, project deferrals, payment risk, contract repricing, working capital exposure
- Search provider used: tavily
- Evidence mode: Live source retrieval
- Fallback data used: false
- Provider error: None
- Retrieval timestamp: 2026-06-09T10:59:15

## Research Plan

- Research objective: Build a governed evidence base for UK infrastructure contractor decision-making on UK fiscal instability and public-sector procurement delay risk in United Kingdom over 1-6 months, using the uk_fiscal_procurement_risk domain pack.
- Decision questions:
  - Should the contractor review its public-sector bid pipeline because fiscal pressure may slow or defer awards?
  - Do gilt-market sensitivity and fiscal credibility concerns justify board-level exposure monitoring?
  - Could departmental budget uncertainty affect project timing, payment assumptions or contract repricing?
  - Which public-sector customers, departments or programmes require payment-risk monitoring?
  - What contractor-specific order book, margin and working-capital data is needed before operational use?
  - What evidence would justify relaxing from heightened monitoring back to normal bid governance?
  - Does official fiscal-risk evidence show constrained headroom or spending pressure that could affect public procurement confidence?
  - Do official public-finance indicators support monitoring of payment, award or departmental-budget pressure?
  - Does HM Treasury or government policy indicate spending constraints, reprioritisation or budget uncertainty relevant to bids?
  - Are gilt-market, rates or financial-stability conditions sensitive enough to affect public-sector financing confidence?
  - Does credible market analysis show fiscal credibility or gilt-yield risk that should trigger board monitoring?
  - Is there evidence that public procurement, infrastructure awards or departmental programmes face delay or deferral pressure?
  - Should contractors monitor working-capital, payment and repricing exposure across public-sector counterparties?
  - What evidence would justify easing from heightened bid-pipeline and payment-risk monitoring?
  - What contract backlog, customer mix, payment terms, bid pipeline and working-capital data is needed before operational use?
- Required source mix:
  - official fiscal outlook / fiscal risks
  - official public finances data
  - government fiscal policy / spending control
  - gilt-market or financial-stability evidence
  - market analysis on fiscal credibility
  - public procurement / infrastructure delay evidence
  - contractor industry payment or working-capital evidence
  - contrary or stabilising fiscal evidence
- Expected evidence types: official_primary, official_guidance, economic_data, market_indicator, specialist_analysis, industry_guidance, reputable_news, contrary_or_stabilising_evidence
- Minimum acceptable coverage: {'minimum_total_requirements': 9, 'minimum_high_priority_requirements': 5, 'high_priority_requirements': ['obr_fiscal_outlook_and_fiscal_risks', 'ons_public_finances_data', 'hm_treasury_fiscal_policy_and_spending_control', 'public_procurement_and_infrastructure_delay_evidence', 'company_data_requirements_for_contractor_exposure'], 'minimum_sources_per_requirement': {'REQ-FISC-A': 1, 'REQ-FISC-B': 1, 'REQ-FISC-C': 1, 'REQ-FISC-D': 1, 'REQ-FISC-E': 1, 'REQ-FISC-F': 1, 'REQ-FISC-G': 1, 'REQ-FISC-H': 1, 'REQ-FISC-I': 1}}
- Refresh priorities:
  - obr_fiscal_outlook_and_fiscal_risks: Latest OBR outlook, fiscal risks or maintained fiscal sustainability evidence.
  - ons_public_finances_data: Latest ONS public sector finances release.
  - hm_treasury_fiscal_policy_and_spending_control: Current Budget, Spending Review, fiscal statement or departmental spending material.
  - bank_of_england_gilt_market_and_financial_stability: Current or recent Bank of England market, financial stability or monetary-policy material.
  - credible_market_analysis_on_gilts_and_fiscal_credibility: Recent market analysis or live reporting where it adds current context.
  - public_procurement_and_infrastructure_delay_evidence: Current procurement, infrastructure pipeline, NAO/IPA or sector evidence.
  - contractor_industry_working_capital_and_payment_risk: Recent or maintained industry/business evidence.
  - contrary_or_stabilising_fiscal_evidence: Current official or credible stabilising evidence.
  - company_data_requirements_for_contractor_exposure: Maintained commercial guidance plus company-specific data before operational use.

## Source Strategy

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: obr_fiscal_outlook_and_fiscal_risks
- Evidence question: Does official fiscal-risk evidence show constrained headroom or spending pressure that could affect public procurement confidence?
- Preferred domains: obr.uk, obr.uk/docs
- Preferred source types: official_primary, economic_data
- Generated queries:
  - site:obr.uk Economic and fiscal outlook 2026 fiscal headroom debt interest borrowing
  - site:obr.uk Fiscal risks and sustainability 2025 UK debt interest spending pressures
  - site:obr.uk welfare trends spending pressures fiscal outlook public finances 2026
  - site:obr.uk UK fiscal instability and public-sector procurement delay risk obr fiscal outlook and fiscal risks 1-6 months
- Minimum acceptable evidence: 1
- Refresh expectation: Latest OBR outlook, fiscal risks or maintained fiscal sustainability evidence.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: ons_public_finances_data
- Evidence question: Do official public-finance indicators support monitoring of payment, award or departmental-budget pressure?
- Preferred domains: ons.gov.uk
- Preferred source types: official_primary, economic_data
- Generated queries:
  - site:ons.gov.uk public sector finances UK latest borrowing debt interest 2026
  - site:ons.gov.uk public sector finances borrowing debt UK fiscal position May 2026
  - site:ons.gov.uk UK fiscal instability and public-sector procurement delay risk ons public finances data 1-6 months
- Minimum acceptable evidence: 1
- Refresh expectation: Latest ONS public sector finances release.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: hm_treasury_fiscal_policy_and_spending_control
- Evidence question: Does HM Treasury or government policy indicate spending constraints, reprioritisation or budget uncertainty relevant to bids?
- Preferred domains: gov.uk, hmtreasury.gov.uk
- Preferred source types: official_primary, official_guidance
- Generated queries:
  - site:gov.uk Spending Review 2025 departmental budgets infrastructure HM Treasury
  - site:gov.uk Spring Statement 2025 fiscal rules departmental spending public investment
  - site:gov.uk HM Treasury fiscal rules public spending infrastructure pipeline
  - site:gov.uk UK fiscal instability and public-sector procurement delay risk hm treasury fiscal policy and spending control 1-6 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current Budget, Spending Review, fiscal statement or departmental spending material.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: bank_of_england_gilt_market_and_financial_stability
- Evidence question: Are gilt-market, rates or financial-stability conditions sensitive enough to affect public-sector financing confidence?
- Preferred domains: bankofengland.co.uk
- Preferred source types: official_primary, market_indicator
- Generated queries:
  - site:bankofengland.co.uk financial stability report gilt market government bonds 2025 2026
  - site:bankofengland.co.uk gilt market conditions financial stability UK rates 2026
  - site:bankofengland.co.uk monetary policy report gilt yields UK government bonds
  - site:bankofengland.co.uk UK fiscal instability and public-sector procurement delay risk bank of england gilt market and financial stability 1-6 months
- Minimum acceptable evidence: 1
- Refresh expectation: Current or recent Bank of England market, financial stability or monetary-policy material.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: credible_market_analysis_on_gilts_and_fiscal_credibility
- Evidence question: Does credible market analysis show fiscal credibility or gilt-yield risk that should trigger board monitoring?
- Preferred domains: reuters.com, ft.com, ifs.org.uk, resolutionfoundation.org, niesr.ac.uk
- Preferred source types: specialist_analysis, reputable_news, market_indicator
- Generated queries:
  - site:reuters.com UK gilt yields fiscal credibility public finances 2026
  - site:ifs.org.uk UK fiscal outlook spending review debt interest 2026
  - site:resolutionfoundation.org UK fiscal headroom gilt yields public finances 2026
  - site:reuters.com UK fiscal instability and public-sector procurement delay risk credible market analysis on gilts and fiscal credibility 1-6 months
  - UK fiscal instability and public-sector procurement delay risk credible market analysis on gilts and fiscal credibility specialist analysis
  - site:reuters.com UK fiscal instability and public-sector procurement delay risk credible market analysis on gilts and fiscal credibility
- Minimum acceptable evidence: 1
- Refresh expectation: Recent market analysis or live reporting where it adds current context.

### official_primary

- Why it matters: Establishes verified safety, security or regulatory baseline.
- Source requirement: public_procurement_and_infrastructure_delay_evidence
- Evidence question: Is there evidence that public procurement, infrastructure awards or departmental programmes face delay or deferral pressure?
- Preferred domains: nao.org.uk, ipa.gov.uk, gov.uk, cabinetoffice.gov.uk, constructionleadershipcouncil.co.uk, reuters.com
- Preferred source types: official_primary, industry_guidance, specialist_analysis, reputable_news
- Generated queries:
  - site:nao.org.uk infrastructure projects delay public procurement major projects 2025 2026
  - site:ipa.gov.uk annual report on major projects infrastructure delays government portfolio 2025
  - site:gov.uk National Infrastructure and Construction Pipeline 2025 procurement projects
  - site:gov.uk Construction Pipeline public procurement infrastructure projects 2026
  - site:cabinetoffice.gov.uk public procurement pipeline infrastructure government contracts
  - site:nao.org.uk UK fiscal instability and public-sector procurement delay risk public procurement and infrastructure delay evidence 1-6 months
  - UK fiscal instability and public-sector procurement delay risk public procurement and infrastructure delay evidence specialist analysis
  - site:reuters.com UK fiscal instability and public-sector procurement delay risk public procurement and infrastructure delay evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current procurement, infrastructure pipeline, NAO/IPA or sector evidence.

### industry_guidance

- Why it matters: Supports evidence coverage.
- Source requirement: contractor_industry_working_capital_and_payment_risk
- Evidence question: Should contractors monitor working-capital, payment and repricing exposure across public-sector counterparties?
- Preferred domains: builduk.org, civilengineeringcontractors.com, constructionleadershipcouncil.co.uk, icaew.com
- Preferred source types: industry_guidance, company_update, specialist_analysis
- Generated queries:
  - site:builduk.org construction payment performance public sector working capital 2025 2026
  - site:civilengineeringcontractors.com infrastructure contractor procurement delay payment risk 2025
  - site:constructionleadershipcouncil.co.uk payment performance construction working capital procurement
  - site:icaew.com late payments construction working capital public sector 2025
  - site:builduk.org UK fiscal instability and public-sector procurement delay risk contractor industry working capital and payment risk 1-6 months
  - UK fiscal instability and public-sector procurement delay risk contractor industry working capital and payment risk specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Recent or maintained industry/business evidence.

### contrary_or_stabilising_evidence

- Why it matters: Tests the downside case and supports confidence discipline.
- Source requirement: contrary_or_stabilising_fiscal_evidence
- Evidence question: What evidence would justify easing from heightened bid-pipeline and payment-risk monitoring?
- Preferred domains: gov.uk, obr.uk, bankofengland.co.uk, ifs.org.uk, ipa.gov.uk
- Preferred source types: contrary_or_stabilising_evidence, official_primary, specialist_analysis
- Generated queries:
  - site:gov.uk National Infrastructure and Construction Pipeline committed projects 2025
  - site:gov.uk 10 Year Infrastructure Strategy pipeline certainty 2025
  - site:obr.uk fiscal headroom debt falling forecast public finances 2026
  - site:bankofengland.co.uk gilt market functioning stable financial stability 2025
  - site:gov.uk UK fiscal instability and public-sector procurement delay risk contrary or stabilising fiscal evidence 1-6 months
  - UK fiscal instability and public-sector procurement delay risk contrary or stabilising fiscal evidence specialist analysis
  - UK fiscal instability and public-sector procurement delay risk contrary or stabilising fiscal evidence scope limited stabilising contrary evidence
- Minimum acceptable evidence: 1
- Refresh expectation: Current official or credible stabilising evidence.

### specialist_analysis

- Why it matters: Adds market interpretation and scenario framing.
- Source requirement: company_data_requirements_for_contractor_exposure
- Evidence question: What contract backlog, customer mix, payment terms, bid pipeline and working-capital data is needed before operational use?
- Preferred domains: builduk.org, icaew.com, constructionleadershipcouncil.co.uk
- Preferred source types: specialist_analysis, industry_guidance, company_update
- Generated queries:
  - site:builduk.org construction contractor working capital payment terms public sector clients
  - site:icaew.com construction working capital public sector contract payment risk
  - site:builduk.org UK fiscal instability and public-sector procurement delay risk company data requirements for contractor exposure 1-6 months
  - UK fiscal instability and public-sector procurement delay risk company data requirements for contractor exposure specialist analysis
- Minimum acceptable evidence: 1
- Refresh expectation: Maintained commercial guidance plus company-specific data before operational use.

## Search Results Summary

- Total candidate sources found: 98
- Total queries run: 46
- Total selected sources: 9
- Duplicate URLs removed: 0
- Source categories covered: contrary_or_stabilising_evidence, industry_guidance, market_indicator, official_primary, specialist_analysis
- Source categories missing: None
- Fetch failures: 0

## Quantified Evidence Summary

- Source count: 9
- Requirements identified: 9/9
- Strongly covered: 1/9
- Direct snippet-only: 8/9
- Partial or indirect: 0/9
- Historical/context only: 0/9
- Missing: 0/9
- High-weight source count: 3
- Quantified facts: 8
- Score support summary: Scores are supported by 9 selected sources, 100% requirement coverage and 8 extracted quantified facts.
- Confidence cap reason: Confidence capped because public evidence can screen fiscal/procurement risk, but contractor order book, department exposure, payment terms, margins and working-capital data are required for operational decisions.

## Provenance And Extraction Limits

| Source ID | Evidence mode | Fetch status | Inference strength | Extraction confidence | Human review | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | full_text | ok | moderate | high | false | Fetched text available; analyst should still verify context and recency. |
| L2 | snippet_only | snippet_used | direct | low | true | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L3 | snippet_only | snippet_used | direct | low | true | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L4 | snippet_only | snippet_used | direct | low | true | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L5 | snippet_only | snippet_used | moderate | low | true | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L6 | snippet_only | snippet_used | direct | low | true | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L7 | snippet_only | snippet_used | moderate | low | true | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L8 | snippet_only | snippet_used | moderate | low | true | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L9 | snippet_only | snippet_used | weak | low | true | Snippet-only stored candidate evidence; verify full source text before operational use. |

## Scoring Traceability

| Dimension | Score | Label | Confidence | Supporting Evidence | Contrary Evidence | Evidence Quality Limits | Missing Evidence | Cap / Review Reason |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| likelihood | 4 | High | medium | L1, L2, L4, L5, L8 | L8 | L2, L3, L4, L5, L6, L7, L8, L9 | None | Capped because at least one selected source used snippet-only evidence. |
| impact | 4 | High | medium | L1, L3, L6, L9 | L8 | L2, L3, L4, L5, L6, L7, L8, L9 | None | Capped because at least one selected source used snippet-only evidence. |
| immediacy | 3 | Moderate | medium | L4 | L8 | L2, L3, L4, L5, L6, L7, L8, L9 | None | Capped because at least one selected source used snippet-only evidence. |
| exposure | 4 | High | medium | L2, L3, L6, L7, L8, L9 | L8 | L2, L3, L4, L5, L6, L7, L8, L9 | None | Capped because at least one selected source used snippet-only evidence. |
| confidence | 3 | Moderate | low | L1, L2, L8, L9 | L8 | L2, L3, L4, L5, L6, L7, L8, L9 | contractor order book by public-sector customer, departmental bid pipeline and award timing, margin and working-capital sensitivity, payment terms, retentions and aged receivables | Confidence capped because public evidence can screen fiscal/procurement risk, but contractor order book, department exposure, payment terms, margins and working-capital data are required for operational decisions. |
| decision_urgency | 4 | High | medium | L1, L2, L3 | L8 | L2, L3, L4, L5, L6, L7, L8, L9 | None | Capped because at least one selected source used snippet-only evidence. |

## Source Requirement Coverage

- Requirements identified: 9/9
- Strongly covered: 1/9
- Direct snippet-only: 8/9
- Partial or indirect: 0/9
- Historical/context only: 0/9
- Missing: 0/9

| Requirement | Coverage Grade | Supporting Sources | Reason For Grade | Remaining Gap | Gap Affects Confidence |
| --- | --- | --- | --- | --- | --- |
| obr_fiscal_outlook_and_fiscal_risks | strong_direct_full_text | L1 | L1 provides direct full-text or PDF-text evidence for the requirement. | No major source-coverage gap; verify recency, context and operational applicability. | false |
| ons_public_finances_data | direct_snippet_only | L2 | L2 is mapped to the requirement but only snippet/metadata evidence is available. | Mapped source is snippet-only; verify full source text before using this requirement operationally. | true |
| hm_treasury_fiscal_policy_and_spending_control | direct_snippet_only | L3 | L3 is mapped to the requirement but only snippet/metadata evidence is available. | Mapped source is snippet-only; verify full source text before using this requirement operationally. | true |
| bank_of_england_gilt_market_and_financial_stability | direct_snippet_only | L4 | L4 is mapped to the requirement but only snippet/metadata evidence is available. | Mapped source is snippet-only; verify full source text before using this requirement operationally. | true |
| credible_market_analysis_on_gilts_and_fiscal_credibility | direct_snippet_only | L5 | L5 is mapped to the requirement but only snippet/metadata evidence is available. | Mapped source is snippet-only; verify full source text before using this requirement operationally. | true |
| public_procurement_and_infrastructure_delay_evidence | direct_snippet_only | L6 | L6 is mapped to the requirement but only snippet/metadata evidence is available. | Mapped source is snippet-only; verify full source text before using this requirement operationally. | true |
| contractor_industry_working_capital_and_payment_risk | direct_snippet_only | L7 | L7 is mapped to the requirement but only snippet/metadata evidence is available. | Mapped source is snippet-only; verify full source text before using this requirement operationally. | true |
| contrary_or_stabilising_fiscal_evidence | direct_snippet_only | L8 | L8 is mapped to the requirement but only snippet/metadata evidence is available. | Mapped source is snippet-only; verify full source text before using this requirement operationally. | true |
| company_data_requirements_for_contractor_exposure | direct_snippet_only | L9 | L9 is mapped to the requirement but only snippet/metadata evidence is available. | Mapped source is snippet-only; verify full source text before using this requirement operationally. | true |

## Selected Sources

| Source ID | Requirement | Source role | Source value | Query | Decision Question | Title | Reliability | Relevance | Recency | Specificity | Decision value | Independence | Evidence weight | Selection reason | Decision use | Fetch Status | Caveat |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| L1 | obr_fiscal_outlook_and_fiscal_risks | official_anchor | Official fiscal baseline for headroom, borrowing, debt and fiscal-risk constraints. | site:obr.uk Economic and fiscal outlook 2026 fiscal headroom debt interest borrowing | Does official fiscal-risk evidence show constrained headroom or spending pressure that could affect public procurement confidence? | Economic and fiscal outlook – March 2026 | 5 | 5 | 3 | 3 | 5 | 5 | high | trusted domain, direct topic match, fits official_primary | Supports likelihood scoring for continued fiscal pressure and departmental budget uncertainty. | ok | Fetched text available; analyst should still verify context and recency. |
| L2 | ons_public_finances_data | data_or_indicator_source | Official public-finance indicator source for borrowing, deficit and debt monitoring. | site:ons.gov.uk public sector finances borrowing debt UK fiscal position May 2026 | Do official public-finance indicators support monitoring of payment, award or departmental-budget pressure? | Public sector finances, UK - Office for National Statistics | 5 | 4 | 3 | 3 | 3 | 5 | medium |  | Supports public-finance monitoring for borrowing, debt and fiscal-pressure indicators. | snippet_used | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L3 | hm_treasury_fiscal_policy_and_spending_control | official_anchor | Government spending-control and departmental budget source for procurement confidence. | site:gov.uk Spring Statement 2025 fiscal rules departmental spending public investment | Does HM Treasury or government policy indicate spending constraints, reprioritisation or budget uncertainty relevant to bids? | Spending Review 2025 (HTML) | 5 | 4 | 3 | 3 | 2 | 5 | high |  | Supports bid-pipeline review by showing departmental spending plans and capital-budget signals. | snippet_used | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L4 | bank_of_england_gilt_market_and_financial_stability | data_or_indicator_source | Official market and financial-stability source for gilt-yield sensitivity. | site:bankofengland.co.uk monetary policy report gilt yields UK government bonds | Are gilt-market, rates or financial-stability conditions sensitive enough to affect public-sector financing confidence? | What were the drivers of UK long-term interest rates in 2025? | 5 | 4 | 3 | 3 | 3 | 5 | medium |  | Supports board monitoring where long-rate and gilt-market sensitivity affect public-finance confidence. | snippet_used | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L5 | credible_market_analysis_on_gilts_and_fiscal_credibility | specialist_interpretation | Specialist fiscal analysis source for debt-interest pressure and fiscal credibility. | site:ifs.org.uk UK fiscal outlook spending review debt interest 2026 | Does credible market analysis show fiscal credibility or gilt-yield risk that should trigger board monitoring? | Outlook for the public finances \| Institute for Fiscal Studies - IFS | 4 | 4 | 3 | 3 | 2 | 5 | medium |  | Supports market-confidence assessment and debt-interest pressure review. | snippet_used | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L6 | public_procurement_and_infrastructure_delay_evidence | official_anchor | Official programme-delivery evidence showing how funding, scope and timetable changes affect projects. | site:nao.org.uk infrastructure projects delay public procurement major projects 2025 2026 | Is there evidence that public procurement, infrastructure awards or departmental programmes face delay or deferral pressure? | Update on the New Hospital Programme | 5 | 4 | 3 | 3 | 3 | 5 | high |  | Supports impact scoring for programme delay, project deferral and public-sector contract timing. | snippet_used | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L7 | contractor_industry_working_capital_and_payment_risk | operator_or_industry_guidance | Professional-body evidence on late payment and working-capital stress for suppliers. | site:icaew.com late payments construction working capital public sector 2025 | Should contractors monitor working-capital, payment and repricing exposure across public-sector counterparties? | Late Payments: Tackling Poor Payment Practices - ICAEW.com | 5 | 4 | 3 | 3 | 2 | 5 | medium |  | Supports payment-risk monitoring and working-capital stress testing. | snippet_used | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L8 | contrary_or_stabilising_fiscal_evidence | contrary_scope_limit | Official strategy evidence showing committed infrastructure pipeline and stabilising policy intent. | site:gov.uk 10 Year Infrastructure Strategy pipeline certainty 2025 | What evidence would justify easing from heightened bid-pipeline and payment-risk monitoring? | 10 Year Infrastructure Strategy | 4 | 4 | 3 | 3 | 2 | 5 | medium |  | Supports relaxation triggers by showing committed infrastructure strategy and pipeline policy intent. | snippet_used | Snippet-only stored candidate evidence; verify full source text before operational use. |
| L9 | company_data_requirements_for_contractor_exposure | company_required_data | Industry evidence illustrating why contractor-specific retentions, working capital and project data matter. | site:builduk.org construction contractor working capital payment terms public sector clients | What contract backlog, customer mix, payment terms, bid pipeline and working-capital data is needed before operational use? | Retention Payments in the Construction Industry - Build UK | 4 | 4 | 3 | 3 | 3 | 5 | medium | trusted domain, direct topic match, fits specialist_analysis | Supports anti-overclaiming by showing why contractor-specific payment, retention and working-capital data are needed. | snippet_used | Snippet-only stored candidate evidence; verify full source text before operational use. |

## Rejected Sources

| Title | Requirement | Query | Total score | Lowest scoring dimension | Rejection reason | Stronger source covered same requirement |
| --- | --- | --- | ---: | --- | --- | --- |
| Spending Review 2025 (HTML) - GOV.UK | hm_treasury_fiscal_policy_and_spending_control | site:gov.uk Spring Statement 2025 fiscal rules departmental spending public investment | 23 | independence_score | duplicate or near-duplicate | no |
| Infrastructure Pipeline | public_procurement_and_infrastructure_delay_evidence | site:gov.uk Construction Pipeline public procurement infrastructure projects 2026 | 25 | independence_score | duplicate or near-duplicate | no |
| [XLS] National Infrastructure and Construction Pipeline - GOV.UK | contrary_or_stabilising_fiscal_evidence | site:gov.uk National Infrastructure and Construction Pipeline committed projects 2025 | 26 | independence_score | duplicate or near-duplicate | no |
| Projects worth £600 billion in the pipeline as government gets ... | contrary_or_stabilising_fiscal_evidence | site:gov.uk National Infrastructure and Construction Pipeline committed projects 2025 | 26 | independence_score | duplicate or near-duplicate | no |
| The Infrastructure Pipeline | contrary_or_stabilising_fiscal_evidence | site:gov.uk 10 Year Infrastructure Strategy pipeline certainty 2025 | 26 | independence_score | duplicate or near-duplicate | no |
| Economic and fiscal outlook – March 2026 | contrary_or_stabilising_fiscal_evidence | site:obr.uk fiscal headroom debt falling forecast public finances 2026 | 27 | independence_score | duplicate or near-duplicate | no |
| Enhancing the resilience of the gilt repo market \| Bank of England | contrary_or_stabilising_fiscal_evidence | site:bankofengland.co.uk gilt market functioning stable financial stability 2025 | 25 | independence_score | duplicate or near-duplicate | no |
| , 15 January 2022 - 11 April 2028 - Herefordshire Council | contrary_or_stabilising_fiscal_evidence | site:gov.uk UK fiscal instability and public-sector procurement delay risk contrary or stabilising fiscal evidence 1-6 months | 25 | independence_score | duplicate or near-duplicate | no |
| Assembly Questions with the Index Term Children - AIMS Portal | contrary_or_stabilising_fiscal_evidence | site:gov.uk UK fiscal instability and public-sector procurement delay risk contrary or stabilising fiscal evidence 1-6 months | 25 | independence_score | duplicate or near-duplicate | no |
| UK public sector procurement priorities for 2026: What leaders need ... | contrary_or_stabilising_fiscal_evidence | UK fiscal instability and public-sector procurement delay risk contrary or stabilising fiscal evidence specialist analysis | 26 | independence_score | duplicate or near-duplicate | no |

## Evidence Coverage Assessment

- Strongest evidence category: official_primary
- Weakest evidence category: None identified
- Missing evidence: None identified
- Contrary/stabilising evidence: Present
- Confidence impact: Evidence coverage supports higher confidence, subject to analyst review.

## Scenario And Exposure Limits

- Public evidence screens fiscal, procurement and payment-risk exposure; it does not measure a contractor-specific order book.
- Replace public evidence with customer mix, bid pipeline, payment terms, margin and working-capital data before operational use.
- Treat procurement-delay and payment-risk scoring as decision-support, not a forecast of any individual contract award or payment.

## Refresh Triggers

- Refresh OBR outlook and ONS public-finance data after new releases.
- Refresh HM Treasury spending, Budget or Spending Review material after fiscal-policy updates.
- Refresh Bank of England and market-confidence evidence if gilt yields or financial-stability signals move materially.
- Refresh procurement and infrastructure-pipeline evidence before changing bid/no-bid or project-delay controls.
- Replace public evidence with contractor order book, customer mix, payment terms, margin and working-capital data before operational use.

## Analyst Review Controls

- Verify publication dates and current fiscal-policy context.
- Verify snippet-only sources against full source text before operational use.
- Refresh OBR, ONS, HM Treasury and Bank of England evidence after material releases.
- Check procurement pipeline and department-specific programme exposure before bid decisions.
- Validate payment terms, retentions, aged receivables, margins and working-capital exposure with company data.
- Escalate concentrated public-sector exposure to finance, commercial and board review before changing controls.
