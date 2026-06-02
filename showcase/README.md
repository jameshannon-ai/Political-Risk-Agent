# Showcase Cases

These saved artefacts are the dashboard inputs. They preserve the brief, source audit and structured evidence pack for each showcase without requiring a live source run.

| Case | Client type | Brief path | Source audit path | Evidence pack path | Evidence mode | Confidence score | Dashboard status |
|---|---|---|---|---|---|---|---|
| UK ETS Maritime Expansion | UK shipping operator | `showcase/uk_ets_shipping_operator_brief.md` | `showcase/uk_ets_source_audit.md` | `showcase/uk_ets_evidence_pack.json` | saved Tavily-backed showcase | 4/5 | included |
| Hormuz Route Decision Engine | shipping operator | `showcase/hormuz_shipping_operator_brief.md` | `showcase/hormuz_source_audit.md` | `showcase/hormuz_evidence_pack.json` | saved Tavily-backed showcase | 3/5 | included |
| Critical Minerals Exposure Engine | UK advanced manufacturer | `showcase/critical_minerals_advanced_manufacturer_brief.md` | `showcase/critical_minerals_source_audit.md` | `showcase/critical_minerals_evidence_pack.json` | saved Tavily-backed showcase | 3/5 | included |
| Sanctions End-Use Controls | trade finance lender | `showcase/sanctions_trade_finance_sample.md` | `showcase/sanctions_source_audit.md` | `showcase/sanctions_evidence_pack.json` | curated fallback showcase | 4/5 | not currently included |

## What To Review

- Briefs show the client decision, scorecard, evidence-to-score bridge, assumptions and recommended actions.
- Source audits show the research plan, source strategy, selected/rejected sources, coverage gaps and refresh priorities.
- Evidence packs preserve machine-readable source requirements, extracted claims, quantified facts, confidence caps and metadata.

The Streamlit dashboard reads these saved files only. It does not call Tavily or spend live-search credits.
