# Political Risk Agent

Political Risk Agent is a reusable, source-governed workflow that turns public political, geopolitical, regulatory and state-linked evidence into commercial decision-support outputs.

It is not a single report generator. The project shows how a repeatable workflow can define a business decision, plan source requirements, retrieve and rank public evidence, extract decision-relevant claims, label assumptions, score risk, expose confidence limits and present the result in an offline dashboard.

This is a reusable, governed political risk decision-support prototype. It is designed to structure public evidence, source provenance, analyst scoring and commercial decision outputs. It is not a fully autonomous risk oracle and requires human review before operational use.

## Summary

### What is this?

A political-risk-to-business-decision framework. Each case starts with a client-type decision, identifies the political risk trigger, maps that trigger to business exposure, then produces a brief, source audit, evidence pack and dashboard view.

### What problem does it solve?

Political risk analysis often stays descriptive: what happened, where it happened and why it matters. This project pushes the analysis into decision support by asking:

- what decision the business user needs to make
- what evidence is required
- which sources are credible enough to use
- what the quantified or concrete signals are
- how the evidence affects likelihood, impact, immediacy and confidence
- what assumptions are illustrative or company-required
- what would change the recommendation

### What it demonstrates

- decision-first product thinking for commercial risk users
- source planning and requirement coverage
- source ranking, source roles and selected/rejected source audit trails
- evidence extraction and claim cleanup
- evidence-to-score bridges for likelihood, impact, immediacy and confidence
- quantified scenario models where useful
- confidence caps, caveats, refresh triggers and company-data requirements
- an offline Streamlit dashboard that reads saved showcase artefacts only
- clean export hygiene and no API key exposure in public/shareable files

## Current Case Portfolio

The active dashboard cases are saved Tavily-backed showcase outputs. Their evidence packs are marked `search_provider/source_provider: tavily`, `evidence_mode: Live source retrieval`, and `fallback_used/fallback_demo_data_used: false`.

| Case | Client type | Risk pattern | Decision output | Evidence mode |
|---|---|---|---|---|
| UK ETS Maritime Expansion | UK shipping operator | regulatory policy / carbon cost | route-level carbon cost exposure | saved Tavily-backed showcase |
| Hormuz Route Decision Engine | shipping operator | geopolitical/security/sanctions/insurance | transit, delay, reroute or legal hold | saved Tavily-backed showcase |
| Critical Minerals Exposure Engine | UK advanced manufacturer | strategic competition / supply-chain concentration | stockpile, qualify supplier, redesign, allocate or hold | saved Tavily-backed showcase |
| Sanctions Trade Finance Exposure Engine | UK trade finance lender / bank / credit insurer | sanctions / export controls | transaction approval, escalation, legal hold or rejection | saved Tavily-backed showcase |
| Cyber Business Interruption Engine | UK customer-facing operator / retailer / critical services operator | geopolitical cyber / ransomware / operational resilience | downtime, notification, insurance and recovery decision | saved Tavily-backed showcase |

The portfolio is expandable. Future cases can follow the same saved-showcase pattern after a task brief, source run, offline polish pass, tests and dashboard integration.

### Saved Portfolio Case Outside The Dashboard

| Case | Client type | Risk pattern | Decision output | Evidence mode |
|---|---|---|---|---|
| UK Fiscal Instability And Procurement Delay Risk | UK infrastructure contractor bidding for government-funded transport and energy projects | political economy / fiscal credibility / public procurement | bid pipeline review, delay contingency, repricing checks, payment-risk monitoring and board exposure reporting | saved Tavily-backed portfolio case |

This case is a proper saved portfolio case and is useful for reviewing the fresh-topic workflow because it was generated through `main.py run-topic`, refreshed with a targeted Tavily run, then polished offline to improve source quality, graded requirement coverage, provenance, evidence separation and scoring traceability. It is not yet an active dashboard tab.

## How The Workflow Works

1. Define the business decision.
2. Build source requirements.
3. Generate targeted search queries.
4. Retrieve live public sources through Tavily for showcase generation.
5. Rank sources by role, relevance, reliability, specificity, recency and decision value.
6. Extract decision-relevant claims, signals, caveats and refresh triggers.
7. Map evidence back to source requirements.
8. Convert evidence into likelihood, impact, immediacy and confidence scores.
9. Label assumptions as source-supported, illustrative, manual, derived or company-required.
10. Generate a brief, source audit, evidence pack and offline dashboard view.
11. Run tests, quality checks and clean export hygiene.

## How Sources Are Judged

The framework uses source roles so the output does not treat every source as equally authoritative.

- `official_anchor`: anchors rules, policy, sanctions lists, official warnings or regulatory baselines.
- `regulatory_guidance`: explains supervisory, reporting, notification or compliance expectations.
- `specialist_interpretation`: explains practical implications, legal/compliance interpretation or sector context.
- `live_event_reporting`: captures current developments, incidents or operating conditions.
- `data_or_indicator_source`: provides quantified indicators, exposure data or observable signals.
- `market_pricing`, `insurance_market_evidence` or `operator_or_industry_guidance`: helps quantify commercial impact where relevant.
- `contrary_scope_limit`: prevents overstatement by showing easing, limits, exceptions or weaker evidence areas.
- `company_required_data`: marks what public evidence cannot resolve without private company, transaction or operational data.

Official sources anchor facts and rules. Specialist sources explain what those facts mean in practice. Market, insurance and industry sources help quantify exposure. Contrary and scope-limiting sources keep the recommendation honest. Company-required data marks the boundary between a client-type screen and an operational decision.

## How Evidence Becomes A Score

The scorecard is a structured decision-support rubric, not a predictive or statistically validated model.

- `likelihood`: how strongly the evidence suggests the risk condition is present or developing.
- `impact`: commercial severity if the risk affects the client-type user.
- `immediacy`: timing pressure or urgency of the decision.
- `confidence`: source quality, coverage, freshness, contradiction and missing company data.

Each serious output should include an evidence-to-score bridge explaining why the scores were assigned and what would cap or change them.

Generated evidence packs also include traceable scoring fields showing evidence supporting the score, evidence weakening the score, missing evidence, cap reasons, confidence and review requirements.

Current traceable score objects separate:

- `supporting_evidence`: evidence that supports the score
- `contrary_evidence`: evidence that pushes against the risk judgement or supports relaxation
- `evidence_quality_limits`: snippet-only, indirect, low-confidence or review-required evidence
- `missing_evidence`: evidence needed for operational use or a stronger score

This distinction prevents weak source quality from being mislabeled as contrary evidence.

## How Caveats Are Handled

The framework makes uncertainty visible through:

- confidence caps
- graded source requirement coverage
- source quality notes
- source requirement coverage
- selected and rejected source lists
- refresh triggers
- company-data requirements
- assumption labels for source-supported, illustrative, manual, derived and company-required inputs

Illustrative scenario values are not presented as company-specific facts. Company-specific use requires internal data such as contracts, routes, counterparties, bills of materials, supplier records, policy wording, inventory or operational plans depending on the case.

Requirement coverage is graded rather than binary. Coverage grades include `strong_direct_full_text`, `direct_snippet_only`, `partial_or_indirect`, `historical_context_only` and `missing`. Snippet-only or indirect evidence triggers human-review controls and should cap confidence until verified.

## Dashboard

Run:

```bash
streamlit run dashboard_app.py
```

The dashboard reads saved showcase artefacts only:

- saved brief markdown
- saved source audit markdown
- saved evidence pack JSON

It does not call Tavily, run `live_search_mode`, require `.env`, or spend live-search credits when viewed. Source refresh happens deliberately through generation scripts or targeted source-refresh tasks, not through dashboard viewing.

Each case starts with the business decision, then shows the model output, evidence base, source caveats and company-data needed for operational use.

## Active Showcase Files

Saved showcase artefacts live in `showcase/`.

Showcase case artefacts follow the same three-file pattern: brief, source audit and evidence pack.

- UK ETS: `showcase/uk_ets_shipping_operator_brief.md`, `showcase/uk_ets_source_audit.md`, `showcase/uk_ets_evidence_pack.json`
- Hormuz: `showcase/hormuz_shipping_operator_brief.md`, `showcase/hormuz_source_audit.md`, `showcase/hormuz_evidence_pack.json`
- Critical Minerals: `showcase/critical_minerals_advanced_manufacturer_brief.md`, `showcase/critical_minerals_source_audit.md`, `showcase/critical_minerals_evidence_pack.json`
- Sanctions Trade Finance: `showcase/sanctions_trade_finance_exposure_brief.md`, `showcase/sanctions_source_audit.md`, `showcase/sanctions_evidence_pack.json`
- Cyber Business Interruption: `showcase/cyber_business_interruption_brief.md`, `showcase/cyber_source_audit.md`, `showcase/cyber_evidence_pack.json`
- UK Fiscal Instability And Procurement Delay Risk: `showcase/uk_fiscal_instability_procurement_brief.md`, `showcase/uk_fiscal_instability_procurement_source_audit.md`, `showcase/uk_fiscal_instability_procurement_evidence_pack.json` 

`showcase/sanctions_trade_finance_sample.md` is a legacy curated sample retained for reference. It is not the active sanctions dashboard case.

## New Case Workflow

1. Create a task brief using `docs/TASK_BRIEF_TEMPLATE.md`.
2. Define the client type and business decision.
3. Define the political-risk trigger and source requirements.
4. Run a targeted live source generation pass when evidence is needed.
5. Polish the saved output offline.
6. Add or update tests and quality checks.
7. Add dashboard integration only after the saved case meets the source, scoring and caveat standard.

New cases should follow the pattern: task brief, critique, live source run, offline polish, dashboard integration.

For an offline fresh-topic structure run using analyst notes:

```bash
python3 main.py run-topic \
  --topic "Example political risk issue" \
  --business-user trade_finance_lender \
  --decision-context "Approve, escalate or hold a transaction" \
  --region UK \
  --time-horizon "1-3 months" \
  --concerns "sanctions exposure, documentation quality" \
  --source-notes-file path/to/source-notes.txt \
  --output-dir outputs
```

Add `--live` only when deliberately running a live source generation pass.

## How Reviewers Should Evaluate This Project

Start in plain English:

- Does each case begin with a clear business decision?
- Are political-risk triggers explicit?
- Are selected sources visible with URLs?
- Are source roles and caveats shown?
- Is the evidence-to-score bridge clear?
- Are assumptions labelled?
- Are company-data requirements visible?
- Does the dashboard avoid live-search spending when viewed?
- Do tests and quality checks pass?

Then inspect the implementation:

- source planning: `agent/source_planner.py` and `agent/source_requirements.py`
- ranking and source roles: `agent/source_ranker.py`
- evidence extraction: `agent/live_evidence_extraction.py`
- scores and models: relevant `agent/*model.py`, `agent/risk_scoring.py`, `agent/confidence_model.py` and `agent/quantitative_assessment.py`
- saved outputs: `showcase/`
- dashboard: `dashboard_app.py` and `dashboard_helpers.py`
- quality and export checks: `scripts/quality_check.py`, `scripts/check_dashboard_files.py` and `scripts/create_clean_project_zip.py`

To evaluate the newer fresh-topic workflow, inspect the UK Fiscal Instability And Procurement Delay Risk files in `showcase/`. A reviewer should check the evidence pack JSON for `source_claim`, `extracted_evidence`, `analyst_inference`, provenance fields, snippet-only review flags and `traceable_scores`; then compare the source audit and brief to see whether the scoring, caveats and company-data limits remain readable.

For this fiscal case, also check requirement coverage grades in the source audit. A good review should ask how many requirements are strongly covered by direct full text, how many are snippet-only, and which gaps affect confidence.

The fiscal case can be regenerated deliberately with:

```bash
python3 main.py run-topic \
  --topic "UK fiscal instability and public-sector procurement delay risk" \
  --business-user "UK infrastructure contractor" \
  --decision-context "Assess whether fiscal pressure, gilt-market sensitivity, political instability and departmental budget uncertainty should trigger bid pipeline review, payment-risk monitoring, contract repricing, project-delay contingency planning and board-level exposure reporting" \
  --domain uk_fiscal_procurement_risk \
  --output-dir outputs/showcase/uk_fiscal_instability_procurement_risk \
  --live
```

Only run this command when a live source refresh is intentional and a valid API key is available.

## Architecture

### Reusable political risk engine

- intake
- source strategy
- source planning
- live source retrieval for generation tasks
- source ranking
- source fetching
- evidence extraction
- risk-driver synthesis
- exposure mapping
- risk scoring
- confidence assessment
- source audit
- brief generation
- review controls

### Domain-specific layer

- source requirements
- source roles
- risk drivers
- business-user exposure maps
- recommended actions
- watchlist indicators
- case-specific decision or quantitative models
- report templates

## Live Retrieval And Historical Fallback Handling

The active showcase cases are saved Tavily-backed outputs. Fallback/demo evidence is not used in the active dashboard cases and should not be treated as part of the current public showcase evidence base.

Some code and tests still contain fallback/demo handling as a defensive or historical concept for reproducibility and failure handling. If fallback/demo evidence is ever used in a non-active run, it must be labelled clearly and confidence should be capped. It should not be presented as the standard for active public showcase cases.

For deliberate live generation, `live_search_mode` uses `TAVILY_API_KEY` first, then `SERPAPI_API_KEY` if configured. Live generation writes generated files to `outputs/`, which are ignored by Git except for `outputs/.gitkeep`.

## How To Run Generation Manually

From the project directory:

```bash
python3 main.py
```

Choose:

- `manual_source_mode` to paste analyst notes
- `live_search_mode` to run source strategy, search, ranking, extraction, audit and brief generation

For Tavily live generation, create a local `.env` file:

```text
TAVILY_API_KEY=your_key_here
```

Do not commit `.env`.

## Output Files Generated

In `live_search_mode`, each run saves three files to `outputs/`:

- `*-evidence-pack.json`: structured evidence, source plan, selected/rejected sources, coverage, quantified readout and fetch metadata
- `*-source-audit.md`: research plan, source strategy, ranking rationale, rejected sources, quantified summary and review controls
- `*.md`: commercial risk brief

## Why The Source Audit Matters

The source audit is the analyst trail. It shows what the agent searched for, why each requirement matters, which sources were selected, which were rejected, what evidence categories are covered or missing, and what still requires human review.

## Limitations

- This is not legal, insurance, cybersecurity, sanctions, operational or investment advice.
- Company-specific use requires internal data and human review.
- Live retrieval quality depends on available sources, page accessibility and search-provider results.
- Scores are transparent, rule-based decision support rather than predictive truth.
- Market pricing, sanctions, regulatory and operating-condition signals can change quickly.
- The dashboard is intentionally offline and displays saved artefacts rather than live retrieval.

## Run Tests

```bash
python3 scripts/check_dashboard_files.py
python3 -m unittest discover tests
python3 scripts/quality_check.py
```

## Clean Export

Create a shareable project zip without local secrets, virtual environments, git metadata, generated `outputs/` files, `dist/` artefacts or local caches:

```bash
python3 scripts/create_clean_project_zip.py
```

The export is written to `dist/political-risk-agent-clean.zip`.

## Agent / Codex instructions

For durable project guidance, see:

- `AGENTS.md`
- `docs/FRAMEWORK_PRINCIPLES.md`
- `docs/TASK_BRIEF_TEMPLATE.md`

## Future Roadmap

- Add non-interactive CLI arguments for repeatable runs.
- Add configurable scoring weights by domain pack.
- Add stronger source freshness checks by category.
- Add richer domain packs for additional business users.
