# Task Brief: Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers

## Objective

Create a third showcase case brief for the Political Risk Agent focused on production-continuity risk from rare earth magnet and critical-mineral supply disruption affecting a UK advanced manufacturer. This task brief defines the case framing, source requirements, decision logic and acceptance criteria only. It does not generate the case, retrieve live evidence or change the dashboard yet.

## Current status

The project already demonstrates two saved showcase paths:
- UK ETS maritime carbon-cost exposure for shipping operators
- Hormuz route decision logic for shipping operators

The framework now needs a non-shipping, non-carbon, non-route-risk case that proves it can convert strategic competition, export controls and supplier concentration into a decision-grade production-continuity output for a UK-based industrial client type.

No live retrieval should be run for this task brief. No saved showcase artefacts should be changed.

## Business decision

Core business question:

Can a UK advanced manufacturer keep production running if export controls disrupt access to rare earth magnets or critical-mineral inputs?

Decision framing for implementation:

The case should model a UK manufacturer that depends on permanent rare earth magnets or magnet-dependent subcomponents for production-critical applications such as motors, actuators, sensors, robotics, defence-adjacent assemblies, aerospace systems, medical equipment or high-performance industrial machinery. The decision is not whether critical minerals matter in general. The decision is whether a UK operator should keep running with the current sourcing model, build inventory, qualify an alternative supplier, redesign the input, allocate scarce supply to priority customers or move a product line toward production hold.

Practical users:
- Supply Chain Director
- Procurement Lead
- Risk Manager
- CFO

Decision options the case should support:
- continue with current supplier base
- stockpile
- qualify alternative supplier
- redesign input
- allocate scarce inventory to priority customers
- production hold

The output must connect evidence to those decisions. It should not become a generic report saying critical minerals are strategically important.

## In scope

- A UK-based client-type brief for an advanced manufacturer exposed to global rare earth magnet / critical-mineral supply chains
- A rare-earth-magnet-specific continuity case rather than a broad basket-of-minerals report
- A production-continuity framing rather than a geopolitical summary
- UK relevance through policy, industrial exposure and resilience planning
- Global supply-chain risk through export controls, supplier concentration, shortage signals and substitution constraints
- A quantified continuity model built around:
  - production continuity gap = alternative supplier qualification time - inventory runway
- A practical operator logic that distinguishes:
  - immediate supply interruption risk
  - qualification lag risk
  - substitution feasibility
  - customer delivery criticality
  - revenue-at-risk prioritisation
- Clearly labelled scenario inputs:
  - inventory runway: 45 days
  - alternative supplier qualification time: 180 days
  - China-linked supply share: 70%
  - exposed product-line revenue: illustrative £50m
  - substitution difficulty: high
  - customer delivery criticality: high
- Clear labels for each input:
  - source-supported
  - illustrative
  - user/company-provided
  - derived
- A decision-first brief structure that later fits a dashboard view for:
  - exposure summary
  - production continuity gap
  - supplier concentration
  - mitigation options
  - evidence and source audit

## Out of scope

- Do not generate the case yet
- Do not call Tavily
- Do not run `live_search_mode`
- Do not edit `dashboard_app.py`
- Do not change source retrieval logic
- Do not change the UK ETS showcase output
- Do not change the Hormuz showcase output
- Do not change the sanctions showcase
- Do not add broad framework features
- Do not claim company-specific precision without company data
- Do not present illustrative scenario values as factual company estimates
- Do not let the case drift into a general strategic-minerals explainer with no production decision
- Do not imply that export-control news alone proves the manufacturer must halt production without inventory, qualification and substitution analysis

## Source requirements

Required source coverage:
- UK official critical minerals policy source
- UK official trade, industrial strategy or resilience source relevant to manufacturing continuity
- global export-control / live reporting source
- rare earth / magnet supply concentration evidence
- UK industry exposure evidence
- specialist export-control interpretation
- market/pricing or shortage signal
- substitution / alternative supplier feasibility evidence
- contrary/easing evidence
- input classification / product-scope evidence showing which magnet or mineral inputs are actually affected

Required source roles:
- official_anchor
- data_or_indicator_source
- specialist_interpretation
- operator_or_industry_guidance
- market_pricing
- live_event_reporting
- contrary_scope_limit

Preferred source targets:
- GOV.UK Critical Minerals Strategy / Vision 2035
- Department for Business and Trade / UK critical-import or industrial-resilience material where relevant
- British Geological Survey
- UK Parliament / committee sources
- OECD critical raw materials export restrictions
- USGS mineral commodity evidence
- IEA critical minerals data
- CSIS / RUSI / CSS ETH Zurich
- Reuters / AP for live export-control developments
- High Value Manufacturing Catapult for UK industry exposure
- reputable legal/export-control analysis where needed
- magnet-industry, motor-manufacturing or advanced-manufacturing sources where they help distinguish substitution difficulty from generic commodity risk

Core decision questions the future source plan should answer:
- Can the manufacturer continue production with the current supplier base if export-control disruption intensifies?
- Which exact input is controlled or concentration-exposed: finished rare earth magnet, oxide, alloy, sintered component or magnet-dependent subassembly?
- How concentrated is supply for the relevant magnet or critical-mineral input, and how much of that concentration is China-linked?
- What live export-control, licensing or trade-restriction developments could interrupt procurement?
- What is the manufacturer's production runway once current inventory, inbound shipments and qualification lag are compared?
- Can the input be substituted, redesigned or dual-sourced within a commercially useful timeframe?
- How long can production continue based on inventory runway versus alternative supplier qualification time?
- Which mitigation action is currently preferred: stockpile, qualify alternative supplier, redesign input, allocate inventory or production hold?
- What evidence would justify relaxing a high-control stance back to normal procurement?

## Output requirements

The future brief should include:
- Decision Recommendation
- Scope and Specificity
- Dashboard Summary
- Exposure Summary
- Controlled Input Assessment
- Supplier Concentration Assessment
- Production Continuity Model
- Inventory Runway vs Supplier Qualification Gap
- Mitigation Options
- Risk Scorecard
- Evidence-To-Score Bridge
- Source Requirement Coverage
- Evidence Appendix
- Source Audit Summary
- Methodology and Review Controls

The future output should demonstrate:
- a UK manufacturer lens with global supply-chain exposure
- a named controlled-input logic so the reader understands whether the case is about NdFeB magnets, dysprosium exposure, oxide dependence, or a comparable rare-earth magnet bottleneck
- production-continuity decision logic rather than policy summary
- explicit separation between public/live evidence, illustrative assumptions and derived outputs
- anti-overclaiming discipline when company-specific supplier, inventory, BOM or contract data is missing
- decision-grade actions tied to business users:
  - stockpile
  - qualify alternative supplier
  - redesign input
  - allocate scarce inventory
  - production hold

The quantified model should foreground:
- inventory runway
- qualification lag
- continuity gap
- concentration risk
- substitution difficulty
- exposed revenue at risk as an illustrative scenario only
- a clear stance on what is source-supported versus illustrative versus company-required

The future Evidence-To-Score Bridge should explicitly connect:
- likelihood to export-control direction, concentration and source-supported disruption risk
- impact to production criticality, revenue exposure, substitution difficulty and qualification lag
- immediacy to inventory runway versus alternative qualification gap
- confidence to whether company BOM, inventory, supplier and contract data are missing

The future review controls should explicitly require:
- BOM / controlled-input verification
- supplier-country and processing-chain verification
- inventory and open purchase-order validation
- qualification timeline validation from engineering / quality teams
- customer-priority and contract-penalty review before allocation or hold decisions

## Files likely to change

When the case is eventually implemented, likely files include:
- `config/domain_packs.json`
- `agent/source_requirements.py`
- `agent/brief_generator.py`
- `agent/source_audit.py`
- `agent/risk_scoring.py`
- `agent/review_flags.py`
- `showcase/critical_minerals_uk_advanced_manufacturer_brief.md`
- `showcase/critical_minerals_uk_advanced_manufacturer_source_audit.md`
- `showcase/critical_minerals_uk_advanced_manufacturer_evidence_pack.json`
- `tests/...` for case-specific scoring, structure and quality checks
- later, dashboard files only when explicitly requested

This task itself should change only:
- `docs/tasks/CRITICAL_MINERALS_UK_ADVANCED_MANUFACTURER.md`

## Do not change

- `dashboard_app.py`
- UK ETS saved showcase files
- Hormuz saved showcase files
- sanctions saved showcase files
- live source retrieval logic
- Tavily/search provider wiring
- broad framework architecture

## Verification commands

Run:

```bash
python3 -m unittest discover tests
python3 scripts/quality_check.py
```

## Acceptance criteria

- task brief is complete
- case title is: `Critical Minerals Exposure Engine: Rare Earth Magnet Supply Risk for UK Advanced Manufacturers`
- client type is a UK advanced manufacturer
- practical users are clear
- business decision is framed around production continuity
- source requirements and source roles are explicit
- UK relevance is explicit and not just implied
- rare earth magnet specificity is explicit enough to avoid a generic critical-minerals case
- the production continuity gap logic is tied to decisions rather than presented as an abstract metric
- anti-overclaiming controls are explicit about missing BOM, inventory, supplier and contract data
- dashboard potential is clear through named sections and quantified outputs
- output requirements are explicit and decision-first
- illustrative scenario inputs are defined and clearly labelled as non-company-specific
- dashboard concept is noted for a later third case
- no live sources are called
- no dashboard changes are made yet
- no existing showcase outputs are changed
- tests pass
- quality check passes
