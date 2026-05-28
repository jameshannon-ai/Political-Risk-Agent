# Project Summary

## Product Summary

Political Risk Agent is a source-audited workflow for turning political, geopolitical and regulatory disruption into commercial risk briefs. It separates reusable intelligence functions, such as source strategy, ranking, evidence extraction, confidence scoring and audit controls, from domain-specific report templates and exposure maps. The flagship showcase applies the engine to Strait of Hormuz disruption for a marine insurer, but the same structure can support sanctions, election, civil unrest, supply-chain and regulatory-change cases.

## Personal Positioning Notes

### CV Bullet

- Built a Python CLI political risk intelligence agent that performs source strategy, source ranking, evidence extraction, source audit, risk scoring and markdown brief generation, with a Strait of Hormuz marine-insurance showcase.

### Interview Explanation

This project is designed like an analyst workflow inside a company, not a one-off summariser. The reusable engine handles intake, source triage, evidence extraction, confidence assessment, review flags and report generation, while the domain layer controls source categories, exposure maps and report structure. The Hormuz case demonstrates how official, carrier, energy, insurance, vessel-flow, news and specialist evidence can be turned into practical underwriting judgements.

### Demo Talking Points

- The source audit shows selected and rejected sources, ranking rationale, category coverage and review controls.
- The brief argues from evidence through commercial relevance to action.
- Fallback mode makes the demo reliable without API keys, while Tavily/SerpAPI support keeps the live path realistic.
- Domain packs show how the same engine can be reused beyond maritime risk.

### Future Roadmap

- Add non-interactive CLI arguments for repeatable runs.
- Add source freshness thresholds by domain pack.
- Add configurable scoring weights for domain/business-user combinations.
- Add optional PDF export after the markdown workflow is stable.
