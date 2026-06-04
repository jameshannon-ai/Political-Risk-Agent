# Framework Principles

Political Risk Agent is a repeatable workflow for turning political-risk evidence into business decisions. It should not drift into generic event summaries or unsupported company-specific claims.

## Repeatable Case Lifecycle

Each serious case should move through the same lifecycle:

1. Task brief
2. Critique before implementation
3. Targeted live source run when evidence is needed
4. Saved brief, source audit and evidence pack
5. Offline source-quality and output-polish pass
6. Tests and quality checks
7. Dashboard integration only after the saved case meets the standard

The active dashboard cases currently use saved Tavily-backed evidence. They are not fallback/demo cases.

## Political-Risk Trigger To Business Decision

Every case should start with:

- the client type
- the practical user
- the political, geopolitical, regulatory or state-linked trigger
- the business decision that trigger affects
- the decision options available to the user

The output should explain how the trigger becomes commercial exposure. For example, a regulatory rule can become a cost input, sanctions can become a legal-hold trigger, and supplier concentration can become a production-continuity gap.

## Decision-First Design

The framework should begin with the client-type decision, not with a broad country or event summary.

Every output should make clear:

- what choice is being made
- what could block the choice
- what evidence would support or reverse the recommendation
- what data is still required for operational use

The brief, dashboard, evidence pack and source audit should all reinforce the same decision path.

## Source Requirement Design

Source requirements should be written as decision questions, not as generic research topics.

Each requirement should specify:

- what question it answers
- preferred source role
- preferred source targets
- decision use
- caveat or gap risk

Source requirement coverage should show what was required, which sources covered it, the strongest available source and the remaining gap or refresh need.

## Source Ranking And Role Discipline

Source planning should aim for a deliberate role mix where relevant:

- `official_anchor` for rules, policy, sanctions, safety or regulatory baselines
- `regulatory_guidance` for supervisory, reporting, notification or compliance expectations
- `specialist_interpretation` for practical implications
- `operator_or_industry_guidance` for workflow and market behavior
- `market_pricing` or `insurance_market_evidence` for exposure and cost effects
- `live_event_reporting` for current operating conditions
- `data_or_indicator_source` for quantified exposure signals
- `contrary_scope_limit` for easing evidence, exclusions or scope limits
- `company_required_data` for facts public evidence cannot provide

Do not overstate source authority. Law firm commentary is not official guidance. News reporting is not regulatory guidance. Company or broker publications can be useful, but they should be labelled as market, specialist or industry evidence rather than official evidence.

## Evidence Extraction And Claim Cleanup

Evidence rows should be readable and decision-useful.

Rows should include:

- source role
- source value explanation
- requirement mapping
- claim
- quantified or concrete signal where available
- commercial meaning
- decision use
- caveat
- refresh trigger

Avoid boilerplate, cookie text, navigation fragments, raw HTML and generic decision-use wording. If extraction is weak, use snippet or metadata-supported wording and label that limitation.

## Evidence-To-Score Bridge

Likelihood, impact, immediacy and confidence should be traceable to evidence.

- `likelihood`: how strongly evidence suggests the risk condition is present or developing
- `impact`: commercial severity if the risk affects the client-type user
- `immediacy`: timing pressure or urgency
- `confidence`: source quality, coverage, freshness, contradiction and missing company data

Scores are transparent rule-based decision support. They are not statistical forecasts or legal, insurance, cyber, sanctions or investment determinations.

## Confidence Caps And Evidence Sufficiency

Confidence should be capped when:

- source requirements are partially covered
- live market or pricing data is missing
- inputs are illustrative
- important source roles are absent
- evidence is contradictory
- claims require company, transaction or operational data
- fallback/demo evidence is used in a non-active run

The active dashboard cases should show `fallback_used` and `fallback_demo_data_used` as false.

## Assumption Provenance

Every material input should be labelled:

- `source-supported`
- `illustrative`
- `manual/user-provided`
- `derived`
- `company-required`

Derived outputs inherit the caveats of the weakest required input. Scenario calculations should never be presented as company-specific precision unless company-specific data was actually provided.

## Company-Data Boundary

Outputs are client-type decision products unless company data is explicitly supplied.

Do not claim company-specific economics, compliance status, insurance coverage, operational resilience or risk appetite without company-specific data.

Company-required data should be visible in the brief and dashboard. Examples include contracts, routes, fuel burn, bills of materials, supplier ownership, transaction documents, cyber insurance wording, system maps, inventory and customer commitments.

## Dashboard As Saved-Showcase Presentation Layer

The dashboard is an offline presentation layer for saved showcase artefacts. It should read:

- saved brief markdown
- saved source audit markdown
- saved evidence pack JSON

It should not call Tavily, run `live_search_mode`, read `.env` or spend search credits when viewed.

Dashboards should surface:

- decision stance
- quantified outputs
- evidence-to-score bridge
- source requirement coverage
- selected sources with URLs
- source quality notes
- source audit summary
- assumptions and limits

## Source Freshness And Targeted Refresh

Refresh live sources deliberately. Do not broad-rerun Tavily when a wording caveat or dashboard display change is enough.

Use targeted refresh when a core source requirement is weak enough to damage credibility, such as missing official guidance, missing live event reporting, missing pricing/market evidence or missing contrary/scope-limiting evidence.

Document why refresh was needed and preserve the source audit trail.

## Live Evidence And Historical Fallback Handling

The active showcase cases are saved Tavily-backed outputs. Fallback/demo evidence is not part of the current active dashboard evidence base.

Fallback/demo handling may remain in code or tests as a defensive or historical concept. If used in any non-active run, it must be labelled clearly and confidence should be capped. It should not be described as normal for active public cases.

## Public Sharing And No-Secrets Hygiene

Never expose API keys. `.env` must remain ignored. `.env.example` should contain placeholders only.

Generated docs, showcase files and outputs must not contain key-shaped strings. Clean exports should exclude:

- `.env`
- `.git/`
- `.venv/`, `venv/`, `env/`
- caches and `__pycache__/`
- old zip files
- generated `outputs/` files except `outputs/.gitkeep`
- `dist/` artefacts

Public docs should explain limitations clearly and should not imply the dashboard spends live-search credits when viewed.
