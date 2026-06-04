# Political Risk Agent

Political Risk Agent is a reusable, source-audited intelligence workflow for converting political, geopolitical and regulatory disruption into decision-grade commercial risk briefs. It uses governed source planning, source ranking, evidence extraction, qualitative-to-quantitative scoring, risk-driver synthesis and review controls.

## Employer Quick Read

Political Risk Agent is a portfolio project showing how public political, geopolitical and regulatory evidence can be converted into decision-useful commercial risk outputs. It is not a single report: it is a reusable workflow for defining a client decision, planning sources, ranking evidence, extracting claims, scoring risk and producing a brief, source audit, evidence pack and offline dashboard view.

What it demonstrates:

- decision-first product thinking for commercial risk users
- source planning and source requirement coverage
- source ranking, selected/rejected source audit trail and evidence extraction
- evidence-to-score bridges for likelihood, impact, immediacy and confidence
- quantified scenario modelling where useful, with assumptions labelled
- confidence caps, caveats and company-data requirements
- an offline Streamlit dashboard that reads saved showcase artefacts only
- clean export hygiene and no API key exposure in public/shareable files

### Current Case Portfolio

| Case | Client type | Risk pattern | Decision output | Evidence mode |
|---|---|---|---|---|
| UK ETS Maritime Expansion | UK shipping operator | regulatory policy / carbon cost | route-level carbon cost exposure | saved Tavily-backed showcase |
| Hormuz Route Decision Engine | shipping operator | geopolitical/security/sanctions/insurance | transit, delay, reroute or legal hold | saved Tavily-backed showcase |
| Critical Minerals Exposure Engine | UK advanced manufacturer | strategic competition / supply-chain concentration | stockpile, qualify supplier, redesign, allocate or hold | saved Tavily-backed showcase |
| Sanctions Trade Finance Exposure Engine | UK trade finance lender / bank / credit insurer | sanctions / export controls | transaction approval, escalation, legal hold or rejection | saved Tavily-backed showcase |
| Cyber Business Interruption Engine | UK customer-facing operator / retailer / critical services operator | geopolitical cyber / ransomware / operational resilience | downtime, notification, insurance and recovery decision | saved Tavily-backed showcase |

The dashboard is designed as an expandable case portfolio. New cases can be added by saving a brief, source audit and evidence pack, then wiring that saved-showcase pattern into the dashboard.

Run the dashboard:

```bash
streamlit run dashboard_app.py
```

The dashboard displays saved showcase artefacts only. It does not call Tavily or spend live-search credits.

Evidence and governance features:

- source plans and source requirements define what evidence is needed
- selected and rejected sources are retained in the source audit
- evidence rows include claims, quantified signals, decision use, caveats and refresh triggers
- scorecards explain the evidence basis for likelihood, impact, immediacy and confidence
- briefs separate public evidence, illustrative assumptions, derived calculations and company-required data

Limitations:

- this is not legal, insurance or investment advice
- company-specific use requires internal data such as contracts, inventory, routes, counterparties, BOMs and supplier records
- live source quality depends on available sources, page accessibility and search-provider results
- scores are transparent, rule-based decision support rather than predictive truth
- the dashboard is intentionally offline and displays saved artefacts rather than live retrieval

## How To Evaluate This Project

Reviewers should look at:

- `agent/source_planner.py` and `agent/source_requirements.py` for source planning and requirement logic
- `agent/source_ranker.py` for source ranking and source-role handling
- `agent/live_evidence_extraction.py` for evidence extraction and claim cleanup
- showcase briefs for evidence-to-score bridges, confidence caps and caveats
- showcase source audits for selected/rejected source reasoning and refresh priorities
- `dashboard_app.py` for offline saved-showcase dashboard presentation
- `scripts/create_clean_project_zip.py` and `scripts/quality_check.py` for clean export and no-key/public-sharing checks

## Product Value

- Converts complex political risk evidence into structured commercial decisions.
- Links source evidence to business exposure, risk scoring and recommended actions.
- Keeps source quality, confidence and review controls visible.
- Supports repeatable briefing across sectors, geographies and business users.

## Architecture

### Reusable political risk engine

- intake
- source strategy
- live search / curated evidence mode
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

- source categories
- risk drivers
- business-user exposure maps
- recommended actions
- watchlist indicators
- report templates

### Current saved-showcase portfolio

- UK ETS Maritime Expansion: Carbon Cost Exposure
- Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs
- Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers
- Sanctions Trade Finance Exposure Engine: Transaction Approval, Escalation and Legal-Hold Risk
- Cyber Business Interruption Engine: Operational Resilience and Insurance Exposure for UK Retail / Critical Services

These are current saved dashboard cases, not the final limits of the framework. Additional saved samples can remain available in `showcase/`, but they should be clearly labelled unless upgraded into the active dashboard portfolio.

Showcase case artefacts are saved briefs, source audits and evidence packs that can be reviewed without running live retrieval.

## Who It Is For

- `shipping_operator`
- `marine_insurer`
- `importer_exporter`
- `trade_finance_lender`
- `consultant`

## Live vs Fallback Evidence Status

`live_search_mode` uses `TAVILY_API_KEY` first, then `SERPAPI_API_KEY`.

If neither key is set, the app uses the curated local Hormuz source pack at:

```text
examples/hormuz_real_evidence_case.json
```

The brief and source audit clearly state whether evidence came from live retrieval or the curated fallback pack.

## Output Files Generated

In `live_search_mode`, each run saves three files to `outputs/`:

- `*-evidence-pack.json`: structured evidence, source plan, selected/rejected sources, coverage, quantified readout and fetch metadata
- `*-source-audit.md`: research plan, source strategy, ranking rationale, rejected sources, quantified summary and review controls
- `*.md`: commercial risk brief

## Why The Source Audit Matters

The source audit is the analyst trail. It shows what the agent searched for, why each category matters, which sources were selected, which were rejected, what evidence categories are covered or missing, and what still requires human review.

## How To Run

From the project directory:

```bash
python3 main.py
```

Choose:

- `manual_source_mode` to paste analyst notes
- `live_search_mode` to run source strategy, search, ranking, extraction, audit and brief generation

## Run With Tavily

Create a local `.env` file:

```text
TAVILY_API_KEY=your_key_here
```

Then run:

```bash
python3 main.py
```

Choose `live_search_mode`. If Tavily is not configured, the app will try `SERPAPI_API_KEY`; if neither is configured, it will use the curated fallback pack.

## Example Live-Run Input

```text
Topic: Hormuz Route Decision Engine: Sanctions, Insurance and Delay-Cost Trade-Offs
Business user: shipping_operator
Region: Persian Gulf / UK shipping operators
Time horizon: 1-3 months
Concerns: transit controls, vessel detention, safe-passage demands, sanctions exposure, war-risk insurance premiums, AIS/transponder disruption, route delay, rerouting cost, charterparty exposure, crew safety, de-escalation uncertainty
```

## How To Interpret The Saved Showcase Briefs

The active dashboard briefs are structured as decision products:

- client decision stance first
- key judgements linked to evidence
- risk scorecards with evidence-specific rationale
- quantified readouts or scenario models where useful
- evidence-to-score bridges
- source requirement coverage
- selected sources, caveats, refresh triggers and source audits

UK ETS converts regulatory policy into route-level carbon cost exposure. Hormuz converts geopolitical, sanctions, insurance and vessel-flow signals into transit, delay, reroute or legal-hold logic. Critical Minerals converts export-control and supplier concentration evidence into production-continuity decisions. Sanctions Trade Finance converts sanctions/export-control evidence into transaction approval, escalation, legal-hold or rejection logic. Cyber Business Interruption converts geopolitical cyber/ransomware and resilience evidence into downtime, notification, insurance and recovery decisions.

Generic political risk outputs still use a shorter reusable template so the project does not become a single-case report generator.

## Domain Packs

Reusable domain pack examples are stored in:

```text
config/domain_packs.json
```

Future reusable case examples are documented in:

```text
docs/reusable_cases.md
```

## Limitations And Review Controls

- Scoring and extraction are rule-based and transparent.
- Live retrieval quality depends on search provider results and page accessibility.
- PDF extraction requires `pypdf`; otherwise PDF sources are marked metadata-only.
- Market pricing, sanctions and de-escalation signals can change quickly.
- Any underwriting, legal, sanctions or operational decision requires human review.

## Run Tests

```bash
python3 -m unittest discover tests
```

## Dashboard

Run:

```bash
streamlit run dashboard_app.py
```

The dashboard displays the saved UK ETS, Hormuz, Critical Minerals, Sanctions Trade Finance and Cyber Business Interruption showcase outputs. It does not call Tavily or spend search credits.

## Clean Export

Create a shareable project zip without local secrets, virtual environments, git metadata, generated `outputs/` files or local caches:

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

- Add non-interactive CLI arguments for repeatable runs
- Add configurable scoring weights by domain pack
- Add stronger source freshness checks by category
- Add richer domain packs for additional business users
