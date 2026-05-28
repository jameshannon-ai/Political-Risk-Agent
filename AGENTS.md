# Political Risk Agent — Agent Instructions

## Project purpose
Political Risk Agent is a reusable, source-audited intelligence workflow for converting political, geopolitical and regulatory disruption into decision-grade commercial risk outputs.

It supports client-type outputs such as:
- shipping_operator
- trade_finance_lender
- insurer / marine_insurer
- investor / analyst where relevant

It should not become a single-case report generator.

## Core workflow
Preserve this workflow:
1. define client decision
2. create source plan
3. retrieve or load sources
4. rank sources
5. extract evidence and quantified signals
6. assess evidence sufficiency
7. convert evidence into scores
8. generate decision brief / dashboard artefact
9. produce source audit and evidence pack
10. run quality checks

## Output standard
Every serious output should answer:
- What decision does the client-type user need to make?
- What evidence is required?
- Which sources were selected and rejected?
- Why are those sources credible?
- What quantified signals matter?
- How does evidence affect likelihood, impact, immediacy and confidence?
- What should the client-type user do?
- What would change the recommendation?
- What requires private/company/transaction data?

## Client-type, not unsupported company-specific
Outputs should be client-type decision briefs unless company data is explicitly provided.
Do not claim company-specific precision without company-specific data.
Label assumptions clearly.
Separate:
- public/live evidence
- curated fallback evidence
- manual/user-provided inputs
- illustrative assumptions
- derived calculations

## Source gathering principles
The source planner should seek a balanced source role mix where relevant:
- official_anchor
- specialist_interpretation
- operator_or_industry_guidance
- market_pricing
- live_event_reporting
- contrary_scope_limit
- data_or_indicator_source

Official sources anchor rules and facts.
Specialist sources explain practical implications.
Market/operator sources help quantify commercial impact.
Contrary/scope-limiting sources prevent overstatement.

## Evidence quality rules
Evidence rows should include:
- source role
- source value explanation
- requirement mapping
- claim
- quantified signal where available
- commercial meaning
- decision use
- caveat
- refresh trigger

Avoid generic decision-use wording such as:
“Supports operator review and control decisions.”

## Scoring rules
Scores must be domain-specific.
Do not use generic geopolitical score rationales where specific regulatory, sanctions, maritime, operational or financial logic is needed.
Confidence must be capped where:
- evidence is fallback/curated
- calculation inputs are illustrative
- live market/pricing data is missing
- source categories are missing
- claims require company/transaction data
- contradictory evidence exists

## Dashboard rules
Dashboards should display saved showcase artefacts by default.
Dashboards should not call Tavily or spend credits unless explicitly requested.
Dashboards should show:
- decision stance
- quantified outputs
- evidence-to-score bridge
- source requirement coverage
- source audit summary
- assumptions and data limits

## Security rules
Never expose API keys.
.env must remain ignored.
Use .env.example only for placeholders.
Generated docs, showcase files and outputs must not contain key-shaped strings.
Do not print API keys in logs or verification scripts.

## Change discipline
Avoid broad framework expansion unless explicitly requested.
Prefer targeted improvements to:
- output quality
- source quality
- dashboard clarity
- evidence scoring
- source audit clarity

Before editing, summarise:
1. task objective
2. files to inspect
3. files likely to change
4. verification commands

## Verification
Run where relevant:
python3 -m unittest discover tests
python3 scripts/quality_check.py

If a task touches the dashboard, also ensure:
streamlit run dashboard_app.py
works locally, or explain why it was not run.
