# Framework Principles

## Decision-first design
The framework should begin with the client-type decision, not with a generic country or event summary. Every output should make clear:
- what choice is being made
- what could block the choice
- what evidence would support or reverse the recommendation

The brief, dashboard, evidence pack and source audit should all reinforce that same decision path.

## Source role mix
Source planning should aim for a balanced mix of roles where relevant:
- official anchors for rules, policy, sanctions, safety or regulatory baselines
- specialist interpretation for practical implications
- operator or industry guidance for workflow and market behavior
- market pricing for exposure and cost effects
- live event reporting for current operating conditions
- contrary or scope-limiting evidence to prevent overstatement
- data or indicator sources for quantified exposure signals

Not every case needs every source role, but the mix should be deliberate and explainable.

## Source requirement coverage
Each case should map evidence back to named source requirements and decision questions.

Coverage should show:
- what was required
- which sources covered it
- strongest available source
- remaining gap or refresh need

Coverage must not overstate certainty when source roles or source requirements are missing.

## Qualitative-to-quantitative scoring
Likelihood, impact, immediacy and confidence should be traceable to evidence rather than generic intuition.

The framework should:
- convert claims into business-relevant facts
- expose the evidence-to-score bridge
- use domain-specific rationale
- distinguish between strong anchors and illustrative calculations

Quantified evidence should be labelled, readable and tied to decision use.

## Evidence sufficiency
The system should make it visible when the evidence base is insufficient for a high-confidence recommendation.

Evidence sufficiency should consider:
- source diversity
- source quality
- freshness
- requirement coverage
- whether company, operator or transaction data is still missing
- whether contradictory or stabilising evidence narrows the claim

## Client-type outputs
Outputs should be designed for client-types, not fictional precision about a specific company.

Examples:
- shipping_operator
- trade_finance_lender
- insurer / marine_insurer
- investor / analyst where relevant

If a task requires company-specific conclusions, the necessary company data should be requested or the output should remain explicitly illustrative.

## Company-data limits
Do not claim company-specific economics, compliance status or risk appetite unless company-specific data is available.

Always separate:
- public or live evidence
- curated fallback evidence
- manual user-provided inputs
- illustrative assumptions
- derived calculations

Derived outputs should inherit the caveats of the weakest required input.

## Dashboard and showcase principles
Dashboards should default to saved showcase artefacts unless live retrieval is explicitly requested.

Dashboards should surface:
- decision stance
- quantified outputs
- evidence-to-score bridge
- source requirement coverage
- source audit summary
- assumptions and limits

Showcases should demonstrate reusable workflow quality, not become brittle one-off demos.

## Anti-overclaiming rules
Avoid overstating what the evidence proves.

Use scope-limiting language when:
- evidence is partial
- live market or operational conditions are moving quickly
- company-specific data is absent
- contradictory evidence exists
- a calculation depends on illustrative assumptions

Cheaper or more convenient operational options should not override legal, sanctions or policy hold triggers.

## Live vs curated evidence modes
The framework supports both live retrieval and curated fallback evidence.

Live mode should make current-source provenance visible.
Curated mode should be clearly labelled as reproducible fallback evidence.

Confidence should be capped when:
- the run uses curated fallback evidence
- live market data is missing
- key inputs are illustrative
- important source categories are absent

The mode must be obvious in briefs, audits, dashboards and evidence packs.
