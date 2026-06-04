# Task Brief: [Case Name]

## Objective

State what the case should prove and what saved showcase output should be created.

## Client Type

Define the client-type user. Do not claim company-specific precision unless company data is provided.

## Practical Users

List the real users of the output, such as CFO, COO, risk manager, procurement lead, compliance officer, underwriter or operations lead.

## Political Risk Trigger

Describe the political, geopolitical, regulatory or state-linked driver. Keep this specific enough to explain why the case belongs in a political risk workflow.

## Business Decision

State the business question the output must answer.

## Decision Options

List the practical options available to the user.

Examples:

- approve / escalate / legal hold / reject
- transit / delay / reroute / legal hold
- stockpile / qualify supplier / redesign / allocate / production hold
- continue operations / activate incident response / notify / claim / manual fallback

## In Scope

Define the evidence, model and output boundaries.

## Out Of Scope

List what the case must not become, such as generic event reporting, technical advice, legal advice, insurance coverage determination or unsupported company-specific assessment.

## Source Requirements

For each requirement, use this structure:

| Field | Description |
|---|---|
| requirement_id | Stable identifier for the evidence requirement |
| question it answers | The decision question this requirement supports |
| preferred source role | Official, regulatory, specialist, live reporting, data, market, contrary or company-required |
| preferred source targets | Named publishers, agencies, regulators, data sources or credible specialists |
| decision use | How this evidence affects the business decision |
| caveat / gap risk | What can go wrong if this requirement is weak or missing |

Repeat for each source requirement.

## Source Roles Needed

List the intended source role mix. Use only roles relevant to the case.

- `official_anchor`
- `regulatory_guidance`
- `specialist_interpretation`
- `live_event_reporting`
- `data_or_indicator_source`
- `operator_or_industry_guidance`
- `market_pricing`
- `insurance_market_evidence`
- `contrary_scope_limit`
- `company_required_data`

## Evidence-To-Score Logic

Define case-specific scoring logic.

### Likelihood

Explain what evidence should increase or reduce likelihood.

### Impact

Explain how business severity should be assessed.

### Immediacy

Explain what creates timing pressure.

### Confidence

Explain what source coverage, contradiction or missing company data should cap confidence.

## Quantitative / Decision Model

Describe the model, formula or rule logic.

Include:

- inputs
- outputs
- decision thresholds
- labels for illustrative and company-required values

## Assumption Provenance

Material inputs must be labelled:

- `source-supported`
- `illustrative`
- `manual/user-provided`
- `derived`
- `company-required`

## Company Data Required

List the private data needed before operational use.

Examples:

- contracts
- routes
- fuel burn
- bills of materials
- supplier country or ownership
- transaction documents
- sanctions screening results
- insurance policy wording
- system maps
- inventory and customer commitments

## Anti-Overclaiming Controls

State what the output must not claim.

Include wording such as:

`This is a client-type exposure screen, not a company-specific operational assessment, legal advice, insurance coverage determination or transaction clearance decision.`

Tailor the wording to the case.

## Dashboard Concept

Describe how the case should later appear in the dashboard:

- top metrics
- tabs
- key model output
- source quality notes
- company-data caveats

## Output Files

List intended saved files.

Examples:

- `showcase/[case]_brief.md`
- `showcase/[case]_source_audit.md`
- `showcase/[case]_evidence_pack.json`

## Files Likely To Change

List likely modules, scripts, tests and docs.

## Do Not Change

List protected files, cases, dashboard behavior or retrieval logic.

## Verification Commands

```bash
python3 scripts/check_dashboard_files.py
python3 -m unittest discover tests
python3 scripts/quality_check.py
```

Add any case-specific verification commands.

## Acceptance Criteria

Define completion in observable terms:

- task brief complete
- source requirements defined
- evidence mode accurate
- output sections present
- assumptions labelled
- anti-overclaiming controls visible
- tests and quality check pass
